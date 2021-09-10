import unittest

from manage_flags.downloader import Downloader


class DownloaderTestCase(unittest.TestCase):
    def test_wikimedia_title_from_file_url(self):
        url = "https://test.example.com/wikipedia/commons/3/3e/Flag_of_New_Zealand.svg"
        title = Downloader.wikimedia_title_from_file_url(url)

        self.assertEqual("Flag_of_New_Zealand.svg", title)

    def test_strip_title_prefix(self):
        title_with_prefix = "File:Flag_of_New_Zealand.svg"
        title_without_prefix = Downloader.strip_title_prefix(title_with_prefix)

        self.assertEqual(title_without_prefix, "Flag_of_New_Zealand.svg")
