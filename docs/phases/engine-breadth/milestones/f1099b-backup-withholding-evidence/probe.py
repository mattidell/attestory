"""P0 probes for Form 1099-B backup withholding on core v82.

Evidence for docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md.
Charter: docs/reviews/f1099b-backup-withholding/charter-p0.md (Scope 3).
Runs every case in 'Cases that will shape the design' through live_coordinate_run
on core v82, compares lines 25b, 33, 34 and 37 against hand values from the
2025 Form 1040 and Form 1099-B instructions, and writes probe-output-v82.json.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import math
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

# Load audit harness under a unique module name
HARNESS_MODULE = "f1099b_b4_audit_harness"
harness_path = REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py"
spec = importlib.util.spec_from_file_location(HARNESS_MODULE, harness_path)
assert spec is not None and spec.loader is not None
h = importlib.util.module_from_spec(spec)
sys.modules[HARNESS_MODULE] = h
spec.loader.exec_module(h)

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from tests.test_form_1099_withholding import (  # noqa: E402
    DIV_1A_FAMILY,
    DIV_B4_FAMILY,
    INT_B1_FAMILY,
    INT_B4_FAMILY,
    _close,
    _head,
    _introduce,
    _transition,
)

P = "tax.us.2025."
YEAR = "2025"
V82 = h.Core("v82", "v80", "v80")

BOX4_REPORTED_FACT = P + "f1099b.statement-box4-withholding-reported"
BOX7_REPORTED_FACT = P + "f1099b.statement-box7-loss-not-allowed"


# ---- Hand value calculation --------------------------------------------------------


def _bracket(x: float) -> float:
    tax = 0.10 * min(x, 11925)
    if x > 11925:
        tax += 0.12 * (min(x, 48475) - 11925)
    if x > 48475:
        tax += 0.22 * (min(x, 103350) - 48475)
    return tax


def tax_table(ti: float) -> int:
    """2025 Tax Table for single filer."""
    if ti <= 0:
        return 0
    mid = math.floor(ti / 50) * 50 + 25 if ti >= 3000 else math.floor(ti / 25) * 25 + 12.5
    return int(math.floor(_bracket(mid) + 0.5))


def qdcg(ti: float, pref: float) -> int:
    if pref <= 0:
        return tax_table(ti)
    ordinary = ti - pref
    zero_band = max(0.0, min(ti, 48350) - ordinary)
    fifteen = max(0.0, pref - zero_band)
    return min(tax_table(ti), int(math.floor(tax_table(ordinary) + 0.15 * fifteen + 0.5)))


def hand_values(
    *,
    wages: float = 50000,
    w2_withholding: float = 4500,
    st_gain: float = 0,
    lt_gain: float = 0,
    interest: float = 0,
    dividends: float = 0,
    b25: float | None = 0,
    blocked: bool = False,
) -> dict[str, Any]:
    if blocked or b25 is None:
        return {
            "disposition": "blocked",
            "form1040.line-25b": None,
            "form1040.line-33": None,
            "form1040.line-34": None,
            "form1040.line-37": None,
        }
    capital_gain = st_gain + lt_gain
    agi = wages + capital_gain + interest + dividends
    std_ded = 15750
    ti = max(0.0, agi - std_ded)
    pref = max(0.0, lt_gain) if capital_gain > 0 else 0.0
    tax = qdcg(ti, pref)
    total_payments = w2_withholding + b25
    refund = max(0, total_payments - tax)
    owed = max(0, tax - total_payments)
    return {
        "disposition": "published",
        "taxable_income": int(ti),
        "tax": int(tax),
        "form1040.line-25b": int(b25),
        "form1040.line-33": int(total_payments),
        "form1040.line-34": int(refund),
        "form1040.line-37": int(owed),
    }


# ---- Act building helpers ----------------------------------------------------------


def say_statement_answer(acts: list[dict[str, Any]], core: Any, fact_type: str, statement: str, value: str) -> list[dict[str, Any]]:
    fact_id = h.fact_id_for(fact_type, (("statement", statement), ("tax-year", YEAR)))
    kept = []
    for act in acts:
        finding = (act.get("payload") or {}).get("finding") if isinstance(act.get("payload"), dict) else None
        if isinstance(finding, dict) and finding.get("fact_id") == fact_id:
            continue
        kept.append(act)
    acts = kept
    body = h.bundle_for(fact_type, core.content)
    assert body is not None, fact_type
    if not {f["id"] for f in body["fact_types"]} & h._adopted(acts):
        h._add(acts, "bundle-adoption", {"bundle": body})
    h._add(acts, "assertion", {"finding": h._attested(f"demo.b4.probe.{fact_type.split('.')[-1]}.{statement}", fact_id, value)})
    return h.renumber(acts)


def add_interest_and_dividends(
    acts: list[dict[str, Any]],
    int_box1: float,
    int_box4: float | None,
    div_box1a: float,
    div_box4: float | None,
) -> list[dict[str, Any]]:
    # Interest
    b1_head = _head(acts, INT_B1_FAMILY)
    b4_head = _head(acts, INT_B4_FAMILY)
    payer_int, stmt_int = "demo.b4.int.payer", "demo.b4.int.stmt"
    keys_int = (("payer", payer_int), ("statement", stmt_int))
    _introduce(acts, payer_int, "tax.us.interest-payer")
    _introduce(acts, stmt_int, "tax.us.1099int-statement")
    b1_head = _transition(
        acts, (INT_B1_FAMILY, "v1"), b1_head, "demo.b4.int.b1.h1", "demo.b4.int.box1",
        "tax.us.2025.f1099int.box1-interest", keys_int, int_box1,
    )
    if int_box4 is not None:
        b4_head = _transition(
            acts, (INT_B4_FAMILY, "v1"), b4_head, "demo.b4.int.b4.h1", "demo.b4.int.box4",
            "tax.us.2025.f1099int.box4-withholding", keys_int, int_box4,
        )
    _close(acts, "tax.us.2025.f1099int.b1.source-closure", b1_head, "demo.b4.int.closure.box1")
    _close(acts, "tax.us.2025.f1099int.b4.source-closure", b4_head, "demo.b4.int.closure.box4")

    # Dividends
    a_head = _head(acts, DIV_1A_FAMILY)
    div_b4_head = _head(acts, DIV_B4_FAMILY)
    payer_div, stmt_div = "demo.b4.div.payer", "demo.b4.div.stmt"
    keys_div = (("payer", payer_div), ("statement", stmt_div))
    _introduce(acts, payer_div, "tax.us.dividend-payer")
    _introduce(acts, stmt_div, "tax.us.1099div-statement")
    a_head = _transition(
        acts, (DIV_1A_FAMILY, "v1"), a_head, "demo.b4.div.1a.h1", "demo.b4.div.box1a",
        "tax.us.2025.f1099div.box1a-ordinary", keys_div, div_box1a,
    )
    if div_box4 is not None:
        div_b4_head = _transition(
            acts, (DIV_B4_FAMILY, "v1"), div_b4_head, "demo.b4.div.b4.h1", "demo.b4.div.box4",
            "tax.us.2025.f1099div.box4-withholding", keys_div, div_box4,
        )
    _close(acts, "tax.us.2025.f1099div.1a.source-closure", a_head, "demo.b4.div.closure.box1a")
    _close(acts, "tax.us.2025.f1099div.b4.source-closure", div_b4_head, "demo.b4.div.closure.box4")

    # Update line 2a / 3a answers if present in base
    return h.renumber(acts)


# ---- Running through coordinator ---------------------------------------------------


def run_case(core: Any, acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    surface = core.surface()
    finished = h._handover(
        h._finish(
            copy.deepcopy(acts),
            package_path=core.package_path,
            package_version=core.version,
            release_path=core.release_path,
            release_version=core.release_version,
            note=run_id,
        ),
        surface=surface,
        reconfirm=True,
    )
    with tempfile.TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=REPO,
            authoritative_acts=finished,
            workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=h.ccr.USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            return {
                "outcome": "refusal",
                "refusal": outcome.refusal,
                "exit_code": outcome.exit_code,
            }
        assert outcome.presentation_path is not None
        model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))

        lines: dict[str, Any] = {}
        dispositions: dict[str, str] = {}
        blocked_reasons: dict[str, list[str]] = {}

        for section in model.get("sections") or []:
            field = section.get("field") or {}
            fid = str(field.get("id") or "").removeprefix(P)
            resolved = section.get("resolved") or {}
            disp = resolved.get("disposition")
            dispositions[fid] = disp
            if disp in ("published", "published_value", "computed_zero"):
                lines[fid] = resolved.get("value")
            elif disp == "blocked":
                lines[fid] = None
                blocked_reasons[fid] = [
                    str(r.get("sentence") or "") for r in resolved.get("reasons") or []
                    if isinstance(r, dict)
                ]

        return {
            "outcome": "success",
            "dispositions": dispositions,
            "lines": lines,
            "blocked_reasons": blocked_reasons,
        }


# ---- The 9 Cases -------------------------------------------------------------------


def build_cases() -> dict[str, dict[str, Any]]:
    cases: dict[str, dict[str, Any]] = {}

    # Case 1: b4_one_statement
    # 1 statement, covered short-term sale, box 4 answered "yes" (withholding $240)
    acts1 = h.opened()
    acts1 = h.sale(acts1, "covered", "st", proceeds=5000, basis=4000, tag="b4_one")
    acts1 = h.answer(acts1, **h.honest({"covered"}, loss=False))
    stmt1 = "demo.sfa.b4_one.statement"
    acts1 = say_statement_answer(acts1, V82, BOX4_REPORTED_FACT, stmt1, "yes")
    acts1 = say_statement_answer(acts1, V82, BOX7_REPORTED_FACT, stmt1, "no")
    cases["b4_one_statement"] = {
        "description": "One statement with covered ST sale ($1,000 gain), box 4 withholding reported yes ($240)",
        "acts": acts1,
        "hand": hand_values(st_gain=1000, b25=240),
        "v82_expected_disposition": "blocked",
    }

    # Case 2: b4_two_statements
    # 2 statements, each with a sale, both with box 4 reported "yes" ($240 + $100 = $340)
    acts2 = h.opened()
    acts2 = h.sale(acts2, "covered", "st", proceeds=5000, basis=4000, tag="b4_s1")
    acts2 = h.sale(acts2, "covered", "st", proceeds=2000, basis=1500, tag="b4_s2")
    acts2 = h.answer(acts2, **h.honest({"covered"}, loss=False))
    stmt2_1 = "demo.sfa.b4_s1.statement"
    stmt2_2 = "demo.sfa.b4_s2.statement"
    acts2 = say_statement_answer(acts2, V82, BOX4_REPORTED_FACT, stmt2_1, "yes")
    acts2 = say_statement_answer(acts2, V82, BOX7_REPORTED_FACT, stmt2_1, "no")
    acts2 = say_statement_answer(acts2, V82, BOX4_REPORTED_FACT, stmt2_2, "yes")
    acts2 = say_statement_answer(acts2, V82, BOX7_REPORTED_FACT, stmt2_2, "no")
    cases["b4_two_statements"] = {
        "description": "Two statements with covered ST sales ($1,500 total gain), both box 4 yes ($240 + $100 = $340)",
        "acts": acts2,
        "hand": hand_values(st_gain=1500, b25=340),
        "v82_expected_disposition": "blocked",
    }

    # Case 3: b4_st_and_lt
    # 1 statement with both short-term and long-term sales, box 4 reported "yes" ($300)
    acts3 = h.opened()
    acts3 = h.sale(acts3, "covered", "st", proceeds=5000, basis=4000, tag="b4_both")
    # Add long-term sale on same statement entity
    acts3 = h.sale(acts3, "covered", "lt", proceeds=3000, basis=2000, tag="b4_both_lt")
    # Move lt sale transaction to use same statement entity demo.sfa.b4_both.statement, removing redundant entity intro
    filtered_acts3 = [
        a for a in acts3
        if not (a.get("kind") == "entity-introduced" and (a.get("payload") or {}).get("entity", {}).get("id") == "demo.sfa.b4_both_lt.statement")
    ]
    text3 = json.dumps(filtered_acts3).replace("demo.sfa.b4_both_lt.statement", "demo.sfa.b4_both.statement")
    acts3 = h.renumber(json.loads(text3))
    acts3 = h.answer(acts3, **h.honest({"covered"}, loss=False))
    stmt3 = "demo.sfa.b4_both.statement"
    acts3 = say_statement_answer(acts3, V82, BOX4_REPORTED_FACT, stmt3, "yes")
    acts3 = say_statement_answer(acts3, V82, BOX7_REPORTED_FACT, stmt3, "no")
    cases["b4_st_and_lt"] = {
        "description": "One statement with both ST ($1,000) and LT ($1,000) sales, box 4 yes ($300)",
        "acts": acts3,
        "hand": hand_values(st_gain=1000, lt_gain=1000, b25=300),
        "v82_expected_disposition": "blocked",
    }

    # Case 4: b4_amount_no_answer
    # 1 statement with a sale, box 4 question unanswered (missing answer)
    acts4 = h.opened()
    acts4 = h.sale(acts4, "covered", "st", proceeds=5000, basis=4000, tag="b4_noans")
    acts4 = h.answer(acts4, **h.honest({"covered"}, loss=False))
    stmt4 = "demo.sfa.b4_noans.statement"
    # Only answer box 7, leave box 4 unanswered
    acts4 = say_statement_answer(acts4, V82, BOX7_REPORTED_FACT, stmt4, "no")
    cases["b4_amount_no_answer"] = {
        "description": "One statement with covered ST sale, box 4 unanswered (pairing unmet)",
        "acts": acts4,
        "hand": hand_values(st_gain=1000, b25=None, blocked=True),
        "v82_expected_disposition": "blocked",
    }

    # Case 5: b4_answer_no_amount
    # 1 statement with a sale, box 4 answered "no", no amount
    acts5 = h.opened()
    acts5 = h.sale(acts5, "covered", "st", proceeds=5000, basis=4000, tag="b4_noamt")
    acts5 = h.answer(acts5, **h.honest({"covered"}, loss=False))
    stmt5 = "demo.sfa.b4_noamt.statement"
    acts5 = say_statement_answer(acts5, V82, BOX4_REPORTED_FACT, stmt5, "no")
    acts5 = say_statement_answer(acts5, V82, BOX7_REPORTED_FACT, stmt5, "no")
    cases["b4_answer_no_amount"] = {
        "description": "One statement with covered ST sale, box 4 answered no, zero withholding",
        "acts": acts5,
        "hand": hand_values(st_gain=1000, b25=0),
        "v82_expected_disposition": "published",
    }

    # Case 6: b4_no_with_amount
    # On v82, no amount fact exists for 1099-B box 4. Answered "no".
    acts6 = h.opened()
    acts6 = h.sale(acts6, "covered", "st", proceeds=5000, basis=4000, tag="b4_nowith")
    acts6 = h.answer(acts6, **h.honest({"covered"}, loss=False))
    stmt6 = "demo.sfa.b4_nowith.statement"
    acts6 = say_statement_answer(acts6, V82, BOX4_REPORTED_FACT, stmt6, "no")
    acts6 = say_statement_answer(acts6, V82, BOX7_REPORTED_FACT, stmt6, "no")
    cases["b4_no_with_amount"] = {
        "description": "One statement with covered ST sale, box 4 answered no on v82 (zero withholding)",
        "acts": acts6,
        "hand": hand_values(st_gain=1000, b25=0),
        "v82_expected_disposition": "published",
    }

    # Case 7: b4_statement_removed
    # Statement sales removed / none present, but box 4 answer left behind (surplus statement answer)
    acts7 = h.opened()
    acts7 = h.answer(acts7, **h.honest(set(), loss=False))
    stmt7 = "demo.sfa.b4_orphan.statement"
    h._introduce(acts7, stmt7, "tax.us.f1099b-statement")
    acts7 = say_statement_answer(acts7, V82, BOX4_REPORTED_FACT, stmt7, "yes")
    acts7 = say_statement_answer(acts7, V82, BOX7_REPORTED_FACT, stmt7, "no")
    cases["b4_statement_removed"] = {
        "description": "A statement's sales removed, leaving orphan box 4 answer behind; sale counts 0",
        "acts": acts7,
        "hand": hand_values(st_gain=0, b25=0),
        "v82_expected_disposition": "published",
    }

    # Case 8: b4_beside_int_div
    # 1 1099-B statement with covered ST sale (gain $1,000, box 4 yes),
    # beside 1099-INT ($100 int, $50 b4) and 1099-DIV ($200 div, $75 b4).
    acts8 = h.opened()
    acts8 = h.sale(acts8, "covered", "st", proceeds=5000, basis=4000, tag="b4_beside")
    acts8 = h.answer(acts8, **h.honest({"covered"}, loss=False))
    stmt8 = "demo.sfa.b4_beside.statement"
    acts8 = say_statement_answer(acts8, V82, BOX4_REPORTED_FACT, stmt8, "yes")
    acts8 = say_statement_answer(acts8, V82, BOX7_REPORTED_FACT, stmt8, "no")
    acts8 = add_interest_and_dividends(acts8, int_box1=100, int_box4=50, div_box1a=200, div_box4=75)
    cases["b4_beside_int_div"] = {
        "description": "1099-B sale (box 4 yes, $200) beside 1099-INT ($50 b4) and 1099-DIV ($75 b4); total b4 $325",
        "acts": acts8,
        "hand": hand_values(st_gain=1000, interest=100, dividends=200, b25=325),
        "v82_expected_disposition": "blocked",
    }

    # Case 9: b4_no_one_statement
    # Standard single statement covered sale, box 4 answered "no".
    acts9 = h.opened()
    acts9 = h.sale(acts9, "covered", "st", proceeds=5000, basis=4000, tag="b4_std_no")
    acts9 = h.answer(acts9, **h.honest({"covered"}, loss=False))
    stmt9 = "demo.sfa.b4_std_no.statement"
    acts9 = say_statement_answer(acts9, V82, BOX4_REPORTED_FACT, stmt9, "no")
    acts9 = say_statement_answer(acts9, V82, BOX7_REPORTED_FACT, stmt9, "no")
    cases["b4_no_one_statement"] = {
        "description": "Standard one-statement covered ST sale ($1,000 gain), box 4 answered no",
        "acts": acts9,
        "hand": hand_values(st_gain=1000, b25=0),
        "v82_expected_disposition": "published",
    }

    return cases


def main() -> None:
    cases = build_cases()
    results: dict[str, Any] = {}

    print(f"Running {len(cases)} probe cases on core v82...")
    for name, c in cases.items():
        print(f"  -> {name}...", end="", flush=True)
        res = run_case(V82, c["acts"], f"demo.b4.probe.v82.{name}")
        disps = res.get("dispositions", {})
        l25b_disp = disps.get("form1040.line-25b")
        lines = res.get("lines", {})
        blocked_reasons = res.get("blocked_reasons", {})

        watched = {
            "form1040.line-25b": lines.get("form1040.line-25b"),
            "form1040.line-33": lines.get("form1040.line-33"),
            "form1040.line-34": lines.get("form1040.line-34"),
            "form1040.line-37": lines.get("form1040.line-37"),
        }

        entry = {
            "name": name,
            "description": c["description"],
            "core": "v82",
            "v82_actual_disposition": l25b_disp,
            "v82_expected_disposition": c["v82_expected_disposition"],
            "v82_lines": watched,
            "hand_values": c["hand"],
            "blocked_reasons": blocked_reasons.get("form1040.line-25b", []),
            "all_blocked_reasons": {
                k: v for k, v in blocked_reasons.items()
                if k in ("form1040.line-25b", "form1040.line-33", "form1040.line-34", "form1040.line-37")
            },
        }
        results[name] = entry
        print(f" {l25b_disp} (25b={watched['form1040.line-25b']}, 33={watched['form1040.line-33']}, 34={watched['form1040.line-34']})")

    out_file = HERE / "probe-output-v82.json"
    out_file.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"\nWrote {out_file.name}")


if __name__ == "__main__":
    main()
