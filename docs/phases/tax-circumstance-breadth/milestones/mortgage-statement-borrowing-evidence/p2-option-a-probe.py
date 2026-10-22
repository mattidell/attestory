"""Synthetic P2 Option A diagnostic generator; not a test/product entrypoint."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shutil
import sys
import copy
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from packages.derivation.loader import DerivationSchemas
from packages.derivation.live import _resolved_run_material, live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.presentation_projection import PresentationModelError
from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.derivation.production_resolver import (
    PublicationSurface,
    Refusal,
    resolve_production_package,
)
from packages.kernel.facts import fact_id_for
from packages.kernel.act_log import ActLog
from packages.derivation.records import RecordStream

_P0_SPEC = importlib.util.spec_from_file_location(
    "p0_current_path_probe", Path(__file__).resolve().with_name("p0-current-path-probe.py"))
if _P0_SPEC is None or _P0_SPEC.loader is None:
    raise RuntimeError("could not load the committed P0 synthetic fixture helper")
_P0 = importlib.util.module_from_spec(_P0_SPEC)
_P0_SPEC.loader.exec_module(_P0)
_latest_acts = _P0._latest_acts
RUN_SCOPE = _P0.SCOPE
SCOPE_USER = _P0.RUN_USER
TAX_REGISTRY = _P0.tax_registry

CONTENT = ROOT / "packages/content/tax/2025"
RELEASE_DIR = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
PACKAGE_ID = "tax.us.2025.package.core-calculations"
PACKAGE_VERSION = "v49"
RELEASE_ID = "demo.release.sli-worksheet-integration.2025"
RELEASE_VERSION = "v47"
BRIDGE_PACKAGE_VERSION = "v51"
BRIDGE_RELEASE_ID = "demo.release.mortgage-statement-borrowing.2025"
BRIDGE_RELEASE_VERSION = "v1"
BRIDGE_BUNDLE_ID = "demo.tax.2025.f1098-report-local-bridge"
BRIDGE_BUNDLE_VERSION = "v1"
BRIDGE_RULE_PREFIX = "demo.rule.tax.2025.f1098-report-local-bridge"
ACCOUNT_BUNDLE_ID = "demo.tax.2025.mortgage-borrowing-facts"
PRINCIPAL_STATUS = "demo.tax.2025.f1098.principal-within-ceiling"
READINESS_SYMBOL = "demo.tax.2025.mortgage.same-borrowing-ready"
ACCOUNT_FACTS = {
    "recognition": "demo.tax.2025.mortgage.continuing-borrowing",
    "membership": "demo.tax.2025.mortgage.report-membership",
    "ceiling": "demo.tax.2025.mortgage.annual-ceiling",
    "other-debt": "demo.tax.2025.mortgage.other-home-secured-debt",
    "report-link-status": "demo.tax.2025.mortgage.report-link-status",
}
LINE8A_RULE_ID = "tax.us.2025.rule.f1098-line8a"
BRIDGE_TYPES: dict[str, str] = {
    "filing-unit-owns-home": "answer-status.filing-unit-owns-home",
    "shared-main-home": "answer-status.shared-main-home",
    "home-is-collateral": "answer-status.home-is-collateral",
    "owes-the-loan": "answer-status.owes-the-loan",
    "paid-the-interest": "answer-status.paid-the-interest",
    "no-one-else-owes-it": "answer-status.no-one-else-owes-it",
    "what-the-money-paid-for": "answer-status.what-the-money-paid-for",
    "this-is-the-original-loan": "answer-status.this-is-the-original-loan",
    "mortgage-credit-certificate-received": "answer-status.mortgage-credit-certificate-received",
    "box2-outstanding-principal": "reported-box2-principal",
    "box3-origination-date": "reported-box3-origination-date",
    "box9-number-of-properties": "reported-box9-property-count",
}
SOURCE_TYPES = {
    **{key: f"tax.us.2025.f1098.{key}" for key in BRIDGE_TYPES},
}


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text("utf-8"))


def _write_json(path: Path, value: Any) -> bytes:
    raw = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")
    path.write_bytes(raw)
    return raw


def _literal(fact_type: dict[str, Any], value: Any) -> dict[str, Any]:
    return {"op": "category_literal", "fact_type": {"id": fact_type["id"], "version": fact_type["version"]},
            "value": value}


def _answer_value_map(source_fact: dict[str, Any], result_fact: dict[str, Any]) -> dict[str, Any]:
    """Explicit identity mapping from every source enum value to its result domain."""
    values = list(source_fact["value_schema"]["enum"])
    expression: dict[str, Any] = _literal(result_fact, values[-1])
    for source_value in reversed(values[:-1]):
        expression = {
            "op": "choose",
            "when": {"op": "categorical_compare", "cmp": "eq",
                     "left": {"op": "ref", "name": source_fact["id"]},
                     "right": _literal(source_fact, source_value)},
            "then": _literal(result_fact, source_value),
            "else": expression,
        }
    return expression


def _bridge_content(members_dir: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Generate one bundle and 12 meaningful subject-scoped bridge rules."""
    current = _read_json(members_dir / "f1098-circumstances.bundle.v2.json")
    raw_bundle = _read_json(members_dir / "f1098.bundle.json")
    raw_by_id = {fact["id"]: fact for bundle in (current, raw_bundle) for fact in bundle["fact_types"]}
    bridge_facts: list[dict[str, Any]] = []
    rules: list[dict[str, Any]] = []
    citations = _read_json(members_dir / "rule.f1098-residence-interest-reason.v2.json")["citations"]
    subject = {"id": "tax.us.2025.f1098.box1-mortgage-interest", "version": "v1"}

    for source_key, output_suffix in BRIDGE_TYPES.items():
        source = raw_by_id[SOURCE_TYPES[source_key]]
        output = json.loads(json.dumps(source))
        output["id"] = f"demo.tax.2025.f1098.{output_suffix}"
        output["version"] = "v1"
        output["title"] = f"P2 report-local derived read: {source_key}"
        bridge_facts.append(output)
        rule_id = f"{BRIDGE_RULE_PREFIX}.{re.sub(r'[^a-z0-9-]+', '-', source_key)}"
        rule: dict[str, Any] = {
            "schema": "rule-artifact.v13", "id": rule_id, "version": "v1",
            "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
            "role": "computation", "subject": subject,
            "joined": {"id": source["id"], "version": source["version"]},
            "direction": "joined_contains_subject", "requires": [source["id"]], "pins": [],
            "when": True,
            "value": (_answer_value_map(source, output) if "enum" in source["value_schema"]
                      else {"op": "ref", "name": source["id"]}),
            "publishes": output["id"], "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
            "citations": citations,
            "wording": f"Report-local bridge reads this report's {source_key} observation or answer.",
            "notes": "Synthetic feasibility content. The subject is this report's Box 1; joined input keys are exact-report keys.",
        }
        rules.append(rule)
    membership = _account_fact(ACCOUNT_FACTS["membership"], [
        {"name": "payer", "kind": "entity", "entity_kind": "tax.us.mortgage-lender"},
        {"name": "statement", "kind": "entity", "entity_kind": "tax.us.1098-statement"},
        {"name": "tax-year", "kind": "literal", "values": ["2025"]},
        {"name": "borrowing", "kind": "literal", "values": ["demo.f1098.borrowing.same"]}],
        {"type": "string", "enum": ["yes", "no", "cannot-tell"]}, "Report membership assertion")
    membership_output = _account_fact(ACCOUNT_FACTS["report-link-status"], membership["identity_keys"],
        membership["value_schema"], "Derived report-link status")
    box2_source = raw_by_id[SOURCE_TYPES["box2-outstanding-principal"]]
    principal_status = json.loads(json.dumps(box2_source))
    principal_status.update({"id": PRINCIPAL_STATUS, "version": "v1",
        "title": "Derived per-report principal ceiling check",
        "value_schema": {"type": "string", "enum": ["within-ceiling", "over-ceiling", "cannot-tell"]}})
    bundle_facts = [*bridge_facts, membership, membership_output, principal_status,
        _account_fact(ACCOUNT_FACTS["recognition"], [
            {"name": "borrowing", "kind": "literal", "values": ["demo.f1098.borrowing.same"]},
            {"name": "tax-year", "kind": "literal", "values": ["2025"]}],
            {"type": "string", "enum": ["yes", "no", "cannot-tell"]}, "Continuing-borrowing recognition"),
        _account_fact(ACCOUNT_FACTS["ceiling"], [
            {"name": "borrowing", "kind": "literal", "values": ["demo.f1098.borrowing.same"]},
            {"name": "tax-year", "kind": "literal", "values": ["2025"]}],
            {"type": "number"}, "Person-confirmed annual principal ceiling"),
        _account_fact(ACCOUNT_FACTS["other-debt"], [
            {"name": "borrowing", "kind": "literal", "values": ["demo.f1098.borrowing.same"]},
            {"name": "tax-year", "kind": "literal", "values": ["2025"]}],
            {"type": "string", "enum": ["no", "yes", "cannot-tell"]}, "Other secured debt on either home"),
        _account_fact("demo.tax.2025.mortgage.inert-path-unwritten", [
            {"name": "case", "kind": "literal", "values": ["inert"]}], {"type": "string"},
            "Synthetic inert-path discriminator")]
    bundle = {"schema": "bundle.v2", "id": BRIDGE_BUNDLE_ID, "version": BRIDGE_BUNDLE_VERSION,
              "label": "Synthetic P2 report-local and borrowing facts", "fact_types": bundle_facts}
    rules.append({"schema": "rule-artifact.v13", "id": f"{BRIDGE_RULE_PREFIX}.report-link-status",
        "version": "v1", "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation", "subject": subject,
        "joined": {"id": ACCOUNT_FACTS["membership"], "version": "v1"},
        "direction": "joined_contains_subject", "requires": [ACCOUNT_FACTS["membership"]], "pins": [],
        "when": True, "value": {"op": "ref", "name": ACCOUNT_FACTS["membership"]},
        "publishes": ACCOUNT_FACTS["report-link-status"],
        "blocked": {"code": "DEPENDENCY_INVALID", "missing": []}, "citations": citations,
        "notes": "Report-local status reads only the membership assertion whose identity contains this exact report."})
    rules.append({"schema": "rule-artifact.v13", "id": f"{BRIDGE_RULE_PREFIX}.principal-ceiling-status",
        "version": "v1", "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation", "subject": subject,
        "joined": {"id": SOURCE_TYPES["box2-outstanding-principal"], "version": "v1"},
        "direction": "joined_contains_subject", "requires": [SOURCE_TYPES["box2-outstanding-principal"], ACCOUNT_FACTS["ceiling"]],
        "pins": [], "when": True,
        "value": {"op": "choose", "when": {"op": "compare", "cmp": "lte",
            "left": {"op": "ref", "name": SOURCE_TYPES["box2-outstanding-principal"]},
            "right": {"op": "ref", "name": ACCOUNT_FACTS["ceiling"]}},
            "then": _literal({"id": PRINCIPAL_STATUS, "version": "v1"}, "within-ceiling"),
            "else": _literal({"id": PRINCIPAL_STATUS, "version": "v1"}, "over-ceiling")},
        "publishes": PRINCIPAL_STATUS, "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
        "citations": citations, "notes": "Report-local Box 2 check against the common raw borrowing ceiling."})
    rules.extend(_line8a_candidate(members_dir))
    return bundle, rules


