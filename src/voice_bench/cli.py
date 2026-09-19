"""Offline status and planning commands. No live execution command yet."""

import argparse
import json
import sys
from pathlib import Path

from pydantic import ValidationError

from voice_bench.readiness import scaffold_status
from voice_bench.settings import load_config


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status", help="Show implementation status without contacting providers")
    plan = commands.add_parser("plan", help="Validate and display local configuration only")
    plan.add_argument("--config", type=Path, required=True)
    args = parser.parse_args(argv)
    result = scaffold_status()
    if args.command == "plan":
        try:
            config = load_config(args.config)
        except (OSError, ValueError, ValidationError) as exc:
            print(f"Configuration error: {exc}", file=sys.stderr)
            return 2
        result["config"] = config.model_dump(mode="json")
        result["message"] = "Configuration is valid. No calls or artifacts were created."
    print(json.dumps(result, indent=2))
    return 0
