"""Download flag image from Wikimedia Commons."""

import logging
import os.path
import xml.etree.ElementTree as ET
from decimal import InvalidOperation as DecimalInvalidOperation
from urllib.parse import unquote, urlparse
from xml.etree.ElementTree import ParseError as ElementTreeParseError
from xml.parsers.expat import ExpatError
from xml.parsers.expat import errors as expat_errors

import requests

from manage_flags.flagdata import FlagData

from .alpha2image import Alpha2Image
from .scour import Scour


class Downloader:
    """Download flag image from Wikimedia Commons."""

    def __init__(self, flag_data: FlagData):
        """Initialise flag downloader.

        :param flag_data: Map country to Wikimedia Commons flag image
        :type flag_data: FlagData
        """
        self.alpha_2 = flag_data.alpha_2
        self.flag_data = flag_data
        self.url = None

        self.headers = {
            "User-Agent": (
                f"mundo-flags/{requests.__version__} "
                "(+https://github.com/sethfischer/mundo-flags)"
            ),
        }

    def get(self, scour: bool = True) -> str:
        """Download flag image from Wikimedia Commons.

        :return: SVG image
        :rtype: str
        """
        requested_title = self.strip_title_prefix(self.flag_data.commons_title)

        if not self.flag_data.commons_title:
            alpha_2_image = Alpha2Image(self.alpha_2)
            image = alpha_2_image.get()
        else:
            metadata_xml = self.get_metadata(self.flag_data.commons_title)
            self.url = self.parse_file_url(metadata_xml)
            retrived_title = self.wikimedia_title_from_url(self.url)

            if self.strip_title_prefix(requested_title) != retrived_title:
                message = (
                    "{alpha_2} file titles differ {requested} -> {retrived}".format(
                        alpha_2=self.alpha_2,
                        requested=requested_title,
                        retrived=retrived_title,
                    )
                )
                logging.warning(message)

            image = self.get_image(self.url)

        if scour:
            image = self.clean_xml(image)

        return image

    def get_metadata(self, commons_title: str) -> str:
        """Get image metadata.

        :param commons_title: Wikimedia Commons image title
        :type commons_title: str
        :return: Image metadata in XML format
        :rtype: str
        """
        metadata_host = "https://magnus-toolserver.toolforge.org"
        metadata_url = f"{metadata_host}/commonsapi.php?image={commons_title}"

        request = requests.get(metadata_url, self.headers)

        if request.status_code != requests.codes.ok:
            message = "{alpha_2} download HTTP error {status_code}".format(
                alpha_2=self.alpha_2, status_code=request.status_code
            )
            raise RuntimeError(message)

        return request.text

    @staticmethod
    def wikimedia_title_from_url(url: str) -> str:
        """Parse Wikimedia Commons image title from URL.

        :param url: URL of image
        :type url: str
        :return: Image title
        :rtype: str
        """
        a = urlparse(url)
        return os.path.basename(unquote(a.path))

    @staticmethod
    def strip_title_prefix(title: str) -> str:
        """Strip title prefix from Wikimedia Commons image title.

        :param title: Image title
        :type title: str
        :return: Image title without prefix
        :rtype: str
        """
        prefix = "File:"
        if title.startswith(prefix):
            return title[len(prefix) :]
        return title

    def parse_file_url(self, xml_document: str) -> str:
        """Parse image URL from magnus-toolserver metadata.

        :param xml_document: Image metadata XML document
        :type xml_document: str
        :return: Image URL
        :rtype: str
        """
        try:
            root = ET.fromstring(xml_document)
        except ElementTreeParseError as error:
            message = "{alpha_2} metadata parse error ({error})".format(
                alpha_2=self.alpha_2,
                error=error,
            )
            raise RuntimeError(message)

        url = root.find(".//file/urls/file[1]").text

        return url

    def get_image(self, url: str) -> str:
        """Retrive image using HTTP GET.

        :param url: URL
        :type url: str
        """
        request = requests.get(url, headers=self.headers)

        if request.status_code != requests.codes.ok:
            message = "{alpha_2} download HTTP error {status_code}".format(
                alpha_2=self.alpha_2, status_code=request.status_code
            )
            raise RuntimeError(message)

        return request.text

    def clean_xml(self, string: str) -> str:
        """Optimise and clean SVG image.

        :param string: SVG image
        :type string: str
        :raises RuntimeError: Error parsing SVG image
        :return: SVG image
        :rtype: str
        """
        try:
            string = Scour().scour_string(string)
        except ExpatError as error:
            message = "{alpha_2} scour {error_message} {url}".format(
                alpha_2=self.alpha_2,
                error_message=expat_errors.messages[error.code],
                url=self.url,
            )
            raise RuntimeError(message)
        except DecimalInvalidOperation:
            message = "{alpha_2} scour invalid decimal operation {url}".format(
                alpha_2=self.alpha_2,
                url=self.url,
            )
            raise RuntimeError(message)

        return string