def _account_fact(fact_id: str, keys: list[dict[str, Any]], value_schema: dict[str, Any], title: str) -> dict[str, Any]:
    return {"schema": "fact-type.v2", "id": fact_id, "version": "v1", "title": title,
            "nature": "determinable", "identity_keys": keys, "value_schema": value_schema,
            "supersession": {"policy": "free"}}


def _line8a_candidate(members_dir: Path) -> list[dict[str, Any]]:
    subject = {"id": ACCOUNT_FACTS["recognition"], "version": "v1"}
    box1 = "tax.us.2025.f1098.box1-mortgage-interest"
    box3 = "tax.us.2025.f1098.box3-origination-date"
    reason = "tax.us.2025.f1098.residence-interest-reason"
    date_bridge = "demo.tax.2025.f1098.reported-box3-origination-date"
    yes = _literal({"id": ACCOUNT_FACTS["recognition"], "version": "v1"}, "yes")
    link_status_yes = _literal({"id": ACCOUNT_FACTS["report-link-status"], "version": "v1"}, "yes")
    reason_qualified = _literal({"id": reason, "version": "v2"}, "qualified")
    all_ok = {"op": "all", "args": [
        {"op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": ACCOUNT_FACTS["recognition"]}, "right": yes},
        {"op": "collect_categorical_all_equal", "name": ACCOUNT_FACTS["report-link-status"], "value": link_status_yes},
        {"op": "collect_categorical_all_equal", "name": reason, "value": reason_qualified},
        {"op": "collect_categorical_all_equal", "name": PRINCIPAL_STATUS,
         "value": _literal({"id": PRINCIPAL_STATUS, "version": "v1"}, "within-ceiling")},
        {"op": "collect_categorical_all_equal", "name": date_bridge, "value": {"op": "ref", "name": box3}},
        {"op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": ACCOUNT_FACTS["other-debt"]},
         "right": _literal({"id": ACCOUNT_FACTS["other-debt"], "version": "v1"}, "no")},
        {"op": "compare", "cmp": "lte", "left": {"op": "ref", "name": ACCOUNT_FACTS["ceiling"]},
         "right": {"op": "parameter", "parameter_id": "tax.us.2025.f1098.mortgage-interest-limit", "key": {"op": "ref", "name": "filing_status"}}},
    ]}
    path_requires = [ACCOUNT_FACTS["ceiling"], ACCOUNT_FACTS["recognition"], ACCOUNT_FACTS["other-debt"],
        "filing_status", box3]
    path_pins = [{"role": "input", "id": name, "version": "v1", "origin": "assertion"} for name in path_requires]
    readiness = {"schema": "rule-artifact.v14", "id": "demo.tax.2025.rule.mortgage-borrowing-readiness", "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation", "requires": [], "pins": [],
        "when": True,
        "selection": {"mode": "exclusive_presence", "conflict": "refuse", "paths": [{"id": "same-borrowing",
            "activity": {"kind": "source_nonempty", "source_family": {"id": "tax.us.2025.f1098", "version": "v1"},
                "member_fact_types": [{"id": box1, "version": "v1"}]},
            "reads_subject_results": [
                {"symbol": reason, "subject": {"id": box1, "version": "v1"}},
                {"symbol": date_bridge, "subject": {"id": box1, "version": "v1"}},
                {"symbol": ACCOUNT_FACTS["report-link-status"], "subject": {"id": box1, "version": "v1"}},
                {"symbol": PRINCIPAL_STATUS, "subject": {"id": box1, "version": "v1"}}],
            "requires": path_requires, "pins": path_pins,
            "when": True,
            "value": {"op": "all", "args": [
                {"op": "require_closed", "source_set": "tax.us.2025.f1098"}, all_ok]}},
            {"id": "inert", "activity": {"kind": "source_nonempty", "member_fact_type":
                {"id": "demo.tax.2025.mortgage.inert-path-unwritten", "version": "v1"}},
             "reads_subject_results": [], "requires": [], "pins": [], "when": True,
             "value": {"op": "block", "code": "DEPENDENCY_ABSENT"}}],
            "default": {"id": "neither", "reads_subject_results": [], "requires": [], "pins": [], "when": False,
                "value": {"op": "block", "code": "DEPENDENCY_ABSENT"}},
            "refusal": {"code": "DEPENDENCY_INVALID", "missing": ["f1098-same-borrowing-conflict"], "pins": []}},
        "publishes": READINESS_SYMBOL, "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
        "citations": _read_json(members_dir / "rule.f1098-line8a.v2.json").get("citations", []),
        "notes": "Synthetic report-local readiness gate; ordinary answers are not loan-wide."}
    collector = {"schema": "rule-artifact.v6", "id": LINE8A_RULE_ID, "version": "v3",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation", "requires": [READINESS_SYMBOL], "pins": [], "when": True,
        "value": {"op": "choose", "when": {"op": "ref", "name": READINESS_SYMBOL},
            "then": {"op": "add", "args": [{"op": "collect", "name": box1, "source_set": "tax.us.2025.f1098"}]},
            "else": {"op": "block", "code": "DEPENDENCY_INVALID"}},
        "publishes": "tax.us.2025.schedule-a.line8a", "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
        "citations": _read_json(members_dir / "rule.f1098-line8a.v2.json").get("citations", []),
        "composition": {"id": "tax.us.2025.schedule-a", "version": "v1"},
        "notes": "Synthetic successor uses the adopted F1098 Box 1 collector and publishes authorized Schedule A line8a once after readiness."}
    return [readiness, collector]


