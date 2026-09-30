# Adds a PyLevels shortcut, with its icon, to the Start menu and the desktop.
# windows\setup.bat runs this. Run it again if you move the PyLevels folder.
$root = Split-Path -Parent $PSScriptRoot
$shell = New-Object -ComObject WScript.Shell
foreach ($place in @([Environment]::GetFolderPath("Programs"), [Environment]::GetFolderPath("Desktop"))) {
    $link = $shell.CreateShortcut((Join-Path $place "PyLevels.lnk"))
    $link.TargetPath = Join-Path $root ".venv\Scripts\pythonw.exe"
    $link.Arguments = '"' + (Join-Path $root "desktop.py") + '"'
    $link.WorkingDirectory = $root
    $link.IconLocation = Join-Path $root "windows\PyLevels.ico"
    $link.Description = "PyLevels: learn Python by typing code"
    $link.Save()
}
Write-Output "shortcuts added to the Start menu and the desktop"
