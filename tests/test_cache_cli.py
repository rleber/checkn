"""
test_cache_cli.py

Run tests on the checkn-cache CLI.

Usage: pytest tests/test_cache_cli.py
"""

from typer.testing import CliRunner

from checkn.cache import CacheDB
from checkn.cache_cli import app

runner = CliRunner()


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
    assert "No cacheable tests match." in result.stdout


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
