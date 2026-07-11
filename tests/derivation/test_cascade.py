"""Patch acceptance: the correction cascade closes through the machinery.

The signature product move, proven end to end over one workspace act log:
adopt a vocabulary, assert a W-2 input finding, derive line1a and line9 from it,
append the publications — then supersede the W-2. The derived findings, which
stood on the now-displaced input, leave current state; a re-derivation is not
required for the cascade to be correct (Article 6, incomplete-but-true).
"""

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.kernel.act_log import ActLog
from packages.derivation.loader import DerivationSchemas, load_canon, workspace_registry
from packages.derivation.projection import workspace_currency
from packages.derivation.runner import (
    InputFinding,
    RunContext,
    SourceFact,
    append_publications,
    run,
)
from tests.support import act, demo_bundle, demo_entity, demo_finding, demo_payment_fact_id

EXAMPLES = Path(__file__).resolve().parent.parent.parent / "packages" / "sample_data" / "derivation" / "examples"

W2_FACT = demo_payment_fact_id("demo-corp-a")


def _load(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((EXAMPLES / name).read_text("utf-8"))
    return loaded


class CorrectionCascade(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.registry = workspace_registry()
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.log = ActLog(Path(self._tmp.name) / "ws", self.registry)

        # Kernel workspace: adopt the vocabulary, introduce the counterparty,
        # assert the W-2 input finding (value 42000).
        rev = self.log.append(act(0, "bundle-adoption", {"bundle": demo_bundle()}), expected_revision=0)
        rev = self.log.append(act(rev, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Corp A")}), expected_revision=rev)
        w2 = demo_finding("finding-w2", value=42000, basis="attested", evidence_ids=[])
        rev = self.log.append(act(rev, "assertion", {"finding": w2}), expected_revision=rev)

        # Derive line1a (from the W-2) and line9 (from line1a), then persist the
        # publications into the same act log. The W-2 source is pinned by the
        # kernel finding id, so the derivation edge points back to it.
        ctx = RunContext(
            run_id="run.1",
            rules=[_load("rule-artifact.wages-line1a.json"), _load("rule-artifact.total-line9.json")],
            parameters={},
            canon=load_canon(self.schemas),
            inputs=[InputFinding("rounding.convention", "half_up", "f.rounding", "input")],
            sources=[SourceFact("demo.w2.box1", "42000", "finding-w2")],
            closed_sets=frozenset({"demo.w2"}),
            adoption_pin={"role": "adoption", "id": "demo.package.first-slice.2025", "version": "v1"},
            governance_pins=[{"role": "governance", "id": "governance.constitution", "version": "v1"}],
        )
        self.result = run(ctx, self.schemas)
        append_publications(self.log, self.result, actor="user", at="2026-01-01T00:00:00Z")
        self.line1a = next(p.finding["id"] for p in self.result.publications if p.finding["symbol"] == "demo.form1040.line1a")
        self.line9 = next(p.finding["id"] for p in self.result.publications if p.finding["symbol"] == "demo.form1040.line9")

    def test_before_supersession_all_derived_findings_are_current(self) -> None:
        _, derivation = workspace_currency(self.log.read().acts, self.registry)
        self.assertEqual(derivation.displaced_derived_ids, frozenset())
        self.assertEqual(derivation.current_derived_ids, frozenset({self.line1a, self.line9}))

    def test_superseding_the_input_displaces_the_derived_chain(self) -> None:
        # Supersede the W-2: a new finding for the same fact (value 50000).
        rev = self.log.read().revision
        new_w2 = demo_finding("finding-w2-corrected", value=50000, basis="attested", evidence_ids=[])
        self.log.append(act(rev, "assertion", {"finding": new_w2}), expected_revision=rev)

        kernel, derivation = workspace_currency(self.log.read().acts, self.registry)
        # Kernel: the old W-2 finding is displaced by the correction.
        self.assertIn("finding-w2", kernel.displaced_finding_ids)
        self.assertIn("finding-w2-corrected", kernel.current_finding_ids)
        # Derivation: both derived findings that stood on it leave current state,
        # chaining W-2 -> line1a -> line9.
        self.assertEqual(derivation.displaced_derived_ids, frozenset({self.line1a, self.line9}))
        self.assertEqual(derivation.current_derived_ids, frozenset())

    def test_superseding_an_unrelated_finding_does_not_displace(self) -> None:
        # A correction to a different fact leaves the derived chain current.
        rev = self.log.read().revision
        self.log.append(act(rev, "entity-introduced", {"entity": demo_entity("demo-corp-b", "Corp B")}), expected_revision=rev)
        rev = self.log.read().revision
        other = demo_finding("finding-other", fact_id=demo_payment_fact_id("demo-corp-b"), value=999, basis="attested", evidence_ids=[])
        self.log.append(act(rev, "assertion", {"finding": other}), expected_revision=rev)

        _, derivation = workspace_currency(self.log.read().acts, self.registry)
        self.assertEqual(derivation.displaced_derived_ids, frozenset())


if __name__ == "__main__":
    unittest.main()
