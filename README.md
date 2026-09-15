# Sovereign TV Broadcast Station (`sovereign-tv-broadcast-station`)

[![Port](https://img.shields.io/badge/Port-8812-blue.svg)](n8n/webhook_adapter.py)
[![Architecture](https://img.shields.io/badge/Tier-1_Production_Ready-brightgreen.svg)](ROADMAP.md)
[![Status](https://img.shields.io/badge/Status-HEALTHY-success.svg)](http://127.0.0.1:8812/health)

A high-performance 16:9 cinematic video playout and visual stage broadcast microservice. Designed for autonomous television channels, live virtual news broadcasting, and automated Save the Cat! storyboard production streaming.

---

## 📺 Features & Capabilities

1. **Master Stage Cinematic Player (`GET /stage?project_id=<id>`)**:
   - High-fidelity 16:9 widescreen stage canvas with dual-layer Ken Burns pan/zoom crossfading (800ms transition time).
   - Interactive 15-beat Save the Cat! timeline scrubber with instant frame navigation and state retention.
   - Real-time camera optics HUD telemetry (18mm Ultra-Wide, 35mm Master Prime, 85mm Portrait, aperture, ISO, and shutter speed).
   - Teleprompter cue-card rundown with automatic active-beat text highlighting and script scrolling.
   - Dynamic lower-third character generator (CG) breaking news crawl ticker.

2. **Web Audio Sub-Second Synchronization Engine**:
   - Built on the HTML5 Web Audio API with sub-second `timeupdate` listeners.
   - Automatically synchronizes visual story frames with uploaded voiceover/audio narration down to the millisecond.
   - Paced according to Blake Snyder's proportional beat timing distribution (Opening Image through Final Image).

3. **Byte-Range Media & Audio Streaming**:
   - HTTP `206 Partial Content` audio streaming for high-bitrate MP3/WAV tracks with instant seeking and scrubbing.
   - Reverse-proxy and local media mounting for high-resolution 16:9 UHD visual assets.

4. **Multi-Camera Control Room Routing**:
   - Direct support for 4 virtual studio camera angles (Wide Studio, News Desk Close-Up, Floor Camera, Overhead Grid).
   - Live switching controls integrated directly into the Sovereign Studio desktop console.

---

## 🔌 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Returns service health, uptime, aspect ratio, and active studio cameras. |
| `GET` | `/stage` | Serves the HTML5 16:9 Master Stage player interface. |
| `POST` | `/api/v1/broadcast/deploy` | Ingests and activates a new multi-frame broadcast package. |
| `GET` | `/api/v1/broadcast/current` | Retrieves the currently deployed live on-air broadcast payload. |
| `GET` | `/api/v1/broadcast/project/{id}` | Retrieves a specific project broadcast package from cache. |
| `POST` | `/api/v1/execute` | Standard n8n microservice execution endpoint (stage sequencing, ticker update). |
| `GET` | `/audio/{filename}` | Byte-range streaming audio server for show narration and music tracks. |
| `GET` | `/media/{filename}` | Static media file server for generated storyboard images. |

---

## ⚡ Integration with n8n & Sovereign Studio

- **n8n Workflow `PKG-037`**: Receives project audio, recalculates beat boundaries, and deploys the entire package directly to `POST /api/v1/broadcast/deploy`.
- **Sovereign Studio Desktop App**: Embeds `http://127.0.0.1:8812/stage` inside the `TV Control Room` tab using a native macOS WebKit view with hot-reload triggers.

---

## 🛠️ Playout Server Command

```bash
# Start the TV Broadcast Station server on Port 8812
python3 solutions/tv-broadcast-station/n8n/webhook_adapter.py
```
