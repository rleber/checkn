"""
test_npm_module_probe.py

Run tests on NpmModuleProbe's live-lookup and network-failure handling.

Usage: pytest tests/test_npm_module_probe.py
"""

import requests

from checkn.domains.javascript.probes.npm_module_probe import NpmModuleProbe


class _FakeResponse:
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code


def test_run_returns_name_when_registry_has_it(monkeypatch):
    monkeypatch.setattr(requests, "head", lambda url, timeout: _FakeResponse(200))
    assert NpmModuleProbe().run("express") == "express"


def test_run_returns_empty_when_registry_lacks_it(monkeypatch):
    monkeypatch.setattr(requests, "head", lambda url, timeout: _FakeResponse(404))
    assert NpmModuleProbe().run("nonexistent-package") == ""


def test_run_returns_empty_and_warns_on_network_error(monkeypatch, capsys):
    def raise_error(url, timeout):
        raise requests.ConnectionError("boom")

    monkeypatch.setattr(requests, "head", raise_error)
    assert NpmModuleProbe().run("express") == ""
    assert "warning" in capsys.readouterr().err
