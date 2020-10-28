from unittest.mock import patch

from dnk.display.load_sprites import get_character_sprites, Facing


@patch("arcade.load_texture")
def test_sprite_loading_loads_character_sheet(load_texture_mocked):
    sprite_path = "sprite/path/somewhere/to/the/sprite_sheet.png"
    load_texture_mocked.side_effect = range(len(Facing))

    character_sprites = get_character_sprites(sprite_path)

    assert all(
        character_sprites[facing] == i_called
        for i_called, facing in enumerate(
            [
                Facing.DOWN,
                Facing.UP,
                Facing.LEFT,
                Facing.RIGHT,
                Facing.W_DOWN,
                Facing.W_DOWN_BIS,
                Facing.W_UP,
                Facing.W_UP_BIS,
                Facing.W_LEFT,
                Facing.W_RIGHT,
                Facing.W_LEFT_BIS,
                Facing.W_RIGHT_BIS,
            ]
        )
    )
