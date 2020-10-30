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
    SELECTION_COLOR,
)


class OrdersWindow(arcade.Sprite):
    def __init__(self, order_list_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        order_list_widget.sprites.append(self.frame_)

        if hasattr(order_list_widget, "anchor"):
            self.position = order_list_widget.anchor.position
            self.frame_.position = order_list_widget.anchor.position


class OrderDescription(arcade.Sprite):
    def __init__(
        self, order_list_widget, i, order, selected=False, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.order = order

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

        self.topleft = order_list_widget.widget_window.topleft
        self.bottom -= i * FONT_SIZE * 2

        if selected:
            self.frame_ = arcade.Sprite()
            self.frame_.texture = arcade.make_soft_square_texture(
                size=100,
                color=SELECTION_COLOR,
                center_alpha=255,
                outer_alpha=255,
            )
            self.frame_.width = self.width
            self.frame_.height = self.height
            self.frame_.position = self.position

            order_list_widget.sprites.append(self.frame_)


class OrderList(arcade_curtains.Widget):
    def setup_widget(self, scene, callback_once_finished):
        self.scene = scene
        self.orders = self.scene.restaurant.orders[:]
        self.callback_once_finished = callback_once_finished

        self._create_widget_window()
        self.needs_update = False
        self.i = 0

        self.order_list_events = EventGroup()
        for key, value in [(arcade.key.W, -1), (arcade.key.S, 1)]:
            self.order_list_events.key_down(
                key,
                self.move_cursor,
                {"value": value},
            )
        self.order_list_events.key_down(arcade.key.ENTER, self.tear_down)
        self.order_list_events.frame(self.update)
        self.scene.events.register_group(self.order_list_events)

    def _create_widget_window(self):
        self.widget_window = OrdersWindow(self)
        self.sprites.append(self.widget_window)

    def post_setup(self):
        for i, order in enumerate(self.orders):
            selected = i == self.i
            self.sprites.append(
                OrderDescription(self, i, order, selected=selected)
            )

    def move_cursor(self, value):
        if self.orders:
            i = (self.i + value) % len(self.orders)
            self.needs_update = i != self.i
            self.i = i

    def _erase_sprite_list(self):
        while self.sprites:
            self.sprites[0].kill()

    def tear_down(self):
        self._erase_sprite_list()

        self.order_list_events.disable()
        self.callback_once_finished()

    def erase_and_rewrite_list(self):
        self._erase_sprite_list()

        self._create_widget_window()
        self.post_setup()

    def update(self, *args, **kwargs):
        if self.orders != self.scene.restaurant.orders or self.needs_update:
            self.needs_update = False
            self.orders = self.scene.restaurant.orders[:]
            self.erase_and_rewrite_list()
