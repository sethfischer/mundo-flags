#!/usr/bin/env python
"""Lint SVG files."""

import difflib
import os
import sys

from manage_flags.scour import Scour

FLAG_DIRECTORY = os.path.join("flags", "iso3166-1")


def list_files(directory_path: str = FLAG_DIRECTORY) -> list:
    """List SVG images."""
    pathnames = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".svg"):
                pathnames.append(os.path.join(root, str(file)))

    return pathnames


def calculate_delta(pathname: str) -> str:
    """Compare image with expected scoured image."""
    with open(pathname, "r") as file:
        svg = file.read()

    expected_svg = Scour().scour_string(svg)

    delta = difflib.unified_diff(
        svg.splitlines(),
        expected_svg.splitlines(),
        pathname,
        "scour_string",
        lineterm="",
    )

    return "\n".join(delta)


def is_zero_delta(delta: str) -> bool:
    """Test if delta is empty."""
    if len(delta) == 0:
        return True
    return False


def main() -> int:
    """Lint SVG files."""
    return_code = 0
    pathnames = list_files()
    failed = []

    for pathname in pathnames:
        delta = calculate_delta(pathname)

        if not is_zero_delta(delta):
            return_code = 1
            sys.stderr.write(delta + "\n")
            failed.append(pathname)

    if failed:
        sys.stderr.write(f"Summary ({len(failed)}):\n")
        for index, pathname in enumerate(failed, start=1):
            sys.stderr.write(f"{index}. {pathname}\n")

    return return_code


if __name__ == "__main__":

    sys.exit(main())
