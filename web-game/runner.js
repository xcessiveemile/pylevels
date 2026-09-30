// The Python runner: a Web Worker that loads Pyodide (Python in WebAssembly),
// runs the player's code with the level's hidden code, and judges the result
// with the same checker.py the terminal game uses. The page kills this worker
// after 8 seconds if the code never finishes, then starts a fresh one.
// Python ships with the game (vendor/pyodide). The CDN is only a fallback.
let pyodideBase = "vendor/pyodide/";
try {
  importScripts(pyodideBase + "pyodide.js");
} catch (error) {
  pyodideBase = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/";
  importScripts(pyodideBase + "pyodide.js");
}

let pyodide = null;

const HELPERS = `
import io, json, os, sys, tempfile, traceback

def _run(code, hidden):
    """Run code then hidden in a fresh module, in a fresh folder. Returns a result dict."""
    folder = tempfile.mkdtemp()
    os.chdir(folder)
    full = code.rstrip("\\n") + "\\n" + hidden
    out, err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = out, err
    exit_code = 0
    try:
        exec(compile(full, "your_code.py", "exec"), {"__name__": "__main__"})
    except SystemExit as stop:
        exit_code = stop.code if isinstance(stop.code, int) else (0 if stop.code is None else 1)
    except BaseException:
        traceback.print_exc(file=err)
        exit_code = 1
    finally:
        sys.stdout, sys.stderr = old_out, old_err
    return {"stdout": out.getvalue(), "stderr": err.getvalue(), "timed_out": False, "exit_code": exit_code}

def _judge(result_json, level_json, code):
    from checker import judge
    return json.dumps(judge(json.loads(result_json), json.loads(level_json), code))

def _run_and_judge(code, hidden, level_json):
    result = _run(code, hidden)
    verdict = json.loads(_judge(json.dumps(result), level_json, code))
    return json.dumps({"result": result, "verdict": verdict})
`;

async function boot() {
  pyodide = await loadPyodide({ indexURL: pyodideBase });
  const checker = await (await fetch("py/checker.py")).text();
  pyodide.FS.writeFile("/home/pyodide/checker.py", checker);
  pyodide.runPython("import sys; sys.path.insert(0, '/home/pyodide')");
  pyodide.runPython(HELPERS);
  // Warm up once, so the first real run is not slowed down by first-time
  // imports and compilation, which the loop clock must not count.
  pyodide.runPython("import json, math, random, statistics, collections, datetime, dataclasses, tempfile, string, itertools, functools");
  pyodide.globals.get("_run")("print(0)", "");
  postMessage({ type: "ready" });
}

const ready = boot();

onmessage = async (event) => {
  const { id, code, hidden, level } = event.data;
  await ready;
  // The page starts its loop clock only now, when the code really begins.
  postMessage({ type: "started", id });
  try {
    const run = pyodide.globals.get("_run_and_judge");
    const text = run(code, hidden, JSON.stringify(level));
    run.destroy();
    postMessage({ type: "done", id, ...JSON.parse(text) });
  } catch (error) {
    postMessage({ type: "done", id, result: { stdout: "", stderr: String(error), timed_out: false, exit_code: 1 },
                  verdict: { passed: false, diff: "the runner hit a problem: " + String(error).split("\n")[0] } });
  }
};
