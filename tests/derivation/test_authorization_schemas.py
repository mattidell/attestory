"""Published standing-authorization schemas (ADR-0069) and act-log admission."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from packages.derivation.authorization import END_ACT_KIND, GRANT_ACT_KIND
from packages.derivation.loader import DerivationSchemas, workspace_registry
from packages.kernel.act_log import ActLog
from packages.kernel.findings import KERNEL_ACT_KINDS, project as kernel_project
from packages.kernel.schema_registry import SchemaValidationError

UNIVERSE = "a" * 64


def _citizen(
    grant_id: str = "demo.auth.2025.a",
    subject_id: str = "demo.subject.a",
    tax_year: str = "2025",
    universe_id: str = UNIVERSE,
    supersedes: str | None = None,
) -> dict[str, str]:
    citizen: dict[str, str] = {
        "schema": "workspace-calculation-authorization.v1",
        "id": grant_id,
        "subject_id": subject_id,
        "tax_year": tax_year,
        "universe_id": universe_id,
    }
    if supersedes is not None:
        citizen["supersedes"] = supersedes
    return citizen


def _grant_act(index: int = 0) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.act.grant.{index}",
        "kind": GRANT_ACT_KIND,
        "actor": "demo.user",
        "at": "2026-01-15T12:00:00Z",
        "committed_against": index,
        "payload": {"authorization": _citizen()},
    }


class AuthorizationSchemas(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.registry = workspace_registry()

    def test_grant_citizen_validates(self) -> None:
        self.schemas.validate_declared(_citizen())
        self.schemas.validate_declared(_citizen(supersedes="demo.auth.2025.prior"))

    def test_grant_payload_validates(self) -> None:
        self.schemas.validate("act-calculation-authorization.v1", {"authorization": _citizen()})

    def test_end_payload_validates_both_modes(self) -> None:
        for ending in ("suspend", "withdraw"):
            self.schemas.validate(
                "act-calculation-authorization-end.v1",
                {"authorization_id": "demo.auth.2025.a", "ending": ending},
            )

    def test_unknown_ending_is_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate(
                "act-calculation-authorization-end.v1",
                {"authorization_id": "demo.auth.2025.a", "ending": "expire"},
            )

    def test_short_universe_id_is_rejected(self) -> None:
        citizen = _citizen(universe_id="abc")
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(citizen)

    def test_grant_kinds_are_not_kernel_registered(self) -> None:
        self.assertNotIn(GRANT_ACT_KIND, KERNEL_ACT_KINDS)
        self.assertNotIn(END_ACT_KIND, KERNEL_ACT_KINDS)

    def test_act_log_round_trip_and_kernel_compose_over(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        log = ActLog(Path(tmp.name) / "ws", self.registry)
        grant = _grant_act(0)
        log.append(grant, expected_revision=0)
        end = {
            "schema": "act.v1",
            "act_id": "demo.act.end.1",
            "kind": END_ACT_KIND,
            "actor": "demo.user",
            "at": "2026-01-15T12:01:00Z",
            "committed_against": 1,
            "payload": {"authorization_id": "demo.auth.2025.a", "ending": "suspend"},
        }
        log.append(end, expected_revision=1)
        contents = log.read()
        self.assertEqual(len(contents.acts), 2)
        self.assertEqual({act["kind"] for act in contents.acts}, {GRANT_ACT_KIND, END_ACT_KIND})

        kernel_state = kernel_project(contents.acts, self.registry)
        self.assertEqual(kernel_state.fact_state.entities, {})


if __name__ == "__main__":
    unittest.main()
