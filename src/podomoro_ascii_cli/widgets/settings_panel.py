"""
Settings panel for configuring timer durations.
"""
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Input, Label, Static


class SettingsPanel(Static):
    """Panel for configuring timer settings."""

    DEFAULT_CSS = """
    SettingsPanel {
        width: 100%;
        height: auto;
        background: $surface;
        border: solid white;
        padding: 1;
        display: none;
    }

    SettingsPanel.visible {
        display: block;
    }

    SettingsPanel Label {
        color: white;
        width: 30;
    }

    SettingsPanel Input {
        width: 10;
    }

    SettingsPanel Horizontal {
        height: auto;
        margin: 1 0;
    }

    SettingsPanel #settings-title {
        text-align: center;
        text-style: bold;
        color: white;
    }

    SettingsPanel #save-btn {
        color: white;
        background: $success;
    }

    SettingsPanel #cancel-btn {
        color: white;
        background: $primary;
    }
    """

    def __init__(self, settings: dict | None = None) -> None:
        """
        Initialize the settings panel.

        Args:
            settings: Dictionary containing current settings.
        """
        super().__init__()
        self._settings = settings or {
            "work_duration": 25,
            "short_break_duration": 5,
            "long_break_duration": 15,
            "sessions_before_long_break": 4,
        }

    def compose(self) -> ComposeResult:
        """Compose the settings panel."""
        yield Label("SETTINGS", id="settings-title")

        with Horizontal():
            yield Label("Work Duration (min):")
            yield Input(
                value=str(self._settings.get("work_duration", 25)),
                id="work-duration",
                type="integer",
            )

        with Horizontal():
            yield Label("Short Break (min):")
            yield Input(
                value=str(self._settings.get("short_break_duration", 5)),
                id="short-break",
                type="integer",
            )

        with Horizontal():
            yield Label("Long Break (min):")
            yield Input(
                value=str(self._settings.get("long_break_duration", 15)),
                id="long-break",
                type="integer",
            )

        with Horizontal():
            yield Label("Sessions before Long Break:")
            yield Input(
                value=str(self._settings.get("sessions_before_long_break", 4)),
                id="sessions-count",
                type="integer",
            )

        with Horizontal():
            yield Button("Save", id="save-btn", variant="success")
            yield Button("Cancel", id="cancel-btn", variant="primary")

    def show(self) -> None:
        """Show the settings panel."""
        self.add_class("visible")

    def hide(self) -> None:
        """Hide the settings panel."""
        self.remove_class("visible")

    def toggle(self) -> None:
        """Toggle the visibility of the settings panel."""
        if self.has_class("visible"):
            self.hide()
        else:
            self.show()

    def is_visible(self) -> bool:
        """Check if the settings panel is visible."""
        return self.has_class("visible")

    def get_settings(self) -> dict:
        """
        Get the current settings from the input fields.

        Returns:
            Dictionary with the settings values.
        """
        try:
            work_duration = int(self.query_one("#work-duration", Input).value)
        except ValueError:
            work_duration = 25

        try:
            short_break = int(self.query_one("#short-break", Input).value)
        except ValueError:
            short_break = 5

        try:
            long_break = int(self.query_one("#long-break", Input).value)
        except ValueError:
            long_break = 15

        try:
            sessions_count = int(self.query_one("#sessions-count", Input).value)
        except ValueError:
            sessions_count = 4

        return {
            "work_duration": max(1, work_duration),
            "short_break_duration": max(1, short_break),
            "long_break_duration": max(1, long_break),
            "sessions_before_long_break": max(1, sessions_count),
        }

    def update_values(self, settings: dict) -> None:
        """
        Update the input field values.

        Args:
            settings: Dictionary with new settings values.
        """
        self.query_one("#work-duration", Input).value = str(settings.get("work_duration", 25))
        self.query_one("#short-break", Input).value = str(settings.get("short_break_duration", 5))
        self.query_one("#long-break", Input).value = str(settings.get("long_break_duration", 15))
        self.query_one("#sessions-count", Input).value = str(
            settings.get("sessions_before_long_break", 4)
        )
