"""Track 1 controls on one real saved output (core v96, one recorded list).

Run: python3 track1_controls.py
Two saved outputs are used: a recorded list (blocked rows with missing names
and questions) and a synthetic wage return whose line 12e publishes a value.
A control that has no target on one output is judged on the other.  The saved model and report are mutated before the snapshot is taken; each
mutation must fail the strict comparison and the one expected sentence change
must pass.  Writes track1-controls.json next to this file.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from tools import recorded_replay as rr  # noqa: E402

KEY = "v83/returns/case/a_duplicate_on_direct/recorded"


def wage_return() -> list[dict]:
    spec = importlib.util.spec_from_file_location("fsr_l6b", HERE.parent / "line6b-reason-evidence/probe.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["fsr_l6b"] = module
    spec.loader.exec_module(module)
    return module.base("single", benefits=False)  # type: ignore[no-any-return]


def main() -> None:
    outputs = {}
    for name, acts in (("recorded", dict(rr.recorded_lists())[KEY]), ("wage", wage_return())):
        saved = rr.saved_output("v96", acts, "demo.fsr.controls." + name)
        assert saved["outcome"] == "success"
        outputs[name] = saved
    per_output = {name: rr.run_controls(s["model"], s["report"]) for name, s in outputs.items()}
    controls = {}
    for name in per_output["recorded"]:
        judged = {o: v[name] for o, v in per_output.items() if v[name]["available"]}
        controls[name] = {"judged_on": sorted(judged), "ok": bool(judged) and all(v["ok"] for v in judged.values()),
                          "per_output": judged}
    out = {
        "core": "v96",
        "outputs": {
            name: {"records": len(rr.snapshot(s["model"], s["report"])["records"]),
                   "page_fields": len(s["model"]["sections"]), "report_rows": len(s["report"]["dispositions"])}
            for name, s in outputs.items()
        },
        "recorded_list": KEY,
        "second_snapshot_identical": all(
            rr.diff_snapshots(rr.snapshot(s["model"], s["report"]), rr.snapshot(s["model"], s["report"])) == []
            for s in outputs.values()
        ),
        "controls": controls,
        "all_ok": all(c["ok"] for c in controls.values()),
    }
    text = json.dumps(out, indent=1) + "\n"
    rr._check_no_local_paths(text, "controls")
    (HERE / "track1-controls.json").write_text(text)
    print(json.dumps({k: out[k] for k in ("outputs", "all_ok")}, indent=1))
    print({n: c["judged_on"] for n, c in controls.items()})
    assert out["all_ok"]


if __name__ == "__main__":
    main()
