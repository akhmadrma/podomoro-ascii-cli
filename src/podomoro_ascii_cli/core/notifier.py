

from pathlib import Path
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    import notifypy

# Default sound file path
DEFAULT_SOUND_FILE = Path("assets/notification.wav")


NotificationType = Literal["work_to_break", "break_to_work"]


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
    try:                                      
      from notifypy import Notify                                                                                                                
    except ImportError:                                                                                                                          
      # If notifypy is not installed, silently skip                                                                                              
      return 

    # Set up notification
    notification: "notifypy.Notify" = Notify()
    notification.title = "Podomoro ASCII CLI"

    # Set message based on type
    if notification_type == "work_to_break":
        notification.message = "Break Time!"
    else:  # break_to_work
        notification.message = "Work Time!"

    # Set audio if available
    audio_path = sound_path or DEFAULT_SOUND_FILE
    if audio_path.exists():
        notification.audio = str(audio_path)

    # Send non-blocking notification
    try:
        notification.send(block=False)
    except Exception:
        # Silently fail if notification doesn't work
        pass
