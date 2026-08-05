"""Generate the additive Form 1099-INT box-8 → Form 1040 line-2a succession.

Reads the accepted v18/v13 graph and writes only new content citizens plus
package v19, published-packages v14, release v12, and adoption v19. Historical
box-12 / line-2a@v1 packages and registries remain byte-for-byte.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
FIXTURES = ROOT / "packages" / "sample_data" / "form1099int_box8_line2a"

SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}

BOX8_AMOUNT = "tax.us.2025.f1099int.box8-tax-exempt-interest"
BOX8_CLOSURE = "tax.us.2025.f1099int.b8.source-closure"
BOX8_FAMILY = "tax.us.2025.f1099int.b8"
BOX8_SUBTOTAL = "tax.us.2025.interest.b8-tax-exempt-subtotal"
BOX9_AUTH = "tax.us.2025.f1099int.box9-specified-pab-authority"
BOX8_BUNDLE = "tax.us.2025.f1099int.box8.vocabulary"
BOX8_MAPPING = "tax.us.2025.closure-mapping.f1099int-b8"
BOX8_SUBTOTAL_RULE = "tax.us.2025.rule.f1099int-b8-subtotal"
BOX8_CITATION = "tax.us.2025.citation.f1099int.box8"
BOX8_QUANTITY = "tax.us.2025.quantity.tax-exempt-interest"

BOX12_FAMILY = "tax.us.2025.f1099div.12"
BOX12_SUBTOTAL = "tax.us.2025.dividends.12-subtotal"
LINE2A_TOTAL = "tax.us.2025.tax-exempt-interest.line2a-total"
LINE2A_RULE = "tax.us.2025.rule.form1040-line2a"
LINE2A_FIELD = "tax.us.2025.form1040.line-2a"
NO_F1099INT = "tax.us.2025.line2a-scope.no-f1099int-tax-exempt"

# Residual scope (unconditional yes) excludes no-f1099int, which is the Path A/B gate.
RESIDUAL_SCOPE: tuple[tuple[str, str], ...] = (
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
        {"name": "payer", "kind": "entity", "entity_kind": "tax.us.interest-payer"},
        {"name": "statement", "kind": "entity", "entity_kind": "tax.us.1099int-statement"},
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


def _box8_bundle() -> dict[str, Any]:
    return {
        "schema": "bundle.v2",
        "id": BOX8_BUNDLE,
        "version": "v1",
        "label": (
            "Form 1099-INT box-8 tax-exempt interest and box-9 absence/zero "
            "authority for tax year 2025"
        ),
        "fact_types": [
            {
                "schema": "fact-type.v2",
                "id": BOX8_AMOUNT,
                "version": "v1",
                "title": (
                    "Tax-exempt interest reported in box 8 of one logical Form "
                    "1099-INT statement instance furnished by a payer for 2025; the "
                    "statement instance is peer to evidence and its identity carries no "
                    "file, upload, scan, document, or evidence key (ADR-0015). Multiple "
                    "originals from one payer are distinct statement instances; a "
                    "corrected copy of the same logical return answers this same fact "
                    "and supersedes its prior finding. Nonnegative source amount only. "
                    "Specified private-activity-bond interest already included in box 8 "
                    "is witnessed separately in box 9 and must not be added a second time."
                ),
                "nature": "determinable",
                "identity_keys": _statement_keys(),
                "value_schema": {"type": "number", "minimum": 0},
                "supersession": {"policy": "free"},
                "source_amount": True,
                "quantity": {"id": BOX8_QUANTITY, "version": "v1"},
            },
            {
                "schema": "fact-type.v2",
                "id": BOX8_CLOSURE,
                "version": "v1",
                "title": (
                    "User-attested closure of the Form 1099-INT box-8 source family for "
                    "2025, keyed on the family membership horizon current at attestation "
                    "(ADR-0017): true asserts every furnished 1099-INT box-8 amount is "
                    "recorded as of that horizon. This claim covers box 8 only — never "
                    "boxes 1, 3, or 10, taxable-interest composition, Form 1099-DIV box 12, "
                    "or residual line-2a scope completeness. A later membership transition "
                    "displaces this closure through horizon succession; re-attestation on "
                    "the successor horizon is required."
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
                "id": BOX9_AUTH,
                "version": "v1",
                "title": (
                    "Explicit companion authority for Form 1099-INT box 9 (specified "
                    "private activity bond interest) on the same logical statement as a "
                    "box-8 member. Only explicit null (absent) or numeric zero is "
                    "admissible on the bounded line-2a route. A nonzero value is a hard "
                    "admission block and never creates Form 6251 or AMT input. This is an "
                    "authority witness, not a composed amount; box 9 is already included "
                    "in box 8 and must not be added a second time to line 2a."
                ),
                "nature": "determinable",
                "identity_keys": _statement_keys(),
                "value_schema": {
                    "anyOf": [{"type": "null"}, {"const": 0}],
                },
                "supersession": {"policy": "free"},
            },
        ],
    }


def _family() -> dict[str, Any]:
    return {
        "schema": "source-family.v1",
        "id": BOX8_FAMILY,
        "version": "v1",
        "title": "Form 1099-INT box 8 statement items, tax year 2025",
        "scope": SCOPE,
        "closure_claim": (
            "Every tax-exempt interest amount reported in box 8 of a Form "
            "1099-INT furnished to the taxpayer for tax year 2025 is recorded as a "
            "statement item as of the keyed horizon. This claim covers Form 1099-INT "
            "box 8 only: it says nothing about boxes 1, 3, or 10, Form 1099-DIV box 12, "
            "Form 1099-OID tax-exempt sources, premium adjustments, or Form 1040 line 2a "
            "completeness. Closed with members authorizes the multi-payer sum of current "
            "members; closed-empty authorizes subtotal 0."
        ),
        "member_predicate": {"fact_type": BOX8_AMOUNT},
        "authorizes_subtotal": BOX8_SUBTOTAL,
    }


def _mapping() -> dict[str, Any]:
    return {
        "schema": "source-closure-mapping.v2",
        "id": BOX8_MAPPING,
        "version": "v1",
        "family": {"id": BOX8_FAMILY, "version": "v1"},
        "member_fact_type": {"id": BOX8_AMOUNT, "version": "v1"},
        "closure_fact_type": {"id": BOX8_CLOSURE, "version": "v1"},
        "closure_horizon_key": "family-horizon",
        "admits_symbol": BOX8_SUBTOTAL,
        "admission": {"condition": "current-literal-true"},
    }


def _subtotal_rule() -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v3",
        "id": BOX8_SUBTOTAL_RULE,
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
                        "name": BOX8_AMOUNT,
                        "source_set": BOX8_FAMILY,
                    }
                ],
            },
            "mode": {"op": "ref", "name": "rounding.convention"},
        },
        "publishes": BOX8_SUBTOTAL,
        "citations": [
            {"id": BOX8_CITATION, "version": "v1"},
        ],
        "blocked": {"code": "OPEN_DEPENDENCY", "missing": ["rounding.convention"]},
        "notes": (
            "Aggregates current Form 1099-INT box-8 tax-exempt interest findings "
            "into the family subtotal. Closed-empty publishes zero only through "
            "current literal-true closure admitted by the adopted mapping. Never "
            "adds box 9 a second time and never reads taxable-interest families."
        ),
    }


def _line2a_rule_v2() -> dict[str, Any]:
    residual_ids = [_scope_id(token) for token, _ in RESIDUAL_SCOPE]
    path_a = _yes_compare(NO_F1099INT)
    when_args: list[dict[str, Any]] = [
        {"op": "require_closed", "source_set": BOX12_FAMILY},
    ]
    when_args.extend(_yes_compare(sid) for sid in residual_ids)
    # Path A: no-f1099int = yes → INT contribution 0 (box-8 not required).
    # Path B: declaration is not yes → require box-8 closed + box-8 subtotal.
    when_args.append(
        {
            "op": "choose",
            "when": path_a,
            "then": True,
            "else": {
                "op": "all",
                "args": [
                    {"op": "require_closed", "source_set": BOX8_FAMILY},
                    {
                        "op": "conditional_dependency_set",
                        "condition": True,
                        "members": [{"op": "ref", "name": BOX8_SUBTOTAL}],
                    },
                ],
            },
        }
    )
    always_requires = [BOX12_SUBTOTAL, NO_F1099INT, *residual_ids]
    return {
        "schema": "rule-artifact.v3",
        "id": LINE2A_RULE,
        "version": "v2",
        "scope": SCOPE,
        "role": "computation",
        "requires": always_requires,
        "pins": [
            {"role": "input", "id": BOX12_SUBTOTAL, "version": "v1", "origin": "assertion"},
            {"role": "input", "id": NO_F1099INT, "version": "v1", "origin": "assertion"},
            *[
                {"role": "input", "id": sid, "version": "v1", "origin": "assertion"}
                for sid in residual_ids
            ],
        ],
        "when": {"op": "all", "args": when_args},
        "value": {
            "op": "add",
            "args": [
                {"op": "ref", "name": BOX12_SUBTOTAL},
                {
                    "op": "choose",
                    "when": path_a,
                    "then": 0,
                    "else": {"op": "ref", "name": BOX8_SUBTOTAL},
                },
            ],
        },
        "publishes": LINE2A_TOTAL,
        "citations": [
            {"id": "tax.us.2025.citation.form1040.line-2a", "version": "v1"},
            {"id": "tax.us.2025.citation.f1099div.box12", "version": "v1"},
            {"id": BOX8_CITATION, "version": "v1"},
            {"id": "tax.us.2025.citation.publication-550.tax-exempt-interest", "version": "v1"},
        ],
        "blocked": {
            "code": "DEPENDENCY_ABSENT",
            "missing": always_requires,
        },
        "notes": (
            "Form 1040 line 2a successor for the bounded 2025 multi-family class: "
            "closed box-12 subtotal plus Path A (no-f1099int-tax-exempt=yes → INT "
            "contribution 0) or Path B (box-8 family closed → closed box-8 subtotal). "
            "Box-9 absence/zero is enforced at admission on each statement companion. "
            "Residual scope components remain unconditional yes. Historical @v1 "
            "(box-12-only with unconditional no-f1099int=yes) remains immutable. "
            "Line 2a is reported-but-not-directly-taxable and is never an input to "
            "line 9 or taxable-income arithmetic."
        ),
    }


def _line2a_field_v2() -> dict[str, Any]:
    return {
        "schema": "form-field.v3",
        "id": LINE2A_FIELD,
        "version": "v2",
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
            "direct-reporting class of closed Form 1099-DIV box-12 exempt-interest "
            "dividends and/or closed Form 1099-INT box-8 tax-exempt interest under "
            "Path A (no Form 1099-INT tax-exempt source) or Path B (closed box-8 "
            "family), when every remaining excluded source, premium adjustment, and "
            "excluded downstream dependency is explicitly declared absent. "
            "Reported-but-not-directly-taxable; does not enter line 9 or taxable "
            "income. Does not implement Form 1099-OID tax-exempt sources, premium "
            "calculations, Form 6251, or general tax-exempt-interest support."
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
                    "amount on line 2a from the closed box-12 and/or closed box-8 "
                    "families under explicit scope-completeness authority. The amount "
                    "is reported but not directly taxable on this return graph."
                ),
            },
            "computed_zero": {
                "render": "0",
                "explain": (
                    "A current derived finding publishes a computed zero from present "
                    "box-12 and/or box-8 findings that sum to zero under explicit "
                    "scope authority."
                ),
            },
            "closure_backed_zero": {
                "render": "0",
                "explain": (
                    "A current derived finding publishes a zero because the supported "
                    "tax-exempt-interest families are attested closed on their current "
                    "horizons with no recorded members (or Path A contributes zero from "
                    "the INT slot), under explicit scope-completeness authority."
                ),
            },
            "blocked": {
                "render": "",
                "explain": (
                    "Line 2a is blocked because scope-completeness authority is "
                    "incomplete, an excluded source or dependency is present, the "
                    "box-12 family is unclosed, or Path B lacks a closed box-8 family."
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
                    "No bounded line-2a value is published because a residual "
                    "scope-completeness component is not yes (an excluded source or "
                    "downstream dependency is present)."
                ),
            },
        },
    }


def _citation() -> dict[str, Any]:
    return {
        "schema": "citation.v1",
        "id": BOX8_CITATION,
        "version": "v1",
        "authority": {
            "family": "irs-instructions",
            "form_id": "1099-INT",
            "tax_year": 2025,
        },
    }


def _quantity() -> dict[str, Any]:
    return {
        "schema": "quantity-vocabulary.v8",
        "id": BOX8_QUANTITY,
        "version": "v1",
        "quantities": ["tax-exempt-interest"],
    }


def _package_v19(citizens: dict[str, dict[str, Any]]) -> dict[str, Any]:
    package = _load(CONTENT / "package.core-calculations.v18.json")
    package = copy.deepcopy(package)
    package["schema"] = "artifact-package.v16"
    package["version"] = "v19"
    package["admitted_schemas"] = sorted(
        set(package["admitted_schemas"]) | {"quantity-vocabulary.v7", "quantity-vocabulary.v8"}
    )

    replacements: dict[str, dict[str, Any]] = {
        LINE2A_RULE: {
            "role": "computation",
            "schema": "rule-artifact.v3",
            "version": "v2",
        },
        LINE2A_FIELD: {
            "role": "form-field",
            "schema": "form-field.v3",
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
        {"id": BOX8_BUNDLE, "role": "fact-type-bundle", "schema": "bundle.v2", "version": "v1"},
        {"id": BOX8_FAMILY, "role": "source-family", "schema": "source-family.v1", "version": "v1"},
        {
            "id": BOX8_MAPPING,
            "role": "source-closure-mapping",
            "schema": "source-closure-mapping.v2",
            "version": "v1",
        },
        {
            "id": BOX8_SUBTOTAL_RULE,
            "role": "computation",
            "schema": "rule-artifact.v3",
            "version": "v1",
        },
        {
            "id": BOX8_CITATION,
            "role": "citation",
            "schema": "citation.v1",
            "version": "v1",
        },
        {
            "id": BOX8_QUANTITY,
            "role": "parameter",
            "schema": "quantity-vocabulary.v8",
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

    entrypoints: list[dict[str, Any]] = []
    for entry in package["entrypoints"]:
        if entry["id"] == LINE2A_RULE:
            entrypoints.append({"id": entry["id"], "version": "v2"})
        else:
            entrypoints.append(dict(entry))
    entry_ids = {e["id"] for e in entrypoints}
    for eid, ever in [
        (BOX8_BUNDLE, "v1"),
        (BOX8_SUBTOTAL_RULE, "v1"),
    ]:
        if eid not in entry_ids:
            entrypoints.append({"id": eid, "version": ever})
    package["entrypoints"] = entrypoints
    package["package_checksum"] = _package_checksum(package)
    return package


def render_content_files() -> dict[str, dict[str, Any]]:
    citizens: dict[str, dict[str, Any]] = {}
    citizens["f1099int-box8.bundle.json"] = _box8_bundle()
    citizens["family.f1099int-b8.json"] = _family()
    citizens["closure-mapping.f1099int-b8.json"] = _mapping()
    citizens["rule.f1099int-b8-subtotal.json"] = _subtotal_rule()
    citizens["rule.form1040-line2a.v2.json"] = _line2a_rule_v2()
    citizens["form1040.line-2a.form-field.v2.json"] = _line2a_field_v2()
    citizens["citation.f1099int.box8.json"] = _citation()
    citizens["quantity.tax-exempt-interest.json"] = _quantity()

    package = _package_v19(citizens)
    citizens["package.core-calculations.v19.json"] = package

    registry = _load(CONTENT / "published-packages.v13.json")
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
    if (package["id"], "v19") not in existing_pkgs:
        registry["packages"].append(
            {
                "id": package["id"],
                "version": "v19",
                "checksum": package["package_checksum"],
            }
        )
    registry["packages"] = sorted(
        registry["packages"], key=lambda row: (row["id"], row["version"])
    )
    # Bump registry version marker for the successor published surface.
    if "version" in registry:
        registry["version"] = "v14"
    elif "id" in registry:
        pass
    citizens["published-packages.v14.json"] = registry
    return citizens


def render_fixture_files(citizens: dict[str, dict[str, Any]]) -> dict[Path, bytes]:
    registry_bytes = _document(citizens["published-packages.v14.json"])
    package = citizens["package.core-calculations.v19.json"]
    release = {
        "schema": "release-registry.v1",
        "id": "demo.release.2025",
        "version": "v12",
        "package_registry_sha256": hashlib.sha256(registry_bytes).hexdigest(),
    }
    release_bytes = _document(release)
    adoption = {
        "schema": "act.v1",
        "act_id": "demo.act.adopt.core.v19",
        "kind": "package-adoption",
        "actor": "demo.user.filer-1",
        "at": "2026-08-05T12:00:00Z",
        "committed_against": 1,
        "payload": {
            "package": {
                "id": package["id"],
                "version": "v19",
                "checksum": package["package_checksum"],
            },
            "release": {
                "id": "demo.release.2025",
                "version": "v12",
                "checksum": hashlib.sha256(release_bytes).hexdigest(),
            },
            "scope": {"jurisdiction": "us", "year": "2025"},
            "revision": 18,
            "supersedes": "demo.act.adopt.core.v18",
            "audit": {
                "note": (
                    "synthetic Form 1099-INT box-8 line-2a succession adoption; "
                    "non-authoritative"
                )
            },
        },
    }
    return {
        FIXTURES
        / "publication_surface"
        / "releases"
        / "demo.release.2025.v12.json": release_bytes,
        FIXTURES / "adoptions" / "adopt-core-v19-current.json": _document(adoption),
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
