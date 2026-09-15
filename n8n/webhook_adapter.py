#!/usr/bin/env python3
"""
Sovereign TV Broadcast Station (PKG-032) - Webhook Adapter & Playout Stage Server
Port: 8812
Serves 16:9 Cinematic Playout Stage, RESTful Broadcast APIs, and n8n webhook integration.
"""
import os
import sys
import json
import mimetypes
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.core import CoreEngine

PORT = 8812
STATIC_DIR = ROOT / "src" / "static"
DATA_DIR = ROOT / "data"
BROADCASTS_DIR = DATA_DIR / "broadcasts"
MEDIA_DIR = ROOT / "media"

BROADCASTS_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

engine = CoreEngine()

# In-memory broadcast cache
CURRENT_BROADCAST_FILE = DATA_DIR / "current_broadcast.json"
current_broadcast_data = {}

if CURRENT_BROADCAST_FILE.exists():
    try:
        with open(CURRENT_BROADCAST_FILE, "r", encoding="utf-8") as f:
            current_broadcast_data = json.load(f)
    except Exception as e:
        print(f"[TV Server] Could not load current_broadcast.json: {e}")


class BroadcastPlayoutHandler(BaseHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-SBB-Auth, X-OpenAI-API-Key")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # 1. Health check
        if path in ("/health", "/healthz"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(engine.health_check()).encode("utf-8"))
            return

        # 2. Playout Stage UI (/stage, /stage_player.html, /player)
        if path in ("/stage", "/stage/", "/stage_player.html", "/player") or (path == "/" and not self.headers.get("Accept", "").startswith("application/json")):
            stage_html_path = STATIC_DIR / "stage_player.html"
            if stage_html_path.exists():
                with open(stage_html_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"stage_player.html not found.")
                return

        # 3. Root API info
        if path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(engine.health_check()).encode("utf-8"))
            return

        # 4. GET /api/v1/broadcast/current
        if path == "/api/v1/broadcast/current":
            global current_broadcast_data
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(current_broadcast_data or {"status": "EMPTY", "frames": []}).encode("utf-8"))
            return

        # 5. GET /api/v1/broadcast/project/{project_id}
        if path.startswith("/api/v1/broadcast/project/"):
            project_id = path.replace("/api/v1/broadcast/project/", "").strip()
            target_file = BROADCASTS_DIR / f"{project_id}.json"
            if target_file.exists():
                with open(target_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(data).encode("utf-8"))
                return
            elif current_broadcast_data.get("project_id") == project_id:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(current_broadcast_data).encode("utf-8"))
                return
            else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"Broadcast project '{project_id}' not found"}).encode("utf-8"))
                return

        # 6. GET /api/v1/broadcast/projects (list)
        if path == "/api/v1/broadcast/projects":
            projects = []
            for f in BROADCASTS_DIR.glob("*.json"):
                try:
                    with open(f, "r", encoding="utf-8") as pf:
                        pdata = json.load(pf)
                        projects.append({
                            "project_id": pdata.get("project_id", f.stem),
                            "broadcast_title": pdata.get("broadcast_title", f.stem),
                            "frames_count": len(pdata.get("frames", [])),
                            "has_audio": bool(pdata.get("audio_url"))
                        })
                except Exception:
                    pass
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"projects": projects}).encode("utf-8"))
            return

        # 7. Static / Media Serving (/media/..., /audio/...)
        if path.startswith("/media/") or path.startswith("/audio/"):
            rel_sub = path.split("/", 2)[-1]
            local_candidate = MEDIA_DIR / rel_sub
            if not local_candidate.exists():
                local_candidate = DATA_DIR / rel_sub

            if local_candidate.exists() and local_candidate.is_file():
                mime, _ = mimetypes.guess_type(str(local_candidate))
                mime = mime or "application/octet-stream"
                file_size = local_candidate.stat().st_size

                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.send_header("Content-Length", str(file_size))
                self.send_header("Accept-Ranges", "bytes")
                self.send_cors_headers()
                self.end_headers()

                with open(local_candidate, "rb") as mf:
                    while chunk := mf.read(65536):
                        self.wfile.write(chunk)
                return

        self.send_response(404)
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(b'{"error": "Not Found"}')

    def do_POST(self):
        auth_header = self.headers.get("X-SBB-Auth")
        expected_secret = os.environ.get("SBB_SHARED_SECRET", "sbb_local_dev_secret_2026")

        parsed = urlparse(self.path)
        path = parsed.path

        # Check auth for sensitive endpoints, allowing local development bypass if matching
        if auth_header and auth_header != expected_secret:
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "Unauthorized"}')
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            data = json.loads(body)
        except Exception:
            data = {}

        # 1. POST /api/v1/broadcast/deploy
        if path in ("/api/v1/broadcast/deploy", "/deploy"):
            global current_broadcast_data
            current_broadcast_data = data

            # Persist current
            try:
                with open(CURRENT_BROADCAST_FILE, "w", encoding="utf-8") as f:
                    json.dump(current_broadcast_data, f, indent=2)
            except Exception as e:
                print(f"[TV Server] Error persisting current_broadcast: {e}")

            # Also persist indexed by project_id
            project_id = data.get("project_id") or "proj-active-broadcast"
            target_proj_file = BROADCASTS_DIR / f"{project_id}.json"
            try:
                with open(target_proj_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
            except Exception as e:
                print(f"[TV Server] Error persisting project broadcast: {e}")

            response = {
                "status": "SUCCESS",
                "message": "Broadcast show package successfully deployed to Sovereign TV Playout Stage",
                "project_id": project_id,
                "broadcast_title": data.get("broadcast_title", "Sovereign Master Broadcast"),
                "frames_count": len(data.get("frames", [])),
                "audio_url": data.get("audio_url"),
                "playout_url": f"http://127.0.0.1:{PORT}/stage?project_id={project_id}",
                "timestamp": sys.float_info.max
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        # 2. Default feature execution (n8n integration)
        action = data.get("action", "assemble_broadcast_package")
        payload = data.get("payload", data)
        res = engine.execute_feature(action, payload)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(res).encode("utf-8"))

    def log_message(self, format, *args):
        # Concise logging
        pass


def run():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), BroadcastPlayoutHandler)
    print(f"[TV Broadcast Station] Webhook Adapter & Playout Stage listening on http://0.0.0.0:{PORT}")
    print(f" -> Stage Player UI available at: http://127.0.0.1:{PORT}/stage")
    server.serve_forever()


if __name__ == "__main__":
    run()