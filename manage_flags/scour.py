"""Wrappers around scour.

`Scour`_ is an SVG optimizer/cleaner.

.. _Scour: https://github.com/scour-project/scour
"""

from scour.scour import generateDefaultOptions, scourString


class Scour:
    """Wrapper around scour."""

    def __init__(self):
        """Initialise with default options."""
        self.options = self.default_options()

    @staticmethod
    def default_options():
        """Create default options."""
        options = generateDefaultOptions()

        options.indent_depth = 2  # --nindent=2
        options.indent_type = "space"  # --indent=space
        options.keep_defs = True  # --keep-unreferenced-defs
        options.protect_ids_noninkscape = True  # --protect-ids-noninkscape
        options.simple_colors = False  # --disable-simplify-colors
        options.strip_comments = True  # --enable-comment-stripping
        options.strip_xml_space_attribute = True  # --strip-xml-space
        options.style_to_xml = False  # --disable-style-to-xml

        return options

    def scour_string(self, string: str) -> str:
        """Scour an XML string.

        :param string: SVG image
        :type string: str
        :return: SVG image
        :rtype: str
        """
        return scourString(string, self.options)

    def scour_string_multipass(self, string: str, iterations: int = 3) -> str:
        """Scour an XML string with multiple iterations.

        Scouring an already scoured SVG can sometimes `produce a smaller SVG`_.

        .. _`produce a smaller SVG`: https://github.com/scour-project/scour/issues/124

        :param string: SVG image
        :type string: str
        :param: iterations: Number of iterations
        :type iterations: int
        :return: SVG image
        :rtype: str
        """
        for _ in range(iterations):
            string = self.scour_string(string)

        return string
