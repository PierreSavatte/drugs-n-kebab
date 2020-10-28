from dnk.models import restaurant


def test_restaurant_has_different_sizes(restaurant_size):
    r = restaurant.Restaurant(size=restaurant_size)

    assert r.size == restaurant_size


def test_get_random_ethnicity():
    assert isinstance(
        restaurant.RestaurantSize.get_random(), restaurant.RestaurantSize
    )
