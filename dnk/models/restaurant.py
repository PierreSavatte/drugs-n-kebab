from dnk.models import RandomlyGettableEnum


class RestaurantSizeType(RandomlyGettableEnum):
    BIG = "big"
    MEDIUM = "medium"
    SMALL = "small"


SIZE_SIZE_TYPE_MAPPING = {
    RestaurantSizeType.BIG: (20, 20),
    RestaurantSizeType.MEDIUM: (15, 15),
    RestaurantSizeType.SMALL: (10, 10),
}


class Restaurant:
    def __init__(self, size_type):
        self.size_type = size_type
        self.size = SIZE_SIZE_TYPE_MAPPING[size_type]
