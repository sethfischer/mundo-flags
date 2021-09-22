"""Validate a flag collection."""

from os import listdir
from os.path import basename, isfile, join, splitext

import pycountry

from .validator_error import ValidatorError


class Validator:
    """Validate a flag collection."""

    def __init__(self, flag_directory: str):
        """Initialise flag collection validator."""
        self.flag_directory = flag_directory
        self.additional_flags = set()
        self.missing_flags = set()
        self.errors = []

    def validate(self) -> bool:
        """Validate a flag collection."""
        collection = self.flag_collection()
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
        """Test if collection has validation errors."""
        if len(self.errors) > 0:
            return True

        return False

    @staticmethod
    def pathname_to_alpha_2(path: str) -> str:
        """Parse ISO alpha-2 country code from flag pathname."""
        base = basename(path)
        root = splitext(base)[0]
        return root.upper()

    def flag_collection(self) -> list:
        """Get list of flags in collection."""
        collection = []
        for f in listdir(self.flag_directory):
            if isfile(join(self.flag_directory, f)):
                collection.append(self.pathname_to_alpha_2(f))

        return collection

    @staticmethod
    def iso_countries() -> list:
        """Get list of countries."""
        countries = []
        for country in pycountry.countries:
            countries.append(country.alpha_2)

        return countries
