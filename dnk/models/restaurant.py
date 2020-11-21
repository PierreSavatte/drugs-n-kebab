from enum import Enum
import time

from dnk.models import RandomlyInitialisable
from dnk.models.order import Order
from dnk.settings import ORDER_FREQUENCY, FIRST_ORDER_DELAY, ORDER_LIMIT


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

        self.last_ts_received_order = (
            time.time() + FIRST_ORDER_DELAY
        )  # Let the player breath at the beginning
        self.orders = []

    def update(self):
        now = time.time()
        if now >= self.last_ts_received_order + ORDER_FREQUENCY:
            self.last_ts_received_order = now
            if len(self.orders) < ORDER_LIMIT:
                self.orders.append(Order.get_random())
