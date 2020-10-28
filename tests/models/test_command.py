import pytest

from dnk.models.command import Command, CommandTypes


@pytest.fixture(
    params=list(CommandTypes),
    ids=[
        f"CommandType={command_type.name}"
        for command_type in list(CommandTypes)
    ],
)
def command_type(request):
    return request.param


def test_command_has_all_data_needed(command_type):
    command = Command(command_type=command_type)
    values = command_type.value

    assert command.name == values["name"]
    assert command.base_preparation_time == values["base_preparation_time"]
    assert command.recipe == values["recipe"]


def test_get_random_command():
    assert isinstance(Command.get_random(), Command)
