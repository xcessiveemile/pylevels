"""Runs the player's code in a separate Python process.

The app never runs player code itself. It writes the code to a file,
starts a fresh Python on that file, and reads back what it printed.
If the code takes longer than TIMEOUT_SECONDS it gets killed.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

TIMEOUT_SECONDS = 3


def run_code(user_code, hidden_code=""):
    """Run user_code (plus optional hidden_code) and return what happened.

    Returns a dict: {"stdout": str, "stderr": str, "timed_out": bool, "exit_code": int}
    exit_code is 0 when the program finished cleanly, anything else means it crashed.
    """
    full_code = user_code.rstrip("\n") + "\n" + hidden_code

    # A temporary folder that is deleted again when the "with" block ends.
    with tempfile.TemporaryDirectory() as folder:
        code_file = Path(folder) / "player_code.py"
        code_file.write_text(full_code, encoding="utf-8")

        try:
            # "-I" starts Python in isolated mode: it ignores environment
            # variables and does not add the current folder to the import path.
            result = subprocess.run(
                [sys.executable, "-I", str(code_file)],
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                stdin=subprocess.DEVNULL,
                cwd=folder,
            )
        except subprocess.TimeoutExpired:
            return {"stdout": "", "stderr": "", "timed_out": True, "exit_code": -1}

    return {
        "stdout": result.stdout,
        "stderr": clean_traceback(result.stderr, str(code_file)),
        "timed_out": False,
        "exit_code": result.returncode,
    }


def clean_traceback(stderr, code_path):
    """Replace the long temp file path in a traceback with a short name."""
    return stderr.replace(code_path, "your_code.py")
