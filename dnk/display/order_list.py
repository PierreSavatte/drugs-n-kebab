import arcade
import arcade_curtains
from arcade_curtains.event import EventGroup

from dnk.settings import (
    FONTS,
    WIDGET_BACKGROUND_COLOR,
    WIDGET_FRAME_COLOR,
    WIDGET_FRAME_SIZE,
    FONT_SIZE,
    LINE_SEPARATION,
    MARGIN,
    TEXT_COLOR,
    WIDGET_WIDTH,
    WIDGET_HEIGHT,
    SELECTION_COLOR,
)

POSITION_ATTR_NAMES = [
    "position",
    "center_x",
    "center_y",
    "left",
    "right",
    "top",
    "bottom",
    "width",
    "height",
]


class Text(arcade.Sprite):
    def __init__(
        self,
        sprite_list,
        text,
        font_size=FONT_SIZE,
        text_color=None,
        highlight_color=None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        if not text_color:
            text_color = TEXT_COLOR

        self.text = text

        image = arcade.get_text_image(
            text=text,
            text_color=text_color,
            font_size=font_size,
            font_name=FONTS,
        )
        self._texture = arcade.Texture(text)
        self.texture.image = image

        self.width = image.width
        self.height = image.height

        self.highlighted = highlight_color
        if highlight_color:
            self.frame_ = arcade.Sprite()
            self.frame_.texture = arcade.make_soft_square_texture(
                size=100,
                color=highlight_color,
                center_alpha=255,
                outer_alpha=255,
            )
            self.frame_.width = self.width
            self.frame_.height = self.height

            sprite_list.append(self.frame_)
        sprite_list.append(self)

    def __setattr__(self, key, value):
        if hasattr(self, "highlighted") and self.highlighted:
            if key in POSITION_ATTR_NAMES:
                setattr(self.frame_, key, value)
        super().__setattr__(key, value)


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


class OrderList(arcade_curtains.Widget):
    def setup_widget(self, scene, callback_once_finished):
        self.scene = scene
        self.orders = self.scene.restaurant.orders[:]
        self.callback_once_finished = callback_once_finished

        self._create_widget_window()
        self.needs_update = False
        self.i = 0

        # ---
        # Events
        # ---
        self.order_list_events = EventGroup()
        # Movement events
        for key, value in [(arcade.key.W, -1), (arcade.key.S, 1)]:
            self.order_list_events.key_down(
                key,
                self.move_cursor,
                {"value": value},
            )
        # Tear-down events
        for key in [arcade.key.ENTER, arcade.key.ESCAPE]:
            self.order_list_events.key_down(key, self.tear_down, {"key": key})
        # Update event
        self.order_list_events.frame(self.update)
        # Register events group
        self.scene.events.register_group(self.order_list_events)

    def _create_widget_window(self):
        self.widget_window = OrdersWindow(self)
        self.sprites.append(self.widget_window)

    def post_setup(self):
        for i, order in enumerate(self.orders):
            name_text = Text(
                sprite_list=self.sprites,
                text=order.name.upper(),
                highlight_color=SELECTION_COLOR if i == self.i else None,
            )
            name_text.top = (
                self.anchor.center_y + self.widget_window.height / 2 - MARGIN
            )
            name_text.left = (
                self.anchor.center_x - self.widget_window.width / 2 + MARGIN
            )
            name_text.bottom -= i * FONT_SIZE * LINE_SEPARATION

            recipe_text = Text(
                sprite_list=self.sprites,
                text=order.get_recipe_string(),
                font_size=FONT_SIZE - 3,
            )
            recipe_text.bottom = name_text.bottom
            recipe_text.left = name_text.right + 10

    def move_cursor(self, value):
        if self.orders:
            i = (self.i + value) % len(self.orders)
            self.needs_update = i != self.i
            self.i = i

    def _erase_sprite_list(self):
        while self.sprites:
            self.sprites[0].kill()

    def tear_down(self, key):
        self._erase_sprite_list()

        self.order_list_events.disable()

        order_selected = (
            self.orders[self.i] if (key == arcade.key.ENTER) else None
        )
        self.callback_once_finished(order_selected=order_selected)

    def erase_and_rewrite_list(self):
        self._erase_sprite_list()

        self._create_widget_window()
        self.post_setup()

    def update(self, delta_time=None):
        if self.orders != self.scene.restaurant.orders or self.needs_update:
            self.needs_update = False
            self.orders = self.scene.restaurant.orders[:]
            self.erase_and_rewrite_list()
