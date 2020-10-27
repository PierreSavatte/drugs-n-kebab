import arcade
from arcade_curtains import BaseScene

from dnk.display import exit_game
from dnk.display.character_sprite import CharacterSprite, Direction
from dnk.display.load_restaurant import load_restaurant_file, RestaurantLayers
from dnk.models.character import Character, Ethnicities, Genders
from dnk.settings import SPRITE_SCALING


class RestaurantScene(BaseScene):
    def setup(self):

        # Restaurant layers (floor, walls, furniture, ...)
        restaurant = load_restaurant_file("restaurant")
        self.collidable_layers = arcade.SpriteList()
        for layer_setting in RestaurantLayers.ordered():
            layer_name = layer_setting.value["name"]
            layer = arcade.tilemap.process_layer(
                map_object=restaurant,
                layer_name=layer_name,
                scaling=SPRITE_SCALING,
            )
            setattr(self, layer_name, layer)
            if layer_setting.value["collidable"]:
                self.collidable_layers.extend(layer)

        # Actors
        self.actors = arcade.SpriteList()
        self.player = CharacterSprite(
            Character(Genders.MAN, Ethnicities.AFRICAN)
        )
        self.actors.append(self.player)

        # Physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.collidable_layers
        )

        # Event to allow player to walk
        for key, direction in [
            (arcade.key.W, Direction.UP),
            (arcade.key.S, Direction.DOWN),
            (arcade.key.D, Direction.RIGHT),
            (arcade.key.A, Direction.LEFT),
        ]:
            self.events.key(
                key, self.player.move, {"direction": direction.value}
            )

        self.events.key(arcade.key.ESCAPE, exit_game)

    @property
    def all_layers(self):
        return {
            layer_setting.value["name"]: getattr(
                self, layer_setting.value["name"]
            )
            for layer_setting in list(RestaurantLayers)
        }

    def enter_scene(self, previous_scene):
        arcade.set_background_color(arcade.color.WHITE)
