# PyLevels theory

Each card teaches one small idea. Read one card, then go and try the level. Stuck? Come back and read the card again. That is normal, and it is how everyone learns.

## World 1: Basics
- [ ] done

This world is about showing things on the screen, keeping values, and doing sums.

### Printing with print
Big idea: `print()` shows something on the screen.

Put what you want to show inside the brackets. Text goes inside quotes. Numbers need no quotes.

```python
print("hello")
print(42)
```
```output
hello
42
```
Note: `print(hello)` without quotes is an error, because Python looks for a variable called hello.

### Printing several things
Big idea: commas let one `print()` show several things on one line.

Python puts a space between them. Add `sep="-"` to put something else between them. An empty `print()` prints an empty line.

```python
print("sun", "moon")
print("a", "b", "c", sep="-")
print()
print("done")
```
```output
sun moon
a-b-c

done
```

### Comments with #
Big idea: anything after `#` is a note for people, and Python skips it.

Use comments to explain your code to yourself. Python does not run them.

```python
# this line does nothing
print("hi")  # this note is skipped too
```
```output
hi
```

### Variables: name tags
Big idea: a variable is a name tag you stick on a value.

Write the name, then `=`, then the value. After that, you can use the name instead of the value. The name has no quotes.

```python
city = "Antwerp"
year = 2026
print(city)
print(year)
```
```output
Antwerp
2026
```
Note: `=` means "stick this name on this value". It does not mean "is equal to".

### Changing a variable
Big idea: you can move a name tag to a new value.

Python works out the right side first. Then it sticks the name on the answer. `count += 5` is a short way to write `count = count + 5`.

```python
count = 10
count = count + 1
print(count)
count += 5
print(count)
```
```output
11
16
```

### Types: text, numbers, True/False
Big idea: every value has a type, which means what kind of value it is.

- `str`: text in quotes, like `"hi"`
- `int`: a whole number, like `7`
- `float`: a number with a dot, like `2.5`
- `bool`: `True` or `False`

`type()` tells you the type of a value.

```python
print(type("hi"))
print(type(7))
print(type(2.5))
```
```output
<class 'str'>
<class 'int'>
<class 'float'>
```

### Converting: int, float, str
Big idea: `int()`, `float()` and `str()` turn a value into another type.

`"42"` looks like a number, but it is text. `int("42")` makes it a real number. `str(7)` turns a number into text. `int(3.9)` just cuts off the decimals.

```python
print(int("42") + 1)
print(float("1.5"))
print(str(7) + " items")
print(int(3.9))
```
```output
43
1.5
7 items
3
```
Note: `"5" + 1` is an error. Python will not add text and a number.

### Arithmetic: + - * /
Big idea: Python can do sums, like a calculator.

`+` adds, `-` takes away, `*` multiplies and `/` divides. `/` always gives a number with a dot.

```python
width = 7
height = 3
print(width * height)
print(7 / 2)
print(8 / 2)
```
```output
21
3.5
4.0
```

### Floor division //
Big idea: `//` tells you how many whole times one number fits in another.

It divides, then throws away the leftover part. You have 17 apples and boxes of 5. You can fill 3 whole boxes.

```python
print(17 // 5)
seconds = 500
print(seconds // 60)
```
```output
3
8
```

### Remainder %
Big idea: `%` (modulo) gives what is left over after dividing.

17 apples in boxes of 5: three full boxes, and 2 apples left over. So `17 % 5` is 2.

```python
print(17 % 5)
seconds = 500
print(seconds % 60)
print(10 % 2)
```
```output
2
20
0
```
Note: a number is even when `n % 2` is 0, because nothing is left over.

### Power ** and square root
Big idea: `**` means "to the power of".

`2 ** 3` means 2 times 2 times 2. Power `0.5` gives the square root.

```python
print(2 ** 3)
print(2 ** 10)
print(16 ** 0.5)
```
```output
8
1024
4.0
```

### round, abs, min, max
Big idea: these ready-made helpers tidy up numbers.

- `round(x, 2)` keeps 2 decimals. `round(x)` gives a whole number.
- `abs(x)` removes a minus sign.
- `min` and `max` pick the smallest and the biggest.

```python
print(round(3.14159, 2))
print(round(2.7))
print(abs(-5))
print(min(3, 1, 2))
print(max(3, 1, 2))
```
```output
3.14
3
5
1
3
```

### Functions: a first look
Big idea: a function is a small recipe with a name, and `return` gives back its answer.

`def` starts the recipe. `x` is the input. `return` hands the answer back. The lines pushed in by 4 spaces belong to the function. World 6 explains all of this slowly.

```python
def double(x):
    return x * 2

print(double(4))
print(double(2.5))
```
```output
8
5.0
```
Note: when a level says "do not print inside it", use `return`, not `print`.

### Default values: a first look
Big idea: an input can have a backup value, used when you leave it out.

In `mark="?"`, the `"?"` is the backup. If you give a second value, that one is used instead.

```python
def ask(word, mark="?"):
    return word + mark

print(ask("why"))
print(ask("why", "!!"))
```
```output
why?
why!!
```

### Drill
Print your city and the year on two lines. Then print how many whole minutes fit in 500 seconds, and how many seconds are left over. Last, write `triple(x)` that returns x times three.

## World 2: Flow
- [ ] done

This world is about yes or no questions, and letting your program choose what to do.

### True and False (booleans)
Big idea: a boolean is a value that is either `True` or `False`.

Booleans are the answers to yes or no questions. Write them with a capital letter and no quotes.

```python
logged_in = True
print(logged_in)
print(3 < 5)
```
```output
True
True
```

### Comparisons: == != < >
Big idea: a comparison asks a yes or no question and answers `True` or `False`.

- `==` equal? and `!=` not equal?
- `<` smaller? and `>` bigger?
- `<=` smaller or equal? and `>=` bigger or equal?

Text is compared like in a dictionary: "apple" comes before "pear".

```python
age = 18
print(age == 18)
print(age != 18)
print(age >= 21)
print("apple" < "pear")
```
```output
True
False
False
True
```
Note: one `=` stores a value. Two `==` compare two values.

### Chained comparisons
Big idea: `1 <= n <= 10` asks "is n between 1 and 10?" in one go.

It reads like maths. Both parts must be true.

```python
n = 7
print(1 <= n <= 10)
n = 50
print(1 <= n <= 10)
```
```output
True
False
```

### Keeping a True/False answer
Big idea: a comparison gives a value, so you can store it or return it.

This is handy in functions. The function below gives back True or False straight away, with no `if` needed.

```python
def is_even(n):
    return n % 2 == 0

print(is_even(10))
print(is_even(7))
```
```output
True
False
```

### and: both must be true
Big idea: `and` gives True only when both sides are True.

You need a ticket and you must be 18. Missing one of them is enough to say no.

