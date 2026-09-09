"""
test_homebrew_api_cache.py

Run tests on checkn.domains.homebrew.api_cache.

Usage: pytest tests/test_homebrew_api_cache.py
"""

from checkn.domains.homebrew.api_cache import read_names


def test_read_names_missing_file(tmp_path, capsys):
    missing = tmp_path / "does_not_exist.txt"
    assert read_names(missing, "formula") == []
    assert "missing" in capsys.readouterr().err


def test_read_names_too_small_looks_malformed(tmp_path, capsys):
    small_file = tmp_path / "formula_names.txt"
    small_file.write_text("only\na\nfew\nlines\n")
    assert read_names(small_file, "formula") == []
    assert "truncated or malformed" in capsys.readouterr().err


def test_read_names_valid_file(tmp_path):
    valid_file = tmp_path / "formula_names.txt"
    valid_file.write_text("\n".join(f"pkg{i}" for i in range(200)))
    names = read_names(valid_file, "formula")
    assert len(names) == 200
    assert "pkg0" in names
