"""
test_cache_cli.py

Run tests on the checkn-cache CLI.

Usage: pytest tests/test_cache_cli.py
"""

from datetime import datetime

from typer.testing import CliRunner

from checkn.cache import CacheDB
from checkn.cache_cli import _format_updated_at, app
from checkn.core.cacheable_probe import CacheableNameProbe

runner = CliRunner()


class _FailingProbe(CacheableNameProbe):
    title = "failing"
    domain = "test"

    def _fetch_all(self) -> list[str]:
        return []


def test_format_updated_at_never_loaded():
    assert _format_updated_at(None) == "(never)"


def test_format_updated_at_formats_in_local_time():
    value = "2026-09-07T07:00:08.342621+00:00"
    expected = datetime.fromisoformat(value).astimezone().strftime("%Y-%m-%d %H:%M %Z")
    assert _format_updated_at(value) == expected


def test_path():
    result = runner.invoke(app, ["path"])
    assert result.exit_code == 0
    assert str(CacheDB().path) in result.stdout


def test_status_reports_nothing_loaded_after_clear():
    runner.invoke(app, ["clear"])
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "No cache sections loaded." in result.stdout


def test_reload_no_matching_domain():
    result = runner.invoke(app, ["reload", "-d", "not-a-real-domain"])
    assert result.exit_code == 1
    assert "No cacheable probes match." in result.stdout


def test_build_exits_nonzero_when_a_probe_fails(monkeypatch):
    monkeypatch.setattr("checkn.cache_cli._cacheable_probes", lambda domains: [_FailingProbe()])
    result = runner.invoke(app, ["build"])
    assert result.exit_code == 1
    assert "0 entries" in result.stderr
    CacheDB().clear("test")


def test_reload_exits_nonzero_when_a_probe_fails(monkeypatch):
    monkeypatch.setattr("checkn.cache_cli._cacheable_probes", lambda domains: [_FailingProbe()])
    result = runner.invoke(app, ["reload"])
    assert result.exit_code == 1
    assert "0 entries" in result.stderr
    CacheDB().clear("test")


def test_status_highlights_failed_reload(monkeypatch):
    monkeypatch.setattr("checkn.cache_cli._cacheable_probes", lambda domains: [_FailingProbe()])
    runner.invoke(app, ["build"])

    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "status" in result.stdout
    assert "reload failed" in result.stdout

    # warning banner comes after the table, not before
    banner = "warning: 1 probe(s) have a failed reload pending: test failing"
    assert banner in result.stdout
    assert result.stdout.index(banner) > result.stdout.index("reload failed")

    CacheDB().clear("test")


def test_status_column_always_present_and_shows_okay_when_nothing_failed():
    runner.invoke(app, ["clear"])
    CacheDB().replace_name_set("test", "ok", ["a"])

    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "status" in result.stdout
    assert "okay" in result.stdout
    assert "warning:" not in result.stdout

    CacheDB().clear("test")


def test_reload_status_contains_and_clear_python():
    runner.invoke(app, ["clear", "-d", "python"])

    reload_result = runner.invoke(app, ["reload", "-d", "python"])
    assert reload_result.exit_code == 0
    assert "python: pypi module" in reload_result.stdout

    cache = CacheDB()
    assert cache.is_loaded("python", "pypi module")
    assert cache.contains("python", "pypi module", "requests")

    status_result = runner.invoke(app, ["status", "-d", "python"])
    assert status_result.exit_code == 0
    assert "pypi module" in status_result.stdout

    clear_result = runner.invoke(app, ["clear", "-d", "python"])
    assert clear_result.exit_code == 0
    assert not cache.is_loaded("python", "pypi module")
