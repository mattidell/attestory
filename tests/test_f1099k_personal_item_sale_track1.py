"""Tests for Form 1099-K personal item sale loss reporting and migration (Track 1).

Covers all 33 materially distinct disposition paths settled in D2 and proved in
d2_probe.py, now running through live_coordinate_run and build_presentation_model
against adopted production content:
- Package core-calculations v48
- Published packages registry v46
- Release demo.release.sli-worksheet-integration.2025 v46
"""

from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.presentation_projection import build_presentation_model
from packages.derivation.production_resolver import PublicationSurface
from packages.tax.loader import (
    load_f1099k_bundle,
    load_f1099k_circumstances_bundle,
)
from tests.test_f1098_mortgage_interest_line12e_track2 import _load_fixture_adoption
from tests.test_form1099g_box1_schedule1_line7 import _act, _attested
from tests.test_ssa1099_benefits_line6_track2 import _ssa_acts

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
REGISTRY_PATH = CONTENT / "published-packages.v46.json"
RELEASE_DIR = ROOT / "packages" / "sample_data" / "student_loan_worksheet_integration" / "publication_surface" / "releases"
RELEASE_PATH = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v46.json"
PACKAGE_PATH = CONTENT / "package.core-calculations.v48.json"

REGISTRY_V45_PATH = CONTENT / "published-packages.v45.json"
RELEASE_V45_PATH = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v45.json"
PACKAGE_V47_PATH = CONTENT / "package.core-calculations.v47.json"

SURFACE = PublicationSurface(RELEASE_DIR, REGISTRY_PATH, CONTENT)
SURFACE_V45 = PublicationSurface(RELEASE_DIR, REGISTRY_V45_PATH, CONTENT)

USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}

FACT = "tax.us.2025.f1099k."
BOX1A = FACT + "box1a-gross-amount"
BOX4 = FACT + "box4-federal-withholding"
CLOSURE_TYPE = FACT + "source-closure"
FAMILY_ID = "tax.us.2025.f1099k"
REASON_SYMBOL = FACT + "statement-loss-reason"
TOP_ENTRY_SYMBOL = "tax.us.2025.schedule1.top-entry"
UNRESOLVED_SYMBOL = "tax.us.2025.f1099k.unresolved"

Q1 = FACT + "covers-only-single-item"
Q3 = FACT + "acquired-by-purchase"
Q4 = FACT + "primary-purpose-at-acquisition"
Q5 = FACT + "exclusive-personal-use"
Q7 = FACT + "digital-asset-involvement"
Q8_PRICE = FACT + "agreed-item-price"
Q8_SHIP = FACT + "shipping-arrangement"
Q9_FEES = FACT + "platform-fees"
Q9_SELLER_SHIP = FACT + "seller-paid-shipping"
Q10_TAX = FACT + "sales-tax-collected-by-platform"
Q10_REFUND = FACT + "refund-amount"
Q11_BUYER_SHIP = FACT + "buyer-paid-shipping"
Q12_COST = FACT + "purchase-cost"
Q12_GATE = FACT + "cost-basis-known"
Q13 = FACT + "lasting-improvements-or-adjustments"

CIRCUMSTANCE_FACTS = (
    Q1, Q3, Q4, Q5, Q7, Q8_PRICE, Q8_SHIP, Q9_FEES, Q9_SELLER_SHIP,
    Q10_TAX, Q10_REFUND, Q11_BUYER_SHIP, Q12_COST, Q12_GATE, Q13,
)


def _statement_fact_id(fact_type: str, payer: str = "demo.platform.a", stmt: str = "demo.stmt.a") -> str:
    return f"{fact_type}|payer={payer},statement={stmt},tax-year=2025"


