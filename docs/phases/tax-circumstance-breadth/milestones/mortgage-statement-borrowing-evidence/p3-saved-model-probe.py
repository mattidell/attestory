"""Bounded P3 saved-model prototype over retained P2 content and fixtures."""
from __future__ import annotations

import copy
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

from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.records import RecordStream
from packages.kernel.act_log import ActLog
from packages.tax.loader import tax_registry


def _load_sibling(filename: str, module_name: str) -> Any:
    path = Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


P0 = _load_sibling("p0-current-path-probe.py", "p3_p0_fixtures")
P2 = _load_sibling("p2-option-a-probe.py", "p3_p2_candidate")

P2_RETAINED = ROOT / "temp/mortgage-statement-borrowing/p2-bridge-20261022T080544Z"
P2_CONTENT = P2_RETAINED / "candidate-content"
P2_SEED = P2_RETAINED / "synthetic-seed-acts.json"
ACCOUNT_FACTS = {
    "recognition": "demo.tax.2025.mortgage.continuing-borrowing",
    "membership": "demo.tax.2025.mortgage.report-membership",
    "ceiling": "demo.tax.2025.mortgage.annual-ceiling",
    "other-debt": "demo.tax.2025.mortgage.other-home-secured-debt",
}
LINK_STATUS = "demo.tax.2025.f1098.report-link-status"
BOX2_STATUS = "demo.tax.2025.f1098.principal-within-ceiling"
BOX3_BRIDGE = "demo.tax.2025.f1098.reported-box3-origination-date"
READINESS = "demo.tax.2025.mortgage.same-borrowing-ready"
LINE8A = "tax.us.2025.schedule-a.line8a"
LINE8A_RULE = "tax.us.2025.rule.f1098-line8a"
REASON = "tax.us.2025.f1098.residence-interest-reason"
BOX1 = "tax.us.2025.f1098.box1-mortgage-interest"
BOX2 = "tax.us.2025.f1098.box2-outstanding-principal"
BOX3 = "tax.us.2025.f1098.box3-origination-date"


