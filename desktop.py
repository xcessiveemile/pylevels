"""PyLevels as a desktop app: a native window, everything offline.

The window shows the game from web-game/ (Python, the editor, the levels and
the media all ship inside it). The tutor is picked in settings: Claude Code
on this computer (your own subscription), your own free Gemini key, or a
local AI model through Ollama. Your own music goes in the music/ folder.
No terminal, no browser, no separate server.

    .venv/bin/python desktop.py
"""

import os
import shutil
import subprocess
import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote, unquote

import webview

import local_ai
import progress
import tutor


def allow_autoplay():
    """Let the backdrop video start on its own in the app window.

    The window library builds WebKit's settings without saying that media may
    play without a click, so the video would sit still with a play button.
    This wraps the settings object it creates and switches that on.
    """
    try:
        import WebKit
        from webview.platforms import cocoa
    except ImportError:
        return
    real_configuration = WebKit.WKWebViewConfiguration

    class Allocated:
        def init(self):
            config = real_configuration.alloc().init()
            config.setMediaTypesRequiringUserActionForPlayback_(0)   # 0 means: none
            config.setAllowsInlineMediaPlayback_(True) if hasattr(config, "setAllowsInlineMediaPlayback_") else None
            return config

    class Configuration:
        @staticmethod
        def alloc():
            return Allocated()

    class WebKitWithAutoplay:
        WKWebViewConfiguration = Configuration

        def __getattr__(self, name):
            return getattr(WebKit, name)

    cocoa.WebKit = WebKitWithAutoplay()

GAME_FOLDER = Path(__file__).parent / "web-game"
GAME_PORT = 8767

# Your own songs: put them in this folder, or use "add music" in the music panel.
MUSIC_FOLDER = Path(__file__).parent / "music"
MUSIC_TYPES = [".mp3", ".m4a", ".aac", ".wav", ".flac", ".ogg", ".opus"]
MUSIC_ADDRESS = "/my-music/"   # the page finds the music folder at this address


class RangeHandler(SimpleHTTPRequestHandler):
    """Serves the game folder, with byte ranges: WebKit needs those to play video."""

    def log_message(self, format, *args):
        pass   # quiet

    def translate_path(self, path):
        """Addresses starting with /my-music/ come from the music folder."""
        if path.startswith(MUSIC_ADDRESS):
            name = unquote(path[len(MUSIC_ADDRESS):].split("?")[0])
            return str(MUSIC_FOLDER / Path(name).name)   # .name: no way out of the folder
        return super().translate_path(path)

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path) or "Range" not in self.headers:
            return super().send_head()
        try:
            size = os.path.getsize(path)
            file = open(path, "rb")
        except OSError:
            self.send_error(404)
            return None
        # "bytes=start-end", either end may be missing.
        first, last = self.headers["Range"].replace("bytes=", "").split("-")
        start = int(first) if first else max(size - int(last), 0)
        end = int(last) if last and first else size - 1
        end = min(end, size - 1)
        file.seek(start)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        self._range_length = end - start + 1
        return file

    def copyfile(self, source, outputfile):
        length = getattr(self, "_range_length", None)
        if length is None:
            return super().copyfile(source, outputfile)
        outputfile.write(source.read(length))


def serve_game():
    """Start the game's own little server on this computer and return its address."""
    handler = partial(RangeHandler, directory=str(GAME_FOLDER))
    # Always the same port if it is free, so the page's own settings (volume,
    # music) are remembered between launches. Port 0 means: any free port.
    try:
        server = ThreadingHTTPServer(("127.0.0.1", GAME_PORT), handler)
    except OSError:
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{server.server_address[1]}/"


class Api:
    """What the game can call: window.pywebview.api.<name>(...)"""

    window = None   # set once the window exists, so quit can close it

    def quit(self, data=None):
        """Save one last time, then close the app."""
        if data:
            progress.save(data)
        # Close a moment later, so this call can still answer the page first.
        threading.Timer(0.2, self.window.destroy).start()
        return True

    def tutor(self, system, prompt):
        return tutor.run_claude(system, prompt)

    def sign_in(self):
        """Open Claude's sign-in page in the browser."""
        return tutor.start_login()

    def local_models(self, address):
        """Which models Ollama has on this computer."""
        return local_ai.models(address)

    def local_tutor(self, address, model, system, prompt):
        return local_ai.run(address, model, system, prompt)

    def music_list(self):
        """Your own songs from the music folder, as tracks for the music panel."""
        MUSIC_FOLDER.mkdir(exist_ok=True)
        songs = sorted(f for f in MUSIC_FOLDER.iterdir() if f.suffix.lower() in MUSIC_TYPES)
        return [{"title": f.stem, "artist": "your music", "file": MUSIC_ADDRESS + quote(f.name), "mine": f.name} for f in songs]

    def add_music(self):
        """Pick songs on this computer and copy them into the music folder."""
        kinds = ";".join("*" + t for t in MUSIC_TYPES)
        dialog = webview.FileDialog.OPEN if hasattr(webview, "FileDialog") else webview.OPEN_DIALOG
        chosen = self.window.create_file_dialog(dialog, allow_multiple=True, file_types=(f"Music ({kinds})",)) or []
        MUSIC_FOLDER.mkdir(exist_ok=True)
        for name in chosen:
            if Path(name).suffix.lower() in MUSIC_TYPES:
                shutil.copy2(name, MUSIC_FOLDER / Path(name).name)
        return self.music_list()

    def remove_music(self, name):
        """Take one song out of the music folder (the copy only, never the original)."""
        song = MUSIC_FOLDER / Path(name).name
        if song.suffix.lower() in MUSIC_TYPES and song.exists():
            song.unlink()
        return self.music_list()

    def open_link(self, url):
        """Open a web address in your normal browser."""
        if url.startswith("https://"):
            open_on_computer(url)
        return True

    def open_music_folder(self):
        """Show the music folder in Finder."""
        MUSIC_FOLDER.mkdir(exist_ok=True)
        open_on_computer(str(MUSIC_FOLDER))
        return True

    def load_progress(self):
        """Your saved progress, from progress.json (shared with the terminal game)."""
        return progress.load()

    def save_progress(self, data):
        """Write your progress to progress.json, so it is still there next time."""
        progress.save(data)
        return True

    def status(self):
        ok, message = tutor.status()
        return {"ok": ok, "message": message}


