from enum import Enum

from dnk.models import RandomlyInitialisable


class RestaurantSizeType(Enum):
    BIG = "big"
    MEDIUM = "medium"
    SMALL = "small"


SIZE_SIZE_TYPE_MAPPING = {
    RestaurantSizeType.BIG: (20, 20),
    RestaurantSizeType.MEDIUM: (15, 15),
    RestaurantSizeType.SMALL: (10, 10),
}


class Restaurant(RandomlyInitialisable):
    expected_enums_at_init = [RestaurantSizeType]

    def __init__(self, size_type):
        self.size_type = size_type
        self.size = SIZE_SIZE_TYPE_MAPPING[size_type]
