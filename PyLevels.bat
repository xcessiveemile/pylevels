@echo off
rem PyLevels for Windows: double-click this file to play.
rem The first start sets everything up (a minute or two), then the game opens
rem in its own window. After that you can also use the PyLevels shortcut in
rem the Start menu. Problems are written to %LOCALAPPDATA%\PyLevels\PyLevels.log
cd /d "%~dp0"
".venv\Scripts\python.exe" -c "import webview, textual" >nul 2>&1
if errorlevel 1 (
  echo First start: setting up PyLevels, this takes a minute or two...
  call windows\setup.bat
  if errorlevel 1 (
    echo.
    echo Setting up failed, see the messages above.
    pause
    exit /b 1
  )
)
start "" ".venv\Scripts\pythonw.exe" desktop.py
