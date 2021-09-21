"""Data structures for flag data."""

from dataclasses import dataclass, field


@dataclass
class FlagData:
    """Flag data."""

    alpha_2: str
    commons_title: str = field(default="")
