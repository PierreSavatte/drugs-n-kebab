import random
from enum import Enum

from dnk.models import RandomlyInitialisable
from dnk.settings import PREPARATION_TIME_UNIT


class Ingredients(Enum):
    BREAD = "bread"
    LAMB = "lamb"
    SALAD = "salad"
    TOMATO = "tomato"
    ONION = "onion"
    POTATO = "potato"


class OrderTypes(Enum):
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


class Order(RandomlyInitialisable):
    expected_enums_at_init = [OrderTypes]

    def __init__(self, order_type, quantity=None):
        values = order_type.value
        self.name = values["name"]
        self.base_preparation_time = values["base_preparation_time"]
        self.recipe = values["recipe"]

        if not quantity:
            quantity = random.randint(1, 5)
        self.quantity = quantity
