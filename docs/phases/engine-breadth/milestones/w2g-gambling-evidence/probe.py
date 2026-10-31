"""P0 probe: how a return with gambling winnings is refused on core v64.

Runs synthetic returns through packages.derivation.live.live_coordinate_run on the
committed core v64 package. Reuses the committed test builders for the base return
(wages, W-2 box 2, every closure, every absence answer). Nothing in the repository is
modified; the output is written to probe-output.json beside this file.

Run from the repository root:  python3 docs/phases/engine-breadth/milestones/w2g-gambling-evidence/probe.py

Each scenario changes only the absence answers (or nothing); core v64 has no fact type
for a Form W-2G, so there is no way to record the winnings themselves.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.derivation.production_resolver import PublicationSurface  # noqa: E402
from tests.test_form_1099_k_income import _handover  # noqa: E402
from tests.test_form_1099_withholding import (  # noqa: E402
    CONTENT,
    RELEASE_DIR,
    _add,
    _assert,
    _base,
    _introduce,
    _social_security_withholding,
    _unemployment_withholding,
)
from tests.test_refund_or_amount_owed_track1 import ROOT, USER, _finish  # noqa: E402

PACKAGE_V64 = CONTENT / "package.core-calculations.v64.json"
RELEASE_V62 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v62.json"
SURFACE_V64 = PublicationSurface(RELEASE_DIR, CONTENT / "published-packages.v62.json", CONTENT)

P = "tax.us.2025."
OTHER_INCOME = P + "schedule1-part1-scope.no-sch1-other-income"
GAMBLING_A = P + "schedule-a-boundary.no-gambling-other-declared"
INTEREST = ("schedule1-line10", "form1040-line8", "form1040-line25c", "form1040-line25d",
            "schedule-a", "form1040-line12", "form1040-line11")
SYMBOLS = {
    "line8_additional_income": P + "income.additional-income",
    "schedule1_line10": P + "schedule1.line10-additional-income",
    "total_income": P + "income.total-income",
    "agi": P + "income.agi",
    "taxable_income": P + "income.taxable-income",
    "line24_total_tax": P + "tax.line24-total-tax",
    "line25a": P + "payments.line25a",
    "line25b": P + "payments.line25b",
    "line25c": P + "payments.line25c",
    "line25d": P + "payments.line25d",
    "line33": P + "payments.line33",
    "line35a_refund": P + "payments.line35a-refunded",
    "line37_owed": P + "payments.line37-amount-owed",
}


def set_answer(acts: list[dict[str, object]], fact_type: str, value: object) -> None:
    hits = 0
    for act in acts:
        finding = cast(dict[str, Any], act["payload"]).get("finding")
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(fact_type + "|"):
            finding["value"] = value
            hits += 1
    assert hits == 1, (fact_type, hits)


def base_acts(*, wages: float = 50000.0, w2_withheld: float = 4500.0, joint: bool = False) -> list[dict[str, object]]:
    acts = _base(wages=wages, w2_withheld=w2_withheld, joint=joint)
    _unemployment_withholding(acts, [])
    _social_security_withholding(acts, [])
    return acts


def throwaway_w2g_bundle() -> dict[str, Any]:
    """The design's two amount fact types (P0 section 3.1), as a bundle held only in this
    probe's act log. It is not a repository citizen and is not part of any package."""
    keys = [
        {"kind": "entity", "name": "payer", "entity_kind": "tax.us.gambling-payer"},
        {"kind": "entity", "name": "statement", "entity_kind": "tax.us.w2g-statement"},
        {"kind": "literal", "name": "tax-year", "values": ["2025"]},
    ]
    def amount(fid: str, title: str) -> dict[str, Any]:
        return {"schema": "fact-type.v2", "id": fid, "version": "v1", "title": title,
                "nature": "determinable", "identity_keys": keys,
                "value_schema": {"type": "number", "minimum": 0}, "supersession": {"policy": "free"}}
    return {"schema": "bundle.v2", "id": "demo.probe.w2g.vocabulary", "version": "v1",
            "label": "Throwaway W-2G amount fact types (probe only)",
            "fact_types": [amount(P + "w2g.box1-winnings", "Form W-2G box 1 (probe only)"),
                           amount(P + "w2g.box4-withholding", "Form W-2G box 4 (probe only)")]}


def with_w2g_recorded(acts: list[dict[str, object]], box1: float, box4: float) -> list[dict[str, object]]:
    acts = copy.deepcopy(acts)
    _add(acts, "bundle-adoption", {"bundle": throwaway_w2g_bundle()})
    _introduce(acts, "demo.w2g.payer.1", "tax.us.gambling-payer")
    _introduce(acts, "demo.w2g.stmt.1", "tax.us.w2g-statement")
    keys = (("payer", "demo.w2g.payer.1"), ("statement", "demo.w2g.stmt.1"))
    _assert(acts, "demo.w2g.probe.box1", P + "w2g.box1-winnings", keys, box1)
    _assert(acts, "demo.w2g.probe.box4", P + "w2g.box4-withholding", keys, box4)
    return acts


