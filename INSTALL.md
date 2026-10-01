# Installing PyLevels

PyLevels runs on **Mac** and **Windows**. It is free and needs no account.
You need about 400 MB of free space and an internet connection the first
time (to download its parts). After that it works offline.

- [Mac](#mac)
- [Windows](#windows)
- [Setting up the tutor](#setting-up-the-tutor)
- [Updating](#updating)
- [Uninstalling](#uninstalling)

---

## Mac

**You need:** macOS 12 (Monterey) or newer.

### 1. Check that Python is there

Open **Terminal** (press cmd+space, type *Terminal*, press enter) and type:

```bash
python3 --version
```

- If it prints `Python 3.9` or higher, you're good.
- If a window asks to install the **command line developer tools**, click
  **Install** and wait for it to finish. That gives you Python.
- If it says the command is not found, install Python from
  [python.org/downloads](https://www.python.org/downloads/).

### 2. Download PyLevels

**Option A, with git (recommended):** in Terminal:

```bash
cd ~/Documents
git clone https://github.com/xcessiveemile/pylevels.git
```

**Option B, as a ZIP:** on the GitHub page click **Code → Download ZIP**,
double-click the ZIP to unzip it, and move the `pylevels-main` folder
somewhere you'll keep it (for example Documents). Then unlock it once in
Terminal, because macOS locks apps downloaded from the internet:

```bash
xattr -dr com.apple.quarantine ~/Documents/pylevels-main
```

(Change the path if you put the folder somewhere else. Tip: type
`xattr -dr com.apple.quarantine ` with a space at the end, then drag the folder
into the Terminal window and press enter.)

### 3. Open it

Open the folder and double-click **PyLevels.app**.

The first start sets everything up by itself. You'll see a notification;
it takes a minute or two. Then the game opens in its own window. From then
on it opens straight away. Closing the window quits.

**Tip:** drag PyLevels.app to your Dock to keep it there. Leave the app inside
its folder, because it needs the files next to it.

### If something goes wrong on Mac

| What you see | What to do |
|---|---|
| *"PyLevels can't be opened because Apple cannot check it"* | Right-click PyLevels.app → **Open** → **Open**. On newer macOS: System Settings → Privacy & Security → scroll down → **Open Anyway**. |
| *"PyLevels opened from a locked copy"* | You skipped the unlock step: run the `xattr` command from step 2. |
| *"Setting up failed"* | Check your internet connection and try again. The details are in `~/Library/Logs/PyLevels.log`. |
| Nothing happens at all | Open Terminal, `cd` into the folder and run `bash setup.sh`. It prints what goes wrong. |

---

## Windows

**You need:** Windows 10 or 11.

### 1. Install Python

1. Go to [python.org/downloads](https://www.python.org/downloads/) and download
   **Python 3.13** (versions 3.9 to 3.13 work).
2. Run the installer. On the first screen, **tick "Add python.exe to PATH"**,
   then click **Install Now**.

Already have Python? Open Command Prompt and type `py --version`. Any
version from 3.9 to 3.13 is fine.

### 2. Download PyLevels

On the GitHub page click **Code → Download ZIP**. Right-click the ZIP →
**Extract All…** and put the folder somewhere you'll keep it, for example
Documents. (Or, with git: `git clone https://github.com/xcessiveemile/pylevels.git`.)

### 3. Open it

Open the folder and double-click **PyLevels.bat**.

- If Windows shows *"Windows protected your PC"*, click **More info → Run
  anyway**. This happens because the file is new to Windows, not because
  something is wrong.
- A black window shows the setup. It takes a minute or two the first time.
- Then the game opens in its own window, and a **PyLevels** shortcut appears
  on your desktop and in the Start menu. Use that shortcut from now on.

### If something goes wrong on Windows

| What you see | What to do |
|---|---|
| *"PyLevels needs Python 3.9 or newer"* | Install Python (step 1) and make sure **Add python.exe to PATH** was ticked. Then double-click PyLevels.bat again. |
| Setup stops with red pip errors | Check your internet connection and try again. If you have Python 3.14, install 3.13 next to it; PyLevels picks it automatically. |
| The game window is blank | Install the Microsoft Edge WebView2 Runtime from [microsoft.com](https://developer.microsoft.com/microsoft-edge/webview2/) (Windows 11 already has it). |
| The shortcut stopped working after moving the folder | Double-click `windows\setup.bat` in the new place; it makes new shortcuts. |
| Anything else | The details are in `%LOCALAPPDATA%\PyLevels\PyLevels.log` (paste that into the File Explorer address bar). |

---

## Setting up the tutor

PyLevels works without a tutor, and the reference answer (ctrl+G) is always
there. But a tutor that gives hints is nicer. In the game, open **settings**
and pick one:

**Gemini key (free, easiest)**
1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey) and
   sign in with a Google account.
2. Click **Create API key** and copy it.
3. Paste it into the box in settings and press enter.

**Local AI (free, private, works offline)**
1. Install Ollama from [ollama.com/download](https://ollama.com/download) and open it.
2. In Terminal (Mac) or Command Prompt (Windows), download a model once:
   `ollama pull llama3.2` (about 2 GB).
3. In settings, choose **local AI**. It finds your model by itself.

**Claude (if you have a Claude subscription)**
1. Install [Claude Code](https://claude.com/claude-code).
2. In settings, choose **Claude** and click **sign in**.

The top bar shows *tutor ✓* when it's ready.

---

## Updating

Your progress lives in `progress.json` and your own songs in the `music`
folder. Both stay put when you update.

- **With git:** in the PyLevels folder, run `git pull`.
- **With a ZIP:** download the new ZIP, unzip it, then copy `progress.json`
  and the `music` folder from your old PyLevels folder into the new one.
  On Mac, run the unlock command again for the new folder.

The next start sets up anything new by itself.

---

## Uninstalling

Delete the PyLevels folder. That's everything: PyLevels doesn't install
anything elsewhere, apart from:

- **Mac:** the log file `~/Library/Logs/PyLevels.log`.
- **Windows:** the desktop and Start menu shortcuts, and the folder
  `%LOCALAPPDATA%\PyLevels` with the log.
