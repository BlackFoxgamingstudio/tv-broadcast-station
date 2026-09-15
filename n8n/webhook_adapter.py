#!/usr/bin/env python3
import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.core import CoreEngine

PORT = 8812
engine = CoreEngine()

class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/health", "/healthz", "/"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(engine.health_check()).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        auth_header = self.headers.get("X-SBB-Auth")
        if auth_header != os.environ.get("SBB_SHARED_SECRET", "sbb_local_dev_secret_2026"):
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "Unauthorized"}')
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            data = json.loads(body)
        except Exception:
            data = {}

        action = data.get("action", "assemble_broadcast_package")
        payload = data.get("payload", data)
        res = engine.execute_feature(action, payload)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(res).encode())

    def log_message(self, format, *args):
        pass

def run():
    server = HTTPServer(("0.0.0.0", PORT), WebhookHandler)
    print(f"[TV Broadcast Station] Webhook Adapter listening on http://0.0.0.0:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    run()