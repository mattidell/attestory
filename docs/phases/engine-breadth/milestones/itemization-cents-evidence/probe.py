"""P0 probe (itemization-cents): on the real coordinator (live_coordinate_run, core v65),
record two members of 100.40 in each family an attachment itemizes and read whether the
attachment publishes or blocks, with the subtotal and the row sum. Whole-dollar control
(100 + 100) alongside. Synthetic demo.* data only. Run from the repo root:

    python3 docs/phases/engine-breadth/milestones/itemization-cents-evidence/probe.py

Reads the committed tests' helpers; changes nothing.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from tests import test_collect_closure as cc  # noqa: E402
from tests import test_w2g_gambling as w2g  # noqa: E402
from tests.test_withholding_closure import _strip_closure  # noqa: E402
from tests.test_attachment_closure import _boundary_form8949  # noqa: E402

P = "tax.us.2025."
# Per-family base amount (x2 members; cents case adds .40): the Schedule B threshold is $1,500
# and Schedule A needs itemized deductions over the standard deduction to publish.
BASE = {"f1099int.b1": 800.0, "f1099div.1a": 800.0, "f1098": 10000.0}
# family -> (attachment rule suffix, attachment publication symbol, subtotal symbol, trigger family or None, trigger amount, companion or None)
CASES: dict[str, tuple[str, str, str, str | None, float, str | None]] = {
    "f1099g.1": ("schedule-1", "schedule1.disposition", "unemployment.box1-subtotal", None, 0.0, None),
    "w2g.b1": ("schedule-1", "schedule1.disposition", "gambling.b1-winnings-subtotal", None, 0.0, None),
    "f1098e.1": ("schedule-1", "schedule1.disposition", "sli-worksheet.line1-total-interest-paid-subtotal", "f1099g.1", 1000.0, "f1098e.box2-checked-authority"),
    "f1099int.b1": ("schedule-b", "scheduleb.disposition", "interest.b1-subtotal", None, 0.0, None),  # scale 800
    "f1099int.b3": ("schedule-b", "scheduleb.disposition", "interest.b3-subtotal", "f1099int.b1", 2000.0, None),
    "f1099oid.b1": ("schedule-b", "scheduleb.disposition", "interest.oid-subtotal", "f1099int.b1", 2000.0, None),
    "non-form-interest": ("schedule-b", "scheduleb.disposition", "interest.non-form-subtotal", "f1099int.b1", 2000.0, None),
    "form1065-k1.box5": ("schedule-b", "scheduleb.disposition", "interest.form1065-k1-box5-subtotal", "f1099int.b1", 2000.0, None),
    "f1099int.b10": ("schedule-b", "scheduleb.disposition", "interest.b10-market-discount-subtotal", "f1099int.b1", 2000.0, None),
    "f1099oid.b5": ("schedule-b", "scheduleb.disposition", "interest.oid-b5-market-discount-subtotal", "f1099int.b1", 2000.0, None),
    "scheduleb.adjustment.nominee": ("schedule-b", "scheduleb.disposition", "interest.scheduleb-nominee-subtotal", "f1099int.b1", 2000.0, None),
    "scheduleb.adjustment.abp-adjustment": ("schedule-b", "scheduleb.disposition", "interest.scheduleb-abp-adjustment-subtotal", "f1099int.b1", 2000.0, None),
    "f1099div.1a": ("schedule-b", "scheduleb.disposition", "dividends.1a-subtotal", None, 0.0, None),
    "f1099div.2a": ("schedule-d", "schedule-d.disposition", "dividends.2a-subtotal", "f1099b.covered-st-proceeds", 1000.0, None),
    "f1099b.covered-st-proceeds": ("schedule-d", "schedule-d.disposition", "f1099b.covered-st-proceeds-subtotal", None, 0.0, None),
    "f1099b.covered-w-st-proceeds": ("f8949", "form8949.disposition", "f1099b.covered-w-st-proceeds-subtotal", None, 0.0, None),
    "f1098": ("schedule-a", "scheduleA.disposition", "schedule-a.line8a", None, 0.0, None),
    "f1099k": ("schedule-1", "schedule1.disposition", "f1099k.box1a-subtotal", "f1099g.1", 1000.0, None),
}


def run_acts(acts: list[dict[str, object]], run_id: str) -> Any:
    for _ in range(5):
        try:
            return w2g._run(acts, run_id)
        except Exception as exc:  # a member contradicting a base "none" declaration
            m = re.search(r"contradiction: (\S+) is currently", str(exc))
            if not m:
                raise
            acts = _strip_closure(acts, m.group(1))
    raise AssertionError("too many declaration removals")


def acts_for(family: str, amounts: list[float], tag: str) -> list[dict[str, object]]:
    _, _, _, trigger, tamount, companion = CASES[family]
    if family == "w2g.b1":
        return w2g._w2g_return([(a, None) for a in amounts])
    acts = w2g._w2g_return([])
    if family.startswith("f1099b.covered-w-"):
        _boundary_form8949(acts)
    if trigger is not None:
        acts = cc._add_member(acts, P + trigger, tamount, close=True, tag="t" + trigger.replace(".", "-"))
    for i, amount in enumerate(amounts):
        last = i == len(amounts) - 1
        if companion is not None:
            from tests.test_attachment_closure import _add_member_with_companion
            acts = _add_member_with_companion(acts, P + family, amount, tag=f"{tag}{i}", companion=P + companion)
        else:
            acts = cc._add_member(acts, P + family, amount, close=last, tag=f"{tag}{i}")
    return acts


def summarize(run: Any, family: str) -> dict[str, Any]:
    rule, sym, subtotal, *_ = CASES[family]
    out: dict[str, Any] = {"attachment": rule}
    row = next((r for r in run.blocked if str(r.get("artifact_id", "")).endswith("rule.attachment." + rule)), None)
    if P + sym in run.pubs:
        out["attachment_outcome"] = "published"
        value = run.pubs[P + sym]["value"]
        for part in value.get("itemizations", []):
            for rs in part["row_sets"]:
                if rs["subtotal"]["symbol"] == P + subtotal:
                    out.update(part=part["part_id"], row_sum=rs["row_sum"], subtotal=rs["subtotal"]["value"])
    elif row is not None:
        out["attachment_outcome"] = "blocked"
        out["code"] = row.get("code")
        out["missing"] = [m.replace(P, "") for m in row.get("missing", [])]
    else:
        out["attachment_outcome"] = "not published, no blocked row (held or inapplicable)"
    if P + subtotal in run.pubs:
        out["subtotal_symbol_value"] = str(run.pubs[P + subtotal]["value"])
    else:
        out["subtotal_symbol_value"] = None
    return out


# Cases where rounding each subtotal first differs from rounding only the total: each is
# (members as (family, amount)), read on core v65. Line 2a (1099-DIV box 12 + 1099-INT box 8) is
# paper-only: a box 12 member needs a companion fact this harness does not record. Hand v65 / v66 values are in the design doc.
DOLLAR_CASES: dict[str, list[tuple[str, float]]] = {
    "d1_line2b_two_interest_families_up": [("f1099int.b1", 100.40), ("f1099int.b3", 100.40)],
    "d2_line2b_two_interest_families_half": [("f1099int.b1", 100.50), ("f1099int.b3", 100.50)],
    "d3_line2b_less_nominee_adjustment": [("f1099int.b1", 300.60), ("scheduleb.adjustment.nominee", 100.40)],
    "d4_line25b_interest_and_dividend_withholding": [("f1099int.b4", 100.40), ("f1099div.b4", 100.40)],
}
WATCH = ("interest.taxable-total", "tax-exempt-interest.line2a-total", "payments.line25b", "payments.line25d",
         "income.agi", "tax.line24-total-tax", "payments.line35a-refunded", "payments.line37-amount-owed")


def dollar_cases() -> dict[str, Any]:
    out: dict[str, Any] = {}
    for name, members in DOLLAR_CASES.items():
        try:
            acts = w2g._w2g_return([])
            for i, (family, amount) in enumerate(members):
                acts = cc._add_member(acts, P + family, amount, close=True, tag=f"dc{name[:2]}{i}")
            run = run_acts(acts, f"demo.ic.{name[:2]}")
            out[name] = {"members": members, "v65": {s: (str(run.pubs[P + s]["value"]) if P + s in run.pubs else None) for s in WATCH},
                         "blocked": sorted(str(r.get("artifact_id")).replace(P, "") for r in run.blocked)}
        except Exception as exc:
            out[name] = {"members": members, "error": f"{type(exc).__name__}: {str(exc)[:300]}"}
        print(name, json.dumps(out[name]), file=sys.stderr, flush=True)
    return out


def main() -> None:
    results: dict[str, Any] = {}
    if sys.argv[1:] == ["cases"]:
        print(json.dumps({"dollar_cases": dollar_cases()}, indent=1, sort_keys=True))
        return
    only = sys.argv[1:] or sorted(CASES)
    for family in only:
        tag = family.replace(".", "-")
        entry: dict[str, Any] = {}
        base = BASE.get(family, 100.0)
        for label, amounts in ((f"cents_{base + 0.40:g}_x2", [base + 0.40] * 2), (f"whole_{base:g}_x2", [base] * 2)):
            try:
                entry[label] = summarize(run_acts(acts_for(family, amounts, tag + label[:2]), f"demo.ic.{tag}.{label[:3]}"), family)
            except Exception as exc:  # recorded, not hidden
                entry[label] = {"error": f"{type(exc).__name__}: {str(exc)[:300]}"}
        results[family] = entry
        print(family, json.dumps(entry), file=sys.stderr, flush=True)
    print(json.dumps({"tie_out": results, "dollar_cases": dollar_cases() if not sys.argv[1:] else None}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
