"""Load JSON databases into Python data structures."""

import json
import os.path

from . import DATABASE_DIR
from .flagdata import FlagData


def loadDatabase(database_name: str) -> dict:
    """Load JSON data into a dictionary."""
    with open(os.path.join(DATABASE_DIR, database_name + ".json"), "r") as file:
        database = json.load(file)

    data = {}

    for row in database[database_name]:
        data[row["alpha_2"]] = FlagData(**row)

    return data


iso3166_1 = loadDatabase("iso3166-1")
