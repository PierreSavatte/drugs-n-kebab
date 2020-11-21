import time

import freezegun
import pytest

from dnk.models import restaurant
from dnk.settings import ORDER_FREQUENCY, ORDER_LIMIT
from dnk.models.order import Order


def test_restaurant_has_different_sizes(restaurant_size_type):
    r = restaurant.Restaurant(size_type=restaurant_size_type)

    assert r.size_type == restaurant_size_type


def test_get_random_restaurant():
    assert isinstance(
        restaurant.Restaurant.get_random(),
        restaurant.Restaurant,
    )


@pytest.mark.parametrize(
    "restaurant_size_type, expected_size",
    zip(
        [
            restaurant.RestaurantSizeType.SMALL,
            restaurant.RestaurantSizeType.MEDIUM,
            restaurant.RestaurantSizeType.BIG,
        ],
        [10, 15, 20],
    ),
)
def test_restaurant_has_size_value_depending_on_its_restaurant_size(
    restaurant_size_type, expected_size
):
    r = restaurant.Restaurant(size_type=restaurant_size_type)

    assert r.size == (expected_size, expected_size)


@freezegun.freeze_time("2020-10-28 18:24")
def test_restaurant_receive_order_frequently(restaurant_size_type):
    r = restaurant.Restaurant(size_type=restaurant_size_type)

    r.last_ts_received_order = time.time() - ORDER_FREQUENCY
    assert not r.orders

    r.update()

    assert len(r.orders) and isinstance(r.orders[0], Order)
    assert r.last_ts_received_order == time.time()


def test_restaurant_can_not_receive_more_than_max_orders(restaurant_size_type):
    r = restaurant.Restaurant(size_type=restaurant_size_type)
    original_orders = [Order.get_random() for _ in range(ORDER_LIMIT)]

    # Copy original orders in the restaurant.orders
    r.orders = original_orders[:]
    r.last_ts_received_order = time.time() - ORDER_FREQUENCY

    r.update()

    assert r.orders == original_orders
