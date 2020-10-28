import random


class RandomlyInitialisable:
    expected_enums_at_init = []

    @classmethod
    def get_random(cls):
        values = [
            random.choice(list(enum)) for enum in cls.expected_enums_at_init
        ]
        return cls(*values)
