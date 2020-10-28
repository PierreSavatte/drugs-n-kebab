import enum
import os
import random
from functools import partial

import arcade
import arcade_curtains

from dnk.display.load_sprites import (
    sprites_path,
    get_character_sprites,
    Facing,
)
from dnk.settings import (
    SPRITE_HEIGHT,
    SPRITE_WIDTH,
    SPRITE_SCALING,
    ORIGINAL_CHARACTER_SPRITE_HEIGHT,
    ORIGINAL_SPRITE_WIDTH,
    MOVEMENT_ANIMATION_DURATION,
)


class Direction(enum.Enum):
    UP = {"movement": (0, SPRITE_HEIGHT), "facing": Facing.UP}
    DOWN = {"movement": (0, -SPRITE_HEIGHT), "facing": Facing.DOWN}
    RIGHT = {"movement": (SPRITE_WIDTH, 0), "facing": Facing.RIGHT}
    LEFT = {"movement": (-SPRITE_WIDTH, 0), "facing": Facing.LEFT}


class CharacterSprite(arcade.Sprite):
    def __init__(self, model_character, restaurant_scene):
        super().__init__()

        # Compute relative points (to the sprite center, not scaled) from absolute
        center_x, center_y = (
            ORIGINAL_SPRITE_WIDTH // 2,
            ORIGINAL_CHARACTER_SPRITE_HEIGHT // 2,
        )
        self.set_hit_box(
            points=[
                (absolute_x - center_x, absolute_y - center_y)
                for absolute_x, absolute_y in [
                    (0, 0),
                    (0, ORIGINAL_SPRITE_WIDTH),
                    (ORIGINAL_SPRITE_WIDTH, 0),
                    (ORIGINAL_SPRITE_WIDTH, ORIGINAL_SPRITE_WIDTH),
                ]
            ]
        )
        self.restaurant_scene = restaurant_scene

        self.sprite_path = os.path.join(
            sprites_path,
            "restaurant",
            "characters",
            model_character.ethnicity.value,
            f"{model_character.gender.value}.png",
        )

        self.facing_sprites = get_character_sprites(self.sprite_path)
        self.moving_mode = False
        self.update_facing(Facing.UP)

        self.scale = SPRITE_SCALING

        carpet = random.choice(restaurant_scene.carpets)
        self.bottom = restaurant_scene.bottom
        self.center_x = carpet.center_x

    def _update_walking(self, new_facing, moving_mode=None):
        self.update_facing(new_facing)
        if moving_mode is not None:
            self.moving_mode = moving_mode

    def _get_walking_animation(self, facing, new_pos):
        # Get intermediary facing
        walking_facing_1 = Facing["_".join(["W", facing.name])]
        walking_facing_2 = Facing["_".join([walking_facing_1.name, "BIS"])]

        seq = arcade_curtains.Sequence.from_sprite(self)
        # At 0, Start moving mode and set 1st walking sprite
        seq[0].callback = partial(
            self._update_walking, new_facing=walking_facing_1, moving_mode=True
        )
        # In the middle, set 2nd walking sprite
        seq[MOVEMENT_ANIMATION_DURATION / 2].callback = partial(
            self._update_walking, new_facing=walking_facing_2
        )
        # At the end, finish moving mode and set facing asked
        seq[MOVEMENT_ANIMATION_DURATION].callback = partial(
            self._update_walking, new_facing=facing, moving_mode=False
        )
        # At the end, the sprite will be at the new_pos
        seq[MOVEMENT_ANIMATION_DURATION].frame = arcade_curtains.KeyFrame(
            position=new_pos
        )
        return seq

    def is_inside_restaurant(self, alt_pos=None):
        # Get position
        if alt_pos is None:
            alt_pos = self.position
        x, y = alt_pos

        (min_x, min_y), (max_x, max_y) = self.restaurant_scene.walkable_zone

        return min_x < x < max_x and min_y < y < max_y

    def will_collide_with_list(self, new_pos):
        import copy

        old_position = copy.copy(self.position)
        self.position = new_pos
        sprites_collide = self.collides_with_list(
            self.restaurant_scene.collidable_layers
        )
        self.position = old_position
        return sprites_collide

    def move(self, direction):
        if not self.moving_mode:
            delta_x, delta_y = direction["movement"]
            new_facing = direction["facing"]

            x, y = self.position
            new_pos = x + delta_x, y + delta_y

            # If position is outside the window
            if not self.is_inside_restaurant(
                alt_pos=new_pos
            ) or self.will_collide_with_list(new_pos):
                new_pos = self.position

            self.animate(self._get_walking_animation(new_facing, new_pos))

    def update_facing(self, new_facing):
        self.facing = new_facing
        self.texture = self.facing_sprites[new_facing]
