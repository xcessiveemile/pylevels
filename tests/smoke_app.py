"""Starts the app headless, plays level 1-1 with the hint, and exits.
Run with: python tests/smoke_app.py"""

import asyncio
import faulthandler
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# If something hangs, print where after 30 seconds instead of waiting forever.
faulthandler.dump_traceback_later(30, exit=True)

import tempfile

from textual.widgets import TextArea

import progress
import tutor
from app import PyLevelsApp, EntryScreen, LevelScreen, MapScreen, OverviewScreen

# Use a throwaway progress file so the test never touches real progress.
progress.PROGRESS_FILE = Path(tempfile.mkdtemp()) / "progress.json"
# Point the tutor at a command that does not exist, so the test needs no login.
tutor.CLAUDE_COMMAND = "no-such-command"


async def main():
    app = PyLevelsApp()
    async with app.run_test(size=(100, 36)) as pilot:
        await pilot.pause()
        assert isinstance(app.screen, EntryScreen), "entry screen did not open"

        await pilot.press("o")
        await pilot.pause()
        assert isinstance(app.screen, OverviewScreen), "overview did not open"
        await pilot.press("down", "escape")
        await pilot.pause()

        await pilot.press("enter")
        await pilot.pause()
        assert isinstance(app.screen, MapScreen), "map did not open"

        await pilot.press("enter")
        await pilot.pause()
        assert isinstance(app.screen, LevelScreen), "level did not open"

        await pilot.press("ctrl+r")
        await pilot.pause(0.6)
        assert not app.screen.passed, "starter code should not pass"

        await pilot.press("f1")
        await pilot.pause(1.0)
        assert app.screen.used_hint, "hint did not register"
        assert len(app.screen.hints_given) == 1, "tutor reply did not arrive"
        assert "claude" in app.screen.hints_given[0]

        editor = app.screen.query_one("#editor", TextArea)
        editor.text = editor.text + app.screen.level["hint"]
        await pilot.press("ctrl+r")
        await pilot.pause(2.0)
        assert app.screen.passed, "level should have passed"

        await pilot.press("ctrl+n")
        await pilot.pause()
        assert app.screen.level["id"] != "1-1", "ctrl+n did not move on"

        await pilot.press("escape")
        await pilot.pause(0.8)
        assert isinstance(app.screen, MapScreen), "escape did not return to map"
        print("smoke test passed")


asyncio.run(main())
