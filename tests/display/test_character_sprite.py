from dnk.models.character import Character
from dnk.display.character_sprite import CharacterSprite


def test_character_has_sprite_related_to_their_ethnicity(gender, ethnicity):
    c = Character(gender=gender.value, ethnicity=ethnicity.value)

    sprite = CharacterSprite(c)

    assert (
        sprite.sprite_path
        == f"restaurant/characters/{ethnicity.value}/{gender.value}.png"
    )
