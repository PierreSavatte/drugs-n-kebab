from unittest.mock import patch

import arcade
import pytest
from arcade_curtains.event import Event

from dnk.display.character_sprite import Facing, Direction
from dnk.settings import (
    SPRITE_HEIGHT,
)


@pytest.fixture
def cash_register(restaurant_scene):
    return restaurant_scene.restaurant_window.cash_registers[0]


@pytest.fixture
def place_player_in_front_of_cash_register(restaurant_window, cash_register):
    # Correctly position the character
    restaurant_window.player_sprite.center_x = cash_register.center_x
    restaurant_window.player_sprite.bottom = (
        cash_register.bottom + SPRITE_HEIGHT
    )
    restaurant_window.player_sprite.facing = Facing.DOWN


def test_display_sub_window_when_user_hits_e(restaurant_scene):
    assert (
        restaurant_scene.start_interactive_window,
        {},
    ) in restaurant_scene.events.event_group.handlers[
        (Event.KEY_DOWN, arcade.key.E)
    ]


@patch("dnk.display.restaurant_scene.OrderList")
def test_order_list_is_displayed_when_user_interacts_with_cashregister(
    order_list,
    restaurant_scene,
    cash_register,
    place_player_in_front_of_cash_register,
):
    assert (
        restaurant_scene.restaurant_window.player_sprite.can_interact_with()
        == [cash_register]
    )

    # Is called after the player hits the 'e' key
    restaurant_scene.start_interactive_window()

    order_list.assert_called_once()


@patch("dnk.display.restaurant_scene.OrderList")
def test_order_list_is_not_displayed_when_user_interacts_with_nothing(
    order_list, restaurant_scene
):
    assert (
        restaurant_scene.restaurant_window.player_sprite.can_interact_with()
        == []
    )

    # Is called after the player hits the 'e' key
    restaurant_scene.start_interactive_window()

    order_list.assert_not_called()


def test_setting_order_list_will_delete_the_events_for_user_to_move(
    restaurant_scene,
    cash_register,
    place_player_in_front_of_cash_register,
):
    # Is called after the player hits the 'e' key
    restaurant_scene.start_interactive_window()

    restaurant_window = restaurant_scene.restaurant_window

    for key, direction in [
        (arcade.key.W, Direction.UP.value),
        (arcade.key.S, Direction.DOWN.value),
        (arcade.key.A, Direction.LEFT.value),
        (arcade.key.D, Direction.RIGHT.value),
    ]:
        assert (
            restaurant_window.player_sprite.start_moving,
            {"direction": direction},
        ) not in restaurant_scene.events.event_group.handlers[
            (Event.KEY_DOWN, key)
        ]

        assert (
            restaurant_window.player_sprite.stop_moving,
            {"direction": direction},
        ) not in restaurant_scene.events.event_group.handlers[
            (Event.KEY_UP, key)
        ]
