"""
test_cache.py

Run tests on CacheDB

Usage: pytest tests/test_cache.py
"""

from pathlib import Path

from checkn.cache import CacheDB


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
    assert rows[0].test == "pypi module"
    assert rows[0].entry_count == 3
    assert rows[0].updated_at is not None


def test_status_empty_when_nothing_loaded(tmp_path):
    cache = new_cache(tmp_path)
    assert cache.status() == []


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
