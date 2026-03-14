"""
Core functionality for the Pomodoro timer.
"""
from podomoro_ascii_cli.core.config import DEFAULT_SETTINGS, load_settings, save_settings
from podomoro_ascii_cli.core.notifier import (
    DEFAULT_SOUND_FILE,
    send_notification,
    stop_notification_sound,
)
from podomoro_ascii_cli.core.session import Session, SessionType
from podomoro_ascii_cli.core.timer import Timer

__all__ = [
    # Config
    "DEFAULT_SETTINGS",
    "load_settings",
    "save_settings",
    # Session
    "Session",
    "SessionType",
    # Timer
    "Timer",
    # Notifier
    "DEFAULT_SOUND_FILE",
    "send_notification",
    "stop_notification_sound",
]
