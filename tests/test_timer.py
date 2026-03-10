"""
Tests for the timer module.
"""
import pytest

from podomoro_ascii_cli.core.timer import Timer


class TestTimer:
    """Test cases for the Timer class."""

    def test_timer_init(self):
        """Test timer initialization."""
        timer = Timer(1500)  # 25 minutes in seconds
        assert timer.total_seconds == 1500
        assert timer.remaining_seconds == 1500
        assert timer.is_running is False
        assert timer.is_paused is False

    def test_timer_start(self):
        """Test starting the timer."""
        timer = Timer(60)
        timer.start()
        assert timer.is_running is True
        assert timer.is_paused is False

    def test_timer_pause(self):
        """Test pausing the timer."""
        timer = Timer(60)
        timer.start()
        timer.pause()
        assert timer.is_running is False
        assert timer.is_paused is True

    def test_timer_resume(self):
        """Test resuming the timer."""
        timer = Timer(60)
        timer.start()
        timer.pause()
        timer.resume()
        assert timer.is_running is True
        assert timer.is_paused is False

    def test_timer_stop(self):
        """Test stopping and resetting the timer."""
        timer = Timer(60)
        timer.start()
        timer.tick()  # Decrement to 59
        timer.stop()
        assert timer.is_running is False
        assert timer.is_paused is False
        assert timer.remaining_seconds == 60

    def test_timer_tick(self):
        """Test timer tick decrements remaining time."""
        timer = Timer(60)
        timer.start()
        finished = timer.tick()
        assert timer.remaining_seconds == 59
        assert finished is False

    def test_timer_tick_not_running(self):
        """Test tick does nothing when timer is not running."""
        timer = Timer(60)
        finished = timer.tick()
        assert timer.remaining_seconds == 60
        assert finished is False

    def test_timer_tick_reaches_zero(self):
        """Test tick returns True when timer reaches zero."""
        timer = Timer(1)
        timer.start()
        finished = timer.tick()
        assert finished is True
        assert timer.is_running is False

    def test_timer_get_mm_ss(self):
        """Test MM:SS formatting."""
        timer = Timer(1500)  # 25 minutes
        assert timer.get_mm_ss() == "25:00"

        timer = Timer(90)  # 1 minute 30 seconds
        assert timer.get_mm_ss() == "01:30"

        timer = Timer(5)  # 5 seconds
        assert timer.get_mm_ss() == "00:05"

    def test_timer_elapsed_seconds(self):
        """Test elapsed seconds calculation."""
        timer = Timer(100)
        timer.start()
        timer.tick()
        timer.tick()
        assert timer.elapsed_seconds == 2

    def test_timer_progress_ratio(self):
        """Test progress ratio calculation."""
        timer = Timer(100)
        timer.start()
        timer.tick()
        timer.tick()
        assert timer.progress_ratio == 0.02

    def test_timer_set_duration_when_stopped(self):
        """Test setting duration when timer is stopped."""
        timer = Timer(60)
        timer.set_duration(120)
        assert timer.total_seconds == 120
        assert timer.remaining_seconds == 120

    def test_timer_set_duration_when_running(self):
        """Test setting duration when timer is running does nothing."""
        timer = Timer(60)
        timer.start()
        timer.set_duration(120)
        assert timer.total_seconds == 60
