"""Run Pattern Lab with Python's standard library (no Flask installation needed)."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import mimetypes

from algorithms import ALGORITHMS, compare_algorithms

ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 5000


class PatternLabHandler(BaseHTTPRequestHandler):
    def send_bytes(self, status, payload, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def send_json(self, status, value):
        payload = json.dumps(value).encode("utf-8")
        self.send_bytes(status, payload, "application/json; charset=utf-8")

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            file_path = ROOT / "templates" / "index.html"
            content_type = "text/html; charset=utf-8"
        elif self.path.startswith("/static/"):
            relative = self.path[len("/static/"):].split("?", 1)[0]
            file_path = (ROOT / "static" / relative).resolve()
            static_root = (ROOT / "static").resolve()
            if static_root not in file_path.parents:
                self.send_error(404)
                return
            content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
            if content_type.startswith("text/") or content_type in ("application/javascript",):
                content_type += "; charset=utf-8"
        else:
            self.send_error(404)
            return

        try:
            self.send_bytes(200, file_path.read_bytes(), content_type)
        except FileNotFoundError:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/api/compare":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 1_000_000:
                self.send_json(413, {"error": "Request is too large."})
                return
            data = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            self.send_json(400, {"error": "Request must contain valid JSON."})
            return

        text = data.get("text", "") if isinstance(data, dict) else None
        pattern = data.get("pattern", "") if isinstance(data, dict) else None
        selected = data.get("algorithms", list(ALGORITHMS)) if isinstance(data, dict) else None
        if not isinstance(text, str) or not isinstance(pattern, str):
            self.send_json(400, {"error": "Text and pattern must be strings."})
        elif len(text) > 100_000 or len(pattern) > 10_000:
            self.send_json(413, {"error": "Please keep the text under 100,000 characters and pattern under 10,000."})
        elif not pattern:
            self.send_json(400, {"error": "Enter a pattern to search for."})
        else:
            try:
                self.send_json(200, compare_algorithms(text, pattern, selected))
            except (ValueError, TypeError) as error:
                self.send_json(400, {"error": str(error)})

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), PatternLabHandler)
    print(f"Pattern Lab is running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop the server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nPattern Lab stopped.")
    finally:
        server.server_close()
