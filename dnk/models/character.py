import random

from dnk.models import RandomlyGettable


class Ethnicities(RandomlyGettable):
    AFRICAN = "african"
    FRENCH = "french"
    JAPANESE = "japanese"


class Genders(RandomlyGettable):
    WOMAN = "woman"
    MAN = "man"


ETHNICITY_NAMES = {
    Ethnicities.AFRICAN: {
        Genders.WOMAN: ["Vumi", "Ima"],
        Genders.MAN: ["Elikia", "Nsi"],
    },
    Ethnicities.FRENCH: {
        Genders.WOMAN: ["Marie", "Lucie"],
        Genders.MAN: ["Claude", "Quentin"],
    },
    Ethnicities.JAPANESE: {
        Genders.WOMAN: ["Hisae", "Yumiko"],
        Genders.MAN: ["Genjiro", "Ryoichi"],
    },
}


class Character:
    def __init__(self, gender, ethnicity, name=None):
        self.gender = gender
        self.ethnicity = ethnicity
        self.name = name or self._random_name()

    def _random_name(self):
        e = Ethnicities(self.ethnicity)
        g = Genders(self.gender)
        return random.choice(ETHNICITY_NAMES[e][g])
