"""A small bridge so the website version can use the tutor on this Mac.

It listens on this computer only (127.0.0.1) and answers the website's
tutor questions through the claude command, on your own subscription.
Run it, then put http://localhost:8766 in the website's settings.

    .venv/bin/python tutor_bridge.py

Keep it for yourself: it is bound to this machine, and sharing a Claude
subscription with other people is not allowed by Anthropic's terms.
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import tutor

PORT = 8766


class Bridge(BaseHTTPRequestHandler):
    def send_json(self, code, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(code)
        # The website runs on another origin, so the browser asks for these.
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_json(200, {"ok": True})

    def do_GET(self):
        ok, message = tutor.status()
        self.send_json(200, {"ok": ok, "message": message})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        try:
            data = json.loads(self.rfile.read(length) or b"{}")
        except ValueError:
            self.send_json(400, {"error": "bad request"})
            return
        system, prompt = data.get("system"), data.get("prompt")
        if not isinstance(system, str) or not isinstance(prompt, str):
            self.send_json(400, {"error": "bad request"})
            return
        self.send_json(200, {"text": tutor.run_claude(system, prompt)})

    def log_message(self, format, *args):
        print("bridge:", format % args)


if __name__ == "__main__":
    print(f"tutor bridge on http://localhost:{PORT}  (this computer only)")
    print("put that address in the website's settings, under tutor")
    HTTPServer(("127.0.0.1", PORT), Bridge).serve_forever()
