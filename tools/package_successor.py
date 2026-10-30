"""Construct a package successor in memory; this does not publish it."""

from __future__ import annotations

import copy
import argparse
import ctypes
import hashlib
import json
import os
import re
import secrets
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import (
    PackageIntegrityError, citizen_checksum, load_published_citizen_checksums,
    load_published_package_checksums, package_instance_checksum, validate_package,
    verify_published_package,
)
from packages.kernel.schema_registry import SchemaRegistryError, SchemaValidationError


class SuccessorError(ValueError):
    """The declared successor cannot be constructed safely."""


@dataclass(frozen=True)
class SuccessorResult:
    package: bytes
    registry: bytes
    release: bytes
    inherited_inconsistencies: tuple[tuple[str, str], ...]


def _version(value: str) -> int:
    if not re.fullmatch(r"v[1-9][0-9]*", value):
        raise SuccessorError(f"invalid version: {value}")
    return int(value[1:])


def _key(value: Mapping[str, Any]) -> tuple[str, str]:
    identity, version = value.get("id"), value.get("version")
    if not isinstance(identity, str) or not isinstance(version, str):
        raise SuccessorError("identity needs string id and version")
    return (identity, version)


def _registry_checks(raw: bytes) -> tuple[dict[tuple[str, str], str], dict[tuple[str, str], str]]:
    """Use both existing path-based loaders against one owned temporary snapshot."""
    document = json.loads(raw)
    if not isinstance(document, dict) or "citizens" not in document or "packages" not in document:
        raise SuccessorError("registry must contain citizens and packages arrays")
    with tempfile.NamedTemporaryFile(prefix="package-successor-registry-") as snapshot:
        snapshot.write(raw)
        snapshot.flush()
        try:
            packages = load_published_package_checksums(Path(snapshot.name))
            citizens = load_published_citizen_checksums(Path(snapshot.name))
        except PackageIntegrityError as exc:
            raise SuccessorError(str(exc).split(": ", 1)[-1]) from exc
    return packages, citizens


def _encode(value: Any) -> bytes:
    return (json.dumps(value, indent=2) + "\n").encode("utf-8")


def _member_index(members: list[dict[str, Any]], key: tuple[str, str]) -> int:
    found = [i for i, member in enumerate(members) if _key(member) == key]
    if len(found) != 1:
        raise SuccessorError(f"member must occur exactly once: {key}")
    return found[0]


def _validate(package: dict[str, Any], package_checksums: Mapping[tuple[str, str], str],
              citizen_checksums: Mapping[tuple[str, str], str],
              corpus: dict[tuple[str, str], dict[str, Any]], schemas: DerivationSchemas,
              inherited: dict[tuple[str, str], dict[str, Any]] | None = None,
              predecessor_checksums: Mapping[tuple[str, str], str] | None = None) -> tuple[tuple[str, str], ...]:
    verify_published_package(package, package_checksums)
    inconsistencies = []
    for pin in package["members"]:
        body = corpus.get(_key(pin))
        if body is None:
            raise SuccessorError(f"missing member: {_key(pin)}")
        if _key(body) != _key(pin):
            raise SuccessorError(f"member identity mismatch: {_key(pin)}")
        if body.get("schema") != pin.get("schema"):
            key = _key(pin)
            if inherited is not None and (inherited.get(key) != pin or predecessor_checksums is None or predecessor_checksums.get(key) != citizen_checksum(body)):
                raise SuccessorError(f"schema-pin mismatch: {key}")
            if inherited is None and citizen_checksums.get(key) != citizen_checksum(body):
                raise SuccessorError(f"schema-pin mismatch with unverified body: {key}")
            inconsistencies.append(key)
    outcome = validate_package(package, corpus, schemas, citizen_checksums)
    if not outcome.ok:
        raise SuccessorError(f"invalid package: {outcome.issues}")
    return tuple(inconsistencies)


