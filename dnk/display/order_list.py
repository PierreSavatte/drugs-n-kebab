import time
import arcade
import arcade_curtains
from arcade_curtains.event import EventGroup

from dnk.settings import (
    FONTS,
    WIDGET_BACKGROUND_COLOR,
    WIDGET_FRAME_COLOR,
    WIDGET_FRAME_SIZE,
    FONT_SIZE,
    WIDGET_WIDTH,
    WIDGET_HEIGHT,
)


class OrdersWindow(arcade.Sprite):
    def __init__(self, order_list_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.order_list_widget = order_list_widget

        self.texture = arcade.make_soft_square_texture(
            size=100,
            color=WIDGET_BACKGROUND_COLOR,
            center_alpha=255,
            outer_alpha=255,
        )
        self.width = WIDGET_WIDTH
        self.height = WIDGET_HEIGHT

        self.frame_ = arcade.Sprite()
        self.frame_.texture = arcade.make_soft_square_texture(
            size=100,
            color=WIDGET_FRAME_COLOR,
            center_alpha=255,
            outer_alpha=255,
        )
        self.frame_.width = WIDGET_WIDTH + WIDGET_FRAME_SIZE
        self.frame_.height = WIDGET_HEIGHT + WIDGET_FRAME_SIZE
        self.order_list_widget.sprites.append(self.frame_)

        if hasattr(order_list_widget, "anchor"):
            self.position = order_list_widget.anchor.position
            self.frame_.position = order_list_widget.anchor.position


class OrderDescription(arcade.Sprite):
    def __init__(self, order_list_widget, i, order, *args, **kwargs):
        super().__init__(*args, **kwargs)

        image = arcade.get_text_image(
            text=order.name,
            text_color=(0, 0, 0),
            font_size=FONT_SIZE,
            font_name=FONTS,
        )
        self._texture = arcade.Texture(order.name)
        self.texture.image = image

        self.width = image.width
        self.height = image.height

        self.position = order_list_widget.anchor.position

        self.bottom -= i * FONT_SIZE


class OrderList(arcade_curtains.Widget):
    def setup_widget(self, scene, callback_once_finished):
        self.scene = scene
        self.orders = self.scene.restaurant.orders[:]
        self.callback_once_finished = callback_once_finished

        self.widget_window = OrdersWindow(self)
        self.sprites.append(self.widget_window)
        self.i = 0

        self.order_list_events = EventGroup()
        for key, value in [(arcade.key.W, 1), (arcade.key.S, -1)]:
            self.order_list_events.key_down(
                key,
                self.move_cursor,
                {"value": value},
            )
        self.order_list_events.key_down(arcade.key.ENTER, self.tear_down)
        self.order_list_events.frame(self.update)
        self.scene.events.register_group(self.order_list_events)

        self.todelete = time.time()

    def post_setup(self):
        for i, order in enumerate(self.orders):
            self.sprites.append(OrderDescription(self, i, order))

    def move_cursor(self, value):
        if self.orders:
            self.i = (self.i + value) % len(self.orders)

    def _erase_sprite_list(self):
        while self.sprites:
            self.sprites.pop()

    def tear_down(self):
        self._erase_sprite_list()

        self.order_list_events.disable()
        self.scene.events.remove_key_down(arcade.key.ENTER, self.tear_down)
        self.scene.events.remove_frame(self.update)

        self.callback_once_finished()

    def erase_and_rewrite_list(self):
        self._erase_sprite_list()

        self.sprites.append(OrdersWindow(self))
        for i, order in enumerate(self.orders):
            self.sprites.append(OrderDescription(self, i, order))

    def update(self, *args, **kwargs):
        if self.orders != self.scene.restaurant.orders:
            self.orders = self.scene.restaurant.orders[:]
            self.erase_and_rewrite_list()