```python
age = 20
has_ticket = False
print(age >= 18 and has_ticket)
print(age >= 18 and age < 30)
```
```output
False
True
```

### or: one is enough
Big idea: `or` gives True when at least one side is True.

```python
day = "sun"
print(day == "sat" or day == "sun")
age = 40
member = False
print(age >= 65 or member)
```
```output
True
False
```
Note: write the full question on both sides. `day == "sat" or "sun"` does not do what you expect.

### not: flip it
Big idea: `not` turns True into False, and False into True.

```python
is_open = False
print(not is_open)
print(not 3 < 5)
```
```output
True
False
```

### if: only when true
Big idea: `if` runs some lines only when a question is True.

The `if` line ends with a colon `:`. The lines under it are pushed in by 4 spaces. That push is called indenting. Those lines run only when the answer is True.

```python
temp = 25
if temp >= 20:
    print("warm")
print("bye")
```
```output
warm
bye
```
Note: forgetting the colon `:` at the end of the `if` line is a very common error.

### else: otherwise
Big idea: `else` runs when the `if` question was False.

It is the "otherwise" part. Exactly one of the two blocks runs, never both.

```python
temp = 12
if temp >= 20:
    print("warm")
else:
    print("cold")
```
```output
cold
```

### elif: more choices
Big idea: `elif` means "else if": ask another question when the one above was False.

Python checks from top to bottom. It runs only the first block that is True, then skips the rest.

```python
n = 0
if n < 0:
    print("negative")
elif n == 0:
    print("zero")
else:
    print("positive")
```
```output
zero
```

### Order matters in elif
Big idea: Python stops at the first True question, so put the smallest limit first.

Let's check `cm = 175` step by step. Is 175 below 170? No. Is 175 below 180? Yes. So it prints M and stops.

```python
cm = 175
if cm < 170:
    print("S")
elif cm < 180:
    print("M")
else:
    print("L")
```
```output
M
```

### if with return in a function
Big idea: in a function, each choice can `return` its own answer.

`return` gives the answer back and ends the function at once. So the lines below it do not run.

```python
def state(temp):
    if temp <= 0:
        return "ice"
    return "water"

print(state(-5))
print(state(40))
```
```output
ice
water
```

### One-line if
Big idea: `a if question else b` picks one of two values in one line.

```python
score = 62
label = "pass" if score >= 50 else "fail"
print(label)
```
```output
pass
```

### Empty means False
Big idea: in an `if`, empty things and zero count as False.

`0`, `""` (empty text), `[]` (empty list) and `None` all count as False. So `if items:` means "if the list is not empty".

```python
items = []
if items:
    print("has items")
else:
    print("empty")
```
```output
empty
```

### Drill
Write `size(cm)` that returns "S" below 170, "M" below 180, and "L" for the rest. Then set `label` to "pass" or "fail" in one line.

## World 3: Strings
- [ ] done

This world is about text. Go slowly on index and slicing: they are the tricky part.

### What is a string
Big idea: a string is a piece of text inside quotes.

A string is characters in a row, like beads on a string. A character is one letter, digit, space or sign.

```python
word = "Python"
greeting = 'hi there'
print(word)
print(greeting)
```
```output
Python
hi there
```
Note: single quotes and double quotes both work.

### len: counting characters
Big idea: `len()` tells you how many characters a string has.

Spaces count too. So "hi there" has 8 characters.

```python
print(len("Python"))
print(len("hi there"))
```
```output
6
8
```

### What is an index
Big idea: each character has a position number, called its index, and counting starts at 0.

Think of numbered lockers. The first locker is number 0, not 1. Put the index in square brackets to get that one character.

```text
word:   P  y  t  h  o  n
index:  0  1  2  3  4  5
```
```python
word = "Python"
print(word[0])
print(word[1])
print(word[5])
```
```output
P
y
n
```

### The last index is len - 1
Big idea: the last character sits at index `len(word) - 1`, because counting starts at 0.

"Python" has 6 characters, so its indexes go from 0 to 5. There is no index 6.

```python
word = "Python"
print(len(word))
print(word[len(word) - 1])
print(word[6])
```
```output
6
n
IndexError: string index out of range
```

### Negative index
Big idea: negative numbers count from the end, so `-1` is always the last character.

You do not need to know how long the word is.

```text
word:       P   y   t   h   o   n
index:      0   1   2   3   4   5
from end:  -6  -5  -4  -3  -2  -1
```
```python
word = "Python"
print(word[-1])
print(word[-2])
```
```output
n
o
```

### Slicing: taking a piece
Big idea: `word[start:stop]` takes a piece of the string.

It starts at index `start`. It stops just before index `stop`. The character at `stop` is not included.

```python
word = "Python"
print(word[0:2])
print(word[2:5])
```
```output
Py
tho
```

### Slicing step by step
Big idea: a slice takes start, then the next one, and so on, and stops before stop.

Let's do `word[2:5]` slowly:

- index 2 is t: take it
- index 3 is h: take it
- index 4 is o: take it
- index 5: stop here, do not take it

```text
word:   P  y  t  h  o  n
index:  0  1  2  3  4  5
            [ t  h  o ]
```
So you get "tho". That is 5 - 2 = 3 characters.

Note: stop minus start tells you how many characters you get.

### Slicing shortcuts
Big idea: leave out start to begin at the start, and leave out stop to go to the end.

- `word[:3]` the first 3 characters
- `word[3:]` from index 3 to the end
- `word[-2:]` the last 2 characters

```python
word = "Python"
print(word[:3])
print(word[3:])
print(word[-2:])
```
```output
Pyt
hon
on
```

### Slicing with a step
Big idea: a third number in a slice is the step: how far to jump each time.

`word[::2]` takes every second character. `word[::-1]` walks backwards, so it gives the word reversed.

```python
word = "Python"
print(word[::2])
print(word[::-1])
```
```output
Pto
nohtyP
```

### lower and upper
Big idea: `.lower()` and `.upper()` give the text in small or capital letters.

A method is a tool that belongs to a value. You use it with a dot. The old text stays the same. You get a new string back.

```python
word = "Hello"
print(word.lower())
print(word.upper())
print(word)
```
```output
hello
HELLO
Hello
```
Note: `word.upper()` alone on a line changes nothing. Print it, or store it with `word = word.upper()`.

### strip: remove outside spaces
Big idea: `.strip()` removes the spaces at the start and the end.

You can use methods one after another. Python does them left to right.

```python
email = "  Ada@Mail.com  "
print(email.strip())
print(email.strip().lower())
```
```output
Ada@Mail.com
ada@mail.com
```

### More string methods
Big idea: strings have many handy methods, used with a dot.

- `replace(old, new)` swaps one piece of text for another
- `find(piece)` gives the index where it starts, or -1
- `count(piece)` counts how often it appears
- `endswith(piece)` and `startswith(piece)` check the end or the start

