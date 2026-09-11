"""
test_cache.py

Run tests on CacheDB

Usage: pytest tests/test_cache.py
"""

import sqlite3
from pathlib import Path

from checkn.cache import (
    SKIP_KIND_NETWORK_UNAVAILABLE,
    SKIP_KIND_NOT_APPLICABLE,
    CacheDB,
)


def new_cache(tmp_path: Path) -> CacheDB:
    return CacheDB(path=tmp_path / "cache.db")


def test_not_loaded_initially(tmp_path):
    cache = new_cache(tmp_path)
    assert cache.is_loaded("python", "pypi module") is False
    assert cache.contains("python", "pypi module", "requests") is False


def test_replace_name_set_populates_and_marks_loaded(tmp_path):
    cache = new_cache(tmp_path)
    cache.replace_name_set("python", "pypi module", ["requests", "flask"])

    assert cache.is_loaded("python", "pypi module") is True
    assert cache.contains("python", "pypi module", "requests") is True
    assert cache.contains("python", "pypi module", "flask") is True
    assert cache.contains("python", "pypi module", "nonexistent") is False


def test_replace_name_set_overwrites_previous_contents(tmp_path):
    cache = new_cache(tmp_path)
    cache.replace_name_set("python", "pypi module", ["requests"])
    cache.replace_name_set("python", "pypi module", ["flask"])

    assert cache.contains("python", "pypi module", "requests") is False
    assert cache.contains("python", "pypi module", "flask") is True


def test_status_reports_entry_count_and_timestamp(tmp_path):
    cache = new_cache(tmp_path)
    cache.replace_name_set("python", "pypi module", ["requests", "flask", "click"])

    rows = cache.status("python")
    assert len(rows) == 1
    assert rows[0].domain == "python"
    assert rows[0].probe == "pypi module"
    assert rows[0].entry_count == 3
    assert rows[0].updated_at is not None


def test_status_empty_when_nothing_loaded(tmp_path):
    cache = new_cache(tmp_path)
    assert cache.status() == []


def test_mark_failed_records_failure_without_prior_data(tmp_path):
    cache = new_cache(tmp_path)
    cache.mark_failed("python", "pypi module")

    rows = cache.status("python")
    assert len(rows) == 1
    assert rows[0].last_failed_at is not None
    assert rows[0].updated_at is None
    assert rows[0].entry_count == 0
    assert cache.is_loaded("python", "pypi module") is False


def test_mark_failed_preserves_existing_data(tmp_path):
    cache = new_cache(tmp_path)
    cache.replace_name_set("python", "pypi module", ["requests", "flask"])

    cache.mark_failed("python", "pypi module")

    rows = cache.status("python")
    assert rows[0].last_failed_at is not None
    assert rows[0].entry_count == 2
    assert cache.contains("python", "pypi module", "requests") is True


def test_replace_name_set_clears_prior_failure(tmp_path):
    cache = new_cache(tmp_path)
    cache.mark_failed("python", "pypi module")

    cache.replace_name_set("python", "pypi module", ["requests"])

    rows = cache.status("python")
    assert rows[0].last_failed_at is None


def test_mark_not_applicable_records_reason_without_prior_data(tmp_path):
    cache = new_cache(tmp_path)
    cache.mark_not_applicable(
        "apt", "apt package", "requires linux, this system is macos"
    )

    rows = cache.status("apt")
    assert len(rows) == 1
    assert rows[0].last_failed_at is not None
    assert rows[0].skip_reason == "requires linux, this system is macos"
    assert rows[0].skip_kind == SKIP_KIND_NOT_APPLICABLE
    assert rows[0].updated_at is None
    assert rows[0].entry_count == 0
    assert cache.is_loaded("apt", "apt package") is False


def test_mark_not_applicable_preserves_existing_data(tmp_path):
    cache = new_cache(tmp_path)
    cache.replace_name_set("apt", "apt package", ["curl", "git"])

    cache.mark_not_applicable("apt", "apt package", "requires linux")

    rows = cache.status("apt")
    assert rows[0].skip_reason == "requires linux"
    assert rows[0].entry_count == 2
    assert cache.contains("apt", "apt package", "curl") is True


def test_mark_failed_clears_prior_not_applicable(tmp_path):
    cache = new_cache(tmp_path)
    cache.mark_not_applicable("apt", "apt package", "requires linux")

    cache.mark_failed("apt", "apt package")

    rows = cache.status("apt")
    assert rows[0].last_failed_at is not None
    assert rows[0].skip_reason is None


def test_mark_not_applicable_clears_prior_failure_reason_state(tmp_path):
    cache = new_cache(tmp_path)
    cache.mark_failed("apt", "apt package")

    cache.mark_not_applicable("apt", "apt package", "requires linux")

    rows = cache.status("apt")
    assert rows[0].skip_reason == "requires linux"


def test_replace_name_set_clears_prior_not_applicable(tmp_path):
    cache = new_cache(tmp_path)
    cache.mark_not_applicable("apt", "apt package", "requires linux")

    cache.replace_name_set("apt", "apt package", ["curl"])

    rows = cache.status("apt")
    assert rows[0].last_failed_at is None
    assert rows[0].skip_reason is None


