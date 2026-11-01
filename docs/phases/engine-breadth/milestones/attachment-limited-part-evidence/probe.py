"""P0 probe (attachment-limited-part): on the real coordinator (live_coordinate_run, core v69 /
release v67 / registry v67), run the #245 cases and read what the Schedule A attachment does today:
published (and with which parts and tie-outs) or blocked (and on what), beside the published lines
the attachment is meant to match (8a, 16, the total, line 12e).

Cases: a standard-deduction filer with winnings and losses; an itemizer (Form 1098) with losses
below winnings; a losses-only itemizer (no Form 1098); an itemizer with losses above winnings
(rows 9,000, line 16 6,000); an itemizer without losses (the control).
Synthetic demo.* data only. Reuses the committed tests' helpers (which build the returns on the
v67 declarations; core v69 adds none that these returns need); changes nothing. From the repo root:

    python3 docs/phases/engine-breadth/milestones/attachment-limited-part-evidence/probe.py
"""
from __future__ import annotations

import copy
import json
import sys
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.derivation.production_resolver import PublicationSurface  # noqa: E402
from tests import test_w2g_gambling as w2g  # noqa: E402
from tests.helpers import current_core_returns as c  # noqa: E402
from tests.test_form_1099_k_income import _handover  # noqa: E402
from tests.test_refund_or_amount_owed_track1 import _finish  # noqa: E402

P = c.P
CONTENT = c.CONTENT
RELEASE_DIR = c.RELEASE_DIR
PACKAGE = CONTENT / "package.core-calculations.v69.json"
RELEASE = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v67.json"
SURFACE = PublicationSurface(RELEASE_DIR, CONTENT / "published-packages.v67.json", CONTENT)
ATTACHMENT = P + "scheduleA.disposition"
LINES = ("schedule-a.line8a", "schedule-a.line16", "schedule-a.total", "gambling.losses-subtotal",
         "gambling.b1-winnings-subtotal", "deductions.line-12e", "income.taxable-income")


def run_v69(acts: list[dict[str, object]], run_id: str) -> dict[str, Any]:
    finished = _finish(copy.deepcopy(acts), package_path=PACKAGE, package_version="v69", release_path=RELEASE,
                       release_version="v67", note=run_id)
    finished = _handover(finished, surface=SURFACE, reconfirm=True)
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"), repo_root=c.ROOT, authoritative_acts=finished,
            workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user=c.USER, request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
            surface=SURFACE, output_name="out.json",
        )
        if outcome.refusal is not None:
            return {"refusal": f"{outcome.refusal.reason} {outcome.refusal.detail}"}
        pubs = {str(p.finding["symbol"]): p.finding for p in outcome.publications or ()}
        report = json.loads(outcome.output_path.read_text(encoding="utf-8")) if outcome.output_path else {}
    disp = [r for r in report.get("dispositions", []) if r.get("artifact_id") == P + "rule.attachment.schedule-a"]
    out: dict[str, Any] = {"lines": {}}
    for s in LINES:
        if P + s in pubs:
            out["lines"][s] = format(Decimal(str(pubs[P + s]["value"])).normalize(), "f")
    out["attachment_disposition"] = [
        {k: (v if k != "pins" else len(v)) for k, v in r.items() if k in ("disposition", "code", "missing", "pins")}
        for r in disp]
    for r in out["attachment_disposition"]:
        if "missing" in r:
            r["missing"] = [str(m).replace(P, "") for m in r["missing"]]
    if ATTACHMENT in pubs:
        v = pubs[ATTACHMENT]["value"]
        out["attachment"] = {
            "required": v["required"],
            "parts": [{"part_id": p["part_id"],
                       "row_sums": [r["row_sum"] for r in p["row_sets"]],
                       "part_sum": p["part_sum"],
                       "tie_out": {"line": p["tie_out"]["line_symbol"].replace(P, ""), "value": p["tie_out"]["line_value"]}}
                      for p in v["itemizations"]],
        }
    out["other_blocked"] = sorted({str(r.get("artifact_id")).replace(P, "") for r in report.get("dispositions", [])
                                   if r.get("disposition") == "blocked"} - {"rule.attachment.schedule-a"})
    return out


def main() -> None:
    w2g_ret = lambda: [(6000.0, 1440.0)]  # noqa: E731  one Form W-2G: winnings 6,000, withholding 1,440
    cases: dict[str, list[dict[str, object]]] = {}
    cases["case0_standard_deduction_with_losses"] = c.add_gambling_losses(w2g._w2g_return(w2g_ret()), [2000.0])
    cases["case1_itemizer_mortgage_20000_losses_2000"] = c.declare_no_other_line16(
        c.add_gambling_losses(c.add_mortgage_itemizer(w2g._w2g_return(w2g_ret()), 20000.0), [2000.0]))
    cases["case2_losses_only_itemizer_winnings_20000_losses_20000"] = c.declare_no_other_line16(
        c.add_gambling_losses(w2g._w2g_return([(20000.0, 4800.0)]), [20000.0]))
    cases["case3_itemizer_losses_9000_above_winnings_6000"] = c.declare_no_other_line16(
        c.add_gambling_losses(c.add_mortgage_itemizer(w2g._w2g_return(w2g_ret()), 20000.0), [9000.0]))
    cases["case4_itemizer_no_losses_control"] = c.declare_no_other_line16(
        c.add_gambling_losses(c.add_mortgage_itemizer(w2g._w2g_return(w2g_ret()), 20000.0), []))
    result = {name: run_v69(acts, f"demo.alp.{i}") for i, (name, acts) in enumerate(cases.items())}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
