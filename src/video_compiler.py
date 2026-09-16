"""
Sovereign TV Broadcast Station — Video Compiler Engine
Compiles 16:9 1080p YouTube-Ready MP4 Videos from Save the Cat! Beat Visuals & Logic Pro AIFF Soundtracks.
"""
import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from PIL import Image, ImageDraw, ImageFont

FFMPEG_BIN = "/opt/homebrew/bin/ffmpeg" if os.path.exists("/opt/homebrew/bin/ffmpeg") else "ffmpeg"
BACKEND_DIR = Path("/Users/russellpowers/Library/Mobile Documents/com~apple~CloudDocs/codingprojects/workingstoryboardai/backend")
DOWNLOADS_DIR = Path.home() / "Downloads"

class VideoCompiler:
    """Automates rendering of broadcast storyboard presentations into 1080p YouTube MP4 videos."""

    @staticmethod
    def render_project_video(broadcast_data: Dict[str, Any], output_dir: Optional[Path] = None, force_recompile: bool = False) -> Dict[str, Any]:
        project_id = broadcast_data.get("project_id", "broadcast_presentation")
        title = broadcast_data.get("broadcast_title", project_id)
        frames = broadcast_data.get("frames", [])
        total_audio_duration = float(broadcast_data.get("audio_duration", 80.0))

        if output_dir is None:
            output_dir = Path(__file__).resolve().parent.parent / "data" / "exports"
        output_dir.mkdir(parents=True, exist_ok=True)

        safe_title = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in title)
        output_filename = f"{safe_title}_1080p.mp4"
        output_mp4 = output_dir / output_filename
        downloads_target = DOWNLOADS_DIR / output_filename

        # Fast path: If already compiled and valid (> 10MB) and not forced, check if any frame images are newer
        if not force_recompile and output_mp4.exists() and output_mp4.stat().st_size > 10 * 1024 * 1024:
            mp4_mtime = output_mp4.stat().st_mtime
            any_newer = False
            for f in frames:
                iurl = f.get("image_url", "")
                if iurl:
                    iname = Path(iurl).name
                    for test_dir in [
                        Path("/Users/russellpowers/Sovereign Biz Box/solutions/tv-broadcast-station/data/media"),
                        Path("/Users/russellpowers/Sovereign Biz Box/solutions/storyboard-ai/backend/frame_images"),
                        Path("/Users/russellpowers/Sovereign Biz Box/solutions/storyboard-ai/backend/generated_images")
                    ]:
                        cand = test_dir / iname
                        if cand.exists() and cand.stat().st_mtime > mp4_mtime:
                            any_newer = True
                            break
                if any_newer:
                    break

            if not any_newer:
                file_size_mb = round(output_mp4.stat().st_size / (1024 * 1024), 2)
                # Try to sync to Downloads - also try pid_alias name as fallback
                pid_alias_dl = DOWNLOADS_DIR / f"{project_id}_1080p.mp4"
                try:
                    # Always ensure the Downloads copy is identical to output_mp4
                    if not downloads_target.exists() or downloads_target.stat().st_mtime < output_mp4.stat().st_mtime or downloads_target.stat().st_size != output_mp4.stat().st_size:
                        shutil.copy2(output_mp4, downloads_target)
                except Exception:
                    try:
                        shutil.copy2(output_mp4, pid_alias_dl)
                    except Exception:
                        pass
                
                # Report a valid downloads_path even if title-based path doesn't exist but alias does
                dl_path = None
                if downloads_target.exists():
                    dl_path = str(downloads_target)
                elif pid_alias_dl.exists():
                    dl_path = str(pid_alias_dl)
                    
                return {
                    "status": "SUCCESS",
                    "cached": True,
                    "project_id": project_id,
                    "title": title,
                    "output_path": str(output_mp4),
                    "downloads_path": dl_path,
                    "filename": output_filename,
                    "size_mb": file_size_mb,
                    "duration_sec": total_audio_duration,
                    "resolution": "1920x1080 (1080p)",
                    "codec": "H.264 / AAC 320k (YouTube Recommended)",
                    "frames_compiled": len(frames)
                }

        tmp_dir = output_dir / f"tmp_render_{project_id}"
        tmp_dir.mkdir(parents=True, exist_ok=True)

        # Locate audio file
        audio_url = broadcast_data.get("audio_url", "")
        audio_file_path = None

        if audio_url:
            import urllib.parse
            raw_audio_filename = audio_url.split("/")[-1]
            audio_filename = urllib.parse.unquote(raw_audio_filename)
            name_variants = [audio_filename, raw_audio_filename, audio_filename.replace(" ", "_"), audio_filename.replace("_", " ")]
            
            search_dirs = [
                Path("/Users/russellpowers/Sovereign Biz Box/solutions/tv-broadcast-station/data/audio"),
                Path("/Users/russellpowers/Sovereign Biz Box/solutions/tv-broadcast-station/data"),
                Path("/Users/russellpowers/Sovereign Biz Box/solutions/storyboard-ai/backend/audio"),
                BACKEND_DIR / "audio",
                Path.home() / "Downloads"
            ]

            for sdir in search_dirs:
                if not sdir.exists():
                    continue
                for var in name_variants:
                    cand = sdir / var
                    if cand.exists() and cand.is_file():
                        audio_file_path = cand
                        break
                    # Also check m4a / aif alternative extensions
                    for ext in [".m4a", ".aif", ".aiff", ".wav", ".mp3"]:
                        cand_ext = sdir / f"{Path(var).stem}{ext}"
                        if cand_ext.exists() and cand_ext.is_file():
                            audio_file_path = cand_ext
                            break
                    if audio_file_path:
                        break
                if audio_file_path:
                    break

        # Generate prepared 1920x1080 slides for each frame
        concat_lines = []
        for i, frame in enumerate(frames):
            slide_path = tmp_dir / f"slide_{i:02d}.png"
            img_url = frame.get("image_url", "")

            # Resolve local image file
            local_img = None
            if img_url:
                rel = img_url.split(":8815/")[-1]
                parts = rel.split("/", 1)
                parts[0] = parts[0].replace("-", "_")
                candidate_paths = [
                    Path("/Users/russellpowers/Sovereign Biz Box/solutions/tv-broadcast-station/data/media") / Path(rel).name,
                    Path("/Users/russellpowers/Sovereign Biz Box/solutions/tv-broadcast-station/data/frame-images") / Path(rel).name,
                    Path("/Users/russellpowers/Sovereign Biz Box/solutions/storyboard-ai/backend/generated_images") / Path(rel).name,
                    Path("/Users/russellpowers/Sovereign Biz Box/solutions/tv-broadcast-station/data/media") / f"{frame.get('frame_id')}.png",
                    Path("/Users/russellpowers/Sovereign Biz Box/solutions/tv-broadcast-station/media") / Path(rel).name,
                    BACKEND_DIR / "/".join(parts),
                    BACKEND_DIR / "generated_images" / Path(rel).name,
                    BACKEND_DIR / "frame_images" / Path(rel).name
                ]
                for cp in candidate_paths:
                    if cp.exists():
                        try:
                            # Test if openable without permission errors
                            with open(cp, "rb") as test_f:
                                test_f.read(10)
                            local_img = cp
                            break
                        except Exception:
                            continue

            if local_img and local_img.exists():
                try:
                    im = Image.open(local_img).convert("RGB")
                    im = im.resize((1920, 1080), Image.Resampling.LANCZOS)
                except Exception:
                    local_img = None

            if not local_img:
                im = Image.new("RGB", (1920, 1080), color=(13, 18, 29))
                draw_bg = ImageDraw.Draw(im)
                draw_bg.rectangle([(0, 0), (1920, 1080)], fill=(13, 18, 29))
                draw_bg.rectangle([(80, 80), (1840, 1000)], outline=(30, 41, 59), width=3)

            # ─── Render Complete Sovereign TV Broadcast Interface & Teleprompter Words ───
            import textwrap
            
            def _get_font(fname: str, size: int):
                for path in [
                    f"/System/Library/Fonts/Supplemental/{fname}.ttf",
                    f"/System/Library/Fonts/{fname}.ttf",
                    "/System/Library/Fonts/Supplemental/Arial.ttf",
                    "/System/Library/Fonts/Helvetica.ttc"
                ]:
                    if os.path.exists(path):
                        try:
                            return ImageFont.truetype(path, size)
                        except Exception:
                            pass
                return ImageFont.load_default()

            font_title = _get_font("Arial Bold", 24)
            font_badge = _get_font("Arial Bold", 16)
            font_optics = _get_font("Arial Bold", 18)
            font_banner = _get_font("Arial Bold", 20)
            font_sub = _get_font("Arial", 24)
            font_ticker = _get_font("Arial Bold", 19)

            overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)

            # 1. Top HUD Bar
            # Subtle dark gradient across top 110px
            for y in range(110):
                alpha = int(220 * (1 - y / 110))
                draw.line([(0, y), (1920, y)], fill=(7, 7, 12, alpha))

            # LIVE ON AIR badge
            draw.rounded_rectangle([(40, 28), (170, 72)], radius=6, fill=(255, 0, 68, 230))
            draw.ellipse([(52, 45), (62, 55)], fill=(255, 255, 255, 255))
            draw.text((70, 39), "LIVE ON AIR", font=font_badge, fill=(255, 255, 255, 255))

            # Show Title
            show_title = title.upper()
            draw.text((190, 39), show_title, font=font_title, fill=(255, 255, 255, 255))

            # Optics Badge
            shot_optics = frame.get("shot_type") or "Cinematic 16:9 Widescreen (35mm Lens)"
            optics_text = f"OPTICS: {shot_optics}"
            if len(optics_text) > 55:
                optics_text = optics_text[:52] + "..."
            optics_bbox = draw.textbbox((0, 0), optics_text, font=font_optics)
            optics_w = optics_bbox[2] - optics_bbox[0] + 30
            opt_x1 = 1920 - 40 - optics_w
            draw.rounded_rectangle([(opt_x1, 28), (1920 - 40, 72)], radius=6, fill=(13, 18, 29, 210), outline=(0, 210, 255, 255), width=2)
            draw.text((opt_x1 + 15, 39), optics_text, font=font_optics, fill=(0, 210, 255, 255))

            # 2. Lower-Third Storyboard Teleprompter & Beat Banner
            seq = frame.get("sequence", i + 1)
            b_name = frame.get("beat_name", f"Beat {i+1}").upper()
            f_title = frame.get("title", f"Beat {i+1}")
            clean_title = f_title.split("—")[-1].strip().upper() if "—" in f_title else f_title.upper()
            act_name = frame.get("act", "Act 1").upper()
            beat_banner_text = f"BEAT {seq:02d}: {b_name} — {clean_title} ({act_name})"

            banner_bbox = draw.textbbox((0, 0), beat_banner_text, font=font_banner)
            banner_w = min(1824, banner_bbox[2] - banner_bbox[0] + 36)

            box_y1 = 855
            box_y2 = 1005

            # Banner sits on top of the teleprompter box
            draw.rounded_rectangle([(48, box_y1 - 38), (48 + banner_w, box_y1)], radius=4, fill=(0, 82, 255, 245))
            draw.text((64, box_y1 - 32), beat_banner_text, font=font_banner, fill=(255, 255, 255, 255))

            # Teleprompter narrative box
            draw.rounded_rectangle([(48, box_y1), (1872, box_y2)], radius=6, fill=(10, 12, 18, 225), outline=(30, 41, 59, 180), width=1)
            # Cyan accent strip
            draw.rectangle([(48, box_y1), (55, box_y2)], fill=(0, 210, 255, 255))

            # Subtitle narration words
            narration = frame.get("action_text") or frame.get("description") or frame.get("dialogue_text") or ""
            if not narration and frame.get("prompt"):
                narration = frame.get("prompt")
            # Clean newlines for subtitle wrapping
            clean_narration = " ".join(narration.replace("\n", " ").split())
            lines = textwrap.wrap(clean_narration, width=115)
            curr_y = box_y1 + 16
            for line in lines[:3]:
                draw.text((75, curr_y), line, font=font_sub, fill=(244, 244, 248, 255))
                curr_y += 36

            # 3. Bottom News Ticker Bar
            draw.rectangle([(0, 1020), (1920, 1080)], fill=(7, 10, 16, 255))
            draw.line([(0, 1020), (1920, 1020)], fill=(0, 210, 255, 200), width=2)

            draw.rectangle([(0, 1020), (220, 1080)], fill=(255, 0, 85, 255))
            draw.text((35, 1038), "⚡ BREAKING", font=font_ticker, fill=(255, 255, 255, 255))

            ticker_msg = f"BREAKING: {show_title}  |  15 SAVE THE CAT! BEATS IN 16:9 UHD  |  BEAT {seq:02d} OF {len(frames)}: {b_name}  |  SNN AUTONOMOUS TV BROADCAST ACTIVE"
            draw.text((245, 1040), ticker_msg, font=font_ticker, fill=(0, 240, 255, 255))

            # Composite overlay with background slide image
            final_im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
            final_im.save(slide_path, format="PNG")
            dur = max(0.5, float(frame.get("duration_sec", 3.0)))
            concat_lines.append(f"file '{slide_path.resolve()}'")
            concat_lines.append(f"duration {dur:.4f}")

        if frames:
            last_slide = tmp_dir / f"slide_{len(frames)-1:02d}.png"
            concat_lines.append(f"file '{last_slide.resolve()}'")

        concat_file = tmp_dir / "concat.txt"
        with open(concat_file, "w") as cf:
            cf.write("\n".join(concat_lines) + "\n")

        safe_title = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in title)
        output_filename = f"{safe_title}_1080p.mp4"
        output_mp4 = output_dir / output_filename

        cmd = [
            FFMPEG_BIN, "-y",
            "-f", "concat", "-safe", "0", "-i", str(concat_file)
        ]

        if audio_file_path and audio_file_path.exists():
            cmd.extend(["-i", str(audio_file_path)])
            cmd.extend([
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "aac", "-b:a", "320k", "-shortest",
                "-movflags", "+faststart",
                str(output_mp4)
            ])
        else:
            cmd.extend([
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
                "-movflags", "+faststart",
                str(output_mp4)
            ])

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"FFmpeg encoding failed: {res.stderr[-400:]}")

        file_size_mb = round(output_mp4.stat().st_size / (1024 * 1024), 2)

        downloads_target = DOWNLOADS_DIR / output_filename
        try:
            shutil.copy2(output_mp4, downloads_target)
        except Exception:
            downloads_target = None

        # Also maintain project_id named alias in exports directory
        pid_alias = output_dir / f"{project_id}_1080p.mp4"
        try:
            if pid_alias != output_mp4:
                shutil.copy2(output_mp4, pid_alias)
        except Exception:
            pass

        return {
            "status": "SUCCESS",
            "project_id": project_id,
            "title": title,
            "output_path": str(output_mp4),
            "downloads_path": str(downloads_target) if downloads_target else None,
            "filename": output_filename,
            "size_mb": file_size_mb,
            "duration_sec": total_audio_duration,
            "resolution": "1920x1080 (1080p)",
            "codec": "H.264 / AAC 320k (YouTube Recommended)",
            "frames_compiled": len(frames)
        }
