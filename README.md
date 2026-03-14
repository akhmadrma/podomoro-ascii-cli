# Podomoro ASCII CLI

`podomoro-ascii-cli` is a full-screen terminal Pomodoro timer built with [Textual](https://textual.textualize.io/). It shows the countdown as large ASCII art, tracks the current work/break cycle, and lets you adjust durations without leaving the app.

## Features

- Full-screen terminal UI powered by Textual
- Large ASCII countdown rendered with `pyfiglet`
- Standard Pomodoro cycle with work, short break, and long break sessions
- Keyboard shortcuts and clickable buttons for timer control
- In-app settings screen for changing durations and cycle length
- Desktop notifications at session transitions when notification support is available
- Simple JSON settings file created automatically on first run
- Test coverage for the timer, session state machine, and settings persistence

## Requirements

- Python `3.12+`
- A terminal that can run full-screen Textual apps

## Installation

### Option 1: Poetry

```bash
poetry install
poetry run podomoro
```

### Option 2: pip

Install from the project directory:

```bash
pip install .
podomoro
```

### Option 3: Run as a module during development

```bash
PYTHONPATH=src python -m podomoro_ascii_cli
```

## Usage

Launch the app:

```bash
podomoro
```

When the app starts, it loads settings from `settings.json` in the current working directory. If the file does not exist, it is created automatically with default values.

Default session values:

- Work: `25` minutes
- Short break: `5` minutes
- Long break: `15` minutes
- Sessions before long break: `4`

## Controls

The app supports both keyboard shortcuts and on-screen buttons.

| Action | Key | Notes |
| --- | --- | --- |
| Start / Resume | `S` | Starts the timer or resumes from pause |
| Pause | `P` | Pauses the active timer |
| Stop & Reset | `Q` | Stops the timer, resets the cycle, and clears total work time |
| Open Settings | `C` | Opens the settings screen |
| Quit | `Ctrl+C` | Exits the app |
| Save settings and close settings screen | `Esc` | Saves the current settings form |

## How the Timer Cycle Works

The session state machine follows this pattern:

`WORK -> SHORT_BREAK -> WORK -> SHORT_BREAK -> ... -> WORK -> LONG_BREAK -> WORK`

With the default settings, the cycle is:

1. Work session 1
2. Short break
3. Work session 2
4. Short break
5. Work session 3
6. Short break
7. Work session 4
8. Long break
9. Back to work session 1

The session label in the UI shows the current phase and current work-session number, for example `WORK TIME [Session 2/4]`.

## Interface Overview

The main screen includes:

- A header and footer from Textual
- A session label showing the current phase and cycle position
- A large ASCII timer display in `MM:SS` format
- A progress bar for the current session
- A `Total Work` counter that accumulates active work-session time
- Start, Pause, and Stop buttons

Notes about behavior:

- The `Total Work` counter increases only while a work session is actively running.
- The `Total Work` counter resets when you stop the timer with `Q` or the Stop button.
- Finishing a session automatically advances to the next session type and resets the timer duration for that phase.

## Settings

Press `C` to open the full-screen settings screen.

You can configure:

- Work duration
- Short break duration
- Long break duration
- Number of work sessions before a long break

Invalid or empty inputs fall back to defaults, and all values are clamped to a minimum of `1`.

### settings.json

Settings are stored in a local `settings.json` file:

```json
{
  "work_duration": 25,
  "short_break_duration": 5,
  "long_break_duration": 15,
  "sessions_before_long_break": 4
}
```

Important detail: the file is read from and written to the directory where you run the app, not a global config directory. Running `podomoro` from different folders will create separate `settings.json` files.

## Notifications

When a session finishes, the app attempts to send a desktop notification:

- `work_to_break` shows `Break Time!`
- `break_to_work` shows `Work Time!`

Notification delivery is best-effort:

- If `notifypy` is unavailable, the app skips notifications silently.
- If the operating system blocks notifications, the timer still continues normally.
- The code looks for an optional sound file at `assets/notification.wav`, but that file is not currently present in this repository.

## Development

Install development dependencies:

```bash
poetry install --with dev
```

Run tests:

```bash
poetry run pytest
```

Run tests with coverage:

```bash
poetry run pytest --cov=podomoro_ascii_cli
```

Run pylint:

```bash
poetry run pylint src tests
```

## Project Structure

```text
src/podomoro_ascii_cli/
  main.py                  Textual app entry point
  core/
    timer.py               Countdown timer logic
    session.py             Pomodoro session state machine
    config.py              Settings load/save helpers
    notifier.py            Desktop notification integration
  widgets/
    ascii_timer.py         Large ASCII timer widget
    controls.py            Start/pause/stop buttons
    progress_bar.py        Session progress display
    session_label.py       Current session label
    settings_panel.py      Settings screen
    total_work_counter.py  Accumulated work-time widget
tests/
  test_timer.py
  test_session.py
  test_config.py
```

## Entry Points

The project exposes a console script:

```toml
[project.scripts]
podomoro = "podomoro_ascii_cli.main:run"
```

You can also start it with:

```bash
python -m podomoro_ascii_cli
```

## Current Status

- Package version: `0.1.0`
- Development status: `Alpha`
- License: `MIT`

## Known Limitations

- There are no CLI flags yet; the app is launched directly into the TUI.
- Settings are stored per working directory rather than in a user-level config path.
- The accumulated work counter is session-local and is not persisted across app restarts.
- The repository does not currently include a notification sound asset.
