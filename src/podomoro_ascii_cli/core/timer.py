"""
Countdown timer with start/pause/resume/stop functionality.
"""


class Timer:
    """
    Countdown timer for Pomodoro sessions.
    
    Tracks remaining time, elapsed time, and provides
    start, pause, resume, and stop functionality.
    """
    
    def __init__(self, duration_seconds: int) -> None:
        """
        Initialize the timer.
        
        Args:
            duration_seconds: Total duration of the timer in seconds.
        """
        self._total_seconds = duration_seconds
        self._remaining_seconds = duration_seconds
        self._is_running = False
        self._is_paused = False
    
    @property
    def total_seconds(self) -> int:
        """Total duration of the timer in seconds."""
        return self._total_seconds
    
    @property
    def remaining_seconds(self) -> int:
        """Remaining time in seconds."""
        return self._remaining_seconds
    
    @property
    def is_running(self) -> bool:
        """Whether the timer is currently running."""
        return self._is_running
    
    @property
    def is_paused(self) -> bool:
        """Whether the timer is paused."""
        return self._is_paused
    
    @property
    def elapsed_seconds(self) -> int:
        """Elapsed time in seconds."""
        return self._total_seconds - self._remaining_seconds
    
    @property
    def progress_ratio(self) -> float:
        """Progress ratio (0.0 to 1.0) for progress bar."""
        if self._total_seconds == 0:
            return 0.0
        return self.elapsed_seconds / self._total_seconds
    
    def set_duration(self, duration_seconds: int) -> None:
        """
        Set a new duration for the timer.
        
        Args:
            duration_seconds: New duration in seconds.
        """
        if not self._is_running:
            self._total_seconds = duration_seconds
            self._remaining_seconds = duration_seconds
    
    def start(self) -> None:
        """Start or resume the timer."""
        self._is_running = True
        self._is_paused = False
    
    def pause(self) -> None:
        """Pause the timer."""
        self._is_paused = True
        self._is_running = False
    
    def resume(self) -> None:
        """Resume the timer from pause."""
        self._is_paused = False
        self._is_running = True
    
    def stop(self) -> None:
        """Stop and reset the timer."""
        self._is_running = False
        self._is_paused = False
        self._remaining_seconds = self._total_seconds
    
    def tick(self) -> bool:
        """
        Decrement the timer by one second.
        
        Should be called every second when the timer is running.
        
        Returns:
            True if the timer has reached zero, False otherwise.
        """
        if self._is_running and not self._is_paused:
            if self._remaining_seconds > 0:
                self._remaining_seconds -= 1
                if self._remaining_seconds == 0:
                    self._is_running = False
                    return True
        return False
    
    def get_mm_ss(self) -> str:
        """
        Get the remaining time as MM:SS string.
        
        Returns:
            Time in format "MM:SS".
        """
        minutes = self._remaining_seconds // 60
        seconds = self._remaining_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
