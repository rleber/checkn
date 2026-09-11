"""
test_os_support.py

Run tests on checkn.utils.os_support.

Usage: pytest tests/test_os_support.py
"""

import checkn.utils.os_support as os_support


def test_current_os_maps_known_platform_system_values(monkeypatch):
    monkeypatch.setattr(os_support.platform, "system", lambda: "Darwin")
    assert os_support.current_os() == os_support.MACOS

    monkeypatch.setattr(os_support.platform, "system", lambda: "Linux")
    assert os_support.current_os() == os_support.LINUX

    monkeypatch.setattr(os_support.platform, "system", lambda: "Windows")
    assert os_support.current_os() == os_support.WINDOWS


def test_current_os_falls_back_to_lowercased_raw_value(monkeypatch):
    monkeypatch.setattr(os_support.platform, "system", lambda: "SomeFutureOS")
    assert os_support.current_os() == "somefutureos"


def test_is_supported_with_no_restriction():
    assert os_support.is_supported(None) is True


def test_is_supported_matches_current_os(monkeypatch):
    monkeypatch.setattr(os_support, "current_os", lambda: os_support.LINUX)
    assert os_support.is_supported(os_support.LINUX) is True
    assert os_support.is_supported(os_support.MACOS) is False
