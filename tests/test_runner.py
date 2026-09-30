import time

from runner import run_code, TIMEOUT_SECONDS


def test_captures_stdout():
    result = run_code('print("hi")\nprint(1 + 1)')
    assert result["stdout"] == "hi\n2\n"
    assert result["stderr"] == ""
    assert result["timed_out"] is False


def test_exit_code_is_zero_on_success_and_not_on_error():
    assert run_code("print(1)")["exit_code"] == 0
    assert run_code("print(1)\nraise ValueError('no')")["exit_code"] != 0


def test_captures_traceback():
    result = run_code("print(missing_name)")
    assert result["stdout"] == ""
    assert "NameError" in result["stderr"]
    assert "missing_name" in result["stderr"]
    assert result["timed_out"] is False


def test_traceback_hides_temp_path():
    result = run_code("1 / 0")
    assert "your_code.py" in result["stderr"]
    assert "player_code.py" not in result["stderr"]


def test_hidden_code_runs_after_user_code():
    result = run_code("def f():\n    return 42", hidden_code="print(f())\n")
    assert result["stdout"] == "42\n"


def test_infinite_loop_is_killed_within_timeout():
    start = time.monotonic()
    result = run_code("while True:\n    pass")
    elapsed = time.monotonic() - start
    assert result["timed_out"] is True
    assert elapsed < TIMEOUT_SECONDS + 1


def test_input_does_not_hang():
    result = run_code("x = input()")
    assert result["timed_out"] is False
    assert "EOFError" in result["stderr"]
