"""Synthetic P2 Option A diagnostic generator; not a test/product entrypoint.

The current increment creates report-local same-subject bridges in an
ephemeral, checksum-verified package and validates its exclusive member graph.
It does not run the coordinator or claim the connected borrowing outcome.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from packages.derivation.loader import DerivationSchemas
from packages.derivation.live import _resolved_run_material
from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.derivation.production_resolver import (
    PublicationSurface,
    Refusal,
    resolve_production_package,
)

_P0_SPEC = importlib.util.spec_from_file_location(
    "p0_current_path_probe", Path(__file__).resolve().with_name("p0-current-path-probe.py"))
if _P0_SPEC is None or _P0_SPEC.loader is None:
    raise RuntimeError("could not load the committed P0 synthetic fixture helper")
_P0 = importlib.util.module_from_spec(_P0_SPEC)
_P0_SPEC.loader.exec_module(_P0)
_latest_acts = _P0._latest_acts
RUN_SCOPE = _P0.SCOPE
SCOPE_USER = _P0.RUN_USER

CONTENT = ROOT / "packages/content/tax/2025"
RELEASE_DIR = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
PACKAGE_ID = "tax.us.2025.package.core-calculations"
PACKAGE_VERSION = "v49"
RELEASE_ID = "demo.release.sli-worksheet-integration.2025"
RELEASE_VERSION = "v47"
BRIDGE_PACKAGE_VERSION = "v50"
BRIDGE_RELEASE_ID = "demo.release.mortgage-statement-borrowing.2025"
BRIDGE_RELEASE_VERSION = "v1"
BRIDGE_BUNDLE_ID = "demo.tax.2025.f1098-report-local-bridge"
BRIDGE_BUNDLE_VERSION = "v1"
BRIDGE_RULE_PREFIX = "demo.rule.tax.2025.f1098-report-local-bridge"
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
    bundle = {"schema": "bundle.v2", "id": BRIDGE_BUNDLE_ID, "version": BRIDGE_BUNDLE_VERSION,
              "label": "Synthetic P2 report-local bridge outputs", "fact_types": bridge_facts}
    return bundle, rules


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
    package["members"].append({"id": BRIDGE_BUNDLE_ID, "version": BRIDGE_BUNDLE_VERSION,
                               "schema": "bundle.v2", "role": "fact-type-bundle"})
    package["entrypoints"] = [
        {**entry, "version": "v3"}
        if entry.get("id") == "tax.us.2025.rule.f1098-residence-interest-reason"
        else entry
        for entry in package["entrypoints"]
    ]
    package["entrypoints"].append({"id": BRIDGE_BUNDLE_ID, "version": BRIDGE_BUNDLE_VERSION})
    for rule in rules:
        _write_json(members / f"{rule['id']}.json", rule)
        package["members"].append({"id": rule["id"], "version": "v1",
                                   "schema": "rule-artifact.v13", "role": "computation"})
    package["members"] = [member for member in package["members"]
                          if not (member["id"] == "tax.us.2025.rule.f1098-residence-interest-reason"
                                  and member["version"] == "v2")]
    _write_json(members / "rule.f1098-residence-interest-reason.v3.json", successor_reason)
    package["members"].append({"id": successor_reason["id"], "version": "v3",
                               "schema": "rule-artifact.v14", "role": "computation"})

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

    acts = _latest_acts(second_report=True, second_box2=220000.0, fixture_answers=True)
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
    shutil.copy2(members / f"package.core-calculations.{BRIDGE_PACKAGE_VERSION}.json",
                 retained / f"package.core-calculations.{BRIDGE_PACKAGE_VERSION}.json")
    shutil.copy2(registry_path, retained / registry_path.name)
    shutil.copy2(release_path, retained / release_path.name)
    return surface, pins, acts


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
        if fact_type.startswith("tax.us.2025.f1098."):
            by_type.setdefault(fact_type, []).append(identity)
    return [{"fact_type": name, "count": len(ids), "identities": sorted(ids)}
            for name, ids in sorted(by_type.items())]


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
        if len(candidate_rules) != len(BRIDGE_TYPES):
            raise RuntimeError(f"expected {len(BRIDGE_TYPES)} candidate rules, resolved {len(candidate_rules)}")
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
        derived_inventory = [
            {"result": "per-report support/status for each exact report", "count_in_seed": 0,
             "state": "not supplied; must be derived by candidate content"},
            {"result": "borrowing-level category and ceiling comparison", "count_in_seed": 0,
             "state": "not supplied; must be derived by candidate content"},
            {"result": "authorized Schedule A line8a publication", "count_in_seed": 0,
             "state": "not supplied; must be derived by candidate content"},
        ]
        result = {
            "stage": "report-local-bridge-package-resolution",
            "evidence_ceiling": "synthetic source/answer acts plus successful real package validation and source-material discovery; no rule execution or filing claim",
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
                "same_borrowing_recognition": "not present in imported P0 seed; supplied separately in next increment",
                "exact_report_links": "not present in imported P0 seed; supplied separately in next increment",
                "annual_ceiling": "not present in imported P0 seed; supplied separately in next increment",
                "other_home_debt": "not present in imported P0 seed; supplied separately in next increment",
                "return_filing_status": "present as a separate return-wide raw fact in imported base acts",
            },
            "derived_inventory": derived_inventory,
            "six_case_execution": "not run; connected borrowing reconciliation and line8a collector are not implemented",
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
