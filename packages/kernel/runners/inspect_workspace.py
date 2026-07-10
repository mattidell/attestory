"""Inspect a synthetic kernel workspace from its append-only act log."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from packages.kernel.act_log import ActLog
from packages.kernel.read_models import build_read_model
from packages.kernel.schema_registry import SchemaRegistry


def _select_view(model: dict[str, Any], view: str) -> Any:
    if view == "all":
        return model
    if view == "current":
        return model["current"]
    if view == "history":
        return model["history_by_fact"]
    if view == "open":
        return model["open_fact_ids"]
    raise ValueError(f"unknown view: {view}")


def _human(model: dict[str, Any]) -> str:
    lines = [f"Revision: {model['revision']}"]
    current = model["current"]
    lines.append("Current findings:")
    for finding_id in current["finding_ids"]:
        finding = current["findings"][finding_id]["finding"]
        lines.append(f"  - {finding_id}: {finding['fact_id']} = {finding['value']}")
    if not current["finding_ids"]:
        lines.append("  - none")

    lines.append("Open facts:")
    for fact_id in model["open_fact_ids"]:
        lines.append(f"  - {fact_id}")
    if not model["open_fact_ids"]:
        lines.append("  - none")

    lines.append("History:")
    for fact_id, entries in model["history_by_fact"].items():
        rendered = ", ".join(
            f"{entry['finding_id']} ({'current' if entry['current'] else 'displaced'})"
            for entry in entries
        )
        lines.append(f"  - {fact_id}: {rendered}")
    if not model["history_by_fact"]:
        lines.append("  - none")
    return "\n".join(lines) + "\n"


def inspect_workspace(workspace: Path, view: str = "all") -> Any:
    registry = SchemaRegistry()
    contents = ActLog(workspace, registry).read()
    model = build_read_model(contents.acts, registry)
    return _select_view(model, view)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace",
        required=True,
        type=Path,
        help="Path to a workspace directory containing acts.jsonl",
    )
    parser.add_argument(
        "--view",
        choices=("all", "current", "history", "open"),
        default="all",
        help="Projection to print",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON instead of the human-readable summary",
    )
    args = parser.parse_args(argv)

    selected = inspect_workspace(args.workspace, args.view)
    if args.json or args.view != "all":
        print(json.dumps(selected, indent=2, sort_keys=True))
    else:
        print(_human(selected), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
