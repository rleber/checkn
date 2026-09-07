"""
test_cache_cli.py

Run tests on the checkn-cache CLI.

Usage: pytest tests/test_cache_cli.py
"""

from datetime import datetime

from typer.testing import CliRunner

from checkn.cache import CacheDB
from checkn.cache_cli import _format_updated_at, app

runner = CliRunner()


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
