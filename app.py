"""The Textual app: entry, map, overview, settings and level screens.

Visual choice: an underwater scene behind everything (see scene.py), one
accent colour you pick in settings (ice blue by default), and one two-frame
character, a star: ✧ waiting, ✦ lit when you pass, and a dim ✧ when you fail.
"""

import dataclasses
import os
import subprocess
import time

from rich.style import Style
from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.color import Color
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.containers import VerticalScroll
from textual.widgets import Button, Input, Static, TextArea
from textual.widgets.text_area import TextAreaTheme

import checker
import progress
import runner
import tutor
from levels import SPACE_WORLDS, WORLDS, all_drills, all_levels, next_drill, next_level, round_level
from scene import (Canvas, OceanPainter, SpacePainter, draw_bar, draw_glow_bar, from_hex, mix,
                   shimmer, to_hex, SPACE_BOTTOM, SPACE_TOP, WATER_BOTTOM, WATER_TOP)

# The colours you can pick in settings. The first one is the default.
ACCENTS = {
    "ice": "#8fe3ff",
    "aqua": "#5ee6c8",
    "pearl": "#eef6ff",
    "lavender": "#c9a7ff",
    "mint": "#b8f0c8",
    "coral": "#ff9a86",
    "rose": "#ff9ad0",
}
ACCENT = ACCENTS["ice"]   # the current accent, changed by set_accent()

DEEP = to_hex(WATER_TOP)       # app background, matches the top of the water
SEABED = to_hex(WATER_BOTTOM)  # bottom of the screen, behind the buttons
PANEL = "#071a33"        # editor and output boxes
LINE = "#1f4a6b"         # borders
TEXT = "#ffffff"         # main text, pure white for the sharpest read over video
SOFT = "#e6f2fa"         # secondary text
DIM = "#b5d2e3"          # quiet text
MUTED = "#8fb0c4"        # things not done yet
RED = "#ff9aa6"

STAR_WAIT = "○"          # a level not done yet
STAR_LIT = "✦"           # a level done
STAR_TEXT = {0: "☆☆☆", 1: "★☆☆", 2: "★★☆", 3: "★★★"}
MOST_LEVELS = max(len(world["levels"]) for world in WORLDS + SPACE_WORLDS)


def worlds_for(app):
    """The world list of the mode you are in: the sea's levels or space's drills."""
    return SPACE_WORLDS if app.mode == "space" else WORLDS

RUN_HELP = f"[bold {TEXT}]ctrl+enter[/] runs your code, and once it passes, [bold {TEXT}]ctrl+enter[/] again goes to the next one"

# Set by web/serve.py: leave the background see-through so the browser's
# real scene shows behind the game instead of the painted one.
TRANSPARENT = os.environ.get("PYLEVELS_TRANSPARENT") == "1"

# Where things sit on the map, in rows from the top.
MAP_FIRST_ROW = 5
MAP_ROW_GAP = 2


def set_accent(name):
    """Switch the accent colour for the whole game."""
    global ACCENT
    ACCENT = ACCENTS.get(name, ACCENTS["ice"])


def star_colour(count):
    """Colour of a level marker by stars earned: muted, then brighter and brighter."""
    if count == 0:
        return MUTED
    if count == 3:
        return ACCENT
    return to_hex(mix(from_hex(TEXT), from_hex(ACCENT), 0.35 * count))


# ------------------------------------------------------------------ buttons


class BarButton(Button):
    """A button that does not take keyboard focus away from the editor."""

    can_focus = False


class ButtonBar(Horizontal):
    """A row of buttons along the bottom. Each button's name is an action."""

    def __init__(self, buttons):
        super().__init__()
        self.buttons = buttons   # list of (name, label)

    def compose(self) -> ComposeResult:
        for name, label in self.buttons:
            yield BarButton(label, name=name, id=f"button-{name}")


# --------------------------------------------------------------- status bar


class StatusBar(Static):
    """One line at the top of a screen: XP, stars, streak, and the level clock."""

    def __init__(self):
        super().__init__()
        self.extra = ""   # text the level screen adds, like the timer

    def on_mount(self):
        self.set_interval(0.05, self.refresh_text)

    def refresh_text(self):
        """Redrawn often so the XP count-up and the clock stay live."""
        app = self.app
        stats = app.progress
        completed, count, earned, possible, seconds = totals(stats)
        # shown_xp creeps toward the real XP so the number visibly climbs.
        if app.shown_xp < stats["xp"]:
            app.shown_xp += 1
        xp_colour = ACCENT if app.shown_xp < stats["xp"] else TEXT
        self.update(
            f" [bold {ACCENT}]PyLevels[/] [{DIM}]· {app.mode}[/]   "
            f"[{DIM}]xp[/] [bold {xp_colour}]{app.shown_xp}[/]   "
            f"[{DIM}]stars[/] [bold {TEXT}]{earned}[/][{DIM}]/{possible}[/]   "
            f"[{DIM}]done[/] [bold {TEXT}]{completed}[/][{DIM}]/{count}[/]   "
            f"[{DIM}]streak[/] [bold {TEXT}]{stats['streak']}[/]"
            f"   {self.extra}"
            f"   [{DIM}]tutor[/] {tutor_markup(app)}"
        )


def tutor_markup(app):
    """A short coloured word for the tutor connection: checking, ready or off."""
    ok, message = app.tutor_status
    if ok is None:
        return f"[{DIM}]…[/]"
    if ok:
        return f"[{ACCENT}]✓[/]"
    return f"[{RED}]✗ off, see settings[/]"


# ------------------------------------------------------------------ the sea


class SceneView(Static):
    """Paints the water and refreshes it so bubbles rise and creatures swim."""

    def __init__(self):
        super().__init__()
        self.painter = OceanPainter()
        self.tick = 0

    def on_mount(self):
        self.pick_painter()
        self.set_interval(0.4, self.advance)
        self.set_interval(0.05, self.refresh_if_climbing)

    def pick_painter(self):
        """Water in the sea, stars in space."""
        self.painter = SpacePainter() if self.app.mode == "space" else OceanPainter()
        self.painter.resize(self.size.width, self.size.height)
        self.refresh()

    def on_resize(self):
        self.painter.resize(self.size.width, self.size.height)
        self.refresh()

    def advance(self):
        self.tick += 1
        if not TRANSPARENT:
            self.painter.advance()
        self.refresh()

    def refresh_if_climbing(self):
        """While XP is counting up, redraw fast so the tank fills smoothly."""
        if self.app.shown_xp < self.app.progress["xp"]:
            self.app.drop_tick += 1
            self.refresh()

    def render(self):
        canvas = Canvas(self.size.width, self.size.height)
        if TRANSPARENT:
            canvas.clear_background()
        else:
            self.painter.paint(canvas, self.tick)
        self.draw(canvas)
        shimmer(canvas, self.tick)
        return canvas.to_text()

    def draw(self, canvas):
        """Screens that draw on top of the water override this."""


