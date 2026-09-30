"""Opens the real app window, checks the game loads, then closes. Exit code 0 = fine.

    .venv/bin/python tests/app_smoke.py      (Windows: .venv\\Scripts\\python.exe tests\\app_smoke.py)

Used by the Windows check on GitHub. Not a pytest file: it needs a screen.
"""

import os
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import webview   # noqa: E402
import desktop   # noqa: E402

checks = {}


def run(window):
    time.sleep(3)
    for _ in range(60):   # wait for the entry screen (Python in the page loads meanwhile)
        if window.evaluate_js("document.getElementById('screen').className") == "screen entry":
            break
        time.sleep(1)
    js = window.evaluate_js
    checks["entry screen"] = js("document.getElementById('screen').className") == "screen entry"
    checks["app functions seen"] = js("!!(window.pywebview && window.pywebview.api && window.pywebview.api.music_list)")
    checks["music panel"] = js("document.querySelectorAll('#playlist div').length") >= 1
    js("document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter'}))")
    time.sleep(1)
    js("document.dispatchEvent(new KeyboardEvent('keydown', {key: 's'}))")
    time.sleep(2)
    checks["tutor choices"] = js("document.querySelectorAll('.choice').length") == 3
    window.destroy()


def give_up():
    time.sleep(150)
    print("the window did not finish in time", flush=True)
    os._exit(2)


if __name__ == "__main__":
    threading.Thread(target=give_up, daemon=True).start()
    api = desktop.Api()
    window = webview.create_window("PyLevels check", desktop.serve_game(), js_api=api, width=1200, height=800)
    api.window = window
    webview.start(run, window)
    for name, ok in checks.items():
        print(("ok    " if ok else "FAIL  ") + name, flush=True)
    sys.exit(0 if checks and all(checks.values()) else 1)