def build_successor(package: dict[str, Any], registry_bytes: bytes, release: dict[str, Any],
                    corpus: dict[tuple[str, str], dict[str, Any]], changes: dict[str, Any],
                    schemas: DerivationSchemas | None = None) -> SuccessorResult:
    """Return package, registry and release bytes from an explicit change set.

    Each member edit is an add, remove or replace; additions and replacements
    carry complete member pins and an optional ``before`` anchor. Registry
    additions follow changed members, with an optional per-member anchor.
    """
    allowed = {"package_version", "release_version", "schema", "members", "entrypoints",
               "bindings", "binding_sort", "admitted_schemas", "release_key_order", "registry_sort", "registry_tail", "registry_new_key_order"}
    if set(changes) - allowed:
        raise SuccessorError("unknown change-set field")
    for name in ("package_version", "release_version"):
        if not isinstance(changes.get(name), str):
            raise SuccessorError(f"{name} must be a string")
    for name in ("members", "entrypoints", "bindings", "admitted_schemas"):
        if name in changes and (not isinstance(changes[name], list) or any(not isinstance(edit, dict) for edit in changes[name])):
            raise SuccessorError(f"{name} must be a list of edits")
    for name, supported in (("binding_sort", "symbol"), ("registry_sort", "id_version")):
        if name in changes and changes[name] != supported:
            raise SuccessorError(f"unsupported {name}")
    if "schema" in changes and (not isinstance(changes["schema"], str) or not changes["schema"]):
        raise SuccessorError("schema must be a nonempty string")
    for name, keys in (("registry_new_key_order", {"id", "version", "checksum"}),
                       ("release_key_order", {"id", "version", "schema", "package_registry_sha256"})):
        if name in changes:
            order = changes[name]
            if not isinstance(order, list) or not all(isinstance(key, str) for key in order) or len(order) != len(keys) or set(order) != keys:
                raise SuccessorError(f"invalid {name}")
    if "registry_tail" in changes:
        tail = changes["registry_tail"]
        if (not isinstance(tail, list) or not tail or any(not isinstance(item, list) or len(item) != 2
                or not all(isinstance(part, str) and part for part in item) for item in tail)):
            raise SuccessorError("invalid registry_tail")
        if "registry_sort" not in changes:
            raise SuccessorError("registry tail requires registry sort")
    schemas = schemas or DerivationSchemas()
    registry = json.loads(registry_bytes)
    schemas.validate_declared(release)
    if release["package_registry_sha256"] != hashlib.sha256(registry_bytes).hexdigest():
        raise SuccessorError("release registry hash mismatch")
    package_checksums, predecessor_citizens = _registry_checks(registry_bytes)
    _validate(package, package_checksums, predecessor_citizens, corpus, schemas)
    inherited = {_key(pin): pin for pin in package["members"]}
    candidate = copy.deepcopy(package)
    next_registry = copy.deepcopy(registry)
    if _version(changes["package_version"]) <= _version(package["version"]):
        raise SuccessorError("package version must increase")
    if _version(changes["release_version"]) <= _version(release["version"]):
        raise SuccessorError("release version must increase")
    candidate["version"] = changes["package_version"]
    if "schema" in changes:
        candidate["schema"] = changes["schema"]
    if (candidate["id"], candidate["version"]) in package_checksums:
        raise SuccessorError("package already in predecessor registry")
    touched: set[tuple[str, str]] = set()
    changed: list[tuple[dict[str, Any], Any]] = []
    for edit in changes.get("members", []):
        operation = edit.get("op")
        if operation not in {"add", "remove", "replace"} or set(edit) - {"op", "old", "new", "before", "at_end", "registry_before"}:
            raise SuccessorError("unsupported member edit")
        old = edit.get("old")
        new = edit.get("new")
        if (operation in {"remove", "replace"} and not isinstance(old, dict)) or (operation in {"add", "replace"} and not isinstance(new, dict)):
            raise SuccessorError("member edit needs its required pins")
        if (operation == "add" and old is not None) or (operation == "remove" and new is not None):
            raise SuccessorError("unexpected member pin")
        if new is not None and not all(isinstance(new.get(field), str) for field in ("id", "version", "schema", "role")):
            raise SuccessorError("new member pin is incomplete")
        for anchor in ("before", "registry_before"):
            if anchor in edit and (not isinstance(edit[anchor], list) or len(edit[anchor]) != 2 or not all(isinstance(value, str) for value in edit[anchor])):
                raise SuccessorError("invalid member placement anchor")
        if "at_end" in edit and (operation != "replace" or not isinstance(edit["at_end"], bool) or "before" in edit):
            raise SuccessorError("invalid member placement")
        for pin in (old, new):
            if pin is not None:
                key = _key(pin)
                if key in touched:
                    raise SuccessorError(f"conflicting member edit: {key}")
                touched.add(key)
        if operation in {"remove", "replace"}:
            index = _member_index(candidate["members"], _key(old))
            if candidate["members"][index] != old:
                raise SuccessorError("old member pin mismatch")
        if operation in {"add", "replace"}:
            body = corpus.get(_key(new))
            if body is None or body.get("id") != new["id"] or body.get("version") != new["version"] or body.get("schema") != new["schema"]:
                raise SuccessorError("new member absent or pin mismatch")
            if any(_key(pin) == _key(new) for pin in candidate["members"]):
                raise SuccessorError("new member already exists")
            if operation == "replace":
                old_body = corpus[_key(old)]
                if (old["id"] != new["id"] or _version(new["version"]) <= _version(old["version"])
                    or old["role"] != new["role"] or old["schema"].rsplit(".v", 1)[0] != new["schema"].rsplit(".v", 1)[0]
                    or old_body.get("scope") != body.get("scope")):
                    raise SuccessorError("replacement is not structurally compatible")
            changed.append((new, edit.get("registry_before")))
        if operation == "remove":
            candidate["members"].pop(index)
        elif operation == "replace":
            candidate["members"].pop(index)
            if "before" in edit:
                index = _member_index(candidate["members"], tuple(edit["before"]))
            elif edit.get("at_end") is True:
                index = len(candidate["members"])
            candidate["members"].insert(index, copy.deepcopy(new))
        else:
            index = _member_index(candidate["members"], tuple(edit["before"])) if "before" in edit else len(candidate["members"])
            candidate["members"].insert(index, copy.deepcopy(new))
    for field in ("entrypoints", "bindings", "admitted_schemas"):
        target = candidate["input_bindings" if field == "bindings" else field]
        seen_edits: set[str] = set()
        for edit in changes.get(field, []):
            if edit.get("op") == "replace" and set(edit) == {"op", "old", "new"}:
                old, new = edit["old"], edit["new"]
                markers = [json.dumps(value, sort_keys=True) for value in (old, new)]
                if any(marker in seen_edits for marker in markers) or target.count(old) != 1 or new in target:
                    raise SuccessorError(f"conflicting {field} replacement")
                seen_edits.update(markers)
                target[target.index(old)] = copy.deepcopy(new)
                continue
            if set(edit) != {"op", "value"} or edit["op"] not in {"add", "remove"}:
                raise SuccessorError(f"unsupported {field} edit")
            value = edit["value"]
            marker = json.dumps(value, sort_keys=True)
            if marker in seen_edits:
                raise SuccessorError(f"conflicting {field} edit")
            seen_edits.add(marker)
            if edit["op"] == "remove":
                if target.count(value) != 1:
                    raise SuccessorError(f"missing or ambiguous {field} value")
                target.remove(value)
            else:
                if value in target:
                    raise SuccessorError(f"duplicate {field} value")
                target.append(copy.deepcopy(value))
    if "binding_sort" in changes:
        candidate["input_bindings"].sort(key=lambda item: item["symbol"])
    citizen_entries = dict(predecessor_citizens)
    key_order = changes.get("registry_new_key_order", ["id", "version", "checksum"])
    if sorted(key_order) != ["checksum", "id", "version"]:
        raise SuccessorError("invalid registry entry key order")
    for pin, anchor in changed:
        key = _key(pin)
        digest = citizen_checksum(corpus[key])
        if key in citizen_entries:
            if citizen_entries[key] != digest:
                raise SuccessorError("existing citizen checksum mismatch")
            continue
        entry = {"id": key[0], "version": key[1], "checksum": digest}
        entry = {name: entry[name] for name in key_order}
        index = _member_index(next_registry["citizens"], tuple(anchor)) if anchor else len(next_registry["citizens"])
        next_registry["citizens"].insert(index, entry)
        citizen_entries[key] = digest
    if "registry_sort" in changes:
        if changes["registry_sort"] != "id_version":
            raise SuccessorError("unsupported registry order")
        tail = [tuple(key) for key in changes.get("registry_tail", [])]
        if len(set(tail)) != len(tail):
            raise SuccessorError("duplicate registry tail")
        entries = next_registry["citizens"]
        tail_entries = [entries[_member_index(entries, key)] for key in tail]
        next_registry["citizens"] = sorted((entry for entry in entries if _key(entry) not in tail), key=_key) + tail_entries
    elif "registry_tail" in changes:
        raise SuccessorError("registry tail requires registry sort")
    candidate["package_checksum"] = package_instance_checksum(candidate)
    package_entry = {"id": candidate["id"], "version": candidate["version"], "checksum": candidate["package_checksum"]}
    next_registry["packages"].append({name: package_entry[name] for name in key_order})
    if "registry_sort" in changes:
        next_registry["packages"].sort(key=_key)
    output_registry = _encode(next_registry)
    candidate_packages, candidate_citizens = _registry_checks(output_registry)
    inconsistencies = _validate(candidate, candidate_packages, candidate_citizens, corpus, schemas, inherited, predecessor_citizens)
    next_release = copy.deepcopy(release)
    next_release["version"] = changes["release_version"]
    next_release["package_registry_sha256"] = hashlib.sha256(output_registry).hexdigest()
    if "release_key_order" in changes:
        order = changes["release_key_order"]
        if set(order) != set(next_release) or len(order) != len(next_release):
            raise SuccessorError("invalid release key order")
        next_release = {key: next_release[key] for key in order}
    schemas.validate_declared(next_release)
    return SuccessorResult(_encode(candidate), output_registry, _encode(next_release), inconsistencies)


