import pytest

from dnk.display.order_list import OrderList


@pytest.fixture
def in_order_list(restaurant_scene):
    restaurant_scene.widget.remove_keyboard_events()
    restaurant_scene.in_sub_window = True
    order_list = OrderList(
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


def test_order_list_display_order_list(restaurant_scene):
    OrderList(
        restaurant_scene.interactive_window_sprites,
        scene=restaurant_scene,
        callback_once_finished=restaurant_scene.end_interactive_window,
    )


# def test_player_can_select_order_in_list_using_wasd_keys():
#     assert False


# def test_employee_can_take_an_order(
#     gender, ethnicity, restaurant_size_type, order_type
# ):
#     employee = Employee(gender.value, ethnicity.value)
#     restaurant = Restaurant(restaurant_size_type)
#     order = Order(order_type)
#     restaurant.orders = [order]
#
#     # employee.take_an_order(restaurant, order)
#     #
#     # assert restaurant.orders == []
#     # assert employee.customer_order == order
#     assert False
