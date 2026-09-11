"""
test_cacheable_probe.py

Run tests on CacheableNameProbe's reload failure-signaling.

Usage: pytest tests/test_cacheable_probe.py
"""

from pathlib import Path

from checkn.cache import CacheDB
from checkn.core.cacheable_probe import CacheableNameProbe
from checkn.utils import os_support


class _FakeProbe(CacheableNameProbe):
    title = "fake"
    domain = "test"

    def __init__(self, names: list[str]) -> None:
        super().__init__()
        self._names = names
        self.fetch_all_calls = 0

    def _fetch_all(self) -> list[str]:
        self.fetch_all_calls += 1
        return self._names


class _RequiresOtherOsProbe(_FakeProbe):
    title = "fake"
    domain = "test"
    required_os = os_support.LINUX


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


def test_reload_returns_none_and_skips_fetch_when_os_unsupported(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(os_support, "current_os", lambda: os_support.MACOS)
    cache = new_cache(tmp_path)
    probe = _RequiresOtherOsProbe(["a", "b"])

    assert probe.reload(cache) is None
    assert probe.fetch_all_calls == 0
    assert not cache.is_loaded("test", "fake")

    err = capsys.readouterr().err
    assert "not applicable" in err
    assert "requires linux" in err
    assert "this system is macos" in err

    status = cache.status("test")[0]
    assert status.skip_reason is not None
    assert status.last_failed_at is not None


def test_not_applicable_reload_leaves_existing_cache_section_untouched(
    tmp_path, capsys, monkeypatch
):
    cache = new_cache(tmp_path)

    populating_probe = _FakeProbe(["a", "b"])
    populating_probe.title = "fake"
    assert populating_probe.reload(cache) is True

    monkeypatch.setattr(os_support, "current_os", lambda: os_support.MACOS)
    gated_probe = _RequiresOtherOsProbe([])
    assert gated_probe.reload(cache) is None

    assert cache.is_loaded("test", "fake")
    assert cache.contains("test", "fake", "a")
    assert cache.contains("test", "fake", "b")


def test_run_returns_empty_without_calling_fetch_when_os_unsupported(monkeypatch):
    monkeypatch.setattr(os_support, "current_os", lambda: os_support.MACOS)
    probe = _RequiresOtherOsProbe(["a"])
    assert probe.run("a") == ""
    assert probe.fetch_all_calls == 0
