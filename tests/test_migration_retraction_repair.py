"""Repair regressions: migration adoption must read *then-current*
predecessor findings through the authoritative projection, and
ADR-0072's nonzero-blocks-migration rule must cover a retracted
predecessor exactly as it already covers a withdrawn one.

This file covers two defects in migration adoption's handling of a
predecessor whose answer has stopped being current, plus a boundary
regression proving where that handling does and does not apply:

1. ``_present_successor_claims`` used to select "the last recorded
   finding per fact, minus withdrawn fact ids" -- invisible to
   retraction, so a retracted answer was still presented as a
   then-current claim to carry forward.
2. Fixing (1) alone removes the accident that today blocks a retracted
   *nonzero* predecessor from migrating (it was blocked only because it
   was still presented, and the live-claim guard caught it) -- so the
   nonzero-blocks-migration guard must be extended to retraction too, or
   a historical nonzero claim would migrate silently once (1) is fixed.

The governing rule (ADR-0072 Decision 4) is stated in value, not
mechanism: a live or withdrawn predecessor whose true last value is
nonzero always blocks a ``resolved-required`` migration; a genuinely
zero predecessor migrates freely; the only accepted resolution is a
same-identity correction to a genuinely zero value. Retraction is a
third way a predecessor's answer stops being live, and joins withdrawal
under that same rule, changing no product meaning.

Regression 6 (below) proves the boundary of both fixes: entity
succession removes the keyed proposition from the current lattice
entirely, so it is not withdrawal or retraction and neither function
above ever examines a fact on a superseded entity -- superseding the
entity behind a nonzero predecessor adopts with no claim and no
refusal, while retracting the same finding still refuses.

Vocabulary is synthetic (``demo.*``), numeric-valued so zero/nonzero
means what it says (unlike ``tests.test_assertion_standing_track0``'s
own ``PRED``/``SUCC`` migration control, which is enum-valued and so
cannot exercise the zero-value resolution path at all). Built through
``findings.project`` -- the same admission path every other kernel-only
migration test in this milestone uses.
"""

from __future__ import annotations

import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from typing import Any

from packages.kernel import facts
from packages.kernel.findings import (
    MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM,
    FindingModelError,
    project,
)
from tests.support import act, demo_entity, demo_finding, registry_with_demo_kinds

RETRACTION_KIND = "finding-retracted"

PRED_TYPE = "demo.migration-retraction.legacy-amount"
SUCC_TYPE = "demo.migration-retraction.migrated-claim"
MIGRATION_ID = "demo.migration-retraction.succession"
FAMILY = {"id": "demo.migration-retraction.family", "version": "v1"}
SCOPE = {"tax-year": "2025"}

PRED_FACT_ID = f"{PRED_TYPE}|instance=only"


def _fact_type(type_id: str) -> dict[str, Any]:
    return {
        "schema": "fact-type.v1",
        "id": type_id,
        "title": type_id,
        "nature": "determinable",
        "identity_keys": [{"name": "instance", "kind": "literal", "values": ["only"]}],
        "value_schema": {"type": "number"},
        "supersession": {"policy": "free"},
    }


BUNDLE = {
    "schema": "bundle.v1",
    "id": "demo.migration-retraction.bundle",
    "label": "Migration/retraction repair vocabulary",
    "fact_types": [_fact_type(PRED_TYPE), _fact_type(SUCC_TYPE)],
}

MIGRATION = {
    "schema": "migration-artifact.v1",
    "id": MIGRATION_ID,
    "version": "v1",
    "title": "Migration/retraction repair succession",
    "finding_mapping": {"policy": "presented-claim"},
    "pairs": [{"predecessor": PRED_TYPE, "successor": SUCC_TYPE}],
}

# ---------------------------------------------------------------------------
# Entity-keyed fixtures for the entity-succession boundary (regression 6):
# a fact type keyed on an entity, so superseding that entity removes the
# fact from the current lattice entirely -- unlike retraction, which only
# ends an answer, leaving the fact itself in place.

ENTITY_KIND = "demo.migration-retraction.counterparty"
ENTITY_ID = "demo.mrt.entity-1"
PRED_ENTITY_TYPE = "demo.migration-retraction.legacy-entity-amount"
SUCC_ENTITY_TYPE = "demo.migration-retraction.migrated-entity-claim"
ENTITY_MIGRATION_ID = "demo.migration-retraction.entity-succession"
PRED_ENTITY_FACT_ID = f"{PRED_ENTITY_TYPE}|counterparty={ENTITY_ID}"


def _entity_fact_type(type_id: str) -> dict[str, Any]:
    return {
        "schema": "fact-type.v1",
        "id": type_id,
        "title": type_id,
        "nature": "determinable",
        "identity_keys": [
            {"name": "counterparty", "kind": "entity", "entity_kind": ENTITY_KIND}
        ],
        "value_schema": {"type": "number"},
        "supersession": {"policy": "free"},
    }


