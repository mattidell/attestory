"""Track 0: the assertion-standing lifecycle spike (checkpoint T0-A).

Every case below runs through a real boundary, never a hand-built state:

- the **revision layer** is ``ActLog.append`` against a real workspace
  directory and the published schema registry;
- the **admission layer** is ``findings.project`` / ``findings.apply_act``,
  which folds each act through the same appliers production uses.

Ids, entities, and values are synthetic ``demo.*`` / ``demo-*`` throughout.
The vocabulary is the P2 probe's, so the executed evidence lines up with what
that probe recorded on the committed kernel.
"""

from __future__ import annotations

import itertools
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.kernel.act_log import ActLog, ActLogError
from packages.kernel.schema_registry import SchemaValidationError
from packages.kernel.currency import compute_currency
from packages.kernel.findings import (
    FindingModelError,
    _current_value_for_fact,
    _current_values_for_fact_type,
    _NO_CURRENT_VALUE,
    project,
)
from tests.support import (
    act,
    demo_entity,
    demo_evidence,
    demo_finding,
    registry_with_demo_kinds,
)

RETRACTION_KIND = "finding-retracted"
PAYLOAD_EXAMPLE = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "prototypes"
    / "assertion-standing-retraction-semantics"
    / "act-finding-retracted.v1.example.json"
)

# ------------------------------------------------------------------ vocabulary
ATTR = "demo.report-owner-attribution"   # nominee-shaped forcing fact (non-family)
MEMBER = "demo.w2.box1"                  # source-family member control
PRED, SUCC = "demo.pred.flag", "demo.succ.flag"   # migration control
LOCKED = "demo.single-shot"              # locked-policy control
GATED = "demo.gated.amount"              # closed-on-attestation control
GATE = "demo.gated.closure"              # its gate fact type


def ft(
    type_id: str,
    keys: list[dict[str, Any]],
    value_schema: dict[str, Any],
    schema: str = "fact-type.v1",
    policy: str = "free",
    gate: str | None = None,
) -> dict[str, Any]:
    supersession: dict[str, Any] = {"policy": policy}
    if gate is not None:
        supersession["gate"] = {"fact_type": gate}
    return {
        "schema": schema,
        "id": type_id,
        "title": type_id,
        "nature": "determinable",
        "identity_keys": keys,
        "value_schema": value_schema,
        "supersession": supersession,
    }


ENTITY_KEYS: list[dict[str, Any]] = [
    {"name": "report", "kind": "entity", "entity_kind": "demo.report"},
    {"name": "owner", "kind": "entity", "entity_kind": "demo.person"},
]
LITERAL_YEAR: list[dict[str, Any]] = [{"name": "tax-year", "kind": "literal", "values": ["2025"]}]
CP_KEYS: list[dict[str, Any]] = [
    {"name": "counterparty", "kind": "entity", "entity_kind": "demo.counterparty"},
    {"name": "period", "kind": "literal", "values": ["2025"]},
]

BUNDLE_V1 = {
    "schema": "bundle.v1",
    "id": "demo.track0.vocabulary",
    "label": "Track 0 vocabulary",
    "fact_types": [
        ft(ATTR, ENTITY_KEYS, {"type": "number"}),
        ft(MEMBER, CP_KEYS, {"type": "number"}),
        ft(PRED, LITERAL_YEAR, {"enum": ["yes", "no"]}),
        ft(SUCC, LITERAL_YEAR, {"enum": ["yes", "no"]}),
    ],
}
# fact-type.v3 is the only published fact-type version whose supersession
# vocabulary carries `locked` and `closed-on-attestation`, and only bundle.v3
# carries fact-type.v3. The act log cannot commit a bundle.v3 adoption -
# `_payload_schema_id` selects act-bundle-adoption.v1/.v2 by the nested
# bundle's declared schema and has no v3 branch - so the policy-gate cases are
# exercised at the projection boundary only (P2 observation O8a-V3).
BUNDLE_V3 = {
    "schema": "bundle.v3",
    "id": "demo.track0.policies",
    "label": "Track 0 policy vocabulary",
    "fact_types": [
        ft(LOCKED, LITERAL_YEAR, {"enum": ["a", "b"]}, schema="fact-type.v3", policy="locked"),
        ft(GATE, LITERAL_YEAR, {"type": "boolean"}, schema="fact-type.v3"),
        ft(
            GATED,
            LITERAL_YEAR,
            {"type": "number"},
            schema="fact-type.v3",
            policy="closed-on-attestation",
            gate=GATE,
        ),
    ],
}
MIGRATION = {
    "schema": "migration-artifact.v1",
    "id": "demo.track0.succession",
    "version": "v1",
    "title": "Track 0 succession",
    "finding_mapping": {"policy": "presented-claim"},
    "pairs": [{"predecessor": PRED, "successor": SUCC}],
}

ATTR_PAT = f"{ATTR}|report=demo-report-1,owner=demo-pat"
ATTR_KIM = f"{ATTR}|report=demo-report-1,owner=demo-kim"
MEMBER_FACT = f"{MEMBER}|counterparty=demo-corp-a,period=2025"
PRED_FACT = f"{PRED}|tax-year=2025"
LOCKED_FACT = f"{LOCKED}|tax-year=2025"
GATED_FACT = f"{GATED}|tax-year=2025"
GATE_FACT = f"{GATE}|tax-year=2025"

F_450 = "demo-finding-attr-450"
F_250 = "demo-finding-attr-250"
F_250_AGAIN = "demo-finding-attr-250-reasserted"
F_KIM = "demo-finding-attr-kim-100"

FAMILY = {"id": "demo.w2", "version": "v1"}
FAMILY_SCOPE = {"tax-year": "2025"}


def fnd(finding_id: str, fact_id: str, value: Any) -> dict[str, Any]:
    return demo_finding(
        finding_id=finding_id, fact_id=fact_id, value=value, basis="attested", evidence_ids=[]
    )


def retraction(index: int, finding_id: str, actor: str = "user") -> dict[str, Any]:
    envelope = act(index, RETRACTION_KIND, {"finding_id": finding_id})
    envelope["actor"] = actor
    return envelope


