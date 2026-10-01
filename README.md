# PyLevels

A calm little desktop app (Mac and Windows) that teaches Python by typing real code, one level at a
time, with underwater (and outer space) scenery behind it.

- **Sea**: nine worlds of eight levels each, from `print` to classes and
  files. Every level is a new small task.
- **Space**: the same nine topics as drills. One idea shown ten different
  ways, so you learn to spot it in any shape.
- **Theory**: short flashcards for every world, written in plain words.
- **Tutor**: ask for a hint or talk about your code. The tutor sees your code
  and your last run, and nudges you without giving the answer away.

You pass a level when your program prints exactly what the level expects.
Python runs inside the app, so nothing on your computer is touched.

## Install

**Step-by-step instructions for Mac and Windows: [INSTALL.md](INSTALL.md)**

The short version:

- **Mac** (macOS 12+, Python 3.9+): `git clone https://github.com/xcessiveemile/pylevels.git`,
  then open **PyLevels.app** in the folder.
- **Windows** (10 or 11, Python 3.9 to 3.13 from python.org): download the
  ZIP, unzip it, double-click **PyLevels.bat**.

The first start sets everything up by itself (a minute or two). After that
the app opens straight away and works offline.

## The tutor: pick one in settings

The game works without a tutor (the reference answer, ctrl+G, never needs
one), but it's nicer with one. Open **settings** and choose:

| Choice | Cost | What you need |
|---|---|---|
| **Claude** | your own Claude subscription | [Claude Code](https://claude.com/claude-code) installed and signed in. Settings has a *sign in* button. |
| **Gemini key** | free | A free key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey), pasted into settings. It stays on your computer. |
| **Local AI** | free, offline, private | [Ollama](https://ollama.com/download) running, and one model downloaded, e.g. `ollama pull llama3.2`. Settings finds your models. |

The status line at the top shows which tutor is on, with a ✓ when it's ready.

## Your own music

The music bubble in the bottom right plays background music. Click it, then
**+ add your music** to pick songs from your computer (mp3, m4a, aac, wav,
flac, ogg). They're copied into the `music/` folder in this project and play
first. **open folder** shows that folder, so you can also drop files in
yourself. Hover a song and click × to remove it. The built-in playlist is one
calm track streamed from YouTube, so it needs internet.

## Keys

| Where | Key | What it does |
|---|---|---|
| Menu | enter / O / T / S | levels, overview, theory, settings |
| Map | arrows, enter | pick a level and play it |
| Map | W | switch between Sea and Space |
| Level | ctrl+enter | run your code |
| Level | ctrl+H | a hint from the tutor |
| Level | ctrl+T | talk with the tutor |
| Level | ctrl+G | the reference answer |
| Level | ctrl+K | the theory for this level |
| Level | tab | next level, once you've passed |
| Theory | ← → | previous / next card |
| Anywhere | esc | back |

Stars: 3 for a clean pass, 2 if you used the tutor, 1 after many tries or
skips. Stars turn into XP.

## Your progress

Progress is saved to `progress.json` in this folder after every change. Git
ignores it, so pulling updates never overwrites it. **Settings → start over**
(press R twice) resets it.

## Other ways to play

- **Terminal version**: `.venv/bin/python main.py` plays the same sea levels
  as a terminal game (its tutor uses Claude Code only).
  `PyLevels.command` opens that version in a browser tab with footage behind it.
- **Browser version**: `web-game/` is the same game as the app, as a static
  page (Python runs in the page via Pyodide). Serve the folder with any static
  server, e.g. `python3 -m http.server -d web-game 8790`.

## Adding levels

A level is one Python dict in a `levels/world_XX.py` file. See
[LEVELS.md](LEVELS.md) for the shape, then run
`.venv/bin/python export_levels.py` so the app picks it up.

## How it's built

| Part | What it does |
|---|---|
| `desktop.py` | the app: a native window (pywebview) showing `web-game/`, plus the tutor, save and music functions the page calls |
| `web-game/` | the game itself: `game.js`, `style.css`, `levels.json`, Pyodide and CodeMirror in `vendor/` |
| `local_ai.py` | talks to Ollama for the local AI tutor |
| `tutor.py` | talks to Claude Code for the Claude tutor |
| `progress.py` | reads and writes `progress.json` |
| `levels/`, `checker.py` | the levels and how a pass is judged |
| `PyLevels.app` | the Mac launcher: sets up on first start, then opens `desktop.py` |
| `PyLevels.bat`, `windows/` | the Windows launcher, setup and Start-menu shortcut |
| `setup.sh`, `build_launcher.sh` | make the `.venv` and build the small launcher that shows the app as PyLevels in the Dock |
| `app.py`, `main.py`, `web/` | the terminal version |

Tests: `.venv/bin/python -m pytest`. `tests/app_smoke.py` opens the real window once;
GitHub runs both on Windows for every push.

## Credits

Background videos from [Pexels](https://www.pexels.com) under the Pexels
licence: "Video of Dolphins Swimming", and "A red and purple nebula with stars
in the background" by Frank Cone. Python in the page by
[Pyodide](https://pyodide.org), editor by [CodeMirror](https://codemirror.net).

## Licence

MIT, see [LICENSE](LICENSE).