```python
text = "the sun and the moon"
print(text.replace("sun", "star"))
print(text.find("sun"))
print(text.count("the"))
print("main.py".endswith(".py"))
```
```output
the star and the moon
4
2
True
```

### in: is it inside?
Big idea: `in` asks "is this piece inside the text?" and answers True or False.

```python
print("moon" in "the moon is up")
print("a" in "aeiou")
print("x" in "aeiou")
```
```output
True
True
False
```

### Looping over letters
Big idea: a `for` loop over a string visits one character at a time.

World 4 explains loops. Here we count the vowels in "banana".

```python
count = 0
for letter in "banana":
    if letter in "aeiou":
        count += 1
print(count)
```
```output
3
```

### split: cut into pieces
Big idea: `.split()` cuts text into a list of pieces.

With empty brackets, it cuts at the spaces. Put a sign in the brackets, like `"@"`, to cut there instead.

```python
print("a big red car".split())
email = "ada@mail.com"
print(email.split("@"))
print(email.split("@")[0])
```
```output
['a', 'big', 'red', 'car']
['ada', 'mail.com']
ada
```

### Two pieces into two names
Big idea: `a, b = ...` puts two pieces into two names at once.

This is called unpacking. The number of names must match the number of pieces.

```python
user, domain = "ada@mail.com".split("@")
print(user)
print(domain)
```
```output
ada
mail.com
```
Note: a function can give back both with `return user, domain`. That pair is called a tuple (see World 6).

### join: glue pieces together
Big idea: `"-".join(pieces)` glues the pieces together, with `-` between them.

It is the opposite of split. The text before the dot is the glue.

```python
print(", ".join(["tea", "jam", "milk"]))
print("-".join("moon"))
```
```output
tea, jam, milk
m-o-o-n
```

### f-strings: values inside text
Big idea: put `f` before the quotes, and each `{}` drops a value into the text.

```python
name = "Ada"
age = 36
print(f"{name} is {age} years old")
print(f"{name[0]}.")
print(f"3 + 4 = {3 + 4}")
```
```output
Ada is 36 years old
A.
3 + 4 = 7
```
Note: if you forget the `f`, Python prints the curly brackets as they are.

### f-strings: formatting numbers
Big idea: after a colon inside `{}`, you choose how a number looks.

- `:.2f` two decimals
- `:,` a comma every three digits
- `:.0%` a percentage
- `:03` zeros in front, 3 digits wide

```python
print(f"{4.5:.2f}")
print(f"{9876543:,}")
print(f"{1234.5:,.2f}")
print(f"{0.75:.0%}")
print(f"{7:03}")
```
```output
4.50
9,876,543
1,234.50
75%
007
```

### Drill
From `email = "  Ada.Smith@Mail.com "` print the clean lowercase email, then the part before the @, then the part after it. Before you run `"planet"[1:4]`, say the answer out loud.

## World 4: Lists and loops
- [ ] done

This world is about keeping many values in one list, and doing something for each of them.

### What is a list
Big idea: a list keeps many values in order, inside one variable.

Write it with square brackets `[ ]` and commas between the items. An item is one value in the list.

```python
colours = ["red", "green", "blue"]
print(colours)
print(len(colours))
```
```output
['red', 'green', 'blue']
3
```

### List index
Big idea: a list is a row of numbered lockers, and the first locker is number 0.

It works just like the index of a string.

```text
planets:  "Mercury"  "Venus"  "Earth"  "Mars"
index:        0         1        2        3
from end:    -4        -3       -2       -1
```
```python
planets = ["Mercury", "Venus", "Earth", "Mars"]
print(planets[0])
print(planets[2])
print(planets[-1])
```
```output
Mercury
Earth
Mars
```
Note: the third item is index 2, because counting starts at 0.

### List slicing
Big idea: a slice of a list gives a smaller list.

It works like slicing a string. Start at `start`, stop just before `stop`.

```python
planets = ["Mercury", "Venus", "Earth", "Mars"]
print(planets[0:2])
print(planets[2:])
print(planets[-2:])
```
```output
['Mercury', 'Venus']
['Earth', 'Mars']
['Earth', 'Mars']
```
Note: one index gives one item. A slice, with a colon, always gives a list.

### Changing an item
Big idea: `planets[1] = "Neptune"` puts a new value in locker 1.

Lists can change. Strings cannot.

```python
planets = ["Mercury", "Venus", "Earth"]
planets[1] = "Neptune"
print(planets)
```
```output
['Mercury', 'Neptune', 'Earth']
```

### Lists inside lists
Big idea: in `rows[1][0]`, first pick the row, then pick the item in that row.

Read the brackets from left to right, one step at a time.

```python
rows = [[1, 2], [3, 4]]
print(rows[1])
print(rows[1][0])
words = ["moon", "sun"]
print(words[0][-1])
```
```output
[3, 4]
3
n
```

### append: add to the end
Big idea: `.append(x)` adds one item to the end of a list.

You often start with an empty list `[]` and let it grow.

```python
basket = []
basket.append("tea")
basket.append("jam")
print(basket)
```
```output
['tea', 'jam']
```

### pop and remove
Big idea: `.pop()` takes the last item out, and `.remove(x)` takes out the first x.

`pop` also gives you the item it took out.

```python
nums = [3, 1, 4, 1]
last = nums.pop()
print(last)
nums.remove(3)
print(nums)
```
```output
1
[1, 4]
```

### sort and sorted
Big idea: `sorted(list)` gives a new sorted list, and `.sort()` sorts the list itself.

Add `reverse=True` to sort from high to low.

```python
scores = [72, 95, 48]
print(sorted(scores))
scores.sort(reverse=True)
print(scores)
```
```output
[48, 72, 95]
[95, 72, 48]
```
Note: `x = scores.sort()` makes x `None`, because `.sort()` gives nothing back.

### len, sum and in
Big idea: `len` counts the items, `sum` adds them up, and `in` checks if an item is there.

```python
nums = [4, 9, 2]
print(len(nums))
print(sum(nums))
print(9 in nums)
```
```output
3
15
True
```

### for loops: do this for each
Big idea: a `for` loop means "do this for each item in the list".

The name after `for` holds one item each round. The pushed-in lines run once per item.

```python
colours = ["red", "green", "blue"]
for colour in colours:
    print(colour)
```
```output
red
green
blue
```
Round 1: colour is "red". Round 2: "green". Round 3: "blue". Then the loop ends.

### Looping backwards
Big idea: `reversed(list)` lets a `for` loop go from the last item to the first.

```python
for colour in reversed(["red", "green", "blue"]):
    print(colour)
```
```output
blue
green
red
```

### range: counting numbers
Big idea: `range(3)` counts 0, 1, 2: three numbers, starting at 0.

Like a slice, the stop number is not included.

```python
for i in range(3):
    print(i)
```
```output
0
1
2
```

