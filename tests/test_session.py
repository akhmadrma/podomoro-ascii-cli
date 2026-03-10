"""
Tests for the session module.
"""
import pytest

from podomoro_ascii_cli.core.session import Session, SessionType


class TestSession:
    """Test cases for the Session class."""

    def test_session_init(self):
        """Test session initialization."""
        session = Session()
        assert session.session_type == SessionType.WORK
        assert session.session_number == 1
        assert session.sessions_before_long_break == 4

    def test_session_init_custom_sessions(self):
        """Test session initialization with custom sessions count."""
        session = Session(sessions_before_long_break=3)
        assert session.sessions_before_long_break == 3

    def test_session_advance_work_to_short_break(self):
        """Test advancing from work to short break."""
        session = Session()
        session.advance()
        assert session.session_type == SessionType.SHORT_BREAK
        assert session.session_number == 1

    def test_session_advance_short_break_to_work(self):
        """Test advancing from short break to work."""
        session = Session()
        session.advance()  # To short break
        session.advance()  # Back to work
        assert session.session_type == SessionType.WORK
        assert session.session_number == 2

    def test_session_advance_to_long_break(self):
        """Test advancing to long break after 4 work sessions."""
        session = Session()
        # Complete 3 full work + short break cycles
        for _ in range(3):
            session.advance()  # Work -> Short Break
            session.advance()  # Short Break -> Work

        # Now at work session 4
        assert session.session_number == 4
        assert session.session_type == SessionType.WORK

        # This advance should go to long break
        session.advance()
        assert session.session_type == SessionType.LONG_BREAK
        assert session.session_number == 4

    def test_session_advance_long_break_to_work(self):
        """Test advancing from long break resets to work session 1."""
        session = Session()
        # Complete a full cycle to get to long break
        for _ in range(3):
            session.advance()  # Work -> Short Break
            session.advance()  # Short Break -> Work
        session.advance()  # Work -> Long Break

        assert session.session_type == SessionType.LONG_BREAK

        session.advance()  # Long Break -> Work (reset)
        assert session.session_type == SessionType.WORK
        assert session.session_number == 1

    def test_session_reset(self):
        """Test resetting the session."""
        session = Session()
        session.advance()
        session.advance()
        session.reset()
        assert session.session_type == SessionType.WORK
        assert session.session_number == 1

    def test_session_get_label_work(self):
        """Test getting label for work session."""
        session = Session()
        assert session.get_label() == "WORK TIME"

    def test_session_get_label_short_break(self):
        """Test getting label for short break."""
        session = Session()
        session.advance()
        assert session.get_label() == "SHORT BREAK"

    def test_session_get_label_long_break(self):
        """Test getting label for long break."""
        session = Session()
        for _ in range(3):
            session.advance()
            session.advance()
        session.advance()
        assert session.get_label() == "LONG BREAK"

    def test_session_set_sessions_before_long_break(self):
        """Test setting sessions before long break."""
        session = Session()
        session.sessions_before_long_break = 2
        assert session.sessions_before_long_break == 2

    def test_session_set_sessions_before_long_break_invalid(self):
        """Test setting invalid sessions before long break raises error."""
        session = Session()
        with pytest.raises(ValueError, match="must be at least 1"):
            session.sessions_before_long_break = 0
