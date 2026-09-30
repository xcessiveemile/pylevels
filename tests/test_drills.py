"""Checks every space drill: shape, ten rounds, and every round solvable."""

from checker import judge
from levels import SPACE_WORLDS, all_drills, all_levels, round_level
from runner import run_code

REQUIRED_KEYS = {"id", "title", "brief", "lesson", "starter", "expected", "hidden", "hint", "concepts", "rounds"}


def test_every_drill_has_the_keys_and_ten_rounds():
    for drill in all_drills():
        assert set(drill.keys()) == REQUIRED_KEYS, f"drill {drill.get('id')} has wrong keys"
        assert len(drill["rounds"]) == 10, f"drill {drill['id']} needs ten rounds"
        for part in drill["rounds"]:
            for key in ("brief", "starter", "expected", "hidden", "hint", "tip"):
                assert key in part, f"drill {drill['id']} has a round without {key}"
        assert drill["lesson"].strip(), f"drill {drill['id']} has no lesson"


def test_ids_are_unique_across_levels_and_drills():
    ids = [level["id"] for level in all_levels()] + [drill["id"] for drill in all_drills()]
    assert len(ids) == len(set(ids))


def test_space_has_four_or_five_drills_per_world():
    counts = [len(world["levels"]) for world in SPACE_WORLDS]
    assert counts == [4, 4, 4, 5, 4, 5, 4, 4, 4], counts


def test_every_round_is_solved_by_the_hint_and_not_by_the_starter():
    for drill in all_drills():
        for number in range(len(drill["rounds"])):
            level = round_level(drill, number)
            solution = level["starter"] + level["hint"]
            result = run_code(solution, level["hidden"])
            verdict = judge(result, level, solution)
            assert verdict["passed"], f"{drill['id']} round {number + 1}: {verdict['diff']}"
            alone = run_code(level["starter"], level["hidden"])
            assert not judge(alone, level, level["starter"])["passed"], f"{drill['id']} round {number + 1} passes with the starter"


def test_every_round_is_a_different_task():
    """Ten faces of one concept: the briefs must all differ."""
    for drill in all_drills():
        briefs = {part["brief"] for part in drill["rounds"]}
        assert len(briefs) == 10, f"drill {drill['id']} repeats a task"
