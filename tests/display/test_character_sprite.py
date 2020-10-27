import os

import pytest

from dnk.display.character_sprite import (
    CharacterSprite,
    Direction,
    Facing,
    MOVEMENT_ANIMATION_DURATION,
)
from dnk.models.character import Character


@pytest.fixture
def character(gender, ethnicity):
    return Character(gender=gender, ethnicity=ethnicity)


def test_character_sprite_has_sprite_related_to_their_ethnicity(character):
    sprite = CharacterSprite(character)

    expected_path = os.path.join(
        "restaurant",
        "characters",
        character.ethnicity.value,
        f"{character.gender.value}.png",
    )
    assert expected_path in sprite.sprite_path


def test_character_sprite_has_walking_animation(
    character,
):
    sprite = CharacterSprite(character)

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


def test_character_sprite_animation_moves_sprite(
    character,
):
    sprite = CharacterSprite(character)
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
    character,
):
    sprite = CharacterSprite(character)
    x, y = sprite.position
    sprite.moving_mode = True

    sprite.move(Direction.DOWN.value)

    assert sprite.position == (x, y)
