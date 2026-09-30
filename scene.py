"""Paints the underwater scene: deep blue water, soft light rays from the
surface, rising bubbles, and sea life that swims past now and then.
Also a small Canvas to draw text on top of it.

Colours are (red, green, blue) tuples from 0 to 255.
"""

import math
import random

from rich.text import Text

WATER_TOP = (10, 70, 104)       # near the surface
WATER_MIDDLE = (7, 38, 76)
WATER_BOTTOM = (3, 12, 38)      # the deep
LIGHT = (140, 220, 230)         # sunlight through the water
BUBBLE = "#9fd9e6"
CREATURE = "#c9e8f2"
CREATURE_DIM = "#6fa3b8"

# Sea life, drawn as small pictures. Spaces are see-through.
DOLPHIN_LEFT = [
    "        __,",
    " __.--'`  `\\",
    "<_.-'__     )",
    "     `'--'`",
]
FISH_LEFT = ["<°))><"]
FISH_RIGHT = ["><((°>"]
JELLYFISH = [
    " .-.",
    "( ~ )",
    " ///",
]
TURTLE_RIGHT = [
    "   _,-._",
    "_/ (   ) \\_",
    "  `-...-'",
]


def mix(colour_a, colour_b, amount):
    """Blend two colours. amount 0 gives a, amount 1 gives b."""
    amount = max(0.0, min(1.0, amount))
    return tuple(
        round(colour_a[i] + (colour_b[i] - colour_a[i]) * amount) for i in range(3)
    )


def to_hex(colour):
    return "#{:02x}{:02x}{:02x}".format(*colour)


def from_hex(text):
    """Turn "#1a2b3c" back into (26, 43, 60)."""
    text = text.lstrip("#")
    return tuple(int(text[i:i + 2], 16) for i in (0, 2, 4))


# The shimmer: a band of ice light that sweeps across the lettering now and then.
# From the centre of the band outward: white ice, pale cyan, sea blue, then the
# letter's own colour again.
ICE_STOPS = [(0, (232, 251, 255)), (4, (150, 230, 255)), (8, (86, 190, 232)), (13, None)]
SHIMMER_SPEED = 3        # columns per tick
SHIMMER_GAP = 90         # columns of rest between two sweeps


def shimmer(canvas, tick):
    """Tint the letters that lie inside the sweeping band."""
    travel = canvas.width + SHIMMER_GAP
    band_x = (tick * SHIMMER_SPEED) % travel - SHIMMER_GAP // 2
    for y in range(canvas.height):
        for x in range(canvas.width):
            colour = canvas.fg[y][x]
            if colour is None or canvas.chars[y][x] == " ":
                continue
            # The band leans like a light ray, so use x plus a bit of y.
            distance = abs(x + y * 0.8 - band_x)
            if distance < ICE_STOPS[-1][0]:
                canvas.fg[y][x] = to_hex(ice_colour(distance, from_hex(colour)))


def ice_colour(distance, own_colour):
    """Blend between the ice stops for this distance from the band's centre."""
    for (start, start_colour), (end, end_colour) in zip(ICE_STOPS, ICE_STOPS[1:]):
        if distance <= end:
            end_colour = end_colour or own_colour
            return mix(start_colour, end_colour, (distance - start) / (end - start))
    return own_colour


