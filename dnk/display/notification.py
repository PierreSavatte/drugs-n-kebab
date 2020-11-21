import time

import arcade_curtains

from dnk.display.load_sprites import notification_sprite_path
from dnk.settings import (
    SPRITE_SCALING,
    NOTIFICATION_ANIMATION_DURATION,
    NOTIFICATION_WAITING_DURATION,
    SPRITE_HEIGHT,
)


class Notification(arcade_curtains.Sprite):
    def __init__(self, target):
        super().__init__(notification_sprite_path)
        self.scale = SPRITE_SCALING
        self.top = target.top
        self.right = target.right
        self.start_position = self.position[:]
        self.time_triggered = time.time()

        # self.alpha = NOTIFICATION_ALPHA
        self.animate(
            duration=NOTIFICATION_ANIMATION_DURATION,
            position=self.end_position,
        )

    @property
    def end_position(self):
        start_x, end_y = self.start_position
        return start_x, end_y + (SPRITE_HEIGHT // 2)

    @property
    def is_ready_to_be_deleted(self):
        return (
            time.time()
            >= self.time_triggered
            + NOTIFICATION_ANIMATION_DURATION
            + NOTIFICATION_WAITING_DURATION
        )
