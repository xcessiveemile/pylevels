WORLD = {'name': 'Classes', 'title': '__init__, methods, dunders, inheritance'}

# A drill is one concept shown ten different ways. Each round is its own
# small task with its own brief, starter, expected output and hint.
DRILLS = [
    {'id': 's8-1',
     'title': 'Init and attributes',
     'brief': 'A class that stores things on self.',
     'lesson': 'A class is a blueprint. __init__(self, ...) runs when you create one, and self.name = name '
               'stores a value on that object. Create with Dog("Rex"), read with dog.name.  Example: class Dog:  '
               'def __init__(self, name):  self.name = name',
     'starter': '',
     'expected': '',
     'hidden': '',
     'hint': '',
     'concepts': ['classes', '__init__', 'attributes'],
     'rounds': [{'brief': 'Write class Dog with __init__(name) storing name, then print the name of a Dog called '
                          'Rex.',
                 'starter': '# define Dog here\n',
                 'expected': 'Rex\n',
                 'hidden': 'print(Dog("Rex").name)\n',
                 'hint': 'class Dog:\n    def __init__(self, name):\n        self.name = name',
                 'tip': 'class Name: with def __init__(self, ...): storing self.x = x.'},
                {'brief': 'Write class Point storing x and y.',
                 'starter': '# define Point here\n',
                 'expected': '3 4\n',
                 'hidden': 'p = Point(3, 4)\nprint(p.x, p.y)\n',
                 'hint': 'class Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y',
                 'tip': 'class Name: with def __init__(self, ...): storing self.x = x.'},
                {'brief': 'Write class Counter whose count starts at 0.',
                 'starter': '# define Counter here\n',
                 'expected': '0\n',
                 'hidden': 'print(Counter().count)\n',
                 'hint': 'class Counter:\n    def __init__(self):\n        self.count = 0',
                 'tip': 'class Name: with def __init__(self, ...): storing self.x = x.'},
                {'brief': 'Write class Book with title and pages, and print the pages of a Book.',
                 'starter': '# define Book here\n',
                 'expected': '412\n',
                 'hidden': 'print(Book("Dune", 412).pages)\n',
                 'hint': 'class Book:\n'
                         '    def __init__(self, title, pages):\n'
                         '        self.title = title\n'
                         '        self.pages = pages',
                 'tip': 'class Name: with def __init__(self, ...): storing self.x = x.'},
                {'brief': 'Write class Track(title, bpm=120) with a default bpm.',
                 'starter': '# define Track here\n',
                 'expected': '120\n90\n',
                 'hidden': 't = Track("Night")\nprint(t.bpm)\nprint(Track("Day", 90).bpm)\n',
                 'hint': 'class Track:\n'
                         '    def __init__(self, title, bpm=120):\n'
                         '        self.title = title\n'
                         '        self.bpm = bpm',
                 'tip': 'class Name: with def __init__(self, ...): storing self.x = x.'},
                {'brief': 'Write class Account starting with balance 0 and an empty list of moves.',
                 'starter': '# define Account here\n',
                 'expected': '0 []\n',
                 'hidden': 'a = Account()\nprint(a.balance, a.moves)\n',
                 'hint': 'class Account:\n'
                         '    def __init__(self):\n'
                         '        self.balance = 0\n'
                         '        self.moves = []',
                 'tip': 'class Name: with def __init__(self, ...): storing self.x = x.'},
                {'brief': 'Write class Circle(r) that also stores area as 3.14159 times r squared, rounded to 2 '
                          'decimals, in __init__.',
                 'starter': '# define Circle here\n',
                 'expected': '12.57\n',
                 'hidden': 'print(Circle(2).area)\n',
                 'hint': 'class Circle:\n'
                         '    def __init__(self, r):\n'
                         '        self.r = r\n'
                         '        self.area = round(3.14159 * r * r, 2)',
                 'tip': 'class Name: with def __init__(self, ...): storing self.x = x.'},
                {'brief': 'Write class Player(name) with a score that starts at 0, then change the score to 5 '
                          'and print it.',
                 'starter': '# define Player here, then make one, set score to 5 and print it\n',
                 'expected': '5\n',
                 'hidden': '',
                 'hint': 'class Player:\n'
                         '    def __init__(self, name):\n'
                         '        self.name = name\n'
                         '        self.score = 0\n'
                         '\n'
                         'p = Player("Kim")\n'
                         'p.score = 5\n'
                         'print(p.score)',
                 'tip': 'class Name: with def __init__(self, ...): storing self.x = x.'},
                {'brief': 'Write class Temperature(celsius) that also stores fahrenheit as celsius times 1.8 '
                          'plus 32.',
                 'starter': '# define Temperature here\n',
                 'expected': '212.0\n',
                 'hidden': 'print(Temperature(100).fahrenheit)\n',
                 'hint': 'class Temperature:\n'
                         '    def __init__(self, celsius):\n'
                         '        self.celsius = celsius\n'
                         '        self.fahrenheit = celsius * 1.8 + 32',
                 'tip': 'class Name: with def __init__(self, ...): storing self.x = x.'},
                {'brief': 'Write class Pair(a, b) that stores both and their sum as total.',
                 'starter': '# define Pair here\n',
                 'expected': '13\n',
                 'hidden': 'print(Pair(4, 9).total)\n',
                 'hint': 'class Pair:\n'
                         '    def __init__(self, a, b):\n'
                         '        self.a = a\n'
                         '        self.b = b\n'
                         '        self.total = a + b',
                 'tip': 'class Name: with def __init__(self, ...): storing self.x = x.'}]},
    {'id': 's8-2',
     'title': 'Methods',
     'brief': 'Functions inside a class that read and change self.',
     'lesson': 'A method is a function inside a class. It always takes self first, and through self it reads or '
               "changes the object's values.  Example: def add(self, n):  self.count = self.count + n",
     'starter': '',
     'expected': '',
     'hidden': '',
     'hint': '',
     'concepts': ['classes', 'methods'],
     'rounds': [{'brief': 'Write class Cat(name) with speak() returning name plus " says meow".',
                 'starter': '# define Cat here\n',
                 'expected': 'Mia says meow\n',
                 'hidden': 'print(Cat("Mia").speak())\n',
                 'hint': 'class Cat:\n'
                         '    def __init__(self, name):\n'
                         '        self.name = name\n'
                         '\n'
                         '    def speak(self):\n'
                         '        return self.name + " says meow"',
                 'tip': 'a method is def name(self, ...): inside the class, using self.'},
                {'brief': 'Write class Counter starting at 0 with add(n).',
                 'starter': '# define Counter here\n',
                 'expected': '7\n',
                 'hidden': 'c = Counter()\nc.add(2)\nc.add(5)\nprint(c.count)\n',
                 'hint': 'class Counter:\n'
                         '    def __init__(self):\n'
                         '        self.count = 0\n'
                         '\n'
                         '    def add(self, n):\n'
                         '        self.count = self.count + n',
                 'tip': 'a method is def name(self, ...): inside the class, using self.'},
                {'brief': 'Write class Thermostat starting at 20 with up() and down() changing temp by 1.',
                 'starter': '# define Thermostat here\n',
                 'expected': '21\n',
                 'hidden': 't = Thermostat()\nt.up()\nt.up()\nt.down()\nprint(t.temp)\n',
                 'hint': 'class Thermostat:\n'
                         '    def __init__(self):\n'
                         '        self.temp = 20\n'
                         '\n'
                         '    def up(self):\n'
                         '        self.temp = self.temp + 1\n'
                         '\n'
                         '    def down(self):\n'
                         '        self.temp = self.temp - 1',
                 'tip': 'a method is def name(self, ...): inside the class, using self.'},
                {'brief': 'Write class Box(w, h) with area() returning w times h.',
                 'starter': '# define Box here\n',
                 'expected': '21\n',
                 'hidden': 'print(Box(3, 7).area())\n',
                 'hint': 'class Box:\n'
                         '    def __init__(self, w, h):\n'
                         '        self.w = w\n'
                         '        self.h = h\n'
                         '\n'
                         '    def area(self):\n'
                         '        return self.w * self.h',
                 'tip': 'a method is def name(self, ...): inside the class, using self.'},
                {'brief': 'Write class Account(balance) with deposit(n) and withdraw(n).',
                 'starter': '# define Account here\n',
                 'expected': '120\n',
                 'hidden': 'a = Account(100)\na.deposit(50)\na.withdraw(30)\nprint(a.balance)\n',
                 'hint': 'class Account:\n'
                         '    def __init__(self, balance):\n'
                         '        self.balance = balance\n'
                         '\n'
                         '    def deposit(self, n):\n'
                         '        self.balance = self.balance + n\n'
                         '\n'
                         '    def withdraw(self, n):\n'
                         '        self.balance = self.balance - n',
                 'tip': 'a method is def name(self, ...): inside the class, using self.'},
                {'brief': 'Write class Point(x, y) with dist() returning the distance to (0, 0).',
                 'starter': '# define Point here\n',
                 'expected': '5.0\n',
                 'hidden': 'print(Point(3, 4).dist())\n',
                 'hint': 'class Point:\n'
                         '    def __init__(self, x, y):\n'
                         '        self.x = x\n'
                         '        self.y = y\n'
                         '\n'
                         '    def dist(self):\n'
                         '        return (self.x ** 2 + self.y ** 2) ** 0.5',
                 'tip': 'a method is def name(self, ...): inside the class, using self.'},
                {'brief': 'Write class Playlist with an empty songs list, add(song), and count() returning how '
                          'many songs.',
                 'starter': '# define Playlist here\n',
                 'expected': '2\n',
                 'hidden': 'p = Playlist()\np.add("a")\np.add("b")\nprint(p.count())\n',
                 'hint': 'class Playlist:\n'
                         '    def __init__(self):\n'
                         '        self.songs = []\n'
                         '\n'
                         '    def add(self, song):\n'
                         '        self.songs.append(song)\n'
                         '\n'
                         '    def count(self):\n'
                         '        return len(self.songs)',
                 'tip': 'a method is def name(self, ...): inside the class, using self.'},
                {'brief': 'Write class Light with on False, and toggle() that flips it.',
                 'starter': '# define Light here\n',
                 'expected': 'True\nFalse\n',
                 'hidden': 'l = Light()\nl.toggle()\nprint(l.on)\nl.toggle()\nprint(l.on)\n',
                 'hint': 'class Light:\n'
                         '    def __init__(self):\n'
                         '        self.on = False\n'
                         '\n'
                         '    def toggle(self):\n'
                         '        self.on = not self.on',
                 'tip': 'a method is def name(self, ...): inside the class, using self.'},
                {'brief': 'Write class Stack with push(item), pop() returning the last item, and an items list.',
                 'starter': '# define Stack here\n',
                 'expected': '2\n[1]\n',
                 'hidden': 's = Stack()\ns.push(1)\ns.push(2)\nprint(s.pop())\nprint(s.items)\n',
                 'hint': 'class Stack:\n'
                         '    def __init__(self):\n'
                         '        self.items = []\n'
                         '\n'
                         '    def push(self, item):\n'
                         '        self.items.append(item)\n'
                         '\n'
                         '    def pop(self):\n'
                         '        return self.items.pop()',
                 'tip': 'a method is def name(self, ...): inside the class, using self.'},
                {'brief': 'Write class Wallet(coins) with spend(n) that returns False without changing coins '
                          'when there are not enough, else True.',
                 'starter': '# define Wallet here\n',
                 'expected': 'True\nFalse\n6\n',
                 'hidden': 'w = Wallet(10)\nprint(w.spend(4))\nprint(w.spend(20))\nprint(w.coins)\n',
                 'hint': 'class Wallet:\n'
                         '    def __init__(self, coins):\n'
                         '        self.coins = coins\n'
                         '\n'
                         '    def spend(self, n):\n'
                         '        if n > self.coins:\n'
                         '            return False\n'
                         '        self.coins = self.coins - n\n'
                         '        return True',
                 'tip': 'a method is def name(self, ...): inside the class, using self.'}]},
    {'id': 's8-3',
     'title': 'Dunder methods',
     'brief': '__str__, __repr__, __eq__, __len__ and friends.',
     'lesson': "Dunder methods make objects work with Python's own tools: __str__ decides what print shows, "
               '__repr__ the developer view, __eq__ what == means, __len__ what len gives.  Example: def '
               '__str__(self):  return f"{self.w} x {self.h}"',
     'starter': '',
     'expected': '',
     'hidden': '',
     'hint': '',
     'concepts': ['__str__', '__repr__', '__eq__', '__len__'],
     'rounds': [{'brief': 'Write class Box(w, h) whose __str__ returns "w x h".',
                 'starter': '# define Box here\n',
                 'expected': '2 x 3\n',
                 'hidden': 'print(Box(2, 3))\n',
                 'hint': 'class Box:\n'
                         '    def __init__(self, w, h):\n'
                         '        self.w = w\n'
                         '        self.h = h\n'
                         '\n'
                         '    def __str__(self):\n'
                         '        return f"{self.w} x {self.h}"',
                 'tip': '__str__ for print, __repr__ for the developer view, __eq__ for ==, __len__ for len.'},
                {'brief': 'Write class Point(x, y) whose __repr__ returns "Point(x, y)".',
                 'starter': '# define Point here\n',
                 'expected': 'Point(3, 4)\n',
                 'hidden': 'print(Point(3, 4))\n',
                 'hint': 'class Point:\n'
                         '    def __init__(self, x, y):\n'
                         '        self.x = x\n'
                         '        self.y = y\n'
                         '\n'
                         '    def __repr__(self):\n'
                         '        return f"Point({self.x}, {self.y})"',
                 'tip': '__str__ for print, __repr__ for the developer view, __eq__ for ==, __len__ for len.'},
                {'brief': 'Write class Point(x, y) with __eq__ that compares both numbers.',
                 'starter': '# define Point here\n',
                 'expected': 'True\nFalse\n',
                 'hidden': 'print(Point(1, 2) == Point(1, 2))\nprint(Point(1, 2) == Point(2, 1))\n',
                 'hint': 'class Point:\n'
                         '    def __init__(self, x, y):\n'
                         '        self.x = x\n'
                         '        self.y = y\n'
                         '\n'
                         '    def __eq__(self, other):\n'
                         '        return self.x == other.x and self.y == other.y',
                 'tip': '__str__ for print, __repr__ for the developer view, __eq__ for ==, __len__ for len.'},
                {'brief': 'Write class Playlist(songs) with __len__ returning how many songs.',
                 'starter': '# define Playlist here\n',
                 'expected': '3\n',
                 'hidden': 'print(len(Playlist(["a", "b", "c"])))\n',
                 'hint': 'class Playlist:\n'
                         '    def __init__(self, songs):\n'
                         '        self.songs = songs\n'
                         '\n'
                         '    def __len__(self):\n'
                         '        return len(self.songs)',
                 'tip': '__str__ for print, __repr__ for the developer view, __eq__ for ==, __len__ for len.'},
                {'brief': 'Write class Money(cents) with __str__ returning the amount like €12.50.',
                 'starter': '# define Money here\n',
                 'expected': '€12.50\n',
                 'hidden': 'print(Money(1250))\n',
                 'hint': 'class Money:\n'
                         '    def __init__(self, cents):\n'
                         '        self.cents = cents\n'
                         '\n'
                         '    def __str__(self):\n'
                         '        return f"€{self.cents / 100:.2f}"',
                 'tip': '__str__ for print, __repr__ for the developer view, __eq__ for ==, __len__ for len.'},
                {'brief': 'Write class Vector(x, y) with __add__ returning a new Vector of the sums, and '
                          '__repr__ as Vector(x, y).',
                 'starter': '# define Vector here\n',
                 'expected': 'Vector(4, 6)\n',
                 'hidden': 'print(Vector(1, 2) + Vector(3, 4))\n',
                 'hint': 'class Vector:\n'
                         '    def __init__(self, x, y):\n'
                         '        self.x = x\n'
                         '        self.y = y\n'
                         '\n'
                         '    def __add__(self, other):\n'
                         '        return Vector(self.x + other.x, self.y + other.y)\n'
                         '\n'
                         '    def __repr__(self):\n'
                         '        return f"Vector({self.x}, {self.y})"',
                 'tip': '__str__ for print, __repr__ for the developer view, __eq__ for ==, __len__ for len.'},
                {'brief': 'Write class Deck(cards) with __getitem__ so deck[i] gives the i-th card.',
                 'starter': '# define Deck here\n',
                 'expected': 'two\n',
                 'hidden': 'd = Deck(["ace", "two"])\nprint(d[1])\n',
                 'hint': 'class Deck:\n'
                         '    def __init__(self, cards):\n'
                         '        self.cards = cards\n'
                         '\n'
                         '    def __getitem__(self, i):\n'
                         '        return self.cards[i]',
                 'tip': '__str__ for print, __repr__ for the developer view, __eq__ for ==, __len__ for len.'},
                {'brief': 'Write class Temperature(c) with __lt__ so temperatures can be sorted, and print the '
                          'sorted list of their c values.',
                 'starter': '# define Temperature here\n',
                 'expected': '[10, 20, 30]\n',
                 'hidden': 'temps = sorted([Temperature(30), Temperature(10), Temperature(20)])\n'
                           'print([t.c for t in temps])\n',
                 'hint': 'class Temperature:\n'
                         '    def __init__(self, c):\n'
                         '        self.c = c\n'
                         '\n'
                         '    def __lt__(self, other):\n'
                         '        return self.c < other.c',
                 'tip': '__str__ for print, __repr__ for the developer view, __eq__ for ==, __len__ for len.'},
                {'brief': 'Write class Cat(name) with __str__ returning "Cat: name" and __repr__ returning '
                          '"Cat(name)".',
                 'starter': '# define Cat here\n',
                 'expected': "Cat: Mia\nCat('Mia')\n",
                 'hidden': 'c = Cat("Mia")\nprint(c)\nprint(repr(c))\n',
                 'hint': 'class Cat:\n'
                         '    def __init__(self, name):\n'
                         '        self.name = name\n'
                         '\n'
                         '    def __str__(self):\n'
                         '        return f"Cat: {self.name}"\n'
                         '\n'
                         '    def __repr__(self):\n'
                         '        return f"Cat({self.name!r})"',
                 'tip': '__str__ for print, __repr__ for the developer view, __eq__ for ==, __len__ for len.'},
                {'brief': 'Write class Bag(items) with __contains__ so `x in bag` works.',
                 'starter': '# define Bag here\n',
                 'expected': 'True\nFalse\n',
                 'hidden': 'b = Bag(["pen", "key"])\nprint("key" in b)\nprint("cat" in b)\n',
                 'hint': 'class Bag:\n'
                         '    def __init__(self, items):\n'
                         '        self.items = items\n'
                         '\n'
                         '    def __contains__(self, item):\n'
                         '        return item in self.items',
                 'tip': '__str__ for print, __repr__ for the developer view, __eq__ for ==, __len__ for len.'}]},
    {'id': 's8-4',
     'title': 'Inheritance and more',
     'brief': 'Subclasses, super(), class attributes, properties, dataclasses.',
     'lesson': 'class Dog(Animal): makes Dog inherit everything from Animal, and it can override methods; '
               "super().__init__(...) runs the parent's setup. A class attribute is shared by all objects. "
               '@property lets a method look like a value.  Example: class Dog(Animal):',
     'starter': '',
     'expected': '',
     'hidden': '',
     'hint': '',
     'concepts': ['inheritance', 'super', 'class attributes', 'property', 'dataclass'],
     'rounds': [{'brief': 'Write Animal(name) with describe() returning "animal: name", and Dog(Animal) whose '
                          'describe() returns "dog: name".',
                 'starter': '# define Animal and Dog here\n',
                 'expected': 'animal: x\ndog: Rex\n',
                 'hidden': 'print(Animal("x").describe())\nprint(Dog("Rex").describe())\n',
                 'hint': 'class Animal:\n'
                         '    def __init__(self, name):\n'
                         '        self.name = name\n'
                         '\n'
                         '    def describe(self):\n'
                         '        return f"animal: {self.name}"\n'
                         '\n'
                         '\n'
                         'class Dog(Animal):\n'
                         '    def describe(self):\n'
                         '        return f"dog: {self.name}"',
                 'tip': "class Child(Parent): inherits; super().__init__() runs the parent's setup."},
                {'brief': 'Write Media(title) and Track(Media) whose __init__ also takes bpm and calls '
                          'super().__init__(title).',
                 'starter': '# define Media and Track here\n',
                 'expected': 'Night 128\n',
                 'hidden': 't = Track("Night", 128)\nprint(t.title, t.bpm)\n',
                 'hint': 'class Media:\n'
                         '    def __init__(self, title):\n'
                         '        self.title = title\n'
                         '\n'
                         '\n'
                         'class Track(Media):\n'
                         '    def __init__(self, title, bpm):\n'
                         '        super().__init__(title)\n'
                         '        self.bpm = bpm',
                 'tip': "class Child(Parent): inherits; super().__init__() runs the parent's setup."},
                {'brief': 'Write class Track with a class attribute plays_total and play() that adds one to it.',
                 'starter': '# define Track here\n',
                 'expected': '2\n',
                 'hidden': 'Track().play()\nTrack().play()\nprint(Track.plays_total)\n',
                 'hint': 'class Track:\n'
                         '    plays_total = 0\n'
                         '\n'
                         '    def play(self):\n'
                         '        Track.plays_total = Track.plays_total + 1',
                 'tip': "class Child(Parent): inherits; super().__init__() runs the parent's setup."},
                {'brief': 'Write class Circle(r) with a property area returning 3.14159 times r squared, rounded '
                          'to 2 decimals.',
                 'starter': '# define Circle here\n',
                 'expected': '3.14\n',
                 'hidden': 'print(Circle(1).area)\n',
                 'hint': 'class Circle:\n'
                         '    def __init__(self, r):\n'
                         '        self.r = r\n'
                         '\n'
                         '    @property\n'
                         '    def area(self):\n'
                         '        return round(3.14159 * self.r ** 2, 2)',
                 'tip': "class Child(Parent): inherits; super().__init__() runs the parent's setup."},
                {'brief': 'Write class Circle with a classmethod from_diameter(d) that returns a Circle with r = '
                          'd / 2.',
                 'starter': '# define Circle here\n',
                 'expected': '5.0\n',
                 'hidden': 'print(Circle.from_diameter(10).r)\n',
                 'hint': 'class Circle:\n'
                         '    def __init__(self, r):\n'
                         '        self.r = r\n'
                         '\n'
                         '    @classmethod\n'
                         '    def from_diameter(cls, d):\n'
                         '        return cls(d / 2)',
                 'tip': "class Child(Parent): inherits; super().__init__() runs the parent's setup."},
                {'brief': 'Write a dataclass Point with x and y as floats, then print Point(1, 2) and whether '
                          'Point(1, 2) equals Point(1, 2).',
                 'starter': 'from dataclasses import dataclass\n\n# define Point here\n',
                 'expected': 'Point(x=1, y=2)\nTrue\n',
                 'hidden': 'print(Point(1, 2))\nprint(Point(1, 2) == Point(1, 2))\n',
                 'hint': '@dataclass\nclass Point:\n    x: float\n    y: float',
                 'tip': "class Child(Parent): inherits; super().__init__() runs the parent's setup."},
                {'brief': 'Write Shape with area() returning 0, and Square(Shape) with side and area() returning '
                          'side squared. Print both areas.',
                 'starter': '# define Shape and Square here\n',
                 'expected': '0\n16\n',
                 'hidden': 'print(Shape().area())\nprint(Square(4).area())\n',
                 'hint': 'class Shape:\n'
                         '    def area(self):\n'
                         '        return 0\n'
                         '\n'
                         '\n'
                         'class Square(Shape):\n'
                         '    def __init__(self, side):\n'
                         '        self.side = side\n'
                         '\n'
                         '    def area(self):\n'
                         '        return self.side * self.side',
                 'tip': "class Child(Parent): inherits; super().__init__() runs the parent's setup."},
                {'brief': 'Write Dog(Animal) so that isinstance(Dog(), Animal) is True, both classes empty apart '
                          'from pass.',
                 'starter': '# define Animal and Dog here\n',
                 'expected': 'True\nFalse\n',
                 'hidden': 'print(isinstance(Dog(), Animal))\nprint(isinstance(Animal(), Dog))\n',
                 'hint': 'class Animal:\n    pass\n\n\nclass Dog(Animal):\n    pass',
                 'tip': "class Child(Parent): inherits; super().__init__() runs the parent's setup."},
                {'brief': 'Write BankAccount(balance) with withdraw(n) refusing to go negative (returns False), '
                          'and SavingsAccount(BankAccount) with apply_interest(rate).',
                 'starter': '# define both classes here\n',
                 'expected': 'False\n150.0\n',
                 'hidden': 'a = SavingsAccount(100)\n'
                           'print(a.withdraw(500))\n'
                           'a.apply_interest(0.5)\n'
                           'print(a.balance)\n',
                 'hint': 'class BankAccount:\n'
                         '    def __init__(self, balance):\n'
                         '        self.balance = balance\n'
                         '\n'
                         '    def withdraw(self, n):\n'
                         '        if n > self.balance:\n'
                         '            return False\n'
                         '        self.balance = self.balance - n\n'
                         '        return True\n'
                         '\n'
                         '\n'
                         'class SavingsAccount(BankAccount):\n'
                         '    def apply_interest(self, rate):\n'
                         '        self.balance = self.balance * (1 + rate)',
                 'tip': "class Child(Parent): inherits; super().__init__() runs the parent's setup."},
                {'brief': 'Write class Robot with a staticmethod unit() returning "cm" and an instance attribute '
                          'height.',
                 'starter': '# define Robot here\n',
                 'expected': '120 cm\n',
                 'hidden': 'r = Robot(120)\nprint(r.height, Robot.unit())\n',
                 'hint': 'class Robot:\n'
                         '    def __init__(self, height):\n'
                         '        self.height = height\n'
                         '\n'
                         '    @staticmethod\n'
                         '    def unit():\n'
                         '        return "cm"',
                 'tip': "class Child(Parent): inherits; super().__init__() runs the parent's setup."}]},
    # add your own drills here
]
