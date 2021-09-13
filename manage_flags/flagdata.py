from dataclasses import dataclass, field


@dataclass
class FlagData:

    alpha_2: str
    commons_title: str = field(default="")