OVERLAY_SOURCE = r'''"""P3 only: isolated group presentation overlay loaded by the probe."""
from __future__ import annotations
import copy
from collections.abc import Mapping, Sequence
from typing import Any


def install(projection: Any, live: Any, live_session: Any) -> dict[str, Any]:
    base_build = live.build_presentation_model
    base_validate = projection.validate_presentation_model
    base_mortgage = projection._mortgage_interest_explanation
    base_mortgage_validate = projection._validate_mortgage_interest_explanation
    ctx: dict[str, Any] = {}

    def validate_group(value: Any, model_run_id: str | None = None) -> None:
        p = "$.mortgageInterestExplanation"
        if not isinstance(value, Mapping) or value.get("schema") != "mortgage-interest-explanation.v2":
            base_mortgage_validate(value)
            return
        required = {"schema", "runId", "workspaceRevision", "accounts", "sharedSupport",
                    "readiness", "line8aDisposition", "limitReference"}
        if set(value) != required:
            raise projection.PresentationModelError(f"{p}: unexpected group-model fields")
        if value["runId"] != model_run_id or not isinstance(value["runId"], str):
            raise projection.PresentationModelError(f"{p}.runId: does not match saved run")
        if not isinstance(value["workspaceRevision"], int) or isinstance(value["workspaceRevision"], bool):
            raise projection.PresentationModelError(f"{p}.workspaceRevision: expected coordinator revision")
        accounts = value["accounts"]
        if not isinstance(accounts, list) or len(accounts) != 2:
            raise projection.PresentationModelError(f"{p}.accounts: expected exactly two reports")
        identities: set[tuple[str, str, str]] = set()
        for i, row in enumerate(accounts):
            path = f"{p}.accounts[{i}]"
            expected = {"statementKeys", "statementLabel", "reportedInterest", "reasonChain",
                        "membershipStatus", "box2Status", "box3Observation"}
            if not isinstance(row, Mapping) or set(row) != expected:
                raise projection.PresentationModelError(f"{path}: malformed report row")
            keys = row["statementKeys"]
            if not isinstance(keys, Mapping) or set(keys) != {"payer", "statement", "taxYear"}:
                raise projection.PresentationModelError(f"{path}.statementKeys: malformed source identity")
            ident = (keys["payer"], keys["statement"], keys["taxYear"])
            if not all(isinstance(item, str) and item for item in ident) or ident in identities:
                raise projection.PresentationModelError(f"{path}.statementKeys: duplicate or invalid identity")
            identities.add(ident)
            if keys["taxYear"] != "2025":
                raise projection.PresentationModelError(f"{path}.statementKeys: unexpected year")
            label = row["statementLabel"]
            if not isinstance(label, Mapping) or set(label) - {"lender", "statement", "taxYear"}:
                raise projection.PresentationModelError(f"{path}.statementLabel: malformed saved label")
            amount = row["reportedInterest"]
            if not isinstance(amount, Mapping) or set(amount) != {"value", "sourceFindingId", "sourceFactType", "title"}:
                raise projection.PresentationModelError(f"{path}.reportedInterest: malformed amount source")
            if (amount["sourceFactType"] != "tax.us.2025.f1098.box1-mortgage-interest"
                    or not isinstance(amount["value"], (int, float)) or isinstance(amount["value"], bool)
                    or not isinstance(amount["sourceFindingId"], str) or not amount["sourceFindingId"]):
                raise projection.PresentationModelError(f"{path}.reportedInterest: invalid raw source")
            for field in ("reasonChain", "membershipStatus", "box2Status", "box3Observation"):
                item = row[field]
                if not isinstance(item, Mapping) or not isinstance(item.get("rule"), Mapping):
                    raise projection.PresentationModelError(f"{path}.{field}: missing actual producer metadata")
                if not all(isinstance(item["rule"].get(k), str) and item["rule"][k] for k in ("id", "version")):
                    raise projection.PresentationModelError(f"{path}.{field}.rule: missing exact pin")
                if not isinstance(item.get("pins"), list):
                    raise projection.PresentationModelError(f"{path}.{field}.pins: expected actual pins")
                if field == "reasonChain":
                    if not all(isinstance(item.get(k), str) and item[k] for k in ("findingId", "value")):
                        raise projection.PresentationModelError(f"{path}.{field}: missing actual reason finding")
                elif item.get("disposition") is None and all(isinstance(item.get(k), str) and item[k]
                        for k in ("findingId", "value")):
                    pass  # compatible with the first positive-only prototype serialization
                elif item.get("disposition") == "published":
                    if not all(isinstance(item.get(k), str) and item[k] for k in ("findingId", "value")):
                        raise projection.PresentationModelError(f"{path}.{field}: published outcome lacks actual finding")
                elif item.get("disposition") not in {"blocked", "inapplicable"} or not isinstance(item.get("code"), str):
                    raise projection.PresentationModelError(f"{path}.{field}: expected a published or actual blocked disposition")
        if len(identities) != 2:
            raise projection.PresentationModelError(f"{p}.accounts: expected two unique reports")
        if not isinstance(value["sharedSupport"], list) or not value["sharedSupport"]:
            raise projection.PresentationModelError(f"{p}.sharedSupport: no actual shared findings")
        for i, item in enumerate(value["sharedSupport"]):
            if (not isinstance(item, Mapping) or not all(isinstance(item.get(k), str) and item[k]
                for k in ("findingId", "factType", "value")) or not isinstance(item.get("keys"), Mapping)):
                raise projection.PresentationModelError(f"{p}.sharedSupport[{i}]: malformed source finding")
        for field in ("readiness", "line8aDisposition"):
            if not isinstance(value[field], Mapping) or not value[field]:
                raise projection.PresentationModelError(f"{p}.{field}: missing actual coordinator outcome")
        limit = value["limitReference"]
        if (not isinstance(limit, Mapping) or not all(isinstance(limit.get(k), str) and limit[k]
                for k in ("id", "version", "filingStatus", "value", "note"))):
            raise projection.PresentationModelError(f"{p}.limitReference: missing exact limit content")

    def validate_model(model: Any) -> None:
        if isinstance(model, Mapping) and isinstance(model.get("mortgageInterestExplanation"), Mapping) \
                and model["mortgageInterestExplanation"].get("schema") == "mortgage-interest-explanation.v2":
            copy_without_group = dict(model)
            group = copy_without_group.pop("mortgageInterestExplanation")
            base_validate(copy_without_group)
            validate_group(group, model.get("runId"))
        else:
            base_validate(model)

    def fact_key(state: Any, finding: Mapping[str, Any]) -> dict[str, str]:
        from packages.kernel.facts import facts_of
        fact = facts_of(state.fact_state).get(str(finding.get("fact_id")))
        return dict(fact.keys) if fact is not None else {}

    def pub_rows(publications: Sequence[Any]) -> list[Mapping[str, Any]]:
        return [p.finding for p in publications if isinstance(getattr(p, "finding", None), Mapping)]

    def find_pub(publications: Sequence[Any], symbol: str, rule_id: str, keys: Mapping[str, str]):
        from packages.kernel.facts import facts_of
        matches = []
        for finding in pub_rows(publications):
            got = finding.get("symbol", "")
            if not isinstance(got, str) or not got.startswith(symbol + "|"):
                continue
            _basis, pin = projection._exact_rule_basis(finding,
                resolved_members=ctx["resolved_members"], expected_rule_id=rule_id)
            rule = next((m for m in ctx["resolved_members"]
                         if m.get("id") == pin["id"] and m.get("version") == pin["version"]), None)
            subject = rule.get("subject", {}) if isinstance(rule, Mapping) else {}
            subject_id = subject.get("id") if isinstance(subject, Mapping) else None
            matched_subjects = []
            for source_pin in finding.get("pins", []) or []:
                if not isinstance(source_pin, Mapping) or source_pin.get("role") != "input":
                    continue
                source = ctx["state"].findings.get(str(source_pin.get("id")))
                fact = facts_of(ctx["state"].fact_state).get(str(source.get("fact_id"))) if source else None
                if fact is not None and fact.fact_type_id == subject_id:
                    matched_subjects.append(dict(fact.keys))
            if len(matched_subjects) == 1 and all(matched_subjects[0].get(k) == v for k, v in keys.items()):
                matches.append(finding)
        if len(matches) > 1:
            raise projection.PresentationModelError(f"ambiguous P3 join for {symbol!r}")
        return matches[0] if matches else None

    def actual_result(finding: Mapping[str, Any], resolved_members: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
        basis, rule_pin = projection._exact_rule_basis(finding, resolved_members=resolved_members)
        return {"findingId": finding["id"], "value": str(finding.get("value")),
                "rule": {"id": rule_pin["id"], "version": rule_pin["version"]},
                "pins": list(finding.get("pins", []) or []),
                **({"basis": {k: list(v) for k, v in basis.items()}} if basis is not None else {})}

    def source_finding(state: Any, fact_type: str, keys: Mapping[str, str]) -> Mapping[str, Any] | None:
        from packages.kernel.currency import compute_currency
        from packages.kernel.facts import facts_of
        current = compute_currency(state).current_finding_ids
        fact_map = facts_of(state.fact_state)
        matches = [f for fid, f in state.findings.items() if fid in current
                   and fact_map.get(str(f.get("fact_id"))) is not None
                   and fact_map[str(f["fact_id"])].fact_type_id == fact_type
                   and dict(fact_map[str(f["fact_id"])].keys) == dict(keys)]
        if len(matches) > 1:
            raise projection.PresentationModelError(f"ambiguous current source {fact_type!r}")
        return matches[0] if matches else None

    def raw_source(state: Any, fact_type: str, keys: Mapping[str, str]) -> dict[str, Any] | None:
        from packages.kernel.facts import facts_of
        finding = source_finding(state, fact_type, keys)
        if finding is None:
            return None
        fact = facts_of(state.fact_state)[str(finding["fact_id"])]
        return {"findingId": finding["id"], "value": str(finding.get("value")),
                "factType": fact.fact_type_id, "keys": dict(fact.keys),
                "evidenceIds": list(finding.get("evidence_ids", []) or [])}

    def rule_row(finding: Mapping[str, Any], resolved_members: Sequence[Mapping[str, Any]], expected_id: str | None = None) -> dict[str, Any]:
        _basis, pin = projection._exact_rule_basis(finding, resolved_members=resolved_members,
                                                   expected_rule_id=expected_id)
        return {"disposition": "published", "findingId": finding["id"], "value": str(finding.get("value")),
                "rule": {"id": pin["id"], "version": pin["version"]},
                "pins": list(finding.get("pins", []) or [])}

    def outcome_row(publications: Sequence[Any], symbol: str, rule_id: str,
                    keys: Mapping[str, str], resolved_members: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
        finding = find_pub(publications, symbol, rule_id, keys)
        if finding is not None:
            return rule_row(finding, resolved_members, rule_id)
        rule = next((m for m in resolved_members if m.get("id") == rule_id and "publishes" in m), None)
        if rule is None:
            raise projection.PresentationModelError(f"P3 status rule {rule_id!r} is not resolved")
        subject_id = rule.get("subject", {}).get("id") if isinstance(rule.get("subject"), Mapping) else None
        from packages.kernel.facts import facts_of
        fact_map = facts_of(ctx["state"].fact_state)
        matches = []
        for row in ctx["dispositions"]:
            if row.get("artifact_id") != rule_id or row.get("disposition") == "published":
                continue
            subject_keys = []
            for pin in row.get("pins", []) or []:
                source = ctx["state"].findings.get(str(pin.get("id"))) if isinstance(pin, Mapping) else None
                fact = fact_map.get(str(source.get("fact_id"))) if source else None
                if fact is not None and fact.fact_type_id == subject_id:
                    subject_keys.append(dict(fact.keys))
            if len(subject_keys) == 1 and all(subject_keys[0].get(k) == v for k, v in keys.items()):
                matches.append(row)
        if len(matches) != 1:
            raise projection.PresentationModelError(
                f"P3 expected one exact published/blocked result for {rule_id!r}; found {len(matches)}")
        row = matches[0]
        result = {"disposition": row["disposition"], "rule": {"id": rule_id, "version": rule["version"]},
                  "pins": list(row.get("pins", []) or [])}
        for key in ("code", "missing"):
            if key in row:
                result[key] = row[key]
        return result

    def group_explanation(*, resolved_members: Sequence[Mapping[str, Any]], state: Any,
                          publications: Sequence[Any], publications_by_id: Mapping[str, Mapping[str, Any]]):
        reason_pubs = [f for f in pub_rows(publications)
                       if str(f.get("symbol", "")).startswith(projection._MORTGAGE_REASON_SYMBOL + "|")]
        if len(reason_pubs) < 2:
            return base_mortgage(resolved_members=resolved_members, state=state,
                                 publications=publications, publications_by_id=publications_by_id)
        if len(reason_pubs) != 2:
            raise projection.PresentationModelError("P3 overlay is bounded to exactly two statement reasons")
        from packages.kernel.facts import facts_of
        fact_map = facts_of(state.fact_state)
        resolved_rules = { (m.get("id"), m.get("version")): m for m in resolved_members if "publishes" in m }
        def report_identity(finding: Mapping[str, Any]) -> tuple[str, str, str]:
            box1_ids = [p.get("id") for p in finding.get("pins", []) or []
                        if isinstance(p, Mapping) and p.get("role") == "input"
                        and p.get("id") in state.findings
                        and (fact := fact_map.get(str(state.findings[p["id"]].get("fact_id")))) is not None
                        and fact.fact_type_id == projection._MORTGAGE_BOX1_FACT_TYPE]
            if len(box1_ids) != 1:
                raise projection.PresentationModelError("P3 reason must pin one report Box 1 source")
            keys = dict(fact_map[str(state.findings[box1_ids[0]]["fact_id"])].keys)
            return tuple(str(keys[k]) for k in ("payer", "statement", "tax-year"))

        reason_pubs.sort(key=report_identity)
        accounts = []
        for reason_finding in reason_pubs:
            identity = {"payer": report_identity(reason_finding)[0],
                        "statement": report_identity(reason_finding)[1],
                        "tax-year": report_identity(reason_finding)[2]}
            report_keys = {k: str(identity[k]) for k in ("payer", "statement", "tax-year")}
            if set(identity) < {"payer", "statement", "tax-year"}:
                raise projection.PresentationModelError("P3 reason identity is not an exact F1098 report")
            reason_basis, reason_pin = projection._exact_rule_basis(
                reason_finding, resolved_members=resolved_members,
                expected_rule_id=projection._MORTGAGE_REASON_RULE_ID)
            reason_rule = resolved_rules.get((reason_pin["id"], reason_pin["version"]))
            if reason_rule is None:
                raise projection.PresentationModelError("P3 reason rule pin is not resolved")
            # P2's selected reason rule references bridge output fact types;
            # those bridge producers in turn name their exact raw input type
            # in `joined`. Add only those lineage-pinned raw refs to a local
            # metadata copy so the existing provenance walker can label leaves.
            # No producer, rule evaluation, publication, or global validator is changed.
            answer_rule_for_labels = copy.deepcopy(reason_rule)
            pending_ids = [p.get("id") for p in reason_finding.get("pins", []) or []
                           if isinstance(p, Mapping) and p.get("role") in {"input", "dependency"}]
            visited_ids: set[str] = set()
            raw_refs: set[tuple[str, str]] = set()
            while pending_ids:
                child_id = str(pending_ids.pop())
                if child_id in visited_ids:
                    continue
                visited_ids.add(child_id)
                publication = publications_by_id.get(child_id)
                if publication is None:
                    continue
                pending_ids.extend(str(p.get("id")) for p in publication.get("pins", []) or []
                                   if isinstance(p, Mapping) and p.get("role") in {"input", "dependency"}
                                   and isinstance(p.get("id"), str))
                symbol = str(publication.get("symbol", ""))
                if not symbol.startswith("demo.tax.2025.f1098.answer-status."):
                    continue
                _basis, bridge_pin = projection._exact_rule_basis(publication,
                    resolved_members=resolved_members)
                bridge_rule = resolved_rules.get((bridge_pin["id"], bridge_pin["version"]))
                joined = bridge_rule.get("joined") if isinstance(bridge_rule, Mapping) else None
                subject = bridge_rule.get("subject") if isinstance(bridge_rule, Mapping) else None
                if (not isinstance(joined, Mapping) or not isinstance(joined.get("id"), str)
                        or not isinstance(joined.get("version"), str)
                        or not isinstance(subject, Mapping)
                        or subject.get("id") != projection._MORTGAGE_BOX1_FACT_TYPE):
                    raise projection.PresentationModelError("lineage bridge lacks exact joined type or report subject")
                raw_refs.add((joined["id"], joined["version"]))
            for raw_id, raw_version in sorted(raw_refs):
                answer_rule_for_labels["value"] = {
                    "op": "metadata_refs", "original": answer_rule_for_labels["value"],
                    "rawSourceType": {"op": "category_literal",
                        "fact_type": {"id": raw_id, "version": raw_version}, "value": "metadata-only"}}
            answer_chains = projection._mortgage_basis_answers(
                reason_finding, publications_by_id=publications_by_id, state=state, fact_map=fact_map,
                resolved_members=resolved_members, reason_rule=answer_rule_for_labels)
            box1_pins = [p for p in reason_finding.get("pins", []) or []
                         if isinstance(p, Mapping) and p.get("role") == "input"
                         and p.get("id") in state.findings
                         and fact_map.get(str(state.findings[p["id"]].get("fact_id"))) is not None
                         and fact_map[str(state.findings[p["id"]].get("fact_id"))].fact_type_id == "tax.us.2025.f1098.box1-mortgage-interest"]
            if len(box1_pins) != 1:
                raise projection.PresentationModelError("P3 reason must pin one exact report Box 1 finding")
            box1 = state.findings[box1_pins[0]["id"]]
            box1_fact = fact_map[str(box1["fact_id"])]
            if dict(box1_fact.keys) != report_keys:
                raise projection.PresentationModelError("P3 Box 1 finding does not match its report reason")
            reason_value = str(reason_finding.get("value"))
            def mappings(value: Any) -> list[Mapping[str, Any]]:
                rows: list[Mapping[str, Any]] = []
                if isinstance(value, Mapping):
                    rows.append(value)
                    for nested in value.values():
                        rows.extend(mappings(nested))
                elif isinstance(value, list):
                    for nested in value:
                        rows.extend(mappings(nested))
                return rows
            reason_type_refs = {(node["fact_type"].get("id"), node["fact_type"].get("version"))
                for node in mappings(reason_rule.get("value"))
                if node.get("op") == "category_literal" and isinstance(node.get("fact_type"), Mapping)
                and node["fact_type"].get("id") == projection._MORTGAGE_REASON_SYMBOL}
            if len(reason_type_refs) != 1:
                raise projection.PresentationModelError("pinned reason rule lacks one exact reason type ref")
            reason_type_id, reason_type_version = next(iter(reason_type_refs))
            reason_type_entries = [ft for m in resolved_members for ft in
                ([m] if str(m.get("schema", "")).startswith("fact-type.") else
                 [x for x in m.get("fact_types", []) if isinstance(x, Mapping)]
                 if str(m.get("schema", "")).startswith("bundle.") else [])
                if ft.get("id") == reason_type_id and ft.get("version") == reason_type_version]
            if len(reason_type_entries) != 1:
                raise projection.PresentationModelError("pinned reason type version is not uniquely resolved")
            reason_schema = reason_type_entries[0].get("value_schema", {})
            reason_choices = reason_schema.get("oneOf", []) if isinstance(reason_schema, Mapping) else []
            description = next((item.get("description") for item in reason_choices
                                if isinstance(item, Mapping) and item.get("const") == reason_value
                                and isinstance(item.get("description"), str)), None)
            if not description:
                raise projection.PresentationModelError("P3 reason value lacks description in pinned type version")
            link = outcome_row(publications, "demo.tax.2025.mortgage.report-link-status",
                "demo.rule.tax.2025.f1098-report-local-bridge.report-link-status", identity, resolved_members)
            principal = outcome_row(publications, "demo.tax.2025.f1098.principal-within-ceiling",
                "demo.rule.tax.2025.f1098-report-local-bridge.principal-ceiling-status", identity, resolved_members)
            box3 = outcome_row(publications, "demo.tax.2025.f1098.reported-box3-origination-date",
                "demo.rule.tax.2025.f1098-report-local-bridge.box3-origination-date", report_keys, resolved_members)
            accounts.append({
                "statementKeys": {"payer": report_keys["payer"], "statement": report_keys["statement"], "taxYear": report_keys["tax-year"]},
                "statementLabel": projection._statement_label(identity, state),
                "reportedInterest": {"value": projection._numeric_value(box1.get("value"), symbol=projection._MORTGAGE_BOX1_FACT_TYPE),
                    "sourceFindingId": box1_pins[0]["id"], "sourceFactType": projection._MORTGAGE_BOX1_FACT_TYPE,
                    "title": state.fact_state.fact_types[projection._MORTGAGE_BOX1_FACT_TYPE]["title"]},
                "reasonChain": {"disposition": "published", "findingId": reason_finding["id"], "value": reason_value,
                    "description": description, "rule": {"id": reason_pin["id"], "version": reason_pin["version"]},
                    "pins": list(reason_finding.get("pins", []) or []), "sourceDocuments": answer_chains["sourceDocuments"],
                    "personAnswers": answer_chains["personAnswers"], "declaredDefaults": answer_chains["declaredDefaults"],
                    **({"basis": {k: list(v) for k, v in reason_basis.items()}} if reason_basis is not None else {})},
                "membershipStatus": link,
                "box2Status": principal,
                "box3Observation": box3,
            })
        # Actual shared account findings are raw current assertions, not display-derived conclusions.
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
        pubs = pub_rows(publications)
        readiness = [f for f in pubs if str(f.get("symbol", "")).startswith("demo.tax.2025.mortgage.same-borrowing-ready")]
        readiness_rule_id = "demo.tax.2025.rule.mortgage-borrowing-readiness"
        if len(readiness) == 1:
            ready_row = rule_row(readiness[0], resolved_members, readiness_rule_id)
        else:
            blocked_readiness = [r for r in ctx["dispositions"]
                                 if r.get("artifact_id") == readiness_rule_id and r.get("disposition") != "published"]
            if len(readiness) or len(blocked_readiness) != 1:
                raise projection.PresentationModelError("P3 expected one actual readiness publication or disposition")
            readiness_rule = next((m for m in resolved_members if m.get("id") == readiness_rule_id), None)
            if readiness_rule is None:
                raise projection.PresentationModelError("P3 readiness rule is not resolved")
            ready_row = {"disposition": blocked_readiness[0]["disposition"],
                "rule": {"id": readiness_rule_id, "version": readiness_rule["version"]},
                "pins": list(blocked_readiness[0].get("pins", []) or [])}
            for key in ("code", "missing"):
                if key in blocked_readiness[0]:
                    ready_row[key] = blocked_readiness[0][key]
        line_rows = [r for r in ctx["dispositions"] if r.get("artifact_id") == "tax.us.2025.rule.f1098-line8a"]
        if len(line_rows) != 1:
            raise projection.PresentationModelError("P3 expected exactly one actual line8a disposition")
        amount_pubs = [f for f in pubs if f.get("symbol") == "tax.us.2025.schedule-a.line8a"]
        if len(amount_pubs) > 1:
            raise projection.PresentationModelError("P3 received ambiguous line8a publications")
        if amount_pubs:
            line_rows[0] = dict(line_rows[0], publication={"findingId": amount_pubs[0]["id"],
                "value": str(amount_pubs[0].get("value")), "pins": list(amount_pubs[0].get("pins", []) or [])})
        limit_members = [m for m in resolved_members if m.get("id") == "tax.us.2025.f1098.mortgage-interest-limit"
                         and m.get("version") == "v1"]
        if len(limit_members) != 1:
            raise projection.PresentationModelError("P3 limit parameter is not uniquely resolved")
        status_findings = []
        for finding_id in current:
            f = state.findings.get(finding_id)
            ft = fact_map.get(str(f.get("fact_id"))) if f else None
            if ft is not None and ft.fact_type_id == "tax.us.2025.filing-status":
                status_findings.append(f)
        if len(status_findings) != 1:
            raise projection.PresentationModelError("P3 expected one actual filing status source")
        filing_status = str(status_findings[0].get("value"))
        param = limit_members[0]
        param_values = param.get("values", {})
        if filing_status not in param_values:
            raise projection.PresentationModelError("P3 selected filing status has no declared limit")
        return {"schema": "mortgage-interest-explanation.v2", "runId": ctx["run_id"],
            "workspaceRevision": ctx["workspace_revision"], "accounts": accounts,
            "sharedSupport": shared_support, "readiness": ready_row,
            "line8aDisposition": line_rows[0],
            "limitReference": {"id": param["id"], "version": param["version"],
                "filingStatus": filing_status, "value": str(param_values[filing_status]),
                "note": "This run uses this declared conservative debt-limit parameter; the candidate contains no higher pre-2017 limit branch."}}

    def build_with_context(**kwargs: Any) -> dict[str, Any]:
        ctx.update({"run_id": kwargs["run_id"], "workspace_revision": kwargs.get("workspace_revision"),
                    "dispositions": kwargs["dispositions"], "state": kwargs["state"],
                    "resolved_members": kwargs["resolved_members"]})
        try:
            return base_build(**kwargs)
        finally:
            ctx.clear()

    projection._mortgage_interest_explanation = group_explanation
    projection._validate_mortgage_interest_explanation = validate_group
    projection.validate_presentation_model = validate_model
    live.build_presentation_model = build_with_context
    live_session.validate_presentation_model = validate_model
    return {"baseBuild": base_build, "baseValidate": base_validate,
            "baseMortgage": base_mortgage, "baseMortgageValidate": base_mortgage_validate,
            "context": ctx, "groupBuilder": group_explanation, "groupValidator": validate_group}
'''


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _copy_p2_surface(output_dir: Path) -> PublicationSurface:
    if not P2_CONTENT.is_dir() or not P2_SEED.is_file():
        raise RuntimeError(f"retained P2 evidence is missing: {P2_RETAINED.relative_to(ROOT)}")
    members = output_dir / "candidate-members"
    releases = output_dir / "candidate-releases"
    shutil.copytree(P2.CONTENT, members)
    releases.mkdir()
    for path in P2_CONTENT.iterdir():
        if path.is_file():
            shutil.copy2(path, members / path.name)
            if path.name.startswith("demo.release."):
                shutil.copy2(path, releases / path.name)
    registry = members / "published-packages.p48-p2.json"
    if not registry.is_file() or not list(releases.iterdir()):
        raise RuntimeError("retained P2 package registry or release is missing")
    return PublicationSurface(releases, registry, members)


