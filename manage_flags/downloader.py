import json
import os.path
import xml.etree.ElementTree as ET

import requests
from scour.scour import generateDefaultOptions, scourString

from . import DATABASE_DIR
from .alpha2image import Alpha2Image


class Downloader:
    def __init__(self, alpha_2: str):
        self.alpha_2 = alpha_2
        self.url = None
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

        if not self.commons_titles[self.alpha_2]:
            alpha_2_image = Alpha2Image(self.alpha_2)
            image = alpha_2_image.get()
        else:
            metadata_xml = self.getMetadata(self.commons_titles[self.alpha_2])
            self.url = self.parseFileUrl(metadata_xml)
            image = self.getImage(self.url)

        image = self.scour(image)

        return image

    def getMetadata(self, commons_title: str) -> str:
        metadata_host = "https://magnus-toolserver.toolforge.org"
        metadata_url = f"{metadata_host}/commonsapi.php?image={commons_title}"

        request = requests.get(metadata_url)

        return request.text

    def parseFileUrl(self, request_text: str) -> str:
        root = ET.fromstring(request_text)
        url = root.find(".//file/urls/file[1]").text

        return url

    def getImage(self, url: str) -> str:
        request = requests.get(url)

        return request.text

    def scour(self, image: str) -> str:
        options = generateDefaultOptions()
        options.indent_depth = 2  # --nindent=2
        options.indent_type = "space"  # --indent=space
        options.keep_defs = True  # --keep-unreferenced-defs
        options.protect_ids_noninkscape = True  # --protect-ids-noninkscape
        options.simple_colors = False  # --disable-simplify-colors
        options.strip_xml_space_attribute = True  # --strip-xml-space
        options.style_to_xml = False  # --disable-style-to-xml

        return scourString(image, options)
