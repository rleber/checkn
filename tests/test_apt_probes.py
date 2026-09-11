"""
test_apt_probes.py

Run tests on PackageProbe and InstalledPackageProbe's fetch/parse logic
and OS gating. Neither apt/dpkg nor the real Debian dump are hit for
real -- run_command and requests.get are mocked -- see
test_homebrew_domain.py / test_ruby_domain.py for the contrasting style
used where the real tool is actually installed.

Usage: pytest tests/test_apt_probes.py
"""

import subprocess

from checkn.domains.apt.probes.installed_package_probe import InstalledPackageProbe
from checkn.domains.apt.probes.package_probe import PackageProbe
from checkn.utils import os_support


def _completed(stdout: str, returncode: int = 0) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=[], returncode=returncode, stdout=stdout, stderr=""
    )


class _FakeResponse:
    def __init__(self, text: str) -> None:
        self.text = text

    def raise_for_status(self) -> None:
        pass


def _fake_allpackages_dump(*names: str) -> _FakeResponse:
    """
    Build a dump shaped like packages.debian.org's real
    allpackages?format=txt.gz *after* requests has auto-decoded its
    Content-Encoding: x-gzip response (see package_probe.py) -- header/
    copyright lines followed by "name (version) description" entries.
    """
    header = (
        'All Debian Packages in "stable"\n\nGenerated: Fri Sep 11 00:00:00 2026 UTC\n\n'
    )
    body = "\n".join(f"{name} (1.0-1) a fake package for testing" for name in names)
    return _FakeResponse(header + body)


def test_package_probe_has_no_os_restriction():
    """
    Unlike installed-package, published package existence is fetched over
    the network -- it doesn't need apt/dpkg, so it should work on any OS.
    """
    assert PackageProbe.required_os is None


def test_installed_package_probe_is_linux_only():
    assert InstalledPackageProbe.required_os == os_support.LINUX


def test_package_probe_parses_allpackages_dump(monkeypatch):
    import checkn.domains.apt.probes.package_probe as module

    monkeypatch.setattr(
        module.requests,
        "get",
        lambda url: _fake_allpackages_dump("bash", "curl", "vim"),
    )
    assert PackageProbe()._fetch_all() == ["bash", "curl", "vim"]


def test_package_probe_skips_header_and_copyright_lines(monkeypatch):
    import checkn.domains.apt.probes.package_probe as module

    monkeypatch.setattr(
        module.requests, "get", lambda url: _fake_allpackages_dump("bash")
    )
    assert PackageProbe()._fetch_all() == ["bash"]


def test_package_probe_dedupes_names_repeated_across_components(monkeypatch):
    """
    The real dump lists a name once per component it's published in (e.g.
    both "main" and "contrib"), so the same package name can appear on
    multiple lines -- verified directly against the live endpoint, where
    ~790 of ~150k names repeat this way.
    """
    import checkn.domains.apt.probes.package_probe as module

    monkeypatch.setattr(
        module.requests,
        "get",
        lambda url: _fake_allpackages_dump("bash", "bash", "vim"),
    )
    assert PackageProbe()._fetch_all() == ["bash", "vim"]


def test_package_probe_returns_empty_when_dump_has_no_entries(monkeypatch):
    import checkn.domains.apt.probes.package_probe as module

    monkeypatch.setattr(module.requests, "get", lambda url: _fake_allpackages_dump())
    assert PackageProbe()._fetch_all() == []


def test_installed_package_probe_parses_dpkg_query_output(monkeypatch):
    import checkn.domains.apt.probes.installed_package_probe as module

    monkeypatch.setattr(
        module, "run_command", lambda args: _completed("bash\ncoreutils\n")
    )
    assert InstalledPackageProbe()._fetch_all() == ["bash", "coreutils"]


def test_installed_package_probe_returns_empty_on_failure(monkeypatch):
    import checkn.domains.apt.probes.installed_package_probe as module

    monkeypatch.setattr(
        module, "run_command", lambda args: _completed("", returncode=1)
    )
    assert InstalledPackageProbe()._fetch_all() == []
