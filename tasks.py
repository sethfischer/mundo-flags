"""Invoke tasks for mundo-flags flag collection."""

import os.path
import tempfile
from os import getcwd

from invoke import run, task
from jinja2 import BaseLoader, Environment

BUILD_ROOT_DIRECTORY = "_build"
FLAG_ROOT_DIRECTORY = "flags"
GIT_REMOTE = "git@github.com:sethfischer/mundo-flags.git"
GIT_REMOTE_HTTPS = "https://github.com/sethfischer/mundo-flags"

release_directory = os.path.join(FLAG_ROOT_DIRECTORY, "release")
cwd = getcwd()

release_readme_template = """\
mundo-flags {{ version }}

{{ homepage }}

Flag images are dedicated to the public domain (CC0 1.0) by their respective
authors.
CC0 1.0 Universal (CC0 1.0) Public Domain Dedication
https://creativecommons.org/publicdomain/zero/1.0/
"""


@task(help={"tag": "Git tag"})
def build(c, tag="0.0.0"):
    """Build release archive."""
    release_name = f"mundo-flags_{tag}"
    release_directory = os.path.join(BUILD_ROOT_DIRECTORY, release_name)
    changelog_filepath = os.path.join(release_directory, "CHANGELOG.md")

    readme_filepath = os.path.join(release_directory, "README.txt")
    template = Environment(loader=BaseLoader()).from_string(release_readme_template)
    readme_content = template.render(version=tag, homepage=GIT_REMOTE_HTTPS)

    with tempfile.TemporaryDirectory() as tmp_directory:
        run(f"git clone {GIT_REMOTE} {tmp_directory}")
        with c.cd(tmp_directory):
            c.run(f"git checkout tags/{tag} -b build-release")
            c.run("virtualenv .venv")
            c.run(". .venv/bin/activate")
            c.run("pip install -U pip")
            c.run("poetry install")
            c.run(f"mkdir -p {BUILD_ROOT_DIRECTORY}")
            c.run(f"cp -r flags {release_directory}")
            c.run(f'echo "{readme_content}" > {readme_filepath}')
            c.run(f"poetry run cz changelog --file-name {changelog_filepath}")
            c.run(
                (
                    f"tar --owner=0 --group=0 --create --gzip "
                    f"--file={release_directory}.tar.gz "
                    f"--directory={BUILD_ROOT_DIRECTORY} "
                    f"{release_name}"
                )
            )
            with c.cd(BUILD_ROOT_DIRECTORY):
                c.run(f"zip -T -r {release_name}.zip {release_name}")
            c.run(f"cp {BUILD_ROOT_DIRECTORY}/{release_name}.tar.gz {cwd}/")
            c.run(f"cp {BUILD_ROOT_DIRECTORY}/{release_name}.zip {cwd}/")
