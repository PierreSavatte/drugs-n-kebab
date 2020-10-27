import arcade

from dnk.display import PixelArtScene, exit_game
from dnk.display.character_sprite import CharacterSprite, Direction
from dnk.models.character import Character, Ethnicities, Genders


class RestaurantScene(PixelArtScene):
    def setup(self):
        self.actors = arcade.SpriteList()

        self.player = CharacterSprite(
            Character(Genders.get_random(), Ethnicities.get_random())
        )
        self.actors.append(self.player)

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

    def enter_scene(self, previous_scene):
        arcade.set_background_color(arcade.color.WHITE)
