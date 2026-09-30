"""Writes web-game/levels.json from the level files, for the browser version.

Run again whenever you change a level:  python export_levels.py
"""

import json
from pathlib import Path

from levels import SPACE_WORLDS, WORLDS
from tutor import theory_for

OUT = Path(__file__).parent / "web-game" / "levels.json"


def export():
    data = {"sea": [], "space": []}
    for world in WORLDS:
        data["sea"].append({"name": world["name"], "title": world["title"], "levels": world["levels"]})
    for world in SPACE_WORLDS:
        data["space"].append({"name": world["name"], "title": world["title"], "levels": world["levels"]})
    # The theory notes per world number, so the online tutor has them too.
    data["theory"] = {}
    for world_number in range(1, 10):
        data["theory"][str(world_number)] = theory_for({"id": f"{world_number}-1"})
    # The whole theory file too, for the theory screen in the browser.
    theory_file = Path(__file__).parent / "THEORY.md"
    data["theory_full"] = theory_file.read_text(encoding="utf-8") if theory_file.exists() else ""
    OUT.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT.name}: {sum(len(w['levels']) for w in data['sea'])} levels, {sum(len(w['levels']) for w in data['space'])} drills")


if __name__ == "__main__":
    export()
