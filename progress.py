"""Loads and saves the player's progress in progress.json (next to main.py)."""

import json
from datetime import date, timedelta
from pathlib import Path

DEFAULT_FILE = Path(__file__).parent / "progress.json"
PROGRESS_FILE = DEFAULT_FILE
XP_PER_STAR = 10

def empty_progress():
    """A brand new progress record. Built fresh each time so nothing is shared."""
    return {
        "stars": {},
        "times": {},        # best time per level, in whole seconds
        "streak": 0,
        "last_played": "",
        "xp": 0,
        "accent": "ice",    # the UI colour chosen in settings
    }


def load():
    """Read progress.json, or start fresh if it does not exist yet."""
    if not PROGRESS_FILE.exists():
        return empty_progress()
    data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    # Fill in any key that an older file might be missing.
    for key, value in empty_progress().items():
        data.setdefault(key, value)
    return data


def save(progress):
    """Write progress to disk, nicely indented so a human can read it."""
    text = json.dumps(progress, indent=2)
    # Write to a temporary file first, then swap it in. If the app closes
    # halfway through, the old file is still whole instead of half written.
    temporary = PROGRESS_FILE.with_suffix(".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(PROGRESS_FILE)
    # A copy for the browser version, so its page can show the XP tank and colour.
    # Only for the real file: tests point PROGRESS_FILE somewhere else.
    mirror = Path(__file__).parent / "web" / "static" / "progress.json"
    if PROGRESS_FILE == DEFAULT_FILE and mirror.parent.exists():
        mirror.write_text(text, encoding="utf-8")


XP_PER_TANK = 100


# Every tank you fill is a step deeper into the sea.
TANK_NAMES = ["Tide Pool", "Shallows", "Reef", "Kelp Forest", "Open Sea", "Twilight Zone", "Abyss", "Trench"]


def tank_state(xp):
    """Which tank you are filling and how full it is, as (tank_number, fill 0..1)."""
    return xp // XP_PER_TANK + 1, (xp % XP_PER_TANK) / XP_PER_TANK


def tank_name(tank_number):
    """The name of a tank. Past the last name, tanks keep the deepest one."""
    return TANK_NAMES[min(tank_number, len(TANK_NAMES)) - 1]


def record_pass(progress, level_id, stars, seconds):
    """Update progress after passing a level. Returns the XP gained."""
    old_stars = progress["stars"].get(level_id, 0)
    gained = 0

    # Stars only ever go up, and XP is only given for the improvement.
    if stars > old_stars:
        progress["stars"][level_id] = stars
        gained = (stars - old_stars) * XP_PER_STAR
        progress["xp"] += gained

    # Keep the fastest time for this level.
    best = progress["times"].get(level_id)
    if best is None or seconds < best:
        progress["times"][level_id] = seconds

    update_streak(progress)
    save(progress)
    return gained


def best_time(progress, level_id):
    return progress["times"].get(level_id)


def format_time(seconds):
    """Turn 75 into 1:15."""
    seconds = int(seconds)
    return f"{seconds // 60}:{seconds % 60:02d}"


def update_streak(progress):
    """Add one to the streak if the last pass was yesterday, reset if older."""
    today = date.today()
    yesterday = today - timedelta(days=1)
    last = progress["last_played"]

    if last == str(today):
        return
    if last == str(yesterday):
        progress["streak"] += 1
    else:
        progress["streak"] = 1
    progress["last_played"] = str(today)


def stars_for(progress, level_id):
    return progress["stars"].get(level_id, 0)


def calculate_stars(used_hint, run_count):
    """3 stars clean, 2 with the hint, 1 if it took more than 5 runs."""
    if run_count > 5:
        return 1
    if used_hint:
        return 2
    return 3
