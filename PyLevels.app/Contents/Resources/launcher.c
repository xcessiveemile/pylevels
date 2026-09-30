// PyLevels launcher: runs desktop.py inside this app bundle's own process,
// so macOS sees the window as PyLevels (Dock dot, name, icon), not as Python.
// build_launcher.sh compiles it for the Python in .venv, which fills in
// PYLEVELS_HOME and PYLEVELS_PYTHON. "pylevels-bin --check" only tests that it can start.
#include <Python.h>
#include <mach-o/dyld.h>
#include <libgen.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char **argv) {
    char exe[PATH_MAX], real[PATH_MAX], app[PATH_MAX], site[PATH_MAX];
    uint32_t size = sizeof exe;
    if (_NSGetExecutablePath(exe, &size) != 0 || !realpath(exe, real)) return 1;
    // .../pylevels/PyLevels.app/Contents/MacOS/pylevels-bin -> .../pylevels
    strcpy(app, real);
    for (int i = 0; i < 4; i++) strcpy(app, dirname(app));
    snprintf(site, sizeof site, "%s/.venv/lib/python%s/site-packages", app, PYLEVELS_PYTHON);
    if (argc > 1 && strcmp(argv[1], "--check") == 0)
        return access(PYLEVELS_HOME, R_OK) == 0 && access(site, R_OK) == 0 ? 0 : 1;
    if (chdir(app) != 0) return 1;

    PyConfig config;
    PyConfig_InitPythonConfig(&config);
    PyConfig_SetBytesString(&config, &config.home, PYLEVELS_HOME);
    PyConfig_SetBytesString(&config, &config.pythonpath_env, site);
    char *args[] = { real, "desktop.py" };
    PyStatus status = PyConfig_SetBytesArgv(&config, 2, args);
    if (!PyStatus_Exception(status)) status = Py_InitializeFromConfig(&config);
    PyConfig_Clear(&config);
    if (PyStatus_Exception(status)) Py_ExitStatusException(status);
    return Py_RunMain();
}
