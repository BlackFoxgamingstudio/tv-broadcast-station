"""
TickerOverlayEngine: Real-time news crawl banners, financial tickers, and lower-third graphics.
Author: Russell Alan Powers
"""
import time
from typing import Dict, Any, List, Optional

class TickerOverlayEngine:
    THEMES = {
        "BREAKING": {"badge": "BREAKING NEWS", "theme_color": "#FF3B30", "priority": 1},
        "TECH": {"badge": "SOVEREIGN TECH", "theme_color": "#007AFF", "priority": 2},
        "MARKETS": {"badge": "SAAS REPLACEMENT INDEX", "theme_color": "#34C759", "priority": 3},
        "COMMUNITY": {"badge": "COMMUNITY CHALLENGE", "theme_color": "#AF52DE", "priority": 4}
    }

    def generate_ticker_feed(
        self,
        headlines: Optional[List[str]] = None,
        system_vitals: Optional[Dict[str, Any]] = None,
        category: str = "BREAKING"
    ) -> Dict[str, Any]:
        headlines = headlines or [
            "BREAKING: Sovereign Biz Box replaces commercial SaaS toolchains with zero cloud egress fees",
            "MARKETS: 10-Year Software Sovereignty index up 34 percent across enterprise deployments",
            "EDGE VITAL: Apple Silicon Mac Mini node thermal balance optimal at 42.5C",
            "SECURITY: Zero-Trust X-SBB-Auth active across all 35 local microservices"
        ]

        vitals = system_vitals or {
            "CPU_LOAD": "0.42",
            "ACTIVE_PIPELINES": "65",
            "UPTIME": "99.99%",
            "AIR_TEMP": "21.5C",
            "NET_EGRESS_COST": "$0.00"
        }

        theme_info = self.THEMES.get(category.upper(), self.THEMES["BREAKING"])
        crawl_string = "  ★  ".join(headlines)

        return {
            "crawl_string": crawl_string,
            "items_count": len(headlines),
            "lower_third": {
                "headline": headlines[0] if headlines else "SOVEREIGN BROADCAST LIVE",
                "subtext": "Sovereign News Network (SNN) — Bare-Metal Studio Feed",
                "badge": theme_info["badge"],
                "theme_color": theme_info["theme_color"],
                "speed_px_per_sec": 120,
                "position": "BOTTOM_OVERLAY_16_9"
            },
            "vitals_ticker": vitals,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
