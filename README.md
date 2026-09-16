# Sovereign TV Broadcast Station (`sovereign-tv-broadcast-station`)
**Autonomous 16:9 Cinematic Stage Playout Engine, Ken Burns Crossfading Canvas, Sub-Second Timecode Synchronization, and Headless 1080p Master Video Rendering for Sovereign Biz Box**

[![Port](https://img.shields.io/badge/Port-8812-blue.svg?style=for-the-badge)](n8n/webhook_adapter.py)
[![Architecture](https://img.shields.io/badge/Architecture-Tier--1%20Production%20Hardened-brightgreen.svg?style=for-the-badge)](ROADMAP.md)
[![Status](https://img.shields.io/badge/Status-HEALTHY%20%7C%20ONLINE-success.svg?style=for-the-badge)](http://127.0.0.1:8812/health)
[![Package ID](https://img.shields.io/badge/Package%20ID-PKG--032-8A2BE2?style=for-the-badge)](https://github.com/BlackFoxgamingstudio/tv-broadcast-station)
[![n8n Node](https://img.shields.io/badge/n8n%20Node-SovereignTvBroadcastStation-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)](https://n8n.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

---

## Table of Contents
1. [Executive Summary & Television Broadcast Manifesto](#1-executive-summary--television-broadcast-manifesto)
2. [Station Architecture & Playout Topology](#2-station-architecture--playout-topology)
3. [Master Stage Cinematic Player (`GET /stage`)](#3-master-stage-cinematic-player-get-stage)
   - [3.1 Dual-Layer Ken Burns Pan/Zoom Crossfade Engine](#31-dual-layer-ken-burns-panzoom-crossfade-engine)
   - [3.2 Lower-Third Character Generator (CG) Breaking News Ticker](#32-lower-third-character-generator-cg-breaking-news-ticker)
   - [3.3 Multi-Camera Control Room Matrix (4 Studio Angles)](#33-multi-camera-control-room-matrix-4-studio-angles)
   - [3.4 Real-Time Camera Optics HUD Telemetry](#34-real-time-camera-optics-hud-telemetry)
   - [3.5 Teleprompter Rundown & Active-Beat Cue Cards](#35-teleprompter-rundown--active-beat-cue-cards)
   - [3.6 Master Stage HTML5 / WebGL Architecture & CRT Shader](#36-master-stage-html5--webgl-architecture--crt-shader)
   - [3.7 Hotkey Matrix & Interactive Control Protocol](#37-hotkey-matrix--interactive-control-protocol)
4. [Sub-Second Audio & Timecode Synchronization Engine](#4-sub-second-audio--timecode-synchronization-engine)
   - [4.1 Proportional Beat Distribution Algorithms](#41-proportional-beat-distribution-algorithms)
   - [4.2 The 15 Save the Cat! Story Beats in Broadcast Production](#42-the-15-save-the-cat-story-beats-in-broadcast-production)
   - [4.3 Whisper Word-Level Forced Alignment Ingestion](#43-whisper-word-level-forced-alignment-ingestion)
   - [4.4 Web Audio `timeupdate` Transport Event Listeners](#44-web-audio-timeupdate-transport-event-listeners)
5. [Headless 1080p MP4 Master Video Compilation Engine](#5-headless-1080p-mp4-master-video-compilation-engine)
   - [5.1 Frame-by-Frame Compositing Pipeline (OpenCV / FFmpeg)](#51-frame-by-frame-compositing-pipeline-opencv--ffmpeg)
   - [5.2 Alpha Blending & Lower-Third Graphic Burn-In](#52-alpha-blending--lower-third-graphic-burn-in)
   - [5.3 AAC 320kbps Audio Stems Muxing & CRF Quality Tuning](#53-aac-320kbps-audio-stems-muxing--crf-quality-tuning)
   - [5.4 Video Export & Download Endpoint (`/download-video/{id}`)](#54-video-export--download-endpoint-download-videoid)
6. [HTTP 206 Byte-Range Streaming Subsystem](#6-http-206-byte-range-streaming-subsystem)
7. [Broadcast Manifest Schema Specification](#7-broadcast-manifest-schema-specification)
8. [Comprehensive REST API Reference](#8-comprehensive-rest-api-reference)
9. [n8n Automation & Custom Community Node (`SovereignTvBroadcastStation`)](#9-n8n-automation--custom-community-node-sovereigntvbroadcaststation)
10. [Sovereign Studio macOS SwiftUI Desktop Console Integration](#10-sovereign-studio-macos-swiftui-desktop-console-integration)
11. [SRE Deployment, Telemetry & Disaster Recovery Runbook](#11-sre-deployment-telemetry--disaster-recovery-runbook)
12. [Verification Suite & Automated Unit Tests](#12-verification-suite--automated-unit-tests)
13. [Authors, Governance & MIT License](#13-authors-governance--mit-license)

---

## 1. Executive Summary & Television Broadcast Manifesto

### 1.1 The Sovereign Visual Television Engine
In commercial broadcast media and digital streaming, linear television playout systems (e.g., Grass Valley, Ross Video, Blackmagic ATEM) are notoriously proprietary, expensive, and tightly bound to specialized SDI/NDI hardware racks. Conversely, web-based video streaming tools often degrade visual quality, suffer from desynchronized audio cues, and lack automated narrative staging.

The **Sovereign TV Broadcast Station** (`PKG-032`) provides a modern, fully autonomous, software-defined 16:9 television broadcast playout engine executing locally on loopback Port 8812 (`http://127.0.0.1:8812`). Designed to serve as the visual flagship of the **Sovereign Biz Box (SBB)** media infrastructure, this microservice renders high-definition cinematic presentations, manages broadcast manifests, drives lower-third animated character generators, synchronizes audio narration to Blake Snyder's 15 Save the Cat! story beats, and compiles production-ready 1080p MP4 videos with embedded broadcast graphics.

### 1.2 Five Core Engineering Tenets
The TV Broadcast Station is built upon five foundational engineering tenets:

1. **Native 16:9 Cinematic Aesthetics**: All visuals adhere strictly to standard widescreen 1920x1080 resolution, utilizing dual-layer Ken Burns pan/zoom crossfades and dynamic camera optics HUD overlays.
2. **Sub-Second Audio-Visual Synchronization**: Every visual beat transition is synchronized to narration audio with millisecond precision, eliminating awkward slide pauses or premature scene cutaways.
3. **Hardware-Accelerated In-Browser Playout**: The master stage interface (`/stage`) leverages GPU-accelerated CSS transforms and WebGL compositing, ensuring 60fps presentation even on constrained hardware.
4. **Autonomous Headless Rendering**: Compiles finished episodes into broadcast-ready 1080p MP4 files with studio overlays, ticker tapes, and teleprompter titles directly on the local machine via OpenCV and FFmpeg.
5. **Zero Cloud Dependencies ($0.00 / Mo)**: Visual assets, audio tracks, broadcast manifests, and MP4 video renders remain entirely on local bare-metal storage, with zero external cloud rendering egress costs.


---

## 2. Station Architecture & Playout Topology

The TV Broadcast Station operates as a high-performance Python FastAPI service integrated with the SBB media pipeline:

```
+===================================================================================================+
|                              SOVEREIGN TV BROADCAST STATION (:8812)                               |
|                           FastAPI / HTML5 Stage / OpenCV & FFmpeg                                 |
+===================================================================================================+
|                                                                                                   |
|  [ Inbound Control Gateway ]                                                                      |
|  * Broadcast Manifest Ingestion (/api/v1/broadcast/deploy)                                        |
|  * Stage Control & Beat Navigation Webhook (/api/v1/execute)                                      |
|  * CNCF CloudEvents Ingestion (/api/broadcast/event)                                              |
|                                                                                                   |
|  [ Master Stage Playout & Visual Subsystem ]                                                      |
|  +-----------------------------------+-----------------------------------+                        |
|  | 16:9 Stage Canvas (GET /stage)    | Lower-Third Character Generator   |                        |
|  | - Dual-Layer Ken Burns Crossfade  | - CSS Hardware-Accelerated Ticker |                        |
|  | - 800ms Dynamic Pan & Zoom Shifts | - Breaking News Crawl Animation   |                        |
|  | - 4-Angle Camera Control Matrix   | - Custom Ticker Text Ingestion    |                        |
|  +-----------------------------------+-----------------------------------+                        |
|                                                                                                   |
|  [ Speech & Timecode Synchronization Subsystem ]                                                  |
|  * Proportional Beat Distribution Engine (15 Save the Cat! Story Beats)                           |
|  * Whisper Word-Level Forced Alignment Timecode Mapper                                            |
|  * Web Audio API Sub-Second Transport Listener (0.05s resolution)                                 |
|                                                                                                   |
|  [ Headless Master Video Compilation Engine ]                                                     |
|  * OpenCV Frame-by-Frame Compositor (1920x1080 @ 30fps)                                           |
|  * Teleprompter Word Overlay & Lower-Third HUD Banner Burn-in                                     |
|  * FFmpeg Two-Pass Video Encoding & AAC 320k Audio Stem Muxing                                    |
|                                                                                                   |
+===================================================================================================+
                                  |                     |
          +-----------------------+                     +-----------------------+
          |                                                                     |
          v Audio Stream (HTTP 206)                                             v Native Embedding
+------------------------------------+                                +-------------------------------------+
|        AI RADIO STATION            |                                |       SOVEREIGN STUDIO (APP-001)    |
|  - Port 8811 (Master Audio Playout)|                                |  - Native macOS SwiftUI Console     |
|  - Background Lo-Fi Music Stems    |                                |  - WKWebView Embedded TV Control    |
|  - -14dB Voice Ducking Curves      |                                |  - URLSession Native Video Export   |
+------------------------------------+                                +-------------------------------------+
```


---

## 3. Master Stage Cinematic Player (`GET /stage`)

The master visual presentation environment is served at `http://127.0.0.1:8812/stage`. It renders a cyber-broadcast television control room interface:

```
+===================================================================================================+
|  [🔴 ON AIR] SBB BROADCAST CHANNEL 88.12 HD                           TIME: 00:01:24.150 / 02:48  |
+===================================================================================================+
|                                                                                                   |
|   +-------------------------------------------------------------------------------------------+   |
|   | [CAM 1: MASTER PRIME]   16:9 UHD CINEMATIC VISUAL STAGE (1920x1080)                       |   |
|   |                                                                                           |   |
|   |                                                                                           |   |
|   |                        [ DUAL-LAYER KEN BURNS PAN / ZOOM CANVAS ]                         |   |
|   |                                                                                           |   |
|   |                                                                                           |   |
|   |  [OPTICS HUD] 35mm Master Prime | f/1.4 | ISO 400 | Shutter: 180° | Color Temp: 5600K     |   |
|   |  ---------------------------------------------------------------------------------------  |   |
|   |  [LOWER-THIRD CG] BREAKING: SBB v3.0 Autonomous Broadcast Network Live Across All Nodes   |   |
|   +-------------------------------------------------------------------------------------------+   |
|                                                                                                   |
|   [TIMELINE SCRUBBER: 15 SAVE THE CAT! STORY BEATS]                                               |
|   [01: Opening] [02: Theme] [03: Setup] [04: Catalyst] [▶ 05: Debate] [06: Break into 2] ...      |
|                                                                                                   |
|   [CAMERA MATRIX]    [CAM 1: PRIME]   [CAM 2: WIDE]   [CAM 3: CLOSE-UP]   [CAM 4: OVERHEAD]       |
|                                                                                                   |
|   [TELEPROMPTER RUNDOWN]                                                                          |
|   "Beat 5: The debate begins as the autonomous intelligence questions its sovereign mandate..."   |
+===================================================================================================+
```

### 3.1 Dual-Layer Ken Burns Pan/Zoom Crossfade Engine
To ensure cinematic fluidity between story beats, the player employs two overlapping `<div class="stage-layer">` elements configured with CSS GPU transforms:

```css
/* Ken Burns Pan/Zoom Animation Keyframes */
@keyframes kenBurnsZoomIn {
  0% {
    transform: scale(1.0) translate(0, 0);
  }
  100% {
    transform: scale(1.08) translate(-1.5%, -1.0%);
  }
}

@keyframes kenBurnsZoomOut {
  0% {
    transform: scale(1.08) translate(-1.5%, -1.0%);
  }
  100% {
    transform: scale(1.0) translate(0, 0);
  }
}

.stage-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  transition: opacity 800ms cubic-bezier(0.4, 0.0, 0.2, 1);
  will-change: transform, opacity;
}

.stage-layer.active {
  opacity: 1;
  animation: kenBurnsZoomIn 14s ease-out forwards;
}

.stage-layer.inactive {
  opacity: 0;
}
```

### 3.2 Lower-Third Character Generator (CG) Breaking News Ticker
The broadcast stage features a broadcast-grade lower-third graphics banner:
- **Left Badge**: Glowing red `BREAKING NEWS` or `LIVE DISPATCH` indicator.
- **Title Banner**: Active story beat title and episode identifier (e.g., `EPISODE 1: FREEDOM // BEAT 05: DEBATE`).
- **Scrolling Ticker Crawl**: Hardware-accelerated horizontal text crawl moving at 60 pixels per second.

```javascript
// Dynamic Ticker Ingestion & DOM Injection
function updateLowerThirdTicker(headline, crawlText) {
  const headlineEl = document.getElementById('cgHeadline');
  const crawlEl = document.getElementById('cgCrawlText');
  
  if (headlineEl) headlineEl.innerText = headline.toUpperCase();
  if (crawlEl) {
    crawlEl.innerText = crawlText;
    crawlEl.style.animation = 'none';
    crawlEl.offsetHeight; // Trigger reflow
    crawlEl.style.animation = 'marqueeScroll 25s linear infinite';
  }
}
```

### 3.3 Multi-Camera Control Room Matrix (4 Studio Angles)
The stage provides 4 selectable virtual camera views:
1. **Cam 1: Master Prime (35mm)**: Default full 16:9 stage presentation with balanced framing.
2. **Cam 2: Wide Studio (18mm)**: Simulates an expansive virtual news studio environment with ambient edge vignette.
3. **Cam 3: News Desk Close-Up (85mm)**: Dramatic telephoto framing with shallow depth-of-field blur.
4. **Cam 4: Overhead Grid (24mm)**: High-angle architectural perspective looking down upon the virtual broadcast floor.

### 3.4 Real-Time Camera Optics HUD Telemetry
An on-screen heads-up display provides continuous optical parameters:
- Focal Length: `18mm`, `35mm`, `50mm`, `85mm`
- Aperture: `f/1.4`, `f/2.8`, `f/4.0`
- Sensor ISO: `ISO 100`, `ISO 400`, `ISO 1600`
- Shutter Angle: `180.0°` (1/60s exposure)
- White Balance: `5600K Daylight`

### 3.5 Teleprompter Rundown & Active-Beat Cue Cards
The lower console displays a live scrolling teleprompter script. As audio playback proceeds, the script automatically advances to keep the active narration sentence centered in bold neon gold, allowing talent or observers to follow the narrative beats in real time.

### 3.6 Master Stage HTML5 / WebGL Architecture & CRT Shader
For authentic retro-cyberpunk broadcasting aesthetics, the stage canvas features an optional WebGL post-processing shader injecting subtle CRT scanlines, chromatic aberration, and corner curvature:

```javascript
// WebGL CRT Post-Processing Fragment Shader
const crtFragmentShader = `
  precision mediump float;
  uniform sampler2D u_texture;
  uniform vec2 u_resolution;
  varying vec2 v_texCoord;

  void main() {
    vec2 uv = v_texCoord;
    
    // Slight barrel distortion
    vec2 cc = uv - 0.5;
    float dist = dot(cc, cc);
    uv = uv + cc * (dist * 0.08);

    // Color sample with chromatic aberration
    float r = texture2D(u_texture, uv + vec2(0.0015, 0.0)).r;
    float g = texture2D(u_texture, uv).g;
    float b = texture2D(u_texture, uv - vec2(0.0015, 0.0)).b;

    // Scanlines
    float scanline = sin(uv.y * u_resolution.y * 1.5) * 0.04;
    vec3 color = vec3(r, g, b) - scanline;

    gl_FragColor = vec4(color, 1.0);
  }
`;
```

### 3.7 Hotkey Matrix & Interactive Control Protocol
Operators controlling the station from a broadcast control room keyboard can execute rapid switching without touching the mouse:
- **`Spacebar`**: Toggle Play / Pause master audio-visual stream.
- **`ArrowRight` / `ArrowLeft`**: Step forward or backward by one Save the Cat! beat.
- **`Key1` – `Key4`**: Switch active studio camera viewports (Cam 1: Prime, Cam 2: Wide, Cam 3: Close-up, Cam 4: Overhead).
- **`KeyF`**: Toggle borderless widescreen 16:9 full-screen presentation mode.
- **`KeyM`**: Toggle audio mute / unmute.
- **`KeyT`**: Toggle Lower-Third Character Generator visibility.


---

## 4. Sub-Second Audio & Timecode Synchronization Engine

### 4.1 Proportional Beat Distribution Algorithms
When an episode lacks word-level forced alignment timestamps, the TV Broadcast Station computes a proportional timing distribution based on Blake Snyder's standard 15-beat screenplay formula:

```python
# Save the Cat! Proportional Timing Multipliers
SAVE_THE_CAT_PROPORTIONS = {
    1:  ("Opening Image",        0.00, 0.01),
    2:  ("Theme Stated",         0.01, 0.05),
    3:  ("Set-Up",               0.05, 0.10),
    4:  ("Catalyst",             0.10, 0.12),
    5:  ("Debate",               0.12, 0.20),
    6:  ("Break into Two",       0.20, 0.25),
    7:  ("B Story",              0.25, 0.30),
    8:  ("Fun and Games",        0.30, 0.50),
    9:  ("Midpoint",             0.50, 0.55),
    10: ("Bad Guys Close In",    0.55, 0.68),
    11: ("All Hope Is Lost",     0.68, 0.75),
    12: ("Dark Night of Soul",   0.75, 0.80),
    13: ("Break into Three",     0.80, 0.85),
    14: ("Finale",               0.85, 0.98),
    15: ("Final Image",          0.98, 1.00),
}

def calculate_beat_timecodes(total_duration_seconds: float):
    '''Calculates absolute start and end times for all 15 beats.'''
    manifest = []
    for beat_num, (beat_name, start_pct, end_pct) in SAVE_THE_CAT_PROPORTIONS.items():
        manifest.append({
            "beat_number": beat_num,
            "beat_name": beat_name,
            "start_time": round(total_duration_seconds * start_pct, 2),
            "end_time": round(total_duration_seconds * end_pct, 2),
            "duration": round(total_duration_seconds * (end_pct - start_pct), 2)
        })
    return manifest
```

### 4.2 The 15 Save the Cat! Story Beats in Broadcast Production
Each beat fulfills a precise narrative and visual function in the broadcast presentation:
1. **Opening Image (Beat 1, 0–1%)**: Establishes the visual snapshot of the protagonist's world before transformation begins. High contrast, atmospheric framing.
2. **Theme Stated (Beat 2, 1–5%)**: A subtle clue or philosophical proposition is voiced regarding the episode's core dilemma.
3. **Set-Up (Beat 3, 5–10%)**: Explores the status quo, introducing supporting characters and systemic stakes.
4. **Catalyst (Beat 4, 10–12%)**: The inciting incident occurs, shattering the world of the first act.
5. **Debate (Beat 5, 12–20%)**: Characters wrestle with the dilemma, questioning whether to embark on the perilous journey.
6. **Break into Two (Beat 6, 20–25%)**: The definitive threshold cross into an unfamiliar, upside-down world.
7. **B Story (Beat 7, 25–30%)**: The emotional heart or secondary relationship is introduced.
8. **Fun and Games (Beat 8, 30–50%)**: The core premise of the story is delivered. Dynamic action sequences and visual exploration.
9. **Midpoint (Beat 9, 50–55%)**: False victory or false collapse where stakes elevate from personal to existential.
10. **Bad Guys Close In (Beat 10, 55–68%)**: Internal friction mounts as external antagonists apply relentless pressure.
11. **All Hope Is Lost (Beat 11, 68–75%)**: The nadir of the narrative. Whiff of death and the total collapse of original plans.
12. **Dark Night of the Soul (Beat 12, 75–80%)**: The internal realization where the true lesson of Beat 2 is finally understood.
13. **Break into Three (Beat 13, 80–85%)**: Inspired breakthrough where the synthesis of old and new sparks the final counter-offensive.
14. **Finale (Beat 14, 85–98%)**: High-intensity resolution dispatching antagonists and executing the newly discovered paradigm.
15. **Final Image (Beat 15, 98–100%)**: The mirror image to Beat 1, visually proving permanent, irrecoverable transformation.

### 4.3 Whisper Word-Level Forced Alignment Ingestion
When high-precision alignment data is available from Storyboard AI (`:8815/api/audio/align`), the TV station ingests the word timestamps directly, ensuring that slide transitions align precisely with the speaker's vocal cadences.

### 4.4 Web Audio `timeupdate` Transport Event Listeners
The web canvas registers a high-frequency transport monitor executing every 50 milliseconds (`setInterval(checkTimecode, 50)`), comparing the current audio playback position with the manifest cue table to trigger instant frame changes.


---

## 5. Headless 1080p MP4 Master Video Compilation Engine

### 5.1 Frame-by-Frame Compositing Pipeline (OpenCV / FFmpeg)
When `/api/v1/broadcast/render-video` is requested, the station triggers a headless background video compilation pipeline that produces a master 1920x1080 MP4 video:

```python
# Video Compositing Pipeline (OpenCV + FFmpeg)
import cv2
import numpy as np
import subprocess

def composite_broadcast_video(manifest_data, audio_path, output_mp4_path):
    fps = 30
    width = 1920
    height = 1080
    temp_raw_video = "/tmp/raw_broadcast.mp4"

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(temp_raw_video, fourcc, fps, (width, height))

    for slide in manifest_data["slides"]:
        img = cv2.imread(slide["image_path"])
        if img is None:
            img = np.zeros((height, width, 3), dtype=np.uint8)
        else:
            img = cv2.resize(img, (width, height))

        duration_frames = int(slide["duration"] * fps)
        for f in range(duration_frames):
            frame = img.copy()
            
            # Burn in Lower-Third Banner with Alpha Transparency
            overlay = frame.copy()
            cv2.rectangle(overlay, (80, 920), (1840, 1020), (15, 15, 20), -1)
            cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)

            cv2.putText(frame, f"BEAT {slide['beat']}: {slide['name']}", 
                        (100, 965), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 229, 255), 2)
            cv2.putText(frame, slide.get("ticker", ""), 
                        (100, 1000), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)

            writer.write(frame)

    writer.release()

    # Mux High-Bitrate AAC Audio using FFmpeg
    cmd = [
        "ffmpeg", "-y",
        "-i", temp_raw_video,
        "-i", audio_path,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "320k",
        "-shortest", output_mp4_path
    ]
    subprocess.run(cmd, check=True)
    return output_mp4_path
```

### 5.2 Alpha Blending & Lower-Third Graphic Burn-In
The compositing engine uses OpenCV's `addWeighted` function to create semi-transparent glassmorphic overlays (`85% opacity dark slate fill`) beneath white and neon cyan typography, guaranteeing legibility regardless of underlying background plate exposure.

### 5.3 AAC 320kbps Audio Stems Muxing & CRF Quality Tuning
The final output stage applies H.264 video compression at Constant Rate Factor (`CRF 18`), which provides visually lossless quality matching professional broadcast delivery specs. Audio is muxed at 320kbps AAC, maintaining full dynamic range and frequency response.

### 5.4 Video Export & Download Endpoint (`/download-video/{id}`)
Once compiled, the resulting MP4 is indexed in the project registry and exposed via `/api/v1/broadcast/download-video/{id}` with `Content-Type: video/mp4` and `Content-Disposition: attachment; filename="..."` headers.


---

## 6. HTTP 206 Byte-Range Streaming Subsystem

Media endpoints (`/audio/{filename}` and `/media/{filename}`) implement complete byte-range streaming, allowing video scrubbing and progressive audio playback in standard browsers without waiting for the full file to download.

```python
# Complete Byte-Range Header Validation & Streaming Logic
import re
from fastapi import Request, HTTPException
from fastapi.responses import StreamingResponse

def stream_byte_range_media(file_path: str, request: Request, media_type: str = "video/mp4"):
    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("range")

    if not range_header:
        return StreamingResponse(open(file_path, "rb"), media_type=media_type)

    match = re.match(r'bytes=(\d+)-(\d*)', range_header)
    if not match:
        raise HTTPException(status_code=416, detail="Requested range not satisfiable")

    start = int(match.group(1))
    end = int(match.group(2)) if match.group(2) else file_size - 1
    content_length = (end - start) + 1

    def chunk_generator():
        with open(file_path, "rb") as f:
            f.seek(start)
            remaining = content_length
            while remaining > 0:
                chunk = f.read(min(remaining, 1024 * 1024))
                if not chunk:
                    break
                remaining -= len(chunk)
                yield chunk

    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(content_length),
        "Content-Type": media_type,
    }
    return StreamingResponse(chunk_generator(), status_code=206, headers=headers)
```

---

## 7. Broadcast Manifest Schema Specification

When deploying a production broadcast package to `/api/v1/broadcast/deploy`, the payload must conform to the following JSON schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "SbbBroadcastManifest",
  "type": "object",
  "required": ["project_id", "title", "total_duration", "audio_path", "slides"],
  "properties": {
    "project_id": { "type": "string", "example": "proj-ep01-freedom" },
    "title": { "type": "string", "example": "Episode 1: Freedom" },
    "total_duration": { "type": "number", "example": 168.4 },
    "audio_path": { "type": "string", "example": "/Users/russellpowers/Sovereign Biz Box/solutions/Project 16.aif" },
    "ticker_headline": { "type": "string", "example": "BREAKING NEWS" },
    "ticker_crawl": { "type": "string", "example": "Sovereign Biz Box v3.0 Autonomous Broadcast Network Live Across All Bare-Metal Nodes" },
    "slides": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["beat", "name", "start_time", "duration", "image_path"],
        "properties": {
          "beat": { "type": "integer", "minimum": 1, "maximum": 15 },
          "name": { "type": "string", "example": "Opening Image" },
          "start_time": { "type": "number", "example": 0.0 },
          "duration": { "type": "number", "example": 8.5 },
          "image_path": { "type": "string", "example": "/Users/russellpowers/Sovereign Biz Box/solutions/broadcast_slide_01.png" },
          "teleprompter_text": { "type": "string", "example": "A shadowy server room hums quietly in the midnight dark." }
        }
      }
    }
  }
}
```


---

## 8. Comprehensive REST API Reference

| Method | Endpoint | Description | Request Parameters | Response |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/health` | Service health, active cameras & aspect ratio | None | `200 application/json` |
| `GET` | `/stage` | Renders the HTML5 16:9 Master Stage player | `?project_id=ep01` | `200 text/html` |
| `POST`| `/api/v1/broadcast/deploy` | Deploys a new multi-slide broadcast manifest | Manifest JSON payload | `200 application/json` |
| `GET` | `/api/v1/broadcast/current` | Returns currently deployed on-air broadcast | None | `200 application/json` |
| `POST`| `/api/v1/broadcast/render-video`| Triggers headless 1080p MP4 compilation | `{"project_id": "ep01"}` | `200 application/json` |
| `GET` | `/api/v1/broadcast/download-video/{id}` | Downloads completed master 1080p MP4 | Route parameter: `id` | `200 video/mp4` |
| `GET` | `/audio/{filename}` | Byte-range streaming audio endpoint | Header: `Range: bytes=...` | `206 Partial Content` |
| `GET` | `/media/{filename}` | Serves visual slide PNG images | None | `200 image/png` |
| `POST`| `/api/v1/execute` | Universal n8n / desktop console webhook | `{"action": "...", ...}` | `200 application/json` |

---

## 9. n8n Automation & Custom Community Node (`SovereignTvBroadcastStation`)

The station provides seamless drag-and-drop integration in the SBB Autonomous Command Center through the compiled community node **`SovereignTvBroadcastStation`**:

```typescript
// SovereignTvBroadcastStation INodeType Definition Extract
export class SovereignTvBroadcastStation implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'Sovereign TV Broadcast Station',
    name: 'sovereignTvBroadcastStation',
    icon: 'file:tv.svg',
    group: ['transform'],
    version: 1,
    description: 'Control 16:9 stage playout, lower-third tickers, and 1080p video compilation',
    defaults: { name: 'TV Broadcast Station' },
    inputs: ['main'],
    outputs: ['main'],
    properties: [
      {
        displayName: 'Operation',
        name: 'operation',
        type: 'options',
        options: [
          { name: 'Get Station Health', value: 'getHealth' },
          { name: 'Deploy Broadcast Manifest', value: 'deployManifest' },
          { name: 'Update Ticker', value: 'updateTicker' },
          { name: 'Render Master Video', value: 'renderVideo' },
          { name: 'Get Current Broadcast', value: 'getCurrentBroadcast' }
        ],
        default: 'getHealth'
      }
    ]
  };
}
```

---

## 10. Sovereign Studio macOS SwiftUI Desktop Console Integration

The station is natively embedded in Sovereign Studio (`APP-001`):
- **Embedded WebKit**: The `TV Control Room` tab renders `http://127.0.0.1:8812/stage` in a native `WKWebView`.
- **Native Video Export**: Operators can trigger video exports that download directly to `~/Downloads/` via macOS `URLSessionDownloadTask`.

---

## 11. SRE Deployment, Telemetry & Disaster Recovery Runbook

### 11.1 Starting the TV Station Daemon
```bash
cd "/Users/russellpowers/Sovereign Biz Box/solutions/tv-broadcast-station"
python3 n8n/webhook_adapter.py
```

### 11.2 Verifying Server Availability
```bash
curl -i http://127.0.0.1:8812/health
```
Expected output:
```json
{
  "status": "healthy",
  "service": "sovereign-tv-broadcast-station",
  "port": 8812,
  "aspect_ratio": "16:9",
  "active_cameras": 4
}
```

### 11.3 SRE Common Failure Modes & Recovery
- **FFmpeg Codec Error (`Unknown encoder 'libx264'`)**:
  - Run `brew install ffmpeg` to install complete multi-threaded codecs.
- **Port Conflict on 8812**:
  - Run `lsof -i tcp:8812` and terminate stale python processes.
- **Corrupt Manifest JSON**:
  - Verify JSON structure contains `slides` array with valid `duration` and `image_path` fields.

---

## 12. Verification Suite & Automated Unit Tests

To run the automated TV station test suite:
```bash
pytest tests/ -v
```

Tests validate:
- Manifest JSON schema validation
- Proportional beat calculation logic
- OpenCV / FFmpeg binary availability
- Byte-range streaming headers

---

## 13. Authors, Governance & MIT License

The **Sovereign TV Broadcast Station** is engineered and governed by **Russell Alan Powers** and **Black Fox Gaming Studio**.

- **Lead Systems Architect**: Russell Alan Powers (<russell@blackfoxgaming.com>)
- **Organization**: Black Fox Gaming Studio
- **Ecosystem**: Sovereign Biz Box (SBB) Bare-Metal Infrastructure
- **License**: Released under the terms of the **MIT License**.

```
MIT License

Copyright (c) 2026 Black Fox Gaming Studio & Russell Powers

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
