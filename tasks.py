#! /usr/bin/env python

import os.path
import tempfile
from os import getcwd

from invoke import run, task

BUILD_ROOT_DIRECTORY = "_build"
FLAG_ROOT_DIRECTORY = "flags"
GIT_REMOTE = "git@github.com:sethfischer/mundo-flags.git"
GIT_REMOTE_HTTPS = "https://github.com/sethfischer/mundo-flags"

release_directory = os.path.join(FLAG_ROOT_DIRECTORY, "release")
cwd = getcwd()

release_readme = """\
mundo-flags {version}

{homepage}

Flag images are dedicated to the public domain (CC0 1.0) by their respective
authors.
CC0 1.0 Universal (CC0 1.0) Public Domain Dedication
https://creativecommons.org/publicdomain/zero/1.0/
"""


@task(help={"tag": "Git tag"})
def build(c, tag="0.0.0"):
    """Build release archive"""
    release_name = "mundo-flags_{tag}".format(tag=tag)
    release_directory = os.path.join(BUILD_ROOT_DIRECTORY, release_name)
    with tempfile.TemporaryDirectory() as tmp_directory:
        run(
            "git clone {remote} {directory}".format(
                remote=GIT_REMOTE, directory=tmp_directory
            )
        )
        with c.cd(tmp_directory):
            c.run("git checkout tags/{tag} -b build-release".format(tag=tag))
            c.run("virtualenv .venv")
            c.run(". .venv/bin/activate")
            c.run("pip install -U pip")
            c.run("poetry install")
            c.run("mkdir -p {build_root}".format(build_root=BUILD_ROOT_DIRECTORY))
            c.run(
                "cp -r flags {release_directory}".format(
                    release_directory=release_directory
                )
            )
            c.run(
                'echo "{content}" > {file_path}'.format(
                    content=release_readme.format(
                        version=tag,
                        homepage=GIT_REMOTE_HTTPS,
                    ),
                    file_path=os.path.join(release_directory, "README.txt"),
                )
            )
            c.run(
                "poetry run cz changelog --file-name {file_path}".format(
                    file_path=os.path.join(release_directory, "CHANGELOG.md")
                )
            )
            c.run(
                "tar --owner=0 --group=0 -czf {archive_file_path}.tar.gz --directory={build_root} {release_name}".format(  # noqa: E501
                    archive_file_path=release_directory,
                    build_root=BUILD_ROOT_DIRECTORY,
                    release_name=release_name,
                )
            )
            with c.cd(BUILD_ROOT_DIRECTORY):
                c.run(
                    "zip -T -r {archive_file_path}.zip {release_directory}".format(
                        archive_file_path=release_name,
                        release_directory=release_name,
                    )
                )
            c.run(
                "cp {build_root}/{release_name}.tar.gz {cwd}/".format(
                    build_root=BUILD_ROOT_DIRECTORY, cwd=cwd, release_name=release_name
                )
            )
            c.run(
                "cp {build_root}/{release_name}.zip {cwd}/".format(
                    build_root=BUILD_ROOT_DIRECTORY, cwd=cwd, release_name=release_name
                )
            )