def _run_case(name: str, seed: list[dict[str, Any]], surface: PublicationSurface,
              out_dir: Path, *, run_id: str, overlay_sha256: str,
              render_page: Any, repo_root: Path) -> dict[str, Any]:
    case_dir = out_dir / "cases" / name
    case_dir.mkdir(parents=True, exist_ok=False)
    _write_json(case_dir / "synthetic-seed-acts.json", seed)
    with TemporaryDirectory(prefix=f"demo-f1098-p3-{name}-") as workspace_temp:
        capability = WorkspaceCapability(Path(workspace_temp) / "workspace")
        log = ActLog(capability.location, tax_registry())
        log.append_batch(seed, expected_revision=0)
        content = log.read()
        outcome = P2.live_coordinate_run(
            capability, repo_root=repo_root, authoritative_acts=content.acts,
            workspace_revision=content.revision, run_scope=P2.RUN_SCOPE, scope_user=P2.SCOPE_USER,
            request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[], surface=surface,
            output_name=f"{name}.json", schemas=DerivationSchemas(),
        )
        if outcome.refusal is not None:
            summary = {"case": name, "outcome": "refused", "refusal": {
                "reason": outcome.refusal.reason, "detail": outcome.refusal.detail}}
            _write_json(case_dir / "summary.json", summary)
            return summary
        if outcome.output_path is None or outcome.presentation_path is None:
            raise RuntimeError(f"{name}: coordinator returned no durable output/model")
        shutil.copy2(outcome.output_path, case_dir / "coordinator-report.json")
        shutil.copy2(outcome.presentation_path, case_dir / "presentation-model.json")
        model = json.loads((case_dir / "presentation-model.json").read_text("utf-8"))
        from packages.derivation.live_session import _render_page
        rendered = _render_page(repo_root, capability, outcome.presentation_path)
        (case_dir / "rendered.html").write_bytes(rendered)
        records = RecordStream(capability.location / "records", DerivationSchemas()).read()
        _write_json(case_dir / "synthetic-records.json", records.records)
        from packages.tax.f1098_statement_review import associate_saved_run
        association = associate_saved_run(model, RecordStream(capability.location / "records", DerivationSchemas()),
                                           content.revision)
        line = [d for d in json.loads((case_dir / "coordinator-report.json").read_text("utf-8")).get("dispositions", [])
                if d.get("artifact_id") == LINE8A_RULE]
        explanation = model.get("mortgageInterestExplanation")
        summary = {"case": name, "outcome": "completed", "runId": model.get("runId"),
            "workspaceRevision": explanation.get("workspaceRevision") if isinstance(explanation, dict) else content.revision,
            "line8aDispositions": line, "modelSchema": explanation.get("schema") if isinstance(explanation, dict) else None,
            "reportCount": len(explanation.get("accounts", [])) if isinstance(explanation, dict) else 0,
            "renderedBytes": len(rendered), "htmlSerializedFromReloadedModel": True,
            "overlaySha256": overlay_sha256,
            "savedRunAssociation": association,
            "modelFile": "presentation-model.json", "coordinatorReport": "coordinator-report.json",
            "syntheticRecords": "synthetic-records.json"}
        _write_json(case_dir / "summary.json", summary)
        return summary


