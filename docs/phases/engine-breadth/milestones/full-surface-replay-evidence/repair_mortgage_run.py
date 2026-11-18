"""Repair evidence (FSR-R1): v95 against v96 on the synthetic mortgage list, with the declared changes.

Run: python3 repair_mortgage_run.py
The 775 recorded lists reach none of the mortgage explanation block; this one
list does.  The expectations are the same 133 as track1_demo.py; the ones the
775 lists left unused and this list uses are reported.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from tests import test_recorded_replay_full_surface as suite  # noqa: E402
from tools import recorded_replay as rr  # noqa: E402

sys.path.insert(0, str(HERE))
import track1_demo  # noqa: E402

def main() -> None:
    full = json.loads((HERE / "track1-v95-v96.json").read_text())
    unused_before = {row["note"] for row in full["unused_expectations"]}
    expectations = track1_demo.declared_expectations()
    summary = rr.run_full("v95", "v96", expectations, workers=1, lists=[("demo/mortgage-borrowing", suite.mortgage_explanation_acts())])
    unused_after = {row["note"] for row in summary["unused_expectations"]}
    out = {
        "lists": summary["lists"], "classes": summary["classes"], "unexpected_differences": summary["unexpected_differences"],
        "optional_blocks_reached": summary["optional_blocks_reached"],
        "expectations_used": summary["expectations_used"],
        "used_here_but_unused_on_the_775": sorted(unused_before - unused_after),
        "still_unused": sorted(unused_before & unused_after),
    }
    text = json.dumps(out, indent=1) + "\n"
    rr._check_no_local_paths(text, "repair-mortgage-v95-v96.json")
    (HERE / "repair-mortgage-v95-v96.json").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
