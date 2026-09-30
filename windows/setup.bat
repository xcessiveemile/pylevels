@echo off
rem Creates the virtual environment and installs everything the game needs,
rem then adds a PyLevels shortcut to the Start menu and the desktop.
rem PyLevels.bat runs this for you on the first start.
cd /d "%~dp0.."

rem The newest Python 3.9 or later that the window library supports.
set "PY="
for %%v in (3.13 3.12 3.11 3.10 3.9 3.14) do (
  if not defined PY py -%%v -c "import sys" >nul 2>&1 && set "PY=py -%%v"
)
if not defined PY python -c "import sys; sys.exit(sys.version_info < (3, 9))" >nul 2>&1 && set "PY=python"
if not defined PY (
  echo PyLevels needs Python 3.9 or newer.
  echo Install it from https://www.python.org/downloads/ and tick "Add python.exe to PATH",
  echo then double-click PyLevels.bat again.
  exit /b 1
)
echo Using %PY%

rem A venv stops working when the folder moves or its Python is removed: make a new one.
if exist ".venv" (
  ".venv\Scripts\python.exe" -c "import sys" >nul 2>&1 || rmdir /s /q ".venv"
)
if not exist ".venv\Scripts\python.exe" (
  %PY% -m venv .venv || exit /b 1
)
".venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
".venv\Scripts\python.exe" -m pip install --quiet -r requirements.txt || exit /b 1

powershell -NoProfile -ExecutionPolicy Bypass -File "windows\shortcut.ps1"
echo PyLevels is set up.
exit /b 0
