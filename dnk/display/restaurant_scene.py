import random

import arcade
from arcade_curtains import BaseScene, Widget
from arcade_curtains.event import EventGroup

from dnk.display import exit_game
from dnk.display.character_sprite import CharacterSprite, Direction
from dnk.display.load_restaurant import load_restaurant_file, RestaurantLayers
from dnk.display.notification import Notification
from dnk.display.order_list import OrderList
from dnk.models.character import Character
from dnk.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from dnk.settings import SPRITE_SCALING


class RestaurantScene(BaseScene):
    def setup(self, restaurant=None):
        self.restaurant = restaurant

        self.restaurant_sprites = arcade.SpriteList()
        self.restaurant_window = RestaurantWidget(
            self.restaurant_sprites,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            scene=self,
        )

        self.interactive_window_sprites = arcade.SpriteList()
        self.in_sub_window = False
        self.interactive_window = None

        self.events.key_down(arcade.key.ESCAPE, exit_game)
        self.events.key_down(arcade.key.E, self.start_interactive_window)

    def start_interactive_window(self):
        for (
            interactive_sprite
        ) in self.restaurant_window.player.can_interact_with():
            if interactive_sprite in self.restaurant_window.cash_registers:
                self.restaurant_window.player_movement_events.disable()
                self.in_sub_window = True
                self.interactive_window = OrderList(
                    self.interactive_window_sprites,
                    scene=self,
                    callback_once_finished=self.end_interactive_window,
                )

    def end_interactive_window(self):
        self.restaurant_window.player_movement_events.enable()
        self.in_sub_window = False
        self.interactive_window = None

    def enter_scene(self, previous_scene):
        arcade.set_background_color(arcade.color.WHITE)


class RestaurantWidget(Widget):
    def update(self, *args, **kwargs):
        if not self.scene.in_sub_window:
            # Let the player continue walking
            self.player.update()

        # Updates the restaurant (maybe receive an order)
        nb_orders = len(self.scene.restaurant.orders)
        self.scene.restaurant.update()

        # Add notifications
        if len(self.scene.restaurant.orders) > nb_orders:
            cash_register = random.choice(self.cash_registers)
            notification = Notification(cash_register)
            self.sprites.append(notification)

        # Remove notifications
        for sprite in self.notifications_sprites:
            if sprite.is_ready_to_be_deleted:
                self.sprites.remove(sprite)

    @property
    def notifications_sprites(self):
        return [
            sprite
            for sprite in self.sprites
            if isinstance(sprite, Notification)
        ]

    def setup_widget(self, scene):
        self.scene = scene

        # Restaurant layers (floor, walls, furniture, ...)
        restaurant_map = load_restaurant_file(
            f"{self.scene.restaurant.size_type.value}_restaurant"
        )
        self.collidable_layers = arcade.SpriteList()
        for layer_setting in RestaurantLayers.ordered():
            layer_name = layer_setting.value["name"]
            layer = arcade.tilemap.process_layer(
                map_object=restaurant_map,
                layer_name=layer_name,
                scaling=SPRITE_SCALING,
            )
            setattr(self, layer_name, layer)
            if layer_setting.value["collidable"]:
                self.collidable_layers.extend(layer)
            self.sprites.extend(layer)

        # Actors
        self.actors = arcade.SpriteList()
        self.player = CharacterSprite(Character.get_random(), self)
        self.actors.append(self.player)

        self.sprites.extend(self.actors)

        # Events
        self.scene.events.frame(self.update)

        self.player_movement_events = EventGroup()
        for key, direction in [
            (arcade.key.W, Direction.UP),
            (arcade.key.S, Direction.DOWN),
            (arcade.key.D, Direction.RIGHT),
            (arcade.key.A, Direction.LEFT),
        ]:
            self.player_movement_events.key_down(
                key, self.player.start_moving, {"direction": direction.value}
            )
            self.player_movement_events.key_up(
                key, self.player.stop_moving, {"direction": direction.value}
            )
        self.scene.events.register_group(self.player_movement_events)

    @property
    def walkable_zone(self):
        return self.bottomleft, self.topright

    @property
    def all_layers(self):
        return {
            layer_setting.value["name"]: getattr(
                self, layer_setting.value["name"]
            )
            for layer_setting in list(RestaurantLayers)
        }
