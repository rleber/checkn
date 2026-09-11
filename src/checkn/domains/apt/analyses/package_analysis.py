"""
apt package classification analysis.
"""

from checkn.core.name_analysis import NameAnalysis


class PackageAnalysis(NameAnalysis):
    """
    Determines if the target name is an apt package, distinguishing
    installed from merely published. "Package" works on any OS (it's a
    network fetch of Debian's published index); "installed package" only
    means anything on Linux and is "" everywhere else -- see
    InstalledPackageProbe.required_os.
    """

    title = "package"

    def _analyze(self, name: str) -> str:
        """
        Prefer the local, installed check -- it doesn't need the published
        package list at all, so it's tried first. On a non-Linux system
        it's always "", falling straight through to the published check.
        """
        if self.lab.execute("installed package", name):
            return "installed package"
        if self.lab.execute("package", name):
            return "uninstalled package"
        return ""
