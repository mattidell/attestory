"""Bounded Track 0 declaration/coordinator check; synthetic only."""
from __future__ import annotations

import copy
import argparse
import hashlib
import importlib.util
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SPEC = importlib.util.spec_from_file_location("t0_p2", Path(__file__).with_name("p2-option-a-probe.py"))
assert SPEC and SPEC.loader
P2 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(P2)
_act_finding = P2._act_finding
from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.derivation.production_resolver import PublicationSurface, Refusal, resolve_production_package
from packages.derivation.loader import DerivationSchemas
from packages.kernel.facts import fact_id_for

BOX1 = "tax.us.2025.f1098.box1-mortgage-interest"
SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}
CARRIERS = {
    "affirmed": "demo.tax.2025.f1098.borrowing-affirmed",
    "denied": "demo.tax.2025.f1098.borrowing-denied",
    "unknown": "demo.tax.2025.f1098.borrowing-unresolved",
    "withdrawn": "demo.tax.2025.f1098.borrowing-withdrawn",
}
BASE_PACKAGE_VERSION = "v51"
BASE_REGISTRY_FILENAME = "published-packages.v49.json"
BASE_RELEASE_VERSION = "v49"
INTERMEDIATE_PACKAGE_VERSION = "v52"
P2_CANDIDATE_REGISTRY_FILENAME = "published-packages.t0-intermediate-v52.json"
T0_PACKAGE_VERSION = "v57"
T0_REGISTRY_FILENAME = "published-packages.t0-p57.json"
T0_RELEASE_VERSION = "v7"


def read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text("utf-8"))


