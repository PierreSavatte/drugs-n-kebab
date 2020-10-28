import random
from enum import Enum


class RandomlyGettable(Enum):
    @classmethod
    def get_random(cls):
        return random.choice(list(cls))
