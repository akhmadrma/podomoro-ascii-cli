"""
Control buttons: Start, Pause, Stop.
"""
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button


class ControlButtons(Horizontal):
    """Widget containing the control buttons for the timer."""

    DEFAULT_CSS = """
    ControlButtons {
        align: center middle;
        height: auto;
        margin: 1;
    }

    ControlButtons Button {
        margin: 0 1;
        min-width: 12;
    }

    ControlButtons #start-btn {
        color: white;
        background: $primary;
    }

    ControlButtons #pause-btn {
        color: white;
        background: $primary;
    }

    ControlButtons #stop-btn {
        color: white;
        background: $error;
    }
    """

    def __init__(self) -> None:
        """Initialize the control buttons."""
        super().__init__()
        self._is_running = False
        self._is_paused = False

    def compose(self) -> ComposeResult:
        """Compose the control buttons."""
        yield Button("Start [S]", id="start-btn", variant="primary")
        yield Button("Pause [P]", id="pause-btn", variant="primary", disabled=True)
        yield Button("Stop [Q]", id="stop-btn", variant="error")

    def on_mount(self) -> None:
        """Initialize button states."""
        self._update_button_states()

    def set_running(self, running: bool) -> None:
        """
        Update the running state.

        Args:
            running: True if timer is running, False otherwise.
        """
        self._is_running = running
        self._is_paused = False
        self._update_button_states()

    def set_paused(self, paused: bool) -> None:
        """
        Update the paused state.

        Args:
            paused: True if timer is paused, False otherwise.
        """
        self._is_paused = paused
        self._is_running = not paused
        self._update_button_states()

    def set_stopped(self) -> None:
        """Set the state to stopped (not running, not paused)."""
        self._is_running = False
        self._is_paused = False
        self._update_button_states()

    def _update_button_states(self) -> None:
        """Update button labels and states based on current state."""
        start_btn = self.query_one("#start-btn", Button)
        pause_btn = self.query_one("#pause-btn", Button)
        stop_btn = self.query_one("#stop-btn", Button)

        if self._is_running and not self._is_paused:
            # Timer is running - show Resume disabled, Pause enabled
            start_btn.label = "Start [S]"
            start_btn.disabled = True
            pause_btn.label = "Pause [P]"
            pause_btn.disabled = False
        elif self._is_paused:
            # Timer is paused - show Resume enabled, Pause disabled
            start_btn.label = "Resume [S]"
            start_btn.disabled = False
            pause_btn.label = "Pause [P]"
            pause_btn.disabled = True
        else:
            # Timer is stopped - show Start enabled, Pause disabled
            start_btn.label = "Start [S]"
            start_btn.disabled = False
            pause_btn.label = "Pause [P]"
            pause_btn.disabled = True

        # Stop button is always enabled
        stop_btn.disabled = False
