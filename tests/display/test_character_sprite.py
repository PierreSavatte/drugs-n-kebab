import os

import pytest

from dnk.display.character_sprite import (
    CharacterSprite,
    Direction,
    Facing,
    MOVEMENT_ANIMATION_DURATION,
)
from dnk.models.character import Character
from dnk.models.restaurant import Restaurant, RestaurantSizeType
from dnk.display.restaurant_scene import RestaurantScene


@pytest.fixture
def character(gender, ethnicity):
    return Character(gender=gender, ethnicity=ethnicity)


@pytest.fixture
def restaurant_scene():
    return RestaurantScene(
        restaurant=Restaurant(size_type=RestaurantSizeType.SMALL)
    )


def test_character_sprite_has_sprite_related_to_their_ethnicity(
    character, restaurant_scene
):
    sprite = CharacterSprite(character, restaurant_scene)

    expected_path = os.path.join(
        "restaurant",
        "characters",
        character.ethnicity.value,
        f"{character.gender.value}.png",
    )
    assert expected_path in sprite.sprite_path


def test_character_sprite_has_walking_animation(character, restaurant_scene):
    sprite = CharacterSprite(character, restaurant_scene)

    x, y = sprite.position
    walking_animation = sprite._get_walking_animation(
        Facing.DOWN, (x + 10, y + 10)
    )

    for time, facing, moving_mode in [
        (0, Facing.W_DOWN, True),
        (MOVEMENT_ANIMATION_DURATION / 2, Facing.W_DOWN_BIS, None),
        (MOVEMENT_ANIMATION_DURATION, Facing.DOWN, False),
    ]:
        callback_kwargs = walking_animation.callbacks[time].keywords
        expected_kwargs = {"new_facing": facing}
        if moving_mode is not None:
            expected_kwargs["moving_mode"] = moving_mode
        assert callback_kwargs == expected_kwargs


def test_character_sprite_animation_moves_sprite(character, restaurant_scene):
    sprite = CharacterSprite(character, restaurant_scene)
    x, y = sprite.position
    new_position = (x + 10, y + 10)

    walking_animation = sprite._get_walking_animation(
        Facing.DOWN, new_position
    )

    assert (
        walking_animation.keyframes[MOVEMENT_ANIMATION_DURATION].position
        == new_position
    )


def test_character_sprite_can_not_move_if_already_in_moving_mode(
    character, restaurant_scene
):
    sprite = CharacterSprite(character, restaurant_scene)
    x, y = sprite.position
    sprite.moving_mode = True

    sprite.move(Direction.DOWN.value)

    assert sprite.position == (x, y)


def test_character_sprite_must_be_init_with_restaurant(
    character, restaurant_scene
):
    sprite = CharacterSprite(character, restaurant_scene)

    assert sprite.restaurant_scene is restaurant_scene


def test_character_sprite_can_say_if_its_insite_the_restaurant(
    character, restaurant_scene
):
    _, (max_x, max_y) = restaurant_scene.walkable_zone

    sprite = CharacterSprite(character, restaurant_scene)

    assert sprite.is_inside_restaurant()

    sprite.position = max_x, max_y

    assert not sprite.is_inside_restaurant()


# def test_character_sprite_cannot_walk_outside_the_restaurant(
#     character, restaurant_scene
# ):
#     import arcade
#     import arcade_curtains
#
#     curtains = arcade_curtains.Curtains()
#     w = arcade.Window()
#     curtains.bind(w)
#     curtains.add_scene("restaurant_scene", restaurant_scene)
#     curtains.set_scene("restaurant_scene")
#
#     (min_x, min_y), (max_x, max_y) = restaurant_scene.walkable_zone
#
#     sprite = CharacterSprite(character, restaurant_scene)
#
#     # (max_x, max_y)
#     sprite.position = max_x, max_y
#
#     # 1
#     sprite.move(Direction.RIGHT.value)
#     assert sprite.position == (max_x, max_y)
#
#     # 2
#     sprite.move(Direction.UP.value)
#     assert sprite.position == (max_x, max_y)
#
#     # (max_x, max_y)
#     sprite.position = min_x, min_y
#
#     # 3
#     sprite.move(Direction.LEFT.value)
#     assert sprite.position == (min_x, min_y)
#
#     # 4
#     sprite.move(Direction.DOWN.value)
#     assert sprite.position == (min_x, min_y)


def test_character_sprite_spawns_at_a_carpet_position(
    character, restaurant_scene
):
    sprite = CharacterSprite(character, restaurant_scene)

    assert sprite.center_x in [
        carpet.center_x for carpet in restaurant_scene.carpets
    ]