def _successor_report_reason(members_dir: Path) -> dict[str, Any]:
    """Retain ordered reason logic while consuming keyed bridge findings."""
    reason = _read_json(members_dir / "rule.f1098-residence-interest-reason.v2.json")
    reason["version"] = "v3"
    replacements = {SOURCE_TYPES[key]: f"demo.tax.2025.f1098.{suffix}"
                    for key, suffix in BRIDGE_TYPES.items()}
    reason["requires"] = list(dict.fromkeys(replacements.get(name, name) for name in reason["requires"]))

    def rewrite(node: Any) -> Any:
        if isinstance(node, dict):
            result = {key: rewrite(value) for key, value in node.items()}
            if result.get("op") == "ref" and result.get("name") in replacements:
                result["name"] = replacements[result["name"]]
            if result.get("op") == "category_literal":
                source = result.get("fact_type")
                if isinstance(source, dict) and source.get("id") in replacements:
                    result["fact_type"] = {"id": replacements[source["id"]], "version": "v1"}
            return result
        if isinstance(node, list):
            return [rewrite(item) for item in node]
        return node

    reason["value"] = rewrite(reason["value"])
    reason["notes"] = ("Successor of the adopted per-report reason rule. Retains its ordered reason "
                       "logic while consuming same-report keyed P2 bridge findings.")
    return reason