def run(acts: list[dict[str, object]], run_id: str) -> dict[str, Any]:
    finished = _finish(
        copy.deepcopy(acts), package_path=PACKAGE_V64, package_version="v64",
        release_path=RELEASE_V62, release_version="v62", note=run_id,
    )
    finished = _handover(finished, surface=SURFACE_V64, reconfirm=True)
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"), repo_root=ROOT, authoritative_acts=finished,
            workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user=USER, request={"schema": "run-request.v1"}, run_id=run_id,
            governance_pins=[], surface=SURFACE_V64, output_name="out.json",
        )
        if outcome.refusal is not None:
            return {"refusal": str(outcome.refusal.reason), "detail": str(outcome.refusal.detail)}
        pubs = {str(i.finding["symbol"]): i.finding for i in outcome.publications or ()}
        report = json.loads(Path(outcome.output_path).read_text(encoding="utf-8")) if outcome.output_path else {}
    blocked = [
        {"artifact": str(r["artifact_id"]).replace(P, ""), "code": r["code"],
         "missing": [str(m).replace(P, "") for m in r["missing"]]}
        for r in report.get("dispositions", []) if r.get("disposition") == "blocked"
    ]
    # the first (root) causes: blocks whose code is not a plain downstream DEPENDENCY_ABSENT
    return {
        "values": {k: (pubs[s]["value"] if s in pubs else None) for k, s in SYMBOLS.items()},
        "blocked_count": len(blocked),
        "blocked_roots": sorted((b for b in blocked if b["code"] != "DEPENDENCY_ABSENT"),
                                key=lambda b: b["artifact"]),
        "blocked_all": sorted(b["artifact"] for b in blocked),
        "dispositions_of_interest": [
            {k: r.get(k) for k in ("artifact_id", "disposition", "code", "missing") if k in r}
            for r in report.get("dispositions", [])
            if any(t in str(r.get("artifact_id", "")) for t in INTEREST)
            and r.get("disposition") != "published"
        ],
        "disposition_kinds": sorted({str(r.get("disposition")) for r in report.get("dispositions", [])}),
    }


def main() -> None:
    out: dict[str, Any] = {"core": "v64", "scenarios": {}}
    sc = out["scenarios"]
    sc["S0_no_gambling"] = run(base_acts(), "demo.w2g.p0.s0")

    a = base_acts(); set_answer(a, OTHER_INCOME, "no")
    sc["S1_other_income_answered_no"] = run(a, "demo.w2g.p0.s1")

    a = base_acts(); set_answer(a, GAMBLING_A, "no")
    sc["S2_schedule_a_gambling_answered_no"] = run(a, "demo.w2g.p0.s2")

    a = base_acts(); set_answer(a, OTHER_INCOME, "no"); set_answer(a, GAMBLING_A, "no")
    sc["S3_both_no"] = run(a, "demo.w2g.p0.s3")

    # The silent hazard: nothing can record a W-2G on v64, so a filer who answers yes to both
    # is computed with the winnings left out (the answers, not the engine, hold the boundary).
    sc["S4_both_yes_is_S0"] = {"same_values_as_S0": sc["S0_no_gambling"]["values"]
                                == run(base_acts(), "demo.w2g.p0.s4")["values"]}
    # A log that carries a W-2G (as a successor package would record it), run on v64: is the
    # amount refused, or silently left out? (ADR-0082 decision 4 is the standing answer for the
    # withholding amounts v59 added.)
    sc["S5_w2g_in_log_run_on_v64"] = run(with_w2g_recorded(base_acts(), 6000.0, 1440.0), "demo.w2g.p0.s5")
    sc["S5_w2g_in_log_run_on_v64"]["same_values_as_S0"] = (
        sc["S5_w2g_in_log_run_on_v64"].get("values") == sc["S0_no_gambling"]["values"])

    # Twin runs. Core v64 cannot record a W-2G, so each hand-computed case (see
    # p0-trace-and-design.md section 5) is checked against the engine's own tax table by running
    # a wage-only return with the same adjusted gross income and the same total withholding.
    # This checks the arithmetic (tax table, standard deduction, payments), not the route.
    twins = {
        "T1_single_1200_no_withholding": (dict(wages=51200.0, w2_withheld=4500.0), {"agi": "51200", "taxable_income": "35450", "line24_total_tax": "4019", "line25d": "4500", "line35a_refund": "481", "line37_owed": "0"}),
        "T2_single_6000_1440_withheld": (dict(wages=56000.0, w2_withheld=5940.0), {"agi": "56000", "taxable_income": "40250", "line24_total_tax": "4595", "line25d": "5940", "line35a_refund": "1345", "line37_owed": "0"}),
        "T3_joint_base_80000": (dict(wages=80000.0, w2_withheld=7000.0, joint=True), {"agi": "80000", "taxable_income": "48500", "line24_total_tax": "5346", "line25d": "7000", "line35a_refund": "1654", "line37_owed": "0"}),
        "T4_joint_two_w2g_5000_720_withheld": (dict(wages=85000.0, w2_withheld=7720.0, joint=True), {"agi": "85000", "taxable_income": "53500", "line24_total_tax": "5946", "line25d": "7720", "line35a_refund": "1774", "line37_owed": "0"}),
    }
    out["twins"] = {}
    for name, (kw, expected) in twins.items():
        got = run(base_acts(**kw), "demo.w2g.p0." + name)["values"]
        out["twins"][name] = {"expected_by_hand": expected,
                              "engine": {k: got[k] for k in expected},
                              "match": all(got[k] == v for k, v in expected.items())}
    Path(__file__).with_name("probe-output.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
