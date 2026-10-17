"""D2 Candidate Citizen Probe: build the candidate citizens in a temporary
surface and execute the 33 materially distinct disposition paths through
``live_coordinate_run`` and the real presentation model.

Nothing here is adopted; nothing is written into ``packages/content``.

The probe demonstrates:
1. Single comparison formula (D1 review finding 1):
   Amount Realized = Agreed Price + Buyer Shipping Received - Refunds Given Back
   Selling Expenses = Platform Fees + Seller-Paid Shipping Deducted
   Loss Condition = (Net Amount < Purchase Cost) and (improvements == 'no')
   Reconciliation = Agreed Price + Platform Tax + Buyer Shipping == Box 1a
2. Owner Decision (2026-10-16):
   - Form 1099-K completeness answer required only where Schedule 1 is determined.
   - Without completeness answer, Schedule 1 attachment blocks with BLOCK_ABSENT.
   - W-2-only return never evaluates Schedule 1 attachment; asked nothing.
   - Income and tax do not depend on Form 1099-K.
   - Unsupported / unresolved / excluded statement withholds Schedule 1 attachment
     and presents as unresolved condition with the required saved explanation:
     "Because this statement is unresolved, the return's income does not yet account for this Form 1099-K statement."
3. Track 0 adversarial closure across all 33 materially distinct paths.

Run from the repository root:
    python3 docs/phases/tax-circumstance-breadth/milestones/personal-item-sale-circumstances-evidence/d2_probe.py
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.derivation.production_resolver import PublicationSurface
from tests.test_form1099g_box1_schedule1_line7 import _act, _attested
from tests.test_f1098_mortgage_interest_line12e_track2 import _load_fixture_adoption
from tests.test_ssa1099_benefits_line6_track2 import _ssa_acts

CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
PACKAGE_PATH = CONTENT / "package.core-calculations.v45.json"
REGISTRY_PATH = CONTENT / "published-packages.v43.json"
RELEASE_DIR = ROOT / "packages" / "sample_data" / "student_loan_worksheet_integration" / "publication_surface" / "releases"
RELEASE_PATH = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v43.json"

USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}

FACT = "tax.us.2025.f1099k."
BOX1A = FACT + "box1a-gross-amount"
BOX4 = FACT + "box4-federal-withholding"
CLOSURE_TYPE = FACT + "source-closure"
FAMILY_ID = "tax.us.2025.f1099k"
ENTRY_SYMBOL = FACT + "statement-loss-entry"
REASON_SYMBOL = FACT + "statement-loss-reason"
TOP_ENTRY_SYMBOL = "tax.us.2025.schedule1.top-entry"
UNRESOLVED_SYMBOL = "tax.us.2025.f1099k.unresolved"
NOT_ASKED_PARAM = "tax.us.2025.parameter.f1099k-not-asked-default"
DEFAULT_ZERO_PARAM = "tax.us.2025.parameter.default-zero"
INERT_FACT = FACT + "inert-path-unwritten"

REASON_DESCRIPTIONS: dict[str, str] = {
    "supported-loss": "This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1.",
    "unsupported-gain": "The sale resulted in a gain or profit, which cannot be reported as a personal item loss on Schedule 1.",
    "break-even-sale": "The sale broke even with no gain or loss, so no adjustment is reported on Schedule 1.",
    "investment-purpose-excluded": "The item was acquired for investment or profit; personal item loss treatment does not apply.",
    "resale-inventory-excluded": "The item was acquired for resale or business inventory; personal item loss treatment does not apply.",
    "prior-depreciable-use-excluded": "The item was used for business or rental purposes; personal item loss treatment does not apply.",
    "digital-asset-excluded": "The transaction involved digital assets or virtual currency, which are outside the scope of this personal item sale route.",
    "multi-sale-statement-unsupported": "The Form 1099-K statement covers more than a single personal item sale.",
    "non-purchase-acquisition-unsupported": "The item was not acquired by purchase.",
    "basis-adjustment-unsupported": "Lasting improvements or other basis adjustments were made to the item.",
    "backup-withholding-unsupported": "Federal income tax was withheld (Box 4), which requires separate reporting.",
    "cost-basis-unknown": "The original purchase cost of the item is unknown.",
    "shipping-arrangement-unknown": "The shipping arrangement is unknown.",
    "buyer-payment-unknown": "The agreed item price is unknown.",
    "platform-tax-unknown": "The platform sales tax amount is unknown.",
    "buyer-shipping-unknown": "The buyer-paid shipping amount is unknown.",
    "refund-status-unknown": "The refund amount is unknown.",
    "platform-fees-unknown": "The platform selling fees amount is unknown.",
    "seller-shipping-unknown": "The seller-paid shipping amount is unknown.",
    "cannot-tell-improvements": "It is not known whether lasting improvements or other basis adjustments were made to the item.",
    "cannot-tell-asset-type": "It is not known whether the transaction involved digital assets or virtual currency.",
    "cannot-tell-use": "It is not known whether the item was used exclusively for personal purposes.",
    "cannot-tell-purpose": "It is not known whether the item was acquired for personal use.",
    "cannot-tell-acquisition": "It is not known whether the item was acquired by purchase.",
    "cannot-tell-sale-scope": "It is not known whether the statement covers only a single personal item sale.",
    "improvements-unanswered": "The question regarding lasting improvements has no current answer.",
    "cost-basis-unanswered": "The question regarding cost basis has no current answer.",
    "shipping-arrangement-unanswered": "The question regarding shipping arrangement has no current answer.",
    "agreed-price-unanswered": "The question regarding agreed item price has no current answer.",
    "platform-tax-unanswered": "The question regarding platform sales tax has no current answer.",
    "buyer-shipping-unanswered": "The question regarding buyer-paid shipping has no current answer.",
    "refund-status-unanswered": "The question regarding refunds given back has no current answer.",
    "platform-fees-unanswered": "The question regarding platform selling fees has no current answer.",
    "seller-shipping-unanswered": "The question regarding seller-paid shipping has no current answer.",
    "asset-type-unanswered": "The question regarding digital assets has no current answer.",
    "personal-use-unconfirmed": "The question regarding exclusive personal use has no current answer.",
    "purpose-unanswered": "The question regarding primary purpose at acquisition has no current answer.",
    "acquisition-type-unanswered": "The question regarding acquisition by purchase has no current answer.",
    "single-sale-unanswered": "The question regarding single item sale scope has no current answer.",
    "unexplained-reconciliation-discrepancy": "The reported Box 1a amount does not reconcile with the item price, sales tax, and shipping amounts.",
    "multiple-f1099k-out-of-scope": "More than one Form 1099-K statement was received; reporting personal item sale losses across multiple statements is outside the supported scope of this return.",
}

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

EXPLANATION_SENTENCE = (
    "Because this statement is unresolved, the return's income does not yet account for this Form 1099-K statement."
)


def _read_json(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text("utf-8")))


def _identity_keys() -> list[dict[str, Any]]:
    return [
        {"name": "payer", "kind": "entity", "entity_kind": "tax.us.1099k-platform"},
        {"name": "statement", "kind": "entity", "entity_kind": "tax.us.1099k-statement"},
        {"name": "tax-year", "kind": "literal", "values": ["2025"]},
    ]


def _f1099k_bundle() -> dict[str, Any]:
    return {
        "schema": "bundle.v2",
        "id": "tax.us.2025.f1099k.vocabulary",
        "version": "v1",
        "label": "Form 1099-K vocabulary for personal item sale loss reporting",
        "fact_types": [
            {
                "schema": "fact-type.v2",
                "id": BOX1A,
                "version": "v1",
                "title": "Form 1099-K box 1a gross payment amount",
                "nature": "determinable",
                "identity_keys": _identity_keys(),
                "value_schema": {"type": "number", "minimum": 0},
                "supersession": {"policy": "free"},
            },
            {
                "schema": "fact-type.v2",
                "id": BOX4,
                "version": "v1",
                "title": "Form 1099-K box 4 federal income tax withheld",
                "nature": "determinable",
                "identity_keys": _identity_keys(),
                "value_schema": {"type": "number", "minimum": 0},
                "optional_default": {"parameter": {"id": DEFAULT_ZERO_PARAM, "version": "v1"}},
                "supersession": {"policy": "free"},
            },
            {
                "schema": "fact-type.v2",
                "id": CLOSURE_TYPE,
                "version": "v1",
                "title": "Closure witness for Form 1099-K source family at a keyed horizon",
                "nature": "determinable",
                "identity_keys": [
                    {"name": "family-horizon", "kind": "entity", "entity_kind": "kernel.family-horizon"},
                    {"name": "tax-year", "kind": "literal", "values": ["2025"]},
                ],
                "value_schema": {"type": "boolean"},
                "supersession": {"policy": "free"},
            },
            {
                "schema": "fact-type.v2",
                "id": REASON_SYMBOL,
                "version": "v1",
                "title": "Categorical reason classification for Form 1099-K statement loss eligibility",
                "nature": "determinable",
                "identity_keys": _identity_keys(),
                "value_schema": {
                    "oneOf": [{"const": k, "description": v} for k, v in REASON_DESCRIPTIONS.items()]
                },
                "supersession": {"policy": "free"},
            },
            {
                "schema": "fact-type.v2",
                "id": UNRESOLVED_SYMBOL,
                "version": "v1",
                "title": "Unresolved condition sentinel for Form 1099-K personal item sale reporting",
                "nature": "determinable",
                "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
                "value_schema": {"type": "string", "enum": ["unresolved"]},
                "supersession": {"policy": "free"},
            },
            {
                "schema": "fact-type.v2",
                "id": INERT_FACT,
                "version": "v1",
                "title": "Named by the selection rule inert second path. Nothing writes it.",
                "nature": "determinable",
                "identity_keys": [{"name": "marker", "kind": "literal", "values": ["unused"]}],
                "value_schema": {"type": "string", "enum": ["unused"]},
                "supersession": {"policy": "free"},
            },
        ],
    }


def _f1099k_circumstances_bundle() -> dict[str, Any]:
    def _enum_ft(fact_id: str, title: str, values: list[str]) -> dict[str, Any]:
        return {
            "schema": "fact-type.v2",
            "id": fact_id,
            "version": "v1",
            "title": title,
            "nature": "determinable",
            "identity_keys": _identity_keys(),
            "value_schema": {"enum": values},
            "optional_default": {"parameter": {"id": NOT_ASKED_PARAM, "version": "v1"}},
            "supersession": {"policy": "free"},
        }

    def _num_ft(fact_id: str, title: str) -> dict[str, Any]:
        return {
            "schema": "fact-type.v2",
            "id": fact_id,
            "version": "v1",
            "title": title,
            "nature": "determinable",
            "identity_keys": _identity_keys(),
            "value_schema": {
                "oneOf": [
                    {"type": "number", "minimum": 0},
                    {"type": "string", "enum": ["cannot-tell", "not-asked"]},
                ]
            },
            "optional_default": {"parameter": {"id": NOT_ASKED_PARAM, "version": "v1"}},
            "supersession": {"policy": "free"},
        }

    return {
        "schema": "bundle.v2",
        "id": "tax.us.2025.f1099k-circumstances.vocabulary",
        "version": "v1",
        "label": "Form 1099-K circumstances vocabulary for personal item sale loss reporting",
        "fact_types": [
            _enum_ft(Q1, "Q1: Covers only a single personal item sale", ["yes", "no", "cannot-tell", "not-asked"]),
            _enum_ft(Q3, "Q3: Acquired by purchase", ["yes", "no", "cannot-tell", "not-asked"]),
            _enum_ft(Q4, "Q4: Primary purpose at acquisition", ["personal-use", "investment-or-profit", "resale-or-inventory", "cannot-tell", "not-asked"]),
            _enum_ft(Q5, "Q5: Used exclusively for personal purposes", ["yes", "no", "cannot-tell", "not-asked"]),
            _enum_ft(Q7, "Q7: Digital asset or virtual currency involvement", ["no", "yes", "cannot-tell", "not-asked"]),
            _num_ft(Q8_PRICE, "Q8: Agreed item price"),
            _enum_ft(Q8_SHIP, "Q8: Shipping arrangement", ["platform-pass-through", "seller-received-shipping", "none", "cannot-tell", "not-asked"]),
            _num_ft(Q9_FEES, "Q9: Platform selling fees"),
            _num_ft(Q9_SELLER_SHIP, "Q9: Seller-paid shipping amount"),
            _num_ft(Q10_TAX, "Q10: Sales tax collected by platform"),
            _num_ft(Q10_REFUND, "Q10: Refund amount given back by seller"),
            _num_ft(Q11_BUYER_SHIP, "Q11: Buyer-paid shipping amount"),
            _num_ft(Q12_COST, "Q12: Original purchase cost"),
            _enum_ft(Q12_GATE, "Q12: Cost basis known gate", ["yes", "cannot-tell", "not-asked"]),
            _enum_ft(Q13, "Q13: Lasting improvements or adjustments", ["no", "yes", "cannot-tell", "not-asked"]),
        ],
    }


def _not_asked_parameter() -> dict[str, Any]:
    return {
        "schema": "parameter-declaration.v1",
        "id": NOT_ASKED_PARAM,
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax", "effective_from": "2025-01-01"},
        "values": "not-asked",
    }


def _family_declaration() -> dict[str, Any]:
    return {
        "schema": "source-family.v1",
        "id": FAMILY_ID,
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "title": "Form 1099-K box 1a gross payment amount statement items, tax year 2025",
        "authorizes_subtotal": TOP_ENTRY_SYMBOL,
        "member_predicate": {"fact_type": BOX1A},
        "closure_claim": (
            "Every personal item sale amount reported in box 1a of a Form 1099-K furnished to the taxpayer "
            "for tax year 2025 is recorded as a statement item as of the keyed horizon. Closed with members authorizes "
            "one statement's Box 1a; closed-empty authorizes subtotal 0. Does not authorize a multi-payer sum."
        ),
    }


def _closure_mapping() -> dict[str, Any]:
    return {
        "schema": "source-closure-mapping.v2",
        "id": "tax.us.2025.closure-mapping.f1099k",
        "version": "v1",
        "family": {"id": FAMILY_ID, "version": "v1"},
        "member_fact_type": {"id": BOX1A, "version": "v1"},
        "closure_fact_type": {"id": CLOSURE_TYPE, "version": "v1"},
        "closure_horizon_key": "family-horizon",
        "admits_symbol": TOP_ENTRY_SYMBOL,
        "admission": {"condition": "current-literal-true"},
    }


def _ref(name: str) -> dict[str, Any]:
    return {"op": "ref", "name": name}


def _cat_eq(name: str, value: str) -> dict[str, Any]:
    return {
        "op": "categorical_compare",
        "cmp": "eq",
        "left": _ref(name),
        "right": {"op": "category_literal", "fact_type": {"id": name, "version": "v1"}, "value": value},
    }


def _block(code: str) -> dict[str, Any]:
    return {"op": "block", "code": code}


def _choose(when: dict[str, Any], then: Any, otherwise: Any) -> dict[str, Any]:
    return {"op": "choose", "when": when, "then": then, "else": otherwise}


def _reason_cat(val: str) -> dict[str, Any]:
    return {
        "op": "category_literal",
        "fact_type": {"id": REASON_SYMBOL, "version": "v1"},
        "value": val,
    }


def _statement_loss_reason_value_tree() -> dict[str, Any]:
    expected_box1a = {"op": "add", "args": [_ref(Q8_PRICE), _ref(Q10_TAX), _ref(Q11_BUYER_SHIP)]}
    reconciliation_mismatch = {"op": "compare", "cmp": "ne", "left": _ref(BOX1A), "right": expected_box1a}

    buyer_shipping_received = _choose(_cat_eq(Q8_SHIP, "seller-received-shipping"), _ref(Q11_BUYER_SHIP), 0)
    gross_realized = {"op": "add", "args": [_ref(Q8_PRICE), buyer_shipping_received]}
    amount_realized = {"op": "subtract", "left": gross_realized, "right": _ref(Q10_REFUND)}
    seller_shipping_deducted = _choose(
        {"op": "any", "args": [_cat_eq(Q8_SHIP, "seller-received-shipping"), _cat_eq(Q8_SHIP, "none")]},
        _ref(Q9_SELLER_SHIP),
        0,
    )
    selling_expenses = {"op": "add", "args": [_ref(Q9_FEES), seller_shipping_deducted]}
    net_amount = {"op": "subtract", "left": amount_realized, "right": selling_expenses}

    is_gain = {"op": "compare", "cmp": "gt", "left": net_amount, "right": _ref(Q12_COST)}
    is_breakeven = {"op": "compare", "cmp": "eq", "left": net_amount, "right": _ref(Q12_COST)}

    tail = _choose(
        is_gain,
        _reason_cat("unsupported-gain"),
        _choose(is_breakeven, _reason_cat("break-even-sale"), _reason_cat("supported-loss")),
    )

    tail = _choose(reconciliation_mismatch, _reason_cat("unexplained-reconciliation-discrepancy"), tail)
    tail = _choose({"op": "compare", "cmp": "gt", "left": _ref(BOX4), "right": 0}, _reason_cat("backup-withholding-unsupported"), tail)
    tail = _choose(_cat_eq(Q13, "yes"), _reason_cat("basis-adjustment-unsupported"), tail)
    tail = _choose(_cat_eq(Q7, "yes"), _reason_cat("digital-asset-excluded"), tail)
    tail = _choose(_cat_eq(Q5, "no"), _reason_cat("prior-depreciable-use-excluded"), tail)
    tail = _choose(_cat_eq(Q4, "resale-or-inventory"), _reason_cat("resale-inventory-excluded"), tail)
    tail = _choose(_cat_eq(Q4, "investment-or-profit"), _reason_cat("investment-purpose-excluded"), tail)
    tail = _choose(_cat_eq(Q3, "no"), _reason_cat("non-purchase-acquisition-unsupported"), tail)
    tail = _choose(_cat_eq(Q1, "no"), _reason_cat("multi-sale-statement-unsupported"), tail)

    tail = _choose(_cat_eq(Q13, "cannot-tell"), _reason_cat("cannot-tell-improvements"), tail)
    tail = _choose(_cat_eq(Q12_GATE, "cannot-tell"), _reason_cat("cost-basis-unknown"), tail)
    tail = _choose(_cat_eq(Q12_COST, "cannot-tell"), _reason_cat("cost-basis-unknown"), tail)
    tail = _choose(_cat_eq(Q9_SELLER_SHIP, "cannot-tell"), _reason_cat("seller-shipping-unknown"), tail)
    tail = _choose(_cat_eq(Q9_FEES, "cannot-tell"), _reason_cat("platform-fees-unknown"), tail)
    tail = _choose(_cat_eq(Q8_SHIP, "cannot-tell"), _reason_cat("shipping-arrangement-unknown"), tail)
    tail = _choose(_cat_eq(Q10_REFUND, "cannot-tell"), _reason_cat("refund-status-unknown"), tail)
    tail = _choose(_cat_eq(Q11_BUYER_SHIP, "cannot-tell"), _reason_cat("buyer-shipping-unknown"), tail)
    tail = _choose(_cat_eq(Q10_TAX, "cannot-tell"), _reason_cat("platform-tax-unknown"), tail)
    tail = _choose(_cat_eq(Q8_PRICE, "cannot-tell"), _reason_cat("buyer-payment-unknown"), tail)
    tail = _choose(_cat_eq(Q7, "cannot-tell"), _reason_cat("cannot-tell-asset-type"), tail)
    tail = _choose(_cat_eq(Q5, "cannot-tell"), _reason_cat("cannot-tell-use"), tail)
    tail = _choose(_cat_eq(Q4, "cannot-tell"), _reason_cat("cannot-tell-purpose"), tail)
    tail = _choose(_cat_eq(Q3, "cannot-tell"), _reason_cat("cannot-tell-acquisition"), tail)
    tail = _choose(_cat_eq(Q1, "cannot-tell"), _reason_cat("cannot-tell-sale-scope"), tail)

    tail = _choose(_cat_eq(Q13, "not-asked"), _reason_cat("improvements-unanswered"), tail)
    tail = _choose(_cat_eq(Q12_GATE, "not-asked"), _reason_cat("cost-basis-unanswered"), tail)
    tail = _choose(_cat_eq(Q12_COST, "not-asked"), _reason_cat("cost-basis-unanswered"), tail)
    tail = _choose(_cat_eq(Q9_SELLER_SHIP, "not-asked"), _reason_cat("seller-shipping-unanswered"), tail)
    tail = _choose(_cat_eq(Q9_FEES, "not-asked"), _reason_cat("platform-fees-unanswered"), tail)
    tail = _choose(_cat_eq(Q8_SHIP, "not-asked"), _reason_cat("shipping-arrangement-unanswered"), tail)
    tail = _choose(_cat_eq(Q10_REFUND, "not-asked"), _reason_cat("refund-status-unanswered"), tail)
    tail = _choose(_cat_eq(Q11_BUYER_SHIP, "not-asked"), _reason_cat("buyer-shipping-unanswered"), tail)
    tail = _choose(_cat_eq(Q10_TAX, "not-asked"), _reason_cat("platform-tax-unanswered"), tail)
    tail = _choose(_cat_eq(Q8_PRICE, "not-asked"), _reason_cat("agreed-price-unanswered"), tail)
    tail = _choose(_cat_eq(Q7, "not-asked"), _reason_cat("asset-type-unanswered"), tail)
    tail = _choose(_cat_eq(Q5, "not-asked"), _reason_cat("personal-use-unconfirmed"), tail)
    tail = _choose(_cat_eq(Q4, "not-asked"), _reason_cat("purpose-unanswered"), tail)
    tail = _choose(_cat_eq(Q3, "not-asked"), _reason_cat("acquisition-type-unanswered"), tail)
    tail = _choose(_cat_eq(Q1, "not-asked"), _reason_cat("single-sale-unanswered"), tail)

    tail = _choose(
        {"op": "compare", "cmp": "gt", "left": {"op": "shared_key_count", "fact_type": BOX1A, "key": "tax-year"}, "right": 1},
        _reason_cat("multiple-f1099k-out-of-scope"),
        tail,
    )

    return tail


def _statement_loss_reason_rule() -> dict[str, Any]:
    requires = [
        BOX1A, BOX4, Q1, Q3, Q4, Q5, Q7, Q8_PRICE, Q8_SHIP,
        Q9_FEES, Q9_SELLER_SHIP, Q10_TAX, Q10_REFUND, Q11_BUYER_SHIP,
        Q12_COST, Q12_GATE, Q13,
    ]
    return {
        "schema": "rule-artifact.v14",
        "id": "tax.us.2025.rule.f1099k-statement-loss-reason",
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation",
        "subject": {"id": BOX1A, "version": "v1"},
        "requires": requires,
        "pins": [],
        "when": True,
        "value": _statement_loss_reason_value_tree(),
        "publishes": REASON_SYMBOL,
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "citations": [],
        "notes": "Classifies the categorical eligibility reason for a Form 1099-K statement subject.",
    }


def _schedule1_top_entry_rule() -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v14",
        "id": "tax.us.2025.rule.schedule1-top-entry",
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation",
        "requires": [],
        "pins": [],
        "when": {
            "op": "all",
            "args": [
                {"op": "require_closed", "source_set": FAMILY_ID},
                {
                    "op": "choose",
                    "when": {
                        "op": "compare",
                        "cmp": "gt",
                        "left": {"op": "count", "name": BOX1A, "source_set": FAMILY_ID},
                        "right": 1,
                    },
                    "then": {"op": "block", "code": "MULTIPLE_F1099K_OUT_OF_SCOPE"},
                    "else": True,
                },
            ],
        },
        "value": {
            "op": "choose",
            "when": {
                "op": "compare",
                "cmp": "eq",
                "left": {"op": "count", "name": BOX1A, "source_set": FAMILY_ID},
                "right": 0,
            },
            "then": 0,
            "else": {
                "op": "choose",
                "when": {
                    "op": "collect_categorical_all_equal",
                    "name": REASON_SYMBOL,
                    "value": {
                        "op": "category_literal",
                        "fact_type": {"id": REASON_SYMBOL, "version": "v1"},
                        "value": "supported-loss",
                    },
                },
                "then": {"op": "add", "args": [{"op": "collect", "name": BOX1A, "source_set": FAMILY_ID}]},
                "else": {"op": "block", "code": "DEPENDENCY_ABSENT"},
            },
        },
        "publishes": TOP_ENTRY_SYMBOL,
        "blocked": {"code": "BLOCK_CLOSURE", "missing": [FAMILY_ID]},
        "citations": [],
        "notes": "Selects Form 1099-K loss entries into Schedule 1 top entry.",
    }


def _unresolved_rule() -> dict[str, Any]:
    active_path = {
        "id": "statement",
        "activity": {
            "kind": "source_nonempty",
            "source_family": {"id": FAMILY_ID, "version": "v1"},
            "member_fact_types": [{"id": BOX1A, "version": "v1"}],
        },
        "reads_subject_results": [{"symbol": REASON_SYMBOL, "subject": {"id": BOX1A, "version": "v1"}}],
        "requires": [],
        "pins": [],
        "when": {
            "op": "choose",
            "when": {
                "op": "compare",
                "cmp": "gt",
                "left": {"op": "count", "name": BOX1A, "source_set": FAMILY_ID},
                "right": 1,
            },
            "then": True,
            "else": {
                "op": "not",
                "value": {
                    "op": "collect_categorical_all_equal",
                    "name": REASON_SYMBOL,
                    "value": {
                        "op": "category_literal",
                        "fact_type": {"id": REASON_SYMBOL, "version": "v1"},
                        "value": "supported-loss",
                    },
                },
            },
        },
        "value": {"op": "block", "code": "DEPENDENCY_ABSENT"},
    }
    inert_path = {
        "id": "inert",
        "activity": {
            "kind": "source_nonempty",
            "member_fact_types": [{"id": INERT_FACT, "version": "v1"}],
        },
        "reads_subject_results": [],
        "requires": [],
        "pins": [],
        "when": True,
        "value": {"op": "block", "code": "DEPENDENCY_ABSENT"},
    }
    default_path = {
        "id": "neither",
        "reads_subject_results": [],
        "requires": [],
        "pins": [],
        "when": False,
        "value": False,
    }
    return {
        "schema": "rule-artifact.v14",
        "id": "tax.us.2025.rule.f1099k-unresolved",
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation",
        "requires": [],
        "pins": [],
        "when": True,
        "selection": {
            "mode": "exclusive_presence",
            "conflict": "refuse",
            "paths": [active_path, inert_path],
            "default": default_path,
            "refusal": {"code": "DEPENDENCY_INVALID", "missing": ["f1099k-unresolved-conflict"], "pins": []},
        },
        "publishes": UNRESOLVED_SYMBOL,
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "citations": [],
        "notes": "Blocks when any Form 1099-K statement is unresolved or unsupported.",
    }


def _attachment_rule_v3() -> dict[str, Any]:
    v2 = _read_json(CONTENT / "rule.attachment.schedule-1.v2.json")
    v3 = copy.deepcopy(v2)
    v3["version"] = "v3"
    v3["requirement"]["subtotals"].append(TOP_ENTRY_SYMBOL)
    v3["itemizations"].append({
        "authority": {"kind": "single_family", "source_family": {"id": FAMILY_ID, "version": "v1"}},
        "label": "Schedule 1 top entry: Form 1099-K personal item sale loss gross payment amount",
        "part_id": "sch1-top-entry-f1099k",
        "row_sets": [
            {
                "rows": {
                    "member_fact_type": {"id": BOX1A, "version": "v1"},
                    "op": "collect_members",
                    "source_family": {"id": FAMILY_ID, "version": "v1"},
                },
                "subtotal_symbol": TOP_ENTRY_SYMBOL,
            }
        ],
        "tie_out": {"line_symbol": TOP_ENTRY_SYMBOL},
    })
    return v3


def _top_entry_field() -> dict[str, Any]:
    return {
        "schema": "form-field.v3",
        "id": "tax.us.2025.schedule1.top-entry.form-field",
        "version": "v1",
        "form": {"authority": "IRS", "form_id": "1040-SCH-1", "jurisdiction": "US-federal", "tax_year": 2025},
        "line": "sch1-top",
        "label": "Form 1099-K personal item sale loss gross payment amount (Schedule 1 top entry)",
        "description": "Entered above Part I line 1 when personal items were sold at a loss.",
        "binds_symbol": TOP_ENTRY_SYMBOL,
        "dispositions": {
            "published_value": {"explain": "This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1.", "render": "{value}"},
            "computed_zero": {"explain": "No personal item sale loss entry.", "render": "{value}"},
            "closure_backed_zero": {"explain": "No Form 1099-K statements were received for 2025.", "render": "{value}"},
            "blocked": {"codes": ["DEPENDENCY_ABSENT", "DEPENDENCY_INVALID", "SOURCE_SET_UNCLOSED"], "explain": "Form 1099-K loss entry cannot be computed.", "render": ""},
            "guard_inapplicable": {"explain": "Not evaluated.", "render": ""},
        },
    }


def _unresolved_field() -> dict[str, Any]:
    return {
        "schema": "form-field.v3",
        "id": "tax.us.2025.form.f1099k.unresolved.form-field",
        "version": "v1",
        "form": {"authority": "IRS", "form_id": "1040-SCH-1", "jurisdiction": "US-federal", "tax_year": 2025},
        "line": "f1099k-unresolved",
        "label": "Unresolved Form 1099-K condition",
        "description": "Indicates an open condition or unsupported statement on Form 1099-K.",
        "binds_symbol": UNRESOLVED_SYMBOL,
        "dispositions": {
            "blocked": {"codes": ["DEPENDENCY_ABSENT", "DEPENDENCY_INVALID"], "explain": EXPLANATION_SENTENCE, "render": ""},
            "guard_inapplicable": {"explain": "No open condition: statements resolved or no statement received.", "render": ""},
            "published_value": {"explain": "Not used.", "render": ""},
            "computed_zero": {"explain": "Not used.", "render": ""},
            "closure_backed_zero": {"explain": "Not used.", "render": ""},
        },
    }


def _write_member(member_dir: Path, name: str, citizen: dict[str, Any]) -> tuple[str, str]:
    path = member_dir / name
    path.write_text(json.dumps(citizen, indent=2) + "\n", encoding="utf-8")
    stored = _read_json(path)
    return citizen["id"], citizen_checksum(stored)


def _build_surface(root: Path) -> tuple[PublicationSurface, str, str, str, str]:
    member_dir = root / "members"
    member_dir.mkdir()
    old_attachment_file = "rule.attachment.schedule-1.v2.json"
    for source in sorted(CONTENT.rglob("*.json")):
        if source.name == old_attachment_file:
            continue
        dest = member_dir / source.relative_to(CONTENT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(source.read_bytes())

    registry = _read_json(REGISTRY_PATH)
    new_checksums: list[tuple[str, str, str]] = []

    b1_id, b1_sum = _write_member(member_dir, "f1099k.bundle.json", _f1099k_bundle())
    new_checksums.append((b1_id, "v1", b1_sum))

    b2_id, b2_sum = _write_member(member_dir, "f1099k-circumstances.bundle.json", _f1099k_circumstances_bundle())
    new_checksums.append((b2_id, "v1", b2_sum))

    p_id, p_sum = _write_member(member_dir, "parameter.f1099k-not-asked-default.json", _not_asked_parameter())
    new_checksums.append((p_id, "v1", p_sum))

    fam_id, fam_sum = _write_member(member_dir, "family.f1099k.json", _family_declaration())
    new_checksums.append((fam_id, "v1", fam_sum))

    map_id, map_sum = _write_member(member_dir, "closure-mapping.f1099k.json", _closure_mapping())
    new_checksums.append((map_id, "v1", map_sum))

    r1_id, r1_sum = _write_member(member_dir, "rule.f1099k-statement-loss-reason.probe.json", _statement_loss_reason_rule())
    new_checksums.append((r1_id, "v1", r1_sum))

    r2_id, r2_sum = _write_member(member_dir, "rule.schedule1-top-entry.probe.json", _schedule1_top_entry_rule())
    new_checksums.append((r2_id, "v1", r2_sum))

    r3_id, r3_sum = _write_member(member_dir, "rule.f1099k-unresolved.probe.json", _unresolved_rule())
    new_checksums.append((r3_id, "v1", r3_sum))

    att_id, att_sum = _write_member(member_dir, "rule.attachment.schedule-1.v3.json", _attachment_rule_v3())
    new_checksums.append((att_id, "v3", att_sum))

    f1_id, f1_sum = _write_member(member_dir, "form-field.schedule1-top-entry.probe.json", _top_entry_field())
    new_checksums.append((f1_id, "v1", f1_sum))

    f2_id, f2_sum = _write_member(member_dir, "form-field.f1099k-unresolved.probe.json", _unresolved_field())
    new_checksums.append((f2_id, "v1", f2_sum))

    for cid, version, checksum in new_checksums:
        registry["citizens"].append({"id": cid, "version": version, "checksum": checksum})

    package = _read_json(PACKAGE_PATH)
    package["schema"] = "artifact-package.v36"
    if "rule-artifact.v14" not in package.get("admitted_schemas", []):
        package.setdefault("admitted_schemas", []).append("rule-artifact.v14")

    package["version"] = "v46"

    for fact_id in CIRCUMSTANCE_FACTS:
        package.setdefault("input_bindings", []).append({
            "fact_type": {"id": fact_id, "version": "v1"},
            "mode": "optional_default",
            "symbol": fact_id,
        })
    package.setdefault("input_bindings", []).append({
        "fact_type": {"id": BOX4, "version": "v1"},
        "mode": "optional_default",
        "symbol": BOX4,
    })

    package["members"] = [m for m in package["members"] if m["id"] != "tax.us.2025.rule.attachment.schedule-1"]
    package["entrypoints"] = [e for e in package["entrypoints"] if e["id"] != "tax.us.2025.rule.attachment.schedule-1"]

    package["entrypoints"].append({"id": att_id, "version": "v3"})
    package["entrypoints"].append({"id": r1_id, "version": "v1"})
    package["entrypoints"].append({"id": r2_id, "version": "v1"})
    package["entrypoints"].append({"id": r3_id, "version": "v1"})
    package["entrypoints"].append({"id": f1_id, "version": "v1"})
    package["entrypoints"].append({"id": f2_id, "version": "v1"})

    package["members"].append({"id": b1_id, "role": "fact-type-bundle", "schema": "bundle.v2", "version": "v1"})
    package["members"].append({"id": b2_id, "role": "fact-type-bundle", "schema": "bundle.v2", "version": "v1"})
    package["members"].append({"id": p_id, "role": "parameter", "schema": "parameter-declaration.v1", "version": "v1"})
    package["members"].append({"id": fam_id, "role": "source-family", "schema": "source-family.v1", "version": "v1"})
    package["members"].append({"id": map_id, "role": "source-closure-mapping", "schema": "source-closure-mapping.v2", "version": "v1"})
    package["members"].append({"id": r1_id, "role": "computation", "schema": "rule-artifact.v14", "version": "v1"})
    package["members"].append({"id": r2_id, "role": "computation", "schema": "rule-artifact.v14", "version": "v1"})
    package["members"].append({"id": r3_id, "role": "computation", "schema": "rule-artifact.v14", "version": "v1"})
    package["members"].append({"id": att_id, "role": "attachment-rule", "schema": "attachment-rule.v4", "version": "v3"})
    package["members"].append({"id": f1_id, "role": "form-field", "schema": "form-field.v3", "version": "v1"})
    package["members"].append({"id": f2_id, "role": "form-field", "schema": "form-field.v3", "version": "v1"})

    package_path = member_dir / "package.core-calculations.v46.json"
    package_path.write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    stored_package = _read_json(package_path)
    package_checksum = package_instance_checksum(stored_package)
    package["package_checksum"] = package_checksum
    package_path.write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")

    registry.setdefault("packages", [])
    registry["packages"].append({"id": package["id"], "version": "v46", "checksum": package_checksum})
    registry_path = root / "published-packages.probe.json"
    registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")

    release = _read_json(RELEASE_PATH)
    release["version"] = "v44"
    release_dir = root / "releases"
    release_dir.mkdir()
    release_path = release_dir / "demo.release.sli-worksheet-integration.2025.v44.json"
    release["package_registry_sha256"] = hashlib.sha256(registry_path.read_bytes()).hexdigest()
    release_path.write_text(json.dumps(release, indent=2) + "\n", encoding="utf-8")
    release_checksum = hashlib.sha256(release_path.read_bytes()).hexdigest()

    return (
        PublicationSurface(release_dir, registry_path, member_dir),
        release_checksum,
        package["id"],
        "v46",
        package_checksum,
    )


def _statement_fact_id(fact_type: str, payer: str = "demo.platform.a", stmt: str = "demo.stmt.a") -> str:
    return f"{fact_type}|payer={payer},statement={stmt},tax-year=2025"


def _finish_acts(
    acts: list[dict[str, object]],
    *,
    release_checksum: str,
    package_id: str,
    package_version: str,
    package_checksum: str,
    release_version: str = "v44",
) -> list[dict[str, object]]:
    built = copy.deepcopy(acts)
    adoption = copy.deepcopy(_load_fixture_adoption())
    adoption["act_id"] = f"demo.f1099k.adopt.{len(built):03d}"
    adoption["committed_against"] = len(built)
    payload = adoption["payload"]
    assert isinstance(payload, dict)
    payload["package"] = {"id": package_id, "version": package_version, "checksum": package_checksum}
    payload["release"] = {"id": "demo.release.sli-worksheet-integration.2025", "version": release_version, "checksum": release_checksum}
    payload["audit"] = {"note": "synthetic D2 candidate citizen probe; throwaway surface, not adopted content"}
    built.append(adoption)
    for index, row in enumerate(built):
        row["committed_against"] = index
        row["actor"] = USER
    return built


def _run_probe(acts: list[dict[str, object]], run_id: str, surface: PublicationSurface) -> dict[str, Any]:
    started = time.monotonic()
    with TemporaryDirectory() as tmp:
        try:
            result = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "workspace"),
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id=run_id,
                governance_pins=[],
                surface=surface,
                output_name="out.json",
            )
        except Exception as exc:
            return {
                "run_id": run_id,
                "seconds": round(time.monotonic() - started, 2),
                "exception": {"type": type(exc).__name__, "message": str(exc)},
            }

        elapsed = round(time.monotonic() - started, 2)
        if result.refusal is not None:
            return {
                "run_id": run_id,
                "seconds": elapsed,
                "refusal": {
                    "reason": result.refusal.reason,
                    "detail": result.refusal.detail,
                    "issues": [dict(i) for i in result.refusal.issues],
                },
            }

        assert result.output_path is not None and result.presentation_path is not None
        report = json.loads(result.output_path.read_text("utf-8"))
        model = json.loads(result.presentation_path.read_text("utf-8"))

        publications = [copy.deepcopy(p.finding) for p in (result.publications or ())]
        top_entry_pubs = [p for p in publications if p.get("symbol") == TOP_ENTRY_SYMBOL]
        loss_reason_pubs = [p for p in publications if p.get("symbol", "").startswith(REASON_SYMBOL)]

        dispositions = report.get("dispositions", [])
        top_entry_disps = [d for d in dispositions if d.get("symbol") == TOP_ENTRY_SYMBOL or "schedule1-top-entry" in str(d.get("artifact_id", ""))]
        sch1_att_disps = [d for d in dispositions if "attachment.schedule-1" in str(d.get("artifact_id", ""))]
        unresolved_disps = [d for d in dispositions if "f1099k-unresolved" in str(d.get("artifact_id", ""))]
        statement_loss_disps = [d for d in dispositions if "f1099k-statement-loss-reason" in str(d.get("artifact_id", ""))]

        sections = model.get("sections", [])
        top_entry_field = next((s for s in sections if (s.get("field") or {}).get("id") == "tax.us.2025.schedule1.top-entry.form-field"), None)
        unresolved_field = next((s for s in sections if (s.get("field") or {}).get("id") == "tax.us.2025.form.f1099k.unresolved.form-field"), None)
        line8_field = next((s for s in sections if s.get("id") == "line-8"), None)
        line9_field = next((s for s in sections if s.get("id") == "line-9"), None)

        line8_val = (line8_field or {}).get("resolved", {}).get("value")
        line9_val = (line9_field or {}).get("resolved", {}).get("value")

        top_disp = ((top_entry_field or {}).get("resolved") or {}).get("disposition")
        if top_disp == "published_value":
            top_entry_explain = ((top_entry_field or {}).get("field") or {}).get("dispositions", {}).get("published_value", {}).get("explain", "")
        else:
            top_entry_explain = ((top_entry_field or {}).get("field") or {}).get("dispositions", {}).get("blocked", {}).get("explain", "")
        unres_field_dict = (unresolved_field or {}).get("field") or {}
        unresolved_explain = unres_field_dict.get("dispositions", {}).get("blocked", {}).get("explain", "")
        unresolved_resolved = (unresolved_field or {}).get("resolved") or {}
        unresolved_reasons = [r["sentence"] for r in unresolved_resolved.get("reasons", [])]

        return {
            "run_id": run_id,
            "seconds": elapsed,
            "publications": publications,
            "top_entry_publications": top_entry_pubs,
            "loss_reason_publications": loss_reason_pubs,
            "top_entry_dispositions": top_entry_disps,
            "statement_loss_dispositions": statement_loss_disps,
            "schedule1_attachment_dispositions": sch1_att_disps,
            "unresolved_dispositions": unresolved_disps,
            "top_entry_field_resolved": (top_entry_field or {}).get("resolved"),
            "unresolved_field_resolved": unresolved_resolved,
            "top_entry_explain": top_entry_explain,
            "unresolved_explain": unresolved_explain,
            "unresolved_reasons": unresolved_reasons,
            "line8_value": line8_val,
            "line9_value": line9_val,
            "presentation_rows_count": len(sections),
        }


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

    add("bundle-adoption", {"bundle": _f1099k_bundle()})
    add("bundle-adoption", {"bundle": _f1099k_circumstances_bundle()})

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
    closure_fact_id = f"{CLOSURE_TYPE}|family-horizon={horizon},tax-year=2025"
    acts.append(_act(len(acts), "assertion", {"finding": _attested(f"f.close.{horizon}", closure_fact_id, closed)}))


def measure_neighbor_baselines(surface: PublicationSurface, rel_sum: str, pkg_id: str, pkg_ver: str, pkg_sum: str) -> dict[str, Any]:
    print("\n" + "=" * 85)
    print("Baseline Comparison for Neighbor Returns (Unmodified Release v43 vs Candidate v44/v46)")
    print("=" * 85)

    from tests.test_f1098e_student_loan_interest_agi_track6 import (
        _load as _load_sli,
        _f1098e_acts,
        Statement,
        SLI_SCOPE_UNIVERSAL_TOKENS,
        SLI_SCOPE_LEGAL_ZERO_TOKENS,
        SCHED1_LINE_TOKENS,
    )

    base_surf = PublicationSurface(RELEASE_DIR, REGISTRY_PATH, CONTENT)
    rel_base_sum = hashlib.sha256(RELEASE_PATH.read_bytes()).hexdigest()
    pkg_base = json.loads(PACKAGE_PATH.read_text("utf-8"))
    pkg_base_sum = pkg_base["package_checksum"]

    def run_base(acts: list[dict[str, object]], run_id: str) -> dict[str, Any]:
        finished = _finish_acts(
            acts,
            release_checksum=rel_base_sum,
            package_id=pkg_base["id"],
            package_version=pkg_base["version"],
            package_checksum=pkg_base_sum,
            release_version="v43",
        )
        return _run_probe(finished, run_id, surface=base_surf)

    # 1. W-2 only return
    w2_acts = _ssa_acts(wages=90000.0, benefits=[])
    w2_acts.pop()
    res_w2_base = run_base(w2_acts, "demo.w2.baseline")
    res_w2_cand = _run_probe(
        _finish_acts(w2_acts, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
        "demo.w2.candidate", surface=surface,
    )

    # 2. Unemployment return ($500.00 unemployment)
    unemp_base_acts = _ssa_acts(wages=90000.0, benefits=[], unemployment=500.0)
    unemp_base_acts.pop()
    unemp_base_acts.append(_act(len(unemp_base_acts), "bundle-adoption", {"bundle": _load_sli("f1098e.bundle.json")}))
    unemp_base_acts.append(_act(len(unemp_base_acts), "bundle-adoption", {"bundle": _load_sli("sli-scope.bundle.json")}))
    unemp_base_acts.append(_act(len(unemp_base_acts), "bundle-adoption", {"bundle": _load_sli("schedule1-adjustments-scope.bundle.json")}))
    unemp_base_acts.append(_act(len(unemp_base_acts), "horizon-genesis", {"family": {"id": "tax.us.2025.f1098e.1", "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1098e.h0"}))
    unemp_base_acts.append(_act(len(unemp_base_acts), "assertion", {"finding": _attested("demo.f1098e.closure", "tax.us.2025.f1098e.1.source-closure|family-horizon=demo.f1098e.h0,tax-year=2025", True)}))
    for tok in SLI_SCOPE_UNIVERSAL_TOKENS + SLI_SCOPE_LEGAL_ZERO_TOKENS:
        unemp_base_acts.append(_act(len(unemp_base_acts), "assertion", {"finding": _attested(f"demo.sli-scope.{tok}", f"tax.us.2025.sli-scope.{tok}|tax-year=2025", "yes")}))
    for tok in SCHED1_LINE_TOKENS:
        unemp_base_acts.append(_act(len(unemp_base_acts), "assertion", {"finding": _attested(f"demo.sched1-scope.{tok}", f"tax.us.2025.schedule1-adjustments-scope.{tok}|tax-year=2025", "yes")}))
    res_unemp_base = run_base(unemp_base_acts, "demo.unemp.baseline")

    unemp_cand_acts_with = _make_base_acts(wages=90000.0, unemployment=500.0)
    unemp_cand_acts_with.append(_act(len(unemp_cand_acts_with), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
    _add_family_closure(unemp_cand_acts_with, "demo.f1099k.h0", closed=True)
    res_unemp_cand_with = _run_probe(
        _finish_acts(unemp_cand_acts_with, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
        "demo.unemp.cand.with", surface=surface,
    )

    unemp_cand_acts_without = _make_base_acts(wages=90000.0, unemployment=500.0)
    unemp_cand_acts_without.append(_act(len(unemp_cand_acts_without), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
    res_unemp_cand_without = _run_probe(
        _finish_acts(unemp_cand_acts_without, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
        "demo.unemp.cand.without", surface=surface,
    )

    # 3. Student loan interest return ($1,500 interest)
    sli_acts_base = _f1098e_acts(statements=[Statement(lender="demo.lender", stmt="demo.stmt", box1=1500.0)], wages=90000.0)
    sli_acts_base.pop()
    res_sli_base = run_base(sli_acts_base, "demo.sli.base")

    sli_cand_with = _f1098e_acts(statements=[Statement(lender="demo.lender", stmt="demo.stmt", box1=1500.0)], wages=90000.0)
    sli_cand_with.pop()
    sli_cand_with.append(_act(len(sli_cand_with), "bundle-adoption", {"bundle": _f1099k_bundle()}))
    sli_cand_with.append(_act(len(sli_cand_with), "bundle-adoption", {"bundle": _f1099k_circumstances_bundle()}))
    sli_cand_with.append(_act(len(sli_cand_with), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
    _add_family_closure(sli_cand_with, "demo.f1099k.h0", closed=True)
    res_sli_cand_with = _run_probe(
        _finish_acts(sli_cand_with, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
        "demo.sli.cand.with", surface=surface,
    )

    sli_cand_without = _f1098e_acts(statements=[Statement(lender="demo.lender", stmt="demo.stmt", box1=1500.0)], wages=90000.0)
    sli_cand_without.pop()
    sli_cand_without.append(_act(len(sli_cand_without), "bundle-adoption", {"bundle": _f1099k_bundle()}))
    sli_cand_without.append(_act(len(sli_cand_without), "bundle-adoption", {"bundle": _f1099k_circumstances_bundle()}))
    sli_cand_without.append(_act(len(sli_cand_without), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
    res_sli_cand_without = _run_probe(
        _finish_acts(sli_cand_without, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
        "demo.sli.cand.without", surface=surface,
    )

    def _fmt(res: dict[str, Any]) -> str:
        att = (res.get("schedule1_attachment_dispositions") or [{}])[0].get("disposition", "none")
        line9 = str(res.get("line9_value", "none"))
        rows = str(res.get("presentation_rows_count", "none"))
        return f"Sch1: {att:<12} | L9: {line9:<10} | Rows: {rows:<4}"

    print(f"{'Return Scenario':<44} | {'Measurement':<40}")
    print("-" * 88)
    print(f"{'1. W-2 only (Baseline, unmodified release v43)':<44} | {_fmt(res_w2_base)}")
    print(f"{'1. W-2 only (Candidate v46 surface)':<44} | {_fmt(res_w2_cand)}")
    print(f"{'2. Unemployment (Baseline, unmodified)':<44} | {_fmt(res_unemp_base)}")
    print(f"{'2. Unemployment (Candidate + 1099-K closure)':<44} | {_fmt(res_unemp_cand_with)}")
    print(f"{'2. Unemployment (Candidate - 1099-K closure)':<44} | {_fmt(res_unemp_cand_without)}")
    print(f"{'3. Student Loan (Baseline, unmodified)':<44} | {_fmt(res_sli_base)}")
    print(f"{'3. Student Loan (Candidate + 1099-K closure)':<44} | {_fmt(res_sli_cand_with)}")
    print(f"{'3. Student Loan (Candidate - 1099-K closure)':<44} | {_fmt(res_sli_cand_without)}")
    print("=" * 88)

    return {
        "w2_baseline": res_w2_base,
        "w2_candidate": res_w2_cand,
        "unemp_baseline": res_unemp_base,
        "unemp_candidate_with": res_unemp_cand_with,
        "unemp_candidate_without": res_unemp_cand_without,
        "sli_baseline": res_sli_base,
        "sli_candidate_with": res_sli_cand_with,
        "sli_candidate_without": res_sli_cand_without,
    }


def build_and_run_all_paths() -> tuple[dict[str, Any], dict[str, Any]]:
    with TemporaryDirectory() as tmp_root:
        surface, rel_sum, pkg_id, pkg_ver, pkg_sum = _build_surface(Path(tmp_root))

        results: dict[str, Any] = {}

        # -------------------------------------------------------------------
        # Path 1: closed-empty return with 1099-K completeness answer
        # -------------------------------------------------------------------
        acts1 = _make_base_acts(wages=90000.0)
        acts1.append(_act(len(acts1), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        _add_family_closure(acts1, "demo.f1099k.h0", closed=True)
        results["1. closed-empty-with-completeness"] = _run_probe(
            _finish_acts(acts1, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p1.closed-empty", surface,
        )

        # -------------------------------------------------------------------
        # Path 2: Unemployment Schedule 1 return WITH 1099-K completeness answer
        # -------------------------------------------------------------------
        acts2 = _make_base_acts(wages=90000.0, unemployment=500.0)
        acts2.append(_act(len(acts2), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        _add_family_closure(acts2, "demo.f1099k.h0", closed=True)
        results["2. unemployment-with-completeness"] = _run_probe(
            _finish_acts(acts2, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p2.unemployment-with-closure", surface,
        )

        # -------------------------------------------------------------------
        # Path 3: Unemployment Schedule 1 return WITHOUT 1099-K completeness answer
        # -------------------------------------------------------------------
        acts3 = _make_base_acts(wages=90000.0, unemployment=500.0)
        acts3.append(_act(len(acts3), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        # No closure asserted
        results["3. unemployment-without-completeness"] = _run_probe(
            _finish_acts(acts3, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p3.unemployment-unclosed", surface,
        )

        # -------------------------------------------------------------------
        # Path 4: W-2-only return
        # -------------------------------------------------------------------
        acts4 = _ssa_acts(wages=90000.0, benefits=[])
        acts4.pop()
        results["4. w2-only-return"] = _run_probe(
            _finish_acts(acts4, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p4.w2-only", surface,
        )

        # -------------------------------------------------------------------
        # Path 5: Single supported loss (platform pass-through shipping)
        # -------------------------------------------------------------------
        acts5 = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts5, "demo.platform.a", "demo.stmt.a")
        acts5.append(_act(len(acts5), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts5.append(_act(len(acts5), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 880.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts5, payer="demo.platform.a", stmt="demo.stmt.a", box1a=880.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "platform-pass-through", Q9_FEES: 80.0,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 56.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 24.0,
                Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts5, "demo.f1099k.h1", closed=True)
        results["5. supported-loss-pass-through-shipping"] = _run_probe(
            _finish_acts(acts5, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p5.supported-loss-pass-through", surface,
        )

        # -------------------------------------------------------------------
        # Path 6: Single supported loss (seller-received shipping)
        # -------------------------------------------------------------------
        acts6 = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts6, "demo.platform.a", "demo.stmt.a")
        acts6.append(_act(len(acts6), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts6.append(_act(len(acts6), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 880.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts6, payer="demo.platform.a", stmt="demo.stmt.a", box1a=880.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "seller-received-shipping", Q9_FEES: 80.0,
                Q9_SELLER_SHIP: 24.0, Q10_TAX: 56.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 24.0,
                Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts6, "demo.f1099k.h1", closed=True)
        results["6. supported-loss-seller-received-shipping"] = _run_probe(
            _finish_acts(acts6, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p6.supported-loss-seller-shipping", surface,
        )

        # -------------------------------------------------------------------
        # Path 7: Single supported loss with refund
        # -------------------------------------------------------------------
        acts7 = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts7, "demo.platform.a", "demo.stmt.a")
        acts7.append(_act(len(acts7), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts7.append(_act(len(acts7), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 800.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts7, payer="demo.platform.a", stmt="demo.stmt.a", box1a=800.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "platform-pass-through", Q9_FEES: 80.0,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 0.0, Q10_REFUND: 100.0, Q11_BUYER_SHIP: 0.0,
                Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts7, "demo.f1099k.h1", closed=True)
        results["7. supported-loss-with-refund"] = _run_probe(
            _finish_acts(acts7, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p7.supported-loss-refund", surface,
        )

        # -------------------------------------------------------------------
        # Path 8: Single supported loss with free shipping seller-paid
        # -------------------------------------------------------------------
        acts8 = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts8, "demo.platform.a", "demo.stmt.a")
        acts8.append(_act(len(acts8), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts8.append(_act(len(acts8), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 800.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts8, payer="demo.platform.a", stmt="demo.stmt.a", box1a=800.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "none", Q9_FEES: 80.0,
                Q9_SELLER_SHIP: 30.0, Q10_TAX: 0.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 0.0,
                Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts8, "demo.f1099k.h1", closed=True)
        results["8. supported-loss-free-shipping-seller-paid"] = _run_probe(
            _finish_acts(acts8, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p8.supported-loss-free-shipping", surface,
        )

        # -------------------------------------------------------------------
        # Path 9: Two supported personal losses
        # -------------------------------------------------------------------
        acts9 = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts9, "demo.platform.a", "demo.stmt.a")
        _add_statement_entities(acts9, "demo.platform.b", "demo.stmt.b")
        acts9.append(_act(len(acts9), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts9.append(_act(len(acts9), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 880.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts9, payer="demo.platform.a", stmt="demo.stmt.a", box1a=880.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "platform-pass-through", Q9_FEES: 80.0,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 56.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 24.0,
                Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        acts9.append(_act(len(acts9), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.b", _statement_fact_id(BOX1A, "demo.platform.b", "demo.stmt.b"), 400.0)},
            "successor": {"id": "demo.f1099k.h2", "predecessor": "demo.f1099k.h1"},
        }))
        _add_statement_assertions(
            acts9, payer="demo.platform.b", stmt="demo.stmt.b", box1a=400.0, box4=0.0,
            answers={
                Q8_PRICE: 400.0, Q8_SHIP: "none", Q9_FEES: 50.0,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 0.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 0.0,
                Q12_COST: 500.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts9, "demo.f1099k.h2", closed=True)
        results["9. two-statements-out-of-scope"] = _run_probe(
            _finish_acts(acts9, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p9.two-statements", surface,
        )

        def _run_single_case(label: str, run_id: str, box1a: float, box4: float, answers: dict[str, Any]) -> dict[str, Any]:
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
            return _run_probe(
                _finish_acts(acts, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
                run_id, surface,
            )

        # -------------------------------------------------------------------
        # Paths 10-22: Stops and Exclusions
        # -------------------------------------------------------------------
        results["10. unsupported-gain"] = _run_single_case(
            "unsupported-gain", "demo.p10.gain", box1a=1200.0, box4=0.0,
            answers={Q8_PRICE: 1200.0, Q9_FEES: 100.0, Q12_COST: 800.0, Q10_TAX: 0.0, Q11_BUYER_SHIP: 0.0},
        )
        results["11. break-even-sale"] = _run_single_case(
            "break-even-sale", "demo.p11.breakeven", box1a=800.0, box4=0.0,
            answers={Q8_PRICE: 800.0, Q9_FEES: 100.0, Q12_COST: 700.0, Q10_TAX: 0.0, Q11_BUYER_SHIP: 0.0},
        )
        results["12. investment-purpose-excluded"] = _run_single_case(
            "investment-purpose-excluded", "demo.p12.investment", box1a=880.0, box4=0.0,
            answers={Q4: "investment-or-profit"},
        )
        results["13. resale-inventory-excluded"] = _run_single_case(
            "resale-inventory-excluded", "demo.p13.resale", box1a=880.0, box4=0.0,
            answers={Q4: "resale-or-inventory"},
        )
        results["14. prior-depreciable-use-excluded"] = _run_single_case(
            "prior-depreciable-use-excluded", "demo.p14.depreciable", box1a=880.0, box4=0.0,
            answers={Q5: "no"},
        )
        results["15. digital-asset-excluded"] = _run_single_case(
            "digital-asset-excluded", "demo.p15.digital-asset", box1a=880.0, box4=0.0,
            answers={Q7: "yes"},
        )
        results["16. multi-sale-statement-unsupported"] = _run_single_case(
            "multi-sale-statement-unsupported", "demo.p16.multi-sale", box1a=880.0, box4=0.0,
            answers={Q1: "no"},
        )
        results["17. non-purchase-acquisition-unsupported"] = _run_single_case(
            "non-purchase-acquisition-unsupported", "demo.p17.non-purchase", box1a=880.0, box4=0.0,
            answers={Q3: "no"},
        )
        results["18. basis-adjustment-unsupported"] = _run_single_case(
            "basis-adjustment-unsupported", "demo.p18.basis-adjustment", box1a=880.0, box4=0.0,
            answers={Q13: "yes"},
        )
        results["19. backup-withholding-unsupported"] = _run_single_case(
            "backup-withholding-unsupported", "demo.p19.withholding", box1a=880.0, box4=150.0,
            answers={},
        )
        results["20. cost-basis-unknown"] = _run_single_case(
            "cost-basis-unknown", "demo.p20.cost-unknown", box1a=880.0, box4=0.0,
            answers={Q12_GATE: "cannot-tell"},
        )
        results["21. unanswered-stop"] = _run_single_case(
            "unanswered-stop", "demo.p21.unanswered", box1a=880.0, box4=0.0,
            answers={Q5: None},  # omitted -> resolves to optional_default "not-asked"
        )
        results["22. unexplained-reconciliation-discrepancy"] = _run_single_case(
            "unexplained-reconciliation-discrepancy", "demo.p22.reconciliation", box1a=850.0, box4=0.0,
            answers={Q8_PRICE: 700.0, Q10_TAX: 0.0, Q11_BUYER_SHIP: 0.0},
        )

        # -------------------------------------------------------------------
        # Path 23: Supported alongside unsupported
        # -------------------------------------------------------------------
        acts23 = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts23, "demo.platform.a", "demo.stmt.a")
        _add_statement_entities(acts23, "demo.platform.b", "demo.stmt.b")
        acts23.append(_act(len(acts23), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts23.append(_act(len(acts23), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 880.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts23, payer="demo.platform.a", stmt="demo.stmt.a", box1a=880.0, box4=0.0,
            answers={Q8_PRICE: 800.0, Q9_FEES: 80.0, Q10_TAX: 56.0, Q11_BUYER_SHIP: 24.0, Q12_COST: 1000.0},
        )
        acts23.append(_act(len(acts23), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.b", _statement_fact_id(BOX1A, "demo.platform.b", "demo.stmt.b"), 1200.0)},
            "successor": {"id": "demo.f1099k.h2", "predecessor": "demo.f1099k.h1"},
        }))
        _add_statement_assertions(
            acts23, payer="demo.platform.b", stmt="demo.stmt.b", box1a=1200.0, box4=0.0,
            answers={Q8_PRICE: 1200.0, Q9_FEES: 100.0, Q10_TAX: 0.0, Q11_BUYER_SHIP: 0.0, Q12_COST: 800.0},  # unsupported gain
        )
        _add_family_closure(acts23, "demo.f1099k.h2", closed=True)
        results["23. supported-alongside-unsupported"] = _run_probe(
            _finish_acts(acts23, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p23.supported-alongside-unsupported", surface,
        )

        # -------------------------------------------------------------------
        # Path 24: Late member after closure
        # -------------------------------------------------------------------
        acts24 = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts24, "demo.platform.a", "demo.stmt.a")
        _add_statement_entities(acts24, "demo.platform.b", "demo.stmt.b")
        acts24.append(_act(len(acts24), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts24.append(_act(len(acts24), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 880.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(acts24, payer="demo.platform.a", stmt="demo.stmt.a", box1a=880.0, box4=0.0)
        _add_family_closure(acts24, "demo.f1099k.h1", closed=True)
        # Late member added at h2 without re-closing
        acts24.append(_act(len(acts24), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.b", _statement_fact_id(BOX1A, "demo.platform.b", "demo.stmt.b"), 400.0)},
            "successor": {"id": "demo.f1099k.h2", "predecessor": "demo.f1099k.h1"},
        }))
        _add_statement_assertions(acts24, payer="demo.platform.b", stmt="demo.stmt.b", box1a=400.0, box4=0.0)
        results["24. late-member-after-closure"] = _run_probe(
            _finish_acts(acts24, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p24.late-member", surface,
        )

        # -------------------------------------------------------------------
        # Path 25: Gain/loss boundary correction
        # -------------------------------------------------------------------
        acts25 = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts25, "demo.platform.a", "demo.stmt.a")
        acts25.append(_act(len(acts25), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts25.append(_act(len(acts25), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 880.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts25, payer="demo.platform.a", stmt="demo.stmt.a", box1a=880.0, box4=0.0,
            answers={Q8_PRICE: 800.0, Q9_FEES: 80.0, Q10_TAX: 56.0, Q11_BUYER_SHIP: 24.0, Q12_COST: 1200.0},
        )
        _add_family_closure(acts25, "demo.f1099k.h1", closed=True)
        # Correct cost basis from 1200.0 to 600.0 (proceeds 720.0 > 600.0 -> gain)
        acts25.append(_act(len(acts25), "assertion", {"finding": _attested("f.cost.corrected", _statement_fact_id(Q12_COST, "demo.platform.a", "demo.stmt.a"), 600.0)}))
        results["25. gain-loss-boundary-correction"] = _run_probe(
            _finish_acts(acts25, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p25.boundary-correction", surface,
        )

        # -------------------------------------------------------------------
        # Path 26: Omitted platform fee (stops with platform-fees-unanswered)
        # -------------------------------------------------------------------
        acts26 = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts26, "demo.platform.a", "demo.stmt.a")
        acts26.append(_act(len(acts26), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts26.append(_act(len(acts26), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 800.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts26, payer="demo.platform.a", stmt="demo.stmt.a", box1a=800.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "none", Q9_FEES: None,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 0.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 0.0,
                Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts26, "demo.f1099k.h1", closed=True)
        results["26. omitted-platform-fee"] = _run_probe(
            _finish_acts(acts26, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p26.omitted-fees", surface,
        )

        # -------------------------------------------------------------------
        # Path 27: Withdrawn amount (stops with agreed-price-unanswered)
        # -------------------------------------------------------------------
        acts27 = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts27, "demo.platform.a", "demo.stmt.a")
        acts27.append(_act(len(acts27), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts27.append(_act(len(acts27), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 880.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts27, payer="demo.platform.a", stmt="demo.stmt.a", box1a=880.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "platform-pass-through", Q9_FEES: 80.0,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 56.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 24.0,
                Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        acts27.append(_act(len(acts27), "finding-retracted", {"finding_id": "f.agreed-item-price.demo.stmt.a"}))
        _add_family_closure(acts27, "demo.f1099k.h1", closed=True)
        results["27. withdrawn-amount"] = _run_probe(
            _finish_acts(acts27, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p27.withdrawn-amount", surface,
        )

        # -------------------------------------------------------------------
        # Path 28: Improvements "can't tell" (stops with cannot-tell-improvements)
        # -------------------------------------------------------------------
        acts28 = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts28, "demo.platform.a", "demo.stmt.a")
        acts28.append(_act(len(acts28), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts28.append(_act(len(acts28), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 880.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts28, payer="demo.platform.a", stmt="demo.stmt.a", box1a=880.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "platform-pass-through", Q9_FEES: 80.0,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 56.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 24.0,
                Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "cannot-tell",
            },
        )
        _add_family_closure(acts28, "demo.f1099k.h1", closed=True)
        results["28. cannot-tell-improvements"] = _run_probe(
            _finish_acts(acts28, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p28.cannot-tell-improvements", surface,
        )

        # -------------------------------------------------------------------
        # Path 29: Boundary Case 1 (seller-received shipping gain)
        # Price 800, seller-received shipping 100, label 20, cost 850, Box 1a 900
        # -------------------------------------------------------------------
        acts29 = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts29, "demo.platform.a", "demo.stmt.a")
        acts29.append(_act(len(acts29), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts29.append(_act(len(acts29), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 900.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts29, payer="demo.platform.a", stmt="demo.stmt.a", box1a=900.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "seller-received-shipping", Q9_FEES: 0.0,
                Q9_SELLER_SHIP: 20.0, Q10_TAX: 0.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 100.0,
                Q12_COST: 850.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts29, "demo.f1099k.h1", closed=True)
        results["29. boundary-case-1-seller-received-shipping-gain"] = _run_probe(
            _finish_acts(acts29, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p29.boundary-1", surface,
        )

        # -------------------------------------------------------------------
        # Path 30: Boundary Case 2 (refund loss)
        # Price 800, refund 100, cost 750, Box 1a 800
        # -------------------------------------------------------------------
        acts30 = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts30, "demo.platform.a", "demo.stmt.a")
        acts30.append(_act(len(acts30), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts30.append(_act(len(acts30), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 800.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts30, payer="demo.platform.a", stmt="demo.stmt.a", box1a=800.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "none", Q9_FEES: 0.0,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 0.0, Q10_REFUND: 100.0, Q11_BUYER_SHIP: 0.0,
                Q12_COST: 750.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts30, "demo.f1099k.h1", closed=True)
        results["30. boundary-case-2-refund-loss"] = _run_probe(
            _finish_acts(acts30, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p30.boundary-2", surface,
        )

        # -------------------------------------------------------------------
        # Path 31: Boundary Case 3 (none shipping, seller-paid shipping loss)
        # Price 800, arrangement none, seller-paid shipping 100, cost 750, Box 1a 800
        # -------------------------------------------------------------------
        acts31 = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts31, "demo.platform.a", "demo.stmt.a")
        acts31.append(_act(len(acts31), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts31.append(_act(len(acts31), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 800.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts31, payer="demo.platform.a", stmt="demo.stmt.a", box1a=800.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "none", Q9_FEES: 0.0,
                Q9_SELLER_SHIP: 100.0, Q10_TAX: 0.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 0.0,
                Q12_COST: 750.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts31, "demo.f1099k.h1", closed=True)
        results["31. boundary-case-3-none-shipping-seller-paid-loss"] = _run_probe(
            _finish_acts(acts31, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p31.boundary-3", surface,
        )

        # -------------------------------------------------------------------
        # Path 32: Boundary Case 4 (pass-through shipping loss)
        # Price 800, pass-through shipping 100, cost 850, Box 1a 900
        # -------------------------------------------------------------------
        acts32 = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts32, "demo.platform.a", "demo.stmt.a")
        acts32.append(_act(len(acts32), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts32.append(_act(len(acts32), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 900.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts32, payer="demo.platform.a", stmt="demo.stmt.a", box1a=900.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "platform-pass-through", Q9_FEES: 0.0,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 0.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 100.0,
                Q12_COST: 850.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts32, "demo.f1099k.h1", closed=True)
        results["32. boundary-case-4-pass-through-shipping-loss"] = _run_probe(
            _finish_acts(acts32, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p32.boundary-4", surface,
        )

        # -------------------------------------------------------------------
        # Path 33: Boundary Case 5 (pass-through with seller-paid shipping gain)
        # Price 900, pass-through, seller-paid shipping 100, cost 850, Box 1a 900
        # -------------------------------------------------------------------
        acts33 = _make_base_acts(wages=90000.0)
        _add_statement_entities(acts33, "demo.platform.a", "demo.stmt.a")
        acts33.append(_act(len(acts33), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts33.append(_act(len(acts33), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, "demo.platform.a", "demo.stmt.a"), 900.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts33, payer="demo.platform.a", stmt="demo.stmt.a", box1a=900.0, box4=0.0,
            answers={
                Q8_PRICE: 900.0, Q8_SHIP: "platform-pass-through", Q9_FEES: 0.0,
                Q9_SELLER_SHIP: 100.0, Q10_TAX: 0.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 0.0,
                Q12_COST: 850.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts33, "demo.f1099k.h1", closed=True)
        results["33. boundary-case-5-pass-through-seller-paid-gain"] = _run_probe(
            _finish_acts(acts33, release_checksum=rel_sum, package_id=pkg_id, package_version=pkg_ver, package_checksum=pkg_sum),
            "demo.p33.boundary-5", surface,
        )

        neighbor_results = measure_neighbor_baselines(surface, rel_sum, pkg_id, pkg_ver, pkg_sum)
        return results, neighbor_results


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
}


def main() -> None:
    print("=" * 110)
    print("D2 Candidate Citizen Probe: Executing 33 Disposition Paths and Asserting Outcomes")
    print("=" * 110)

    results, neighbor_results = build_and_run_all_paths()

    header = f"{'Path':<44} | {'Reason / Top Token':<32} | {'Unres':<10} | {'Status':<6}"
    print(header)
    print("-" * len(header))

    failed: list[str] = []

    for name, res in results.items():
        if "exception" in res:
            print(f"{name:<44} | EXCEPTION: {res['exception']['type']} {res['exception']['message']}")
            failed.append(f"{name}: exception {res['exception']['type']}")
            continue
        if "refusal" in res:
            print(f"{name:<44} | REFUSAL: {res['refusal']['reason']}")
            failed.append(f"{name}: refusal {res['refusal']['reason']}")
            continue

        decl = EXPECTED_OUTCOMES.get(name)
        if decl is None:
            failed.append(f"{name}: missing expected outcome declaration")
            continue

        expected_token = decl["expected_token"]
        is_stmt_reason = decl["is_statement_reason"]

        actual_token: str
        if is_stmt_reason:
            reason_pubs = [p.get("value") for p in res.get("loss_reason_publications", [])]
            if reason_pubs and all(r == expected_token for r in reason_pubs):
                actual_token = expected_token
            else:
                actual_token = str(reason_pubs)
        else:
            if expected_token == "0":
                top_pubs = res.get("top_entry_publications") or []
                actual_token = str(top_pubs[0].get("value")) if top_pubs else "none"
            else:
                top_disps = res.get("top_entry_dispositions") or [{}]
                actual_token = str(top_disps[0].get("code") or top_disps[0].get("disposition"))

        mismatch = False
        if actual_token != expected_token:
            mismatch = True
            failed.append(f"{name}: expected {expected_token}, got {actual_token}")

        # Assert top-entry published amount (Box 1a on supported-loss, 0 on closed-empty, none on stops)
        expected_top_amt = decl.get("expected_top_amount")
        top_pubs = res.get("top_entry_publications") or []
        if expected_top_amt is not None:
            if not top_pubs:
                mismatch = True
                failed.append(f"{name}: expected top-entry amount {expected_top_amt}, got no publications")
            else:
                actual_top_val = top_pubs[0].get("value")
                try:
                    if float(actual_top_val) != float(expected_top_amt):
                        mismatch = True
                        failed.append(f"{name}: expected top-entry amount {expected_top_amt}, got {actual_top_val}")
                except (ValueError, TypeError):
                    if actual_top_val != expected_top_amt:
                        mismatch = True
                        failed.append(f"{name}: expected top-entry amount {expected_top_amt}, got {actual_top_val}")
        else:
            if top_pubs:
                actual_top_val = top_pubs[0].get("value")
                mismatch = True
                failed.append(f"{name}: expected no top-entry publication, got {actual_top_val}")

        top_explain = res.get("top_entry_explain") or ""
        unres_reasons = res.get("unresolved_reasons") or []
        unres_explain = res.get("unresolved_explain") or ""
        top_disp = (res.get("top_entry_field_resolved") or {}).get("disposition")
        unres_disp = (res.get("unresolved_field_resolved") or {}).get("disposition")

        if decl.get("expected_unres_disp") and unres_disp != decl["expected_unres_disp"]:
            mismatch = True
            failed.append(f"{name}: expected unresolved disposition {decl['expected_unres_disp']}, got {unres_disp}")

        for exp_sent in decl["expected_top_sentences"]:
            if top_disp not in ("blocked", "published_value") or top_explain != exp_sent:
                mismatch = True
                failed.append(f"{name}: expected top-entry sentence {exp_sent!r}, got disp={top_disp!r}, explain={top_explain!r}")

        for exp_sent in decl["expected_unres_sentences"]:
            if unres_disp != "blocked" or exp_sent not in unres_reasons:
                mismatch = True
                failed.append(f"{name}: expected unresolved reason sentence {exp_sent!r}, got reasons={unres_reasons!r}")

        status = "FAIL" if mismatch else "PASS"
        token_summary = f"{actual_token} (exp: {expected_token})" if mismatch else actual_token
        print(f"{name:<44} | {token_summary:<32} | {str(unres_disp):<10} | {status:<6}")

        if decl["expected_top_sentences"] or decl["expected_unres_sentences"]:
            if top_disp in ("blocked", "published_value") and top_explain:
                print(f"   [Top Entry Row]   disposition: {top_disp} | explain: {top_explain!r}")
            if unres_disp == "blocked":
                print(f"   [Unresolved Row]  disposition: {unres_disp} | explain: {unres_explain!r}")
                for sent in unres_reasons:
                    print(f"                     projected sentence: {sent!r}")

    print("=" * 110)
    print(f"Total paths run: {len(results)}, Failed / Findings: {len(failed)}")
    if failed:
        for f in failed:
            print(f"  FAILED: {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()
