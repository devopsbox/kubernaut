#!/usr/bin/env python3

import sys
from pathlib import Path
from subprocess import run

PACKAGES = Path(__file__).absolute().parent / "out"


class Uploader(object):
    """
    Upload packages to Bintray.
    """

    def __init__(self, version):
        self.version = version

    def upload_ubuntu(self, release):
        """Upload a .deb for a specific release, e.g. 'xenial'."""
        file_path = PACKAGES / release / "kubernaut_{}_amd64.deb".format(
            self.version
        )
        self._upload(file_path, "kubernaut_shim", "ubuntu/" + release)

    def upload_fedora(self, release):
        """Upload a .rpm for a specific Fedora release, e.g. '25'."""
        file_path = (
            PACKAGES / ("fedora-" + release) /
            "kubernaut_shim-{}-1.x86_64.rpm".format(self.version)
        )
        self._upload(file_path, "kubernaut_shim-rpm", "fedora/" + release)

    def _upload(self, file_path, repository, distro):
        """Upload a file to a repository.

        :param file_path Path: Path to package to upload.
        :param repository str: Bintray repository.
        :param version str: Version of package.
        :param extra str: Extra options to attach to end of Bintray URL.
        """
        run("package_cloud " + "push " + "datawireio/stable/" + distro + " " + str(file_path), check=True, shell=True)


def main(version):
    uploader = Uploader(version)
    for release in ["xenial", "yakkety", "zesty"]:
        uploader.upload_ubuntu(release)

    for release in ["25", "26"]:
        uploader.upload_fedora(release)


if __name__ == '__main__':
    main(sys.argv[1])
