"""Repair evidence (FSR-R3): the controls and tests fail when the tool stops comparing a part.

Run: python3 repair_mutations.py
Each mutation replaces one function of tools.recorded_replay in memory for the
length of the run (nothing is written to the tool).  For each, the standard
controls on two real saved outputs (the harness wage return and the synthetic
mortgage return) and the fast tests of the strict classifier are run; the
output lists what stops passing.  The unmutated run must list nothing.
"""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
import pytest  # noqa: E402

from tests import test_recorded_replay_full_surface as suite  # noqa: E402
from tools import recorded_replay as rr  # noqa: E402

ORIGINAL_SNAPSHOT = rr.snapshot
ORIGINAL_SAME = rr._same


def dropping(predicate):  # type: ignore[no-untyped-def]
    def snapshot(model, report):  # type: ignore[no-untyped-def]
        snap = ORIGINAL_SNAPSHOT(model, report)
        snap["records"] = [r for r in snap["records"] if not predicate(r)]
        return snap
    return snapshot


MUTATIONS = {
    "none": lambda: None,
    "drop every graph record": lambda: setattr(rr, "snapshot", dropping(lambda r: r[0] == "graph")),
    "drop every other-model-key record": lambda: setattr(rr, "snapshot", dropping(lambda r: r[0] == "model")),
    "drop the mortgage explanation block": lambda: setattr(
        rr, "snapshot", dropping(lambda r: r[0] == "model" and r[1].startswith("mortgageBorrowingExplanation") or r[2].startswith("mortgageBorrowingExplanation"))),
    "compare values with plain ==": lambda: setattr(rr, "_same", lambda a, b: a == b),
}


class Collect:
    def __init__(self) -> None:
        self.failed: list[str] = []

    def pytest_runtest_logreport(self, report):  # type: ignore[no-untyped-def]
        if report.when == "call" and report.failed:
            self.failed.append(report.nodeid.split("::", 1)[1])


def main() -> None:
    harness = rr._get_harness()
    outputs = {
        "wage return": rr.saved_output("v96", harness.opened(), "demo.fsr.mut1"),
        "mortgage return": rr.saved_output("v96", suite.mortgage_explanation_acts(), "demo.fsr.mut2"),
    }
    results = {}
    for name, apply in MUTATIONS.items():
        rr.snapshot, rr._same = ORIGINAL_SNAPSHOT, ORIGINAL_SAME
        apply()
        controls = {}
        for label, saved in outputs.items():
            verdicts = rr.run_controls(saved["model"], saved["report"])
            controls[label] = sorted(k for k, v in verdicts.items() if v["available"] and not v["ok"])
        collector = Collect()
        with contextlib.redirect_stdout(io.StringIO()):
            pytest.main(["-q", "-n", "0", "-p", "no:cacheprovider", "-k", "not real_saved and not mortgage_explanation_block",
                         str(REPO / "tests/test_recorded_replay_full_surface.py")], plugins=[collector])
        results[name] = {"controls_that_stop_failing": controls, "tests_that_fail": sorted(collector.failed)}
    rr.snapshot, rr._same = ORIGINAL_SNAPSHOT, ORIGINAL_SAME
    print(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
