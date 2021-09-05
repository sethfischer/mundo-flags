#! /usr/bin/env python

import logging
import os.path
import sys
from decimal import InvalidOperation as DecimalInvalidOperation
from time import sleep
from xml.parsers.expat import ExpatError
from xml.parsers.expat import errors as expat_errors

import pycountry

from manage_flags.downloader import Downloader
from manage_flags.validator import Validator

FLAG_DIRECTORY = "svg"

logging.basicConfig(format="%(levelname)s:%(message)s")


def flagPathname(alpha_2: str, svg: str) -> str:
    return os.path.join(FLAG_DIRECTORY, alpha_2.lower() + ".svg")


def downlad_iso_3166_1_flag(alpha_2: str, exit_on_error: bool = True) -> bool:
    downloader = Downloader(alpha_2)

    try:
        svg = downloader.get()

        pathname = flagPathname(alpha_2, svg)
        file = open(pathname, "w")
        file.write(svg)
        file.close
    except ExpatError as error:
        message = "{alpha_2} scour ({error_message}) {url}".format(
            alpha_2=alpha_2,
            error_message=expat_errors.messages[error.code],
            url=downloader.url,
        )
        logging.error(message)
        if exit_on_error:
            sys.exit(1)

        return False
    except DecimalInvalidOperation as error:
        message = "{alpha_2} scour ({error}) {url}".format(
            alpha_2=alpha_2,
            error=error,
            url=downloader.url,
        )
        logging.error(message)
        if exit_on_error:
            sys.exit(1)

    return True


def downlad_iso_3166_1_flags(delay: int):
    for country in pycountry.countries:
        downlad_iso_3166_1_flag(country.alpha_2, exit_on_error=False)
        sleep(delay)


def validate_collection():
    validator = Validator(FLAG_DIRECTORY)

    if validator.validate() is False:
        for error in validator.errors:
            logging.error(error.getMessage())

        sys.exit(1)

    sys.exit()


def main(args):
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
        help="Download flag by ISO 31661-1 alpha 2 country code",
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
