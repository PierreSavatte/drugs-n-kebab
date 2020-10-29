import time
from unittest.mock import patch

import arcade
import freezegun
import pytest
from arcade_curtains import event

from dnk.display.character_sprite import CharacterSprite, Direction
from dnk.display.load_restaurant import RestaurantLayers
from dnk.display.notification import Notification
from dnk.display.restaurant_scene import RestaurantScene
from dnk.models.restaurant import Restaurant
from dnk.settings import (
    SPRITE_HEIGHT,
    SPRITE_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    ORDER_FREQUENCY,
    NOTIFICATION_ANIMATION_DURATION,
    NOTIFICATION_WAITING_DURATION,
)


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

    assert restaurant_scene.widget.walkable_zone == (
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


def test_restaurant_widget_holds_player(restaurant_widget):

    assert isinstance(restaurant_widget.player, CharacterSprite)
    assert restaurant_widget.player in restaurant_widget.actors


def test_player_can_start_moving_in_restaurant(
    restaurant_scene, restaurant_widget
):
    assert (
        restaurant_widget.player.start_moving,
        {"direction": Direction.UP.value},
    ) in restaurant_scene.events.handlers[(event.Event.KEY_DOWN, arcade.key.W)]
    assert (
        restaurant_widget.player.start_moving,
        {"direction": Direction.DOWN.value},
    ) in restaurant_scene.events.handlers[(event.Event.KEY_DOWN, arcade.key.S)]
    assert (
        restaurant_widget.player.start_moving,
        {"direction": Direction.LEFT.value},
    ) in restaurant_scene.events.handlers[(event.Event.KEY_DOWN, arcade.key.A)]
    assert (
        restaurant_widget.player.start_moving,
        {"direction": Direction.RIGHT.value},
    ) in restaurant_scene.events.handlers[(event.Event.KEY_DOWN, arcade.key.D)]


def test_player_can_stop_moving_in_restaurant(
    restaurant_scene, restaurant_widget
):
    assert (
        restaurant_widget.player.stop_moving,
        {"direction": Direction.UP.value},
    ) in restaurant_scene.events.handlers[(event.Event.KEY_UP, arcade.key.W)]
    assert (
        restaurant_widget.player.stop_moving,
        {"direction": Direction.DOWN.value},
    ) in restaurant_scene.events.handlers[(event.Event.KEY_UP, arcade.key.S)]
    assert (
        restaurant_widget.player.stop_moving,
        {"direction": Direction.LEFT.value},
    ) in restaurant_scene.events.handlers[(event.Event.KEY_UP, arcade.key.A)]
    assert (
        restaurant_widget.player.stop_moving,
        {"direction": Direction.RIGHT.value},
    ) in restaurant_scene.events.handlers[(event.Event.KEY_UP, arcade.key.D)]


@patch("arcade.get_window")
@patch("dnk.display.character_sprite.CharacterSprite.update")
def test_character_sprite_keeps_walking_every_frame(
    character_sprite_update_method, _, restaurant_scene, restaurant_widget
):
    assert (
        restaurant_widget.update,
        {},
    ) in restaurant_scene.events.handlers[event.Event.FRAME]

    restaurant_widget.update()

    character_sprite_update_method.assert_called_once()


def test_restaurant_scene_holds_all_the_layers(restaurant_widget):
    assert restaurant_widget.all_layers.keys() == {
        layer.value["name"] for layer in list(RestaurantLayers)
    }


def test_restaurant_scene_define_good_layers_as_collidable(restaurant_widget):

    assert isinstance(restaurant_widget.collidable_layers, arcade.SpriteList)
    assert set(restaurant_widget.collidable_layers) == set(
        [
            *restaurant_widget.cooking_stations,
            *restaurant_widget.cash_registers,
            *restaurant_widget.furniture,
        ]
    )


@patch("dnk.models.restaurant.Restaurant.update")
def test_restaurant_widget_update_calls_restaurant_update(
    restaurant_update_method, restaurant
):
    restaurant_scene = RestaurantScene(restaurant)
    widget = restaurant_scene.widget
    assert (
        widget.update,
        {},
    ) in restaurant_scene.events.handlers[event.Event.FRAME]

    widget.update()

    restaurant_update_method.assert_called_once()


@patch("arcade.get_window")
@freezegun.freeze_time("2020-10-28 18:24")
def test_restaurant_widget_triggers_a_notification_when_order_received(
    _,
    restaurant,
):
    restaurant_scene = RestaurantScene(restaurant)
    restaurant.last_ts_received_order = time.time() - ORDER_FREQUENCY

    assert not restaurant_scene.widget.notifications_sprites

    restaurant_scene.widget.update()

    assert (
        len(restaurant_scene.widget.notifications_sprites) == 1
    ) and isinstance(
        restaurant_scene.widget.notifications_sprites[0], Notification
    )


@patch("arcade.get_window")
@freezegun.freeze_time("2020-10-28 18:24")
def test_restaurant_widget_deletes_notification_when_notification_is_finished(
    _,
    restaurant,
):
    restaurant_scene = RestaurantScene(restaurant)

    # Notification was created, and is ready to be deleted
    notification = Notification(target=restaurant_scene.sprites[0])
    notification.time_triggered = (
        time.time()
        - NOTIFICATION_ANIMATION_DURATION
        - NOTIFICATION_WAITING_DURATION
    )
    restaurant_scene.widget.sprites.append(notification)

    restaurant_scene.widget.update()

    assert notification not in restaurant_scene.widget.sprites
    assert notification not in restaurant_scene.sprites
