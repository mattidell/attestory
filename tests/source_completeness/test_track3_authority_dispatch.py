"""Source Completeness Track 3: adopted mapping and single dispatch.

ADR-0014 on the real two-layer ``collect`` path: the admitted family set
is resolved internally from the adopted declaration/mapping pair, the
current literal-true closure finding on the current horizon, and nothing
else. Every authority defect in the ratified negative battery blocks —
never zeroes — and the caller-supplied ``closed_sets`` input no longer
exists on any constructor.
"""

import dataclasses
import unittest
from typing import Any

from packages.derivation.evaluator import BLOCK_CLOSURE
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import RunContext, run
from packages.derivation.runners.derive import _context
from packages.derivation.source_authority import (
    ClosureFindingRecord,
    SourceAuthorityError,
)
from tests.support import demo_closure_authority

ADOPTION_PIN = {"role": "adoption", "id": "demo.package.sc.2025", "version": "v1"}
GOV_PINS = [{"role": "governance", "id": "governance.constitution", "version": "v1"}]

RULE = {
    "schema": "rule-artifact.v1",
    "id": "demo.rule.w2-subtotal",
    "version": "v1",
    "scope": {"tax_year": 2025, "jurisdiction": "us", "family": "tax"},
    "role": "computation",
    "requires": [],
    "when": True,
    "value": {
        "op": "add",
        "args": [{"op": "collect", "name": "demo.w2.box1", "source_set": "demo.w2"}],
    },
    "publishes": "demo.form1040.line1a",
    "blocked": {"code": "OPEN_DEPENDENCY", "missing": []},
}


class DispatchFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.canon = load_canon(self.schemas)

    def context(self, **overrides: Any) -> RunContext:
        base: dict[str, Any] = dict(
            run_id="run.sc",
            rules=[RULE],
            parameters={},
            canon=self.canon,
            inputs=[],
            sources=[],
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOV_PINS,
        )
        base.update(demo_closure_authority())
        base.update(overrides)
        return RunContext(**base)

    def assert_blocked_closure(self, ctx: RunContext) -> None:
        result = run(ctx, self.schemas)
        self.assertEqual(result.publications, [])
        blocked = {b["artifact_id"]: b for b in result.blocked}
        self.assertEqual(blocked[RULE["id"]]["code"], BLOCK_CLOSURE)

    def closure_finding(self, **overrides: Any) -> ClosureFindingRecord:
        base: dict[str, Any] = dict(
            finding_id="f.closure.demo",
            fact_type="demo.w2.closure",
            horizon_id="demo.h0",
            value=True,
        )
        base.update(overrides)
        return ClosureFindingRecord(**base)


class ClosureBackedZero(DispatchFixture):
    def test_admitted_empty_family_publishes_zero_with_authority_pins(self) -> None:
        result = run(self.context(), self.schemas)
        finding = result.publications[0].finding
        self.assertEqual(finding["symbol"], "demo.form1040.line1a")
        self.assertEqual(finding["value"], "0")
        pins = {(p["role"], p["id"]) for p in finding["pins"]}
        # ADR-0014 decision 5: exact mapping version, exact declaration,
        # exact current closure finding. Horizon identity travels in the
        # closure finding's fact key.
        self.assertIn(("package", "demo.mapping.w2"), pins)
        self.assertIn(("package", "demo.w2"), pins)
        self.assertIn(("input", "f.closure.demo"), pins)

    def test_present_source_aggregation_never_pins_closure(self) -> None:
        from packages.derivation.runner import SourceFact

        result = run(
            self.context(sources=[SourceFact("demo.w2.box1", "42000", "f.w2a")]),
            self.schemas,
        )
        finding = result.publications[0].finding
        self.assertEqual(finding["value"], "42000")
        pinned = {p["id"] for p in finding["pins"]}
        self.assertNotIn("demo.mapping.w2", pinned)
        self.assertNotIn("f.closure.demo", pinned)

    def test_both_runners_agree_on_the_closure_zero(self) -> None:
        ctx = self.context()
        primary = run(ctx, self.schemas).publications[0].finding
        reference = run_reference(ctx, self.schemas).publications[0].finding
        self.assertEqual(primary, reference)


