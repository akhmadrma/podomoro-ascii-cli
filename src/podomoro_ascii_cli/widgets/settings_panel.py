"""
Settings screen for configuring timer durations.
"""
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label


class SettingsScreen(Screen[dict | None]):
    """Full-screen settings for configuring timer settings."""

    DEFAULT_CSS = """
    SettingsScreen {
        align: center middle;
    }

    #settings-container {
        width: 60;
        height: auto;
        background: $surface;
        border: solid $primary;
        padding: 2 4;
    }

    #settings-title {
        text-align: center;
        text-style: bold;
        color: $primary;
        width: 100%;
        margin-bottom: 1;
    }

    SettingsScreen Label {
        color: white;
        width: 32;
    }

    SettingsScreen Input {
        width: 10;
    }

    SettingsScreen Horizontal {
        height: auto;
        margin: 1 0;
    }

    #button-row {
        height: auto;
        margin-top: 2;
        align: center middle;
    }

    #save-btn {
        margin-right: 2;
    }
    """

    BINDINGS = [
        Binding("escape", "save_and_exit", "Save & Exit"),
    ]

    def __init__(self, settings: dict | None = None) -> None:
        """
        Initialize the settings screen.

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
        """Compose the settings screen."""
        yield Header()

        with Center():
            with Vertical(id="settings-container"):
                yield Label("⚙  SETTINGS", id="settings-title")

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

                with Horizontal(id="button-row"):
                    yield Button("Save", id="save-btn", variant="success")
                    yield Button("Cancel", id="cancel-btn", variant="default")

        yield Footer()

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

    def action_save_and_exit(self) -> None:
        """Save the settings and dismiss the screen."""
        self.dismiss(self.get_settings())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "save-btn":
            self.dismiss(self.get_settings())
        elif event.button.id == "cancel-btn":
            self.dismiss(None)
