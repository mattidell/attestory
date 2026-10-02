#!/usr/bin/env python3
"""Generate three ignored, one-run Track 6b presentation fixtures.

Run from the repository root with:

    python3 tools/presentation_harness/examples/generate_track6b_saved_presentations.py

Each case uses one disposable package and one ``live_coordinate_run`` for both
the worksheet and statement calculation. The output fixture is copied from
the real coordinator's presentation writer, then reopened and validated.
All added identities and values are synthetic ``demo.*`` data.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

# Allow the documented direct command from the repository root as well as
# `python -m ...`; Python otherwise puts only this nested tools directory on
# `sys.path[0]`.
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import package_instance_checksum, validate_package
from packages.derivation.presentation_projection import validate_presentation_model
from packages.derivation.production_resolver import PublicationSurface
from tests.test_f1098e_student_loan_interest_agi_track6 import (
    SCOPE,
    USER,
    Statement,
    _f1098e_acts,
    _member_fact_id,
    _renumber,
)
from tests.test_sli_bounded_method_transfer_p1 import (
    CONTENT,
    PACKAGE_FILE,
    REGISTRY_FILE,
    RELEASE_FILE,
    TRACK6,
    DisposableSurface,
)
from tools.generate_ssa_no_activity_content import _bytes, _citizen_checksum

RULE_SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}
BOX1 = "tax.us.2025.f1098e.box1-student-loan-interest"
LINKS = "demo.tax.sli-statement-to-borrowing"
CLAIMS = "demo.tax.sli-statement-scope-claim"
REDUCTIONS = "demo.tax.sli-borrowing-reduction"
COUNT = "demo.tax.sli-statement-link-count"
CLASSIFIER = "demo.tax.sli-statement-scope-classification"
SCOPE_COUNT = "demo.tax.sli-statement-scope-disqualifier-count"
AMOUNT = "demo.tax.sli-statement-amount"
CONCLUSION = "demo.tax.sli-bare-statement-conclusion"
CONCLUSION_TYPE = "demo.tax.sli-conclusion-token"
RESPONSIBILITY_TYPE = "demo.tax.sli-responsibility-token"
NO_LINK_PARAMETER = "demo.parameter.sli-no-link-reduction"
NO_CLAIM_PARAMETER = "demo.parameter.sli-no-statement-scope-claim"
RESPONSIBILITIES = (
    ("demo.tax.sli-responsibility-institution", "demo.rule.sli-responsibility-institution"),
    ("demo.tax.sli-responsibility-credential", "demo.rule.sli-responsibility-credential"),
    ("demo.tax.sli-responsibility-half-time", "demo.rule.sli-responsibility-half-time"),
)
LINKER = "demo.rule.sli-link-count"
CLASSIFIER_RULE = "demo.rule.sli-statement-scope-classifier"
SCOPE_COUNT_RULE = "demo.rule.sli-statement-scope-disqualifier-count"
AMOUNT_RULE = "demo.rule.sli-statement-amount"
CONCLUSION_RULE = "demo.rule.sli-bare-statement-conclusion"
REDUCTION_RULE = "demo.rule.sli-link-reduction"
CLAIM_BUNDLE = "demo.bundle.sli-statement-reader"
CLAIM_BUNDLE_VERSION = "v1"
CLAIM_ENTITY_KIND = "demo.sli-statement-scope-circumstance"
CLAIM_SCENARIOS = {"ordinary": None, "adverse": "vehicle", "unresolved": "demo-untreated"}


def _fact_type(
    fact_id: str,
    title: str,
    identity_keys: list[dict[str, Any]],
    value_schema: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema": "fact-type.v2", "id": fact_id, "version": "v1", "title": title,
        "nature": "determinable", "identity_keys": identity_keys,
        "value_schema": value_schema, "supersession": {"policy": "free"},
    }


def _attested(finding_id: str, fact_id: str, value: Any) -> dict[str, Any]:
    return {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }


def _reader_rule(
    rule_id: str,
    publishes: str,
    *,
    subject: str = BOX1,
    value: Any,
    role: str | None = None,
    requires: list[str] | None = None,
    when: Any = True,
    joined: str | None = None,
    direction: str | None = None,
    wording: str | None = None,
    line_note: str | None = None,
) -> dict[str, Any]:
    rule: dict[str, Any] = {
        "schema": "rule-artifact.v12", "id": rule_id, "version": "v1", "scope": RULE_SCOPE,
        "subject": {"id": subject, "version": "v1"}, "role": "computation",
        "requires": list(requires or []), "pins": [], "when": when, "value": value,
        "publishes": publishes, "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
    }
    if joined is not None:
        rule["joined"] = {"id": joined, "version": "v1"}
        rule["direction"] = direction or "joined_contains_subject"
    if role:
        rule["reader_role"] = role
    if wording is not None:
        rule["wording"] = wording
    if line_note is not None:
        rule["lineNote"] = line_note
    return rule


def _ref(symbol: str) -> dict[str, str]:
    return {"op": "ref", "name": symbol}


def _eq_zero(symbol: str) -> dict[str, Any]:
    return {"op": "compare", "cmp": "eq", "left": _ref(symbol), "right": 0}


def _token(token_type: str, value: str) -> dict[str, Any]:
    return {"op": "category_literal", "fact_type": {"id": token_type, "version": "v1"}, "value": value}


def _link_coverage(links: str, reductions: str, parameter: str) -> dict[str, Any]:
    return {
        "op": "link_coverage", "links": links, "reductions": reductions,
        "empty": {"parameter": {"id": parameter, "version": "v1"}},
    }


def _package_members() -> tuple[list[tuple[dict[str, Any], str]], list[dict[str, str]]]:
    statement_keys: list[dict[str, Any]] = [
        {"name": "lender", "kind": "entity", "entity_kind": "tax.us.student-loan-lender"},
        {"name": "statement", "kind": "entity", "entity_kind": "tax.us.1098e-statement"},
        {"name": "tax-year", "kind": "literal", "values": ["2025"]},
    ]
    bundle_types = [
        _fact_type(LINKS, "Synthetic statement-to-borrowing links", statement_keys + [
            {"name": "borrowing", "kind": "entity", "entity_kind": "demo.sli-borrowing"},
        ], {"type": "object"}),
        _fact_type(CLAIMS, "Synthetic statement-wide use-of-proceeds claims", statement_keys + [
            {"name": "circumstance", "kind": "entity", "entity_kind": CLAIM_ENTITY_KIND},
        ], {"enum": ["tuition", "vehicle", "demo-untreated"]}),
        _fact_type(CONCLUSION_TYPE, "Synthetic bare-statement conclusion token", statement_keys, {"enum": ["no-enumerated-adverse"]}),
        _fact_type(RESPONSIBILITY_TYPE, "Synthetic responsibility applicability token", statement_keys, {"enum": ["applies"]}),
    ]
    bundle = {
        "schema": "bundle.v2", "id": CLAIM_BUNDLE, "version": CLAIM_BUNDLE_VERSION,
        "label": "Synthetic Track 6b statement-reader input vocabulary", "fact_types": bundle_types,
    }
    def parameter(parameter_id: str) -> tuple[dict[str, Any], str]:
        return ({
            "schema": "parameter-declaration.v1", "id": parameter_id, "version": "v1",
            "scope": RULE_SCOPE, "values": "0",
        }, "parameter")

    link_count = _reader_rule(
        LINKER, COUNT, value={"op": "link_count", "links": LINKS}, role="link-count", joined=LINKS,
    )
    classifier_value = {
        "op": "choose",
        "when": {"op": "categorical_compare", "cmp": "eq", "left": _ref(CLAIMS), "right": _token(CLAIMS, "vehicle")},
        "then": 1,
        "else": {
            "op": "choose",
            "when": {"op": "categorical_compare", "cmp": "eq", "left": _ref(CLAIMS), "right": _token(CLAIMS, "tuition")},
            "then": 0,
            "else": {"op": "block", "code": "DEPENDENCY_INVALID"},
        },
    }
    classifier = _reader_rule(CLASSIFIER_RULE, CLASSIFIER, subject=CLAIMS, value=classifier_value, role="statement-scope-classifier")
    scope_count = _reader_rule(
        SCOPE_COUNT_RULE, SCOPE_COUNT, value=_link_coverage(CLAIMS, CLASSIFIER, NO_CLAIM_PARAMETER),
        role="statement-scope-disqualifier-count", joined=CLAIMS,
    )
    reduction = _reader_rule(REDUCTION_RULE, REDUCTIONS, subject=LINKS, value=0)
    amount_value = {
        "op": "choose",
        "when": {"op": "compare", "cmp": "gt", "left": _ref(SCOPE_COUNT), "right": 0},
        "then": 0,
        "else": {
            "op": "subtract", "left": _ref(BOX1),
            "right": _link_coverage(LINKS, REDUCTIONS, NO_LINK_PARAMETER),
        },
    }
    amount = _reader_rule(AMOUNT_RULE, AMOUNT, value=amount_value, role="statement-amount", requires=[SCOPE_COUNT], joined=LINKS)
    conclusion = _reader_rule(
        CONCLUSION_RULE, CONCLUSION, value=_token(CONCLUSION_TYPE, "no-enumerated-adverse"),
        role="bare-statement-conclusion", requires=[COUNT, SCOPE_COUNT],
        when={"op": "all", "args": [_eq_zero(COUNT), _eq_zero(SCOPE_COUNT)]},
        line_note=("Eligibility is taken as met for the interest on {statement}: nothing said about this statement as a whole "
                   "matches a disqualifying circumstance this calculation checks."),
    )
    resp_wordings = (
        "No borrowing is currently linked to {statement}. You are responsible for the eligible-institution condition. "
        "It applies because this calculation treats the interest on {statement} as deductible. This view does not check it.",
        "You are responsible for the recognised-credential condition. It applies because this calculation treats the interest "
        "on {statement} as deductible. This view does not check it.",
        "You are responsible for the half-time course-load condition. It applies because this calculation treats the interest "
        "on {statement} as deductible. This view does not check it.",
    )
    responsibilities = [
        _reader_rule(
            rule_id, symbol, value=_token(RESPONSIBILITY_TYPE, "applies"), role="responsibility",
            requires=[CONCLUSION, AMOUNT],
            when={"op": "all", "args": [
                {"op": "categorical_compare", "cmp": "eq", "left": _ref(CONCLUSION), "right": _token(CONCLUSION_TYPE, "no-enumerated-adverse")},
                {"op": "compare", "cmp": "gt", "left": _ref(AMOUNT), "right": 0},
            ]},
            wording=wording,
        )
        for (symbol, rule_id), wording in zip(RESPONSIBILITIES, resp_wordings, strict=True)
    ]
    members: list[tuple[dict[str, Any], str]] = [
        (bundle, "fact-type-bundle"), (parameter(NO_LINK_PARAMETER)[0], "parameter"),
        (parameter(NO_CLAIM_PARAMETER)[0], "parameter"),
        (link_count, "computation"), (classifier, "computation"), (scope_count, "computation"),
        (reduction, "computation"), (amount, "computation"), (conclusion, "computation"),
        *((item, "computation") for item in responsibilities),
    ]
    entrypoints = [{"id": citizen["id"], "version": citizen["version"]} for citizen, _role in members]
    return members, entrypoints


def _seal_disposable_reader_package(surface: DisposableSurface) -> Any:
    additions, extra_entrypoints = _package_members()
    member_root = surface.members
    package_path = member_root / PACKAGE_FILE
    package = json.loads(package_path.read_text("utf-8"))
    package["schema"] = "artifact-package.v34"
    existing_ids = {(member["id"], member["version"]) for member in package["members"]}
    for citizen, role in additions:
        key = (citizen["id"], citizen["version"])
        if key in existing_ids:
            raise ValueError(f"temporary reader member collides with the cloned package: {key}")
        existing_ids.add(key)
        package["members"].append({"id": citizen["id"], "role": role, "schema": citizen["schema"], "version": citizen["version"]})
        (member_root / f"{citizen['id']}.json").write_bytes(_bytes(citizen))
    package["entrypoints"].extend(extra_entrypoints)
    package["admitted_schemas"] = sorted(set(package["admitted_schemas"]) | {citizen["schema"] for citizen, _ in additions})
    package.pop("package_checksum", None)
    package["package_checksum"] = package_instance_checksum(package)

    registry_path = member_root / REGISTRY_FILE
    registry = json.loads(registry_path.read_text("utf-8"))
    for citizen, _role in additions:
        registry["citizens"].append({
            "id": citizen["id"], "version": citizen["version"], "checksum": _citizen_checksum(citizen),
        })
    package_entry = next(entry for entry in registry["packages"] if entry["id"] == package["id"] and entry["version"] == package["version"])
    package_entry["checksum"] = package["package_checksum"]
    registry_bytes = _bytes(registry)
    registry_path.write_bytes(registry_bytes)
    package_path.write_bytes(_bytes(package))

    release_path = surface.releases / RELEASE_FILE
    release = json.loads(release_path.read_text("utf-8"))
    release["package_registry_sha256"] = hashlib.sha256(registry_bytes).hexdigest()
    release_bytes = _bytes(release)
    release_path.write_bytes(release_bytes)
    adoption = surface.adoption["payload"]
    adoption["package"]["checksum"] = package["package_checksum"]
    adoption["release"]["checksum"] = hashlib.sha256(release_bytes).hexdigest()

    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in member_root.glob("*.json"):
        citizen = json.loads(path.read_text("utf-8"))
        if isinstance(citizen, dict) and isinstance(citizen.get("id"), str) and isinstance(citizen.get("version"), str):
            corpus[(citizen["id"], citizen["version"])] = citizen
    result = validate_package(package, corpus, DerivationSchemas())
    if not result.ok:
        raise RuntimeError("DISPOSABLE_PACKAGE_ADMISSION_FAILED: " + "; ".join(issue.code + ": " + issue.detail for issue in result.issues))
    return result.resolved_members


def _case_acts(surface: DisposableSurface, name: str) -> list[dict[str, Any]]:
    statement_specs = [
        Statement(lender="demo.lender.reader.s1", stmt="demo.statement.reader.s1", box1=400.0),
        Statement(lender="demo.lender.reader.s2", stmt="demo.statement.reader.s2", box1=700.0),
    ]
    acts = _f1098e_acts(statements=statement_specs, close=True, wages=50000)
    # The base helper closes with a v33 adoption; this demonstration adopts
    # the locally resealed v34 successor exactly once at the end instead.
    if acts and acts[-1].get("kind") == "package-adoption":
        acts.pop()
    labels = {statement_specs[0].stmt: "S1", statement_specs[1].stmt: "S2"}
    for act in acts:
        payload = act.get("payload")
        if not isinstance(payload, dict):
            continue
        entity = payload.get("entity")
        if isinstance(entity, dict) and entity.get("id") in labels:
            entity["label"] = labels[str(entity["id"])]

    # Install the claim/link vocabulary in the kernel before asserting a claim.
    bundle = next(citizen for citizen, _role in _package_members()[0] if citizen["id"] == CLAIM_BUNDLE)
    acts.append({
        "schema": "act.v1", "act_id": "demo.track6b.bundle.reader", "actor": USER,
        "at": "2026-09-27T12:00:00Z", "committed_against": len(acts),
        "kind": "bundle-adoption", "payload": {"bundle": bundle},
    })
    circumstance = CLAIM_SCENARIOS[name]
    if circumstance is not None:
        value = "vehicle" if name == "adverse" else "demo-untreated"
        claim_entity_id = f"demo.sli.circumstance.{name}"
        acts.append({
            "schema": "act.v1", "act_id": f"demo.track6b.entity.{name}", "actor": USER,
            "at": "2026-09-27T12:01:00Z", "committed_against": len(acts),
            "kind": "entity-introduced",
            "payload": {"entity": {"schema": "entity.v1", "id": claim_entity_id, "kind": CLAIM_ENTITY_KIND,
                                     "label": f"S1 statement-wide {circumstance} claim"}},
        })
        claim_fact_id = (
            f"{CLAIMS}|lender={statement_specs[0].lender},statement={statement_specs[0].stmt},"
            f"tax-year=2025,circumstance={claim_entity_id}"
        )
        acts.append({
            "schema": "act.v1", "act_id": f"demo.track6b.claim.{name}", "actor": USER,
            "at": "2026-09-27T12:02:00Z", "committed_against": len(acts),
            "kind": "assertion",
            "payload": {"finding": _attested(f"demo.finding.track6b.claim.{name}", claim_fact_id, value)},
        })
    package_adoption = json.loads(json.dumps(surface.adoption))
    package_adoption["act_id"] = "demo.track6b.adopt.core.v34"
    package_adoption["committed_against"] = len(acts)
    acts.append(package_adoption)
    return _renumber(acts)


def _surface(subject: DisposableSurface) -> PublicationSurface:
    return PublicationSurface(subject.releases, subject.members / REGISTRY_FILE, subject.members)


def _prepare_case(
    name: str,
    root: Path = ROOT,
) -> tuple[DisposableSurface, list[dict[str, Any]], Any]:
    """Return the sealed v34 surface, synthetic acts, and resolved v12/v34 members.

    This is a focused test seam for comparing the two runners against the same
    validated package graph. The saved-file generator uses the same prepared
    objects for its one live-coordinate run.
    """
    if name not in CLAIM_SCENARIOS:
        raise ValueError(f"unknown Track 6b case {name!r}")
    target_dir = root / "temp" / "track6b" / name
    target_dir.mkdir(parents=True, exist_ok=True)
    surface_dir = Path(tempfile.mkdtemp(prefix=".surface-", dir=target_dir))
    surface = DisposableSurface(surface_dir)
    resolved_members = _seal_disposable_reader_package(surface)
    acts = _case_acts(surface, name)
    return surface, acts, resolved_members


def _run_case(
    name: str,
    root: Path = ROOT,
) -> tuple[Any, list[tuple[dict[str, Any], dict[str, Any]]], Path]:
    """Run one case and return live evidence for focused fidelity assertions.

    Callers that need only the saved-file proof should discard the first two
    tuple items before reopening ``saved_path``. The workspace and disposable
    resolved surface remain under ignored `temp/track6b/<case>/` for audit.
    """
    target_dir = root / "temp" / "track6b" / name
    target_dir.mkdir(parents=True, exist_ok=True)
    # Live residency must be outside the repository tree; only its generated
    # presentation artifact crosses back into ignored `temp/` below.
    workspace_dir = Path(tempfile.mkdtemp(prefix="track6b-workspace-"))
    surface, acts, resolved_members = _prepare_case(name, root)
    output = live_coordinate_run(
        WorkspaceCapability(workspace_dir / "L"), repo_root=root,
        authoritative_acts=acts, workspace_revision=len(acts), run_scope=SCOPE,
        scope_user=USER, request={"schema": "run-request.v1"},
        run_id=f"demo.track6b.{name}", governance_pins=[], surface=_surface(surface), output_name="out.json",
    )
    if output.refusal is not None:
        raise RuntimeError(f"LIVE_RUN_REFUSED ({name}): {output.refusal}")
    if output.presentation_path is None or not output.presentation_path.is_file():
        raise RuntimeError(f"LIVE_PRESENTATION_MISSING ({name})")
    if output.output_path is None or not output.output_path.is_file():
        raise RuntimeError(f"LIVE_DISPOSITION_REPORT_MISSING ({name})")
    saved_path = target_dir / "presentation.json"
    shutil.copyfile(output.presentation_path, saved_path)
    return output, resolved_members, saved_path


def generate_saved_presentations(root: Path = ROOT) -> dict[str, Path]:
    output_paths: dict[str, Path] = {}
    for name in CLAIM_SCENARIOS:
        outcome, resolved_members, fixture_path = _run_case(name, root)
        # The browser source is now the saved file alone. Drop the output that
        # carries live publications before reopening the durable model.
        del outcome
        del resolved_members
        saved_model = json.loads(fixture_path.read_text(encoding="utf-8"))
        validate_presentation_model(saved_model)
        view = saved_model.get("calculationView")
        if not isinstance(view, dict) or view.get("integrated") is not False:
            raise RuntimeError(f"SAVED_CALCULATION_VIEW_INVALID ({name})")
        if not any(section.get("id") == "line-sch1-21" for section in saved_model.get("sections", [])):
            raise RuntimeError(f"SAVED_WORKSHEET_MISSING ({name})")
        output_paths[name] = fixture_path
        print(f"{name}: {fixture_path.relative_to(root)} ({len(view.get('groups', []))} statement groups)")
    return output_paths


def main() -> None:
    generate_saved_presentations()


if __name__ == "__main__":
    main()
