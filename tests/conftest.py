import pytest

from dnk.models import character
from dnk.models import restaurant


@pytest.fixture(
    params=list(character.Ethnicities),
    ids=[
        f"Ethnicity={ethnicity.name}"
        for ethnicity in list(character.Ethnicities)
    ],
)
def ethnicity(request):
    return request.param


@pytest.fixture(
    params=list(character.Genders),
    ids=[f"Gender={gender.name}" for gender in list(character.Genders)],
)
def gender(request):
    return request.param


@pytest.fixture(
    params=list(restaurant.RestaurantSizeType),
    ids=[
        f"RestaurantSize={restaurant_size.name}"
        for restaurant_size in list(restaurant.RestaurantSizeType)
    ],
)
def restaurant_size_type(request):
    return request.param
