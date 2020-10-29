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
    DEBUG_MODE,
    SPRITE_HEIGHT,
    SPRITE_WIDTH,
    SPRITE_SCALING,
    ORIGINAL_CHARACTER_SPRITE_HEIGHT,
    ORIGINAL_SPRITE_WIDTH,
    ORIGINAL_SPRITE_HEIGHT,
    MOVEMENT_ANIMATION_DURATION,
)


class Direction(enum.Enum):
    UP = {"movement": (0, SPRITE_HEIGHT), "facing": Facing.UP}
    DOWN = {"movement": (0, -SPRITE_HEIGHT), "facing": Facing.DOWN}
    RIGHT = {"movement": (SPRITE_WIDTH, 0), "facing": Facing.RIGHT}
    LEFT = {"movement": (-SPRITE_WIDTH, 0), "facing": Facing.LEFT}


KEY_MAPPING = {
    arcade.key.W: Direction.UP,
    arcade.key.S: Direction.DOWN,
    arcade.key.D: Direction.RIGHT,
    arcade.key.A: Direction.LEFT,
}


class ActionSprite(arcade.Sprite):

    DELTA = {
        # UP
        Facing.UP: (0, SPRITE_HEIGHT),
        Facing.W_UP: (0, SPRITE_HEIGHT),
        Facing.W_UP_BIS: (0, SPRITE_HEIGHT),
        # DOWN
        Facing.DOWN: (0, -SPRITE_HEIGHT),
        Facing.W_DOWN: (0, -SPRITE_HEIGHT),
        Facing.W_DOWN_BIS: (0, -SPRITE_HEIGHT),
        # RIGHT
        Facing.RIGHT: (SPRITE_HEIGHT, 0),
        Facing.W_RIGHT: (SPRITE_HEIGHT, 0),
        Facing.W_RIGHT_BIS: (SPRITE_HEIGHT, 0),
        # LEFT
        Facing.LEFT: (-SPRITE_HEIGHT, 0),
        Facing.W_LEFT: (-SPRITE_HEIGHT, 0),
        Facing.W_LEFT_BIS: (-SPRITE_HEIGHT, 0),
    }

    def __init__(self, character_sprite):
        super().__init__(
            os.path.join(
                sprites_path,
                "restaurant",
                "action_sprite.png",
            )
        )
        # Since the character is facing up:
        self.scale = SPRITE_SCALING
        self.keep_pace(character_sprite)

        # Set the hit box
        half_original_sprite_width = ORIGINAL_SPRITE_WIDTH // 2
        half_original_sprite_height = ORIGINAL_SPRITE_HEIGHT // 2
        self.set_hit_box(
            points=[
                (
                    absolute_x - half_original_sprite_width,
                    absolute_y - half_original_sprite_height,
                )
                for absolute_x, absolute_y in [
                    (0, 0),
                    (0, half_original_sprite_height),
                    (half_original_sprite_width, 0),
                    (half_original_sprite_width, half_original_sprite_height),
                ]
            ]
        )
        character_sprite.after_change("position", self.keep_pace)
        character_sprite.after_change("facing", self.keep_pace)

    def keep_pace(self, character_sprite, attribute=None, old=None, new=None):
        delta_x, delta_y = ActionSprite.DELTA[character_sprite.facing]
        self.bottom = character_sprite.bottom + delta_y
        self.center_x = character_sprite.center_x + delta_x


