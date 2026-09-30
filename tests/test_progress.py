import tempfile
from pathlib import Path

import progress


def fresh():
    progress.PROGRESS_FILE = Path(tempfile.mkdtemp()) / "progress.json"
    return progress.load()


def test_first_pass_gives_xp_stars_and_time():
    data = fresh()
    gained = progress.record_pass(data, "1-1", 3, 42)
    assert gained == 30
    assert data["xp"] == 30
    assert data["stars"]["1-1"] == 3
    assert data["times"]["1-1"] == 42


def test_stars_only_go_up_and_xp_only_for_improvement():
    data = fresh()
    progress.record_pass(data, "1-1", 2, 50)
    assert progress.record_pass(data, "1-1", 1, 20) == 0
    assert data["stars"]["1-1"] == 2
    assert progress.record_pass(data, "1-1", 3, 60) == 10
    assert data["xp"] == 30


def test_best_time_is_kept():
    data = fresh()
    progress.record_pass(data, "1-1", 3, 50)
    progress.record_pass(data, "1-1", 3, 20)
    progress.record_pass(data, "1-1", 3, 90)
    assert progress.best_time(data, "1-1") == 20


def test_saved_file_is_reloaded():
    data = fresh()
    progress.record_pass(data, "2-3", 3, 12)
    again = progress.load()
    assert again["stars"]["2-3"] == 3
    assert again["times"]["2-3"] == 12
    assert again["xp"] == 30


def test_format_time():
    assert progress.format_time(75) == "1:15"
    assert progress.format_time(5) == "0:05"


def test_calculate_stars():
    assert progress.calculate_stars(False, 1) == 3
    assert progress.calculate_stars(True, 1) == 2
    assert progress.calculate_stars(False, 6) == 1