def open_on_computer(target):
    """Open a web address in the browser, or a folder in Finder / File Explorer."""
    if sys.platform == "win32":
        os.startfile(target)
    elif sys.platform == "darwin":
        subprocess.run(["open", target])
    else:
        subprocess.run(["xdg-open", target])


def log_to_file_on_windows():
    """Started by double-click on Windows (pythonw) there is no console: write to a log file."""
    if sys.platform != "win32" or sys.stdout is not None:
        return
    folder = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "PyLevels"
    folder.mkdir(parents=True, exist_ok=True)
    sys.stdout = sys.stderr = open(folder / "PyLevels.log", "a", buffering=1, encoding="utf-8")


def self_test(window):
    """Opens the game, checks it loads and that the tutor call answers, then closes."""
    import time
    time.sleep(10)
    screen = window.evaluate_js("document.getElementById('screen').className")
    api_seen = window.evaluate_js("!!(window.pywebview && window.pywebview.api)")
    # The api call is a promise in the page, so store its answer and read it back.
    window.evaluate_js("window.__reply = null; window.pywebview.api.tutor('Reply with the single word pong.', 'ping').then(r => window.__reply = r)")
    reply = None
    for _ in range(150):
        time.sleep(1)
        reply = window.evaluate_js("window.__reply")
        if reply:
            break
    video = window.evaluate_js("(function(){ var v = document.getElementById('video-sea'); if (!v) return 'none'; var before = 'paused=' + v.paused + ' time=' + v.currentTime.toFixed(1) + ' ready=' + v.readyState + ' ended=' + v.ended + ' err=' + (v.error && v.error.code) + ' vis=' + document.visibilityState + ' display=' + getComputedStyle(v).display; v.play(); return before; })()")
    time.sleep(2)
    video += window.evaluate_js("(function(){ var v = document.getElementById('video-sea'); return ' | after play(): paused=' + v.paused + ' time=' + v.currentTime.toFixed(1); })()")
    print("self test: screen =", screen, "| api =", api_seen, "| tutor =", reply, "| video:", video)
    window.destroy()


def show_app_icon():
    """Give the window the PyLevels icon in the Dock, also when plain Python runs this file."""
    try:
        from AppKit import NSApplication, NSImage
    except ImportError:
        return
    icon = Path(__file__).parent / "PyLevels.app" / "Contents" / "Resources" / "PyLevels.icns"
    image = NSImage.alloc().initWithContentsOfFile_(str(icon))
    if image:
        NSApplication.sharedApplication().setApplicationIconImage_(image)


if __name__ == "__main__":
    log_to_file_on_windows()
    allow_autoplay()
    show_app_icon()
    print("tutor:", tutor.status(), flush=True)   # shows up in the log file
    api = Api()
    window = webview.create_window(
        "PyLevels", serve_game(), js_api=api,
        width=1440, height=900, min_size=(960, 640), background_color="#03132c",
    )
    api.window = window
    # WebKit only lets media start from a user action; a call from here counts
    # as one, so the backdrop video is set going as soon as the page is in.
    def play_videos():
        import time
        for _ in range(20):
            time.sleep(0.5)
            try:
                playing = window.evaluate_js("(function(){ var ok = false; document.querySelectorAll('video').forEach(function(v){ v.play(); if (v.readyState >= 3) ok = true; }); return ok; })()")
            except Exception:
                playing = False
            if playing:
                break
    window.events.loaded += lambda: threading.Thread(target=play_videos, daemon=True).start()

    if "--selftest" in sys.argv:
        webview.start(self_test, window)
    else:
        # private_mode=False keeps the page's settings between launches.
        webview.start(private_mode=False)
