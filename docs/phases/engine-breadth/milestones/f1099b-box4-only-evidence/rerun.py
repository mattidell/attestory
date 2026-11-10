"""Replay every recorded core v83 return on live v84 and scratch v85, as recorded.

Evidence for docs/phases/engine-breadth/milestones/f1099b-box4-only.md.
Charter: docs/reviews/f1099b-box4-only/charter-p0.md.

The act lists are the ones tests/test_f1099b_backup_withholding_v83.py runs:
Track 0, the 213 returns, and the zero box-4 sample. No answer is substituted.
Each live v84 pin is classified against live scratch v85.

    python3 rerun.py /path/outside/core.json [output.json]

The earlier milestone's test module is loaded under a unique name inside each
worker process.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

EXPECTED = REPO / "tests/fixtures/f1099b_backup_withholding_v83/expected.json"
TEST = REPO / "tests/test_f1099b_backup_withholding_v83.py"
PRESENT = "tax.us.2025.f1099b.no-sale-box4-present"
AMOUNT = "tax.us.2025.f1099b.no-sale-box4-withholding"


def load_test() -> Any:
    name = "f1099b_b4only_p0_v83_test"
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


def _missing(pin: dict[str, Any], line: str = "form1040.line-25b") -> list[str]:
    rows = pin.get("rows") or {}
    row = rows.get("form1040-line25b") or rows.get(line)
    if isinstance(row, list) and len(row) == 3 and isinstance(row[2], list):
        return [str(item) for item in row[2]]
    blocked = pin.get("blocked_reasons") or {}
    return []


def classify(v84: dict[str, Any], v85: dict[str, Any]) -> dict[str, Any]:
    if v84 == v85:
        return {"class": "identical"}
    if "error" in v84 or "error" in v85:
        return {"class": "counterexample", "changed": _diff(v84, v85)[:24]}
    v84_line = (v84.get("lines") or {}).get("form1040.line-25b")
    v85_line = (v85.get("lines") or {}).get("form1040.line-25b")
    v84_ok = isinstance(v84_line, (int, float)) or v84_line == 0
    v85_blocked = isinstance(v85_line, str) and "block" in v85_line
    missing = []
    row = (v85.get("rows") or {}).get("form1040-line25b")
    if isinstance(row, list) and len(row) == 3 and isinstance(row[2], list):
        missing = [str(item) for item in row[2]]
    reasons = (v85.get("reasons") or {}).get("form1040.line-25b") or []
    asks_present = PRESENT in json.dumps(v85) or any("no closed sale" in str(s) for s in reasons)
    asks_amount = AMOUNT in json.dumps(v85) or any("report no closed sale" in str(s) and "Enter" in str(s) for s in reasons)
    if v84_ok and v85_blocked and asks_present:
        return {"class": "asks_no_sale_present", "v85_missing": missing[:8]}
    if v84_ok and v85_blocked and asks_amount:
        return {"class": "asks_no_sale_amount", "v85_missing": missing[:8]}
    v84_blocked = isinstance(v84_line, str) and "block" in str(v84_line)
    if v84_blocked and v85_blocked:
        changed = _diff(v84, v85)
        if asks_present:
            return {"class": "still_blocked_also_asks_present", "changed": changed[:24]}
        return {"class": "still_blocked", "changed": changed[:24]}
    return {"class": "counterexample", "changed": _diff(v84, v85)[:24]}


def _published_v84(test: Any) -> Any:
    return test.track0().h.Core("v84", "v82", "v82")


def _pin_run(test: Any, core: Any, acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    t = test.track0()
    with t.h.loader_entries(core):
        return test.pin(t.run_coordinate(core, acts, run_id))


def _pair(item: tuple[str, list[dict[str, Any]]]) -> tuple[str, dict[str, Any]]:
    key, acts = item
    test = load_test()
    slug = key.replace("/", ".")
    v85 = scratch_core(test, Path(os.environ["B4ONLY_CORE"]))
    v84 = _published_v84(test)
    pin85 = _pin_run(test, v85, acts, "demo.b4only.nb.v85." + slug)
    pin84 = _pin_run(test, v84, acts, "demo.b4only.nb.v84." + slug)
    row = classify(pin84, pin85)
    if row["class"] != "identical":
        row["v84_line25b"] = pin84.get("error") or (pin84.get("lines") or {}).get("form1040.line-25b")
        row["v85_line25b"] = pin85.get("error") or (pin85.get("lines") or {}).get("form1040.line-25b")
    return key, row


def tasks(test: Any, expected: dict[str, Any]) -> list[tuple[str, list[dict[str, Any]]]]:
    t = test.track0()
    print("building track 0 act lists", flush=True)
    cases = dict(test.decided_cases(t))
    print("exporting the 213 returns", flush=True)
    with tempfile.TemporaryDirectory() as tmp:
        exported = test.export_returns(Path(tmp))
    returns = test.return_acts(t, exported)
    v84 = _published_v84(test)
    out: list[tuple[str, list[dict[str, Any]]]] = []
    for key in expected["track0"]:
        out.append((f"track0/{key}", cases[key]))
    for key in expected["returns"]:
        out.append((f"returns/{key}", returns[key]))
    for key in expected["zero_sample"]:
        out.append((f"zero/{key}", test.with_zero(t, returns[key], v84)))
    return out


def main() -> None:
    if len(sys.argv) not in (2, 3):
        raise SystemExit("usage: rerun.py <scratch-core.json> [output.json]")
    core_path = Path(sys.argv[1]).resolve()
    out_name = sys.argv[2] if len(sys.argv) == 3 else "rerun-output.json"
    out_path = HERE / out_name
    if out_path.parent != HERE or out_path.suffix != ".json":
        raise SystemExit("output must be a json file in the evidence directory")
    os.environ["B4ONLY_CORE"] = str(core_path)
    test = load_test()
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    work = tasks(test, expected)
    only = {item for item in os.environ.get("B4ONLY_RERUN_ONLY", "").split(",") if item}
    if only:
        work = [item for item in work if item[0] in only]
        missing = only - {item[0] for item in work}
        if missing:
            raise SystemExit(f"unknown recorded ids: {sorted(missing)[:8]}")
    workers = int(os.environ.get("B4ONLY_WORKERS") or min(6, os.cpu_count() or 2))
    print(f"running {len(work)} recorded returns on live v84 and scratch v85", flush=True)
    found: dict[str, dict[str, Any]] = {}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        done = 0
        for key, row in pool.map(_pair, work):
            found[key] = row
            done += 1
            if done % 20 == 0 or done == len(work):
                print(f"{done}/{len(work)} {key} {row['class']}", flush=True)
    counts = dict(Counter(found[key]["class"] for key in found))
    changes = [{"id": key, **found[key]} for key in sorted(found) if found[key]["class"] != "identical"]
    asks = [key for key in sorted(found) if found[key]["class"] == "asks_no_sale_present"]
    identical = [key for key in sorted(found) if found[key]["class"] == "identical"]
    payload = {
        "core": "live-v84-and-live-v85",
        "compared_to": "live v84 against live scratch v85; recorded answers, not substituted",
        "answers": "recorded, not substituted",
        "runs": len(found),
        "live_runs": len(found) * 2,
        "counts": counts,
        "classes": {key: found[key]["class"] for key in sorted(found)},
        "asks_no_sale_present_ids": asks,
        "identical_ids": identical,
        "changes": changes,
        "change_count": len(changes),
    }
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"rerun output contains {needle}")
    out_path.write_text(text, encoding="utf-8")
    print(json.dumps({"runs": len(found), "counts": counts, "changes": len(changes),
                      "output": out_path.name}, indent=2))


if __name__ == "__main__":
    main()
