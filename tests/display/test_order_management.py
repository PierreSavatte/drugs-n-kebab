from unittest.mock import patch

import pytest

from dnk.display.order_list import OrderList
from dnk.models.order import Order, OrderTypes


@pytest.fixture
def list_of_orders_the_restaurant_has(restaurant):
    restaurant.orders = [
        Order(OrderTypes.KEBAB),
        Order(OrderTypes.FRENCH_FRIES),
    ]
    return restaurant.orders


@pytest.fixture
def in_order_list(list_of_orders_the_restaurant_has, restaurant_scene):
    restaurant_scene.widget.remove_keyboard_events()
    restaurant_scene.in_sub_window = True
    order_list = OrderList(
        restaurant_scene.interactive_window_sprites,
        scene=restaurant_scene,
        callback_once_finished=restaurant_scene.end_interactive_window,
    )
    restaurant_scene.interactive_window = order_list

    return order_list


def test_order_list_needs_scene_and_callback(restaurant_scene):
    OrderList(
        restaurant_scene.interactive_window_sprites,
        scene=restaurant_scene,
        callback_once_finished=restaurant_scene.end_interactive_window,
    )


@patch("arcade.Sprite.get_adjusted_hit_box")
@patch("arcade.get_text_image")
def test_order_list_display_order_list(
    get_text_image,
    get_adjusted_hit_box,
    list_of_orders_the_restaurant_has,
    restaurant_scene,
):
    get_adjusted_hit_box.return_value = []
    OrderList(
        restaurant_scene.interactive_window_sprites,
        scene=restaurant_scene,
        callback_once_finished=restaurant_scene.end_interactive_window,
    )

    assert get_text_image.call_count == len(list_of_orders_the_restaurant_has)
