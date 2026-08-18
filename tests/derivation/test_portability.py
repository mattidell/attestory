"""Track 5 verification: purity and second-runner portability.

- E11.2 portability: the primary (forward saturation) and reference
  (demand-driven) runners produce byte-identical published findings and
  blocked surfaces across scenarios. Content-addressed ids make this a strict
  byte comparison, not a structural one.
- E11.1 sealed execution: the evaluator and both runners read no ambient state
  (clock, randomness, environment, filesystem) — a static import scan plus a
  double-run determinism check.
- E11.3 no orchestrated traversal / deletion attribution: order independence is
  proven by the two strategies agreeing; deleting an input makes the dependent
  value's absence attributable to the named missing input in the record.
"""

import json
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.loader import DerivationSchemas, load_canon
from tests.support import demo_closure_authority
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import (
    InputFinding,
    RunContext,
    RunResult,
    SourceFact,
    run,
)

EXAMPLES = Path(__file__).resolve().parent.parent.parent / "packages" / "sample_data" / "derivation" / "examples"
SRC = Path(__file__).resolve().parent.parent.parent / "packages" / "derivation"

ADOPTION_PIN = {"role": "adoption", "id": "demo.package.first-slice.2025", "version": "v1"}
GOV_PINS = [{"role": "governance", "id": "governance.constitution", "version": "v1"}]


