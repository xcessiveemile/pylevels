from checker import check


def test_exact_match_passes():
    result = check("11\n", "11\n")
    assert result["passed"] is True
    assert result["diff"] == ""


def test_trailing_whitespace_on_lines_is_ignored():
    result = check("hello   \nworld \n\n\n", "hello\nworld\n")
    assert result["passed"] is True


def test_missing_final_newline_is_ignored():
    assert check("hello", "hello\n")["passed"] is True


def test_wrong_output_fails_with_useful_diff():
    result = check("4 7\n", "11\n")
    assert result["passed"] is False
    assert result["diff"] == 'line 1: expected "11" but got "4 7"'


def test_diff_points_at_first_wrong_line():
    result = check("a\nb\nx\n", "a\nb\nc\n")
    assert result["diff"] == 'line 3: expected "c" but got "x"'


def test_missing_line_is_reported():
    result = check("a\n", "a\nb\n")
    assert result["diff"] == 'line 2: expected "b" but got nothing'


def test_extra_line_is_reported():
    result = check("a\nb\n", "a\n")
    assert result["diff"] == 'line 2: expected nothing but got "b"'


def test_leading_whitespace_still_matters():
    assert check("  a\n", "a\n")["passed"] is False


# ---------------------------------------------------------------- judge

from checker import judge, hardcoded_answer

PRINT_LEVEL = {
    "id": "1-3", "title": "Two numbers, one line",
    "brief": "Print the sum of a and b on one line.",
    "starter": "a = 4\nb = 7\n", "expected": "11\n", "hidden": "",
    "hint": "print(a + b)", "concepts": ["print"],
}
HELLO_LEVEL = {
    "id": "1-1", "title": "Hello", "brief": "Print the word hello.",
    "starter": "", "expected": "hello\n", "hidden": "",
    "hint": 'print("hello")', "concepts": ["print"],
}
FUNCTION_LEVEL = {
    "id": "2-3", "title": "Even check", "brief": "Write is_even(n).",
    "starter": "", "expected": "True\nFalse\n",
    "hidden": "print(is_even(4))\nprint(is_even(7))\n",
    "hint": "def is_even(n):\n    return n % 2 == 0", "concepts": [],
}


def ok(stdout):
    return {"stdout": stdout, "stderr": "", "timed_out": False, "exit_code": 0}


def test_right_output_but_crash_fails():
    result = {"stdout": "11\n", "stderr": "Traceback...\nNameError: name 'x' is not defined", "timed_out": False, "exit_code": 1}
    verdict = judge(result, PRINT_LEVEL, "a = 4\nb = 7\nprint(a + b)\nprint(x)")
    assert verdict["passed"] is False
    assert "NameError" in verdict["diff"]


def test_typing_the_answer_fails():
    verdict = judge(ok("11\n"), PRINT_LEVEL, "a = 4\nb = 7\nprint(11)")
    assert verdict["passed"] is False
    assert "don't type the answer" in verdict["diff"]


def test_typing_the_answer_as_string_fails():
    verdict = judge(ok("11\n"), PRINT_LEVEL, 'a = 4\nb = 7\nprint("11")')
    assert verdict["passed"] is False


def test_computing_the_answer_passes():
    assert judge(ok("11\n"), PRINT_LEVEL, "a = 4\nb = 7\nprint(a + b)")["passed"] is True


def test_literal_is_allowed_when_the_reference_answer_uses_it():
    assert judge(ok("hello\n"), HELLO_LEVEL, 'print("hello")')["passed"] is True


def test_function_levels_are_not_checked_for_literals():
    code = "def is_even(n):\n    if n % 2 == 0:\n        return True\n    return False"
    assert judge(ok("True\nFalse\n"), FUNCTION_LEVEL, code)["passed"] is True


def test_whole_list_typed_in_is_caught():
    level = dict(PRINT_LEVEL, expected="[1, 4, 9, 16, 25]\n", hint="print([n * n for n in range(1, 6)])")
    assert hardcoded_answer("print([1, 4, 9, 16, 25])", level) == "[1, 4, 9, 16, 25]"
    assert hardcoded_answer("print([n * n for n in range(1, 6)])", level) is None


def test_wrong_output_still_reports_the_line():
    verdict = judge(ok("4 7\n"), PRINT_LEVEL, "a = 4\nb = 7\nprint(a, b)")
    assert verdict["diff"] == 'line 1: expected "11" but got "4 7"'


def test_reusing_a_starter_literal_is_caught():
    level = {
        "id": "1-2", "title": "Two lines", "brief": "Print the name and age.",
        "starter": 'name = "Ada"\nage = 36\n', "expected": "Ada\n36\n", "hidden": "",
        "hint": "print(name)\nprint(age)", "concepts": [],
    }
    assert hardcoded_answer('name = "Ada"\nage = 36\nprint("Ada")\nprint(36)', level) == "Ada"
    assert hardcoded_answer('name = "Ada"\nage = 36\nprint(name)\nprint(age)', level) is None