### range with start, stop, step
Big idea: `range(start, stop, step)` counts from start, jumps by step, and stops before stop.

Here `list()` just shows all the numbers at once.

```python
print(list(range(1, 6)))
print(list(range(2, 11, 2)))
print(list(range(5, 0, -1)))
```
```output
[1, 2, 3, 4, 5]
[2, 4, 6, 8, 10]
[5, 4, 3, 2, 1]
```

### enumerate: number and item
Big idea: `enumerate` gives you the position and the item together.

Add `start=1` to count from 1 instead of 0.

```python
for i, food in enumerate(["tea", "jam"], start=1):
    print(f"{i}. {food}")
```
```output
1. tea
2. jam
```

### zip: two lists side by side
Big idea: `zip` walks through two lists at the same time, one pair per round.

```python
names = ["Ann", "Bo"]
ages = [30, 25]
for name, age in zip(names, ages):
    print(name, age)
```
```output
Ann 30
Bo 25
```

### A running total
Big idea: to add things up, start at 0 before the loop, and add inside the loop.

```python
total = 0
for n in [4, 9, 2]:
    total = total + n
print(total)
```
```output
15
```
Note: put `total = 0` before the loop. Inside the loop it would go back to 0 every round.

### The best so far
Big idea: to find the biggest, keep the best so far and swap it when you see a bigger one.

Start with the first item as the best.

```python
numbers = [4, 9, 2]
best = numbers[0]
for n in numbers:
    if n > best:
        best = n
print(best)
```
```output
9
```

### Building a new list
Big idea: start with an empty list, and `append` the items you want inside the loop.

```python
doubled = []
for n in [4, 9, 2]:
    doubled.append(n * 2)
print(doubled)
```
```output
[8, 18, 4]
```

### None: nothing found
Big idea: `None` means "no value", and a function can return it when it found nothing.

`return` inside a loop stops the function at once.

```python
def first_even(numbers):
    for n in numbers:
        if n % 2 == 0:
            return n
    return None

print(first_even([3, 8, 5]))
print(first_even([1, 3]))
```
```output
8
None
```

### while loops
Big idea: `while` repeats as long as its question is True.

```python
n = 3
while n > 0:
    print(n)
    n = n - 1
print("go")
```
```output
3
2
1
go
```
Note: something inside must change, or the loop never stops.

### break and continue
Big idea: `break` leaves the loop now, and `continue` skips to the next round.

```python
for n in range(1, 10):
    if n == 3:
        continue
    if n == 5:
        break
    print(n)
```
```output
1
2
4
```

### Drill
Given `scores = [72, 95, 48, 88]`, print each score with its number starting at 1. Then build a list of the scores of 50 or more, and print it from high to low.

## World 5: Dicts and sets
- [ ] done

This world is about finding values by a name instead of by a position.

### What is a dict
Big idea: a dict links keys to values, like a phone book links names to numbers.

Dict is short for dictionary. Write it with curly brackets `{ }`. Each pair is `key: value`, with commas between the pairs.

```python
capitals = {"France": "Paris", "Spain": "Madrid"}
print(capitals)
print(len(capitals))
```
```output
{'France': 'Paris', 'Spain': 'Madrid'}
2
```

### Looking up a value
Big idea: `d[key]` gives the value for that key.

You look things up by name, not by position. If the key is not there, you get an error.

```python
capitals = {"France": "Paris", "Spain": "Madrid"}
print(capitals["Spain"])
print(capitals["Italy"])
```
```output
Madrid
KeyError: 'Italy'
```

### Adding and changing
Big idea: `d[key] = value` adds a new pair, or changes the value if the key is already there.

Each key can appear only once.

```python
stock = {"apple": 4}
stock["pear"] = 2
stock["apple"] = stock["apple"] + 5
print(stock)
```
```output
{'apple': 9, 'pear': 2}
```

### Removing with del
Big idea: `del d[key]` removes that key and its value.

```python
user = {"name": "Ada", "age": 36}
del user["age"]
print(user)
```
```output
{'name': 'Ada'}
```

### get: a safe lookup
Big idea: `d.get(key, backup)` gives the value, or the backup when the key is missing.

It never crashes. With no backup, it gives `None`.

```python
user = {"name": "Ada"}
print(user.get("name"))
print(user.get("phone"))
print(user.get("phone", "n/a"))
```
```output
Ada
None
n/a
```

### in, keys and values
Big idea: `in` checks the keys, `.keys()` gives all keys, and `.values()` gives all values.

```python
stock = {"apple": 4, "pear": 0}
print("apple" in stock)
print(list(stock.keys()))
print(list(stock.values()))
```
```output
True
['apple', 'pear']
[4, 0]
```

### Looping over a dict
Big idea: a `for` loop over a dict gives you the keys, one by one.

```python
ages = {"Ann": 30, "Bo": 25}
for name in ages:
    print(name, ages[name])
```
```output
Ann 30
Bo 25
```

### items: key and value together
Big idea: `.items()` gives each key and its value together, in one loop.

```python
stock = {"apple": 4, "pear": 0, "kiwi": 7}
for fruit, count in stock.items():
    if count > 0:
        print(fruit, count)
```
```output
apple 4
kiwi 7
```

### Counting with a dict
Big idea: to count, look up the count so far (0 if new), add one, and store it back.

```python
counts = {}
for word in ["a", "b", "a"]:
    counts[word] = counts.get(word, 0) + 1
print(counts)
```
```output
{'a': 2, 'b': 1}
```
Step by step: "a" is new, so 0 + 1 = 1. "b" is new, so 1. "a" again: 1 + 1 = 2.

### Tuples: fixed pairs
Big idea: a tuple is a small fixed group of values in round brackets, like `("apple", 2)`.

A loop can unpack each pair into two names.

```python
orders = [("apple", 2), ("pear", 1)]
for fruit, quantity in orders:
    print(fruit, quantity)
```
```output
apple 2
pear 1
```

### Totals per key
Big idea: to add up amounts per key, add the amount instead of 1.

```python
totals = {}
for name, points in [("Ann", 3), ("Bo", 1), ("Ann", 2)]:
    totals[name] = totals.get(name, 0) + points
print(totals)
```
```output
{'Ann': 5, 'Bo': 1}
```

### Nested data
Big idea: data can be dicts inside lists inside dicts, so go in one step at a time.

Read from left to right: the key, then the index, then the key.

```python
data = {"users": [{"name": "A", "tags": ["x", "y"]}]}
print(data["users"][0]["name"])
print(data["users"][0]["tags"][1])
```
```output
A
y
```

### Sets: no repeats
Big idea: a set is a bag of values where each value appears only once.

`set(list)` removes the repeats. A set has no order, so use `sorted` to print it in order.

