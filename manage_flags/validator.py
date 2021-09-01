from os import listdir
from os.path import basename, isfile, join, splitext

import pycountry

from .validator_error import ValidatorError


class Validator:
    def __init__(self, flag_directory: str):
        self.flag_directory = flag_directory
        self.additional_flags = set()
        self.missing_flags = set()
        self.errors = []

    def validate(self) -> bool:
        collection = self.svg_collection()
        iso_countries = self.iso_countries()

        self.additional_flags = set(iso_countries) - set(collection)
        if len(self.additional_flags) > 0:
            self.errors.append(
                ValidatorError(
                    "additional_flags",
                    "Additional flags",
                    list(self.additional_flags),
                )
            )

        self.missing_flags = set(collection) - set(iso_countries)
        if len(self.missing_flags) > 0:
            self.errors.append(
                ValidatorError(
                    "missing_flags", "Missing flags", list(self.missing_flags)
                )
            )

        if len(self.errors) > 0:
            return False

        return True

    def hasErrors(self) -> bool:
        if len(self.errors) > 0:
            return True

        return False

    def filename_to_alpha_2(self, path: str) -> str:
        base = basename(path)
        root = splitext(base)[0]
        return root.upper()

    def svg_collection(self) -> list:
        collection = []
        for f in listdir(self.flag_directory):
            if isfile(join(self.flag_directory, f)):
                collection.append(self.filename_to_alpha_2(f))

        return collection

    def iso_countries(self) -> list:
        countries = []
        for country in pycountry.countries:
            countries.append(country.alpha_2)

        return countries
