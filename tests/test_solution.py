#!/usr/bin/env python3
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.core import CoreEngine

class TestTVBroadcastStation(unittest.TestCase):
    def setUp(self):
        self.engine = CoreEngine()

    def test_01_health_check(self):
        h = self.engine.health_check()
        self.assertEqual(h["status"], "HEALTHY")
        self.assertEqual(h["port"], 8812)

    def test_02_broadcast_stage_chunking(self):
        md = "# Header\n\nFirst paragraph text.\n\n```mermaid\ngraph LR\n  A-->B\n```\n\nSecond paragraph text."
        res = self.engine.execute_feature("chunk_broadcast_frames", {"raw_markdown": md, "topic": "Tech News"})
        self.assertEqual(res["status"], "SUCCESS")
        frames = res["result"]["frames"]
        self.assertGreaterEqual(len(frames), 2)
        # Check diagram was extracted
        has_diagram = any(f["type"] == "DIAGRAM_MERMAID" for f in frames)
        self.assertTrue(has_diagram)

    def test_03_ticker_overlay(self):
        res = self.engine.execute_feature("generate_ticker_feed", {})
        self.assertEqual(res["status"], "SUCCESS")
        t = res["result"]
        self.assertIn("crawl_string", t)
        self.assertIn("lower_third", t)
        self.assertEqual(t["lower_third"]["badge"], "BREAKING NEWS")

    def test_04_master_broadcast_package(self):
        res = self.engine.execute_feature("assemble_broadcast_package", {"content": "Sample broadcast text."})
        self.assertEqual(res["status"], "SUCCESS")
        pkg = res["result"]
        self.assertTrue(pkg["ready_for_playout"])
        self.assertEqual(pkg["format"], "16:9_UHD")

if __name__ == "__main__":
    unittest.main(verbosity=2)