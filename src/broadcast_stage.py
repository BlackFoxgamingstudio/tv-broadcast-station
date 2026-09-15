"""
BroadcastStage: Parses narrative text & telemetry into ordered 16:9 visual frames.
Direct implementation of "TV Broadcast Stage OOP Architecture".
Author: Russell Alan Powers
"""
import re
import time
import hashlib
from typing import Dict, Any, List

class BroadcastStage:
    """The Director: parses raw markdown/data into timed visual 'shots' for broadcast."""

    def create_visual_frames(self, raw_markdown: str, topic: str = "Live Broadcast") -> List[Dict[str, Any]]:
        frames = []
        frame_idx = 1

        # 1. Extract Mermaid Diagrams
        mermaid_blocks = re.findall(r"```mermaid(.*?)```", raw_markdown, re.DOTALL)
        for block in mermaid_blocks:
            frames.append({
                "frame_id": f"FRAME-{frame_idx:02d}",
                "type": "DIAGRAM_MERMAID",
                "title": f"Architecture Overview — {topic}",
                "content": block.strip(),
                "display_duration_sec": 10.0,
                "transition": "FADE_IN"
            })
            frame_idx += 1

        # 2. Clean out mermaid blocks to process paragraphs
        clean_text = re.sub(r"```mermaid.*?```", "", raw_markdown, flags=re.DOTALL)

        # 3. Extract Markdown Tables
        table_blocks = re.findall(r"(\|.*?\|\n\|[-| :]+\|\n(?:\|.*?\|\n?)+)", clean_text)
        for tbl in table_blocks:
            frames.append({
                "frame_id": f"FRAME-{frame_idx:02d}",
                "type": "GRAPHIC_TABLE",
                "title": "Data Comparison Matrix",
                "content": tbl.strip(),
                "display_duration_sec": 8.0,
                "transition": "SLIDE_LEFT"
            })
            frame_idx += 1

        # Clean tables out
        clean_text = re.sub(r"(\|.*?\|\n\|[-| :]+\|\n(?:\|.*?\|\n?)+)", "", clean_text)

        # 4. Split remaining text into bite-sized teleprompter chunks (paragraphs)
        paragraphs = [p.strip() for p in clean_text.split("\n\n") if len(p.strip()) > 20]
        for p in paragraphs:
            # Strip headers
            text_body = re.sub(r"^#+\s*", "", p)
            frames.append({
                "frame_id": f"FRAME-{frame_idx:02d}",
                "type": "BITE_SIZED_TEXT",
                "title": topic,
                "content": text_body[:300],
                "display_duration_sec": max(5.0, len(text_body.split()) * 0.35),
                "transition": "CROSS_FADE"
            })
            frame_idx += 1

        return frames