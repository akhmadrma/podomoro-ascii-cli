"""
Tests for the notifier module.
"""

import sys
import types

from podomoro_ascii_cli.core import notifier


class DummyProcess:
    """Minimal subprocess double for sound playback tests."""

    def __init__(self, running: bool = True) -> None:
        self._running = running
        self.terminated = False
        self.killed = False
        self.wait_calls = 0

    def poll(self):
        return None if self._running else 0

    def terminate(self) -> None:
        self.terminated = True
        self._running = False

    def kill(self) -> None:
        self.killed = True
        self._running = False

    def wait(self, timeout: float | None = None) -> int:
        self.wait_calls += 1
        return 0


class DummyNotify:
    """Minimal notifypy replacement."""

    def __init__(self) -> None:
        self.title = ""
        self.message = ""
        self.sent = False

    def send(self, block: bool = False) -> None:
        self.sent = True


def install_dummy_notifypy(monkeypatch) -> None:
    """Provide a minimal notifypy module for notifier tests."""
    monkeypatch.setitem(
        sys.modules,
        "notifypy",
        types.SimpleNamespace(Notify=DummyNotify),
    )


def test_send_notification_plays_sound_when_audio_exists(monkeypatch, tmp_path):
    """Notification sound is started separately from desktop notification delivery."""
    sound_file = tmp_path / "notification.wav"
    sound_file.write_bytes(b"wav")

    started = {}

    install_dummy_notifypy(monkeypatch)
    monkeypatch.setattr(notifier, "_sound_process", None)
    monkeypatch.setattr(notifier, "_get_sound_command", lambda _: ["player", "sound"])

    def fake_popen(command, stdout=None, stderr=None):
        started["command"] = command
        return DummyProcess()

    monkeypatch.setattr(notifier.subprocess, "Popen", fake_popen)

    notifier.send_notification("work_to_break", sound_path=sound_file)

    assert started["command"] == ["player", "sound"]


def test_send_notification_skips_sound_when_no_player(monkeypatch, tmp_path):
    """Notification still sends when no audio player is available."""
    sound_file = tmp_path / "notification.wav"
    sound_file.write_bytes(b"wav")

    install_dummy_notifypy(monkeypatch)
    monkeypatch.setattr(notifier, "_sound_process", None)
    monkeypatch.setattr(notifier, "_get_sound_command", lambda _: None)

    notifier.send_notification("break_to_work", sound_path=sound_file)

    assert notifier._sound_process is None


def test_stop_notification_sound_terminates_running_process(monkeypatch):
    """Stopping notification sound terminates the active playback process."""
    process = DummyProcess()
    monkeypatch.setattr(notifier, "_sound_process", process)

    notifier.stop_notification_sound()

    assert process.terminated is True
    assert notifier._sound_process is None
