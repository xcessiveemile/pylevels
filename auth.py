"""Signs in to Claude from inside the game.

`claude auth login` prints a sign-in link and then waits on its standard input
for the code the browser hands back. Driving it over pipes, instead of giving
it the terminal, means the sign-in works the same in a terminal and in the
browser preview, where the game cannot pause itself.
"""

import json
import os
import re
import select
import subprocess
import time

CLAUDE_COMMAND = "claude"
CODE_PROMPT = "Paste code here"   # the command prints this when it wants the code
LINK = re.compile(r"https://\S+")
START_SECONDS = 30                # long enough for the command to print the link
FINISH_SECONDS = 120              # long enough for the exchange to come back
POLL_SECONDS = 0.2

NOT_INSTALLED = "the claude command is not installed. Install Claude Code first."


class LoginError(Exception):
    """Something went wrong that the player should be told about in plain words."""


def clean_env():
    """The environment for the claude command.

    CLAUDECODE is set when the game itself was started from inside Claude Code,
    and the command refuses to start nested. Removing it keeps things simple.
    """
    env = dict(os.environ)
    env.pop("CLAUDECODE", None)
    return env


def signed_in():
    """True when the claude command is installed and logged in."""
    try:
        result = subprocess.run(
            [CLAUDE_COMMAND, "auth", "status", "--json"],
            capture_output=True,
            text=True,
            timeout=20,
            stdin=subprocess.DEVNULL,
            env=clean_env(),
        )
    except (OSError, subprocess.SubprocessError):
        return False
    try:
        return bool(json.loads(result.stdout)["loggedIn"])
    except (ValueError, KeyError, TypeError):
        return False


def account_name():
    """The signed-in email, or None. Only used to say who you came back as."""
    try:
        result = subprocess.run(
            [CLAUDE_COMMAND, "auth", "status", "--json"],
            capture_output=True,
            text=True,
            timeout=20,
            stdin=subprocess.DEVNULL,
            env=clean_env(),
        )
        return json.loads(result.stdout).get("email")
    except (OSError, subprocess.SubprocessError, ValueError, AttributeError):
        return None


class LoginSession:
    """One run of `claude auth login`, held open while the player fetches the code.

    Use it in two steps: start() gives you the link to open, finish() hands the
    code back. stop() ends it if the player walks away instead.
    """

    def __init__(self):
        self.process = None
        self.url = None

    def start(self):
        """Begin the sign-in and return the link to open."""
        try:
            self.process = subprocess.Popen(
                [CLAUDE_COMMAND, "auth", "login", "--claudeai"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=clean_env(),
            )
        except FileNotFoundError:
            raise LoginError(NOT_INSTALLED)
        except OSError as error:
            raise LoginError(f"could not start the sign-in: {error}")

        text = self.read(CODE_PROMPT, START_SECONDS)
        found = LINK.search(text)
        if found is None:
            self.stop()
            raise LoginError(last_line(text) or "the sign-in did not offer a link.")
        self.url = found.group(0).rstrip(".,")
        return self.url

    def finish(self, code):
        """Hand the code back. Returns nothing; raises LoginError if it failed."""
        if self.process is None or self.process.poll() is not None:
            raise LoginError("the sign-in stopped before the code arrived.")
        try:
            self.process.stdin.write((code.strip() + "\n").encode())
            self.process.stdin.flush()
        except (OSError, ValueError):
            raise LoginError("the sign-in stopped before the code arrived.")

        text = self.read(None, FINISH_SECONDS)
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.stop()
            raise LoginError("the sign-in did not finish in time.")

        if not signed_in():
            raise LoginError(last_line(text) or "that code was not accepted.")

    def read(self, marker, seconds):
        """Collect output until the marker shows up, or to the end when it is None.

        Reads the pipe directly so the half-written 'paste code here' prompt,
        which never ends in a newline, still comes through.
        """
        deadline = time.monotonic() + seconds
        text = ""
        while time.monotonic() < deadline:
            if marker is not None and marker in text:
                break
            ready, _, _ = select.select([self.process.stdout], [], [], POLL_SECONDS)
            if ready:
                chunk = os.read(self.process.stdout.fileno(), 4096)
                if not chunk:            # the command closed its output
                    break
                text += chunk.decode("utf-8", "replace")
            elif self.process.poll() is not None:
                break
        return text

    def stop(self):
        """End the sign-in, whether it finished or the player walked away."""
        if self.process is None:
            return
        try:
            if self.process.poll() is None:
                self.process.kill()
                self.process.wait(timeout=5)
        except (OSError, subprocess.SubprocessError):
            pass
        for stream in (self.process.stdin, self.process.stdout):
            try:
                if stream is not None:
                    stream.close()
            except OSError:
                pass


def last_line(text):
    """The last line of an error is usually the one that says what went wrong."""
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    return lines[-1] if lines else ""
