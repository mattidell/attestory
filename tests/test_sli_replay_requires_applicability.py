"""Marshalling a current statement link requires the applicability reading.

ADR 0077 Part 5, replay steps 2 and 3: a current statement inclusion that
``current_claim_applicability`` does not report ``current`` is not joined,
and a marker stands in its place. That omission can only happen when the
reading is supplied. Before this repair, a caller that left it out got every
inclusion joined, so an unreviewed box 1 rewrite published its new amount.

Marshalling now refuses when a current statement inclusion is present and no
reading was supplied. A state with no current inclusion marshals as before.
``live_run`` has no acts to read applicability from, so it refuses that state;
``live_coordinate_run`` supplies the reading and is the route for it.
"""
from __future__ import annotations

import json
import unittest
from typing import Any

import pytest

from packages.derivation.live import (
    LiveRunError,
    _resolve_run_authorization,
    _resolved_run_material,
    _statement_inclusion_applicability,
    live_run,
)
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.marshal import ClaimApplicabilityMissing, marshal_run_context
from packages.derivation.package_validation import validate_package
from packages.derivation.runner import run
from packages.kernel.currency import compute_currency
from packages.kernel.findings import project
import tests.test_sli_track4_support_chain as T4
import tests.test_sli_track5_worksheet_integration as t5

# Integration by construction: the recorder builds each workspace and the
# whole core calculations v40 package marshals over a fresh recovery.
pytestmark = pytest.mark.live

_UNSET = object()


def _material() -> tuple[dict[str, Any], list[dict[str, Any]], Any]:
    """Core calculations v40, its resolved members, and its runner material."""
    package = json.loads(t5.V40_PACKAGE.read_text("utf-8"))
    validation = validate_package(package, t5._corpus(), DerivationSchemas())
    if not validation.ok:
        raise AssertionError([issue.detail for issue in validation.issues])
    members = list(validation.resolved_members)
    return package, members, _resolved_run_material(t5._Graph(members, package))


def marshal(acts: tuple[dict[str, Any], ...], run_id: str, reading: Any = _UNSET) -> Any:
    """Marshal v40 as the coordinator does; ``reading`` omitted leaves the argument out."""
    schemas = DerivationSchemas()
    package, members, material = _material()
    rules, parameters, families, mappings, fact_types, bindings, collect_names = material
    state = project(acts, schemas.registry)
    currency = compute_currency(state)
    extra = {} if reading is _UNSET else {"claim_applicability": reading}
    return marshal_run_context(
        run_id=run_id, state=state, currency=currency, rules=rules, parameters=parameters,
        canon=load_canon(schemas), adoption_pin={"role": "adoption", "id": package["id"], "version": package["version"]},
        governance_pins=[], family_declarations=families, closure_mappings=mappings, fact_types=fact_types,
        input_bindings=bindings, collect_source_names=collect_names,
        emission_only_source_names=list(material.emission_only_names),
        authorization=_resolve_run_authorization(
            acts, run_scope=t5.SCOPE, scope_user=t5.USER, rules=rules,
            corpus={member["id"]: member for member in members}, package=package),
        reporting_year=2025, parameter_index=material.parameter_index, **extra)


def reading(acts: tuple[dict[str, Any], ...]) -> list[dict[str, str]]:
    """The applicability reading ``live_coordinate_run`` supplies."""
    schemas = DerivationSchemas()
    state = project(acts, schemas.registry)
    return _statement_inclusion_applicability(acts, schemas.registry, state, compute_currency(state))


def call_live_run(acts: tuple[dict[str, Any], ...], run_id: str) -> Any:
    schemas = DerivationSchemas()
    package, _members, material = _material()
    rules, parameters, families, mappings, fact_types, bindings, collect_names = material
    state = project(acts, schemas.registry)
    return live_run(
        {"schema": "run-request.v1"}, run_id=run_id, state=state, currency=compute_currency(state),
        rules=rules, parameters=parameters, canon=load_canon(schemas),
        adoption_pin={"role": "adoption", "id": package["id"], "version": package["version"]},
        governance_pins=[], schemas=schemas, family_declarations=families, closure_mappings=mappings,
        fact_types=fact_types, input_bindings=bindings, collect_source_names=collect_names,
        emission_only_source_names=list(material.emission_only_names), parameter_index=material.parameter_index)


class ReplayRequiresApplicability(unittest.TestCase):

    def rewritten(self) -> t5.Return:
        """The plain case at 1500, then an unreviewed box 1 rewrite to 1900."""
        ws = t5.Return(amounts={"cedar": 1500.0})
        self.addCleanup(ws.raw.cleanup)
        ws.plain()
        ws.unscoped_rewrite("cedar", 1900.0)
        return ws

    def test_an_unreviewed_rewrite_without_the_reading_is_refused(self) -> None:
        acts = self.rewritten().acts()
        with self.assertRaises(ClaimApplicabilityMissing) as caught:
            marshal(acts, "demo.run.replay-requires.rewrite")
        self.assertIn(T4.INCL, str(caught.exception))
        self.assertIn("claim_applicability", str(caught.exception))
        with self.assertRaises(LiveRunError):
            call_live_run(acts, "demo.run.replay-requires.rewrite-live")

    def test_with_the_reading_the_rewrite_blocks_on_the_marker(self) -> None:
        ws = self.rewritten()
        acts = ws.acts()
        self.assertEqual([row["applicability"] for row in reading(acts) if row["relationship_type"] == T4.INCL],
                         ["unresolved-applicability"])
        result = run(marshal(acts, "demo.run.replay-requires.marker", reading(acts)), DerivationSchemas())
        self.assertEqual(t5.published(result, t5.STANDING), {ws.statement["cedar"]: "applicability-unestablished"})
        self.assertNotIn("1900", json.dumps([pub.finding.get("value") for pub in result.publications
                                             if str(pub.finding["symbol"]).startswith("tax.us.2025.schedule1")]))

    def test_a_current_link_needs_the_reading_even_when_it_would_be_kept(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0})
        self.addCleanup(ws.raw.cleanup)
        ws.plain()
        acts = ws.acts()
        with self.assertRaises(ClaimApplicabilityMissing):
            marshal(acts, "demo.run.replay-requires.plain")
        with self.assertRaises(LiveRunError):
            call_live_run(acts, "demo.run.replay-requires.plain-live")
        result = run(marshal(acts, "demo.run.replay-requires.plain-read", reading(acts)), DerivationSchemas())
        self.assertEqual(t5.published(result, t5.STANDING), {ws.statement["cedar"]: "none"})

    def test_a_state_with_no_current_link_marshals_as_before(self) -> None:
        for case in ("no-claims", "link-withdrawn"):
            with self.subTest(case=case):
                ws = t5.Return(amounts={"cedar": 1500.0})
                self.addCleanup(ws.raw.cleanup)
                if case == "link-withdrawn":
                    ws.plain()
                    ws.outcome("statement-inclusion", "autumn", "cedar", "withdrawn")
                acts = ws.acts()
                self.assertEqual(reading(acts), [])
                schemas = DerivationSchemas()
                unread = run(marshal(acts, f"demo.run.replay-requires.{case}"), schemas)
                read = run(marshal(acts, f"demo.run.replay-requires.{case}", []), schemas)
                self.assertEqual(T4.surface(unread), T4.surface(read))
                live = call_live_run(acts, f"demo.run.replay-requires.{case}")
                self.assertTrue(live.publications)


if __name__ == "__main__":
    unittest.main()
