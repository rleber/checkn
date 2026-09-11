"""
test_cacheable_probe.py

Run tests on CacheableNameProbe's reload failure-signaling.

Usage: pytest tests/test_cacheable_probe.py
"""

from pathlib import Path

import requests

from checkn.cache import SKIP_KIND_NETWORK_UNAVAILABLE, CacheDB
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


class _RaisingProbe(CacheableNameProbe):
    title = "fake"
    domain = "test"

    def __init__(self, exc: BaseException) -> None:
        super().__init__()
        self._exc = exc
        self.fetch_all_calls = 0

    def _fetch_all(self) -> list[str]:
        self.fetch_all_calls += 1
        raise self._exc


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


def test_reload_returns_none_and_skips_fetch_when_os_unsupported(
    tmp_path, capsys, monkeypatch
):
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


def test_reload_returns_none_and_warns_on_connection_error(tmp_path, capsys):
    cache = new_cache(tmp_path)
    probe = _RaisingProbe(requests.exceptions.ConnectionError("no route to host"))

    assert probe.reload(cache) is None
    assert probe.fetch_all_calls == 1
    assert not cache.is_loaded("test", "fake")

    err = capsys.readouterr().err
    assert "network unavailable" in err
    assert "no route to host" in err

    status = cache.status("test")[0]
    assert status.skip_kind == SKIP_KIND_NETWORK_UNAVAILABLE
    assert status.last_failed_at is not None


def test_reload_returns_none_and_warns_on_timeout(tmp_path, capsys):
    cache = new_cache(tmp_path)
    probe = _RaisingProbe(requests.exceptions.Timeout("timed out"))

    assert probe.reload(cache) is None
    status = cache.status("test")[0]
    assert status.skip_kind == SKIP_KIND_NETWORK_UNAVAILABLE
    assert "network unavailable" in capsys.readouterr().err


def test_network_unavailable_reload_leaves_existing_cache_section_untouched(
    tmp_path, capsys
):
    cache = new_cache(tmp_path)

    populating_probe = _FakeProbe(["a", "b"])
    assert populating_probe.reload(cache) is True

    offline_probe = _RaisingProbe(
        requests.exceptions.ConnectionError("no route to host")
    )
    assert offline_probe.reload(cache) is None

    assert cache.is_loaded("test", "fake")
    assert cache.contains("test", "fake", "a")
    assert cache.contains("test", "fake", "b")


def test_network_unavailable_does_not_retry_within_one_reload(tmp_path):
    cache = new_cache(tmp_path)
    probe = _RaisingProbe(requests.exceptions.ConnectionError("no route to host"))

    probe.reload(cache)

    assert probe.fetch_all_calls == 1


def test_reload_returns_false_and_warns_on_unexpected_fetch_error(tmp_path, capsys):
    """
    A non-connectivity error (e.g. a bug, or an HTTP error status) from
    _fetch_all() shouldn't be treated as "network unavailable" -- but it
    also shouldn't propagate and abort every other probe's reload in the
    same run, so it's handled the same way an empty fetch already is.
    """
    cache = new_cache(tmp_path)
    probe = _RaisingProbe(ValueError("malformed response"))

    assert probe.reload(cache) is False
    assert not cache.is_loaded("test", "fake")

    err = capsys.readouterr().err
    assert "malformed response" in err

    status = cache.status("test")[0]
    assert status.skip_kind is None
    assert status.last_failed_at is not None
