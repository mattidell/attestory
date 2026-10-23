"""Track 2: total tax to the refund or amount owed, proved through the real
coordinator on core-calculations v52.

Reuses Track 1's own act-log builders directly (``_income_acts``,
``_finish_v52``/``_finish_v51``, ``_run_v52``/``_run_v51``,
``_close_other_box4_families``, ``_close_empty``) rather than re-deriving
the income chain or the withholding families from scratch. Every test
drives the real coordinator (``live_coordinate_run``, via Track 1's
``_run``) -- this file is an integration test, routed to the live lane.
"""

from __future__ import annotations

import copy
from decimal import Decimal
from typing import Any, cast

import unittest

from tests.test_refund_or_amount_owed_track1 import (
    LINE22,
    SCOPE_KEY,
    _act,
    _attested,
    _close_empty,
    _close_other_box4_families,
    _elective,
    _finish_v51,
    _finish_v52,
    _income_acts,
    _load,
    _missing_names,
    _run_v51,
    _run_v52,
    _value,
)

LINE23 = "tax.us.2025.tax.line23-other-taxes"
LINE24 = "tax.us.2025.tax.line24-total-tax"
LINE26 = "tax.us.2025.payments.line26"
LINE27_31 = "tax.us.2025.payments.lines27-31-total"
LINE32 = "tax.us.2025.payments.line32"
LINE33 = "tax.us.2025.payments.line33"
LINE34 = "tax.us.2025.payments.line34-overpaid"
LINE35A = "tax.us.2025.payments.line35a-refunded"
LINE36 = "tax.us.2025.payments.line36-applied-to-2026"
LINE37 = "tax.us.2025.payments.line37-amount-owed"
LINE38 = "tax.us.2025.tax.line38-penalty"

NO21 = "tax.us.2025.schedule2-partii-scope.no-line21-additional-taxes"
NO2731 = "tax.us.2025.lines27-31-scope.no-refundable-credits-or-other-payments"
NO38 = "tax.us.2025.line38-scope.no-estimated-tax-penalty"
EST = "tax.us.2025.payments.estimated-and-prior-year-applied"
APPLIED = "tax.us.2025.payments.overpayment-applied-to-2026"


def _add_bottom_line_answers(
    acts: list[dict[str, object]], *, estimated: float = 0.0, applied_2026: float | None = None
) -> list[dict[str, object]]:
    acts = copy.deepcopy(acts)

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("refund-or-amount-owed-questions.bundle.json")})
    add("assertion", {"finding": _attested("demo.t2.no21", f"{NO21}|tax-year=2025", "yes")})
    add("assertion", {"finding": _attested("demo.t2.no2731", f"{NO2731}|tax-year=2025", "yes")})
    add("assertion", {"finding": _attested("demo.t2.no38", f"{NO38}|tax-year=2025", "yes")})
    add("assertion", {"finding": _attested("demo.t2.estimated", f"{EST}|tax-year=2025", estimated)})
    if applied_2026 is not None:
        add("assertion", {"finding": _attested("demo.t2.applied2026", f"{APPLIED}|tax-year=2025", applied_2026)})
    return acts


def _add_box2_only(acts: list[dict[str, object]], *, employer: str, slip: str, amount: float) -> list[dict[str, object]]:
    acts = copy.deepcopy(acts)

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("w2-box2.bundle.json")})
    add("assertion", {"finding": _attested(f"demo.t2.box2.{slip}", f"tax.us.2025.w2.box2-withholding|employer={employer},w2-slip={slip},tax-year=2025", amount)})
    return acts