ENTITY_BUNDLE = {
    "schema": "bundle.v1",
    "id": "demo.migration-retraction.entity-bundle",
    "label": "Migration/retraction repair entity vocabulary",
    "fact_types": [_entity_fact_type(PRED_ENTITY_TYPE), _entity_fact_type(SUCC_ENTITY_TYPE)],
}

ENTITY_MIGRATION = {
    "schema": "migration-artifact.v1",
    "id": ENTITY_MIGRATION_ID,
    "version": "v1",
    "title": "Migration/retraction repair entity succession",
    "finding_mapping": {"policy": "presented-claim"},
    "pairs": [{"predecessor": PRED_ENTITY_TYPE, "successor": SUCC_ENTITY_TYPE}],
}


def _finding(finding_id: str, value: Any, fact_id: str = PRED_FACT_ID) -> dict[str, Any]:
    return demo_finding(
        finding_id=finding_id, fact_id=fact_id, value=value, basis="attested", evidence_ids=[]
    )


def _retraction(index: int, finding_id: str) -> dict[str, Any]:
    return act(index, RETRACTION_KIND, {"finding_id": finding_id})


def _migration_act(index: int) -> dict[str, Any]:
    return act(index, "migration-adoption", {"migration": MIGRATION})


def _bundle_act(index: int) -> dict[str, Any]:
    return act(index, "bundle-adoption", {"bundle": BUNDLE})


def _claims_for_predecessor(state: Any) -> tuple[dict[str, Any], ...]:
    return tuple(
        claim
        for claim in state.presented_successor_claims
        if claim["migration_id"] == MIGRATION_ID and claim["predecessor_fact_id"] == PRED_FACT_ID
    )