class CharacterSprite(arcade_curtains.ObservableSprite):
    def __init__(self, model_character, restaurant_widget):
        super().__init__()

        # Compute relative points (to the sprite center, not scaled) from absolute
        relative_center_x, relative_center_y = (
            ORIGINAL_SPRITE_WIDTH // 2,
            ORIGINAL_CHARACTER_SPRITE_HEIGHT // 2,
        )
        self.set_hit_box(
            points=[
                (
                    absolute_x - relative_center_x,
                    absolute_y - relative_center_y,
                )
                for absolute_x, absolute_y in [
                    (0, 0),
                    (0, ORIGINAL_SPRITE_WIDTH),
                    (ORIGINAL_SPRITE_WIDTH, 0),
                    (ORIGINAL_SPRITE_WIDTH, ORIGINAL_SPRITE_HEIGHT),
                ]
            ]
        )
        self.restaurant_widget = restaurant_widget

        self.sprite_path = os.path.join(
            sprites_path,
            "restaurant",
            "characters",
            model_character.ethnicity.value,
            f"{model_character.gender.value}.png",
        )

        self.facing_sprites = get_character_sprites(self.sprite_path)
        self.direction = None
        self.already_moving = False
        self.update_facing(Facing.UP)

        self.scale = SPRITE_SCALING

        carpet = random.choice(restaurant_widget.carpets)
        self.bottom = restaurant_widget.bottom
        self.center_x = carpet.center_x

        self.action_sprite = ActionSprite(self)
        if DEBUG_MODE:
            restaurant_widget.scene.events.before_draw(
                self.add_action_sprite_to_sprite_list,
                {"scene": restaurant_widget.scene},
            )
            restaurant_widget.scene.events.after_draw(
                self.remove_action_sprite_to_sprite_list,
                {"scene": restaurant_widget.scene},
            )

    def add_action_sprite_to_sprite_list(self, scene):
        scene.sprites.append(self.action_sprite)

    def remove_action_sprite_to_sprite_list(self, scene):
        scene.sprites.remove(self.action_sprite)

    def _update_walking(self, new_facing, finished_moving=False):
        self.update_facing(new_facing)
        if finished_moving:
            self.already_moving = False

    def _get_walking_animation(self, facing, new_pos):
        # Get intermediary facing
        walking_facing_1 = Facing["_".join(["W", facing.name])]
        walking_facing_2 = Facing["_".join([walking_facing_1.name, "BIS"])]

        seq = arcade_curtains.Sequence.from_sprite(self)
        # At 0, Start moving mode and set 1st walking sprite
        seq[0].callback = partial(
            self._update_walking, new_facing=walking_facing_1
        )
        # In the middle, set 2nd walking sprite
        seq[MOVEMENT_ANIMATION_DURATION / 2].callback = partial(
            self._update_walking, new_facing=walking_facing_2
        )
        # At the end, finish moving mode and set facing asked
        seq[MOVEMENT_ANIMATION_DURATION].callback = partial(
            self._update_walking, new_facing=facing, finished_moving=True
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

        (min_x, min_y), (max_x, max_y) = self.restaurant_widget.walkable_zone

        return min_x < x < max_x and min_y < y < max_y

    def will_collide_with_list(self, new_pos):
        import copy

        old_position = copy.copy(self.position)
        self.position = new_pos
        sprites_collide = self.collides_with_list(
            self.restaurant_widget.collidable_layers
        )
        self.position = old_position
        return sprites_collide

    def continue_moving(self):
        # Triggers animation only if not already moving and
        # direction not yet erased
        if not self.already_moving and self.direction:
            self.already_moving = True
            delta_x, delta_y = self.direction["movement"]
            new_facing = self.direction["facing"]

            x, y = self.position
            new_pos = x + delta_x, y + delta_y

            # If position is outside the window
            if not self.is_inside_restaurant(
                alt_pos=new_pos
            ) or self.will_collide_with_list(new_pos):
                new_pos = self.position

            self.animate(self._get_walking_animation(new_facing, new_pos))

    def start_moving(self, direction):
        self.direction = direction

    def stop_moving(self, direction):
        if self.direction == direction:
            self.direction = None

    def update_facing(self, new_facing):
        self.facing = new_facing
        self.texture = self.facing_sprites[new_facing]

    def update(self, *args, **kwargs):
        self.continue_moving()
