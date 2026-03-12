"""
Widget that displays the total accumulated work session time in HH:MM format.
"""
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label


def _format_hh_mm(total_seconds: int) -> str:
    """Format total seconds as HH:MM string."""
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"


class TotalWorkCounter(Widget):
    """Displays the total accumulated working time in HH:MM format."""

    DEFAULT_CSS = """
    TotalWorkCounter {
        height: auto;
        width: auto;
        padding: 0 1;
    }
    """

    total_seconds: reactive[int] = reactive(0)

    def compose(self) -> ComposeResult:
        """Compose the widget with a standard Label."""
        yield Label(f"Total Work: {_format_hh_mm(self.total_seconds)}", id="total-work-label")

    def watch_total_seconds(self, value: int) -> None:
        """React to changes in total_seconds and update the label."""
        try:
            label = self.query_one("#total-work-label", Label)
            label.update(f"Total Work: {_format_hh_mm(value)}")
        except Exception:
            pass

    def set_total_seconds(self, value: int) -> None:
        """Set the total accumulated work seconds."""
        self.total_seconds = value

    def increment(self) -> None:
        """Increment the counter by one second."""
        self.total_seconds += 1

    def reset(self) -> None:
        """Reset the counter to zero."""
        self.total_seconds = 0
