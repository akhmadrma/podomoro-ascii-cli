"""
Pomodoro session state machine.
"""
from enum import Enum


class SessionType(Enum):
    """Types of Pomodoro sessions."""
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"


class Session:
    """
    Pomodoro session state machine.
    
    Manages the session cycle: WORK → SHORT_BREAK → WORK → SHORT_BREAK → 
    WORK → SHORT_BREAK → WORK → LONG_BREAK (repeats).
    """
    
    def __init__(self, sessions_before_long_break: int = 4) -> None:
        """
        Initialize the session state machine.
        
        Args:
            sessions_before_long_break: Number of work sessions before a long break.
        """
        self._session_type = SessionType.WORK
        self._session_number = 1
        self._sessions_before_long_break = sessions_before_long_break
    
    @property
    def session_type(self) -> SessionType:
        """Current session type."""
        return self._session_type
    
    @property
    def session_number(self) -> int:
        """Current session number in the cycle (1-based)."""
        return self._session_number
    
    @property
    def sessions_before_long_break(self) -> int:
        """Number of work sessions before a long break."""
        return self._sessions_before_long_break
    
    @sessions_before_long_break.setter
    def sessions_before_long_break(self, value: int) -> None:
        """Set the number of sessions before a long break."""
        if value < 1:
            raise ValueError("sessions_before_long_break must be at least 1")
        self._sessions_before_long_break = value
    
    def advance(self) -> None:
        """
        Advance to the next session in the cycle.
        
        The cycle follows:
        - WORK → SHORT_BREAK (if not at long break threshold)
        - WORK → LONG_BREAK (if at long break threshold)
        - SHORT_BREAK → WORK (increment session number)
        - LONG_BREAK → WORK (reset session number to 1)
        """
        if self._session_type == SessionType.WORK:
            # After work, determine break type
            if self._session_number % self._sessions_before_long_break == 0:
                self._session_type = SessionType.LONG_BREAK
            else:
                self._session_type = SessionType.SHORT_BREAK
        elif self._session_type == SessionType.SHORT_BREAK:
            # After short break, back to work
            self._session_type = SessionType.WORK
            self._session_number += 1
        elif self._session_type == SessionType.LONG_BREAK:
            # After long break, back to work and reset cycle
            self._session_type = SessionType.WORK
            self._session_number = 1
    
    def reset(self) -> None:
        """Reset the session to the initial state (WORK, Session 1)."""
        self._session_type = SessionType.WORK
        self._session_number = 1
    
    def get_label(self) -> str:
        """
        Get the display label for the current session.
        
        Returns:
            Display label: "WORK TIME", "SHORT BREAK", or "LONG BREAK".
        """
        labels = {
            SessionType.WORK: "WORK TIME",
            SessionType.SHORT_BREAK: "SHORT BREAK",
            SessionType.LONG_BREAK: "LONG BREAK",
        }
        return labels[self._session_type]
