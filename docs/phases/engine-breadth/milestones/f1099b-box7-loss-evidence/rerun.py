"""Replay every recorded core v83 return on scratch core v84, with the recorded answers.

Evidence for docs/phases/engine-breadth/milestones/f1099b-box7-loss.md.
Charter: docs/reviews/f1099b-box7-loss/charter-track0.md.

The act lists are the ones tests/test_f1099b_backup_withholding_v83.py runs:
Track 0, the 213 returns, and the zero box-4 sample. No answer is substituted.
Each pin is classified against tests/fixtures/f1099b_backup_withholding_v83/expected.json.

    python3 rerun.py /path/outside/core.json [output.json]

BOX7_RERUN_LIVE_PAIR=1 runs each recorded return on published v83 and on the
scratch core, and classifies those two live results against each other.
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
    """A blocked line 16 row that stopped naming sale-count symbols and nothing else."""
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


def _published_v83(test: Any) -> Any:
    return test.track0().h.Core("v83", "v81", "v81")


def _pin_run(test: Any, core: Any, acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    return test.pin(test.track0().run_coordinate(core, acts, run_id))


def _one(item: tuple[str, list[dict[str, Any]], dict[str, Any]]) -> tuple[str, dict[str, Any]]:
    key, acts, pinned = item
    test = load_test()
    core = scratch_core(test, Path(os.environ["BOX7_CORE"]))
    got = _pin_run(test, core, acts, "demo.b7.rerun." + key.replace("/", "."))
    row = classify(pinned, got)
    if row["class"] != "identical":
        row["v84_disposition"] = got.get("error") or (got.get("lines") or {}).get("schedule-d.line-16")
    return key, row


def _pair(item: tuple[str, list[dict[str, Any]], dict[str, Any]]) -> tuple[str, dict[str, Any]]:
    """Live v83 and live scratch v84, classified against each other.

    The fixture pin is support only. A change is a difference between the two live runs.
    """
    key, acts, pinned = item
    test = load_test()
    slug = key.replace("/", ".")
    v84 = scratch_core(test, Path(os.environ["BOX7_CORE"]))
    v83 = _published_v83(test)
    pin84 = _pin_run(test, v84, acts, "demo.b7.nb.v84." + slug)
    pin83 = _pin_run(test, v83, acts, "demo.b7.nb.v83." + slug)
    row = classify(pin83, pin84)
    row["v83_vs_fixture"] = "identical" if pin83 == pinned else "differs"
    row["v84_vs_fixture"] = "identical" if pin84 == pinned else "differs"
    if row["class"] != "identical":
        row["v83_disposition"] = pin83.get("error") or (pin83.get("lines") or {}).get("schedule-d.line-16")
        row["v84_disposition"] = pin84.get("error") or (pin84.get("lines") or {}).get("schedule-d.line-16")
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
    if len(sys.argv) not in (2, 3):
        raise SystemExit("usage: rerun.py <scratch-core.json> [output.json]")
    core_path = Path(sys.argv[1]).resolve()
    out_name = sys.argv[2] if len(sys.argv) == 3 else "rerun-output.json"
    out_path = HERE / out_name
    if out_path.parent != HERE or out_path.suffix != ".json":
        raise SystemExit("output must be a json file in the evidence directory")
    os.environ["BOX7_CORE"] = str(core_path)
    test = load_test()
    core = scratch_core(test, core_path)
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    work = tasks(test, core, expected)
    only = {item for item in os.environ.get("BOX7_RERUN_ONLY", "").split(",") if item}
    if only:
        work = [item for item in work if item[0] in only]
        missing = only - {item[0] for item in work}
        if missing:
            raise SystemExit(f"unknown recorded ids: {sorted(missing)[:8]}")
    pair = os.environ.get("BOX7_RERUN_LIVE_PAIR") == "1"
    workers = int(os.environ.get("BOX7_WORKERS") or min(6, os.cpu_count() or 2))
    print(f"running {len(work)} recorded returns{' on live v83 and v84' if pair else ''}", flush=True)
    found: dict[str, dict[str, Any]] = {}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        done = 0
        for key, row in pool.map(_pair if pair else _one, work):
            found[key] = row
            done += 1
            if done % 20 == 0 or done == len(work):
                print(f"{done}/{len(work)} {key} {row['class']}", flush=True)
    counts: dict[str, int] = {}
    fixture_counts = {"v83_identical": 0, "v83_differs": 0, "v84_identical": 0, "v84_differs": 0}
    changes = []
    for key in sorted(found):
        label = found[key]["class"]
        counts[label] = counts.get(label, 0) + 1
        if found[key].get("v83_vs_fixture") == "identical":
            fixture_counts["v83_identical"] += 1
        elif "v83_vs_fixture" in found[key]:
            fixture_counts["v83_differs"] += 1
        if found[key].get("v84_vs_fixture") == "identical":
            fixture_counts["v84_identical"] += 1
        elif "v84_vs_fixture" in found[key]:
            fixture_counts["v84_differs"] += 1
        if label != "identical":
            changes.append({"id": key, **found[key]})
    payload = {
        "core": "live-v83-and-live-v84" if pair else "v84",
        "compared_to": (
            "live v83 against live scratch v84; fixture pin is support"
            if pair else "tests/fixtures/f1099b_backup_withholding_v83/expected.json"
        ),
        "answers": "recorded, not substituted",
        "runs": len(found),
        "live_runs": len(found) * (2 if pair else 1),
        "counts": counts,
        "fixture_support": fixture_counts if pair else None,
        "classes": {key: found[key]["class"] for key in sorted(found)},
        "changes": changes,
    }
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"rerun output contains {needle}")
    out_path.write_text(text, encoding="utf-8")
    print(json.dumps({"runs": len(found), "counts": counts, "changes": len(changes),
                      "output": out_path.name}, indent=2))


if __name__ == "__main__":
    if os.environ.get("BOX7_RERUN_WORKER") != "1":
        os.environ["BOX7_RERUN_WORKER"] = "1"
        main()
