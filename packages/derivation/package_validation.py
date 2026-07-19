"""Closed-package validation as a contained, recorded outcome.

ADR-0006 decisions 6 and 7. A package is a closed manifest: exact member
versions, scope cross-checked per member as content (year/jurisdiction never
in ids), closure in both directions, and unique output ownership. This
validator wires those checks to the *published* schemas and, crucially,
never lets one bad member abort the whole run (decision 3): a schema-invalid
or absent member becomes a recorded issue while the rest of the package is
still checked. The result is data the derivation record can carry.

The it2 attack corpus is the acceptance bar (round-2 adversary parity):
- parity 1 (blast radius): one invalid member is contained, not fatal.
- parity 3 (duplicate output): two members publishing one symbol is rejected.
- parity 6 (package closure): a referenced parameter/table not in the
  package is rejected.
- attack 5 (year identity): a member whose scope disagrees with the package
  scope is rejected; identity never rides in the id.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from packages.kernel.schema_registry import SchemaValidationError
from packages.derivation.loader import DerivationSchemas, PACKAGE_SCHEMA

_RULE_ROLES = frozenset({"computation", "applicability", "field-mapping", "cross-form-bridge"})
_RULE_ARTIFACT_SCHEMAS = frozenset({"rule-artifact.v1", "rule-artifact.v2", "rule-artifact.v3"})
_SCOPE_KEYS = ("tax_year", "jurisdiction", "family")

# E14.2 (extended by ADR-0032): record-kind and contribution citizens are never
# permissible rule/package dependencies. Runs consume facts, not process accounts
# or contribution events.
_NON_INPUT_SCHEMAS = frozenset({
    "contribution.v1",
    "contribution-record.v1",
    "derivation-record.v1",
    "derivation-record.v2",
})


@dataclass(frozen=True)
class MemberIssue:
    """One thing wrong with one member, named so a record can carry it."""

    member_id: str
    version: str
    code: str
    detail: str


@dataclass(frozen=True)
class CitationResolution:
    """One exact package citation resolved without external legal claims."""

    citation_id: str
    version: str
    status: str = "statically_resolved"


@dataclass(frozen=True)
class PackageValidation:
    """A contained validation outcome for one package against a corpus."""

    package_id: str
    ok: bool
    issues: tuple[MemberIssue, ...]
    output_owners: dict[str, str]
    citation_resolutions: tuple[CitationResolution, ...]
    resolved_members: tuple[dict[str, Any], ...] = ()


class PackageIntegrityError(ValueError):
    """An offered package is not the immutable published instance."""


def package_instance_checksum(package: Mapping[str, Any]) -> str:
    """Return the SHA-256 of canonical package bytes, excluding its checksum.

    ``package_checksum`` records the checksum rather than participating in its
    own digest. The published-package registry pins that same digest by exact
    package id/version, so recomputing the field after an in-place edit cannot
    rewrite an already published package version.
    """
    body = {key: value for key, value in package.items() if key != "package_checksum"}
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def citizen_checksum(citizen: dict[str, Any]) -> str:
    """Return the SHA-256 of canonical citizen bytes."""
    canonical = json.dumps(citizen, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def load_published_package_checksums(path: Path) -> dict[tuple[str, str], str]:
    """Load the small publication registry for immutable package instances."""
    document: dict[str, Any] = json.loads(path.read_text("utf-8"))
    entries = document.get("packages")
    if not isinstance(entries, list):
        raise PackageIntegrityError(f"{path}: packages must be an array")
    registry: dict[tuple[str, str], str] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise PackageIntegrityError(f"{path}: package entry must be an object")
        package_id = entry.get("id")
        version = entry.get("version")
        checksum = entry.get("checksum")
        if not isinstance(package_id, str) or not isinstance(version, str):
            raise PackageIntegrityError(f"{path}: package entry needs string id and version")
        if not isinstance(checksum, str) or len(checksum) != 64:
            raise PackageIntegrityError(f"{path}: package entry {package_id}@{version} has invalid checksum")
        key = (package_id, version)
        if key in registry:
            raise PackageIntegrityError(f"{path}: duplicate package entry {package_id}@{version}")
        registry[key] = checksum
    return registry


def load_published_citizen_checksums(path: Path) -> dict[tuple[str, str], str]:
    """Load the publication registry for immutable citizen bytes."""
    document: dict[str, Any] = json.loads(path.read_text("utf-8"))
    entries = document.get("citizens", [])
    if not isinstance(entries, list):
        raise PackageIntegrityError(f"{path}: citizens must be an array")
    registry: dict[tuple[str, str], str] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise PackageIntegrityError(f"{path}: citizen entry must be an object")
        citizen_id = entry.get("id")
        version = entry.get("version")
        checksum = entry.get("checksum")
        if not isinstance(citizen_id, str) or not isinstance(version, str):
            raise PackageIntegrityError(f"{path}: citizen entry needs string id and version")
        if not isinstance(checksum, str) or len(checksum) != 64:
            raise PackageIntegrityError(f"{path}: citizen entry {citizen_id}@{version} has invalid checksum")
        key = (citizen_id, version)
        if key in registry:
            raise PackageIntegrityError(f"{path}: duplicate citizen entry {citizen_id}@{version}")
        registry[key] = checksum
    return registry


def verify_published_package(
    package: Mapping[str, Any], published_checksums: Mapping[tuple[str, str], str]
) -> None:
    """Reject an unpublished, corrupted, or rewritten package instance."""
    package_id = package.get("id")
    version = package.get("version")
    recorded = package.get("package_checksum")
    if not isinstance(package_id, str) or not isinstance(version, str):
        raise PackageIntegrityError("package needs string id and version")
    if not isinstance(recorded, str):
        raise PackageIntegrityError(f"{package_id}@{version}: package_checksum is missing")
    actual = package_instance_checksum(package)
    if recorded != actual:
        raise PackageIntegrityError(f"{package_id}@{version}: PACKAGE_CHECKSUM_MISMATCH")
    published = published_checksums.get((package_id, version))
    if published is None:
        raise PackageIntegrityError(f"{package_id}@{version}: PACKAGE_UNPUBLISHED")
    if actual != published:
        raise PackageIntegrityError(f"{package_id}@{version}: PACKAGE_VERSION_REWRITE")


def _corpus_key(citizen_id: str, version: str) -> tuple[str, str]:
    return (citizen_id, version)


def _iter_parameter_and_table_refs(expr: Any) -> Iterable[str]:
    """Yield every parameter_id / table_id referenced anywhere in an expression."""
    if isinstance(expr, dict):
        op = expr.get("op")
        if op == "parameter" and isinstance(expr.get("parameter_id"), str):
            yield expr["parameter_id"]
        if op in {"range_lookup", "bracket_fold"} and isinstance(expr.get("table_id"), str):
            yield expr["table_id"]
        for value in expr.values():
            yield from _iter_parameter_and_table_refs(value)
    elif isinstance(expr, list):
        for item in expr:
            yield from _iter_parameter_and_table_refs(item)


def _iter_collect_source_sets(expr: Any) -> Iterable[str]:
    """Yield the adopted family identities named by ``collect`` expressions."""
    if isinstance(expr, dict):
        if expr.get("op") == "collect" and isinstance(expr.get("source_set"), str):
            yield expr["source_set"]
        for value in expr.values():
            yield from _iter_collect_source_sets(value)
    elif isinstance(expr, list):
        for item in expr:
            yield from _iter_collect_source_sets(item)


def _iter_ref_names(expr: Any) -> Iterable[str]:
    """Yield declared ref names, including conditional dependency members."""
    if isinstance(expr, dict):
        if expr.get("op") == "ref" and isinstance(expr.get("name"), str):
            yield expr["name"]
        for value in expr.values():
            yield from _iter_ref_names(value)
    elif isinstance(expr, list):
        for item in expr:
            yield from _iter_ref_names(item)


def validate_package(
    package: dict[str, Any],
    corpus: dict[tuple[str, str], dict[str, Any]],
    schemas: DerivationSchemas,
    published_citizen_checksums: Mapping[tuple[str, str], str] | None = None,
) -> PackageValidation:
    """Validate a package against a corpus of (id, version) -> citizen.

    Never raises for citizen-level defects: each becomes a MemberIssue and
    validation continues, so the caller can record every problem at once and
    let unaffected members proceed.
    """
    package_id = str(package.get("id", "<unidentified>"))

    try:
        schemas.validate_declared(package)
    except SchemaValidationError as exc:
        return PackageValidation(
            package_id=package_id,
            ok=False,
            issues=(MemberIssue(package_id, str(package.get("version", "")), "PACKAGE_SCHEMA_INVALID", str(exc)),),
            output_owners={},
            citation_resolutions=(),
            resolved_members=(),
        )

    package_scope = {key: package["scope"].get(key) for key in _SCOPE_KEYS}
    issues: list[MemberIssue] = []
    resolved: list[tuple[dict[str, Any], dict[str, Any]]] = []  # (pin, citizen)

    for pin in package["members"]:
        key = _corpus_key(pin["id"], pin["version"])
        citizen = corpus.get(key)
        if citizen is None:
            issues.append(MemberIssue(pin["id"], pin["version"], "MEMBER_ABSENT", "member not present in corpus"))
            continue
        try:
            schemas.validate_declared(citizen)
        except SchemaValidationError as exc:
            issues.append(MemberIssue(pin["id"], pin["version"], "MEMBER_SCHEMA_INVALID", str(exc)))
            continue

        if published_citizen_checksums is not None:
            expected_checksum = published_citizen_checksums.get(key)
            if expected_checksum is None:
                issues.append(MemberIssue(pin["id"], pin["version"], "MEMBER_UNPUBLISHED", "member not in publication registry"))
                continue
            actual_checksum = citizen_checksum(citizen)
            if expected_checksum != actual_checksum:
                issues.append(MemberIssue(pin["id"], pin["version"], "MEMBER_CHECKSUM_MISMATCH", "member bytes do not match publication registry"))
                continue

        resolved.append((pin, citizen))

    member_ids = {pin["id"] for pin in package["members"]}
    citation_keys = {
        _corpus_key(pin["id"], pin["version"])
        for pin, citizen in resolved
        if citizen["schema"] == "citation.v1" and pin["role"] == "citation"
    }
    produced: dict[str, list[str]] = {}

    admitted = package.get("admitted_schemas", [])
    has_admitted = "admitted_schemas" in package

    # 1. Fact surface compilation Q(P)
    fact_surface: set[tuple[str, str]] = set()
    fact_quantities: dict[str, dict[str, Any]] = {}
    fact_defaults: dict[str, dict[str, Any]] = {}

    for pin, citizen in resolved:
        if citizen["schema"] in {"bundle.v1", "bundle.v2"}:
            for ft in citizen.get("fact_types", []):
                fact_surface.add((ft["id"], ft.get("version", "v1")))
                if "quantity" in ft:
                    fact_quantities[ft["id"]] = ft["quantity"]
                if "optional_default" in ft:
                    fact_defaults[ft["id"]] = ft["optional_default"]["parameter"]
        elif citizen["schema"] == "fact-type.v2":
            fact_surface.add((citizen["id"], citizen["version"]))
            if "quantity" in citizen:
                fact_quantities[citizen["id"]] = citizen["quantity"]
            if "optional_default" in citizen:
                fact_defaults[citizen["id"]] = citizen["optional_default"]["parameter"]

    # 2. Member level checks
    for pin, citizen in resolved:
        pin_role = pin["role"]

        if has_admitted and citizen["schema"] not in admitted:
            issues.append(MemberIssue(pin["id"], pin["version"], "SCHEMA_NOT_ADMITTED",
                                       f"schema {citizen['schema']!r} not in admitted_schemas"))

        # E14.2 / ADR-0032: contribution and record citizens are not inputs.
        if citizen["schema"] in _NON_INPUT_SCHEMAS:
            issues.append(MemberIssue(
                pin["id"], pin["version"], "E14_2_FORBIDDEN_DEPENDENCY",
                f"schema {citizen['schema']!r} is not a permissible package dependency "
                f"(records and contributions are not rule inputs)",
            ))

        if citizen["schema"] in _RULE_ARTIFACT_SCHEMAS:
            if pin_role != citizen["role"]:
                issues.append(MemberIssue(pin["id"], pin["version"], "ROLE_MISMATCH",
                                           f"package role {pin_role!r} != rule role {citizen['role']!r}"))
        elif citizen["schema"] in {"parameter-declaration.v1", "quantity-vocabulary.v1", "role-canon.v1"}:
            if pin_role != "parameter":
                issues.append(MemberIssue(pin["id"], pin["version"], "ROLE_MISMATCH",
                                           f"parameter declared as role {pin_role!r}"))
        elif citizen["schema"] in {"form-field.v1", "form-field.v2"}:
            if pin_role != "form-field":
                issues.append(MemberIssue(pin["id"], pin["version"], "ROLE_MISMATCH",
                                           f"form-field declared as role {pin_role!r}"))
        elif citizen["schema"] == "source-family.v1":
            if pin_role != "source-family":
                issues.append(MemberIssue(pin["id"], pin["version"], "ROLE_MISMATCH",
                                           f"source-family declared as role {pin_role!r}"))
        elif citizen["schema"] == "source-closure-mapping.v2":
            if pin_role != "source-closure-mapping":
                issues.append(MemberIssue(pin["id"], pin["version"], "ROLE_MISMATCH",
                                           f"source-closure-mapping declared as role {pin_role!r}"))
        elif citizen["schema"] == "taxable-interest-composition.v1":
            if pin_role != "composition":
                issues.append(MemberIssue(pin["id"], pin["version"], "ROLE_MISMATCH",
                                           f"composition declared as role {pin_role!r}"))
        elif citizen["schema"] == "citation.v1":
            if pin_role != "citation":
                issues.append(MemberIssue(pin["id"], pin["version"], "ROLE_MISMATCH",
                                           f"citation declared as role {pin_role!r}"))
        elif citizen["schema"] == "fact-type.v2":
            if pin_role != "fact-type":
                issues.append(MemberIssue(pin["id"], pin["version"], "ROLE_MISMATCH",
                                           f"fact-type declared as role {pin_role!r}"))
        elif citizen["schema"] in {"bundle.v1", "bundle.v2"}:
            if pin_role != "fact-type-bundle":
                issues.append(MemberIssue(pin["id"], pin["version"], "ROLE_MISMATCH",
                                           f"bundle declared as role {pin_role!r}"))
        elif citizen["schema"] in {"operation-semantics.v1", "operation-semantics.v2"}:
            if pin_role != "operation-semantics":
                issues.append(MemberIssue(pin["id"], pin["version"], "ROLE_MISMATCH",
                                           f"operation-semantics declared as role {pin_role!r}"))

        if "scope" in citizen:
            member_scope = {key: citizen.get("scope", {}).get(key) for key in _SCOPE_KEYS}
            if member_scope != package_scope:
                issues.append(MemberIssue(pin["id"], pin["version"], "SCOPE_MISMATCH",
                                          f"member scope {member_scope} != package scope {package_scope}"))

        if citizen["schema"] in _RULE_ARTIFACT_SCHEMAS:
            produced.setdefault(citizen["publishes"], []).append(pin["id"])
            for ref in set(_iter_parameter_and_table_refs(citizen["when"])) | set(
                _iter_parameter_and_table_refs(citizen["value"])
            ):
                if ref not in member_ids:
                    issues.append(MemberIssue(pin["id"], pin["version"], "CLOSURE_MISSING_PARAMETER",
                                              f"references {ref!r}, absent from package"))
            # Pin-target half of E14.2: a rule pin naming a contribution/record
            # citizen is a forbidden dependency declaration.
            for rule_pin in citizen.get("pins", []):
                target_key = _corpus_key(rule_pin["id"], rule_pin["version"])
                target = corpus.get(target_key)
                if target is not None and target.get("schema") in _NON_INPUT_SCHEMAS:
                    issues.append(MemberIssue(
                        pin["id"], pin["version"], "E14_2_FORBIDDEN_DEPENDENCY",
                        f"rule pin {rule_pin['id']!r} declares forbidden dependency "
                        f"schema {target['schema']!r}",
                    ))
            for citation in citizen.get("citations", []):
                citation_key = _corpus_key(citation["id"], citation["version"])
                if citation_key not in citation_keys:
                    issues.append(MemberIssue(pin["id"], pin["version"], "CITATION_ABSENT",
                                              f"rule citation {citation_key} is not an exact citation package member"))

        # Mapping exact joins validation
        if citizen["schema"] == "source-closure-mapping.v2":
            for mapping_key in ("member_fact_type", "closure_fact_type"):
                ft_pin = citizen.get(mapping_key)
                if ft_pin:
                    ft_key = (ft_pin["id"], ft_pin["version"])
                    if ft_key not in fact_surface:
                        issues.append(MemberIssue(pin["id"], pin["version"], "MAPPING_FACT_TYPE_NOT_ADMITTED",
                                                  f"mapping {mapping_key} {ft_key} not in package fact surface"))

        # Form-field binds symbol & citation validation
        if citizen["schema"] in {"form-field.v1", "form-field.v2"}:
            cit_pin = citizen.get("citation")
            if cit_pin and _corpus_key(cit_pin["id"], cit_pin["version"]) not in citation_keys:
                issues.append(MemberIssue(pin["id"], pin["version"], "CITATION_ABSENT",
                                          f"form-field citation {(cit_pin['id'], cit_pin['version'])} is not an exact citation package member"))

    # 3. Input bindings validation
    input_symbols = set()
    for binding in package.get("input_bindings", []):
        input_symbols.add(binding["symbol"])
        ft_pin = binding["fact_type"]
        ft_key = (ft_pin["id"], ft_pin["version"])
        if ft_key not in fact_surface and ft_pin["id"] != "rounding.convention":
            issues.append(MemberIssue(package_id, "", "BINDING_FACT_TYPE_NOT_ADMITTED",
                                      f"bound fact type {ft_key} not in package fact surface"))
        if binding["mode"] == "optional_default":
            ft_id = ft_pin["id"]
            if ft_id not in fact_defaults:
                issues.append(MemberIssue(package_id, "", "BINDING_DEFAULT_MISSING",
                                          f"optional_default binding {ft_id} has no default parameter defined on fact type"))
            else:
                param_pin = fact_defaults[ft_id]
                if param_pin["id"] not in member_ids:
                    issues.append(MemberIssue(package_id, "", "BINDING_DEFAULT_ABSENT",
                                              f"optional_default parameter {param_pin['id']} not in package"))

    # 4. Form-field binds symbol closure
    for pin, citizen in resolved:
        if citizen["schema"] in {"form-field.v1", "form-field.v2"}:
            symbol = citizen["binds_symbol"]
            if symbol not in produced and symbol not in input_symbols:
                issues.append(MemberIssue(pin["id"], pin["version"], "FORM_FIELD_BINDING_MISSING",
                                          f"form-field binds_symbol {symbol!r} is not produced or bound in package"))
            elif symbol in produced and len(produced[symbol]) > 1:
                conflict = next((c for c in package.get("conflict_semantics", []) if c["symbol"] == symbol), None)
                if conflict is None or "selected_producer" not in conflict or conflict["selected_producer"]["id"] not in member_ids:
                    issues.append(MemberIssue(pin["id"], pin["version"], "FORM_FIELD_PRODUCER_CONFLICT",
                                              f"multiple producers for form-field symbol {symbol!r} without conflict selection"))

    # 5. Quantity validations (ADR-0028 decision 7)
    quantity_vocabularies = {}
    for pin, citizen in resolved:
        if citizen["schema"] == "quantity-vocabulary.v1":
            quantity_vocabularies[citizen["id"]] = citizen["quantities"]

    for ft_id, q_pin in fact_quantities.items():
        q_id = q_pin["id"]
        if q_id not in member_ids:
            issues.append(MemberIssue(ft_id, "", "QUANTITY_VOCABULARY_ABSENT",
                                      f"quantity vocabulary {q_id} not in package"))
        else:
            vocab = next((c for p, c in resolved if c["id"] == q_id), None)
            if vocab is not None:
                quantities = vocab.get("quantities", [])
                q_name = q_id.split(".")[-1]
                if q_name not in quantities:
                    issues.append(MemberIssue(ft_id, "", "QUANTITY_NOT_IN_VOCABULARY",
                                              f"quantity name {q_name!r} not in vocabulary quantities {quantities}"))

    # Helper to resolve input quantity
    source_families = {}
    for pin, citizen in resolved:
        if citizen["schema"] == "source-family.v1":
            source_families[citizen["authorizes_subtotal"]] = citizen["member_predicate"]["fact_type"]

    def get_input_quantity(symbol: str) -> str | None:
        ft_id = source_families.get(symbol, symbol)
        ft_citizen = None
        for pin, citizen in resolved:
            if citizen["schema"] in {"bundle.v1", "bundle.v2"}:
                for ft in citizen.get("fact_types", []):
                    if ft["id"] == ft_id:
                        ft_citizen = ft
                        break
            elif citizen["schema"] == "fact-type.v2" and citizen["id"] == ft_id:
                ft_citizen = citizen
                break
        
        if ft_citizen is not None:
            if ft_citizen.get("schema") == "fact-type.v2" and ft_citizen.get("source_amount") is True:
                if "quantity" not in ft_citizen:
                    issues.append(MemberIssue(ft_id, "", "QUANTITY_TAG_MISSING",
                                              f"source amount fact type {ft_id} is missing quantity tag"))
                    return None
                return str(ft_citizen["quantity"]["id"])
        return None

    # 6. Force-declare same-quantity source aggregation (ADR-0028 decision 8)
    for pin, citizen in resolved:
        if citizen["schema"] in _RULE_ARTIFACT_SCHEMAS:
            inputs = citizen.get("requires", [])
            input_qs = []
            for inp in inputs:
                q = get_input_quantity(inp)
                if q is not None:
                    input_qs.append(q)
            q_counts: dict[str, int] = {}
            for q in input_qs:
                q_counts[q] = q_counts.get(q, 0) + 1
            shared_qs = [q for q, count in q_counts.items() if count >= 2]
            if shared_qs:
                publishes = citizen["publishes"]
                obligations = package.get("composition_obligations", [])
                if publishes not in obligations:
                    issues.append(MemberIssue(pin["id"], pin["version"], "FORCE_DECLARE_COMPOSITION_MISSING",
                                              f"symbol {publishes!r} aggregates multiple inputs of the same quantity {shared_qs} but is not declared in composition_obligations"))

    # 7. Composition obligations & Slot bijection (ADR-0028 decision 6)
    for S in package.get("composition_obligations", []):
        comp_member = None
        for pin, citizen in resolved:
            if pin["role"] == "composition" and citizen.get("publishes") == S:
                comp_member = (pin, citizen)
                break
        if comp_member is None:
            issues.append(MemberIssue(package_id, "", "COMPOSITION_MEMBER_MISSING",
                                      f"composition member publishing {S!r} is missing from package"))
        else:
            comp_pin, comp_citizen = comp_member
            prod_rule = None
            for pin, citizen in resolved:
                if citizen["schema"] in _RULE_ARTIFACT_SCHEMAS and citizen["publishes"] == S:
                    prod_rule = (pin, citizen)
                    break
            if prod_rule is None:
                issues.append(MemberIssue(package_id, "", "COMPOSITION_PRODUCER_MISSING",
                                          f"producing rule for obligated composition symbol {S!r} is missing from package"))
            else:
                rule_pin, rule_citizen = prod_rule
                r_comp = rule_citizen.get("composition")
                if r_comp is None:
                    issues.append(MemberIssue(rule_pin["id"], rule_pin["version"], "COMPOSITION_PIN_MISSING",
                                              f"rule {rule_pin['id']} publishes composition symbol {S!r} but is missing composition pin"))
                elif r_comp["id"] != comp_pin["id"] or r_comp["version"] != comp_pin["version"]:
                     issues.append(MemberIssue(rule_pin["id"], rule_pin["version"], "COMPOSITION_PIN_MISMATCH",
                                               f"rule {rule_pin['id']} composition pin resolves to {r_comp['id']} {r_comp['version']}, expected {comp_pin['id']} {comp_pin['version']}"))
                comp_constituents = {c["authorizes_subtotal"] for c in comp_citizen.get("constituents", [])}
                rule_requires = set(rule_citizen.get("requires", []))
                if comp_constituents != rule_requires:
                     issues.append(MemberIssue(comp_pin["id"], comp_pin["version"], "COMPOSITION_SLOT_BIJECTION_MISMATCH",
                                               f"composition constituents {comp_constituents} do not match rule requires {rule_requires}"))

    # 8. Inbound Reachability validation (ADR-0027 decision 4)
    if "entrypoints" in package:
        adj: dict[str, set[str]] = {m_id: set() for m_id in member_ids}
        # The historical v1 package remains an intentionally recorded RG-1
        # refusal.  These are the v2 closure edges that its successor adopts;
        # applying them retroactively would alter the historical contained
        # issue surface without changing any v1 bytes.
        closed_v2_surface = str(package.get("version")) != "v1"
        bundles_for_fact: dict[str, set[str]] = {}
        for bundle_pin, bundle in resolved:
            if bundle["schema"] not in {"bundle.v1", "bundle.v2"}:
                continue
            for fact in bundle.get("fact_types", []):
                bundles_for_fact.setdefault(fact["id"], set()).add(bundle_pin["id"])
        binding_fact_types = {
            binding["symbol"]: binding["fact_type"]["id"]
            for binding in package.get("input_bindings", [])
        }
        role_canons = {
            pin["id"] for pin, citizen in resolved
            if citizen["schema"] == "role-canon.v1"
        }
        for pin, citizen in resolved:
            m_id = pin["id"]
            # The immutable role canon is authority for every package pin.  It
            # is therefore an inbound dependency of every other member, not a
            # decorative co-located document.
            if closed_v2_surface and citizen["schema"] != "role-canon.v1":
                adj[m_id].update(role_canons)
            if citizen["schema"] in _RULE_ARTIFACT_SCHEMAS:
                declared_refs = set(citizen.get("requires", []))
                declared_refs.update(_iter_ref_names(citizen["when"]))
                declared_refs.update(_iter_ref_names(citizen["value"]))
                for req in declared_refs:
                    for p_id in produced.get(req, []):
                        adj[m_id].add(p_id)
                    if closed_v2_surface:
                        adj[m_id].update(bundles_for_fact.get(binding_fact_types.get(req, ""), set()))
                if closed_v2_surface:
                    for source_set in _iter_collect_source_sets(citizen["when"]):
                        for p2, c2 in resolved:
                            if c2["schema"] == "source-family.v1" and c2["id"] == source_set:
                                adj[m_id].add(p2["id"])
                    for source_set in _iter_collect_source_sets(citizen["value"]):
                        for p2, c2 in resolved:
                            if c2["schema"] == "source-family.v1" and c2["id"] == source_set:
                                adj[m_id].add(p2["id"])
                for pid in set(_iter_parameter_and_table_refs(citizen["when"])) | set(
                    _iter_parameter_and_table_refs(citizen["value"])
                ):
                    if pid in member_ids:
                        adj[m_id].add(pid)
                comp = citizen.get("composition")
                if comp and comp["id"] in member_ids:
                    adj[m_id].add(comp["id"])
                for citation in citizen.get("citations", []):
                    if _corpus_key(citation["id"], citation["version"]) in citation_keys:
                        adj[m_id].add(citation["id"])
            elif citizen["schema"] in {"form-field.v1", "form-field.v2"}:
                symbol = citizen["binds_symbol"]
                for p_id in produced.get(symbol, []):
                    adj[m_id].add(p_id)
                cit = citizen.get("citation")
                if cit and cit["id"] in member_ids:
                    adj[m_id].add(cit["id"])
            elif citizen["schema"] == "source-closure-mapping.v2":
                for mapping_key in ("member_fact_type", "closure_fact_type"):
                    ft_pin = citizen.get(mapping_key)
                    if ft_pin and ft_pin["id"] in member_ids:
                        adj[m_id].add(ft_pin["id"])
                    elif ft_pin and closed_v2_surface:
                        adj[m_id].update(bundles_for_fact.get(ft_pin["id"], set()))
            elif citizen["schema"] == "taxable-interest-composition.v1":
                for c in citizen.get("constituents", []):
                    sf_id = c["source_family"]["id"]
                    if sf_id in member_ids:
                        adj[m_id].add(sf_id)
            elif citizen["schema"] == "source-family.v1":
                ft_id = citizen["member_predicate"]["fact_type"]
                for p_id in member_ids:
                    for p2, c2 in resolved:
                        if c2["id"] == p_id and c2["schema"] in {"bundle.v1", "bundle.v2"}:
                            if any(ft["id"] == ft_id for ft in c2.get("fact_types", [])):
                                adj[m_id].add(p_id)
                # ALSO depend on source-closure-mapping for this family
                for p2, c2 in resolved:
                    if c2["schema"] == "source-closure-mapping.v2":
                        if c2.get("member_fact_type", {}).get("id") == ft_id:
                            adj[m_id].add(c2["id"])
            elif citizen["schema"] in {"bundle.v1", "bundle.v2"}:
                for ft in citizen.get("fact_types", []):
                    if "quantity" in ft:
                        q_id = ft["quantity"]["id"]
                        if q_id in member_ids:
                            adj[m_id].add(q_id)
                    optional_default = ft.get("optional_default") if closed_v2_surface else None
                    if isinstance(optional_default, dict):
                        parameter = optional_default.get("parameter")
                        if isinstance(parameter, dict) and parameter.get("id") in member_ids:
                            adj[m_id].add(parameter["id"])

        roots = set()
        for entry in package.get("entrypoints", []):
            roots.add(entry["id"])
        for pin, citizen in resolved:
            if citizen["schema"] in {"form-field.v1", "form-field.v2"}:
                roots.add(pin["id"])

        queue = list(roots & member_ids)
        visited = set(queue)
        while queue:
            curr = queue.pop(0)
            for neighbor in adj.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        for m_id in member_ids:
            if m_id not in visited:
                m_pin = next(p for p in package["members"] if p["id"] == m_id)
                issues.append(MemberIssue(m_id, m_pin["version"], "MEMBER_UNREACHABLE",
                                         f"member {m_id} is unreachable from package entrypoints or form fields"))

    # 9. Unique output ownership (decision 7)
    declared_conflicts = {c["symbol"] for c in package.get("conflict_semantics", [])}
    output_owners: dict[str, str] = {}
    for symbol, owners in sorted(produced.items()):
        if len(owners) > 1 and symbol not in declared_conflicts:
            issues.append(MemberIssue(owners[1], "", "OUTPUT_OWNERSHIP_CONFLICT",
                                      f"symbol {symbol!r} published by {sorted(owners)}"))
        output_owners[symbol] = owners[0]

    return PackageValidation(
        package_id=package_id,
        ok=not issues,
        issues=tuple(issues),
        output_owners=output_owners,
        citation_resolutions=tuple(
            CitationResolution(citation_id=citation_id, version=version)
            for citation_id, version in sorted(citation_keys)
        ),
        resolved_members=tuple(citizen for pin, citizen in resolved),
    )
