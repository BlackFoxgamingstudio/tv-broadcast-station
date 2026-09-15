#!/usr/bin/env python3
import sys
import json
import argparse
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR.parent) not in sys.path:
    sys.path.insert(0, str(SRC_DIR.parent))

from src.core import CoreEngine

def main():
    parser = argparse.ArgumentParser(description="SBB Solution PKG-032: TV Broadcast Station")
    parser.add_argument("--health", action="store_true", help="Service health check")
    parser.add_argument("--exec", type=str, default="assemble_broadcast_package", help="Feature action name")
    parser.add_argument("--payload", type=str, default="{}", help="JSON payload")
    args = parser.parse_args()

    engine = CoreEngine()
    if args.health:
        print(json.dumps(engine.health_check(), indent=2))
        return

    p = json.loads(args.payload)
    res = engine.execute_feature(args.exec, p)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()