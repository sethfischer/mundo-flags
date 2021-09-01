class ValidatorError:
    def __init__(self, name: str, description: str, countries: list):
        self.name = name
        self.description = description
        self.countries = sorted(countries)

    def getMessage(self) -> str:
        return self.description + ": " + ", ".join(self.countries)
