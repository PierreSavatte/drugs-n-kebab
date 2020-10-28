import pytest
import arcade
from arcade_curtains import event

from unittest.mock import patch

from dnk.settings import (
    SPRITE_HEIGHT,
    SPRITE_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
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


def test_restaurant_scene_has_walkable_zone_defined_based_on_restaurant_size_and_position(
    restaurant,
):
    x, y = restaurant.size

    restaurant_scene = RestaurantScene(restaurant)

    half_restaurant_width = (y * SPRITE_WIDTH) // 2
    half_restaurant_height = (x * SPRITE_HEIGHT) // 2

    center_x, center_y = SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2

    assert restaurant_scene.walkable_zone == (
        (center_x - half_restaurant_width, center_y - half_restaurant_height),
        (center_x + half_restaurant_width, center_y + half_restaurant_height),
    )


@patch("dnk.display.restaurant_scene.CharacterSprite")
@patch("arcade.PhysicsEngineSimple")
@patch("arcade.tilemap.process_layer")
@patch("dnk.display.restaurant_scene.load_restaurant_file")
def test_restaurant_scene_loads_good_layers_depending_on_the_size(
    load_restaurant_file_mocked, _, __, ___, restaurant
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


def test_player_can_start_moving_in_restaurant(restaurant):
    restaurant_scene = RestaurantScene(restaurant)
    assert (
        restaurant_scene.player.start_moving,
        {"direction": Direction.UP.value},
    ) in restaurant_scene.events.handlers[(event.Event.KEY_DOWN, arcade.key.W)]
    assert (
        restaurant_scene.player.start_moving,
        {"direction": Direction.DOWN.value},
    ) in restaurant_scene.events.handlers[(event.Event.KEY_DOWN, arcade.key.S)]
    assert (
        restaurant_scene.player.start_moving,
        {"direction": Direction.LEFT.value},
    ) in restaurant_scene.events.handlers[(event.Event.KEY_DOWN, arcade.key.A)]
    assert (
        restaurant_scene.player.start_moving,
        {"direction": Direction.RIGHT.value},
    ) in restaurant_scene.events.handlers[(event.Event.KEY_DOWN, arcade.key.D)]


def test_player_can_stop_moving_in_restaurant(restaurant):
    restaurant_scene = RestaurantScene(restaurant)
    assert (
        restaurant_scene.player.stop_moving,
        {"direction": Direction.UP.value},
    ) in restaurant_scene.events.handlers[(event.Event.KEY_UP, arcade.key.W)]
    assert (
        restaurant_scene.player.stop_moving,
        {"direction": Direction.DOWN.value},
    ) in restaurant_scene.events.handlers[(event.Event.KEY_UP, arcade.key.S)]
    assert (
        restaurant_scene.player.stop_moving,
        {"direction": Direction.LEFT.value},
    ) in restaurant_scene.events.handlers[(event.Event.KEY_UP, arcade.key.A)]
    assert (
        restaurant_scene.player.stop_moving,
        {"direction": Direction.RIGHT.value},
    ) in restaurant_scene.events.handlers[(event.Event.KEY_UP, arcade.key.D)]


def test_character_sprite_keeps_walking_every_frame(restaurant):
    restaurant_scene = RestaurantScene(restaurant)
    assert (
        restaurant_scene.player.update,
        {},
    ) in restaurant_scene.events.handlers[event.Event.FRAME]


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
