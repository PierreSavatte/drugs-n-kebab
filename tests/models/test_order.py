from dnk.models.order import Order, OrderStatus


def test_order_has_all_data_needed(order_type):
    order = Order(order_type=order_type)
    values = order_type.value

    assert order.name == values["name"]
    assert order.base_preparation_time == values["base_preparation_time"]
    assert order.recipe == values["recipe"]


def test_get_random_order():
    assert isinstance(Order.get_random(), Order)


def test_order_has_status_and_default_is_in_line(order_type):
    order = Order(order_type=order_type)

    assert order.status == OrderStatus.IN_LINE


def test_order_can_format_recipe(order_type):
    order = Order(order_type=order_type)

    recipe_string = order.get_recipe_string()
    assert [
        ingredient.value in recipe_string and str(quantity) in recipe_string
        for ingredient, quantity in order.recipe.items()
    ]
