WORLD = {'name': 'Dicts', 'title': 'lookups, loops, counting, nested data'}

# A drill is one concept shown ten different ways. Each round is its own
# small task with its own brief, starter, expected output and hint.
DRILLS = [
    {'id': 's5-1',
     'title': 'Lookups and changes',
     'brief': 'Reading, adding, changing and removing entries.',
     'lesson': 'A dict maps keys to values: d = {"name": "Ada"}. Read with d["name"], add or change with '
               'd["key"] = value, remove with del d["key"], and d.get("key", fallback) never errors.  Example: '
               'prices["tea"]',
     'starter': '',
     'expected': '',
     'hidden': '',
     'hint': '',
     'concepts': ['dicts'],
     'rounds': [{'brief': 'Print the capital of France from the dict.',
                 'starter': 'capitals = {"France": "Paris", "Peru": "Lima"}\n',
                 'expected': 'Paris\n',
                 'hidden': '',
                 'hint': 'print(capitals["France"])',
                 'tip': 'd["key"] reads, d["key"] = value writes, del d["key"] removes, d.get("key", fallback) '
                        'is safe.'},
                {'brief': 'Add Spain with Madrid to the dict and print the dict.',
                 'starter': 'capitals = {"France": "Paris"}\n',
                 'expected': "{'France': 'Paris', 'Spain': 'Madrid'}\n",
                 'hidden': '',
                 'hint': 'capitals["Spain"] = "Madrid"\nprint(capitals)',
                 'tip': 'd["key"] reads, d["key"] = value writes, del d["key"] removes, d.get("key", fallback) '
                        'is safe.'},
                {'brief': 'Change the price of tea to 3 and print the dict.',
                 'starter': 'prices = {"tea": 2, "cake": 4}\n',
                 'expected': "{'tea': 3, 'cake': 4}\n",
                 'hidden': '',
                 'hint': 'prices["tea"] = 3\nprint(prices)',
                 'tip': 'd["key"] reads, d["key"] = value writes, del d["key"] removes, d.get("key", fallback) '
                        'is safe.'},
                {'brief': 'Remove cake from the dict and print the dict.',
                 'starter': 'prices = {"tea": 2, "cake": 4}\n',
                 'expected': "{'tea': 2}\n",
                 'hidden': '',
                 'hint': 'del prices["cake"]\nprint(prices)',
                 'tip': 'd["key"] reads, d["key"] = value writes, del d["key"] removes, d.get("key", fallback) '
                        'is safe.'},
                {'brief': 'Print the phone number, or "none" if there is no phone key, using get.',
                 'starter': 'user = {"name": "Ivy"}\n',
                 'expected': 'none\n',
                 'hidden': '',
                 'hint': 'print(user.get("phone", "none"))',
                 'tip': 'd["key"] reads, d["key"] = value writes, del d["key"] removes, d.get("key", fallback) '
                        'is safe.'},
                {'brief': 'Print whether the dict has a key called age.',
                 'starter': 'user = {"name": "Ivy", "age": 30}\n',
                 'expected': 'True\n',
                 'hidden': '',
                 'hint': 'print("age" in user)',
                 'tip': 'd["key"] reads, d["key"] = value writes, del d["key"] removes, d.get("key", fallback) '
                        'is safe.'},
                {'brief': 'Print how many entries the dict has.',
                 'starter': 'stock = {"a": 1, "b": 2, "c": 3}\n',
                 'expected': '3\n',
                 'hidden': '',
                 'hint': 'print(len(stock))',
                 'tip': 'd["key"] reads, d["key"] = value writes, del d["key"] removes, d.get("key", fallback) '
                        'is safe.'},
                {'brief': 'Print the list of keys.',
                 'starter': 'stock = {"apple": 1, "kiwi": 2}\n',
                 'expected': "['apple', 'kiwi']\n",
                 'hidden': '',
                 'hint': 'print(list(stock.keys()))',
                 'tip': 'd["key"] reads, d["key"] = value writes, del d["key"] removes, d.get("key", fallback) '
                        'is safe.'},
                {'brief': 'Print the list of values.',
                 'starter': 'stock = {"apple": 1, "kiwi": 2}\n',
                 'expected': '[1, 2]\n',
                 'hidden': '',
                 'hint': 'print(list(stock.values()))',
                 'tip': 'd["key"] reads, d["key"] = value writes, del d["key"] removes, d.get("key", fallback) '
                        'is safe.'},
                {'brief': 'Increase the apple count by 5 and print the new count.',
                 'starter': 'stock = {"apple": 1, "kiwi": 2}\n',
                 'expected': '6\n',
                 'hidden': '',
                 'hint': 'stock["apple"] = stock["apple"] + 5\nprint(stock["apple"])',
                 'tip': 'd["key"] reads, d["key"] = value writes, del d["key"] removes, d.get("key", fallback) '
                        'is safe.'}]},
    {'id': 's5-2',
     'title': 'Looping over a dict',
     'brief': 'keys, values and items in a loop.',
     'lesson': 'Looping over a dict gives its keys. .values() gives the values, .items() gives key and value '
               'pairs together.  Example: for name, age in ages.items():',
     'starter': '',
     'expected': '',
     'hidden': '',
     'hint': '',
     'concepts': ['dicts', 'for', 'items'],
     'rounds': [{'brief': 'Print each key on its own line.',
                 'starter': 'ages = {"Ada": 36, "Bo": 25}\n',
                 'expected': 'Ada\nBo\n',
                 'hidden': '',
                 'hint': 'for name in ages:\n    print(name)',
                 'tip': 'for key in d, for value in d.values(), for key, value in d.items().'},
                {'brief': 'Print each value on its own line.',
                 'starter': 'ages = {"Ada": 36, "Bo": 25}\n',
                 'expected': '36\n25\n',
                 'hidden': '',
                 'hint': 'for age in ages.values():\n    print(age)',
                 'tip': 'for key in d, for value in d.values(), for key, value in d.items().'},
                {'brief': 'Print each entry as key: value, one per line.',
                 'starter': 'ages = {"Ada": 36, "Bo": 25}\n',
                 'expected': 'Ada: 36\nBo: 25\n',
                 'hidden': '',
                 'hint': 'for name, age in ages.items():\n    print(f"{name}: {age}")',
                 'tip': 'for key in d, for value in d.values(), for key, value in d.items().'},
                {'brief': 'Print the names of everyone older than 30, one per line.',
                 'starter': 'ages = {"Ada": 36, "Bo": 25, "Cy": 41}\n',
                 'expected': 'Ada\nCy\n',
                 'hidden': '',
                 'hint': 'for name, age in ages.items():\n    if age > 30:\n        print(name)',
                 'tip': 'for key in d, for value in d.values(), for key, value in d.items().'},
                {'brief': 'Print the total of all the values.',
                 'starter': 'prices = {"tea": 2, "cake": 4, "jam": 3}\n',
                 'expected': '9\n',
                 'hidden': '',
                 'hint': 'total = 0\nfor price in prices.values():\n    total = total + price\nprint(total)',
                 'tip': 'for key in d, for value in d.values(), for key, value in d.items().'},
                {'brief': 'Print the key with the highest value.',
                 'starter': 'scores = {"Ada": 80, "Bo": 95, "Cy": 70}\n',
                 'expected': 'Bo\n',
                 'hidden': '',
                 'hint': 'best = ""\n'
                         'best_score = -1\n'
                         'for name, score in scores.items():\n'
                         '    if score > best_score:\n'
                         '        best = name\n'
                         '        best_score = score\n'
                         'print(best)',
                 'tip': 'for key in d, for value in d.values(), for key, value in d.items().'},
                {'brief': 'Print the keys in alphabetical order, one per line.',
                 'starter': 'stock = {"pear": 1, "apple": 4, "kiwi": 2}\n',
                 'expected': 'apple\nkiwi\npear\n',
                 'hidden': '',
                 'hint': 'for name in sorted(stock):\n    print(name)',
                 'tip': 'for key in d, for value in d.values(), for key, value in d.items().'},
                {'brief': 'Print each item name in upper case with its count, like APPLE 4.',
                 'starter': 'stock = {"apple": 4, "kiwi": 2}\n',
                 'expected': 'APPLE 4\nKIWI 2\n',
                 'hidden': '',
                 'hint': 'for name, count in stock.items():\n    print(name.upper(), count)',
                 'tip': 'for key in d, for value in d.values(), for key, value in d.items().'},
                {'brief': 'Print how many entries have a value of 0.',
                 'starter': 'stock = {"apple": 0, "kiwi": 2, "fig": 0}\n',
                 'expected': '2\n',
                 'hidden': '',
                 'hint': 'count = 0\n'
                         'for value in stock.values():\n'
                         '    if value == 0:\n'
                         '        count = count + 1\n'
                         'print(count)',
                 'tip': 'for key in d, for value in d.values(), for key, value in d.items().'},
                {'brief': 'Build a new dict with every value doubled and print it.',
                 'starter': 'prices = {"tea": 2, "cake": 4}\n',
                 'expected': "{'tea': 4, 'cake': 8}\n",
                 'hidden': '',
                 'hint': 'doubled = {}\n'
                         'for name, price in prices.items():\n'
                         '    doubled[name] = price * 2\n'
                         'print(doubled)',
                 'tip': 'for key in d, for value in d.values(), for key, value in d.items().'}]},
    {'id': 's5-3',
     'title': 'Counting with a dict',
     'brief': 'The counts[key] = counts.get(key, 0) + 1 pattern.',
     'lesson': 'To count things, use a dict: counts[key] = counts.get(key, 0) + 1 adds one to a key, starting '
               'from 0 when the key is new.  Example: for word in words:  counts[word] = counts.get(word, 0) + 1',
     'starter': '',
     'expected': '',
     'hidden': '',
     'hint': '',
     'concepts': ['dicts', 'get', 'counting'],
     'rounds': [{'brief': 'Write count_words(text) that returns a dict from each word to how often it appears.',
                 'starter': '# define count_words here\n',
                 'expected': "{'a': 3, 'b': 1, 'c': 1}\n",
                 'hidden': 'print(count_words("a b a c a"))\n',
                 'hint': 'def count_words(text):\n'
                         '    counts = {}\n'
                         '    for word in text.split():\n'
                         '        counts[word] = counts.get(word, 0) + 1\n'
                         '    return counts',
                 'tip': 'counts[key] = counts.get(key, 0) + 1'},
                {'brief': 'Write count_letters(word) that returns a dict from each letter to its count.',
                 'starter': '# define count_letters here\n',
                 'expected': "{'h': 1, 'e': 1, 'l': 2, 'o': 1}\n",
                 'hidden': 'print(count_letters("hello"))\n',
                 'hint': 'def count_letters(word):\n'
                         '    counts = {}\n'
                         '    for letter in word:\n'
                         '        counts[letter] = counts.get(letter, 0) + 1\n'
                         '    return counts',
                 'tip': 'counts[key] = counts.get(key, 0) + 1'},
                {'brief': 'Write totals(orders) that sums the quantities per fruit from (fruit, quantity) pairs.',
                 'starter': '# define totals here\n',
                 'expected': "{'apple': 5, 'pear': 1}\n",
                 'hidden': 'print(totals([("apple", 2), ("pear", 1), ("apple", 3)]))\n',
                 'hint': 'def totals(orders):\n'
                         '    result = {}\n'
                         '    for fruit, quantity in orders:\n'
                         '        result[fruit] = result.get(fruit, 0) + quantity\n'
                         '    return result',
                 'tip': 'counts[key] = counts.get(key, 0) + 1'},
                {'brief': 'Count the numbers in the list and print the dict.',
                 'starter': 'numbers = [1, 2, 1, 3, 1]\n',
                 'expected': '{1: 3, 2: 1, 3: 1}\n',
                 'hidden': '',
                 'hint': 'counts = {}\nfor n in numbers:\n    counts[n] = counts.get(n, 0) + 1\nprint(counts)',
                 'tip': 'counts[key] = counts.get(key, 0) + 1'},
                {'brief': 'Write most_common(words) that returns the word that appears most often.',
                 'starter': '# define most_common here\n',
                 'expected': 'x\n',
                 'hidden': 'print(most_common(["x", "y", "x", "z", "x"]))\n',
                 'hint': 'def most_common(words):\n'
                         '    counts = {}\n'
                         '    for word in words:\n'
                         '        counts[word] = counts.get(word, 0) + 1\n'
                         '    return max(counts, key=counts.get)',
                 'tip': 'counts[key] = counts.get(key, 0) + 1'},
                {'brief': 'Write vowel_counts(text) that returns a dict counting only the vowels a, e, i, o, u.',
                 'starter': '# define vowel_counts here\n',
                 'expected': "{'a': 4, 'o': 1}\n",
                 'hidden': 'print(vowel_counts("banana boat"))\n',
                 'hint': 'def vowel_counts(text):\n'
                         '    counts = {}\n'
                         '    for letter in text:\n'
                         '        if letter in "aeiou":\n'
                         '            counts[letter] = counts.get(letter, 0) + 1\n'
                         '    return counts',
                 'tip': 'counts[key] = counts.get(key, 0) + 1'},
                {'brief': 'Write group_by_length(words) that returns a dict from length to the list of words '
                          'with that length.',
                 'starter': '# define group_by_length here\n',
                 'expected': "{1: ['a', 'd'], 2: ['bb', 'cc']}\n",
                 'hidden': 'print(group_by_length(["a", "bb", "cc", "d"]))\n',
                 'hint': 'def group_by_length(words):\n'
                         '    groups = {}\n'
                         '    for word in words:\n'
                         '        groups.setdefault(len(word), []).append(word)\n'
                         '    return groups',
                 'tip': 'counts[key] = counts.get(key, 0) + 1'},
                {'brief': 'Count how many times each first letter appears in the names and print the dict.',
                 'starter': 'names = ["Ada", "Amy", "Bo"]\n',
                 'expected': "{'A': 2, 'B': 1}\n",
                 'hidden': '',
                 'hint': 'counts = {}\n'
                         'for name in names:\n'
                         '    counts[name[0]] = counts.get(name[0], 0) + 1\n'
                         'print(counts)',
                 'tip': 'counts[key] = counts.get(key, 0) + 1'},
                {'brief': 'Write score_totals(rounds) summing points per player from (player, points) pairs.',
                 'starter': '# define score_totals here\n',
                 'expected': "{'kim': 7, 'bo': 5}\n",
                 'hidden': 'print(score_totals([("kim", 3), ("bo", 5), ("kim", 4)]))\n',
                 'hint': 'def score_totals(rounds):\n'
                         '    totals = {}\n'
                         '    for player, points in rounds:\n'
                         '        totals[player] = totals.get(player, 0) + points\n'
                         '    return totals',
                 'tip': 'counts[key] = counts.get(key, 0) + 1'},
                {'brief': 'Write unique_count(items) that returns how many different items there are, using a '
                          'dict or a set.',
                 'starter': '# define unique_count here\n',
                 'expected': '3\n',
                 'hidden': 'print(unique_count([1, 1, 2, 3, 3, 3]))\n',
                 'hint': 'def unique_count(items):\n    return len(set(items))',
                 'tip': 'counts[key] = counts.get(key, 0) + 1'}]},
    {'id': 's5-4',
     'title': 'Nested data and sets',
     'brief': 'Dicts inside lists inside dicts, and sets.',
     'lesson': 'Data nests: a dict can hold lists that hold dicts. Read one level at a time with brackets. A set '
               'keeps unique values; set(list) removes duplicates and & - | combine sets.  Example: '
               'data["users"][0]["name"]',
     'starter': '',
     'expected': '',
     'hidden': '',
     'hint': '',
     'concepts': ['nested', 'sets'],
     'rounds': [{'brief': 'Print the second tag of the first user.',
                 'starter': 'data = {"users": [{"name": "A", "tags": ["x", "y"]}]}\n',
                 'expected': 'y\n',
                 'hidden': '',
                 'hint': 'print(data["users"][0]["tags"][1])',
                 'tip': 'read nested data one bracket at a time; set(list) removes duplicates.'},
                {'brief': "Print each user's name, one per line.",
                 'starter': 'data = {"users": [{"name": "A"}, {"name": "B"}]}\n',
                 'expected': 'A\nB\n',
                 'hidden': '',
                 'hint': 'for user in data["users"]:\n    print(user["name"])',
                 'tip': 'read nested data one bracket at a time; set(list) removes duplicates.'},
                {'brief': "Print each user's name and how many tags they have, like A 2.",
                 'starter': 'data = {"users": [{"name": "A", "tags": ["x", "y"]}, {"name": "B", "tags": []}]}\n',
                 'expected': 'A 2\nB 0\n',
                 'hidden': '',
                 'hint': 'for user in data["users"]:\n    print(user["name"], len(user["tags"]))',
                 'tip': 'read nested data one bracket at a time; set(list) removes duplicates.'},
                {'brief': 'Print the total of all the scores in the nested list.',
                 'starter': 'players = [{"name": "A", "score": 5}, {"name": "B", "score": 9}]\n',
                 'expected': '14\n',
                 'hidden': '',
                 'hint': 'total = 0\nfor player in players:\n    total = total + player["score"]\nprint(total)',
                 'tip': 'read nested data one bracket at a time; set(list) removes duplicates.'},
                {'brief': 'Print the set of the list, to remove duplicates (sorted so the order is fixed).',
                 'starter': 'numbers = [3, 1, 3, 2, 1]\n',
                 'expected': '[1, 2, 3]\n',
                 'hidden': '',
                 'hint': 'print(sorted(set(numbers)))',
                 'tip': 'read nested data one bracket at a time; set(list) removes duplicates.'},
                {'brief': 'Print the items that are in both sets, sorted.',
                 'starter': 'a = {1, 2, 3, 4}\nb = {3, 4, 5}\n',
                 'expected': '[3, 4]\n',
                 'hidden': '',
                 'hint': 'print(sorted(a & b))',
                 'tip': 'read nested data one bracket at a time; set(list) removes duplicates.'},
                {'brief': 'Print the items that are in a but not in b, sorted.',
                 'starter': 'a = {1, 2, 3, 4}\nb = {3, 4, 5}\n',
                 'expected': '[1, 2]\n',
                 'hidden': '',
                 'hint': 'print(sorted(a - b))',
                 'tip': 'read nested data one bracket at a time; set(list) removes duplicates.'},
                {'brief': 'Add the word moon to the set and print whether moon is in it.',
                 'starter': 'words = {"sun", "star"}\n',
                 'expected': 'True\n',
                 'hidden': '',
                 'hint': 'words.add("moon")\nprint("moon" in words)',
                 'tip': 'read nested data one bracket at a time; set(list) removes duplicates.'},
                {'brief': 'Print the name of the player with the highest score.',
                 'starter': 'players = [{"name": "A", "score": 5}, {"name": "B", "score": 9}]\n',
                 'expected': 'B\n',
                 'hidden': '',
                 'hint': 'best = players[0]\n'
                         'for player in players:\n'
                         '    if player["score"] > best["score"]:\n'
                         '        best = player\n'
                         'print(best["name"])',
                 'tip': 'read nested data one bracket at a time; set(list) removes duplicates.'},
                {'brief': 'Write all_tags(users) that returns the sorted list of every different tag across all '
                          'users.',
                 'starter': '# define all_tags here\n',
                 'expected': "['x', 'y', 'z']\n",
                 'hidden': 'print(all_tags([{"tags": ["x", "y"]}, {"tags": ["y", "z"]}]))\n',
                 'hint': 'def all_tags(users):\n'
                         '    tags = set()\n'
                         '    for user in users:\n'
                         '        for tag in user["tags"]:\n'
                         '            tags.add(tag)\n'
                         '    return sorted(tags)',
                 'tip': 'read nested data one bracket at a time; set(list) removes duplicates.'}]},
    # add your own drills here
]
