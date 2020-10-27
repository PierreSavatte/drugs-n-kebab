import pytest

from dnk.models import character


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
