from unittest.mock import patch, Mock

import arcade
import pytest
from arcade_curtains import event

from dnk.display.order_list import OrderList, Text
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

    nb_orders = len(list_of_orders_the_restaurant_has)
    # The name of the order and the recipe
    nb_calls = nb_orders * 2

    assert get_text_image.call_count == nb_calls

    orders_names = [
        order.name.upper() for order in list_of_orders_the_restaurant_has
    ]
    orders_recipes = [
        order.get_recipe_string()
        for order in list_of_orders_the_restaurant_has
    ]
    texts_displayed = sorted(
        [call[1]["text"] for call in get_text_image.call_args_list]
    )
    assert texts_displayed == sorted([*orders_names, *orders_recipes])


def test_order_list_can_be_closed_when_clicked_on_enter(
    restaurant_scene, restaurant_window
):
    order_list = OrderList(
        restaurant_scene.interactive_window_sprites,
        scene=restaurant_scene,
        callback_once_finished=restaurant_scene.end_interactive_window,
    )

    # Getting the order_list_events group
    # Is init after the player_movement_events event group
    event_group = restaurant_scene.events.event_groups[2]
    assert (
        order_list.tear_down,
        {},
    ) in event_group.handlers[(event.Event.KEY_DOWN, arcade.key.ENTER)]


@patch("arcade.get_window")
def test_order_list_when_closed_use_the_callback(
    _, restaurant_scene, restaurant_window
):
    callback_once_finished = Mock()
    order_list = OrderList(
        restaurant_scene.interactive_window_sprites,
        scene=restaurant_scene,
        callback_once_finished=callback_once_finished,
    )
    # Getting the player_movement_events group
    order_list.tear_down()

    callback_once_finished.assert_called_once()


@patch("arcade.Sprite.get_adjusted_hit_box")
@patch("arcade.get_text_image")
@patch("arcade.get_window")
def test_order_list_deletes_its_sprites_when_closed(
    _,
    __,
    get_adjusted_hit_box,
    list_of_orders_the_restaurant_has,
    restaurant_scene,
):
    get_adjusted_hit_box.return_value = []
    order_list = OrderList(
        restaurant_scene.interactive_window_sprites,
        scene=restaurant_scene,
        callback_once_finished=restaurant_scene.end_interactive_window,
    )

    window_and_frame = 2
    order_names_and_desc = len(list_of_orders_the_restaurant_has) * 2
    select_highlighting = 1
    assert (
        len(order_list.sprites)
        == order_names_and_desc + window_and_frame + select_highlighting
    )
    assert (
        len(restaurant_scene.interactive_window_sprites)
        == order_names_and_desc + window_and_frame + select_highlighting
    )

    # Close the window using enter
    order_list.tear_down()
    assert len(order_list.sprites) == 0
    assert len(restaurant_scene.interactive_window_sprites) == 0


def test_order_list_highlight_selected_order(
    list_of_orders_the_restaurant_has,
    restaurant_scene,
):
    order_list = OrderList(
        restaurant_scene.interactive_window_sprites,
        scene=restaurant_scene,
        callback_once_finished=restaurant_scene.end_interactive_window,
    )

    selected_order = list_of_orders_the_restaurant_has[order_list.i]

    (text_selected_order,) = [
        sprite
        for sprite in order_list.sprites
        if isinstance(sprite, Text)
        and sprite.text == selected_order.name.upper()
    ]
    other_orders = [
        sprite
        for sprite in order_list.sprites
        if isinstance(sprite, Text)
        and sprite.text != selected_order.name.upper()
    ]

    assert (
        hasattr(text_selected_order, "frame_")
        and isinstance(text_selected_order.frame_, arcade.Sprite)
        and text_selected_order.frame_ in order_list.sprites
    )

    assert all(not hasattr(order, "frame_") for order in other_orders)
