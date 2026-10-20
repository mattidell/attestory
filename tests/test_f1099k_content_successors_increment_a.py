"""Increment A focused tests: content successors, package adoption, and family version threading.

Validates:
1. The 7 content successors validate against their published schemas.
2. package.core-calculations.v49.json passes validate_package with zero issues.
3. published-packages.v47.json and demo release v47 match and contain all citizen checksums.
4. f1099k_family_version_from_package extracts "v1" from v48 and "v2" from v49.
5. f1099k_family_version_for_workspace extracts "v1" for unadopted or v48 workspaces, and "v2" for v49 workspaces.
6. record_f1099k_statement_durably and record_f1099k_no_statements_durably resolve the family version
   from the workspace's adopted package automatically when family_version is None, preserving
   FAMILY_VERSION = "v1" without hard-coding "v2".
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from typing import Any

from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import (
    load_published_citizen_checksums,
    package_instance_checksum,
    validate_package,
)
from packages.kernel.act_log import ActLog
from packages.tax.f1099k_statement_recording import (
    FAMILY_ID,
    FAMILY_VERSION,
    F1099KAdoptionResolutionError,
    f1099k_family_version_for_workspace,
    f1099k_family_version_from_package,
    record_f1099k_no_statements_durably,
    record_f1099k_statement_durably,
)
from packages.tax.loader import TAX_CONTENT_DIR, tax_registry
from tests.support import act


class F1099KContentSuccessorsIncrementATests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = tax_registry()
        self.content_dir = TAX_CONTENT_DIR
        self.temp = TemporaryDirectory(prefix="f1099k-inc-a-")
        self.addCleanup(self.temp.cleanup)

    def test_content_successors_schema_validation(self) -> None:
        """All 7 new content successor citizens validate cleanly against their schemas."""
        cases = [
            ("family.f1099k.v2.json", "source-family.v1", "v2"),
            ("closure-mapping.f1099k.v2.json", "source-closure-mapping.v2", "v2"),
            ("rule.f1099k-box1a-subtotal.json", "rule-artifact.v14", "v1"),
            ("rule.f1099k-statement-loss-reason.v4.json", "rule-artifact.v14", "v4"),
            ("rule.schedule1-top-entry.v3.json", "rule-artifact.v14", "v3"),
            ("rule.attachment.schedule-1.v4.json", "attachment-rule.v4", "v4"),
            ("rule.f1099k-unresolved.v3.json", "rule-artifact.v14", "v3"),
        ]
        for filename, expected_schema, expected_version in cases:
            file_path = self.content_dir / filename
            self.assertTrue(file_path.exists(), f"File {filename} must exist")
            data = json.loads(file_path.read_text("utf-8"))
            self.assertEqual(data.get("schema"), expected_schema)
            self.assertEqual(data.get("version"), expected_version)
            self.registry.validate(expected_schema, data)

        # Inspect specific contract points
        family_v2 = json.loads((self.content_dir / "family.f1099k.v2.json").read_text("utf-8"))
        self.assertEqual(
            family_v2.get("authorizes_subtotal"),
            "tax.us.2025.f1099k.box1a-subtotal",
        )
        self.assertIn("members", family_v2.get("closure_claim", {}))

        mapping_v2 = json.loads((self.content_dir / "closure-mapping.f1099k.v2.json").read_text("utf-8"))
        self.assertEqual(mapping_v2.get("family", {}).get("id"), "tax.us.2025.f1099k")
        self.assertEqual(mapping_v2.get("family", {}).get("version"), "v2")
        self.assertEqual(mapping_v2.get("admits_symbol"), "tax.us.2025.f1099k.box1a-subtotal")

        subtotal_rule = json.loads((self.content_dir / "rule.f1099k-box1a-subtotal.json").read_text("utf-8"))
        self.assertEqual(subtotal_rule.get("publishes"), "tax.us.2025.f1099k.box1a-subtotal")

        reason_v4 = json.loads((self.content_dir / "rule.f1099k-statement-loss-reason.v4.json").read_text("utf-8"))
        self.assertEqual(reason_v4.get("publishes"), "tax.us.2025.f1099k.statement-loss-reason")
        self.assertNotIn("shared_key_count", json.dumps(reason_v4))

        top_entry_v3 = json.loads((self.content_dir / "rule.schedule1-top-entry.v3.json").read_text("utf-8"))
        self.assertEqual(top_entry_v3.get("publishes"), "tax.us.2025.schedule1.top-entry")
        path0 = top_entry_v3.get("selection", {}).get("paths", [])[0]
        self.assertEqual(path0.get("when", {}).get("op"), "require_closed")
        self.assertEqual(path0.get("when", {}).get("source_set"), "tax.us.2025.f1099k")
        self.assertIn("tax.us.2025.f1099k.box1a-subtotal", path0.get("requires", []))

        unres_v3 = json.loads((self.content_dir / "rule.f1099k-unresolved.v3.json").read_text("utf-8"))
        self.assertEqual(unres_v3.get("publishes"), "tax.us.2025.f1099k.unresolved")

        attachment_v4 = json.loads((self.content_dir / "rule.attachment.schedule-1.v4.json").read_text("utf-8"))
        item = next(i for i in attachment_v4.get("itemizations", []) if i.get("part_id") == "sch1-top-entry-f1099k")
        self.assertEqual(item.get("authority", {}).get("source_family", {}).get("version"), "v2")
        self.assertEqual(item.get("tie_out", {}).get("line_symbol"), "tax.us.2025.f1099k.box1a-subtotal")
        self.assertIn("tax.us.2025.schedule1.top-entry", attachment_v4.get("requirement", {}).get("subtotals", []))

    def test_package_v49_validation_and_release(self) -> None:
        """package.core-calculations.v49 validates against all members with 0 issues."""
        corpus: dict[tuple[str, str], dict[str, Any]] = {}
        for path in self.content_dir.glob("*.json"):
            if path.name.startswith(("published-packages", "package.")):
                continue
            try:
                data = json.loads(path.read_text("utf-8"))
                if isinstance(data, dict) and "id" in data and "version" in data:
                    corpus[(data["id"], data["version"])] = data
            except Exception:
                pass

        pkg_path = self.content_dir / "package.core-calculations.v49.json"
        pkg_data = json.loads(pkg_path.read_text("utf-8"))
        manifest_path = self.content_dir / "published-packages.v47.json"
        checksums = load_published_citizen_checksums(manifest_path)
        schemas = DerivationSchemas()

        result = validate_package(pkg_data, corpus, schemas, checksums)
        self.assertTrue(result.ok, f"Package v49 validation issues: {result.issues}")
        self.assertEqual(len(result.issues), 0)

        # Confirm package checksum matches canonical instance checksum
        self.assertEqual(pkg_data["package_checksum"], package_instance_checksum(pkg_data))

        # Release v47 references published-packages.v47.json SHA-256
        release_path = (
            Path(__file__).resolve().parent.parent
            / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
            / "demo.release.sli-worksheet-integration.2025.v47.json"
        )
        release_data = json.loads(release_path.read_text("utf-8"))
        manifest_sha = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        self.assertEqual(release_data["package_registry_sha256"], manifest_sha)

    def test_f1099k_family_version_from_package(self) -> None:
        """f1099k_family_version_from_package correctly inspects packages."""
        v48_path = self.content_dir / "package.core-calculations.v48.json"
        v49_path = self.content_dir / "package.core-calculations.v49.json"

        self.assertEqual(f1099k_family_version_from_package(v48_path), "v1")
        self.assertEqual(f1099k_family_version_from_package(str(v48_path)), "v1")
        self.assertEqual(f1099k_family_version_from_package(json.loads(v48_path.read_text("utf-8"))), "v1")

        self.assertEqual(f1099k_family_version_from_package(v49_path), "v2")
        self.assertEqual(f1099k_family_version_from_package(str(v49_path)), "v2")
        self.assertEqual(f1099k_family_version_from_package(json.loads(v49_path.read_text("utf-8"))), "v2")

        # Fallback to module constant on empty or non-1099-K package
        self.assertEqual(f1099k_family_version_from_package({}), FAMILY_VERSION)
        self.assertEqual(FAMILY_VERSION, "v1")

    def _adopt_package(
        self,
        log: ActLog,
        pkg_version: str,
        *,
        actor: str = "demo.taxpayer",
        scope: dict[str, str] | None = None,
        revision: int = 1,
        supersedes: str | None = None,
        corrupt_release: bool = False,
    ) -> dict[str, Any]:
        pkg_file = self.content_dir / f"package.core-calculations.{pkg_version}.json"
        pkg_data = json.loads(pkg_file.read_text("utf-8"))
        release_ver = "v47" if pkg_version == "v49" else "v46"
        release_dir = (
            self.content_dir.parent.parent.parent
            / "sample_data"
            / "student_loan_worksheet_integration"
            / "publication_surface"
            / "releases"
        )
        release_file = release_dir / f"demo.release.sli-worksheet-integration.2025.{release_ver}.json"
        release_checksum = (
            "0" * 64 if corrupt_release else hashlib.sha256(release_file.read_bytes()).hexdigest()
        )
        payload: dict[str, Any] = {
            "package": {
                "id": pkg_data["id"],
                "version": pkg_data["version"],
                "checksum": pkg_data["package_checksum"],
            },
            "release": {
                "id": "demo.release.sli-worksheet-integration.2025",
                "version": release_ver,
                "checksum": release_checksum,
            },
            "scope": scope or {"jurisdiction": "us", "year": "2025"},
            "revision": revision,
        }
        if supersedes is not None:
            payload["supersedes"] = supersedes
        current_rev = log.read().revision
        item = act(
            current_rev,
            "package-adoption",
            payload,
        )
        item["actor"] = actor
        item["committed_against"] = current_rev
        log.append(item, expected_revision=current_rev)
        return item

    def test_f1099k_family_version_for_workspace_and_recording(self) -> None:
        """Writers automatically resolve family_version from adopted package without hard-coding."""
        log_path = Path(self.temp.name) / "workspace_v49"
        log = ActLog(log_path, self.registry)

        # Before any package adoption, defaults to "v1"
        self.assertEqual(f1099k_family_version_for_workspace(log, actor="demo.taxpayer"), "v1")

        # Adopt v49 package
        self._adopt_package(log, "v49")
        self.assertEqual(f1099k_family_version_for_workspace(log, actor="demo.taxpayer"), "v2")

        # Record a statement without passing family_version -> writes with "v2"
        res = record_f1099k_statement_durably(
            log,
            self.registry,
            submission_id="sub.001",
            payer_id="demo.payer.1",
            payer_label="Payer One",
            statement_ref="stmt.001",
            statement_label="Statement 1",
            box1a=1000.0,
            box4=0.0,
            evidence_id="ev.001",
            actor="demo.taxpayer",
            at="2026-04-15T12:00:00Z",
            expected_revision=log.read().revision,
        )
        self.assertGreater(res["revision"], 0)

        # Verify acts written into log have family version "v2"
        acts = log.read().acts
        genesis_acts = [a for a in acts if a.get("kind") == "horizon-genesis"]
        self.assertEqual(len(genesis_acts), 1)
        self.assertEqual(genesis_acts[0]["payload"]["family"]["id"], FAMILY_ID)
        self.assertEqual(genesis_acts[0]["payload"]["family"]["version"], "v2")

        transition_acts = [a for a in acts if a.get("kind") == "member-transition"]
        self.assertEqual(len(transition_acts), 1)
        self.assertEqual(transition_acts[0]["payload"]["family"]["id"], FAMILY_ID)
        self.assertEqual(transition_acts[0]["payload"]["family"]["version"], "v2")

    def test_f1099k_v48_workspace_preserves_v1(self) -> None:
        """A workspace adopting v48 preserves family version v1 automatically."""
        log_path = Path(self.temp.name) / "workspace_v48"
        log = ActLog(log_path, self.registry)

        self._adopt_package(log, "v48")
        self.assertEqual(f1099k_family_version_for_workspace(log, actor="demo.taxpayer"), "v1")

        res = record_f1099k_statement_durably(
            log,
            self.registry,
            submission_id="sub.v48.001",
            payer_id="demo.payer.v48",
            payer_label="Payer V48",
            statement_ref="stmt.v48.001",
            statement_label="Statement V48",
            box1a=500.0,
            box4=0.0,
            evidence_id="ev.v48.001",
            actor="demo.taxpayer",
            at="2026-04-15T12:00:00Z",
            expected_revision=log.read().revision,
        )
        self.assertGreater(res["revision"], 0)

        acts = log.read().acts
        genesis_acts = [a for a in acts if a.get("kind") == "horizon-genesis"]
        self.assertEqual(len(genesis_acts), 1)
        self.assertEqual(genesis_acts[0]["payload"]["family"]["version"], "v1")

        transition_acts = [a for a in acts if a.get("kind") == "member-transition"]
        self.assertEqual(len(transition_acts), 1)
        self.assertEqual(transition_acts[0]["payload"]["family"]["version"], "v1")

    def test_record_no_statements_family_version_threading(self) -> None:
        """record_f1099k_no_statements_durably resolves family version from workspace."""
        log_path = Path(self.temp.name) / "workspace_no_stmt"
        log = ActLog(log_path, self.registry)

        self._adopt_package(log, "v49")
        res = record_f1099k_no_statements_durably(
            log,
            self.registry,
            submission_id="sub.none.001",
            evidence_id="ev.none.001",
            actor="demo.taxpayer",
            at="2026-04-15T12:00:00Z",
            expected_revision=log.read().revision,
        )
        self.assertGreater(res["revision"], 0)

        acts = log.read().acts
        genesis_acts = [a for a in acts if a.get("kind") == "horizon-genesis"]
        self.assertEqual(len(genesis_acts), 1)
        self.assertEqual(genesis_acts[0]["payload"]["family"]["version"], "v2")

    def test_adoption_by_other_actor_preserves_v1(self) -> None:
        """Adoption by another actor does not select for current actor, keeping v1."""
        log_path = Path(self.temp.name) / "workspace_other_actor"
        log = ActLog(log_path, self.registry)

        self._adopt_package(log, "v49", actor="other.taxpayer")
        # For demo.taxpayer, there is no adoption in scope -> v1
        self.assertEqual(f1099k_family_version_for_workspace(log, actor="demo.taxpayer"), "v1")

        # Recording for demo.taxpayer writes with v1
        res = record_f1099k_statement_durably(
            log,
            self.registry,
            submission_id="sub.actor.001",
            payer_id="demo.payer.actor",
            payer_label="Payer Actor",
            statement_ref="stmt.actor.001",
            statement_label="Statement Actor",
            box1a=750.0,
            box4=0.0,
            evidence_id="ev.actor.001",
            actor="demo.taxpayer",
            at="2026-04-15T12:00:00Z",
            expected_revision=log.read().revision,
        )
        self.assertGreater(res["revision"], 0)
        acts = log.read().acts
        genesis_acts = [a for a in acts if a.get("kind") == "horizon-genesis"]
        self.assertEqual(genesis_acts[0]["payload"]["family"]["version"], "v1")

    def test_adoption_by_other_scope_preserves_v1(self) -> None:
        """Adoption for another scope (e.g. tax year 2024) preserves v1 for 2025."""
        log_path = Path(self.temp.name) / "workspace_other_scope"
        log = ActLog(log_path, self.registry)

        self._adopt_package(log, "v49", scope={"jurisdiction": "us", "year": "2024"})
        self.assertEqual(f1099k_family_version_for_workspace(log, actor="demo.taxpayer", tax_year="2025"), "v1")

    def test_superseded_adoption_selects_active(self) -> None:
        """A superseded adoption yields to the superseding act."""
        log_path = Path(self.temp.name) / "workspace_superseded"
        log = ActLog(log_path, self.registry)

        # First adopt v49 (revision 1)
        act1 = self._adopt_package(log, "v49", revision=1)
        self.assertEqual(f1099k_family_version_for_workspace(log, actor="demo.taxpayer"), "v2")

        # Now adopt v48 (revision 2), superseding act1
        act2 = self._adopt_package(log, "v48", revision=2, supersedes=act1["act_id"])
        self.assertEqual(f1099k_family_version_for_workspace(log, actor="demo.taxpayer"), "v1")

        # Now adopt v49 (revision 3), superseding act2
        self._adopt_package(log, "v49", revision=3, supersedes=act2["act_id"])
        self.assertEqual(f1099k_family_version_for_workspace(log, actor="demo.taxpayer"), "v2")

    def test_unresolvable_adoption_raises_error(self) -> None:
        """When an adoption exists in scope but cannot be resolved, refuse with named error."""
        log_path = Path(self.temp.name) / "workspace_unresolvable"
        log = ActLog(log_path, self.registry)

        # Adopt with corrupt release checksum
        self._adopt_package(log, "v49", corrupt_release=True)

        with self.assertRaises(F1099KAdoptionResolutionError):
            f1099k_family_version_for_workspace(log, actor="demo.taxpayer")

        with self.assertRaises(F1099KAdoptionResolutionError):
            record_f1099k_statement_durably(
                log,
                self.registry,
                submission_id="sub.bad.001",
                payer_id="demo.payer.bad",
                payer_label="Payer Bad",
                statement_ref="stmt.bad.001",
                statement_label="Statement Bad",
                box1a=100.0,
                box4=0.0,
                evidence_id="ev.bad.001",
                actor="demo.taxpayer",
                at="2026-04-15T12:00:00Z",
                expected_revision=log.read().revision,
            )


if __name__ == "__main__":
    unittest.main()
