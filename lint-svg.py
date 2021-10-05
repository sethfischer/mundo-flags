#!/usr/bin/env python
"""Lint SVG files."""

import difflib
import logging
import os
import sys
from argparse import Namespace
from typing import Optional

from manage_flags.scour import Scour

FLAG_DIRECTORY = os.path.join("flags", "iso3166-1")

logging.basicConfig(format="%(levelname)s:%(message)s")


def list_files(directory_path: str = FLAG_DIRECTORY) -> list:
    """List SVG images."""
    pathnames = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".svg"):
                pathnames.append(os.path.join(root, str(file)))

    return pathnames


def actual_svg(pathname: str) -> str:
    """Read SVG image from disk."""
    with open(pathname, "r") as file:
        svg = file.read()
    return svg


def expected_svg(image: str) -> str:
    """Calculate expected SVG."""
    return Scour().scour_string(image)


def calculate_delta(actual_svg: str, expected_svg: str) -> str:
    """Calculate diff of two SVG images."""
    delta = difflib.unified_diff(
        actual_svg.splitlines(),
        expected_svg.splitlines(),
        "actual",
        "expected",
        lineterm="",
    )

    return "\n".join(delta)


def lint_svg(pathname: str, args: Namespace) -> Optional[str]:
    """Lint SVG image."""
    actual = actual_svg(pathname)
    expected = expected_svg(actual)

    if actual == expected:
        return None

    if args.warn_on_error:
        logging.warning(
            f"{pathname} not optimised "
            f"actual={len(actual)} "
            f"expected={len(expected)} "
            f"({len(actual) - len(expected):+})"
        )

    if args.show_diff:
        delta = calculate_delta(actual, expected)
        sys.stderr.write(delta + "\n")

    return pathname


def main(args: Namespace) -> int:
    """Lint SVG files."""
    return_code = 1
    pathnames = list_files()
    summary = []

    for pathname in pathnames:
        result = lint_svg(pathname, args)
        if result is not None:
            summary.append(result)

    if args.show_summary:
        logging.error(f"Summary ({len(summary)} errors)")
        for index, pathname in enumerate(summary, start=1):
            logging.error(f"{index}. {pathname}")

    if args.warn_on_error or not summary:
        return_code = 0

    return return_code


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Lint SVG images")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--warn-on-error",
        action="store_true",
        dest="warn_on_error",
        help=(
            "Convert errors to warnings and display file size delta. "
            "Useful if scour issue #124 is encountered. "
            "See https://github.com/scour-project/scour/issues/124"
        ),
    )
    group.add_argument(
        "--show-diff",
        action="store_true",
        dest="show_diff",
        help="Print diff to stderr.",
    )

    parser.add_argument(
        "--show-summary",
        action="store_true",
        dest="show_summary",
        help="Display summary at end of output.",
    )

    parser.set_defaults(warn_on_error=False, show_diff=False, show_summary=False)

    result = main(parser.parse_args())

    sys.exit(result)
