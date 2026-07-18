"""Track 4b: repo-side ADR-0031 envelope gate (scanner, installer, per-clone check).

Seeded markers below are built by concatenation so this file's own bytes
never form a forbidden marker; the committed text therefore passes the
gate it tests.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

REPO_ROOT = Path(__file__).resolve().parent.parent
SCANNER = REPO_ROOT / "tools" / "envelope_scan.py"
INSTALLER = REPO_ROOT / "tools" / "install_envelope_hooks.py"
PYTHON = sys.executable

SEED_USER_PATH = "/Users" + "/someone/documents/w2-2025.pdf"
SEED_SSN = "123-45" + "-6789"
SEED_DIR = "upl" + "oads"
PRAGMA = "envelope-scan:" + " allow"


def _run(
    args: list[str], cwd: Path, stdin_text: str | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, cwd=cwd, input=stdin_text, capture_output=True, text=True
    )


def _git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return _run(
        ["git", "-c", "user.name=demo", "-c", "user.email=demo@example.invalid", *args],
        cwd,
    )


def _init_repo(root: Path) -> None:
    for args in (["init", "-q"],):
        completed = _git(args, root)
        assert completed.returncode == 0, completed.stderr


def _stage(root: Path, name: str, text: str) -> None:
    target = root / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    completed = _git(["add", name], root)
    assert completed.returncode == 0, completed.stderr


class ScannerTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()
        self.addCleanup(self._tmp.cleanup)
        _init_repo(self.root)

    def _scan_staged(self) -> subprocess.CompletedProcess[str]:
        return _run([PYTHON, str(SCANNER), "--staged"], self.root)

    def test_staged_personal_path_is_refused(self) -> None:
        _stage(self.root, "note.md", f"see {SEED_USER_PATH}\n")
        completed = self._scan_staged()
        self.assertEqual(completed.returncode, 1, completed.stdout)
        self.assertIn("refused", completed.stdout)

    def test_staged_ssn_shape_is_refused(self) -> None:
        _stage(self.root, "facts.json", f'{{"value": "{SEED_SSN}"}}\n')
        self.assertEqual(self._scan_staged().returncode, 1)

    def test_staged_forbidden_path_name_is_refused(self) -> None:
        _stage(self.root, f"{SEED_DIR}/scan.json", "{}\n")
        self.assertEqual(self._scan_staged().returncode, 1)

    def test_clean_staged_envelope_passes(self) -> None:
        _stage(self.root, "demo.json", '{"id": "demo.w2.1", "value": 1}\n')
        completed = self._scan_staged()
        self.assertEqual(completed.returncode, 0, completed.stdout)

    def test_quoted_bare_marker_documentation_passes(self) -> None:
        # Review records quote bare markers; without a following path
        # segment they are documentation, not a leak.
        _stage(self.root, "review.md", "scanned for (`/Users/`, `local-data/`)\n")
        self.assertEqual(self._scan_staged().returncode, 0)

    def test_pragma_line_is_exempt(self) -> None:
        _stage(self.root, "fixture.md", f"synthetic {SEED_USER_PATH}  <!-- {PRAGMA} -->\n")
        self.assertEqual(self._scan_staged().returncode, 0)

    def test_push_range_scan_refuses_seeded_commit(self) -> None:
        _stage(self.root, "clean.md", "clean\n")
        _git(["commit", "-q", "-m", "clean", "--no-verify"], self.root)
        first = _git(["rev-parse", "HEAD"], self.root).stdout.strip()
        _stage(self.root, "leak.md", f"{SEED_USER_PATH}\n")
        _git(["commit", "-q", "-m", "leak", "--no-verify"], self.root)
        second = _git(["rev-parse", "HEAD"], self.root).stdout.strip()
        stdin_text = f"refs/heads/main {second} refs/heads/main {first}\n"
        completed = _run([PYTHON, str(SCANNER), "--push"], self.root, stdin_text)
        self.assertEqual(completed.returncode, 1, completed.stdout)

    def test_push_new_ref_scans_unpushed_commits(self) -> None:
        _stage(self.root, "leak.md", f"{SEED_USER_PATH}\n")
        _git(["commit", "-q", "-m", "leak", "--no-verify"], self.root)
        head = _git(["rev-parse", "HEAD"], self.root).stdout.strip()
        zero = "0" * len(head)
        stdin_text = f"refs/heads/new {head} refs/heads/new {zero}\n"
        completed = _run([PYTHON, str(SCANNER), "--push"], self.root, stdin_text)
        self.assertEqual(completed.returncode, 1, completed.stdout)


class HookInstallTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()
        self.addCleanup(self._tmp.cleanup)
        _init_repo(self.root)
        # The shim invokes the repo-relative committed scanner.
        (self.root / "tools").mkdir()
        shutil.copy(SCANNER, self.root / "tools" / "envelope_scan.py")
        completed = _run([PYTHON, str(INSTALLER)], self.root)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_installed_gates_verify_and_tamper_is_detected(self) -> None:
        self.assertEqual(_run([PYTHON, str(SCANNER), "--verify"], self.root).returncode, 0)
        hook = self.root / ".git" / "hooks" / "pre-push"
        hook.write_bytes(hook.read_bytes() + b"# edited\n")
        completed = _run([PYTHON, str(SCANNER), "--verify"], self.root)
        self.assertEqual(completed.returncode, 1)
        self.assertIn("does not match", completed.stdout)

    def test_real_commit_of_seeded_marker_is_refused_by_hook(self) -> None:
        _stage(self.root, "leak.md", f"{SEED_USER_PATH}\n")
        completed = _git(["commit", "-q", "-m", "leak"], self.root)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("refused", completed.stdout + completed.stderr)

    def test_real_commit_of_clean_envelope_passes_hook(self) -> None:
        _stage(self.root, "demo.md", "synthetic demo content\n")
        completed = _git(["commit", "-q", "-m", "clean"], self.root)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)


class ThisCloneTests(unittest.TestCase):
    def test_this_clone_has_verified_envelope_gates(self) -> None:
        completed = _run([PYTHON, str(SCANNER), "--verify"], REPO_ROOT)
        self.assertEqual(
            completed.returncode,
            0,
            "the ADR-0031 envelope gates are not installed in this clone; "
            "run: python3 tools/install_envelope_hooks.py\n" + completed.stdout,
        )


if __name__ == "__main__":
    unittest.main()
