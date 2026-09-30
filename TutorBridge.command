#!/bin/bash
# Double-click to let the website version use the Claude tutor on this Mac.
# Leave this window open while you play; close it to stop.
cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ]; then bash setup.sh; fi
exec .venv/bin/python tutor_bridge.py
