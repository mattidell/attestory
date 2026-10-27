"""The mortgage publication candidate is additive and reproducible on its pinned base."""
from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.generate_mortgage_borrowing_consumer_successors import (
    BASE_PACKAGE_REL,
    DELTA_REL,
    BASE_REGISTRY_REL,
    BASE_RELEASE_REL,
    GenerationGuardError,
    PACKAGE_REL,
    REGISTRY_REL,
    RELEASE_REL,
    _pinned_json,
    _merge_package,
    _write_outputs,
    build,
)


class MortgagePackageRebuildTests(unittest.TestCase):
    def test_rebuild_is_deterministic_and_keeps_selected_base_surfaces(self) -> None:
        first = build()
        second = build()
        self.assertEqual(first, second)
        self.assertEqual(set(first), {PACKAGE_REL, REGISTRY_REL, RELEASE_REL})

        package = json.loads(first[PACKAGE_REL])
        registry = json.loads(first[REGISTRY_REL])
        release = json.loads(first[RELEASE_REL])
        root = Path(__file__).resolve().parents[1]
        for relative, expected in first.items():
            self.assertEqual((root / relative).read_bytes(), expected)
        base = _pinned_json(root, BASE_PACKAGE_REL)
        base_registry = _pinned_json(root, BASE_REGISTRY_REL)
        base_release = _pinned_json(root, BASE_RELEASE_REL)
        delta = json.loads((root / DELTA_REL).read_text("utf-8"))
        self.assertEqual(package["version"], "v57")
        retired = {
            ("tax.us.2025.rule.attachment.schedule-a", "v1"),
            ("tax.us.2025.rule.f1098-line8a", "v2"),
            ("tax.us.2025.rule.f1098-residence-interest-reason", "v2"),
            ("tax.us.2025.rule.form1040-line12e", "v1"),
        }
        base_entrypoints = {(row["id"], row["version"]) for row in base["entrypoints"]}
        candidate_entrypoints = {(row["id"], row["version"]) for row in package["entrypoints"]}
        self.assertTrue(base_entrypoints - retired <= candidate_entrypoints)
        self.assertEqual(candidate_entrypoints - (base_entrypoints - retired), {(row["id"], row["version"]) for row in delta["entrypoints"]})
        for field_name in ("admitted_schemas", "composition_obligations", "conflict_semantics", "input_bindings", "scope"):
            self.assertEqual(package[field_name], base[field_name], field_name)
        package_rows = {(row["id"], row["version"]) for row in package["members"]}
        base_rows = {(row["id"], row["version"]) for row in base["members"]}
        retired = {
            ("tax.us.2025.rule.attachment.schedule-a", "v1"),
            ("tax.us.2025.rule.f1098-line8a", "v2"),
            ("tax.us.2025.rule.f1098-residence-interest-reason", "v2"),
            ("tax.us.2025.rule.form1040-line12e", "v1"),
        }
        self.assertTrue((base_rows - retired) <= package_rows)
        candidate_by_id = {row["id"]: row for row in package["members"]}
        base_by_id = {row["id"]: row for row in base["members"]}
        for identifier, row in base_by_id.items():
            if (identifier, row["version"]) not in retired:
                self.assertEqual(candidate_by_id[identifier], row)
        added_ids = {row["id"] for row in delta["members"]}
        self.assertEqual(len(added_ids), 44)
        self.assertTrue(added_ids <= set(candidate_by_id))
        self.assertEqual(release["version"], "v55")
        self.assertEqual(release["id"], base_release["id"])
        self.assertEqual(release["package_registry_sha256"], hashlib.sha256(first[REGISTRY_REL]).hexdigest())
        base_citizens = {(row["id"], row["version"]): row for row in base_registry["citizens"]}
        new_citizens = {(row["id"], row["version"]): row for row in registry["citizens"]}
        for key, row in base_citizens.items():
            self.assertEqual(new_citizens[key], row)
        base_packages = {(row["id"], row["version"]): row for row in base_registry["packages"]}
        new_packages = {(row["id"], row["version"]): row for row in registry["packages"]}
        for key, row in base_packages.items():
            self.assertEqual(new_packages[key], row)
        self.assertIn(("tax.us.2025.package.core-calculations", "v57"), new_packages)

    def test_rejects_duplicate_durable_delta_member(self) -> None:
        root = Path(__file__).resolve().parents[1]
        delta = json.loads((root / DELTA_REL).read_text("utf-8"))
        base = _pinned_json(root, BASE_PACKAGE_REL)
        delta["members"].append(dict(delta["members"][0]))
        with self.assertRaisesRegex(GenerationGuardError, "44-addition"):
            _merge_package(base, delta)

    def test_build_is_independent_of_git_history_and_guards_base_bytes(self) -> None:
        source_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(source_root / "packages/content/tax/2025", root / "packages/content/tax/2025")
            base_release = root / BASE_RELEASE_REL
            base_release.parent.mkdir(parents=True)
            shutil.copy2(source_root / BASE_RELEASE_REL, base_release)
            delta_path = root / DELTA_REL
            delta_path.parent.mkdir(parents=True)
            shutil.copy2(source_root / DELTA_REL, delta_path)
            self.assertEqual(build(root), build(source_root))
            (root / BASE_PACKAGE_REL).write_bytes((root / BASE_PACKAGE_REL).read_bytes() + b" ")
            with self.assertRaisesRegex(GenerationGuardError, "base bytes changed"):
                build(root)

    def test_write_mode_refuses_existing_candidate_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / PACKAGE_REL
            first.parent.mkdir(parents=True)
            first.write_bytes(b"sentinel")
            with self.assertRaisesRegex(GenerationGuardError, "refusing to overwrite"):
                _write_outputs(root, {PACKAGE_REL: b"replacement", REGISTRY_REL: b"new"})
            self.assertEqual(first.read_bytes(), b"sentinel")
            self.assertFalse((root / REGISTRY_REL).exists())


if __name__ == "__main__":
    unittest.main()
