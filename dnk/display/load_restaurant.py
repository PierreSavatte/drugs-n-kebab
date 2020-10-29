import os
from enum import Enum

import arcade

root_path = os.path.dirname(os.path.abspath(__file__))
resources_path = os.path.join(root_path, "..", "resources")
tiled_path = os.path.join(resources_path, "tiled")

# We are assuming the carpets are at the bottom of the restaurants


class RestaurantLayers(Enum):
    FLOOR_AND_WALLS = {
        "name": "floor_and_walls",
        "collidable": False,
        "interactive": False,
    }
    FURNITURE = {
        "name": "furniture",
        "collidable": True,
        "interactive": False,
    }
    CASH_REGISTERS = {
        "name": "cash_registers",
        "collidable": True,
        "interactive": True,
    }
    COOKING_STATIONS = {
        "name": "cooking_stations",
        "collidable": True,
        "interactive": True,
    }
    CHAIRS = {
        "name": "chairs",
        "collidable": False,
        "interactive": False,
    }
    CARPETS = {
        "name": "carpets",
        "collidable": False,
        "interactive": False,
    }

    @classmethod
    def ordered(cls):
        return [
            cls.FLOOR_AND_WALLS,
            cls.FURNITURE,
            cls.CASH_REGISTERS,
            cls.COOKING_STATIONS,
            cls.CHAIRS,
            cls.CARPETS,
        ]


def load_restaurant_file(restaurant_name):
    return arcade.tilemap.read_tmx(
        os.path.join(tiled_path, f"{restaurant_name}.tmx")
    )
