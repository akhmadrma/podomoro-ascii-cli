"""
ASCII timer widget displaying countdown in pyfiglet format.
"""
import pyfiglet
from textual.widgets import Static


class ASCIITimer(Static):
    """Widget to display the timer as large ASCII art."""

    DEFAULT_CSS = """
    ASCIITimer {
        text-align: center;
        color: white;
        text-style: bold;
        width: 100%;
        height: auto;
    }
    """

    def __init__(self, time_string: str = "25:00") -> None:
        """
        Initialize the ASCII timer.

        Args:
            time_string: Initial time to display in MM:SS format.
        """
        super().__init__()
        self._time_string = time_string
        self._figlet_font = "big"

    def update_time(self, time_string: str) -> None:
        """
        Update the displayed time.

        Args:
            time_string: Time string in MM:SS format.
        """
        self._time_string = time_string
        self.update(self._render_ascii())

    def _render_ascii(self) -> str:
        """Render the time as ASCII art using pyfiglet."""
        try:
            fig = pyfiglet.Figlet(font=self._figlet_font)
            ascii_art = fig.renderText(self._time_string)
            return ascii_art
        except Exception:
            # Fallback to plain text if pyfiglet fails
            return f"\n  {self._time_string}\n"

    def on_mount(self) -> None:
        """Initialize the display."""
        self.update(self._render_ascii())
