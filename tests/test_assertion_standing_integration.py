"""Integration unit: the withdrawal lifecycle through the real act log.

Track 0 (``tests/test_assertion_standing_track0.py``) proved the lifecycle
almost entirely by folding act tuples through ``findings.project`` — the
right instrument for discriminating mechanisms, but not proof the capability
works in a workspace. This unit drives the real ``ActLog`` against a real
workspace directory: every act here is appended with its own revision,
committed to a real file on disk, read back, and only then projected.
Nothing here constructs a tuple of acts and folds it directly without first
passing it through ``ActLog.append``.

Two forcing consumers, named by the integration-unit charter:

- a synthetic nominee-shaped fact (``INTEGRATION_ATTR``): per-report,
  per-owner, ``free`` supersession, matching no source-family member
  predicate. This is the shape the paused nominee-allocation work needs;
  it carries no tax meaning.
- ``tax.us.2025.f1098.liable-and-paid``, through the real content registry
  and the committed f1098 bundle. Track 0 verified it sits in no declared
  subset, companion-presence, companion-equality, or family-member
  relation, so it exercises the ordinary retraction path, not a fenced one.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.kernel.act_log import ActLog, ActLogError
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for
from packages.kernel.findings import (
    FindingModelError,
    _current_value_for_fact,
    _NO_CURRENT_VALUE,
    apply_act,
    initial_state,
    project,
)
from packages.kernel.read_models import build_read_model
from packages.tax.loader import TAX_CONTENT_DIR, tax_registry
from tests.support import demo_entity, registry_with_demo_kinds

RETRACTION_KIND = "finding-retracted"


def _envelope(
    act_id: str,
    kind: str,
    payload: dict[str, Any],
    committed_against: int,
    actor: str = "user",
    at: str = "2026-01-01T00:00:00Z",
) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": act_id,
        "kind": kind,
        "actor": actor,
        "at": at,
        "committed_against": committed_against,
        "payload": payload,
    }


class LoggedFold:
    """Appends acts to a real ``ActLog`` one at a time, folding incrementally.

    ``self.folded`` is built the *fold* way: one ``apply_act`` call per act,
    as each act lands. ``self.log.read()`` afterward gives the *replay* way:
    the committed file, re-read from disk and re-validated by the registry.
    The two must agree — that agreement is what "replay equals fold" means.
    """

    def __init__(self, log: ActLog, registry: Any) -> None:
        self.log = log
        self.registry = registry
        self.revision = 0
        self.folded = initial_state()
        self.committed: list[dict[str, Any]] = []

    def append(
        self,
        act_id: str,
        kind: str,
        payload: dict[str, Any],
        actor: str = "user",
        at: str = "2026-01-01T00:00:00Z",
    ) -> dict[str, Any]:
        envelope = _envelope(act_id, kind, payload, self.revision, actor, at)
        self.revision = self.log.append(envelope, expected_revision=self.revision)
        self.committed.append(envelope)
        self.folded = apply_act(self.folded, envelope, self.registry)
        return envelope


# --------------------------------------------------------------- consumer 1
# A synthetic nominee-shaped fact: the shape the paused nominee-allocation
# work needs. Per-report, per-owner, ``free`` supersession, no source-family
# member predicate declared for it anywhere. No tax classification or
# consequence is attached; it is a forcing consumer only.

INTEGRATION_ATTR = "integration.nominee.report-owner-attribution"
INTEGRATION_KEYS: list[dict[str, Any]] = [
    {"name": "report", "kind": "entity", "entity_kind": "integration.report"},
    {"name": "owner", "kind": "entity", "entity_kind": "integration.person"},
]
INTEGRATION_BUNDLE: dict[str, Any] = {
    "schema": "bundle.v1",
    "id": "integration.nominee.vocabulary",
    "label": "Integration nominee-shaped forcing vocabulary",
    "fact_types": [
        {
            "schema": "fact-type.v1",
            "id": INTEGRATION_ATTR,
            "title": "Synthetic nominee-shaped attribution (forcing consumer only)",
            "nature": "determinable",
            "identity_keys": INTEGRATION_KEYS,
            "value_schema": {"type": "number"},
            "supersession": {"policy": "free"},
        }
    ],
}


def _integration_fact_id(owner: str) -> str:
    return fact_id_for(
        INTEGRATION_ATTR, (("report", "integration-report-1"), ("owner", owner))
    )


def _integration_finding(finding_id: str, fact_id: str, value: int) -> dict[str, Any]:
    return {
        "schema": "finding.v1",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }


class SyntheticNomineeShapedLifecycle(unittest.TestCase):
    """The full lifecycle for the synthetic forcing consumer, through a real
    workspace directory. Two owners of the same report stay independent
    throughout — nothing in this class ever folds a tuple directly."""

    OWNER_A = "integration-owner-pat"
    OWNER_B = "integration-owner-kim"

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        root = Path(self._tmp.name)
        schema_dir = root / "schemas"
        schema_dir.mkdir()
        self.registry = registry_with_demo_kinds(schema_dir)
        self.workspace = root / "workspace"
        self.log = ActLog(self.workspace, self.registry)
        self.fact_a = _integration_fact_id(self.OWNER_A)
        self.fact_b = _integration_fact_id(self.OWNER_B)

        self.lf = LoggedFold(self.log, self.registry)
        self.lf.append("int-000-bundle", "bundle-adoption", {"bundle": INTEGRATION_BUNDLE})
        self.lf.append(
            "int-001-report",
            "entity-introduced",
            {"entity": demo_entity("integration-report-1", "Report 1", "integration.report")},
        )
        self.lf.append(
            "int-002-pat",
            "entity-introduced",
            {"entity": demo_entity(self.OWNER_A, "Pat", "integration.person")},
        )
        self.lf.append(
            "int-003-kim",
            "entity-introduced",
            {"entity": demo_entity(self.OWNER_B, "Kim", "integration.person")},
        )

        # A: assert, correct, withdraw (retract), assert again.
        self.lf.append(
            "int-004-a-first",
            "assertion",
            {"finding": _integration_finding("int-finding-a-450", self.fact_a, 450)},
        )
        self.lf.append(
            "int-005-b-only",
            "assertion",
            {"finding": _integration_finding("int-finding-b-100", self.fact_b, 100)},
        )
        self.lf.append(
            "int-006-a-correct",
            "assertion",
            {"finding": _integration_finding("int-finding-a-250", self.fact_a, 250)},
        )
        self.retracting_act_id = "int-007-a-retract"
        self.lf.append(
            "int-007-a-retract", RETRACTION_KIND, {"finding_id": "int-finding-a-250"}, actor="auditor-1"
        )
        self.lf.append(
            "int-008-a-reassert",
            "assertion",
            {"finding": _integration_finding("int-finding-a-250-again", self.fact_a, 250)},
        )

    def _replayed_state(self) -> Any:
        """Read the committed log back off disk and project it."""
        contents = self.log.read()
        return project(contents.acts, self.registry)

    def test_full_lifecycle_and_owner_independence(self) -> None:
        state = self._replayed_state()
        view = compute_currency(state)
        # A: retracted-then-reasserted finding is current; the retracted and
        # corrected-away findings for A are not.
        self.assertIn("int-finding-a-250-again", view.current_finding_ids)
        self.assertNotIn("int-finding-a-250", view.current_finding_ids)
        self.assertNotIn("int-finding-a-450", view.current_finding_ids)
        self.assertEqual(_current_value_for_fact(state, self.fact_a), 250)
        # B never touched: independent throughout.
        self.assertIn("int-finding-b-100", view.current_finding_ids)
        self.assertEqual(_current_value_for_fact(state, self.fact_b), 100)

    def test_withdrawn_fact_returns_to_the_unanswered_shape(self) -> None:
        """After retraction and before reassertion, the fact has no current
        answer at all -- not a zero, not a false, not an opposite claim."""
        contents = self.log.read()
        state_after_retraction = project(contents.acts[:8], self.registry)
        value = _current_value_for_fact(state_after_retraction, self.fact_a)
        self.assertIs(value, _NO_CURRENT_VALUE)
        view = compute_currency(state_after_retraction)
        self.assertEqual(
            view.current_finding_ids & {"int-finding-a-450", "int-finding-a-250"}, frozenset()
        )

    # ---------------------------------------------------------- replay==fold
    def test_replay_equals_fold(self) -> None:
        """Read the committed log back from disk and project it; the result
        must equal the state built incrementally, one act at a time, as it
        was appended. This is the property the append-only design rests on."""
        replayed = self._replayed_state()
        self.assertEqual(replayed, self.lf.folded)
        # And the read models built from each path agree too.
        replayed_model = build_read_model(self.log.read().acts, self.registry)
        folded_view = compute_currency(self.lf.folded)
        self.assertEqual(
            sorted(replayed_model["current"]["finding_ids"]),
            sorted(folded_view.current_finding_ids),
        )

    # ------------------------------------------------------------ attribution
    def test_attribution_recoverable_by_walking_the_log(self) -> None:
        """From a finding id to the act that carried it, and from a
        displacement reason to the act that withdrew it -- both recovered by
        walking the committed log, never from a field on the finding itself."""
        contents = self.log.read()
        acts_by_id = {a["act_id"]: a for a in contents.acts}

        # Finding -> the act that carried it (walk the log for the assertion
        # whose payload names this finding id).
        target_finding_id = "int-finding-a-250"
        carrying_act = next(
            a
            for a in contents.acts
            if a["kind"] == "assertion" and a["payload"]["finding"]["id"] == target_finding_id
        )
        self.assertEqual(carrying_act["act_id"], "int-006-a-correct")
        self.assertEqual(carrying_act["actor"], "user")

        # Displacement reason -> the act that withdrew it.
        state = project(contents.acts, self.registry)
        view = compute_currency(state)
        reasons = {r.kind: r.by for r in view.reasons[target_finding_id]}
        self.assertIn("retraction", reasons)
        retracting_act_id = reasons["retraction"]
        retracting_act = acts_by_id[retracting_act_id]
        self.assertEqual(retracting_act["kind"], RETRACTION_KIND)
        self.assertEqual(retracting_act["payload"], {"finding_id": target_finding_id})
        self.assertEqual(retracting_act["actor"], "auditor-1")

        # The whole ordered history for the fact survives the walk.
        history = [
            (a["act_id"], a["kind"])
            for a in contents.acts
            if a["kind"] in ("assertion", RETRACTION_KIND)
            and (
                (a["kind"] == "assertion" and a["payload"]["finding"]["fact_id"] == self.fact_a)
                or (a["kind"] == RETRACTION_KIND and a["payload"]["finding_id"] in
                    {"int-finding-a-450", "int-finding-a-250", "int-finding-a-250-again"})
            )
        ]
        self.assertEqual(
            [act_id for act_id, _ in history],
            ["int-004-a-first", "int-006-a-correct", "int-007-a-retract", "int-008-a-reassert"],
        )

    # ---------------------------------------------------------- the two gates
    def test_log_refuses_a_stale_revision(self) -> None:
        """The log's own staleness check: a client that computes an envelope
        against a revision the workspace has already moved past."""
        stale = _envelope(
            "int-stale-retract",
            RETRACTION_KIND,
            {"finding_id": "int-finding-b-100"},
            committed_against=self.lf.revision - 1,
        )
        with self.assertRaises(ActLogError) as caught:
            self.log.append(stale, expected_revision=self.lf.revision - 1)
        self.assertIn("stale revision", str(caught.exception))
        # The log itself is untouched by the refused attempt.
        self.assertEqual(self.log.read().revision, self.lf.revision)

    def test_admission_refuses_a_target_no_longer_current(self) -> None:
        """Distinct from the log's staleness check: a client at the *current*
        revision (the log accepts the envelope structurally) that names a
        finding admission's own currency projection says is no longer
        current -- here, the already-retracted-and-corrected-away
        ``int-finding-a-250``."""
        current_revision = self.lf.revision
        envelope = _envelope(
            "int-noncurrent-retract",
            RETRACTION_KIND,
            {"finding_id": "int-finding-a-250"},
            committed_against=current_revision,
        )
        # The log admits it -- the revision is exactly current.
        new_revision = self.log.append(envelope, expected_revision=current_revision)
        self.assertEqual(new_revision, current_revision + 1)
        # Admission (projecting the committed log) refuses it.
        contents = self.log.read()
        with self.assertRaises(FindingModelError) as caught:
            project(contents.acts, self.registry)
        self.assertIn("not current", str(caught.exception))


# --------------------------------------------------------------- consumer 2
# tax.us.2025.f1098.liable-and-paid, through the real content registry.


class RealF1098Lifecycle(unittest.TestCase):
    """The same lifecycle proof, through the real production tax registry
    and the committed f1098 bundle, against a second real workspace."""

    FACT_TYPE = "tax.us.2025.f1098.liable-and-paid"
    LENDER_A = "integration-lender-a"
    LENDER_B = "integration-lender-b"
    STATEMENT_A = "integration-1098-statement-a"
    STATEMENT_B = "integration-1098-statement-b"

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.registry = tax_registry()
        self.bundle = json.loads(
            (Path(TAX_CONTENT_DIR) / "f1098.bundle.json").read_text("utf-8")
        )
        self.workspace = Path(self._tmp.name) / "workspace"
        self.log = ActLog(self.workspace, self.registry)
        self.fact_a = fact_id_for(
            self.FACT_TYPE,
            (("payer", self.LENDER_A), ("statement", self.STATEMENT_A), ("tax-year", "2025")),
        )
        self.fact_b = fact_id_for(
            self.FACT_TYPE,
            (("payer", self.LENDER_B), ("statement", self.STATEMENT_B), ("tax-year", "2025")),
        )

        self.lf = LoggedFold(self.log, self.registry)
        self.lf.append("f1098-000-bundle", "bundle-adoption", {"bundle": self.bundle})
        self.lf.append(
            "f1098-001-lender-a",
            "entity-introduced",
            {"entity": demo_entity(self.LENDER_A, "Lender A", "tax.us.mortgage-lender")},
        )
        self.lf.append(
            "f1098-002-statement-a",
            "entity-introduced",
            {"entity": demo_entity(self.STATEMENT_A, "Statement A", "tax.us.1098-statement")},
        )
        self.lf.append(
            "f1098-003-lender-b",
            "entity-introduced",
            {"entity": demo_entity(self.LENDER_B, "Lender B", "tax.us.mortgage-lender")},
        )
        self.lf.append(
            "f1098-004-statement-b",
            "entity-introduced",
            {"entity": demo_entity(self.STATEMENT_B, "Statement B", "tax.us.1098-statement")},
        )

        # A: assert "yes", correct to "no", withdraw (retract), assert "yes" again.
        self.lf.append(
            "f1098-005-a-first",
            "assertion",
            {"finding": self._finding("f1098-finding-a-yes", self.fact_a, "yes")},
        )
        self.lf.append(
            "f1098-006-b-only",
            "assertion",
            {"finding": self._finding("f1098-finding-b-no", self.fact_b, "no")},
        )
        self.lf.append(
            "f1098-007-a-correct",
            "assertion",
            {"finding": self._finding("f1098-finding-a-no", self.fact_a, "no")},
        )
        self.lf.append(
            "f1098-008-a-retract",
            RETRACTION_KIND,
            {"finding_id": "f1098-finding-a-no"},
            actor="auditor-2",
        )
        self.lf.append(
            "f1098-009-a-reassert",
            "assertion",
            {"finding": self._finding("f1098-finding-a-yes-again", self.fact_a, "yes")},
        )

    def _finding(self, finding_id: str, fact_id: str, value: str) -> dict[str, Any]:
        return {
            "schema": "finding.v1",
            "id": finding_id,
            "fact_id": fact_id,
            "value": value,
            "basis": "attested",
            "evidence_ids": [],
        }

    def _replayed_state(self) -> Any:
        contents = self.log.read()
        return project(contents.acts, self.registry)

    def test_full_lifecycle_and_independence_on_real_content(self) -> None:
        state = self._replayed_state()
        view = compute_currency(state)
        self.assertIn("f1098-finding-a-yes-again", view.current_finding_ids)
        self.assertNotIn("f1098-finding-a-no", view.current_finding_ids)
        self.assertNotIn("f1098-finding-a-yes", view.current_finding_ids)
        self.assertEqual(_current_value_for_fact(state, self.fact_a), "yes")
        # B untouched: independent throughout.
        self.assertIn("f1098-finding-b-no", view.current_finding_ids)
        self.assertEqual(_current_value_for_fact(state, self.fact_b), "no")

    def test_withdrawn_fact_returns_to_the_unanswered_shape(self) -> None:
        contents = self.log.read()
        state_after_retraction = project(contents.acts[:9], self.registry)
        value = _current_value_for_fact(state_after_retraction, self.fact_a)
        self.assertIs(value, _NO_CURRENT_VALUE)

    def test_replay_equals_fold(self) -> None:
        replayed = self._replayed_state()
        self.assertEqual(replayed, self.lf.folded)
        replayed_model = build_read_model(self.log.read().acts, self.registry)
        folded_view = compute_currency(self.lf.folded)
        self.assertEqual(
            sorted(replayed_model["current"]["finding_ids"]),
            sorted(folded_view.current_finding_ids),
        )

    def test_read_models_derivation_and_currency_agree_at_each_stage(self) -> None:
        """Read models, and the unified current-standing path
        (``_current_value_for_fact``), agree at each stage of the lifecycle."""
        contents = self.log.read()
        for count, (finding_id, value) in {
            6: ("f1098-finding-a-yes", "yes"),
            7: ("f1098-finding-a-yes", "yes"),  # b-only: fact_a's pointer unchanged
            8: ("f1098-finding-a-no", "no"),
            9: (None, None),  # retracted: fact reopens
            10: ("f1098-finding-a-yes-again", "yes"),
        }.items():
            with self.subTest(after_acts=count):
                acts = contents.acts[:count]
                state = project(acts, self.registry)
                model = build_read_model(acts, self.registry)
                current = _current_value_for_fact(state, self.fact_a)
                self.assertEqual(None if current is _NO_CURRENT_VALUE else current, value)
                pointer = model["facts"][self.fact_a]["current_finding_id"]
                self.assertEqual(pointer, finding_id)
                self.assertEqual(
                    model["current"]["finding_ids"].count(finding_id) if finding_id else 0,
                    1 if finding_id else 0,
                )

    def test_attribution_recoverable_by_walking_the_log(self) -> None:
        contents = self.log.read()
        acts_by_id = {a["act_id"]: a for a in contents.acts}

        target_finding_id = "f1098-finding-a-no"
        carrying_act = next(
            a
            for a in contents.acts
            if a["kind"] == "assertion" and a["payload"]["finding"]["id"] == target_finding_id
        )
        self.assertEqual(carrying_act["act_id"], "f1098-007-a-correct")

        state = project(contents.acts, self.registry)
        view = compute_currency(state)
        reasons = {r.kind: r.by for r in view.reasons[target_finding_id]}
        self.assertIn("retraction", reasons)
        retracting_act = acts_by_id[reasons["retraction"]]
        self.assertEqual(retracting_act["kind"], RETRACTION_KIND)
        self.assertEqual(retracting_act["payload"], {"finding_id": target_finding_id})
        self.assertEqual(retracting_act["actor"], "auditor-2")

    def test_log_refuses_a_stale_revision(self) -> None:
        stale = _envelope(
            "f1098-stale-retract",
            RETRACTION_KIND,
            {"finding_id": "f1098-finding-b-no"},
            committed_against=self.lf.revision - 1,
        )
        with self.assertRaises(ActLogError) as caught:
            self.log.append(stale, expected_revision=self.lf.revision - 1)
        self.assertIn("stale revision", str(caught.exception))
        self.assertEqual(self.log.read().revision, self.lf.revision)

    def test_admission_refuses_a_target_no_longer_current(self) -> None:
        current_revision = self.lf.revision
        envelope = _envelope(
            "f1098-noncurrent-retract",
            RETRACTION_KIND,
            {"finding_id": "f1098-finding-a-no"},
            committed_against=current_revision,
        )
        new_revision = self.log.append(envelope, expected_revision=current_revision)
        self.assertEqual(new_revision, current_revision + 1)
        contents = self.log.read()
        with self.assertRaises(FindingModelError) as caught:
            project(contents.acts, self.registry)
        self.assertIn("not current", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
