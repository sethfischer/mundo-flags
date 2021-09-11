import unittest

from manage_flags.scour import Scour


class ScourTestCase(unittest.TestCase):
    def test_strip_comments(self):
        svg = """\
<?xml version="1.0" encoding="UTF-8"?>
<!-- a comment -->
<svg width="960" height="480" version="1.1" viewBox="0 0 960 480" xmlns="http://www.w3.org/2000/svg">
  <rect width="960" height="480" fill="gray" stroke="#000"/>
</svg>
"""
        expected = """\
<?xml version="1.0" encoding="UTF-8"?>
<svg width="960" height="480" version="1.1" viewBox="0 0 960 480" xmlns="http://www.w3.org/2000/svg">
  <rect width="960" height="480" fill="gray" stroke="#000"/>
</svg>
"""

        result = Scour().scourString(svg)

        self.assertEqual(result, expected)