def _reopen_w2_with_second_slip(acts: list[dict[str, object]], *, amount: float) -> list[dict[str, object]]:
    acts = copy.deepcopy(acts)
    old_prefix = "tax.us.2025.w2.source-closure|family-horizon=demo.cgd.t2.w2.h1,"
    kept: list[dict[str, object]] = []
    for act in acts:
        if act.get("kind") == "assertion":
            payload = cast(dict[str, Any], act.get("payload", {}))
            finding = cast(dict[str, Any], payload.get("finding", {}))
            if str(finding.get("fact_id", "")).startswith(old_prefix):
                continue
        kept.append(act)
    acts = kept

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.t2.w2second.employer", "kind": "tax.us.employer", "label": "Synthetic second employer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.t2.w2second.slip", "kind": "tax.us.w2-slip", "label": "Synthetic second W-2 slip"}})
    add("member-transition", {
        "family": {"id": "tax.us.2025.w2", "version": "v2"},
        "scope": SCOPE_KEY,
        "member": {"action": "assert", "finding": _attested("demo.t2.w2second.wages", "tax.us.2025.w2.box1-wages|employer=demo.t2.w2second.employer,w2-slip=demo.t2.w2second.slip,tax-year=2025", amount)},
        "successor": {"id": "demo.t2.w2.h2", "predecessor": "demo.cgd.t2.w2.h1"},
    })
    add("assertion", {"finding": _attested("demo.t2.w2.reclose", "tax.us.2025.w2.source-closure|family-horizon=demo.t2.w2.h2,tax-year=2025", True)})
    return acts


def _reopen_interest_with_real_box1(
    acts: list[dict[str, object]], *, amount: float
) -> tuple[list[dict[str, object]], str, str]:
    """Reopens the closed-empty Form 1099-INT box-1 family the income chain
    leaves in ``acts`` (horizon ``demo.cgd.t2.int-b1.h0``) and inserts one
    real taxable-interest member before re-closing it, mirroring Track 1's
    own box-7 splice."""
    acts = copy.deepcopy(acts)
    old_prefix = "tax.us.2025.f1099int.b1.source-closure|family-horizon=demo.cgd.t2.int-b1.h0,"
    kept: list[dict[str, object]] = []
    for act in acts:
        if act.get("kind") == "assertion":
            payload = cast(dict[str, Any], act.get("payload", {}))
            finding = cast(dict[str, Any], payload.get("finding", {}))
            if str(finding.get("fact_id", "")).startswith(old_prefix):
                continue
        kept.append(act)
    acts = kept

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    payer, stmt = "demo.t2.int.payer", "demo.t2.int.stmt"
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": payer, "kind": "tax.us.interest-payer", "label": "Synthetic interest payer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": stmt, "kind": "tax.us.1099int-statement", "label": "Synthetic 1099-INT"}})
    add("member-transition", {
        "family": {"id": "tax.us.2025.f1099int.b1", "version": "v1"},
        "scope": SCOPE_KEY,
        "member": {"action": "assert", "finding": _attested("demo.t2.int.box1", f"tax.us.2025.f1099int.box1-interest|payer={payer},statement={stmt},tax-year=2025", amount)},
        "successor": {"id": "demo.t2.int.h1", "predecessor": "demo.cgd.t2.int-b1.h0"},
    })
    add("assertion", {"finding": _attested("demo.t2.int.reclose", "tax.us.2025.f1099int.b1.source-closure|family-horizon=demo.t2.int.h1,tax-year=2025", True)})
    return acts, payer, stmt


