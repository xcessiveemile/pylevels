"""Plays PyLevels in the browser with real footage behind it.

Run with:  python web/serve.py   then open http://localhost:8765

Drop your own footage in web/static/background/ as scene.mp4 (a video) or
scene.jpg (a photo). Without either, a painted sea is shown.
The game itself is told to leave its background transparent so the
footage shows through.

Two environment variables matter when hosting (see DEPLOY.md):
  PYLEVELS_HOST   the address to listen on, default localhost
  PORT            the port, default 8765
"""

import os
import sys
from pathlib import Path

from textual_serve.server import Server

HERE = Path(__file__).parent
PROJECT = HERE.parent
HOST = os.environ.get("PYLEVELS_HOST", "localhost")
PORT = int(os.environ.get("PORT", "8765"))

# Use the project's own venv when it exists, otherwise whatever Python runs this file.
VENV_PYTHON = PROJECT / ".venv" / "bin" / "python"
PYTHON = VENV_PYTHON if VENV_PYTHON.exists() else Path(sys.executable)

# Quotes around the paths keep spaces in folder names safe.
command = f'env PYLEVELS_TRANSPARENT=1 "{PYTHON}" "{PROJECT / "main.py"}"'

server = Server(
    command,
    host=HOST,
    port=PORT,
    title="PyLevels",
    statics_path=HERE / "static",
    templates_path=HERE / "templates",
)
server.serve()
