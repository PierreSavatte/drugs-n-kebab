import sys

import arcade
from OpenGL import GL as gl
from arcade_curtains import Curtains

from dnk.settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


def exit_game():
    sys.exit(0)


class Window(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.curtains = Curtains(self, draw_kwargs={"filter": gl.GL_NEAREST})

        self.curtains.add_scene("restaurant", RestaurantScene())

    def setup(self):
        self.curtains.set_scene("restaurant")


from .restaurant import RestaurantScene
