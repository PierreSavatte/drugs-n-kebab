import arcade
from arcade_curtains import BaseScene, Widget

from dnk.display import exit_game
from dnk.display.character_sprite import CharacterSprite, Direction
from dnk.display.load_restaurant import load_restaurant_file, RestaurantLayers
from dnk.models.character import Character, Ethnicities, Genders
from dnk.settings import SPRITE_SCALING

from dnk.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class RestaurantScene(BaseScene):
    def setup(self, restaurant=None):
        self.sprites = arcade.SpriteList()
        self.widget = RestaurantWidget(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            restaurant=restaurant,
            events=self.events,
        )
        self.widget.register(self.sprites)

        self.events.key(arcade.key.ESCAPE, exit_game)

    def enter_scene(self, previous_scene):
        arcade.set_background_color(arcade.color.WHITE)

    def __getattr__(self, item):
        # If the attribute isn't already part of self, check if the widget has it
        if item in dir(self.widget):
            return getattr(self.widget, item)
        else:
            raise AttributeError(
                f"Nor {type(self)} nor {type(self)}.widget has an attribute named '{item}'."
            )


class RestaurantWidget(Widget):
    def setup_widget(self, restaurant=None, events=None):
        self.restaurant = restaurant

        # Restaurant layers (floor, walls, furniture, ...)
        restaurant_map = load_restaurant_file(
            f"{restaurant.size_type.value}_restaurant"
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
        self.player = CharacterSprite(
            Character(Genders.get_random(), Ethnicities.get_random()), self
        )
        self.actors.append(self.player)

        self.sprites.extend(self.actors)

        # Event to allow player to walk
        for key, direction in [
            (arcade.key.W, Direction.UP),
            (arcade.key.S, Direction.DOWN),
            (arcade.key.D, Direction.RIGHT),
            (arcade.key.A, Direction.LEFT),
        ]:
            events.key(key, self.player.move, {"direction": direction.value})

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
