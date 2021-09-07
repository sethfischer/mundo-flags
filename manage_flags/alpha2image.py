from jinja2 import Environment, PackageLoader, select_autoescape


class Alpha2Image:
    def __init__(self, alpha_2: str):
        self.alpha_2 = alpha_2

    def get(self) -> str:
        env = Environment(
            loader=PackageLoader("manage_flags"), autoescape=select_autoescape()
        )

        template = env.get_template("alpha2image.svg")

        return template.render(alpha_2=self.alpha_2)
