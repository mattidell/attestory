"""Generate Form 1099-G box 1 → Schedule 1 line 7 / Form 1040 line 8 content.

Reads the ratified core-calculations@v17 / published-packages@v12 graph and
writes only new content citizens plus package v20, published-packages v15,
release v13, and adoption v20. Historical packages, schemas, and registries
remain byte-for-byte.

Track 0 binding (plan defaults): Alternative A Schedule 1 line-10 completeness;
box-4 null/zero companion; residual via tax-year absence authorities; line-9 v5
adds published line 8 exactly once; Schedule 1 attachment citizen (ADR-0036).
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
FIXTURES = ROOT / "packages" / "sample_data" / "form1099g_box1_schedule1_line7"

SCOPE = {
    "tax_year": 2025,
    "jurisdiction": "US-federal",
    "family": "individual-income-tax",
}

# Source family
BOX1_AMOUNT = "tax.us.2025.f1099g.box1-unemployment"
BOX1_CLOSURE = "tax.us.2025.f1099g.1.source-closure"
BOX1_FAMILY = "tax.us.2025.f1099g.1"
BOX1_SUBTOTAL = "tax.us.2025.unemployment.box1-subtotal"
BOX4_AUTH = "tax.us.2025.f1099g.box4-federal-withholding-authority"
BOX1_BUNDLE = "tax.us.2025.f1099g.box1.vocabulary"
QUANTITY_ID = "tax.us.2025.quantity.unemployment-compensation"

# Residual / repayment / Schedule 1 Part I absence scope
SCH1_SCOPE_BUNDLE = "tax.us.2025.schedule1-part1-scope.vocabulary"
SCH1_SCOPE_PREFIX = "tax.us.2025.schedule1-part1-scope"

SCOPE_COMPONENTS: tuple[tuple[str, str], ...] = (
    (
        "no-sch1-line1-taxable-refunds",
        "No Schedule 1 line 1 taxable refunds, credits, or offsets of state and "
        "local income taxes are present for the bounded additional-income claim.",
    ),
    (
        "no-sch1-line2a-alimony",
        "No Schedule 1 line 2a alimony received is present for the bounded "
        "additional-income claim.",
    ),
    (
        "no-sch1-line3-business",
        "No Schedule 1 line 3 business income or loss is present for the bounded "
        "additional-income claim.",
    ),
    (
        "no-sch1-line4-other-gains",
        "No Schedule 1 line 4 other gains or losses are present for the bounded "
        "additional-income claim.",
    ),
    (
        "no-sch1-line5-rental",
        "No Schedule 1 line 5 rental real estate, royalties, partnerships, S "
        "corporations, trusts, etc. income is present for the bounded "
        "additional-income claim.",
    ),
    (
        "no-sch1-line6-farm",
        "No Schedule 1 line 6 farm income or loss is present for the bounded "
        "additional-income claim.",
    ),
    (
        "no-sch1-other-income",
        "No Schedule 1 other income (lines 8a–8z / line 9 aggregate) is present "
        "for the bounded additional-income claim.",
    ),
    (
        "no-unemployment-repayment",
        "No unemployment compensation repayment of prior- or current-year "
        "overpayment is present for the bounded unemployment claim. Correction of "
        "a statement uses free supersession; repayment is unsupported and blocks.",
    ),
    (
        "no-f1099g-box2-state-refund",
        "No Form 1099-G box 2 state or local income tax refund, credit, or offset "
        "is present for the bounded unemployment claim. Box-1 family closure never "
        "proves box 2 absent.",
    ),
    (
        "no-f1099g-other-payment-classes",
        "No Form 1099-G boxes 5–7 or 9 (RTAA, taxable grants, agriculture payments, "
        "market gain) or other co-occurring unsupported 1099-G payment classes are "
        "present for the bounded unemployment claim. Box-1 closure never proves "
        "other boxes absent.",
    ),
)

# Schedule 1 / Form 1040 symbols
LINE7_TOTAL = "tax.us.2025.schedule1.line7-unemployment"
LINE7_RULE = "tax.us.2025.rule.schedule1-line7"
LINE7_FIELD = "tax.us.2025.schedule1.line-7"
LINE10_TOTAL = "tax.us.2025.schedule1.line10-additional-income"
LINE10_RULE = "tax.us.2025.rule.schedule1-line10"
LINE10_FIELD = "tax.us.2025.schedule1.line-10"
LINE8_TOTAL = "tax.us.2025.income.additional-income"  # Form 1040 line 8
LINE8_RULE = "tax.us.2025.rule.form1040-line8"
LINE8_FIELD = "tax.us.2025.form1040.line-8"
LINE9_RULE = "tax.us.2025.rule.form1040-line9"
ATTACHMENT_RULE = "tax.us.2025.rule.attachment.schedule-1"
ATTACHMENT_DISPOSITION = "tax.us.2025.schedule1.disposition"


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
    return f"{SCH1_SCOPE_PREFIX}.{token}"


def _statement_keys() -> list[dict[str, Any]]:
    return [
        {
            "name": "payer",
            "kind": "entity",
            "entity_kind": "tax.us.unemployment-payer",
        },
        {
            "name": "statement",
            "kind": "entity",
            "entity_kind": "tax.us.1099g-statement",
        },
        {"name": "tax-year", "kind": "literal", "values": ["2025"]},
    ]


def _box1_bundle() -> dict[str, Any]:
    return {
        "schema": "bundle.v2",
        "id": BOX1_BUNDLE,
        "version": "v1",
        "label": (
            "Form 1099-G box-1 unemployment compensation and box-4 federal "
            "withholding absence/zero companion for tax year 2025"
        ),
        "fact_types": [
            {
                "schema": "fact-type.v2",
                "id": BOX1_AMOUNT,
                "version": "v1",
                "title": (
                    "Unemployment compensation reported in box 1 of one logical "
                    "Form 1099-G statement instance furnished by a payer/agency "
                    "for 2025; the statement instance is peer to evidence and its "
                    "identity carries no file, upload, scan, document, or evidence "
                    "key (ADR-0015). Multiple originals from one payer are distinct "
                    "statement instances; a corrected copy of the same logical "
                    "return answers this same fact and supersedes its prior finding. "
                    "Nonnegative source amount only. Never absorbs box 2 or boxes "
                    "5–7/9 payment classes."
                ),
                "nature": "determinable",
                "identity_keys": _statement_keys(),
                "value_schema": {"type": "number", "minimum": 0},
                "supersession": {"policy": "free"},
                "source_amount": True,
                "quantity": {"id": QUANTITY_ID, "version": "v1"},
            },
            {
                "schema": "fact-type.v2",
                "id": BOX1_CLOSURE,
                "version": "v1",
                "title": (
                    "User-attested closure of the Form 1099-G box-1 source family for "
                    "2025, keyed on the family membership horizon current at "
                    "attestation (ADR-0017): true asserts every furnished 1099-G "
                    "box-1 unemployment amount is recorded as of that horizon. This "
                    "claim covers box 1 only — never box 2, boxes 5–7/9, box 4 "
                    "withholding computation, Schedule 1 completeness, or Form 1040 "
                    "line 8. A later membership transition displaces this closure "
                    "through horizon succession; re-attestation on the successor "
                    "horizon is required."
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
                "id": BOX4_AUTH,
                "version": "v1",
                "title": (
                    "Explicit companion authority for Form 1099-G box 4 (federal "
                    "income tax withheld) on the same logical statement as a box-1 "
                    "member. Only explicit null (absent) or numeric zero is "
                    "admissible on the bounded unemployment route. A nonzero value "
                    "is a hard admission block and never creates Form 1040 line 25b "
                    "or any payments computation. This is an authority witness, not "
                    "a composed amount and never reduces box-1 income."
                ),
                "nature": "determinable",
                "identity_keys": _statement_keys(),
                "value_schema": {"anyOf": [{"type": "null"}, {"const": 0}]},
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
                    f"Schedule 1 / Form 1099-G residual scope completeness "
                    f"component: {title} Contributed categorical assertion, domain "
                    "{yes, no}, no default, presence-before-value, free supersession. "
                    "yes asserts the named excluded source or dependency is absent; "
                    "no asserts it is present and blocks the bounded additional-income "
                    "claim. Absence is not a manufactured zero amount for an "
                    "unimplemented producer."
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
        "id": SCH1_SCOPE_BUNDLE,
        "version": "v1",
        "label": (
            "Schedule 1 Part I absence authorities, unemployment repayment block, "
            "and Form 1099-G residual absence authorities for the bounded 2025 "
            "additional-income (line 8) claim"
        ),
        "fact_types": fact_types,
    }


def _family() -> dict[str, Any]:
    return {
        "schema": "source-family.v1",
        "id": BOX1_FAMILY,
        "version": "v1",
        "title": "Form 1099-G box 1 unemployment compensation statement items, tax year 2025",
        "scope": SCOPE,
        "closure_claim": (
            "Every unemployment compensation amount reported in box 1 of a Form "
            "1099-G furnished to the taxpayer for tax year 2025 is recorded as a "
            "statement item as of the keyed horizon. This claim covers Form 1099-G "
            "box 1 only: it says nothing about box 2 state/local refunds, boxes "
            "5–7 or 9, box 4 withholding, unemployment repayments, other Schedule 1 "
            "income classes, or Form 1040 line 8 completeness. Closed with members "
            "authorizes the multi-payer sum of current members; closed-empty "
            "authorizes subtotal 0."
        ),
        "member_predicate": {"fact_type": BOX1_AMOUNT},
        "authorizes_subtotal": BOX1_SUBTOTAL,
    }


def _mapping() -> dict[str, Any]:
    return {
        "schema": "source-closure-mapping.v2",
        "id": "tax.us.2025.closure-mapping.f1099g-1",
        "version": "v1",
        "family": {"id": BOX1_FAMILY, "version": "v1"},
        "member_fact_type": {"id": BOX1_AMOUNT, "version": "v1"},
        "closure_fact_type": {"id": BOX1_CLOSURE, "version": "v1"},
        "closure_horizon_key": "family-horizon",
        "admits_symbol": BOX1_SUBTOTAL,
        "admission": {"condition": "current-literal-true"},
    }


def _subtotal_rule() -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v3",
        "id": "tax.us.2025.rule.f1099g-1-subtotal",
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
                        "name": BOX1_AMOUNT,
                        "source_set": BOX1_FAMILY,
                    }
                ],
            },
            "mode": {"op": "ref", "name": "rounding.convention"},
        },
        "publishes": BOX1_SUBTOTAL,
        "citations": [
            {"id": "tax.us.2025.citation.f1099g.box1", "version": "v1"},
        ],
        "blocked": {"code": "OPEN_DEPENDENCY", "missing": ["rounding.convention"]},
        "notes": (
            "Aggregates current Form 1099-G box-1 unemployment findings into the "
            "family subtotal. Closed-empty publishes zero only through current "
            "literal-true closure admitted by the adopted mapping. Never reads box "
            "4, residual boxes, or Schedule 1 absence authorities."
        ),
    }


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


def _scope_ids() -> list[str]:
    return [_scope_id(token) for token, _ in SCOPE_COMPONENTS]


def _line7_rule() -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v3",
        "id": LINE7_RULE,
        "version": "v1",
        "scope": SCOPE,
        "role": "computation",
        "requires": [BOX1_SUBTOTAL],
        "pins": [
            {
                "role": "input",
                "id": BOX1_SUBTOTAL,
                "version": "v1",
                "origin": "assertion",
            }
        ],
        "when": {
            "op": "require_closed",
            "source_set": BOX1_FAMILY,
        },
        "value": {"op": "ref", "name": BOX1_SUBTOTAL},
        "publishes": LINE7_TOTAL,
        "citations": [
            {"id": "tax.us.2025.citation.schedule1.line-7", "version": "v1"},
            {"id": "tax.us.2025.citation.f1099g.box1", "version": "v1"},
        ],
        "blocked": {
            "code": "DEPENDENCY_ABSENT",
            "missing": [BOX1_SUBTOTAL],
        },
        "notes": (
            "Schedule 1 (Form 1040) line 7 for the bounded 2025 class: equals the "
            "closed Form 1099-G box-1 family subtotal. Box-1 family closure alone "
            "never asserts general Schedule 1 completeness. Box-4 companion is "
            "enforced at admission. Does not implement repayment arithmetic."
        ),
    }


def _line10_rule() -> dict[str, Any]:
    scope_ids = _scope_ids()
    when_args: list[dict[str, Any]] = [
        {"op": "require_closed", "source_set": BOX1_FAMILY},
    ]
    when_args.extend(_yes_compare(sid) for sid in scope_ids)
    return {
        "schema": "rule-artifact.v3",
        "id": LINE10_RULE,
        "version": "v1",
        "scope": SCOPE,
        "role": "computation",
        "requires": [LINE7_TOTAL, *scope_ids],
        "pins": [
            {
                "role": "input",
                "id": LINE7_TOTAL,
                "version": "v1",
                "origin": "assertion",
            },
            *[
                {"role": "input", "id": sid, "version": "v1", "origin": "assertion"}
                for sid in scope_ids
            ],
        ],
        "when": {"op": "all", "args": when_args},
        "value": {"op": "ref", "name": LINE7_TOTAL},
        "publishes": LINE10_TOTAL,
        "citations": [
            {"id": "tax.us.2025.citation.schedule1.line-10", "version": "v1"},
            {"id": "tax.us.2025.citation.schedule1.line-7", "version": "v1"},
        ],
        "blocked": {
            "code": "DEPENDENCY_ABSENT",
            "missing": [LINE7_TOTAL, *scope_ids],
        },
        "notes": (
            "Schedule 1 line 10 Alternative A for the bounded 2025 class: equals "
            "closed unemployment (line 7) only when every unsupported Schedule 1 "
            "Part I income class (lines 1, 2a, 3, 4, 5, 6, other-income 8/9), "
            "unemployment repayment, and residual Form 1099-G payment classes are "
            "explicitly declared absent (yes). Closed-empty unemployment with "
            "complete absences publishes explicit zero. Does not manufacture zero "
            "amounts for unimplemented producers. Not a general Schedule 1 claim."
        ),
    }


def _line8_rule() -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v3",
        "id": LINE8_RULE,
        "version": "v1",
        "scope": SCOPE,
        "role": "computation",
        "requires": [LINE10_TOTAL],
        "pins": [
            {
                "role": "input",
                "id": LINE10_TOTAL,
                "version": "v1",
                "origin": "assertion",
            }
        ],
        "when": True,
        "value": {"op": "ref", "name": LINE10_TOTAL},
        "publishes": LINE8_TOTAL,
        "citations": [
            {"id": "tax.us.2025.citation.form1040.line-8", "version": "v1"},
            {"id": "tax.us.2025.citation.schedule1.line-10", "version": "v1"},
        ],
        "blocked": {
            "code": "DEPENDENCY_ABSENT",
            "missing": [LINE10_TOTAL],
        },
        "notes": (
            "Form 1040 line 8 for the bounded 2025 class: equals complete Schedule 1 "
            "line 10 additional income. Published once into line-9 v5. Closed-empty "
            "with complete absences yields explicit zero rather than silent omission."
        ),
    }


def _line9_v5() -> dict[str, Any]:
    return {
        "blocked": {
            "code": "DEPENDENCY_ABSENT",
            "missing": [
                "tax.us.2025.wages.total-w2-box1",
                "tax.us.2025.interest.taxable-total",
                "tax.us.2025.dividends.ordinary-total",
                "tax.us.2025.capital-gains.line7a-total",
                LINE8_TOTAL,
            ],
        },
        "citations": [
            {
                "id": "tax.us.2025.citation.form1040.line-9",
                "version": "v1",
            }
        ],
        "id": LINE9_RULE,
        "notes": (
            "Form 1040 Line 9 v5: total income adds the published Form 1040 line 8 "
            "(complete Schedule 1 line 10 / additional income) exactly once to the "
            "existing four components from v4 (wages, taxable interest, ordinary "
            "dividends, selected line-7a). Does not read raw Form 1099-G box-1 "
            "members, Schedule 1 line 7 raw subtotal twice, or line 2a. Historical "
            "v1–v4 remain immutable."
        ),
        "pins": [
            {
                "id": "tax.us.2025.wages.total-w2-box1",
                "origin": "assertion",
                "role": "input",
                "version": "v1",
            },
            {
                "id": "tax.us.2025.interest.taxable-total",
                "origin": "assertion",
                "role": "input",
                "version": "v1",
            },
            {
                "id": "tax.us.2025.dividends.ordinary-total",
                "origin": "assertion",
                "role": "input",
                "version": "v1",
            },
            {
                "id": "tax.us.2025.capital-gains.line7a-total",
                "origin": "assertion",
                "role": "input",
                "version": "v1",
            },
            {
                "id": LINE8_TOTAL,
                "origin": "assertion",
                "role": "input",
                "version": "v1",
            },
        ],
        "publishes": "tax.us.2025.income.total-income",
        "requires": [
            "tax.us.2025.wages.total-w2-box1",
            "tax.us.2025.interest.taxable-total",
            "tax.us.2025.dividends.ordinary-total",
            "tax.us.2025.capital-gains.line7a-total",
            LINE8_TOTAL,
        ],
        "role": "computation",
        "schema": "rule-artifact.v2",
        "scope": SCOPE,
        "value": {
            "args": [
                {"name": "tax.us.2025.wages.total-w2-box1", "op": "ref"},
                {"name": "tax.us.2025.interest.taxable-total", "op": "ref"},
                {"name": "tax.us.2025.dividends.ordinary-total", "op": "ref"},
                {"name": "tax.us.2025.capital-gains.line7a-total", "op": "ref"},
                {"name": LINE8_TOTAL, "op": "ref"},
            ],
            "op": "add",
        },
        "version": "v5",
        "when": True,
    }


def _field_dispositions(
    *,
    published_explain: str,
    blocked_explain: str,
    codes: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "published_value": {
            "render": "{value}",
            "explain": published_explain,
        },
        "computed_zero": {
            "render": "0",
            "explain": "A current derived finding publishes a computed zero under complete authority.",
        },
        "closure_backed_zero": {
            "render": "0",
            "explain": (
                "A current derived finding publishes zero because the supporting "
                "source family is attested closed-empty under complete authority."
            ),
        },
        "blocked": {
            "render": "",
            "explain": blocked_explain,
            "codes": codes
            or [
                "DEPENDENCY_ABSENT",
                "DEPENDENCY_INVALID",
                "CATEGORICAL_DOMAIN_MISMATCH",
                "SOURCE_SET_UNCLOSED",
            ],
        },
        "guard_inapplicable": {
            "render": "",
            "explain": (
                "No value is published because a completeness or guard condition "
                "is not satisfied."
            ),
        },
    }


def _line7_field() -> dict[str, Any]:
    return {
        "schema": "form-field.v3",
        "id": LINE7_FIELD,
        "version": "v1",
        "form": {
            "authority": "IRS",
            "form_id": "1040-SCH-1",
            "tax_year": 2025,
            "jurisdiction": "US-federal",
        },
        "line": "sch1-7",
        "label": "Unemployment compensation",
        "description": (
            "Schedule 1 (Form 1040) 2025, line 7: unemployment compensation from "
            "the closed Form 1099-G box-1 family for the bounded class. Does not "
            "implement repayment checkbox arithmetic or general Schedule 1 income."
        ),
        "binds_symbol": LINE7_TOTAL,
        "citation": {
            "id": "tax.us.2025.citation.schedule1.line-7",
            "version": "v1",
        },
        "dispositions": _field_dispositions(
            published_explain=(
                "A current derived finding publishes this unemployment compensation "
                "amount on Schedule 1 line 7 from the closed Form 1099-G box-1 family."
            ),
            blocked_explain=(
                "Schedule 1 line 7 is blocked because the box-1 family is unclosed "
                "or its subtotal is unavailable."
            ),
        ),
    }


def _line10_field() -> dict[str, Any]:
    return {
        "schema": "form-field.v3",
        "id": LINE10_FIELD,
        "version": "v1",
        "form": {
            "authority": "IRS",
            "form_id": "1040-SCH-1",
            "tax_year": 2025,
            "jurisdiction": "US-federal",
        },
        "line": "sch1-10",
        "label": "Additional income",
        "description": (
            "Schedule 1 (Form 1040) 2025, line 10 for the bounded class: equals "
            "line 7 when every unsupported Part I income class, repayment, and "
            "residual Form 1099-G payment class is explicitly declared absent. "
            "Not a general Schedule 1 completeness claim."
        ),
        "binds_symbol": LINE10_TOTAL,
        "citation": {
            "id": "tax.us.2025.citation.schedule1.line-10",
            "version": "v1",
        },
        "dispositions": _field_dispositions(
            published_explain=(
                "A current derived finding publishes complete Schedule 1 line 10 "
                "additional income from closed unemployment under explicit Part I "
                "absence authority."
            ),
            blocked_explain=(
                "Schedule 1 line 10 is blocked because absence authority is incomplete, "
                "an excluded class is present, or unemployment is unclosed."
            ),
        ),
    }


def _line8_field() -> dict[str, Any]:
    return {
        "schema": "form-field.v3",
        "id": LINE8_FIELD,
        "version": "v1",
        "form": {
            "authority": "IRS",
            "form_id": "1040",
            "tax_year": 2025,
            "jurisdiction": "US-federal",
        },
        "line": "8",
        "label": "Additional income from Schedule 1",
        "description": (
            "Form 1040 (2025), line 8: additional income from complete Schedule 1 "
            "line 10 for the bounded unemployment class. Published exactly once into "
            "line-9 v5. Explicit zero when closed-empty unemployment meets complete "
            "absences; never a silent omission."
        ),
        "binds_symbol": LINE8_TOTAL,
        "citation": {
            "id": "tax.us.2025.citation.form1040.line-8",
            "version": "v1",
        },
        "dispositions": _field_dispositions(
            published_explain=(
                "A current derived finding publishes Form 1040 line 8 from complete "
                "Schedule 1 line 10. This amount is added exactly once to total income "
                "on line 9."
            ),
            blocked_explain=(
                "Form 1040 line 8 is blocked because Schedule 1 line 10 is incomplete "
                "or unavailable."
            ),
        ),
    }


def _attachment_rule() -> dict[str, Any]:
    """Schedule 1 attachment citizen (ADR-0036 content) for the bounded route.

    Required when the closed box-1 unemployment subtotal is strictly greater than
    zero (paper: attach Schedule 1 when additional income is reported). Line 8
    publication for closed-empty + complete absences is carried by the line-10 /
    line-8 computation rules (explicit zero), not by forcing an attachment
    disposition when the threshold is not crossed — matching existing attachment
    substrate (strictly_greater_than) without a new evaluator operation.
    """
    scope_answers = [
        {
            "check": "value",
            "equals": "yes",
            "fact_type": {"id": sid, "version": "v1"},
            "symbol": sid,
        }
        for sid in _scope_ids()
    ]
    return {
        "schema": "attachment-rule.v4",
        "id": ATTACHMENT_RULE,
        "version": "v1",
        "title": (
            "Schedule 1 (Additional Income and Adjustments to Income): bounded "
            "route itemizes line 7 unemployment from the closed Form 1099-G box-1 "
            "family; required when the closed box-1 subtotal is strictly greater "
            "than zero; completeness value-checks Alternative A Part I absences, "
            "repayment-not-present, and residual Form 1099-G payment-class absences. "
            "Not a general Schedule 1 claim; Part II adjustments are out of scope."
        ),
        "scope": SCOPE,
        "attachment": {
            "authority": "IRS",
            "form_id": "1040-SCH-1",
            "jurisdiction": "US-federal",
            "tax_year": 2025,
        },
        "publishes": ATTACHMENT_DISPOSITION,
        "requirement": {
            "comparison": "strictly_greater_than",
            "subtotals": [BOX1_SUBTOTAL],
            "threshold_parameter": {
                "id": "tax.us.2025.parameter.default-zero",
                "version": "v1",
            },
            "citation": {
                "id": "tax.us.2025.citation.attachment.schedule-1",
                "version": "v1",
            },
        },
        "itemizations": [
            {
                "part_id": "line-7-unemployment",
                "label": "Line 7: Unemployment compensation",
                "authority": {
                    "kind": "single_family",
                    "source_family": {"id": BOX1_FAMILY, "version": "v1"},
                },
                "row_sets": [
                    {
                        "rows": {
                            "op": "collect_members",
                            "source_family": {"id": BOX1_FAMILY, "version": "v1"},
                            "member_fact_type": {
                                "id": BOX1_AMOUNT,
                                "version": "v1",
                            },
                        },
                        "subtotal_symbol": BOX1_SUBTOTAL,
                    }
                ],
                "tie_out": {"line_symbol": BOX1_SUBTOTAL},
            }
        ],
        "completeness": {
            "required_answers": scope_answers,
        },
    }


def _citations() -> dict[str, dict[str, Any]]:
    return {
        "citation.f1099g.box1.json": {
            "schema": "citation.v1",
            "id": "tax.us.2025.citation.f1099g.box1",
            "version": "v1",
            "authority": {
                "family": "irs-instructions",
                "form_id": "1099-G",
                "tax_year": 2025,
            },
        },
        "citation.schedule1.line-7.json": {
            "schema": "citation.v1",
            "id": "tax.us.2025.citation.schedule1.line-7",
            "version": "v1",
            "authority": {
                "family": "irs-instructions",
                "form_id": "1040-SCH-1",
                "tax_year": 2025,
            },
        },
        "citation.schedule1.line-10.json": {
            "schema": "citation.v1",
            "id": "tax.us.2025.citation.schedule1.line-10",
            "version": "v1",
            "authority": {
                "family": "irs-instructions",
                "form_id": "1040-SCH-1",
                "tax_year": 2025,
            },
        },
        "citation.form1040.line-8.json": {
            "schema": "citation.v1",
            "id": "tax.us.2025.citation.form1040.line-8",
            "version": "v1",
            "authority": {
                "family": "irs-instructions",
                "form_id": "1040",
                "tax_year": 2025,
            },
        },
        "citation.attachment.schedule-1.json": {
            "schema": "citation.v1",
            "id": "tax.us.2025.citation.attachment.schedule-1",
            "version": "v1",
            "authority": {
                "family": "irs-instructions",
                "form_id": "1040-SCH-1",
                "tax_year": 2025,
            },
        },
    }


def _quantity() -> dict[str, Any]:
    return {
        "schema": "quantity-vocabulary.v9",
        "id": QUANTITY_ID,
        "version": "v1",
        "quantities": ["unemployment-compensation"],
    }


def _package_v20() -> dict[str, Any]:
    package = copy.deepcopy(_load(CONTENT / "package.core-calculations.v19.json"))
    package["schema"] = "artifact-package.v17"
    package["version"] = "v20"
    package["admitted_schemas"] = sorted(
        set(package["admitted_schemas"]) | {"quantity-vocabulary.v9"}
    )

    replacements: dict[str, dict[str, Any]] = {
        LINE9_RULE: {
            "role": "computation",
            "schema": "rule-artifact.v2",
            "version": "v5",
        },
    }
    members: list[dict[str, Any]] = []
    for member in package["members"]:
        rep = replacements.get(member["id"])
        if rep:
            members.append({"id": member["id"], **rep})
        else:
            members.append(dict(member))

    additions = [
        {
            "id": BOX1_BUNDLE,
            "role": "fact-type-bundle",
            "schema": "bundle.v2",
            "version": "v1",
        },
        {
            "id": SCH1_SCOPE_BUNDLE,
            "role": "fact-type-bundle",
            "schema": "bundle.v2",
            "version": "v1",
        },
        {
            "id": BOX1_FAMILY,
            "role": "source-family",
            "schema": "source-family.v1",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.closure-mapping.f1099g-1",
            "role": "source-closure-mapping",
            "schema": "source-closure-mapping.v2",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.rule.f1099g-1-subtotal",
            "role": "computation",
            "schema": "rule-artifact.v3",
            "version": "v1",
        },
        {
            "id": LINE7_RULE,
            "role": "computation",
            "schema": "rule-artifact.v3",
            "version": "v1",
        },
        {
            "id": LINE10_RULE,
            "role": "computation",
            "schema": "rule-artifact.v3",
            "version": "v1",
        },
        {
            "id": LINE8_RULE,
            "role": "computation",
            "schema": "rule-artifact.v3",
            "version": "v1",
        },
        {
            "id": LINE7_FIELD,
            "role": "form-field",
            "schema": "form-field.v3",
            "version": "v1",
        },
        {
            "id": LINE10_FIELD,
            "role": "form-field",
            "schema": "form-field.v3",
            "version": "v1",
        },
        {
            "id": LINE8_FIELD,
            "role": "form-field",
            "schema": "form-field.v3",
            "version": "v1",
        },
        {
            "id": ATTACHMENT_RULE,
            "role": "attachment-rule",
            "schema": "attachment-rule.v4",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.citation.f1099g.box1",
            "role": "citation",
            "schema": "citation.v1",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.citation.schedule1.line-7",
            "role": "citation",
            "schema": "citation.v1",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.citation.schedule1.line-10",
            "role": "citation",
            "schema": "citation.v1",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.citation.form1040.line-8",
            "role": "citation",
            "schema": "citation.v1",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.citation.attachment.schedule-1",
            "role": "citation",
            "schema": "citation.v1",
            "version": "v1",
        },
        {
            "id": QUANTITY_ID,
            "role": "parameter",
            "schema": "quantity-vocabulary.v9",
            "version": "v1",
        },
    ]
    existing = {(m["id"], m["version"]) for m in members}
    for add in additions:
        key = (add["id"], add["version"])
        if key not in existing:
            members.append(add)
            existing.add(key)
        else:
            # Replace existing version selection for same id if needed.
            members = [m for m in members if not (m["id"] == add["id"])]
            members.append(add)
            existing = {(m["id"], m["version"]) for m in members}

    package["members"] = sorted(members, key=lambda m: (m["id"], m["version"]))

    entrypoints: list[dict[str, Any]] = []
    for entry in package["entrypoints"]:
        if entry["id"] == LINE9_RULE:
            entrypoints.append({"id": LINE9_RULE, "version": "v5"})
        else:
            entrypoints.append(dict(entry))
    entry_ids = {e["id"] for e in entrypoints}
    for eid, ever in [
        (BOX1_BUNDLE, "v1"),
        (SCH1_SCOPE_BUNDLE, "v1"),
        ("tax.us.2025.rule.f1099g-1-subtotal", "v1"),
        (LINE7_RULE, "v1"),
        (LINE10_RULE, "v1"),
        (LINE8_RULE, "v1"),
        (ATTACHMENT_RULE, "v1"),
        ("tax.us.2025.citation.attachment.schedule-1", "v1"),
    ]:
        if eid not in entry_ids:
            entrypoints.append({"id": eid, "version": ever})
    package["entrypoints"] = entrypoints
    package["package_checksum"] = _package_checksum(package)
    return package


def render_content_files() -> dict[str, dict[str, Any]]:
    citizens: dict[str, dict[str, Any]] = {}
    citizens["f1099g-box1.bundle.json"] = _box1_bundle()
    citizens["schedule1-part1-scope.bundle.json"] = _scope_bundle()
    citizens["family.f1099g-1.json"] = _family()
    citizens["closure-mapping.f1099g-1.json"] = _mapping()
    citizens["rule.f1099g-1-subtotal.json"] = _subtotal_rule()
    citizens["rule.schedule1-line7.json"] = _line7_rule()
    citizens["rule.schedule1-line10.json"] = _line10_rule()
    citizens["rule.form1040-line8.json"] = _line8_rule()
    citizens["rule.form1040-line9.v5.json"] = _line9_v5()
    citizens["schedule1.line-7.form-field.json"] = _line7_field()
    citizens["schedule1.line-10.form-field.json"] = _line10_field()
    citizens["form1040.line-8.form-field.json"] = _line8_field()
    citizens["rule.attachment.schedule-1.json"] = _attachment_rule()
    citizens["quantity.unemployment-compensation.json"] = _quantity()
    citizens.update(_citations())

    package = _package_v20()
    citizens["package.core-calculations.v20.json"] = package

    registry = copy.deepcopy(_load(CONTENT / "published-packages.v14.json"))
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
    if (package["id"], "v20") not in existing_pkgs:
        registry["packages"].append(
            {
                "id": package["id"],
                "version": "v20",
                "checksum": package["package_checksum"],
            }
        )
    registry["packages"] = sorted(
        registry["packages"], key=lambda row: (row["id"], row["version"])
    )
    citizens["published-packages.v15.json"] = registry
    return citizens


def render_fixture_files(citizens: dict[str, dict[str, Any]]) -> dict[Path, bytes]:
    registry_bytes = _document(citizens["published-packages.v15.json"])
    package = citizens["package.core-calculations.v20.json"]
    release = {
        "schema": "release-registry.v1",
        "id": "demo.release.2025",
        "version": "v13",
        "package_registry_sha256": hashlib.sha256(registry_bytes).hexdigest(),
    }
    release_bytes = _document(release)
    adoption = {
        "schema": "act.v1",
        "act_id": "demo.act.adopt.core.v20",
        "kind": "package-adoption",
        "actor": "demo.user.filer-1",
        "at": "2026-08-05T12:00:00Z",
        "committed_against": 1,
        "payload": {
            "package": {
                "id": package["id"],
                "version": "v20",
                "checksum": package["package_checksum"],
            },
            "release": {
                "id": "demo.release.2025",
                "version": "v13",
                "checksum": hashlib.sha256(release_bytes).hexdigest(),
            },
            "scope": {"jurisdiction": "us", "year": "2025"},
            "revision": 20,
            "supersedes": "demo.act.adopt.core.v19",
            "audit": {
                "note": (
                    "synthetic Form 1099-G box-1 Schedule 1 line 7 / Form 1040 "
                    "line 8 successor adoption; non-authoritative"
                )
            },
        },
    }
    return {
        FIXTURES
        / "publication_surface"
        / "releases"
        / "demo.release.2025.v13.json": release_bytes,
        FIXTURES / "adoptions" / "adopt-core-v20-current.json": _document(adoption),
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
