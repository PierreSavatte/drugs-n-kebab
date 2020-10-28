from enum import Enum

from dnk.settings import PREPARATION_TIME_UNIT
from dnk.models import RandomlyInitialisable


class Ingredients(Enum):
    BREAD = "bread"
    LAMB = "lamb"
    SALAD = "salad"
    TOMATO = "tomato"
    ONION = "onion"
    POTATO = "potato"


class CommandTypes(Enum):
    KEBAB = {
        "name": "kebab",
        "base_preparation_time": 4 * PREPARATION_TIME_UNIT,
        "recipe": {
            Ingredients.BREAD: 1,
            Ingredients.LAMB: 1,
            Ingredients.SALAD: 1,
            Ingredients.TOMATO: 1,
            Ingredients.ONION: 1,
        },
    }
    FRENCH_FRIES = {
        "name": "french fries",
        "base_preparation_time": 1 * PREPARATION_TIME_UNIT,
        "recipe": {
            Ingredients.BREAD: 1,
            Ingredients.LAMB: 1,
            Ingredients.SALAD: 1,
            Ingredients.TOMATO: 1,
            Ingredients.ONION: 1,
        },
    }


class Command(RandomlyInitialisable):
    expected_enums_at_init = [CommandTypes]

    def __init__(self, command_type):
        values = command_type.value
        self.name = values["name"]
        self.base_preparation_time = values["base_preparation_time"]
        self.recipe = values["recipe"]
