"""Schema registry: versioned JSON Schema citizens with strict validation.

Per Article 9 (Canon) and ADR-0003: a published schema version is
immutable (enforced by checksum manifest), instances name their schema
version, and validation is strict with rejection — no tolerant reading,
no coercion, no repair.
"""

from __future__ import annotations

import hashlib
import json
from collections import OrderedDict
from pathlib import Path
from typing import Any, Sequence

import jsonschema

KERNEL_SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas" / "kernel"
PUBLISHED_MANIFEST_NAME = "published.json"

# Two content-addressed memos. Both exist only because loading and validating
# are *pure* functions of bytes: a published schema version is immutable
# (Article 9, ADR-0003) and validation neither coerces nor repairs, so the same
# (schema bytes, instance) pair can only ever reach the same verdict.
#
# Every key is a content digest, never a path or a schema id alone. That is the
# property that keeps the memo honest: a mutated published file hashes
# differently, so it *misses* both caches and takes the full uncached path that
# raises. Keying on paths would let a mutation silently reuse the pre-mutation
# compile — the exact failure `tests/test_schema_registry.py` exists to catch.
#
# `_COMPILED_SCHEMAS` skips re-parsing and re-compiling 113 schema documents on
# every SchemaRegistry construction. `_VALIDATION_VERDICTS` skips re-validating
# content documents that the run has already checked; it is bounded because a
# long-lived process (the coordinator, a test session) would otherwise retain
# every instance it ever saw.
_COMPILED_SCHEMAS: dict[tuple[str, str], tuple[dict[str, Any], jsonschema.Draft202012Validator]] = {}
_VALIDATION_VERDICTS: OrderedDict[tuple[str, str, str], tuple[str, ...] | None] = OrderedDict()
_VALIDATION_VERDICTS_MAX = 50_000


def clear_caches() -> None:
    """Drop both memos. For tests that need a cold registry; never required
    for correctness, since every key is content-addressed."""
    _COMPILED_SCHEMAS.clear()
    _VALIDATION_VERDICTS.clear()


class SchemaRegistryError(Exception):
    """A defect in the schema set itself (missing, mutated, malformed)."""


