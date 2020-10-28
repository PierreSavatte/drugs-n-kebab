from dnk.models import RandomlyGettable


class RestaurantSize(RandomlyGettable):
    BIG = "big"
    MEDIUM = "medium"
    SMALL = "small"


class Restaurant:
    def __init__(self, size):
        self.size = size
