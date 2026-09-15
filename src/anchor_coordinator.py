"""
AnchorCoordinator: Feeds teleprompter cues and camera switching to 3D avatar anchor.
Author: Russell Alan Powers
"""
import time
from typing import Dict, Any, List

class AnchorCoordinator:
    CAMERA_SHOTS = ["WIDE_STUDIO", "ANCHOR_CLOSEUP", "SPLIT_SCREEN_DATA", "PICTURE_IN_PICTURE"]

    def coordinate_anchor_rundown(self, frames: List[Dict[str, Any]]) -> Dict[str, Any]:
        shots = []
        for idx, frame in enumerate(frames):
            cam = self.CAMERA_SHOTS[idx % len(self.CAMERA_SHOTS)]
            emotion = "SERIOUS" if "BREAKING" in frame.get("title", "") else "CONFIDENT"
            shots.append({
                "shot_index": idx + 1,
                "camera_angle": cam,
                "anchor_emotion": emotion,
                "teleprompter_cue": frame.get("content", "")[:120] + "...",
                "duration_sec": frame.get("display_duration_sec", 6.0)
            })

        return {
            "total_shots": len(shots),
            "estimated_segment_runtime_sec": sum(s["duration_sec"] for s in shots),
            "anchor_shots": shots
        }