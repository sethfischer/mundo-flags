#! /usr/bin/env python
"""Manage flags CLI tool."""

import logging
import os.path
import sys
from time import sleep

import pycountry

from manage_flags.database import iso3166_1
from manage_flags.downloader import Downloader
from manage_flags.validator import Validator

FLAG_DIRECTORY = os.path.join("flags", "iso3166-1")

logging.basicConfig(format="%(levelname)s:%(message)s")


def flagPathname(alpha_2: str, svg: str) -> str:
    """Generate pathname for flag image."""
    return os.path.join(FLAG_DIRECTORY, alpha_2.lower() + ".svg")


def downlad_iso_3166_1_flag(alpha_2: str, exit_on_error: bool = True) -> bool:
    """Download a flag image from Wikimedia Commons."""
    if alpha_2 not in iso3166_1:
        logging.critical("Invalid alpha-2 code: {alpha_2}".format(alpha_2=alpha_2))
        sys.exit(1)

    downloader = Downloader(iso3166_1[alpha_2])

    try:
        svg = downloader.get()

        pathname = flagPathname(alpha_2, svg)
        file = open(pathname, "w")
        file.write(svg)
        file.close
    except RuntimeError as error:
        logging.error(error)
        if exit_on_error:
            sys.exit(1)
        return False

    return True


def downlad_iso_3166_1_flags(delay: int):
    """Batch download flag images from Wikimedia Commons."""
    for country in pycountry.countries:
        downlad_iso_3166_1_flag(country.alpha_2, exit_on_error=False)
        sleep(delay)


def validate_collection():
    """Validate flag collection."""
    validator = Validator(FLAG_DIRECTORY)

    if validator.validate() is False:
        for error in validator.errors:
            logging.error(error.get_message())

        sys.exit(1)

    sys.exit()


def main(args):
    """Manage flags CLI tool."""
    if args.cmd == "download":
        if args.alpha_2 is not None:
            downlad_iso_3166_1_flag(args.alpha_2)
        if args.all_countries:
            downlad_iso_3166_1_flags(1)

    if args.cmd == "validate":
        validate_collection()

    sys.exit()


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Manage flags collection")
    subparsers = parser.add_subparsers(title="subcommands", dest="cmd")

    parser_download = subparsers.add_parser("download", help="download flags")
    parser_validate = subparsers.add_parser("validate", help="validate flag collection")

    group = parser_download.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--country",
        dest="alpha_2",
        help="Download flag by ISO 31661-1 alpha-2 country code",
    )
    group.add_argument(
        "--all-countries",
        action="store_true",
        dest="all_countries",
        help="Download all flags for all ISO 31661-1 countries",
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    main(parser.parse_args())
