"""Foreground published-v92/v93 replay, with resumable external part file.

Run: python3 <this-file> <work-directory-outside-the-repository>
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]


def sentences(pin):
    found = set(pin.get("questions") or [])
    for key in ("reasons", "blocked_reasons"):
        for values in (pin.get(key) or {}).values():
            found.update(values)
    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("work", type=Path)
    parser.add_argument("--summarize-only", action="store_true")
    args = parser.parse_args()
    work = args.work.resolve()
    if work == REPO or REPO in work.parents:
        raise SystemExit("work directory must be outside the repository")
    work.mkdir(parents=True, exist_ok=True)
    part, native, clock = (work / name for name in ("recorded-part.json", "recorded-native.json", "recorded-wall.json"))
    spent = json.loads(clock.read_text()) if clock.exists() else []
    workers = max(1, (os.cpu_count() or 2) - 1)
    if not args.summarize_only:
        start = time.monotonic()
        try:
            subprocess.run([sys.executable, str(REPO / "tools/recorded_replay.py"), "neighbour",
                "v92", "v93", "--workers", str(workers), "--part", str(part), "--out", str(native)],
                check=True, cwd=REPO)
        finally:
            spent.append(round(time.monotonic() - start, 3))
            clock.write_text(json.dumps(spent) + "\n")
    results = json.loads(part.read_text())["results"]
    counts = Counter(row["class"] for row in results.values())
    errors = Counter(row["pins"]["v92"].get("error") for row in results.values())
    changes = []
    for key, row in sorted(results.items()):
        if row["class"] != "identical":
            changes.append({"id": key, **{k: v for k, v in row.items() if k != "pins"},
                "added_sentences": sorted(sentences(row["pins"]["v93"]) - sentences(row["pins"]["v92"]))})
    body = {"baseline": "published v92 / registry v90 / release v90",
        "successor": "published v93 / registry v91 / release v91", "lists": "recorded_lists(), unmodified",
        "workers": workers, "distinct_lists": len(results), "coordinate_attempts": 2*len(results),
        "wall_time_s": round(sum(spent), 3), "counts": dict(counts),
        "successful_coordinate_runs_per_core": errors.get(None, 0),
        "same_errors_per_core": {k: v for k, v in errors.items() if k is not None},
        "changes": changes, "classes": {key: row["class"] for key, row in sorted(results.items())},
        "part_file_retained": True}
    text = json.dumps(body, indent=2) + "\n"
    assert not re.search(r"/(?:Users|private|tmp|var)/", text)
    (HERE / "track1-replay.json").write_text(text)
    print(json.dumps({k: body[k] for k in ("distinct_lists", "wall_time_s", "counts", "same_errors_per_core")}, indent=2))
    assert len(results) == 775 and counts == {"identical": 775}


if __name__ == "__main__":
    main()