class AuthorityNegatives(DispatchFixture):
    """False, absent, displaced, truthy, ambiguous: blocked, never zero."""

    def test_false_closure_finding_blocks(self) -> None:
        self.assert_blocked_closure(
            self.context(closure_findings=[self.closure_finding(value=False)])
        )

    def test_absent_closure_finding_blocks(self) -> None:
        self.assert_blocked_closure(self.context(closure_findings=[]))

    def test_displaced_closure_finding_blocks(self) -> None:
        # The finding is keyed on a superseded horizon: on the dispatch
        # path that is indistinguishable from absence (ADR-0017).
        self.assert_blocked_closure(
            self.context(
                closure_findings=[self.closure_finding(horizon_id="demo.h0")],
                current_horizons={"demo.w2": "demo.h1"},
            )
        )

    def test_truthy_non_boolean_closure_blocks(self) -> None:
        for truthy in ("true", 1, "yes"):
            with self.subTest(value=truthy):
                self.assert_blocked_closure(
                    self.context(closure_findings=[self.closure_finding(value=truthy)])
                )

    def test_duplicate_closure_findings_block(self) -> None:
        self.assert_blocked_closure(
            self.context(
                closure_findings=[
                    self.closure_finding(),
                    self.closure_finding(finding_id="f.closure.demo-2"),
                ]
            )
        )

    def test_missing_horizon_chain_blocks(self) -> None:
        self.assert_blocked_closure(self.context(current_horizons={}))


class AdoptedContentDefects(DispatchFixture):
    """Fabricated, duplicate, or mismatched mappings are loud errors."""

    def fabricate(self, **mapping_overrides: Any) -> dict[str, Any]:
        mapping = dict(demo_closure_authority()["closure_mappings"][0])
        mapping.update(mapping_overrides)
        return mapping

    def test_fabricated_mapping_for_undeclared_family_raises(self) -> None:
        mapping = self.fabricate(family={"id": "demo.fabricated", "version": "v1"})
        with self.assertRaisesRegex(SourceAuthorityError, "fabricated mapping"):
            run(self.context(closure_mappings=[mapping]), self.schemas)

    def test_duplicate_mapping_authority_raises(self) -> None:
        authority = demo_closure_authority()
        double = [
            authority["closure_mappings"][0],
            self.fabricate(id="demo.mapping.w2-second"),
        ]
        with self.assertRaisesRegex(SourceAuthorityError, "duplicate mapping"):
            run(self.context(closure_mappings=double), self.schemas)

    def test_mapping_predicate_mismatch_raises(self) -> None:
        mapping = self.fabricate(member_fact_type="demo.w2.box2")
        with self.assertRaisesRegex(SourceAuthorityError, "claim/predicate"):
            run(self.context(closure_mappings=[mapping]), self.schemas)

    def test_label_cannot_broaden_authority(self) -> None:
        # A rule collecting over the mapped family but publishing a
        # broader symbol is rejected before any evaluation (ADR-0016).
        broad = dict(RULE)
        broad["id"] = "demo.rule.grand-total"
        broad["publishes"] = "demo.income.grand-total"
        with self.assertRaisesRegex(SourceAuthorityError, "authorizes only"):
            run(self.context(rules=[broad]), self.schemas)


class CallerInjection(unittest.TestCase):
    """ADR-0014 consequence 1: closed_sets is removed, not renamed."""

    def test_run_context_has_no_closed_sets_field(self) -> None:
        fields = {f.name for f in dataclasses.fields(RunContext)}
        self.assertNotIn("closed_sets", fields)

    def test_constructing_with_closed_sets_is_a_type_error(self) -> None:
        with self.assertRaises(TypeError):
            RunContext(  # type: ignore[call-arg]
                run_id="run.injection",
                rules=[],
                parameters={},
                canon={},
                inputs=[],
                sources=[],
                adoption_pin=ADOPTION_PIN,
                governance_pins=GOV_PINS,
                closed_sets=frozenset({"demo.w2"}),
            )

    def test_scenario_files_with_closed_sets_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "ADR-0014"):
            _context({"closed_sets": ["demo.w2"], "run_id": "run.legacy"})

    def test_no_module_reintroduces_a_closed_sets_carrier(self) -> None:
        # The audit the milestone requires: no production module accepts
        # or forwards a caller-named closed set. The evaluator's internal
        # Environment field is the two-layer check itself and is built
        # only from resolved admissions inside the runner.
        from pathlib import Path

        allowed = {
            Path("packages/derivation/evaluator.py"),  # the two-layer check itself
            Path("packages/derivation/runner.py"),  # builds the set from admissions
            Path("packages/derivation/runners/derive.py"),  # rejects the legacy key
        }
        offenders = []
        for path in Path("packages").rglob("*.py"):
            if "closed_sets" in path.read_text("utf-8") and path not in allowed:
                offenders.append(str(path))
        self.assertEqual(offenders, [])
        runner_text = Path("packages/derivation/runner.py").read_text("utf-8")
        self.assertIn("closed_sets=frozenset(self.admissions)", runner_text)


if __name__ == "__main__":
    unittest.main()
