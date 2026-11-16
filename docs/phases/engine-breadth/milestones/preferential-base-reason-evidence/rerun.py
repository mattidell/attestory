"""Classify the recorded-return replay of published v90 against scratch v91.

The part file stays outside the repository. This writes a path-free summary
beside the script: every list's class, every number change, and every
computing return that gained or lost a question.

    python3 rerun.py --part <part-file> --log <time-log> --workers N

A computing return is one whose v90 pin has Form 1040 lines and none of those
lines is blocked. A question is new when its sentence is absent from the v90
pin.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools.recorded_replay import summarize_rerun  # noqa: E402


def _questions(pin: dict[str, Any]) -> list[str]:
    return [str(item) for item in (pin.get("questions") or [])]


def _computing(pin: dict[str, Any]) -> bool:
    if "error" in pin:
        return False
    lines = {
        name: value
        for name, value in (pin.get("lines") or {}).items()
        if str(name).startswith("form1040.")
    }
    if not lines:
        return False
    return not any(isinstance(value, str) and "blocked" in value for value in lines.values())


def _wall_time(log_path: Path) -> float:
    text = log_path.read_text(encoding="utf-8")
    found = re.findall(r"^real\s+([0-9.]+)\s*$", text, flags=re.M)
    if not found:
        raise SystemExit("the time log has no real line")
    return float(found[-1])


def classify(results: dict[str, Any]) -> dict[str, Any]:
    counts: Counter[str] = Counter()
    classes: dict[str, str] = {}
    numbers: list[dict[str, Any]] = []
    gained: list[dict[str, Any]] = []
    lost: list[dict[str, Any]] = []
    sentence_fields: Counter[str] = Counter()
    by_set: dict[str, Counter[str]] = {}
    for key, row in sorted(results.items()):
        kind = str(row.get("class"))
        counts[kind] += 1
        classes[key] = kind
        prefix = key.split("/", 1)[0]
        by_set.setdefault(prefix, Counter())[kind] += 1
        for field in row.get("sentence_fields") or []:
            sentence_fields[str(field)] += 1
        if kind == "numbers_changed":
            numbers.append({
                "id": key,
                "number_fields": row.get("number_fields") or [],
                "lines": row.get("lines") or [],
            })
        pins = row.get("pins") or {}
        left = pins.get("v90") or {}
        right = pins.get("v91") or {}
        if not isinstance(left, dict) or not isinstance(right, dict):
            continue
        if not _computing(left):
            continue
        old = set(_questions(left))
        new = set(_questions(right))
        added = sorted(new - old)
        removed = sorted(old - new)
        if added:
            gained.append({"id": key, "added": added})
        if removed:
            lost.append({"id": key, "removed": removed})
    return {
        "counts": dict(counts),
        "by_set": {name: dict(value) for name, value in sorted(by_set.items())},
        "classes": classes,
        "numbers_changed": numbers,
        "newly_asked_on_computing_return": gained,
        "questions_removed_on_computing_return": lost,
        "sentence_field_counts": dict(sentence_fields),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--workers", type=int, required=True)
    args = parser.parse_args()
    loaded = json.loads(args.part.read_text(encoding="utf-8"))
    results = loaded["results"] if isinstance(loaded.get("results"), dict) else loaded
    v83 = summarize_rerun(results, baseline_version="v90", comparison_version="v91")
    body = classify(results)
    payload = {
        "cores": "published core v90 and scratch core v91",
        "lists": len(results),
        "workers": args.workers,
        "wall_time_s": _wall_time(args.log),
        "counts": body["counts"],
        "by_set": body["by_set"],
        "numbers_changed": body["numbers_changed"],
        "newly_asked_on_computing_return": body["newly_asked_on_computing_return"],
        "questions_removed_on_computing_return": body["questions_removed_on_computing_return"],
        "sentence_field_counts": body["sentence_field_counts"],
        "v83_runs": v83["runs"],
        "v83_counts": v83["counts"],
        "v90_matches_v83_fixture": v83["v90_matches_fixture"],
        "classes": body["classes"],
    }
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit("rerun output contains a local path")
    (HERE / "rerun-output.json").write_text(text, encoding="utf-8")
    print(json.dumps({
        "lists": payload["lists"],
        "workers": payload["workers"],
        "wall_time_s": payload["wall_time_s"],
        "counts": payload["counts"],
        "numbers_changed": len(payload["numbers_changed"]),
        "newly_asked_on_computing_return": len(payload["newly_asked_on_computing_return"]),
        "questions_removed_on_computing_return": len(payload["questions_removed_on_computing_return"]),
        "v90_matches_v83_fixture": payload["v90_matches_v83_fixture"],
    }, indent=2))


if __name__ == "__main__":
    main()
