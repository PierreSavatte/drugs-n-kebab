import random
from enum import Enum


class RandomlyGettableEnum(Enum):
    @classmethod
    def get_random(cls):
        return random.choice(list(cls))