def centred(canvas, y, text, colour, bold=False):
    """Write a line so that its middle sits in the middle of the canvas."""
    canvas.write((canvas.width - len(text)) // 2, y, text, colour, bold=bold)


# ------------------------------------------------------------------ totals


def stars_in(world, stars):
    """Stars earned in a world, and the most it could have."""
    earned = sum(stars.get(level["id"], 0) for level in world["levels"])
    return earned, 3 * len(world["levels"])


def totals(stats):
    """Levels completed, levels in total, stars earned, stars possible, seconds played."""
    everything = all_levels() + all_drills()
    completed = sum(1 for level in everything if stats["stars"].get(level["id"], 0) > 0)
    earned = sum(stars_in(world, stats["stars"])[0] for world in WORLDS + SPACE_WORLDS)
    possible = sum(stars_in(world, stats["stars"])[1] for world in WORLDS + SPACE_WORLDS)
    seconds = sum(stats["times"].values())
    return completed, len(everything), earned, possible, seconds


def next_up(stats):
    """The first sea level and the first space drill without stars, each or None."""
    level = None
    for candidate in all_levels():
        if stats["stars"].get(candidate["id"], 0) == 0:
            level = candidate
            break
    drill = None
    for candidate in all_drills():
        if stats["stars"].get(candidate["id"], 0) == 0:
            drill = candidate
            break
    return level, drill


def draw_xp_bar(canvas, x, y, width, app):
    """The XP bar with its caption above: name and tier, then the count.

    Uses the climbing shown_xp so it fills live. Every full bar is a tier up,
    and the bar glows brighter with every tier.
    """
    if TRANSPARENT:
        return   # the browser page draws its own glowing bar
    tank_number, fill = progress.tank_state(app.shown_xp)
    into = app.shown_xp % progress.XP_PER_TANK
    climbing = app.shown_xp < app.progress["xp"]
    name = f"{progress.tank_name(tank_number)} {tank_number}"
    count = f"{into}/{progress.XP_PER_TANK} xp" + (f"  +{app.progress['xp'] - app.shown_xp}" if climbing else "")
    canvas.clear_row(y - 1, canvas.width)
    canvas.write(x, y - 1, name, ACCENT, bold=True)
    canvas.write(x + width - len(count), y - 1, count, ACCENT if climbing else SOFT, bold=climbing)
    draw_glow_bar(canvas, x, y, width, fill, ACCENT, tank_number)


class LevelSceneView(SceneView):
    """The water behind a level, with the XP bar in the corner."""

    def draw(self, canvas):
        draw_corner_bar(canvas, self.app, buttons_width=120)


def draw_corner_bar(canvas, app, buttons_width):
    """The XP bar bottom right, in line with the buttons, when there is room."""
    width = 30
    x = canvas.width - width - 2
    y = canvas.height - 2
    if x > buttons_width + 2 and y > 5:
        draw_xp_bar(canvas, x, y, width, app)


# -------------------------------------------------------------- entry screen


class EntryView(SceneView):
    """The welcome screen: nothing but the sea, then the title fading in."""

    FADE_TICKS = 8   # about three seconds

    def draw(self, canvas):
        # Blend the text in from the water colour so the game builds up gently.
        amount = min(1.0, self.tick / self.FADE_TICKS)
        top = max(canvas.height // 2 - 3, 2)
        for y in range(top, top + 6):
            canvas.clear_row(y, canvas.width)
        centred(canvas, top, "P y L e v e l s", faded(ACCENT, amount, canvas, top), bold=True)
        centred(canvas, top + 1, "a quiet dive into Python", faded(SOFT, amount, canvas, top + 1))
        if amount >= 1.0:
            centred(canvas, top + 3, "enter  dive into the sea      L  launch into space", TEXT)
            level, drill = next_up(self.app.progress)
            if level is not None:
                centred(canvas, top + 5, f"next in the sea: {level['id']}  {level['title']}", SOFT)
            if drill is not None:
                centred(canvas, top + 6, f"next in space: {drill['id']}  {drill['title']}", SOFT)
            centred(canvas, top + 8, "O overview   S settings   Q quit", DIM)
            centred(canvas, top + 10, self.app.star, ACCENT)


def faded(colour_hex, amount, canvas, y):
    """A text colour blended toward the water behind it. amount 1 is fully visible."""
    water = canvas.bg[min(y, canvas.height - 1)][canvas.width // 2] or WATER_TOP
    return to_hex(mix(water, from_hex(colour_hex), amount))


class EntryScreen(Screen):
    """Shown on launch. Enter dives in, O overview, S settings, Q quits."""

    BINDINGS = [
        Binding("enter", "play", "dive in", show=False),
        Binding("l", "launch", "launch", show=False),
        Binding("o", "overview", "overview", show=False),
        Binding("s", "settings", "settings", show=False),
        Binding("q", "quit", "quit", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield EntryView()

    async def on_button_pressed(self, event):
        await self.run_action(event.button.name)

    def action_play(self):
        self.app.set_mode("sea")
        self.app.switch_screen(MapScreen())

    def action_launch(self):
        """Space: the same topics as drills, ten rounds each."""
        self.app.set_mode("space")
        self.app.switch_screen(MapScreen())

    def action_overview(self):
        self.app.push_screen(OverviewScreen())

    def action_settings(self):
        self.app.push_screen(SettingsScreen())


# ----------------------------------------------------------- overview screen


class OverviewView(SceneView):
    """Everything at a glance, and a cursor to jump straight into any level."""

    BAR_WIDTH = 30
    HEADER_ROWS = 9
    TEXT_WIDTH = 84    # the list never reaches further right than this

    def __init__(self):
        super().__init__()
        self.scroll = 0     # how many list rows are scrolled off the top
        self.cursor = 0     # which openable row is highlighted
        self.rows = []      # built on every draw, see build_rows
        self.targets = []   # indexes of rows that open a level or drill

    def draw(self, canvas):
        stats = self.app.progress
        completed, count, earned, possible, seconds = totals(stats)
        for y in range(1, self.HEADER_ROWS):
            canvas.clear_row(y, self.TEXT_WIDTH)

        canvas.write(2, 1, "your dive so far", ACCENT, bold=True)
        canvas.write(22, 1, f"{progress.format_time(seconds)} played   streak {stats['streak']}", DIM)
        self.summary_bar(canvas, 3, "levels", completed, count)
        self.summary_bar(canvas, 4, "stars", earned, possible)
        draw_xp_bar(canvas, 10, 6, self.BAR_WIDTH, self.app)
        level, drill = next_up(stats)
        canvas.write(2, 7, "next   " + (f"sea {level['id']} {level['title']}" if level else "sea done") +
                     "   ·   " + (f"space {drill['id']} {drill['title']}" if drill else "space done"), SOFT)

        self.build_rows(stats)
        visible = canvas.height - self.HEADER_ROWS - 4   # leave room for the buttons
        self.keep_cursor_visible(visible)
        for offset, row in enumerate(self.rows[self.scroll:self.scroll + visible]):
            y = self.HEADER_ROWS + offset
            index = self.scroll + offset
            canvas.clear_row(y, self.TEXT_WIDTH)
            chosen = self.targets and index == self.targets[self.cursor]
            canvas.write(1, y, "▸" if chosen else " ", ACCENT, bold=True)
            canvas.write(3, y, row["text"], ACCENT if chosen else row["colour"], bold=row["bold"] or bool(chosen))
            if row["bar"] is not None:
                draw_bar(canvas, 60, y, 12, row["bar"], ACCENT, "#2b5470")
        if self.scroll + visible < len(self.rows):
            canvas.write(2, self.HEADER_ROWS + visible, "↓ more", DIM)

    def summary_bar(self, canvas, y, label, value, most):
        canvas.write(2, y, f"{label:<7}", SOFT)
        draw_bar(canvas, 10, y, self.BAR_WIDTH, value / max(most, 1), ACCENT, "#2b5470")
        canvas.write(10 + self.BAR_WIDTH + 2, y, f"{value} / {most}", TEXT, bold=True)

    def build_rows(self, stats):
        """Rows are dicts: text, colour, bold, bar (0..1 or None), level (dict or None)."""
        self.rows = [self.heading("the sea   one new task per level")]
        self.rows += self.world_rows(WORLDS, stats)
        self.rows.append(self.heading("space   one concept, ten tasks"))
        self.rows += self.world_rows(SPACE_WORLDS, stats)
        self.targets = [index for index, row in enumerate(self.rows) if row["level"] is not None]
        self.cursor = max(0, min(self.cursor, len(self.targets) - 1))

    def heading(self, text):
        return {"text": text, "colour": ACCENT, "bold": True, "bar": None, "level": None}

    def world_rows(self, worlds, stats):
        rows = []
        for index, world in enumerate(worlds):
            earned, possible = stars_in(world, stats["stars"])
            done = sum(1 for level in world["levels"] if stats["stars"].get(level["id"], 0) > 0)
            complete = done == len(world["levels"])
            colour = ACCENT if earned == possible else (TEXT if done > 0 else MUTED)
            mark = "  ✓ all done" if complete else ""
            text = f"{index + 1}  {world['name']:<16} ★ {earned:>2}/{possible:<2}   {done}/{len(world['levels'])} done{mark}"
            rows.append({"text": text, "colour": colour, "bold": True, "bar": earned / max(possible, 1), "level": None})
            for level in world["levels"]:
                rows.append(self.level_row(level, stats))
            rows.append({"text": "", "colour": DIM, "bold": False, "bar": None, "level": None})
        return rows

    def level_row(self, level, stats):
        stars = stats["stars"].get(level["id"], 0)
        best = stats["times"].get(level["id"])
        time_text = progress.format_time(best) if best is not None else "  –  "
        mark = STAR_LIT + " done" if stars > 0 else STAR_WAIT
        text = f"   {level['id']:<5} {level['title']:<26} {STAR_TEXT[stars]}  {time_text:>5}  {mark}"
        return {"text": text, "colour": star_colour(stars) if stars > 0 else MUTED, "bold": stars > 0, "bar": None, "level": level}

    def keep_cursor_visible(self, visible):
        """Scroll so the highlighted row is on screen."""
        if not self.targets:
            return
        row = self.targets[self.cursor]
        if row < self.scroll + 1:
            self.scroll = max(0, row - 1)
        if row >= self.scroll + visible:
            self.scroll = row - visible + 1

    def move(self, step):
        if self.targets:
            self.cursor = (self.cursor + step) % len(self.targets)
        self.refresh()

    def scroll_by(self, lines):
        self.scroll = max(0, self.scroll + lines)
        # Bring the cursor along so enter still opens what you see.
        if self.targets:
            first_visible = next((i for i, row in enumerate(self.targets) if row >= self.scroll), len(self.targets) - 1)
            self.cursor = first_visible
        self.refresh()

    def chosen(self):
        """The level or drill under the cursor, or None."""
        if not self.targets:
            return None
        return self.rows[self.targets[self.cursor]]["level"]


class OverviewScreen(Screen):
    """Every level and drill. Move with the arrows, enter opens one. Esc goes back."""

    BINDINGS = [
        Binding("up", "move(-1)", "up", show=False),
        Binding("down", "move(1)", "down", show=False),
        Binding("pageup", "page_up", "page up", show=False),
        Binding("pagedown", "page_down", "page down", show=False),
        Binding("enter", "open", "open", show=False),
        Binding("escape", "back", "back", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield OverviewView()
        yield StatusBar()
        yield ButtonBar([("open", "▶ open  enter"), ("back", "back  esc")])

    def on_screen_resume(self):
        self.query_one(OverviewView).refresh()

    async def on_button_pressed(self, event):
        await self.run_action(event.button.name)

    def on_mouse_scroll_down(self, event):
        self.query_one(OverviewView).scroll_by(3)

    def on_mouse_scroll_up(self, event):
        self.query_one(OverviewView).scroll_by(-3)

    def action_move(self, step):
        self.query_one(OverviewView).move(step)

    def action_page_up(self):
        self.query_one(OverviewView).scroll_by(-10)

    def action_page_down(self):
        self.query_one(OverviewView).scroll_by(10)

    def action_open(self):
        chosen = self.query_one(OverviewView).chosen()
        if chosen is None:
            return
        # A drill lives in space, a level in the sea: the scene follows.
        self.app.set_mode("space" if "rounds" in chosen else "sea")
        self.app.push_screen(open_screen(chosen))

    def action_back(self):
        self.app.pop_screen()


# ----------------------------------------------------------- settings screen


class SettingsView(SceneView):
    """Three sections: the UI colour, the tutor connection, and your progress."""

    def __init__(self):
        super().__init__()
        self.names = list(ACCENTS)
        self.cursor = 0
        self.tutor_note = ""      # the last message from a sign-in or a check
        self.reset_armed = False  # reset asks you to press it twice

    def on_mount(self):
        current = self.app.progress.get("accent", "ice")
        self.cursor = self.names.index(current) if current in ACCENTS else 0

    def draw(self, canvas):
        for y in range(1, 26):
            canvas.clear_row(y, 90)
        canvas.write(2, 1, "settings", ACCENT, bold=True)

        canvas.write(2, 3, "ui colour", TEXT, bold=True)
        canvas.write(14, 3, "↑ ↓ choose   enter apply", DIM)
        for index, name in enumerate(self.names):
            y = 5 + index
            chosen = name == self.app.progress.get("accent", "ice")
            canvas.write(2, y, "▸" if index == self.cursor else " ", ACCENT, bold=True)
            canvas.write(4, y, "██████", ACCENTS[name])
            canvas.write(12, y, name, TEXT if index == self.cursor else SOFT, bold=index == self.cursor)
            if chosen:
                canvas.write(22, y, "✓ current", ACCENTS[name])

        y = 5 + len(self.names) + 1
        canvas.write(2, y, "tutor", TEXT, bold=True)
        ok, message = self.app.tutor_status
        colour = DIM if ok is None else (ACCENT if ok else RED)
        canvas.write(14, y, "checking…" if ok is None else message, colour)
        canvas.write(2, y + 1, "hints and talk use the claude command on this computer, on your own subscription", DIM)
        canvas.write(2, y + 2, "L sign in   C check again", DIM)
        if self.tutor_note:
            canvas.write(2, y + 3, self.tutor_note, SOFT)

        y = y + 5
        canvas.write(2, y, "progress", TEXT, bold=True)
        completed, count, earned, possible, seconds = totals(self.app.progress)
        canvas.write(14, y, f"{completed}/{count} done   {earned}/{possible} stars   {self.app.progress['xp']} xp", SOFT)
        if self.reset_armed:
            canvas.write(2, y + 1, "R again to wipe everything and start over, any other key to keep it", RED, bold=True)
        else:
            canvas.write(2, y + 1, "R start over (asks twice)", DIM)

    def move(self, step):
        self.cursor = (self.cursor + step) % len(self.names)
        self.reset_armed = False
        self.refresh()


class SettingsScreen(Screen):
    BINDINGS = [
        Binding("up", "move(-1)", "up", show=False),
        Binding("down", "move(1)", "down", show=False),
        Binding("enter", "apply", "apply", show=False),
        Binding("l", "login", "sign in", show=False),
        Binding("c", "check", "check", show=False),
        Binding("r", "reset", "start over", show=False),
        Binding("escape", "back", "back", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield SettingsView()
        yield StatusBar()
        yield ButtonBar([("login", "sign in  L"), ("reset", "start over  R"), ("back", "back  esc")])

    async def on_button_pressed(self, event):
        await self.run_action(event.button.name)

    def action_move(self, step):
        self.query_one(SettingsView).move(step)

    def action_apply(self):
        view = self.query_one(SettingsView)
        self.app.apply_accent(view.names[view.cursor])
        view.refresh()
        self.notify(f"colour set to {view.names[view.cursor]}", timeout=2)

    def action_login(self):
        """Sign in to Claude: in a terminal by pausing the game, in the browser in a new tab."""
        view = self.query_one(SettingsView)
        view.reset_armed = False
        if TRANSPARENT:
            view.tutor_note = tutor.start_login()
        else:
            try:
                with self.app.suspend():
                    subprocess.run(["claude", "auth", "login", "--claudeai"])
                view.tutor_note = "back from sign-in"
            except Exception as error:
                view.tutor_note = f"could not start the sign-in here: {error}"
        view.refresh()
        self.action_check()

    def action_check(self):
        self.query_one(SettingsView).reset_armed = False
        self.app.check_tutor()
        self.notify("checking the tutor connection", timeout=2)

    def action_reset(self):
        view = self.query_one(SettingsView)
        if not view.reset_armed:
            view.reset_armed = True
            view.refresh()
            return
        accent = self.app.progress.get("accent", "ice")
        self.app.progress = progress.empty_progress()
        self.app.progress["accent"] = accent
        progress.save(self.app.progress)
        self.app.shown_xp = 0
        view.reset_armed = False
        view.refresh()
        self.notify("progress wiped, fresh start", title="start over", timeout=4)

    def on_key(self, event):
        """Any key other than R disarms the reset."""
        if event.key != "r":
            self.query_one(SettingsView).reset_armed = False

    def action_back(self):
        self.app.pop_screen()


# --------------------------------------------------------------- map screen


class MapView(SceneView):
    """The world map drawn onto the water, with the XP tank in the corner."""

    def __init__(self):
        super().__init__()
        self.world_index = 0
        self.level_index = 0

    def draw(self, canvas):
        for y in (2, 3):
            canvas.clear_row(y, 70)
        tagline = "a slow drift through space, ten rounds a drill" if self.app.mode == "space" else "a quiet dive into Python"
        canvas.write(2, 2, tagline, SOFT)
        canvas.write(2 + len(tagline) + 2, 2, self.app.star, ACCENT)
        canvas.write(2, 3, f"↑ ↓ world   ← → level   enter or click to play   W switch     {STAR_LIT} done   {STAR_WAIT} not yet", DIM)

        for index, world in enumerate(worlds_for(self.app)):
            self.draw_row(canvas, index, world, MAP_FIRST_ROW + index * MAP_ROW_GAP)

        level, drill = next_up(self.app.progress)
        pick = drill if self.app.mode == "space" else level
        y = MAP_FIRST_ROW + len(worlds_for(self.app)) * MAP_ROW_GAP + 1
        canvas.clear_row(y, 70)
        if pick is not None:
            canvas.write(2, y, f"next up  {pick['id']}  {pick['title']}   ·   enter plays the highlighted one", SOFT)
        else:
            canvas.write(2, y, "everything here is done, well dived", ACCENT)

        draw_corner_bar(canvas, self.app, buttons_width=80)

    def draw_row(self, canvas, index, world, y):
        stars = self.app.progress["stars"]
        levels = world["levels"]
        earned, possible = stars_in(world, stars)
        done = sum(1 for level in levels if stars.get(level["id"], 0) > 0)
        name_colour = ACCENT if earned == possible else (TEXT if done > 0 else MUTED)

        canvas.clear_row(y, 24 + MOST_LEVELS * 2 + 26 + len(world["title"]) + 2)
        canvas.write(2, y, f"{index + 1:>2}", DIM)
        canvas.write(6, y, world["name"], name_colour, bold=True)

        x = 24
        for level_index, level in enumerate(levels):
            count = stars.get(level["id"], 0)
            symbol = STAR_LIT if count > 0 else STAR_WAIT
            if index == self.world_index and level_index == self.level_index:
                canvas.write(x - 1, y, f"[{symbol}]", ACCENT, bold=True)
            else:
                canvas.write(x, y, symbol, star_colour(count), bold=count == 3)
            x += 2

        x = 24 + MOST_LEVELS * 2 + 2
        score_colour = ACCENT if earned == possible else (TEXT if earned else MUTED)
        canvas.write(x, y, f"★ {earned:>2}/{possible:<2}", score_colour, bold=earned > 0)
        draw_bar(canvas, x + 10, y, 10, earned / max(possible, 1), ACCENT, "#2b5470")
        canvas.write(x + 22, y, world["title"], DIM if done > 0 else MUTED)

    def row_at(self, y):
        """Which world row is at this screen row, or None."""
        for index in range(len(worlds_for(self.app))):
            if y == MAP_FIRST_ROW + index * MAP_ROW_GAP:
                return index
        return None


class MapScreen(Screen):
    """The home of the game once you dive in: one row per world."""

    BINDINGS = [
        Binding("up", "move_world(-1)", "world up", show=False),
        Binding("down", "move_world(1)", "world down", show=False),
        Binding("left", "move_level(-1)", "level left", show=False),
        Binding("right", "move_level(1)", "level right", show=False),
        Binding("enter", "open_level", "play", show=False),
        Binding("o", "overview", "overview", show=False),
        Binding("w", "switch_mode", "switch", show=False),
        Binding("s", "settings", "settings", show=False),
        Binding("q", "quit", "quit", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield MapView()
        yield StatusBar()
        yield ButtonBar([
            ("open_level", "▶ play  enter"),
            ("switch_mode", "space ▸  W" if self.app.mode == "sea" else "sea ▸  W"),
            ("overview", "overview  O"),
            ("settings", "settings  S"),
            ("quit", "quit  Q"),
        ])

    def on_mount(self):
        self.jump_to_first_unfinished()

    def on_screen_resume(self):
        """Called when we come back from a level: redraw with the new stars."""
        self.query_one(MapView).refresh()

    # Textual runs actions asynchronously, so this handler waits for it to finish.
    async def on_button_pressed(self, event):
        await self.run_action(event.button.name)

    def action_switch_mode(self):
        """Sea to space or back. The map, scene and buttons are rebuilt."""
        self.app.set_mode("space" if self.app.mode == "sea" else "sea")
        self.app.switch_screen(MapScreen())

    def jump_to_first_unfinished(self):
        """Put the cursor on the first level that has no stars yet."""
        view = self.query_one(MapView)
        stars = self.app.progress["stars"]
        for world_index, world in enumerate(worlds_for(self.app)):
            for level_index, level in enumerate(world["levels"]):
                if stars.get(level["id"], 0) == 0:
                    view.world_index = world_index
                    view.level_index = level_index
                    view.refresh()
                    return

    def action_move_world(self, step):
        view = self.query_one(MapView)
        worlds = worlds_for(self.app)
        view.world_index = (view.world_index + step) % len(worlds)
        view.level_index = min(view.level_index, len(worlds[view.world_index]["levels"]) - 1)
        view.refresh()

    def action_move_level(self, step):
        view = self.query_one(MapView)
        count = len(worlds_for(self.app)[view.world_index]["levels"])
        view.level_index = (view.level_index + step) % count
        view.refresh()

    def action_open_level(self):
        view = self.query_one(MapView)
        chosen = worlds_for(self.app)[view.world_index]["levels"][view.level_index]
        self.app.push_screen(open_screen(chosen))

    def action_overview(self):
        self.app.push_screen(OverviewScreen())

    def action_settings(self):
        self.app.push_screen(SettingsScreen())

    def on_click(self, event):
        """Clicking a row opens that world's first unfinished level."""
        view = self.query_one(MapView)
        if event.widget is not view:
            return
        index = view.row_at(event.y)
        if index is None:
            return
        view.world_index = index
        view.level_index = self.first_unfinished_in(worlds_for(self.app)[index])
        view.refresh()
        self.action_open_level()

    def first_unfinished_in(self, world):
        stars = self.app.progress["stars"]
        for index, level in enumerate(world["levels"]):
            if stars.get(level["id"], 0) == 0:
                return index
        return 0


# ------------------------------------------------------------- level screen


def open_screen(chosen):
    """A level screen for a sea level, or for round one of a space drill."""
    if "rounds" in chosen:
        return LevelScreen(round_level(chosen, 0), drill=chosen)
    return LevelScreen(chosen)


class LevelScreen(Screen):
    """Brief on top, editor in the middle, output and buttons at the bottom."""

    # priority=True makes these win over the editor's own key handling.
    # Every action has a ctrl key and an F key. In the browser the page turns
    # the ctrl keys into the F keys, because terminals swallow some ctrl keys.
    BINDINGS = [
        Binding("ctrl+enter", "run_or_next", "run", priority=True, show=False),
        Binding("f5", "run_or_next", "run", priority=True, show=False),
        Binding("ctrl+r", "run", "run", priority=True, show=False),
        Binding("ctrl+h", "hint", "hint", priority=True, show=False),
        Binding("f1", "hint", "hint", priority=True, show=False),
        Binding("ctrl+g", "answer", "answer", priority=True, show=False),
        Binding("f2", "answer", "answer", priority=True, show=False),
        Binding("ctrl+t", "talk", "talk", priority=True, show=False),
        Binding("f3", "talk", "talk", priority=True, show=False),
        Binding("ctrl+y", "copy_output", "copy output", priority=True, show=False),
        Binding("f4", "copy_output", "copy output", priority=True, show=False),
        Binding("ctrl+n", "next_level", "next", priority=True, show=False),
        Binding("f6", "next_level", "next", priority=True, show=False),
        Binding("ctrl+l", "login", "log in", priority=True, show=False),
        Binding("escape", "back", "map", priority=True, show=False),
    ]

    # Log in has no button: the tutor's message says ctrl+L when it is needed.
    BUTTONS = [
        ("run_or_next", "▶ run  ctrl+enter"),
        ("hint", "hint  ctrl+H"),
        ("talk", "talk  ctrl+T"),
        ("answer", "answer  ctrl+G"),
        ("next_level", "next ▸  ctrl+enter"),
        ("back", "back  esc"),
    ]

    def __init__(self, level, drill=None):
        super().__init__()
        self.level = level
        self.drill = drill          # the space drill this level is a round of, or None
        self.round = 0              # which round of the drill, from 0
        self.run_count = 0
        self.used_hint = False
        self.passed = False
        self.last_output = ""     # stdout and stderr from the last run
        self.output_text = ""     # plain text in the output panel, for copying
        self.hints_given = []     # what the tutor already said
        self.chat_history = []    # (who, text) pairs from the talk screen
        self.last_verdict = ""    # the checker's line from the last run
        self.asking = False       # True while a hint request is running
        self.opened_at = time.monotonic()
        self.started_at = None    # set at the first keystroke
        self.finished_in = None   # seconds, once passed
        self.passed_code = None   # the code that passed, so ctrl+enter knows to move on

    def compose(self) -> ComposeResult:
        yield LevelSceneView()
        yield StatusBar()
        yield Static(id="level-title")
        yield Static(self.level["brief"], id="level-brief")
        yield TextArea.code_editor(self.level["starter"], language="python", id="editor")
        with Vertical(id="output-box"):
            yield Static(id="output-title")
            yield Static(id="output")
        yield ButtonBar(self.BUTTONS)

    def on_mount(self):
        editor = self.query_one("#editor", TextArea)
        editor.register_theme(night_theme())
        editor.theme = "night"
        editor.focus()
        self.update_title()
        self.set_star(STAR_WAIT, DIM, "")
        if self.drill is not None and self.drill.get("lesson"):
            # A drill opens with its lesson, then each round shows its tip.
            self.show_output(f"[bold {ACCENT}]the idea[/]  {escape_markup(self.drill['lesson'])}\n\n[{DIM}]{RUN_HELP}[/]", self.drill["lesson"])
        else:
            self.show_output(f"[{DIM}]{RUN_HELP}[/]", "")
        self.show_tip()
        self.query_one("#button-next_level", Button).disabled = True
        self.set_interval(0.5, self.update_clock)

    async def on_button_pressed(self, event):
        await self.run_action(event.button.name)
        if event.button.name != "back":
            self.query_one("#editor", TextArea).focus()

    def on_text_area_changed(self, event):
        """The clock starts the moment you type something."""
        if self.started_at is None and not self.passed:
            self.started_at = time.monotonic()

    def seconds_so_far(self):
        if self.finished_in is not None:
            return self.finished_in
        if self.started_at is None:
            return 0
        return int(time.monotonic() - self.started_at)

    def update_clock(self):
        bar = self.query_one(StatusBar)
        clock = progress.format_time(self.seconds_so_far())
        if self.finished_in is not None:
            bar.extra = f"[{DIM}]time[/] [bold {ACCENT}]{clock}[/]   [bold {ACCENT}]✓ completed[/]"
        elif self.started_at is None:
            bar.extra = f"[{DIM}]time starts when you type[/]"
        else:
            bar.extra = f"[{DIM}]time[/] [bold {TEXT}]{clock}[/]"

    def show_tip(self):
        """The round's one-line tip goes under the brief."""
        tip = self.level.get("tip", "")
        text = self.level["brief"] + (f"\n[{DIM}]tip  {escape_markup(tip)}[/]" if tip else "")
        self.query_one("#level-brief", Static).update(text)

    def update_title(self):
        stars = progress.stars_for(self.app.progress, self.level["id"])
        best = progress.best_time(self.app.progress, self.level["id"])
        done = f"   [bold {ACCENT}]✓ completed[/]   [{DIM}]best {progress.format_time(best)}[/]" if best is not None else ""
        self.query_one("#level-title", Static).update(
            f" [{DIM}]{self.level['id']}[/]  [bold {ACCENT}]{self.level['title']}[/]"
            f"   [{ACCENT}]{STAR_TEXT[stars]}[/]{done}{self.round_markup()}"
        )

    def round_markup(self):
        """For a drill: round 3 of 10 and a row of dots that fill as rounds pass."""
        if self.drill is None:
            return ""
        total = len(self.drill["rounds"])
        dots = STAR_LIT * self.round + STAR_WAIT * (total - self.round)
        return (f"   [{DIM}]round[/] [bold {TEXT}]{self.round + 1}[/][{DIM}] of {total}[/]  [{ACCENT}]{dots}[/]"
                f"   [{DIM}]{self.drill['brief']}[/]")

    def set_star(self, face, colour, message):
        self.app.star = face
        self.query_one("#output-title", Static).update(
            f" [bold {colour}]{face}[/]  [{DIM}]output[/]   {message}"
        )

    def show_output(self, markup, plain):
        """Show styled text in the output panel and remember the plain version."""
        self.output_text = plain
        self.query_one("#output", Static).update(markup)

    # ------------------------------------------------------------- actions

    def action_run_or_next(self):
        """One key for the whole flow: run, and once the code has passed, go on."""
        code = self.query_one("#editor", TextArea).text
        if self.passed and code == self.passed_code:
            self.action_next_level()
        else:
            self.action_run()

    def action_run(self):
        self.run_count += 1
        code = self.query_one("#editor", TextArea).text
        result = runner.run_code(code, self.level["hidden"])

        if result["timed_out"]:
            self.show_fail(f"your code was still running after {runner.TIMEOUT_SECONDS} seconds, so it was stopped. Look for a loop that never ends. (There is no time limit on you, only on the code.)", "")
            return

        self.last_output = result["stdout"] + result["stderr"]
        outcome = checker.judge(result, self.level, code)
        self.last_verdict = "passed" if outcome["passed"] else outcome["diff"]
        if outcome["passed"]:
            self.show_pass(result["stdout"])
        else:
            self.show_fail(outcome["diff"], self.last_output)

    def action_hint(self):
        """Ask the tutor for a nudge. Runs in the background so the UI stays alive."""
        if self.asking:
            return
        self.used_hint = True
        self.asking = True
        self.set_star(STAR_WAIT, ACCENT, f"[{ACCENT}]the tutor is thinking[/]")
        code = self.query_one("#editor", TextArea).text
        self.fetch_hint(code)

    # Textual's @work runs this function in a separate thread.
    @work(thread=True)
    def fetch_hint(self, code):
        text = tutor.ask_for_hint(self.level, code, self.last_output, self.last_verdict, self.hints_given)
        # Widgets may only be touched from the main thread, so hand the result over.
        self.app.call_from_thread(self.show_hint, text)

    def show_hint(self, text):
        self.asking = False
        self.hints_given.append(text)
        number = len(self.hints_given)
        self.set_star(STAR_WAIT, ACCENT, f"[{ACCENT}]hint {number}[/]   [{DIM}]ask again for more[/]")
        self.show_output(escape_markup(text), text)

    def action_talk(self):
        """Open the talk screen: a back-and-forth with the tutor about this level."""
        self.used_hint = True
        self.app.push_screen(ChatScreen(self))

    def action_answer(self):
        """Show the level's reference answer. Costs a star, like a hint."""
        self.used_hint = True
        self.set_star(STAR_WAIT, ACCENT, f"[{ACCENT}]answer[/]")
        self.show_output(escape_markup(self.level["hint"]), self.level["hint"])

    def action_copy_output(self):
        """Put the output panel's text on the clipboard."""
        copy_to_clipboard(self.app, self.output_text)
        self.notify("output copied to the clipboard", timeout=2)

    def action_login(self):
        """Sign in to Claude: the browser version opens a sign-in tab, a
        terminal pauses the game and runs the sign-in in place."""
        if TRANSPARENT:
            note = tutor.start_login()
            self.set_star(STAR_WAIT, ACCENT, f"[{ACCENT}]sign-in[/]")
            self.show_output(f"[{SOFT}]{escape_markup(note)}[/]\n\n[{DIM}]then ask for a hint again[/]", note)
            self.app.check_tutor()
            return
        try:
            with self.app.suspend():
                subprocess.run(["claude", "auth", "login", "--claudeai"])
        except Exception as error:
            self.show_output(
                f"[{RED}]could not start the sign-in here: {escape_markup(str(error))}[/]\n\n"
                f"[{DIM}]run  claude auth login  in any terminal instead[/]",
                f"could not start the sign-in here: {error}",
            )
            return
        self.app.check_tutor()
        self.set_star(STAR_WAIT, ACCENT, f"[{ACCENT}]back from sign-in[/]")
        self.show_output(f"[{DIM}]ask the tutor for a hint[/]", "")

    def action_next_level(self):
        if not self.passed:
            return
        if self.drill is not None:
            following = next_drill(self.drill["id"])
        else:
            following = next_level(self.level["id"])
        if following is None:
            self.notify("that was the last one, well done", title="all done", timeout=5)
            return
        self.app.switch_screen(open_screen(following))

    def action_back(self):
        self.app.pop_screen()

    # ------------------------------------------------------- pass and fail

    def show_pass(self, stdout):
        if self.drill is not None and self.round + 1 < len(self.drill["rounds"]):
            self.next_round(stdout)
            return
        extra_runs = self.run_count
        if self.drill is not None:
            # In a drill, one run per round is the minimum, only the extra ones count.
            extra_runs = self.run_count - len(self.drill["rounds"]) + 1
        stars = progress.calculate_stars(self.used_hint, extra_runs)
        # If you never typed, the time counts from when the level opened.
        started = self.started_at if self.started_at is not None else self.opened_at
        self.finished_in = int(time.monotonic() - started)
        gained = progress.record_pass(self.app.progress, self.level["id"], stars, self.finished_in)
        self.passed = True
        self.passed_code = self.query_one("#editor", TextArea).text
        self.update_title()
        self.update_clock()

        self.show_output(escape_markup(stdout.rstrip("\n")), stdout.rstrip("\n"))
        self.set_star(STAR_LIT, ACCENT, f"[bold {ACCENT}]passed[/]  {STAR_TEXT[stars]}")
        self.flash_output()
        self.count_up_xp(gained)
        self.light_next_button()
        clock = progress.format_time(self.finished_in)
        self.notify(
            (f"{STAR_TEXT[stars]}   +{gained} xp   in {clock}" if gained
             else f"{STAR_TEXT[stars]}   passed again, no new xp   in {clock}"),
            title=f"level {self.level['id']} complete",
            timeout=5,
        )

    def next_round(self, stdout):
        """A drill round passed: load the next round's values into the editor."""
        self.round += 1
        self.level = round_level(self.drill, self.round)
        self.show_output(escape_markup(stdout.rstrip("\n")), stdout.rstrip("\n"))
        self.set_star(STAR_LIT, ACCENT, f"[bold {ACCENT}]round {self.round} done[/]   [{DIM}]same idea, new task, read the brief[/]")
        self.flash_output()
        self.update_title()
        self.show_tip()
        editor = self.query_one("#editor", TextArea)
        editor.text = self.level["starter"]
        editor.focus()
        self.last_output = ""
        self.last_verdict = ""

    def show_fail(self, diff, output):
        plain = diff + "\n\n" + output.rstrip()
        self.show_output(
            f"[bold {RED}]{escape_markup(diff)}[/]\n\n[{SOFT}]{escape_markup(output.rstrip())}[/]",
            plain,
        )
        self.set_star(STAR_WAIT, RED, f"[{RED}]not yet[/]   [{DIM}]read the line above, then try again[/]")
        self.shake_output()
        box = self.query_one("#output-box")
        box.styles.border = ("round", RED)
        self.set_timer(0.8, self.calm_border)

    def calm_border(self):
        self.query_one("#output-box").styles.border = ("round", LINE)

    def light_next_button(self):
        """Enable the next button and make it pulse a few times."""
        button = self.query_one("#button-next_level", Button)
        button.disabled = False
        button.add_class("glow")
        self.pulses_left = 6
        self.pulse_timer = self.set_interval(0.35, self.pulse_next_button)

    def pulse_next_button(self):
        button = self.query_one("#button-next_level", Button)
        if self.pulses_left <= 0:
            self.pulse_timer.stop()
            button.styles.opacity = 1.0
            return
        self.pulses_left -= 1
        button.styles.animate("opacity", value=0.55 if self.pulses_left % 2 else 1.0, duration=0.3)

    def flash_output(self):
        """Light the output box up in the accent colour, then let it fade back.

        The glow colour is opaque, mixed from the panel and the accent, so it
        looks the same in a terminal and in the browser's transparent mode.
        """
        box = self.query_one("#output-box")
        glow = to_hex(mix(from_hex(PANEL), from_hex(ACCENT), 0.45))
        box.styles.background = Color.parse(glow)
        box.styles.border = ("round", ACCENT)
        box.styles.animate("background", value=Color.parse(PANEL), duration=1.6, easing="out_cubic")
        self.set_timer(1.6, self.calm_border)

    def shake_output(self):
        """Nudge the output box left and right a few times."""
        self.shake_steps = [2, -2, 1, -1, 0]
        self.shake_timer = self.set_interval(0.05, self.shake_step)

    def shake_step(self):
        """One step of the shake: move the box, stop when the steps run out."""
        if not self.shake_steps:
            self.shake_timer.stop()
            return
        box = self.query_one("#output-box")
        box.styles.offset = (self.shake_steps.pop(0), 0)

    def count_up_xp(self, gained):
        """Show the XP ticking up one point at a time in the output title."""
        if gained == 0:
            self.set_star(STAR_LIT, ACCENT, f"[bold {ACCENT}]passed again[/]  no new xp")
            return
        self.xp_shown = 0
        self.xp_target = gained
        self.xp_timer = self.set_interval(0.04, self.xp_tick)

    def xp_tick(self):
        """Add one point to the shown XP, stop once the target is reached."""
        if self.xp_shown >= self.xp_target:
            self.xp_timer.stop()
            return
        self.xp_shown += 1
        stars = progress.stars_for(self.app.progress, self.level["id"])
        done = self.xp_shown == self.xp_target
        self.set_star(
            STAR_LIT,
            ACCENT,
            f"[bold {ACCENT}]passed[/]  {STAR_TEXT[stars]}  [bold {ACCENT}]+{self.xp_shown} xp[/]"
            + (f"   [{DIM}]ctrl+enter for the next one[/]" if done else ""),
        )


# -------------------------------------------------------------- talk screen


class ChatScreen(Screen):
    """Talk with the tutor about the level you came from, as long as you like."""

    BINDINGS = [
        Binding("escape", "back", "back", priority=True, show=False),
    ]

    WELCOME = ("tutor", "Ask me anything about this level, or about a Python idea you have not "
                        "seen before. I can see your code and your last run.")

    def __init__(self, level_screen):
        super().__init__()
        self.level_screen = level_screen
        self.waiting = False

    def compose(self) -> ComposeResult:
        yield SceneView()
        yield StatusBar()
        yield Static(id="chat-title")
        yield VerticalScroll(id="chat-log")
        yield Input(placeholder="type a question and press enter", id="question")
        yield ButtonBar([("send", "send  enter"), ("back", "back to the level  esc")])

    def on_mount(self):
        level = self.level_screen.level
        self.query_one("#chat-title", Static).update(
            f" [{DIM}]talk about[/]  [bold {ACCENT}]{level['id']}  {level['title']}[/]"
        )
        history = self.level_screen.chat_history
        for who, text in [self.WELCOME] + history:
            self.add_message(who, text)
        self.query_one("#question", Input).focus()

    async def on_button_pressed(self, event):
        await self.run_action(event.button.name)

    def on_input_submitted(self, event):
        self.action_send()

    def action_send(self):
        box = self.query_one("#question", Input)
        question = box.value.strip()
        if not question or self.waiting:
            return
        box.value = ""
        self.waiting = True
        self.level_screen.chat_history.append(("you", question))
        self.add_message("you", question)
        self.add_message("tutor", "…", thinking=True)
        self.fetch_reply(question)

    # Textual's @work runs this in a separate thread so typing stays smooth.
    @work(thread=True)
    def fetch_reply(self, question):
        screen = self.level_screen
        code = screen.query_one("#editor", TextArea).text
        history = screen.chat_history[:-1]   # everything before this question
        reply = tutor.chat(screen.level, code, screen.last_output, screen.last_verdict, history, question)
        self.app.call_from_thread(self.show_reply, reply)

    def show_reply(self, reply):
        self.waiting = False
        self.level_screen.chat_history.append(("tutor", reply))
        self.query_one("#thinking").remove()
        self.add_message("tutor", reply)

    def add_message(self, who, text, thinking=False):
        """Put one message in the log and scroll to it."""
        label = "you" if who == "you" else "tutor"
        colour = ACCENT if who == "you" else SOFT
        message = Static(
            f"[bold {colour}]{label}[/]  {escape_markup(text)}",
            classes="chat-you" if who == "you" else "chat-tutor",
            id="thinking" if thinking else None,
        )
        log = self.query_one("#chat-log", VerticalScroll)
        log.mount(message)
        log.scroll_end(animate=False)

    def action_back(self):
        self.app.pop_screen()


def copy_to_clipboard(app, text):
    """Copy through the terminal, and through pbcopy on a Mac, which is more reliable."""
    app.copy_to_clipboard(text)
    try:
        subprocess.run(["pbcopy"], input=text, text=True, check=False)
    except FileNotFoundError:
        pass


def night_theme():
    """The editor's colour theme: dracula's syntax colours on our deep-water panel."""
    theme = dataclasses.replace(TextAreaTheme.get_builtin_theme("dracula"), name="night")
    theme.base_style = Style(color=TEXT, bgcolor=PANEL)
    theme.gutter_style = Style(color=DIM, bgcolor=PANEL)
    theme.cursor_line_style = Style(bgcolor="#0b2445")
    theme.cursor_line_gutter_style = Style(color=TEXT, bgcolor="#0b2445")
    return theme


def escape_markup(text):
    """Stop square brackets in program output from being read as colour tags."""
    return text.replace("[", "\\[")


# ---------------------------------------------------------------------- app


class PyLevelsApp(App):
    TITLE = "PyLevels"
    ENABLE_COMMAND_PALETTE = False

    # $accent is a CSS variable, see get_css_variables, so settings can change it.
    CSS = f"""
    Screen {{
        background: $deep;
        color: {TEXT};
        layers: scene default;
        overflow: hidden hidden;
    }}
    SceneView, LevelSceneView, MapView, EntryView, OverviewView, SettingsView {{
        layer: scene;
        position: absolute;
        offset: 0 0;
        width: 100%;
        height: 100%;
    }}

    StatusBar {{
        dock: top;
        height: 1;
        width: 100%;
        background: $deep;
    }}

    ButtonBar {{
        dock: bottom;
        height: 3;
        width: auto;
        padding: 0 0 0 2;
        background: $seabed;
    }}
    BarButton {{
        height: 3;
        min-width: 10;
        margin: 0 1 0 0;
        padding: 0 1;
        border: round #dcecf4 30%;
        background: #dcecf4 8%;
        color: {TEXT};
        text-style: none;
        content-align: center middle;
    }}
    BarButton:hover {{
        border: round $accent 80%;
        color: $accent;
        background: #dcecf4 16%;
    }}
    BarButton.-active {{
        background: $accent 35%;
        color: {TEXT};
        border: round $accent;
    }}
    BarButton:disabled {{
        color: #dcecf4 30%;
        border: round #dcecf4 12%;
        background: #dcecf4 3%;
    }}
    BarButton.glow {{
        color: $accent;
        border: round $accent 90%;
        background: $accent 18%;
        text-style: bold;
    }}

    ToastRack {{
        dock: top;
        align: right top;
        margin: 2 3 0 0;
    }}
    Toast {{
        background: {PANEL};
        border: round $accent;
        color: {TEXT};
        padding: 1 2;
    }}
    Toast .toast--title {{
        color: $accent;
        text-style: bold;
    }}

    #chat-title {{
        height: 2;
        width: auto;
        padding: 1 1 0 1;
        background: $deep;
    }}
    #chat-log {{
        height: 1fr;
        margin: 0 3;
        padding: 1 2;
        border: round {LINE};
        background: {PANEL};
    }}
    .chat-you, .chat-tutor {{
        margin-bottom: 1;
    }}
    .chat-you {{
        color: {TEXT};
    }}
    #question {{
        margin: 1 3 1 3;
        border: round {LINE};
        background: {PANEL};
        color: {TEXT};
    }}
    #question:focus {{
        border: round $accent;
    }}

    #level-title {{
        height: 2;
        width: auto;
        padding: 1 1 0 1;
        background: $deep;
    }}
    #level-brief {{
        height: auto;
        width: auto;
        padding: 0 2 1 2;
        background: $deep;
    }}
    #editor {{
        height: 1fr;
        margin: 0 3;
        border: round {LINE};
        background: {PANEL};
    }}
    #editor:focus {{
        border: round $accent;
    }}
    #output-box {{
        height: 10;
        margin: 1 3 1 3;
        border: round {LINE};
        background: {PANEL};
    }}
    #output-title {{
        height: 1;
    }}
    #output {{
        padding: 0 2;
        height: 1fr;
        overflow-y: auto;
    }}
    """

    def __init__(self):
        # ansi_color=True lets "ansi_default" mean "no colour, let the terminal decide".
        super().__init__(ansi_color=TRANSPARENT)
        self.progress = progress.load()
        set_accent(self.progress.get("accent", "ice"))
        self.shown_xp = self.progress["xp"]   # what the status bar shows, climbs on a pass
        self.drop_tick = 0                    # drives the drops flying into the tank
        self.mode = "sea"                     # "sea" for levels, "space" for drills
        self.tutor_status = (None, "checking")  # (ok, message) from tutor.status()
        self.star = STAR_WAIT

    def get_css_variables(self):
        """Adds $accent, $deep and $seabed to the CSS: the colour you picked,
        and the top and bottom of the scene, water in the sea, dark in space."""
        variables = super().get_css_variables()
        variables["accent"] = ACCENT
        in_space = getattr(self, "mode", "sea") == "space"
        variables["deep"] = to_hex(SPACE_TOP) if in_space else DEEP
        variables["seabed"] = to_hex(SPACE_BOTTOM) if in_space else SEABED
        return variables

    def set_mode(self, mode):
        """Sea or space. Restyles the backgrounds to match."""
        self.mode = mode
        self.refresh_css()

    def apply_accent(self, name):
        """Change the accent everywhere and remember it."""
        set_accent(name)
        self.progress["accent"] = name
        progress.save(self.progress)
        self.refresh_css()

    def on_mount(self):
        if TRANSPARENT:
            self.make_transparent()
        self.push_screen(EntryScreen())
        self.check_tutor()

    # Runs in a thread: the claude command can take a second or two.
    @work(thread=True)
    def check_tutor(self):
        result = tutor.status()
        self.call_from_thread(self.set_tutor_status, result)

    def set_tutor_status(self, result):
        self.tutor_status = result
        for view in self.screen.query(SettingsView):
            view.refresh()

    def make_transparent(self):
        """Extra CSS for the browser: screen, titles and bars without a background."""
        self.stylesheet.add_source(
            """
            Screen { background: ansi_default; }
            #level-title, #level-brief, #chat-title, ButtonBar, StatusBar { background: ansi_default; }
            BarButton, BarButton:hover, BarButton:disabled, BarButton.glow { background: ansi_default; }
            """
        )
        self.stylesheet.reparse()
        self.stylesheet.update(self)
