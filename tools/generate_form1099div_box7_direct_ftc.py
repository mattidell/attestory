"""Generate the additive Form 1099-DIV box-7 direct FTC (no Form 1116) route.

Reads the accepted v20/v15/v13 graph and writes only new content citizens plus
package v21, published-packages v16, release v14, and adoption v21. Historical
residual, packages, and registries remain byte-for-byte.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
FIXTURES = ROOT / "packages" / "sample_data" / "form1099div_box7_direct_ftc"

SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}

BOX7_AMOUNT = "tax.us.2025.f1099div.box7-foreign-tax-paid"
BOX7_CLOSURE = "tax.us.2025.f1099div.7.source-closure"
BOX7_FAMILY = "tax.us.2025.f1099div.7"
BOX7_SUBTOTAL = "tax.us.2025.foreign-tax.box7-subtotal"
BOX8_AUTH = "tax.us.2025.f1099div.box8-country-companion"
BOX12_BUNDLE = "tax.us.2025.f1099div.box12.vocabulary"
BOX7_BUNDLE = "tax.us.2025.f1099div.box7.vocabulary"
DIRECT_FTC_SCOPE = "tax.us.2025.direct-ftc-scope.vocabulary"

SCH3_L1 = "tax.us.2025.schedule3.line1-direct-ftc"
SCH3_L8 = "tax.us.2025.schedule3.line8-total"
L20 = "tax.us.2025.credits.form1040-line20"
TAX_AFTER = "tax.us.2025.tax.after-nonrefundable-credits"
LINE16 = "tax.us.2025.tax.total-tax"

# Tax-year scope components: associated income, creditability, election, Sch3, L16/L19 absences.
SCOPE_COMPONENTS: tuple[tuple[str, str], ...] = (
    (
        "all-foreign-income-passive",
        "All foreign-source gross income in the bounded class is passive-category income.",
    ),
    (
        "all-foreign-income-on-1099div",
        "All foreign-source gross income and foreign taxes in the class are reported on qualified Form 1099-DIV payee statements only.",
    ),
    (
        "no-f1099int-foreign-tax",
        "No foreign tax from Form 1099-INT is present on this return for the bounded direct-election claim.",
    ),
    (
        "no-k1-k3-foreign-tax",
        "No foreign tax from Schedule K-1 or Schedule K-3 is present on this return for the bounded direct-election claim.",
    ),
    (
        "no-other-foreign-tax-source",
        "No foreign tax from any source outside the selected Form 1099-DIV class is present for the bounded direct-election claim.",
    ),
    (
        "tax-type-creditable",
        "Selected foreign taxes are income, war profits, or excess profits taxes, or taxes in lieu of such taxes.",
    ),
    (
        "legal-liability-and-paid",
        "Taxpayer is legally liable for and has paid (cash method) the selected foreign taxes.",
    ),
    (
        "no-refund-rebate-subsidy",
        "Selected foreign taxes are not refundable, rebated, subsidized, or reimbursed.",
    ),
    (
        "no-excluded-income-association",
        "Selected foreign taxes are not associated with excluded income.",
    ),
    (
        "holding-period-16-day-met",
        "Dividend holding-period requirement met (at least 16 days; Pub. 514 / Schedule 3 exception).",
    ),
    (
        "no-short-sale-obligation",
        "No disqualifying short-sale or related obligation to pay the dividend.",
    ),
    (
        "country-recognized-non-terrorism",
        "Taxes paid to countries recognized by the United States that do not support terrorism, as required by the Schedule 3 exception path.",
    ),
    (
        "no-carryback-carryforward",
        "No foreign-tax carryback or carryforward applies for the election year.",
    ),
    (
        "no-schedule-a-deduction-election",
        "No Schedule A foreign-tax deduction election is present.",
    ),
    (
        "no-form-1116-required",
        "No Form-1116-required condition is present; the direct-election route applies without Form 1116.",
    ),
    (
        "no-sch3-line2",
        "Schedule 3 Part I line 2 credit is absent for the bounded class.",
    ),
    (
        "no-sch3-line3",
        "Schedule 3 Part I line 3 credit is absent for the bounded class.",
    ),
    (
        "no-sch3-line4",
        "Schedule 3 Part I line 4 credit is absent for the bounded class.",
    ),
    (
        "no-sch3-line5",
        "Schedule 3 Part I line 5 credit is absent for the bounded class.",
    ),
    (
        "no-sch3-line6",
        "Schedule 3 Part I line 6 credit is absent for the bounded class.",
    ),
    (
        "no-line17-schedule2-additional",
        "Form 1040 line 17 / Schedule 2 additional tax affecting line 18 is absent for the bounded class.",
    ),
    (
        "no-line19-ctc-odc",
        "Form 1040 line 19 child tax credit / other dependent credit is absent for the bounded class.",
    ),
    (
        "no-schedule2-regular-tax-add",
        "Schedule 2 line 1a/1z amounts that would change regular tax for the credit cap are absent for the bounded class.",
    ),
    (
        "no-form-4972-on-line16",
        "Form 4972 tax included on Form 1040 line 16 is absent for the bounded class.",
    ),
)

ELECTION_FACT = "tax.us.2025.direct-ftc.election"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text("utf-8"))
    assert isinstance(value, dict)
    return value


def _document(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _checksum(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _package_checksum(package: dict[str, Any]) -> str:
    return _checksum({k: v for k, v in package.items() if k != "package_checksum"})


def _scope_id(token: str) -> str:
    return f"tax.us.2025.direct-ftc-scope.{token}"


def _statement_keys() -> list[dict[str, Any]]:
    return [
        {"name": "payer", "kind": "entity", "entity_kind": "tax.us.dividend-payer"},
        {"name": "statement", "kind": "entity", "entity_kind": "tax.us.1099div-statement"},
        {"name": "tax-year", "kind": "literal", "values": ["2025"]},
    ]


def _yes_compare(fact_id: str) -> dict[str, Any]:
    return {
        "op": "categorical_compare",
        "cmp": "eq",
        "left": {"op": "ref", "name": fact_id},
        "right": {
            "op": "category_literal",
            "value": "yes",
            "fact_type": {"id": fact_id, "version": "v1"},
        },
    }


def _box12_bundle_v2() -> dict[str, Any]:
    """Successor box-12 vocabulary without residual (residual moves to box-7 bundle)."""
    base = _load(CONTENT / "f1099div-box12.bundle.json")
    fact_types = [
        ft
        for ft in base["fact_types"]
        if ft["id"] != "tax.us.2025.f1099div.recorded-boxes"
    ]
    return {
        "schema": "bundle.v2",
        "id": BOX12_BUNDLE,
        "version": "v2",
        "label": (
            "Form 1099-DIV box-12 exempt-interest dividends and box-13 absence/zero "
            "authority for tax year 2025 without residual recorded-boxes "
            "(box-7 residual succession)"
        ),
        "fact_types": fact_types,
    }


def _box7_bundle() -> dict[str, Any]:
    return {
        "schema": "bundle.v2",
        "id": BOX7_BUNDLE,
        "version": "v1",
        "label": (
            "Form 1099-DIV box-7 foreign tax paid, box-8 country companion, "
            "residual recorded-boxes v4 (3 and 5 only), and direct-election "
            "election fact for tax year 2025"
        ),
        "fact_types": [
            {
                "schema": "fact-type.v2",
                "id": BOX7_AMOUNT,
                "version": "v1",
                "title": (
                    "Foreign tax paid reported in box 7 of one logical Form 1099-DIV "
                    "statement instance furnished by a payer for 2025, in U.S. dollars. "
                    "The statement instance is peer to evidence and its identity carries "
                    "no file, upload, scan, document, or evidence key (ADR-0015). Multiple "
                    "originals from one payer are distinct statement instances; a corrected "
                    "copy of the same logical return answers this same fact and supersedes "
                    "its prior finding. Nonnegative source amount only. Box 7 is a credit "
                    "source and never reduces dividend income."
                ),
                "nature": "determinable",
                "identity_keys": _statement_keys(),
                "value_schema": {"type": "number", "minimum": 0},
                "supersession": {"policy": "free"},
                "source_amount": True,
                "quantity": {
                    "id": "tax.us.2025.quantity.foreign-tax-paid",
                    "version": "v1",
                },
            },
            {
                "schema": "fact-type.v2",
                "id": BOX7_CLOSURE,
                "version": "v1",
                "title": (
                    "User-attested closure of the Form 1099-DIV box-7 source family for "
                    "2025, keyed on the family membership horizon current at attestation "
                    "(ADR-0017): true asserts every furnished 1099-DIV box-7 amount is "
                    "recorded as of that horizon. This claim covers box 7 only — never "
                    "boxes 1a/1b/2a/12, residual recorded boxes 3 and 5, or Schedule 3 / "
                    "Form 1040 credit completeness. A later membership transition displaces "
                    "this closure through horizon succession; re-attestation on the "
                    "successor horizon is required."
                ),
                "nature": "determinable",
                "identity_keys": [
                    {
                        "name": "family-horizon",
                        "kind": "entity",
                        "entity_kind": "kernel.family-horizon",
                    },
                    {"name": "tax-year", "kind": "literal", "values": ["2025"]},
                ],
                "value_schema": {"type": "boolean"},
                "supersession": {"policy": "free"},
            },
            {
                "schema": "fact-type.v2",
                "id": BOX8_AUTH,
                "version": "v1",
                "title": (
                    "Explicit companion authority for Form 1099-DIV box 8 (foreign country "
                    "or U.S. possession) on the same logical statement as a box-7 member. "
                    "Admissible states: a non-empty country/possession name string, or the "
                    "explicit RIC sentinel not_applicable (Form 1099-DIV instructions: RICs "
                    "do not complete box 8). Missing companion fails closed. Multi-country "
                    "supplemental allocation of one box-7 amount is excluded. This is an "
                    "authority witness, not a composed credit amount."
                ),
                "nature": "determinable",
                "identity_keys": _statement_keys(),
                "value_schema": {
                    "type": "string",
                    "minLength": 1,
                },
                "supersession": {"policy": "free"},
            },
            {
                "schema": "fact-type.v2",
                "id": ELECTION_FACT,
                "version": "v1",
                "title": (
                    "Taxpayer election to claim the foreign tax credit without filing "
                    "Form 1116 for tax year 2025 under the Schedule 3 / Form 1116 "
                    "instructions direct-election procedure. Elective; domain {yes, no}; "
                    "no default; presence-before-value; free supersession. yes elects the "
                    "bounded route; no declines it and blocks the direct credit."
                ),
                "nature": "elective",
                "identity_keys": [
                    {"name": "tax-year", "kind": "literal", "values": ["2025"]},
                ],
                "value_schema": {"enum": ["yes", "no"]},
                "supersession": {"policy": "free"},
            },
            {
                "schema": "fact-type.v2",
                "id": "tax.us.2025.f1099div.recorded-boxes",
                "version": "v4",
                "title": (
                    "Successor residual recorded non-composable 1099-DIV box content for "
                    "one logical statement instance: boxes 3 and 5 only are recorded but "
                    "never composed into any line. Each box carries either its reported "
                    "number or explicit null as the declared absence of that box — absence "
                    "is asserted, never assumed. Boxes 2a, 7, and 12 are omitted because "
                    "the successor graph composes them through independent families. "
                    "Historical residual v1/v2/v3 remain immutable history; mixed "
                    "residual/family graphs are rejected at package validation."
                ),
                "nature": "determinable",
                "identity_keys": _statement_keys(),
                "value_schema": {
                    "type": "object",
                    "properties": {
                        "3": {"type": ["number", "null"]},
                        "5": {"type": ["number", "null"]},
                    },
                    "required": ["3", "5"],
                    "additionalProperties": False,
                },
                "supersession": {"policy": "free"},
            },
        ],
    }


def _scope_bundle() -> dict[str, Any]:
    fact_types = []
    for token, title in SCOPE_COMPONENTS:
        fact_types.append(
            {
                "schema": "fact-type.v2",
                "id": _scope_id(token),
                "version": "v1",
                "title": (
                    f"Direct foreign-tax-credit scope component: {title} Contributed "
                    "categorical assertion, domain {yes, no}, no default, "
                    "presence-before-value, free supersession. yes asserts the named "
                    "condition for the bounded class; no asserts the blocking condition "
                    "is present."
                ),
                "nature": "determinable",
                "identity_keys": [
                    {"name": "tax-year", "kind": "literal", "values": ["2025"]},
                ],
                "value_schema": {"enum": ["yes", "no"]},
                "supersession": {"policy": "free"},
            }
        )
    return {
        "schema": "bundle.v2",
        "id": DIRECT_FTC_SCOPE,
        "version": "v1",
        "label": (
            "Direct foreign-tax-credit (no Form 1116) scope, creditability, election "
            "completeness, and Schedule 3 / Form 1040 absence authorities for 2025"
        ),
        "fact_types": fact_types,
    }


def _family() -> dict[str, Any]:
    return {
        "schema": "source-family.v1",
        "id": BOX7_FAMILY,
        "version": "v1",
        "title": "Form 1099-DIV box 7 statement items, tax year 2025",
        "scope": SCOPE,
        "closure_claim": (
            "Every foreign-tax-paid amount reported in box 7 of a Form 1099-DIV "
            "furnished to the taxpayer for tax year 2025 is recorded as a statement "
            "item as of the keyed horizon. This claim covers Form 1099-DIV box 7 only: "
            "it says nothing about boxes 1a, 1b, 2a, or 12, residual recorded "
            "non-composable boxes (3, 5), Form 1099-INT foreign tax, Schedule K-1/K-3 "
            "foreign tax, Schedule 3 completeness, or Form 1040 credit lines. Closed "
            "with members authorizes the multi-payer sum of current members; "
            "closed-empty authorizes subtotal 0."
        ),
        "member_predicate": {"fact_type": BOX7_AMOUNT},
        "authorizes_subtotal": BOX7_SUBTOTAL,
    }


def _mapping() -> dict[str, Any]:
    return {
        "schema": "source-closure-mapping.v2",
        "id": "tax.us.2025.closure-mapping.f1099div-7",
        "version": "v1",
        "family": {"id": BOX7_FAMILY, "version": "v1"},
        "member_fact_type": {"id": BOX7_AMOUNT, "version": "v1"},
        "closure_fact_type": {"id": BOX7_CLOSURE, "version": "v1"},
        "closure_horizon_key": "family-horizon",
        "admits_symbol": BOX7_SUBTOTAL,
        "admission": {"condition": "current-literal-true"},
    }


def _subtotal_rule() -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v3",
        "id": "tax.us.2025.rule.f1099div-7-subtotal",
        "version": "v1",
        "scope": SCOPE,
        "role": "computation",
        "requires": ["rounding.convention"],
        "pins": [
            {
                "role": "input",
                "id": "rounding.convention",
                "version": "v1",
                "origin": "assertion",
            }
        ],
        "when": True,
        "value": {
            "op": "round",
            "value": {
                "op": "add",
                "args": [
                    {
                        "op": "collect",
                        "name": BOX7_AMOUNT,
                        "source_set": BOX7_FAMILY,
                    }
                ],
            },
            "mode": {"op": "ref", "name": "rounding.convention"},
        },
        "publishes": BOX7_SUBTOTAL,
        "citations": [
            {"id": "tax.us.2025.citation.f1099div.box7", "version": "v1"},
        ],
        "blocked": {"code": "OPEN_DEPENDENCY", "missing": ["rounding.convention"]},
        "notes": (
            "Aggregates current successor box-7 foreign-tax-paid findings into the "
            "family subtotal. Closed-empty publishes zero only through current "
            "literal-true closure admitted by the adopted mapping. Never reads residual "
            "recorded-boxes content. Box 7 is a credit source, not income."
        ),
    }


def _mfj_compare() -> dict[str, Any]:
    return {
        "op": "categorical_compare",
        "cmp": "eq",
        "left": {"op": "ref", "name": "filing_status"},
        "right": {
            "op": "category_literal",
            "value": "married_filing_jointly",
            "fact_type": {"id": "tax.us.2025.filing-status", "version": "v1"},
        },
    }


def _threshold_expr() -> dict[str, Any]:
    return {
        "op": "choose",
        "when": _mfj_compare(),
        "then": 600,
        "else": 300,
    }


def _min_subtotal_regular_tax() -> dict[str, Any]:
    return {
        "op": "choose",
        "when": {
            "op": "compare",
            "cmp": "lte",
            "left": {"op": "ref", "name": BOX7_SUBTOTAL},
            "right": {"op": "ref", "name": LINE16},
        },
        "then": {"op": "ref", "name": BOX7_SUBTOTAL},
        "else": {"op": "ref", "name": LINE16},
    }


def _schedule3_line1_rule() -> dict[str, Any]:
    scope_ids = [_scope_id(token) for token, _ in SCOPE_COMPONENTS]
    creditability = [
        _scope_id(t)
        for t in (
            "tax-type-creditable",
            "legal-liability-and-paid",
            "no-refund-rebate-subsidy",
            "no-excluded-income-association",
            "holding-period-16-day-met",
            "no-short-sale-obligation",
            "country-recognized-non-terrorism",
        )
    ]
    associated = [
        _scope_id(t)
        for t in (
            "all-foreign-income-passive",
            "all-foreign-income-on-1099div",
            "no-f1099int-foreign-tax",
            "no-k1-k3-foreign-tax",
            "no-other-foreign-tax-source",
        )
    ]
    election_side = [
        _scope_id(t)
        for t in (
            "no-carryback-carryforward",
            "no-schedule-a-deduction-election",
            "no-form-1116-required",
        )
    ]
    regular_tax_scope = [
        _scope_id(t)
        for t in (
            "no-schedule2-regular-tax-add",
            "no-form-4972-on-line16",
        )
    ]
    requires = [
        BOX7_SUBTOTAL,
        LINE16,
        ELECTION_FACT,
        "filing_status",
        "rounding.convention",
        *scope_ids,
    ]
    when_args: list[dict[str, Any]] = [
        {"op": "require_closed", "source_set": BOX7_FAMILY},
        {
            "op": "categorical_compare",
            "cmp": "eq",
            "left": {"op": "ref", "name": ELECTION_FACT},
            "right": {
                "op": "category_literal",
                "value": "yes",
                "fact_type": {"id": ELECTION_FACT, "version": "v1"},
            },
        },
        {
            "op": "compare",
            "cmp": "lte",
            "left": {"op": "ref", "name": BOX7_SUBTOTAL},
            "right": _threshold_expr(),
        },
    ]
    when_args.extend(_yes_compare(sid) for sid in associated)
    when_args.extend(_yes_compare(sid) for sid in creditability)
    when_args.extend(_yes_compare(sid) for sid in election_side)
    when_args.extend(_yes_compare(sid) for sid in regular_tax_scope)
    return {
        "schema": "rule-artifact.v3",
        "id": "tax.us.2025.rule.schedule3-line1-direct-ftc",
        "version": "v1",
        "scope": SCOPE,
        "role": "computation",
        "requires": requires,
        "pins": [
            {"role": "input", "id": BOX7_SUBTOTAL, "version": "v1", "origin": "assertion"},
            {"role": "input", "id": "tax.us.2025.rule.form1040-line16", "version": "v5", "origin": "assertion"},
            {"role": "input", "id": ELECTION_FACT, "version": "v1", "origin": "assertion"},
            {
                "role": "input",
                "id": "tax.us.2025.filing-status",
                "version": "v1",
                "origin": "assertion",
            },
            {
                "role": "input",
                "id": "rounding.convention",
                "version": "v1",
                "origin": "assertion",
            },
            *[
                {"role": "input", "id": sid, "version": "v1", "origin": "assertion"}
                for sid in scope_ids
            ],
        ],
        "when": {"op": "all", "args": when_args},
        "value": {
            "op": "round",
            "value": _min_subtotal_regular_tax(),
            "mode": {"op": "ref", "name": "rounding.convention"},
        },
        "publishes": SCH3_L1,
        "citations": [
            {"id": "tax.us.2025.citation.schedule3.line1", "version": "v1"},
            {"id": "tax.us.2025.citation.f1099div.box7", "version": "v1"},
            {"id": "tax.us.2025.citation.form1116.direct-election", "version": "v1"},
            {"id": "tax.us.2025.citation.publication-514.ftc", "version": "v1"},
        ],
        "blocked": {
            "code": "DEPENDENCY_ABSENT",
            "missing": requires,
        },
        "notes": (
            "Schedule 3 line 1 direct foreign tax credit without Form 1116 for the "
            "bounded 2025 class: min(closed box-7 subtotal, Form 1040 line 16 regular "
            "tax) only when election=yes, creditability components are yes, associated "
            "income completeness is yes, threshold gate passes (block not clip), and "
            "regular-tax scope absences hold. Threshold is $600 MFJ else $300 including "
            "MFS. Does not implement Form 1116, carryovers, or Schedule A deduction."
        ),
    }


def _schedule3_line8_rule() -> dict[str, Any]:
    absences = [
        _scope_id(t)
        for t in (
            "no-sch3-line2",
            "no-sch3-line3",
            "no-sch3-line4",
            "no-sch3-line5",
            "no-sch3-line6",
        )
    ]
    when_args: list[dict[str, Any]] = [_yes_compare(sid) for sid in absences]
    return {
        "schema": "rule-artifact.v3",
        "id": "tax.us.2025.rule.schedule3-line8",
        "version": "v1",
        "scope": SCOPE,
        "role": "computation",
        "requires": [SCH3_L1, *absences],
        "pins": [
            {"role": "input", "id": SCH3_L1, "version": "v1", "origin": "assertion"},
            *[
                {"role": "input", "id": sid, "version": "v1", "origin": "assertion"}
                for sid in absences
            ],
        ],
        "when": {"op": "all", "args": when_args},
        "value": {"op": "ref", "name": SCH3_L1},
        "publishes": SCH3_L8,
        "citations": [
            {"id": "tax.us.2025.citation.schedule3.line8", "version": "v1"},
        ],
        "blocked": {
            "code": "DEPENDENCY_ABSENT",
            "missing": [SCH3_L1, *absences],
        },
        "notes": (
            "Schedule 3 line 8 for the bounded class equals line 1 only when every "
            "other Schedule 3 Part I credit (lines 2–6) is explicitly absent. No "
            "unsupported credit is silently defaulted to zero."
        ),
    }


def _line20_rule() -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v3",
        "id": "tax.us.2025.rule.form1040-line20",
        "version": "v1",
        "scope": SCOPE,
        "role": "computation",
        "requires": [SCH3_L8],
        "pins": [
            {"role": "input", "id": SCH3_L8, "version": "v1", "origin": "assertion"},
        ],
        "when": True,
        "value": {"op": "ref", "name": SCH3_L8},
        "publishes": L20,
        "citations": [
            {"id": "tax.us.2025.citation.form1040.line-20", "version": "v1"},
        ],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": [SCH3_L8]},
        "notes": (
            "Form 1040 line 20 binds to Schedule 3 line 8 for the bounded "
            "nonrefundable-credit succession. Counts the foreign tax credit once."
        ),
    }


def _tax_after_credit_rule() -> dict[str, Any]:
    absences = [
        _scope_id("no-line17-schedule2-additional"),
        _scope_id("no-line19-ctc-odc"),
    ]
    when_args: list[dict[str, Any]] = [_yes_compare(sid) for sid in absences]
    # line_18 = line_16; line_21 = line_20; line_22 = max(line_18 - line_21, 0)
    return {
        "schema": "rule-artifact.v3",
        "id": "tax.us.2025.rule.form1040-tax-after-credits",
        "version": "v1",
        "scope": SCOPE,
        "role": "computation",
        "requires": [LINE16, L20, *absences, "rounding.convention"],
        "pins": [
            {
                "role": "input",
                "id": "tax.us.2025.rule.form1040-line16",
                "version": "v5",
                "origin": "assertion",
            },
            {"role": "input", "id": L20, "version": "v1", "origin": "assertion"},
            *[
                {"role": "input", "id": sid, "version": "v1", "origin": "assertion"}
                for sid in absences
            ],
            {
                "role": "input",
                "id": "rounding.convention",
                "version": "v1",
                "origin": "assertion",
            },
        ],
        "when": {"op": "all", "args": when_args},
        "value": {
            "op": "round",
            "value": {
                "op": "max",
                "args": [
                    {
                        "op": "subtract",
                        "left": {"op": "ref", "name": LINE16},
                        "right": {"op": "ref", "name": L20},
                    },
                    0,
                ],
            },
            "mode": {"op": "ref", "name": "rounding.convention"},
        },
        "publishes": TAX_AFTER,
        "citations": [
            {"id": "tax.us.2025.citation.form1040.line-22", "version": "v1"},
        ],
        "blocked": {
            "code": "DEPENDENCY_ABSENT",
            "missing": [LINE16, L20, *absences, "rounding.convention"],
        },
        "notes": (
            "Bounded tax after nonrefundable credits: max(line_16 - line_20, 0) when "
            "line 17 and line 19 are explicitly absent so line_18 = line_16 and "
            "line_21 = line_20. Preserves tax.us.2025.tax.total-tax as line-16 regular "
            "tax; never overwrites that symbol. Floors at zero; never negative tax."
        ),
    }


def _field(
    *,
    field_id: str,
    line: str,
    label: str,
    form_id: str,
    binds: str,
    citation_id: str,
    description: str,
    published_explain: str,
    blocked_explain: str,
) -> dict[str, Any]:
    return {
        "schema": "form-field.v3",
        "id": field_id,
        "version": "v1",
        "form": {
            "authority": "IRS",
            "form_id": form_id,
            "tax_year": 2025,
            "jurisdiction": "US-federal",
        },
        "line": line,
        "label": label,
        "description": description,
        "binds_symbol": binds,
        "citation": {"id": citation_id, "version": "v1"},
        "dispositions": {
            "published_value": {
                "render": "{value}",
                "explain": published_explain,
            },
            "computed_zero": {
                "render": "0",
                "explain": "A current derived finding publishes a computed zero.",
            },
            "closure_backed_zero": {
                "render": "0",
                "explain": (
                    "A current derived finding publishes zero through honest closed-empty "
                    "or zero-credit authority on the direct-election path."
                ),
            },
            "blocked": {
                "render": "",
                "explain": blocked_explain,
                "codes": [
                    "DEPENDENCY_ABSENT",
                    "DEPENDENCY_INVALID",
                    "CATEGORICAL_DOMAIN_MISMATCH",
                    "SOURCE_SET_UNCLOSED",
                ],
            },
            "guard_inapplicable": {
                "render": "",
                "explain": (
                    "No value is published because a scope, election, threshold, or "
                    "creditability component is not satisfied for the bounded class."
                ),
            },
        },
    }


def _fields() -> dict[str, dict[str, Any]]:
    return {
        "schedule3.line-1.form-field.json": _field(
            field_id="tax.us.2025.schedule3.line-1",
            line="Sch3-1",
            label="Foreign tax credit",
            form_id="1040-Schedule-3",
            binds=SCH3_L1,
            citation_id="tax.us.2025.citation.schedule3.line1",
            description=(
                "Schedule 3 (Form 1040) Part I line 1: foreign tax credit under the "
                "direct election without Form 1116 for the bounded 2025 Form 1099-DIV "
                "box-7 class. Equals min(creditable box-7 subtotal, Form 1040 line 16) "
                "when election, creditability, associated-income, and threshold "
                "authorities hold. Does not complete Form 1116."
            ),
            published_explain=(
                "Direct foreign tax credit without Form 1116: published from closed "
                "box-7 foreign tax paid, under named creditability and election "
                "authority, capped at regular tax (Form 1040 line 16)."
            ),
            blocked_explain=(
                "Schedule 3 line 1 is blocked because election, creditability, "
                "associated-income, threshold, closure, or regular-tax scope authority "
                "is incomplete or failed."
            ),
        ),
        "schedule3.line-8.form-field.json": _field(
            field_id="tax.us.2025.schedule3.line-8",
            line="Sch3-8",
            label="Total other nonrefundable credits",
            form_id="1040-Schedule-3",
            binds=SCH3_L8,
            citation_id="tax.us.2025.citation.schedule3.line8",
            description=(
                "Schedule 3 (Form 1040) line 8: total of Part I for the bounded class "
                "equals line 1 when every other Part I credit is explicitly absent."
            ),
            published_explain=(
                "Schedule 3 line 8 equals line 1 under explicit absence of other Part I "
                "credits; carries to Form 1040 line 20."
            ),
            blocked_explain=(
                "Schedule 3 line 8 is blocked because line 1 is blocked or another Part I "
                "credit absence authority is incomplete."
            ),
        ),
        "form1040.line-20.form-field.json": _field(
            field_id="tax.us.2025.form1040.line-20",
            line="20",
            label="Other nonrefundable credits from Schedule 3",
            form_id="1040",
            binds=L20,
            citation_id="tax.us.2025.citation.form1040.line-20",
            description=(
                "Form 1040 line 20: nonrefundable credits from Schedule 3 line 8 for the "
                "bounded direct foreign-tax-credit class."
            ),
            published_explain=(
                "Form 1040 line 20 equals Schedule 3 line 8 (direct foreign tax credit "
                "without Form 1116 for the bounded class)."
            ),
            blocked_explain="Form 1040 line 20 is blocked because Schedule 3 line 8 is blocked.",
        ),
        "form1040.tax-after-credits.form-field.json": _field(
            field_id="tax.us.2025.form1040.tax-after-credits",
            line="22",
            label="Tax after nonrefundable credits",
            form_id="1040",
            binds=TAX_AFTER,
            citation_id="tax.us.2025.citation.form1040.line-22",
            description=(
                "Form 1040 bounded tax after nonrefundable credits: max(line 16 − line 20, 0) "
                "when line 17 and line 19 are explicitly absent. Distinct from "
                "tax.us.2025.tax.total-tax (line 16 regular tax)."
            ),
            published_explain=(
                "Tax after nonrefundable credits floors at zero: line 16 regular tax minus "
                "line 20 credits under line 17/19 absence. Line 16 meaning is preserved."
            ),
            blocked_explain=(
                "Tax after credits is blocked because line 16, line 20, or line 17/19 "
                "absence authority is incomplete."
            ),
        ),
    }


def _dividend_universe_v4() -> dict[str, Any]:
    return {
        "schema": "dividend-universe.v4",
        "id": "tax.us.2025.dividend-universe",
        "version": "v4",
        "title": (
            "Successor Form 1099-DIV box universe for tax year 2025 with composable "
            "boxes 2a, 12, and 7"
        ),
        "scope": SCOPE,
        "composable_boxes": [
            {"box": "1a", "family": {"id": "tax.us.2025.f1099div.1a", "version": "v1"}},
            {"box": "1b", "family": {"id": "tax.us.2025.f1099div.1b", "version": "v1"}},
            {"box": "2a", "family": {"id": "tax.us.2025.f1099div.2a", "version": "v1"}},
            {"box": "12", "family": {"id": "tax.us.2025.f1099div.12", "version": "v1"}},
            {"box": "7", "family": {"id": BOX7_FAMILY, "version": "v1"}},
        ],
        "recorded_non_composable_boxes": ["3", "5"],
        "recorded_boxes_fact_type": {
            "id": "tax.us.2025.f1099div.recorded-boxes",
            "version": "v4",
        },
        "capital_gain_signal": {
            "box": "2a",
            "signal": "CAPITAL_GAIN_DISTRIBUTION_RECORDED",
            "source": "current_successor_family_member",
        },
    }


def _citations() -> dict[str, dict[str, Any]]:
    return {
        "citation.f1099div.box7.json": {
            "schema": "citation.v1",
            "id": "tax.us.2025.citation.f1099div.box7",
            "version": "v1",
            "authority": {
                "family": "irs-instructions",
                "form_id": "1099-DIV",
                "tax_year": 2025,
            },
        },
        "citation.schedule3.line1.json": {
            "schema": "citation.v1",
            "id": "tax.us.2025.citation.schedule3.line1",
            "version": "v1",
            "authority": {
                "family": "irs-instructions",
                "form_id": "1040",
                "tax_year": 2025,
            },
        },
        "citation.schedule3.line8.json": {
            "schema": "citation.v1",
            "id": "tax.us.2025.citation.schedule3.line8",
            "version": "v1",
            "authority": {
                "family": "irs-form",
                "form_id": "1040-Schedule-3",
                "tax_year": 2025,
            },
        },
        "citation.form1040.line-20.json": {
            "schema": "citation.v1",
            "id": "tax.us.2025.citation.form1040.line-20",
            "version": "v1",
            "authority": {
                "family": "irs-instructions",
                "form_id": "1040",
                "tax_year": 2025,
            },
        },
        "citation.form1040.line-22.json": {
            "schema": "citation.v1",
            "id": "tax.us.2025.citation.form1040.line-22",
            "version": "v1",
            "authority": {
                "family": "irs-instructions",
                "form_id": "1040",
                "tax_year": 2025,
            },
        },
        "citation.form1116.direct-election.json": {
            "schema": "citation.v1",
            "id": "tax.us.2025.citation.form1116.direct-election",
            "version": "v1",
            "authority": {
                "family": "irs-instructions",
                "form_id": "1116",
                "tax_year": 2025,
            },
        },
        "citation.publication-514.ftc.json": {
            "schema": "citation.v1",
            "id": "tax.us.2025.citation.publication-514.ftc",
            "version": "v1",
            "authority": {
                "family": "irs-publication",
                "publication": "514",
                "revision": "2025",
            },
        },
    }


def _quantity() -> dict[str, Any]:
    return {
        "schema": "quantity-vocabulary.v10",
        "id": "tax.us.2025.quantity.foreign-tax-paid",
        "version": "v1",
        "quantities": ["foreign-tax-paid"],
    }


def _package_v21(citizens: dict[str, dict[str, Any]]) -> dict[str, Any]:
    # Successor of ratified main tip core v20 (after 8949 / box-8 / 1099-G).
    package = _load(CONTENT / "package.core-calculations.v20.json")
    package = copy.deepcopy(package)
    package["schema"] = "artifact-package.v18"
    package["version"] = "v21"
    package["admitted_schemas"] = sorted(
        set(package["admitted_schemas"])
        | {
            "dividend-universe.v4",
            "quantity-vocabulary.v10",
        }
    )

    replacements: dict[str, dict[str, Any]] = {
        "tax.us.2025.dividend-universe": {
            "role": "dividend-universe",
            "schema": "dividend-universe.v4",
            "version": "v4",
        },
        BOX12_BUNDLE: {
            "role": "fact-type-bundle",
            "schema": "bundle.v2",
            "version": "v2",
        },
    }
    members: list[dict[str, Any]] = []
    changed: list[dict[str, Any]] = []
    for member in package["members"]:
        rep = replacements.get(member["id"])
        if rep:
            changed.append({"id": member["id"], **rep})
        else:
            members.append(dict(member))

    additions = [
        {"id": BOX7_BUNDLE, "role": "fact-type-bundle", "schema": "bundle.v2", "version": "v1"},
        {
            "id": DIRECT_FTC_SCOPE,
            "role": "fact-type-bundle",
            "schema": "bundle.v2",
            "version": "v1",
        },
        {"id": BOX7_FAMILY, "role": "source-family", "schema": "source-family.v1", "version": "v1"},
        {
            "id": "tax.us.2025.closure-mapping.f1099div-7",
            "role": "source-closure-mapping",
            "schema": "source-closure-mapping.v2",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.rule.f1099div-7-subtotal",
            "role": "computation",
            "schema": "rule-artifact.v3",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.rule.schedule3-line1-direct-ftc",
            "role": "computation",
            "schema": "rule-artifact.v3",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.rule.schedule3-line8",
            "role": "computation",
            "schema": "rule-artifact.v3",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.rule.form1040-line20",
            "role": "computation",
            "schema": "rule-artifact.v3",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.rule.form1040-tax-after-credits",
            "role": "computation",
            "schema": "rule-artifact.v3",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.schedule3.line-1",
            "role": "form-field",
            "schema": "form-field.v3",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.schedule3.line-8",
            "role": "form-field",
            "schema": "form-field.v3",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.form1040.line-20",
            "role": "form-field",
            "schema": "form-field.v3",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.form1040.tax-after-credits",
            "role": "form-field",
            "schema": "form-field.v3",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.citation.f1099div.box7",
            "role": "citation",
            "schema": "citation.v1",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.citation.schedule3.line1",
            "role": "citation",
            "schema": "citation.v1",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.citation.schedule3.line8",
            "role": "citation",
            "schema": "citation.v1",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.citation.form1040.line-20",
            "role": "citation",
            "schema": "citation.v1",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.citation.form1040.line-22",
            "role": "citation",
            "schema": "citation.v1",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.citation.form1116.direct-election",
            "role": "citation",
            "schema": "citation.v1",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.citation.publication-514.ftc",
            "role": "citation",
            "schema": "citation.v1",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.quantity.foreign-tax-paid",
            "role": "parameter",
            "schema": "quantity-vocabulary.v10",
            "version": "v1",
        },
    ]
    existing = {(m["id"], m["version"]) for m in members} | {
        (m["id"], m["version"]) for m in changed
    }
    for add in additions:
        key = (add["id"], add["version"])
        if key not in existing:
            changed.append(add)
            existing.add(key)

    package["members"] = members + sorted(changed, key=lambda m: (m["id"], m["version"]))

    entrypoints: list[dict[str, Any]] = []
    for entry in package["entrypoints"]:
        if entry["id"] == "tax.us.2025.dividend-universe":
            entrypoints.append({"id": entry["id"], "version": "v4"})
        elif entry["id"] == BOX12_BUNDLE:
            entrypoints.append({"id": entry["id"], "version": "v2"})
        else:
            entrypoints.append(dict(entry))
    entry_ids = {e["id"] for e in entrypoints}
    for eid, ever in [
        (BOX7_BUNDLE, "v1"),
        (DIRECT_FTC_SCOPE, "v1"),
        ("tax.us.2025.rule.f1099div-7-subtotal", "v1"),
        ("tax.us.2025.rule.schedule3-line1-direct-ftc", "v1"),
        ("tax.us.2025.rule.schedule3-line8", "v1"),
        ("tax.us.2025.rule.form1040-line20", "v1"),
        ("tax.us.2025.rule.form1040-tax-after-credits", "v1"),
    ]:
        if eid not in entry_ids:
            entrypoints.append({"id": eid, "version": ever})
    package["entrypoints"] = entrypoints
    package["package_checksum"] = _package_checksum(package)
    return package


def render_content_files() -> dict[str, dict[str, Any]]:
    citizens: dict[str, dict[str, Any]] = {}
    citizens["f1099div-box12.bundle.v2.json"] = _box12_bundle_v2()
    citizens["f1099div-box7.bundle.json"] = _box7_bundle()
    citizens["direct-ftc-scope.bundle.json"] = _scope_bundle()
    citizens["family.f1099div-7.json"] = _family()
    citizens["closure-mapping.f1099div-7.json"] = _mapping()
    citizens["rule.f1099div-7-subtotal.json"] = _subtotal_rule()
    citizens["rule.schedule3-line1-direct-ftc.json"] = _schedule3_line1_rule()
    citizens["rule.schedule3-line8.json"] = _schedule3_line8_rule()
    citizens["rule.form1040-line20.json"] = _line20_rule()
    citizens["rule.form1040-tax-after-credits.json"] = _tax_after_credit_rule()
    citizens["dividend-universe.v4.json"] = _dividend_universe_v4()
    citizens["quantity.foreign-tax-paid.json"] = _quantity()
    citizens.update(_citations())
    citizens.update(_fields())

    package = _package_v21(citizens)
    citizens["package.core-calculations.v21.json"] = package

    registry = _load(CONTENT / "published-packages.v15.json")
    registry = copy.deepcopy(registry)
    existing_citizens = {(c["id"], c["version"]) for c in registry["citizens"]}
    for citizen in citizens.values():
        if str(citizen.get("schema", "")).startswith("artifact-package."):
            continue
        key = (citizen["id"], citizen["version"])
        if key not in existing_citizens:
            registry["citizens"].append(
                {
                    "id": citizen["id"],
                    "version": citizen["version"],
                    "checksum": _checksum(citizen),
                }
            )
            existing_citizens.add(key)
    registry["citizens"] = sorted(
        registry["citizens"], key=lambda row: (row["id"], row["version"])
    )
    existing_pkgs = {(p["id"], p["version"]) for p in registry["packages"]}
    if (package["id"], "v21") not in existing_pkgs:
        registry["packages"].append(
            {
                "id": package["id"],
                "version": "v21",
                "checksum": package["package_checksum"],
            }
        )
    registry["packages"] = sorted(
        registry["packages"], key=lambda row: (row["id"], row["version"])
    )
    citizens["published-packages.v16.json"] = registry
    return citizens


def render_fixture_files(citizens: dict[str, dict[str, Any]]) -> dict[Path, bytes]:
    registry_bytes = _document(citizens["published-packages.v16.json"])
    package = citizens["package.core-calculations.v21.json"]
    release = {
        "schema": "release-registry.v1",
        "id": "demo.release.2025",
        "version": "v14",
        "package_registry_sha256": hashlib.sha256(registry_bytes).hexdigest(),
    }
    release_bytes = _document(release)
    adoption = {
        "schema": "act.v1",
        "act_id": "demo.act.adopt.core.v21",
        "kind": "package-adoption",
        "actor": "demo.user.filer-1",
        "at": "2026-08-05T12:00:00Z",
        "committed_against": 1,
        "payload": {
            "package": {
                "id": package["id"],
                "version": "v21",
                "checksum": package["package_checksum"],
            },
            "release": {
                "id": "demo.release.2025",
                "version": "v14",
                "checksum": hashlib.sha256(release_bytes).hexdigest(),
            },
            "scope": {"jurisdiction": "us", "year": "2025"},
            "revision": 21,
            "supersedes": "demo.act.adopt.core.v20",
            "audit": {
                "note": (
                    "synthetic Form 1099-DIV box-7 direct FTC; package v21 union "
                    "of v20; non-authoritative"
                )
            },
        },
    }
    return {
        FIXTURES
        / "publication_surface"
        / "releases"
        / "demo.release.2025.v14.json": release_bytes,
        FIXTURES / "adoptions" / "adopt-core-v21-current.json": _document(adoption),
    }


def render_all() -> dict[Path, bytes]:
    citizens = render_content_files()
    content_files = {CONTENT / name: _document(value) for name, value in citizens.items()}
    return {**content_files, **render_fixture_files(citizens)}


def main() -> None:
    files = render_all()
    for path, body in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
    print(f"wrote {len(files)} files")


if __name__ == "__main__":
    main()