class RepairRegressions(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.registry = registry_with_demo_kinds(Path(self._tmp.name))

    def _resolved_required(self) -> None:
        self.registry.migration_resolution_policies[MIGRATION_ID] = "resolved-required"

    # ---------------------------------------------------------- regression 1
    def test_retracted_finding_is_not_presented_as_a_successor_claim(self) -> None:
        """A retracted predecessor answer is not a then-current claim: no
        ``resolved-required`` policy in effect, so this documents defect 1
        in isolation -- adoption succeeds (nothing here is nonzero-blocked)
        and produces no claim for the retracted predecessor fact."""
        acts = [
            _bundle_act(0),
            act(1, "assertion", {"finding": _finding("f1", 100)}),
            _retraction(2, "f1"),
            _migration_act(3),
        ]
        state = project(tuple(acts), self.registry)
        self.assertEqual(_claims_for_predecessor(state), ())

    # ---------------------------------------------------------- regression 2
    def test_retracted_nonzero_predecessor_blocks_resolved_required_migration(self) -> None:
        """Defect 2: fixing defect 1 alone would let this migrate silently
        (the retracted 100 is no longer presented, so the old
        withdrawal-only guard would never see it). The merged guard
        extends ADR-0072's nonzero block to a retracted predecessor, so
        adoption still refuses -- and the refusal still names the
        unresolved claim's fact_id."""
        acts = [
            _bundle_act(0),
            act(1, "assertion", {"finding": _finding("f1", 100)}),
            _retraction(2, "f1"),
            _migration_act(3),
        ]
        self._resolved_required()
        with self.assertRaises(FindingModelError) as ctx:
            project(tuple(acts), self.registry)
        self.assertIn(MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM, str(ctx.exception))
        self.assertIn(PRED_FACT_ID, str(ctx.exception))

    # ---------------------------------------------------------- regression 3
    def test_retracted_genuinely_zero_predecessor_migrates_freely(self) -> None:
        """A retracted predecessor whose true last value is genuinely zero
        migrates freely under ``resolved-required``, exactly as a
        withdrawn zero predecessor already does: retraction is a way an
        answer stops being live, never itself a resolution mechanism, but
        it also never blocks a claim that was already zero."""
        acts = [
            _bundle_act(0),
            act(1, "assertion", {"finding": _finding("f1", 0)}),
            _retraction(2, "f1"),
            _migration_act(3),
        ]
        self._resolved_required()
        state = project(tuple(acts), self.registry)
        self.assertEqual(_claims_for_predecessor(state), ())
        self.assertIn(PRED_TYPE, state.fact_state.retired_fact_type_ids)

    # ---------------------------------------------------------- regression 4
    def test_withdrawn_predecessor_behaviour_unchanged_nonzero_and_zero(self) -> None:
        """The existing withdrawn-predecessor behaviour (ADR-0072 Decision
        4, proven end to end in
        ``tests.test_legacy_pairing_coexistence_migration``) is unchanged
        by folding retraction into the same guard: a nonzero withdrawn
        predecessor still blocks, a genuinely zero withdrawn predecessor
        still migrates freely, and neither presents a claim (a withdrawn
        finding's own value is preserved but no longer live)."""
        genesis = act(
            0, "horizon-genesis", {"family": FAMILY, "scope": SCOPE, "horizon_id": "demo.mrt.h0"}
        )
        base = [
            _bundle_act(1),
            act(2, "assertion", {"finding": _finding("f-nonzero", 100)}),
        ]
        withdraw_nonzero = act(
            3,
            "member-transition",
            {
                "family": FAMILY,
                "scope": SCOPE,
                "member": {"action": "remove", "fact_id": PRED_FACT_ID},
                "successor": {"id": "demo.mrt.h1", "predecessor": "demo.mrt.h0"},
            },
        )
        acts_nonzero = [genesis, *base, withdraw_nonzero, _migration_act(4)]
        self._resolved_required()
        with self.assertRaises(FindingModelError) as ctx:
            project(tuple(acts_nonzero), self.registry)
        self.assertIn(MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM, str(ctx.exception))
        self.assertIn(PRED_FACT_ID, str(ctx.exception))

        acts_zero = [
            genesis,
            _bundle_act(1),
            act(2, "assertion", {"finding": _finding("f-zero", 0)}),
            act(
                3,
                "member-transition",
                {
                    "family": FAMILY,
                    "scope": SCOPE,
                    "member": {"action": "remove", "fact_id": PRED_FACT_ID},
                    "successor": {"id": "demo.mrt.h1", "predecessor": "demo.mrt.h0"},
                },
            ),
            _migration_act(4),
        ]
        state = project(tuple(acts_zero), self.registry)
        self.assertEqual(_claims_for_predecessor(state), ())
        self.assertIn(PRED_FACT_ID, state.withdrawn_fact_ids)
        self.assertIn(PRED_TYPE, state.fact_state.retired_fact_type_ids)

    # ---------------------------------------------------------- regression 5
    def test_ordinary_correction_still_presents_the_corrected_value(self) -> None:
        """A corrected fact's last finding is the correction itself, which
        is current under the projection -- the merged predicate must not
        disturb ordinary correction. This proves the correction (not the
        superseded original) is what migration presents as the claim."""
        acts = [
            _bundle_act(0),
            act(1, "assertion", {"finding": _finding("f-original", 100)}),
            act(2, "assertion", {"finding": _finding("f-corrected", 55)}),
            _migration_act(3),
        ]
        state = project(tuple(acts), self.registry)
        claims = _claims_for_predecessor(state)
        self.assertEqual(len(claims), 1, claims)
        self.assertEqual(claims[0]["predecessor_finding_id"], "f-corrected")
        self.assertEqual(Decimal(str(claims[0]["proposed_value"])), Decimal("55"))

    # ---------------------------------------------------------- regression 6
    def test_entity_supersession_is_not_withdrawal_or_retraction(self) -> None:
        """Entity succession is different in kind from withdrawal and
        retraction: it removes the keyed proposition itself from the
        current lattice, rather than ending an answer to a proposition
        that remains. Superseding the entity behind a nonzero predecessor
        finding adopts the ``resolved-required`` migration with no claim
        presented and no refusal -- the fact is simply absent from
        ``facts.facts_of``, never reaching either
        ``_present_successor_claims`` or
        ``_refuse_unresolved_nonzero_noncurrent_predecessors``. Retracting
        the same finding instead of superseding the entity refuses, because
        the fact remains in the lattice with a nonzero last-recorded value
        that is no longer current. Asserting the lattice absence directly
        (not just the successful/refused outcome) makes the reason for the
        difference visible."""
        self.registry.migration_resolution_policies[ENTITY_MIGRATION_ID] = "resolved-required"
        entity_acts = [
            act(0, "entity-introduced", {"entity": demo_entity(ENTITY_ID, "Entity 1", ENTITY_KIND)}),
            act(1, "bundle-adoption", {"bundle": ENTITY_BUNDLE}),
            act(2, "assertion", {"finding": _finding("f-entity", 100, fact_id=PRED_ENTITY_FACT_ID)}),
        ]

        superseded_acts = [
            *entity_acts,
            act(3, "entity-superseded", {"entity_id": ENTITY_ID}),
            act(4, "migration-adoption", {"migration": ENTITY_MIGRATION}),
        ]
        superseded_state = project(tuple(superseded_acts), self.registry)
        superseded_claims = tuple(
            claim
            for claim in superseded_state.presented_successor_claims
            if claim["migration_id"] == ENTITY_MIGRATION_ID
        )
        self.assertEqual(superseded_claims, ())
        self.assertNotIn(PRED_ENTITY_FACT_ID, facts.facts_of(superseded_state.fact_state))

        retracted_acts = [
            *entity_acts,
            _retraction(3, "f-entity"),
            act(4, "migration-adoption", {"migration": ENTITY_MIGRATION}),
        ]
        with self.assertRaises(FindingModelError) as ctx:
            project(tuple(retracted_acts), self.registry)
        self.assertIn(MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM, str(ctx.exception))
        self.assertIn(PRED_ENTITY_FACT_ID, str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
