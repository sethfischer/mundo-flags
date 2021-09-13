import unittest

from manage_flags.database import iso3166_1
from manage_flags.flagdata import FlagData


class Iso31661TestCase(unittest.TestCase):
    def test_country_count(self):

        self.assertEqual(len(iso3166_1), 249)

    def test_country(self):
        alpha_2 = "NZ"
        commons_title = "File:Flag_of_New_Zealand.svg"
        expected = FlagData(alpha_2=alpha_2, commons_title=commons_title)

        self.assertEqual(iso3166_1[alpha_2], expected)