class Canvas:
    """A grid of characters, each with its own text colour and background."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.chars = [[" "] * width for _ in range(height)]
        self.fg = [[None] * width for _ in range(height)]
        self.bg = [[WATER_BOTTOM] * width for _ in range(height)]
        self.bold = [[False] * width for _ in range(height)]

    def clear_row(self, y, up_to_x):
        """Remove drawings from a row so text on it reads cleanly."""
        if 0 <= y < self.height:
            for x in range(min(up_to_x, self.width)):
                self.chars[y][x] = " "
                self.fg[y][x] = None

    def clear_background(self):
        """Forget every background colour, so the terminal's own shows through."""
        for y in range(self.height):
            self.bg[y] = [None] * self.width

    def write(self, x, y, text, colour, bold=False):
        """Put text on the canvas. Anything past the edges is dropped."""
        if y < 0 or y >= self.height:
            return
        for offset, char in enumerate(text):
            column = x + offset
            if 0 <= column < self.width:
                self.chars[y][column] = char
                self.fg[y][column] = colour
                self.bold[y][column] = bold

    def draw_sprite(self, x, y, rows, colour):
        """Draw a small picture. Spaces in the picture leave the water visible."""
        for row_number, row in enumerate(rows):
            for offset, char in enumerate(row):
                if char != " ":
                    self.write(x + offset, y + row_number, char, colour)

    def to_text(self):
        """Turn the grid into a Rich Text, one style span per run of equal cells."""
        text = Text(no_wrap=True)
        for y in range(self.height):
            run_start = 0
            run_style = self.style_at(0, y)
            for x in range(1, self.width + 1):
                style = self.style_at(x, y) if x < self.width else None
                if style != run_style:
                    text.append("".join(self.chars[y][run_start:x]), style=run_style)
                    run_start = x
                    run_style = style
            if y < self.height - 1:
                text.append("\n")
        return text

    def style_at(self, x, y):
        """Rich style for one cell. A cell with no background stays see-through."""
        parts = []
        if self.bold[y][x]:
            parts.append("bold")
        if self.fg[y][x] is not None:
            parts.append(self.fg[y][x])
        if self.bg[y][x] is not None:
            parts.append(f"on {to_hex(self.bg[y][x])}")
        return " ".join(parts) or None


