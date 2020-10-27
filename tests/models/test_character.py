from unittest.mock import patch

import pytest

from dnk.models import character


@pytest.fixture(
    params=list(character.Ethnicities),
    ids=[
        f"PieceBlueprints.{ethnicity.name}"
        for ethnicity in list(character.Ethnicities)
    ],
)
def ethnicity(request):
    return request.param


@pytest.fixture(
    params=list(character.Genders),
    ids=[
        f"PieceBlueprints.{gender.name}" for gender in list(character.Genders)
    ],
)
def gender(request):
    return request.param


def test_character_initialization(gender, ethnicity):
    c = character.Character(gender=gender.value, ethnicity=ethnicity.value)
    assert c.ethnicity == ethnicity.value
    assert c.gender == gender.value


def test_character_can_be_init_with_a_name(gender, ethnicity):
    c = character.Character(
        gender=gender.value, ethnicity=ethnicity.value, name="This is my name"
    )
    assert c.name == "This is my name"


@patch("random.choice")
def test_character_has_name_related_to_their_ethnicity_if_no_name_given(
    mock_choice, gender, ethnicity
):
    mock_choice.side_effect = lambda x: x[0]

    c = character.Character(gender=gender.value, ethnicity=ethnicity.value)
    selected_name = character.ETHNICITY_NAMES[ethnicity][gender][0]

    assert c.name == selected_name
