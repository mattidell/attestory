"""Track 0 probe: the allocation lifecycle on the ADR-0073 retraction contract,
against the COMMITTED Form 1099-INT report identity.

Vocabulary, used strictly throughout (owner direction 2026-09-07):

  actor / workspace operator   the person recorded on an act (Matt, Alex)
  allocation recipient         the named other person interest is allocated to
                               (Pat, Kim) -- never an author of anything here
  taxpayer / workspace subject the person whose return this is
  payer report                 the documentary Form 1099-INT box-1 report

THE SELECTED WORKSPACE MODEL. The canonical fact is ONE SHARED CURRENT
WORKSPACE ANSWER per (payer report, allocation recipient). It is NOT a
separately individuated personal statement belonging to its author. Each
assertion or correction act records which actor supplied that answer and when;
a later recorded actor may replace or retract it. History preserves every actor
and value. None of this establishes that an earlier actor recanted or changed
their belief. Actor is PROVENANCE ONLY -- the kernel enforces no permission.

The fact's question is defined WITHOUT its speaker:

    "The amount of interest reported on this identified Form 1099-INT that is
     allocated to this named other person."

The finding supplies the current answer with attested basis; the enclosing
assertion act supplies who stated it and when; a later tax rule -- not this
fact -- decides any nominee-interest consequence.

REPORT IDENTITY IS THE COMMITTED ONE, not an invented demo entity. The
allocation is keyed by payer + statement + tax-year + recipient, so it shares
the box-1 report's own identity components
(packages/tax/report_statement_identity.py, packages/content/tax/2025/
f1099int.bundle.json). The documentary report is contributed through the real
admission boundary, and the probe joins the allocation to the exact current
box-1 finding a later rule would consume.

Only synthetic demo.* / demo-* identities and values. No absolute paths.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT))

from packages.derivation.loader import DerivationSchemas  # noqa: E402
from packages.kernel import currency, facts, findings  # noqa: E402
from packages.kernel.findings import (  # noqa: E402
    _NO_CURRENT_VALUE,
    _current_value_for_fact,
    project,
)
from packages.tax.report_statement_identity import (  # noqa: E402
    PAYER_ENTITY_KIND,
    STATEMENT_ENTITY_KIND,
    build_1099int_report_entity_acts,
    contribute_1099int_report,
    derive_1099int_box1_fact_id,
    derive_reported_payer_entity_id,
    derive_reported_statement_entity_id,
)

SEP = "=" * 78

PAYER = "Demo Savings Bank"
STMT_A = "demo-stmt-a"
STMT_B = "demo-stmt-b"
YEAR = 2025
PRIOR_YEAR = 2024

MATT = "demo-user-matt"
ALEX = "demo-user-alex"

ALLOCATION_FACT_TYPE = "demo.nominee-allocation.amount"
RECIPIENT_KIND = "demo.person"

FAMILY_PREDECESSOR = "demo.cgd.t2.int-b1.h0"


def header(t: str) -> None:
    print("\n" + SEP + "\n" + t + "\n" + SEP)


def allocation_fact_id(*, payer_name: str, statement_reference: str,
                       tax_year: int, recipient_id: str) -> str:
    """Allocation identity SHARES the box-1 report's identity components.

    payer + statement + tax-year are derived by the committed document-side
    conventions, so the allocation is anchored to the same real report a later
    rule will read -- not to a parallel invented entity.
    """
    return facts.fact_id_for(
        ALLOCATION_FACT_TYPE,
        (
            ("payer", derive_reported_payer_entity_id(payer_name)),
            ("statement", derive_reported_statement_entity_id(
                payer_name=payer_name, statement_reference=statement_reference)),
            ("tax-year", str(tax_year)),
            ("recipient", recipient_id),
        ),
    )


def bundle() -> dict[str, Any]:
    return {
        "schema": "bundle.v1",
        "id": "demo.nominee-allocation-vocab",
        "label": "Demo nominee-allocation recording vocabulary",
        "fact_types": [
            {
                "schema": "fact-type.v1",
                "id": ALLOCATION_FACT_TYPE,
                # The question, stated WITHOUT its speaker.
                "title": (
                    "The amount of interest reported on this identified Form "
                    "1099-INT that is allocated to this named other person"
                ),
                "nature": "determinable",
                "identity_keys": [
                    {"name": "payer", "kind": "entity", "entity_kind": PAYER_ENTITY_KIND},
                    {"name": "statement", "kind": "entity",
                     "entity_kind": STATEMENT_ENTITY_KIND},
                    # the committed f1099int bundle keys tax-year as a literal
                    {"name": "tax-year", "kind": "literal",
                     "values": [str(PRIOR_YEAR), str(YEAR)]},
                    {"name": "recipient", "kind": "entity", "entity_kind": RECIPIENT_KIND},
                ],
                "value_schema": {"type": "number", "minimum": 0},
                # ADR-0073 Decision 3: 'locked' would refuse retraction outright.
                "supersession": {"policy": "free"},
            }
        ],
    }


def entity(eid: str, kind: str, label: str) -> dict[str, Any]:
    return {"schema": "entity.v1", "id": eid, "kind": kind, "label": label}


def finding(fid_: str, fact_id: str, value: Any) -> dict[str, Any]:
    return {
        "schema": "finding.v2",
        "id": fid_,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }


def main() -> int:
    schemas = DerivationSchemas()
    reg = schemas.registry
    results: dict[str, Any] = {}

    pat = "demo-recipient-pat"
    kim = "demo-recipient-kim"

    acts: list[dict[str, Any]] = []

    def add(kind: str, payload: dict[str, Any]) -> None:
        acts.append({"schema": "act.v1", "kind": kind, "payload": payload, "actor": MATT})

    # Adopt the COMMITTED Form 1099-INT bundle -- the real box-1 fact type,
    # not a demo stand-in -- alongside the allocation vocabulary.
    committed_1099int = json.loads(
        (REPO_ROOT / "packages/content/tax/2025/f1099int.bundle.json")
        .read_text(encoding="utf-8")
    )
    add("bundle-adoption", {"bundle": committed_1099int})
    add("bundle-adoption", {"bundle": bundle()})
    seen: set[str] = set()
    for stmt in (STMT_A, STMT_B):
        for e in build_1099int_report_entity_acts(
            payer_name=PAYER, statement_reference=stmt, act_index=0
        ):
            eid = e["payload"]["entity"]["id"]
            if eid in seen:
                continue
            seen.add(eid)
            acts.append({"schema": "act.v1", "kind": e["kind"],
                         "payload": e["payload"], "actor": MATT})
    for rid, label in ((pat, "Pat (allocation recipient)"),
                       (kim, "Kim (allocation recipient)")):
        add("entity-introduced", {"entity": entity(rid, RECIPIENT_KIND, label)})
    # box-1 reports are family-scoped (ADR-0017); the chain needs genesis first
    add("horizon-genesis", {
        "family": {"id": "tax.us.2025.f1099int.b1", "version": "v1"},
        "scope": {"tax-year": str(YEAR), "subject": "demo.primary"},
        "horizon_id": FAMILY_PREDECESSOR})
    add("evidence-submitted", {"evidence": {
        "schema": "evidence.v1", "id": "demo.evidence.report.alloc",
        "kind": "demo.report-1099int-copy",
        "label": "Synthetic Form 1099-INT copy",
        "content": {"mode": "document-report-entry", "synthetic": True}}})

    for i, a in enumerate(acts):
        a["committed_against"] = i
        a["act_id"] = f"demo.alloc.act.{i:03d}"
        a["at"] = f"2026-09-07T00:{i // 60:02d}:{i % 60:02d}Z"
    state = project(tuple(dict(a) for a in acts), reg)
    n = len(acts)

    header("Committed report identity -- contributed through the real boundary")
    admitted = contribute_1099int_report(
        state,
        payer_name=PAYER, statement_reference=STMT_A, tax_year=YEAR, amount=1200.0,
        scope={"tax-year": str(YEAR), "subject": "demo.primary"},
        family_predecessor_id=FAMILY_PREDECESSOR,
        family_successor_id="demo.alloc.int-b1.h1",
        registry=reg, record_id="demo.crec.report.a",
        act_index=n, contribution_id="demo.contribution.report.a",
        evidence_id="demo.evidence.report.alloc",
        finding_id="demo.finding.box1.a", committed_against=n,
    )
    if admitted.terminal_record.get("phase") != "completed":
        raise AssertionError(f"report not admitted: {admitted.terminal_record}")
    state = admitted.state
    n += 4

    box1_a = derive_1099int_box1_fact_id(
        payer_name=PAYER, statement_reference=STMT_A, tax_year=YEAR)
    print(f"  box-1 fact id (committed derivation):\n    {box1_a}")
    print(f"  admitted: {admitted.terminal_record.get('phase')}")

    pat_a = allocation_fact_id(payer_name=PAYER, statement_reference=STMT_A,
                               tax_year=YEAR, recipient_id=pat)
    kim_a = allocation_fact_id(payer_name=PAYER, statement_reference=STMT_A,
                               tax_year=YEAR, recipient_id=kim)
    pat_b = allocation_fact_id(payer_name=PAYER, statement_reference=STMT_B,
                               tax_year=YEAR, recipient_id=pat)
    pat_a_prior = allocation_fact_id(payer_name=PAYER, statement_reference=STMT_A,
                                     tax_year=PRIOR_YEAR, recipient_id=pat)

    idx = [n]

    def commit(kind: str, payload: dict[str, Any], actor: str) -> dict[str, Any]:
        nxt = idx[0]
        a = {"schema": "act.v1", "act_id": f"demo.alloc.act.{nxt:03d}", "kind": kind,
             "actor": actor, "at": f"2026-09-07T01:{nxt // 60:02d}:{nxt % 60:02d}Z",
             "committed_against": nxt, "payload": payload}
        nonlocal state
        state = findings.apply_act(state, a, reg)
        idx[0] = nxt + 1
        return a

    header("A2 / A3 -- record one recipient, then several")
    commit("assertion", {"finding": finding("demo-f-pat-1", pat_a, 300)}, MATT)
    a_kim = commit("assertion", {"finding": finding("demo-f-kim-1", kim_a, 150)}, MATT)
    view = currency.compute_currency(state)
    cur = set(view.current_finding_ids)
    results["A2"] = "demo-f-pat-1" in cur
    results["A3"] = {"demo-f-pat-1", "demo-f-kim-1"} <= cur and pat_a != kim_a
    print(f"  A2={results['A2']}  A3={results['A3']}")

    header("A5 -- two reports from the SAME payer stay distinct")
    print(f"  statement A: {pat_a}")
    print(f"  statement B: {pat_b}")
    results["A5"] = pat_a != pat_b
    print(f"  A5={results['A5']}")

    header("A5b -- same statement reference, DIFFERENT tax year, no collision")
    print(f"  {YEAR}:      {pat_a}")
    print(f"  {PRIOR_YEAR}: {pat_a_prior}")
    results["A5b"] = pat_a != pat_a_prior
    print(f"  A5b={results['A5b']}")

    header("A4 -- a workspace actor changes the amount allocated to Pat")
    kim_before = dict(state.findings["demo-f-kim-1"])
    corr = commit("assertion", {"finding": finding("demo-f-pat-2", pat_a, 250)}, MATT)
    kim_after = dict(state.findings["demo-f-kim-1"])
    view = currency.compute_currency(state)
    results["A4"] = (kim_before == kim_after
                     and "demo-f-kim-1" in view.current_finding_ids)
    print(f"  Matt changes the allocation to Pat from 300 to 250 (act {corr['act_id']})")
    print(f"  the current allocation to Kim is the identical finding: "
          f"{kim_before == kim_after}")
    print(f"  still supported by its same original assertion act {a_kim['act_id']}, "
          f"actor {a_kim['actor']}: {'demo-f-kim-1' in view.current_finding_ids}")
    print(f"  A4={results['A4']}")

    header("A4b -- CROSS-ACTOR correction (shared-workspace revision)")
    alex_corr = commit("assertion", {"finding": finding("demo-f-pat-alex", pat_a, 275)},
                       ALEX)
    view = currency.compute_currency(state)
    current_pat = [f for f in view.current_finding_ids
                   if state.findings[f]["fact_id"] == pat_a]
    results["A4b"] = (current_pat == ["demo-f-pat-alex"]
                      and "demo-f-pat-2" in state.findings
                      and corr["actor"] != alex_corr["actor"])
    print(f"  Matt supplied 250 (act {corr['act_id']}, actor {corr['actor']}, "
          f"at {corr['at']})")
    print(f"  Alex supplied 275 at the SAME fact identity (act {alex_corr['act_id']}, "
          f"actor {alex_corr['actor']}, at {alex_corr['at']})")
    print(f"  current: {current_pat} = {state.findings['demo-f-pat-alex']['value']}")
    print(f"  Matt's finding is historical and still present: "
          f"{'demo-f-pat-2' in state.findings}")
    print("  -> shared-workspace revision. NOT evidence that Alex speaks for Matt.")
    print("     The kernel enforces no permission; actor is provenance only.")
    print(f"  A4b={results['A4b']}")

    header("A7 -- correcting the box-1 amount does not detach the allocation")
    box1_before = _current_value_for_fact(state, box1_a)
    # SC-R2: the fact is already a family member, so a same-member correction
    # belongs on the ordinary assertion path, not another member-transition.
    box1_corr = commit("assertion",
                       {"finding": finding("demo.finding.box1.a2", box1_a, 1300.0)},
                       MATT)
    box1_after = _current_value_for_fact(state, box1_a)
    view = currency.compute_currency(state)
    still = [f for f in view.current_finding_ids
             if state.findings[f]["fact_id"] == pat_a]
    same_id = derive_1099int_box1_fact_id(
        payer_name=PAYER, statement_reference=STMT_A, tax_year=YEAR) == box1_a
    results["A7"] = bool(still) and box1_before != box1_after and same_id
    print(f"  box-1 corrected {box1_before} -> {box1_after} at the SAME fact id "
          f"(act {box1_corr['act_id']})")
    print(f"  the report fact id is unchanged: {same_id}")
    print(f"  allocation still current: {still}")
    print(f"  A7={results['A7']}")

    header("Join -- allocation to the exact current box-1 finding a rule consumes")
    view = currency.compute_currency(state)
    current_box1 = [f for f in view.current_finding_ids
                    if state.findings[f]["fact_id"] == box1_a]
    shares = (f"payer={derive_reported_payer_entity_id(PAYER)}" in pat_a
              and f"tax-year={YEAR}" in pat_a)
    results["join"] = bool(current_box1) and shares
    print(f"  current box-1 finding(s) for {box1_a}:\n    {current_box1}")
    print(f"  allocation identity shares payer/statement/tax-year: {shares}")
    print(f"  join={results['join']}")

    header("A6 -- Alex removes from current use the allocation Matt supplied")
    r_act = commit("finding-retracted", {"finding_id": "demo-f-pat-alex"}, ALEX)
    r2 = commit("finding-retracted", {"finding_id": "demo-f-kim-1"}, ALEX)
    view = currency.compute_currency(state)
    pat_current = [f for f in view.current_finding_ids
                   if state.findings[f]["fact_id"] == pat_a]
    hist = {"demo-f-pat-1", "demo-f-pat-2"} <= set(state.findings)
    results["A6"] = (not pat_current and hist
                     and sorted(r_act["payload"]) == ["finding_id"])
    print(f"  retraction payload fields: {sorted(r_act['payload'])}")
    print(f"  Kim's allocation was supplied by {a_kim['actor']} at {a_kim['at']}")
    print(f"  removed from current use by {r2['actor']} at {r2['at']} "
          f"(act {r2['act_id']})")
    print(f"  the different actor's retraction was ADMITTED: "
          f"{'demo-f-kim-1' not in view.current_finding_ids}")
    print(f"  Matt's earlier findings remain historical: {hist}")
    print("  -> nothing here says Matt recanted. Admission never consults actor")
    print("     identity; this is provenance, not enforcement.")
    print(f"  A6={results['A6']}")

    header("T0-G1 -- both current-standing readers agree")
    enforce_val = _current_value_for_fact(state, pat_a)
    results["G1_agrees"] = enforce_val is _NO_CURRENT_VALUE and not pat_current
    print(f"  _current_value_for_fact = "
          f"{'<NO_CURRENT_VALUE>' if enforce_val is _NO_CURRENT_VALUE else enforce_val}")
    print(f"  read-model currency current: {bool(pat_current)}")
    print(f"  agree={results['G1_agrees']}")

    header("A11 -- assert again at the SAME fact identity")
    try:
        again = commit("assertion", {"finding": finding("demo-f-pat-3", pat_a, 275)},
                       MATT)
        view = currency.compute_currency(state)
        now = [f for f in view.current_finding_ids
               if state.findings[f]["fact_id"] == pat_a]
        results["A11"] = now == ["demo-f-pat-3"]
        print(f"  re-asserted at the SAME fact id: {pat_a}")
        print(f"  current: {now} = {state.findings['demo-f-pat-3']['value']} "
              f"(act {again['act_id']}, actor {again['actor']})")
    except Exception as exc:  # noqa: BLE001
        results["A11"] = False
        print(f"  REFUSED: {exc}")

    header("Revival by id reuse must still be refused")
    try:
        commit("assertion", {"finding": finding("demo-f-pat-2", pat_a, 250)}, MATT)
        results["id_reuse_refused"] = False
        print("  ADMITTED -- unexpected")
    except Exception as exc:  # noqa: BLE001
        results["id_reuse_refused"] = True
        print(f"  refused: {exc}")

    header("RESULT SUMMARY")
    for k in ("A2", "A3", "A4", "A4b", "A5", "A5b", "A6", "A7", "A11",
              "join", "G1_agrees", "id_reuse_refused"):
        print(f"  {k:18} {results.get(k)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