def run_probe(*, positive_only: bool = False, remaining_only: bool = False,
              empty_control_only: bool = False) -> dict[str, Any]:
    if not (ROOT / ".gitignore").is_file():
        raise RuntimeError("repository root is not the expected project")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = ROOT / "temp/mortgage-statement-borrowing" / f"p3-saved-model-{stamp}"
    out_dir.mkdir(parents=True, exist_ok=False)
    overlay_path = out_dir / "p3-presentation-overlay.py"
    overlay_path.write_text(OVERLAY_SOURCE, encoding="utf-8")
    overlay_sha256 = hashlib.sha256(overlay_path.read_bytes()).hexdigest()
    overlay_spec = importlib.util.spec_from_file_location("p3_presentation_overlay", overlay_path)
    if overlay_spec is None or overlay_spec.loader is None:
        raise RuntimeError("could not load the generated presentation overlay")
    overlay = importlib.util.module_from_spec(overlay_spec)
    overlay_spec.loader.exec_module(overlay)
    import packages.derivation.presentation_projection as projection
    import packages.derivation.live as live
    import packages.derivation.live_session as live_session
    original = overlay.install(projection, live, live_session)

    # The overlay targets only the internal mortgage presentation adapter and
    # its strict model validator. Coordinator, resolver, runners and tax content
    # remain the imported production implementations.
    surface = _copy_p2_surface(out_dir)
    seed = json.loads(P2_SEED.read_text("utf-8"))
    _write_json(out_dir / "retained-p2-seed-acts.json", seed)
    cases = ["positive-baseline", "b-contrary-payment", "b-membership-missing",
             "principal-contradicts-ceiling", "loose-upper-bound", "origination-disagreement"]
    p2_summaries = []
    selected_cases = (cases[:1] if positive_only else [] if empty_control_only
                      else cases[1:] if remaining_only else cases)
    for case in selected_cases:
        p2_summaries.append(_run_case(case, P2._case_acts(seed, case), surface, out_dir,
            run_id=f"demo.mortgage.p3.{case}.p51-v1", overlay_sha256=overlay_sha256,
            render_page=None, repo_root=ROOT))

    # Compatibility controls use the actual adopted v49/v47 graph. They prove
    # adapter compatibility for closed-empty and singleton only; they do not
    # make P2's inert no-activity selector a production route.
    # Same source construction as P0's _latest_acts, with no Form 1098 report.
    empty_acts = P0._make_base_acts()
    empty_acts.extend(P0._f1098_rows(P0.mortgage_fixture_acts(None)))
    registry = P0.tax_registry()
    empty_acts.append({"schema": "act.v1", "act_id": "demo.f1098.p3.closed-empty-vocabulary",
        "kind": "bundle-adoption", "actor": "demo.taxpayer", "at": "2026-10-22T12:00:00Z",
        "committed_against": len(empty_acts),
        "payload": {"bundle": P0.load_f1098_circumstances_bundle(registry, version="v2")}})
    empty_acts = P0._finish_acts_v49(empty_acts)
    singleton_acts = P0._latest_acts(fixture_answers=True)
    controls = [] if positive_only else [
        _run_case("v49-closed-empty-control", empty_acts, P0.SURFACE, out_dir,
            run_id="demo.mortgage.p3.v49-closed-empty", overlay_sha256=overlay_sha256,
            render_page=None, repo_root=ROOT),
    ] if empty_control_only else [
        _run_case("v49-closed-empty-control", empty_acts, P0.SURFACE, out_dir,
            run_id="demo.mortgage.p3.v49-closed-empty", overlay_sha256=overlay_sha256,
            render_page=None, repo_root=ROOT),
        _run_case("v49-singleton-control", singleton_acts, P0.SURFACE, out_dir,
            run_id="demo.mortgage.p3.v49-singleton", overlay_sha256=overlay_sha256,
            render_page=None, repo_root=ROOT),
    ]
    result = {"stage": "bounded-group-saved-model-probe", "output_directory": str(out_dir.relative_to(ROOT)),
        "overlay_file": str(overlay_path.relative_to(ROOT)),
        "overlay_method": "Generated overlay module loaded by importlib in a dedicated probe process; monkeypatches only live.build_presentation_model and the presentation module's mortgage explanation/strict validator, plus live_session's validator for saved reload/render. The process exits after the probe; no production source is edited.",
        "unchanged_production_path": ["production package resolver", "marshal", "dispatch/evaluation", "live_coordinate_run", "record stream", "coordinator report writing"],
        "positive_only_checkpoint": positive_only, "remaining_only_checkpoint": remaining_only,
        "empty_control_only_checkpoint": empty_control_only, "overlay_sha256": overlay_sha256,
        "p2_cases": p2_summaries, "v49_controls": controls,
        "limitations": ["P2 input assertions and fixture borrowing key remain synthetic and manually supplied.",
            "No recorder, source/membership/account correction lifecycle, or production route selection is demonstrated.",
            "v49 controls show presentation overlay compatibility only; P2's inert selector does not demonstrate no-activity route selection.",
            "Box 3 mismatch is shown as two raw report observations beside the actual coordinator block; no conflict-specific conclusion is added."],
        "restore_functions": sorted(original.keys())}
    _write_json(out_dir / "probe-summary.json", result)
    return result


if __name__ == "__main__":
    print(json.dumps(run_probe(positive_only="--positive-only" in sys.argv[1:],
                               remaining_only="--remaining-only" in sys.argv[1:],
                               empty_control_only="--empty-control-only" in sys.argv[1:]), indent=2, sort_keys=True))
