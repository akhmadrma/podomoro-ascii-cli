
import subprocess
from pathlib import Path
from shutil import which
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    import notifypy

# Default sound file path
DEFAULT_SOUND_FILE = Path("assets/notification.wav")

_sound_process: subprocess.Popen[bytes] | None = None


NotificationType = Literal["work_to_break", "break_to_work"]


def _get_sound_command(sound_path: Path) -> list[str] | None:
    """Return a best-effort command for playing notification audio."""
    players: tuple[tuple[str, list[str]], ...] = (
        ("afplay", ["afplay", str(sound_path)]),
        ("paplay", ["paplay", str(sound_path)]),
        ("aplay", ["aplay", str(sound_path)]),
        (
            "ffplay",
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", str(sound_path)],
        ),
        ("play", ["play", "-q", str(sound_path)]),
    )

    for executable, command in players:
        if which(executable):
            return command

    return None


def _play_sound(sound_path: Path) -> None:
    """Start notification sound playback if a supported player is available."""
    global _sound_process

    stop_notification_sound()

    command = _get_sound_command(sound_path)
    if command is None:
        return

    try:
        _sound_process = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        _sound_process = None


def stop_notification_sound() -> None:
    """Stop the active notification sound, if one is playing."""
    global _sound_process

    if _sound_process is None:
        return

    if _sound_process.poll() is None:
        try:
            _sound_process.terminate()
            _sound_process.wait(timeout=1)
        except Exception:
            try:
                _sound_process.kill()
                _sound_process.wait(timeout=1)
            except Exception:
                pass

    _sound_process = None


def send_notification(
    notification_type: NotificationType,
    sound_path: Path | None = None,
) -> None:
    """
    Send a desktop notification with optional sound.

    Args:
        notification_type: Type of notification ("work_to_break" or "break_to_work")
        sound_path: Path to the sound file. If None, uses default.
    """
    audio_path = sound_path or DEFAULT_SOUND_FILE
    if audio_path.exists():
        _play_sound(audio_path)

    try:
        from notifypy import Notify
    except ImportError:
        # If notifypy is not installed, silently skip desktop notifications.
        return

    # Set up notification
    notification: "notifypy.Notify" = Notify()
    notification.title = "Podomoro ASCII CLI"

    # Set message based on type
    if notification_type == "work_to_break":
        notification.message = "Break Time!"
    else:  # break_to_work
        notification.message = "Work Time!"

    # Send non-blocking notification without audio so the app can stop playback later.
    try:
        notification.send(block=False)
    except Exception:
        # Silently fail if notification doesn't work
        pass