def base_acts() -> list[dict[str, Any]]:
    """Vocabulary and entities, before any assertion. Indices 0-6."""
    return [
        act(0, "bundle-adoption", {"bundle": BUNDLE_V1}),
        act(1, "bundle-adoption", {"bundle": BUNDLE_V3}),
        act(2, "entity-introduced", {"entity": demo_entity("demo-report-1", "Report 1", "demo.report")}),
        act(3, "entity-introduced", {"entity": demo_entity("demo-pat", "Pat", "demo.person")}),
        act(4, "entity-introduced", {"entity": demo_entity("demo-kim", "Kim", "demo.person")}),
        act(5, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Corp A")}),
        act(6, "evidence-submitted", {"evidence": demo_evidence()}),
    ]


class Track0Base(unittest.TestCase):
    """Shared registry over the real published kernel schemas."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp_path = Path(self._tmp.name)
        self.registry = registry_with_demo_kinds(self.tmp_path)
        self.registry.family_member_predicates.add(MEMBER)

    def current_value(self, state: Any, fact_id: str) -> Any:
        return _current_value_for_fact(state, fact_id)

    def reason_kinds(self, view: Any, finding_id: str) -> list[str]:
        return [reason.kind for reason in view.reasons.get(finding_id, ())]


class TestPayloadContract(Track0Base):
    """The Payload Instantiation Gate, discharged by instantiation."""

    def test_committed_positive_instance_validates_against_the_published_schema(self) -> None:
        """Boundary: SchemaRegistry.validate on the committed instance file."""
        instance = json.loads(PAYLOAD_EXAMPLE.read_text("utf-8"))
        self.registry.validate("act-finding-retracted.v1", instance)
        self.assertEqual(instance, {"finding_id": F_250})

    def test_payload_admits_nothing_but_a_finding_id(self) -> None:
        """Boundary: SchemaRegistry.validate; the payload names no fact,
        value, reason, replacement, or actor."""
        for extra in ("fact_id", "value", "reason", "replacement", "actor"):
            with self.subTest(field=extra):
                with self.assertRaises(SchemaValidationError):
                    self.registry.validate(
                        "act-finding-retracted.v1", {"finding_id": F_250, extra: "x"}
                    )
        with self.assertRaises(SchemaValidationError):
            self.registry.validate("act-finding-retracted.v1", {})
        with self.assertRaises(SchemaValidationError):
            self.registry.validate("act-finding-retracted.v1", {"finding_id": ""})

    def test_committed_instance_drives_a_real_fold(self) -> None:
        """Boundary: findings.project, fed the committed instance verbatim."""
        instance = json.loads(PAYLOAD_EXAMPLE.read_text("utf-8"))
        acts = base_acts() + [
            act(7, "assertion", {"finding": fnd(F_450, ATTR_PAT, 450)}),
            act(8, "assertion", {"finding": fnd(F_250, ATTR_PAT, 250)}),
            {**act(9, RETRACTION_KIND, instance)},
        ]
        state = project(tuple(acts), self.registry)
        self.assertEqual(state.retracted_finding_ids, frozenset({F_250}))
        self.assertIs(self.current_value(state, ATTR_PAT), _NO_CURRENT_VALUE)


class TestRevisionLayer(Track0Base):
    """The act log: a real workspace file, real envelope + payload validation."""

    def _log_with_base(self) -> tuple[ActLog, int, list[dict[str, Any]]]:
        log = ActLog(self.tmp_path / "ws", self.registry)
        revision = 0
        # bundle.v3 cannot be committed to the log (see BUNDLE_V3's note), so
        # the logged prefix carries the v1 vocabulary only.
        logged = [a for a in base_acts() if a["payload"].get("bundle", {}).get("schema") != "bundle.v3"]
        committed: list[dict[str, Any]] = []
        for index, a in enumerate(logged):
            entry = {**a, "act_id": f"demo-log-act-{index:03d}", "committed_against": index}
            revision = log.append(entry, revision)
            committed.append(entry)
        return log, revision, committed

    def test_act_log_commits_a_real_retraction_act(self) -> None:
        """Boundary: ActLog.append. The envelope validates against act.v1 and
        the payload against act-finding-retracted.v1, both from the published
        manifest; the actor is recorded on the line."""
        log, revision, _ = self._log_with_base()
        for finding_id, value in ((F_450, 450), (F_250, 250)):
            entry = {
                **act(0, "assertion", {"finding": fnd(finding_id, ATTR_PAT, value)}),
                "act_id": f"demo-log-assert-{finding_id}",
                "committed_against": revision,
            }
            revision = log.append(entry, revision)
        entry = {
            **retraction(0, F_250, actor="demo-user-b"),
            "act_id": "demo-log-retract",
            "committed_against": revision,
        }
        revision = log.append(entry, revision)

        contents = log.read()
        self.assertEqual(contents.revision, revision)
        last = contents.acts[-1]
        self.assertEqual(last["kind"], RETRACTION_KIND)
        self.assertEqual(last["payload"], {"finding_id": F_250})
        self.assertEqual(last["actor"], "demo-user-b")
        # And the committed log projects: the same acts, folded.
        state = project(contents.acts, self.registry)
        self.assertEqual(state.retracted_finding_ids, frozenset({F_250}))

    def test_L6_act_log_refuses_a_stale_committed_against(self) -> None:
        """L6, revision layer. Boundary: ActLog.append. This is the *other*
        staleness layer from the admission refusal below; the two are
        deliberately separate tests because they catch different clients."""
        log, revision, _ = self._log_with_base()
        entry = {
            **act(0, "assertion", {"finding": fnd(F_450, ATTR_PAT, 450)}),
            "act_id": "demo-log-assert-450",
            "committed_against": revision,
        }
        revision = log.append(entry, revision)
        stale = {
            **retraction(0, F_450),
            "act_id": "demo-log-retract-stale",
            "committed_against": revision - 1,
        }
        with self.assertRaises(ActLogError) as caught:
            log.append(stale, revision)
        self.assertIn("commits against revision", str(caught.exception))


class TestLifecycle(Track0Base):
    """L1-L5: assert, correct, retract, reassert, independence.

    Boundary throughout: findings.project (which folds every act through
    findings.apply_act) plus currency.compute_currency over the result.
    """

    def _through(self, count: int) -> Any:
        return project(tuple(self.acts[:count]), self.registry)

    def setUp(self) -> None:
        super().setUp()
        self.acts = base_acts() + [
            act(7, "assertion", {"finding": fnd(F_450, ATTR_PAT, 450)}),          # L1
            act(8, "assertion", {"finding": fnd(F_KIM, ATTR_KIM, 100)}),          # L5
            act(9, "assertion", {"finding": fnd(F_250, ATTR_PAT, 250)}),          # L2
            retraction(10, F_250),                                                # L3
            act(11, "assertion", {"finding": fnd(F_250_AGAIN, ATTR_PAT, 250)}),   # L4
        ]

    def test_L1_assertion_is_current(self) -> None:
        state = self._through(8)
        view = compute_currency(state)
        self.assertIn(F_450, view.current_finding_ids)
        self.assertEqual(self.current_value(state, ATTR_PAT), 450)

    def test_L2_correction_replaces_the_answer_and_keeps_the_fact(self) -> None:
        state = self._through(10)
        view = compute_currency(state)
        self.assertIn(F_250, view.current_finding_ids)
        self.assertNotIn(F_450, view.current_finding_ids)
        self.assertEqual(self.reason_kinds(view, F_450), ["correction"])
        self.assertEqual(self.current_value(state, ATTR_PAT), 250)

    def test_L3_retraction_leaves_no_current_answer_and_no_opposite_claim(self) -> None:
        state = self._through(11)
        view = compute_currency(state)
        self.assertEqual(view.current_finding_ids & {F_450, F_250}, frozenset())
        self.assertEqual(self.reason_kinds(view, F_250), ["retraction"])
        # No zero, no false, no opposite claim: the fact simply has no answer.
        self.assertIs(self.current_value(state, ATTR_PAT), _NO_CURRENT_VALUE)
        self.assertNotIn(ATTR_PAT, _current_values_for_fact_type(state, ATTR))
        # The corrected-away answer is not revived by the retraction.
        self.assertEqual(self.reason_kinds(view, F_450), ["correction"])
        # The proposition itself is untouched: no entity died, no family moved.
        self.assertEqual(state.withdrawn_fact_ids, frozenset())
        self.assertEqual(state.fact_state.retired_fact_type_ids, frozenset())

    def test_L3_by_names_the_retracting_act(self) -> None:
        """The retraction reason names the act, which is the attribution path:
        the envelope carries actor and time."""
        state = self._through(11)
        view = compute_currency(state)
        reason = view.reasons[F_250][0]
        self.assertEqual(reason.kind, "retraction")
        self.assertEqual(reason.by, self.acts[10]["act_id"])
        self.assertEqual(state.retraction_acts[F_250], self.acts[10]["act_id"])

    def test_L4_reassertion_is_a_new_finding_that_becomes_current(self) -> None:
        state = self._through(12)
        view = compute_currency(state)
        self.assertIn(F_250_AGAIN, view.current_finding_ids)
        self.assertEqual(self.current_value(state, ATTR_PAT), 250)
        # Same stable fact, not a new one.
        self.assertEqual(state.findings[F_250_AGAIN]["fact_id"], ATTR_PAT)

    def test_L4_retracted_finding_carries_both_retraction_and_correction(self) -> None:
        """The retracted finding is displaced twice over: first by the
        retraction, then again by the reassertion that corrects it away.
        Explanation consumers must tolerate composed reasons.

        Note the *list* order is `compute_currency`'s contributor order
        (corrections, withdrawals, migrations, retractions, then closure),
        not the order the events happened in. Nothing in the reason tuple
        carries event time; the act log does. This test asserts the order the
        committed kernel actually produces rather than the event order, so a
        later decision to make reason order chronological fails here loudly
        instead of passing silently."""
        state = self._through(12)
        view = compute_currency(state)
        self.assertEqual(set(self.reason_kinds(view, F_250)), {"correction", "retraction"})
        self.assertEqual(self.reason_kinds(view, F_250), ["correction", "retraction"])
        by = {reason.kind: reason.by for reason in view.reasons[F_250]}
        self.assertEqual(by["retraction"], self.acts[10]["act_id"])
        self.assertEqual(by["correction"], F_250_AGAIN)

    def test_L4_history_retains_all_three_findings_in_order(self) -> None:
        state = self._through(12)
        self.assertEqual(
            [fid for fid, f in state.findings.items() if f["fact_id"] == ATTR_PAT],
            [F_450, F_250, F_250_AGAIN],
        )

    def test_L4_revival_by_id_reuse_is_refused(self) -> None:
        """The existing duplicate-id check, not a new rule: a reassertion may
        not resurrect the retracted finding by reusing its id."""
        acts = list(self.acts[:11]) + [
            act(11, "assertion", {"finding": fnd(F_250, ATTR_PAT, 250)})
        ]
        with self.assertRaises(FindingModelError) as caught:
            project(tuple(acts), self.registry)
        self.assertIn("finding already exists", str(caught.exception))

    def test_L5_an_independent_proposition_is_untouched(self) -> None:
        for count in (9, 10, 11, 12):
            with self.subTest(after_acts=count):
                state = project(tuple(self.acts[:count]), self.registry)
                view = compute_currency(state)
                self.assertIn(F_KIM, view.current_finding_ids)
                self.assertEqual(self.current_value(state, ATTR_KIM), 100)
                self.assertNotIn(F_KIM, view.reasons)
                self.assertEqual(state.findings[F_KIM], fnd(F_KIM, ATTR_KIM, 100))


class TestAdmissionRefusals(Track0Base):
    """The five refusals, each at the admission boundary (findings.project)."""

    def _attr_acts(self) -> list[dict[str, Any]]:
        return base_acts() + [
            act(7, "assertion", {"finding": fnd(F_450, ATTR_PAT, 450)}),
            act(8, "assertion", {"finding": fnd(F_250, ATTR_PAT, 250)}),
        ]

    def test_refusal_1_unknown_finding(self) -> None:
        acts = self._attr_acts() + [retraction(9, "demo-finding-nonexistent")]
        with self.assertRaises(FindingModelError) as caught:
            project(tuple(acts), self.registry)
        self.assertIn("cannot retract unknown finding", str(caught.exception))

    def test_L6_refusal_2_corrected_away_finding_is_refused_at_admission(self) -> None:
        """L6 / D5. The client is at the current revision - the act log has no
        objection - and still may not retract the finding a later correction
        displaced. Nothing is silently retracted: 250 stays current."""
        acts = self._attr_acts() + [retraction(9, F_450)]
        with self.assertRaises(FindingModelError) as caught:
            project(tuple(acts), self.registry)
        message = str(caught.exception)
        self.assertIn("is not current", message)
        self.assertIn("correction by", message)
        surviving = project(tuple(self._attr_acts()), self.registry)
        self.assertEqual(self.current_value(surviving, ATTR_PAT), 250)

    def test_refusal_2_already_retracted_finding(self) -> None:
        acts = self._attr_acts() + [retraction(9, F_250), retraction(10, F_250)]
        with self.assertRaises(FindingModelError) as caught:
            project(tuple(acts), self.registry)
        self.assertIn("retraction by", str(caught.exception))

    def test_refusal_2_entity_displaced_finding(self) -> None:
        acts = self._attr_acts() + [
            act(9, "entity-superseded", {"entity_id": "demo-pat"}),
            retraction(10, F_250),
        ]
        with self.assertRaises(FindingModelError) as caught:
            project(tuple(acts), self.registry)
        self.assertIn("individuation by demo-pat", str(caught.exception))

    def test_refusal_2_migration_displaced_finding(self) -> None:
        acts = base_acts() + [
            act(7, "assertion", {"finding": fnd("demo-finding-pred", PRED_FACT, "yes")}),
            act(8, "migration-adoption", {"migration": MIGRATION}),
            retraction(9, "demo-finding-pred"),
        ]
        with self.assertRaises(FindingModelError) as caught:
            project(tuple(acts), self.registry)
        self.assertIn("supersession by demo.track0.succession", str(caught.exception))

    def test_L14_refusal_3_locked_policy(self) -> None:
        """L14 / D3, projection boundary only: bundle.v3 cannot ride the act
        log, so `project` is where a locked fact type can be exercised."""
        acts = base_acts() + [
            act(7, "assertion", {"finding": fnd("demo-finding-locked", LOCKED_FACT, "a")}),
            retraction(8, "demo-finding-locked"),
        ]
        with self.assertRaises(FindingModelError) as caught:
            project(tuple(acts), self.registry)
        message = str(caught.exception)
        self.assertIn("supersession policy 'locked'", message)
        self.assertIn("cannot retract", message)

    def test_L14_locked_correction_is_refused_on_the_same_predicate(self) -> None:
        """Retraction is not stricter than correction; it is the same gate."""
        acts = base_acts() + [
            act(7, "assertion", {"finding": fnd("demo-finding-locked", LOCKED_FACT, "a")}),
            act(8, "assertion", {"finding": fnd("demo-finding-locked-2", LOCKED_FACT, "b")}),
        ]
        with self.assertRaises(FindingModelError) as caught:
            project(tuple(acts), self.registry)
        self.assertIn("supersession policy 'locked'", str(caught.exception))

    def test_L14_locked_retraction_message_describes_retraction_not_correction(
        self,
    ) -> None:
        """(R1) The retraction refusal must not borrow the correction path's
        wording. It names the act actually refused (ending an answer) and the
        docstring's own reason: `already_answered` reads history, so
        retracting a `locked` fact's single answer would leave it permanently
        unanswerable. The correction-path message at the `already_answered`
        dispatch is unrelated and is asserted unchanged below."""
        acts = base_acts() + [
            act(7, "assertion", {"finding": fnd("demo-finding-locked", LOCKED_FACT, "a")}),
            retraction(8, "demo-finding-locked"),
        ]
        with self.assertRaises(FindingModelError) as caught:
            project(tuple(acts), self.registry)
        message = str(caught.exception)
        self.assertNotIn("correction", message)
        self.assertIn("ending this answer", message)
        self.assertIn("already_answered", message)
        self.assertIn("permanently unanswerable", message)

    def test_L14_locked_correction_message_is_unchanged(self) -> None:
        """(R1) The correction path's message at the `already_answered`
        dispatch is correct in its own place and must not change."""
        acts = base_acts() + [
            act(7, "assertion", {"finding": fnd("demo-finding-locked", LOCKED_FACT, "a")}),
            act(8, "assertion", {"finding": fnd("demo-finding-locked-2", LOCKED_FACT, "b")}),
        ]
        with self.assertRaises(FindingModelError) as caught:
            project(tuple(acts), self.registry)
        message = str(caught.exception)
        self.assertIn(
            "which does not permit correction here",
            message,
        )

    def test_L14_refusal_4_closed_on_attestation_with_the_gate_true(self) -> None:
        acts = base_acts() + [
            act(7, "assertion", {"finding": fnd("demo-finding-gated", GATED_FACT, 10)}),
            act(8, "assertion", {"finding": fnd("demo-finding-gate", GATE_FACT, True)}),
            retraction(9, "demo-finding-gated"),
        ]
        with self.assertRaises(FindingModelError) as caught:
            project(tuple(acts), self.registry)
        self.assertIn("is currently attested true", str(caught.exception))

    def test_L14_closed_on_attestation_permits_retraction_before_closure(self) -> None:
        """The gate is a state predicate, so the same act is admitted while
        the gate is absent and refused once it is attested true."""
        acts = base_acts() + [
            act(7, "assertion", {"finding": fnd("demo-finding-gated", GATED_FACT, 10)}),
            retraction(8, "demo-finding-gated"),
        ]
        state = project(tuple(acts), self.registry)
        self.assertEqual(state.retracted_finding_ids, frozenset({"demo-finding-gated"}))
        self.assertIs(self.current_value(state, GATED_FACT), _NO_CURRENT_VALUE)

    def test_L14_closed_on_attestation_permits_reassertion_after_retraction(self) -> None:
        """A reassertion after retraction is a correction, gated on closure
        exactly as today: admitted while the gate is not true."""
        acts = base_acts() + [
            act(7, "assertion", {"finding": fnd("demo-finding-gated", GATED_FACT, 10)}),
            retraction(8, "demo-finding-gated"),
            act(9, "assertion", {"finding": fnd("demo-finding-gated-2", GATED_FACT, 12)}),
        ]
        state = project(tuple(acts), self.registry)
        self.assertEqual(self.current_value(state, GATED_FACT), 12)

    def test_L13_refusal_5_family_member_fact(self) -> None:
        """L13 / D2. ADR-0023 routes membership changes through
        member-transition; a retraction would leave a member fact with no
        current answer, which no closure or subtotal consumer expects."""
        acts = self._member_acts() + [retraction(9, "demo-finding-member")]
        with self.assertRaises(FindingModelError) as caught:
            project(tuple(acts), self.registry)
        message = str(caught.exception)
        self.assertIn("is currently a source-family member", message)
        self.assertIn("member-transition removal", message)

    def test_L13_member_transition_removal_of_the_same_fact_is_admitted(self) -> None:
        """The route the refusal names actually works, on the same fact."""
        acts = self._member_acts() + [
            act(
                9,
                "member-transition",
                {
                    "family": FAMILY,
                    "scope": FAMILY_SCOPE,
                    "member": {"action": "remove", "fact_id": MEMBER_FACT},
                    "successor": {"id": "demo-h2", "predecessor": "demo-h1"},
                },
            )
        ]
        state = project(tuple(acts), self.registry)
        view = compute_currency(state)
        self.assertIn(MEMBER_FACT, state.withdrawn_fact_ids)
        self.assertEqual(self.reason_kinds(view, "demo-finding-member"), ["withdrawal"])
        # A withdrawal, not a retraction: the two roots stay distinct.
        self.assertEqual(state.retracted_finding_ids, frozenset())

    def _member_acts(self) -> list[dict[str, Any]]:
        return base_acts() + [
            act(
                7,
                "horizon-genesis",
                {"family": FAMILY, "scope": FAMILY_SCOPE, "horizon_id": "demo-h0"},
            ),
            act(
                8,
                "member-transition",
                {
                    "family": FAMILY,
                    "scope": FAMILY_SCOPE,
                    "member": {
                        "action": "assert",
                        "finding": fnd("demo-finding-member", MEMBER_FACT, 10),
                    },
                    "successor": {"id": "demo-h1", "predecessor": "demo-h0"},
                },
            ),
        ]


class TestAuthorityIsAStateGate(Track0Base):
    """L7: who retracts is recorded and never consulted."""

    def test_L7_a_different_envelope_actor_may_retract_under_free(self) -> None:
        """Boundary: findings.project. Admission runs exactly the predicate
        that would govern this actor *correcting* the fact - the ADR-0041
        state gate - so a second actor is admitted here not because permission
        was granted but because `free` asks no identity question at all."""
        acts = base_acts() + [
            act(7, "assertion", {"finding": fnd(F_450, ATTR_PAT, 450)}),
            retraction(8, F_450, actor="demo-user-b"),
        ]
        state = project(tuple(acts), self.registry)
        self.assertEqual(state.retracted_finding_ids, frozenset({F_450}))
        self.assertIs(self.current_value(state, ATTR_PAT), _NO_CURRENT_VALUE)

    def test_L7_the_actor_changes_nothing_about_the_outcome(self) -> None:
        """The same act under three different actors folds identically, and
        under `locked` all three are refused: the gate is state, not identity."""
        outcomes = set()
        for actor in ("user", "demo-user-b", "demo-user-c"):
            acts = base_acts() + [
                act(7, "assertion", {"finding": fnd(F_450, ATTR_PAT, 450)}),
                retraction(8, F_450, actor=actor),
            ]
            state = project(tuple(acts), self.registry)
            outcomes.add((state.retracted_finding_ids, self.current_value(state, ATTR_PAT)))

            locked_acts = base_acts() + [
                act(7, "assertion", {"finding": fnd("demo-finding-locked", LOCKED_FACT, "a")}),
                retraction(8, "demo-finding-locked", actor=actor),
            ]
            with self.assertRaises(FindingModelError):
                project(tuple(locked_acts), self.registry)
        self.assertEqual(len(outcomes), 1)


class TestEdgeVocabularyUnchanged(Track0Base):
    """Retraction contributes a displacement root, never a third edge kind."""

    def test_declared_edge_kinds_are_untouched(self) -> None:
        from packages.kernel.currency import DECLARED_EDGE_KINDS

        self.assertEqual(DECLARED_EDGE_KINDS, frozenset({"derivation", "individuation"}))

    def test_retraction_reason_kind_is_a_root_not_an_edge(self) -> None:
        from packages.kernel.currency import DECLARED_EDGE_KINDS

        acts = base_acts() + [
            act(7, "assertion", {"finding": fnd(F_450, ATTR_PAT, 450)}),
            retraction(8, F_450),
        ]
        view = compute_currency(project(tuple(acts), self.registry))
        kinds = {reason.kind for reasons in view.reasons.values() for reason in reasons}
        self.assertIn("retraction", kinds)
        self.assertEqual(kinds & DECLARED_EDGE_KINDS, set())


if __name__ == "__main__":
    unittest.main()


# =====================================================================
# Checkpoint T0-B: every reader agrees; neighbors are untouched.
#
# The kernel is unchanged from T0-A. Everything below either asserts an
# agreement, or *measures and records* a disagreement that the Substrate
# unit owns. Nothing under packages/derivation/ or packages/tax/ is
# modified; those modules are imported and called exactly as production
# calls them.
# =====================================================================


class TestL11ReaderAgreement(Track0Base):
    """L11 / D1: after a retraction, every reader agrees there is no
    current answer.

    Boundaries: findings.project, currency.compute_currency,
    findings._current_value_for_fact, findings._current_values_for_fact_type,
    read_models.build_read_model, and derivation.marshal.marshal_run_context
    (the sole production constructor for evaluator input).
    """

    BINDING = [{"symbol": "demo.attr.symbol", "fact_type": {"id": ATTR, "version": "v1"}}]

    def _acts(self) -> list[dict[str, Any]]:
        return base_acts() + [
            act(7, "assertion", {"finding": fnd(F_450, ATTR_PAT, 450)}),
            act(8, "assertion", {"finding": fnd(F_250, ATTR_PAT, 250)}),
            retraction(9, F_250),
        ]

    def _context(self, acts: list[dict[str, Any]]) -> Any:
        from packages.derivation.marshal import marshal_run_context

        state = project(tuple(acts), self.registry)
        return marshal_run_context(
            run_id="demo.run.track0b",
            state=state,
            currency=compute_currency(state),
            rules=[],
            parameters={},
            canon={},
            adoption_pin={"role": "adoption", "id": "demo.package", "version": "v1"},
            governance_pins=[
                {"role": "governance", "id": "governance.constitution", "version": "v1"}
            ],
            input_bindings=self.BINDING,
        )

    def test_L11_all_kernel_readers_and_the_read_model_agree(self) -> None:
        from packages.kernel.read_models import build_read_model

        acts = self._acts()
        state = project(tuple(acts), self.registry)
        view = compute_currency(state)
        model = build_read_model(tuple(acts), self.registry)

        self.assertEqual(view.current_finding_ids, frozenset())
        self.assertIs(self.current_value(state, ATTR_PAT), _NO_CURRENT_VALUE)
        self.assertEqual(_current_values_for_fact_type(state, ATTR), {})
        self.assertEqual(model["current"]["finding_ids"], [])
        self.assertEqual(model["current"]["findings"], {})
        self.assertIsNone(model["facts"][ATTR_PAT]["current_finding_id"])
        # The fact returns to the L0 "unanswered" shape: it is open again,
        # which is the product meaning of a retraction - no answer, not a
        # zero and not an opposite claim.
        self.assertIn(ATTR_PAT, model["open_fact_ids"])
        # History is retained in full, every entry marked non-current.
        self.assertEqual(
            [(e["finding_id"], e["current"]) for e in model["history_by_fact"][ATTR_PAT]],
            [(F_450, False), (F_250, False)],
        )

    def test_L11_marshal_run_context_stops_supplying_the_retracted_answer(self) -> None:
        """marshal_run_context selects from currency.current_finding_ids, so
        it agrees with the full projection without any change of its own."""
        before = self._acts()[:-1]
        self.assertEqual(
            [(i.symbol, i.value, i.finding_id) for i in self._context(before).inputs],
            [("demo.attr.symbol", 250, F_250)],
        )
        self.assertEqual(self._context(self._acts()).inputs, [])

    def test_L11_reassertion_restores_every_reader_together(self) -> None:
        from packages.kernel.read_models import build_read_model

        acts = self._acts() + [
            act(10, "assertion", {"finding": fnd(F_250_AGAIN, ATTR_PAT, 250)})
        ]
        state = project(tuple(acts), self.registry)
        model = build_read_model(tuple(acts), self.registry)
        self.assertEqual(
            compute_currency(state).current_finding_ids, frozenset({F_250_AGAIN})
        )
        self.assertEqual(self.current_value(state, ATTR_PAT), 250)
        self.assertEqual(model["current"]["finding_ids"], [F_250_AGAIN])
        self.assertNotIn(ATTR_PAT, model["open_fact_ids"])
        self.assertEqual(
            [(i.symbol, i.finding_id) for i in self._context(acts).inputs],
            [("demo.attr.symbol", F_250_AGAIN)],
        )


class TestL11MeasuredDisagreements(Track0Base):
    """L11 measurement, now repaired by the Substrate unit (ADR-0073
    Decision 5): the two out-of-kernel readers the plan predicted would
    disagree with the full projection now agree with it. The class name and
    docstring are kept for continuity with the measurement history; each
    test below now asserts the *repaired* verdict and documents, in its own
    docstring, what the prior measured disagreement was and why the new
    verdict is correct - the compatibility-matrix record for both.

    `packages/tax/coverage.py` and `packages/tax/ssa_benefits.py` are
    called exactly as production calls them (the latter via its repaired
    signature).
    """

    # A source-amount fact type that is *not* a source-family member, so a
    # retraction of its answer is admitted (refusal 5 does not apply).
    SOURCE_TYPE = "demo.unconsumed.amount"
    SOURCE_FACT = f"{SOURCE_TYPE}|tax-year=2025"
    SOURCE_BUNDLE = {
        "schema": "bundle.v2",
        "id": "demo.track0b.source",
        "version": "v1",
        "label": "Track 0-B source bundle",
        "fact_types": [
            {
                "schema": "fact-type.v2",
                "id": SOURCE_TYPE,
                "version": "v1",
                "title": "Unconsumed demo amount",
                "nature": "determinable",
                "source_amount": True,
                "quantity": {"id": "demo.quantity.amount", "version": "v1"},
                "identity_keys": LITERAL_YEAR,
                "value_schema": {"type": "number"},
                "supersession": {"policy": "free"},
            }
        ],
    }

    def test_coverage_untranslated_source_findings_agrees(self) -> None:
        """Repair of the measured disagreement (formerly
        ``test_coverage_untranslated_source_findings_disagrees``).

        `packages/tax/coverage.py::untranslated_source_findings` used to
        exclude only `state.withdrawn_fact_ids` with its own hand-rolled
        last-write-wins scan, with no notion of a retracted finding (let
        alone entity or migration supersession), so it kept reporting a
        retracted answer as a current untranslated source finding after
        every kernel reader agreed the fact had no current answer. The
        repair reads `compute_currency(state).current_finding_ids` - the
        single current-standing path (ADR-0073 Decision 5) - instead. No
        signature change was required for existing callers: the new
        `currency` parameter is optional.
        """
        from packages.tax.coverage import untranslated_source_findings

        acts = base_acts() + [
            act(7, "bundle-adoption", {"bundle": self.SOURCE_BUNDLE}),
            act(8, "assertion", {"finding": fnd("demo-finding-src", self.SOURCE_FACT, 42)}),
        ]
        before = project(tuple(acts), self.registry)
        self.assertEqual(
            [(u.finding_id, u.value) for u in untranslated_source_findings(before, [])],
            [("demo-finding-src", 42)],
        )

        after = project(tuple(acts + [retraction(9, "demo-finding-src")]), self.registry)
        # Every kernel reader: no current answer.
        self.assertEqual(compute_currency(after).current_finding_ids, frozenset())
        self.assertIs(self.current_value(after, self.SOURCE_FACT), _NO_CURRENT_VALUE)
        # coverage.py now agrees: the retracted answer is no longer reported.
        self.assertEqual(
            [(u.finding_id, u.value) for u in untranslated_source_findings(after, [])],
            [],
            "repair regression: coverage.untranslated_source_findings still "
            "reads the retracted answer as current",
        )

    def test_ssa_fail_open_is_closed(self) -> None:
        """Repair of the fail-open Track 0 measured (formerly
        ``test_ssa_validate_projected_source_boundary_disagrees``, "MEASURED
        DISAGREEMENT (not repaired)").

        `packages/tax/ssa_benefits.py::validate_projected_source_boundary`
        used to be called in production as
        ``validate_projected_source_boundary(state.findings.values(),
        state.withdrawn_fact_ids)`` (packages/derivation/live.py) - a
        signature with **no channel for retraction, entity supersession, or
        migration supersession at all**. The repair (substrate unit,
        ADR-0073 Decision 5) changed the signature: the second parameter is
        now required and is ``compute_currency(state).current_finding_ids``
        - the single current-standing path every other kernel reader
        already uses - not a withdrawn-fact-id set.

        This test calls the function exactly as the repaired production
        call site does. It fails if the old signature (or the old
        withdrawn-fact-id-only body, called with this same
        ``current_finding_ids`` argument) is restored: a fact-id set and a
        finding-id set never collide as strings, so an old body checking
        ``fact_id in withdrawn`` against a finding-id argument would find
        no match, exclude nothing, and wrongly accept the retracted case
        below.
        """
        from packages.kernel.facts import fact_id_for
        from packages.tax.loader import TAX_CONTENT_DIR, tax_registry
        from packages.tax.ssa_benefits import (
            SsaBenefitsError,
            validate_projected_source_boundary,
        )

        registry = tax_registry()
        content = Path(TAX_CONTENT_DIR)
        ssa_bundle = json.loads((content / "ssa1099.bundle.v2.json").read_text("utf-8"))
        filing_bundle = next(
            json.loads(path.read_text("utf-8"))
            for path in sorted(content.glob("*.json"))
            if (lambda d: isinstance(d, dict)
                and str(d.get("schema", "")).startswith("bundle")
                and any(ft["id"] == "tax.us.2025.filing-status" for ft in d.get("fact_types", [])))(
                    json.loads(path.read_text("utf-8")))
        )
        statement = "demo-ssa-statement-4"
        suffix = f"statement={statement},tax-year=2025"

        def ssa(finding_id: str, box: str, value: Any) -> dict[str, Any]:
            return {"schema": "finding.v1", "id": finding_id,
                    "fact_id": f"tax.us.2025.ssa1099.{box}|{suffix}",
                    "value": value, "basis": "attested", "evidence_ids": []}

        family = {"id": "tax.us.2025.ssa1099.benefits", "version": "v1"}
        scope = {"tax-year": "2025"}
        filing_fact = fact_id_for("tax.us.2025.filing-status", (("tax-year", "2025"),))
        acts = [
            act(0, "bundle-adoption", {"bundle": ssa_bundle}),
            act(1, "bundle-adoption", {"bundle": filing_bundle}),
            act(2, "entity-introduced", {"entity": {
                "schema": "entity.v1", "id": statement,
                "kind": "tax.us.ssa1099-statement", "label": "Demo SSA statement"}}),
            act(3, "assertion", {"finding": {
                "schema": "finding.v1", "id": "demo-filing-status",
                "fact_id": filing_fact, "value": "married_filing_jointly",
                "basis": "attested", "evidence_ids": []}}),
            act(4, "assertion", {"finding": ssa("demo-ssa4-b3", "box3-benefits-paid", 1000)}),
            act(5, "assertion", {"finding": ssa("demo-ssa4-b4", "box4-repayment", 0)}),
            act(6, "assertion", {"finding": ssa("demo-ssa4-b6", "box6-withholding", 0)}),
            act(7, "assertion", {"finding": ssa("demo-ssa4-recip", "recipient", "spouse")}),
            act(8, "assertion", {"finding": ssa("demo-ssa4-kind", "statement-kind", "ssa-1099")}),
            act(9, "assertion", {"finding": ssa("demo-ssa4-lump", "lump-sum-election", False)}),
            act(10, "horizon-genesis", {"family": family, "scope": scope, "horizon_id": "demo-ssa4-h0"}),
            act(11, "member-transition", {
                "family": family, "scope": scope,
                "member": {"action": "assert", "finding": ssa("demo-ssa4-b5", "box5-net-benefits", 1000)},
                "successor": {"id": "demo-ssa4-h1", "predecessor": "demo-ssa4-h0"}}),
        ]

        def verdict(sequence: list[dict[str, Any]]) -> str:
            state = project(tuple(sequence), registry)
            currency = compute_currency(state)
            try:
                validate_projected_source_boundary(
                    state.findings.values(), currency.current_finding_ids
                )
            except SsaBenefitsError:
                return "refuses"
            return "accepts"

        self.assertEqual(verdict(acts), "accepts")

        # The T0-B path is refused by the sixth refusal, so it cannot reach
        # this boundary at all. Asserted, not assumed.
        with self.assertRaises(FindingModelError):
            project(tuple(acts + [retraction(12, "demo-ssa4-b4")]), registry)

        # The surviving path: filing status participates in no declared
        # relation, so retracting it is admitted.
        retracted = acts + [retraction(12, "demo-filing-status")]
        state = project(tuple(retracted), registry)
        self.assertEqual(state.retracted_finding_ids, frozenset({"demo-filing-status"}))
        self.assertIs(_current_value_for_fact(state, filing_fact), _NO_CURRENT_VALUE)
        self.assertEqual(
            verdict(retracted),
            "refuses",
            "fail-open regression: production admits a spouse-recipient SSA "
            "statement whose married-filing-jointly authority was retracted",
        )

    def test_measured_scope_of_the_source_amount_exposure(self) -> None:
        """How much of the production corpus the disagreement can reach.

        Refusal 5 fences every `source_amount` fact type that is also a
        source-family member predicate, so the disagreement is only
        reachable through the ones that are not. This test records the
        exact set so a future content change that widens it is visible.
        """
        from packages.tax.loader import TAX_CONTENT_DIR, tax_registry

        registry = tax_registry()
        source_amount_types: set[str] = set()
        for path in sorted(Path(TAX_CONTENT_DIR).glob("*.json")):
            try:
                document = json.loads(path.read_text("utf-8"))
            except json.JSONDecodeError:
                continue
            if not isinstance(document, dict) or "fact_types" not in document:
                continue
            for fact_type in document["fact_types"]:
                if fact_type.get("source_amount") is True:
                    source_amount_types.add(fact_type["id"])

        unfenced = source_amount_types - registry.family_member_predicates
        self.assertEqual(
            sorted(unfenced),
            [
                "tax.us.2025.f1099int.box11-bond-premium",
                "tax.us.2025.f1099r.ira-box2a-taxable-amount",
                "tax.us.2025.interest.accrued-interest-migrated.presented-claim",
                "tax.us.2025.interest.current-year-adjustment.pairing-scoped",
                "tax.us.2025.ssa1099.box3-benefits-paid",
                "tax.us.2025.ssa1099.box3-workers-comp",
                "tax.us.2025.ssa1099.box4-repayment",
            ],
        )
        self.assertTrue(source_amount_types & registry.family_member_predicates)


class TestL10DerivationDependency(unittest.TestCase):
    """L10 / D4: a derived result pinned on the retracted answer.

    Boundary: derivation.projection.workspace_currency over the combined
    kernel + derivation registry (derivation.loader.workspace_registry),
    with real `derived-publication` acts. Nothing under
    packages/derivation/ is modified - D4 needed no change there, which
    was one of the charter's stop conditions.
    """

    SYMBOL = "demo.attr.total"

    def setUp(self) -> None:
        from packages.derivation.loader import workspace_registry

        self.registry = workspace_registry()

    def _derived(self, index: int, derived_id: str, pinned: str, value: Any) -> dict[str, Any]:
        return act(index, "derived-publication", {
            "run_id": "demo.run.track0b",
            "finding": {
                "schema": "derived-finding.v1",
                "id": derived_id,
                "symbol": self.SYMBOL,
                "value": str(value),
                "version": "v1",
                "pins": [
                    {"role": "adoption", "id": "demo.package", "version": "v1"},
                    {"role": "governance", "id": "governance.constitution", "version": "v1"},
                    {"role": "input", "id": pinned, "version": "v1"},
                ],
            },
        })

    def _base(self) -> list[dict[str, Any]]:
        return base_acts() + [
            act(7, "assertion", {"finding": fnd(F_450, ATTR_PAT, 450)}),
            act(8, "assertion", {"finding": fnd(F_250, ATTR_PAT, 250)}),
            self._derived(9, "demo-derived-001", F_250, 250),
        ]

    def test_L10_derived_finding_is_current_before_the_retraction(self) -> None:
        from packages.derivation.projection import workspace_currency

        _, derivation = workspace_currency(tuple(self._base()), self.registry)
        self.assertEqual(derivation.current_derived_ids, frozenset({"demo-derived-001"}))
        self.assertEqual(derivation.displaced_derived_ids, frozenset())

    def test_L10_retraction_displaces_the_derived_finding(self) -> None:
        from packages.derivation.projection import workspace_currency

        acts = self._base() + [retraction(10, F_250)]
        kernel, derivation = workspace_currency(tuple(acts), self.registry)
        self.assertEqual(derivation.displaced_derived_ids, frozenset({"demo-derived-001"}))
        self.assertEqual(derivation.current_derived_ids, frozenset())

        # The retraction root is in the closure, and it is named on the
        # *kernel* finding. The derived finding's own reason names the
        # derivation edge it was displaced along, never the root kind -
        # `displacement_closure` always labels a dependent with the edge
        # kind, so no root kind (retraction, correction, withdrawal,
        # supersession) can ever appear directly on a derived finding.
        # The two compose: derived -> F_250 -> retraction -> act id.
        self.assertEqual(
            [(r.kind, r.by) for r in derivation.reasons["demo-derived-001"]],
            [("derivation", F_250)],
        )
        self.assertEqual(
            [(r.kind, r.by) for r in kernel.reasons[F_250]],
            [("retraction", acts[10]["act_id"])],
        )
        self.assertIn(F_250, kernel.displaced_finding_ids)

    def test_L10_reassertion_produces_a_new_derived_id_and_no_revival(self) -> None:
        from packages.derivation.projection import workspace_currency

        acts = self._base() + [
            retraction(10, F_250),
            act(11, "assertion", {"finding": fnd(F_250_AGAIN, ATTR_PAT, 250)}),
            self._derived(12, "demo-derived-002", F_250_AGAIN, 250),
        ]
        _, derivation = workspace_currency(tuple(acts), self.registry)
        # A fresh derived finding, not a revived one; the old id stays
        # displaced even though the reasserted value is identical.
        self.assertEqual(derivation.current_derived_ids, frozenset({"demo-derived-002"}))
        self.assertEqual(derivation.displaced_derived_ids, frozenset({"demo-derived-001"}))

    def test_L10_kernel_projection_ignores_derived_publication_acts(self) -> None:
        """ADR-0010 compose-over holds with the new act kind present."""
        acts = self._base() + [retraction(10, F_250)]
        state = project(tuple(acts), self.registry)
        self.assertNotIn("demo-derived-001", state.findings)
        self.assertEqual(state.retracted_finding_ids, frozenset({F_250}))


class TestL12EvidenceStanding(Track0Base):
    """L12: evidence standing and assertion standing are separate lifecycles.

    Boundary: findings.project, currency.compute_currency,
    read_models.build_read_model.
    """

    DOC_ID = "demo-finding-documentary"

    def _acts(self, *, with_retraction: bool) -> list[dict[str, Any]]:
        documentary = demo_finding(
            finding_id=self.DOC_ID, fact_id=ATTR_KIM, value=5,
            basis="documentary", evidence_ids=["demo-evidence-001"],
        )
        acts = base_acts() + [
            act(7, "assertion", {"finding": fnd(F_450, ATTR_PAT, 450)}),
            act(8, "assertion", {"finding": documentary}),
            act(9, "evidence-replaced", {"evidence_id": "demo-evidence-001"}),
        ]
        return acts + [retraction(10, F_450)] if with_retraction else acts

    def test_L12_withdrawn_evidence_leaves_the_documentary_finding_current(self) -> None:
        from packages.kernel.read_models import build_read_model

        acts = self._acts(with_retraction=True)
        state = project(tuple(acts), self.registry)
        view = compute_currency(state)
        model = build_read_model(tuple(acts), self.registry)

        self.assertIn(self.DOC_ID, view.current_finding_ids)
        self.assertEqual(self.reason_kinds(view, self.DOC_ID), [])
        self.assertEqual(
            model["current"]["findings"][self.DOC_ID]["evidence"][0]["status"], "withdrawn"
        )
        # Evidence withdrawal is not a displacement root; only the
        # separately retracted finding carries a retraction reason.
        self.assertEqual(self.reason_kinds(view, F_450), ["retraction"])

    def test_L12_a_retraction_changes_no_evidence_currency(self) -> None:
        without = compute_currency(project(tuple(self._acts(with_retraction=False)), self.registry))
        with_it = compute_currency(project(tuple(self._acts(with_retraction=True)), self.registry))
        self.assertEqual(without.current_evidence_ids, with_it.current_evidence_ids)
        self.assertEqual(without.displaced_evidence_ids, with_it.displaced_evidence_ids)
        self.assertEqual(with_it.displaced_evidence_ids, frozenset({"demo-evidence-001"}))


class TestL8L9Neighbors(Track0Base):
    """L8 and L9: entity retirement and an unrelated member transition,
    with a retraction act present in the log.

    Boundary: findings.project, currency.compute_currency.
    """

    def test_L8_entity_retirement_still_displaces_by_individuation(self) -> None:
        acts = base_acts() + [
            act(7, "assertion", {"finding": fnd(F_450, ATTR_PAT, 450)}),
            act(8, "assertion", {"finding": fnd(F_KIM, ATTR_KIM, 100)}),
            retraction(9, F_450),
            act(10, "entity-superseded", {"entity_id": "demo-kim"}),
        ]
        view = compute_currency(project(tuple(acts), self.registry))
        # Exactly as the P2 probe recorded: entity retirement displaces by
        # individuation, and the retraction root stays a separate reason on
        # a separate finding. The two lifecycles do not merge.
        self.assertEqual(self.reason_kinds(view, F_KIM), ["individuation"])
        self.assertEqual(self.reason_kinds(view, F_450), ["retraction"])
        self.assertEqual(view.current_finding_ids, frozenset())

    def test_L9_an_unrelated_member_transition_is_unaffected(self) -> None:
        acts = base_acts() + [
            act(7, "horizon-genesis", {"family": FAMILY, "scope": FAMILY_SCOPE, "horizon_id": "demo-h0"}),
            act(8, "member-transition", {
                "family": FAMILY, "scope": FAMILY_SCOPE,
                "member": {"action": "assert", "finding": fnd("demo-finding-member", MEMBER_FACT, 10)},
                "successor": {"id": "demo-h1", "predecessor": "demo-h0"}}),
            act(9, "assertion", {"finding": fnd(F_450, ATTR_PAT, 450)}),
            retraction(10, F_450),
        ]
        state = project(tuple(acts), self.registry)
        view = compute_currency(state)
        self.assertIn("demo-finding-member", view.current_finding_ids)
        self.assertEqual(self.current_value(state, MEMBER_FACT), 10)
        # No horizon advanced and no fact was withdrawn: retracting an
        # unrelated finding never moves a family.
        self.assertEqual(
            state.horizon_state.current_by_chain,
            {("demo.w2", "v1", (("tax-year", "2025"),)): "demo-h1"},
        )
        self.assertEqual(state.withdrawn_fact_ids, frozenset())


class TestD6AuthorizationFold(unittest.TestCase):
    """D6: standing authorization is untouched by a retraction.

    Boundary: derivation.authorization.project / resolve, on an existing
    grant fixture extended by appending the retraction act. The fold is
    not modified: ADR-0010 compose-over means it simply does not own the
    `finding-retracted` kind, which is why the two states are equal.
    """

    GRANT = {
        "kind": "calculation-authorization",
        "payload": {"authorization": {
            "schema": "workspace-calculation-authorization.v1",
            "id": "demo-grant-1",
            "subject_id": "demo-subject-1",
            "tax_year": "2025",
            "universe_id": "demo-universe-1",
        }},
    }

    def test_D6_resolved_status_is_identical_before_and_after(self) -> None:
        from packages.derivation import authorization

        retract = {"kind": RETRACTION_KIND, "payload": {"finding_id": F_250}}
        before = authorization.project([self.GRANT])
        after = authorization.project([self.GRANT, retract])
        self.assertEqual(before, after)

        args = ("demo-subject-1", "2025", "demo-universe-1")
        resolved_before = authorization.resolve(before, *args)
        resolved_after = authorization.resolve(after, *args)
        self.assertEqual(resolved_before.status, authorization.STATUS_ADMITTED)
        self.assertEqual(
            (resolved_before.status, resolved_before.grant_id, resolved_before.detail),
            (resolved_after.status, resolved_after.grant_id, resolved_after.detail),
        )

    def test_D6_the_fold_does_not_own_the_retraction_kind(self) -> None:
        from packages.derivation import authorization

        self.assertNotIn(RETRACTION_KIND, authorization._APPLIERS)


class TestRealContentF1098Control(unittest.TestCase):
    """The real-content control: `tax.us.2025.f1098.liable-and-paid`.

    Read first, before choosing it: it is declared `fact-type.v2` with
    supersession policy `free`; it is **not** a source-family member
    predicate (the f1098 family's member predicate is
    `box1-mortgage-interest`); it is **not** a subset-invariant
    participant (the only declared pair is 1099-DIV box 1b / box 1a); and
    it appears in neither `domain_companion_presence_pairs` nor
    `domain_companion_equality_pairs`, as a subordinate or as a companion.
    So none of the five refusals fences it and it is genuinely retractable
    - which is what makes it a usable control rather than a case that
    refuses for an uninteresting reason.

    Boundary: findings.project over the real `tax_registry()` and the
    committed f1098 bundle, plus every L11 reader. Entity ids and the
    answer are synthetic; the fact type and bundle are production content.
    """

    FACT_TYPE = "tax.us.2025.f1098.liable-and-paid"
    PAYER = "demo-lender-1"
    STATEMENT = "demo-1098-statement-1"

    def setUp(self) -> None:
        from packages.kernel.facts import fact_id_for
        from packages.tax.loader import TAX_CONTENT_DIR, tax_registry

        self.registry = tax_registry()
        self.bundle = json.loads(
            (Path(TAX_CONTENT_DIR) / "f1098.bundle.json").read_text("utf-8")
        )
        self.fact_id = fact_id_for(
            self.FACT_TYPE,
            (("payer", self.PAYER), ("statement", self.STATEMENT), ("tax-year", "2025")),
        )

    def test_the_control_is_unfenced_by_all_five_refusals(self) -> None:
        """The companion / subset / family reading, asserted rather than
        described, so a content change that fences this fact type shows up
        here as a failed premise instead of a silently weaker control."""
        from packages.tax.loader import (
            domain_companion_equality_pairs,
            domain_companion_presence_pairs,
        )

        self.assertNotIn(self.FACT_TYPE, self.registry.family_member_predicates)
        self.assertNotIn(self.FACT_TYPE, self.registry.subset_invariant_pairs)
        self.assertNotIn(self.FACT_TYPE, self.registry.subset_invariant_pairs.values())
        presence = domain_companion_presence_pairs()
        self.assertNotIn(self.FACT_TYPE, presence)
        for companions in presence.values():
            listed = [companions] if isinstance(companions, str) else companions
            self.assertNotIn(self.FACT_TYPE, listed)
        equality = domain_companion_equality_pairs()
        self.assertNotIn(self.FACT_TYPE, equality)
        self.assertNotIn(self.FACT_TYPE, equality.values())
        declared = next(
            ft for ft in self.bundle["fact_types"] if ft["id"] == self.FACT_TYPE
        )
        self.assertEqual(declared["supersession"], {"policy": "free"})

    def _finding(self, finding_id: str, value: str) -> dict[str, Any]:
        return {
            "schema": "finding.v1",
            "id": finding_id,
            "fact_id": self.fact_id,
            "value": value,
            "basis": "attested",
            "evidence_ids": [],
        }

    def _acts(self) -> list[dict[str, Any]]:
        def entity(index: int, entity_id: str, kind: str, label: str) -> dict[str, Any]:
            return act(index, "entity-introduced", {"entity": {
                "schema": "entity.v1", "id": entity_id, "kind": kind, "label": label}})

        return [
            act(0, "bundle-adoption", {"bundle": self.bundle}),
            entity(1, self.PAYER, "tax.us.mortgage-lender", "Demo lender"),
            entity(2, self.STATEMENT, "tax.us.1098-statement", "Demo 1098 statement"),
            act(3, "assertion", {"finding": self._finding("demo-f1098-yes", "yes")}),      # L1
            act(4, "assertion", {"finding": self._finding("demo-f1098-no", "no")}),        # L2
            retraction(5, "demo-f1098-no"),                                               # L3
            act(6, "assertion", {"finding": self._finding("demo-f1098-yes-again", "yes")}),# L4
        ]

    def _readers(self, count: int) -> dict[str, Any]:
        """Every L11 reader at one point in the sequence."""
        from packages.derivation.marshal import marshal_run_context
        from packages.kernel.read_models import build_read_model

        acts = tuple(self._acts()[:count])
        state = project(acts, self.registry)
        currency = compute_currency(state)
        model = build_read_model(acts, self.registry)
        context = marshal_run_context(
            run_id="demo.run.f1098", state=state, currency=currency,
            rules=[], parameters={}, canon={},
            adoption_pin={"role": "adoption", "id": "demo.package", "version": "v1"},
            governance_pins=[{"role": "governance", "id": "governance.constitution", "version": "v1"}],
            input_bindings=[{"symbol": self.FACT_TYPE,
                             "fact_type": {"id": self.FACT_TYPE, "version": "v1"}}],
        )
        value = _current_value_for_fact(state, self.fact_id)
        return {
            "state": state,
            "currency": sorted(currency.current_finding_ids),
            "current_value": None if value is _NO_CURRENT_VALUE else value,
            "by_type": _current_values_for_fact_type(state, self.FACT_TYPE),
            "read_model_current": model["current"]["finding_ids"],
            "read_model_pointer": model["facts"][self.fact_id]["current_finding_id"],
            "open": self.fact_id in model["open_fact_ids"],
            "history": [(e["finding_id"], e["current"]) for e in model["history_by_fact"][self.fact_id]],
            "marshalled": [(i.symbol, i.value, i.finding_id) for i in context.inputs],
        }

    def test_L1_L4_and_L11_on_real_content(self) -> None:
        expected = {
            4: ("demo-f1098-yes", "yes", False),
            5: ("demo-f1098-no", "no", False),
            6: (None, None, True),            # L3: retracted, fact reopens
            7: ("demo-f1098-yes-again", "yes", False),
        }
        for count, (finding_id, value, is_open) in expected.items():
            with self.subTest(after_acts=count):
                r = self._readers(count)
                self.assertEqual(r["currency"], [finding_id] if finding_id else [])
                self.assertEqual(r["current_value"], value)
                self.assertEqual(r["by_type"], {self.fact_id: value} if value else {})
                self.assertEqual(r["read_model_current"], [finding_id] if finding_id else [])
                self.assertEqual(r["read_model_pointer"], finding_id)
                self.assertEqual(r["open"], is_open)
                self.assertEqual(
                    r["marshalled"],
                    [(self.FACT_TYPE, value, finding_id)] if finding_id else [],
                )

    def test_real_content_history_and_composed_reasons_survive(self) -> None:
        r = self._readers(7)
        self.assertEqual(
            r["history"],
            [("demo-f1098-yes", False), ("demo-f1098-no", False), ("demo-f1098-yes-again", True)],
        )
        reasons = compute_currency(r["state"]).reasons["demo-f1098-no"]
        self.assertEqual(
            {reason.kind for reason in reasons}, {"retraction", "correction"}
        )

    def test_no_real_content_invariant_reads_the_retracted_answer(self) -> None:
        """Reported, not repaired: on this control every reader agrees, so
        there is no invariant here that needs a repair. The disagreements
        this milestone must still fix live on `source_amount` fact types
        (see TestL11MeasuredDisagreements), not on this taxpayer-authority
        declaration."""
        r = self._readers(6)
        self.assertIsNone(r["current_value"])
        self.assertEqual(r["currency"], [])
        self.assertEqual(r["marshalled"], [])
        self.assertTrue(r["open"])


class TestRetractionRespectsAdmissionInvariants(Track0Base):
    """T0-C: the sixth refusal. Post-repair form of the T0-B wedge finding.

    `apply_assertion` runs four admission enforcers after recording a
    finding: subset invariants, declaration/signal contradictions,
    companion presence, and companion equality.
    `apply_finding_retracted` now runs the identical four over the
    *prospective* post-retraction state and refuses on violation.

    The argument is consistency with an accepted contract, not a new
    product choice: the kernel already decides that a declared companion
    may not be left unanswered, so an act that ends an answer must land
    inside the same admissible-state set as an act that supplies one.
    The wedge the T0-B version of this test demonstrated is now
    unreachable.
    """

    def _ssa_fixture(self, statement: str) -> tuple[Any, list[dict[str, Any]], str]:
        from packages.tax.loader import TAX_CONTENT_DIR, tax_registry

        registry = tax_registry()
        bundle = json.loads(
            (Path(TAX_CONTENT_DIR) / "ssa1099.bundle.v2.json").read_text("utf-8")
        )
        suffix = f"statement={statement},tax-year=2025"

        def ssa(finding_id: str, box: str, value: Any) -> dict[str, Any]:
            return {"schema": "finding.v1", "id": finding_id,
                    "fact_id": f"tax.us.2025.ssa1099.{box}|{suffix}",
                    "value": value, "basis": "attested", "evidence_ids": []}

        family = {"id": "tax.us.2025.ssa1099.benefits", "version": "v1"}
        scope = {"tax-year": "2025"}
        acts = [
            act(0, "bundle-adoption", {"bundle": bundle}),
            act(1, "entity-introduced", {"entity": {
                "schema": "entity.v1", "id": statement,
                "kind": "tax.us.ssa1099-statement", "label": "Demo SSA statement"}}),
            act(2, "assertion", {"finding": ssa("demo-ssa2-b3", "box3-benefits-paid", 1000)}),
            act(3, "assertion", {"finding": ssa("demo-ssa2-b4", "box4-repayment", 0)}),
            act(4, "assertion", {"finding": ssa("demo-ssa2-b6", "box6-withholding", 0)}),
            act(5, "assertion", {"finding": ssa("demo-ssa2-recip", "recipient", "taxpayer")}),
            act(6, "assertion", {"finding": ssa("demo-ssa2-kind", "statement-kind", "ssa-1099")}),
            act(7, "assertion", {"finding": ssa("demo-ssa2-lump", "lump-sum-election", False)}),
            act(8, "horizon-genesis", {"family": family, "scope": scope, "horizon_id": "demo-ssa2-h0"}),
            act(9, "member-transition", {
                "family": family, "scope": scope,
                "member": {"action": "assert", "finding": ssa("demo-ssa2-b5", "box5-net-benefits", 1000)},
                "successor": {"id": "demo-ssa2-h1", "predecessor": "demo-ssa2-h0"}}),
        ]
        return registry, acts, suffix

    def test_retracting_a_declared_companion_is_now_refused(self) -> None:
        """The exact sequence that wedged the statement in T0-B. It is now
        refused at admission, and the refusal names the violated invariant
        by carrying the enforcer's own message through."""
        registry, acts, _ = self._ssa_fixture("demo-ssa-statement-2")
        with self.assertRaises(FindingModelError) as caught:
            project(tuple(acts + [retraction(10, "demo-ssa2-b4")]), registry)
        message = str(caught.exception)
        self.assertIn("cannot retract finding demo-ssa2-b4", message)
        self.assertIn("no assertion could create", message)
        self.assertIn("companion presence violated", message)

    def test_the_wedge_is_unreachable(self) -> None:
        """Nothing is recorded by a refused act, so the statement that T0-B
        wedged is untouched: box 4 keeps its answer and the next assertion
        touching the statement is admitted."""
        registry, acts, suffix = self._ssa_fixture("demo-ssa-statement-3")
        state = project(tuple(acts), registry)
        self.assertEqual(state.retracted_finding_ids, frozenset())
        self.assertEqual(
            _current_value_for_fact(state, f"tax.us.2025.ssa1099.box4-repayment|{suffix}"), 0
        )
        corrected = project(tuple(acts + [act(10, "assertion", {"finding": {
            "schema": "finding.v1", "id": "demo-ssa3-b3-corrected",
            "fact_id": f"tax.us.2025.ssa1099.box3-benefits-paid|{suffix}",
            "value": 1000, "basis": "attested", "evidence_ids": []}})]), registry)
        self.assertEqual(
            _current_value_for_fact(corrected, f"tax.us.2025.ssa1099.box3-benefits-paid|{suffix}"), 1000
        )

    def test_both_appliers_run_the_same_four_enforcers(self) -> None:
        """The contrast that makes the repair precise, inverted from its
        T0-B form: the four enforcers are now required in *both* appliers.
        Retraction reuses them; it does not restate their predicates."""
        import inspect

        from packages.kernel import findings as findings_module

        assertion_source = inspect.getsource(findings_module.apply_assertion)
        retraction_source = inspect.getsource(
            findings_module._refuse_retraction_violating_admission_invariants
        )
        enforcers = (
            "_enforce_subset_invariants",
            "_enforce_declaration_signal_contradictions",
            "_enforce_companion_presence",
            "_enforce_companion_equalities",
        )
        for enforcer in enforcers:
            self.assertIn(enforcer, assertion_source)
        # The retraction path names the enforcers through one shared tuple
        # rather than four inline calls, so the tuple is what must contain
        # them - a reimplemented predicate would show up as a body of its
        # own here instead.
        self.assertEqual(
            tuple(f.__name__ for f in findings_module._ADMISSION_ENFORCERS), enforcers
        )
        self.assertIn("_ADMISSION_ENFORCERS", retraction_source)
        self.assertNotIn("companion presence violated", retraction_source)
        self.assertNotIn("subset invariant violated", retraction_source)

    def test_an_admitted_retraction_always_lands_in_the_admissible_set(self) -> None:
        """Deliverable 4, stated as the property rather than a case list:
        every retraction the kernel admits leaves a state that satisfies all
        four enforcers on the touched fact - which is exactly the set of
        states an assertion can also reach."""
        from packages.kernel import findings as findings_module

        acts = base_acts() + [
            act(7, "assertion", {"finding": fnd(F_450, ATTR_PAT, 450)}),
            act(8, "assertion", {"finding": fnd(F_250, ATTR_PAT, 250)}),
            retraction(9, F_250),
        ]
        state = project(tuple(acts), self.registry)
        self.assertEqual(state.retracted_finding_ids, frozenset({F_250}))
        for enforce in findings_module._ADMISSION_ENFORCERS:
            enforce(state, self.registry, (ATTR_PAT,))  # must not raise


# ---------------------------------------------------------------------
# T0-C deliverable 3: the ordered-path question, by execution, on real
# committed 2025 content.
# ---------------------------------------------------------------------

# The eight declared relations, with the source family each member fact
# type belongs to. Every participant is read from the production registry;
# nothing here invents a relation.
_RELATION_GROUPS: tuple[tuple[str, tuple[str, ...], str], ...] = (
    ("companion-presence f1098e box1/box2",
     ("tax.us.2025.f1098e.box1-student-loan-interest",
      "tax.us.2025.f1098e.box2-checked-authority"),
     "tax.us.2025.f1098e.1"),
    ("companion-presence f1099div box12/box13",
     ("tax.us.2025.f1099div.box12-exempt-interest-dividends",
      "tax.us.2025.f1099div.box13-specified-pab-authority"),
     "tax.us.2025.f1099div.box12"),
    ("companion-presence f1099div box7/box8+box1a",
     ("tax.us.2025.f1099div.box7-foreign-tax-paid",
      "tax.us.2025.f1099div.box8-country-companion",
      "tax.us.2025.f1099div.box1a-ordinary"),
     "tax.us.2025.f1099div.box7"),
    ("companion-presence f1099g box1/box4",
     ("tax.us.2025.f1099g.box1-unemployment",
      "tax.us.2025.f1099g.box4-federal-withholding-authority"),
     "tax.us.2025.f1099g.box1"),
    ("companion-presence f1099int box8/box9",
     ("tax.us.2025.f1099int.box8-tax-exempt-interest",
      "tax.us.2025.f1099int.box9-specified-pab-authority"),
     "tax.us.2025.f1099int.box8"),
    ("companion-presence + equality f1099r IRA",
     ("tax.us.2025.f1099r.ira-box1-taxable-distribution",
      "tax.us.2025.f1099r.ira-box2a-taxable-amount",
      "tax.us.2025.f1099r.ira-sep-simple-checkbox",
      "tax.us.2025.f1099r.distribution-code",
      "tax.us.2025.f1099r.box2b-not-determined"),
     "tax.us.2025.f1099r.ira"),
    ("companion-presence ssa1099 box5/six witnesses",
     ("tax.us.2025.ssa1099.box5-net-benefits",
      "tax.us.2025.ssa1099.box3-benefits-paid",
      "tax.us.2025.ssa1099.box4-repayment",
      "tax.us.2025.ssa1099.box6-withholding",
      "tax.us.2025.ssa1099.recipient",
      "tax.us.2025.ssa1099.statement-kind",
      "tax.us.2025.ssa1099.lump-sum-election"),
     "tax.us.2025.ssa1099.benefits"),
    ("subset f1099div box1b <= box1a",
     ("tax.us.2025.f1099div.box1b-qualified",
      "tax.us.2025.f1099div.box1a-ordinary"),
     "tax.us.2025.f1099div"),
)


class TestOrderedRetractabilityOnRealContent(unittest.TestCase):
    """T0-C deliverable 3. For every declared subset, companion-presence
    and companion-equality relation on committed 2025 content, determine by
    execution which facts are retractable directly, which only after
    retracting a dependent first, and which are not retractable by any
    order at all.

    Fixtures are generated from the committed content itself - value
    domains, identity keys and family membership are all read from
    `tax_registry()` - so a content change reshapes the fixtures rather
    than silently invalidating a hand-written one.

    Boundary throughout: `findings.project` over the real `tax_registry()`.
    """

    registry: Any
    fact_types: dict[str, dict[str, Any]]
    bundle_of: dict[str, dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        from packages.tax.loader import TAX_CONTENT_DIR, tax_registry

        cls.registry = tax_registry()
        cls.fact_types = {}
        cls.bundle_of = {}
        for path in sorted(Path(TAX_CONTENT_DIR).glob("*.json")):
            try:
                document = json.loads(path.read_text("utf-8"))
            except json.JSONDecodeError:
                continue
            if not isinstance(document, dict):
                continue
            if not str(document.get("schema", "")).startswith("bundle"):
                continue
            for fact_type in document.get("fact_types", []):
                cls.fact_types[fact_type["id"]] = fact_type
                cls.bundle_of[fact_type["id"]] = document

    # -------------------------------------------------- fixture generation
    @staticmethod
    def _same(a: Any, b: Any) -> bool:
        """Type-aware equality so `False` never matches `0`."""
        if isinstance(a, bool) != isinstance(b, bool):
            return False
        return bool(a == b)

    def _candidate_values(self, type_id: str) -> list[Any]:
        schema = self.fact_types[type_id]["value_schema"]
        if "const" in schema:
            return [schema["const"]]
        if "enum" in schema:
            return list(schema["enum"])
        declared = schema.get("type")
        types = declared if isinstance(declared, list) else [declared]
        out: list[Any] = []
        if "number" in types or "integer" in types:
            out.append(0)
        if "boolean" in types:
            out += [False, True]
        if "string" in types:
            out.append("2025-01-01" if schema.get("format") == "date" else "US")
        if "null" in types:
            out.append(None)
        return out or [0]

    def _value_for(self, type_id: str) -> Any:
        candidates = self._candidate_values(type_id)
        domain = getattr(self.registry, "companion_value_domains", {}).get(type_id)
        if domain:
            allowed = [c for c in candidates if any(self._same(c, d) for d in domain)]
            candidates = allowed or sorted(domain, key=repr)
        return candidates[0]

    def _build(self, type_ids: tuple[str, ...], family_id: str) -> tuple[
        list[dict[str, Any]], dict[str, str], dict[str, str], int
    ]:
        """A workspace in which every named fact type has a current answer.

        Member fact types are admitted through horizon-genesis plus
        member-transition (a plain assertion would be refused by ADR-0023
        routing); companions and subset dominants are asserted *before*
        their subordinates, or the enforcers would reject the fixture
        itself.
        """
        from packages.kernel.facts import fact_id_for

        documents: list[dict[str, Any]] = []
        for type_id in type_ids:
            document = self.bundle_of[type_id]
            if not any(d is document for d in documents):
                documents.append(document)

        entity_kinds = {
            key["entity_kind"]
            for type_id in type_ids
            for key in self.fact_types[type_id]["identity_keys"]
            if key["kind"] == "entity"
        }
        entity_ids = {kind: "demo-" + kind.replace(".", "-") + "-1" for kind in entity_kinds}

        acts: list[dict[str, Any]] = []
        index = 0
        for document in documents:
            acts.append(act(index, "bundle-adoption", {"bundle": document}))
            index += 1
        for kind, entity_id in sorted(entity_ids.items()):
            acts.append(act(index, "entity-introduced", {"entity": {
                "schema": "entity.v1", "id": entity_id, "kind": kind,
                "label": f"Demo {kind}"}}))
            index += 1

        subordinates = set(self.registry.companion_presence_pairs) | set(
            self.registry.subset_invariant_pairs
        )
        ordered = sorted(type_ids, key=lambda t: (1 if t in subordinates else 0, t))
        members = [t for t in ordered if t in self.registry.family_member_predicates]
        plain = [t for t in ordered if t not in self.registry.family_member_predicates]

        finding_ids: dict[str, str] = {}
        fact_ids: dict[str, str] = {}

        def finding(type_id: str) -> dict[str, Any]:
            keys = tuple(
                (key["name"], entity_ids[key["entity_kind"]]) if key["kind"] == "entity"
                else (key["name"], str(key["values"][0]))
                for key in self.fact_types[type_id]["identity_keys"]
            )
            finding_id = "demo-f-" + type_id.split(".")[-1]
            finding_ids[type_id] = finding_id
            fact_ids[type_id] = fact_id_for(type_id, keys)
            return {"schema": "finding.v1", "id": finding_id,
                    "fact_id": fact_ids[type_id], "value": self._value_for(type_id),
                    "basis": "attested", "evidence_ids": []}

        for type_id in plain:
            acts.append(act(index, "assertion", {"finding": finding(type_id)}))
            index += 1
        if members:
            family = {"id": family_id, "version": "v1"}
            scope = {"tax-year": "2025"}
            acts.append(act(index, "horizon-genesis", {
                "family": family, "scope": scope, "horizon_id": "demo-t0c-h0"}))
            index += 1
            for n, type_id in enumerate(members):
                acts.append(act(index, "member-transition", {
                    "family": family, "scope": scope,
                    "member": {"action": "assert", "finding": finding(type_id)},
                    "successor": {"id": f"demo-t0c-h{n + 1}", "predecessor": f"demo-t0c-h{n}"}}))
                index += 1
        return acts, finding_ids, fact_ids, index

    def _attempt(self, acts: list[dict[str, Any]], start: int, finding_ids: list[str]) -> str:
        sequence = list(acts) + [
            retraction(start + n, finding_id) for n, finding_id in enumerate(finding_ids)
        ]
        try:
            project(tuple(sequence), self.registry)
        except FindingModelError as exc:
            message = str(exc)
            if "source-family member" in message:
                return "refused-5"
            if "no assertion could create" in message:
                return "refused-6"
            return "refused-other"
        return "admitted"

    # ------------------------------------------------------------- tests
    def test_every_relation_participant_is_covered(self) -> None:
        """Premise check: the eight groups cover every participant of every
        declared subset, companion-presence and companion-equality relation,
        so the classification below is exhaustive rather than a sample."""
        declared: set[str] = set()
        declared |= set(self.registry.subset_invariant_pairs)
        declared |= set(self.registry.subset_invariant_pairs.values())
        declared |= set(self.registry.companion_equality_pairs)
        declared |= set(self.registry.companion_equality_pairs.values())
        for subordinate, companions in self.registry.companion_presence_pairs.items():
            declared.add(subordinate)
            declared |= set([companions] if isinstance(companions, str) else companions)
        covered = {t for _, types, _ in _RELATION_GROUPS for t in types}
        self.assertEqual(declared, covered)
        self.assertEqual(len(declared), 24)

    def test_every_fixture_is_admissible_before_any_retraction(self) -> None:
        """Each relation really is reachable on real content: if a fixture
        did not admit, a later 'not retractable' verdict would be a bug in
        the fixture rather than a property of the contract."""
        for label, types, family in _RELATION_GROUPS:
            with self.subTest(relation=label):
                acts, _, _, _ = self._build(types, family)
                state = project(tuple(acts), self.registry)
                for type_id in types:
                    self.assertTrue(
                        any(f["fact_id"].startswith(type_id + "|") for f in state.findings.values()),
                        f"{type_id} has no finding in its own fixture",
                    )

    def test_direct_retractability_of_every_participant(self) -> None:
        """Set A / set C, by execution. Every one of the 24 participants is
        fenced: subordinates by refusal 5 (they are all source-family member
        predicates), companions and subset dominants by refusal 6."""
        observed: dict[str, str] = {}
        for label, types, family in _RELATION_GROUPS:
            acts, finding_ids, _, nxt = self._build(types, family)
            for type_id in types:
                with self.subTest(relation=label, fact_type=type_id):
                    outcome = self._attempt(acts, nxt, [finding_ids[type_id]])
                    self.assertIn(outcome, {"refused-5", "refused-6"})
                    observed[type_id] = outcome
        member_fenced = {t for t, o in observed.items() if o == "refused-5"}
        invariant_fenced = {t for t, o in observed.items() if o == "refused-6"}
        self.assertEqual(member_fenced, set(self.registry.family_member_predicates) & set(observed))
        self.assertEqual(len(member_fenced) + len(invariant_fenced), 24)
        # No participant is retractable directly: set A, restricted to
        # relation participants, is empty.
        self.assertEqual([t for t, o in observed.items() if o == "admitted"], [])
        # The exact sets, so track-0-findings.md section 6b and this test
        # cannot drift apart. Nine were already fenced by refusal 5 before
        # T0-C; the fifteen below are fenced by the sixth refusal
        # specifically, and are the product-meaning result of deliverable 3.
        self.assertEqual(sorted(member_fenced), [
            "tax.us.2025.f1098e.box1-student-loan-interest",
            "tax.us.2025.f1099div.box12-exempt-interest-dividends",
            "tax.us.2025.f1099div.box1a-ordinary",
            "tax.us.2025.f1099div.box1b-qualified",
            "tax.us.2025.f1099div.box7-foreign-tax-paid",
            "tax.us.2025.f1099g.box1-unemployment",
            "tax.us.2025.f1099int.box8-tax-exempt-interest",
            "tax.us.2025.f1099r.ira-box1-taxable-distribution",
            "tax.us.2025.ssa1099.box5-net-benefits",
        ])
        self.assertEqual(sorted(invariant_fenced), [
            "tax.us.2025.f1098e.box2-checked-authority",
            "tax.us.2025.f1099div.box13-specified-pab-authority",
            "tax.us.2025.f1099div.box8-country-companion",
            "tax.us.2025.f1099g.box4-federal-withholding-authority",
            "tax.us.2025.f1099int.box9-specified-pab-authority",
            "tax.us.2025.f1099r.box2b-not-determined",
            "tax.us.2025.f1099r.distribution-code",
            "tax.us.2025.f1099r.ira-box2a-taxable-amount",
            "tax.us.2025.f1099r.ira-sep-simple-checkbox",
            "tax.us.2025.ssa1099.box3-benefits-paid",
            "tax.us.2025.ssa1099.box4-repayment",
            "tax.us.2025.ssa1099.box6-withholding",
            "tax.us.2025.ssa1099.lump-sum-election",
            "tax.us.2025.ssa1099.recipient",
            "tax.us.2025.ssa1099.statement-kind",
        ])

    def test_no_order_of_retractions_reaches_any_participant(self) -> None:
        """Set B is empty. Retraction sequences are prefix-closed - a
        sequence is admitted only if its first act is - and every length-1
        retraction is refused above, so no longer order can exist. The
        richest relation's 42 ordered pairs are executed as the empirical
        backstop for that argument."""
        label, types, family = _RELATION_GROUPS[6]
        self.assertIn("ssa1099", label)
        acts, finding_ids, _, nxt = self._build(types, family)
        admitted_pairs = [
            (a, b)
            for a, b in itertools.permutations(types, 2)
            if self._attempt(acts, nxt, [finding_ids[a], finding_ids[b]]) == "admitted"
        ]
        self.assertEqual(admitted_pairs, [])

    def test_the_declared_member_transition_route_does_unblock_companions(self) -> None:
        """The mitigation, and the reason set C is 'not retractable by any
        order of *retractions*' rather than 'unreachable'. Withdrawing the
        subordinate through the declared member-transition route - the same
        route refusal 5 names - makes every companion retractable."""
        label, types, family = _RELATION_GROUPS[6]
        acts, finding_ids, fact_ids, nxt = self._build(types, family)
        subordinate = "tax.us.2025.ssa1099.box5-net-benefits"
        removal = act(nxt, "member-transition", {
            "family": {"id": family, "version": "v1"}, "scope": {"tax-year": "2025"},
            "member": {"action": "remove", "fact_id": fact_ids[subordinate]},
            "successor": {"id": "demo-t0c-h9", "predecessor": "demo-t0c-h1"}})
        for type_id in types:
            if type_id == subordinate:
                continue
            with self.subTest(companion=type_id):
                self.assertEqual(
                    self._attempt(acts + [removal], nxt + 1, [finding_ids[type_id]]),
                    "admitted",
                )

    def test_correction_remains_available_for_every_fenced_participant(self) -> None:
        """The other mitigation, and the reason the third set is narrower
        than 'the user cannot change this answer': only withdrawal-to-no-
        answer is blocked. Every fenced participant can still be corrected."""
        label, types, family = _RELATION_GROUPS[6]
        acts, _, fact_ids, nxt = self._build(types, family)
        for type_id in types:
            if type_id in self.registry.family_member_predicates:
                continue  # a member's value is corrected through its own route
            with self.subTest(fact_type=type_id):
                correction = act(nxt, "assertion", {"finding": {
                    "schema": "finding.v1", "id": "demo-f-corrected",
                    "fact_id": fact_ids[type_id], "value": self._value_for(type_id),
                    "basis": "attested", "evidence_ids": []}})
                state = project(tuple(acts + [correction]), self.registry)
                self.assertIn("demo-f-corrected", state.findings)

    def test_declaration_signal_declarations_are_retractable_directly(self) -> None:
        """The declaration/signal enforcer is monotonically permissive under
        retraction: removing a value can only make the declaration absent,
        never make it equal to the contradicting literal. Both declared
        rules' declaration fact types are retractable directly - the only
        facts reached by this deliverable that are."""
        rules = getattr(self.registry, "declaration_signal_contradictions", [])
        self.assertTrue(rules)
        for rule in rules:
            declaration = rule["declaration_fact_type"]
            with self.subTest(declaration=declaration):
                self.assertIn(declaration, self.fact_types)
                acts, finding_ids, _, nxt = self._build((declaration,), "unused")
                self.assertEqual(self._attempt(acts, nxt, [finding_ids[declaration]]), "admitted")


class TestNoAssertionReachableStateBecameUnreachable(Track0Base):
    """T0-C deliverable 4. The sixth refusal narrows what a *retraction*
    may do; it must not narrow what an assertion may do, and every state a
    retraction still reaches must be one an assertion could also reach.
    """

    def test_the_sixth_refusal_is_confined_to_the_retraction_applier(self) -> None:
        """`apply_assertion` does not consult the retraction guard, so no
        assertion can be refused by it."""
        import inspect

        from packages.kernel import findings as findings_module

        assertion_source = inspect.getsource(findings_module.apply_assertion)
        self.assertNotIn(
            "_refuse_retraction_violating_admission_invariants", assertion_source
        )
        retraction_source = inspect.getsource(findings_module.apply_finding_retracted)
        self.assertIn(
            "_refuse_retraction_violating_admission_invariants", retraction_source
        )

    def test_an_admitted_retraction_matches_never_having_answered(self) -> None:
        """The equivalence that makes 'assertion-reachable' concrete: after
        an admitted retraction, every current-value reader reports exactly
        what it reports for a workspace in which the fact was never
        answered at all. The retraction adds history, not a new kind of
        current state."""
        from packages.kernel.read_models import build_read_model

        answered_then_retracted = base_acts() + [
            act(7, "assertion", {"finding": fnd(F_450, ATTR_PAT, 450)}),
            act(8, "assertion", {"finding": fnd(F_KIM, ATTR_KIM, 100)}),
            retraction(9, F_450),
        ]
        never_answered = base_acts() + [
            act(7, "assertion", {"finding": fnd(F_KIM, ATTR_KIM, 100)}),
        ]
        retracted_state = project(tuple(answered_then_retracted), self.registry)
        pristine_state = project(tuple(never_answered), self.registry)

        self.assertIs(self.current_value(retracted_state, ATTR_PAT), _NO_CURRENT_VALUE)
        self.assertIs(self.current_value(pristine_state, ATTR_PAT), _NO_CURRENT_VALUE)
        self.assertEqual(
            _current_values_for_fact_type(retracted_state, ATTR),
            _current_values_for_fact_type(pristine_state, ATTR),
        )
        retracted_model = build_read_model(tuple(answered_then_retracted), self.registry)
        pristine_model = build_read_model(tuple(never_answered), self.registry)
        self.assertEqual(
            retracted_model["current"]["finding_ids"], pristine_model["current"]["finding_ids"]
        )
        self.assertEqual(retracted_model["open_fact_ids"], pristine_model["open_fact_ids"])
        self.assertEqual(
            retracted_model["facts"][ATTR_PAT]["current_finding_id"],
            pristine_model["facts"][ATTR_PAT]["current_finding_id"],
        )
        # The one intended difference: history is retained, not erased.
        self.assertEqual(len(retracted_model["history_by_fact"][ATTR_PAT]), 1)
        self.assertNotIn(ATTR_PAT, pristine_model["history_by_fact"])

    def test_every_relation_fixture_still_admits_by_assertion_alone(self) -> None:
        """No assertion-or-member-transition sequence that admitted before
        T0-C is refused now: each of the eight real-content relation
        fixtures is built purely from assertions and member transitions and
        still projects."""
        # Reuse the content-driven fixture builder rather than restating it.
        builder = TestOrderedRetractabilityOnRealContent(
            methodName="test_every_relation_participant_is_covered"
        )
        builder.setUpClass()
        for label, types, family in _RELATION_GROUPS:
            with self.subTest(relation=label):
                acts, _, _, _ = builder._build(types, family)
                state = project(tuple(acts), builder.registry)
                self.assertEqual(state.retracted_finding_ids, frozenset())
