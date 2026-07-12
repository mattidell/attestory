"""Track 4 verification: the saturation runner end to end.

Covers derivation-becomes-executable as tested contracts:
- E3.1 eligibility & saturation: a dependency chain computes to a fixpoint.
- E12.1 blocking vocabulary: absent / invalid / closure are distinct codes.
- E13.1 pins carry roles; E13.2 pin values come from versioned inputs, never
  runner constants (source audit + value check).
- demo_source_closure (parity 2): an empty unclosed source blocks; the same
  source declared complete publishes zero, pinned to the closure.
- demo_invalid_elective (attack 8): an out-of-domain elective blocks with an
  invalid code and leaks no exception text.
- Determinism seed for Track 5: content-addressed ids are re-run and
  shuffle-order invariant.
"""

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.evaluator import BLOCK_ABSENT, BLOCK_CLOSURE, BLOCK_LOOKUP_MISS
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.records import RecordStream
from tests.support import demo_closure_authority
from packages.derivation.runner import (
    InputFinding,
    RunContext,
    SourceFact,
    run,
    run_and_record,
)

EXAMPLES = Path(__file__).resolve().parent.parent.parent / "packages" / "sample_data" / "derivation" / "examples"

ADOPTION_PIN = {"role": "adoption", "id": "demo.package.first-slice.2025", "version": "v1"}
GOV_PINS = [{"role": "governance", "id": "governance.constitution", "version": "v1"}]


