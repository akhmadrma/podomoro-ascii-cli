"""
Settings persistence for timer configuration.
"""

import json
from pathlib import Path
from typing import Any

# Default settings for the Pomodoro timer
DEFAULT_SETTINGS: dict[str, Any] = {
    "work_duration": 25,
    "short_break_duration": 5,
    "long_break_duration": 15,
    "sessions_before_long_break": 4,
}

# Settings file path in the app's working directory
SETTINGS_FILE = Path("settings.json")


def load_settings() -> dict[str, Any]:
    """
    Load settings from settings.json.

    If the file doesn't exist, create it with default values.

    Returns:
        Dictionary containing the current settings.
    """
    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with SETTINGS_FILE.open("r") as f:
            settings = json.load(f)
        # Merge with defaults to ensure all keys exist
        merged = DEFAULT_SETTINGS.copy()
        merged.update(settings)
        return merged
    except (json.JSONDecodeError, IOError):
        # If file is corrupted, recreate with defaults
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict[str, Any]) -> None:
    """
    Save settings to settings.json.

    Args:
        settings: Dictionary containing the settings to save.
    """
    try:
        with SETTINGS_FILE.open("w") as f:
            json.dump(settings, f, indent=2)
    except IOError as e:
        # Log error but don't crash the app
        print(f"Warning: Could not save settings: {e}")


# Type alias for convenience
Config = load_settings
