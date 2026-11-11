"""Replay recorded v83 returns on patched v85 and scratch v86.

Evidence for docs/phases/engine-breadth/milestones/selection-keyed-collect.md.
Charter: docs/reviews/selection-keyed-collect/charter-p0.md.

Each recorded return is run as recorded, then with the v85 no-sale box 4
present question answered no when that question appears.

    python3 rerun.py /path/outside/core.json
"""

from __future__ import annotations

import copy
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
EXPECTED = REPO / "tests/fixtures/f1099b_backup_withholding_v83/expected.json"
TEST = REPO / "tests/test_f1099b_backup_withholding_v83.py"
PRESENT = "tax.us.2025.f1099b.no-sale-box4-present"


def load_test() -> Any:
    name = "skc_p0_v83_test"
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(name, TEST)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def _load_engine(scratch: Path) -> None:
    root = str(scratch)
    if root in sys.path:
        sys.path.remove(root)
    sys.path.insert(0, root)
    if str(REPO) not in sys.path:
        sys.path.append(str(REPO))


def scratch_core(test: Any, core_path: Path) -> Any:
    body = json.loads(core_path.read_text(encoding="utf-8"))
    t = test.track0()
    return t.h.Core(
        body["version"], body["registry"], body["release_version"],
        content=Path(body["content"]), releases=Path(body["releases"]),
        loader_from=body.get("loader_from"),
    )


def published_v85(test: Any) -> Any:
    return test.track0().h.Core("v85", "v83", "v83")


