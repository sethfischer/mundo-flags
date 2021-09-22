import unittest

from manage_flags.downloader import Downloader
from manage_flags.flagdata import FlagData


class DownloaderTestCase(unittest.TestCase):
    def test_wikimedia_title_from_url(self):
        url = "https://test.example.com/wikipedia/commons/3/3e/Flag_of_New_Zealand.svg"
        title = Downloader.wikimedia_title_from_url(url)

        self.assertEqual("Flag_of_New_Zealand.svg", title)

    def test_strip_title_prefix(self):
        title_with_prefix = "File:Flag_of_New_Zealand.svg"
        title_without_prefix = Downloader.strip_title_prefix(title_with_prefix)

        self.assertEqual(title_without_prefix, "Flag_of_New_Zealand.svg")

    def test_alpha_2(self):
        alpha_2 = "NZ"
        flag_data = FlagData(alpha_2=alpha_2)
        downloader = Downloader(flag_data)

        self.assertEqual(alpha_2, downloader.alpha_2)

    def test_commons_title(self):
        alpha_2 = "NZ"
        commons_title = "File:Flag_of_New_Zealand.svg"
        flag_data = FlagData(alpha_2=alpha_2, commons_title=commons_title)
        downloader = Downloader(flag_data)

        self.assertEqual(commons_title, downloader.flag_data.commons_title)
