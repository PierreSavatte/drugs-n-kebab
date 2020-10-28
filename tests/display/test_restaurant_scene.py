import pytest
import arcade

from unittest.mock import patch

from dnk.settings import SPRITE_HEIGHT, SPRITE_WIDTH
from dnk.models.restaurant import Restaurant
from dnk.display.restaurant_scene import RestaurantScene
from dnk.display.character_sprite import CharacterSprite, Direction
from dnk.display.load_restaurant import RestaurantLayers


@pytest.fixture
def restaurant(restaurant_size_type):
    return Restaurant(restaurant_size_type)


def test_restaurant_scene_takes_a_model_to_be_init(restaurant):
    restaurant_scene = RestaurantScene(restaurant)

    assert restaurant_scene.restaurant == restaurant


def test_restaurant_scene_has_size_defined_based_on_restaurant_size(
    restaurant,
):
    x, y = restaurant.size

    restaurant_scene = RestaurantScene(restaurant)

    assert restaurant_scene.walkable_zone == (
        (0, 0),
        (x * SPRITE_HEIGHT, y * SPRITE_WIDTH),
    )


@patch("arcade.tilemap.process_layer")
@patch("dnk.display.restaurant_scene.load_restaurant_file")
def test_restaurant_scene_loads_good_layers_depending_on_the_size(
    load_restaurant_file_mocked, _, restaurant
):
    size_name = restaurant.size_type.value

    RestaurantScene(restaurant)

    load_restaurant_file_mocked.assert_called_once_with(
        f"{size_name}_restaurant"
    )


def test_restaurant_scene_holds_player(restaurant):
    restaurant_scene = RestaurantScene(restaurant)

    assert isinstance(restaurant_scene.player, CharacterSprite)
    assert restaurant_scene.player in restaurant_scene.actors


def test_player_can_move_in_restaurant(restaurant):
    restaurant_scene = RestaurantScene(restaurant)
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


def test_restaurant_scene_holds_all_the_layers(restaurant):
    restaurant_scene = RestaurantScene(restaurant)

    assert restaurant_scene.all_layers.keys() == {
        layer.value["name"] for layer in list(RestaurantLayers)
    }


def test_restaurant_scene_define_good_layers_as_collidable(restaurant):
    restaurant_scene = RestaurantScene(restaurant)

    assert isinstance(restaurant_scene.collidable_layers, arcade.SpriteList)
    assert set(restaurant_scene.collidable_layers) == set(
        [
            *restaurant_scene.cooking_stations,
            *restaurant_scene.cash_registers,
            *restaurant_scene.furniture,
        ]
    )
