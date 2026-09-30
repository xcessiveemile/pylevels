# Writing a level

A level is one Python dict. You add it to the `LEVELS` list in one of the
files in `levels/`. That is the whole job. No registration, no config.

## The shape

Every level has exactly these eight keys:

```python
{
    "id": "3-4",                       # world number, dash, level number. Must be unique.
    "title": "Count the vowels",       # short, shows at the top of the screen
    "brief": "Write vowels(text) that returns how many vowels are in text.",  # max two sentences
    "starter": "# define vowels here\n",   # what the editor starts with
    "expected": "3\n0\n",              # exact stdout that means "pass"
    "hidden": 'print(vowels("banana"))\nprint(vowels("xyz"))\n',   # runs after the player's code
    "hint": 'def vowels(text):\n    count = 0\n    for letter in text:\n        if letter in "aeiou":\n            count = count + 1\n    return count',
    "concepts": ["strings", "for", "if"],
}
```

## What each key does

- **id** — `"<world>-<number>"`. Look at the last level in the file and add one.
- **title** — three or four words.
- **brief** — one or two sentences. Say what to do, not how. The player
  learns by reading the starter, typing, running, and reading the error.
- **starter** — the code already in the editor when the level opens. Use
  `\n` for new lines. Can be empty `""`.
- **expected** — what the program must print. One `\n` per line. Trailing
  spaces on a line do not matter, but everything else must match exactly.
- **hidden** — code that runs *after* the player's code. Use it to call a
  function or class the player was asked to write. Leave as `""` when the
  player prints things directly.
- **hint** — the full answer. Shown when the player presses F2, and given
  to the tutor as the reference it must not reveal.
  The rule is: `starter + hint` must produce `expected`. That is what the
  test checks.
- **concepts** — a list of words, just for your own bookkeeping.

Two rules the game enforces on every level: the program must exit without an
error, and on levels with empty `hidden`, the player may not type an expected
line in as a literal unless your `hint` uses that literal too. So for a level
that gives `name = "Ada"` and expects `Ada`, `print("Ada")` fails and
`print(name)` passes. The tests check that the starter alone cannot pass and
that typing the expected output cannot pass.

## Two kinds of level

**Print levels.** The player prints something. `hidden` is empty.

```python
{
    "id": "3-5",
    "title": "Shout twice",
    "brief": "Print the word in upper case, twice, on one line with a space between.",
    "starter": 'word = "go"\n',
    "expected": "GO GO\n",
    "hidden": "",
    "hint": "print(word.upper(), word.upper())",
    "concepts": ["strings", "print"],
}
```

**Function levels.** The player defines something, `hidden` calls it.
Put two or three calls in `hidden` so a lucky guess does not pass.

```python
{
    "id": "4-4",
    "title": "Biggest",
    "brief": "Write biggest(numbers) that returns the largest number, without using max().",
    "starter": "# define biggest here\n",
    "expected": "9\n-1\n",
    "hidden": "print(biggest([3, 9, 2]))\nprint(biggest([-5, -1]))\n",
    "hint": "def biggest(numbers):\n    best = numbers[0]\n    for n in numbers:\n        if n > best:\n            best = n\n    return best",
    "concepts": ["lists", "for", "if"],
}
```

## Getting `expected` right

Do not type it by hand. Run the answer and copy what it prints:

```bash
python3 -c 'word = "go"
print(word.upper(), word.upper())'
```

Then put `\n` where the line breaks were.

## Check your level

```bash
python -m pytest tests/test_levels.py
```

This loads every level, checks the eight keys and unique ids, and runs
`starter + hint` to see that it prints `expected`. If your level fails,
the message tells you which line was wrong.

## Adding a whole world

1. Copy `levels/world_09_errors_files.py` to `levels/world_10_something.py`.
2. Change `WORLD` and replace the levels.
3. Open `levels/__init__.py` and add the new module to both the import
   and the `WORLD_MODULES` list.
4. Update the counts in `tests/test_levels.py::test_level_counts` (every
   world has 8 levels now, so add an 8, or the real count of your new world).


# Writing a drill (the space world)

Space drills live in `levels/space_XX_*.py` in a `DRILLS` list. A drill is one
concept shown ten different ways. The drill names the concept and carries a
`lesson`, a few sentences with a tiny example that the player reads at round
one. Each of its ten rounds is a small task of its own, with its own brief,
starter, expected output, hint and a one-line `tip` that names the piece of
Python it needs without giving the answer:

```python
{
    "id": "s1-5",
    "title": "Doubling",
    "brief": "Multiplying by two, in different shapes.",   # the concept
    "lesson": "Multiplying uses *. Example: 3 * 2 is 6.",
    "starter": "", "expected": "", "hidden": "", "hint": "",   # unused at this level
    "concepts": ["arithmetic"],
    "rounds": [
        {"brief": "Print n times two.", "starter": "n = 4\n", "expected": "8\n",
         "hidden": "", "hint": "print(n * 2)", "tip": "* multiplies"},
        {"brief": "Write double(x) that returns x times two.", "starter": "# define double here\n",
         "expected": "14\n", "hidden": "print(double(7))\n", "hint": "def double(x):\n    return x * 2"},
        # ... ten rounds, each a different task
    ],
}
```

The rounds follow the same rules as levels. The tests run `starter + hint`
for every round, check the starter alone never passes, and check that the ten
briefs are all different. Ten rounds is the rule: the point is to meet the
same idea from ten angles until you recognise it anywhere.
