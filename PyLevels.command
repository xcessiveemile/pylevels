#!/bin/bash
# Double-click this file to start PyLevels in your browser.
# It sets itself up the first time, then keeps running in this Terminal
# window until you close the window.
cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ]; then
  echo "first start: setting up..."
  bash setup.sh
fi
( sleep 1.5; open "http://localhost:8765" ) &
exec .venv/bin/python web/serve.py
