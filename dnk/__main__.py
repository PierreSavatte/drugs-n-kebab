import arcade

from dnk.display import Window


def main():
    window = Window()
    window.setup()
    window.center_window()
    try:
        arcade.run()
    except KeyboardInterrupt:
        pass
