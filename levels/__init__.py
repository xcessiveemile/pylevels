"""Collects every world in order. Add a new world by importing it and
appending it to WORLDS. A world is a module with a WORLD dict and a LEVELS list."""

from levels import (
    space_01_basics,
    space_02_flow,
    space_03_strings,
    space_04_lists_loops,
    space_05_dicts,
    space_06_functions,
    space_07_comprehensions,
    space_08_classes,
    space_09_errors_files,
    world_01_basics,
    world_02_flow,
    world_03_strings,
    world_04_lists_loops,
    world_05_dicts,
    world_06_functions,
    world_07_comprehensions,
    world_08_classes,
    world_09_errors_files,
)

WORLD_MODULES = [
    world_01_basics,
    world_02_flow,
    world_03_strings,
    world_04_lists_loops,
    world_05_dicts,
    world_06_functions,
    world_07_comprehensions,
    world_08_classes,
    world_09_errors_files,
]

# Each entry: {"name": str, "title": str, "levels": [level dicts]}
WORLDS = []
for module in WORLD_MODULES:
    WORLDS.append({
        "name": module.WORLD["name"],
        "title": module.WORLD["title"],
        "levels": module.LEVELS,
    })


def all_levels():
    """Every level from every world, in play order."""
    levels = []
    for world in WORLDS:
        levels.extend(world["levels"])
    return levels


def find_level(level_id):
    """Return the level dict with this id, or None."""
    for level in all_levels():
        if level["id"] == level_id:
            return level
    return None


def next_level(level_id):
    """Return the level that comes after this one, or None at the very end."""
    levels = all_levels()
    for index, level in enumerate(levels):
        if level["id"] == level_id and index + 1 < len(levels):
            return levels[index + 1]
    return None


# ------------------------------------------------------------------- space

# Space is the second world set: the same topics as drills. A drill is played
# ten rounds in a row, each round with different values, so it sticks.
SPACE_MODULES = [
    space_01_basics,
    space_02_flow,
    space_03_strings,
    space_04_lists_loops,
    space_05_dicts,
    space_06_functions,
    space_07_comprehensions,
    space_08_classes,
    space_09_errors_files,
]

SPACE_WORLDS = []
for module in SPACE_MODULES:
    SPACE_WORLDS.append({
        "name": module.WORLD["name"],
        "title": module.WORLD["title"],
        "levels": module.DRILLS,
    })


def all_drills():
    drills = []
    for world in SPACE_WORLDS:
        drills.extend(world["levels"])
    return drills


def next_drill(drill_id):
    """The drill after this one, or None at the very end."""
    drills = all_drills()
    for index, drill in enumerate(drills):
        if drill["id"] == drill_id and index + 1 < len(drills):
            return drills[index + 1]
    return None


def round_level(drill, number):
    """One round of a drill as a normal level dict.

    Every round is its own small task: it brings its own brief, starter,
    expected output, hidden code and hint. The drill gives the id and title.
    """
    part = drill["rounds"][number]
    return {
        "id": drill["id"],
        "title": drill["title"],
        "brief": part["brief"],
        "starter": part["starter"],
        "expected": part["expected"],
        "hidden": part["hidden"],
        "hint": part["hint"],
        "concepts": drill["concepts"],
        "tip": part.get("tip", ""),
    }