def _make_base_acts(wages: float = 90000.0, unemployment: float | None = None) -> list[dict[str, object]]:
    acts = _ssa_acts(wages=wages, benefits=[], unemployment=unemployment)
    acts.pop()  # drop SSA milestone adoption

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    # Close student loan interest family closed-empty so Schedule 1 subtotal line21 evaluates to 0.00
    from tests.test_f1098e_student_loan_interest_agi_track6 import (
        _load as _load_sli,
        SLI_SCOPE_UNIVERSAL_TOKENS,
        SLI_SCOPE_LEGAL_ZERO_TOKENS,
        SCHED1_LINE_TOKENS,
    )
    add("bundle-adoption", {"bundle": _load_sli("f1098e.bundle.json")})
    add("bundle-adoption", {"bundle": _load_sli("sli-scope.bundle.json")})
    add("bundle-adoption", {"bundle": _load_sli("schedule1-adjustments-scope.bundle.json")})
    add("horizon-genesis", {"family": {"id": "tax.us.2025.f1098e.1", "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1098e.h0"})
    add("assertion", {"finding": _attested("demo.f1098e.closure", "tax.us.2025.f1098e.1.source-closure|family-horizon=demo.f1098e.h0,tax-year=2025", True)})
    for token in SLI_SCOPE_UNIVERSAL_TOKENS + SLI_SCOPE_LEGAL_ZERO_TOKENS:
        add("assertion", {"finding": _attested(f"demo.sli-scope.{token}", f"tax.us.2025.sli-scope.{token}|tax-year=2025", "yes")})
    for token in SCHED1_LINE_TOKENS:
        add("assertion", {"finding": _attested(f"demo.sched1-scope.{token}", f"tax.us.2025.schedule1-adjustments-scope.{token}|tax-year=2025", "yes")})

    add("bundle-adoption", {"bundle": load_f1099k_bundle(version="v2")})
    add("bundle-adoption", {"bundle": load_f1099k_circumstances_bundle()})

    return acts


def _add_statement_entities(acts: list[dict[str, object]], payer: str, stmt: str) -> None:
    acts.append(_act(len(acts), "entity-introduced", {"entity": {"schema": "entity.v1", "id": payer, "kind": "tax.us.1099k-platform", "label": "Synthetic platform"}}))
    acts.append(_act(len(acts), "entity-introduced", {"entity": {"schema": "entity.v1", "id": stmt, "kind": "tax.us.1099k-statement", "label": "Synthetic Form 1099-K"}}))


def _add_statement_assertions(
    acts: list[dict[str, object]],
    *,
    payer: str = "demo.platform.a",
    stmt: str = "demo.stmt.a",
    box1a: float = 880.0,
    box4: float = 0.0,
    answers: dict[str, Any] | None = None,
) -> None:
    ans: dict[str, Any] = {
        Q1: "yes", Q3: "yes", Q4: "personal-use", Q5: "yes", Q7: "no",
        Q8_PRICE: 800.0, Q8_SHIP: "platform-pass-through", Q9_FEES: 80.0,
        Q9_SELLER_SHIP: 0.0, Q10_TAX: 56.0, Q10_REFUND: 0.0,
        Q11_BUYER_SHIP: 24.0, Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "no",
    }
    if answers:
        ans.update(answers)

    acts.append(_act(len(acts), "assertion", {"finding": _attested(f"f.b1a.{stmt}", _statement_fact_id(BOX1A, payer, stmt), box1a)}))
    acts.append(_act(len(acts), "assertion", {"finding": _attested(f"f.b4.{stmt}", _statement_fact_id(BOX4, payer, stmt), box4)}))

    for fact_id, val in ans.items():
        if val is not None:
            short = fact_id.rsplit(".", 1)[-1]
            acts.append(_act(len(acts), "assertion", {"finding": _attested(f"f.{short}.{stmt}", _statement_fact_id(fact_id, payer, stmt), val)}))


def _add_family_closure(acts: list[dict[str, object]], horizon: str, closed: bool = True) -> None:
    acts.append(_act(len(acts), "assertion", {"finding": _attested(f"f.closure.{horizon}", f"{CLOSURE_TYPE}|family-horizon={horizon},tax-year=2025", closed)}))


def _finish_acts(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    pkg_data = json.loads(PACKAGE_PATH.read_text("utf-8"))
    pkg_csum = pkg_data["package_checksum"]
    rel_csum = hashlib.sha256(RELEASE_PATH.read_bytes()).hexdigest()

    built = copy.deepcopy(acts)
    adoption = copy.deepcopy(_load_fixture_adoption())
    adoption["act_id"] = f"demo.f1099k.adopt.{len(built):03d}"
    adoption["committed_against"] = len(built)
    payload = adoption["payload"]
    assert isinstance(payload, dict)
    payload["package"] = {"id": "tax.us.2025.package.core-calculations", "version": "v48", "checksum": pkg_csum}
    payload["release"] = {"id": "demo.release.sli-worksheet-integration.2025", "version": "v46", "checksum": rel_csum}
    payload["audit"] = {"note": "synthetic Form 1099-K personal item sale loss track1 test"}
    built.append(adoption)
    for index, row in enumerate(built):
        row["committed_against"] = index
        row["actor"] = USER
    return built


def _finish_acts_v45(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    pkg_data = json.loads(PACKAGE_V47_PATH.read_text("utf-8"))
    pkg_csum = pkg_data["package_checksum"]
    rel_csum = hashlib.sha256(RELEASE_V45_PATH.read_bytes()).hexdigest()

    built = copy.deepcopy(acts)
    adoption = copy.deepcopy(_load_fixture_adoption())
    adoption["act_id"] = f"demo.f1099k.adopt.{len(built):03d}"
    adoption["committed_against"] = len(built)
    payload = adoption["payload"]
    assert isinstance(payload, dict)
    payload["package"] = {"id": "tax.us.2025.package.core-calculations", "version": "v47", "checksum": pkg_csum}
    payload["release"] = {"id": "demo.release.sli-worksheet-integration.2025", "version": "v45", "checksum": rel_csum}
    payload["audit"] = {"note": "synthetic Form 1099-K personal item sale loss track1 test on v45"}
    built.append(adoption)
    for index, row in enumerate(built):
        row["committed_against"] = index
        row["actor"] = USER
    return built


EXPECTED_OUTCOMES: dict[str, dict[str, Any]] = {
    "1. closed-empty-with-completeness": {
        "expected_token": "0",
        "expected_top_amount": 0,
        "is_statement_reason": False,
        "expected_top_disp": "published",
        "expected_unres_disp": "guard_inapplicable",
        "expected_top_sentences": [],
        "expected_unres_sentences": [],
    },
    "2. unemployment-with-completeness": {
        "expected_token": "0",
        "expected_top_amount": 0,
        "is_statement_reason": False,
        "expected_top_disp": "published",
        "expected_unres_disp": "guard_inapplicable",
        "expected_top_sentences": [],
        "expected_unres_sentences": [],
    },
    "3. unemployment-without-completeness": {
        "expected_token": "SOURCE_SET_UNCLOSED",
        "expected_top_amount": None,
        "is_statement_reason": False,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "guard_inapplicable",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [],
    },
    "4. w2-only-return": {
        "expected_token": "SOURCE_SET_UNCLOSED",
        "expected_top_amount": None,
        "is_statement_reason": False,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "guard_inapplicable",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [],
    },
    "5. supported-loss-pass-through-shipping": {
        "expected_token": "supported-loss",
        "expected_top_amount": 880.0,
        "is_statement_reason": True,
        "expected_top_disp": "published",
        "expected_unres_disp": "guard_inapplicable",
        "expected_top_sentences": [
            "This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1."
        ],
        "expected_unres_sentences": [],
    },
    "6. supported-loss-seller-received-shipping": {
        "expected_token": "supported-loss",
        "expected_top_amount": 880.0,
        "is_statement_reason": True,
        "expected_top_disp": "published",
        "expected_unres_disp": "guard_inapplicable",
        "expected_top_sentences": [
            "This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1."
        ],
        "expected_unres_sentences": [],
    },
    "7. supported-loss-with-refund": {
        "expected_token": "supported-loss",
        "expected_top_amount": 800.0,
        "is_statement_reason": True,
        "expected_top_disp": "published",
        "expected_unres_disp": "guard_inapplicable",
        "expected_top_sentences": [
            "This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1."
        ],
        "expected_unres_sentences": [],
    },
    "8. supported-loss-free-shipping-seller-paid": {
        "expected_token": "supported-loss",
        "expected_top_amount": 800.0,
        "is_statement_reason": True,
        "expected_top_disp": "published",
        "expected_unres_disp": "guard_inapplicable",
        "expected_top_sentences": [
            "This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1."
        ],
        "expected_unres_sentences": [],
    },
    "9. two-statements-out-of-scope": {
        "expected_token": "multiple-f1099k-out-of-scope",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "More than one Form 1099-K statement was received; reporting personal item sale losses across multiple statements is outside the supported scope of this return."
        ],
    },
    "10. unsupported-gain": {
        "expected_token": "unsupported-gain",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "The sale resulted in a gain or profit, which cannot be reported as a personal item loss on Schedule 1."
        ],
    },
    "11. break-even-sale": {
        "expected_token": "break-even-sale",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "The sale broke even with no gain or loss, so no adjustment is reported on Schedule 1."
        ],
    },
    "12. investment-purpose-excluded": {
        "expected_token": "investment-purpose-excluded",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "The item was acquired for investment or profit; personal item loss treatment does not apply."
        ],
    },
    "13. resale-inventory-excluded": {
        "expected_token": "resale-inventory-excluded",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "The item was acquired for resale or business inventory; personal item loss treatment does not apply."
        ],
    },
    "14. prior-depreciable-use-excluded": {
        "expected_token": "prior-depreciable-use-excluded",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "The item was used for business or rental purposes; personal item loss treatment does not apply."
        ],
    },
    "15. digital-asset-excluded": {
        "expected_token": "digital-asset-excluded",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "The transaction involved digital assets or virtual currency, which are outside the scope of this personal item sale route."
        ],
    },
    "16. multi-sale-statement-unsupported": {
        "expected_token": "multi-sale-statement-unsupported",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "The Form 1099-K statement covers more than a single personal item sale."
        ],
    },
    "17. non-purchase-acquisition-unsupported": {
        "expected_token": "non-purchase-acquisition-unsupported",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "The item was not acquired by purchase."
        ],
    },
    "18. basis-adjustment-unsupported": {
        "expected_token": "basis-adjustment-unsupported",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "Lasting improvements or other basis adjustments were made to the item."
        ],
    },
    "19. backup-withholding-unsupported": {
        "expected_token": "backup-withholding-unsupported",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "Federal income tax was withheld (Box 4), which requires separate reporting."
        ],
    },
    "20. cost-basis-unknown": {
        "expected_token": "cost-basis-unknown",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "The original purchase cost of the item is unknown."
        ],
    },
    "21. unanswered-stop": {
        "expected_token": "personal-use-unconfirmed",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "The question regarding exclusive personal use has no current answer."
        ],
    },
    "22. unexplained-reconciliation-discrepancy": {
        "expected_token": "unexplained-reconciliation-discrepancy",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "The reported Box 1a amount does not reconcile with the item price, sales tax, and shipping amounts."
        ],
    },
    "23. supported-alongside-unsupported": {
        "expected_token": "multiple-f1099k-out-of-scope",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "More than one Form 1099-K statement was received; reporting personal item sale losses across multiple statements is outside the supported scope of this return."
        ],
    },
    "24. late-member-after-closure": {
        "expected_token": "multiple-f1099k-out-of-scope",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "More than one Form 1099-K statement was received; reporting personal item sale losses across multiple statements is outside the supported scope of this return."
        ],
    },
    "25. gain-loss-boundary-correction": {
        "expected_token": "unsupported-gain",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "The sale resulted in a gain or profit, which cannot be reported as a personal item loss on Schedule 1."
        ],
    },
    "26. omitted-platform-fee": {
        "expected_token": "platform-fees-unanswered",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "The question regarding platform selling fees has no current answer."
        ],
    },
    "27. withdrawn-amount": {
        "expected_token": "agreed-price-unanswered",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "The question regarding agreed item price has no current answer."
        ],
    },
    "28. cannot-tell-improvements": {
        "expected_token": "cannot-tell-improvements",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "It is not known whether lasting improvements or other basis adjustments were made to the item."
        ],
    },
    "29. boundary-case-1-seller-received-shipping-gain": {
        "expected_token": "unsupported-gain",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "The sale resulted in a gain or profit, which cannot be reported as a personal item loss on Schedule 1."
        ],
    },
    "30. boundary-case-2-refund-loss": {
        "expected_token": "supported-loss",
        "expected_top_amount": 800.0,
        "is_statement_reason": True,
        "expected_top_disp": "published",
        "expected_unres_disp": "guard_inapplicable",
        "expected_top_sentences": [
            "This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1."
        ],
        "expected_unres_sentences": [],
    },
    "31. boundary-case-3-none-shipping-seller-paid-loss": {
        "expected_token": "supported-loss",
        "expected_top_amount": 800.0,
        "is_statement_reason": True,
        "expected_top_disp": "published",
        "expected_unres_disp": "guard_inapplicable",
        "expected_top_sentences": [
            "This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1."
        ],
        "expected_unres_sentences": [],
    },
    "32. boundary-case-4-pass-through-shipping-loss": {
        "expected_token": "supported-loss",
        "expected_top_amount": 900.0,
        "is_statement_reason": True,
        "expected_top_disp": "published",
        "expected_unres_disp": "guard_inapplicable",
        "expected_top_sentences": [
            "This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1."
        ],
        "expected_unres_sentences": [],
    },
    "33. boundary-case-5-pass-through-seller-paid-gain": {
        "expected_token": "additional-seller-shipping-unsupported",
        "expected_top_amount": None,
        "is_statement_reason": True,
        "expected_top_disp": "blocked",
        "expected_unres_disp": "blocked",
        "expected_top_sentences": ["Form 1099-K loss entry cannot be computed."],
        "expected_unres_sentences": [
            "Shipping the person paid in addition to a platform-supplied label is not yet handled, so the route cannot tell whether the sale was a gain or a loss."
        ],
    },
}


