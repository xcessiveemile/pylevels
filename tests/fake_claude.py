"""A stand-in for the claude command, so tests never touch the network.

It copies the real command's shape: it prints a link, then waits on standard
input for the code without a newline after the prompt. Signing in leaves a
marker file, and the status command reports on that, the way the real command
remembers a login.
"""

import os
import sys
import tempfile
from pathlib import Path

LINK = "https://claude.example/oauth/authorize?state=abc123"

SCRIPT = f'''
import os, sys
state = os.environ["PYLEVELS_FAKE_STATE"]
argv = sys.argv[1:]
if argv[:2] == ["auth", "status"]:
    print('{{"loggedIn": %s, "email": "player@example.com"}}' % ("true" if os.path.exists(state) else "false"))
    sys.exit(0)
if argv[:2] == ["auth", "login"]:
    if os.environ.get("PYLEVELS_FAKE_NO_LINK"):
        print("could not reach the sign-in service")
        sys.exit(1)
    print("Opening browser to sign in\\u2026")
    print("If the browser didn't open, visit: {LINK}")
    print("Paste code here if prompted > ", end="")
    sys.stdout.flush()
    if os.environ.get("PYLEVELS_FAKE_HANG"):
        import time; time.sleep(300)
    code = sys.stdin.readline().strip()
    if code == "goodcode":
        open(state, "w").write("in")
        print("\\nLogin successful")
        sys.exit(0)
    print("\\nInvalid code")
    sys.exit(1)
sys.exit(2)
'''


def build():
    """Write the fake command and return (path to it, path to its marker file)."""
    folder = Path(tempfile.mkdtemp())
    script = folder / "fake_claude_script.py"
    script.write_text(SCRIPT)

    command = folder / "claude"
    command.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{script}" "$@"\n')
    command.chmod(0o755)

    marker = folder / "logged-in"
    os.environ["PYLEVELS_FAKE_STATE"] = str(marker)
    return command, marker