```python
words = ["b", "a", "b", "c", "a"]
print(sorted(set(words)))
s = {1, 2}
s.add(3)
print(3 in s)
```
```output
['a', 'b', 'c']
True
```
Note: `{}` is an empty dict. An empty set is `set()`.

### Set maths: & and -
Big idea: `a & b` keeps what is in both sets, and `a - b` keeps what is only in a.

`a | b` keeps everything that is in either set.

```python
a = {1, 2, 3}
b = {2, 3, 4}
print(sorted(a & b))
print(sorted(a - b))
print(sorted(a | b))
```
```output
[2, 3]
[1]
[1, 2, 3, 4]
```

### Drill
From `orders = [("apple", 2), ("pear", 1), ("apple", 3)]` build a dict with the total per fruit. Print it, then print the sorted list of the different fruits.

## World 6: Functions
- [ ] done

This world is about making your own functions. Take it one card at a time.

### What is a function
Big idea: a function is a recipe: you write it once and use it many times.

It is like a vending machine. You put something in, and it gives something back. You already know some ready-made ones: `print`, `len` and `round`.

```python
print(len("hello"))
print(round(2.567, 1))
```
```output
5
2.6
```

### def: writing a function
Big idea: `def` writes down a new recipe and gives it a name.

The line is: `def`, the name, brackets, and a colon. The recipe lines go under it, pushed in by 4 spaces.

```python
def say_hi():
    print("hi!")
```
Nothing is printed yet. The recipe is only written down, not used.

### Calling a function
Big idea: to use a function, write its name with brackets: this is called calling it.

Each call runs the recipe once.

```python
def say_hi():
    print("hi!")

say_hi()
say_hi()
```
```output
hi!
hi!
```

### Parameters: the inputs
Big idea: a parameter is an empty slot in the recipe, filled in when you call it.

The names inside the brackets of the `def` line are the parameters. Inside the function, you use those names.

```python
def greet(name):
    print("hi " + name)

greet("Ada")
greet("Bo")
```
```output
hi Ada
hi Bo
```
In the first call, `name` is "Ada". In the second, it is "Bo".

### Arguments fill the slots
Big idea: the values in the call fill the parameters in order: first to first, second to second.

The values you give in the call are called arguments.

```python
def show(a, b):
    print(a, "then", b)

show(1, 2)
show(2, 1)
```
```output
1 then 2
2 then 1
```
In `show(1, 2)`: a is 1 and b is 2. Swap them and the answer swaps too.

### return: the answer comes back
Big idea: `return` hands an answer back to the line that called the function.

Think of the vending machine again: `return` is the drink that comes out.

```python
def double(n):
    return n * 2

result = double(4)
print(result)
```
```output
8
```

### The call becomes the answer
Big idea: when the function returns, the call is replaced by the answer.

What happens in `result = add(2, 3)`:

- Python jumps into `add`, with a = 2 and b = 3
- `total = 2 + 3`, so total is 5
- `return total` sends 5 back
- `add(2, 3)` becomes 5, so result is 5

```python
def add(a, b):
    total = a + b
    return total

result = add(2, 3)
print(result)
print(add(10, 1) * 2)
```
```output
5
22
```
So `add(10, 1) * 2` becomes `11 * 2`.

### return vs print
Big idea: `print` only shows a value, but `return` gives it back so your code can use it.

A function with no `return` gives back `None`, which means "nothing".

```python
def shout_print(word):
    print(word.upper())

def shout_return(word):
    return word.upper()

a = shout_print("hi")
b = shout_return("hi")
print(a)
print(b + "!")
```
```output
HI
None
HI!
```
Note: when a level says "return, do not print", use `return` in the function.

### Parameter names live inside
Big idea: inside the function, use the parameter name, whatever the caller's variable is called.

```python
def double(n):
    return n * 2

price = 4
print(double(price))
print(double(10))
```
```output
8
20
```
In the first call, `n` is 4. The function never sees the name `price`.

### return stops the function
Big idea: when Python reaches `return`, the function ends right there.

This is handy for special cases, like an empty list.

```python
def average(numbers):
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

print(average([4, 6]))
print(average([]))
```
```output
5.0
0
```

### Default values
Big idea: a default value is a backup, used when the caller leaves that input out.

```python
def power(base, exponent=2):
    return base ** exponent

print(power(5))
print(power(5, 3))
```
```output
25
125
```
Note: parameters with a default go after the ones without.

### Keyword arguments
Big idea: in a call you can name the slot, like `greeting="yo"`, and then order does not matter.

```python
def greet(name, greeting="hi"):
    return greeting + " " + name

print(greet("Bo"))
print(greet(greeting="yo", name="Bo"))
```
```output
hi Bo
yo Bo
```

### *args: any number of inputs
Big idea: a star `*` before a parameter collects all the inputs into one group.

The group is a tuple: a fixed list in round brackets. You can loop over it or `sum` it.

```python
def show_all(*things):
    print(things)

show_all(1, 2, 3)
show_all("a", "b")
```
```output
(1, 2, 3)
('a', 'b')
```

### **kwargs: named extras
Big idea: two stars `**` collect named inputs into a dict.

Loop over it with `.items()`, like any dict.

```python
def show(**options):
    print(options)

show(size=2, color="red")
```
```output
{'size': 2, 'color': 'red'}
```

### Returning two values
Big idea: `return a, b` gives back two values at once, as a tuple.

Unpacking with `lo, hi = ...` puts each value in its own name.

```python
def min_max(nums):
    return min(nums), max(nums)

print(min_max([4, 1, 9]))
lo, hi = min_max([4, 1, 9])
print(hi - lo)
```
```output
(1, 9)
8
```

### A function is a value too
Big idea: a function name without brackets is the function itself, and you can pass it around.

`key=len` tells `sorted`: compare the words by their length.

```python
measure = len
print(measure("hello"))
words = ["kiwi", "fig", "banana"]
print(sorted(words, key=len))
```
```output
5
['fig', 'kiwi', 'banana']
```

### Passing a function in
Big idea: a parameter can hold a function, and you call it inside.

In `apply(add_one, 5)`, `func` is `add_one`. So `func(5)` is `add_one(5)`, which is 6.

```python
def add_one(n):
    return n + 1

def apply(func, value):
    return func(value)

print(apply(add_one, 5))
```
```output
6
```

### lambda: a tiny function
Big idea: `lambda x: x * 2` is a one-line function with no name.

It is handy as a `key`, to say what to compare.

```python
users = [{"name": "A", "age": 40}, {"name": "B", "age": 20}]
youngest = min(users, key=lambda u: u["age"])
print(youngest["name"])
```
```output
B
```

### Recursion: calling itself
Big idea: a recursive function solves a problem by calling itself on a smaller problem.

It needs a stop rule, called the base case. Here it stops at 0.

```python
def count_down(n):
    if n == 0:
        return
    print(n)
    count_down(n - 1)

count_down(3)
```
```output
3
2
1
```

