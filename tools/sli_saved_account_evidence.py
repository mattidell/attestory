"""Experimental saved evidence for synthetic student-loan account runs.

This format is local milestone research data, not a published schema, tax result,
or production recording API. It stores coordinator output as returned and joins
only recorded finding IDs and structured fact keys.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from typing import Any, cast


FORMAT = "sli-saved-account-evidence.v1"


class SavedEvidenceError(ValueError):
    """The saved account evidence is malformed or cannot support its claims."""


def _json_copy(value: Any, label: str) -> Any:
    try:
        return json.loads(json.dumps(value, sort_keys=True, separators=(",", ":")))
    except (TypeError, ValueError) as exc:
        raise SavedEvidenceError(f"{label} is not JSON data") from exc


def _owner_identity(owner_type: str, owner_id: str, owner: Mapping[str, Any]) -> dict[str, Any]:
    identity: dict[str, Any] = {"type": owner_type, "id": owner_id}
    for key in ("artifact_id", "symbol", "subject", "act_id", "finding_id"):
        if key in owner:
            identity[key] = _json_copy(owner[key], f"owner {key}")
    if owner_type == "publication" and "id" in owner:
        identity["finding_id"] = owner["id"]
    return identity


def capture(
    *,
    run_id: str,
    package: Mapping[str, Any],
    publications: Sequence[Any],
    dispositions: Sequence[Mapping[str, Any]],
    current_findings: Mapping[str, Mapping[str, Any]],
    fact_keys: Mapping[str, Mapping[str, Any]],
    evidence_by_id: Mapping[str, Mapping[str, Any]],
    contextual_findings: Mapping[str, Mapping[str, Any]] | None = None,
    selected_producer_ids: Sequence[str] | None = None,
    all_findings: Mapping[str, Mapping[str, Any]] | None = None,
    displacement_reasons: Mapping[str, Sequence[Mapping[str, str]]] | None = None,
    lineage_acts: Sequence[Mapping[str, Any]] = (),
    experiment_metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Capture actual live output and its exact current input-pin support.

    ``publications`` are the coordinator's real Publication objects. Caller
    supplied maps must be derived from a freshly reopened act projection.
    Context records are labeled separately and never counted as evaluated
    dependencies.
    """
    if not run_id or not package.get("id") or not package.get("version"):
        raise SavedEvidenceError("run and package identity are required")
    rows: list[dict[str, Any]] = []
    pub_by_id: dict[str, dict[str, Any]] = {}
    adoption_refs: set[tuple[str, str]] = set()
    for publication in publications:
        finding = _json_copy(publication.finding, "publication finding")
        finding_id = finding.get("id")
        if not isinstance(finding_id, str) or finding_id in pub_by_id:
            raise SavedEvidenceError("publication finding IDs must be unique strings")
        act = _json_copy(publication.act, "publication act")
        if act.get("run_id") != run_id or act.get("finding") != finding:
            raise SavedEvidenceError("publication act does not match this run and finding")
        for pin in finding.get("pins", []):
            if pin.get("role") == "adoption":
                adoption_refs.add((pin.get("id", ""), pin.get("version", "")))
        row = {"finding": finding, "act": act}
        pub_by_id[finding_id] = row
        rows.append(row)

    disposition_rows = [_json_copy(row, "disposition") for row in dispositions]
    for row in disposition_rows:
        if row.get("run_id", run_id) != run_id:
            raise SavedEvidenceError("disposition belongs to a different run")
    if (package["id"], package["version"]) not in adoption_refs:
        raise SavedEvidenceError("package provenance is not corroborated by publication adoption pins")

    producer_ids = sorted(set(selected_producer_ids or []))
    selected_publications = sorted(
        row["finding"]["id"] for row in rows
        if producer_ids and any(pin.get("role") == "computation" and pin.get("id") in producer_ids
                                for pin in row["finding"].get("pins", []))
    )
    scoped_roots = set(selected_publications) if producer_ids else set(pub_by_id)
    scoped_dispositions = disposition_rows
    selected_reachable: set[str] = set()
    selection_queue = list(scoped_roots)
    while selection_queue:
        current_id = selection_queue.pop(0)
        if current_id in selected_reachable:
            continue
        selected_reachable.add(current_id)
        for pin in pub_by_id[current_id]["finding"].get("pins", []):
            target = pin.get("id")
            if pin.get("role") == "input" and target in pub_by_id and target not in selected_reachable:
                selection_queue.append(target)

    support_ids: set[str] = set()
    unresolved: list[dict[str, Any]] = []
    queue: list[tuple[str, str, dict[str, Any], list[dict[str, Any]]]] = [
        ("publication", row["finding"]["id"], row["finding"], row["finding"].get("pins", [])) for row in rows
    ]
    queue.extend(("disposition", str(row.get("artifact_id", "disposition")), row,
                  row.get("pins", [])) for row in scoped_dispositions)
    visited_publications: set[str] = set()
    while queue:
        owner_type, owner_id, owner, pins = queue.pop(0)
        for pin in pins:
            if pin.get("role") != "input":
                continue
            target = pin.get("id")
            if not isinstance(target, str):
                unresolved.append({"owner": _owner_identity(owner_type, owner_id, owner), "pin": pin})
            elif target in current_findings:
                support_ids.add(target)
            elif target in pub_by_id:
                if target not in visited_publications:
                    visited_publications.add(target)
                    child = pub_by_id[target]["finding"]
                    queue.append(("publication", target, child, child.get("pins", [])))
            else:
                unresolved.append({"owner": _owner_identity(owner_type, owner_id, owner), "pin": pin})

    # Blocked dependency references are recorded by the coordinator as fact-ID
    # strings, not as pins. Retain that actual refusal evidence separately;
    # never synthesize input pins for the missing records.
    recorded_blocked_dependencies = []
    for row in scoped_dispositions:
        if row.get("disposition") == "blocked":
            recorded_blocked_dependencies.append(_json_copy(row, "blocked disposition"))

    support: list[dict[str, Any]] = []
    for finding_id in sorted(support_ids):
        finding = _json_copy(current_findings[finding_id], "support finding")
        if finding.get("id") != finding_id:
            raise SavedEvidenceError("support map key does not match finding ID")
        fact_id = finding.get("fact_id")
        keys = fact_keys.get(fact_id) if isinstance(fact_id, str) else None
        if not isinstance(keys, Mapping):
            unresolved.append({"owner_type": "support-finding", "owner_id": finding_id,
                               "target": "structured-fact-identity"})
            keys = {}
        ev: list[dict[str, Any]] = []
        for evidence_id in finding.get("evidence_ids", []):
            record = evidence_by_id.get(evidence_id)
            if record is None:
                unresolved.append({"owner_type": "support-finding", "owner_id": finding_id,
                                   "target": evidence_id})
            else:
                ev.append(_json_copy(record, "evidence record"))
        support.append({"finding": finding, "fact": {"fact_id": fact_id,
                                                       "fact_type_id": keys.get("fact_type_id"),
                                                       "bindings": _json_copy(keys.get("bindings", {}), "fact keys"),
                                                       "individuated_by": _json_copy(keys.get("individuated_by", []), "fact individuality")},
                        "evidence": ev})

    context: list[dict[str, Any]] = []
    for finding_id, finding in sorted((contextual_findings or {}).items()):
        if finding_id in support_ids:
            continue
        fact_id = finding.get("fact_id")
        keys = fact_keys.get(fact_id, {}) if isinstance(fact_id, str) else {}
        context.append({"finding": _json_copy(finding, "context finding"),
                        "fact": {"fact_id": fact_id, "fact_type_id": keys.get("fact_type_id"),
                                 "bindings": _json_copy(keys.get("bindings", {}), "context fact keys"),
                                 "individuated_by": _json_copy(keys.get("individuated_by", []), "context individuality")}})

    lineage: list[dict[str, Any]] = []
    current_ids = set(current_findings)
    for finding_id, raw in sorted((all_findings or {}).items()):
        finding = _json_copy(raw, "lineage finding")
        fact_id = finding.get("fact_id")
        keys = fact_keys.get(fact_id) if isinstance(fact_id, str) else None
        if not isinstance(keys, Mapping):
            unresolved.append({"owner_type": "lineage-finding", "owner_id": finding_id,
                               "target": "structured-fact-identity"})
            keys = {}
        evidence = [evidence_by_id[item] for item in finding.get("evidence_ids", []) if item in evidence_by_id]
        lineage.append({"finding": finding,
                        "status": "current" if finding_id in current_ids else "displaced",
                        "displacement_reasons": _json_copy((displacement_reasons or {}).get(finding_id, []),
                                                            "displacement reasons"),
                        "fact": {"fact_id": fact_id, "fact_type_id": keys.get("fact_type_id"),
                                 "bindings": _json_copy(keys.get("bindings", {}), "lineage fact keys"),
                                 "individuated_by": _json_copy(keys.get("individuated_by", []), "lineage individuality")},
                        "evidence": _json_copy(evidence, "lineage evidence")})

    return {
        "format": FORMAT,
        "provenance": {"run_id": run_id, "package": {"id": package["id"], "version": package["version"]}},
        "scope": {"kind": "whole-run-with-explicit-account-selection" if producer_ids else "whole-run",
                  "selected_producer_ids": producer_ids,
                  "selected_publication_ids": selected_publications,
                  "required_support_publication_ids": sorted(selected_reachable - scoped_roots),
                  "other_run_publication_ids": sorted(set(pub_by_id) - selected_reachable)},
        "experiment_metadata": _json_copy(dict(experiment_metadata or {}), "experiment metadata"),
        "publications": rows,
        "dispositions": disposition_rows,
        "recorded_blocked_dependencies": recorded_blocked_dependencies,
        "evaluated_support": support,
        "context_only": context,
        "lineage": lineage,
        "lineage_acts": [_json_copy(row, "lineage act") for row in lineage_acts],
        "unresolved_support": unresolved,
        "complete": not unresolved,
    }