class OceanPainter:
    """Keeps track of bubbles and sea life, and paints the water onto a Canvas."""

    def __init__(self):
        self.width = 0
        self.height = 0
        self.bubbles = []     # list of [x, y, speed]
        self.creatures = []   # list of dicts, see new_creature

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.bubbles = []
        for _ in range((width * height) // 90):
            self.bubbles.append([random.randrange(max(width, 1)), random.randrange(max(height, 1)), random.choice([1, 1, 2])])
        self.creatures = [self.new_creature() for _ in range(3)]

    def new_creature(self):
        """Pick a creature and start it just outside one edge of the screen."""
        kind = random.choice(["dolphin", "fish", "fish", "jellyfish", "turtle"])
        if kind == "dolphin":
            rows, speed = DOLPHIN_LEFT, -2.0
        elif kind == "fish":
            going_right = random.random() < 0.5
            rows, speed = (FISH_RIGHT, 1.5) if going_right else (FISH_LEFT, -1.5)
        elif kind == "turtle":
            rows, speed = TURTLE_RIGHT, 0.7
        else:
            rows, speed = JELLYFISH, 0.0
        widest = max(len(row) for row in rows)
        start_x = -widest if speed > 0 else self.width
        if speed == 0:
            start_x = random.randrange(max(self.width - widest, 1))
        return {
            "rows": rows,
            "x": float(start_x),
            "y": random.randrange(max(self.height - len(rows) - 2, 1)) + 1,
            "speed": speed,
            "age": 0,
            "wait": random.randrange(4, 30),   # ticks before it appears
            "colour": CREATURE if kind == "dolphin" else CREATURE_DIM,
        }

    def advance(self):
        """Move everything one step. Called once per tick."""
        for bubble in self.bubbles:
            bubble[1] -= bubble[2]
            if bubble[1] < 0:
                bubble[1] = self.height - 1
                bubble[0] = random.randrange(max(self.width, 1))
        for index, creature in enumerate(self.creatures):
            if creature["wait"] > 0:
                creature["wait"] -= 1
                continue
            creature["age"] += 1
            creature["x"] += creature["speed"]
            # A jellyfish drifts upward slowly instead of sideways.
            if creature["speed"] == 0 and creature["age"] % 3 == 0:
                creature["y"] -= 1
            if self.is_gone(creature):
                self.creatures[index] = self.new_creature()

    def is_gone(self, creature):
        widest = max(len(row) for row in creature["rows"])
        return creature["x"] > self.width or creature["x"] < -widest or creature["y"] < -len(creature["rows"])

    def paint(self, canvas, tick):
        self.paint_water(canvas, tick)
        self.paint_bubbles(canvas)
        self.paint_creatures(canvas)

    def paint_water(self, canvas, tick):
        height = max(canvas.height - 1, 1)
        for y in range(canvas.height):
            depth = y / height
            if depth < 0.45:
                base = mix(WATER_TOP, WATER_MIDDLE, depth / 0.45)
            else:
                base = mix(WATER_MIDDLE, WATER_BOTTOM, (depth - 0.45) / 0.55)
            for x in range(canvas.width):
                canvas.bg[y][x] = mix(base, LIGHT, self.light_amount(x, y, canvas, tick))

    def light_amount(self, x, y, canvas, tick):
        """Soft diagonal rays of sunlight, strongest near the surface, swaying slowly."""
        depth = y / max(canvas.height - 1, 1)
        total = 0.0
        for ray in range(4):
            centre = canvas.width * (0.15 + 0.25 * ray) + y * 0.5 + 3 * math.sin(tick / 9 + ray)
            distance = (x - centre) / (5 + 3 * depth * 4)
            total += math.exp(-distance * distance)
        return 0.16 * total * (1 - depth) ** 1.5

    def paint_bubbles(self, canvas):
        for x, y, speed in self.bubbles:
            if 0 <= y < canvas.height and x < canvas.width:
                canvas.chars[int(y)][x] = "°" if speed > 1 else "·"
                canvas.fg[int(y)][x] = BUBBLE

    def paint_creatures(self, canvas):
        for creature in self.creatures:
            if creature["wait"] > 0:
                continue
            canvas.draw_sprite(int(creature["x"]), creature["y"], creature["rows"], creature["colour"])


# -------------------------------------------------------------- the xp bar

GLASS = (200, 235, 255)
WATER_DEEP = (12, 70, 130)


def draw_glow_bar(canvas, x, y, width, fill, accent_hex, tier=1):
    """A one-row XP bar with real colour: the filled part shades from deep
    blue to the accent, and every tier makes it brighter and whiter."""
    accent = from_hex(accent_hex)
    bright = mix(accent, GLASS, min(0.7, 0.12 * (tier - 1)))   # whiter with every tier
    lit = round(fill * width)
    for column in range(width):
        cell_x = x + column
        if cell_x >= canvas.width or y >= canvas.height:
            continue
        base = canvas.bg[y][cell_x] or WATER_DEEP
        if column < lit:
            canvas.bg[y][cell_x] = mix(WATER_DEEP, bright, 0.25 + 0.75 * column / max(width - 1, 1))
            canvas.chars[y][cell_x] = "▔" if tier >= 3 else " "
            canvas.fg[y][cell_x] = to_hex(mix(bright, GLASS, 0.5))
        else:
            canvas.bg[y][cell_x] = mix(base, GLASS, 0.08)
            canvas.chars[y][cell_x] = " "
            canvas.fg[y][cell_x] = None
    if tier >= 5 and lit > 0 and x + lit - 1 < canvas.width:
        canvas.chars[y][x + lit - 1] = "✦"    # a spark at the tip from tier five on
        canvas.fg[y][x + lit - 1] = to_hex(GLASS)


def draw_bar(canvas, x, y, width, fill, accent_hex, dim_hex):
    """A slim progress bar made of blocks, lit up to `fill` (0..1)."""
    lit = round(fill * width)
    canvas.write(x, y, "█" * lit, accent_hex)
    canvas.write(x + lit, y, "░" * (width - lit), dim_hex)


# ------------------------------------------------------------------ space

SPACE_TOP = (2, 3, 12)
SPACE_BOTTOM = (10, 8, 34)
SPACE_NEBULA = (110, 60, 160)
STAR_SOFT = (120, 130, 190)
STAR_BRIGHT = (235, 238, 255)
PLANET_COLOURS = [(180, 110, 70), (70, 130, 190), (150, 150, 120), (200, 120, 150)]


class SpacePainter:
    """Deep space: a nebula, breathing stars, a ringed planet with a moon, and a comet."""

    def __init__(self):
        self.width = 0
        self.height = 0
        self.stars = []      # [x, y, phase]
        self.planet = [0, 0, 2]       # x, y, radius of the big planet
        self.moon = [0.0, 0.0]        # the moon's angle and its radius of orbit
        self.comet = [0.0, 0.0]

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.stars = [[random.randrange(max(width, 1)), random.randrange(max(height, 1)), random.randrange(6)]
                      for _ in range((width * height) // 30)]
        self.planet = [int(width * 0.82), int(height * 0.70), 3]
        self.moon = [0.0, 9.0]
        self.comet = [float(width), float(random.randrange(2, max(height // 2, 3)))]

    def advance(self):
        """The comet drifts down and left, the moon circles the planet."""
        self.comet[0] -= 1.5
        self.comet[1] += 0.25
        if self.comet[0] < -6 or self.comet[1] > self.height:
            self.comet = [float(self.width), float(random.randrange(2, max(self.height // 2, 3)))]
        self.moon[0] += 0.08

    def paint(self, canvas, tick):
        self.paint_space(canvas)
        self.paint_stars(canvas, tick)
        self.paint_planet(canvas)
        self.paint_moon(canvas)
        self.paint_comet(canvas)

    def paint_space(self, canvas):
        height = max(canvas.height - 1, 1)
        for y in range(canvas.height):
            base = mix(SPACE_TOP, SPACE_BOTTOM, y / height)
            for x in range(canvas.width):
                # Two soft nebula clouds, violet low left and teal high right.
                dx = (x - canvas.width * 0.28) / (canvas.width * 0.22)
                dy = (y - canvas.height * 0.62) / (canvas.height * 0.25)
                colour = mix(base, SPACE_NEBULA, 0.22 * math.exp(-(dx * dx + dy * dy)))
                dx = (x - canvas.width * 0.75) / (canvas.width * 0.2)
                dy = (y - canvas.height * 0.2) / (canvas.height * 0.2)
                canvas.bg[y][x] = mix(colour, (40, 110, 130), 0.14 * math.exp(-(dx * dx + dy * dy)))

    def paint_stars(self, canvas, tick):
        for x, y, phase in self.stars:
            if y < canvas.height and x < canvas.width:
                glow = (math.sin((tick + phase) / 2.2) + 1) / 2
                canvas.chars[y][x] = "✦" if glow > 0.9 else ("•" if glow > 0.6 else "·")
                canvas.fg[y][x] = to_hex(mix(STAR_SOFT, STAR_BRIGHT, glow))

    def paint_planet(self, canvas):
        """A round planet lit from the upper left, with a thin ring through it.

        Cells are about twice as tall as wide, so x distances count half.
        """
        x0, y0, radius = self.planet
        colour = (196, 128, 84)
        for y in range(y0 - radius, y0 + radius + 1):
            for x in range(x0 - radius * 2 - 1, x0 + radius * 2 + 2):
                if not (0 <= y < canvas.height and 0 <= x < canvas.width):
                    continue
                dx = (x - x0) / 2
                dy = y - y0
                distance = math.sqrt(dx * dx + dy * dy)
                if distance <= radius + 0.4:
                    light = 1.0 - 0.45 * (dx / radius + dy / radius) / 2 - 0.35 * (distance / radius) ** 2
                    canvas.bg[y][x] = mix((8, 6, 20), colour, max(0.12, min(1.0, light)))
                    canvas.chars[y][x] = " "
                    canvas.fg[y][x] = None
        # The ring: a line of light across the middle, wider than the planet.
        ring_y = y0
        for x in range(x0 - radius * 2 - 6, x0 + radius * 2 + 7):
            if 0 <= x < canvas.width and 0 <= ring_y < canvas.height:
                inside = abs(x - x0) / 2 <= radius
                canvas.chars[ring_y][x] = "─" if not inside else "━"
                canvas.fg[ring_y][x] = to_hex((230, 214, 190)) if not inside else to_hex((120, 90, 70))

    def paint_moon(self, canvas):
        angle, orbit = self.moon
        x = int(self.planet[0] + math.cos(angle) * orbit * 2)
        y = int(self.planet[1] + math.sin(angle) * orbit * 0.6)
        if 0 <= x < canvas.width and 0 <= y < canvas.height:
            canvas.chars[y][x] = "●"
            canvas.fg[y][x] = to_hex((205, 205, 215))

    def paint_comet(self, canvas):
        x, y = int(self.comet[0]), int(self.comet[1])
        canvas.write(x, y, "☄", "#eef2ff")
        canvas.write(x + 2, y, "· ·  ·", "#8a96c8")
