"""Generate the additive Form 1099-DIV box-12 → Form 1040 line-2a route.

Reads the accepted v16/v11/v8 graph and writes only new content citizens plus
package v17, published-packages v12, release v10, and adoption v17. Historical
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
FIXTURES = ROOT / "packages" / "sample_data" / "form1099div_box12_line2a"

SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}

BOX12_AMOUNT = "tax.us.2025.f1099div.box12-exempt-interest-dividends"
BOX12_CLOSURE = "tax.us.2025.f1099div.12.source-closure"
BOX12_FAMILY = "tax.us.2025.f1099div.12"
BOX12_SUBTOTAL = "tax.us.2025.dividends.12-subtotal"
BOX13_AUTH = "tax.us.2025.f1099div.box13-specified-pab-authority"
LINE2A_TOTAL = "tax.us.2025.tax-exempt-interest.line2a-total"
LINE2A_RULE = "tax.us.2025.rule.form1040-line2a"
LINE2A_FIELD = "tax.us.2025.form1040.line-2a"
BOX12_BUNDLE = "tax.us.2025.f1099div.box12.vocabulary"
BOX2A_BUNDLE = "tax.us.2025.f1099div.box2a.vocabulary"

SCOPE_COMPONENTS: tuple[tuple[str, str], ...] = (
    ("no-f1099int-tax-exempt", "No Form 1099-INT tax-exempt interest source is present on this return for the bounded line-2a claim."),
    ("no-f1099oid-tax-exempt", "No Form 1099-OID tax-exempt interest or OID source is present on this return for the bounded line-2a claim."),
    ("no-unreported-tax-exempt", "No unreported or non-form tax-exempt interest is present on this return for the bounded line-2a claim."),
    ("no-premium-adjustment", "No tax-exempt bond or acquisition premium adjustment is present on this return for the bounded line-2a claim."),
    ("no-child-income-election", "No child-income election that consumes tax-exempt interest is present for the bounded line-2a claim."),
    ("no-taxable-social-security", "No taxable Social Security computation that consumes tax-exempt interest is present for the bounded line-2a claim."),
    ("no-amt-form-6251", "No Form 6251 / AMT consumer of tax-exempt interest is present for the bounded line-2a claim."),
    ("no-credit-using-tax-exempt", "No credit that consumes tax-exempt interest is present for the bounded line-2a claim."),
    ("no-deduction-using-tax-exempt", "No deduction that consumes tax-exempt interest is present for the bounded line-2a claim."),
)


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
    return f"tax.us.2025.line2a-scope.{token}"


def _statement_keys() -> list[dict[str, Any]]:
    return [
        {"name": "payer", "kind": "entity", "entity_kind": "tax.us.dividend-payer"},
        {"name": "statement", "kind": "entity", "entity_kind": "tax.us.1099div-statement"},
        {"name": "tax-year", "kind": "literal", "values": ["2025"]},
    ]


def _box2a_bundle_v2() -> dict[str, Any]:
    """Successor box-2a vocabulary without residual (residual moves to box-12 bundle)."""
    base = _load(CONTENT / "f1099div-box2a.bundle.json")
    fact_types = [
        ft
        for ft in base["fact_types"]
        if ft["id"] != "tax.us.2025.f1099div.recorded-boxes"
    ]
    return {
        "schema": "bundle.v2",
        "id": BOX2A_BUNDLE,
        "version": "v2",
        "label": (
            "Form 1099-DIV box-2a successor member and closure vocabulary for tax year "
            "2025 without residual recorded-boxes (box-12 residual succession)"
        ),
        "fact_types": fact_types,
    }


def _box12_bundle() -> dict[str, Any]:
    return {
        "schema": "bundle.v2",
        "id": BOX12_BUNDLE,
        "version": "v1",
        "label": (
            "Form 1099-DIV box-12 exempt-interest dividends, box-13 absence/zero "
            "authority, and residual recorded-boxes v3 for tax year 2025"
        ),
        "fact_types": [
            {
                "schema": "fact-type.v2",
                "id": BOX12_AMOUNT,
                "version": "v1",
                "title": (
                    "Exempt-interest dividends reported in box 12 of one logical Form "
                    "1099-DIV statement instance furnished by a payer for 2025; the "
                    "statement instance is peer to evidence and its identity carries no "
                    "file, upload, scan, document, or evidence key (ADR-0015). Multiple "
                    "originals from one payer are distinct statement instances; a "
                    "corrected copy of the same logical return answers this same fact "
                    "and supersedes its prior finding. Nonnegative source amount only."
                ),
                "nature": "determinable",
                "identity_keys": _statement_keys(),
                "value_schema": {"type": "number", "minimum": 0},
                "supersession": {"policy": "free"},
                "source_amount": True,
                "quantity": {
                    "id": "tax.us.2025.quantity.exempt-interest-dividends",
                    "version": "v1",
                },
            },
            {
                "schema": "fact-type.v2",
                "id": BOX12_CLOSURE,
                "version": "v1",
                "title": (
                    "User-attested closure of the Form 1099-DIV box-12 source family for "
                    "2025, keyed on the family membership horizon current at attestation "
                    "(ADR-0017): true asserts every furnished 1099-DIV box-12 amount is "
                    "recorded as of that horizon. This claim covers box 12 only — never "
                    "boxes 1a/1b/2a, residual recorded boxes, or Form 1040 line 2a "
                    "completeness. A later membership transition displaces this closure "
                    "through horizon succession; re-attestation on the successor horizon "
                    "is required."
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
                "id": BOX13_AUTH,
                "version": "v1",
                "title": (
                    "Explicit companion authority for Form 1099-DIV box 13 (specified "
                    "private activity bond interest dividends) on the same logical "
                    "statement as a box-12 member. Only explicit null (absent) or "
                    "numeric zero is admissible on the bounded line-2a route. A nonzero "
                    "value is a hard admission block and never creates Form 6251 or AMT "
                    "input. This is an authority witness, not a composed amount."
                ),
                "nature": "determinable",
                "identity_keys": _statement_keys(),
                "value_schema": {
                    "anyOf": [{"type": "null"}, {"const": 0}],
                },
                "supersession": {"policy": "free"},
            },
            {
                "schema": "fact-type.v2",
                "id": "tax.us.2025.f1099div.recorded-boxes",
                "version": "v3",
                "title": (
                    "Successor residual recorded non-composable 1099-DIV box content for "
                    "one logical statement instance: boxes 3, 5, and 7 only are recorded "
                    "but never composed into any line. Each box carries either its "
                    "reported number or explicit null as the declared absence of that "
                    "box — absence is asserted, never assumed. Boxes 2a and 12 are "
                    "omitted because the successor graph composes them through independent "
                    "families. Historical residual v1 and residual v2 remain immutable "
                    "history; mixed residual/family graphs are rejected at package "
                    "validation."
                ),
                "nature": "determinable",
                "identity_keys": _statement_keys(),
                "value_schema": {
                    "type": "object",
                    "properties": {
                        "3": {"type": ["number", "null"]},
                        "5": {"type": ["number", "null"]},
                        "7": {"type": ["number", "null"]},
                    },
                    "required": ["3", "5", "7"],
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
                    f"Line-2a scope completeness component: {title} Contributed "
                    "categorical assertion, domain {yes, no}, no default, "
                    "presence-before-value, free supersession. yes asserts the named "
                    "excluded source or downstream dependency is absent; no asserts it "
                    "is present and blocks the bounded line-2a claim."
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
        "id": "tax.us.2025.line2a-scope.vocabulary",
        "version": "v1",
        "label": (
            "Form 1040 line-2a scope/completeness absence authorities for the bounded "
            "2025 tax-exempt-interest claim"
        ),
        "fact_types": fact_types,
    }


def _family() -> dict[str, Any]:
    return {
        "schema": "source-family.v1",
        "id": BOX12_FAMILY,
        "version": "v1",
        "title": "Form 1099-DIV box 12 statement items, tax year 2025",
        "scope": SCOPE,
        "closure_claim": (
            "Every exempt-interest dividend amount reported in box 12 of a Form "
            "1099-DIV furnished to the taxpayer for tax year 2025 is recorded as a "
            "statement item as of the keyed horizon. This claim covers Form 1099-DIV "
            "box 12 only: it says nothing about boxes 1a, 1b, or 2a, residual recorded "
            "non-composable boxes (3, 5, 7), Form 1099-INT or Form 1099-OID tax-exempt "
            "sources, premium adjustments, or Form 1040 line 2a completeness. Closed "
            "with members authorizes the multi-payer sum of current members; "
            "closed-empty authorizes subtotal 0."
        ),
        "member_predicate": {"fact_type": BOX12_AMOUNT},
        "authorizes_subtotal": BOX12_SUBTOTAL,
    }


def _mapping() -> dict[str, Any]:
    return {
        "schema": "source-closure-mapping.v2",
        "id": "tax.us.2025.closure-mapping.f1099div-12",
        "version": "v1",
        "family": {"id": BOX12_FAMILY, "version": "v1"},
        "member_fact_type": {"id": BOX12_AMOUNT, "version": "v1"},
        "closure_fact_type": {"id": BOX12_CLOSURE, "version": "v1"},
        "closure_horizon_key": "family-horizon",
        "admits_symbol": BOX12_SUBTOTAL,
        "admission": {"condition": "current-literal-true"},
    }


def _subtotal_rule() -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v3",
        "id": "tax.us.2025.rule.f1099div-12-subtotal",
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
                        "name": BOX12_AMOUNT,
                        "source_set": BOX12_FAMILY,
                    }
                ],
            },
            "mode": {"op": "ref", "name": "rounding.convention"},
        },
        "publishes": BOX12_SUBTOTAL,
        "citations": [
            {"id": "tax.us.2025.citation.f1099div.box12", "version": "v1"},
        ],
        "blocked": {"code": "OPEN_DEPENDENCY", "missing": ["rounding.convention"]},
        "notes": (
            "Aggregates current successor box-12 exempt-interest dividend findings "
            "into the family subtotal. Closed-empty publishes zero only through "
            "current literal-true closure admitted by the adopted mapping. Never "
            "reads residual recorded-boxes content."
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


def _line2a_rule() -> dict[str, Any]:
    scope_ids = [_scope_id(token) for token, _ in SCOPE_COMPONENTS]
    when_args: list[dict[str, Any]] = [
        {"op": "require_closed", "source_set": BOX12_FAMILY},
    ]
    when_args.extend(_yes_compare(sid) for sid in scope_ids)
    return {
        "schema": "rule-artifact.v3",
        "id": LINE2A_RULE,
        "version": "v1",
        "scope": SCOPE,
        "role": "computation",
        "requires": [BOX12_SUBTOTAL, *scope_ids],
        "pins": [
            {"role": "input", "id": BOX12_SUBTOTAL, "version": "v1", "origin": "assertion"},
            *[
                {"role": "input", "id": sid, "version": "v1", "origin": "assertion"}
                for sid in scope_ids
            ],
        ],
        "when": {"op": "all", "args": when_args},
        "value": {"op": "ref", "name": BOX12_SUBTOTAL},
        "publishes": LINE2A_TOTAL,
        "citations": [
            {"id": "tax.us.2025.citation.form1040.line-2a", "version": "v1"},
            {"id": "tax.us.2025.citation.f1099div.box12", "version": "v1"},
            {"id": "tax.us.2025.citation.publication-550.tax-exempt-interest", "version": "v1"},
        ],
        "blocked": {
            "code": "DEPENDENCY_ABSENT",
            "missing": [BOX12_SUBTOTAL, *scope_ids],
        },
        "notes": (
            "Form 1040 line 2a for the bounded 2025 class: equals the closed box-12 "
            "family subtotal only when every excluded tax-exempt source, premium "
            "adjustment, and excluded downstream dependency is explicitly declared "
            "absent (yes). Box-13 absence/zero is enforced at admission on each "
            "statement companion. Line 2a is reported-but-not-directly-taxable and "
            "is never an input to line 9 or taxable-income arithmetic."
        ),
    }


def _line2a_field() -> dict[str, Any]:
    return {
        "schema": "form-field.v3",
        "id": LINE2A_FIELD,
        "version": "v1",
        "form": {
            "authority": "IRS",
            "form_id": "1040",
            "tax_year": 2025,
            "jurisdiction": "US-federal",
        },
        "line": "2a",
        "label": "Tax-exempt interest",
        "description": (
            "Form 1040 (2025), line 2a: tax-exempt interest for the contracted "
            "direct-reporting class of Form 1099-DIV box-12 exempt-interest "
            "dividends when every excluded tax-exempt source, premium adjustment, "
            "and excluded downstream dependency is explicitly declared absent. "
            "Reported-but-not-directly-taxable; does not enter line 9 or taxable "
            "income. Does not implement Form 1099-INT/OID tax-exempt sources, "
            "premium calculations, Form 6251, or general tax-exempt-interest support."
        ),
        "binds_symbol": LINE2A_TOTAL,
        "citation": {
            "id": "tax.us.2025.citation.form1040.line-2a",
            "version": "v1",
        },
        "dispositions": {
            "published_value": {
                "render": "{value}",
                "explain": (
                    "A current derived finding publishes this tax-exempt interest "
                    "amount on line 2a from the closed box-12 family under explicit "
                    "scope-completeness authority. The amount is reported but not "
                    "directly taxable on this return graph."
                ),
            },
            "computed_zero": {
                "render": "0",
                "explain": (
                    "A current derived finding publishes a computed zero from present "
                    "box-12 findings that sum to zero under explicit scope authority."
                ),
            },
            "closure_backed_zero": {
                "render": "0",
                "explain": (
                    "A current derived finding publishes a zero because the box-12 "
                    "family is attested closed on its current horizon with no recorded "
                    "members, under explicit scope-completeness authority."
                ),
            },
            "blocked": {
                "render": "",
                "explain": (
                    "Line 2a is blocked because scope-completeness authority is "
                    "incomplete, an excluded source or dependency is present, or the "
                    "box-12 family is unclosed."
                ),
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
                    "No bounded line-2a value is published because a scope-completeness "
                    "component is not yes (an excluded source or downstream dependency "
                    "is present)."
                ),
            },
        },
    }


def _dividend_universe_v3() -> dict[str, Any]:
    return {
        "schema": "dividend-universe.v3",
        "id": "tax.us.2025.dividend-universe",
        "version": "v3",
        "title": (
            "Successor Form 1099-DIV box universe for tax year 2025 with composable "
            "boxes 2a and 12"
        ),
        "scope": SCOPE,
        "composable_boxes": [
            {"box": "1a", "family": {"id": "tax.us.2025.f1099div.1a", "version": "v1"}},
            {"box": "1b", "family": {"id": "tax.us.2025.f1099div.1b", "version": "v1"}},
            {"box": "2a", "family": {"id": "tax.us.2025.f1099div.2a", "version": "v1"}},
            {"box": "12", "family": {"id": BOX12_FAMILY, "version": "v1"}},
        ],
        "recorded_non_composable_boxes": ["3", "5", "7"],
        "recorded_boxes_fact_type": {
            "id": "tax.us.2025.f1099div.recorded-boxes",
            "version": "v3",
        },
        "capital_gain_signal": {
            "box": "2a",
            "signal": "CAPITAL_GAIN_DISTRIBUTION_RECORDED",
            "source": "current_successor_family_member",
        },
    }


def _citations() -> dict[str, dict[str, Any]]:
    return {
        "citation.form1040.line-2a.json": {
            "schema": "citation.v1",
            "id": "tax.us.2025.citation.form1040.line-2a",
            "version": "v1",
            "authority": {
                "family": "irs-instructions",
                "form_id": "1040",
                "tax_year": 2025,
            },
        },
        "citation.f1099div.box12.json": {
            "schema": "citation.v1",
            "id": "tax.us.2025.citation.f1099div.box12",
            "version": "v1",
            "authority": {
                "family": "irs-instructions",
                "form_id": "1099-DIV",
                "tax_year": 2025,
            },
        },
        "citation.publication-550.tax-exempt-interest.json": {
            "schema": "citation.v1",
            "id": "tax.us.2025.citation.publication-550.tax-exempt-interest",
            "version": "v1",
            "authority": {
                "family": "irs-publication",
                "publication": "550",
                "revision": "2025",
            },
        },
    }


def _quantity() -> dict[str, Any]:
    return {
        "schema": "quantity-vocabulary.v6",
        "id": "tax.us.2025.quantity.exempt-interest-dividends",
        "version": "v1",
        "quantities": ["exempt-interest-dividends"],
    }


def _package_v17(citizens: dict[str, dict[str, Any]]) -> dict[str, Any]:
    package = _load(CONTENT / "package.core-calculations.v16.json")
    package = copy.deepcopy(package)
    package["schema"] = "artifact-package.v14"
    package["version"] = "v17"
    package["admitted_schemas"] = sorted(
        set(package["admitted_schemas"]) | {"dividend-universe.v3", "quantity-vocabulary.v6"}
    )

    replacements: dict[str, dict[str, Any]] = {
        "tax.us.2025.dividend-universe": {
            "role": "dividend-universe",
            "schema": "dividend-universe.v3",
            "version": "v3",
        },
        BOX2A_BUNDLE: {
            "role": "fact-type-bundle",
            "schema": "bundle.v2",
            "version": "v2",
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
        {"id": BOX12_BUNDLE, "role": "fact-type-bundle", "schema": "bundle.v2", "version": "v1"},
        {
            "id": "tax.us.2025.line2a-scope.vocabulary",
            "role": "fact-type-bundle",
            "schema": "bundle.v2",
            "version": "v1",
        },
        {"id": BOX12_FAMILY, "role": "source-family", "schema": "source-family.v1", "version": "v1"},
        {
            "id": "tax.us.2025.closure-mapping.f1099div-12",
            "role": "source-closure-mapping",
            "schema": "source-closure-mapping.v2",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.rule.f1099div-12-subtotal",
            "role": "computation",
            "schema": "rule-artifact.v3",
            "version": "v1",
        },
        {
            "id": LINE2A_RULE,
            "role": "computation",
            "schema": "rule-artifact.v3",
            "version": "v1",
        },
        {
            "id": LINE2A_FIELD,
            "role": "form-field",
            "schema": "form-field.v3",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.citation.form1040.line-2a",
            "role": "citation",
            "schema": "citation.v1",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.citation.f1099div.box12",
            "role": "citation",
            "schema": "citation.v1",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.citation.publication-550.tax-exempt-interest",
            "role": "citation",
            "schema": "citation.v1",
            "version": "v1",
        },
        {
            "id": "tax.us.2025.quantity.exempt-interest-dividends",
            "role": "parameter",
            "schema": "quantity-vocabulary.v6",
            "version": "v1",
        },
    ]
    existing = {(m["id"], m["version"]) for m in members}
    for add in additions:
        key = (add["id"], add["version"])
        if key not in existing:
            members.append(add)
            existing.add(key)

    package["members"] = sorted(members, key=lambda m: (m["id"], m["version"]))

    # Entrypoints: pin dividend-universe v3 and add line-2a rule; replace box2a vocabulary version.
    entrypoints: list[dict[str, Any]] = []
    for entry in package["entrypoints"]:
        if entry["id"] == "tax.us.2025.dividend-universe":
            entrypoints.append({"id": entry["id"], "version": "v3"})
        elif entry["id"] == BOX2A_BUNDLE:
            entrypoints.append({"id": entry["id"], "version": "v2"})
        else:
            entrypoints.append(dict(entry))
    entry_ids = {e["id"] for e in entrypoints}
    for eid, ever in [
        (BOX12_BUNDLE, "v1"),
        ("tax.us.2025.line2a-scope.vocabulary", "v1"),
        ("tax.us.2025.rule.f1099div-12-subtotal", "v1"),
        (LINE2A_RULE, "v1"),
    ]:
        if eid not in entry_ids:
            entrypoints.append({"id": eid, "version": ever})
    package["entrypoints"] = entrypoints
    package["package_checksum"] = _package_checksum(package)
    return package


def render_content_files() -> dict[str, dict[str, Any]]:
    citizens: dict[str, dict[str, Any]] = {}
    citizens["f1099div-box2a.bundle.v2.json"] = _box2a_bundle_v2()
    citizens["f1099div-box12.bundle.json"] = _box12_bundle()
    citizens["line2a-scope.bundle.json"] = _scope_bundle()
    citizens["family.f1099div-12.json"] = _family()
    citizens["closure-mapping.f1099div-12.json"] = _mapping()
    citizens["rule.f1099div-12-subtotal.json"] = _subtotal_rule()
    citizens["rule.form1040-line2a.json"] = _line2a_rule()
    citizens["form1040.line-2a.form-field.json"] = _line2a_field()
    citizens["dividend-universe.v3.json"] = _dividend_universe_v3()
    citizens["quantity.exempt-interest-dividends.json"] = _quantity()
    citizens.update(_citations())

    package = _package_v17(citizens)
    citizens["package.core-calculations.v17.json"] = package

    registry = _load(CONTENT / "published-packages.v11.json")
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
    # Also publish box2a bundle v2 which is under a filename key
    registry["citizens"] = sorted(
        registry["citizens"], key=lambda row: (row["id"], row["version"])
    )
    existing_pkgs = {(p["id"], p["version"]) for p in registry["packages"]}
    if (package["id"], "v17") not in existing_pkgs:
        registry["packages"].append(
            {
                "id": package["id"],
                "version": "v17",
                "checksum": package["package_checksum"],
            }
        )
    registry["packages"] = sorted(
        registry["packages"], key=lambda row: (row["id"], row["version"])
    )
    citizens["published-packages.v12.json"] = registry
    return citizens


def render_fixture_files(citizens: dict[str, dict[str, Any]]) -> dict[Path, bytes]:
    registry_bytes = _document(citizens["published-packages.v12.json"])
    package = citizens["package.core-calculations.v17.json"]
    release = {
        "schema": "release-registry.v1",
        "id": "demo.release.2025",
        "version": "v10",
        "package_registry_sha256": hashlib.sha256(registry_bytes).hexdigest(),
    }
    release_bytes = _document(release)
    adoption = {
        "schema": "act.v1",
        "act_id": "demo.act.adopt.core.v17",
        "kind": "package-adoption",
        "actor": "demo.user.filer-1",
        "at": "2026-08-04T12:00:00Z",
        "committed_against": 1,
        "payload": {
            "package": {
                "id": package["id"],
                "version": "v17",
                "checksum": package["package_checksum"],
            },
            "release": {
                "id": "demo.release.2025",
                "version": "v10",
                "checksum": hashlib.sha256(release_bytes).hexdigest(),
            },
            "scope": {"jurisdiction": "us", "year": "2025"},
            "revision": 16,
                "supersedes": "demo.act.adopt.core.v16",
            "audit": {
                "note": (
                    "synthetic Form 1099-DIV box-12 line-2a successor adoption; "
                    "non-authoritative"
                )
            },
        },
    }
    return {
        FIXTURES
        / "publication_surface"
        / "releases"
        / "demo.release.2025.v10.json": release_bytes,
        FIXTURES / "adoptions" / "adopt-core-v17-current.json": _document(adoption),
    }


def render_all() -> dict[Path, bytes]:
    citizens = render_content_files()
    content_files = {CONTENT / name: _document(value) for name, value in citizens.items()}
    return {**content_files, **render_fixture_files(citizens)}


def main() -> None:
    for path, body in render_all().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
    print(f"wrote {len(render_all())} files")


if __name__ == "__main__":
    main()
