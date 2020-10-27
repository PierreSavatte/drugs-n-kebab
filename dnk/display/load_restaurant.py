import os
from enum import Enum

import arcade

root_path = os.path.dirname(os.path.abspath(__file__))
resources_path = os.path.join(root_path, "..", "resources")
tiled_path = os.path.join(resources_path, "tiled")


class RestaurantLayers(Enum):
    FLOOR_AND_WALLS = {
        "name": "floor_and_walls",
        "collidable": False,
    }
    FURNITURE = {
        "name": "furniture",
        "collidable": True,
    }
    CASH_REGISTERS = {
        "name": "cash_registers",
        "collidable": True,
    }
    COOKING_STATIONS = {
        "name": "cooking_stations",
        "collidable": True,
    }
    CHAIRS = {
        "name": "chairs",
        "collidable": False,
    }
    CARPETS = {
        "name": "carpets",
        "collidable": False,
    }


def load_restaurant_file(restaurant_name):
    return arcade.tilemap.read_tmx(
        os.path.join(tiled_path, f"{restaurant_name}.tmx")
    )
