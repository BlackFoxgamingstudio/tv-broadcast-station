"""
AnchorCoordinator: Feeds teleprompter cues, camera switching & PiP transitions to 3D avatar anchor.
Direct implementation of Mainframe LiveStreamPlayerView & PiPLayoutView specifications.
Author: Russell Alan Powers
"""
import time
from typing import Dict, Any, List

class AnchorCoordinator:
    CAMERA_SHOTS = [
        {"angle": "WIDE_STUDIO", "fov": 65, "camera_id": "CAM_01"},
        {"angle": "ANCHOR_CLOSEUP", "fov": 45, "camera_id": "CAM_02"},
        {"angle": "SPLIT_SCREEN_DATA", "fov": 55, "camera_id": "CAM_03"},
        {"angle": "PICTURE_IN_PICTURE", "fov": 50, "camera_id": "CAM_04"}
    ]

    def coordinate_anchor_rundown(self, frames: List[Dict[str, Any]]) -> Dict[str, Any]:
        shots = []
        for idx, frame in enumerate(frames):
            cam_cfg = self.CAMERA_SHOTS[idx % len(self.CAMERA_SHOTS)]
            frame_type = frame.get("type", "BITE_SIZED_TEXT")
            
            # Context-aware emotion & camera logic
            if frame_type == "DIAGRAM_MERMAID":
                camera_angle = "PICTURE_IN_PICTURE"
                emotion = "EXPLANATORY"
            elif frame_type == "GRAPHIC_TABLE":
                camera_angle = "SPLIT_SCREEN_DATA"
                emotion = "ANALYTICAL"
            elif frame_type == "CALLOUT_ALERT":
                camera_angle = "ANCHOR_CLOSEUP"
                emotion = "URGENT"
            else:
                camera_angle = cam_cfg["angle"]
                emotion = "CONFIDENT"

            cue_text = frame.get("content", "")
            shots.append({
                "shot_index": idx + 1,
                "camera_angle": camera_angle,
                "camera_id": cam_cfg["camera_id"],
                "anchor_emotion": emotion,
                "teleprompter_cue": (cue_text[:140] + "...") if len(cue_text) > 140 else cue_text,
                "duration_sec": frame.get("display_duration_sec", 6.0),
                "pip_layout": frame.get("layout", {}).get("split", "100_MAIN"),
                "transition": frame.get("transition", "CROSS_FADE")
            })

        total_runtime = sum(s["duration_sec"] for s in shots)
        return {
            "total_shots": len(shots),
            "estimated_segment_runtime_sec": round(total_runtime, 1),
            "teleprompter_wpm": 140,
            "anchor_shots": shots
        }
