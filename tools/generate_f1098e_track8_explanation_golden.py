"""Track 8: explain a real Form 1098-E / Student Loan Interest route's own
pin chain, live.

Runs the ``below-floor`` scenario (Track 6 path (b): single statement, full
eligibility, MAGI below the phaseout floor -- also one of this track's own
presentation goldens, ``tools.generate_f1098e_track8_presentation_goldens``)
through the real coordinator (``live_coordinate_run``), then walks
``tax.us.2025.income.agi``'s own pin chain with the already-shipped,
milestone-agnostic explanation walker (``packages/derivation/
explanation.py``): AGI <- Schedule 1 line 26 (total adjustments) <- the SLI
worksheet's own published Schedule 1 line 21 <- the worksheet's twenty-nine
pins (eligibility components, MAGI phaseout parameters, the closure-backed
family, the capped line-1 subtotal, ...).

``LiveCoordinatorOutcome.publications`` (an additive field this track added)
carries the full in-memory publication list the live run already computed --
the two durable output artifacts intentionally summarize dispositions without
a `value` field, which is enough for the presentation projector but not for
`explain()`'s node values. No RunContext shortcut: every value here is the
real live path's own output, walked, not re-derived.

Deterministic and demoable: the same scenario always prints the same report,
which is what the paired golden-regression test pins, exactly like
``tests/derivation/test_explanation_cli.py``'s own subprocess-pinned pattern.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from packages.derivation.explanation import ExplanationNode, explain, index_derived, render_text
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from tests.test_f1098e_student_loan_interest_agi_track6 import Statement, _f1098e_acts, _renumber
from tools.generate_f1098e_track8_presentation_goldens import USER, SCOPE, _surface

TARGET_SYMBOL = "tax.us.2025.income.agi"


def _acts() -> list[dict[str, object]]:
    statements = [Statement(lender="demo.f1098e.t8.lender.bf", stmt="demo.f1098e.t8.stmt.bf", box1=3000.0)]
    return _f1098e_acts(statements=statements, close=True, wages=50000)


def build_report() -> dict[str, Any]:
    acts = _renumber(_acts())
    with TemporaryDirectory() as raw:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(raw) / "L"), repo_root=ROOT, authoritative_acts=acts,
            workspace_revision=len(acts), run_scope=SCOPE, scope_user=USER,
            request={"schema": "run-request.v1"}, run_id="demo.f1098e.t8.explain.below-floor",
            governance_pins=[], surface=_surface(), output_name="explain.json",
        )
        assert outcome.refusal is None, outcome.refusal
        assert outcome.publications is not None
        derived = index_derived([pub.finding for pub in outcome.publications])
        target = next(
            finding for finding in derived.values() if finding["symbol"] == TARGET_SYMBOL
        )
        node = explain(target["id"], role="output", derived=derived)
        return {"run_id": outcome.run_id, "target_symbol": TARGET_SYMBOL, "explanation": node.to_dict()}


def _human(report: dict[str, Any]) -> str:
    def _node(d: dict[str, Any]) -> ExplanationNode:
        return ExplanationNode(
            finding_id=d["finding_id"], role=d["role"], kind=d["kind"], symbol=d["symbol"],
            value=d["value"], version=d["version"], produced_by=d["produced_by"],
            children=tuple(_node(c) for c in d["children"]),
        )

    lines = [f"Run: {report['run_id']}", f"Target: {report['target_symbol']}", "Explanation:"]
    lines.append(render_text(_node(report["explanation"]), indent=1))
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print the JSON report instead of the human summary")
    args = parser.parse_args(argv)

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(_human(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
