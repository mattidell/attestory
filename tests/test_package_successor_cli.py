"""Exercise the command as a process with a committed historical delta."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages/content/tax/2025"
RELEASES = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"


class CommandTests(unittest.TestCase):
    def test_invalid_option_has_concise_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            corpus = root / "corpus"
            corpus.mkdir()
            package, registry, release, changes = [root / name for name in ("package.json", "registry.json", "release.json", "changes.json")]
            for path in (package, registry, release):
                path.write_text("{}")
            changes.write_text('{"package_version":"v2","release_version":"v2","registry_new_key_order":null}')
            target = root / "candidate"
            command = [sys.executable, "-m", "tools.package_successor", "--package", str(package), "--registry", str(registry),
                       "--release", str(release), "--corpus", str(corpus), "--changes", str(changes), "--output", str(target)]
            completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("invalid registry_new_key_order", completed.stderr)
            self.assertNotIn("Traceback", completed.stderr)
            self.assertFalse(target.exists())

    def test_command_and_existing_destination_refusal(self) -> None:
        package = CONTENT / "package.core-calculations.v57.json"
        registry = CONTENT / "published-packages.v55.json"
        release = RELEASES / "demo.release.sli-worksheet-integration.2025.v55.json"
        changes = ROOT / "tests/fixtures/package_successor/v57-to-v58.json"
        sources = [path.read_bytes() for path in (package, registry, release, changes)]
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory).resolve() / "candidate"
            command = [sys.executable, "-m", "tools.package_successor", "--package", str(package),
                       "--registry", str(registry), "--release", str(release), "--corpus", str(CONTENT),
                       "--changes", str(changes), "--output", str(target)]
            completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=True)
            report = json.loads(completed.stdout)
            self.assertIn("ADR-0082", report["publication_boundary"])
            self.assertTrue(report["inherited_inconsistencies"])
            self.assertEqual((target / "package.json").read_bytes(), (CONTENT / "package.core-calculations.v58.json").read_bytes())
            self.assertEqual((target / "registry.json").read_bytes(), (CONTENT / "published-packages.v56.json").read_bytes())
            self.assertEqual((target / "release.json").read_bytes(), (RELEASES / "demo.release.sli-worksheet-integration.2025.v56.json").read_bytes())
            refused = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertNotEqual(refused.returncode, 0)
            self.assertIn("destination already exists", refused.stderr)
            self.assertEqual([path.read_bytes() for path in (package, registry, release, changes)], sources)
