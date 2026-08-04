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

# attachment-rule.v6 keeps the class authority in the source-family pin.  The
# terminal family token is the bounded class marker shared by the synthetic
# gate and the later class-specific families; it is not inferred from labels.
_V3_ADJUSTMENT_BINDINGS = {
    "nominee_distribution": ("Nominee Distribution", "nominee"),
    "accrued_interest": ("Accrued Interest", "accrued-interest"),
    "abp_adjustment": ("ABP Adjustment", "abp-adjustment"),
}

_V11_ADJUSTMENT_SLOTS = (
    ("tax.us.2025.scheduleb.adjustment.nominee", "tax.us.2025.interest.scheduleb-nominee-subtotal"),
    ("tax.us.2025.scheduleb.adjustment.accrued-interest", "tax.us.2025.interest.scheduleb-accrued-interest-subtotal"),
    ("tax.us.2025.scheduleb.adjustment.abp-adjustment", "tax.us.2025.interest.scheduleb-abp-adjustment-subtotal"),
)

# E14.2 (extended by ADR-0032): record-kind and contribution citizens are never
# permissible rule/package dependencies. Runs consume facts, not process accounts
# or contribution events.
_NON_INPUT_SCHEMAS = frozenset({
    "contribution.v1",
    "contribution-record.v1",
    "derivation-record.v1",
    "derivation-record.v2",
    "derivation-record.v3",
    "derivation-record.v4",
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


def _iter_collect_exprs(expr: Any) -> Iterable[dict[str, Any]]:
    """Yield every ``collect`` expression node anywhere in an expression."""
    if isinstance(expr, dict):
        if expr.get("op") == "collect":
            yield expr
        for value in expr.values():
            yield from _iter_collect_exprs(value)
    elif isinstance(expr, list):
        for item in expr:
            yield from _iter_collect_exprs(item)


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


def _iter_require_closed_source_sets(expr: Any) -> Iterable[str]:
    """Yield every family named by a ``require_closed`` node."""
    if isinstance(expr, dict):
        if expr.get("op") == "require_closed" and isinstance(expr.get("source_set"), str):
            yield expr["source_set"]
        for value in expr.values():
            yield from _iter_require_closed_source_sets(value)
    elif isinstance(expr, list):
        for item in expr:
            yield from _iter_require_closed_source_sets(item)


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


def _iter_cds_member_names(expr: Any) -> Iterable[str]:
    """Yield ``ref`` names declared as ``conditional_dependency_set`` members.

    ADR-0037's node names its active dependency set in one closed list; this
    is a narrower cousin of ``_iter_ref_names`` used only to locate the
    declared-absence symbols ADR-0038's domain guard must check, never the
    ordinary reads elsewhere in the expression tree.
    """
    if isinstance(expr, dict):
        if expr.get("op") == "conditional_dependency_set":
            for member in expr.get("members", []):
                if isinstance(member, dict) and member.get("op") == "ref" and isinstance(member.get("name"), str):
                    yield member["name"]
        for value in expr.values():
            yield from _iter_cds_member_names(value)
    elif isinstance(expr, list):
        for item in expr:
            yield from _iter_cds_member_names(item)


def _iter_category_literal_fact_types(expr: Any) -> Iterable[str]:
    """Yield fact type ids named by ``category_literal`` nodes anywhere in
    an expression tree - the signal that a symbol is read categorically,
    not merely present as an ordinary numeric/other conditional_dependency_
    set member."""
    if isinstance(expr, dict):
        if expr.get("op") == "category_literal":
            fact_type = expr.get("fact_type")
            fact_type_id = fact_type.get("id") if isinstance(fact_type, dict) else fact_type
            if isinstance(fact_type_id, str):
                yield fact_type_id
        for value in expr.values():
            yield from _iter_category_literal_fact_types(value)
    elif isinstance(expr, list):
        for item in expr:
            yield from _iter_category_literal_fact_types(item)


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
    fact_types_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    fact_quantities: dict[str, dict[str, Any]] = {}
    fact_defaults: dict[str, dict[str, Any]] = {}

    for pin, citizen in resolved:
        if citizen["schema"] in {"bundle.v1", "bundle.v2"}:
            for ft in citizen.get("fact_types", []):
                fact_surface.add((ft["id"], ft.get("version", "v1")))
                fact_types_by_key[(ft["id"], ft.get("version", "v1"))] = ft
                if "quantity" in ft:
                    fact_quantities[ft["id"]] = ft["quantity"]
                if "optional_default" in ft:
                    fact_defaults[ft["id"]] = ft["optional_default"]["parameter"]
        elif citizen["schema"] == "fact-type.v2":
            fact_surface.add((citizen["id"], citizen["version"]))
            fact_types_by_key[(citizen["id"], citizen["version"])] = citizen
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
        elif citizen["schema"] in {
            "parameter-declaration.v1",
            "quantity-vocabulary.v1",
            "quantity-vocabulary.v2",
            "quantity-vocabulary.v3",
            "role-canon.v1",
        }:
            if pin_role != "parameter":
                issues.append(MemberIssue(pin["id"], pin["version"], "ROLE_MISMATCH",
                                           f"parameter declared as role {pin_role!r}"))
        elif citizen["schema"] in {"form-field.v1", "form-field.v2", "form-field.v3"}:
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
        elif citizen["schema"] in {"dividend-universe.v1", "dividend-universe.v2"}:
            if pin_role != "dividend-universe":
                issues.append(MemberIssue(pin["id"], pin["version"], "ROLE_MISMATCH",
                                           f"dividend-universe declared as role {pin_role!r}"))
        elif citizen["schema"] == "checked-conclusion-binding.v1":
            if pin_role != "checked-conclusion-binding":
                issues.append(MemberIssue(pin["id"], pin["version"], "ROLE_MISMATCH",
                                           f"checked-conclusion-binding declared as role {pin_role!r}"))
        elif citizen["schema"] in {"attachment-rule.v1", "attachment-rule.v2", "attachment-rule.v3", "attachment-rule.v4", "attachment-rule.v5", "attachment-rule.v6"}:
            if pin_role != "attachment-rule":
                issues.append(MemberIssue(pin["id"], pin["version"], "ROLE_MISMATCH",
                                           f"attachment-rule declared as role {pin_role!r}"))

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
        if citizen["schema"] in {"form-field.v1", "form-field.v2", "form-field.v3"}:
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
        if citizen["schema"] in {"form-field.v1", "form-field.v2", "form-field.v3"}:
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
        if citizen["schema"] in {
            "quantity-vocabulary.v1",
            "quantity-vocabulary.v2",
            "quantity-vocabulary.v3",
        }:
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
        # Schedule B interest-adjustment route: line 2b@v4 publishes taxable-total
        # after subtracting closed adjustment classes from the positive composition.
        # The selected composition citizen publishes the positive-total basis, not
        # taxable-total; resolve composition through the producer pin instead of
        # requiring a second selected version of the same composition id. This is a
        # structural fact about rule.form1040-line2b@v4 itself, not about which
        # package version adopts it, so no package-version gate is applied here.
        if comp_member is None and S == "tax.us.2025.interest.taxable-total":
            for pin, citizen in resolved:
                if (
                    citizen["schema"] in _RULE_ARTIFACT_SCHEMAS
                    and citizen.get("publishes") == S
                    and pin["id"] == "tax.us.2025.rule.form1040-line2b"
                    and pin["version"] == "v4"
                ):
                    r_comp = citizen.get("composition")
                    if not isinstance(r_comp, dict):
                        break
                    for cpin, ccitizen in resolved:
                        if (
                            cpin["role"] == "composition"
                            and cpin["id"] == r_comp.get("id")
                            and cpin["version"] == r_comp.get("version")
                            and ccitizen.get("publishes") == "tax.us.2025.interest.positive-total"
                        ):
                            comp_member = (cpin, ccitizen)
                            break
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
                v11_adjustment_route = (
                    rule_pin["id"] == "tax.us.2025.rule.form1040-line2b"
                    and rule_pin["version"] == "v4"
                )
                expected_adjustment_subtotals = {
                    subtotal for _family, subtotal in _V11_ADJUSTMENT_SLOTS
                } if v11_adjustment_route else set()
                expected_rule_requires = comp_constituents | expected_adjustment_subtotals
                if expected_rule_requires != rule_requires:
                    issues.append(MemberIssue(comp_pin["id"], comp_pin["version"], "COMPOSITION_SLOT_BIJECTION_MISMATCH",
                                               f"composition constituents {expected_rule_requires} do not match rule requires {rule_requires}"))
                family_slots: list[tuple[str, str, str]] = []
                for constituent in comp_citizen.get("constituents", []):
                    family_pin = constituent["source_family"]
                    family = next(
                        (
                            c for p, c in resolved
                            if c.get("schema") == "source-family.v1"
                            and p["id"] == family_pin["id"]
                            and p["version"] == family_pin["version"]
                        ),
                        None,
                    )
                    if family is None:
                        issues.append(MemberIssue(
                            comp_pin["id"], comp_pin["version"], "COMPOSITION_FAMILY_ABSENT",
                            f"composition family {(family_pin['id'], family_pin['version'])} is not an exact package member",
                        ))
                        continue
                    subtotal = constituent["authorizes_subtotal"]
                    if family["authorizes_subtotal"] != subtotal:
                        issues.append(MemberIssue(
                            comp_pin["id"], comp_pin["version"], "COMPOSITION_FAMILY_SUBTOTAL_MISMATCH",
                            f"composition pairs family {family['id']!r} with {subtotal!r}, not its authorized subtotal {family['authorizes_subtotal']!r}",
                        ))
                    family_slots.append((family["id"], family["version"], subtotal))
                if len(family_slots) != len(set(family_slots)):
                    issues.append(MemberIssue(
                        comp_pin["id"], comp_pin["version"], "COMPOSITION_SLOT_DUPLICATE",
                        "composition repeats a family/subtotal slot",
                    ))

                expected_subtotals = [slot[2] for slot in family_slots]
                expected_families = [slot[0] for slot in family_slots]
                if v11_adjustment_route:
                    expected_subtotals.extend(subtotal for _family, subtotal in _V11_ADJUSTMENT_SLOTS)
                    expected_families.extend(family for family, _subtotal in _V11_ADJUSTMENT_SLOTS)
                value_refs = list(_iter_ref_names(rule_citizen.get("value")))
                closure_reads = list(_iter_require_closed_source_sets(rule_citizen.get("when")))
                input_pins = [p["id"] for p in rule_citizen.get("pins", []) if p.get("role") == "input"]
                for actual, expected, code, label in (
                    (value_refs, expected_subtotals, "COMPOSITION_VALUE_REFS_MISMATCH", "value refs"),
                    (closure_reads, expected_families, "COMPOSITION_CLOSURE_READS_MISMATCH", "closure reads"),
                    (input_pins, expected_subtotals, "COMPOSITION_INPUT_PINS_MISMATCH", "input pins"),
                ):
                    if sorted(actual) != sorted(expected) or len(actual) != len(expected):
                        issues.append(MemberIssue(
                            rule_pin["id"], rule_pin["version"], code,
                            f"composition producer {label} {actual} do not form the exact declared slot surface {expected}",
                        ))

    # Interest-composition successor-graph coherence: each package version below
    # must select one exact successor graph across composition, line-2b,
    # form-field, and Schedule B content. Historical packages are deliberately
    # outside this additive gate. Composition/line-2b/Schedule-B mixing is
    # already caught by the slot-bijection checks above; the form-field content
    # successor carries no such structural join, so it needs this explicit
    # per-version coherence check.
    _successor_graphs: dict[str, tuple[str, dict[str, tuple[str, str]]]] = {
        "v9": ("K1_SUCCESSOR_GRAPH_MIXED", {
            "tax.us.2025.interest-composition": ("taxable-interest-composition.v1", "v2"),
            "tax.us.2025.rule.form1040-line2b": ("rule-artifact.v3", "v2"),
            "tax.us.2025.form1040.line-2b": ("form-field.v3", "v3"),
            "tax.us.2025.rule.attachment.schedule-b": ("attachment-rule.v2", "v2"),
        }),
        "v10": ("MD_SUCCESSOR_GRAPH_MIXED", {
            "tax.us.2025.interest-composition": ("taxable-interest-composition.v1", "v3"),
            "tax.us.2025.rule.form1040-line2b": ("rule-artifact.v3", "v3"),
            "tax.us.2025.form1040.line-2b": ("form-field.v3", "v4"),
            "tax.us.2025.rule.attachment.schedule-b": ("attachment-rule.v2", "v3"),
        }),
    }
    if package.get("id") == "tax.us.2025.package.core-calculations" and package.get("version") in _successor_graphs:
        pkg_version = str(package.get("version"))
        code, expected_successors = _successor_graphs[pkg_version]
        members_by_id = {pin["id"]: pin for pin in package["members"]}
        for member_id, (schema, version) in expected_successors.items():
            pin = members_by_id.get(member_id)
            if pin is None or pin.get("schema") != schema or pin.get("version") != version:
                issues.append(MemberIssue(
                    member_id, str(pin.get("version", "") if pin else ""), code,
                    f"{pkg_version} requires {member_id}@{version} under {schema}, got {pin!r}",
                ))

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
                # Only v3 can declare refs outside `requires`: conditional
                # dependency members are nested `ref` expressions in `when`.
                # v1/v2 keep their requires-only edge computation unchanged.
                if citizen["schema"] == "rule-artifact.v3":
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
            elif citizen["schema"] in {"form-field.v1", "form-field.v2", "form-field.v3"}:
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
            elif citizen["schema"] == "attachment-rule.v6":
                for part in citizen.get("itemizations", []):
                    authority = part.get("authority", {})
                    if authority.get("kind") == "composition":
                        composition_pin = authority.get("composition", {})
                        if composition_pin.get("id") in member_ids:
                            adj[m_id].add(composition_pin["id"])
                    for row_set in part.get("row_sets", []):
                        rows = row_set.get("rows", {})
                        family_pin = rows.get("source_family", {})
                        if family_pin.get("id") in member_ids:
                            adj[m_id].add(family_pin["id"])
                        member_pin = rows.get("member_fact_type", {})
                        if member_pin.get("id") in member_ids:
                            adj[m_id].add(member_pin["id"])
                    for adjustment in part.get("adjustment_rows", []):
                        rows = adjustment.get("rows", {})
                        family_pin = rows.get("source_family", {})
                        if family_pin.get("id") in member_ids:
                            adj[m_id].add(family_pin["id"])
                        member_pin = rows.get("member_fact_type", {})
                        if member_pin.get("id") in member_ids:
                            adj[m_id].add(member_pin["id"])
                for answer in citizen.get("completeness", {}).get("required_answers", []):
                    fact_pin = answer.get("fact_type", {})
                    if fact_pin.get("id") in member_ids:
                        adj[m_id].add(fact_pin["id"])
                requirement = citizen.get("requirement", {})
                for subtotal in requirement.get("subtotals", []):
                    for p_id in produced.get(subtotal, []):
                        adj[m_id].add(p_id)
                citation_pin = requirement.get("citation", {})
                if citation_pin.get("id") in member_ids:
                    adj[m_id].add(citation_pin["id"])
                threshold_pin = requirement.get("threshold_parameter", {})
                if threshold_pin.get("id") in member_ids:
                    adj[m_id].add(threshold_pin["id"])
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
            if citizen["schema"] in {"form-field.v1", "form-field.v2", "form-field.v3"}:
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

    # 9. Runtime universe guard (ADR-0035 production condition, adversary A2).
    # The paper unrepresentability becomes a mechanical check: every collect
    # must target the declared member fact type of a source family the package
    # carries, and no rule may consume recorded-non-composable content named
    # by a dividend-universe citizen. The collect-target half binds the
    # package-language generations that postdate ADR-0035 (artifact-package.v3
    # onward); the already-published v1/v2 instances are recorded history, the
    # same posture as the v1 closure-edge exemption above.
    universe_guard_active = package.get("schema") in {
        "artifact-package.v3",
        "artifact-package.v4",
        "artifact-package.v5",
        "artifact-package.v6",
        "artifact-package.v8",
        "artifact-package.v9",
        "artifact-package.v7",
        "artifact-package.v10",
        "artifact-package.v11",
        "artifact-package.v12",
        "artifact-package.v13",
        "artifact-package.v14",
    }
    source_family_members = {
        citizen["id"]: citizen["member_predicate"]["fact_type"]
        for _, citizen in resolved
        if citizen["schema"] == "source-family.v1"
    }
    recorded_non_composable: set[str] = set()
    composable_box2a_members: set[str] = set()
    composable_box12_members: set[str] = set()
    historical_recorded_boxes_v1 = False
    successor_box2a_member = False
    historical_recorded_box12 = False
    successor_box12_member = False
    for _, citizen in resolved:
        if citizen["schema"] == "dividend-universe.v1":
            recorded_non_composable.add(citizen["recorded_boxes_fact_type"]["id"])
        elif citizen["schema"] in {"dividend-universe.v2", "dividend-universe.v3"}:
            recorded_non_composable.add(citizen["recorded_boxes_fact_type"]["id"])
            for box in citizen.get("composable_boxes", []):
                family = box.get("family") or {}
                family_id = family.get("id")
                member = source_family_members.get(str(family_id))
                if member and box.get("box") == "2a":
                    composable_box2a_members.add(member)
                if member and box.get("box") == "12":
                    composable_box12_members.add(member)
        elif citizen["schema"] == "source-family.v1":
            if citizen.get("id") == "tax.us.2025.f1099div.12":
                composable_box12_members.add(citizen["member_predicate"]["fact_type"])
        if citizen["schema"] == "fact-type.v2":
            if (
                citizen.get("id") == "tax.us.2025.f1099div.recorded-boxes"
                and citizen.get("version") == "v1"
            ):
                historical_recorded_boxes_v1 = True
            if citizen.get("id") == "tax.us.2025.f1099div.box2a-capital-gain-distribution":
                successor_box2a_member = True
                composable_box2a_members.add(citizen["id"])
        if citizen["schema"] == "bundle.v2":
            for fact_type in citizen.get("fact_types", []):
                if (
                    fact_type.get("id") == "tax.us.2025.f1099div.recorded-boxes"
                    and fact_type.get("version") == "v1"
                ):
                    historical_recorded_boxes_v1 = True
                if fact_type.get("id") == "tax.us.2025.f1099div.box2a-capital-gain-distribution":
                    successor_box2a_member = True
                    composable_box2a_members.add(fact_type["id"])
                if fact_type.get("id") == "tax.us.2025.f1099div.box12-exempt-interest-dividends":
                    successor_box12_member = True
                if (
                    fact_type.get("id") == "tax.us.2025.f1099div.recorded-boxes"
                    and "12" in fact_type.get("value_schema", {}).get("properties", {})
                ):
                    historical_recorded_box12 = True
    # ADR-0050 decision 3: reject mixed historical recorded box-2a content and
    # successor family members in one adopted package graph.
    if historical_recorded_boxes_v1 and successor_box2a_member:
        issues.append(MemberIssue(
            package_id, package.get("version", ""), "MIXED_BOX2A_GRAPH",
            "package admits both historical recorded-boxes v1 (property 2a) and "
            "successor box-2a family members; exclusive graphs only",
        ))
    if historical_recorded_box12 and successor_box12_member:
        issues.append(MemberIssue(
            package_id, package.get("version", ""), "MIXED_BOX12_GRAPH",
            "package admits both historical recorded-boxes content with box 12 "
            "and successor box-12 family members; exclusive graphs only",
        ))
    for pin, citizen in resolved:
        if citizen["schema"] not in _RULE_ARTIFACT_SCHEMAS:
            continue
        collect_names: set[str] = set()
        for expr_key in ("when", "value"):
            for collect in _iter_collect_exprs(citizen[expr_key]):
                name = collect.get("name")
                if isinstance(name, str):
                    collect_names.add(name)
                collect_set = collect.get("source_set")
                if not universe_guard_active:
                    continue
                declared_member = source_family_members.get(str(collect_set))
                if declared_member is None:
                    issues.append(MemberIssue(pin["id"], pin["version"], "COLLECT_TARGET_NOT_FAMILY",
                                              f"collect names source_set {collect_set!r}, which no package source-family declares"))
                elif name != declared_member:
                    issues.append(MemberIssue(pin["id"], pin["version"], "COLLECT_TARGET_NOT_FAMILY",
                                              f"collect targets {name!r}, not the declared member fact type {declared_member!r} of family {collect_set!r}"))
        consumed = collect_names | set(citizen.get("requires", []))
        consumed.update(_iter_ref_names(citizen["when"]))
        consumed.update(_iter_ref_names(citizen["value"]))
        for forbidden in sorted(consumed & recorded_non_composable):
            issues.append(MemberIssue(pin["id"], pin["version"], "RECORDED_NON_COMPOSABLE_INPUT",
                                      f"rule consumes recorded-non-composable content {forbidden!r}; the dividend universe does not compose residual recorded boxes"))
        # ADR-0050 decision 6/7: line 9 and line 16 successors consume selected
        # publications only — never raw box-2a members via collect/ref.
        publishes = citizen.get("publishes", "")
        if publishes in {
            "tax.us.2025.income.total-income",
            "tax.us.2025.tax.total-tax",
        }:
            raw_box2a = sorted(consumed & composable_box2a_members)
            if raw_box2a:
                issues.append(MemberIssue(
                    pin["id"], pin["version"], "RAW_BOX2A_DOWNSTREAM_READ",
                    f"rule publishing {publishes!r} consumes raw box-2a members "
                    f"{raw_box2a}; selected line-7a publication only",
                ))
            raw_box12 = sorted(consumed & composable_box12_members)
            if raw_box12:
                issues.append(MemberIssue(
                    pin["id"], pin["version"], "RAW_BOX12_DOWNSTREAM_READ",
                    f"rule publishing {publishes!r} consumes raw box-12 members "
                    f"{raw_box12}; exempt-interest dividends remain reported-only",
                ))

    # 10. Attachment answer encoding guard (ADR-0036 production condition 2).
    # Completeness is presence-semantics only because every answer value is
    # truthy: the categorical all-truthy string domain pin is load-bearing, so
    # a boolean or otherwise falsy-encodable Part III answer fact type on an
    # attachment is rejected at admission.
    for pin, citizen in resolved:
        if citizen["schema"] not in {"attachment-rule.v1", "attachment-rule.v2", "attachment-rule.v3", "attachment-rule.v4", "attachment-rule.v5", "attachment-rule.v6"}:
            continue
        answers = list(citizen["completeness"]["required_answers"])
        for branch in citizen["completeness"].get("branch_requirements", []):
            answers.extend(branch.get("adds_required", []))
        for answer in answers:
            answer_pin = answer["fact_type"]
            answer_key = _corpus_key(answer_pin["id"], answer_pin["version"])
            fact_type = fact_types_by_key.get(answer_key)
            if fact_type is None:
                issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_ANSWER_FACT_TYPE_ABSENT",
                                          f"answer fact type {answer_key} not in package fact surface"))
                continue
            value_schema = fact_type.get("value_schema", {})
            domain = value_schema.get("enum")
            categorical = (
                list(value_schema) == ["enum"]
                and isinstance(domain, list)
                and len(domain) > 0
                and all(isinstance(v, str) and v for v in domain)
            )
            if not categorical:
                issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_ANSWER_NOT_CATEGORICAL",
                                          f"answer fact type {answer_pin['id']!r} must declare a categorical all-truthy string domain "
                                          f"(e.g. yes/no); boolean or falsy-valued encodings can short-circuit completeness"))
            # ADR-0055 Decision 1: a "value"-checked answer's `equals` must
            # itself be a value the fact type's own declared domain admits -
            # a required equality against an impossible value can never be
            # satisfied, so completeness could never be reached honestly.
            elif answer.get("check") == "value" and answer.get("equals") not in domain:
                issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_ANSWER_EQUALS_NOT_IN_DOMAIN",
                                          f"answer fact type {answer_pin['id']!r} check:value equals "
                                          f"{answer.get('equals')!r}, not in its own declared domain {domain}"))

    # 10b. attachment-rule.v2 authority and row-set admission. Schema shape
    # alone cannot prove that a row set belongs to its declared family or that
    # a composition-backed part is structurally complete.
    families_by_key = {
        (citizen["id"], citizen["version"]): citizen
        for _, citizen in resolved if citizen["schema"] == "source-family.v1"
    }
    compositions_by_key = {
        (citizen["id"], citizen["version"]): citizen
        for _, citizen in resolved if citizen["schema"] == "taxable-interest-composition.v1"
    }
    for pin, citizen in resolved:
        if citizen["schema"] not in {"attachment-rule.v2", "attachment-rule.v3", "attachment-rule.v4", "attachment-rule.v5", "attachment-rule.v6"}:
            continue
        for part in citizen["itemizations"]:
            actual_slots: list[tuple[str, str, str]] = []
            for row_set in part["row_sets"]:
                rows = row_set["rows"]
                family_pin = rows["source_family"]
                family = families_by_key.get((family_pin["id"], family_pin["version"]))
                if family is None:
                    issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_ROW_FAMILY_ABSENT",
                                              f"part {part['part_id']!r} names absent family {family_pin}"))
                    continue
                if rows["member_fact_type"]["id"] != family["member_predicate"]["fact_type"]:
                    issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_ROW_MEMBER_MISMATCH",
                                              f"part {part['part_id']!r} row member does not equal family {family['id']!r} canonical predicate"))
                if row_set["subtotal_symbol"] != family["authorizes_subtotal"]:
                    issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_ROW_SUBTOTAL_MISMATCH",
                                              f"part {part['part_id']!r} row subtotal is not authorized by family {family['id']!r}"))
                actual_slots.append((family["id"], family["version"], row_set["subtotal_symbol"]))
            authority = part["authority"]
            if authority["kind"] == "single_family":
                family_pin = authority["source_family"]
                family = families_by_key.get((family_pin["id"], family_pin["version"]))
                authority_slots: list[tuple[str, str, str]] = [] if family is None else [(family["id"], family["version"], family["authorizes_subtotal"])]
                if actual_slots != authority_slots:
                    issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_SINGLE_FAMILY_BIJECTION_MISMATCH",
                                              f"part {part['part_id']!r} row sets {actual_slots} do not exactly equal authority {authority_slots}"))
                if family is not None and part["tie_out"]["line_symbol"] != family["authorizes_subtotal"]:
                    issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_LINE_AUTHORITY_MISMATCH",
                                              f"part {part['part_id']!r} line symbol does not equal its family subtotal"))
            else:
                comp_pin = authority["composition"]
                comp = compositions_by_key.get((comp_pin["id"], comp_pin["version"]))
                authority_slots = [] if comp is None else [
                    (slot["source_family"]["id"], slot["source_family"]["version"], slot["authorizes_subtotal"])
                    for slot in comp["constituents"]
                ]
                if sorted(actual_slots) != sorted(authority_slots) or len(actual_slots) != len(authority_slots):
                    issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_COMPOSITION_BIJECTION_MISMATCH",
                                              f"part {part['part_id']!r} row sets {actual_slots} do not exactly equal composition slots {authority_slots}"))
                if comp is None:
                    issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_COMPOSITION_ABSENT",
                                              f"part {part['part_id']!r} names absent composition {comp_pin}"))
                elif part["tie_out"]["line_symbol"] != comp["publishes"]:
                    subtractive_positive_basis = (
                        citizen["schema"] == "attachment-rule.v6"
                        and part["tie_out"].get("operation") == "subtract"
                        and bool(part.get("adjustment_rows"))
                        and comp.get("publishes") == "tax.us.2025.interest.positive-total"
                        and part["tie_out"]["line_symbol"] == "tax.us.2025.interest.taxable-total"
                    )
                    if not subtractive_positive_basis:
                        issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_LINE_AUTHORITY_MISMATCH",
                                                  f"part {part['part_id']!r} line symbol does not equal composition publication"))

    # 10c. attachment-rule.v6 keeps the v2 positive row contract and adds a
    # closed, typed subtractive surface.  The schema fixes the vocabulary;
    # admission fixes the joins and the signed whole-part surface.
    for pin, citizen in resolved:
        if citizen["schema"] != "attachment-rule.v6":
            continue
        for part in citizen["itemizations"]:
            actual_positive = [row_set["subtotal_symbol"] for row_set in part["row_sets"]]
            actual_adjustments = [row["subtotal_symbol"] for row in part["adjustment_rows"]]
            tie_out = part["tie_out"]
            if tie_out["positive_subtotals"] != actual_positive:
                issues.append(MemberIssue(
                    pin["id"], pin["version"], "ATTACHMENT_TIE_OUT_SURFACE_MISMATCH",
                    f"part {part['part_id']!r} positive tie-out surface does not equal row sets",
                ))
            if tie_out["adjustment_subtotals"] != actual_adjustments:
                issues.append(MemberIssue(
                    pin["id"], pin["version"], "ATTACHMENT_TIE_OUT_SURFACE_MISMATCH",
                    f"part {part['part_id']!r} adjustment tie-out surface does not equal adjustment rows",
                ))
            if tie_out["operation"] != "subtract":
                issues.append(MemberIssue(
                    pin["id"], pin["version"], "ATTACHMENT_TIE_OUT_OPERATION_INVALID",
                    f"part {part['part_id']!r} must use the existing subtract vocabulary",
                ))
            actual_slots = []
            for row_set in part["row_sets"]:
                rows = row_set["rows"]
                family_pin = rows["source_family"]
                family = families_by_key.get((family_pin["id"], family_pin["version"]))
                if family is None:
                    issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_ROW_FAMILY_ABSENT",
                                              f"part {part['part_id']!r} names absent family {family_pin}"))
                    continue
                if rows["member_fact_type"]["id"] != family["member_predicate"]["fact_type"]:
                    issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_ROW_MEMBER_MISMATCH",
                                              f"part {part['part_id']!r} row member does not equal family {family['id']!r} canonical predicate"))
                if row_set["subtotal_symbol"] != family["authorizes_subtotal"]:
                    issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_ROW_SUBTOTAL_MISMATCH",
                                              f"part {part['part_id']!r} row subtotal is not authorized by family {family['id']!r}"))
                actual_slots.append((family["id"], family["version"], row_set["subtotal_symbol"]))
            for adjustment in part["adjustment_rows"]:
                expected_binding = _V3_ADJUSTMENT_BINDINGS.get(adjustment["kind"])
                rows = adjustment["rows"]
                family_pin = rows["source_family"]
                if expected_binding is not None:
                    expected_label, expected_family_token = expected_binding
                    if adjustment["label"] != expected_label:
                        issues.append(MemberIssue(
                            pin["id"], pin["version"], "ATTACHMENT_ADJUSTMENT_LABEL_MISMATCH",
                            f"part {part['part_id']!r} kind {adjustment['kind']!r} requires label {expected_label!r}",
                        ))
                    actual_family_token = family_pin["id"].rsplit(".", 1)[-1]
                    if actual_family_token != expected_family_token:
                        issues.append(MemberIssue(
                            pin["id"], pin["version"], "ATTACHMENT_ADJUSTMENT_AUTHORITY_MISMATCH",
                            f"part {part['part_id']!r} kind {adjustment['kind']!r} requires the {expected_family_token!r} class authority, got {family_pin!r}",
                        ))
                family = families_by_key.get((family_pin["id"], family_pin["version"]))
                if family is None:
                    issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_ADJUSTMENT_FAMILY_ABSENT",
                                              f"part {part['part_id']!r} names absent adjustment family {family_pin}"))
                    continue
                if rows["member_fact_type"]["id"] != family["member_predicate"]["fact_type"]:
                    issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_ADJUSTMENT_MEMBER_MISMATCH",
                                              f"part {part['part_id']!r} adjustment member does not equal family {family['id']!r} canonical predicate"))
                if adjustment["subtotal_symbol"] != family["authorizes_subtotal"]:
                    issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_ADJUSTMENT_SUBTOTAL_MISMATCH",
                                              f"part {part['part_id']!r} adjustment subtotal is not authorized by family {family['id']!r}"))
            if (
                pin["id"] == "tax.us.2025.rule.attachment.schedule-b"
                and pin["version"] == "v4"
            ):
                actual_adjustment_slots = [
                    (adjustment["rows"]["source_family"]["id"], adjustment["subtotal_symbol"])
                    for adjustment in part["adjustment_rows"]
                ]
                expected_adjustment_slots = list(_V11_ADJUSTMENT_SLOTS) if part["part_id"] == "part-i-interest" else []
                if sorted(actual_adjustment_slots) != sorted(expected_adjustment_slots) or len(actual_adjustment_slots) != len(expected_adjustment_slots):
                    issues.append(MemberIssue(
                        pin["id"], pin["version"], "ATTACHMENT_ADJUSTMENT_CLASS_SURFACE_MISMATCH",
                        f"v11 Schedule B part {part['part_id']!r} adjustment slots {actual_adjustment_slots} do not equal the exact three-class surface",
                    ))
            authority = part["authority"]
            if authority["kind"] == "single_family":
                family_pin = authority["source_family"]
                family = families_by_key.get((family_pin["id"], family_pin["version"]))
                authority_slots = [] if family is None else [(family["id"], family["version"], family["authorizes_subtotal"])]
                if actual_slots != authority_slots:
                    issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_SINGLE_FAMILY_BIJECTION_MISMATCH",
                                              f"part {part['part_id']!r} positive row sets do not equal authority"))
            else:
                comp_pin = authority["composition"]
                comp = compositions_by_key.get((comp_pin["id"], comp_pin["version"]))
                authority_slots = [] if comp is None else [
                    (slot["source_family"]["id"], slot["source_family"]["version"], slot["authorizes_subtotal"])
                    for slot in comp["constituents"]
                ]
                if sorted(actual_slots) != sorted(authority_slots) or len(actual_slots) != len(authority_slots):
                    issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_COMPOSITION_BIJECTION_MISMATCH",
                                              f"part {part['part_id']!r} positive row sets do not equal composition slots"))
                if comp is None:
                    issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_COMPOSITION_ABSENT",
                                              f"part {part['part_id']!r} names absent composition {comp_pin}"))
                elif tie_out["line_symbol"] != comp["publishes"]:
                    subtractive_positive_basis = (
                        citizen["schema"] == "attachment-rule.v6"
                        and tie_out.get("operation") == "subtract"
                        and bool(part.get("adjustment_rows"))
                        and comp.get("publishes") == "tax.us.2025.interest.positive-total"
                        and tie_out["line_symbol"] == "tax.us.2025.interest.taxable-total"
                    )
                    if not subtractive_positive_basis:
                        issues.append(MemberIssue(pin["id"], pin["version"], "ATTACHMENT_LINE_AUTHORITY_MISMATCH",
                                                  f"part {part['part_id']!r} line symbol does not equal composition publication"))

    # 10a. Declared-absence CMDN member domain guard (ADR-0038 production
    # condition 1): a conditional_dependency_set member fact type that the
    # *same rule* also reads categorically (a category_literal naming it)
    # must declare the categorical {yes, no} domain, never boolean or an
    # open string domain - the same categorical-domain-pin load-bearing
    # pattern check 10 established for attachment answers, generalized to
    # CMDN's second declared-absence consumer. Scoped to category_literal-
    # referenced members only, never every CMDN member unconditionally:
    # ADR-0037's own generic substrate members are ordinary numeric/other
    # reads with no categorical shape at all, and must stay domain-agnostic
    # (this guard is additive to ADR-0038's own instantiation, not a
    # retroactive constraint on the substrate ADR-0037 already committed
    # and reviewed). A member's symbol name resolves to its fact type id
    # through a package input_binding when one is declared, falling back to
    # the legacy demo-path convention (symbol == fact type id) every other
    # unbound rule-artifact.v3 ref already relies on (see marshal.py).
    binding_fact_types_local = {
        binding["symbol"]: binding["fact_type"]["id"]
        for binding in package.get("input_bindings", [])
    }
    fact_types_by_id: dict[str, dict[str, Any]] = {}
    for (ft_id, _ft_version), ft in fact_types_by_key.items():
        fact_types_by_id.setdefault(ft_id, ft)
    for pin, citizen in resolved:
        if citizen["schema"] != "rule-artifact.v3":
            continue
        member_names = set(_iter_cds_member_names(citizen["when"])) | set(
            _iter_cds_member_names(citizen["value"])
        )
        categorical_fact_types = set(_iter_category_literal_fact_types(citizen["when"])) | set(
            _iter_category_literal_fact_types(citizen["value"])
        )
        for name in sorted(member_names):
            fact_type_id = binding_fact_types_local.get(name, name)
            if fact_type_id not in categorical_fact_types:
                continue
            fact_type = fact_types_by_id.get(fact_type_id)
            if fact_type is None:
                issues.append(MemberIssue(pin["id"], pin["version"], "CONDITIONAL_DEPENDENCY_MEMBER_FACT_TYPE_ABSENT",
                                          f"conditional_dependency_set member {name!r} names no fact type "
                                          f"in the package fact surface"))
                continue
            value_schema = fact_type.get("value_schema", {})
            domain = value_schema.get("enum")
            yes_no = (
                list(value_schema) == ["enum"]
                and isinstance(domain, list)
                and set(domain) == {"yes", "no"}
            )
            if not yes_no:
                issues.append(MemberIssue(pin["id"], pin["version"], "CONDITIONAL_DEPENDENCY_MEMBER_NOT_YES_NO",
                                          f"conditional_dependency_set member fact type {fact_type_id!r} must "
                                          f"declare the categorical {{yes, no}} domain, never boolean or an "
                                          f"open string domain"))

    # 11. Unique output ownership (decision 7)
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