def _load(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((EXAMPLES / name).read_text("utf-8"))
    return loaded


class RunnerFixture(unittest.TestCase):
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

    def published(self, result: Any) -> dict[str, str]:
        return {pub.finding["symbol"]: pub.finding["value"] for pub in result.publications}


class EligibilityAndSaturation(RunnerFixture):
    def test_chain_computes_to_fixpoint(self) -> None:
        # line15 present and below the split: tax-table fires; wages collects
        # and rounds. Both publish in one saturation.
        ctx = self.context(inputs=[
            InputFinding("rounding.convention", "half_up", "f.rounding", "input"),
            InputFinding("filing_status", "single", "f.filing", "choice"),
            InputFinding("demo.form1040.line15", "14950", "f.line15", "input"),
        ])
        result = run(ctx, self.schemas)
        published = self.published(result)
        self.assertEqual(published["demo.form1040.line1a"], "42000")
        self.assertEqual(published["demo.form1040.line16"], "1559")

    def test_ineligible_rule_finalizes_blocked_on_missing_dependency(self) -> None:
        # No line15: tax-table never becomes eligible, so it saturates blocked
        # with the absent dependency named.
        result = run(self.context(), self.schemas)
        blocked = {b["artifact_id"]: b for b in result.blocked}
        self.assertIn(self.tax["id"], blocked)
        self.assertEqual(blocked[self.tax["id"]]["code"], BLOCK_ABSENT)
        self.assertIn("demo.form1040.line15", blocked[self.tax["id"]]["missing"])

    def test_false_guard_is_inapplicable_not_blocked(self) -> None:
        ctx = self.context(inputs=[
            InputFinding("rounding.convention", "half_up", "f.rounding", "input"),
            InputFinding("filing_status", "single", "f.filing", "choice"),
            InputFinding("demo.form1040.line15", "200000", "f.line15", "input"),  # >= split
        ])
        result = run(ctx, self.schemas)
        dispositions = {d["artifact_id"]: d for d in result.dispositions}
        self.assertEqual(dispositions[self.tax["id"]]["disposition"], "inapplicable")
        self.assertFalse(dispositions[self.tax["id"]]["guard_result"])


class BlockingVocabulary(RunnerFixture):
    def test_unclosed_empty_source_blocks_with_closure_code(self) -> None:
        result = run(self.context(sources=[]), self.schemas)
        blocked = {b["artifact_id"]: b for b in result.blocked}
        self.assertEqual(blocked[self.wages["id"]]["code"], BLOCK_CLOSURE)

    def test_closure_authority_empty_source_publishes_zero(self) -> None:
        # ADR-0014: the zero requires the full recorded authority chain —
        # adopted declaration and mapping plus a current literal-true
        # closure finding on the current horizon. No closed-set input exists.
        result = run(
            self.context(sources=[], **demo_closure_authority()), self.schemas
        )
        self.assertEqual(self.published(result)["demo.form1040.line1a"], "0")

    def test_out_of_domain_elective_blocks_invalid_without_leaking_exceptions(self) -> None:
        ctx = self.context(inputs=[
            InputFinding("rounding.convention", "half_up", "f.rounding", "input"),
            InputFinding("filing_status", "martian", "f.filing", "choice"),  # well-typed, out of domain
            InputFinding("demo.form1040.line15", "14950", "f.line15", "input"),
        ])
        result = run(ctx, self.schemas)
        blocked = {b["artifact_id"]: b for b in result.blocked}
        entry = blocked[self.tax["id"]]
        self.assertEqual(entry["code"], BLOCK_LOOKUP_MISS)
        joined = " ".join(entry["missing"])
        self.assertNotIn("Traceback", joined)
        self.assertNotIn("Error", joined)


class PinsProvenance(RunnerFixture):
    def test_published_finding_pins_carry_roles(self) -> None:
        result = run(self.context(), self.schemas)
        wages_pub = next(p for p in result.publications if p.finding["symbol"] == "demo.form1040.line1a")
        roles = {p["role"] for p in wages_pub.finding["pins"]}
        self.assertIn("field-mapping", roles)   # the firing rule
        self.assertIn("input", roles)           # collected W-2 findings
        self.assertIn("operation-semantics", roles)  # round canon
        self.assertIn("adoption", roles)
        self.assertIn("governance", roles)
        # Every pin is role-bearing (no bare id bags).
        for pin in wages_pub.finding["pins"]:
            self.assertEqual(set(pin), {"role", "id", "version"})

    def test_collected_source_findings_are_pinned(self) -> None:
        result = run(self.context(), self.schemas)
        wages_pub = next(p for p in result.publications if p.finding["symbol"] == "demo.form1040.line1a")
        pinned_ids = {p["id"] for p in wages_pub.finding["pins"]}
        self.assertIn("f.w2a", pinned_ids)
        self.assertIn("f.w2b", pinned_ids)

    def test_governance_pin_value_comes_from_context_not_a_constant(self) -> None:
        # E13.2: the pinned governance identity is exactly the versioned input
        # passed in — swap it and the pin follows.
        other_gov = [{"role": "governance", "id": "governance.constitution", "version": "v9"}]
        result = run(self.context(governance_pins=other_gov), self.schemas)
        pub = result.publications[0]
        gov = [p for p in pub.finding["pins"] if p["role"] == "governance"]
        self.assertEqual(gov, other_gov)

    def test_runner_source_hardcodes_no_governance_identity(self) -> None:
        # E13.2 audit: no pinned value may originate in runner code.
        source = (Path(__file__).resolve().parent.parent.parent / "packages" / "derivation" / "runner.py").read_text()
        self.assertNotIn("governance.", source)
        self.assertNotIn("constitution", source)


class Determinism(RunnerFixture):
    def test_rerun_and_shuffled_order_yield_identical_finding_ids(self) -> None:
        ctx = self.context(inputs=[
            InputFinding("rounding.convention", "half_up", "f.rounding", "input"),
            InputFinding("filing_status", "single", "f.filing", "choice"),
            InputFinding("demo.form1040.line15", "14950", "f.line15", "input"),
        ])
        first = {p.finding["symbol"]: p.finding["id"] for p in run(ctx, self.schemas).publications}
        shuffled = self.context(rules=[self.tax, self.wages], inputs=ctx.inputs)
        second = {p.finding["symbol"]: p.finding["id"] for p in run(shuffled, self.schemas).publications}
        self.assertEqual(first, second)


class RecordIntegration(RunnerFixture):
    def test_run_and_record_gates_and_closes_the_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            stream = RecordStream(Path(tmp) / "ws", self.schemas)
            ctx = self.context(inputs=[
                InputFinding("rounding.convention", "half_up", "f.rounding", "input"),
                InputFinding("filing_status", "single", "f.filing", "choice"),
                InputFinding("demo.form1040.line15", "14950", "f.line15", "input"),
            ])
            result = run_and_record(
                ctx, self.schemas, stream,
                workspace_revision=7,
                adopted_packages={"demo.package.first-slice.2025"},
                start_record_id="rec.start",
                completion_record_id="rec.done",
            )
            self.assertEqual(stream.open_runs(), {})  # started + completed pair
            standing = stream.standings()["run.1"]
            assert standing.closing is not None
            symbols = {p["symbol"] for p in standing.closing["published"]}
            self.assertEqual(symbols, {"demo.form1040.line1a", "demo.form1040.line16"})
            self.assertEqual(len(result.publications), 2)


if __name__ == "__main__":
    unittest.main()
