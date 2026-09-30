#!/bin/bash
# Builds the small launcher inside PyLevels.app for the Python in .venv, so
# the game window shows up as PyLevels (name and Dock icon) and not as Python.
# setup.sh runs this. It needs Apple's command line tools (xcode-select
# --install). Without them the app still works: it starts Python directly.
set -e
cd "$(dirname "$0")"
xcode-select -p >/dev/null 2>&1 || { echo "no command line tools, skipping the launcher"; exit 1; }
PY=.venv/bin/python
ask() { "$PY" -c "import sys, sysconfig; print($1)"; }
HOME_DIR=$(ask "sys.base_prefix")
VERSION=$(ask "'%d.%d' % sys.version_info[:2]")
INCLUDE=$(ask "sysconfig.get_paths()['include']")
LIBDIR=$(ask "sysconfig.get_config_var('LIBDIR')")
FRAMEWORKS=$(cd "$HOME_DIR/../../.." && pwd)   # some Pythons are found as Python3.framework in here
OUT=PyLevels.app/Contents/MacOS/pylevels-bin
clang -O2 -o "$OUT" PyLevels.app/Contents/Resources/launcher.c \
  -I"$INCLUDE" -L"$LIBDIR" -lpython"$VERSION" -Wl,-rpath,"$LIBDIR" -Wl,-rpath,"$FRAMEWORKS" \
  -DPYLEVELS_HOME="\"$HOME_DIR\"" -DPYLEVELS_PYTHON="\"$VERSION\""
"$OUT" --check || { rm -f "$OUT"; echo "the launcher does not start with this Python"; exit 1; }
echo "launcher built for Python $VERSION"
