import pytest

from dnk.models.order import Order, OrderTypes


@pytest.fixture(
    params=list(OrderTypes),
    ids=[f"OrderType={order_type.name}" for order_type in list(OrderTypes)],
)
def order_type(request):
    return request.param


def test_order_has_all_data_needed(order_type):
    order = Order(order_type=order_type)
    values = order_type.value

    assert order.name == values["name"]
    assert order.base_preparation_time == values["base_preparation_time"]
    assert order.recipe == values["recipe"]


def test_get_random_order():
    assert isinstance(Order.get_random(), Order)
