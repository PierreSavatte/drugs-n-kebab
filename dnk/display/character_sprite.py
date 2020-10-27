import enum
import os

import arcade

from dnk.display.load_sprites import (
    sprites_path,
    get_character_sprites,
    Facing,
)
from dnk.settings import (
    SPRITE_HEIGHT,
    SPRITE_WIDTH,
    SPRITE_SCALING,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)


class Direction(enum.Enum):
    UP = {"movement": (0, SPRITE_HEIGHT), "facing": Facing.UP}
    DOWN = {"movement": (0, -SPRITE_HEIGHT), "facing": Facing.DOWN}
    RIGHT = {"movement": (SPRITE_WIDTH, 0), "facing": Facing.RIGHT}
    LEFT = {"movement": (-SPRITE_WIDTH, 0), "facing": Facing.LEFT}


class CharacterSprite(arcade.Sprite):
    def __init__(self, model_character):
        self.sprite_path = os.path.join(
            sprites_path,
            "restaurant",
            "characters",
            model_character.ethnicity.value,
            f"{model_character.gender.value}.png",
        )
        super().__init__(self.sprite_path)

        self.scale = SPRITE_SCALING
        self.bottom = 0
        self.left = 0
        self.facing_sprites = get_character_sprites(self.sprite_path)
        self.update_facing(Facing.UP)

    def move(self, direction):
        delta_x, delta_y = direction["movement"]
        x, y = self.position
        new_x, new_y = x + delta_x, y + delta_y
        if 0 < new_x < SCREEN_WIDTH and 0 < new_y < SCREEN_HEIGHT:
            self.position = new_x, new_y

        new_facing = direction["facing"]
        if new_facing != self.facing:
            self.update_facing(new_facing)

    def update_facing(self, new_facing):
        self.facing = new_facing
        self.texture = self.facing_sprites[new_facing]
