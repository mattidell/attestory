"""P3 revision probe: run the respecified successor citizens this revision
proposes, using P2's throwaway-surface technique (a temporary registry,
release, and member directory; nothing is written into ``packages/content``).

Covers the charter's six items:

1. the box 2 read with an over-limit principal (finding 1's repair);
2. an absent box 9 (finding 5's repair);
3. the closed-empty row, unchanged;
4. the unresolved selection's validity and the sentences it actually
   produces for "can't tell" and for a refinance (findings 2 and 4's
   repair, via a new per-statement ``residence-interest-reason`` fact
   that supplies the sentence, read by the selection rule);
5. a deliberate double match on the line 8a symbol, to show the
   demonstrations would detect it (finding 6);
6. the personal-expense zero next to zero interest, as the person sees
   them (section 2 "How a disallowed statement differs from zero interest").

None of this is adopted. Every result below is a probe result. The
successor rules built here are not citizens; they exist only in this
process's temporary directory. Run from the repository root:

    python3 docs/phases/tax-circumstance-breadth/milestones/mortgage-interest-circumstances-evidence/p3_probe.py
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.derivation.production_resolver import PublicationSurface

_P0_PATH = Path(__file__).with_name("p0_current_path.py")
_P0_SPEC = importlib.util.spec_from_file_location("p0_current_path", _P0_PATH)
assert _P0_SPEC is not None and _P0_SPEC.loader is not None
p0 = importlib.util.module_from_spec(_P0_SPEC)
_P0_SPEC.loader.exec_module(p0)

from tests.test_f1098_mortgage_interest_line12e_track2 import (  # noqa: E402
    _attested,
    _load,
    _member_fact_id,
)

CONTENT = p0.CONTENT
PACKAGE_PATH = p0.PACKAGE_PATH
REGISTRY_PATH = p0.REGISTRY_PATH
RELEASE_PATH = p0.RELEASE_PATH
SCOPE = p0.SCOPE
USER = p0.USER
LINE8A_SYMBOL = "tax.us.2025.schedule-a.line8a"

FACT = "tax.us.2025.f1098."
BOX1 = FACT + "box1-mortgage-interest"
BOX2 = FACT + "box2-outstanding-principal"
BOX9 = FACT + "box9-number-of-properties"
REASON = FACT + "residence-interest-reason"
INERT = FACT + "inert-path-unwritten"
UNRESOLVED_SYMBOL = FACT + "residence-interest-unresolved"
LIMIT_PARAM = "tax.us.2025.f1098.mortgage-interest-limit"
BOX9_DEFAULT_PARAM = "tax.us.2025.parameter.f1098-box9-default-single-property"

NEW_YES_NO_FACTS = tuple(
    FACT + short
    for short in (
        "owns-the-home",
        "lives-there-most-of-the-time",
        "home-is-collateral",
        "owes-the-loan",
        "paid-the-interest",
        "no-one-else-owes-it",
        "this-is-the-original-loan",
    )
)
WHAT_FOR = FACT + "what-the-money-paid-for"
CERT = FACT + "mortgage-credit-certificate-received"


# ---------------------------------------------------------------------------
# New content: fact types, parameter, rules, field
# ---------------------------------------------------------------------------


def _identity_keys() -> list[dict[str, Any]]:
    return [
        {"name": "payer", "kind": "entity", "entity_kind": "tax.us.mortgage-lender"},
        {"name": "statement", "kind": "entity", "entity_kind": "tax.us.1098-statement"},
        {"name": "tax-year", "kind": "literal", "values": ["2025"]},
    ]


def _yes_no_fact(fact_id: str) -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": fact_id,
        "version": "v1",
        "title": f"P3 probe ordinary statement: {fact_id.rsplit('.', 1)[-1]}",
        "nature": "determinable",
        "identity_keys": _identity_keys(),
        "value_schema": {"enum": ["yes", "no", "cannot-tell"]},
        "supersession": {"policy": "free"},
    }


def _bundle() -> dict[str, Any]:
    fact_types = [_yes_no_fact(short) for short in NEW_YES_NO_FACTS]
    fact_types.append({
        "schema": "fact-type.v2",
        "id": WHAT_FOR,
        "version": "v1",
        "title": "P3 probe ordinary statement: what the money paid for",
        "nature": "determinable",
        "identity_keys": _identity_keys(),
        "value_schema": {"enum": ["bought-the-home", "unrelated-personal-expense", "other", "cannot-tell"]},
        "supersession": {"policy": "free"},
    })
    fact_types.append({
        "schema": "fact-type.v2",
        "id": CERT,
        "version": "v1",
        "title": "P3 probe ordinary statement: mortgage credit certificate (polarity-safe, finding 7)",
        "nature": "determinable",
        "identity_keys": _identity_keys(),
        "value_schema": {"enum": ["received", "not-received", "cannot-tell"]},
        "supersession": {"policy": "free"},
    })
    fact_types.append({
        "schema": "fact-type.v2",
        "id": BOX9,
        "version": "v1",
        "title": "Form 1098 box9-number-of-properties (P3 probe successor: absent is one property, finding 5)",
        "nature": "determinable",
        "identity_keys": _identity_keys(),
        "value_schema": {"type": "number"},
        "supersession": {"policy": "free"},
        "optional_default": {"parameter": {"id": BOX9_DEFAULT_PARAM, "version": "v1"}},
    })
    fact_types.append({
        "schema": "fact-type.v2",
        "id": REASON,
        "version": "v1",
        "title": "P3 probe: the one reason this statement's interest is or is not qualified residence interest",
        "nature": "determinable",
        "identity_keys": _identity_keys(),
        "value_schema": {
            "enum": [
                "qualified",
                "use-unrelated-personal-expense",
                "not-collateral",
                "not-paid",
                "cannot-tell-use",
                "certificate-received",
                "debt-limit-over",
                "outside-coverage",
            ],
            "oneOf": [
                {"const": "qualified", "description": "The interest qualifies as home mortgage interest for this statement."},
                {"const": "use-unrelated-personal-expense", "description": "The borrowed money paid for a personal expense that was not buying, building, or improving the home, so this interest is not qualified residence interest."},
                {"const": "not-collateral", "description": "The home is not collateral for this loan, so the debt is not secured acquisition indebtedness."},
                {"const": "not-paid", "description": "The person said they do not owe this loan or did not pay this interest, so there is no deduction to publish for this statement."},
                {"const": "cannot-tell-use", "description": "You said you cannot tell what the borrowed money paid for. The application cannot reach a conclusion about this interest until that is known."},
                {"const": "certificate-received", "description": "A mortgage credit certificate was reported for this loan. The reduced amount is left with the person; this route does not compute Form 8396."},
                {"const": "debt-limit-over", "description": "The outstanding principal on this statement is over the limit this route uses. The prorated amount is left with the person."},
                {"const": "outside-coverage", "description": "This statement's circumstances are outside what this route computes. The treatment is left with the person."},
            ],
        },
        "supersession": {"policy": "free"},
    })
    fact_types.append({
        "schema": "fact-type.v2",
        "id": INERT,
        "version": "v1",
        "title": "Named by the unresolved-field's inert second selection path. Nothing writes it.",
        "nature": "determinable",
        "identity_keys": [{"name": "marker", "kind": "literal", "values": ["unused"]}],
        "value_schema": {"type": "string", "enum": ["unused"], "oneOf": [{"const": "unused", "description": "This value is never written."}]},
        "supersession": {"policy": "free"},
    })
    return {
        "schema": "bundle.v2",
        "id": "tax.us.2025.f1098-successor.vocabulary",
        "version": "v1",
        "label": "P3 probe: respecified Form 1098 ordinary statements and reason",
        "fact_types": fact_types,
    }


def _box9_default_parameter() -> dict[str, Any]:
    return {
        "schema": "parameter-declaration.v1",
        "id": BOX9_DEFAULT_PARAM,
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax", "effective_from": "2025-01-01"},
        "values": 1,
    }


def _ref(name: str) -> dict[str, Any]:
    return {"op": "ref", "name": name}


def _cat_eq(name: str, value: str) -> dict[str, Any]:
    return {
        "op": "categorical_compare", "cmp": "eq", "left": _ref(name),
        "right": {"op": "category_literal", "fact_type": {"id": name, "version": "v1"}, "value": value},
    }


def _reason_lit(value: str) -> dict[str, Any]:
    return {"op": "category_literal", "fact_type": {"id": REASON, "version": "v1"}, "value": value}


def _choose(when: Any, then: Any, otherwise: Any) -> dict[str, Any]:
    return {"op": "choose", "when": when, "then": then, "else": otherwise}


def _limit_ref() -> dict[str, Any]:
    return {"op": "parameter", "parameter_id": LIMIT_PARAM, "key": _ref("filing_status")}


def _reason_rule() -> dict[str, Any]:
    requires = [*NEW_YES_NO_FACTS, WHAT_FOR, CERT, BOX2, BOX9, "filing_status"]
    value = _choose(
        _cat_eq(WHAT_FOR, "unrelated-personal-expense"), _reason_lit("use-unrelated-personal-expense"),
        _choose(
            _cat_eq(FACT + "home-is-collateral", "no"), _reason_lit("not-collateral"),
            _choose(
                _cat_eq(FACT + "paid-the-interest", "no"), _reason_lit("not-paid"),
                _choose(
                    _cat_eq(WHAT_FOR, "cannot-tell"), _reason_lit("cannot-tell-use"),
                    _choose(
                        _cat_eq(CERT, "received"), _reason_lit("certificate-received"),
                        _choose(
                            {"op": "compare", "cmp": "gt", "left": _ref(BOX2), "right": _limit_ref()},
                            _reason_lit("debt-limit-over"),
                            _choose(
                                {
                                    "op": "all",
                                    "args": [
                                        _cat_eq(FACT + "owns-the-home", "yes"),
                                        _cat_eq(FACT + "lives-there-most-of-the-time", "yes"),
                                        _cat_eq(FACT + "home-is-collateral", "yes"),
                                        _cat_eq(FACT + "paid-the-interest", "yes"),
                                        _cat_eq(FACT + "no-one-else-owes-it", "yes"),
                                        _cat_eq(WHAT_FOR, "bought-the-home"),
                                        _cat_eq(FACT + "this-is-the-original-loan", "yes"),
                                        _cat_eq(CERT, "not-received"),
                                        {"op": "compare", "cmp": "eq", "left": _ref(BOX9), "right": 1},
                                    ],
                                },
                                _reason_lit("qualified"),
                                _reason_lit("outside-coverage"),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )
    return {
        "schema": "rule-artifact.v13",
        "id": "tax.us.2025.rule.f1098-residence-interest-reason",
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation",
        "subject": {"id": BOX1, "version": "v1"},
        "requires": requires,
        "pins": [{"role": "parameter", "id": LIMIT_PARAM, "version": "v1"}],
        "when": True,
        "value": value,
        "publishes": REASON,
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "citations": [],
        "notes": "P3 probe only. Not an adopted rule. See findings 2 and 4.",
    }


def _line8a_rule(rule_id: str) -> dict[str, Any]:
    """One producer for ``tax.us.2025.schedule-a.line8a`` (section 2's four
    arms collapsed to one, per finding 6's "propose fewer" option). This
    probe found a further reason to collapse them: the Schedule A
    attachment's own itemization ties out this exact symbol through
    ``_one_row``, which requires exactly one disposition row for it --
    satisfied only while exactly one rule is ever attempted for it at all,
    which four independent producer rules do not guarantee even when their
    guards are genuinely disjoint. See the probe's ``double-match`` result
    and the design's revision note.

    finding 1's repair: ``ref``, not ``collect``, for box 2. finding 5's
    repair: box 9 reads the successor fact type, whose ``optional_default``
    supplies 1 when absent. Box 3's date stop is deferred -- see the
    findings (``rule-artifact.v13`` has no date-comparison op)."""
    requires = [BOX9, BOX2, "tax.us.2025.f1098.box3-origination-date", "filing_status", *NEW_YES_NO_FACTS, WHAT_FOR, CERT]
    qualified = {
        "op": "all",
        "args": [
            _cat_eq(FACT + "owns-the-home", "yes"),
            _cat_eq(FACT + "lives-there-most-of-the-time", "yes"),
            _cat_eq(FACT + "home-is-collateral", "yes"),
            _cat_eq(FACT + "paid-the-interest", "yes"),
            _cat_eq(FACT + "no-one-else-owes-it", "yes"),
            _cat_eq(WHAT_FOR, "bought-the-home"),
            _cat_eq(FACT + "this-is-the-original-loan", "yes"),
            _cat_eq(CERT, "not-received"),
            {"op": "compare", "cmp": "eq", "left": _ref(BOX9), "right": 1},
        ],
    }
    value = _choose(
        _cat_eq(WHAT_FOR, "unrelated-personal-expense"), 0,
        _choose(
            _cat_eq(FACT + "home-is-collateral", "no"), 0,
            _choose(
                _cat_eq(FACT + "paid-the-interest", "no"), 0,
                _choose(
                    qualified,
                    _choose(
                        {"op": "compare", "cmp": "gt", "left": _ref(BOX2), "right": _limit_ref()},
                        {"op": "block", "code": "VALUE_INVALID"},
                        {"op": "add", "args": [{"op": "collect", "name": BOX1, "source_set": "tax.us.2025.f1098"}]},
                    ),
                    {"op": "block", "code": "DEPENDENCY_ABSENT"},
                ),
            ),
        ),
    )
    when = {
        "op": "all",
        "args": [
            {"op": "require_closed", "source_set": "tax.us.2025.f1098"},
            _choose(
                {"op": "compare", "cmp": "gt", "left": {"op": "count", "name": BOX1, "source_set": "tax.us.2025.f1098"}, "right": 1},
                {"op": "block", "code": "MULTIPLE_F1098_OUT_OF_SCOPE"},
                {"op": "compare", "cmp": "eq", "left": {"op": "count", "name": BOX1, "source_set": "tax.us.2025.f1098"}, "right": 1},
            ),
        ],
    }
    return {
        "schema": "rule-artifact.v13",
        "id": rule_id,
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation",
        "requires": requires,
        "pins": [{"role": "parameter", "id": LIMIT_PARAM, "version": "v1"}],
        "when": when,
        "value": value,
        "publishes": LINE8A_SYMBOL,
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "citations": [],
        "composition": {"id": "tax.us.2025.schedule-a", "version": "v1"},
        "notes": "P3 probe only.",
    }


def _unresolved_rule() -> dict[str, Any]:
    active_path = {
        "id": "statement",
        "activity": {"kind": "source_nonempty", "member_fact_types": [{"id": BOX1, "version": "v1"}]},
        "reads_subject_results": [{"symbol": REASON, "subject": {"id": BOX1, "version": "v1"}}],
        "requires": [],
        "pins": [],
        "when": {
            "op": "not",
            "value": {
                "op": "collect_categorical_all_equal", "name": REASON,
                "value": {"op": "category_literal", "fact_type": {"id": REASON, "version": "v1"}, "value": "qualified"},
            },
        },
        "value": {"op": "block", "code": "DEPENDENCY_ABSENT"},
    }
    inert_path = {
        "id": "inert",
        "activity": {"kind": "source_nonempty", "member_fact_types": [{"id": INERT, "version": "v1"}]},
        "reads_subject_results": [],
        "requires": [],
        "pins": [],
        "when": True,
        "value": {"op": "block", "code": "DEPENDENCY_ABSENT"},
    }
    return {
        "schema": "rule-artifact.v13",
        "id": "tax.us.2025.rule.f1098-residence-interest-unresolved",
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
            "default": {"id": "neither", "reads_subject_results": [], "requires": [], "pins": [], "when": False, "value": False},
            "refusal": {"code": "DEPENDENCY_INVALID", "missing": ["f1098-residence-interest-unresolved-inert-path-conflict"], "pins": []},
        },
        "publishes": UNRESOLVED_SYMBOL,
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "citations": [],
        "notes": "P3 probe only. Second path is an inert placeholder, same technique as tax.us.2025.sli.inert-path-unwritten.",
    }


def _unresolved_field() -> dict[str, Any]:
    return {
        "schema": "form-field.v3",
        "id": "tax.us.2025.form.f1098.residence-interest-unresolved",
        "version": "v1",
        "form": {"authority": "IRS", "form_id": "1040-SCH-A", "jurisdiction": "US-federal", "tax_year": 2025},
        "line": "f1098-unresolved",
        "label": "P3 probe: open condition on the home mortgage interest statement",
        "description": "P3 probe field. Inapplicable when line 8a publishes; otherwise names the open condition.",
        "binds_symbol": UNRESOLVED_SYMBOL,
        "dispositions": {
            "blocked": {"codes": ["DEPENDENCY_ABSENT", "DEPENDENCY_INVALID"], "explain": "An open condition on the Form 1098 statement is still unresolved.", "render": ""},
            "guard_inapplicable": {"explain": "No open condition: line 8a already published, or there is no statement.", "render": ""},
            "published_value": {"explain": "Not used: this field never publishes a value.", "render": ""},
            "computed_zero": {"explain": "Not used: this field never publishes a value.", "render": ""},
            "closure_backed_zero": {"explain": "Not used: this field never publishes a value.", "render": ""},
        },
    }


# ---------------------------------------------------------------------------
# Throwaway surface
# ---------------------------------------------------------------------------


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text("utf-8"))


def _write_member(member_dir: Path, name: str, citizen: dict[str, Any]) -> tuple[str, str]:
    path = member_dir / name
    path.write_text(json.dumps(citizen, indent=2) + "\n", encoding="utf-8")
    stored = _read_json(path)
    return citizen["id"], citizen_checksum(stored)


def _build_surface(root: Path, *, include_duplicate: bool) -> tuple[PublicationSurface, str, str, str, str]:
    member_dir = root / "members"
    member_dir.mkdir()
    old_line8a_file = "rule.schedule-a-line8a.json"
    old_f1098_bundle_file = "f1098.bundle.json"
    for source in sorted(CONTENT.rglob("*.json")):
        if source.name in (old_line8a_file, old_f1098_bundle_file):
            continue
        dest = member_dir / source.relative_to(CONTENT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.link(source, dest)
        except OSError:
            dest.write_bytes(source.read_bytes())

    registry = _read_json(REGISTRY_PATH)
    new_checksums: list[tuple[str, str, str]] = []  # (id, version, checksum)

    # finding 5's probe: box 9 moves from this bundle (plain number, no
    # optional_default) to the successor bundle (optional_default = 1).
    # One id cannot carry two versions of the "right away" schema contract
    # in this package, so the modified copy here drops box 9 entirely
    # rather than declaring a colliding second version. The same (id,
    # version) keeps its declared checksum in the registry; only the
    # bytes in this throwaway member directory differ.
    old_f1098_bundle = _read_json(CONTENT / old_f1098_bundle_file)
    old_f1098_bundle["fact_types"] = [
        ft for ft in old_f1098_bundle["fact_types"] if ft.get("id") != BOX9
    ]
    f1098_bundle_id, f1098_bundle_sum = _write_member(member_dir, old_f1098_bundle_file, old_f1098_bundle)
    replaced = 0
    for entry in registry["citizens"]:
        if entry.get("id") == f1098_bundle_id and entry.get("version") == "v1":
            entry["checksum"] = f1098_bundle_sum
            replaced += 1
    if replaced != 1:
        raise AssertionError(f"expected exactly one f1098.vocabulary registry entry, replaced {replaced}")

    bundle_id, bundle_sum = _write_member(member_dir, "f1098-successor.bundle.json", _bundle())
    new_checksums.append((bundle_id, "v1", bundle_sum))

    param_id, param_sum = _write_member(member_dir, "parameter.f1098-box9-default-single-property.json", _box9_default_parameter())
    new_checksums.append((param_id, "v1", param_sum))

    reason_id, reason_sum = _write_member(member_dir, "rule.f1098-residence-interest-reason.probe.json", _reason_rule())
    new_checksums.append((reason_id, "v1", reason_sum))

    line8a_id, line8a_sum = _write_member(member_dir, "rule.f1098-line8a.probe.json", _line8a_rule("tax.us.2025.rule.f1098-line8a-probe"))
    new_checksums.append((line8a_id, "v1", line8a_sum))

    unresolved_id, unresolved_sum = _write_member(member_dir, "rule.f1098-residence-interest-unresolved.probe.json", _unresolved_rule())
    new_checksums.append((unresolved_id, "v1", unresolved_sum))

    field_id, field_sum = _write_member(member_dir, "form1040.f1098-residence-interest-unresolved.form-field.probe.json", _unresolved_field())
    new_checksums.append((field_id, "v1", field_sum))

    duplicate_id = None
    if include_duplicate:
        # finding 6's hazard, deliberately reproduced: a second producer of
        # the same symbol, guard-for-guard identical to the first. Not a
        # repair -- a probe of what the design must not do.
        dup = _line8a_rule("tax.us.2025.rule.f1098-line8a-duplicate-probe")
        dup["notes"] = "P3 probe only. Deliberate duplicate producer, to probe finding 6."
        duplicate_id, dup_sum = _write_member(member_dir, "rule.f1098-line8a-duplicate.probe.json", dup)
        new_checksums.append((duplicate_id, "v1", dup_sum))

    for cid, version, checksum in new_checksums:
        registry["citizens"].append({"id": cid, "version": version, "checksum": checksum})

    package = _read_json(PACKAGE_PATH)
    package["version"] = "v43"
    package.setdefault("input_bindings", []).append({
        "fact_type": {"id": BOX9, "version": "v1"}, "mode": "optional_default", "symbol": BOX9,
    })
    package["members"] = [m for m in package["members"] if m["id"] != "tax.us.2025.schedule-a.line8a.rule"]
    package["entrypoints"] = [e for e in package["entrypoints"] if e["id"] != "tax.us.2025.schedule-a.line8a.rule"]
    package["entrypoints"].append({"id": line8a_id, "version": "v1"})
    if duplicate_id is not None:
        package["entrypoints"].append({"id": duplicate_id, "version": "v1"})
    package["members"].append({"id": bundle_id, "role": "fact-type-bundle", "schema": "bundle.v2", "version": "v1"})
    package["members"].append({"id": param_id, "role": "parameter", "schema": "parameter-declaration.v1", "version": "v1"})
    package["members"].append({"id": reason_id, "role": "computation", "schema": "rule-artifact.v13", "version": "v1"})
    package["members"].append({"id": line8a_id, "role": "computation", "schema": "rule-artifact.v13", "version": "v1"})
    package["members"].append({"id": unresolved_id, "role": "computation", "schema": "rule-artifact.v13", "version": "v1"})
    package["members"].append({"id": field_id, "role": "form-field", "schema": "form-field.v3", "version": "v1"})
    if duplicate_id is not None:
        package["members"].append({"id": duplicate_id, "role": "computation", "schema": "rule-artifact.v13", "version": "v1"})
    package["conflict_semantics"] = [
        row for row in package["conflict_semantics"] if row.get("symbol") != LINE8A_SYMBOL
    ]
    if duplicate_id is not None:
        package["conflict_semantics"].append({"symbol": LINE8A_SYMBOL, "selected_producer": {"id": line8a_id, "version": "v1"}})
    package_path = member_dir / "package.core-calculations.v43.json"
    package["package_checksum"] = package_instance_checksum(package)
    package_path.write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    package_checksum = package["package_checksum"]
    registry.setdefault("packages", [])
    registry["packages"].append({"id": package["id"], "version": "v43", "checksum": package_checksum})

    registry_path = root / "published-packages.probe.json"
    registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")

    release = _read_json(RELEASE_PATH)
    release["package_registry_sha256"] = hashlib.sha256(registry_path.read_bytes()).hexdigest()
    release_dir = root / "releases"
    release_dir.mkdir()
    release_path = release_dir / RELEASE_PATH.name
    release_path.write_text(json.dumps(release, indent=2) + "\n", encoding="utf-8")
    release_checksum = hashlib.sha256(release_path.read_bytes()).hexdigest()
    return (
        PublicationSurface(release_dir, registry_path, member_dir),
        release_checksum,
        package["id"],
        "v43",
        package_checksum,
    )


# ---------------------------------------------------------------------------
# Acts
# ---------------------------------------------------------------------------


def _member_fact_id_here(fact_type: str) -> str:
    # The same identity keys P0/P2's own fixture uses for its one statement.
    return _member_fact_id(fact_type, "demo.f1098.lender.a", "demo.f1098.stmt.a")


def _probe_acts(
    *,
    box1: float = 20000.0,
    box2: float = 200000.0,
    box9: float | None = 1.0,
    answers: dict[str, str] | None = None,
) -> list[dict[str, object]]:
    """The proven P0/P2 base corpus (wages, filing status, every shared
    absence declaration this package's dependency chain needs, one Form
    1098 statement with its box amounts and legacy confirmations, under
    the real v42 content) plus this probe's new ordinary statements on the
    same statement keys. The trailing adoption is replaced by ``_finish``."""
    acts = p0._f1098_acts(interest=box1, wages=90000, box2=box2, box9=(box9 if box9 is not None else 1.0))
    if box9 is None:
        acts = [
            row for row in acts
            if not (
                isinstance(row.get("payload"), dict)
                and isinstance(row["payload"].get("finding"), dict)
                and str(row["payload"]["finding"].get("fact_id", "")).startswith(BOX9 + "|")
            )
        ]
    acts.pop()  # drop the v29 adoption; _finish appends this probe's own
    acts.extend(p0._selected_current_dependency_acts())

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append({
            "schema": "act.v1", "act_id": f"demo.f1098.p3.act.{len(acts):03d}", "kind": kind,
            "actor": USER, "at": f"2026-10-13T12:{len(acts) // 60:02d}:{len(acts) % 60:02d}Z",
            "committed_against": len(acts), "payload": payload,
        })

    add("bundle-adoption", {"bundle": _bundle()})
    resolved_answers = {
        "owns-the-home": "yes", "lives-there-most-of-the-time": "yes", "home-is-collateral": "yes",
        "owes-the-loan": "yes", "paid-the-interest": "yes", "no-one-else-owes-it": "yes",
        "what-the-money-paid-for": "bought-the-home", "this-is-the-original-loan": "yes",
        "mortgage-credit-certificate-received": "not-received",
    }
    if answers:
        resolved_answers.update(answers)
    for short, value in resolved_answers.items():
        add("assertion", {"finding": _attested(f"demo.f1098.p3.{short}", _member_fact_id_here(FACT + short), value)})
    return acts


def _no_statement_acts() -> list[dict[str, object]]:
    """The closed-empty row: no Form 1098 at all, flag true. The proven P0/P2
    base corpus with ``interest=None``."""
    acts = p0._path_a_acts(wages=90000)
    acts.pop()
    acts.extend(p0._selected_current_dependency_acts())
    return acts


def _finish(
    acts: list[dict[str, object]],
    *,
    release_checksum: str,
    package_id: str,
    package_version: str,
    package_checksum: str,
) -> list[dict[str, object]]:
    built = copy.deepcopy(acts)
    adoption = p0._current_adoption(p0._load_fixture_adoption(), len(built))
    payload = adoption["payload"]
    assert isinstance(payload, dict)
    payload["package"] = {"id": package_id, "version": package_version, "checksum": package_checksum}
    release = payload["release"]
    assert isinstance(release, dict)
    release["checksum"] = release_checksum
    payload["audit"] = {"note": "synthetic P3 revision probe; throwaway surface, not adopted content"}
    built.append(adoption)
    for index, row in enumerate(built):
        row["committed_against"] = index
    return built


# ---------------------------------------------------------------------------
# Run + report
# ---------------------------------------------------------------------------


def _run(acts: list[dict[str, object]], run_id: str, surface: PublicationSurface) -> dict[str, Any]:
    started = time.monotonic()
    with TemporaryDirectory() as tmp:
        try:
            result = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "workspace"), repo_root=ROOT,
                authoritative_acts=acts, workspace_revision=len(acts), run_scope=SCOPE,
                scope_user=USER, request={"schema": "run-request.v1"}, run_id=run_id,
                governance_pins=[], surface=surface, output_name="out.json",
            )
        except Exception as exc:  # a composition defect is a probe result, not a script failure
            return {"run_id": run_id, "seconds": round(time.monotonic() - started, 1), "exception": {"type": type(exc).__name__, "message": str(exc)}}
        elapsed = round(time.monotonic() - started, 1)
        if result.refusal is not None:
            return {"run_id": run_id, "seconds": elapsed, "refusal": {"reason": result.refusal.reason, "detail": result.refusal.detail, "issues": [dict(i) for i in result.refusal.issues]}}
        assert result.output_path is not None and result.presentation_path is not None
        report = json.loads(result.output_path.read_text("utf-8"))
        model = json.loads(result.presentation_path.read_text("utf-8"))
        rows = p0._by_artifact(report)
        findings = p0._publication_rows(result)
        line8a_rows = [r for r in report.get("dispositions", []) if r.get("symbol") == LINE8A_SYMBOL or "line8a" in str(r.get("artifact_id", ""))]
        reason_pubs = [f for f in findings if str(f.get("symbol", "")).startswith(REASON)]
        reason_rows = [r for r in report.get("dispositions", []) if "residence-interest-reason" in str(r.get("artifact_id", ""))]
        unresolved_rows = [r for r in report.get("dispositions", []) if "residence-interest-unresolved" in str(r.get("artifact_id", ""))]
        line8a_pubs = [f for f in findings if f.get("symbol") == LINE8A_SYMBOL]
        line12e_section = next((s for s in model.get("sections", []) if s["id"] == "line-12e"), None)
        unresolved_field = next(
            (
                s for s in model.get("sections", [])
                if (s.get("field") or {}).get("id") == "tax.us.2025.form.f1098.residence-interest-unresolved"
            ),
            None,
        )
        return {
            "run_id": run_id,
            "seconds": elapsed,
            "line8a_dispositions": line8a_rows,
            "line8a_publications": line8a_pubs,
            "reason_publications": reason_pubs,
            "reason_dispositions": reason_rows,
            "unresolved_dispositions": unresolved_rows,
            "unresolved_field_resolved": (unresolved_field or {}).get("resolved"),
            "line12e_value": (line12e_section or {}).get("resolved", {}).get("value"),
            "line12e_disposition": (line12e_section or {}).get("resolved", {}).get("disposition"),
        }


def main() -> None:
    results: dict[str, Any] = {}
    with TemporaryDirectory() as tmp:
        surface, release_checksum, package_id, package_version, package_checksum = _build_surface(
            Path(tmp), include_duplicate=False
        )

        def run_case(name: str, acts: list[dict[str, object]]) -> None:
            built = _finish(
                acts,
                release_checksum=release_checksum,
                package_id=package_id,
                package_version=package_version,
                package_checksum=package_checksum,
            )
            results[name] = _run(built, f"demo.f1098.p3.{name}", surface)

        run_case("supported-purchase", _probe_acts())
        run_case("box2-over-limit", _probe_acts(box2=800000.0))
        run_case("box9-absent", _probe_acts(box9=None))
        run_case("personal-expense", _probe_acts(answers={"what-the-money-paid-for": "unrelated-personal-expense"}))
        run_case("cannot-tell-use", _probe_acts(answers={"what-the-money-paid-for": "cannot-tell"}))
        run_case("refinance", _probe_acts(answers={"this-is-the-original-loan": "no"}))
        run_case("zero-interest", _probe_acts(box1=0.0))
        run_case("closed-empty", _no_statement_acts())

    with TemporaryDirectory() as tmp:
        surface, release_checksum, package_id, package_version, package_checksum = _build_surface(
            Path(tmp), include_duplicate=True
        )

        def run_dup(name: str, acts: list[dict[str, object]]) -> None:
            built = _finish(
                acts, release_checksum=release_checksum, package_id=package_id,
                package_version=package_version, package_checksum=package_checksum,
            )
            results[name] = _run(built, f"demo.f1098.p3.{name}", surface)

        # Zero-dollar double match: the attachment is inapplicable (total
        # under the standard deduction), so its tie-out never joins this
        # symbol. First-publisher-wins is visible cleanly here.
        run_dup("double-match-zero", _probe_acts(answers={"what-the-money-paid-for": "unrelated-personal-expense"}))
        # Qualifying double match: the attachment IS required (total over
        # the standard deduction), so its own tie-out joins this symbol.
        run_dup("double-match-qualifying", _probe_acts())

    print(json.dumps({"probe": "p3-revision", "results": results}, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
