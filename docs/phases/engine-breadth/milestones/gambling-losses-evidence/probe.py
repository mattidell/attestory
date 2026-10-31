"""P0 probe (gambling-losses): on the real coordinator (live_coordinate_run, core v66),
record a Form W-2G and the Schedule A gambling answer "no" (the filer has losses) and read
what refuses each return: the standard-deduction filer, and a filer who would itemize by
either route (a Form 1098 mortgage statement, or the raw itemized-deductions assertion).
Controls: the same returns with the answer "yes", and a return with no W-2G.
Synthetic demo.* data only. Run from the repo root:

    python3 docs/phases/engine-breadth/milestones/gambling-losses-evidence/probe.py

Reads the committed tests' helpers; changes nothing.
"""
from __future__ import annotations

import copy
import json
import re
import sys
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.kernel.findings import FindingModelError  # noqa: E402
from tests import test_collect_closure as cc  # noqa: E402
from tests import test_w2g_gambling as w2g  # noqa: E402
from tests.helpers import current_core_returns as ccr  # noqa: E402
from tests.test_form_1099_withholding import _add  # noqa: E402
from tests.test_refund_or_amount_owed_track1 import _attested  # noqa: E402
from tests.test_withholding_closure import _strip_closure  # noqa: E402

P = "tax.us.2025."
DECLARED = P + "schedule-a-boundary.no-gambling-other-declared"
ITEMIZED = P + "deductions.itemized"
WATCH = (
    "gambling.b1-winnings-subtotal", "schedule1.line8b-gambling", "income.agi", "schedule-a.line8a",
    "schedule-a.total", "schedule-a.excess-over-standard", "scheduleA.disposition", "deductions.line-12e",
    "income.taxable-income", "tax.line24-total-tax", "payments.line35a-refunded", "payments.line37-amount-owed",
)


def run(acts: list[dict[str, object]], run_id: str) -> dict[str, Any]:
    for _ in range(6):
        try:
            return _run_once(acts, run_id)
        except FindingModelError as exc:  # a member contradicting a base declaration: withdraw it
            m = re.search(r"contradiction: (\S+) is currently", str(exc))
            if not m:
                raise
            acts = _strip_closure(acts, m.group(1))
    raise AssertionError("too many declaration removals")


def _run_once(acts: list[dict[str, object]], run_id: str) -> dict[str, Any]:
    finished = ccr.finished_acts(acts, run_id)
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"), repo_root=ccr.ROOT, authoritative_acts=finished,
            workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user=ccr.USER, request={"schema": "run-request.v1"}, run_id=run_id,
            governance_pins=[], surface=ccr.SURFACE, output_name="out.json",
        )
        if outcome.refusal is not None:
            return {"refusal": f"{outcome.refusal.reason} {outcome.refusal.detail}"}
        pubs = {str(p.finding["symbol"]): p.finding for p in outcome.publications or ()}
        report = json.loads(outcome.output_path.read_text(encoding="utf-8")) if outcome.output_path else {}
    disp = report.get("dispositions", [])
    blocked = [r for r in disp if r.get("disposition") == "blocked"]
    held = [r for r in disp if r.get("disposition") not in ("blocked", "published")]
    out: dict[str, Any] = {"published": {}, "bottom_line_published": P + "payments.line35a-refunded" in pubs or P + "payments.line37-amount-owed" in pubs}
    for s in WATCH:
        if P + s in pubs:
            v = pubs[P + s]["value"]
            out["published"][s] = (v if isinstance(v, (dict, bool, str)) else format(Decimal(str(v)).normalize(), "f"))
    out["blocked"] = sorted(
        {(str(r.get("artifact_id", "")).replace(P, ""), str(r.get("code")),
          tuple(sorted(str(x).replace(P, "") for x in r.get("missing", []))))
         for r in blocked})
    out["blocked"] = [{"rule": a, "code": c, "missing": list(m)} for a, c, m in out["blocked"]]
    out["held"] = sorted(str(r.get("artifact_id", "")).replace(P, "") for r in held)
    return out


