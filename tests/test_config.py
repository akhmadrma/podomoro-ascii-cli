"""
Tests for the config module.
"""

import json
import os
import tempfile
from pathlib import Path

import pytest

from podomoro_ascii_cli.core.config import (
    DEFAULT_SETTINGS,
    load_settings,
    save_settings,
)


class TestConfig:
    """Test cases for config functions."""

    def test_default_settings(self):
        """Test default settings values."""
        assert DEFAULT_SETTINGS["work_duration"] == 25
        assert DEFAULT_SETTINGS["short_break_duration"] == 5
        assert DEFAULT_SETTINGS["long_break_duration"] == 15
        assert DEFAULT_SETTINGS["sessions_before_long_break"] == 4

    def test_load_settings_creates_defaults(self, tmp_path, monkeypatch):
        """Test load_settings creates default file if missing."""
        monkeypatch.chdir(tmp_path)

        settings = load_settings()
        assert settings == DEFAULT_SETTINGS
        assert (tmp_path / "settings.json").exists()

    def test_load_settings_existing_file(self, tmp_path, monkeypatch):
        """Test load_settings reads existing file."""
        monkeypatch.chdir(tmp_path)

        custom_settings = {
            "work_duration": 30,
            "short_break_duration": 10,
            "long_break_duration": 20,
            "sessions_before_long_break": 3,
        }

        with open(tmp_path / "settings.json", "w") as f:
            json.dump(custom_settings, f)

        settings = load_settings()
        assert settings["work_duration"] == 30
        assert settings["short_break_duration"] == 10

    def test_load_settings_merges_with_defaults(self, tmp_path, monkeypatch):
        """Test load_settings merges partial settings with defaults."""
        monkeypatch.chdir(tmp_path)

        partial_settings = {"work_duration": 30}

        with open(tmp_path / "settings.json", "w") as f:
            json.dump(partial_settings, f)

        settings = load_settings()
        assert settings["work_duration"] == 30
        assert (
            settings["short_break_duration"] == DEFAULT_SETTINGS["short_break_duration"]
        )

    def test_load_settings_corrupted_file(self, tmp_path, monkeypatch):
        """Test load_settings recreates defaults if file is corrupted."""
        monkeypatch.chdir(tmp_path)

        with open(tmp_path / "settings.json", "w") as f:
            f.write("invalid json")

        settings = load_settings()
        assert settings == DEFAULT_SETTINGS

    def test_save_settings(self, tmp_path, monkeypatch):
        """Test save_settings writes to file."""
        monkeypatch.chdir(tmp_path)

        custom_settings = {
            "work_duration": 45,
            "short_break_duration": 10,
            "long_break_duration": 30,
            "sessions_before_long_break": 2,
        }

        save_settings(custom_settings)

        with open(tmp_path / "settings.json", "r") as f:
            saved = json.load(f)

        assert saved == custom_settings
