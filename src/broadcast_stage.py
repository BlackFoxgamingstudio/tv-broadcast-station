"""
BroadcastStage: Parses narrative text, diagrams & telemetry into ordered 16:9 visual frames.
Direct implementation of "TV Broadcast Stage OOP Architecture" and Mainframe PiP specifications.
Author: Russell Alan Powers
"""
import re
import time
import hashlib
from typing import Dict, Any, List, Optional

class BroadcastStage:
    """The Director: parses raw markdown/data into timed visual 'shots' for broadcast."""

    # 16:9 UHD Layout Presets from Mainframe PiP specs
    LAYOUT_PRESETS = {
        "FULLSCREEN_DIAGRAM": {"layout": "16:9_UHD", "aspect": "16:9", "split": "100_MAIN", "safe_margin": 40},
        "50_50_SPLIT": {"layout": "16:9_UHD", "aspect": "16:9", "split": "50_50_DUAL", "safe_margin": 30},
        "PRESENTATION_PIP": {"layout": "16:9_UHD", "aspect": "16:9", "split": "75_SLIDE_25_PIP", "safe_margin": 30},
        "4_WAY_GRID": {"layout": "16:9_UHD", "aspect": "16:9", "split": "25_QUAD", "safe_margin": 20},
        "STANDARD_LOWER_THIRD": {"layout": "16:9_UHD", "aspect": "16:9", "split": "CAMERA_LOWER_THIRD", "safe_margin": 40}
    }

    def __init__(self, speech_wpm: int = 140):
        self.speech_wpm = speech_wpm  # Words per minute for dynamic speech timing

    def _estimate_duration(self, text: str, min_sec: float = 4.0, max_sec: float = 15.0) -> float:
        words = len(text.split())
        calculated = (words / self.speech_wpm) * 60.0
        return max(min_sec, min(max_sec, round(calculated, 1)))

    def create_visual_frames(self, raw_markdown: str, topic: str = "Live Broadcast") -> List[Dict[str, Any]]:
        frames = []
        frame_idx = 1

        # 1. Extract Mermaid Diagrams
        mermaid_blocks = re.findall(r"```mermaid(.*?)```", raw_markdown, re.DOTALL)
        for block in mermaid_blocks:
            clean_block = block.strip()
            frames.append({
                "frame_id": f"FRAME-{frame_idx:02d}",
                "type": "DIAGRAM_MERMAID",
                "layout": self.LAYOUT_PRESETS["FULLSCREEN_DIAGRAM"],
                "title": f"Architecture Overview — {topic}",
                "content": clean_block,
                "display_duration_sec": 10.0,
                "transition": "FADE_IN",
                "pip_mode": "PRESENTATION",
                "theme": "DARK_CYBERPUNK"
            })
            frame_idx += 1

        # 2. Clean out mermaid blocks to process remaining text
        clean_text = re.sub(r"```mermaid.*?```", "", raw_markdown, flags=re.DOTALL)

        # 3. Extract Markdown Tables
        table_pattern = r"(\|.*?\|\r?\n\|[-| :]+\|\r?\n(?:\|.*?\|\r?\n?)+)"
        table_blocks = re.findall(table_pattern, clean_text)
        for tbl in table_blocks:
            clean_table = tbl.strip()
            frames.append({
                "frame_id": f"FRAME-{frame_idx:02d}",
                "type": "GRAPHIC_TABLE",
                "layout": self.LAYOUT_PRESETS["50_50_SPLIT"],
                "title": f"Data Matrix — {topic}",
                "content": clean_table,
                "display_duration_sec": 8.0,
                "transition": "SLIDE_LEFT",
                "pip_mode": "SPLIT_VIEW",
                "theme": "OBSIDIAN_GLASS"
            })
            frame_idx += 1

        # Clean tables out
        clean_text = re.sub(r"(\|.*?\|\r?\n\|[-| :]+\|\r?\n(?:\|.*?\|\r?\n?)+)", "", clean_text)

        # 4. Extract Blockquotes / Callout Alerts
        callouts = re.findall(r"(?:^|\n)>\s*(.*?)(?=\n\n|\n[^\s>]|\Z)", clean_text, re.DOTALL)
        for callout in callouts:
            c_text = re.sub(r"^\[!(NOTE|IMPORTANT|WARNING|TIP|CAUTION)\]\s*", "", callout.strip())
            if len(c_text) > 15:
                frames.append({
                    "frame_id": f"FRAME-{frame_idx:02d}",
                    "type": "CALLOUT_ALERT",
                    "layout": self.LAYOUT_PRESETS["STANDARD_LOWER_THIRD"],
                    "title": f"Key Takeaway — {topic}",
                    "content": c_text,
                    "display_duration_sec": self._estimate_duration(c_text, min_sec=5.0),
                    "transition": "POP_IN",
                    "pip_mode": "LOWER_THIRD",
                    "theme": "ACCENT_GOLD"
                })
                frame_idx += 1

        # Clean callouts out
        clean_text = re.sub(r">\s*.*?(?=\n\n|\n[^\s>]|\Z)", "", clean_text, flags=re.DOTALL)

        # 5. Split remaining text into bite-sized teleprompter chunks (paragraphs)
        paragraphs = [p.strip() for p in clean_text.split("\n\n") if len(p.strip()) > 20]
        for p in paragraphs:
            # Strip headers
            text_body = re.sub(r"^#+\s*", "", p).strip()
            if not text_body:
                continue

            frames.append({
                "frame_id": f"FRAME-{frame_idx:02d}",
                "type": "BITE_SIZED_TEXT",
                "layout": self.LAYOUT_PRESETS["STANDARD_LOWER_THIRD"],
                "title": topic,
                "content": text_body[:350],
                "display_duration_sec": self._estimate_duration(text_body, min_sec=4.0, max_sec=12.0),
                "transition": "CROSS_FADE",
                "pip_mode": "ANCHOR_DESK",
                "theme": "GLASS_MINIMAL"
            })
            frame_idx += 1

        return frames