### Recursion step by step
Big idea: each call waits for the smaller call's answer, then finishes its own sum.

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

print(factorial(3))
```
```output
6
```
- factorial(3) is 3 * factorial(2)
- factorial(2) is 2 * factorial(1)
- factorial(1) is 1 * factorial(0)
- factorial(0) is 1: the base case
- going back up: 1, then 2, then 6

### Drill
Write `add(a, b)` that returns the sum, and print `add(2, 3) * 10`. Then write `greet(name, greeting="hi")`. Last, write a recursive `sum_to(n)` that returns 1 + 2 + ... + n.

## World 7: Comprehensions
- [ ] done

This world is about building a whole new list, dict or set in one short line.

### List comprehension: a loop in one line
Big idea: a list comprehension builds a new list in one line.

Both examples below make the same list. The second one is just shorter.

```python
nums = [1, 2, 3]
doubled = []
for n in nums:
    doubled.append(n * 2)
print(doubled)
print([n * 2 for n in nums])
```
```output
[2, 4, 6]
[2, 4, 6]
```

### Reading a comprehension
Big idea: read `[n * 2 for n in nums]` as "n times 2, for each n in nums".

The first part says what goes into the new list. The `for` part says where the items come from.

```python
print([n * n for n in range(1, 6)])
print([w.upper() for w in ["hi", "yo"]])
print([len(w) for w in ["sun", "moon"]])
```
```output
[1, 4, 9, 16, 25]
['HI', 'YO']
[3, 4]
```

### Filtering with if
Big idea: add `if` at the end of a comprehension to keep only some items.

Read it as "n, for each n in nums, but only if n is even".

```python
nums = [3, 12, 8, 15]
print([n for n in nums if n % 2 == 0])
print([n for n in nums if n > 10])
```
```output
[12, 8]
[12, 15]
```

### Change and filter at once
Big idea: the front part changes each item, and the `if` part chooses which items to keep.

```python
names = ["Al", "Maria", "Bo"]
print([n.lower() for n in names if len(n) <= 3])
users = [{"name": "A", "age": 40}, {"name": "B", "age": 20}]
print([u["name"] for u in users if u["age"] > 30])
```
```output
['al', 'bo']
['A']
```

### Two fors in one comprehension
Big idea: two `for` parts make every combination, like a loop inside a loop.

The first `for` is the outer loop. The second `for` runs fully for each round of the first.

```python
print([(a, b) for a in range(2) for b in range(2)])
```
```output
[(0, 0), (0, 1), (1, 0), (1, 1)]
```
Note: if it needs more than two parts, a normal loop is easier to read.

### Dict comprehension
Big idea: with curly brackets and `key: value`, a comprehension builds a dict.

```python
words = ["sun", "moon"]
print({w: len(w) for w in words})
print({n: n * n for n in range(1, 4)})
```
```output
{'sun': 3, 'moon': 4}
{1: 1, 2: 4, 3: 9}
```

### Set comprehension
Big idea: curly brackets with just one value build a set, so repeats disappear.

```python
words = ["sun", "moon", "sky"]
print(sorted({w[0] for w in words}))
```
```output
['m', 's']
```

### any and all
Big idea: `any` asks "is at least one True?", and `all` asks "are all of them True?".

The part inside the brackets is like a comprehension without square brackets. It is called a generator: it makes the values one at a time.

```python
nums = [3, -1, 5]
print(any(n < 0 for n in nums))
print(all(n > 0 for n in nums))
```
```output
True
False
```

### sum with a generator
Big idea: `sum(... for ...)` adds up values without building a list first.

```python
print(sum(n * n for n in [1, 2, 3]))
print(sum(len(w) for w in ["sun", "moon"]))
```
```output
14
7
```

### max with key
Big idea: `max(words, key=len)` gives the word with the biggest length.

The `key` says what to compare. `min` works the same way.

```python
words = ["fig", "banana", "kiwi"]
print(max(words, key=len))
print(min(words, key=len))
```
```output
banana
fig
```

### Drill
From `text = "the quick brown fox jumps"` make, each in one line: a list of the words longer than 3 letters, a dict from word to length, and the longest word.

## World 8: Classes
- [ ] done

This world is about making your own kinds of objects, each with its own data and actions.

### What is a class
Big idea: a class is a blueprint, and each object you make from it is one real thing.

Think of a cookie cutter. The class is the cutter. Each cookie is an object. All cookies have the same shape, but each can have its own topping.

```python
class Dog:
    pass

rex = Dog()
print(type(rex))
```
```output
<class '__main__.Dog'>
```
`pass` means "nothing here yet".

### __init__: filling in the fields
Big idea: `__init__` runs by itself when you make a new object, and stores its starting values.

The values you give when making the object go into the parameters of `__init__`.

```python
class Dog:
    def __init__(self, name):
        self.name = name

rex = Dog("Rex")
print(rex.name)
```
```output
Rex
```

### self: this object
Big idea: `self` means "this object", the one we are working on now.

`self.name = name` stores the name on this object. Python fills in `self` for you, so you never write it in the call.

```python
class Dog:
    def __init__(self, name, age=1):
        self.name = name
        self.age = age

rex = Dog("Rex", 3)
bo = Dog("Bo")
print(rex.name, rex.age)
print(bo.name, bo.age)
```
```output
Rex 3
Bo 1
```
Note: without `self.` the value is lost when `__init__` ends.

### Attributes: an object's values
Big idea: an attribute is a value stored on an object, like `player.score`.

You can read it and change it with a dot.

```python
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

p = Player("Ada")
p.score = 5
print(p.name, p.score)
```
```output
Ada 5
```

### Methods: what an object can do
Big idea: a method is a function inside a class, and it always gets `self` first.

Call it with a dot: `tom.speak()`.

```python
class Cat:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return self.name + " says meow"

tom = Cat("Tom")
print(tom.speak())
```
```output
Tom says meow
```

### Methods that change the object
Big idea: a method can change the object's own values through `self`.

```python
class Counter:
    def __init__(self):
        self.count = 0

    def add(self, n):
        self.count = self.count + n

c = Counter()
c.add(2)
c.add(3)
print(c.count)
```
```output
5
```

### Class attributes: shared by all
Big idea: a value written straight in the class, not on `self`, is shared by every object.

```python
class Track:
    plays_total = 0

    def play(self):
        Track.plays_total = Track.plays_total + 1

Track().play()
Track().play()
print(Track.plays_total)
```
```output
2
```

### __str__: what print shows
Big idea: `__str__` decides what `print(obj)` shows.

Methods with two underscores on each side are special. Python calls them for you.

```python
class Box:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def __str__(self):
        return f"{self.w} x {self.h}"

print(Box(2, 3))
```
```output
2 x 3
```

### __repr__ and __eq__
Big idea: `__repr__` is the view shown inside lists, and `__eq__` decides what `==` means.

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

print([Point(1, 2)])
print(Point(1, 2) == Point(1, 2))
```
```output
[Point(1, 2)]
True
```