def _materialize_candidate_surface(destination: Path, out_dir: Path) -> tuple[PublicationSurface, dict[str, Any], list[dict[str, Any]]]:
    members = destination / "members"
    releases = destination / "releases"
    members.mkdir(parents=True)
    releases.mkdir(parents=True)
    shutil.copytree(CONTENT, members, dirs_exist_ok=True)
    shutil.copy2(RELEASE_DIR / f"{RELEASE_ID}.{RELEASE_VERSION}.json", releases / f"{RELEASE_ID}.{RELEASE_VERSION}.json")

    package = _read_json(members / f"package.core-calculations.{PACKAGE_VERSION}.json")
    bundle, rules = _bridge_content(members)
    successor_reason = _successor_report_reason(members)
    bridge_bundle_path = members / f"{BRIDGE_BUNDLE_ID}.{BRIDGE_BUNDLE_VERSION}.json"
    _write_json(bridge_bundle_path, bundle)
    package["version"] = BRIDGE_PACKAGE_VERSION
    for fact_type in [ACCOUNT_FACTS["recognition"], ACCOUNT_FACTS["membership"],
                      ACCOUNT_FACTS["ceiling"], ACCOUNT_FACTS["other-debt"]]:
        package["input_bindings"].append({"fact_type": {"id": fact_type, "version": "v1"},
                                          "mode": "required", "symbol": fact_type})
    package["members"].append({"id": BRIDGE_BUNDLE_ID, "version": BRIDGE_BUNDLE_VERSION,
                               "schema": "bundle.v2", "role": "fact-type-bundle"})
    package["entrypoints"] = [
        {**entry, "version": "v3"}
        if entry.get("id") == "tax.us.2025.rule.f1098-residence-interest-reason"
        else {**entry, "version": "v3"}
        if entry.get("id") == LINE8A_RULE_ID
        else entry
        for entry in package["entrypoints"]
    ]
    package["entrypoints"].append({"id": BRIDGE_BUNDLE_ID, "version": BRIDGE_BUNDLE_VERSION})
    for rule in rules:
        _write_json(members / f"{rule['id']}.json", rule)
        package["members"].append({"id": rule["id"], "version": rule["version"],
                                   "schema": rule["schema"], "role": "computation"})
    package["members"] = [member for member in package["members"]
                          if not ((member["id"] == "tax.us.2025.rule.f1098-residence-interest-reason"
                                   and member["version"] == "v2")
                                  or (member["id"] == LINE8A_RULE_ID and member["version"] == "v2"))]
    _write_json(members / "rule.f1098-residence-interest-reason.v3.json", successor_reason)
    package["members"].append({"id": successor_reason["id"], "version": "v3",
                               "schema": "rule-artifact.v14", "role": "computation"})
    line8a = next(rule for rule in rules if rule["id"] == LINE8A_RULE_ID)
    _write_json(members / f"{LINE8A_RULE_ID}.v3.json", line8a)

    registry_path = members / "published-packages.p48-p2.json"
    registry = _read_json(members / "published-packages.v47.json")
    for citizen in [bundle, *rules, successor_reason]:
        registry["citizens"].append({"id": citizen["id"], "version": citizen["version"],
                                     "checksum": citizen_checksum(citizen)})
    package["package_checksum"] = package_instance_checksum(package)
    registry["packages"].append({"id": package["id"], "version": BRIDGE_PACKAGE_VERSION,
                                 "checksum": package["package_checksum"]})
    _write_json(registry_path, registry)
    _write_json(members / f"package.core-calculations.{BRIDGE_PACKAGE_VERSION}.json", package)

    release = {"schema": "release-registry.v1", "id": BRIDGE_RELEASE_ID,
               "version": BRIDGE_RELEASE_VERSION,
               "package_registry_sha256": hashlib.sha256(registry_path.read_bytes()).hexdigest()}
    release_path = releases / f"{BRIDGE_RELEASE_ID}.{BRIDGE_RELEASE_VERSION}.json"
    _write_json(release_path, release)
    surface = PublicationSurface(releases, registry_path, members)

    acts = _latest_acts(second_report=True, box2=240000.0, second_box2=220000.0, fixture_answers=True)
    for act in acts:
        finding = _act_finding(act)
        fact_id = finding.get("fact_id", "")
        if fact_id.startswith("tax.us.2025.f1098.box1-mortgage-interest|"):
            finding["value"] = 8000.0 if "stmt.a" in fact_id else 3000.0
        elif fact_id.startswith("tax.us.2025.f1098.box3-origination-date|"):
            finding["value"] = "2019-03-04"
    acts = _add_account_assertions(acts, bundle)
    adoption = next(act for act in acts if act.get("kind") == "package-adoption")
    adoption["payload"]["package"] = {"id": package["id"], "version": BRIDGE_PACKAGE_VERSION,
                                       "checksum": package["package_checksum"]}
    adoption["payload"]["release"] = {"id": BRIDGE_RELEASE_ID, "version": BRIDGE_RELEASE_VERSION,
                                      "checksum": hashlib.sha256(release_path.read_bytes()).hexdigest()}
    adoption["payload"]["audit"] = {"note": "synthetic P2 report-local bridge candidate"}
    pins = {"package": {"id": package["id"], "version": BRIDGE_PACKAGE_VERSION,
                         "checksum": package["package_checksum"]},
            "registry_sha256": hashlib.sha256(registry_path.read_bytes()).hexdigest(),
            "release": {"id": BRIDGE_RELEASE_ID, "version": BRIDGE_RELEASE_VERSION,
                        "sha256": hashlib.sha256(release_path.read_bytes()).hexdigest()},
            "generated_bundle": {"id": bundle["id"], "version": bundle["version"]},
            "generated_rule_count": len(rules),
            "successor_reason_rule": {"id": successor_reason["id"], "version": successor_reason["version"]}}
    retained = out_dir / "candidate-content"
    retained.mkdir(parents=True, exist_ok=True)
    shutil.copy2(bridge_bundle_path, retained / bridge_bundle_path.name)
    for rule in rules:
        shutil.copy2(members / f"{rule['id']}.json", retained / f"{rule['id']}.json")
    shutil.copy2(members / "rule.f1098-residence-interest-reason.v3.json",
                 retained / "rule.f1098-residence-interest-reason.v3.json")
    shutil.copy2(members / f"{LINE8A_RULE_ID}.v3.json", retained / f"{LINE8A_RULE_ID}.v3.json")
    shutil.copy2(members / f"package.core-calculations.{BRIDGE_PACKAGE_VERSION}.json",
                 retained / f"package.core-calculations.{BRIDGE_PACKAGE_VERSION}.json")
    shutil.copy2(registry_path, retained / registry_path.name)
    shutil.copy2(release_path, retained / release_path.name)
    return surface, pins, acts


