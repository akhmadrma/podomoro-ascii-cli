"""
Progress bar widget for session progress.
"""
from textual.widgets import ProgressBar as TextualProgressBar


class SessionProgressBar(TextualProgressBar):
    """Progress bar showing session progress."""

    DEFAULT_CSS = """
    SessionProgressBar {
        height: auto;
    }

    SessionProgressBar > .bar {
        color: white;
        background: $surface;
    }

    SessionProgressBar > .bar-complete {
        color: white;
        background: $primary;
    }
    """

    def __init__(self) -> None:
        """Initialize the progress bar."""
        super().__init__(show_eta=False)
        self._total_seconds = 0
        self._elapsed_seconds = 0

    def set_total(self, total_seconds: int) -> None:
        """
        Set the total duration.

        Args:
            total_seconds: Total duration in seconds.
        """
        self._total_seconds = total_seconds
        self.total = total_seconds
        self._update_progress()

    def set_elapsed(self, elapsed_seconds: int) -> None:
        """
        Set the elapsed time.

        Args:
            elapsed_seconds: Elapsed time in seconds.
        """
        self._elapsed_seconds = elapsed_seconds
        self.progress = elapsed_seconds

    def update_progress(self, elapsed_seconds: int, total_seconds: int) -> None:
        """
        Update both elapsed and total values.

        Args:
            elapsed_seconds: Elapsed time in seconds.
            total_seconds: Total duration in seconds.
        """
        self._total_seconds = total_seconds
        self._elapsed_seconds = elapsed_seconds
        self.total = total_seconds
        self.progress = elapsed_seconds

    def _update_progress(self) -> None:
        """Update the progress bar display."""
        self.progress = self._elapsed_seconds
