from scour.scour import generateDefaultOptions, scourString


class Scour:
    def __init__(self):
        self.options = self.defaultOptions()

    @staticmethod
    def defaultOptions():
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

    def scourString(self, string: str) -> str:
        return scourString(string, self.options)
