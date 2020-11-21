import pytest

from dnk.display.restaurant_scene import RestaurantScene
from dnk.models.character import Character
from dnk.models.restaurant import Restaurant


@pytest.fixture
def character(random_gender, random_ethnicity):
    return Character(gender=random_gender, ethnicity=random_ethnicity)


@pytest.fixture
def restaurant(restaurant_size_type):
    return Restaurant(restaurant_size_type)


@pytest.fixture
def restaurant_scene(restaurant):
    return RestaurantScene(restaurant)


@pytest.fixture
def restaurant_window(restaurant_scene):
    return restaurant_scene.restaurant_window
