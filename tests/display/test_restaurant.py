import arcade

from dnk.display import restaurant
from dnk.display.character_sprite import CharacterSprite, Direction


def test_restaurant_holds_player():
    restaurant_scene = restaurant.RestaurantScene()

    assert isinstance(restaurant_scene.player, CharacterSprite)
    assert restaurant_scene.player in restaurant_scene.actors


def test_player_can_move_in_restaurant():
    restaurant_scene = restaurant.RestaurantScene()
    assert (
        restaurant_scene.player.move,
        {"direction": Direction.UP.value},
    ) in restaurant_scene.events.handlers[arcade.key.W]
    assert (
        restaurant_scene.player.move,
        {"direction": Direction.DOWN.value},
    ) in restaurant_scene.events.handlers[arcade.key.S]
    assert (
        restaurant_scene.player.move,
        {"direction": Direction.LEFT.value},
    ) in restaurant_scene.events.handlers[arcade.key.A]
    assert (
        restaurant_scene.player.move,
        {"direction": Direction.RIGHT.value},
    ) in restaurant_scene.events.handlers[arcade.key.D]
