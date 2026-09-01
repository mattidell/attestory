"""Rule-scoped dependency-closure digest (ADR-0069 Decision 5).

The re-authorization boundary hashes only the declarations reachable from
the specific rule id(s) a taxpayer's calculation composes — not the whole
adopted package. Reachability reuses, read-only, the expression-tree
walkers ``package_validation.py`` already uses for its entrypoint-rooted
BFS, and roots that walk at the composed rule(s) instead.

Adjacency covers every schema kind that BFS actually emits edges for
(rule-artifact.v1–v6, form-field.v1–v3, source-closure-mapping.v2,
taxable-interest-composition.v1, source-family.v1, attachment-rule.v6/v8,
bundle.v1/v2, and role-canon.v1 as an inbound dependency of every other
member). ``source-family.v2`` uses the same member-predicate / collect
edges as v1 so a package that has migrated families still closes.

This module does not edit ``package_validation.py``.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from packages.derivation.package_validation import (
    _iter_collect_source_sets,
    _iter_parameter_and_table_refs,
    _iter_ref_names,
)

Citizen = dict[str, Any]
Corpus = Mapping[str, Citizen]

_RULE_ARTIFACT_SCHEMAS = frozenset(
    {
        "rule-artifact.v1",
        "rule-artifact.v2",
        "rule-artifact.v3",
        "rule-artifact.v4",
        "rule-artifact.v5",
        "rule-artifact.v6",
        "rule-artifact.v7",
    }
)
_RULE_DECLARED_REFS_OUTSIDE_REQUIRES = frozenset(
    {
        "rule-artifact.v3",
        "rule-artifact.v4",
        "rule-artifact.v5",
        "rule-artifact.v6",
        "rule-artifact.v7",
    }
)
_FORM_FIELD_SCHEMAS = frozenset({"form-field.v1", "form-field.v2", "form-field.v3"})
_BUNDLE_SCHEMAS = frozenset({"bundle.v1", "bundle.v2"})
_SOURCE_FAMILY_SCHEMAS = frozenset({"source-family.v1", "source-family.v2"})
_ATTACHMENT_RULE_BFS_SCHEMAS = frozenset({"attachment-rule.v6", "attachment-rule.v8"})


def _closed_v2_surface(package: Mapping[str, Any] | None) -> bool:
    # Historical artifact-package.v1 keeps its recorded RG-1 refusal; every
    # later package, and a corpus with no package wrapper, uses v2 edges.
    if package is None:
        return True
    return str(package.get("version")) != "v1"


def _binding_fact_types(package: Mapping[str, Any] | None) -> dict[str, str]:
    if package is None:
        return {}
    return {
        binding["symbol"]: binding["fact_type"]["id"]
        for binding in package.get("input_bindings", [])
        if isinstance(binding, dict)
        and isinstance(binding.get("symbol"), str)
        and isinstance(binding.get("fact_type"), dict)
        and isinstance(binding["fact_type"].get("id"), str)
    }


def _citizen_fingerprint(citizen: Citizen) -> str:
    canonical = json.dumps(citizen, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def build_dependency_edges(
    corpus: Corpus,
    *,
    package: Mapping[str, Any] | None = None,
) -> dict[str, set[str]]:
    """member_id -> set(member_id it depends on).

    Edge semantics match ``package_validation.py`` inbound-reachability BFS
    (MEMBER_UNREACHABLE), including the v2 closed-surface extras, rooted
    later at caller-chosen rule ids rather than package entrypoints.
    """
    ids = set(corpus)
    edges: dict[str, set[str]] = {cid: set() for cid in corpus}
    closed = _closed_v2_surface(package)
    binding_fact_types = _binding_fact_types(package)

    produced: dict[str, list[str]] = {}
    bundles_for_fact: dict[str, set[str]] = {}
    families_by_id: dict[str, str] = {}
    role_canons: set[str] = set()
    for cid, citizen in corpus.items():
        schema = citizen.get("schema", "")
        if schema in _RULE_ARTIFACT_SCHEMAS and "publishes" in citizen:
            produced.setdefault(citizen["publishes"], []).append(cid)
        if schema in _BUNDLE_SCHEMAS:
            for fact in citizen.get("fact_types", []):
                fact_id = fact.get("id")
                if isinstance(fact_id, str):
                    bundles_for_fact.setdefault(fact_id, set()).add(cid)
        if schema in _SOURCE_FAMILY_SCHEMAS:
            families_by_id[citizen.get("id", cid)] = cid
        if schema == "role-canon.v1":
            role_canons.add(cid)

    for cid, citizen in corpus.items():
        schema = citizen.get("schema", "")
        if closed and schema != "role-canon.v1":
            edges[cid].update(role_canons)

        if schema in _RULE_ARTIFACT_SCHEMAS:
            when = citizen.get("when", True)
            value = citizen.get("value", {})
            declared_refs = set(citizen.get("requires", []))
            if schema in _RULE_DECLARED_REFS_OUTSIDE_REQUIRES:
                declared_refs.update(_iter_ref_names(when))
                declared_refs.update(_iter_ref_names(value))
            for req in declared_refs:
                for producer_id in produced.get(req, []):
                    edges[cid].add(producer_id)
                if closed:
                    edges[cid].update(
                        bundles_for_fact.get(binding_fact_types.get(req, ""), set())
                    )
            if closed:
                for source_set in set(_iter_collect_source_sets(when)) | set(
                    _iter_collect_source_sets(value)
                ):
                    family_id = families_by_id.get(source_set)
                    if family_id is not None:
                        edges[cid].add(family_id)
            for pid in set(_iter_parameter_and_table_refs(when)) | set(
                _iter_parameter_and_table_refs(value)
            ):
                if pid in ids:
                    edges[cid].add(pid)
            composition = citizen.get("composition")
            if isinstance(composition, dict) and composition.get("id") in ids:
                edges[cid].add(composition["id"])
            for citation in citizen.get("citations", []):
                cite_id = citation.get("id") if isinstance(citation, dict) else None
                if cite_id in ids:
                    cite_ver = citation.get("version")
                    if cite_ver is None or corpus[cite_id].get("version") == cite_ver:
                        edges[cid].add(cite_id)

        elif schema in _FORM_FIELD_SCHEMAS:
            symbol = citizen.get("binds_symbol")
            if isinstance(symbol, str):
                for producer_id in produced.get(symbol, []):
                    edges[cid].add(producer_id)
            citation = citizen.get("citation")
            if isinstance(citation, dict) and citation.get("id") in ids:
                edges[cid].add(citation["id"])

        elif schema == "source-closure-mapping.v2":
            for mapping_key in ("member_fact_type", "closure_fact_type"):
                fact_pin = citizen.get(mapping_key)
                if not isinstance(fact_pin, dict):
                    continue
                fact_id = fact_pin.get("id")
                if fact_id in ids:
                    edges[cid].add(fact_id)
                elif closed and isinstance(fact_id, str):
                    edges[cid].update(bundles_for_fact.get(fact_id, set()))

        elif schema == "taxable-interest-composition.v1":
            for constituent in citizen.get("constituents", []):
                if not isinstance(constituent, dict):
                    continue
                family_pin = constituent.get("source_family")
                if isinstance(family_pin, dict) and family_pin.get("id") in ids:
                    edges[cid].add(family_pin["id"])

        elif schema in _SOURCE_FAMILY_SCHEMAS:
            fact_type = citizen.get("member_predicate", {}).get("fact_type")
            if isinstance(fact_type, str):
                edges[cid].update(bundles_for_fact.get(fact_type, set()))
                for other_id, other in corpus.items():
                    if other.get("schema") != "source-closure-mapping.v2":
                        continue
                    member_pin = other.get("member_fact_type", {})
                    if isinstance(member_pin, dict) and member_pin.get("id") == fact_type:
                        edges[cid].add(other_id)

        elif schema in _ATTACHMENT_RULE_BFS_SCHEMAS:
            for part in citizen.get("itemizations", []):
                if not isinstance(part, dict):
                    continue
                authority = part.get("authority", {})
                if isinstance(authority, dict) and authority.get("kind") == "composition":
                    composition_pin = authority.get("composition", {})
                    if isinstance(composition_pin, dict) and composition_pin.get("id") in ids:
                        edges[cid].add(composition_pin["id"])
                for row_set in part.get("row_sets", []):
                    if not isinstance(row_set, dict):
                        continue
                    rows = row_set.get("rows", {})
                    if not isinstance(rows, dict):
                        continue
                    family_pin = rows.get("source_family", {})
                    if isinstance(family_pin, dict) and family_pin.get("id") in ids:
                        edges[cid].add(family_pin["id"])
                    member_pin = rows.get("member_fact_type", {})
                    if isinstance(member_pin, dict) and member_pin.get("id") in ids:
                        edges[cid].add(member_pin["id"])
                for adjustment in part.get("adjustment_rows", []):
                    if not isinstance(adjustment, dict):
                        continue
                    rows = adjustment.get("rows", {})
                    if not isinstance(rows, dict):
                        continue
                    family_pin = rows.get("source_family", {})
                    if isinstance(family_pin, dict) and family_pin.get("id") in ids:
                        edges[cid].add(family_pin["id"])
                    member_pin = rows.get("member_fact_type", {})
                    if isinstance(member_pin, dict) and member_pin.get("id") in ids:
                        edges[cid].add(member_pin["id"])
            for answer in citizen.get("completeness", {}).get("required_answers", []):
                if not isinstance(answer, dict):
                    continue
                fact_pin = answer.get("fact_type", {})
                if isinstance(fact_pin, dict) and fact_pin.get("id") in ids:
                    edges[cid].add(fact_pin["id"])
            requirement = citizen.get("requirement", {})
            if isinstance(requirement, dict):
                for subtotal in requirement.get("subtotals", []):
                    for producer_id in produced.get(subtotal, []):
                        edges[cid].add(producer_id)
                citation_pin = requirement.get("citation", {})
                if isinstance(citation_pin, dict) and citation_pin.get("id") in ids:
                    edges[cid].add(citation_pin["id"])
                threshold_pin = requirement.get("threshold_parameter", {})
                if isinstance(threshold_pin, dict) and threshold_pin.get("id") in ids:
                    edges[cid].add(threshold_pin["id"])

        elif schema in _BUNDLE_SCHEMAS:
            for fact in citizen.get("fact_types", []):
                if not isinstance(fact, dict):
                    continue
                quantity = fact.get("quantity")
                if isinstance(quantity, dict) and quantity.get("id") in ids:
                    edges[cid].add(quantity["id"])
                optional_default = fact.get("optional_default") if closed else None
                if isinstance(optional_default, dict):
                    parameter = optional_default.get("parameter")
                    if isinstance(parameter, dict) and parameter.get("id") in ids:
                        edges[cid].add(parameter["id"])

    return edges


def rule_scoped_closure(
    root_rule_ids: set[str],
    corpus: Corpus,
    *,
    package: Mapping[str, Any] | None = None,
) -> set[tuple[str, str]]:
    """BFS rooted at the composed rule(s). Returns the (id, version) closure."""
    edges = build_dependency_edges(corpus, package=package)
    visited: set[str] = set()
    queue = [rule_id for rule_id in root_rule_ids if rule_id in corpus]
    visited.update(queue)
    while queue:
        current = queue.pop(0)
        for nxt in edges.get(current, ()):
            if nxt not in visited:
                visited.add(nxt)
                queue.append(nxt)
    return {(cid, str(corpus[cid].get("version", ""))) for cid in visited}


def package_boundary_digest(
    root_rule_ids: set[str],
    corpus: Corpus,
    *,
    package: Mapping[str, Any] | None = None,
) -> str:
    """SHA-256 of the rule-scoped closure: identity plus content fingerprint.

    Hashing citizen bytes (not only id@version) means an in-closure edit
    forces re-authorization even if a caller forgot a version bump. An
    unrelated declaration outside the closure is not hashed.
    """
    visited = {cid for cid, _version in rule_scoped_closure(root_rule_ids, corpus, package=package)}
    payload = [
        {
            "id": cid,
            "version": corpus[cid].get("version", ""),
            "fingerprint": _citizen_fingerprint(corpus[cid]),
        }
        for cid in sorted(visited)
    ]
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()
