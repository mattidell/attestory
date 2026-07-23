"""Focused authoritative-path tests for the local push-envelope posture audit."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools import audit_push_envelope_posture as posture_audit


REPO_ROOT = Path(__file__).resolve().parent.parent
AUDIT = REPO_ROOT / "tools" / "audit_push_envelope_posture.py"


class PushEnvelopePostureAuditTests(unittest.TestCase):
    def test_command_reports_the_verified_local_posture(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(AUDIT)], capture_output=True, text=True, check=False
        )

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(
            json.loads(completed.stdout),
            {
                "credential_confinement": "unestablished",
                "hooked_marker_refused": True,
                "hooks_verified": True,
                "no_verify_bypass_reachable": True,
            },
        )

    def test_missing_hook_never_reports_an_affirmative_posture(self) -> None:
        with TemporaryDirectory() as temporary:
            workspace, remote = posture_audit.make_audit_workspace(Path(temporary))
            (workspace / ".git" / "hooks" / "pre-push").unlink()

            result = posture_audit.audit_workspace(workspace, remote)

        self.assertFalse(result.hooks_verified)
        self.assertFalse(result.verified)
        self.assertEqual(result.credential_confinement, "unestablished")

    def test_tampered_hook_never_reports_an_affirmative_posture(self) -> None:
        with TemporaryDirectory() as temporary:
            workspace, remote = posture_audit.make_audit_workspace(Path(temporary))
            hook = workspace / ".git" / "hooks" / "pre-push"
            hook.write_bytes(hook.read_bytes() + b"# altered\n")

            result = posture_audit.audit_workspace(workspace, remote)

        self.assertFalse(result.hooks_verified)
        self.assertFalse(result.verified)
        self.assertEqual(result.credential_confinement, "unestablished")


if __name__ == "__main__":
    unittest.main()
