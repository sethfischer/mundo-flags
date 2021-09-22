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
        """Scour an XML string."""
        return scourString(string, self.options)