def _load(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((EXAMPLES / name).read_text("utf-8"))
    return loaded


def _findings_blob(result: RunResult) -> str:
    findings = sorted((p.finding for p in result.publications), key=lambda f: f["symbol"])
    return json.dumps(findings, sort_keys=True, separators=(",", ":"))


def _blocked_blob(result: RunResult) -> str:
    return json.dumps(sorted(result.blocked, key=lambda b: b["artifact_id"]),
                      sort_keys=True, separators=(",", ":"))


class PortabilityFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.canon = load_canon(self.schemas)
        self.wages = _load("rule-artifact.wages-line1a.json")
        self.tax = _load("rule-artifact.tax-table-line16.json")
        self.parameters = {
            p["id"]: p
            for p in [
                _load("parameter.regular-tax-split.json"),
                _load("parameter.tax-table-sample.json"),
            ]
        }

    def context(self, **overrides: Any) -> RunContext:
        base: dict[str, Any] = dict(
            run_id="run.1",
            rules=[self.wages, self.tax],
            parameters=self.parameters,
            canon=self.canon,
            inputs=[
                InputFinding("rounding.convention", "half_up", "f.rounding", "input"),
                InputFinding("filing_status", "single", "f.filing", "choice"),
                InputFinding("demo.form1040.line15", "14950", "f.line15", "input"),
            ],
            sources=[
                SourceFact("demo.w2.box1", "40000", "f.w2a"),
                SourceFact("demo.w2.box1", "2000", "f.w2b"),
            ],
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOV_PINS,
        )
        base.update(overrides)
        return RunContext(**base)


class ByteEqualityAcrossRunners(PortabilityFixture):
    def _assert_portable(self, ctx: RunContext) -> None:
        primary = run(ctx, self.schemas)
        reference = run_reference(ctx, self.schemas)
        self.assertEqual(_findings_blob(primary), _findings_blob(reference))
        self.assertEqual(_blocked_blob(primary), _blocked_blob(reference))

    def test_full_chain_is_byte_identical(self) -> None:
        self._assert_portable(self.context())

    def test_blocked_scenario_is_byte_identical(self) -> None:
        # No line15: tax-table never fires; line1a still publishes.
        self._assert_portable(self.context(inputs=[
            InputFinding("rounding.convention", "half_up", "f.rounding", "input"),
            InputFinding("filing_status", "single", "f.filing", "choice"),
        ]))

    def test_closure_zero_scenario_is_byte_identical(self) -> None:
        self._assert_portable(self.context(sources=[], **demo_closure_authority()))

    def test_both_runners_agree_on_computed_values(self) -> None:
        primary = {p.finding["symbol"]: p.finding["value"] for p in run(self.context(), self.schemas).publications}
        reference = {p.finding["symbol"]: p.finding["value"]
                     for p in run_reference(self.context(), self.schemas).publications}
        self.assertEqual(primary, {"demo.form1040.line1a": "42000", "demo.form1040.line16": "1559"})
        self.assertEqual(primary, reference)


class SealedExecution(PortabilityFixture):
    def test_no_ambient_state_imports(self) -> None:
        forbidden = ["import random", "import time", "from datetime", "os.environ", "os.urandom", "time.time"]
        for module in ["evaluator.py", "runner.py", "reference_runner.py"]:
            source = (SRC / module).read_text("utf-8")
            for needle in forbidden:
                with self.subTest(module=module, needle=needle):
                    self.assertNotIn(needle, source)

    def test_double_run_is_deterministic(self) -> None:
        ctx = self.context()
        self.assertEqual(_findings_blob(run(ctx, self.schemas)), _findings_blob(run(ctx, self.schemas)))
        self.assertEqual(_findings_blob(run_reference(ctx, self.schemas)),
                         _findings_blob(run_reference(ctx, self.schemas)))


class AttachmentSchedulingPortability(unittest.TestCase):
    """Track 4 Repair 1: the reference runner must dispatch attachment-rule
    citizens (ADR-0036) the same way the primary runner's `_execute` does —
    `_requires` for eligibility, `attempt_attachment` for the step — instead
    of raising `KeyError: 'when'` on `rule["requires"]` and `state.attempt`.
    """

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.canon = load_canon(self.schemas)
        self.attachment = _load("attachment-rule.v1.demo-attachment.json")
        self.threshold = _load("parameter.attach-threshold.json")

    def context(self, *, subtotal: str | None, sources: list[SourceFact],
                answer: str | None = "yes") -> RunContext:
        inputs = [InputFinding("demo.answer.attach-first", answer, "f.answer", "input")] \
            if answer is not None else []
        if subtotal is not None:
            inputs.append(InputFinding("demo.attach.alpha.subtotal", subtotal, "f.subtotal", "input"))
        return RunContext(
            run_id="run.attach.1",
            rules=[self.attachment],
            parameters={self.threshold["id"]: self.threshold},
            canon=self.canon,
            inputs=inputs,
            sources=sources,
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOV_PINS,
        )

    def _assert_portable(self, ctx: RunContext) -> tuple[RunResult, RunResult]:
        primary = run(ctx, self.schemas)
        reference = run_reference(ctx, self.schemas)
        self.assertEqual(_findings_blob(primary), _findings_blob(reference))
        self.assertEqual(_blocked_blob(primary), _blocked_blob(reference))
        return primary, reference

    def test_synthetic_attachment_required_and_complete_is_byte_identical(self) -> None:
        ctx = self.context(
            subtotal="900",
            sources=[
                SourceFact("demo.fact.attach-item", "600", "f.item-a"),
                SourceFact("demo.fact.attach-item", "300", "f.item-b"),
            ],
        )
        primary, _reference = self._assert_portable(ctx)
        dispositions = {d["artifact_id"]: d for d in primary.dispositions}
        self.assertEqual(dispositions[self.attachment["id"]]["disposition"], "published")

    def test_synthetic_attachment_blocked_itemization_tie_out_is_byte_identical(self) -> None:
        # Subtotal (900) does not match the itemized row sum (600) — a
        # tie-out violation, blocked with the same code and pins in both
        # schedulers.
        ctx = self.context(
            subtotal="900",
            sources=[SourceFact("demo.fact.attach-item", "600", "f.item-a")],
        )
        primary, _reference = self._assert_portable(ctx)
        blocked = {b["artifact_id"]: b for b in primary.blocked}
        self.assertEqual(blocked[self.attachment["id"]]["code"], "ITEMIZATION_TIE_OUT_VIOLATION")

    def test_synthetic_attachment_missing_threshold_subtotal_is_byte_identical(self) -> None:
        # No subtotal input at all: the requirement's own dependency is
        # absent (DEPENDENCY_ABSENT-class), before any itemization or
        # completeness check runs.
        ctx = self.context(subtotal=None, sources=[])
        primary, _reference = self._assert_portable(ctx)
        blocked = {b["artifact_id"]: b for b in primary.blocked}
        self.assertEqual(blocked[self.attachment["id"]]["code"], "DEPENDENCY_ABSENT")
        self.assertIn("demo.attach.alpha.subtotal", blocked[self.attachment["id"]]["missing"])


class DeletionAttribution(PortabilityFixture):
    def test_deleting_an_input_makes_the_dependent_absence_attributable(self) -> None:
        # Delete line15: line16's absence is attributable to the missing input,
        # named in the record's blocked entry — in both runners.
        ctx = self.context(inputs=[
            InputFinding("rounding.convention", "half_up", "f.rounding", "input"),
            InputFinding("filing_status", "single", "f.filing", "choice"),
        ])
        for result in (run(ctx, self.schemas), run_reference(ctx, self.schemas)):
            blocked = {b["artifact_id"]: b for b in result.blocked}
            self.assertIn(self.tax["id"], blocked)
            self.assertIn("demo.form1040.line15", blocked[self.tax["id"]]["missing"])
            published = {p.finding["symbol"] for p in result.publications}
            self.assertNotIn("demo.form1040.line16", published)


if __name__ == "__main__":
    unittest.main()