class Form1099KPersonalItemSaleDispositionPaths(unittest.TestCase):
    """Test all 33 disposition paths using adopted production content."""

    def _run_and_assert(self, path_key: str, acts: list[dict[str, object]], run_id: str) -> None:
        finished = _finish_acts(acts)
        with TemporaryDirectory() as tmp:
            result = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "workspace"),
                repo_root=ROOT,
                authoritative_acts=finished,
                workspace_revision=len(finished),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id=run_id,
                governance_pins=[],
                surface=SURFACE,
                output_name="out.json",
            )
            self.assertIsNone(result.refusal)
            assert result.output_path is not None and result.presentation_path is not None
            report = json.loads(result.output_path.read_text("utf-8"))
            model = json.loads(result.presentation_path.read_text("utf-8"))

            publications = [copy.deepcopy(p.finding) for p in (result.publications or ())]
            top_entry_pubs = [p for p in publications if p.get("symbol") == TOP_ENTRY_SYMBOL]
            loss_reason_pubs = [p for p in publications if str(p.get("symbol", "")).startswith(REASON_SYMBOL)]

            dispositions = report.get("dispositions", [])
            top_entry_disps = [d for d in dispositions if d.get("symbol") == TOP_ENTRY_SYMBOL or "schedule1-top-entry" in str(d.get("artifact_id", ""))]

            sections = model.get("sections", [])
            top_entry_field = next((s for s in sections if (s.get("field") or {}).get("id") == "tax.us.2025.schedule1.top-entry.form-field"), None)
            unresolved_field = next((s for s in sections if (s.get("field") or {}).get("id") == "tax.us.2025.form.f1099k.unresolved.form-field"), None)

            top_disp = ((top_entry_field or {}).get("resolved") or {}).get("disposition")
            if top_disp in ("published_value", "published"):
                top_entry_explain = ((top_entry_field or {}).get("field") or {}).get("dispositions", {}).get("published_value", {}).get("explain", "")
            else:
                top_entry_explain = ((top_entry_field or {}).get("field") or {}).get("dispositions", {}).get("blocked", {}).get("explain", "")

            unresolved_resolved = (unresolved_field or {}).get("resolved") or {}
            unres_disp = unresolved_resolved.get("disposition")
            unresolved_reasons = [r["sentence"] for r in unresolved_resolved.get("reasons", [])]

            decl = EXPECTED_OUTCOMES[path_key]
            expected_token = decl["expected_token"]
            is_stmt_reason = decl["is_statement_reason"]

            if is_stmt_reason:
                reason_pubs = [p.get("value") for p in loss_reason_pubs]
                self.assertTrue(reason_pubs and all(r == expected_token for r in reason_pubs), f"{path_key}: Expected reason {expected_token}, got {reason_pubs}")
            else:
                if expected_token == "0":
                    actual_token = str(top_entry_pubs[0].get("value")) if top_entry_pubs else "none"
                    self.assertEqual(actual_token, expected_token)
                else:
                    actual_code = str(top_entry_disps[0].get("code") or top_entry_disps[0].get("disposition")) if top_entry_disps else "none"
                    self.assertEqual(actual_code, expected_token, f"{path_key}: expected code {expected_token}, got {actual_code}")

            expected_top_amt = decl.get("expected_top_amount")
            if expected_top_amt is not None:
                self.assertTrue(top_entry_pubs, f"{path_key}: expected top-entry amount {expected_top_amt}, got no publications")
                actual_top_val = top_entry_pubs[0].get("value")
                self.assertIsNotNone(actual_top_val)
                assert actual_top_val is not None
                self.assertEqual(float(actual_top_val), float(expected_top_amt))
            else:
                self.assertEqual(len(top_entry_pubs), 0, f"{path_key}: expected no top-entry publication, got {top_entry_pubs}")

            if decl.get("expected_unres_disp"):
                self.assertEqual(unres_disp, decl["expected_unres_disp"])

            for exp_sent in decl["expected_top_sentences"]:
                self.assertEqual(top_entry_explain, exp_sent)

            for exp_sent in decl["expected_unres_sentences"]:
                self.assertIn(exp_sent, unresolved_reasons)

    def _single_statement_case(self, run_id: str, *, box1a: float, box4: float, answers: dict[str, Any]) -> list[dict[str, object]]:
        acts = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts, "demo.platform.a", "demo.stmt.a")
        acts.append(_act(len(acts), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), box1a)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(acts, payer="demo.platform.a", stmt="demo.stmt.a", box1a=box1a, box4=box4, answers=answers)
        _add_family_closure(acts, "demo.f1099k.h1", closed=True)
        return acts

    def test_path_01_closed_empty_with_completeness(self) -> None:
        acts = _make_base_acts(wages=90000.0)
        acts.append(_act(len(acts), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        _add_family_closure(acts, "demo.f1099k.h0", closed=True)
        self._run_and_assert("1. closed-empty-with-completeness", acts, "demo.p1.closed-empty")

    def test_path_02_unemployment_with_completeness(self) -> None:
        acts = _make_base_acts(wages=90000.0, unemployment=500.0)
        acts.append(_act(len(acts), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        _add_family_closure(acts, "demo.f1099k.h0", closed=True)
        self._run_and_assert("2. unemployment-with-completeness", acts, "demo.p2.unemployment-with-closure")

    def test_path_03_unemployment_without_completeness(self) -> None:
        acts = _make_base_acts(wages=90000.0, unemployment=500.0)
        acts.append(_act(len(acts), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        self._run_and_assert("3. unemployment-without-completeness", acts, "demo.p3.unemployment-unclosed")

    def test_path_04_w2_only_return(self) -> None:
        acts = _ssa_acts(wages=90000.0, benefits=[])
        acts.pop()
        self._run_and_assert("4. w2-only-return", acts, "demo.p4.w2-only")

    def test_path_05_supported_loss_pass_through_shipping(self) -> None:
        acts = self._single_statement_case(
            "demo.p5.supported-loss-pass-through", box1a=880.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "platform-pass-through", Q9_FEES: 80.0,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 56.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 24.0,
                Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        self._run_and_assert("5. supported-loss-pass-through-shipping", acts, "demo.p5.supported-loss-pass-through")

    def test_path_06_supported_loss_seller_received_shipping(self) -> None:
        acts = self._single_statement_case(
            "demo.p6.supported-loss-seller-shipping", box1a=880.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "seller-received-shipping", Q9_FEES: 80.0,
                Q9_SELLER_SHIP: 24.0, Q10_TAX: 56.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 24.0,
                Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        self._run_and_assert("6. supported-loss-seller-received-shipping", acts, "demo.p6.supported-loss-seller-shipping")

    def test_path_07_supported_loss_with_refund(self) -> None:
        acts = self._single_statement_case(
            "demo.p7.supported-loss-refund", box1a=800.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "platform-pass-through", Q9_FEES: 80.0,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 0.0, Q10_REFUND: 100.0, Q11_BUYER_SHIP: 0.0,
                Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        self._run_and_assert("7. supported-loss-with-refund", acts, "demo.p7.supported-loss-refund")

    def test_path_08_supported_loss_free_shipping_seller_paid(self) -> None:
        acts = self._single_statement_case(
            "demo.p8.supported-loss-free-shipping", box1a=800.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "none", Q9_FEES: 80.0,
                Q9_SELLER_SHIP: 30.0, Q10_TAX: 0.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 0.0,
                Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        self._run_and_assert("8. supported-loss-free-shipping-seller-paid", acts, "demo.p8.supported-loss-free-shipping")

    def test_path_09_two_statements_out_of_scope(self) -> None:
        acts = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts, "demo.platform.a", "demo.stmt.a")
        _add_statement_entities(acts, "demo.platform.b", "demo.stmt.b")
        acts.append(_act(len(acts), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 880.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts, payer="demo.platform.a", stmt="demo.stmt.a", box1a=880.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "platform-pass-through", Q9_FEES: 80.0,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 56.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 24.0,
                Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.b", _statement_fact_id(BOX1A, "demo.platform.b", "demo.stmt.b"), 400.0)},
            "successor": {"id": "demo.f1099k.h2", "predecessor": "demo.f1099k.h1"},
        }))
        _add_statement_assertions(
            acts, payer="demo.platform.b", stmt="demo.stmt.b", box1a=400.0, box4=0.0,
            answers={
                Q8_PRICE: 400.0, Q8_SHIP: "none", Q9_FEES: 50.0,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 0.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 0.0,
                Q12_COST: 500.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts, "demo.f1099k.h2", closed=True)
        self._run_and_assert("9. two-statements-out-of-scope", acts, "demo.p9.two-statements")

    def test_path_10_unsupported_gain(self) -> None:
        acts = self._single_statement_case(
            "demo.p10.gain", box1a=1200.0, box4=0.0,
            answers={Q8_PRICE: 1200.0, Q9_FEES: 100.0, Q12_COST: 800.0, Q10_TAX: 0.0, Q11_BUYER_SHIP: 0.0},
        )
        self._run_and_assert("10. unsupported-gain", acts, "demo.p10.gain")

    def test_path_11_break_even_sale(self) -> None:
        acts = self._single_statement_case(
            "demo.p11.breakeven", box1a=800.0, box4=0.0,
            answers={Q8_PRICE: 800.0, Q9_FEES: 100.0, Q12_COST: 700.0, Q10_TAX: 0.0, Q11_BUYER_SHIP: 0.0},
        )
        self._run_and_assert("11. break-even-sale", acts, "demo.p11.breakeven")

    def test_path_12_investment_purpose_excluded(self) -> None:
        acts = self._single_statement_case(
            "demo.p12.investment", box1a=880.0, box4=0.0,
            answers={Q4: "investment-or-profit"},
        )
        self._run_and_assert("12. investment-purpose-excluded", acts, "demo.p12.investment")

    def test_path_13_resale_inventory_excluded(self) -> None:
        acts = self._single_statement_case(
            "demo.p13.resale", box1a=880.0, box4=0.0,
            answers={Q4: "resale-or-inventory"},
        )
        self._run_and_assert("13. resale-inventory-excluded", acts, "demo.p13.resale")

    def test_path_14_prior_depreciable_use_excluded(self) -> None:
        acts = self._single_statement_case(
            "demo.p14.depreciable", box1a=880.0, box4=0.0,
            answers={Q5: "no"},
        )
        self._run_and_assert("14. prior-depreciable-use-excluded", acts, "demo.p14.depreciable")

    def test_path_15_digital_asset_excluded(self) -> None:
        acts = self._single_statement_case(
            "demo.p15.digital-asset", box1a=880.0, box4=0.0,
            answers={Q7: "yes"},
        )
        self._run_and_assert("15. digital-asset-excluded", acts, "demo.p15.digital-asset")

    def test_path_16_multi_sale_statement_unsupported(self) -> None:
        acts = self._single_statement_case(
            "demo.p16.multi-sale", box1a=880.0, box4=0.0,
            answers={Q1: "no"},
        )
        self._run_and_assert("16. multi-sale-statement-unsupported", acts, "demo.p16.multi-sale")

    def test_path_17_non_purchase_acquisition_unsupported(self) -> None:
        acts = self._single_statement_case(
            "demo.p17.non-purchase", box1a=880.0, box4=0.0,
            answers={Q3: "no"},
        )
        self._run_and_assert("17. non-purchase-acquisition-unsupported", acts, "demo.p17.non-purchase")

    def test_path_18_basis_adjustment_unsupported(self) -> None:
        acts = self._single_statement_case(
            "demo.p18.basis-adjustment", box1a=880.0, box4=0.0,
            answers={Q13: "yes"},
        )
        self._run_and_assert("18. basis-adjustment-unsupported", acts, "demo.p18.basis-adjustment")

    def test_path_19_backup_withholding_unsupported(self) -> None:
        acts = self._single_statement_case(
            "demo.p19.withholding", box1a=880.0, box4=150.0,
            answers={},
        )
        self._run_and_assert("19. backup-withholding-unsupported", acts, "demo.p19.withholding")

    def test_path_20_cost_basis_unknown(self) -> None:
        acts = self._single_statement_case(
            "demo.p20.cost-unknown", box1a=880.0, box4=0.0,
            answers={Q12_GATE: "cannot-tell"},
        )
        self._run_and_assert("20. cost-basis-unknown", acts, "demo.p20.cost-unknown")

    def test_path_21_unanswered_stop(self) -> None:
        acts = self._single_statement_case(
            "demo.p21.unanswered", box1a=880.0, box4=0.0,
            answers={Q5: None},
        )
        self._run_and_assert("21. unanswered-stop", acts, "demo.p21.unanswered")

    def test_path_22_unexplained_reconciliation_discrepancy(self) -> None:
        acts = self._single_statement_case(
            "demo.p22.reconciliation", box1a=850.0, box4=0.0,
            answers={Q8_PRICE: 700.0, Q10_TAX: 0.0, Q11_BUYER_SHIP: 0.0},
        )
        self._run_and_assert("22. unexplained-reconciliation-discrepancy", acts, "demo.p22.reconciliation")

    def test_path_23_supported_alongside_unsupported(self) -> None:
        acts = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts, "demo.platform.a", "demo.stmt.a")
        _add_statement_entities(acts, "demo.platform.b", "demo.stmt.b")
        acts.append(_act(len(acts), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 880.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts, payer="demo.platform.a", stmt="demo.stmt.a", box1a=880.0, box4=0.0,
            answers={Q8_PRICE: 800.0, Q9_FEES: 80.0, Q10_TAX: 56.0, Q11_BUYER_SHIP: 24.0, Q12_COST: 1000.0},
        )
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.b", _statement_fact_id(BOX1A, "demo.platform.b", "demo.stmt.b"), 1200.0)},
            "successor": {"id": "demo.f1099k.h2", "predecessor": "demo.f1099k.h1"},
        }))
        _add_statement_assertions(
            acts, payer="demo.platform.b", stmt="demo.stmt.b", box1a=1200.0, box4=0.0,
            answers={Q8_PRICE: 1200.0, Q9_FEES: 100.0, Q10_TAX: 0.0, Q11_BUYER_SHIP: 0.0, Q12_COST: 800.0},
        )
        _add_family_closure(acts, "demo.f1099k.h2", closed=True)
        self._run_and_assert("23. supported-alongside-unsupported", acts, "demo.p23.supported-alongside-unsupported")

    def test_path_24_late_member_after_closure(self) -> None:
        acts = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts, "demo.platform.a", "demo.stmt.a")
        _add_statement_entities(acts, "demo.platform.b", "demo.stmt.b")
        acts.append(_act(len(acts), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 880.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(acts, payer="demo.platform.a", stmt="demo.stmt.a", box1a=880.0, box4=0.0)
        _add_family_closure(acts, "demo.f1099k.h1", closed=True)
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.b", _statement_fact_id(BOX1A, "demo.platform.b", "demo.stmt.b"), 400.0)},
            "successor": {"id": "demo.f1099k.h2", "predecessor": "demo.f1099k.h1"},
        }))
        _add_statement_assertions(acts, payer="demo.platform.b", stmt="demo.stmt.b", box1a=400.0, box4=0.0)
        self._run_and_assert("24. late-member-after-closure", acts, "demo.p24.late-member")

    def test_path_25_gain_loss_boundary_correction(self) -> None:
        acts = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts, "demo.platform.a", "demo.stmt.a")
        acts.append(_act(len(acts), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 880.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts, payer="demo.platform.a", stmt="demo.stmt.a", box1a=880.0, box4=0.0,
            answers={Q8_PRICE: 800.0, Q9_FEES: 80.0, Q10_TAX: 56.0, Q11_BUYER_SHIP: 24.0, Q12_COST: 1200.0},
        )
        _add_family_closure(acts, "demo.f1099k.h1", closed=True)
        acts.append(_act(len(acts), "assertion", {"finding": _attested("f.cost.corrected", _statement_fact_id(Q12_COST, "demo.platform.a", "demo.stmt.a"), 600.0)}))
        self._run_and_assert("25. gain-loss-boundary-correction", acts, "demo.p25.boundary-correction")

    def test_path_26_omitted_platform_fee(self) -> None:
        acts = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts, "demo.platform.a", "demo.stmt.a")
        acts.append(_act(len(acts), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 800.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts, payer="demo.platform.a", stmt="demo.stmt.a", box1a=800.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "none", Q9_FEES: None,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 0.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 0.0,
                Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts, "demo.f1099k.h1", closed=True)
        self._run_and_assert("26. omitted-platform-fee", acts, "demo.p26.omitted-fees")

    def test_path_27_withdrawn_amount(self) -> None:
        acts = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts, "demo.platform.a", "demo.stmt.a")
        acts.append(_act(len(acts), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 880.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts, payer="demo.platform.a", stmt="demo.stmt.a", box1a=880.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "platform-pass-through", Q9_FEES: 80.0,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 56.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 24.0,
                Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        acts.append(_act(len(acts), "finding-retracted", {"finding_id": "f.agreed-item-price.demo.stmt.a"}))
        _add_family_closure(acts, "demo.f1099k.h1", closed=True)
        self._run_and_assert("27. withdrawn-amount", acts, "demo.p27.withdrawn-amount")

    def test_path_28_cannot_tell_improvements(self) -> None:
        acts = self._single_statement_case(
            "demo.p28.cannot-tell-improvements", box1a=880.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "platform-pass-through", Q9_FEES: 80.0,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 56.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 24.0,
                Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "cannot-tell",
            },
        )
        self._run_and_assert("28. cannot-tell-improvements", acts, "demo.p28.cannot-tell-improvements")

    def test_path_29_boundary_case_1_seller_received_shipping_gain(self) -> None:
        acts = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts, "demo.platform.a", "demo.stmt.a")
        acts.append(_act(len(acts), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 900.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts, payer="demo.platform.a", stmt="demo.stmt.a", box1a=900.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "seller-received-shipping", Q9_FEES: 0.0,
                Q9_SELLER_SHIP: 20.0, Q10_TAX: 0.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 100.0,
                Q12_COST: 850.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts, "demo.f1099k.h1", closed=True)
        self._run_and_assert("29. boundary-case-1-seller-received-shipping-gain", acts, "demo.p29.boundary-1")

    def test_path_30_boundary_case_2_refund_loss(self) -> None:
        acts = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts, "demo.platform.a", "demo.stmt.a")
        acts.append(_act(len(acts), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 800.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts, payer="demo.platform.a", stmt="demo.stmt.a", box1a=800.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "none", Q9_FEES: 0.0,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 0.0, Q10_REFUND: 100.0, Q11_BUYER_SHIP: 0.0,
                Q12_COST: 750.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts, "demo.f1099k.h1", closed=True)
        self._run_and_assert("30. boundary-case-2-refund-loss", acts, "demo.p30.boundary-2")

    def test_path_31_boundary_case_3_none_shipping_seller_paid_loss(self) -> None:
        acts = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts, "demo.platform.a", "demo.stmt.a")
        acts.append(_act(len(acts), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 800.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts, payer="demo.platform.a", stmt="demo.stmt.a", box1a=800.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "none", Q9_FEES: 0.0,
                Q9_SELLER_SHIP: 100.0, Q10_TAX: 0.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 0.0,
                Q12_COST: 750.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts, "demo.f1099k.h1", closed=True)
        self._run_and_assert("31. boundary-case-3-none-shipping-seller-paid-loss", acts, "demo.p31.boundary-3")

    def test_path_32_boundary_case_4_pass_through_shipping_loss(self) -> None:
        acts = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts, "demo.platform.a", "demo.stmt.a")
        acts.append(_act(len(acts), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 900.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts, payer="demo.platform.a", stmt="demo.stmt.a", box1a=900.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "platform-pass-through", Q9_FEES: 0.0,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 0.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 100.0,
                Q12_COST: 850.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts, "demo.f1099k.h1", closed=True)
        self._run_and_assert("32. boundary-case-4-pass-through-shipping-loss", acts, "demo.p32.boundary-4")

    def test_path_33_boundary_case_5_pass_through_seller_paid_gain(self) -> None:
        acts = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts, "demo.platform.a", "demo.stmt.a")
        acts.append(_act(len(acts), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 900.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts, payer="demo.platform.a", stmt="demo.stmt.a", box1a=900.0, box4=0.0,
            answers={
                Q8_PRICE: 900.0, Q8_SHIP: "platform-pass-through", Q9_FEES: 0.0,
                Q9_SELLER_SHIP: 100.0, Q10_TAX: 0.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 0.0,
                Q12_COST: 850.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts, "demo.f1099k.h1", closed=True)
        self._run_and_assert("33. boundary-case-5-pass-through-seller-paid-gain", acts, "demo.p33.boundary-5")
