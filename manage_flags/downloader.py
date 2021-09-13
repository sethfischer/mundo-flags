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
    def __init__(self, flag_data: FlagData):
        self.alpha_2 = flag_data.alpha_2
        self.flag_data = flag_data
        self.url = None

    def get(self) -> str:
        requested_title = self.strip_title_prefix(self.flag_data.commons_title)

        if not self.flag_data.commons_title:
            alpha_2_image = Alpha2Image(self.alpha_2)
            image = alpha_2_image.get()
        else:
            metadata_xml = self.getMetadata(self.flag_data.commons_title)
            self.url = self.parseFileUrl(metadata_xml)
            retrived_title = self.wikimedia_title_from_file_url(self.url)

            if self.strip_title_prefix(requested_title) != retrived_title:
                message = (
                    "{alpha_2} file titles differ {requested} -> {retrived}".format(
                        alpha_2=self.alpha_2,
                        requested=requested_title,
                        retrived=retrived_title,
                    )
                )
                logging.warning(message)

            image = self.getImage(self.url)

        return self.cleanXml(image)

    @staticmethod
    def getMetadata(commons_title: str) -> str:
        metadata_host = "https://magnus-toolserver.toolforge.org"
        metadata_url = f"{metadata_host}/commonsapi.php?image={commons_title}"

        request = requests.get(metadata_url)

        return request.text

    @staticmethod
    def wikimedia_title_from_file_url(url: str) -> str:
        a = urlparse(url)
        return os.path.basename(unquote(a.path))

    @staticmethod
    def strip_title_prefix(title: str) -> str:
        prefix = "File:"
        if title.startswith(prefix):
            return title[len(prefix) :]
        return title

    def parseFileUrl(self, request_text: str) -> str:
        try:
            root = ET.fromstring(request_text)
        except ElementTreeParseError as error:
            message = "{alpha_2} metadata parse error ({error})".format(
                alpha_2=self.alpha_2,
                error=error,
            )
            raise RuntimeError(message)

        url = root.find(".//file/urls/file[1]").text

        return url

    @staticmethod
    def getImage(url: str) -> str:
        request = requests.get(url)

        return request.text

    def cleanXml(self, string: str) -> str:
        try:
            string = Scour().scourString(string)
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