### Inheritance: a kind of
Big idea: `class Dog(Animal)` means a Dog is a kind of Animal, and it gets all of Animal's methods.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return "animal: " + self.name

class Dog(Animal):
    pass

print(Dog("Rex").describe())
```
```output
animal: Rex
```

### Overriding a method
Big idea: when the child class writes a method with the same name, its own version is used.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return "animal: " + self.name

class Dog(Animal):
    def describe(self):
        return "dog: " + self.name

print(Animal("Tom").describe())
print(Dog("Rex").describe())
```
```output
animal: Tom
dog: Rex
```

### super: use the parent's version
Big idea: `super().__init__(...)` runs the parent's `__init__`, so you only add what is new.

```python
class Media:
    def __init__(self, title):
        self.title = title

class Track(Media):
    def __init__(self, title, bpm):
        super().__init__(title)
        self.bpm = bpm

t = Track("Night", 128)
print(t.title, t.bpm)
```
```output
Night 128
```

### property: a method that looks like a value
Big idea: `@property` lets you read a method like a value, with no brackets.

```python
class Circle:
    def __init__(self, r):
        self.r = r

    @property
    def area(self):
        return round(3.14159 * self.r ** 2, 2)

print(Circle(2).area)
```
```output
12.57
```

### dataclass: less typing
Big idea: `@dataclass` writes `__init__`, `__repr__` and `__eq__` for you.

You only list the fields and their types.

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

print(Point(1, 2))
print(Point(1, 2) == Point(1, 2))
```
```output
Point(x=1, y=2)
True
```

### Drill
Write `BankAccount(balance)` with `deposit(n)`, a `withdraw(n)` that returns False instead of going below 0, and a `__str__`. Then write `SavingsAccount(BankAccount)` that adds `apply_interest(rate)`.

## World 9: Errors, files and modules
- [ ] done

This world is about what to do when things go wrong, saving text in files, and using extra tools.

### What is an error
Big idea: when Python cannot do something, it stops and shows an error (also called an exception).

The last line says what kind of error it is, and why.

```python
print(int("abc"))
```
```output
ValueError: invalid literal for int() with base 10: 'abc'
```

### Reading an error
Big idea: read an error message from the bottom up: the last line says what went wrong.

The line above it shows where it happened. Common kinds:

- `NameError`: a name Python does not know, often a typo
- `TypeError`: wrong kind of value, like text + number
- `ValueError`: right kind, bad value, like `int("abc")`
- `IndexError`: no item at that position
- `KeyError`: no such key in the dict
- `ZeroDivisionError`: dividing by zero

### try and except
Big idea: `try` runs risky code, and `except` catches the error instead of crashing.

If an error happens inside `try`, Python jumps to the `except` block.

```python
def to_int(text):
    try:
        return int(text)
    except ValueError:
        return -1

print(to_int("42"))
print(to_int("abc"))
```
```output
42
-1
```
Note: name the error you expect, like `except ValueError:`. A bare `except:` hides real bugs.

### Catch the right error
Big idea: each `except` catches only the kind of error it names.

```python
try:
    print(10 / 0)
except ZeroDivisionError:
    print("cannot divide by zero")
```
```output
cannot divide by zero
```

### finally: always runs
Big idea: the `finally` block runs at the end every time, error or not.

```python
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
    finally:
        print("done")

print(divide(6, 3))
print(divide(1, 0))
```
```output
done
2.0
done
None
```
"done" shows before each answer, because `finally` runs just before the answer goes back.

### raise: make an error on purpose
Big idea: `raise` creates an error on purpose, when your function gets a bad value.

```python
def check_age(age):
    if age < 18:
        raise ValueError("too young")
    return "ok"

print(check_age(20))
print(check_age(12))
```
```output
ok
ValueError: too young
```

### Your own error type
Big idea: a class that inherits from `Exception` is your own kind of error.

`except ... as e` catches it and puts the error in `e`.

```python
class EmptyListError(Exception):
    pass

try:
    raise EmptyListError("empty")
except EmptyListError as e:
    print(e)
```
```output
empty
```

### Writing a file
Big idea: `open(name, "w")` opens a file for writing, and `with` closes it for you after.

`"w"` starts the file fresh. `"a"` adds to the end. `"\n"` means "new line".

```python
with open("list.txt", "w") as f:
    f.write("milk\n")
    f.write("eggs\n")
```

### Reading a file
Big idea: `open(name)` opens a file for reading, and `.read()` gives all its text.

`.read().splitlines()` gives a list of the lines, without the new line signs.

```python
with open("list.txt", "w") as f:
    f.write("milk\neggs\n")

with open("list.txt") as f:
    lines = f.read().splitlines()
print(lines)
```
```output
['milk', 'eggs']
```

### Looping over a file
Big idea: a `for` loop over a file gives you one line at a time.

Each line ends with `"\n"`, so use `.strip()` to clean it.

```python
with open("list.txt", "w") as f:
    f.write("milk\neggs\n")

with open("list.txt") as f:
    for line in f:
        print(line.strip().upper())
```
```output
MILK
EGGS
```

### import: extra tools
Big idea: `import` brings in a module: a box of extra tools that comes with Python.

```python
import math
print(math.sqrt(16))

from math import pi
print(round(pi, 4))
```
```output
4.0
3.1416
```

### json: text to dict
Big idea: `json.loads` turns JSON text into dicts and lists, and `json.dumps` turns them back into text.

JSON is a common text format for data. It looks a lot like Python dicts.

```python
import json

text = '{"name": "Ada", "langs": ["py", "sql"]}'
data = json.loads(text)
print(data["name"])
print(len(data["langs"]))
print(json.dumps({"a": 1}))
```
```output
Ada
2
{"a": 1}
```

### json with files
Big idea: `json.dump` writes data to a file, and `json.load` reads it back.

Without the s at the end, they work with files instead of text.

```python
import json

with open("users.json", "w") as f:
    json.dump([{"name": "A", "age": 30}], f)

with open("users.json") as f:
    users = json.load(f)