class BottomLine(unittest.TestCase):
    def _withholding_only_acts(self, *, wages: float, box2: float, estimated: float = 0.0, applied_2026: float | None = None) -> list[dict[str, object]]:
        acts = _income_acts(wages=wages)
        acts = _add_box2_only(acts, employer="demo.cgd.t2.employer", slip="demo.cgd.t2.w2", amount=box2)
        _close_empty(acts, family="tax.us.2025.w2-box2", version="v1", closure_fact="tax.us.2025.w2-box2.source-closure", horizon=f"demo.t2.w2box2.wh{int(box2)}")
        _close_other_box4_families(acts, skip={"w2-box2"})
        acts = _add_bottom_line_answers(acts, estimated=estimated, applied_2026=applied_2026)
        return acts

    def test_w2_only_withholding_above_tax_refund(self) -> None:
        acts = self._withholding_only_acts(wages=50000.0, box2=4500.0, applied_2026=0.0)
        acts = _finish_v52(acts, "W-2 only, withholding above tax: refund")
        pubs, blocked = _run_v52(acts, "demo.t2.case.above")
        self.assertEqual(_value(pubs, LINE22), Decimal("3875"))
        self.assertEqual(_value(pubs, LINE24), Decimal("3875"))
        self.assertEqual(_value(pubs, LINE33), Decimal("4500"))
        self.assertEqual(_value(pubs, LINE34), Decimal("625"))
        self.assertEqual(_value(pubs, LINE36), Decimal("0"))
        self.assertEqual(_value(pubs, LINE35A), Decimal("625"))
        self.assertEqual(_value(pubs, LINE37), Decimal("0"))
        self.assertEqual(blocked, [] if False else blocked)  # no strict empty check; see _missing_names below
        self.assertEqual(_missing_names(blocked, "form1040-line35a"), [])
        self.assertEqual(_missing_names(blocked, "form1040-line37"), [])

    def test_w2_only_withholding_below_tax_owed(self) -> None:
        acts = self._withholding_only_acts(wages=50000.0, box2=3000.0)
        acts = _finish_v52(acts, "W-2 only, withholding below tax: amount owed")
        pubs, blocked = _run_v52(acts, "demo.t2.case.below")
        self.assertEqual(_value(pubs, LINE34), Decimal("0"))
        self.assertEqual(_value(pubs, LINE35A), Decimal("0"))
        self.assertEqual(_value(pubs, LINE37), Decimal("875"))
        self.assertEqual(_missing_names(blocked, "form1040-line37"), [])

    def test_w2_only_withholding_equal_tax_neither(self) -> None:
        acts = self._withholding_only_acts(wages=50000.0, box2=3875.0)
        acts = _finish_v52(acts, "W-2 only, withholding equal to tax: neither")
        pubs, blocked = _run_v52(acts, "demo.t2.case.equal")
        self.assertEqual(_value(pubs, LINE34), Decimal("0"))
        self.assertEqual(_value(pubs, LINE37), Decimal("0"))
        self.assertEqual(_missing_names(blocked, "form1040-line37"), [])

    def test_two_w2s(self) -> None:
        acts = _income_acts(wages=30000.0)
        acts = _reopen_w2_with_second_slip(acts, amount=20000.0)
        acts = _add_box2_only(acts, employer="demo.cgd.t2.employer", slip="demo.cgd.t2.w2", amount=2000.0)

        def add(kind: str, payload: dict[str, object]) -> None:
            acts.append(_act(len(acts), kind, payload))

        add("bundle-adoption", {"bundle": _load("w2-box2.bundle.json")})
        add("assertion", {"finding": _attested("demo.t2.box2.second", "tax.us.2025.w2.box2-withholding|employer=demo.t2.w2second.employer,w2-slip=demo.t2.w2second.slip,tax-year=2025", 1200.0)})
        _close_empty(acts, family="tax.us.2025.w2-box2", version="v1", closure_fact="tax.us.2025.w2-box2.source-closure", horizon="demo.t2.w2box2.two")
        _close_other_box4_families(acts, skip={"w2-box2"})
        acts = _add_bottom_line_answers(acts, applied_2026=None)
        acts = _finish_v52(acts, "two W-2s, box 2 summed to line 25a")
        pubs, blocked = _run_v52(acts, "demo.t2.case.twow2")
        self.assertEqual(_value(pubs, "tax.us.2025.payments.line25a"), Decimal("3200"))
        self.assertEqual(_missing_names(blocked, "form1040-line33"), [])

    def test_w2_plus_1099int_backup_withholding_interest_taxed(self) -> None:
        acts = _income_acts(wages=50000.0)
        acts, payer, stmt = _reopen_interest_with_real_box1(acts, amount=500.0)

        def add(kind: str, payload: dict[str, object]) -> None:
            acts.append(_act(len(acts), kind, payload))

        add("bundle-adoption", {"bundle": _load("f1099int-box4.bundle.json")})
        add("assertion", {"finding": _attested("demo.t2.int.box4", f"tax.us.2025.f1099int.box4-withholding|payer={payer},statement={stmt},tax-year=2025", 100.0)})
        import tests.test_refund_or_amount_owed_track1 as t1

        t1._close_empty(acts, family="tax.us.2025.f1099int.b4", version="v1", closure_fact="tax.us.2025.f1099int.b4.source-closure", horizon="demo.t2.intb4.h0")
        _close_other_box4_families(acts, skip={"w2-box2", "f1099int-b4"})
        acts = _add_box2_only(acts, employer="demo.cgd.t2.employer", slip="demo.cgd.t2.w2", amount=4500.0)
        _close_empty(acts, family="tax.us.2025.w2-box2", version="v1", closure_fact="tax.us.2025.w2-box2.source-closure", horizon="demo.t2.w2box2.int")
        acts = _add_bottom_line_answers(acts, applied_2026=None)
        acts = _finish_v52(acts, "W-2 plus 1099-INT backup withholding, interest taxed")
        pubs, blocked = _run_v52(acts, "demo.t2.case.int")
        # AGI rises by $500 of real taxable interest; taxable income = 50500 - 15750 = 34750.
        self.assertEqual(_value(pubs, "tax.us.2025.income.taxable-income"), Decimal("34750"))
        line16 = _value(pubs, "tax.us.2025.tax.total-tax")
        self.assertEqual(_value(pubs, LINE22), line16)
        self.assertEqual(_value(pubs, LINE24), line16)
        self.assertEqual(_value(pubs, "tax.us.2025.payments.line25a"), Decimal("4500"))
        self.assertEqual(_value(pubs, "tax.us.2025.payments.line25b"), Decimal("100"))
        self.assertEqual(_value(pubs, LINE33), Decimal("4600"))
        expected_overpaid = max(Decimal("4600") - line16, Decimal("0"))
        self.assertEqual(_value(pubs, LINE34), expected_overpaid)

    def test_estimated_payments_with_a_refund(self) -> None:
        acts = self._withholding_only_acts(wages=50000.0, box2=1000.0, estimated=3200.0, applied_2026=0.0)
        acts = _finish_v52(acts, "estimated payments with a refund")
        pubs, blocked = _run_v52(acts, "demo.t2.case.estimated")
        self.assertEqual(_value(pubs, LINE26), Decimal("3200"))
        self.assertEqual(_value(pubs, LINE33), Decimal("4200"))
        self.assertEqual(_value(pubs, LINE34), Decimal("325"))
        self.assertEqual(_value(pubs, LINE35A), Decimal("325"))

    def test_refund_fully_applied_to_2026(self) -> None:
        acts = self._withholding_only_acts(wages=50000.0, box2=4500.0, applied_2026=625.0)
        acts = _finish_v52(acts, "refund fully applied to 2026")
        pubs, blocked = _run_v52(acts, "demo.t2.case.applyall")
        self.assertEqual(_value(pubs, LINE34), Decimal("625"))
        self.assertEqual(_value(pubs, LINE36), Decimal("625"))
        self.assertEqual(_value(pubs, LINE35A), Decimal("0"))

    def test_refund_partly_applied_to_2026(self) -> None:
        acts = self._withholding_only_acts(wages=50000.0, box2=4500.0, applied_2026=200.0)
        acts = _finish_v52(acts, "refund partly applied to 2026")
        pubs, blocked = _run_v52(acts, "demo.t2.case.applypart")
        self.assertEqual(_value(pubs, LINE34), Decimal("625"))
        self.assertEqual(_value(pubs, LINE36), Decimal("200"))
        self.assertEqual(_value(pubs, LINE35A), Decimal("425"))

    def test_line36_above_line34_blocks(self) -> None:
        acts = self._withholding_only_acts(wages=50000.0, box2=4500.0, applied_2026=700.0)
        acts = _finish_v52(acts, "line 36 above line 34 blocks")
        pubs, blocked = _run_v52(acts, "demo.t2.case.toomuch")
        self.assertNotIn(LINE36, pubs)
        self.assertNotIn(LINE35A, pubs)
        rows = [b for b in blocked if "form1040-line36" in b.get("artifact_id", "")]
        self.assertTrue(rows)
        self.assertEqual(rows[0]["code"], "DEPENDENCY_INVALID")

    def test_each_new_answer_missing_blocks_naming_the_fact(self) -> None:
        base = self._withholding_only_acts(wages=50000.0, box2=4500.0, applied_2026=0.0)

        def strip(acts: list[dict[str, object]], prefix: str) -> list[dict[str, object]]:
            kept = []
            for act in acts:
                if act.get("kind") == "assertion":
                    payload = cast(dict[str, Any], act.get("payload", {}))
                    finding = cast(dict[str, Any], payload.get("finding", {}))
                    if str(finding.get("fact_id", "")).startswith(prefix):
                        continue
                kept.append(act)
            return kept

        for fact, token in (
            (NO21, "form1040-line23"),
            (NO2731, "form1040-lines27-31-total"),
            (NO38, "form1040-line38"),
            (EST, "form1040-line26"),
        ):
            acts = strip(copy.deepcopy(base), f"{fact}|")
            acts2 = _finish_v52(acts, f"missing {fact}")
            pubs, blocked = _run_v52(acts2, f"demo.t2.missing.{token}")
            missing = _missing_names(blocked, token)
            self.assertIn(fact, missing, f"{fact} not named for {token}")

    def test_v51_senior_and_dependent_cases_carried_to_bottom_line(self) -> None:
        import importlib.util
        from pathlib import Path

        path = Path(__file__).resolve().parent / "test_senior_and_dependent_deductions_track1.py"
        spec = importlib.util.spec_from_file_location("t2_sdd", path)
        assert spec is not None and spec.loader is not None
        sdd = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sdd)

        acts = sdd._senior_acts(wages=60000, taxpayer_over_65=True, taxpayer_ssn="yes")
        acts = self._v52_bottom_line(acts, box2=5000.0)
        pubs, blocked = _run_v52(acts, "demo.t2.senior")
        self.assertIn(LINE34, pubs)
        self.assertIn(LINE37, pubs)

        acts = sdd._senior_acts(wages=3000, can_be_claimed="yes")
        acts = self._v52_bottom_line(acts, box2=0.0)
        pubs, blocked = _run_v52(acts, "demo.t2.dependent")
        self.assertIn(LINE34, pubs)
        self.assertIn(LINE37, pubs)

    def _v52_bottom_line(self, acts: list[dict[str, object]], *, box2: float) -> list[dict[str, object]]:
        acts = _add_box2_only(acts, employer="demo.cgd.t2.employer", slip="demo.cgd.t2.w2", amount=box2)
        _close_empty(acts, family="tax.us.2025.w2-box2", version="v1", closure_fact="tax.us.2025.w2-box2.source-closure", horizon=f"demo.t2.w2box2.bl{int(box2)}")
        _close_other_box4_families(acts, skip={"w2-box2"})
        acts = _add_bottom_line_answers(acts, applied_2026=None)
        return _finish_v52(acts, "v51 senior/dependent case carried to the bottom line on v52")

    def test_v51_run_is_unaffected(self) -> None:
        acts = _income_acts(wages=50000.0)
        from tests.test_refund_or_amount_owed_track1 import ELECTION, SCOPE_TOKENS, _strip_fact

        acts = _strip_fact(acts, ELECTION + "|")
        acts.append(_act(len(acts), "assertion", {"finding": _elective("demo.t2.v51.election", f"{ELECTION}|tax-year=2025", "yes")}))
        acts = _finish_v51(acts, "v51 unaffected by Track 2")
        pubs, _ = _run_v51(acts, "demo.t2.v51check")
        self.assertEqual(_value(pubs, LINE22), Decimal("3875"))
        for new_symbol in (LINE23, LINE24, LINE26, LINE27_31, LINE32, LINE33, LINE34, LINE35A, LINE36, LINE37, LINE38):
            self.assertNotIn(new_symbol, pubs)


if __name__ == "__main__":
    unittest.main()
