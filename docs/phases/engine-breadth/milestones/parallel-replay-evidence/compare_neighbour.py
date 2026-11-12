"""Compare parallel replay output against committed track0-neighbour.json.

Verifies exact equivalence: every list key and every row equal.
Produces equivalence.json under docs/phases/engine-breadth/milestones/parallel-replay-evidence/.
Part of the parallel-replay tooling milestone.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

REPO = Path(__file__).resolve().parents[5]
DEFAULT_COMMITTED = (
    REPO
    / "docs/phases/engine-breadth/milestones/question-wording-evidence/track0-neighbour.json"
)
DEFAULT_EQUIVALENCE = (
    REPO
    / "docs/phases/engine-breadth/milestones/parallel-replay-evidence/equivalence.json"
)

# Benchmark measurements of 20 lists single-process: 349.68 s -> 13550.23 s extrapolated for 775 lists.
SINGLE_PROCESS_BENCHMARK = {
    "measured_lists": 20,
    "measured_wall_time_s": 349.68,
    "extrapolated_775_wall_time_s": 13550.23,
    "extrapolated_hours": 3.76,
    "method": "Measured 20 lists single-process on cores v86 and v87, extrapolated to 775 lists.",
}


def compare(
    replay_data: dict[str, Any],
    committed_data: dict[str, Any],
    wall_time_s: float,
    workers: int = 4,
) -> dict[str, Any]:
    """Compare replay output against committed data with strengthened S1 checks.

    Checks:
    - Top-level `sets`, `distinct_lists`, `runs`, `counts`, and `same_error_on_both_cores`.
    - Every key's class in `classes`.
    - Exact equality of the `changes` list and each change row (including error fields).
    """
    mismatches: list[dict[str, Any]] = []

    # 1. Check top-level metadata and counts
    for top_field in ("sets", "distinct_lists", "runs", "counts", "same_error_on_both_cores"):
        if replay_data.get(top_field) != committed_data.get(top_field):
            mismatches.append({
                "type": f"{top_field}_mismatch",
                "replay": replay_data.get(top_field),
                "committed": committed_data.get(top_field),
            })

    # 2. Check key sets and class per key
    replay_classes = replay_data.get("classes", {})
    committed_classes = committed_data.get("classes", {})

    missing_keys = sorted(set(committed_classes) - set(replay_classes))
    extra_keys = sorted(set(replay_classes) - set(committed_classes))

    if missing_keys:
        mismatches.append({"type": "missing_keys", "keys": missing_keys})
    if extra_keys:
        mismatches.append({"type": "extra_keys", "keys": extra_keys})

    for key in sorted(committed_classes):
        if key in replay_classes and replay_classes[key] != committed_classes[key]:
            mismatches.append({
                "type": "class_mismatch",
                "key": key,
                "replay": replay_classes[key],
                "committed": committed_classes[key],
            })

    # 3. Check every change row and change list ordering
    replay_changes_list = replay_data.get("changes", [])
    committed_changes_list = committed_data.get("changes", [])
    if replay_changes_list != committed_changes_list:
        mismatches.append({
            "type": "changes_list_mismatch",
            "replay": replay_changes_list,
            "committed": committed_changes_list,
        })

    replay_changes_by_id = {row["id"]: row for row in replay_changes_list if isinstance(row, dict) and "id" in row}
    committed_changes_by_id = {row["id"]: row for row in committed_changes_list if isinstance(row, dict) and "id" in row}

    missing_change_ids = sorted(set(committed_changes_by_id) - set(replay_changes_by_id))
    extra_change_ids = sorted(set(replay_changes_by_id) - set(committed_changes_by_id))
    if missing_change_ids:
        mismatches.append({"type": "missing_change_ids", "ids": missing_change_ids})
    if extra_change_ids:
        mismatches.append({"type": "extra_change_ids", "ids": extra_change_ids})

    for cid in sorted(committed_changes_by_id):
        if cid in replay_changes_by_id:
            c_row = committed_changes_by_id[cid]
            r_row = replay_changes_by_id[cid]
            if c_row != r_row:
                mismatches.append({
                    "type": "change_row_mismatch",
                    "id": cid,
                    "replay": r_row,
                    "committed": c_row,
                })

    return {
        "lists": len(committed_classes),
        "workers": workers,
        "wall_time_s": round(wall_time_s, 2),
        "single_process_time": SINGLE_PROCESS_BENCHMARK,
        "counts": replay_data.get("counts", {}),
        "same_error_on_both_cores": replay_data.get("same_error_on_both_cores", {}),
        "mismatches": mismatches,
        "equivalent": len(mismatches) == 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare parallel replay output against committed track0-neighbour.json.")
    parser.add_argument("--replay-output", required=True, type=Path, help="Path to replay output JSON")
    parser.add_argument("--committed", type=Path, default=DEFAULT_COMMITTED, help="Path to committed track0-neighbour.json")
    parser.add_argument("--wall-time", type=float, default=0.0, help="Wall time in seconds")
    parser.add_argument("--wall-time-file", type=Path, default=None, help="File containing wall time in seconds")
    parser.add_argument("--workers", type=int, default=4, help="Worker count used in replay")
    parser.add_argument("--out", type=Path, default=DEFAULT_EQUIVALENCE, help="Path to output equivalence.json")

    args = parser.parse_args()

    replay_data = json.loads(args.replay_output.read_text(encoding="utf-8"))
    committed_data = json.loads(args.committed.read_text(encoding="utf-8"))

    wall_time = args.wall_time
    if args.wall_time_file and args.wall_time_file.exists():
        wall_time = float(args.wall_time_file.read_text(encoding="utf-8").strip())

    result = compare(replay_data, committed_data, wall_time_s=wall_time, workers=args.workers)

    # Verify no absolute or temp paths in result
    result_text = json.dumps(result, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in result_text:
            raise ValueError(f"Equivalence result contains local path needle: {needle}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(result_text, encoding="utf-8")

    print(json.dumps({
        "lists": result["lists"],
        "workers": result["workers"],
        "wall_time_s": result["wall_time_s"],
        "mismatches": len(result["mismatches"]),
        "equivalent": result["equivalent"],
    }, indent=2))

    if not result["equivalent"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