def dumps(document: Mapping[str, Any]) -> bytes:
    """Validate and encode a saved document."""
    reopen(dict(document))
    return (json.dumps(document, sort_keys=True, indent=2) + "\n").encode("utf-8")


def reopen(document: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the file without relying on live coordinator objects."""
    value = _json_copy(dict(document), "saved account evidence")
    if value.get("format") != FORMAT:
        raise SavedEvidenceError("unsupported saved evidence format")
    provenance = value.get("provenance")
    if not isinstance(provenance, dict) or not provenance.get("run_id"):
        raise SavedEvidenceError("run provenance is missing")
    package = provenance.get("package")
    if not isinstance(package, dict) or not package.get("id") or not package.get("version"):
        raise SavedEvidenceError("package provenance is missing")
    publications = value.get("publications")
    if not isinstance(publications, list):
        raise SavedEvidenceError("publications must be a list")
    ids: set[str] = set()
    for row in publications:
        finding = row.get("finding") if isinstance(row, dict) else None
        finding_id = finding.get("id") if isinstance(finding, dict) else None
        if not isinstance(finding, dict) or not isinstance(finding_id, str) or finding_id in ids:
            raise SavedEvidenceError("publication finding IDs must be unique")
        act = row.get("act")
        if not isinstance(act, dict) or act.get("run_id") != provenance["run_id"] or act.get("finding") != finding:
            raise SavedEvidenceError("publication act does not match saved run and finding")
        ids.add(finding_id)
        for pin in finding.get("pins", []):
            if pin.get("role") == "adoption" and (pin.get("id"), pin.get("version")) != (
                package.get("id"), package.get("version")
            ):
                raise SavedEvidenceError("publication adoption pin disagrees with package provenance")
    scope = value.get("scope")
    if not isinstance(scope, dict) or not isinstance(scope.get("selected_producer_ids"), list):
        raise SavedEvidenceError("publication selection scope is missing")
    producer_ids = set(scope["selected_producer_ids"])
    selected = sorted(
        row["finding"]["id"] for row in publications
        if producer_ids and any(pin.get("role") == "computation" and pin.get("id") in producer_ids
                                for pin in row["finding"].get("pins", []))
    )
    roots = set(selected) if producer_ids else set(ids)
    if selected != scope.get("selected_publication_ids"):
        raise SavedEvidenceError("publication selection scope does not match recorded producer pins")
    publication_by_id = {row["finding"]["id"]: row["finding"] for row in publications}
    selected_reachable: set[str] = set()
    selection_queue = list(roots)
    while selection_queue:
        current_id = selection_queue.pop(0)
        if current_id in selected_reachable:
            continue
        selected_reachable.add(current_id)
        for pin in publication_by_id[current_id].get("pins", []):
            target = pin.get("id")
            if pin.get("role") == "input" and target in publication_by_id and target not in selected_reachable:
                selection_queue.append(target)
    if sorted(selected_reachable - roots) != scope.get("required_support_publication_ids") or sorted(
        ids - selected_reachable
    ) != scope.get("other_run_publication_ids"):
        raise SavedEvidenceError("publication dependency scope is inconsistent")
    if not isinstance(value.get("experiment_metadata"), dict):
        raise SavedEvidenceError("experiment metadata must be an object")
    unresolved = value.get("unresolved_support")
    if not isinstance(unresolved, list) or bool(unresolved) == bool(value.get("complete")):
        raise SavedEvidenceError("completeness flag disagrees with unresolved support")
    support = value.get("evaluated_support")
    if not isinstance(support, list):
        raise SavedEvidenceError("evaluated support must be a list")
    support_ids: set[str] = set()
    for row in support:
        finding = row.get("finding", {})
        finding_id = finding.get("id")
        if not isinstance(finding_id, str) or finding_id in support_ids:
            raise SavedEvidenceError("support finding IDs must be unique")
        support_ids.add(finding_id)
        if row.get("fact", {}).get("fact_id") != finding.get("fact_id"):
            raise SavedEvidenceError("support fact identity does not match finding")
        if not isinstance(row.get("fact", {}).get("bindings"), dict) or not isinstance(
            row.get("fact", {}).get("fact_type_id"), str
        ):
            raise SavedEvidenceError("support must retain structured identity keys")
        evidence_ids = set(finding.get("evidence_ids", []))
        stored_ids = {record.get("id") for record in row.get("evidence", [])}
        if not evidence_ids.issubset(stored_ids):
            raise SavedEvidenceError("support evidence is incomplete")
    lineage = value.get("lineage")
    if not isinstance(lineage, list):
        raise SavedEvidenceError("finding lineage snapshot is missing")
    lineage_ids: set[str] = set()
    for row in lineage:
        finding = row.get("finding", {}) if isinstance(row, dict) else {}
        finding_id = finding.get("id")
        if not isinstance(finding_id, str) or finding_id in lineage_ids:
            raise SavedEvidenceError("lineage finding IDs must be unique")
        lineage_ids.add(finding_id)
        if row.get("status") not in {"current", "displaced"}:
            raise SavedEvidenceError("lineage status must be a captured current/displaced snapshot")
        if row.get("fact", {}).get("fact_id") != finding.get("fact_id"):
            raise SavedEvidenceError("lineage fact identity does not match finding")
        evidence_ids = set(finding.get("evidence_ids", []))
        stored_ids = {record.get("id") for record in row.get("evidence", [])}
        if not evidence_ids.issubset(stored_ids):
            raise SavedEvidenceError("lineage evidence is incomplete")
    dispositions = value.get("dispositions")
    if not isinstance(dispositions, list):
        raise SavedEvidenceError("dispositions must be a list")
    scoped_dispositions = [row for row in dispositions if isinstance(row, dict)]
    publication_rows = {row["finding"]["id"]: row for row in publications}
    support_targets = {row["finding"]["id"] for row in support}
    expected_unresolved_pins: set[str] = set()
    pending: list[tuple[str, str, dict[str, Any], list[dict[str, Any]]]] = [
        ("publication", row["finding"]["id"], row["finding"], row["finding"].get("pins", []))
        for row in publications
    ]
    pending.extend(("disposition", str(row.get("artifact_id", "disposition")), row, row.get("pins", []))
                   for row in scoped_dispositions)
    visited: set[str] = set()
    while pending:
        owner_type, owner_id, owner, pins = pending.pop(0)
        if not isinstance(pins, list):
            raise SavedEvidenceError("pins must be a list")
        for pin in pins:
            if not isinstance(pin, dict) or pin.get("role") != "input":
                continue
            target = pin.get("id")
            if not isinstance(target, str):
                raise SavedEvidenceError("input pin has no target identity")
            if target in publication_rows:
                if target not in visited:
                    visited.add(target)
                    finding = publication_rows[target]["finding"]
                    pending.append(("publication", target, finding, finding.get("pins", [])))
            elif target not in support_targets:
                expected_unresolved_pins.add(json.dumps({"owner": _owner_identity(owner_type, owner_id, owner),
                                                         "pin": pin}, sort_keys=True))
    actual_unresolved_pins = {json.dumps({"owner": item.get("owner"), "pin": item.get("pin")}, sort_keys=True)
                              for item in unresolved if isinstance(item, dict) and isinstance(item.get("pin"), dict)}
    if expected_unresolved_pins != actual_unresolved_pins:
        raise SavedEvidenceError("unresolved pin owner/target closure is inconsistent")
    expected_blocked = [row for row in scoped_dispositions if row.get("disposition") == "blocked"]
    if value.get("recorded_blocked_dependencies") != expected_blocked:
        raise SavedEvidenceError("recorded blocked dispositions are incomplete or misattributed")
    for row in dispositions:
        if not isinstance(row, dict):
            raise SavedEvidenceError("dispositions must be objects")
        if row.get("run_id", provenance["run_id"]) != provenance["run_id"]:
            raise SavedEvidenceError("disposition belongs to a different run")
    return cast(dict[str, Any], value)


def loads(data: bytes | str) -> dict[str, Any]:
    try:
        document = json.loads(data)
    except (TypeError, ValueError) as exc:
        raise SavedEvidenceError("saved evidence is not valid JSON") from exc
    if not isinstance(document, dict):
        raise SavedEvidenceError("saved evidence root must be an object")
    return reopen(document)
