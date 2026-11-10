"""Replay every recorded core v83 return on scratch core v84, with the recorded answers.

Evidence for docs/phases/engine-breadth/milestones/f1099b-box7-loss.md.
Charter: docs/reviews/f1099b-box7-loss/charter-p0.md.

The act lists are the ones tests/test_f1099b_backup_withholding_v83.py runs:
Track 0, the 213 returns, and the zero box-4 sample. No answer is substituted.
Each pin is classified against tests/fixtures/f1099b_backup_withholding_v83/expected.json.

    python3 rerun.py /path/outside/core.json
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

EXPECTED = REPO / "tests/fixtures/f1099b_backup_withholding_v83/expected.json"
TEST = REPO / "tests/test_f1099b_backup_withholding_v83.py"


def load_test() -> Any:
    name = "f1099b_b4_v83_box7_rerun"
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(name, TEST)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def scratch_core(test: Any, core_path: Path) -> Any:
    body = json.loads(core_path.read_text(encoding="utf-8"))
    t = test.track0()
    return t.h.Core(
        body["version"], body["registry"], body["release_version"],
        content=Path(body["content"]), releases=Path(body["releases"]),
        loader_from=body.get("loader_from"),
    )


def _diff(left: Any, right: Any) -> list[str]:
    if left == right:
        return []
    if not isinstance(left, dict) or not isinstance(right, dict):
        return ["pin"]
    found = []
    for key in sorted(set(left) | set(right)):
        if left.get(key) == right.get(key):
            continue
        if isinstance(left.get(key), dict) and isinstance(right.get(key), dict):
            for name in sorted(set(left[key]) | set(right[key])):
                if left[key].get(name) != right[key].get(name):
                    found.append(f"{key}.{name}")
        else:
            found.append(str(key))
    return found


def _count_drop(v83: dict[str, Any], v84: dict[str, Any]) -> dict[str, Any] | None:
    """Line 16 v4 does not require the sale-count symbols, so a blocked row stops naming them."""
    left = (v83.get("rows") or {}).get("schedule-d-line16")
    right = (v84.get("rows") or {}).get("schedule-d-line16")
    if not (isinstance(left, list) and isinstance(right, list) and len(left) == 3 and len(right) == 3):
        return None
    if left[0] != "blocked" or right[0] != "blocked" or left[1] != right[1]:
        return None
    if not isinstance(left[2], list) or not isinstance(right[2], list):
        return None
    dropped = [item for item in left[2] if item not in right[2]]
    added = [item for item in right[2] if item not in left[2]]
    kept = [item for item in left[2] if item not in dropped]
    if added or not dropped or kept != right[2]:
        return None
    if not all(str(item).endswith("-count") for item in dropped):
        return None
    rest = {key: value for key, value in v83.items() if key != "rows"}
    other = {key: value for key, value in v84.items() if key != "rows"}
    if rest != other:
        return None
    other_rows = {key: value for key, value in (v83.get("rows") or {}).items() if key != "schedule-d-line16"}
    new_rows = {key: value for key, value in (v84.get("rows") or {}).items() if key != "schedule-d-line16"}
    if other_rows != new_rows:
        return None
    return {"class": "line16_missing_drops_sale_counts", "dropped": dropped, "v84_missing": right[2]}


def classify(v83: dict[str, Any], v84: dict[str, Any]) -> dict[str, Any]:
    if v83 == v84:
        return {"class": "identical"}
    dropped = _count_drop(v83, v84)
    if dropped is not None:
        return dropped
    changed = _diff(v83, v84)
    v83_line = (v83.get("lines") or {}).get("schedule-d.line-16")
    v84_line = (v84.get("lines") or {}).get("schedule-d.line-16")
    v83_blocked = isinstance(v83_line, str) and "block" in v83_line
    v84_number = isinstance(v84_line, (int, float))
    if v83_blocked and v84_number:
        label = "box7_yes_now_computes"
    elif v83_blocked and isinstance(v84_line, str) and "block" in v84_line:
        label = "box7_yes_loss_still_refused"
    else:
        label = "counterexample"
    return {"class": label, "changed": changed[:24]}


def _one(item: tuple[str, list[dict[str, Any]], dict[str, Any]]) -> tuple[str, dict[str, Any]]:
    key, acts, pinned = item
    test = load_test()
    core = scratch_core(test, Path(os.environ["BOX7_CORE"]))
    t = test.track0()
    result = t.run_coordinate(core, acts, "demo.b7.rerun." + key.replace("/", "."))
    got = test.pin(result)
    row = classify(pinned, got)
    if row["class"] != "identical":
        row["v84_disposition"] = got.get("error") or (got.get("lines") or {}).get("schedule-d.line-16")
    return key, row


def tasks(test: Any, core: Any, expected: dict[str, Any]) -> list[tuple[str, list[dict[str, Any]], dict[str, Any]]]:
    t = test.track0()
    print("building track 0 act lists", flush=True)
    cases = dict(test.decided_cases(t))
    print("exporting the 213 returns", flush=True)
    with tempfile.TemporaryDirectory() as tmp:
        exported = test.export_returns(Path(tmp))
    returns = test.return_acts(t, exported)
    out: list[tuple[str, list[dict[str, Any]], dict[str, Any]]] = []
    for key, pinned in expected["track0"].items():
        out.append((f"track0/{key}", cases[key], pinned))
    for key, entry in expected["returns"].items():
        out.append((f"returns/{key}", returns[key], entry["v83"]))
    for key, entry in expected["zero_sample"].items():
        out.append((f"zero/{key}", test.with_zero(t, returns[key], core), entry["v83"]))
    return out


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: rerun.py <scratch-core.json>")
    core_path = Path(sys.argv[1]).resolve()
    os.environ["BOX7_CORE"] = str(core_path)
    test = load_test()
    core = scratch_core(test, core_path)
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    work = tasks(test, core, expected)
    workers = int(os.environ.get("BOX7_WORKERS") or min(6, os.cpu_count() or 2))
    print(f"running {len(work)} recorded returns", flush=True)
    found: dict[str, dict[str, Any]] = {}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        done = 0
        for key, row in pool.map(_one, work):
            found[key] = row
            done += 1
            if done % 20 == 0 or done == len(work):
                print(f"{done}/{len(work)} {key} {row['class']}", flush=True)
    counts: dict[str, int] = {}
    changes = []
    for key in sorted(found):
        label = found[key]["class"]
        counts[label] = counts.get(label, 0) + 1
        if label != "identical":
            changes.append({"id": key, **found[key]})
    payload = {
        "core": "v84",
        "compared_to": "tests/fixtures/f1099b_backup_withholding_v83/expected.json",
        "answers": "recorded, not substituted",
        "runs": len(found),
        "counts": counts,
        "classes": {key: found[key]["class"] for key in sorted(found)},
        "changes": changes,
    }
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"rerun output contains {needle}")
    (HERE / "rerun-output.json").write_text(text, encoding="utf-8")
    print(json.dumps({"runs": len(found), "counts": counts, "changes": len(changes)}, indent=2))


if __name__ == "__main__":
    if os.environ.get("BOX7_RERUN_WORKER") != "1":
        os.environ["BOX7_RERUN_WORKER"] = "1"
        main()
