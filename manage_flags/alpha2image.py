class Alpha2Image:

    template = """\
<?xml version="1.0" encoding="UTF-8"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg">
  <rect width="960" height="480" fill="gray" stroke="#000"/>
  <text x="220" y="360" font-family="monospace" font-size="430">{alpha_2}</text>
</svg>
"""

    def __init__(self, alpha_2: str):
        self.alpha_2 = alpha_2

    def get(self) -> str:
        return self.template.format(alpha_2=self.alpha_2)
