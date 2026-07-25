"""Command-line interface for presentation economy data."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .comparison import build_comparison
from .validation import ValidationError, validate_dataset


def _read_json(path: str) -> Any:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def _serialize(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m tools.presentation_economy")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate")
    validate.add_argument("--dataset", required=True)
    compare = subparsers.add_parser("compare")
    compare.add_argument("--workload", required=True)
    compare.add_argument("--observations", required=True)
    compare.add_argument("--baseline", required=True)
    compare.add_argument("--treatment", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "validate":
            validate_dataset(_read_json(args.dataset))
            sys.stdout.write('{"valid":true}\n')
            return 0
        workload = _read_json(args.workload)
        observation_input = _read_json(args.observations)
        observations = (
            observation_input["observations"]
            if isinstance(observation_input, dict)
            else observation_input
        )
        result = build_comparison(
            workload,
            observations,
            args.baseline,
            args.treatment,
        )
        sys.stdout.write(_serialize(result))
        return 0
    except (OSError, json.JSONDecodeError, ValidationError, KeyError, TypeError) as error:
        sys.stderr.write(f"presentation-economy: {error}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
