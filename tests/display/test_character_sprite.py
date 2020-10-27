import os
import pytest

from dnk.models.character import Character
from dnk.display.character_sprite import (
    CharacterSprite,
    Direction,
    Facing,
    SPRITE_HEIGHT,
)


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


def test_character_sprite_can_move(character):
    sprite = CharacterSprite(character)

    x, y = sprite.position

    sprite.move(Direction.UP.value)

    assert sprite.position == (x, y + SPRITE_HEIGHT)


def test_character_sprite_updates_its_facing_and_default_is_up(character):
    sprite = CharacterSprite(character)

    assert sprite.facing == Facing.UP

    sprite.move(Direction.DOWN.value)

    assert sprite.facing == Facing.DOWN
