"""Historical successor construction and refusal checks."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from packages.kernel.schema_registry import SchemaRegistryError, SchemaValidationError
from tools.package_successor import SuccessorError, SuccessorResult, build_successor, generate_to_directory, load_corpus

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages/content/tax/2025"
RELEASES = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
PREFIX = "tax.us.2025."
DELTAS = ROOT / "tests/fixtures/package_successor"


class SuccessorInputTests(unittest.TestCase):
    def test_malformed_change_set_is_refused_before_loading_inputs(self) -> None:
        for changes in ({}, {"package_version": "v2", "release_version": "v2", "members": "invalid"}):
            with self.subTest(changes=changes), self.assertRaises(SuccessorError):
                build_successor({}, b"", {}, {}, changes)

    def test_invalid_optional_values_are_refused(self) -> None:
        base = {"package_version": "v2", "release_version": "v2"}
        for field in ("binding_sort", "registry_sort", "registry_new_key_order", "release_key_order", "registry_tail", "schema"):
            for value in (None, False, "", ["invalid"]):
                with self.subTest(field=field, value=value), self.assertRaises(SuccessorError):
                    build_successor({}, b"", {}, {}, dict(base, **{field: value}))

    def test_malformed_unused_registry_entries_refuse_at_write_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            corpus = root / "corpus"
            corpus.mkdir()
            pkg, reg, rel, changes = [root / name for name in ("package.json", "registry.json", "release.json", "changes.json")]
            pkg.write_text("{}")
            changes.write_text('{"package_version":"v2","release_version":"v2"}')
            invalid_entries: list[Any] = [[{"id": "demo.unused", "version": "v1", "checksum": 17}],
                                          [{"id": "demo.unused", "version": "v1", "checksum": "short"}],
                                          ["invalid"], None, {}]
            for field in ("citizens", "packages"):
                for invalid in invalid_entries:
                    registry: dict[str, Any] = {"citizens": [], "packages": []}
                    registry[field] = invalid
                    raw = json.dumps(registry).encode()
                    reg.write_bytes(raw)
                    rel.write_text(json.dumps({"id": "demo.release", "version": "v1", "schema": "release-registry.v1",
                                               "package_registry_sha256": hashlib.sha256(raw).hexdigest()}))
                    before = [path.read_bytes() for path in (pkg, reg, rel, changes)]
                    destination = root / "candidate"
                    with self.subTest(field=field, invalid=invalid), self.assertRaises(SuccessorError):
                        generate_to_directory(pkg, reg, rel, corpus, changes, destination)
                    self.assertFalse(destination.exists())
                    self.assertEqual([path.read_bytes() for path in (pkg, reg, rel, changes)], before)

    def test_malformed_candidate_registry_refused_at_write_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            corpus = root / "corpus"
            corpus.mkdir()
            pkg, reg, rel, changes = [root / name for name in ("package.json", "registry.json", "release.json", "changes.json")]
            pkg.write_text(json.dumps({"id": "demo.package", "version": "v1", "members": [], "entrypoints": [],
                                       "admitted_schemas": [], "input_bindings": []}))
            raw = json.dumps({"citizens": [], "packages": []}).encode()
            reg.write_bytes(raw)
            rel.write_text(json.dumps({"id": "demo.release", "version": "v1", "schema": "release-registry.v1",
                                       "package_registry_sha256": hashlib.sha256(raw).hexdigest()}))
            changes.write_text('{"package_version":"v2","release_version":"v2"}')
            before = [path.read_bytes() for path in (pkg, reg, rel, changes)]
            from tools.package_successor import _encode
            for field in ("citizens", "packages"):
                def corrupt_registry(value: Any) -> bytes:
                    if isinstance(value, dict) and "citizens" in value and "packages" in value:
                        value = copy.deepcopy(value)
                        value[field].append({"id": "demo.unused", "version": "v1", "checksum": 17})
                    return _encode(value)
                with self.subTest(field=field), patch("tools.package_successor._validate", return_value=()), patch("tools.package_successor._encode", side_effect=corrupt_registry):
                    with self.assertRaisesRegex(SuccessorError, "invalid checksum"):
                        generate_to_directory(pkg, reg, rel, corpus, changes, root / "candidate")
                self.assertFalse((root / "candidate").exists())
                self.assertEqual([path.read_bytes() for path in (pkg, reg, rel, changes)], before)

    def test_member_edit_refusals_with_synthetic_inputs(self) -> None:
        pin = {"id": "demo.rule", "version": "v1", "schema": "rule-artifact.v1", "role": "computation"}
        package = {"id": "demo.package", "version": "v1", "members": [pin], "input_bindings": []}
        registry = json.dumps({"citizens": [], "packages": []}).encode()
        release = {"version": "v1", "package_registry_sha256": hashlib.sha256(registry).hexdigest()}
        corpus = {("demo.rule", "v1"): dict(pin), ("demo.rule", "v2"): dict(pin, version="v2")}
        changes = {"package_version": "v2", "release_version": "v2"}
        edits = [
            [{"op": "remove", "old": dict(pin, version="v99")}],
            [{"op": "replace", "old": pin, "new": dict(pin, version="v2", schema="rule-artifact.v2")}],
            [{"op": "replace", "old": pin, "new": dict(pin)}],
            [{"op": "remove", "old": pin}, {"op": "remove", "old": pin}],
        ]
        # Real-chain integration exercises _validate; these tests isolate edit refusals.
        with patch("tools.package_successor._validate", return_value=()):
            for member_edits in edits:
                with self.subTest(edits=member_edits), self.assertRaises(SuccessorError):
                    build_successor(package, registry, release, corpus, dict(changes, members=member_edits), MagicMock())

    def test_ambiguous_corpus(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "a.json").write_text('{"id":"demo.rule","version":"v1","value":1}')
            (root / "b.json").write_text('{"id":"demo.rule","version":"v1","value":2}')
            with self.assertRaisesRegex(SuccessorError, "ambiguous corpus"):
                load_corpus(root)

    def test_path_refusals_and_transaction_failures(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            corpus = root / "corpus"
            corpus.mkdir()
            paths = [root / name for name in ("package.json", "registry.json", "release.json", "changes.json")]
            for path in paths:
                path.write_text("{}")
            originals = [path.read_bytes() for path in paths]
            def invoke(destination: Path) -> dict[str, Any]:
                return generate_to_directory(paths[0], paths[1], paths[2], corpus, paths[3], destination)
            with self.assertRaises(SuccessorError):
                invoke(paths[0])
            with self.assertRaises(SuccessorError):
                invoke(corpus / "candidate")
            with self.assertRaises(SuccessorError):
                invoke(CONTENT / "demo-candidate")
            with self.assertRaises(SuccessorError):
                invoke(root / "x" / ".." / "candidate")
            link = root / "alias"
            link.symlink_to(root, target_is_directory=True)
            with self.assertRaises(SuccessorError):
                invoke(link / "candidate")
            result = SuccessorResult(b'{"id":"demo.p","version":"v2","package_checksum":"a"}', b"{}", b'{"id":"demo.r","version":"v2"}', ())
            with patch("tools.package_successor.build_successor", return_value=result):
                with patch("tools.package_successor.os.fsync", side_effect=OSError("injected staging failure")):
                    with self.assertRaises(OSError):
                        invoke(root / "candidate")
                self.assertFalse((root / "candidate").exists())
                self.assertFalse(list(root.glob(".package-successor-*")))
                fsync = os.fsync
                def mutate_source(fd: int) -> None:
                    fsync(fd)
                    paths[3].write_text('{"demo":"changed"}')
                with patch("tools.package_successor.os.fsync", side_effect=mutate_source):
                    with self.assertRaisesRegex(SuccessorError, "input changed"):
                        invoke(root / "candidate")
                self.assertFalse((root / "candidate").exists())
                paths[3].write_bytes(originals[3])
                with patch("tools.package_successor._rename_exclusive", side_effect=OSError("injected failure")):
                    with self.assertRaises(OSError):
                        invoke(root / "candidate")
                self.assertFalse((root / "candidate").exists())
                self.assertFalse(list(root.glob(".package-successor-*")))
                from tools.package_successor import _rename_exclusive
                def collide(parent_fd: int, source: str, destination: str) -> None:
                    (root / destination).mkdir()
                    (root / destination / "owner.txt").write_text("demo competing writer")
                    _rename_exclusive(parent_fd, source, destination)
                with patch("tools.package_successor._rename_exclusive", side_effect=collide):
                    with self.assertRaises(OSError):
                        invoke(root / "candidate")
                self.assertEqual((root / "candidate" / "owner.txt").read_text(), "demo competing writer")
                self.assertFalse(list(root.glob(".package-successor-*")))
                with self.assertRaisesRegex(SuccessorError, "already exists"):
                    invoke(root / "candidate")
            self.assertEqual([path.read_bytes() for path in paths], originals)


@pytest.mark.live  # Validates the real 729-member corpus; exceeds the fast-lane budget under load.
class SuccessorTests(unittest.TestCase):
    corpus: dict[tuple[str, str], dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus = {}
        for path in CONTENT.glob("*.json"):
            value = json.loads(path.read_bytes())
            if isinstance(value, dict) and isinstance(value.get("id"), str) and isinstance(value.get("version"), str):
                key = (value["id"], value["version"])
                if key in cls.corpus and cls.corpus[key] != value:
                    raise AssertionError(f"ambiguous corpus identity: {key}")
                cls.corpus[key] = value

    def chain(self, package_version: int, registry_version: int) -> tuple[dict[str, Any], bytes, dict[str, Any]]:
        package = json.loads((CONTENT / f"package.core-calculations.v{package_version}.json").read_bytes())
        registry = (CONTENT / f"published-packages.v{registry_version}.json").read_bytes()
        release = json.loads((RELEASES / f"demo.release.sli-worksheet-integration.2025.v{registry_version}.json").read_bytes())
        return package, registry, release

    def test_inherited_mismatch_is_reported(self) -> None:
        package, registry, release = self.chain(57, 55)
        result = build_successor(package, registry, release, self.corpus, {"package_version": "v99", "release_version": "v99"})
        self.assertEqual(json.loads(result.package)["version"], "v99")
        self.assertEqual(result.inherited_inconsistencies, ((PREFIX + "rule.schedule3-line1-direct-ftc", "v3"),))

    def test_refuses_bad_release_pin_and_tampered_body(self) -> None:
        package, registry, release = self.chain(57, 55)
        changes = {"package_version": "v99", "release_version": "v99"}
        release_bad = copy.deepcopy(release)
        release_bad["package_registry_sha256"] = "0" * 64
        with self.assertRaisesRegex(SuccessorError, "release registry hash"):
            build_successor(package, registry, release_bad, self.corpus, changes)
        corpus = copy.deepcopy(self.corpus)
        key = (PREFIX + "rule.schedule3-line1-direct-ftc", "v3")
        corpus[key]["schema"] = "rule-artifact.v2"
        with self.assertRaisesRegex(SuccessorError, "unverified body"):
            build_successor(package, registry, release, corpus, changes)

    def test_refuses_missing_and_bad_replacement(self) -> None:
        package, registry, release = self.chain(57, 55)
        pin = next(p for p in package["members"] if p["id"] == PREFIX + "rule.eic-child.counts")
        new = dict(pin, version="v2")
        base = {"package_version": "v99", "release_version": "v99"}
        for edit in (
            {"op": "remove", "old": dict(pin, version="v99")},
            {"op": "replace", "old": pin, "new": dict(new, schema="rule-artifact.v13")},
            {"op": "replace", "old": pin, "new": dict(pin)},
        ):
            with self.subTest(edit=edit), self.assertRaises(SuccessorError):
                build_successor(package, registry, release, self.corpus, dict(base, members=[edit]))
        with self.assertRaisesRegex(SuccessorError, "conflicting"):
            build_successor(package, registry, release, self.corpus,
                            dict(base, members=[{"op": "remove", "old": pin}, {"op": "remove", "old": pin}]))

    def test_existing_validator_rejects_invalid_entrypoint(self) -> None:
        package, registry, release = self.chain(57, 55)
        changes = {"package_version": "v99", "release_version": "v99", "entrypoints": [
            {"op": "add", "value": {"id": "demo.absent", "version": "v1"}}]}
        with self.assertRaisesRegex(SuccessorError, "invalid package"):
            build_successor(package, registry, release, self.corpus, changes)

    def test_first_historical_chain(self) -> None:
        package, registry, release = self.chain(57, 55)
        members = package["members"]
        registry_members = json.loads(registry)["citizens"]
        edits: list[dict[str, Any]] = []
        for name, before in (("rule.eic-child.counts", "rule.eic-child.joint-return-met"), ("rule.ctc-child.counts", "rule.ctc-child.joint-return-met"), ("rule.odc-child.other-tests-met", "rule.odc-dependent-present"), ("rule.odc-child.counts", "")):
            old = next(pin for pin in members if pin["id"] == PREFIX + name)
            new = dict(old, version="v2")
            edit: dict[str, Any] = {"op": "replace", "old": old, "new": new}
            if before:
                next_entry = next(entry for entry in registry_members if entry["id"] == PREFIX + before)
                edit["registry_before"] = [next_entry["id"], next_entry["version"]]
            edits.append(edit)
        for name in ("rule.eic-child.other-claimant-clear", "rule.ctc-child.other-claimant-clear"):
            edits.append({"op": "remove", "old": next(pin for pin in members if pin["id"] == PREFIX + name)})
        for name, role, before, registry_before in (("dtb-questions", "fact-type-bundle", "rule.eic-child.relationship-met", "eic-child-roster.vocabulary"), ("rule.dtb-child.tie-breaker-clear", "computation", "rule.ctc-child.ssn-met", "rule.effective-proceeds-support-count")):
            body = self.corpus[(PREFIX + name, "v1")]
            pin = {"id": body["id"], "role": role, "schema": body["schema"], "version": "v1"}
            anchor = next(item for item in members if item["id"] == PREFIX + before)
            registry_anchor = next(item for item in registry_members if item["id"] == PREFIX + registry_before)
            edits.append({"op": "add", "new": pin, "before": [anchor["id"], anchor["version"]],
                          "registry_before": [registry_anchor["id"], registry_anchor["version"]]})
        bindings = []
        for name in ("another-could-claim", "filer-agi-higher", "filer-is-parent", "form-8332-released", "more-nights-with-filer", "multiple-other-claimants", "other-is-parent", "other-will-claim", "same-agi", "same-nights"):
            fact = PREFIX + "dtb.child." + name
            bindings.append({"op": "add", "value": {"symbol": fact, "fact_type": {"id": fact, "version": "v1"}, "mode": "required"}})
        changes = {"package_version": "v58", "release_version": "v56", "members": edits, "bindings": bindings,
                   "binding_sort": "symbol", "registry_sort": "id_version", "registry_tail": [[PREFIX + "rule.odc-child.counts", "v2"]],
                   "release_key_order": ["id", "version", "schema", "package_registry_sha256"]}
        result = build_successor(package, registry, release, self.corpus, changes)
        self.assertEqual(result.package, (CONTENT / "package.core-calculations.v58.json").read_bytes())
        self.assertEqual(result.registry, (CONTENT / "published-packages.v56.json").read_bytes())
        self.assertEqual(result.release, (RELEASES / "demo.release.sli-worksheet-integration.2025.v56.json").read_bytes())

    def test_second_historical_chain(self) -> None:
        package, registry, release = self.chain(58, 56)
        members = package["members"]
        edits: list[dict[str, Any]] = []
        names = (("f1099g.box4.vocabulary", "fact-type-bundle"), ("f1099g.b4", "source-family"),
                 ("closure-mapping.f1099g-b4", "source-closure-mapping"), ("rule.f1099g-b4-subtotal", "computation"),
                 ("ssa1099.box6.vocabulary", "fact-type-bundle"), ("ssa1099.b6", "source-family"),
                 ("closure-mapping.ssa1099-b6", "source-closure-mapping"), ("rule.ssa1099-b6-subtotal", "computation"))
        for name, role in names:
            body = self.corpus[(PREFIX + name, "v1")]
            edits.append({"op": "add", "new": {"id": body["id"], "role": role, "schema": body["schema"], "version": "v1"}})
        for name in ("form1040.line-25b", "ssa1099.benefits", "closure-mapping.ssa1099-benefits", "rule.form1040-line25b", "rule.schedule1-line7"):
            old = next(pin for pin in members if pin["id"] == PREFIX + name)
            body = self.corpus[(PREFIX + name, "v2")]
            new = dict(old, schema=body["schema"], version="v2")
            edits.append({"op": "replace", "old": old, "new": new, "at_end": name != "form1040.line-25b"})
        entrypoints = [{"op": "replace", "old": {"id": PREFIX + name, "version": "v1"},
                        "new": {"id": PREFIX + name, "version": "v2"}}
                       for name in ("ssa1099.benefits", "closure-mapping.ssa1099-benefits", "rule.schedule1-line7")]
        changes = {"package_version": "v59", "release_version": "v57", "members": edits, "entrypoints": entrypoints,
                   "registry_sort": "id_version", "registry_tail": [[PREFIX + "rule.odc-child.counts", "v2"]],
                   "registry_new_key_order": ["checksum", "id", "version"]}
        result = build_successor(package, registry, release, self.corpus, changes)
        self.assertEqual(result.package, (CONTENT / "package.core-calculations.v59.json").read_bytes())
        self.assertEqual(result.registry, (CONTENT / "published-packages.v57.json").read_bytes())
        self.assertEqual(result.release, (RELEASES / "demo.release.sli-worksheet-integration.2025.v57.json").read_bytes())

    def test_frozen_deltas_cli_and_installation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            for package_version, registry_version, successor in ((57, 55, 58), (58, 56, 59), (59, 57, 60)):
                package = CONTENT / f"package.core-calculations.v{package_version}.json"
                registry = CONTENT / f"published-packages.v{registry_version}.json"
                release = RELEASES / f"demo.release.sli-worksheet-integration.2025.v{registry_version}.json"
                changes = DELTAS / f"v{package_version}-to-v{successor}.json"
                destination = root / f"candidate-{successor}"
                source_bytes = [p.read_bytes() for p in (package, registry, release, changes)]
                report = generate_to_directory(package, registry, release, CONTENT, changes, destination)
                self.assertIn("ADR-0082", report["publication_boundary"])
                self.assertTrue(report["inherited_inconsistencies"])
                self.assertEqual((destination / "package.json").read_bytes(), (CONTENT / f"package.core-calculations.v{successor}.json").read_bytes())
                self.assertEqual((destination / "registry.json").read_bytes(), (CONTENT / f"published-packages.v{registry_version + 1}.json").read_bytes())
                self.assertEqual((destination / "release.json").read_bytes(), (RELEASES / f"demo.release.sli-worksheet-integration.2025.v{registry_version + 1}.json").read_bytes())
                self.assertEqual([p.read_bytes() for p in (package, registry, release, changes)], source_bytes)

    def test_public_boundary_refuses_invalid_candidates(self) -> None:
        package, registry, release = self.chain(57, 55)
        pin = next(p for p in package["members"] if p["id"] == PREFIX + "rule.eic-child.counts")
        base: dict[str, Any] = {"package_version": "v99", "release_version": "v99"}
        cases = [dict(base, members=[{"op": "remove", "old": dict(pin, version="v99")}]),
                 dict(base, members=[{"op": "remove", "old": pin}, {"op": "remove", "old": pin}]),
                 dict(base, schema="artifact-package.v999"),
                 dict(base, entrypoints=[{"op": "add", "value": {"id": "demo.absent", "version": "v1"}}])]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            pkg = root / "predecessor.json"
            reg = root / "registry.json"
            rel = root / "release.json"
            changes = root / "changes.json"
            pkg.write_text(json.dumps(package))
            reg.write_bytes(registry)
            rel.write_text(json.dumps(release))
            empty_corpus = root / "empty-corpus"
            empty_corpus.mkdir()
            changes.write_text(json.dumps(base))
            with self.assertRaisesRegex(SuccessorError, "missing member"):
                generate_to_directory(pkg, reg, rel, empty_corpus, changes, root / "missing-member")
            self.assertFalse((root / "missing-member").exists())
            for index, change in enumerate(cases):
                changes.write_text(json.dumps(change))
                sources = [p.read_bytes() for p in (pkg, reg, rel, changes)]
                with self.subTest(index=index), self.assertRaises((SuccessorError, SchemaRegistryError, SchemaValidationError)):
                    generate_to_directory(pkg, reg, rel, CONTENT, changes, root / f"candidate-{index}")
                self.assertFalse((root / f"candidate-{index}").exists())
                self.assertEqual([p.read_bytes() for p in (pkg, reg, rel, changes)], sources)
            bad_release = dict(release, package_registry_sha256="0" * 64)
            rel.write_text(json.dumps(bad_release))
            changes.write_text(json.dumps(base))
            with self.assertRaisesRegex(SuccessorError, "release registry hash"):
                generate_to_directory(pkg, reg, rel, CONTENT, changes, root / "bad-release")
            self.assertFalse((root / "bad-release").exists())
            registry_document = json.loads(registry)
            registry_document["packages"].append({"id": package["id"], "version": "v99", "checksum": "0" * 64})
            registry_with_collision = json.dumps(registry_document).encode()
            reg.write_bytes(registry_with_collision)
            rel.write_text(json.dumps(dict(release, package_registry_sha256=hashlib.sha256(registry_with_collision).hexdigest())))
            with self.assertRaisesRegex(SuccessorError, "already in predecessor registry"):
                generate_to_directory(pkg, reg, rel, CONTENT, changes, root / "existing-version")
            self.assertFalse((root / "existing-version").exists())
