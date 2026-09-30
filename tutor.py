"""Asks Claude for help through the Claude Code command line.

This uses the `claude` program that is already signed in to your account,
so hints are covered by your subscription. No API key, no extra billing.

Two ways to ask:
  ask_for_hint(...)  one short nudge about where you are stuck right now
  chat(...)          a back-and-forth conversation about the level
"""

import json
import os
import shutil
import subprocess
from pathlib import Path

CLAUDE_COMMAND = "claude"

# Where Claude Code usually lives. An app started from Finder has a bare PATH,
# so the command is looked up here as well.
CLAUDE_PLACES = [
    Path.home() / ".local" / "bin" / "claude",
    Path.home() / ".local" / "bin" / "claude.exe",   # Windows
    Path.home() / ".claude" / "local" / "claude",
    Path("/opt/homebrew/bin/claude"),
    Path("/usr/local/bin/claude"),
]


def find_claude():
    """The full path of the claude command, or the bare name if not found."""
    found = shutil.which(CLAUDE_COMMAND)
    if found:
        return found
    if CLAUDE_COMMAND != "claude":
        return CLAUDE_COMMAND      # a test or a setting asked for a specific name
    for place in CLAUDE_PLACES:
        if place.exists():
            return str(place)
    return CLAUDE_COMMAND
MODEL = "sonnet"
TIMEOUT_SECONDS = 90
THEORY_FILE = Path(__file__).parent / "THEORY.md"

TUTOR_RULES = """You are a calm, excellent Python tutor inside a small game.
The student is a beginner. You see their code with line numbers, the task,
the checker's verdict, the last error, and the theory notes for this topic.

Answer a HINT request like this:
1. Say exactly where they are stuck: the line number and the piece of code,
   or what is missing if nothing is written yet.
2. Explain the one idea they need in simple words, as if for the first time,
   with a tiny example that is not the solution to the task.
3. Give one clear next step, but never write the full solution and never
   quote the reference answer. Naming a function, method or keyword is fine.
4. If the verdict says they typed the answer in, explain why the code must
   compute it instead.
Do not compare to other languages unless the student asks. Short sentences,
no jargon without a one-line explanation. At most six sentences. Plain text
only, no markdown, no code fences. If they had hints already, go one step
further than the last one."""

CHAT_RULES = """You are a calm, excellent Python tutor inside a small game, talking
with a beginner. They can ask about the current task or any Python idea.
Explain in simple words, one idea at a time, with a tiny example that is not
the solution to the task. When something has a name, give the name and what
it means in one line. End with a short question that checks they understood,
when that helps. Do not compare to other languages unless they ask.
Never write the full solution to the task, and never quote the reference answer.
Under eight sentences per reply. Plain text only, no markdown."""


def ask_for_hint(level, code, last_output, verdict, earlier_hints):
    """Return a hint as text, or a short message saying why there is none."""
    prompt = situation(level, code, last_output, verdict)
    if earlier_hints:
        prompt += "\n\nHints already given:\n" + "\n".join(earlier_hints)
    return run_claude(TUTOR_RULES, prompt)


def chat(level, code, last_output, verdict, history, question):
    """Return the tutor's reply to a question, given the conversation so far.

    history is a list of (who, text) pairs, who is "you" or "tutor".
    """
    prompt = situation(level, code, last_output, verdict)
    if history:
        lines = [f"{who}: {text}" for who, text in history]
        prompt += "\n\nConversation so far:\n" + "\n".join(lines)
    prompt += f"\n\nyou: {question}\ntutor:"
    return run_claude(CHAT_RULES, prompt)


def situation(level, code, last_output, verdict):
    """Everything the tutor needs to know about where the player is."""
    parts = [
        f"World: {world_name(level)}   Level: {level['title']}",
        f"Task: {level['brief']}",
        f"Expected output:\n{level['expected']}",
        f"Reference answer (never reveal):\n{level['hint']}",
        "Player's code so far, with line numbers:\n" + numbered(code),
    ]
    if verdict:
        parts.append(f"Checker verdict on the last run: {verdict}")
    if last_output.strip():
        parts.append(f"Output and errors of the last run:\n{last_output}")
    theory = theory_for(level)
    if theory:
        parts.append("Theory notes for this world:\n" + theory)
    return "\n\n".join(parts)