def _add_account_assertions(acts: list[dict[str, Any]], bundle: dict[str, Any]) -> list[dict[str, Any]]:
    adoption = next(i for i, row in enumerate(acts) if row.get("kind") == "package-adoption")
    additions: list[dict[str, Any]] = [{"schema": "act.v1", "act_id": "demo.mortgage.p2.account-bundle",
        "kind": "bundle-adoption", "actor": "demo.taxpayer", "at": "2026-10-22T10:00:00Z",
        "committed_against": adoption, "payload": {"bundle": bundle}}]
    def add_fact(type_id: str, keys: tuple[tuple[str, str], ...], value: Any, suffix: str) -> None:
        fact_id = fact_id_for(type_id, keys)
        finding = {"schema": "finding.v2", "id": f"demo.mortgage.p2.{suffix}", "fact_id": fact_id,
                   "value": value, "basis": "attested", "evidence_ids": []}
        additions.append({"schema": "act.v1", "act_id": f"demo.mortgage.p2.act.{suffix}", "kind": "assertion",
            "actor": "demo.taxpayer", "at": "2026-10-22T10:00:01Z", "committed_against": adoption,
            "payload": {"finding": finding}})
    account = (("borrowing", "demo.f1098.borrowing.same"), ("tax-year", "2025"))
    add_fact(ACCOUNT_FACTS["recognition"], account, "yes", "recognizes-same-borrowing")
    add_fact(ACCOUNT_FACTS["ceiling"], account, 250000.0, "annual-ceiling")
    add_fact(ACCOUNT_FACTS["other-debt"], account, "no", "other-home-debt-no")
    for suffix, payer, statement in (("a", "demo.f1098.lender.a", "demo.f1098.stmt.a"),
                                     ("b", "demo.f1098.lender.b", "demo.f1098.stmt.b")):
        keys = (("payer", payer), ("statement", statement), ("tax-year", "2025"),
                ("borrowing", "demo.f1098.borrowing.same"))
        add_fact(ACCOUNT_FACTS["membership"], keys, "yes", f"report-{suffix}-membership")
    acts[adoption:adoption] = additions
    for index, act in enumerate(acts):
        act["committed_against"] = index
        if act.get("kind") == "package-adoption":
            act.setdefault("payload", {})["revision"] = index
    return acts


