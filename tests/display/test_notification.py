import time
from unittest.mock import patch

import freezegun
import pytest

from dnk.display.notification import Notification
from dnk.settings import (
    NOTIFICATION_ANIMATION_DURATION,
    NOTIFICATION_WAITING_DURATION,
)


@pytest.fixture
def target(restaurant_scene):
    return restaurant_scene.sprites[0]


@pytest.fixture
def notification(target):
    with patch("arcade.get_window"):
        yield Notification(target=target)


def test_notification_spawns_at_topright_of_target_sprite(
    notification, target
):
    assert notification.top == target.top
    assert notification.right == target.right


@freezegun.freeze_time("2020-10-29 9:45")
def test_notification_says_when_it_is_ready_to_be_deleted(notification):
    notification.time_triggered = (
        time.time()
        - NOTIFICATION_ANIMATION_DURATION
        - NOTIFICATION_WAITING_DURATION
    )

    assert notification.is_ready_to_be_deleted