def test_mark_network_unavailable_records_reason_without_prior_data(tmp_path):
    cache = new_cache(tmp_path)
    cache.mark_network_unavailable("apt", "package", "Connection refused")

    rows = cache.status("apt")
    assert len(rows) == 1
    assert rows[0].last_failed_at is not None
    assert rows[0].skip_reason == "Connection refused"
    assert rows[0].skip_kind == SKIP_KIND_NETWORK_UNAVAILABLE
    assert rows[0].updated_at is None
    assert rows[0].entry_count == 0
    assert cache.is_loaded("apt", "package") is False


def test_mark_network_unavailable_preserves_existing_data(tmp_path):
    cache = new_cache(tmp_path)
    cache.replace_name_set("apt", "package", ["curl", "git"])

    cache.mark_network_unavailable("apt", "package", "Connection refused")

    rows = cache.status("apt")
    assert rows[0].skip_kind == SKIP_KIND_NETWORK_UNAVAILABLE
    assert rows[0].entry_count == 2
    assert cache.contains("apt", "package", "curl") is True


def test_mark_failed_clears_prior_network_unavailable(tmp_path):
    cache = new_cache(tmp_path)
    cache.mark_network_unavailable("apt", "package", "Connection refused")

    cache.mark_failed("apt", "package")

    rows = cache.status("apt")
    assert rows[0].skip_reason is None
    assert rows[0].skip_kind is None


def test_replace_name_set_clears_prior_network_unavailable(tmp_path):
    cache = new_cache(tmp_path)
    cache.mark_network_unavailable("apt", "package", "Connection refused")

    cache.replace_name_set("apt", "package", ["curl"])

    rows = cache.status("apt")
    assert rows[0].last_failed_at is None
    assert rows[0].skip_kind is None


def test_ensure_schema_migrates_older_cache_status_table(tmp_path):
    """
    A cache db created before skip_kind existed has a cache_status table
    with only the original 6 columns. CacheDB must add the column on open
    rather than relying on CREATE TABLE IF NOT EXISTS, which is a no-op
    against a table that already exists. A pre-existing not-applicable row
    (skip_reason set, from before skip_kind existed to record it as such)
    is backfilled as SKIP_KIND_NOT_APPLICABLE rather than being left to
    read as a genuine failure -- network-unavailable didn't exist as a
    concept yet, so skip_reason could only ever have come from there.
    """
    db_path = tmp_path / "old_cache.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE cache_status (
                domain TEXT NOT NULL,
                probe TEXT NOT NULL,
                updated_at TEXT,
                entry_count INTEGER NOT NULL DEFAULT 0,
                last_failed_at TEXT,
                skip_reason TEXT,
                PRIMARY KEY (domain, probe)
            )
            """
        )
        conn.execute(
            "INSERT INTO cache_status (domain, probe, updated_at, entry_count) "
            "VALUES ('python', 'pypi module', '2026-01-01T00:00:00+00:00', 5)"
        )
        conn.execute(
            "INSERT INTO cache_status (domain, probe, last_failed_at, skip_reason) "
            "VALUES ('apt', 'installed package', '2026-01-01T00:00:00+00:00', "
            "'requires linux, this system is macos')"
        )

    cache = CacheDB(path=db_path)

    rows = cache.status("python")
    assert len(rows) == 1
    assert rows[0].entry_count == 5
    assert rows[0].skip_kind is None

    migrated_row = cache.status("apt")[0]
    assert migrated_row.skip_kind == SKIP_KIND_NOT_APPLICABLE

    cache.mark_network_unavailable("apt", "package", "no route to host")
    rows_after = {row.probe: row for row in cache.status("apt")}
    assert rows_after["package"].skip_kind == SKIP_KIND_NETWORK_UNAVAILABLE
    assert rows_after["installed package"].skip_kind == SKIP_KIND_NOT_APPLICABLE


def test_ensure_schema_backfills_even_if_column_already_exists_unbackfilled(tmp_path):
    """
    A db that already has the skip_kind column, but with an unbackfilled
    row left over from an earlier version of this migration (added the
    column but didn't backfill it) -- rather than the "column missing"
    branch, which won't fire a second time -- must still get backfilled.
    """
    db_path = tmp_path / "half_migrated.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE cache_status (
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
        conn.execute(
            "INSERT INTO cache_status (domain, probe, last_failed_at, skip_reason) "
            "VALUES ('apt', 'installed package', '2026-01-01T00:00:00+00:00', "
            "'requires linux, this system is macos')"
        )

    cache = CacheDB(path=db_path)

    assert cache.status("apt")[0].skip_kind == SKIP_KIND_NOT_APPLICABLE


def test_clear_domain_scoped(tmp_path):
    cache = new_cache(tmp_path)
    cache.replace_name_set("python", "pypi module", ["requests"])
    cache.replace_name_set("ruby", "gem", ["rails"])

    cache.clear("python")

    assert cache.is_loaded("python", "pypi module") is False
    assert cache.is_loaded("ruby", "gem") is True


def test_clear_all_domains(tmp_path):
    cache = new_cache(tmp_path)
    cache.replace_name_set("python", "pypi module", ["requests"])
    cache.replace_name_set("ruby", "gem", ["rails"])

    cache.clear()

    assert cache.status() == []