def numbered(code):
    """The code with a line number in front of every line."""
    lines = code.splitlines() or [""]
    return "\n".join(f"{number:>3}  {line}" for number, line in enumerate(lines, start=1))


def world_name(level):
    from levels import WORLDS
    number = int(level["id"].split("-")[0])
    if 1 <= number <= len(WORLDS):
        return WORLDS[number - 1]["name"]
    return "unknown"


def theory_for(level, most_characters=8000):
    """The section of THEORY.md for this level's world, or an empty string."""
    if not THEORY_FILE.exists():
        return ""
    number = level["id"].split("-")[0]
    text = THEORY_FILE.read_text(encoding="utf-8")
    marker = f"## World {number}:"
    start = text.find(marker)
    if start == -1:
        return ""
    end = text.find("\n## ", start + len(marker))
    section = text[start:end] if end != -1 else text[start:]
    return section[:most_characters]


def clean_env():
    """The environment for the claude command, without the nesting guard."""
    # The CLAUDECODE variable is set when running inside Claude Code itself,
    # and the command refuses to start nested. Removing it keeps things simple.
    env = dict(os.environ)
    env.pop("CLAUDECODE", None)
    # Make sure the usual tool folders are on the PATH, for Finder-started apps.
    extra = [str(Path.home() / ".local" / "bin"), "/opt/homebrew/bin", "/usr/local/bin"]
    env["PATH"] = os.pathsep.join(extra + [env.get("PATH", "/usr/bin:/bin")])
    # The sign-in lookup needs to know who you are.
    env.setdefault("HOME", str(Path.home()))
    env.setdefault("USER", Path.home().name)
    env.setdefault("LOGNAME", env["USER"])
    return env


def status():
    """Is the claude command installed and signed in? Returns (ok, message)."""
    try:
        result = subprocess.run(
            [find_claude(), "auth", "status", "--json"],
            capture_output=True, text=True, timeout=20, stdin=subprocess.DEVNULL, env=clean_env(),
        )
    except FileNotFoundError:
        return False, "the claude command is not installed"
    except subprocess.TimeoutExpired:
        return False, "the claude command did not answer"
    return read_status(result.stdout)


def read_status(text):
    """Turn the JSON from claude auth status into (ok, message)."""
    try:
        data = json.loads(text)
    except ValueError:
        return False, "could not read the sign-in status"
    if data.get("loggedIn"):
        method = data.get("authMethod", "")
        return True, f"signed in ({method})" if method else "signed in"
    return False, "not signed in"


def start_login():
    """Open Claude's sign-in in the browser, without a terminal. Returns a message.

    The command opens the sign-in page itself and waits for you to finish it.
    """
    try:
        subprocess.Popen(
            [find_claude(), "auth", "login", "--claudeai"],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=clean_env(),
        )
    except FileNotFoundError:
        return "the claude command is not installed. Install Claude Code first."
    return "a sign-in page opened in your browser. Finish it there, then check the status again."


def run_claude(rules, prompt):
    """Run the claude command once and return its answer as text."""
    try:
        result = subprocess.run(
            [
                find_claude(), "-p",
                "--model", MODEL,
                "--tools", "",
                "--no-session-persistence",
                "--system-prompt", rules,
                prompt,
            ],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            stdin=subprocess.DEVNULL,
            env=clean_env(),
        )
    except FileNotFoundError:
        return "the tutor needs the claude command. Install Claude Code, then press ctrl+L to log in."
    except subprocess.TimeoutExpired:
        return "the tutor did not answer in time. Try again in a moment."

    if result.returncode != 0:
        return f"the tutor could not answer: {last_line(result.stderr or result.stdout)}. Press ctrl+L to log in."
    return result.stdout.strip()


def last_line(text):
    """The last line of an error is usually the one that says what went wrong."""
    lines = [line for line in text.strip().splitlines() if line.strip()]
    return lines[-1] if lines else "no reply"
