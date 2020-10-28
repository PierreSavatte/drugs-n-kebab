from dnk.models.command import Command, CommandType


def test_command_has_name():
    command = Command(command_type=CommandType.KEBAB)

    assert command.name == "kebab"


def test_get_random_command():
    assert isinstance(Command.get_random(), Command)