def write(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def add_v51_explicit_answers(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Supply the new adopted-surface inputs explicitly; do not infer/default them."""
    result = copy.deepcopy(acts)
    bundle = read(P2.CONTENT / "senior-and-dependent-deductions.vocabulary.bundle.json")
    if not any(row.get("kind") == "bundle-adoption" and
               row.get("payload", {}).get("bundle", {}).get("id") == bundle["id"] for row in result):
        result.append({"schema": "act.v1", "act_id": "demo.t0.v51.senior-dependent-bundle",
            "kind": "bundle-adoption", "actor": "demo.taxpayer", "at": "2026-10-22T13:10:00Z",
            "committed_against": len(result), "payload": {"bundle": bundle}})
    for fact_type, value, tag in (
        ("tax.us.2025.standard-deduction.can-be-claimed-as-dependent", "no", "can-be-claimed-no"),
        ("tax.us.2025.schedule1a.no-parts-ii-iv-deductions-declared", "yes", "no-parts-ii-iv"),
    ):
        fact_id = fact_id_for(fact_type, (("tax-year", "2025"),))
        if any(act.get("kind") == "assertion" and _act_finding(act).get("fact_id") == fact_id for act in result):
            continue
        result.append({"schema": "act.v1", "act_id": f"demo.t0.v51.{tag}",
            "kind": "assertion", "actor": "demo.taxpayer", "at": "2026-10-22T13:10:01Z",
            "committed_against": len(result), "payload": {"finding": {
                "schema": "finding.v2", "id": f"demo.t0.v51.finding.{tag}", "fact_id": fact_id,
                "value": value, "basis": "attested", "evidence_ids": []}}})
    for index, act in enumerate(result):
        act["committed_against"] = index
        if act.get("kind") == "package-adoption":
            act.setdefault("payload", {})["revision"] = index
    return result


def ceiling_collision_acts(seed: list[dict[str, Any]], case_id: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Apply one exact, synthetic borrowing-key ceiling collision to supplied acts."""
    acts = copy.deepcopy(seed)
    if case_id == "supported-pair-core-v51":
        return acts, {"caseId": case_id, "mutation": "none",
            "suppliedAnswers": {
                "canBeClaimedAsDependent": "no",
                "schedule1aNoPartsIItoIV": "yes",
                "source": "explicit synthetic assertions in synthetic-seed-acts.json"},
            "expected": "supported pair on core v51; line8a $11,000"}
    borrowing_a, borrowing_b = "demo.f1098.borrowing.A", "demo.f1098.borrowing.B"
    keys_a = (("borrowing", borrowing_a), ("tax-year", "2025"))
    keys_b = (("borrowing", borrowing_b), ("tax-year", "2025"))
    fact_a = fact_id_for(P2.ACCOUNT_FACTS["ceiling"], keys_a)
    fact_b = fact_id_for(P2.ACCOUNT_FACTS["ceiling"], keys_b)
    a_claims = [act for act in acts if act.get("kind") == "assertion"
                and _act_finding(act).get("fact_id") == fact_a]
    if len(a_claims) != 1:
        raise AssertionError(f"expected exactly one supplied A ceiling act, found {len(a_claims)}")
    if case_id == "a-ceiling-missing-b-ceiling-300k":
        acts.remove(a_claims[0])
        b_value = 300000.0
        expected = "no favorable mortgage line8a from B's ceiling; A has no selected ceiling"
    elif case_id == "a-valid-dormant-b-ceiling-900k":
        b_value = 900000.0
        expected = "same supported $11,000 line8a; only A's $250,000 ceiling is selected"
    else:
        raise ValueError(f"unknown ceiling collision case: {case_id}")
    if any(act.get("kind") == "assertion" and _act_finding(act).get("fact_id") == fact_b for act in acts):
        raise AssertionError("B ceiling unexpectedly exists in the base fixture")
    b_finding = {"schema": "finding.v2", "id": f"demo.t0.{case_id}.borrowing-b-ceiling",
        "fact_id": fact_b, "value": b_value, "basis": "attested", "evidence_ids": []}
    acts.append({"schema": "act.v1", "act_id": f"demo.t0.{case_id}.borrowing-b-ceiling",
        "kind": "assertion", "actor": "demo.taxpayer", "at": "2026-10-22T13:05:00Z",
        "committed_against": len(acts), "payload": {"finding": b_finding}})
    for index, act in enumerate(acts):
        act["committed_against"] = index
        if act.get("kind") == "package-adoption":
            act.setdefault("payload", {})["revision"] = index
    claims = []
    for act in acts:
        finding = _act_finding(act)
        if finding.get("fact_id") in {fact_a, fact_b}:
            claims.append({"act_id": act.get("act_id"), "fact_id": finding["fact_id"],
                           "value": finding.get("value")})
    expected_claims = 1 if case_id.startswith("a-ceiling-missing") else 2
    if len(claims) != expected_claims:
        raise AssertionError(f"unexpected A/B ceiling claims: {claims}")
    return acts, {"caseId": case_id, "ceilingClaims": claims,
        "expected": expected, "recognizedBorrowing": borrowing_a,
        "unrecognizedBorrowing": borrowing_b}


def add_status_composition(members: Path) -> dict[str, Any]:
    """Add four per-report numeric link counts and one per-report status rule."""
    package_path = members / f"package.core-calculations.{INTERMEDIATE_PACKAGE_VERSION}.json"
    bundle_path = members / f"{P2.BRIDGE_BUNDLE_ID}.v1.json"
    package, bundle = read(package_path), read(bundle_path)
    box = next(ft for ft in read(members / "f1098.bundle.json")["fact_types"] if ft["id"] == BOX1)
    membership = next(ft for ft in bundle["fact_types"] if ft["id"] == P2.ACCOUNT_FACTS["membership"])
    # Keep the outcome carriers distinct, so link_count sees one current outcome
    # class rather than all enum values in one fact type.
    for state, carrier in CARRIERS.items():
        outcome = copy.deepcopy(membership)
        outcome.update({"id": carrier, "version": "v1", "title": f"Synthetic current {state} pair outcome",
                        "value_schema": {"type": "string", "enum": [state]}})
        if not any(ft["id"] == carrier for ft in bundle["fact_types"]):
            bundle["fact_types"].append(outcome)
        if not any(row.get("fact_type", {}).get("id") == carrier for row in package["input_bindings"]):
            package["input_bindings"].append({"fact_type": {"id": carrier, "version": "v1"},
                                              "mode": "required", "symbol": carrier})
    citations = read(members / "rule.f1098-line8a.v2.json").get("citations", [])
    outputs: dict[str, str] = {}
    new_rules: list[dict[str, Any]] = []
    for state, carrier in CARRIERS.items():
        count_id = f"demo.tax.2025.f1098.borrowing-{state}-count"
        count_type = copy.deepcopy(box)
        count_type.update({"id": count_id, "version": "v1", "title": f"Synthetic {state} outcome count per report",
                           "value_schema": {"type": "number"}})
        bundle["fact_types"].append(count_type)
        rule = {"schema": "rule-artifact.v13", "id": f"demo.tax.2025.rule.borrowing-{state}-count",
            "version": "v1", "scope": SCOPE, "role": "computation",
            "subject": {"id": BOX1, "version": "v1"},
            "joined": {"id": carrier, "version": "v1"}, "direction": "joined_contains_subject",
            "requires": [carrier], "pins": [], "when": True,
            "value": {"op": "link_count", "links": carrier}, "publishes": count_id,
            "blocked": {"code": "DEPENDENCY_INVALID", "missing": []}, "citations": citations,
            "notes": "Synthetic exact report/year count; the joined carrier adds borrowing identity."}
        new_rules.append(rule)
        outputs[state] = count_id

    status_id = "demo.tax.2025.f1098.borrowing-current-link-status"
    status_type = copy.deepcopy(box)
    status_type.update({"id": status_id, "version": "v1", "title": "Synthetic report-local relationship status",
                        "value_schema": {"type": "string", "enum": ["none", *CARRIERS.keys(), "conflict"]}})
    bundle["fact_types"].append(status_type)
    expressions = [{"op": "compare", "cmp": "eq", "left": {"op": "ref", "name": outputs[s]}, "right": 1}
                   for s in CARRIERS]
    zeroes = [{"op": "compare", "cmp": "eq", "left": {"op": "ref", "name": outputs[s]}, "right": 0}
              for s in CARRIERS]
    # A current relationship must be unique. Empty is distinct from conflict.
    value: dict[str, Any] = {"op": "category_literal", "fact_type": {"id": status_id, "version": "v1"}, "value": "conflict"}
    for state, predicate in reversed(list(zip(CARRIERS, expressions))):
        value = {"op": "choose", "when": predicate,
                 "then": {"op": "category_literal", "fact_type": {"id": status_id, "version": "v1"}, "value": state},
                 "else": value}
    total = {"op": "add", "args": [{"op": "ref", "name": outputs[s]} for s in CARRIERS]}
    value = {"op": "choose", "when": {"op": "compare", "cmp": "eq", "left": total, "right": 0},
             "then": {"op": "category_literal", "fact_type": {"id": status_id, "version": "v1"}, "value": "none"},
             "else": {"op": "choose", "when": {"op": "compare", "cmp": "eq", "left": total, "right": 1},
                      "then": value,
                      "else": {"op": "category_literal", "fact_type": {"id": status_id, "version": "v1"}, "value": "conflict"}}}
    status = {"schema": "rule-artifact.v13", "id": "demo.tax.2025.rule.borrowing-current-link-status",
        "version": "v1", "scope": SCOPE, "role": "computation",
        "subject": {"id": BOX1, "version": "v1"},
        "joined": {"id": next(iter(CARRIERS.values())), "version": "v1"},
        "direction": "joined_contains_subject", "requires": list(outputs.values()), "pins": [],
        "when": True, "value": value, "publishes": status_id,
        "blocked": {"code": "DEPENDENCY_INVALID", "missing": []}, "citations": citations,
        "notes": "Synthetic per-Box1 fan-in; count results inherit all report keys."}
    new_rules.append(status)

    # Wire the report-local status into the existing readiness selection as a
    # declared keyed read. Keep P2's successful line8a consumer overlay intact.
    readiness_path = members / "demo.tax.2025.rule.mortgage-borrowing-readiness.json"
    readiness = read(readiness_path)
    for path in readiness["selection"]["paths"]:
        if path["id"] == "same-borrowing":
            path["reads_subject_results"].append({"symbol": status_id, "subject": {"id": BOX1, "version": "v1"}})
    write(readiness_path, readiness)
    new_rules.append(readiness)
    for rule in new_rules:
        write(members / f"{rule['id']}.json", rule)
        if not any(m.get("id") == rule["id"] and m.get("version") == rule["version"] for m in package["members"]):
            package["members"].append({"id": rule["id"], "version": rule["version"],
                                       "schema": rule["schema"], "role": "computation"})
    write(bundle_path, bundle)
    package["package_checksum"] = package_instance_checksum(package)
    write(package_path, package)

    registry_path = members / P2_CANDIDATE_REGISTRY_FILENAME
    registry = read(registry_path)
    changed = [bundle, *new_rules]
    changed_keys = {(citizen["id"], citizen["version"]) for citizen in changed}
    registry["citizens"] = [row for row in registry["citizens"]
        if (row["id"], row["version"]) not in changed_keys]
    for citizen in changed:
        registry["citizens"].append({"id": citizen["id"], "version": citizen["version"],
                                    "checksum": citizen_checksum(citizen)})
    registry["packages"] = [row for row in registry["packages"] if row["version"] != INTERMEDIATE_PACKAGE_VERSION]
    registry["packages"].append({"id": package["id"], "version": package["version"],
                                "checksum": package["package_checksum"]})
    write(registry_path, registry)
    release_path = P2.RELEASE_DIR / f"{P2.RELEASE_ID}.{P2.RELEASE_VERSION}.json"
    candidate_release = members.parent / "releases" / f"{P2.BRIDGE_RELEASE_ID}.v1.json"
    release = read(candidate_release)
    release["package_registry_sha256"] = hashlib.sha256(registry_path.read_bytes()).hexdigest()
    write(candidate_release, release)
    # The package adoption is reconstructed by the retained P2 fixture using this hash.
    return {"countRules": [rule["id"] for rule in new_rules[:-1]], "statusRule": status["id"],
            "countFactTypes": outputs, "statusFactType": status_id,
            "representativeRule": new_rules[0], "statusRuleBody": status}


def add_dynamic_account_candidate(surface: Any, acts: list[dict[str, Any]]) -> dict[str, Any]:
    """Replace P2's literal account with opaque entity keys and a keyed account gate."""
    members = surface.member_dir
    package_path = members / f"package.core-calculations.{INTERMEDIATE_PACKAGE_VERSION}.json"
    bundle_path = members / f"{P2.BRIDGE_BUNDLE_ID}.v1.json"
    package, bundle = read(package_path), read(bundle_path)
    A, B = "demo.f1098.borrowing.A", "demo.f1098.borrowing.B"
    entity_kind = "tax.us.mortgage-borrowing-reference"
    for ft in bundle["fact_types"]:
        for key in ft.get("identity_keys", []):
            if key.get("name") == "borrowing":
                key.clear()
                key.update({"name": "borrowing", "kind": "entity", "entity_kind": entity_kind})
    def replace_key(value: Any) -> Any:
        if isinstance(value, str):
            return value.replace("demo.f1098.borrowing.same", A)
        if isinstance(value, list):
            return [replace_key(item) for item in value]
        if isinstance(value, dict):
            return {key: replace_key(item) for key, item in value.items()}
        return value
    acts[:] = [replace_key(act) for act in acts]
    # Convert the raw current report links into the distinct affirmed carrier
    # admitted by the candidate. Values remain synthetic supplied claims.
    carrier_acts = []
    for suffix, payer, statement in (("a", "demo.f1098.lender.a", "demo.f1098.stmt.a"),
                                     ("b", "demo.f1098.lender.b", "demo.f1098.stmt.b")):
        key_tuple = (("payer", payer), ("statement", statement), ("tax-year", "2025"), ("borrowing", A))
        carrier_id = fact_id_for(CARRIERS["affirmed"], key_tuple)
        carrier_acts.append({"schema": "act.v1", "act_id": f"demo.mortgage.t0.affirmed.{suffix}",
            "kind": "assertion", "actor": "demo.taxpayer", "at": "2026-10-22T10:00:02Z",
            "committed_against": 0, "payload": {"finding": {"schema": "finding.v2",
                "id": f"demo.mortgage.t0.affirmed-finding.{suffix}", "fact_id": carrier_id,
                "value": "affirmed", "basis": "attested", "evidence_ids": []}}})
    acts.extend(carrier_acts)
    # Entity introductions follow the existing SLI opaque-reference mechanism.
    introductions = []
    for ref, label in ((A, "Synthetic borrowing A"), (B, "Synthetic borrowing B")):
        introductions.append({"schema": "act.v1", "act_id": f"demo.mortgage.t0.entity.{ref[-1]}",
            "kind": "entity-introduced", "actor": "demo.taxpayer", "at": "2026-10-22T10:00:00Z",
            "committed_against": 0,
            "payload": {"entity": {"schema": "entity.v1", "id": ref, "kind": entity_kind, "label": label}}})
    adoption = next(i for i, act in enumerate(acts) if act.get("kind") == "package-adoption")
    bundle_adoption = next(i for i, act in enumerate(acts) if act.get("kind") == "bundle-adoption"
                           and act.get("payload", {}).get("bundle", {}).get("id") == P2.BRIDGE_BUNDLE_ID)
    acts[bundle_adoption + 1:bundle_adoption + 1] = introductions
    # The supported-pair first case has a single recognized A root. B is
    # introduced as a distinct allowed entity key but carries no account claims.
    def extra_fact(type_id: str, keys: tuple[tuple[str, str], ...], value: Any, tag: str) -> dict[str, Any]:
        fact_id = fact_id_for(type_id, keys)
        return {"schema": "act.v1", "act_id": f"demo.mortgage.t0.{tag}", "kind": "assertion",
            "actor": "demo.taxpayer", "at": "2026-10-22T10:00:01Z", "committed_against": adoption,
            "payload": {"finding": {"schema": "finding.v2", "id": f"demo.mortgage.t0.finding.{tag}",
                "fact_id": fact_id, "value": value, "basis": "attested", "evidence_ids": []}}}
    for index, act in enumerate(acts):
        act["committed_against"] = index
        if act.get("kind") == "package-adoption":
            act.setdefault("payload", {})["revision"] = index
    write(bundle_path, bundle)

    # Per-report affirmed outcome gets an exact full-key numeric support marker.
    affirmed = CARRIERS["affirmed"]
    support_id = "demo.tax.2025.mortgage.f1098-link-support"
    membership_type = next(ft for ft in bundle["fact_types"] if ft["id"] == P2.ACCOUNT_FACTS["membership"])
    affirmed_type = copy.deepcopy(membership_type)
    affirmed_type.update({"id": CARRIERS["affirmed"], "version": "v1", "title": "Synthetic affirmed report link",
                          "value_schema": {"type": "string", "enum": ["affirmed"]}})
    bundle["fact_types"].append(affirmed_type)
    package["input_bindings"].append({"fact_type": {"id": CARRIERS["affirmed"], "version": "v1"},
                                      "mode": "required", "symbol": CARRIERS["affirmed"]})
    support_type = copy.deepcopy(next(ft for ft in bundle["fact_types"] if ft["id"] == affirmed))
    support_type.update({"id": support_id, "title": "Synthetic numeric support per exact linked report",
                         "value_schema": {"type": "number"}})
    bundle["fact_types"].append(support_type)
    ceiling_selected_id = "demo.tax.2025.mortgage.account-ceiling-selected"
    ceiling_selected_type = copy.deepcopy(next(ft for ft in bundle["fact_types"]
                                               if ft["id"] == P2.ACCOUNT_FACTS["recognition"]))
    ceiling_selected_type.update({"id": ceiling_selected_id,
        "title": "Borrowing-keyed selected annual principal ceiling", "value_schema": {"type": "number"}})
    bundle["fact_types"].append(ceiling_selected_type)
    ceiling_bridge = {"schema": "rule-artifact.v13", "id": "demo.tax.2025.rule.mortgage-account-ceiling-selection",
        "version": "v1", "scope": SCOPE, "role": "computation",
        "subject": {"id": P2.ACCOUNT_FACTS["recognition"], "version": "v1"},
        "joined": {"id": P2.ACCOUNT_FACTS["ceiling"], "version": "v1"},
        "direction": "joined_contains_subject", "requires": [P2.ACCOUNT_FACTS["ceiling"]], "pins": [],
        "when": True, "value": {"op": "ref", "name": P2.ACCOUNT_FACTS["ceiling"]},
        "publishes": ceiling_selected_id, "blocked": {"code": "DEPENDENCY_INVALID", "missing": [P2.ACCOUNT_FACTS["ceiling"]]},
        "citations": [], "notes": "Exact borrowing/year join selects the current ceiling for each recognized opaque account."}
    # Parent reports a true support only for an affirmative link whose Box 1,
    # ordinary reason and borrowing-keyed Box 2 comparison resolve.
    principal_rule_path = members / f"{P2.BRIDGE_RULE_PREFIX}.principal-ceiling-status.json"
    principal = read(principal_rule_path)
    principal["subject"] = {"id": affirmed, "version": "v1"}
    principal["direction"] = "subject_contains_joined"
    principal["joined"] = {"id": P2.SOURCE_TYPES["box2-outstanding-principal"], "version": "v1"}
    principal["requires"] = [P2.SOURCE_TYPES["box2-outstanding-principal"], ceiling_selected_id]
    principal_type = next(ft for ft in bundle["fact_types"] if ft["id"] == P2.PRINCIPAL_STATUS)
    principal_type["identity_keys"] = copy.deepcopy(next(ft for ft in bundle["fact_types"] if ft["id"] == affirmed)["identity_keys"])
    principal["value"] = {"op": "choose", "when": {"op": "compare", "cmp": "lte",
        "left": {"op": "ref", "name": P2.SOURCE_TYPES["box2-outstanding-principal"]},
        "right": {"op": "ref", "name": ceiling_selected_id}},
        "then": {"op": "category_literal", "fact_type": {"id": P2.PRINCIPAL_STATUS, "version": "v1"},
                 "value": "within-ceiling"},
        "else": {"op": "category_literal", "fact_type": {"id": P2.PRINCIPAL_STATUS, "version": "v1"},
                 "value": "over-ceiling"}}
    write(principal_rule_path, principal)
    citations = principal.get("citations", [])
    support_rule = {"schema": "rule-artifact.v13", "id": "demo.tax.2025.rule.mortgage-link-support",
        "version": "v1", "scope": SCOPE, "role": "computation",
        "subject": {"id": affirmed, "version": "v1"},
        "joined": {"id": BOX1, "version": "v1"}, "direction": "subject_contains_joined",
        "requires": ["tax.us.2025.f1098.residence-interest-reason", P2.PRINCIPAL_STATUS,
                      P2.ACCOUNT_FACTS["report-link-status"]],
        "pins": [], "when": True,
        "value": {"op": "choose", "when": {"op": "all", "args": [
            {"op": "collect_categorical_all_equal", "name": "tax.us.2025.f1098.residence-interest-reason",
             "value": {"op": "category_literal", "fact_type": {"id": "tax.us.2025.f1098.residence-interest-reason", "version": "v2"}, "value": "qualified"}},
            {"op": "collect_categorical_all_equal", "name": P2.ACCOUNT_FACTS["report-link-status"],
             "value": {"op": "category_literal", "fact_type": {"id": P2.ACCOUNT_FACTS["report-link-status"], "version": "v1"}, "value": "yes"}},
            {"op": "collect_categorical_all_equal", "name": P2.PRINCIPAL_STATUS,
             "value": {"op": "category_literal", "fact_type": {"id": P2.PRINCIPAL_STATUS, "version": "v1"}, "value": "within-ceiling"}}]},
            "then": 1, "else": 0}, "publishes": support_id,
        "blocked": {"code": "DEPENDENCY_INVALID", "missing": []}, "citations": citations,
        "notes": "Synthetic numeric success marker; one means this exact linked report's derived support is qualified."}
    # Distinct per-account count and link coverage. `empty` is a demo-only zero pin.
    count_id = "demo.tax.2025.mortgage.affirmed-link-count"
    count_type = copy.deepcopy(next(ft for ft in bundle["fact_types"] if ft["id"] == P2.ACCOUNT_FACTS["recognition"]))
    count_type.update({"id": count_id, "title": "Affirmed report count per recognized borrowing", "value_schema": {"type": "number"}})
    coverage_id = "demo.tax.2025.mortgage.affirmed-link-coverage"
    coverage_type = copy.deepcopy(count_type)
    coverage_type.update({"id": coverage_id, "title": "Numeric support coverage per borrowing"})
    bundle["fact_types"].extend([count_type, coverage_type])
    count_rule = {"schema": "rule-artifact.v13", "id": "demo.tax.2025.rule.mortgage-affirmed-link-count",
        "version": "v1", "scope": SCOPE, "role": "computation",
        "subject": {"id": P2.ACCOUNT_FACTS["recognition"], "version": "v1"},
        "joined": {"id": affirmed, "version": "v1"}, "direction": "joined_contains_subject",
        "requires": [], "pins": [], "when": True, "value": {"op": "link_count", "links": affirmed},
        "publishes": count_id, "blocked": {"code": "DEPENDENCY_INVALID", "missing": []}, "citations": citations}
    empty_parameter = {"schema": "parameter-declaration.v1", "id": "demo.tax.2025.parameter.mortgage-empty-link-support",
        "version": "v1", "scope": {**SCOPE, "effective_from": "2025-01-01"}, "values": 0}
    coverage_rule = {"schema": "rule-artifact.v13", "id": "demo.tax.2025.rule.mortgage-affirmed-link-coverage",
        "version": "v1", "scope": SCOPE, "role": "computation",
        "subject": {"id": P2.ACCOUNT_FACTS["recognition"], "version": "v1"},
        "joined": {"id": affirmed, "version": "v1"}, "direction": "joined_contains_subject",
        "requires": [], "pins": [], "when": True,
        "value": {"op": "link_coverage", "links": affirmed, "reductions": support_id,
                  "empty": {"parameter": {"id": empty_parameter["id"], "version": "v1"}}},
        "publishes": coverage_id, "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
        "citations": citations, "notes": "Exact full-link-key numerical coverage; no scalar or label joins."}
    account_ready_id = "demo.tax.2025.mortgage.account-readiness"
    ready_type = copy.deepcopy(count_type)
    ready_type.update({"id": account_ready_id, "title": "Borrowing-keyed readiness",
                       "value_schema": {"type": "string", "enum": ["ready"]}})
    bundle["fact_types"].append(ready_type)
    ready_rule = {"schema": "rule-artifact.v13", "id": "demo.tax.2025.rule.mortgage-account-readiness",
        "version": "v1", "scope": SCOPE, "role": "computation",
        "subject": {"id": P2.ACCOUNT_FACTS["recognition"], "version": "v1"},
        "joined": {"id": affirmed, "version": "v1"}, "direction": "joined_contains_subject",
        "requires": [ceiling_selected_id, P2.ACCOUNT_FACTS["other-debt"], count_id, coverage_id],
        "pins": [], "when": True,
        "value": {"op": "choose", "when": {"op": "all", "args": [
            {"op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": P2.ACCOUNT_FACTS["recognition"]},
             "right": {"op": "category_literal", "fact_type": {"id": P2.ACCOUNT_FACTS["recognition"], "version": "v1"}, "value": "yes"}},
            {"op": "compare", "cmp": "gte", "left": {"op": "ref", "name": count_id}, "right": 1},
            {"op": "compare", "cmp": "lte", "left": {"op": "ref", "name": count_id}, "right": 2},
            {"op": "compare", "cmp": "eq", "left": {"op": "shared_key_count",
                "fact_type": P2.ACCOUNT_FACTS["recognition"], "key": "tax-year"}, "right": 1},
            {"op": "compare", "cmp": "eq", "left": {"op": "ref", "name": count_id},
             "right": {"op": "count", "name": BOX1, "source_set": "tax.us.2025.f1098"}},
            {"op": "compare", "cmp": "eq", "left": {"op": "ref", "name": count_id}, "right": {"op": "ref", "name": coverage_id}},
            {"op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": P2.ACCOUNT_FACTS["other-debt"]},
             "right": {"op": "category_literal", "fact_type": {"id": P2.ACCOUNT_FACTS["other-debt"], "version": "v1"}, "value": "no"}}]},
            "then": {"op": "category_literal", "fact_type": {"id": account_ready_id, "version": "v1"}, "value": "ready"},
            "else": {"op": "block", "code": "DEPENDENCY_INVALID"}},
        "publishes": account_ready_id, "blocked": {"code": "DEPENDENCY_INVALID", "missing": [P2.ACCOUNT_FACTS["ceiling"]]},
        "citations": citations, "notes": "Per recognized opaque borrowing/year: same-key ceiling and link coverage."}
    # Replace the old scalar-readiness expression with a return-level declared
    # selector that consumes every Box1 status and every current borrowing root.
    selector_path = members / "demo.tax.2025.rule.mortgage-borrowing-readiness.json"
    selector = read(selector_path)
    path = selector["selection"]["paths"][0]
    path["reads_subject_results"] = [
        read for read in path.get("reads_subject_results", [])
        if read.get("symbol") in {"tax.us.2025.f1098.residence-interest-reason",
                                  "demo.tax.2025.f1098.reported-box3-origination-date",
                                  P2.ACCOUNT_FACTS["report-link-status"]}
    ] + [
        {"symbol": account_ready_id, "subject": {"id": P2.ACCOUNT_FACTS["recognition"], "version": "v1"}},
        {"symbol": ceiling_selected_id, "subject": {"id": P2.ACCOUNT_FACTS["recognition"], "version": "v1"}}]
    path["requires"] = ["filing_status", "tax.us.2025.f1098.box3-origination-date"]
    path["pins"] = [{"role": "input", "id": name, "version": "v1", "origin": "assertion"}
                     for name in path["requires"]]
    path["value"] = {"op": "all", "args": [
        {"op": "require_closed", "source_set": "tax.us.2025.f1098"},
        {"op": "collect_categorical_all_equal", "name": P2.ACCOUNT_FACTS["report-link-status"],
         "value": {"op": "category_literal", "fact_type": {"id": P2.ACCOUNT_FACTS["report-link-status"], "version": "v1"}, "value": "yes"}},
        {"op": "collect_categorical_all_equal", "name": account_ready_id,
         "value": {"op": "category_literal", "fact_type": {"id": account_ready_id, "version": "v1"}, "value": "ready"}},
        {"op": "collect_categorical_all_equal", "name": "demo.tax.2025.f1098.reported-box3-origination-date",
         "value": {"op": "ref", "name": "tax.us.2025.f1098.box3-origination-date"}},
        {"op": "compare", "cmp": "lte",
         "left": {"op": "add", "args": [{"op": "collect", "name": ceiling_selected_id,
                                           "source_set": "tax.us.2025.f1098"}]},
         "right": {"op": "parameter", "parameter_id": "tax.us.2025.f1098.mortgage-interest-limit",
                   "key": {"op": "ref", "name": "filing_status"}}}]}
    selector["selection"]["default"]["value"] = False
    selector["selection"]["default"]["when"] = True
    write(selector_path, selector)
    # P2's synthetic act embeds the old bundle snapshot; make its current
    # adoption match the disposable candidate's exact declared surface.
    for act in acts:
        if act.get("kind") == "bundle-adoption" and act.get("payload", {}).get("bundle", {}).get("id") == P2.BRIDGE_BUNDLE_ID:
            act["payload"]["bundle"] = copy.deepcopy(bundle)
    new_rules = [ceiling_bridge, support_rule, count_rule, coverage_rule, ready_rule, selector]
    for rule in new_rules:
        write(members / f"{rule['id']}.json", rule)
        if not any(m.get("id") == rule["id"] and m.get("version") == rule["version"] for m in package["members"]):
            package["members"].append({"id": rule["id"], "version": rule["version"], "schema": rule["schema"], "role": rule["role"]})
    package["members"].append({"id": empty_parameter["id"], "version": "v1", "schema": empty_parameter["schema"], "role": "parameter"})
    write(members / f"{empty_parameter['id']}.json", empty_parameter)
    write(bundle_path, bundle)
    package["package_checksum"] = package_instance_checksum(package)
    write(package_path, package)
    registry_path = members / P2_CANDIDATE_REGISTRY_FILENAME
    registry = read(registry_path)
    changed = [bundle, *new_rules, empty_parameter, principal]
    changed_keys = {(citizen["id"], citizen["version"]) for citizen in changed}
    registry["citizens"] = [row for row in registry["citizens"] if (row["id"], row["version"]) not in changed_keys]
    for citizen in changed:
        registry["citizens"].append({"id": citizen["id"], "version": citizen["version"], "checksum": citizen_checksum(citizen)})
    registry["packages"] = [row for row in registry["packages"] if row["version"] != INTERMEDIATE_PACKAGE_VERSION]
    registry["packages"].append({"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]})
    write(registry_path, registry)
    release_path = surface.release_dir / f"{P2.BRIDGE_RELEASE_ID}.v1.json"
    release = read(release_path)
    release["package_registry_sha256"] = hashlib.sha256(registry_path.read_bytes()).hexdigest()
    write(release_path, release)
    return {"dynamicBorrowingKeys": [A, B], "accountRules": [r["id"] for r in new_rules],
            "supportFactType": support_id, "accountReadinessFactType": account_ready_id,
            "selectedCeilingFactType": ceiling_selected_id,
            "recognizedRootCount": "shared_key_count(recognition, tax-year) == 1"}


def add_p3_consumers(surface: Any, acts: list[dict[str, Any]], p3: Any) -> tuple[Any, list[dict[str, Any]], dict[str, Any]]:
    """Apply the retained P3 line12e and attachment-completeness successors."""
    members, releases = surface.member_dir, surface.release_dir
    package_path = members / f"package.core-calculations.{INTERMEDIATE_PACKAGE_VERSION}.json"
    package = read(package_path)
    line12e = p3._line12e_successor()
    line12e_path = members / "rule.form1040-line12e.v2.json"
    write(line12e_path, line12e)
    attachment_path = members / "attachment.schedule-a.json"
    attachment = read(attachment_path)
    checks = attachment.get("completeness", {}).get("required_answers", [])
    removed = [item for item in checks if item.get("symbol") == "tax.us.2025.f1098.liable-and-paid"]
    kept = [item for item in checks if item.get("symbol") != "tax.us.2025.f1098.liable-and-paid"]
    expected = {f"tax.us.2025.schedule-a-boundary.{name}-declared" for name in
        ("no-medical", "no-salt", "no-other-interest", "no-investment-interest", "no-charitable",
         "no-casualty-theft", "no-gambling-other")}
    if len(removed) != 1 or {item.get("symbol") for item in kept} != expected:
        raise RuntimeError("candidate attachment does not match the retained P3 completeness successor premise")
    attachment["version"] = "v2"
    attachment["completeness"]["required_answers"] = kept
    attachment_v2_path = members / "attachment.schedule-a.v2.json"
    write(attachment_v2_path, attachment)
    package["version"] = T0_PACKAGE_VERSION
    for collection in (package["members"], package["entrypoints"]):
        for row in collection:
            if row.get("id") == "tax.us.2025.rule.form1040-line12e" and row.get("version") == "v1":
                row["version"] = "v2"
                if collection is package["members"]:
                    row["schema"] = line12e["schema"]
            elif row.get("id") == "tax.us.2025.rule.attachment.schedule-a" and row.get("version") == "v1":
                row["version"] = "v2"
                if collection is package["members"]:
                    row["schema"] = attachment["schema"]
    for row in package["entrypoints"]:
        if row.get("id") == "tax.us.2025.rule.form1040-line12e":
            row["version"] = "v2"
        if row.get("id") == "tax.us.2025.rule.attachment.schedule-a":
            row["version"] = "v2"
    registry = read(members / P2_CANDIDATE_REGISTRY_FILENAME)
    registry["citizens"].append({"id": line12e["id"], "version": "v2", "checksum": citizen_checksum(line12e)})
    registry["citizens"].append({"id": attachment["id"], "version": "v2", "checksum": citizen_checksum(attachment)})
    package["package_checksum"] = package_instance_checksum(package)
    registry["packages"].append({"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]})
    registry_path = members / T0_REGISTRY_FILENAME
    write(registry_path, registry)
    package_path = members / f"package.core-calculations.{T0_PACKAGE_VERSION}.json"
    write(package_path, package)
    release = {"schema": "release-registry.v1", "id": P2.BRIDGE_RELEASE_ID, "version": T0_RELEASE_VERSION,
        "package_registry_sha256": hashlib.sha256(registry_path.read_bytes()).hexdigest()}
    release_path = releases / f"{P2.BRIDGE_RELEASE_ID}.{T0_RELEASE_VERSION}.json"
    write(release_path, release)
    # Rebind the supplied package adoption; no user data is added after the run begins.
    acts = p3._add_schedule_a_boundary_declarations(acts)
    adoption = next(act for act in acts if act.get("kind") == "package-adoption"
                    and act.get("payload", {}).get("package", {}).get("id") == package["id"])
    adoption["payload"]["package"] = {"id": package["id"], "version": T0_PACKAGE_VERSION, "checksum": package["package_checksum"]}
    adoption["payload"]["release"] = {"id": release["id"], "version": T0_RELEASE_VERSION,
        "checksum": hashlib.sha256(release_path.read_bytes()).hexdigest()}
    for index, act in enumerate(acts):
        act["committed_against"] = index
        if act.get("kind") == "package-adoption":
            act.setdefault("payload", {})["revision"] = index
    return PublicationSurface(releases, registry_path, members), acts, {
        "packageVersion": T0_PACKAGE_VERSION, "line12eVersion": "v2", "attachmentVersion": "v2",
        "releaseVersion": T0_RELEASE_VERSION, "removedAttachmentPresenceCheck": removed[0],
        "retainedAttachmentBoundaryAnswers": sorted(expected)}


def keyed_presentation_overlay(source: str) -> str:
    """T0-local repair: display only support keyed to the actual current root."""
    old = '''        # Actual shared account findings are raw current assertions, not display-derived conclusions.
        support_types = ["demo.tax.2025.mortgage.continuing-borrowing",
                         "demo.tax.2025.mortgage.annual-ceiling",
                         "demo.tax.2025.mortgage.other-home-secured-debt"]
        shared_support = []
        for fact_type in support_types:
            candidates = []
            from packages.kernel.currency import compute_currency
            current = compute_currency(state).current_finding_ids
            for finding_id in current:
                f = state.findings.get(finding_id)
                ft = fact_map.get(str(f.get("fact_id"))) if f else None
                if ft is not None and ft.fact_type_id == fact_type:
                    candidates.append((f, ft))
            if len(candidates) != 1:
                raise projection.PresentationModelError(f"P3 expected one current shared support finding for {fact_type}")
            finding, fact = candidates[0]
            shared_support.append({"findingId": finding["id"], "factType": fact_type,
                "value": str(finding.get("value")), "keys": dict(fact.keys),
                "evidenceIds": list(finding.get("evidence_ids", []) or [])})
'''
    new = '''        # T0-only display association: the actual current continuing-borrowing
        # finding supplies structured keys; current claims for another key are
        # not presented as this account's support. Displayed raw claims are not
        # asserted to be consumed inputs; the run's recorded pins remain proof.
        support_types = ["demo.tax.2025.mortgage.continuing-borrowing",
                         "demo.tax.2025.mortgage.annual-ceiling",
                         "demo.tax.2025.mortgage.other-home-secured-debt"]
        from packages.kernel.currency import compute_currency
        current = compute_currency(state).current_finding_ids
        current_rows = []
        for finding_id in current:
            f = state.findings.get(finding_id)
            ft = fact_map.get(str(f.get("fact_id"))) if f else None
            if ft is not None:
                current_rows.append((f, ft))
        roots = [(f, ft) for f, ft in current_rows
                 if ft.fact_type_id == support_types[0]]
        if len(roots) != 1:
            raise projection.PresentationModelError("T0 expected one current continuing-borrowing root")
        active_keys = dict(roots[0][1].keys)
        shared_support = []
        for fact_type in support_types:
            candidates = [(f, ft) for f, ft in current_rows
                          if ft.fact_type_id == fact_type and dict(ft.keys) == active_keys]
            if fact_type == support_types[1] and not candidates:
                # Missing keyed ceiling is represented by the real readiness /
                # consumer disposition below, never by another account's value.
                continue
            if len(candidates) != 1:
                raise projection.PresentationModelError(
                    f"T0 expected one current shared support finding for {fact_type} and root keys")
            finding, fact = candidates[0]
            shared_support.append({"findingId": finding["id"], "factType": fact_type,
                "value": str(finding.get("value")), "keys": dict(fact.keys),
                "evidenceIds": list(finding.get("evidence_ids", []) or [])})
'''
    if source.count(old) != 1:
        raise AssertionError("P3 shared-support source block changed; refusing a fuzzy adapter rewrite")
    return source.replace(old, new, 1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run selected synthetic T0 mortgage cases.")
    parser.add_argument("--case", action="append", required=True, choices=(
        "supported-pair-core-v51",
        "a-ceiling-missing-b-ceiling-300k", "a-valid-dormant-b-ceiling-900k"),
        help="T0 case to execute; may be repeated. The prior supported-pair case is not run here.")
    args = parser.parse_args()
    if len(set(args.case)) != len(args.case):
        parser.error("each ceiling-collision case may be selected only once")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = ROOT / "temp/mortgage-statement-borrowing" / f"t0-dynamic-binding-{stamp}"
    out.mkdir(parents=True, exist_ok=False)
    with TemporaryDirectory(prefix="demo-mortgage-t0-content-") as tmp:
        surface, _pins, acts = P2._materialize_candidate_surface(
            Path(tmp), out, base_package_version=BASE_PACKAGE_VERSION,
            base_registry_filename=BASE_REGISTRY_FILENAME,
            candidate_registry_filename=P2_CANDIDATE_REGISTRY_FILENAME,
            base_release_version=BASE_RELEASE_VERSION,
            candidate_package_version=INTERMEDIATE_PACKAGE_VERSION)
        declaration = {"statusSource": P2.ACCOUNT_FACTS["report-link-status"],
                       "fourOutcomeCountExperiment": "not part of this supported-pair increment",
                       "currentBase": {"corePackage": BASE_PACKAGE_VERSION,
                           "packageRegistry": BASE_REGISTRY_FILENAME,
                           "sourceRelease": BASE_RELEASE_VERSION},
                       "candidate": {"package": T0_PACKAGE_VERSION,
                           "packageRegistry": T0_REGISTRY_FILENAME,
                           "release": T0_RELEASE_VERSION}}
        dynamic = add_dynamic_account_candidate(surface, acts)
        p3spec = importlib.util.spec_from_file_location("t0_p3", Path(__file__).with_name("p3-saved-model-probe.py"))
        assert p3spec and p3spec.loader
        P3 = importlib.util.module_from_spec(p3spec)
        p3spec.loader.exec_module(P3)
        surface, acts, consumers = add_p3_consumers(surface, acts, P3)
        # Supply the two new v51 inputs as explicit synthetic claims; neither
        # the SLI "is claimed" answer nor a default is used to infer them.
        acts = add_v51_explicit_answers(acts)
        # Retain the exact final disposable package artifacts and supplied acts
        # before the ephemeral publication directory is removed.
        retained = out / "candidate-content"
        retained.mkdir(parents=True, exist_ok=True)
        # Preserve the complete disposable surface, including every adopted
        # non-mortgage v51 member and its current parameter content.
        shutil.copytree(surface.member_dir, retained / "members", dirs_exist_ok=True)
        shutil.copytree(surface.release_dir, retained / "releases", dirs_exist_ok=True)
        retain_paths = [surface.member_dir / f"package.core-calculations.{BASE_PACKAGE_VERSION}.json",
            surface.member_dir / BASE_REGISTRY_FILENAME,
            surface.release_dir / f"{P2.RELEASE_ID}.{BASE_RELEASE_VERSION}.json",
            surface.member_dir / f"{P2.BRIDGE_BUNDLE_ID}.v1.json",
            surface.member_dir / f"package.core-calculations.{T0_PACKAGE_VERSION}.json",
            surface.member_dir / T0_REGISTRY_FILENAME,
            surface.release_dir / f"{P2.BRIDGE_RELEASE_ID}.{T0_RELEASE_VERSION}.json",
            surface.member_dir / "rule.form1040-line12e.v2.json",
            surface.member_dir / "attachment.schedule-a.v2.json",
            surface.member_dir / "rule.form1040-standard-deduction.v3.json",
            surface.member_dir / "rule.form1040-line16.v6.json",
            surface.member_dir / "rule.selected-preferential-base.v5.json",
            surface.member_dir / "rule.form1040-line13b.v2.json",
            surface.member_dir / "parameter.standard-deduction-base.json",
            surface.member_dir / "demo.tax.2025.parameter.mortgage-empty-link-support.json",
            surface.member_dir / "demo.tax.2025.rule.mortgage-account-ceiling-selection.json",
            surface.member_dir / "demo.tax.2025.rule.mortgage-link-support.json",
            surface.member_dir / "demo.tax.2025.rule.mortgage-affirmed-link-count.json",
            surface.member_dir / "demo.tax.2025.rule.mortgage-affirmed-link-coverage.json",
            surface.member_dir / "demo.tax.2025.rule.mortgage-account-readiness.json",
            surface.member_dir / "demo.tax.2025.rule.mortgage-borrowing-readiness.json",
            surface.member_dir / f"{P2.BRIDGE_RULE_PREFIX}.principal-ceiling-status.json"]
        for path in retain_paths:
            shutil.copy2(path, retained / path.name)
        (out / "synthetic-seed-acts.json").write_text(json.dumps(acts, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        summary_hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in retain_paths}
        summary: dict[str, Any] = {"stage": "bounded-declaration-check", "outputDirectory": str(out.relative_to(ROOT)),
                                   "declaration": declaration, "dynamicAccount": dynamic,
                                   "P3Consumers": consumers, "retainedCandidateHashes": summary_hashes,
                                   "syntheticSuppliedActs": "synthetic-seed-acts.json",
                                   "selectedCases": list(args.case)}
        candidate_package = read(surface.member_dir / f"package.core-calculations.{T0_PACKAGE_VERSION}.json")
        preserved_member_ids = {"tax.us.2025.rule.form1040-standard-deduction",
                                "tax.us.2025.rule.form1040-line16",
                                "tax.us.2025.rule.form1040-line13b",
                                "tax.us.2025.rule.selected-preferential-base",
                                "tax.us.2025.parameter.standard-deduction-base",
                                "tax.us.2025.parameter.additional-standard-deduction",
                                "tax.us.2025.parameter.preferential-zero-ceiling",
                                "tax.us.2025.parameter.preferential-fifteen-ceiling"}
        summary["preservedCurrentBaseMembers"] = sorted(
            [row for row in candidate_package["members"] if row["id"] in preserved_member_ids],
            key=lambda row: row["id"])
        # Use the same declared P3 presentation-only overlay as the accepted
        # positive, but never replay that unchanged case on this current base.
        overlay = type("Overlay", (), {})()
        overlay_source = keyed_presentation_overlay(P3.OVERLAY_SOURCE)
        adapter_path = out / "t0-keyed-presentation-overlay.py"
        adapter_path.write_text(overlay_source, encoding="utf-8")
        overlay_sha256 = hashlib.sha256(overlay_source.encode("utf-8")).hexdigest()
        exec(compile(overlay_source, str(adapter_path), "exec"), overlay.__dict__)
        import packages.derivation.presentation_projection as projection
        import packages.derivation.live as live
        import packages.derivation.live_session as live_session
        overlay.install(projection, live, live_session)
        case_summaries = []
        for case_id in args.case:
            case_acts, mutation = ceiling_collision_acts(acts, case_id)
            case_resolution = resolve_production_package(case_acts,
                run_scope=P2.RUN_SCOPE, scope_user=P2.SCOPE_USER,
                workspace_revision=len(case_acts), surface=surface, schemas=DerivationSchemas())
            case_dir = out / "cases" / case_id
            case_dir.mkdir(parents=True, exist_ok=False)
            case_summary: dict[str, Any] = {"caseId": case_id, "suppliedMutation": mutation,
                "suppliedActs": str((case_dir / "synthetic-seed-acts.json").relative_to(ROOT))}
            if isinstance(case_resolution, Refusal):
                case_summary.update({"packageValidation": "refused", "reason": case_resolution.reason,
                    "detail": case_resolution.detail, "issues": list(case_resolution.issues)})
                write(case_dir / "package-validation.json", case_summary)
                case_summaries.append(case_summary)
                continue
            case_summary["packageValidation"] = "resolved"
            case_summary["resolvedRuleCount"] = len(case_resolution.resolved_members)
            # _live_case's positive-baseline branch is a no-op apart from the
            # established fixture invariants/revision checks. The supplied acts
            # above are changed before it enters the real coordinator.
            live_case = P2._live_case("positive-baseline", case_acts, surface, case_dir)
            live_case["harnessBranch"] = live_case.get("case")
            live_case["case"] = case_id
            report_path = case_dir / "coordinator-report.json"
            model_path = case_dir / "presentation-model.json"
            records_path = case_dir / "synthetic-records.json"
            if report_path.exists():
                report = read(report_path)
                live_case["runId"] = report.get("run_id")
                target_ids = {P2.LINE8A_RULE_ID, "tax.us.2025.rule.schedule-a-total",
                              "tax.us.2025.rule.form1040-line12e"}
                live_case["consumerOutcomes"] = [{"artifact": item.get("artifact_id"),
                    "symbol": item.get("symbol"), "disposition": item.get("disposition"),
                    "blocked": item.get("blocked"), "missing": item.get("missing"),
                    "finding_id": item.get("finding_id"), "pins": item.get("pins", [])}
                    for item in report.get("dispositions", []) if item.get("artifact_id") in target_ids]
            if model_path.exists():
                model = read(model_path)
                explanation = model.get("mortgageInterestExplanation", {})
                live_case["selectedAccountSupport"] = explanation.get("sharedSupport", [])
                live_case["line12eProjection"] = [{"disposition": section.get("resolved", {}).get("disposition"),
                    "value": section.get("resolved", {}).get("value"),
                    "pins": (section.get("resolved", {}).get("act", {}).get("finding", {}).get("pins", []))}
                    for section in model.get("sections", [])
                    if "line-12e-src-0" in str(section.get("citationSites", []))]
            live_case["durableConsumerHashes"] = {
                name: hashlib.sha256(path.read_bytes()).hexdigest()
                for name, path in (("coordinator-report.json", report_path),
                    ("presentation-model.json", model_path), ("synthetic-records.json", records_path))
                if path.exists()}
            case_summary["coordinatorCase"] = live_case
            case_summaries.append(case_summary)
        summary.update({"outcome": "resolved", "candidatePackage": T0_PACKAGE_VERSION,
            "presentationAdapter": {"path": str(adapter_path.relative_to(ROOT)), "sha256": overlay_sha256},
            "cases": case_summaries, "stage": "bounded-ceiling-collision-coordinator-cases"})
        write(out / "declaration-check.json", summary)
        print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
