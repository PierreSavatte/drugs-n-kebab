import arcade

from dnk.display import Window


def main():
    window = Window()
    window.setup()
    try:
        arcade.run()
    except KeyboardInterrupt:
        pass
