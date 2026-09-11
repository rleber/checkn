"""
Persistent sqlite3 cache for bulk NameProbe results.
"""

import os
import sqlite3
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

DEFAULT_CACHE_PATH = Path.home() / ".checkn_cache.db"

# skip_kind values distinguishing *why* a skipped (last_failed_at set,
# skip_reason set) reload isn't a genuine failure to investigate. NULL
# skip_kind (with skip_reason also NULL) means a genuine failure instead
# -- see mark_failed.
SKIP_KIND_NOT_APPLICABLE = "not_applicable"
SKIP_KIND_NETWORK_UNAVAILABLE = "network_unavailable"


def default_cache_path() -> Path:
    """
    Resolve the cache db path, honoring the CHECKN_CACHE_PATH override.
    """
    override = os.environ.get("CHECKN_CACHE_PATH")
    return Path(override) if override else DEFAULT_CACHE_PATH


@dataclass
class CacheStatus:
    """
    One (domain, probe) cache section's status.
    """

    domain: str
    probe: str
    updated_at: str | None
    entry_count: int
    last_failed_at: str | None
    skip_reason: str | None
    skip_kind: str | None


class CacheDB:
    """
    Stores the full name set for each cacheable NameProbe, keyed by
    (domain, probe), plus when each section was last loaded, last failed
    to load, or was last found not applicable on this system.
    """

    def __init__(self, path: Path | None = None) -> None:
        """
        Open (creating if needed) the cache db at path, or the default location.
        """
        self.path = path or default_cache_path()
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        """
        Open a connection to the cache db.
        """
        return sqlite3.connect(self.path)

    def _ensure_schema(self) -> None:
        """
        Create the cache tables if they don't already exist, and migrate
        an older cache_status table (from before skip_kind existed) by
        adding the column -- CREATE TABLE IF NOT EXISTS is a no-op against
        an existing table, so a fresh column has to be added explicitly or
        an already-populated cache db (as any real one now is) would never
        pick it up. Any pre-existing row with a skip_reason is backfilled
        as SKIP_KIND_NOT_APPLICABLE: network-unavailable didn't exist as a
        concept before this column did, so mark_not_applicable was the
        only thing that could have set skip_reason historically.
        """
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cache_status (
                    domain TEXT NOT NULL,
                    probe TEXT NOT NULL,
                    updated_at TEXT,
                    entry_count INTEGER NOT NULL DEFAULT 0,
                    last_failed_at TEXT,
                    skip_reason TEXT,
                    skip_kind TEXT,
                    PRIMARY KEY (domain, probe)
                )
                """
            )
            columns = {
                row[1] for row in conn.execute("PRAGMA table_info(cache_status)")
            }
            if "skip_kind" not in columns:
                conn.execute("ALTER TABLE cache_status ADD COLUMN skip_kind TEXT")
            # Unconditional (not just right after adding the column above):
            # a cache db that already picked up the column from a prior
            # version of this migration, before this backfill existed,
            # would otherwise be stuck with those rows unclassified
            # forever. Matches nothing once every row is properly tagged,
            # so this is a cheap no-op in steady state.
            conn.execute(
                "UPDATE cache_status SET skip_kind = ? "
                "WHERE skip_kind IS NULL AND skip_reason IS NOT NULL",
                (SKIP_KIND_NOT_APPLICABLE,),
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cached_names (
                    domain TEXT NOT NULL,
                    probe TEXT NOT NULL,
                    name TEXT NOT NULL,
                    PRIMARY KEY (domain, probe, name)
                )
                """
            )

    def is_loaded(self, domain: str, probe: str) -> bool:
        """
        Check whether (domain, probe) has ever been loaded into the cache.
        """
        with self._connect() as conn:
            row = conn.execute(
                "SELECT 1 FROM cache_status WHERE domain = ? AND probe = ? AND updated_at IS NOT NULL",
                (domain, probe),
            ).fetchone()
        return row is not None

    def contains(self, domain: str, probe: str, name: str) -> bool:
        """
        Check whether name is present in the cached set for (domain, probe).
        """
        with self._connect() as conn:
            row = conn.execute(
                "SELECT 1 FROM cached_names WHERE domain = ? AND probe = ? AND name = ?",
                (domain, probe, name),
            ).fetchone()
        return row is not None

    def replace_name_set(self, domain: str, probe: str, names: Iterable[str]) -> None:
        """
        Atomically replace the cached name set for (domain, probe), record
        the current UTC time as when it was loaded, and clear any prior
        failure or not-applicable marker recorded for it.
        """
        names = list(names)
        updated_at = datetime.now(UTC).isoformat()
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM cached_names WHERE domain = ? AND probe = ?",
                (domain, probe),
            )
            conn.executemany(
                "INSERT INTO cached_names (domain, probe, name) VALUES (?, ?, ?)",
                [(domain, probe, name) for name in names],
            )
            conn.execute(
                """
                INSERT INTO cache_status
                    (domain, probe, updated_at, entry_count, last_failed_at, skip_reason, skip_kind)
                VALUES (?, ?, ?, ?, NULL, NULL, NULL)
                ON CONFLICT (domain, probe) DO UPDATE SET
                    updated_at = excluded.updated_at,
                    entry_count = excluded.entry_count,
                    last_failed_at = excluded.last_failed_at,
                    skip_reason = excluded.skip_reason,
                    skip_kind = excluded.skip_kind
                """,
                (domain, probe, updated_at, len(names)),
            )

    def mark_failed(self, domain: str, probe: str) -> None:
        """
        Record that the most recent reload attempt for (domain, probe)
        failed, without touching any data already cached for it. Clears
        any stale skip marker (not-applicable or network-unavailable),
        since this is a genuine failure, not a skip.
        """
        failed_at = datetime.now(UTC).isoformat()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO cache_status (domain, probe, last_failed_at, skip_reason, skip_kind)
                VALUES (?, ?, ?, NULL, NULL)
                ON CONFLICT (domain, probe) DO UPDATE SET
                    last_failed_at = excluded.last_failed_at,
                    skip_reason = excluded.skip_reason,
                    skip_kind = excluded.skip_kind
                """,
                (domain, probe, failed_at),
            )

    def mark_not_applicable(self, domain: str, probe: str, reason: str) -> None:
        """
        Record that (domain, probe) was skipped as not applicable on this
        system (e.g. an unmet OS requirement), without touching any data
        already cached for it. Distinct from mark_failed: this isn't a
        problem to investigate, just an expected mismatch that may
        resolve itself if checkn is ever run somewhere else.
        """
        self._mark_skipped(domain, probe, reason, SKIP_KIND_NOT_APPLICABLE)

    def mark_network_unavailable(self, domain: str, probe: str, reason: str) -> None:
        """
        Record that (domain, probe)'s reload couldn't reach the network,
        without touching any data already cached for it. Distinct from
        mark_failed: this isn't a code problem to investigate, just a
        transient condition that the very next reload attempt (e.g.
        tomorrow's scheduled run) may not hit at all.
        """
        self._mark_skipped(domain, probe, reason, SKIP_KIND_NETWORK_UNAVAILABLE)

    def _mark_skipped(
        self, domain: str, probe: str, reason: str, skip_kind: str
    ) -> None:
        """
        Shared implementation for mark_not_applicable/mark_network_unavailable:
        record a skip (as opposed to a genuine failure) reason and kind.
        """
        checked_at = datetime.now(UTC).isoformat()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO cache_status (domain, probe, last_failed_at, skip_reason, skip_kind)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT (domain, probe) DO UPDATE SET
                    last_failed_at = excluded.last_failed_at,
                    skip_reason = excluded.skip_reason,
                    skip_kind = excluded.skip_kind
                """,
                (domain, probe, checked_at, reason, skip_kind),
            )

    def clear(self, domain: str | None = None) -> None:
        """
        Delete cached rows, either for domain or (if omitted) for every domain.
        """
        with self._connect() as conn:
            if domain is None:
                conn.execute("DELETE FROM cached_names")
                conn.execute("DELETE FROM cache_status")
            else:
                conn.execute("DELETE FROM cached_names WHERE domain = ?", (domain,))
                conn.execute("DELETE FROM cache_status WHERE domain = ?", (domain,))

    def status(self, domain: str | None = None) -> list[CacheStatus]:
        """
        Retrieve cache status rows, either for domain or (if omitted) for every domain.
        """
        query = (
            "SELECT domain, probe, updated_at, entry_count, last_failed_at, skip_reason, skip_kind "
            "FROM cache_status"
        )
        params: tuple[str, ...] = ()
        if domain is not None:
            query += " WHERE domain = ?"
            params = (domain,)
        query += " ORDER BY domain, probe"
        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [CacheStatus(*row) for row in rows]
