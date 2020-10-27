from dnk.display import load_restaurant


def test_restaurant_file_is_loadable_in_game():
    restaurant_name = "restaurant"

    restaurant = load_restaurant.load_restaurant_file(restaurant_name)

    expected_layers = {
        "floor_and_walls",
        "furniture",
        "cash_registers",
        "cooking_stations",
        "chairs",
        "carpets",
    }
    assert set(layer.name for layer in restaurant.layers) == expected_layers
