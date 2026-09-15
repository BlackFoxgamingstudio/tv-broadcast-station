"""
TickerOverlayEngine: Generates real-time news crawl banners and lower-third graphics.
Author: Russell Alan Powers
"""
import time
from typing import Dict, Any, List

class TickerOverlayEngine:
    def generate_ticker_feed(self, headlines: List[str] = None, system_vitals: Dict[str, Any] = None) -> Dict[str, Any]:
        headlines = headlines or [
            "BREAKING: Sovereign Biz Box replaces commercial SaaS toolchains with zero cloud egress fees",
            "MARKETS: 10-Year Software Sovereignty index up 34 percent across enterprise deployments",
            "EDGE VITAL: Raspberry Pi Cluster thermal balance optimal at 42.5C",
            "SECURITY: Zero-Trust X-SBB-Auth active across all 35 local microservices"
        ]

        vitals = system_vitals or {
            "CPU_LOAD": "0.42",
            "ACTIVE_PIPELINES": "62",
            "UPTIME": "99.99%",
            "AIR_TEMP": "21.5C"
        }

        crawl_string = "  ★  ".join(headlines)

        return {
            "crawl_string": crawl_string,
            "items_count": len(headlines),
            "lower_third": {
                "headline": headlines[0] if headlines else "LIVE BROADCAST",
                "subtext": "Sovereign News Network (SNN) — Bare-Metal Studio Feed",
                "badge": "BREAKING NEWS",
                "theme_color": "#FF3B30"
            },
            "vitals_ticker": vitals,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }