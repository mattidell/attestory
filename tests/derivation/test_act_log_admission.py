"""Patch verification: derived-publication acts in the workspace act log.

ADR-0010: publication acts land in the act log (ADR-0008), validated by the
combined registry; the kernel projection owns only kernel kinds and passes over
derived-publication acts (compose-over), so a shared log projects cleanly.
"""

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.kernel.act_log import ActLog
from packages.kernel.read_models import build_read_model
from packages.derivation.loader import DerivationSchemas, load_canon, workspace_registry
from packages.derivation.runner import (
    InputFinding,
    RunContext,
    SourceFact,
    append_publications,
    run,
)

EXAMPLES = Path(__file__).resolve().parent.parent.parent / "packages" / "sample_data" / "derivation" / "examples"


def _load(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((EXAMPLES / name).read_text("utf-8"))
    return loaded


class ActLogAdmission(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.registry = workspace_registry()
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.workspace = Path(self._tmp.name) / "ws"
        ctx = RunContext(
            run_id="run.1",
            rules=[_load("rule-artifact.wages-line1a.json")],
            parameters={},
            canon=load_canon(self.schemas),
            inputs=[InputFinding("rounding.convention", "half_up", "f.rounding", "input")],
            sources=[SourceFact("demo.w2.box1", "40000", "f.w2a"),
                     SourceFact("demo.w2.box1", "2000", "f.w2b")],
            adoption_pin={"role": "adoption", "id": "demo.package.first-slice.2025", "version": "v1"},
            governance_pins=[{"role": "governance", "id": "governance.constitution", "version": "v1"}],
        )
        self.result = run(ctx, self.schemas)

    def test_publications_round_trip_through_the_act_log(self) -> None:
        log = ActLog(self.workspace, self.registry)
        revision = append_publications(log, self.result, actor="user", at="2026-01-01T00:00:00Z")
        self.assertEqual(revision, len(self.result.publications))
        contents = log.read()  # re-reads and re-validates every committed act
        self.assertEqual(len(contents.acts), len(self.result.publications))
        kinds = {act["kind"] for act in contents.acts}
        self.assertEqual(kinds, {"derived-publication"})

    def test_act_ids_are_content_addressed_and_stable(self) -> None:
        log = ActLog(self.workspace, self.registry)
        append_publications(log, self.result, actor="user", at="2026-01-01T00:00:00Z")
        first = [act["act_id"] for act in log.read().acts]
        # A different persistence context (actor/timestamp) yields the same ids.
        other = Path(self._tmp.name) / "ws2"
        log2 = ActLog(other, self.registry)
        append_publications(log2, self.result, actor="auditor", at="2027-06-06T12:00:00Z")
        second = [act["act_id"] for act in log2.read().acts]
        self.assertEqual(first, second)

    def test_kernel_projection_ignores_publication_acts(self) -> None:
        log = ActLog(self.workspace, self.registry)
        append_publications(log, self.result, actor="user", at="2026-01-01T00:00:00Z")
        model = build_read_model(log.read().acts, self.registry)
        # The kernel projects no findings from a log of only publication acts —
        # it does not error, and it does not absorb derived findings.
        self.assertEqual(model["current"]["finding_ids"], [])
        self.assertEqual(model["revision"], len(self.result.publications))


if __name__ == "__main__":
    unittest.main()
