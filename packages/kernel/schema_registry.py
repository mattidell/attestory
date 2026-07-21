"""Schema registry: versioned JSON Schema citizens with strict validation.

Per Article 9 (Canon) and ADR-0003: a published schema version is
immutable (enforced by checksum manifest), instances name their schema
version, and validation is strict with rejection — no tolerant reading,
no coercion, no repair.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Sequence

import jsonschema

KERNEL_SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas" / "kernel"
PUBLISHED_MANIFEST_NAME = "published.json"


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
            digest = _sha256(path)
            if digest != manifest[path.name]:
                raise SchemaRegistryError(
                    f"published schema was mutated: {path.name} "
                    f"(expected {manifest[path.name][:12]}..., found {digest[:12]}...)"
                )
            schema_id = path.name.removesuffix(".schema.json")
            if schema_id in self._schemas:
                raise SchemaRegistryError(f"duplicate schema id across directories: {schema_id}")
            document: dict[str, Any] = json.loads(path.read_text("utf-8"))
            try:
                jsonschema.Draft202012Validator.check_schema(document)
            except jsonschema.SchemaError as exc:
                raise SchemaRegistryError(
                    f"schema document is not valid JSON Schema: {path.name}: {exc.message}"
                ) from exc
            self._schemas[schema_id] = document
            self._validators[schema_id] = jsonschema.Draft202012Validator(document)

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
        errors = sorted(
            self._validators[schema_id].iter_errors(instance),
            key=lambda e: list(e.absolute_path),
        )
        if errors:
            raise SchemaValidationError(
                schema_id,
                [f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}" for e in errors],
            )

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
