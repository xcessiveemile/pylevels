"""Asks a local AI model on this computer for help, through Ollama.

Ollama (ollama.com) runs free AI models on your own computer: no account,
no key, no internet once a model is downloaded. Install it, then download a
model once in a terminal, for example:

    ollama pull llama3.2

The desktop app calls these two functions when the tutor is set to "local AI".
"""

import json
import urllib.error
import urllib.request

OLLAMA_ADDRESS = "http://localhost:11434"
TIMEOUT_SECONDS = 180   # a first answer can be slow while the model loads


def ask(address, path, data=None, timeout=10):
    """Send one request to Ollama and return its JSON answer as a dict."""
    url = (address or OLLAMA_ADDRESS).rstrip("/") + path
    body = json.dumps(data).encode() if data is not None else None
    request = urllib.request.Request(url, data=body, headers={"content-type": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode())


def models(address):
    """The names of the models downloaded in Ollama. Returns {ok, models, message}."""
    try:
        data = ask(address, "/api/tags")
    except (urllib.error.URLError, OSError, ValueError):
        return {"ok": False, "models": [], "message": "Ollama is not running on this computer"}
    names = [model["name"] for model in data.get("models", [])]
    if not names:
        return {"ok": False, "models": [], "message": "Ollama is running but has no models yet"}
    return {"ok": True, "models": names, "message": f"{len(names)} model(s) found"}


def run(address, model, rules, prompt):
    """Ask the model once and return its answer as text."""
    data = {
        "model": model,
        "stream": False,
        "messages": [
            {"role": "system", "content": rules},
            {"role": "user", "content": prompt},
        ],
        "options": {"temperature": 0.4},
    }
    try:
        answer = ask(address, "/api/chat", data, timeout=TIMEOUT_SECONDS)
    except urllib.error.HTTPError as error:
        return f"the local AI could not answer: {error.read().decode(errors='replace')[:200]}"
    except (urllib.error.URLError, OSError):
        return "the local AI is not running. Start Ollama, then try again."
    except ValueError:
        return "the local AI sent something unreadable, try again"
    text = answer.get("message", {}).get("content", "").strip()
    return text or "the tutor had nothing to say, try again"
