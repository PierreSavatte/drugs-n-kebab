import enum
import os

import arcade

from dnk.settings import (
    ORIGINAL_SPRITE_WIDTH,
    ORIGINAL_CHARACTER_SPRITE_HEIGHT,
)

root_path = os.path.dirname(os.path.abspath(__file__))
resources_path = os.path.join(root_path, "..", "resources")
sprites_path = os.path.join(resources_path, "sprites")


notification_sprite_path = os.path.join(sprites_path, "notification.png")


class Facing(enum.Enum):
    UP = "up"
    W_UP = "w_up"
    W_UP_BIS = "w_up_bis"
    DOWN = "down"
    W_DOWN = "w_down"
    W_DOWN_BIS = "w_down_bis"
    RIGHT = "right"
    W_RIGHT = "w_right"
    W_RIGHT_BIS = "w_right_bis"
    LEFT = "left"
    W_LEFT = "w_left"
    W_LEFT_BIS = "w_left_bis"


FACING_ORDER_AND_MIRROR = {
    Facing.DOWN: None,
    Facing.UP: None,
    Facing.LEFT: Facing.RIGHT,
    Facing.W_DOWN: Facing.W_DOWN_BIS,
    Facing.W_UP: Facing.W_UP_BIS,
    Facing.W_LEFT: Facing.W_RIGHT,
    Facing.W_LEFT_BIS: Facing.W_RIGHT_BIS,
}


def get_character_sprites(sprite_path):
    sprites = {}
    params = {
        "y": 0,
        "width": ORIGINAL_SPRITE_WIDTH,
        "height": ORIGINAL_CHARACTER_SPRITE_HEIGHT,
    }
    for x, (facing, facing_mirror) in zip(
        range(0, 112, ORIGINAL_SPRITE_WIDTH), FACING_ORDER_AND_MIRROR.items()
    ):
        sprites[facing] = arcade.load_texture(sprite_path, x=x, **params)
        if facing_mirror:
            sprites[facing_mirror] = arcade.load_texture(
                sprite_path, x=x, flipped_horizontally=True, **params
            )

    return sprites
