"""Flag collection validator errors."""


class ValidatorError:
    """Flag collection validator error."""

    def __init__(self, name: str, description: str, countries: list):
        """Initialise validator error."""
        self.name = name
        self.description = description
        self.countries = sorted(countries)

    def getMessage(self) -> str:
        """Get error message."""
        return self.description + ": " + ", ".join(self.countries)
