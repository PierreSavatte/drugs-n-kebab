import os
from unittest.mock import patch

import pytest

from dnk.display.character_sprite import (
    CharacterSprite,
    Direction,
    Facing,
    MOVEMENT_ANIMATION_DURATION,
)
from dnk.settings import SPRITE_HEIGHT, SPRITE_WIDTH


def test_character_sprite_has_sprite_related_to_their_ethnicity(
    character, restaurant_scene
):
    sprite = CharacterSprite(character, restaurant_scene.widget)

    expected_path = os.path.join(
        "restaurant",
        "characters",
        character.ethnicity.value,
        f"{character.gender.value}.png",
    )
    assert expected_path in sprite.sprite_path


def test_character_sprite_has_walking_animation(character, restaurant_scene):
    sprite = CharacterSprite(character, restaurant_scene.widget)

    x, y = sprite.position
    walking_animation = sprite._get_walking_animation(
        Facing.DOWN, (x + 10, y + 10)
    )

    for time, facing, finished_moving in [
        (0, Facing.W_DOWN, None),
        (MOVEMENT_ANIMATION_DURATION / 2, Facing.W_DOWN_BIS, None),
        (MOVEMENT_ANIMATION_DURATION, Facing.DOWN, True),
    ]:
        callback_kwargs = walking_animation.callbacks[time].keywords
        expected_kwargs = {"new_facing": facing}
        if finished_moving is not None:
            expected_kwargs["finished_moving"] = finished_moving
        assert callback_kwargs == expected_kwargs


def test_character_sprite_animation_moves_sprite(character, restaurant_scene):
    sprite = CharacterSprite(character, restaurant_scene.widget)
    x, y = sprite.position
    new_position = (x + 10, y + 10)

    walking_animation = sprite._get_walking_animation(
        Facing.DOWN, new_position
    )

    assert (
        walking_animation.keyframes[MOVEMENT_ANIMATION_DURATION].position
        == new_position
    )


def test_character_sprite_can_change_direction_if_one_already_started(
    character, restaurant_scene
):
    sprite = CharacterSprite(character, restaurant_scene.widget)
    x, y = sprite.position
    sprite.already_moving = True
    sprite.direction = Direction.DOWN.value

    sprite.start_moving(Direction.UP.value)

    assert sprite.direction == Direction.UP.value


def test_character_sprite_must_be_init_with_restaurant_widget(
    character, restaurant_scene
):
    sprite = CharacterSprite(character, restaurant_scene.widget)

    assert sprite.restaurant_widget is restaurant_scene.widget


def test_character_sprite_can_say_if_its_insite_the_restaurant(
    character, restaurant_scene
):
    _, (max_x, max_y) = restaurant_scene.widget.walkable_zone

    sprite = CharacterSprite(character, restaurant_scene.widget)

    assert sprite.is_inside_restaurant()

    sprite.position = max_x, max_y

    assert not sprite.is_inside_restaurant()


@pytest.mark.parametrize(
    "direction_value, postion_start_name",
    [
        [Direction.RIGHT.value, "topright"],
        [Direction.UP.value, "topright"],
        [Direction.LEFT.value, "bottomleft"],
        [Direction.DOWN.value, "bottomleft"],
    ],
)
@patch("dnk.display.character_sprite.CharacterSprite._get_walking_animation")
@patch("arcade.get_window")
def test_character_sprite_cannot_walk_outside_the_restaurant(
    _,
    get_walking_animation_mocked,
    direction_value,
    postion_start_name,
    character,
    restaurant_scene,
):
    postion_start = getattr(restaurant_scene.widget, postion_start_name)

    sprite = CharacterSprite(character, restaurant_scene.widget)

    sprite.position = postion_start

    sprite.start_moving(direction=direction_value)
    sprite.update()
    get_walking_animation_mocked.assert_called_with(
        direction_value["facing"], postion_start
    )


def test_character_sprite_spawns_at_a_carpet_position(
    character, restaurant_scene
):
    sprite = CharacterSprite(character, restaurant_scene.widget)

    assert sprite.center_x in [
        carpet.center_x for carpet in restaurant_scene.widget.carpets
    ]


@patch("dnk.display.character_sprite.CharacterSprite._get_walking_animation")
@patch("arcade.get_window")
def test_character_sprite_can_start_moving(
    _, get_walking_animation_mocked, character, restaurant_scene
):
    sprite = CharacterSprite(character, restaurant_scene.widget)

    start_x, start_y = sprite.position

    sprite.start_moving(direction=Direction.UP.value)

    # Should be called each frame to update the walking process
    sprite.update()

    get_walking_animation_mocked.assert_called_with(
        Facing.UP, (start_x, start_y + SPRITE_HEIGHT)
    )


@patch("dnk.display.character_sprite.CharacterSprite._get_walking_animation")
@patch("arcade.get_window")
def test_character_sprite_can_stop_moving(
    _, get_walking_animation_mocked, character, restaurant_scene
):
    sprite = CharacterSprite(character, restaurant_scene.widget)

    start_x, start_y = sprite.position
    # Tell sprite to go in a direction
    sprite.direction = Direction.UP.value

    # Stop the movement before init it (in the update)
    sprite.stop_moving(direction=Direction.UP.value)

    # Should be called each frame to update the walking process
    sprite.update()

    get_walking_animation_mocked.assert_not_called()


def test_character_sprite_has_a_sprite_representing_where_the_interaction_is(
    character, restaurant_scene
):
    sprite = CharacterSprite(character, restaurant_scene.widget)

    assert sprite.action_sprite.bottom == sprite.bottom + SPRITE_HEIGHT


def test_action_sprite_follows_the_character_sprite(
    character, restaurant_scene
):
    sprite = CharacterSprite(character, restaurant_scene.widget)

    current_action_sprite_pos = sprite.action_sprite.position
    sprite.position = (sprite.position[0] + 5, sprite.position[1])

    expected_position = (
        current_action_sprite_pos[0] + 5,
        current_action_sprite_pos[1],
    )
    assert sprite.action_sprite.position == expected_position


def test_action_sprite_follows_facing_of_the_character_sprite(
    character, restaurant_scene
):
    sprite = CharacterSprite(character, restaurant_scene.widget)

    sprite.facing = Facing.DOWN

    assert sprite.action_sprite.bottom == sprite.bottom - SPRITE_HEIGHT

    sprite.facing = Facing.LEFT

    assert sprite.action_sprite.center_x == sprite.center_x - SPRITE_WIDTH

    sprite.facing = Facing.RIGHT

    assert sprite.action_sprite.center_x == sprite.center_x + SPRITE_WIDTH


def test_character_can_interact_with_interactive_objects(
    character, restaurant_scene
):
    sprite = CharacterSprite(character, restaurant_scene.widget)

    cash_register = restaurant_scene.widget.cash_registers[0]

    sprite.center_x = cash_register.center_x
    sprite.bottom = cash_register.bottom + SPRITE_HEIGHT
    sprite.facing = Facing.DOWN

    assert sprite.can_interact_with() == [cash_register]

    cooking_station = restaurant_scene.widget.cooking_stations[0]

    sprite.center_x = cooking_station.center_x
    sprite.bottom = cooking_station.bottom - SPRITE_HEIGHT
    sprite.facing = Facing.UP

    assert sprite.can_interact_with() == [cooking_station]