def _pin_run(test: Any, core: Any, acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    t = test.track0()
    with t.h.loader_entries(core):
        return test.pin(t.run_coordinate(core, acts, run_id))


def answer_present_no(test: Any, core: Any, acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    t = test.track0()
    return t.h.say(copy.deepcopy(acts), PRESENT, "no", "skc-present-no", core.content)


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


def classify(v85: dict[str, Any], v86: dict[str, Any]) -> dict[str, Any]:
    if v85 == v86:
        return {"class": "identical"}
    if "error" in v85 or "error" in v86:
        return {"class": "counterexample", "changed": _diff(v85, v86)[:16]}
    v85_line = (v85.get("lines") or {}).get("form1040.line-25b")
    v86_line = (v86.get("lines") or {}).get("form1040.line-25b")
    rows85 = json.dumps(v85.get("rows") or {})
    rows86 = json.dumps(v86.get("rows") or {})
    symbol_gone = "f1099b-b4-amount-symbol" in rows85 and "f1099b-b4-amount-symbol" not in rows86
    line_same = v85_line == v86_line
    changed = _diff(v85, v86)
    payment = {item for item in changed if item.startswith("lines.form1040.line-25") or item.startswith("lines.form1040.line-3") or item.startswith("rows.form1040-line25") or item.startswith("rows.rule.f1099b-b4")}
    if line_same and symbol_gone and set(changed) <= payment | {
        "rows.rule.f1099b-b4-amount-symbol", "rows.rule.f1099b-b4-withholding-subtotal",
    }:
        return {"class": "lines_identical_symbol_retired", "changed": changed[:16]}
    asks = PRESENT in json.dumps(v85) or any(
        "no closed sale" in str(s) for s in (v85.get("reasons") or {}).get("form1040.line-25b") or [])
    if asks and v85_line == "blocked":
        return {"class": "asks_no_sale_present", "v85_line25b": v85_line, "v86_line25b": v86_line}
    if line_same:
        return {"class": "lines_identical_other", "changed": changed[:16]}
    return {"class": "counterexample", "changed": changed[:16], "v85_line25b": v85_line, "v86_line25b": v86_line}


def _pair(item: tuple[str, list[dict[str, Any]], str]) -> tuple[str, dict[str, Any]]:
    key, acts, mode = item
    scratch = Path(os.environ["SKC_SCRATCH"])
    _load_engine(scratch)
    test = load_test()
    v85 = published_v85(test)
    v86 = scratch_core(test, Path(os.environ["SKC_CORE"]))
    if mode == "present_no":
        acts85 = answer_present_no(test, v85, acts)
        acts86 = answer_present_no(test, v86, acts)
    else:
        acts85 = acts
        acts86 = acts
    slug = key.replace("/", ".") + "." + mode
    pin85 = _pin_run(test, v85, acts85, "demo.skc.nb.v85." + slug)
    pin86 = _pin_run(test, v86, acts86, "demo.skc.nb.v86." + slug)
    row = classify(pin85, pin86)
    if row["class"] not in {"identical", "lines_identical_symbol_retired"}:
        row["v85_line25b"] = pin85.get("error") or (pin85.get("lines") or {}).get("form1040.line-25b")
        row["v86_line25b"] = pin86.get("error") or (pin86.get("lines") or {}).get("form1040.line-25b")
    return f"{key}/{mode}", row


def tasks(test: Any, expected: dict[str, Any]) -> list[tuple[str, list[dict[str, Any]]]]:
    t = test.track0()
    cases = dict(test.decided_cases(t))
    with tempfile.TemporaryDirectory() as tmp:
        exported = test.export_returns(Path(tmp))
    returns = test.return_acts(t, exported)
    v85 = published_v85(test)
    out: list[tuple[str, list[dict[str, Any]]]] = []
    for key in expected["track0"]:
        out.append((f"track0/{key}", cases[key]))
    for key in expected["returns"]:
        out.append((f"returns/{key}", returns[key]))
    for key in expected.get("zero_sample") or []:
        out.append((f"zero/{key}", test.with_zero(t, returns[key], v85)))
    return out


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: rerun.py <scratch-core.json>")
    core_path = Path(sys.argv[1]).resolve()
    scratch = core_path.parent
    os.environ["SKC_SCRATCH"] = str(scratch)
    os.environ["SKC_CORE"] = str(core_path)
    _load_engine(scratch)
    test = load_test()
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    recorded = tasks(test, expected)
    work: list[tuple[str, list[dict[str, Any]], str]] = []
    for key, acts in recorded:
        work.append((key, acts, "recorded"))
        work.append((key, acts, "present_no"))
    only = {item for item in os.environ.get("SKC_RERUN_ONLY", "").split(",") if item}
    if only:
        work = [item for item in work if f"{item[0]}/{item[2]}" in only or item[0] in only]
    workers = int(os.environ.get("SKC_WORKERS") or min(6, os.cpu_count() or 2))
    print(f"running {len(work)} recorded variants on v85 and v86", flush=True)
    found: dict[str, dict[str, Any]] = {}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        done = 0
        for key, row in pool.map(_pair, work):
            found[key] = row
            done += 1
            if done % 20 == 0 or done == len(work):
                print(f"{done}/{len(work)} {key} {row['class']}", flush=True)
    counts = dict(Counter(found[key]["class"] for key in found))
    changes = [{"id": key, **found[key]} for key in sorted(found) if found[key]["class"] not in {
        "identical", "lines_identical_symbol_retired", "asks_no_sale_present",
    }]
    payload = {
        "cores": ["v85", "v86"],
        "runs": len(found),
        "live_runs": len(found) * 2,
        "counts": counts,
        "classes": {key: found[key]["class"] for key in sorted(found)},
        "changes": changes,
        "change_count": len(changes),
        "asks_no_sale_present_ids": [key for key in sorted(found) if found[key]["class"] == "asks_no_sale_present"],
        "lines_identical_symbol_retired_ids": [
            key for key in sorted(found) if found[key]["class"] == "lines_identical_symbol_retired"
        ],
        "identical_ids": [key for key in sorted(found) if found[key]["class"] == "identical"],
    }
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"rerun output contains {needle}")
    (HERE / "rerun-output.json").write_text(text, encoding="utf-8")
    print(json.dumps({"runs": len(found), "counts": counts, "changes": len(changes),
                      "output": "rerun-output.json"}, indent=2))


if __name__ == "__main__":
    main()
