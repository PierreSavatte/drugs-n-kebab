import arcade
import arcade_curtains


class OrderList(arcade_curtains.Widget):
    def setup_widget(self, scene, callback_once_finished):
        self.scene = scene
        self.callback_once_finished = callback_once_finished
        self.sprites = arcade.SpriteList()

        # for key in [arcade.key.W, arcade.key.S, arcade.key.D, arcade.key.A]:
        #     self.scene.events.key_down(
        #         key,
        #         self.move_cursor,
        #         {"message": key},
        #     )

        self.scene.events.key_down(arcade.key.ENTER, self.tear_down)

    def tear_down(self):
        for sprite in self.sprites:
            self.scene.sprites.remove(sprite)

        # for key in [arcade.key.W, arcade.key.S, arcade.key.D, arcade.key.A]:
        #     self.scene.events.remove_key_down(key, self.move_cursor)
        self.scene.events.remove_key_down(arcade.key.ENTER, self.tear_down)

        self.callback_once_finished()