class SchemaValidationError(Exception):
    """An instance does not conform to its declared schema version."""

    def __init__(self, schema_id: str, errors: list[str]) -> None:
        self.schema_id = schema_id
        self.errors = errors
        summary = "; ".join(errors[:3])
        super().__init__(f"instance does not conform to {schema_id}: {summary}")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class SchemaRegistry:
    """Loads a directory of published schema versions and validates instances.

    The directory must contain a manifest (``published.json``) mapping
    each schema filename to its sha256. Loading verifies every published
    file matches its checksum and every schema file is published —
    a mutated or unlisted schema is a registry defect, not a warning.
    """

    def __init__(self, schema_dir: Path | Sequence[Path] | None = None) -> None:
        if schema_dir is None:
            self._dirs: list[Path] = [KERNEL_SCHEMA_DIR]
        elif isinstance(schema_dir, Path):
            self._dirs = [schema_dir]
        else:
            self._dirs = list(schema_dir)
        self._schemas: dict[str, dict[str, Any]] = {}
        self._validators: dict[str, jsonschema.Draft202012Validator] = {}
        # schema id -> sha256 of the published bytes this registry loaded.
        # Folded into the validation memo key so that two registries publishing
        # the same schema id from different bytes cannot share a verdict.
        self._digests: dict[str, str] = {}
        self.family_member_predicates: set[str] = set()
        # Domain-declared subset invariants (e.g. ADR-0035 decision 4: 1099-DIV
        # box 1b <= box 1a per statement). Maps a subordinate fact type id to
        # the dominant fact type id it must never exceed for the same key
        # suffix. Empty by default; a tax-layer registry populates pairs. The
        # kernel enforces the relation generically, never naming a domain.
        self.subset_invariant_pairs: dict[str, str] = {}
        # Bidirectional admission-locus contradiction rules (ADR-0038 decision
        # 5, reusing this same mechanism rather than a new admitted citizen):
        # a categorical declaration value and a derived signal read from a
        # *different* recorded fact type's value may never both be current.
        # Each entry names the declaration fact type and its contradicting
        # value, plus the recorded fact type and the field within its value
        # whose presence (non-null on any current instance) raises the
        # signal. Empty by default; a tax-layer registry populates entries.
        # The kernel enforces the relation generically, never naming a domain.
        self.declaration_signal_contradictions: list[dict[str, str]] = []
        # Companion-presence pairs: subordinate member fact type -> one companion
        # fact-type id or a list of companion fact-type ids sharing the same
        # identity-key suffix. Empty by default; a tax-layer registry populates
        # pairs. The kernel enforces presence generically and never names a
        # domain. Optional companion_value_domains restricts admitted values
        # for selected companion types (e.g. absence/zero).
        self.companion_presence_pairs: dict[str, str | list[str]] = {}
        self.companion_value_domains: dict[str, frozenset[object]] = {}
        # Same-statement equality witnesses: subordinate member fact type ->
        # numeric companion fact type.  The kernel enforces the relation
        # generically at finding admission; domain loaders provide the map.
        self.companion_equality_pairs: dict[str, str] = {}
        # Migration id -> resolution policy (e.g. "resolved-required"). Empty
        # by default: apply_migration_adoption's unconditional-adoption
        # behavior is unchanged for any migration id absent from this map.
        # A domain loader populates entries (ADR-0072 Decision 4): resolution
        # for a nonzero predecessor claim is withdrawal or a genuinely-zero
        # correction, never a forced false zero; the kernel enforces the
        # policy generically and never names a migration or fact-type id.
        self.migration_resolution_policies: dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        # A registry may span several published directories (e.g. the kernel and
        # derivation schema families sharing one workspace act log). Each is its
        # own checksum-manifested set; schema ids must be unique across them.
        for directory in self._dirs:
            self._load_directory(directory)

    def _load_directory(self, directory: Path) -> None:
        manifest_path = directory / PUBLISHED_MANIFEST_NAME
        if not manifest_path.exists():
            raise SchemaRegistryError(f"missing schema manifest: {manifest_path}")
        manifest: dict[str, str] = json.loads(manifest_path.read_text("utf-8"))

        schema_files = sorted(directory.glob("*.schema.json"))
        listed = set(manifest)
        present = {p.name for p in schema_files}
        for unlisted in sorted(present - listed):
            raise SchemaRegistryError(f"schema file not published in manifest: {unlisted}")
        for missing in sorted(listed - present):
            raise SchemaRegistryError(f"published schema file is missing: {missing}")

        for path in schema_files:
            # Every file is still hashed on every load: this is the
            # immutability check itself, and it is also the cache key below.
            # Nothing here is skipped by memoization.
            digest = _sha256(path)
            if digest != manifest[path.name]:
                raise SchemaRegistryError(
                    f"published schema was mutated: {path.name} "
                    f"(expected {manifest[path.name][:12]}..., found {digest[:12]}...)"
                )
            schema_id = path.name.removesuffix(".schema.json")
            if schema_id in self._schemas:
                raise SchemaRegistryError(f"duplicate schema id across directories: {schema_id}")
            self._digests[schema_id] = digest
            compiled = _COMPILED_SCHEMAS.get((schema_id, digest))
            if compiled is None:
                document: dict[str, Any] = json.loads(path.read_text("utf-8"))
                try:
                    jsonschema.Draft202012Validator.check_schema(document)
                except jsonschema.SchemaError as exc:
                    raise SchemaRegistryError(
                        f"schema document is not valid JSON Schema: {path.name}: {exc.message}"
                    ) from exc
                # Draft202012Validator resolves local ``$ref`` against ``$id``.
                # Relative family-scoped ids like ``kernel/fact-type.v2`` make
                # jsonschema 4.10 join the fragment into a doubled path
                # (``kernel/kernel/fact-type.v2``) and fail RefResolution. The
                # published document bytes stay intact for checksum immutability;
                # only the in-memory validator drops ``$id`` so ``#/$defs/...``
                # refs resolve against the document root.
                validator_document = {
                    key: value for key, value in document.items() if key != "$id"
                }
                compiled = (document, jsonschema.Draft202012Validator(validator_document))
                # Keyed on (schema id, digest): two registries may publish the
                # same id with different bytes and must never share a compile.
                _COMPILED_SCHEMAS[(schema_id, digest)] = compiled
            self._schemas[schema_id] = compiled[0]
            self._validators[schema_id] = compiled[1]

    def schema_ids(self) -> list[str]:
        return sorted(self._schemas)

    def get(self, schema_id: str) -> dict[str, Any]:
        if schema_id not in self._schemas:
            raise SchemaRegistryError(f"no published schema version: {schema_id}")
        return self._schemas[schema_id]

    def validate(self, schema_id: str, instance: object) -> None:
        """Strictly validate ``instance`` against a published schema version.

        Raises SchemaValidationError listing every violation. Never
        coerces, defaults, or repairs.
        """
        if schema_id not in self._validators:
            raise SchemaRegistryError(f"no published schema version: {schema_id}")

        # The memo key is (bytes of the schema, canonical bytes of the
        # instance). An instance that cannot be canonically serialized is not
        # cached at all rather than keyed on a lossy stand-in — a wrong key is
        # far worse here than a cache miss.
        key: tuple[str, str, str] | None
        try:
            key = (
                self._digests[schema_id],
                schema_id,
                json.dumps(instance, sort_keys=True, separators=(",", ":"), allow_nan=False),
            )
        except (TypeError, ValueError, KeyError):
            key = None

        if key is not None and key in _VALIDATION_VERDICTS:
            _VALIDATION_VERDICTS.move_to_end(key)
            remembered = _VALIDATION_VERDICTS[key]
            if remembered is not None:
                raise SchemaValidationError(schema_id, list(remembered))
            return

        errors = sorted(
            self._validators[schema_id].iter_errors(instance),
            key=lambda e: list(e.absolute_path),
        )
        messages = [
            f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}" for e in errors
        ]
        if key is not None:
            _VALIDATION_VERDICTS[key] = tuple(messages) if messages else None
            if len(_VALIDATION_VERDICTS) > _VALIDATION_VERDICTS_MAX:
                _VALIDATION_VERDICTS.popitem(last=False)
        if messages:
            raise SchemaValidationError(schema_id, messages)

    def validate_declared(self, instance: dict[str, Any]) -> str:
        """Validate an instance against the schema version it names.

        Every citizen names its schema (Article 9); an instance without
        a declaration is rejected outright.
        """
        declared = instance.get("schema")
        if not isinstance(declared, str):
            raise SchemaValidationError("<undeclared>", ["instance names no schema version"])
        self.validate(declared, instance)
        return declared


def write_manifest(schema_dir: Path) -> dict[str, str]:
    """Publish every schema file in a directory by recording checksums.

    Tooling helper for adding new schema versions; republishing an
    existing file with different bytes is the immutability violation the
    registry exists to catch, so callers must only ever add entries.
    """
    manifest = {
        path.name: _sha256(path) for path in sorted(schema_dir.glob("*.schema.json"))
    }
    manifest_path = schema_dir / PUBLISHED_MANIFEST_NAME
    existing: dict[str, str] = {}
    if manifest_path.exists():
        existing = json.loads(manifest_path.read_text("utf-8"))
    for name, digest in existing.items():
        if name in manifest and manifest[name] != digest:
            raise SchemaRegistryError(
                f"refusing to republish mutated schema: {name}; publish a new version instead"
            )
        if name not in manifest:
            raise SchemaRegistryError(f"refusing to unpublish schema: {name}")
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", "utf-8")
    return manifest
