"""Starts the app headless and signs in through the panel, against a stand-in
for the claude command. Checks the three ways out: a good code, a bad code,
and backing out with escape.
Run with: python tests/smoke_login.py"""

import asyncio
import faulthandler
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# If something hangs, print where after 60 seconds instead of waiting forever.
faulthandler.dump_traceback_later(60, exit=True)

from textual.widgets import Button, Input

import auth
import progress
import tutor
from app import LevelScreen, LoginScreen, PyLevelsApp
from tests.fake_claude import LINK, build

# Use a throwaway progress file so the test never touches real progress.
progress.PROGRESS_FILE = Path(tempfile.mkdtemp()) / "progress.json"
# Point the tutor at a command that does not exist, so no hint is ever fetched.
tutor.CLAUDE_COMMAND = "no-such-command"

COMMAND, MARKER = build()
auth.CLAUDE_COMMAND = str(COMMAND)


async def open_panel(pilot, app):
    """Press ctrl+L from a level and wait for the link to arrive."""
    await pilot.press("ctrl+l")
    for _ in range(60):
        await pilot.pause(0.1)
        if isinstance(app.screen, LoginScreen) and app.screen.session.url:
            return app.screen
    raise AssertionError("the sign-in panel never showed a link")


async def main():
    app = PyLevelsApp()
    async with app.run_test(size=(100, 36)) as pilot:
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()
        assert isinstance(app.screen, LevelScreen), "level did not open"
        level = app.screen

        # backing out with escape
        panel = await open_panel(pilot, app)
        process = panel.session.process
        await pilot.press("escape")
        await pilot.pause(0.5)
        assert app.screen is level, "escape did not return to the level"
        assert process.poll() is not None, "escape left the sign-in running"
        assert not auth.signed_in(), "escape should not sign anyone in"

        # a code that is not accepted
        panel = await open_panel(pilot, app)
        panel.query_one("#login-code", Input).value = "nonsense"
        await pilot.press("enter")
        await pilot.pause(1.5)
        assert app.screen is panel, "a bad code should keep the panel open"
        assert not panel.query_one("#login-code", Input).display, "input should be hidden"
        assert not auth.signed_in(), "a bad code must not sign in"
        await pilot.press("escape")
        await pilot.pause(0.5)

        # the code that works
        panel = await open_panel(pilot, app)
        assert panel.session.url == LINK, f"wrong link: {panel.session.url}"
        assert panel.query_one("#login-open", Button).display, "no button to open the page"
        assert panel.query_one("#login-code", Input).display, "nowhere to paste the code"
        panel.query_one("#login-code", Input).value = "goodcode"
        await pilot.press("enter")
        await pilot.pause(2.0)
        assert app.screen is level, "the panel did not close after signing in"
        assert auth.signed_in(), "the sign-in did not take"
        assert "player@example.com" in level.output_text, level.output_text

        print("login smoke test passed")


asyncio.run(main())
