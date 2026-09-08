"""
test_cacheable_probe.py

Run tests on CacheableNameProbe's reload failure-signaling.

Usage: pytest tests/test_cacheable_probe.py
"""

from pathlib import Path

from checkn.cache import CacheDB
from checkn.core.cacheable_probe import CacheableNameProbe


class _FakeProbe(CacheableNameProbe):
    title = "fake"
    domain = "test"

    def __init__(self, names: list[str]) -> None:
        super().__init__()
        self._names = names

    def _fetch_all(self) -> list[str]:
        return self._names


def new_cache(tmp_path: Path) -> CacheDB:
    return CacheDB(path=tmp_path / "cache.db")


def test_reload_returns_true_on_real_data(tmp_path):
    cache = new_cache(tmp_path)
    probe = _FakeProbe(["a", "b"])
    assert probe.reload(cache) is True
    assert cache.contains("test", "fake", "a")


def test_reload_returns_false_and_warns_on_empty(tmp_path, capsys):
    cache = new_cache(tmp_path)
    probe = _FakeProbe([])
    assert probe.reload(cache) is False
    assert not cache.is_loaded("test", "fake")
    assert "0 entries" in capsys.readouterr().err
    assert cache.status("test")[0].last_failed_at is not None


def test_failed_reload_leaves_existing_cache_section_untouched(tmp_path, capsys):
    cache = new_cache(tmp_path)
    probe = _FakeProbe(["a", "b"])
    assert probe.reload(cache) is True

    probe._names = []
    assert probe.reload(cache) is False

    assert cache.is_loaded("test", "fake")
    assert cache.contains("test", "fake", "a")
    assert cache.contains("test", "fake", "b")
    assert "leaving existing cache section unchanged" in capsys.readouterr().err
    assert cache.status("test")[0].last_failed_at is not None
