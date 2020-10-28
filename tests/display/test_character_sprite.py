import os

from unittest.mock import patch
import pytest

from dnk.settings import SPRITE_HEIGHT
from dnk.display.character_sprite import (
    CharacterSprite,
    Direction,
    Facing,
    MOVEMENT_ANIMATION_DURATION,
)
from dnk.display.restaurant_scene import RestaurantScene
from dnk.models.character import Character
from dnk.models.restaurant import Restaurant, RestaurantSizeType


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


def test_character_sprite_can_change_direction_if_one_already_started(
    character, restaurant_scene
):
    sprite = CharacterSprite(character, restaurant_scene)
    x, y = sprite.position
    sprite.already_moving = True
    sprite.direction = Direction.DOWN.value

    sprite.start_moving(Direction.UP.value)

    assert sprite.direction == Direction.UP.value


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
    postion_start = getattr(restaurant_scene, postion_start_name)

    sprite = CharacterSprite(character, restaurant_scene)

    sprite.position = postion_start

    sprite.start_moving(direction=direction_value)
    sprite.update()
    get_walking_animation_mocked.assert_called_with(
        direction_value["facing"], postion_start
    )


def test_character_sprite_spawns_at_a_carpet_position(
    character, restaurant_scene
):
    sprite = CharacterSprite(character, restaurant_scene)

    assert sprite.center_x in [
        carpet.center_x for carpet in restaurant_scene.carpets
    ]


@patch("dnk.display.character_sprite.CharacterSprite._get_walking_animation")
@patch("arcade.get_window")
def test_character_sprite_can_start_moving(
    _, get_walking_animation_mocked, character, restaurant_scene
):
    sprite = CharacterSprite(character, restaurant_scene)

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
    sprite = CharacterSprite(character, restaurant_scene)

    start_x, start_y = sprite.position
    # Tell sprite to go in a direction
    sprite.direction = Direction.UP.value

    # Stop the movement before init it (in the update)
    sprite.stop_moving(direction=Direction.UP.value)

    # Should be called each frame to update the walking process
    sprite.update()

    get_walking_animation_mocked.assert_not_called()
