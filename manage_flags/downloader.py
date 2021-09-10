import json
import logging
import os.path
import xml.etree.ElementTree as ET
from decimal import InvalidOperation as DecimalInvalidOperation
from urllib.parse import unquote, urlparse
from xml.etree.ElementTree import ParseError as ElementTreeParseError
from xml.parsers.expat import ExpatError
from xml.parsers.expat import errors as expat_errors

import requests
from scour.scour import generateDefaultOptions, scourString

from . import DATABASE_DIR
from .alpha2image import Alpha2Image


class Downloader:
    def __init__(self, alpha_2: str, quiet: bool = True):
        self.alpha_2 = alpha_2
        self.url = None

        self.logging = logging.basicConfig(format="%(levelname)s:%(message)s")
        if not quiet:
            self.logger.propagate = False

        self.load_db()

    def load_db(self) -> int:
        db = open(os.path.join(DATABASE_DIR, "iso3166-1.json"))
        commons_titles = json.load(db)

        self.commons_titles = {}

        for country in commons_titles["3166-1"]:
            self.commons_titles[country["alpha_2"]] = country["commons_title"]

        return len(self.commons_titles)

    def get(self) -> str:
        if self.alpha_2 not in self.commons_titles:
            raise NotImplementedError

        requested_title = self.strip_title_prefix(self.commons_titles[self.alpha_2])

        if not self.commons_titles[self.alpha_2]:
            alpha_2_image = Alpha2Image(self.alpha_2)
            image = alpha_2_image.get()
        else:
            metadata_xml = self.getMetadata(self.commons_titles[self.alpha_2])
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

        image = self.scour(image)

        return image

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

    def scour(self, image: str) -> str:
        options = generateDefaultOptions()
        options.indent_depth = 2  # --nindent=2
        options.indent_type = "space"  # --indent=space
        options.keep_defs = True  # --keep-unreferenced-defs
        options.protect_ids_noninkscape = True  # --protect-ids-noninkscape
        options.simple_colors = False  # --disable-simplify-colors
        options.strip_comments = True  # --enable-comment-stripping
        options.strip_xml_space_attribute = True  # --strip-xml-space
        options.style_to_xml = False  # --disable-style-to-xml

        try:
            scoured_image = scourString(image, options)
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

        return scoured_image
