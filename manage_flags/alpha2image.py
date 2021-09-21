"""Create placeholder image.

A placeholder image is created for countries without an official flag.
"""

from jinja2 import Environment, PackageLoader, select_autoescape


class Alpha2Image:
    """Create placeholder image."""

    def __init__(self, alpha_2: str):
        """Initialise with ISO alpha-2 country code."""
        self.alpha_2 = alpha_2

    def get(self) -> str:
        """Create placeholder image."""
        env = Environment(
            loader=PackageLoader("manage_flags"), autoescape=select_autoescape()
        )

        template = env.get_template("alpha2image.svg")

        return template.render(alpha_2=self.alpha_2)
