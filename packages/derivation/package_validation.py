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

from dataclasses import dataclass
from typing import Any, Iterable

from packages.kernel.schema_registry import SchemaValidationError
from packages.derivation.loader import DerivationSchemas, PACKAGE_SCHEMA

_RULE_ROLES = frozenset({"computation", "applicability", "field-mapping", "cross-form-bridge"})
_SCOPE_KEYS = ("tax_year", "jurisdiction", "family")


@dataclass(frozen=True)
class MemberIssue:
    """One thing wrong with one member, named so a record can carry it."""

    member_id: str
    version: str
    code: str
    detail: str


@dataclass(frozen=True)
class PackageValidation:
    """A contained validation outcome for one package against a corpus."""

    package_id: str
    ok: bool
    issues: tuple[MemberIssue, ...]
    output_owners: dict[str, str]


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


def validate_package(
    package: dict[str, Any],
    corpus: dict[tuple[str, str], dict[str, Any]],
    schemas: DerivationSchemas,
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
        resolved.append((pin, citizen))

    member_ids = {pin["id"] for pin in package["members"]}
    produced: dict[str, list[str]] = {}

    for pin, citizen in resolved:
        pin_role = pin["role"]
        # Role agreement: the package member role must equal the citizen's own
        # role (rules) or be "parameter" (parameter declarations). This is the
        # one-role-vocabulary cross-position check (decision 9): the same token
        # means the same thing in the package and in the artifact.
        if citizen["schema"] in {"rule-artifact.v1", "rule-artifact.v2"}:
            if pin_role != citizen["role"]:
                issues.append(MemberIssue(pin["id"], pin["version"], "ROLE_MISMATCH",
                                           f"package role {pin_role!r} != artifact role {citizen['role']!r}"))
        elif citizen["schema"] == "parameter-declaration.v1":
            if pin_role != "parameter":
                issues.append(MemberIssue(pin["id"], pin["version"], "ROLE_MISMATCH",
                                           f"parameter member declared as {pin_role!r}"))

        # Scope as content (decision 6): member scope must match package scope.
        if "scope" in citizen:
            member_scope = {key: citizen.get("scope", {}).get(key) for key in _SCOPE_KEYS}
            if member_scope != package_scope:
                issues.append(MemberIssue(pin["id"], pin["version"], "SCOPE_MISMATCH",
                                          f"member scope {member_scope} != package scope {package_scope}"))

        if citizen["schema"] in {"rule-artifact.v1", "rule-artifact.v2"}:
            produced.setdefault(citizen["publishes"], []).append(pin["id"])
            # Reference closure (decision 6): every parameter/table a member
            # consults must itself be a member.
            for ref in set(_iter_parameter_and_table_refs(citizen["when"])) | set(
                _iter_parameter_and_table_refs(citizen["value"])
            ):
                if ref not in member_ids:
                    issues.append(MemberIssue(pin["id"], pin["version"], "CLOSURE_MISSING_PARAMETER",
                                              f"references {ref!r}, absent from package"))

    # Unique output ownership (decision 7): a symbol with more than one
    # producer is a conflict unless the package declares its resolution.
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
    )