def set_answer(acts: list[dict[str, object]], fact_type: str, value: object) -> list[dict[str, object]]:
    acts = copy.deepcopy(acts)
    w2g._set_answer(acts, fact_type, value)
    return acts


F1098 = P + "f1098."
# The v66 mortgage route also needs the statement's box companions and the filer's circumstance answers
# (what the money paid for, who owns and pays); the values are an ordinary purchase mortgage.
COMPANIONS = (
    ("box2-outstanding-principal", 200000.0), ("box3-origination-date", "2020-06-01"),
    ("box4-overpaid-refund", 0.0), ("box5-mortgage-insurance", 0.0), ("box6-points", 0.0),
    ("box9-number-of-properties", 1.0), ("box11-other", 0.0),
)
AUTHORITY = (
    "liable-and-paid", "qualified-main-home", "acquisition-debt-use", "no-balance-increase", "no-refinance",
    "single-mortgage-single-home", "not-shared-except-spouse", "no-mortgage-interest-credit",
)
ANSWERS = (
    ("owns-the-home", "yes"), ("lives-there-most-of-the-time", "yes"), ("filing-unit-owns-home", "yes"),
    ("shared-main-home", "yes"), ("home-is-collateral", "yes"),
    ("owes-the-loan", "yes"), ("paid-the-interest", "yes"), ("no-one-else-owes-it", "yes"),
    ("this-is-the-original-loan", "yes"), ("what-the-money-paid-for", "bought-the-home"),
    ("mortgage-credit-certificate-received", "not-received"),
)


def with_mortgage(acts: list[dict[str, object]], interest: float) -> list[dict[str, object]]:
    out = cc._add_member(copy.deepcopy(acts), P + "f1098", interest, close=True, tag="gl")
    keys = "payer=demo.cc.gl.payer,statement=demo.cc.gl.statement,tax-year=2025"
    for i, (short, value) in enumerate([*COMPANIONS, *((a, "yes") for a in AUTHORITY), *ANSWERS]):
        cc._adopt(out, F1098 + short)
        _add(out, "assertion", {"finding": _attested(f"demo.gl.f1098.{i}", f"{F1098}{short}|{keys}", value)})
    w2g._set_answer(out, P + "f1098-scope.no-mortgage-statement", False)
    return out


def with_itemized_assertion(acts: list[dict[str, object]], amount: float) -> list[dict[str, object]]:
    acts = copy.deepcopy(acts)
    _add(acts, "assertion", {"finding": _attested("demo.gl.itemized", f"{ITEMIZED}|tax-year=2025", amount)})
    return acts


def returns() -> dict[str, list[dict[str, object]]]:
    win = [(6000.0, 1440.0)]
    out: dict[str, list[dict[str, object]]] = {}
    for label, answer in (("yes", "yes"), ("no", "no")):
        std = w2g._w2g_return(win)
        out[f"standard_w2g_losses-{label}"] = set_answer(std, DECLARED, answer)
        out[f"itemizer_1098_w2g_losses-{label}"] = set_answer(with_mortgage(w2g._w2g_return(win), 20000.0), DECLARED, answer)
        out[f"itemizer_assertion_w2g_losses-{label}"] = set_answer(with_itemized_assertion(w2g._w2g_return(win), 20000.0), DECLARED, answer)
        out[f"standard_no_w2g_losses-{label}"] = set_answer(w2g._w2g_return([]), DECLARED, answer)
        out[f"itemizer_1098_no_w2g_losses-{label}"] = set_answer(with_mortgage(w2g._w2g_return([]), 20000.0), DECLARED, answer)
    return out


def main() -> None:
    only = sys.argv[1:]
    results: dict[str, Any] = {}
    for name, acts in returns().items():
        if only and name not in only:
            continue
        try:
            results[name] = run(acts, "demo.gl." + re.sub(r"[^a-z0-9]+", "-", name))
        except Exception as exc:  # recorded, not hidden
            results[name] = {"error": f"{type(exc).__name__}: {str(exc)[:400]}"}
        print(name, json.dumps(results[name])[:600], file=sys.stderr, flush=True)
    print(json.dumps(results, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
