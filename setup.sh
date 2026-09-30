#!/bin/bash
# Creates the virtual environment and installs everything the game needs.
# Run once:  bash setup.sh   (PyLevels.app and PyLevels.command run it for you)
set -e
cd "$(dirname "$0")"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

# The newest Python 3.9 or later on this computer.
PYTHON=""
for name in python3.14 python3.13 python3.12 python3.11 python3.10 python3; do
  if command -v "$name" >/dev/null 2>&1 && "$name" -c 'import sys; sys.exit(sys.version_info < (3, 9))' 2>/dev/null; then
    PYTHON="$name"; break
  fi
done
if [ -z "$PYTHON" ]; then
  echo "PyLevels needs Python 3.9 or newer. Install it from python.org, then try again."
  exit 1
fi

# A venv stops working when the folder moves or its Python is removed: make a new one.
if [ -d .venv ] && ! .venv/bin/python -c "import sys" >/dev/null 2>&1; then
  rm -rf .venv
fi
if [ ! -x .venv/bin/python ]; then
  "$PYTHON" -m venv .venv
fi
.venv/bin/python -m pip install --quiet --upgrade pip
.venv/bin/python -m pip install --quiet -r requirements.txt
bash build_launcher.sh || echo "(the app will start Python directly, that works too)"
echo "PyLevels is set up. Double-click PyLevels.app, or run: .venv/bin/python desktop.py"