def _raw_fact_inventory(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Inventory only raw source and answer facts supplied in the fixture."""
    by_type: dict[str, list[str]] = {}
    for act in acts:
        payload = act.get("payload", {})
        finding = payload.get("finding") if isinstance(payload, dict) else None
        if not isinstance(finding, dict) and isinstance(payload, dict):
            member = payload.get("member")
            finding = member.get("finding") if isinstance(member, dict) else None
        fact_id = finding.get("fact_id") if isinstance(finding, dict) else None
        if not isinstance(fact_id, str):
            continue
        fact_type, _, identity = fact_id.partition("|")
        if fact_type.startswith(("tax.us.2025.f1098.", "demo.tax.2025.mortgage.")):
            by_type.setdefault(fact_type, []).append(identity)
    return [{"fact_type": name, "count": len(ids), "identities": sorted(ids)}
            for name, ids in sorted(by_type.items())]


def _act_finding(act: dict[str, Any]) -> dict[str, Any]:
    payload = act.get("payload", {})
    if not isinstance(payload, dict):
        return {}
    finding = payload.get("finding")
    if isinstance(finding, dict):
        return finding
    member = payload.get("member")
    finding = member.get("finding") if isinstance(member, dict) else None
    return finding if isinstance(finding, dict) else {}


def _case_acts(seed: list[dict[str, Any]], case: str) -> list[dict[str, Any]]:
    acts = copy.deepcopy(seed)
    if case == "b-contrary-payment":
        for act in acts:
            finding = _act_finding(act)
            fid = finding.get("fact_id", "")
            if fid.startswith("tax.us.2025.f1098.paid-the-interest|") and "stmt.b" in fid:
                finding["value"] = "paid-by-others-or-partial"
    elif case == "b-membership-missing":
        acts = [act for act in acts if not (
            act.get("kind") == "assertion"
            and _act_finding(act).get("fact_id", "").startswith(
                ACCOUNT_FACTS["membership"] + "|")
            and "stmt.b" in _act_finding(act).get("fact_id", ""))]
    elif case == "principal-contradicts-ceiling":
        for act in acts:
            finding = _act_finding(act)
            fid = finding.get("fact_id", "")
            if fid.startswith("tax.us.2025.f1098.box2-outstanding-principal|") and "stmt.b" in fid:
                finding["value"] = 270000.0
    elif case == "loose-upper-bound":
        for act in acts:
            finding = _act_finding(act)
            if finding.get("fact_id", "").startswith(ACCOUNT_FACTS["ceiling"] + "|"):
                finding["value"] = 900000.0
    elif case == "origination-disagreement":
        for act in acts:
            finding = _act_finding(act)
            fid = finding.get("fact_id", "")
            if fid.startswith("tax.us.2025.f1098.box3-origination-date|") and "stmt.b" in fid:
                finding["value"] = "2020-03-04"
    elif case != "positive-baseline":
        raise ValueError(f"unknown case: {case}")
    for index, act in enumerate(acts):
        act["committed_against"] = index
        if act.get("kind") == "package-adoption":
            act.setdefault("payload", {})["revision"] = index
    # Assert the bounded experiment actually contains the intended raw fixture.
    box1 = sorted((_act_finding(a).get("fact_id", "").split("|")[1], _act_finding(a).get("value"))
                  for a in acts if _act_finding(a).get("fact_id", "").startswith("tax.us.2025.f1098.box1-mortgage-interest|"))
    box2 = sorted((_act_finding(a).get("fact_id", "").split("|")[1], _act_finding(a).get("value"))
                  for a in acts if _act_finding(a).get("fact_id", "").startswith("tax.us.2025.f1098.box2-outstanding-principal|"))
    box3 = sorted((_act_finding(a).get("fact_id", "").split("|")[1], _act_finding(a).get("value"))
                  for a in acts if _act_finding(a).get("fact_id", "").startswith("tax.us.2025.f1098.box3-origination-date|"))
    expected_box1 = [3000.0, 8000.0]
    expected_box2 = [240000.0, 270000.0] if case == "principal-contradicts-ceiling" else [220000.0, 240000.0]
    expected_box3 = (["2019-03-04", "2020-03-04"] if case == "origination-disagreement"
                     else ["2019-03-04", "2019-03-04"])
    if sorted(value for _, value in box1) != expected_box1 or sorted(value for _, value in box2) != expected_box2 or sorted(value for _, value in box3) != expected_box3:
        raise AssertionError(f"fixture mutation mismatch: box1={box1}, box2={box2}, box3={box3}")
    return acts


def _live_case(case: str, seed: list[dict[str, Any]], surface: PublicationSurface, case_dir: Path) -> dict[str, Any]:
    acts = _case_acts(seed, case)
    (case_dir / "synthetic-seed-acts.json").write_text(json.dumps(acts, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    workspace_tmp = TemporaryDirectory(prefix=f"demo-f1098-p2-{case}-")
    workspace = Path(workspace_tmp.name) / "workspace"
    capability = WorkspaceCapability(workspace)
    registry = TAX_REGISTRY()
    log = ActLog(workspace, registry)
    log.append_batch(acts, expected_revision=0)
    current = log.read()
    try:
        outcome = live_coordinate_run(
            capability, repo_root=ROOT, authoritative_acts=current.acts, workspace_revision=current.revision,
            run_scope=RUN_SCOPE, scope_user=SCOPE_USER, request={"schema": "run-request.v1"},
            run_id=f"demo.mortgage.p2.{case}.v51-v1", governance_pins=[], surface=surface,
            output_name=f"{case}.json", schemas=DerivationSchemas(),
        )
    except PresentationModelError as exc:
        records = RecordStream(capability.location / "records", DerivationSchemas()).read()
        (case_dir / "synthetic-records.json").write_text(
            json.dumps(records.records, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        live_result = None
        traceback = exc.__traceback__
        while traceback is not None:
            frame_result = traceback.tb_frame.f_locals.get("result")
            if frame_result is not None and hasattr(frame_result, "publications"):
                live_result = frame_result
            traceback = traceback.tb_next
        if live_result is None:
            raise RuntimeError("presentation rejection had no captured live RunResult frame") from exc
        line8a_publications = [publication.finding for publication in live_result.publications
                              if publication.finding.get("symbol") == "tax.us.2025.schedule-a.line8a"]
        publication_path = case_dir / "live-run-in-memory-line8a.json"
        publication_path.write_text(json.dumps({"durability": "in-memory from actual live RunResult; no durable report or presentation",
            "findings": line8a_publications}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        closing = next((row for row in records.records if row.get("phase") == "completed"), {})
        line8a = [row for row in closing.get("dispositions", [])
                  if row.get("artifact_id") == LINE8A_RULE_ID]
        summary = {"case": case, "seed_fact_inventory": _raw_fact_inventory(acts),
            "outcome": "presentation-error-after-recorded-run", "presentation_error": str(exc),
            "durable_report": None, "durable_presentation": None,
            "record_count": len(records.records), "line8a_record_dispositions": line8a,
            "in_memory_publications": publication_path.name,
            "in_memory_line8a_findings": line8a_publications}
        workspace_tmp.cleanup()
        return summary
    summary: dict[str, Any] = {"case": case, "seed_fact_inventory": _raw_fact_inventory(acts),
        "outcome": "refused" if outcome.refusal else "completed",
        "refusal": ({"reason": outcome.refusal.reason, "detail": outcome.refusal.detail,
                     "issues": outcome.refusal.issues} if outcome.refusal else None),
        "durable_report": None, "durable_presentation": None, "record_count": 0}
    if outcome.output_path:
        report_path = case_dir / "coordinator-report.json"
        shutil.copy2(outcome.output_path, report_path)
        report = _read_json(report_path)
        summary["durable_report"] = report_path.name
        summary["report_keys"] = sorted(report)
        summary["line8a_dispositions"] = [item for item in report.get("dispositions", [])
            if item.get("artifact_id") == LINE8A_RULE_ID]
        if outcome.presentation_path:
            shutil.copy2(outcome.presentation_path, case_dir / "presentation-model.json")
            summary["durable_presentation"] = "presentation-model.json"
            records = RecordStream(capability.location / "records", DerivationSchemas()).read()
            (case_dir / "synthetic-records.json").write_text(
                json.dumps(records.records, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            summary["record_count"] = len(records.records)
    workspace_tmp.cleanup()
    return summary


def run_bridge_candidate() -> dict[str, Any]:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = ROOT / "temp/mortgage-statement-borrowing" / f"p2-bridge-{stamp}"
    out_dir.mkdir(parents=True, exist_ok=False)
    with TemporaryDirectory(prefix="demo-f1098-p2-publication-") as publication_tmp:
        surface, pins, acts = _materialize_candidate_surface(Path(publication_tmp), out_dir)
        schemas = DerivationSchemas()
        resolution = resolve_production_package(
            acts,
            run_scope=RUN_SCOPE,
            scope_user=SCOPE_USER,
            workspace_revision=len(acts),
            surface=surface,
            schemas=schemas,
        )
        if isinstance(resolution, Refusal):
            raise RuntimeError(f"candidate publication surface refused: {resolution.reason}: {resolution.detail}; "
                               f"issues={json.dumps(resolution.issues, sort_keys=True)}")
        material = _resolved_run_material(resolution)
        resolved_rules = material[0]
        emission_only = material.emission_only_names
        candidate_rules = [rule for rule in resolved_rules if rule["id"].startswith(BRIDGE_RULE_PREFIX)]
        if len(candidate_rules) != len(BRIDGE_TYPES) + 2:
            raise RuntimeError(f"expected {len(BRIDGE_TYPES) + 2} report-local rules, resolved {len(candidate_rules)}")
        fact_types = [fact for member in resolution.resolved_members
                      if member.get("schema") in {"bundle.v1", "bundle.v2"}
                      for fact in member.get("fact_types", [])]
        fact_type_by_pin = {(fact["id"], fact["version"]): fact for fact in fact_types}
        bridge_rule_rows: list[dict[str, Any]] = []
        for rule in sorted(candidate_rules, key=lambda row: row["id"]):
            joined_pin = rule["joined"]
            output_id = rule["publishes"]
            input_type = fact_type_by_pin[(joined_pin["id"], joined_pin["version"])]
            output_type = next(fact for fact in fact_types if fact["id"] == output_id)
            input_values = input_type.get("value_schema", {}).get("enum")
            bridge_rule_rows.append({
                "rule_id": rule["id"], "rule_version": rule["version"],
                "subject": rule["subject"], "joined": joined_pin,
                "direction": rule["direction"], "publishes": output_id,
                "output_fact_type": {"id": output_type["id"], "version": output_type["version"]},
                "identity_key_names": [key["name"] for key in input_type["identity_keys"]],
                "enum_map": ([{"input": value, "output": value} for value in input_values]
                             if isinstance(input_values, list) else None),
                "value_mode": "explicit per-value categorical map" if isinstance(input_values, list)
                              else "typed report-local value read-through",
            })

        raw_inventory = _raw_fact_inventory(acts)
        case_names = ["positive-baseline", "b-contrary-payment", "b-membership-missing",
                      "principal-contradicts-ceiling", "loose-upper-bound", "origination-disagreement"]
        live_summaries: list[dict[str, Any]] = []
        for case in case_names:
            case_dir = out_dir / "cases" / case
            case_dir.mkdir(parents=True, exist_ok=False)
            summary = _live_case(case, acts, surface, case_dir)
            live_summaries.append(summary)
            if summary["outcome"] == "refused":
                break
        derived_inventory = [
            {"result": "per-report support/status for each exact report", "count_in_seed": 0,
             "state": "not supplied; must be derived by candidate content"},
            {"result": "borrowing-level category and ceiling comparison", "count_in_seed": 0,
             "state": "not supplied; must be derived by candidate content"},
            {"result": "authorized Schedule A line8a publication", "count_in_seed": 0,
             "state": "not supplied; must be derived by candidate content"},
        ]
        result = {
            "stage": "report-local-bridges-and-live-coordinator-cases",
            "evidence_ceiling": "synthetic source/answer acts, exact ephemeral publication resolution, and actual live coordinator outputs; no user input, recorder, or group reader claim",
            "route": pins,
            "bridge_rule_map": bridge_rule_rows,
            "resolved": {"package_id": resolution.package["id"],
                         "package_version": resolution.package["version"],
                         "resolved_member_count": len(resolution.resolved_members),
                         "adoption_act_id": resolution.adoption_act_id,
                         "release_id": resolution.release_id,
                         "candidate_rule_count": len(candidate_rules),
                         "resolved_emission_only_sources": sorted(
                             source for source in emission_only
                             if source.startswith("tax.us.2025.f1098.") or source.startswith("demo.tax.2025.f1098."))},
            "raw_fact_inventory": raw_inventory,
            "raw_account_assertions": {
                "same_borrowing_recognition": "yes; synthetic exact borrowing key",
                "exact_report_links": "yes; both exact reports keyed to the same synthetic borrowing",
                "annual_ceiling": "250000; synthetic raw person assertion",
                "other_home_debt": "no; synthetic raw person assertion",
                "return_filing_status": "present as a separate return-wide raw fact in imported base acts",
            },
            "not_supplied_because_derived": [
                "per-report support/status and reasons", "borrowing-level category/ceiling reconciliation",
                "authorized Schedule A line8a publication",
            ],
            "derived_inventory": derived_inventory,
            "six_case_execution": live_summaries,
            "synthetic_seed": "synthetic-seed-acts.json",
        }
        result["output_directory"] = str(out_dir.relative_to(ROOT))
        (out_dir / "synthetic-seed-acts.json").write_text(
            json.dumps(acts, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (out_dir / "scaffold-result.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return result


if __name__ == "__main__":
    print(json.dumps(run_bridge_candidate(), indent=2, sort_keys=True))
