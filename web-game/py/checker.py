"""Judges a run of the player's code against a level.

A level only passes when all of these are true:
  1. the program finished without any error,
  2. on print levels, the expected output is not simply typed in as a literal,
  3. what it printed matches the expected output.
"""

import io
import tokenize


def normalize(text):
    """Turn output into a list of lines with trailing spaces removed.

    Empty lines at the very end are dropped, so "hi\n" and "hi" are equal.
    """
    lines = [line.rstrip() for line in text.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def check(actual, expected):
    """Return {"passed": bool, "diff": str}.

    diff is empty when passed, otherwise one short line describing
    the first place where the output is wrong.
    """
    actual_lines = normalize(actual)
    expected_lines = normalize(expected)

    if actual_lines == expected_lines:
        return {"passed": True, "diff": ""}

    return {"passed": False, "diff": first_difference(actual_lines, expected_lines)}


def first_difference(actual_lines, expected_lines):
    """Describe the first line that does not match."""
    longest = max(len(actual_lines), len(expected_lines))

    for index in range(longest):
        got = line_or_nothing(actual_lines, index)
        wanted = line_or_nothing(expected_lines, index)
        if got != wanted:
            return f"line {index + 1}: expected {wanted} but got {got}"

    return "outputs differ"


def line_or_nothing(lines, index):
    """Return the line in quotes, or the word nothing if it does not exist."""
    if index < len(lines):
        return f'"{lines[index]}"'
    return "nothing"


def judge(result, level, code):
    """The full verdict for one run. Returns {"passed": bool, "diff": str}.

    result is what runner.run_code returned, level is the level dict,
    code is what the player typed.
    """
    if result["exit_code"] != 0:
        return {"passed": False, "diff": "your code raised an error: " + last_line(result["stderr"])}

    hardcoded = hardcoded_answer(code, level)
    if hardcoded:
        return {
            "passed": False,
            "diff": f"don't type the answer, make the code produce it (found {hardcoded!r} in your code)",
        }

    return check(result["stdout"], level["expected"])


def last_line(text):
    lines = [line for line in text.strip().splitlines() if line.strip()]
    return lines[-1] if lines else "unknown error"


def hardcoded_answer(code, level):
    """On print levels, find an expected line the player typed in as a literal.

    Returns that line, or None. A literal counts as typed in when it appears
    more often in the player's code than in the starter, and the reference
    answer does not use it either. Function levels are skipped: their hidden
    code calls the function with several inputs, which already rules out a
    fixed answer.
    """
    if level["hidden"].strip():
        return None
    typed = literal_counts(code)
    given = literal_counts(level["starter"])
    allowed = literals_in(level["hint"])
    squashed_code = squash(code)
    squashed_starter = squash(level["starter"])
    squashed_hint = squash(level["hint"])

    for line in normalize(level["expected"]):
        line = line.strip()
        if not line or line in allowed:
            continue
        if typed.get(line, 0) > given.get(line, 0):
            return line
        # Also catch longer answers typed as a whole, like [1, 4, 9, 16, 25].
        whole = squash(line)
        if len(line) > 3 and whole not in squashed_hint:
            if squashed_code.count(whole) > squashed_starter.count(whole):
                return line
    return None


def literal_counts(code):
    """How many times each string, number, True, False or None literal appears."""
    counts = {}
    try:
        tokens = tokenize.generate_tokens(io.StringIO(code).readline)
        for token in tokens:
            value = None
            if token.type == tokenize.STRING:
                value = unquote(token.string)
            elif token.type == tokenize.NUMBER:
                value = token.string
            elif token.type == tokenize.NAME and token.string in ("True", "False", "None"):
                value = token.string
            if value is not None:
                counts[value] = counts.get(value, 0) + 1
    except (tokenize.TokenError, SyntaxError):
        pass
    return counts


def literals_in(code):
    """The set of literals used in some code."""
    return set(literal_counts(code))


def unquote(text):
    """Turn the source of a string literal, like '"hi"' or 'f"hi"', into hi."""
    while text and text[0] not in "\"'":
        text = text[1:]      # drop prefixes like f, r, b
    if len(text) >= 6 and text[:3] in ('"""', "'''"):
        return text[3:-3]
    return text[1:-1]


def squash(text):
    """Remove all whitespace, so spacing differences do not matter."""
    return "".join(text.split())
