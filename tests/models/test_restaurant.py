import pytest

from dnk.models import restaurant


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
