"""Track 4 verification: correction through derived displacement and
explicit re-derivation, over one real workspace act log.

Boundary (milestone plan): no auto-rerun orchestration, no W-2c documentary
semantics. The correction is an ordinary same-fact assertion (Track 2); the
rerun is an explicit second derivation call, never triggered automatically.
This is the product's signature move (per the Derivation Cascade
Reconciliation patch): superseding an input displaces every derived finding
that stood on it, and a fresh run publishes the successor.
"""

import json
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.loader import DerivationSchemas, load_canon, workspace_registry
from packages.derivation.projection import workspace_currency
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import InputFinding, RunContext, SourceFact, run
from packages.kernel.read_models import build_read_model

WORKSPACE = Path("packages/sample_data/tax/workspaces/w2_correction_cascade")
RULE = json.loads(Path("packages/content/tax/2025/rule.wages-line1a.json").read_text("utf-8"))

ADOPTION_PIN = {"role": "adoption", "id": "tax.us.2025.package.first-tax-slice", "version": "v1"}
GOV_PINS = [{"role": "governance", "id": "governance.constitution", "version": "v1"}]
OUTPUT_SYMBOL = "tax.us.2025.wages.total-w2-box1"


def _load(path: Path) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads(path.read_text("utf-8"))
    return loaded


def _context(source_finding_id: str, source_value: str, run_id: str) -> RunContext:
    schemas = DerivationSchemas()
    return RunContext(
        run_id=run_id,
        rules=[RULE],
        parameters={},
        canon=load_canon(schemas),
        inputs=[InputFinding("rounding.convention", "half_up", "tax.us.2025.finding.rounding-convention", "input")],
        sources=[SourceFact("tax.us.2025.w2.box1-wages", source_value, source_finding_id)],
        closed_sets=frozenset(),
        adoption_pin=ADOPTION_PIN,
        governance_pins=GOV_PINS,
    )


class CommittedFixtureGolden(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = workspace_registry()
        self.acts = tuple(
            json.loads(line) for line in (WORKSPACE / "acts.jsonl").read_text("utf-8").splitlines()
        )
        self.ids = _load(WORKSPACE / "expected" / "ids.json")

    def test_workspace_rebuilds_its_kernel_read_model_golden(self) -> None:
        model = build_read_model(self.acts, self.registry)
        expected = _load(WORKSPACE / "expected" / "read-model.json")
        self.assertEqual(model, expected)

    def test_kernel_projection_ignores_derived_publication_acts(self) -> None:
        # ADR-0010 compose-over: the kernel currently holds only the corrected
        # box-1 finding; derived findings never enter the kernel's own view.
        model = build_read_model(self.acts, self.registry)
        self.assertEqual(model["current"]["finding_ids"], ["demo-finding-w2-alpha-1-box1-corrected"])


class CorrectionCascadeAndRederivation(unittest.TestCase):
    """The Synthetic Fixtures w2_correction + w2_rederive story, end to end."""

    def setUp(self) -> None:
        self.registry = workspace_registry()
        self.acts = tuple(
            json.loads(line) for line in (WORKSPACE / "acts.jsonl").read_text("utf-8").splitlines()
        )
        self.ids = _load(WORKSPACE / "expected" / "ids.json")
        # The five acts before the correction: bundle, employer, slip,
        # evidence, original assertion, plus the first derived-publication.
        self.pre_correction_acts = self.acts[:6]

    def test_before_correction_the_original_derived_finding_is_current(self) -> None:
        _, derivation = workspace_currency(self.pre_correction_acts, self.registry)
        self.assertEqual(derivation.current_derived_ids, frozenset({self.ids["line1a_v1"]}))
        self.assertEqual(derivation.displaced_derived_ids, frozenset())

    def test_correction_displaces_the_source_and_cascades_to_the_derived_finding(self) -> None:
        # Acts through the corrected assertion, before any rerun: the derived
        # finding that stood on the now-displaced source leaves current state
        # even though nothing about the derived finding itself was rewritten.
        mid_acts = self.acts[:8]
        kernel, derivation = workspace_currency(mid_acts, self.registry)
        self.assertIn("demo-finding-w2-alpha-1-box1", kernel.displaced_finding_ids)
        self.assertIn("demo-finding-w2-alpha-1-box1-corrected", kernel.current_finding_ids)
        self.assertEqual(derivation.displaced_derived_ids, frozenset({self.ids["line1a_v1"]}))
        self.assertEqual(derivation.current_derived_ids, frozenset())
        reason = derivation.reasons[self.ids["line1a_v1"]][0]
        self.assertEqual(reason.kind, "derivation")
        self.assertEqual(reason.by, "demo-finding-w2-alpha-1-box1")

    def test_explicit_rerun_publishes_the_corrected_successor(self) -> None:
        kernel, derivation = workspace_currency(self.acts, self.registry)
        self.assertEqual(derivation.displaced_derived_ids, frozenset({self.ids["line1a_v1"]}))
        self.assertEqual(derivation.current_derived_ids, frozenset({self.ids["line1a_v2"]}))

        successor = next(
            act["payload"]["finding"]
            for act in self.acts
            if act["kind"] == "derived-publication" and act["payload"]["finding"]["id"] == self.ids["line1a_v2"]
        )
        self.assertEqual(successor["symbol"], OUTPUT_SYMBOL)
        self.assertEqual(successor["value"], "53000")
        pinned_inputs = {p["id"] for p in successor["pins"] if p["role"] == "input"}
        self.assertIn("demo-finding-w2-alpha-1-box1-corrected", pinned_inputs)

    def test_rerun_is_never_automatic_the_displaced_state_persists_until_it_runs(self) -> None:
        # No orchestration exists to trigger a rerun on correction (boundary):
        # the mid-state (correction committed, no rerun yet) has zero current
        # derived findings — an explicitly incomplete-but-true state (Article 6)
        # that only an explicit run resolves.
        mid_acts = self.acts[:8]
        _, derivation = workspace_currency(mid_acts, self.registry)
        self.assertEqual(derivation.current_derived_ids, frozenset())


class BothRunnersAgreeOnTheCorrectedRun(unittest.TestCase):
    def test_forward_and_reference_runners_agree_on_the_rederive_context(self) -> None:
        schemas = DerivationSchemas()
        ctx = _context(
            "demo-finding-w2-alpha-1-box1-corrected", "53000", "tax.us.2025.run.cascade-rederive-check"
        )
        primary = run(ctx, schemas)
        reference = run_reference(ctx, schemas)
        primary_values = {p.finding["symbol"]: p.finding["value"] for p in primary.publications}
        reference_values = {p.finding["symbol"]: p.finding["value"] for p in reference.publications}
        self.assertEqual(primary_values, {OUTPUT_SYMBOL: "53000"})
        self.assertEqual(primary_values, reference_values)


class DataSafety(unittest.TestCase):
    def test_committed_cascade_fixture_has_no_private_markers(self) -> None:
        forbidden = ("/Users/", "/private/", "local-data/", "uploads/")
        for path in WORKSPACE.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text("utf-8")
            with self.subTest(path=str(path)):
                self.assertFalse(any(marker in text for marker in forbidden))


if __name__ == "__main__":
    unittest.main()
