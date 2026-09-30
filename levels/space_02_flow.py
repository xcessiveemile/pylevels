WORLD = {'name': 'Flow', 'title': 'comparisons, if / elif / else, and / or / not'}

# A drill is one concept shown ten different ways. Each round is its own
# small task with its own brief, starter, expected output and hint.
DRILLS = [
    {'id': 's2-1',
     'title': 'Comparisons',
     'brief': 'Comparing values gives True or False.',
     'lesson': 'Comparing two values gives True or False: >, <, >=, <=, == for equal, != for not equal. You can '
               'print the result or keep it in a variable.  Example: 5 > 3 is True',
     'starter': '',
     'expected': '',
     'hidden': '',
     'hint': '',
     'concepts': ['comparisons', 'booleans'],
     'rounds': [{'brief': 'Print whether a is bigger than b.',
                 'starter': 'a = 9\nb = 4\n',
                 'expected': 'True\n',
                 'hidden': '',
                 'hint': 'print(a > b)',
                 'tip': '==, !=, <, >, <=, >= give True or False.'},
                {'brief': 'Print whether a and b are equal.',
                 'starter': 'a = 9\nb = 4\n',
                 'expected': 'False\n',
                 'hidden': '',
                 'hint': 'print(a == b)',
                 'tip': '==, !=, <, >, <=, >= give True or False.'},
                {'brief': 'Print whether a is not equal to b.',
                 'starter': 'a = 9\nb = 4\n',
                 'expected': 'True\n',
                 'hidden': '',
                 'hint': 'print(a != b)',
                 'tip': '==, !=, <, >, <=, >= give True or False.'},
                {'brief': 'Print whether age is at least 18.',
                 'starter': 'age = 17\n',
                 'expected': 'False\n',
                 'hidden': '',
                 'hint': 'print(age >= 18)',
                 'tip': '==, !=, <, >, <=, >= give True or False.'},
                {'brief': 'Print whether temp is below zero.',
                 'starter': 'temp = -3\n',
                 'expected': 'True\n',
                 'hidden': '',
                 'hint': 'print(temp < 0)',
                 'tip': '==, !=, <, >, <=, >= give True or False.'},
                {'brief': 'Print whether the two words are the same.',
                 'starter': 'a = "moon"\nb = "Moon"\n',
                 'expected': 'False\n',
                 'hidden': '',
                 'hint': 'print(a == b)',
                 'tip': '==, !=, <, >, <=, >= give True or False.'},
                {'brief': 'Print whether n is between 1 and 10, using one chained comparison.',
                 'starter': 'n = 7\n',
                 'expected': 'True\n',
                 'hidden': '',
                 'hint': 'print(1 <= n <= 10)',
                 'tip': '==, !=, <, >, <=, >= give True or False.'},
                {'brief': 'Print whether the list is empty by comparing its length to 0.',
                 'starter': 'items = []\n',
                 'expected': 'True\n',
                 'hidden': '',
                 'hint': 'print(len(items) == 0)',
                 'tip': '==, !=, <, >, <=, >= give True or False.'},
                {'brief': 'Print whether word comes before other alphabetically.',
                 'starter': 'word = "apple"\nother = "banana"\n',
                 'expected': 'True\n',
                 'hidden': '',
                 'hint': 'print(word < other)',
                 'tip': '==, !=, <, >, <=, >= give True or False.'},
                {'brief': 'Store whether n is even in a variable called even, then print even.',
                 'starter': 'n = 10\n',
                 'expected': 'True\n',
                 'hidden': '',
                 'hint': 'even = n % 2 == 0\nprint(even)',
                 'tip': '==, !=, <, >, <=, >= give True or False.'}]},
    {'id': 's2-2',
     'title': 'If and else',
     'brief': 'Doing one thing or another depending on a condition.',
     'lesson': 'if checks a condition and runs the indented block when it is true; else runs the other block. Do '
               'not forget the colon at the end of the if line.  Example: if x > 0:  print("positive")  else:  '
               'print("not")',
     'starter': '',
     'expected': '',
     'hidden': '',
     'hint': '',
     'concepts': ['if', 'else'],
     'rounds': [{'brief': 'Print "hot" if temp is above 25, otherwise print "fine".',
                 'starter': 'temp = 31\n',
                 'expected': 'hot\n',
                 'hidden': '',
                 'hint': 'if temp > 25:\n    print("hot")\nelse:\n    print("fine")',
                 'tip': 'if condition: then an indented block, else: for the other case. Colons matter.'},
                {'brief': 'Print "adult" if age is 18 or more, otherwise "minor".',
                 'starter': 'age = 12\n',
                 'expected': 'minor\n',
                 'hidden': '',
                 'hint': 'if age >= 18:\n    print("adult")\nelse:\n    print("minor")',
                 'tip': 'if condition: then an indented block, else: for the other case. Colons matter.'},
                {'brief': 'Print "even" or "odd" for n.',
                 'starter': 'n = 13\n',
                 'expected': 'odd\n',
                 'hidden': '',
                 'hint': 'if n % 2 == 0:\n    print("even")\nelse:\n    print("odd")',
                 'tip': 'if condition: then an indented block, else: for the other case. Colons matter.'},
                {'brief': 'Print "empty" if the list has no items, otherwise print how many it has.',
                 'starter': 'items = [3, 1, 4]\n',
                 'expected': '3\n',
                 'hidden': '',
                 'hint': 'if len(items) == 0:\n    print("empty")\nelse:\n    print(len(items))',
                 'tip': 'if condition: then an indented block, else: for the other case. Colons matter.'},
                {'brief': 'Print "yes" only if logged_in is True. Print nothing otherwise.',
                 'starter': 'logged_in = True\n',
                 'expected': 'yes\n',
                 'hidden': '',
                 'hint': 'if logged_in:\n    print("yes")',
                 'tip': 'if condition: then an indented block, else: for the other case. Colons matter.'},
                {'brief': 'Print the bigger of a and b using if and else.',
                 'starter': 'a = 14\nb = 22\n',
                 'expected': '22\n',
                 'hidden': '',
                 'hint': 'if a > b:\n    print(a)\nelse:\n    print(b)',
                 'tip': 'if condition: then an indented block, else: for the other case. Colons matter.'},
                {'brief': 'Print "free" if price is 0, otherwise print the price.',
                 'starter': 'price = 0\n',
                 'expected': 'free\n',
                 'hidden': '',
                 'hint': 'if price == 0:\n    print("free")\nelse:\n    print(price)',
                 'tip': 'if condition: then an indented block, else: for the other case. Colons matter.'},
                {'brief': 'Print "long" if the word has more than 5 letters, otherwise "short".',
                 'starter': 'word = "planetary"\n',
                 'expected': 'long\n',
                 'hidden': '',
                 'hint': 'if len(word) > 5:\n    print("long")\nelse:\n    print("short")',
                 'tip': 'if condition: then an indented block, else: for the other case. Colons matter.'},
                {'brief': 'Set label to "pass" if score is 50 or more, else "fail", in one line with a '
                          'conditional expression, then print label.',
                 'starter': 'score = 64\n',
                 'expected': 'pass\n',
                 'hidden': '',
                 'hint': 'label = "pass" if score >= 50 else "fail"\nprint(label)',
                 'tip': 'if condition: then an indented block, else: for the other case. Colons matter.'},
                {'brief': 'Print "weekend" if day is "sat" or "sun", otherwise "weekday".',
                 'starter': 'day = "sun"\n',
                 'expected': 'weekend\n',
                 'hidden': '',
                 'hint': 'if day == "sat" or day == "sun":\n    print("weekend")\nelse:\n    print("weekday")',
                 'tip': 'if condition: then an indented block, else: for the other case. Colons matter.'}]},
    {'id': 's2-3',
     'title': 'Elif chains',
     'brief': 'Several conditions in a row: the first true one wins.',
     'lesson': 'elif adds more checks in a row. Python goes down the list and runs the first block whose '
               'condition is true, then skips the rest.  Example: if n < 0: ... elif n == 0: ... else: ...',
     'starter': '',
     'expected': '',
     'hidden': '',
     'hint': '',
     'concepts': ['if', 'elif', 'else'],
     'rounds': [{'brief': 'Print "negative", "zero" or "positive" for n.',
                 'starter': 'n = 0\n',
                 'expected': 'zero\n',
                 'hidden': '',
                 'hint': 'if n < 0:\n'
                         '    print("negative")\n'
                         'elif n == 0:\n'
                         '    print("zero")\n'
                         'else:\n'
                         '    print("positive")',
                 'tip': 'if ... elif ... else: the first true condition wins.'},
                {'brief': 'Print "cold" below 10, "mild" up to 20, "warm" above.',
                 'starter': 'temp = 23\n',
                 'expected': 'warm\n',
                 'hidden': '',
                 'hint': 'if temp < 10:\n'
                         '    print("cold")\n'
                         'elif temp <= 20:\n'
                         '    print("mild")\n'
                         'else:\n'
                         '    print("warm")',
                 'tip': 'if ... elif ... else: the first true condition wins.'},
                {'brief': 'Write grade(score): "A" from 90, "B" from 80, "C" from 70, else "F".',
                 'starter': '# define grade here\n',
                 'expected': 'A\nB\nC\nF\n',
                 'hidden': 'print(grade(95))\nprint(grade(82))\nprint(grade(71))\nprint(grade(10))\n',
                 'hint': 'def grade(score):\n'
                         '    if score >= 90:\n'
                         '        return "A"\n'
                         '    elif score >= 80:\n'
                         '        return "B"\n'
                         '    elif score >= 70:\n'
                         '        return "C"\n'
                         '    else:\n'
                         '        return "F"',
                 'tip': 'if ... elif ... else: the first true condition wins.'},
                {'brief': 'Write size(cm): "S" below 170, "M" below 180, else "L".',
                 'starter': '# define size here\n',
                 'expected': 'S\nM\nL\n',
                 'hidden': 'print(size(160))\nprint(size(175))\nprint(size(190))\n',
                 'hint': 'def size(cm):\n'
                         '    if cm < 170:\n'
                         '        return "S"\n'
                         '    elif cm < 180:\n'
                         '        return "M"\n'
                         '    else:\n'
                         '        return "L"',
                 'tip': 'if ... elif ... else: the first true condition wins.'},
                {'brief': 'Print "morning" before 12, "afternoon" before 18, otherwise "evening".',
                 'starter': 'hour = 15\n',
                 'expected': 'afternoon\n',
                 'hidden': '',
                 'hint': 'if hour < 12:\n'
                         '    print("morning")\n'
                         'elif hour < 18:\n'
                         '    print("afternoon")\n'
                         'else:\n'
                         '    print("evening")',
                 'tip': 'if ... elif ... else: the first true condition wins.'},
                {'brief': 'Write ticket(age): 0 under 4, 5 under 12, 12 under 65, else 7.',
                 'starter': '# define ticket here\n',
                 'expected': '0\n5\n12\n7\n',
                 'hidden': 'print(ticket(2))\nprint(ticket(9))\nprint(ticket(40))\nprint(ticket(70))\n',
                 'hint': 'def ticket(age):\n'
                         '    if age < 4:\n'
                         '        return 0\n'
                         '    elif age < 12:\n'
                         '        return 5\n'
                         '    elif age < 65:\n'
                         '        return 12\n'
                         '    else:\n'
                         '        return 7',
                 'tip': 'if ... elif ... else: the first true condition wins.'},
                {'brief': 'Print "one", "two" or "many" depending on count being 1, 2 or more.',
                 'starter': 'count = 2\n',
                 'expected': 'two\n',
                 'hidden': '',
                 'hint': 'if count == 1:\n'
                         '    print("one")\n'
                         'elif count == 2:\n'
                         '    print("two")\n'
                         'else:\n'
                         '    print("many")',
                 'tip': 'if ... elif ... else: the first true condition wins.'},
                {'brief': 'Write state(temp): "ice" at 0 or below, "steam" at 100 or above, else "water".',
                 'starter': '# define state here\n',
                 'expected': 'ice\nwater\nsteam\n',
                 'hidden': 'print(state(-4))\nprint(state(50))\nprint(state(120))\n',
                 'hint': 'def state(temp):\n'
                         '    if temp <= 0:\n'
                         '        return "ice"\n'
                         '    elif temp >= 100:\n'
                         '        return "steam"\n'
                         '    else:\n'
                         '        return "water"',
                 'tip': 'if ... elif ... else: the first true condition wins.'},
                {'brief': 'Print "small", "medium" or "large" for a file of size bytes: under 1000, under '
                          '1000000, else large.',
                 'starter': 'size = 4500\n',
                 'expected': 'medium\n',
                 'hidden': '',
                 'hint': 'if size < 1000:\n'
                         '    print("small")\n'
                         'elif size < 1000000:\n'
                         '    print("medium")\n'
                         'else:\n'
                         '    print("large")',
                 'tip': 'if ... elif ... else: the first true condition wins.'},
                {'brief': 'Write bmi_label(bmi): "under" below 18.5, "normal" below 25, "over" otherwise.',
                 'starter': '# define bmi_label here\n',
                 'expected': 'under\nnormal\nover\n',
                 'hidden': 'print(bmi_label(17))\nprint(bmi_label(22))\nprint(bmi_label(31))\n',
                 'hint': 'def bmi_label(bmi):\n'
                         '    if bmi < 18.5:\n'
                         '        return "under"\n'
                         '    elif bmi < 25:\n'
                         '        return "normal"\n'
                         '    else:\n'
                         '        return "over"',
                 'tip': 'if ... elif ... else: the first true condition wins.'}]},
    {'id': 's2-4',
     'title': 'And, or, not',
     'brief': 'Combining conditions.',
     'lesson': 'and needs both sides true, or needs one side true, not flips a True into a False. Brackets help '
               'when you mix them.  Example: age >= 18 and has_ticket',
     'starter': '',
     'expected': '',
     'hidden': '',
     'hint': '',
     'concepts': ['and', 'or', 'not', 'booleans'],
     'rounds': [{'brief': 'Print whether age is 18 or more AND has_ticket is True.',
                 'starter': 'age = 20\nhas_ticket = False\n',
                 'expected': 'False\n',
                 'hidden': '',
                 'hint': 'print(age >= 18 and has_ticket)',
                 'tip': 'and needs both, or needs one, not flips it.'},
                {'brief': 'Print whether it is raining OR windy.',
                 'starter': 'raining = False\nwindy = True\n',
                 'expected': 'True\n',
                 'hidden': '',
                 'hint': 'print(raining or windy)',
                 'tip': 'and needs both, or needs one, not flips it.'},
                {'brief': 'Print the opposite of open using not.',
                 'starter': 'open = True\n',
                 'expected': 'False\n',
                 'hidden': '',
                 'hint': 'print(not open)',
                 'tip': 'and needs both, or needs one, not flips it.'},
                {'brief': 'Write can_ride(age, height) that is True only when age is at least 12 and height at '
                          'least 140.',
                 'starter': '# define can_ride here\n',
                 'expected': 'True\nFalse\nFalse\n',
                 'hidden': 'print(can_ride(14, 150))\nprint(can_ride(10, 150))\nprint(can_ride(14, 130))\n',
                 'hint': 'def can_ride(age, height):\n    return age >= 12 and height >= 140',
                 'tip': 'and needs both, or needs one, not flips it.'},
                {'brief': 'Write can_enter(age, member) that is True when age is 65 or more OR member is True.',
                 'starter': '# define can_enter here\n',
                 'expected': 'True\nTrue\nFalse\n',
                 'hidden': 'print(can_enter(70, False))\n'
                           'print(can_enter(30, True))\n'
                           'print(can_enter(30, False))\n',
                 'hint': 'def can_enter(age, member):\n    return age >= 65 or member',
                 'tip': 'and needs both, or needs one, not flips it.'},
                {'brief': 'Print whether n is NOT between 1 and 10.',
                 'starter': 'n = 15\n',
                 'expected': 'True\n',
                 'hidden': '',
                 'hint': 'print(not 1 <= n <= 10)',
                 'tip': 'and needs both, or needs one, not flips it.'},
                {'brief': 'Print "ok" if the password is at least 8 characters and is not the word password.',
                 'starter': 'password = "moonlight9"\n',
                 'expected': 'ok\n',
                 'hidden': '',
                 'hint': 'if len(password) >= 8 and password != "password":\n    print("ok")',
                 'tip': 'and needs both, or needs one, not flips it.'},
                {'brief': 'Write is_leap(year): divisible by 4 and not by 100, or divisible by 400.',
                 'starter': '# define is_leap here\n',
                 'expected': 'True\nFalse\nTrue\n',
                 'hidden': 'print(is_leap(2024))\nprint(is_leap(1900))\nprint(is_leap(2000))\n',
                 'hint': 'def is_leap(year):\n    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0',
                 'tip': 'and needs both, or needs one, not flips it.'},
                {'brief': 'Print whether the word is short (under 4 letters) or starts with the letter a.',
                 'starter': 'word = "astro"\n',
                 'expected': 'True\n',
                 'hidden': '',
                 'hint': 'print(len(word) < 4 or word[0] == "a")',
                 'tip': 'and needs both, or needs one, not flips it.'},
                {'brief': 'Write in_range(n, low, high) returning True when n is at least low and at most high.',
                 'starter': '# define in_range here\n',
                 'expected': 'True\nFalse\n',
                 'hidden': 'print(in_range(5, 1, 10))\nprint(in_range(50, 1, 10))\n',
                 'hint': 'def in_range(n, low, high):\n    return n >= low and n <= high',
                 'tip': 'and needs both, or needs one, not flips it.'}]},
    # add your own drills here
]