print(users[0]["age"])
```
```output
30
```
Note: reading a file that does not exist gives `FileNotFoundError`. Catch it with `try`.

### Drill
Write `to_int(text)` that returns -1 when the text is not a number. Then write three words to a file, one per line, read it back, and print how many lines it has.

## World 10: NumPy and Pandas
- [ ] done

These two libraries are used from week one of Term 1. A library is a big box of extra tools you install.

### NumPy arrays
Big idea: a NumPy array is a list of numbers that does maths on every item at once.

No loop needed. That also makes it much faster on big data.

```python
import numpy as np
a = np.array([1, 2, 3])
print(a * 2)
print(a.sum(), a.mean())
```
```output
[2 4 6]
6 2.0
```

### Filtering an array
Big idea: `a[a > 1]` keeps only the items where the question is True.

This is called a mask: a list of True and False that says which items to keep.

```python
import numpy as np
a = np.array([1, 2, 3, 4])
print(a > 2)
print(a[a > 2])
```
```output
[False False  True  True]
[3 4]
```

### Pandas DataFrame: a table
Big idea: a DataFrame is a table, like a spreadsheet, with named columns.

One column on its own is called a Series. In real work you often load a table with `pd.read_csv("file.csv")`.

```python
import pandas as pd
df = pd.DataFrame({"fruit": ["apple", "pear", "kiwi"], "price": [2, 5, 3]})
print(df["price"].sum())
print(df.shape)
```
```output
10
(3, 2)
```

### Choosing rows
Big idea: `df[df["price"] > 2]` keeps only the rows where the question is True.

It is the same mask idea as in NumPy.

```python
import pandas as pd
df = pd.DataFrame({"fruit": ["apple", "pear", "kiwi"], "price": [2, 5, 3]})
cheap = df[df["price"] < 4]
print(list(cheap["fruit"]))
```
```output
['apple', 'kiwi']
```

### groupby: totals per group
Big idea: `groupby` splits the table into groups, then you add up each group.

```python
import pandas as pd
df = pd.DataFrame({"shop": ["A", "B", "A"], "sales": [10, 5, 7]})
totals = df.groupby("shop")["sales"].sum()
print(totals.to_dict())
```
```output
{'A': 17, 'B': 5}
```

### Drill
Make a DataFrame of three fruits with a price and a quantity. Add a column `total` that is price times quantity, and print the rows with a total above 10.

## World 11: Algorithms and Big-O
- [ ] done

An algorithm is a step by step plan to solve a problem. Big-O says how fast it is.

### Big-O: how work grows
Big idea: Big-O tells you how much more work there is when the data gets bigger.

| Big-O | means | example |
|---|---|---|
| O(1) | always the same work | dict lookup |
| O(n) | twice the data, twice the work | one loop |
| O(n²) | twice the data, four times the work | a loop inside a loop |

### in: list versus set
Big idea: `in` on a list checks every item, but `in` on a set or dict jumps straight to it.

So `in` on a list is O(n), and on a set it is O(1). For big data, use a set.

```python
names = ["Ann", "Bo", "Cy"]
fast = set(names)
print("Bo" in names)
print("Bo" in fast)
```
```output
True
True
```

### Binary search
Big idea: in a sorted list, look at the middle and throw away the half where the value cannot be.

Each step halves the list. Even a million items take only about 20 steps.

```python
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

print(binary_search([1, 3, 5, 7, 9], 7))
```
```output
3
```

### Remembering answers
Big idea: store answers you already worked out, so you never work them out twice.

This is called memoisation. A dict is the memory.

```python
memo = {}

def fib(n):
    if n < 2:
        return n
    if n not in memo:
        memo[n] = fib(n - 1) + fib(n - 2)
    return memo[n]

print(fib(50))
```
```output
12586269025
```

### Drill
Write `two_sum(nums, target)` that finds two numbers adding up to target, with one loop and a set. Say why two loops inside each other would be O(n²).

## World 12: SQL and data access
- [ ] done

A database keeps data in tables. SQL is the language you use to ask it questions.

### What is a database
Big idea: a database is a set of tables, and each table is like a spreadsheet with rows and columns.

SQL is the language for talking to it. The words you must know: `SELECT`, `FROM`, `WHERE`, `ORDER BY`, `JOIN`, `GROUP BY`, `INSERT`, `UPDATE`, `DELETE`.

### sqlite3: talking to a database
Big idea: Python's `sqlite3` module connects to a database and runs SQL with `execute`.

`":memory:"` makes a small database that lives only while the program runs. `commit` saves the changes.

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE tracks (title TEXT, bpm INTEGER)")
con.execute("INSERT INTO tracks VALUES (?, ?)", ("Night", 128))
con.commit()
print(con.execute("SELECT title, bpm FROM tracks").fetchall())
```
```output
[('Night', 128)]
```

### Placeholders: the ? signs
Big idea: put `?` in the SQL and give the values apart, never glue them in with f-strings.

This keeps bad input from breaking your database.

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE tracks (title TEXT, bpm INTEGER)")
con.execute("INSERT INTO tracks VALUES (?, ?)", ("Night", 128))
con.execute("INSERT INTO tracks VALUES (?, ?)", ("Calm", 90))
rows = con.execute("SELECT title FROM tracks WHERE bpm > ?", (100,)).fetchall()
print(rows)
```
```output
[('Night',)]
```

### APIs: data from the web
Big idea: an API is a website that answers with data instead of a page.

`requests.get` asks for it, and `.json()` turns the answer into dicts and lists. You install it first with `pip install requests`.

```python
import requests
r = requests.get("https://api.example.com/items")
data = r.json()
```

### Drill
Make a table of users and a table of orders. Put in three of each. Then ask for the total spent per user, with `JOIN` and `GROUP BY`.

## World 13: Tooling
- [ ] done

These are the tools around your code: the terminal, packages, Git and tests.

### The terminal
Big idea: the terminal is a window where you type commands instead of clicking.

```text
pwd              where am I?
ls               what is in this folder?
cd projects      go into a folder
mkdir new        make a folder
python file.py   run a Python file
```

### Virtual environments
Big idea: a virtual environment is a private box of packages for one project.

A package is a library you install, like pandas. One box per project, so projects do not get in each other's way.

```text
python -m venv .venv
source .venv/bin/activate
pip install pandas
```

### Git: saving snapshots
Big idea: Git saves snapshots of your project, called commits, so you can go back and share.

```text
git status
git add .
git commit -m "Add login page"
git push
```
Commit small and often.

### Tests with assert
Big idea: `assert` checks that something is True, and stops with an error when it is not.

A test is a small function that checks your code. `python -m pytest` runs all the tests.

```python
def add(a, b):
    return a + b

assert add(2, 3) == 5
assert add(2, 2) == 5
```
```output
AssertionError
```

### Style: neat code
Big idea: neat code follows the same simple rules everywhere, so others can read it.

- 4 spaces to indent
- `snake_case` for functions and variables
- `PascalCase` for classes
- type hints show the kinds of values: `def area(r: float) -> float:`

### Drill
Make a folder with a virtual environment. Install pytest, write one function and one test for it, and commit it with Git.

## Reading order for the next four weeks

### Your four-week plan
Big idea: a few worlds each week, and by week 4 you can write worlds 1 to 9 from a blank file.

- Week 1: worlds 1 to 4
- Week 2: worlds 5 to 7
- Week 3: worlds 8 and 9, and world 13
- Week 4: worlds 10 and 11, and world 12 if there is time

The goal: type the ideas of worlds 1 to 9 without looking and without help.
