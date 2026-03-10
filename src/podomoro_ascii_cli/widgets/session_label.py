"""
Session label widget for displaying current session type.
"""
from textual.widgets import Static


class SessionLabel(Static):
    """Widget to display the current session type and number."""

    DEFAULT_CSS = """
    SessionLabel {
        text-align: center;
        color: white;
        text-style: bold;
    }
    """

    def __init__(self, label: str = "WORK TIME", session_number: int = 1, total_sessions: int = 4) -> None:
        """
        Initialize the session label.

        Args:
            label: The session type label (e.g., "WORK TIME").
            session_number: Current session number.
            total_sessions: Total sessions before long break.
        """
        super().__init__()
        self._label = label
        self._session_number = session_number
        self._total_sessions = total_sessions

    def update_label(self, label: str, session_number: int | None = None) -> None:
        """
        Update the session label.

        Args:
            label: New label text.
            session_number: Optional new session number.
        """
        self._label = label
        if session_number is not None:
            self._session_number = session_number
        self.update(self._render_text())

    def update_session_number(self, session_number: int) -> None:
        """Update just the session number."""
        self._session_number = session_number
        self.update(self._render_text())

    def _render_text(self) -> str:
        """Render the label text with session counter."""
        return f"{self._label} [Session {self._session_number}/{self._total_sessions}]"

    def on_mount(self) -> None:
        """Initialize the display."""
        self.update(self._render_text())
