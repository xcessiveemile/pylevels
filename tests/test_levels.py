"""Checks every level in every world. Run this after adding a level."""

from checker import check, judge, literals_in
from levels import WORLDS, all_levels
from runner import run_code

REQUIRED_KEYS = {"id", "title", "brief", "starter", "expected", "hidden", "hint", "concepts"}


def test_every_level_has_exactly_the_seven_keys_plus_concepts():
    for level in all_levels():
        assert set(level.keys()) == REQUIRED_KEYS, f"level {level.get('id')} has wrong keys"


def test_ids_are_unique():
    ids = [level["id"] for level in all_levels()]
    assert len(ids) == len(set(ids))


def test_level_counts():
    counts = [len(world["levels"]) for world in WORLDS]
    assert counts == [8, 8, 8, 8, 8, 8, 8, 8, 8]


def test_briefs_are_short():
    for level in all_levels():
        sentences = [s for s in level["brief"].split(". ") if s.strip()]
        assert len(sentences) <= 2, f"level {level['id']} brief is too long"


def test_every_hint_solves_its_level():
    for level in all_levels():
        solution = level["starter"] + level["hint"]
        result = run_code(solution, level["hidden"])
        assert not result["timed_out"], f"level {level['id']} hint timed out"
        outcome = judge(result, level, solution)
        assert outcome["passed"], f"level {level['id']}: {outcome['diff']}\n{result['stderr']}"


def test_starter_alone_never_passes():
    """You must add something. The code you are given is not the answer."""
    for level in all_levels():
        result = run_code(level["starter"], level["hidden"])
        outcome = judge(result, level, level["starter"])
        assert not outcome["passed"], f"level {level['id']} passes with the starter code alone"


def test_typing_the_expected_output_never_passes_a_print_level():
    """print("the answer") must not work on levels that give you variables to use."""
    for level in all_levels():
        if level["hidden"].strip():
            continue
        lines = level["expected"].splitlines()
        cheat = level["starter"] + "".join(f"print({line!r})\n" for line in lines)
        if all(line in literals_in(level["hint"]) for line in lines):
            continue   # a plain print IS the intended answer here, e.g. 1-1
        result = run_code(cheat, level["hidden"])
        outcome = judge(result, level, cheat)
        assert not outcome["passed"], f"level {level['id']} can be passed by typing the answer"