def _read_object(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise SuccessorError(f"JSON object required: {path.name}")
    return value, raw


def load_corpus(directory: Path) -> tuple[dict[tuple[str, str], dict[str, Any]], dict[Path, bytes]]:
    """Read JSON citizens, refusing conflicting bodies for one exact identity."""
    if not directory.is_dir():
        raise SuccessorError("corpus must be an existing directory")
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    snapshots: dict[Path, bytes] = {}
    for path in sorted(directory.rglob("*.json")):
        value, raw = _read_object(path)
        if not isinstance(value.get("id"), str) or not isinstance(value.get("version"), str):
            continue
        if str(value.get("schema", "")).startswith("artifact-package."):
            continue
        snapshots[path.resolve(strict=True)] = raw
        key = _key(value)
        if key in corpus and corpus[key] != value:
            raise SuccessorError(f"ambiguous corpus identity: {key}")
        corpus[key] = value
    return corpus, snapshots


def _rename_exclusive(parent_fd: int, source: str, destination: str) -> None:
    """Atomically rename one directory without replacing any destination."""
    libc = ctypes.CDLL(None, use_errno=True)
    try:
        if sys.platform == "darwin":
            rename = libc.renameatx_np
            flag = 0x00000004  # RENAME_EXCL
        elif sys.platform.startswith("linux"):
            rename = libc.renameat2
            flag = 1  # RENAME_NOREPLACE
        else:
            raise SuccessorError("exclusive directory installation is unsupported on this platform")
    except AttributeError as exc:
        raise SuccessorError("exclusive directory installation is unavailable") from exc
    rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    rename.restype = ctypes.c_int
    if rename(parent_fd, os.fsencode(source), parent_fd, os.fsencode(destination), flag) != 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error), destination)


