"""
Main entry point for PODOMORO ASCII CLI.
"""

from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical
from textual.timer import Timer as TextualTimer
from textual.widgets import Button, Footer, Header

from podomoro_ascii_cli.core import (
    Session,
    SessionType,
    load_settings,
    save_settings,
    send_notification,
)
from podomoro_ascii_cli.core.timer import Timer
from podomoro_ascii_cli.widgets import (
    ASCIITimer,
    ControlButtons,
    SessionLabel,
    SessionProgressBar,
    SettingsPanel,
)


class PodomoroApp(App):
    """
    Main Textual App for the Pomodoro timer.
    """

    TITLE = "Podomoro ASCII CLI"
    CSS = """
    Screen {
        align: center middle;
    }

    #main-container {
        width: 100%;
        height: 100%;
        padding: 1;
    }

    #timer-section {
        width: 100%;
        height: auto;
        align: center middle;
    }

    #controls-section {
        width: 100%;
        height: auto;
    }

    #progress-section {
        width: 100%;
        height: auto;
        align: center middle;
    }

    #settings-section {
        width: 100%;
        height: auto;
    }
    """

    BINDINGS = [
        Binding("s", "start", "Start/Resume"),
        Binding("p", "pause", "Pause"),
        Binding("q", "stop", "Stop & Reset"),
        Binding("c", "toggle_settings", "Settings"),
        Binding("ctrl+c", "quit", "Quit"),
    ]

    def __init__(self) -> None:
        """Initialize the Pomodoro app."""
        super().__init__()
        self._settings = load_settings()
        self._session = Session(
            sessions_before_long_break=self._settings["sessions_before_long_break"]
        )
        self._timer = Timer(self._get_duration_for_session() * 60)
        self._tick_timer: TextualTimer | None = None

    def _get_duration_for_session(self) -> int:
        """Get the duration in minutes for the current session type."""
        session_type = self._session.session_type
        if session_type == SessionType.WORK:
            return self._settings["work_duration"]
        elif session_type == SessionType.SHORT_BREAK:
            return self._settings["short_break_duration"]
        else:  # LONG_BREAK
            return self._settings["long_break_duration"]

    def compose(self) -> ComposeResult:
        """Compose the app UI."""
        yield Header()

        with Vertical(id="main-container"):
            with Center(id="timer-section"):
                yield SessionLabel(
                    label=self._session.get_label(),
                    session_number=self._session.session_number,
                    total_sessions=self._settings["sessions_before_long_break"],
                )
                yield ASCIITimer(self._timer.get_mm_ss())

            with Center(id="progress-section"):
                progress_bar = SessionProgressBar()
                progress_bar.set_total(self._timer.total_seconds)
                progress_bar.set_elapsed(self._timer.elapsed_seconds)
                yield progress_bar

            with Vertical(id="controls-section"):
                yield ControlButtons()

            with Center(id="settings-section"):
                yield SettingsPanel(self._settings)

        yield Footer()

    def on_mount(self) -> None:
        """Initialize the app on mount."""
        self._start_tick_timer()

    def _start_tick_timer(self) -> None:
        """Start the periodic tick timer for UI updates."""
        self._tick_timer = self.set_interval(1, self._on_tick)

    def _on_tick(self) -> None:
        """Handle the periodic tick."""
        if self._timer.is_running:
            finished = self._timer.tick()
            self._update_timer_display()
            self._update_progress_bar()

            if finished:
                self._on_timer_finished()

    def _update_timer_display(self) -> None:
        """Update the ASCII timer display."""
        timer_widget = self.query_one(ASCIITimer)
        timer_widget.update_time(self._timer.get_mm_ss())

    def _update_progress_bar(self) -> None:
        """Update the progress bar."""
        progress_bar = self.query_one(SessionProgressBar)
        progress_bar.update_progress(
            self._timer.elapsed_seconds, self._timer.total_seconds
        )

    def _on_timer_finished(self) -> None:
        """Handle timer completion."""
        # Stop the current timer
        self._timer.stop()
        controls = self.query_one(ControlButtons)
        controls.set_stopped()

        # Send notification
        current_type = self._session.session_type
        if current_type == SessionType.WORK:
            send_notification("work_to_break")
        else:
            send_notification("break_to_work")

        # Advance to next session
        self._session.advance()
        self._reset_timer_for_new_session()
        self._update_session_display()

    def _reset_timer_for_new_session(self) -> None:
        """Reset the timer for a new session."""
        duration_minutes = self._get_duration_for_session()
        self._timer = Timer(duration_minutes * 60)
        self._update_timer_display()

        progress_bar = self.query_one(SessionProgressBar)
        progress_bar.set_total(self._timer.total_seconds)
        progress_bar.set_elapsed(0)

    def _update_session_display(self) -> None:
        """Update the session label display."""
        session_label = self.query_one(SessionLabel)
        session_label.update_label(
            self._session.get_label(),
            self._session.session_number,
        )

    def action_start(self) -> None:
        """Start or resume the timer."""
        if self._timer.is_paused:
            self._timer.resume()
        else:
            self._timer.start()

        controls = self.query_one(ControlButtons)
        controls.set_running(True)

    def action_pause(self) -> None:
        """Pause the timer."""
        if self._timer.is_running:
            self._timer.pause()
            controls = self.query_one(ControlButtons)
            controls.set_paused(True)

    def action_stop(self) -> None:
        """Stop the timer and reset the cycle."""
        self._timer.stop()
        self._session.reset()

        # Reset timer with new work duration
        self._reset_timer_for_new_session()
        self._update_session_display()

        controls = self.query_one(ControlButtons)
        controls.set_stopped()

    def action_toggle_settings(self) -> None:
        """Toggle the settings panel visibility."""
        settings_panel = self.query_one(SettingsPanel)
        settings_panel.toggle()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id

        if button_id == "start-btn":
            self.action_start()
        elif button_id == "pause-btn":
            self.action_pause()
        elif button_id == "stop-btn":
            self.action_stop()
        elif button_id == "save-btn":
            self._save_settings()
        elif button_id == "cancel-btn":
            self._cancel_settings()

    def _save_settings(self) -> None:
        """Save the settings and apply them."""
        settings_panel = self.query_one(SettingsPanel)
        new_settings = settings_panel.get_settings()

        # Save to file
        save_settings(new_settings)
        self._settings = new_settings

        # Update session
        self._session.sessions_before_long_break = new_settings[
            "sessions_before_long_break"
        ]

        # Update session label with new total
        session_label = self.query_one(SessionLabel)
        session_label._total_sessions = new_settings["sessions_before_long_break"]
        session_label.update_label(
            self._session.get_label(),
            self._session.session_number,
        )

        # If timer is not running, update duration for current session
        if not self._timer.is_running:
            self._reset_timer_for_new_session()

        settings_panel.hide()

    def _cancel_settings(self) -> None:
        """Cancel settings changes."""
        settings_panel = self.query_one(SettingsPanel)
        settings_panel.update_values(self._settings)
        settings_panel.hide()


def run() -> None:
    """
    Run the Podomoro app.
    """
    app = PodomoroApp()
    app.run()


if __name__ == "__main__":
    run()
