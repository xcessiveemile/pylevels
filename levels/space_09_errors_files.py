WORLD = {'name': 'Errors & files', 'title': 'try / except, raise, files, json'}

# A drill is one concept shown ten different ways. Each round is its own
# small task with its own brief, starter, expected output and hint.
DRILLS = [
    {'id': 's9-1',
     'title': 'Try and except',
     'brief': 'Catching the specific error that can happen.',
     'lesson': 'try runs code that might fail; except SomeError: runs instead when that error happens. Catch the '
               'specific error: ValueError for bad conversions, ZeroDivisionError, IndexError, KeyError.  '
               'Example: try:  n = int(text)  except ValueError:  n = -1',
     'starter': '',
     'expected': '',
     'hidden': '',
     'hint': '',
     'concepts': ['try', 'except'],
     'rounds': [{'brief': 'Write to_int(text) returning int(text), or -1 when it is not a number.',
                 'starter': '# define to_int here\n',
                 'expected': '42\n-1\n',
                 'hidden': 'print(to_int("42"))\nprint(to_int("abc"))\n',
                 'hint': 'def to_int(text):\n'
                         '    try:\n'
                         '        return int(text)\n'
                         '    except ValueError:\n'
                         '        return -1',
                 'tip': 'try: ... except SomeError: ... catches that one error.'},
                {'brief': 'Write safe_divide(a, b) returning a / b, or "no" when b is zero.',
                 'starter': '# define safe_divide here\n',
                 'expected': '2.0\nno\n',
                 'hidden': 'print(safe_divide(4, 2))\nprint(safe_divide(1, 0))\n',
                 'hint': 'def safe_divide(a, b):\n'
                         '    try:\n'
                         '        return a / b\n'
                         '    except ZeroDivisionError:\n'
                         '        return "no"',
                 'tip': 'try: ... except SomeError: ... catches that one error.'},
                {'brief': 'Write get_item(items, i) returning items[i], or None when the index is out of range.',
                 'starter': '# define get_item here\n',
                 'expected': '2\nNone\n',
                 'hidden': 'print(get_item([1, 2], 1))\nprint(get_item([1, 2], 5))\n',
                 'hint': 'def get_item(items, i):\n'
                         '    try:\n'
                         '        return items[i]\n'
                         '    except IndexError:\n'
                         '        return None',
                 'tip': 'try: ... except SomeError: ... catches that one error.'},
                {'brief': 'Write lookup(d, key) returning d[key], or the text missing when the key is not there.',
                 'starter': '# define lookup here\n',
                 'expected': '1\nmissing\n',
                 'hidden': 'print(lookup({"a": 1}, "a"))\nprint(lookup({"a": 1}, "z"))\n',
                 'hint': 'def lookup(d, key):\n'
                         '    try:\n'
                         '        return d[key]\n'
                         '    except KeyError:\n'
                         '        return "missing"',
                 'tip': 'try: ... except SomeError: ... catches that one error.'},
                {'brief': 'Try to turn the text into a number and print it; if that fails print "not a number".',
                 'starter': 'text = "12x"\n',
                 'expected': 'not a number\n',
                 'hidden': '',
                 'hint': 'try:\n    print(int(text))\nexcept ValueError:\n    print("not a number")',
                 'tip': 'try: ... except SomeError: ... catches that one error.'},
                {'brief': 'Write to_float(text, fallback=0.0) returning float(text) or the fallback.',
                 'starter': '# define to_float here\n',
                 'expected': '2.5\n0.0\n9.9\n',
                 'hidden': 'print(to_float("2.5"))\nprint(to_float("x"))\nprint(to_float("x", 9.9))\n',
                 'hint': 'def to_float(text, fallback=0.0):\n'
                         '    try:\n'
                         '        return float(text)\n'
                         '    except ValueError:\n'
                         '        return fallback',
                 'tip': 'try: ... except SomeError: ... catches that one error.'},
                {'brief': 'Write add_strings(a, b) returning a + b, or None if adding raises a TypeError.',
                 'starter': '# define add_strings here\n',
                 'expected': 'ab\nNone\n',
                 'hidden': 'print(add_strings("a", "b"))\nprint(add_strings("a", 1))\n',
                 'hint': 'def add_strings(a, b):\n'
                         '    try:\n'
                         '        return a + b\n'
                         '    except TypeError:\n'
                         '        return None',
                 'tip': 'try: ... except SomeError: ... catches that one error.'},
                {'brief': 'Write mean(numbers) returning the average, or 0 for an empty list (catch the '
                          'ZeroDivisionError).',
                 'starter': '# define mean here\n',
                 'expected': '3.0\n0\n',
                 'hidden': 'print(mean([2, 4]))\nprint(mean([]))\n',
                 'hint': 'def mean(numbers):\n'
                         '    try:\n'
                         '        return sum(numbers) / len(numbers)\n'
                         '    except ZeroDivisionError:\n'
                         '        return 0',
                 'tip': 'try: ... except SomeError: ... catches that one error.'},
                {'brief': 'Write divide(a, b) that returns a / b, catches ZeroDivisionError returning None, and '
                          'prints "done" in finally every time.',
                 'starter': '# define divide here\n',
                 'expected': 'done\n2.0\ndone\nNone\n',
                 'hidden': 'print(divide(6, 3))\nprint(divide(1, 0))\n',
                 'hint': 'def divide(a, b):\n'
                         '    try:\n'
                         '        return a / b\n'
                         '    except ZeroDivisionError:\n'
                         '        return None\n'
                         '    finally:\n'
                         '        print("done")',
                 'tip': 'try: ... except SomeError: ... catches that one error.'},
                {'brief': 'Write parse_age(text) returning int(text) when it is a whole number between 0 and '
                          '120, else None (catch ValueError, check the range).',
                 'starter': '# define parse_age here\n',
                 'expected': '30\nNone\nNone\n',
                 'hidden': 'print(parse_age("30"))\nprint(parse_age("abc"))\nprint(parse_age("200"))\n',
                 'hint': 'def parse_age(text):\n'
                         '    try:\n'
                         '        age = int(text)\n'
                         '    except ValueError:\n'
                         '        return None\n'
                         '    if 0 <= age <= 120:\n'
                         '        return age\n'
                         '    return None',
                 'tip': 'try: ... except SomeError: ... catches that one error.'}]},
    {'id': 's9-2',
     'title': 'Raising errors',
     'brief': 'raise, custom exception classes, and error messages.',
     'lesson': 'raise ValueError("message") stops the function with an error on purpose. Your own error type is '
               'a class with (Exception) and pass inside. finally runs no matter what.  Example: if amount <= '
               '0:  raise ValueError("must be positive")',
     'starter': '',
     'expected': '',
     'hidden': '',
     'hint': '',
     'concepts': ['raise', 'exceptions'],
     'rounds': [{'brief': 'Write check_age(age) that raises ValueError("too young") below 18 and returns "ok" '
                          'otherwise.',
                 'starter': '# define check_age here\n',
                 'expected': 'ok\ntoo young\n',
                 'hidden': 'print(check_age(20))\n'
                           'try:\n'
                           '    check_age(10)\n'
                           'except ValueError as error:\n'
                           '    print(error)\n',
                 'hint': 'def check_age(age):\n'
                         '    if age < 18:\n'
                         '        raise ValueError("too young")\n'
                         '    return "ok"',
                 'tip': 'raise ValueError("message") stops with an error; class MyError(Exception): pass makes '
                        'your own.'},
                {'brief': 'Write withdraw(balance, amount) that raises ValueError("amount must be positive") for '
                          'amounts of 0 or less, else returns balance minus amount.',
                 'starter': '# define withdraw here\n',
                 'expected': '70\namount must be positive\n',
                 'hidden': 'print(withdraw(100, 30))\n'
                           'try:\n'
                           '    withdraw(100, -5)\n'
                           'except ValueError as error:\n'
                           '    print(error)\n',
                 'hint': 'def withdraw(balance, amount):\n'
                         '    if amount <= 0:\n'
                         '        raise ValueError("amount must be positive")\n'
                         '    return balance - amount',
                 'tip': 'raise ValueError("message") stops with an error; class MyError(Exception): pass makes '
                        'your own.'},
                {'brief': 'Write a class EmptyListError(Exception) and first(items) raising '
                          'EmptyListError("empty") for an empty list.',
                 'starter': '# define EmptyListError and first here\n',
                 'expected': '4\nempty\n',
                 'hidden': 'print(first([4, 5]))\n'
                           'try:\n'
                           '    first([])\n'
                           'except EmptyListError as error:\n'
                           '    print(error)\n',
                 'hint': 'class EmptyListError(Exception):\n'
                         '    pass\n'
                         '\n'
                         '\n'
                         'def first(items):\n'
                         '    if len(items) == 0:\n'
                         '        raise EmptyListError("empty")\n'
                         '    return items[0]',
                 'tip': 'raise ValueError("message") stops with an error; class MyError(Exception): pass makes '
                        'your own.'},
                {'brief': 'Write sqrt(n) raising ValueError("negative") when n is below 0, else returning n ** '
                          '0.5.',
                 'starter': '# define sqrt here\n',
                 'expected': '4.0\nnegative\n',
                 'hidden': 'print(sqrt(16))\ntry:\n    sqrt(-1)\nexcept ValueError as error:\n    print(error)\n',
                 'hint': 'def sqrt(n):\n    if n < 0:\n        raise ValueError("negative")\n    return n ** 0.5',
                 'tip': 'raise ValueError("message") stops with an error; class MyError(Exception): pass makes '
                        'your own.'},
                {'brief': 'Write class InsufficientFunds(Exception) and pay(balance, price) raising it with the '
                          'message "short by N" where N is the missing amount.',
                 'starter': '# define InsufficientFunds and pay here\n',
                 'expected': '30\nshort by 30\n',
                 'hidden': 'print(pay(50, 20))\n'
                           'try:\n'
                           '    pay(50, 80)\n'
                           'except InsufficientFunds as error:\n'
                           '    print(error)\n',
                 'hint': 'class InsufficientFunds(Exception):\n'
                         '    pass\n'
                         '\n'
                         '\n'
                         'def pay(balance, price):\n'
                         '    if price > balance:\n'
                         '        raise InsufficientFunds(f"short by {price - balance}")\n'
                         '    return balance - price',
                 'tip': 'raise ValueError("message") stops with an error; class MyError(Exception): pass makes '
                        'your own.'},
                {'brief': 'Write set_speed(speed) raising TypeError("speed must be a number") when speed is a '
                          'string, else returning speed.',
                 'starter': '# define set_speed here\n',
                 'expected': '30\nspeed must be a number\n',
                 'hidden': 'print(set_speed(30))\n'
                           'try:\n'
                           '    set_speed("fast")\n'
                           'except TypeError as error:\n'
                           '    print(error)\n',
                 'hint': 'def set_speed(speed):\n'
                         '    if isinstance(speed, str):\n'
                         '        raise TypeError("speed must be a number")\n'
                         '    return speed',
                 'tip': 'raise ValueError("message") stops with an error; class MyError(Exception): pass makes '
                        'your own.'},
                {'brief': 'Write must_be_positive(n) that raises ValueError with the message including n, like '
                          '"-3 is not positive", when n is 0 or less.',
                 'starter': '# define must_be_positive here\n',
                 'expected': '5\n-3 is not positive\n',
                 'hidden': 'print(must_be_positive(5))\n'
                           'try:\n'
                           '    must_be_positive(-3)\n'
                           'except ValueError as error:\n'
                           '    print(error)\n',
                 'hint': 'def must_be_positive(n):\n'
                         '    if n <= 0:\n'
                         '        raise ValueError(f"{n} is not positive")\n'
                         '    return n',
                 'tip': 'raise ValueError("message") stops with an error; class MyError(Exception): pass makes '
                        'your own.'},
                {'brief': 'Write validate(user) raising KeyError("name") when the dict has no name key, else '
                          'returning the name.',
                 'starter': '# define validate here\n',
                 'expected': "Ada\nmissing 'name'\n",
                 'hidden': 'print(validate({"name": "Ada"}))\n'
                           'try:\n'
                           '    validate({})\n'
                           'except KeyError as error:\n'
                           '    print("missing", error)\n',
                 'hint': 'def validate(user):\n'
                         '    if "name" not in user:\n'
                         '        raise KeyError("name")\n'
                         '    return user["name"]',
                 'tip': 'raise ValueError("message") stops with an error; class MyError(Exception): pass makes '
                        'your own.'},
                {'brief': 'Write class TooLong(Exception) and short_name(name) raising TooLong("max 5") for '
                          'names over 5 letters, else returning the name.',
                 'starter': '# define TooLong and short_name here\n',
                 'expected': 'Ada\nmax 5\n',
                 'hidden': 'print(short_name("Ada"))\n'
                           'try:\n'
                           '    short_name("Alexander")\n'
                           'except TooLong as error:\n'
                           '    print(error)\n',
                 'hint': 'class TooLong(Exception):\n'
                         '    pass\n'
                         '\n'
                         '\n'
                         'def short_name(name):\n'
                         '    if len(name) > 5:\n'
                         '        raise TooLong("max 5")\n'
                         '    return name',
                 'tip': 'raise ValueError("message") stops with an error; class MyError(Exception): pass makes '
                        'your own.'},
                {'brief': 'Write retry_int(texts) that returns the first text that converts to an int, and '
                          'raises ValueError("none") if none does.',
                 'starter': '# define retry_int here\n',
                 'expected': '7\nnone\n',
                 'hidden': 'print(retry_int(["a", "7", "9"]))\n'
                           'try:\n'
                           '    retry_int(["a", "b"])\n'
                           'except ValueError as error:\n'
                           '    print(error)\n',
                 'hint': 'def retry_int(texts):\n'
                         '    for text in texts:\n'
                         '        try:\n'
                         '            return int(text)\n'
                         '        except ValueError:\n'
                         '            pass\n'
                         '    raise ValueError("none")',
                 'tip': 'raise ValueError("message") stops with an error; class MyError(Exception): pass makes '
                        'your own.'}]},
    {'id': 's9-3',
     'title': 'Files',
     'brief': 'Writing, reading, appending and looping over lines.',
     'lesson': 'with open(path, "w") as f: opens a file for writing and closes it for you; f.write(text) writes. '
               'open(path) reads: f.read() gives all the text, looping over f gives lines. Mode "a" appends.  '
               'Example: with open("notes.txt") as f:  text = f.read()',
     'starter': '',
     'expected': '',
     'hidden': '',
     'hint': '',
     'concepts': ['files', 'with', 'open'],
     'rounds': [{'brief': 'Write the word to notes.txt, then read the file and print its contents.',
                 'starter': 'word = "hello"\n',
                 'expected': 'hello\n',
                 'hidden': '',
                 'hint': 'with open("notes.txt", "w") as f:\n'
                         '    f.write(word)\n'
                         '\n'
                         'with open("notes.txt") as f:\n'
                         '    print(f.read())',
                 'tip': 'with open(path, "w") as f: f.write(text); with open(path) as f: f.read().'},
                {'brief': 'Write the items to list.txt one per line, then read it back and print it.',
                 'starter': 'items = ["milk", "eggs"]\n',
                 'expected': 'milk\neggs\n',
                 'hidden': '',
                 'hint': 'with open("list.txt", "w") as f:\n'
                         '    for item in items:\n'
                         '        f.write(item + "\\n")\n'
                         '\n'
                         'with open("list.txt") as f:\n'
                         '    print(f.read(), end="")',
                 'tip': 'with open(path, "w") as f: f.write(text); with open(path) as f: f.read().'},
                {'brief': 'Write three lines to a file, then print how many lines it has.',
                 'starter': 'lines = ["a", "b", "c"]\n',
                 'expected': '3\n',
                 'hidden': '',
                 'hint': 'with open("f.txt", "w") as f:\n'
                         '    for line in lines:\n'
                         '        f.write(line + "\\n")\n'
                         '\n'
                         'with open("f.txt") as f:\n'
                         '    print(len(f.read().splitlines()))',
                 'tip': 'with open(path, "w") as f: f.write(text); with open(path) as f: f.read().'},
                {'brief': 'Write the lines to a file, then print each line in upper case by looping over the '
                          'file.',
                 'starter': 'lines = ["sun", "moon"]\n',
                 'expected': 'SUN\nMOON\n',
                 'hidden': '',
                 'hint': 'with open("f.txt", "w") as f:\n'
                         '    for line in lines:\n'
                         '        f.write(line + "\\n")\n'
                         '\n'
                         'with open("f.txt") as f:\n'
                         '    for line in f:\n'
                         '        print(line.strip().upper())',
                 'tip': 'with open(path, "w") as f: f.write(text); with open(path) as f: f.read().'},
                {'brief': 'Write first to a file, then append second with mode a, then print the file.',
                 'starter': 'first = "one\\n"\nsecond = "two\\n"\n',
                 'expected': 'one\ntwo\n',
                 'hidden': '',
                 'hint': 'with open("f.txt", "w") as f:\n'
                         '    f.write(first)\n'
                         'with open("f.txt", "a") as f:\n'
                         '    f.write(second)\n'
                         'with open("f.txt") as f:\n'
                         '    print(f.read(), end="")',
                 'tip': 'with open(path, "w") as f: f.write(text); with open(path) as f: f.read().'},
                {'brief': 'Write the numbers to a file one per line, then read them back and print their sum.',
                 'starter': 'numbers = [3, 4, 5]\n',
                 'expected': '12\n',
                 'hidden': '',
                 'hint': 'with open("n.txt", "w") as f:\n'
                         '    for n in numbers:\n'
                         '        f.write(str(n) + "\\n")\n'
                         '\n'
                         'total = 0\n'
                         'with open("n.txt") as f:\n'
                         '    for line in f:\n'
                         '        total = total + int(line)\n'
                         'print(total)',
                 'tip': 'with open(path, "w") as f: f.write(text); with open(path) as f: f.read().'},
                {'brief': 'Write the words to a file, then print how many lines contain the letter a.',
                 'starter': 'words = ["apple", "kiwi", "banana"]\n',
                 'expected': '2\n',
                 'hidden': '',
                 'hint': 'with open("w.txt", "w") as f:\n'
                         '    for word in words:\n'
                         '        f.write(word + "\\n")\n'
                         '\n'
                         'count = 0\n'
                         'with open("w.txt") as f:\n'
                         '    for line in f:\n'
                         '        if "a" in line:\n'
                         '            count = count + 1\n'
                         'print(count)',
                 'tip': 'with open(path, "w") as f: f.write(text); with open(path) as f: f.read().'},
                {'brief': 'Write read_lines(path) that returns the list of lines without newlines, or an empty '
                          'list when the file is missing.',
                 'starter': '# define read_lines here\n',
                 'expected': "['x', 'y']\n[]\n",
                 'hidden': 'with open("a.txt", "w") as f:\n'
                           '    f.write("x\\ny\\n")\n'
                           'print(read_lines("a.txt"))\n'
                           'print(read_lines("nope.txt"))\n',
                 'hint': 'def read_lines(path):\n'
                         '    try:\n'
                         '        with open(path) as f:\n'
                         '            return f.read().splitlines()\n'
                         '    except FileNotFoundError:\n'
                         '        return []',
                 'tip': 'with open(path, "w") as f: f.write(text); with open(path) as f: f.read().'},
                {'brief': 'Write save(path, items) that writes items one per line and returns how many it wrote.',
                 'starter': '# define save here\n',
                 'expected': '3\na\nb\nc\n',
                 'hidden': 'print(save("s.txt", ["a", "b", "c"]))\n'
                           'with open("s.txt") as f:\n'
                           '    print(f.read(), end="")\n',
                 'hint': 'def save(path, items):\n'
                         '    with open(path, "w") as f:\n'
                         '        for item in items:\n'
                         '            f.write(item + "\\n")\n'
                         '    return len(items)',
                 'tip': 'with open(path, "w") as f: f.write(text); with open(path) as f: f.read().'},
                {'brief': 'Write the text to a file, then read it and print the longest line.',
                 'starter': 'text = "hi\\nhello there\\nyo\\n"\n',
                 'expected': 'hello there\n',
                 'hidden': '',
                 'hint': 'with open("t.txt", "w") as f:\n'
                         '    f.write(text)\n'
                         '\n'
                         'with open("t.txt") as f:\n'
                         '    lines = f.read().splitlines()\n'
                         'print(max(lines, key=len))',
                 'tip': 'with open(path, "w") as f: f.write(text); with open(path) as f: f.read().'}]},
    {'id': 's9-4',
     'title': 'JSON and imports',
     'brief': 'json.loads, json.dumps, files with json, and the standard library.',
     'lesson': 'import brings in a module: json.loads turns JSON text into Python data, json.dumps the other '
               'way, json.load and json.dump do the same with files. math, collections and others come with '
               'Python.  Example: import json, then data = json.loads(text)',
     'starter': '',
     'expected': '',
     'hidden': '',
     'hint': '',
     'concepts': ['json', 'import'],
     'rounds': [{'brief': 'Turn the JSON text into a dict and print the name.',
                 'starter': 'text = \'{"name": "Ada", "age": 36}\'\n',
                 'expected': 'Ada\n',
                 'hidden': '',
                 'hint': 'import json\n\ndata = json.loads(text)\nprint(data["name"])',
                 'tip': 'import json; json.loads(text), json.dumps(data), json.load(f), json.dump(data, f).'},
                {'brief': 'Print the dict as a JSON string using json.dumps.',
                 'starter': 'data = {"a": 1, "b": [1, 2]}\n',
                 'expected': '{"a": 1, "b": [1, 2]}\n',
                 'hidden': '',
                 'hint': 'import json\n\nprint(json.dumps(data))',
                 'tip': 'import json; json.loads(text), json.dumps(data), json.load(f), json.dump(data, f).'},
                {'brief': 'Parse the JSON list and print how many items it has.',
                 'starter': "text = '[1, 2, 3, 4]'\n",
                 'expected': '4\n',
                 'hidden': '',
                 'hint': 'import json\n\nprint(len(json.loads(text)))',
                 'tip': 'import json; json.loads(text), json.dumps(data), json.load(f), json.dump(data, f).'},
                {'brief': 'Write the dict to data.json with json.dump, read it back with json.load, and print '
                          'the age.',
                 'starter': 'user = {"name": "Bo", "age": 25}\n',
                 'expected': '25\n',
                 'hidden': '',
                 'hint': 'import json\n'
                         '\n'
                         'with open("data.json", "w") as f:\n'
                         '    json.dump(user, f)\n'
                         '\n'
                         'with open("data.json") as f:\n'
                         '    print(json.load(f)["age"])',
                 'tip': 'import json; json.loads(text), json.dumps(data), json.load(f), json.dump(data, f).'},
                {'brief': 'Print the square root of n using the math module.',
                 'starter': 'n = 144\n',
                 'expected': '12.0\n',
                 'hidden': '',
                 'hint': 'import math\n\nprint(math.sqrt(n))',
                 'tip': 'import json; json.loads(text), json.dumps(data), json.load(f), json.dump(data, f).'},
                {'brief': 'Print the value of pi rounded to 4 decimals, imported from math.',
                 'starter': '',
                 'expected': '3.1416\n',
                 'hidden': '',
                 'hint': 'from math import pi\n\nprint(round(pi, 4))',
                 'tip': 'import json; json.loads(text), json.dumps(data), json.load(f), json.dump(data, f).'},
                {'brief': 'Print the three most common words using Counter from collections.',
                 'starter': 'words = ["a", "b", "a", "c", "a", "b"]\n',
                 'expected': "[('a', 3), ('b', 2)]\n",
                 'hidden': '',
                 'hint': 'from collections import Counter\n\nprint(Counter(words).most_common(2))',
                 'tip': 'import json; json.loads(text), json.dumps(data), json.load(f), json.dump(data, f).'},
                {'brief': 'Write users_over(path, age) reading a JSON list of users from the file and returning '
                          'the names older than age, or [] when the file is missing.',
                 'starter': '# define users_over here\n',
                 'expected': "['A']\n[]\n",
                 'hidden': 'import json\n'
                           'with open("u.json", "w") as f:\n'
                           '    json.dump([{"name": "A", "age": 30}, {"name": "B", "age": 12}], f)\n'
                           'print(users_over("u.json", 18))\n'
                           'print(users_over("missing.json", 18))\n',
                 'hint': 'import json\n'
                         '\n'
                         '\n'
                         'def users_over(path, age):\n'
                         '    try:\n'
                         '        with open(path) as f:\n'
                         '            users = json.load(f)\n'
                         '    except FileNotFoundError:\n'
                         '        return []\n'
                         '    return [u["name"] for u in users if u["age"] > age]',
                 'tip': 'import json; json.loads(text), json.dumps(data), json.load(f), json.dump(data, f).'},
                {'brief': 'Parse the JSON text and print the second tag of the first user.',
                 'starter': 'text = \'{"users": [{"name": "A", "tags": ["x", "y"]}]}\'\n',
                 'expected': 'y\n',
                 'hidden': '',
                 'hint': 'import json\n\ndata = json.loads(text)\nprint(data["users"][0]["tags"][1])',
                 'tip': 'import json; json.loads(text), json.dumps(data), json.load(f), json.dump(data, f).'},
                {'brief': 'Print the dict as JSON with an indent of 2.',
                 'starter': 'data = {"a": 1}\n',
                 'expected': '{\n  "a": 1\n}\n',
                 'hidden': '',
                 'hint': 'import json\n\nprint(json.dumps(data, indent=2))',
                 'tip': 'import json; json.loads(text), json.dumps(data), json.load(f), json.dump(data, f).'}]},
    # add your own drills here
]