def _install(parent: Path, name: str, result: SuccessorResult, snapshots: Mapping[Path, bytes]) -> None:
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    parent_fd = os.open(parent, flags)
    stage = ".package-successor-" + secrets.token_hex(16)
    stage_fd = -1
    owned = False
    created: list[str] = []
    try:
        try:
            os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise SuccessorError("destination already exists")
        os.mkdir(stage, 0o700, dir_fd=parent_fd)
        owned = True
        stage_fd = os.open(stage, flags, dir_fd=parent_fd)
        for filename, data in (("package.json", result.package), ("registry.json", result.registry), ("release.json", result.release)):
            fd = os.open(filename, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=stage_fd)
            created.append(filename)
            with os.fdopen(fd, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
        os.fsync(stage_fd)
        for path, raw in snapshots.items():
            if path.read_bytes() != raw:
                raise SuccessorError(f"input changed during construction: {path.name}")
        _rename_exclusive(parent_fd, stage, name)
        stage = ""
    finally:
        if stage_fd >= 0:
            for filename in created:
                if stage:
                    try:
                        os.unlink(filename, dir_fd=stage_fd)
                    except FileNotFoundError:
                        pass
            os.close(stage_fd)
        if stage and owned:
            try:
                os.rmdir(stage, dir_fd=parent_fd)
            except FileNotFoundError:
                pass
        os.close(parent_fd)


def generate_to_directory(package_path: Path, registry_path: Path, release_path: Path,
                          corpus_dir: Path, changes_path: Path, destination: Path) -> dict[str, Any]:
    """Validate a complete candidate and install it in a new directory."""
    if ".." in destination.parts or destination.name in {"", ".", ".."}:
        raise SuccessorError("destination traversal is not permitted")
    parent = destination.parent.absolute()
    if parent.resolve(strict=True) != parent:
        raise SuccessorError("destination parent must not contain symlinks")
    target = parent / destination.name
    inputs = [package_path.resolve(strict=True), registry_path.resolve(strict=True),
              release_path.resolve(strict=True), changes_path.resolve(strict=True)]
    corpus_root = corpus_dir.resolve(strict=True)
    published_root = (Path(__file__).resolve().parents[1] / "packages").resolve()
    for protected in [*inputs, corpus_root, published_root]:
        if target == protected or target.is_relative_to(protected) or protected.is_relative_to(target):
            raise SuccessorError("destination overlaps a source or published location")
    if os.path.lexists(target):
        raise SuccessorError("destination already exists")
    package, package_raw = _read_object(inputs[0])
    registry_raw = inputs[1].read_bytes()
    release, release_raw = _read_object(inputs[2])
    changes, changes_raw = _read_object(inputs[3])
    corpus, snapshots = load_corpus(corpus_root)
    snapshots.update(dict(zip(inputs, (package_raw, registry_raw, release_raw, changes_raw))))
    if any(target == path or path.is_relative_to(target) for path in snapshots):
        raise SuccessorError("destination overlaps an input")
    result = build_successor(package, registry_raw, release, corpus, changes)
    _install(parent, destination.name, result, snapshots)
    output_package = json.loads(result.package)
    output_release = json.loads(result.release)
    return {"package": {"id": output_package["id"], "version": output_package["version"], "checksum": output_package["package_checksum"]},
            "registry_sha256": hashlib.sha256(result.registry).hexdigest(),
            "release": {"id": output_release["id"], "version": output_release["version"], "sha256": hashlib.sha256(result.release).hexdigest()},
            "inherited_inconsistencies": result.inherited_inconsistencies,
            "publication_boundary": "Candidate only: successor companion declaration and live release evidence are separate duties under ADR-0082."}


def main() -> int:
    parser = argparse.ArgumentParser(description="Construct a validated package successor candidate directory.")
    for name in ("package", "registry", "release", "corpus", "changes", "output"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    try:
        report = generate_to_directory(args.package, args.registry, args.release, args.corpus, args.changes, args.output)
    except (SuccessorError, OSError, ValueError, SchemaRegistryError, SchemaValidationError) as exc:
        print(f"package successor refused: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
