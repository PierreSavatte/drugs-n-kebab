from enum import Enum

from dnk.models import RandomlyInitialisable


class CommandType(Enum):
    KEBAB = "kebab"
    FRENCH_FRIES = "french fries"


class Command(RandomlyInitialisable):
    expected_enums_at_init = [CommandType]

    def __init__(self, command_type):
        self.name = command_type.value
