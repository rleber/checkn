"""
test_apt_domain.py

Run tests on AptDomain. Real apt/dpkg and the real Debian dump are never
hit -- run_command and requests.get are mocked, and each test forces its
own probe.reload() rather than relying on lazy "reload if not yet loaded"
(the probes are process-wide singletons via NameLab, so a later test can't
otherwise be sure it's seeing its own mocked data rather than a stale
reload from an earlier test). Each test also uses names no other test in
this file checks, since NameAnalysis caches its own result per name on
that same singleton. Contrast with test_homebrew_domain.py, which asserts
against real system state instead of mocking.

Usage: pytest tests/domains/test_apt_domain.py
"""

import subprocess

from checkn.domains.apt.domain import AptDomain
from checkn.domains.apt.probes import installed_package_probe, package_probe
from checkn.utils import os_support


def _completed(stdout: str) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=[], returncode=0, stdout=stdout, stderr="")


class _FakeResponse:
    def __init__(self, text: str) -> None:
        self.text = text

    def raise_for_status(self) -> None:
        pass


def _fake_allpackages_dump(*names: str) -> _FakeResponse:
    """
    Shaped like packages.debian.org's dump *after* requests has already
    auto-decoded its Content-Encoding: x-gzip response -- see
    package_probe.py.
    """
    body = "\n".join(f"{name} (1.0-1) a fake package for testing" for name in names)
    return _FakeResponse(body)


def domain() -> AptDomain:
    return AptDomain()


def test_classifies_names_on_linux(monkeypatch):
    monkeypatch.setattr(os_support, "current_os", lambda: os_support.LINUX)
    monkeypatch.setattr(
        package_probe.requests,
        "get",
        lambda url: _fake_allpackages_dump("linux-bash", "linux-vim"),
    )
    monkeypatch.setattr(
        installed_package_probe, "run_command", lambda args: _completed("linux-bash\n")
    )
    domain().lab.item("package").reload()
    domain().lab.item("installed package").reload()

    assert domain().execute("package", "linux-bash") == "installed package"
    assert domain().execute("package", "linux-vim") == "uninstalled package"
    assert domain().execute("package", "linux-unknown") == ""


def test_published_package_works_without_linux(monkeypatch):
    """
    The published-package check has no dependency on apt/dpkg -- it's a
    plain network fetch of Debian's index -- so it should still classify
    a name on a non-Linux system, where "installed package" is gated off
    entirely by required_os.
    """
    monkeypatch.setattr(os_support, "current_os", lambda: os_support.MACOS)
    monkeypatch.setattr(
        package_probe.requests, "get", lambda url: _fake_allpackages_dump("mac-htop")
    )
    domain().lab.item("package").reload()

    assert domain().execute("package", "mac-htop") == "uninstalled package"
    assert domain().execute("package", "mac-unknown") == ""


def test_installed_package_gated_off_on_non_linux(monkeypatch):
    """
    Directly confirms "installed package" itself returns "" on a
    non-Linux system, even for a name InstalledPackageProbe would
    otherwise have just fetched.
    """
    monkeypatch.setattr(os_support, "current_os", lambda: os_support.LINUX)
    monkeypatch.setattr(
        installed_package_probe, "run_command", lambda args: _completed("gated-pkg\n")
    )
    domain().lab.item("installed package").reload()

    monkeypatch.setattr(os_support, "current_os", lambda: os_support.MACOS)
    assert domain().lab.execute("installed package", "gated-pkg") == ""


def test_singleton():
    assert AptDomain() is AptDomain()
    assert AptDomain().lab is AptDomain().lab
