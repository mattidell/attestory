"""Track 3 recorder facts: the two ordinary questions and the link outcomes.

The relationship bundle v2 adds facts a rule can read for what a person said
about a borrowing and about each link: the two ordinary answers, and an
inclusion or financing pair the person cannot tell, denied, or withdrew. It
also declares the system applicability marker, which no recorder writes.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.loader import DerivationSchemas
from packages.kernel.act_log import ActLog
from packages.kernel.facts import fact_id_for
from packages.kernel.findings import project
from packages.tax.loader import install_domain_scoped_supersession, load_sli_relationship_source_bundle
from tests.support import act, demo_entity

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
V1_BUNDLE = CONTENT / "sli-relationship-source.bundle.json"
V2_BUNDLE = CONTENT / "sli-relationship-source.bundle.v2.json"
V1_SHA256 = "8077dbfcdd8c77b6fdcfaf34b3f1064a0cda7f65d9007ea210290d05dd5f1764"

LOAN_COST = "tax.us.2025.sli.loan-paid-only-school-costs"
ENROLLMENT = "tax.us.2025.sli.enrolled-at-least-half-time"
INCLUSION_UNRESOLVED = "tax.us.2025.sli.statement-inclusion-unresolved"
INCLUSION_DENIED = "tax.us.2025.sli.statement-inclusion-denied"
INCLUSION_WITHDRAWN = "tax.us.2025.sli.statement-inclusion-withdrawn"
FINANCING_UNRESOLVED = "tax.us.2025.sli.financing-unresolved"
FINANCING_DENIED = "tax.us.2025.sli.financing-denied"
FINANCING_WITHDRAWN = "tax.us.2025.sli.financing-withdrawn"
APPLICABILITY_MARKER = "tax.us.2025.sli.statement-inclusion-applicability-unestablished"
SCOPE_UNRESOLVED = "tax.us.2025.sli.statement-inclusion-scope-unresolved"

BORROWING_KEY: list[dict[str, Any]] = [
    {"name": "borrowing", "kind": "entity", "entity_kind": "tax.us.student-loan-borrowing-reference"},
]
STATEMENT_PAIR_KEYS: list[dict[str, Any]] = [
    {"name": "lender", "kind": "entity", "entity_kind": "tax.us.student-loan-lender"},
    {"name": "statement", "kind": "entity", "entity_kind": "tax.us.1098e-statement"},
    {"name": "tax-year", "kind": "literal", "values": ["2025"]},
    {"name": "borrowing", "kind": "entity", "entity_kind": "tax.us.student-loan-borrowing-reference"},
]
STATEMENT_KEYS: list[dict[str, Any]] = STATEMENT_PAIR_KEYS[:3]
FINANCING_PAIR_KEYS: list[dict[str, Any]] = [
    {"name": "borrowing", "kind": "entity", "entity_kind": "tax.us.student-loan-borrowing-reference"},
    {"name": "period", "kind": "entity", "entity_kind": "tax.us.educational-period"},
    {"name": "institution", "kind": "entity", "entity_kind": "tax.us.educational-institution"},
    {"name": "programme", "kind": "entity", "entity_kind": "tax.us.educational-programme"},
]
NEW_FACTS: dict[str, tuple[list[dict[str, Any]], dict[str, Any]]] = {
    LOAN_COST: (BORROWING_KEY, {"type": "string", "enum": ["yes", "no", "cannot-tell"]}),
    ENROLLMENT: (BORROWING_KEY, {"type": "string", "enum": ["yes", "no", "cannot-tell"]}),
    INCLUSION_UNRESOLVED: (STATEMENT_PAIR_KEYS, {"enum": ["sli.statement-inclusion.unresolved"]}),
    INCLUSION_DENIED: (STATEMENT_PAIR_KEYS, {"enum": ["sli.statement-inclusion.denied"]}),
    INCLUSION_WITHDRAWN: (STATEMENT_PAIR_KEYS, {"enum": ["sli.statement-inclusion.withdrawn"]}),
    FINANCING_UNRESOLVED: (FINANCING_PAIR_KEYS, {"enum": ["sli.financing.unresolved"]}),
    FINANCING_DENIED: (FINANCING_PAIR_KEYS, {"enum": ["sli.financing.denied"]}),
    FINANCING_WITHDRAWN: (FINANCING_PAIR_KEYS, {"enum": ["sli.financing.withdrawn"]}),
    APPLICABILITY_MARKER: (STATEMENT_PAIR_KEYS,
                           {"enum": ["sli.statement-inclusion.applicability-unestablished"]}),
    SCOPE_UNRESOLVED: (STATEMENT_KEYS, {"enum": ["sli.statement-inclusion.scope-unresolved"]}),
}

# Payload Instantiation Gate: one hand-written, fully resolved finding per new
# fact. Fact ids are literal strings, not computed, so a key-order or naming
# drift in the bundle fails here.
PAYLOAD_ENTITIES = (
    ("demo-loan", "Synthetic study loan", "tax.us.student-loan-borrowing-reference"),
    ("demo-lender", "Synthetic servicer", "tax.us.student-loan-lender"),
    ("demo-stmt", "Synthetic 2025 Form 1098-E", "tax.us.1098e-statement"),
    ("demo-2022", "Synthetic autumn 2022", "tax.us.educational-period"),
    ("demo-college", "Synthetic college", "tax.us.educational-institution"),
    ("demo-programme", "Synthetic programme", "tax.us.educational-programme"),
)
_PAIR = "lender=demo-lender,statement=demo-stmt,tax-year=2025,borrowing=demo-loan"
_FINANCED = "borrowing=demo-loan,period=demo-2022,institution=demo-college,programme=demo-programme"
PAYLOAD_INSTANCES: list[dict[str, Any]] = [
    {"schema": "finding.v2", "id": "demo.finding.track3.loan-paid-only-school-costs",
     "fact_id": "tax.us.2025.sli.loan-paid-only-school-costs|borrowing=demo-loan",
     "value": "yes", "basis": "attested", "evidence_ids": ["demo.evidence.track3.payload"]},
    {"schema": "finding.v2", "id": "demo.finding.track3.enrolled-at-least-half-time",
     "fact_id": "tax.us.2025.sli.enrolled-at-least-half-time|borrowing=demo-loan",
     "value": "cannot-tell", "basis": "attested", "evidence_ids": ["demo.evidence.track3.payload"]},
    {"schema": "finding.v2", "id": "demo.finding.track3.statement-inclusion-unresolved",
     "fact_id": f"tax.us.2025.sli.statement-inclusion-unresolved|{_PAIR}",
     "value": "sli.statement-inclusion.unresolved", "basis": "attested",
     "evidence_ids": ["demo.evidence.track3.payload"]},
    {"schema": "finding.v2", "id": "demo.finding.track3.statement-inclusion-denied",
     "fact_id": f"tax.us.2025.sli.statement-inclusion-denied|{_PAIR}",
     "value": "sli.statement-inclusion.denied", "basis": "attested",
     "evidence_ids": ["demo.evidence.track3.payload"]},
    {"schema": "finding.v2", "id": "demo.finding.track3.statement-inclusion-withdrawn",
     "fact_id": f"tax.us.2025.sli.statement-inclusion-withdrawn|{_PAIR}",
     "value": "sli.statement-inclusion.withdrawn", "basis": "attested",
     "evidence_ids": ["demo.evidence.track3.payload"]},
    {"schema": "finding.v2", "id": "demo.finding.track3.financing-unresolved",
     "fact_id": f"tax.us.2025.sli.financing-unresolved|{_FINANCED}",
     "value": "sli.financing.unresolved", "basis": "attested",
     "evidence_ids": ["demo.evidence.track3.payload"]},
    {"schema": "finding.v2", "id": "demo.finding.track3.financing-denied",
     "fact_id": f"tax.us.2025.sli.financing-denied|{_FINANCED}",
     "value": "sli.financing.denied", "basis": "attested",
     "evidence_ids": ["demo.evidence.track3.payload"]},
    {"schema": "finding.v2", "id": "demo.finding.track3.financing-withdrawn",
     "fact_id": f"tax.us.2025.sli.financing-withdrawn|{_FINANCED}",
     "value": "sli.financing.withdrawn", "basis": "attested",
     "evidence_ids": ["demo.evidence.track3.payload"]},
    {"schema": "finding.v2", "id": "demo.finding.track3.statement-inclusion-applicability-unestablished",
     "fact_id": f"tax.us.2025.sli.statement-inclusion-applicability-unestablished|{_PAIR}",
     "value": "sli.statement-inclusion.applicability-unestablished", "basis": "attested",
     "evidence_ids": ["demo.evidence.track3.payload"]},
    {"schema": "finding.v2", "id": "demo.finding.track3.statement-inclusion-scope-unresolved",
     "fact_id": "tax.us.2025.sli.statement-inclusion-scope-unresolved|"
                "lender=demo-lender,statement=demo-stmt,tax-year=2025",
     "value": "sli.statement-inclusion.scope-unresolved", "basis": "attested",
     "evidence_ids": ["demo.evidence.track3.payload"]},
]


class RelationshipBundleV2(unittest.TestCase):
    def test_v1_bytes_unchanged_and_v2_carries_v1_fact_types_unchanged(self) -> None:
        self.assertEqual(hashlib.sha256(V1_BUNDLE.read_bytes()).hexdigest(), V1_SHA256)
        v1 = json.loads(V1_BUNDLE.read_text("utf-8"))
        v2 = load_sli_relationship_source_bundle()
        self.assertEqual((v2["id"], v2["version"], v2["schema"]), (v1["id"], "v2", v1["schema"]))
        self.assertEqual(v2, json.loads(V2_BUNDLE.read_text("utf-8")))
        self.assertEqual(v2["fact_types"][:3], v1["fact_types"])

    def test_v2_declares_each_new_fact_with_its_keys_and_values(self) -> None:
        v2 = load_sli_relationship_source_bundle()
        by_id = {row["id"]: row for row in v2["fact_types"]}
        self.assertEqual(set(by_id) - {row["id"] for row in v2["fact_types"][:3]}, set(NEW_FACTS))
        for fact_type_id, (keys, values) in NEW_FACTS.items():
            with self.subTest(fact_type_id):
                row = by_id[fact_type_id]
                self.assertEqual((row["schema"], row["version"], row["nature"]),
                                 ("fact-type.v2", "v1", "determinable"))
                self.assertEqual(row["identity_keys"], keys)
                self.assertEqual(row["value_schema"], values)
                self.assertEqual(row["supersession"], {"policy": "free"})
        # The marker is kept distinct from the person's cannot-tell in name and value.
        self.assertNotEqual(by_id[APPLICABILITY_MARKER]["value_schema"],
                            by_id[INCLUSION_UNRESOLVED]["value_schema"])
        self.assertIn("never", by_id[APPLICABILITY_MARKER]["title"])
        # The statement-level doubt is the person's, also distinct from the marker.
        self.assertNotEqual(by_id[SCOPE_UNRESOLVED]["value_schema"],
                            by_id[APPLICABILITY_MARKER]["value_schema"])
        self.assertNotEqual(by_id[SCOPE_UNRESOLVED]["identity_keys"],
                            by_id[APPLICABILITY_MARKER]["identity_keys"])

    def test_one_hand_written_payload_instance_per_new_fact_is_admitted(self) -> None:
        schemas = DerivationSchemas()
        registry = schemas.registry
        bundle = load_sli_relationship_source_bundle()
        self.assertEqual({row["fact_id"].split("|", 1)[0] for row in PAYLOAD_INSTANCES}, set(NEW_FACTS))
        acts: list[dict[str, Any]] = [act(0, "bundle-adoption", {"bundle": bundle})]
        for identity, label, kind in PAYLOAD_ENTITIES:
            acts.append(act(len(acts), "entity-introduced", {"entity": demo_entity(identity, label, kind)}))
        acts.append(act(len(acts), "evidence-submitted", {"evidence": {
            "schema": "evidence.v1", "id": "demo.evidence.track3.payload",
            "kind": "demo.sli.ordinary-answer", "label": "Synthetic Track 3 payload instance",
            "content": {"synthetic": True}}}))
        for finding in PAYLOAD_INSTANCES:
            registry.validate("finding.v2", finding)
            fact_type_id = finding["fact_id"].split("|", 1)[0]
            names = [key["name"] for key in NEW_FACTS[fact_type_id][0]]
            bindings = dict(pair.split("=", 1) for pair in finding["fact_id"].split("|", 1)[1].split(","))
            self.assertEqual(fact_id_for(fact_type_id, tuple((name, bindings[name]) for name in names)),
                             finding["fact_id"])
            acts.append(act(len(acts), "assertion", {"finding": finding}))
        state = project(tuple(acts), registry)
        for finding in PAYLOAD_INSTANCES:
            self.assertEqual(state.findings[finding["id"]]["value"], finding["value"])

    def test_v1_workspace_can_adopt_v2_and_keeps_its_relationship_types(self) -> None:
        schemas = DerivationSchemas()
        install_domain_scoped_supersession(schemas.registry)
        with tempfile.TemporaryDirectory(prefix="sli-track3-") as raw:
            log = ActLog(Path(raw) / "workspace", schemas.registry)
            log.append(act(0, "bundle-adoption", {"bundle": json.loads(V1_BUNDLE.read_text("utf-8"))}),
                       expected_revision=0)
            log.append(act(1, "bundle-adoption", {"bundle": load_sli_relationship_source_bundle()}),
                       expected_revision=1)
            state = project(ActLog(log.path.parent, schemas.registry).read().acts, schemas.registry)
            self.assertTrue(set(NEW_FACTS) <= set(state.fact_state.fact_types))
            self.assertIn("tax.us.2025.sli.statement-inclusion-relationship", state.fact_state.fact_types)


USER = "demo.user.filer"


class _Workspace:
    """A saved v2 workspace: two borrowings, two schoolings, two statements."""

    def __init__(self, bundle: dict[str, Any] | None = None) -> None:
        import tests.test_sli_relationship_recording as track14
        from packages.tax.sli_relationship_recording import introduce_borrowing_reference_durably

        self.raw = tempfile.TemporaryDirectory(prefix="sli-track3-")
        schemas = DerivationSchemas()
        self.registry = install_domain_scoped_supersession(schemas.registry)
        self.log = ActLog(Path(self.raw.name) / "workspace", self.registry)
        form_bundle = json.loads((CONTENT / "f1098e.bundle.json").read_text("utf-8"))
        relationship_bundle = bundle if bundle is not None else load_sli_relationship_source_bundle()
        self.log.append(act(0, "bundle-adoption", {"bundle": form_bundle}), expected_revision=0)
        self.log.append(act(1, "bundle-adoption", {"bundle": relationship_bundle}), expected_revision=1)
        self.borrowing = {"autumn": "demo.track3.borrowing.autumn", "spring": "demo.track3.borrowing.spring"}
        for name, reference in self.borrowing.items():
            introduce_borrowing_reference_durably(
                self.log, self.registry, reference_id=reference, description=f"{name.title()} study loan",
                actor=USER, at="2026-10-02T09:00:00Z")
        entities = [
            ("demo.track3.period.autumn24", "Autumn 2024", "tax.us.educational-period"),
            ("demo.track3.period.spring25", "Spring 2025", "tax.us.educational-period"),
            ("demo.track3.institution.river", "Riverside College", "tax.us.educational-institution"),
            ("demo.track3.programme.bsc", "BSc", "tax.us.educational-programme"),
            ("demo.track3.lender.cedar", "Cedar Servicing", "tax.us.student-loan-lender"),
            ("demo.track3.lender.birch", "Birch Servicing", "tax.us.student-loan-lender"),
            ("demo.track3.statement.cedar", "2025 Form 1098-E from Cedar", "tax.us.1098e-statement"),
            ("demo.track3.statement.birch", "2025 Form 1098-E from Birch", "tax.us.1098e-statement"),
        ]
        for identity, label, kind in entities:
            revision = self.log.read().revision
            self.log.append(act(revision, "entity-introduced", {"entity": demo_entity(identity, label, kind)}),
                            expected_revision=revision)
        school = "tax.us.2025.sli.schooling-situation"
        self.school = {
            "autumn": track14._append_source(
                self.log, self.registry, school,
                (("period", entities[0][0]), ("institution", entities[2][0]), ("programme", entities[3][0])),
                "Riverside College, BSc, autumn 2024", "track3-school-autumn"),
            "spring": track14._append_source(
                self.log, self.registry, school,
                (("period", entities[1][0]), ("institution", entities[2][0]), ("programme", entities[3][0])),
                "Riverside College, BSc, spring 2025", "track3-school-spring"),
        }
        box1 = "tax.us.2025.f1098e.box1-student-loan-interest"
        self.statement = {
            "cedar": track14._append_source(
                self.log, self.registry, box1,
                (("lender", entities[4][0]), ("statement", entities[6][0]), ("tax-year", "2025")),
                1250.0, "track3-statement-cedar"),
            "birch": track14._append_source(
                self.log, self.registry, box1,
                (("lender", entities[5][0]), ("statement", entities[7][0]), ("tax-year", "2025")),
                1800.0, "track3-statement-birch"),
        }

    def recovered(self) -> tuple[Any, frozenset[str]]:
        from packages.kernel.currency import compute_currency

        state = project(ActLog(self.log.path.parent, self.registry).read().acts, self.registry)
        return state, frozenset(compute_currency(state).current_finding_ids)

    def current_values(self, fact_type_id: str) -> dict[str, Any]:
        """Current findings of one fact type in a fresh recovery, by fact id."""
        from packages.kernel.facts import facts_of

        state, current = self.recovered()
        lattice = facts_of(state.fact_state, include_displaced=True)
        return {row["fact_id"]: row["value"] for fid, row in state.findings.items()
                if fid in current and lattice.get(row["fact_id"]) is not None
                and lattice[row["fact_id"]].fact_type_id == fact_type_id}


def _answer_fact_id(fact_type_id: str, borrowing: str) -> str:
    return fact_id_for(fact_type_id, (("borrowing", borrowing),))


QUESTIONS = {"loan-paid-only-school-costs": LOAN_COST, "enrolled-at-least-half-time": ENROLLMENT}


class TwoOrdinaryQuestions(unittest.TestCase):
    def _review(self, ws: _Workspace, name: str) -> dict[str, Any]:
        from packages.tax.sli_relationship_review import prepare_borrowing_answer_review

        return prepare_borrowing_answer_review(
            ws.log, ws.registry, review_id=f"demo.track3.review.{name}", shown_at="2026-10-02T10:00:00Z",
            borrowing_refs=(ws.borrowing["autumn"], ws.borrowing["spring"]))

    def _save(self, ws: _Workspace, review: dict[str, Any], question: str, response: str,
              name: str, borrowing: str = "autumn") -> dict[str, Any]:
        from packages.tax.sli_relationship_review import save_borrowing_answer_review

        return save_borrowing_answer_review(
            ws.log, ws.registry, review, borrowing_ref=ws.borrowing[borrowing], question=question,
            response=response, actor=USER, at="2026-10-02T10:01:00Z",
            submission_id=f"demo.track3.submission.{name}", evidence_id=f"demo.evidence.track3.{name}")

    def test_review_shows_exactly_the_two_owner_approved_questions(self) -> None:
        ws = _Workspace()
        with ws.raw:
            review = self._review(ws, "shown")
            self.assertEqual(review["propositions"], {
                "loan-paid-only-school-costs": "This loan paid only for school costs.",
                "enrolled-at-least-half-time": (
                    "During the schooling this loan paid for, the student was enrolled at least "
                    "half-time in a degree or certificate program."),
            })
            self.assertEqual(review["responses"], {"loan-paid-only-school-costs": "unanswered",
                                                   "enrolled-at-least-half-time": "unanswered"})
            self.assertEqual([card["shown_as"] for card in review["borrowing_choices"]],
                             ["Autumn study loan", "Spring study loan"])

    def test_each_answer_is_its_own_fact_with_its_own_evidence(self) -> None:
        for question, fact_type_id in QUESTIONS.items():
            for response in ("yes", "no", "cannot-tell"):
                with self.subTest(question=question, response=response):
                    ws = _Workspace()
                    with ws.raw:
                        review = self._review(ws, f"{question}-{response}")
                        result = self._save(ws, review, question, response, f"{question}-{response}")
                        fact_id = _answer_fact_id(fact_type_id, ws.borrowing["autumn"])
                        self.assertEqual(result["fact_id"], fact_id)
                        self.assertEqual(ws.current_values(fact_type_id), {fact_id: response})
                        state, current = ws.recovered()
                        self.assertIn(result["finding_id"], current)
                        finding = state.findings[result["finding_id"]]
                        self.assertEqual(finding["evidence_ids"], [result["evidence_id"]])
                        evidence = state.evidence[result["evidence_id"]].evidence
                        self.assertEqual(evidence["kind"], "tax.student-loan.borrowing-answer")
                        self.assertEqual(evidence["content"]["question"], question)
                        self.assertEqual(evidence["content"]["response"], response)
                        self.assertEqual(evidence["content"]["borrowing_ref"], ws.borrowing["autumn"])
                        self.assertEqual(evidence["content"]["recognition_context"]["proposition"],
                                         review["propositions"][question])
                        other = next(q for q in QUESTIONS.values() if q != fact_type_id)
                        self.assertEqual(ws.current_values(other), {})

    def test_both_answers_for_one_loan_are_independent(self) -> None:
        ws = _Workspace()
        with ws.raw:
            review = self._review(ws, "both")
            cost = self._save(ws, review, "loan-paid-only-school-costs", "yes", "both-cost")
            enrolled = self._save(ws, review, "enrolled-at-least-half-time", "cannot-tell", "both-enrolled")
            self.assertNotEqual(cost["evidence_id"], enrolled["evidence_id"])
            self.assertEqual(ws.current_values(LOAN_COST),
                             {_answer_fact_id(LOAN_COST, ws.borrowing["autumn"]): "yes"})
            self.assertEqual(ws.current_values(ENROLLMENT),
                             {_answer_fact_id(ENROLLMENT, ws.borrowing["autumn"]): "cannot-tell"})
            # A second loan for the same schooling needs its own answer.
            spring = self._save(ws, review, "enrolled-at-least-half-time", "yes", "spring-enrolled",
                                borrowing="spring")
            self.assertEqual(ws.current_values(ENROLLMENT), {
                _answer_fact_id(ENROLLMENT, ws.borrowing["autumn"]): "cannot-tell",
                _answer_fact_id(ENROLLMENT, ws.borrowing["spring"]): "yes"})
            self.assertEqual(spring["fact_id"], _answer_fact_id(ENROLLMENT, ws.borrowing["spring"]))

    def test_correcting_each_answer_supersedes_it_and_keeps_history(self) -> None:
        from packages.tax.sli_relationship_review import correct_borrowing_answer_review

        for question, fact_type_id in QUESTIONS.items():
            with self.subTest(question=question):
                ws = _Workspace()
                with ws.raw:
                    review = self._review(ws, f"correct-{question}")
                    first = self._save(ws, review, question, "yes", f"correct-{question}-first")
                    second = correct_borrowing_answer_review(
                        ws.log, ws.registry, self._review(ws, f"correct-{question}-again"),
                        finding_id=first["finding_id"], borrowing_ref=ws.borrowing["autumn"],
                        question=question, response="no", actor=USER, at="2026-10-02T10:02:00Z",
                        submission_id=f"demo.track3.submission.correct-{question}-second",
                        evidence_id=f"demo.evidence.track3.correct-{question}-second")
                    state, current = ws.recovered()
                    self.assertNotIn(first["finding_id"], current)
                    self.assertIn(first["finding_id"], state.findings)
                    self.assertIn(second["finding_id"], current)
                    self.assertEqual(ws.current_values(fact_type_id), {first["fact_id"]: "no"})
                    content = state.evidence[second["evidence_id"]].evidence["content"]
                    self.assertEqual(content["correction_of_finding_id"], first["finding_id"])
                    self.assertEqual(state.evidence[first["evidence_id"]].evidence["content"]["response"], "yes")

    def test_withdrawing_each_answer_leaves_no_current_answer_and_keeps_history(self) -> None:
        from packages.tax.sli_relationship_review import withdraw_borrowing_answer_review

        for question, fact_type_id in QUESTIONS.items():
            with self.subTest(question=question):
                ws = _Workspace()
                with ws.raw:
                    first = self._save(ws, self._review(ws, f"w-{question}"), question, "yes", f"w-{question}")
                    withdraw_borrowing_answer_review(ws.log, ws.registry, finding_id=first["finding_id"],
                                                     actor=USER, at="2026-10-02T10:03:00Z")
                    state, current = ws.recovered()
                    self.assertEqual(ws.current_values(fact_type_id), {})
                    self.assertIn(first["finding_id"], state.findings)
                    self.assertIn(first["evidence_id"], state.evidence)
                    # A withdrawn answer is a missing answer; the person may answer again.
                    again = self._save(ws, self._review(ws, f"w-{question}-again"), question, "cannot-tell",
                                       f"w-{question}-again")
                    self.assertEqual(ws.current_values(fact_type_id), {again["fact_id"]: "cannot-tell"})

    def test_answers_refuse_without_a_recordable_choice(self) -> None:
        from packages.tax.sli_relationship_recording import RelationshipRecordingRefused

        ws = _Workspace()
        with ws.raw:
            review = self._review(ws, "refusals")
            with self.assertRaisesRegex(RelationshipRecordingRefused, "yes, no, or cannot-tell"):
                self._save(ws, review, "loan-paid-only-school-costs", "unanswered", "refuse-unanswered")
            with self.assertRaisesRegex(RelationshipRecordingRefused, "unknown borrowing question"):
                self._save(ws, review, "no-non-qualified-loan-component", "yes", "refuse-question")
            self._save(ws, review, "loan-paid-only-school-costs", "yes", "refuse-first")
            with self.assertRaisesRegex(RelationshipRecordingRefused, "already has a current answer"):
                self._save(ws, review, "loan-paid-only-school-costs", "no", "refuse-second")
            self.assertEqual(ws.current_values(LOAN_COST),
                             {_answer_fact_id(LOAN_COST, ws.borrowing["autumn"]): "yes"})

    def test_v1_only_workspace_adopts_bundle_v2_with_the_first_answer(self) -> None:
        # Track 7, carried item 1: the first answer's save adopts bundle v2
        # before the answer, so a v1-era workspace is not stuck.
        ws = _Workspace(bundle=json.loads(V1_BUNDLE.read_text("utf-8")))
        with ws.raw:
            revision = ws.log.read().revision
            saved = self._save(ws, self._review(ws, "v1"), "loan-paid-only-school-costs", "yes", "v1")
            self.assertEqual(saved["adopted_bundle_version"], "v2")
            added = ws.log.read().acts[revision:]
            self.assertEqual([row["kind"] for row in added],
                             ["bundle-adoption", "evidence-submitted", "contribution", "assertion"])
            self.assertEqual(ws.current_values(LOAN_COST), {_answer_fact_id(LOAN_COST, ws.borrowing["autumn"]): "yes"})
            again = self._save(ws, self._review(ws, "v1-again"), "enrolled-at-least-half-time", "yes", "v1-again")
            self.assertIsNone(again["adopted_bundle_version"])


OUTCOME_TYPES = {
    "financing": {"cannot-tell": FINANCING_UNRESOLVED, "no": FINANCING_DENIED,
                  "withdrawn": FINANCING_WITHDRAWN},
    "statement-inclusion": {"cannot-tell": INCLUSION_UNRESOLVED, "no": INCLUSION_DENIED,
                            "withdrawn": INCLUSION_WITHDRAWN},
}
OUTCOME_VALUES = {
    FINANCING_UNRESOLVED: "sli.financing.unresolved", FINANCING_DENIED: "sli.financing.denied",
    FINANCING_WITHDRAWN: "sli.financing.withdrawn",
    INCLUSION_UNRESOLVED: "sli.statement-inclusion.unresolved",
    INCLUSION_DENIED: "sli.statement-inclusion.denied",
    INCLUSION_WITHDRAWN: "sli.statement-inclusion.withdrawn",
}
ALL_OUTCOME_TYPES = tuple(OUTCOME_VALUES)
SAMPLE_UNRESOLVED = "demo.tax.2025.sli.statement-inclusion-unresolved"


class LinkOutcomes(unittest.TestCase):
    """Cannot tell, no and withdrawal each leave a current fact a rule can require."""

    def _review(self, ws: _Workspace, name: str) -> dict[str, Any]:
        from packages.tax.sli_relationship_review import prepare_review

        return prepare_review(ws.log, ws.registry, review_id=f"demo.track3.review.{name}",
                              shown_at="2026-10-02T11:00:00Z",
                              borrowing_refs=tuple(ws.borrowing.values()),
                              schooling_fact_ids=tuple(ws.school.values()),
                              statement_fact_ids=tuple(ws.statement.values()))

    def _clause(self, ws: _Workspace, kind: str, borrowing: str, target: str,
                response: str) -> dict[str, Any]:
        financing = kind == "financing"
        return {"borrowing_ref": ws.borrowing[borrowing],
                "schooling_fact_id": ws.school[target] if financing else None,
                "statement_fact_id": None if financing else ws.statement[target],
                "financing_response": response if financing else "unanswered",
                "inclusion_response": "unanswered" if financing else response}

    def _save(self, ws: _Workspace, kind: str, borrowing: str, target: str, response: str,
              name: str) -> dict[str, Any]:
        from packages.tax.sli_relationship_review import save_review

        return save_review(ws.log, ws.registry, self._review(ws, name),
                           **self._clause(ws, kind, borrowing, target, response),
                           actor=USER, at="2026-10-02T11:01:00Z",
                           submission_id=f"demo.track3.submission.{name}",
                           evidence_id=f"demo.evidence.track3.{name}")

    def _apply_outcome(self, ws: _Workspace, kind: str, borrowing: str, target: str, outcome: str,
                 finding_id: str, name: str) -> dict[str, Any]:
        from packages.tax.sli_relationship_review import answer_review_claim, withdraw_review_claim

        if outcome == "withdrawn":
            return withdraw_review_claim(ws.log, ws.registry, finding_id=finding_id, actor=USER,
                                         at="2026-10-02T11:02:00Z")
        return answer_review_claim(ws.log, ws.registry, finding_id=finding_id, review=self._review(ws, name),
                                   **self._clause(ws, kind, borrowing, target, outcome),
                                   actor=USER, at="2026-10-02T11:02:00Z",
                                   submission_id=f"demo.track3.submission.{name}",
                                   evidence_id=f"demo.evidence.track3.{name}")

    def _later_yes(self, ws: _Workspace, kind: str, borrowing: str, target: str,
                   predecessor: str, name: str) -> dict[str, Any]:
        from packages.tax.sli_relationship_review import correct_review_claim

        return correct_review_claim(ws.log, ws.registry, finding_id=predecessor, review=self._review(ws, name),
                                    **self._clause(ws, kind, borrowing, target, "yes"),
                                    actor=USER, at="2026-10-02T11:03:00Z",
                                    submission_id=f"demo.track3.submission.{name}",
                                    evidence_id=f"demo.evidence.track3.{name}")

    def _pair(self, ws: _Workspace, kind: str, borrowing: str, target: str, fact_type_id: str) -> str:
        from packages.kernel.facts import facts_of

        state, _current = ws.recovered()
        lattice = facts_of(state.fact_state, include_displaced=True)
        if kind == "financing":
            keys = (("borrowing", ws.borrowing[borrowing]),) + tuple(lattice[ws.school[target]].keys)
        else:
            keys = tuple(lattice[ws.statement[target]].keys) + (("borrowing", ws.borrowing[borrowing]),)
        return fact_id_for(fact_type_id, keys)

    def _outcomes_in_log(self, ws: _Workspace) -> dict[str, list[tuple[str, bool]]]:
        """Every outcome finding in the log by fact type: (fact id, current)."""
        from packages.kernel.facts import facts_of

        state, current = ws.recovered()
        lattice = facts_of(state.fact_state, include_displaced=True)
        found: dict[str, list[tuple[str, bool]]] = {}
        for finding_id, row in state.findings.items():
            fact = lattice.get(row["fact_id"])
            if fact is not None and fact.fact_type_id in ALL_OUTCOME_TYPES + (SAMPLE_UNRESOLVED, APPLICABILITY_MARKER, SCOPE_UNRESOLVED):
                found.setdefault(fact.fact_type_id, []).append((row["fact_id"], finding_id in current))
        return found

    def _assert_pair_state(self, ws: _Workspace, kind: str, borrowing: str, target: str,
                           expected: str | None) -> None:
        """Exactly one current standing for the pair: affirmed, an outcome, or none."""
        relation = ("tax.us.2025.sli.financing-relationship" if kind == "financing"
                    else "tax.us.2025.sli.statement-inclusion-relationship")
        standing: dict[str, Any] = {}
        for fact_type_id in (relation, *OUTCOME_TYPES[kind].values()):
            fact_id = self._pair(ws, kind, borrowing, target, fact_type_id)
            value = ws.current_values(fact_type_id).get(fact_id)
            if value is not None:
                standing[fact_type_id] = value
        if expected is None:
            self.assertEqual(standing, {})
        elif expected == "affirmed":
            self.assertEqual(list(standing), [relation])
        else:
            self.assertEqual(standing, {expected: OUTCOME_VALUES[expected]})

    def test_each_outcome_writes_its_fact_and_a_later_yes_ends_it(self) -> None:
        for kind, target in (("financing", "autumn"), ("statement-inclusion", "cedar")):
            for outcome, fact_type_id in OUTCOME_TYPES[kind].items():
                with self.subTest(kind=kind, outcome=outcome):
                    ws = _Workspace()
                    with ws.raw:
                        name = f"{kind}-{outcome}"
                        affirmed = self._save(ws, kind, "autumn", target, "yes", f"{name}-yes")
                        predecessor = affirmed["claims"][kind]["finding_id"]
                        self._apply_outcome(ws, kind, "autumn", target, outcome, predecessor, f"{name}-answer")
                        state, current = ws.recovered()
                        self.assertNotIn(predecessor, current)
                        self.assertIn(predecessor, state.findings)
                        self._assert_pair_state(ws, kind, "autumn", target, fact_type_id)
                        outcome_ids = [fid for fid, row in state.findings.items() if fid in current
                                       and row["fact_id"] == self._pair(ws, kind, "autumn", target,
                                                                        fact_type_id)]
                        self.assertEqual(len(outcome_ids), 1)
                        if outcome != "withdrawn":
                            # The person's answer is the outcome's evidence.
                            self.assertEqual(state.findings[outcome_ids[0]]["evidence_ids"],
                                             [f"demo.evidence.track3.{name}-answer"])
                        else:
                            evidence_id = state.findings[outcome_ids[0]]["evidence_ids"][0]
                            withdrawal = state.evidence[evidence_id].evidence
                            self.assertEqual(withdrawal["kind"], "tax.student-loan.relationship-withdrawal")
                            self.assertEqual(withdrawal["content"]["withdrawn_finding_id"], predecessor)

                        later = self._later_yes(ws, kind, "autumn", target, predecessor, f"{name}-later")
                        state, current = ws.recovered()
                        self.assertIn(later["claims"][kind]["finding_id"], current)
                        self._assert_pair_state(ws, kind, "autumn", target, "affirmed")
                        # The ended outcome stays in history.
                        self.assertIn(outcome_ids[0], state.findings)
                        self.assertNotIn(outcome_ids[0], current)

    def test_a_later_yes_through_a_fresh_save_also_ends_the_outcome(self) -> None:
        for kind, target in (("financing", "autumn"), ("statement-inclusion", "cedar")):
            for outcome, fact_type_id in OUTCOME_TYPES[kind].items():
                with self.subTest(kind=kind, outcome=outcome):
                    ws = _Workspace()
                    with ws.raw:
                        name = f"fresh-{kind}-{outcome}"
                        affirmed = self._save(ws, kind, "autumn", target, "yes", f"{name}-yes")
                        self._apply_outcome(ws, kind, "autumn", target, outcome,
                                      affirmed["claims"][kind]["finding_id"], f"{name}-answer")
                        self._assert_pair_state(ws, kind, "autumn", target, fact_type_id)
                        self._save(ws, kind, "autumn", target, "yes", f"{name}-again")
                        self._assert_pair_state(ws, kind, "autumn", target, "affirmed")

    def test_no_after_cannot_tell_replaces_the_open_pair_with_a_denial(self) -> None:
        for kind, target in (("financing", "autumn"), ("statement-inclusion", "cedar")):
            with self.subTest(kind=kind):
                ws = _Workspace()
                with ws.raw:
                    name = f"no-after-{kind}"
                    affirmed = self._save(ws, kind, "autumn", target, "yes", f"{name}-yes")
                    predecessor = affirmed["claims"][kind]["finding_id"]
                    self._apply_outcome(ws, kind, "autumn", target, "cannot-tell", predecessor, f"{name}-unsure")
                    self._apply_outcome(ws, kind, "autumn", target, "no", predecessor, f"{name}-no")
                    self._assert_pair_state(ws, kind, "autumn", target, OUTCOME_TYPES[kind]["no"])
                    unresolved = self._pair(ws, kind, "autumn", target, OUTCOME_TYPES[kind]["cannot-tell"])
                    self.assertEqual(self._outcomes_in_log(ws)[OUTCOME_TYPES[kind]["cannot-tell"]],
                                     [(unresolved, False)])

    def test_an_identified_no_or_cannot_tell_without_a_prior_yes_is_recorded(self) -> None:
        ws = _Workspace()
        with ws.raw:
            first = self._save(ws, "financing", "autumn", "spring", "no", "fresh-financing-no")
            second = self._save(ws, "statement-inclusion", "spring", "cedar", "cannot-tell",
                                "fresh-inclusion-unsure")
            self.assertEqual((first["claims"], second["claims"]), ({}, {}))
            self._assert_pair_state(ws, "financing", "autumn", "spring", FINANCING_DENIED)
            self._assert_pair_state(ws, "statement-inclusion", "spring", "cedar", INCLUSION_UNRESOLVED)
            # An unidentified cannot-tell has no pair to key, so it writes nothing.
            from packages.tax.sli_relationship_review import save_review

            save_review(ws.log, ws.registry, self._review(ws, "unidentified"), borrowing_ref=None,
                        schooling_fact_id=None, statement_fact_id=None,
                        financing_response="cannot-tell", inclusion_response="cannot-tell",
                        actor=USER, at="2026-10-02T11:04:00Z",
                        submission_id="demo.track3.submission.unidentified",
                        evidence_id="demo.evidence.track3.unidentified")
            self.assertEqual({t: len(rows) for t, rows in self._outcomes_in_log(ws).items()},
                             {FINANCING_DENIED: 1, INCLUSION_UNRESOLVED: 1})

    def test_a_fresh_no_over_a_current_affirmation_is_refused(self) -> None:
        from packages.tax.sli_relationship_recording import RelationshipRecordingRefused

        for kind, target in (("financing", "autumn"), ("statement-inclusion", "cedar")):
            with self.subTest(kind=kind):
                ws = _Workspace()
                with ws.raw:
                    self._save(ws, kind, "autumn", target, "yes", f"over-{kind}-yes")
                    revision = ws.log.read().revision
                    with self.assertRaisesRegex(RelationshipRecordingRefused, "currently affirmed"):
                        self._save(ws, kind, "autumn", target, "no", f"over-{kind}-no")
                    self.assertEqual(ws.log.read().revision, revision)
                    self._assert_pair_state(ws, kind, "autumn", target, "affirmed")

    def test_the_same_outcome_again_supersedes_the_earlier_one(self) -> None:
        ws = _Workspace()
        with ws.raw:
            affirmed = self._save(ws, "financing", "autumn", "autumn", "yes", "again-yes")
            predecessor = affirmed["claims"]["financing"]["finding_id"]
            self._apply_outcome(ws, "financing", "autumn", "autumn", "cannot-tell", predecessor, "again-1")
            self._apply_outcome(ws, "financing", "autumn", "autumn", "cannot-tell", predecessor, "again-2")
            self._assert_pair_state(ws, "financing", "autumn", "autumn", FINANCING_UNRESOLVED)
            unresolved = self._pair(ws, "financing", "autumn", "autumn", FINANCING_UNRESOLVED)
            self.assertEqual(sorted(self._outcomes_in_log(ws)[FINANCING_UNRESOLVED]),
                             [(unresolved, False), (unresolved, True)])

    def _unknown_borrowing(self, ws: _Workspace, statement: str, name: str) -> dict[str, Any]:
        """The person names the statement but cannot tell which loan it covers."""
        from packages.tax.sli_relationship_review import save_review

        return save_review(ws.log, ws.registry, self._review(ws, name), borrowing_ref=None,
                           schooling_fact_id=None, statement_fact_id=ws.statement[statement],
                           financing_response="unanswered", inclusion_response="cannot-tell",
                           actor=USER, at="2026-10-02T11:06:00Z",
                           submission_id=f"demo.track3.submission.{name}",
                           evidence_id=f"demo.evidence.track3.{name}")

    def _scope_fact_id(self, ws: _Workspace, statement: str) -> str:
        from packages.kernel.facts import facts_of

        state, _current = ws.recovered()
        return fact_id_for(SCOPE_UNRESOLVED, tuple(facts_of(state.fact_state)[ws.statement[statement]].keys))

    def test_cannot_tell_with_a_named_statement_and_unknown_loan_keeps_a_statement_doubt(self) -> None:
        ws = _Workspace()
        with ws.raw:
            result = self._unknown_borrowing(ws, "cedar", "scope-doubt")
            self.assertEqual(result["claims"], {})
            scope = self._scope_fact_id(ws, "cedar")
            self.assertEqual(ws.current_values(SCOPE_UNRESOLVED),
                             {scope: "sli.statement-inclusion.scope-unresolved"})
            state, current = ws.recovered()
            [finding] = [row for fid, row in state.findings.items()
                         if fid in current and row["fact_id"] == scope]
            self.assertEqual(finding["evidence_ids"], ["demo.evidence.track3.scope-doubt"])
            self.assertEqual(ws.current_values(APPLICABILITY_MARKER), {})
            self.assertEqual({t: len(rows) for t, rows in self._outcomes_in_log(ws).items()},
                             {SCOPE_UNRESOLVED: 1})

    def test_a_later_identified_answer_ends_the_statement_doubt(self) -> None:
        for response, standing in (("yes", "affirmed"), ("no", INCLUSION_DENIED),
                                   ("cannot-tell", INCLUSION_UNRESOLVED)):
            with self.subTest(response=response):
                ws = _Workspace()
                with ws.raw:
                    self._unknown_borrowing(ws, "cedar", f"doubt-{response}")
                    self._save(ws, "statement-inclusion", "autumn", "cedar", response, f"doubt-{response}-later")
                    scope = self._scope_fact_id(ws, "cedar")
                    self.assertEqual(ws.current_values(SCOPE_UNRESOLVED), {})
                    self.assertEqual(self._outcomes_in_log(ws)[SCOPE_UNRESOLVED], [(scope, False)])
                    self._assert_pair_state(ws, "statement-inclusion", "autumn", "cedar", standing)

    def test_a_statement_doubt_leaves_an_unrelated_statement_alone(self) -> None:
        ws = _Workspace()
        with ws.raw:
            self._unknown_borrowing(ws, "cedar", "doubt-unrelated")
            self._save(ws, "statement-inclusion", "spring", "birch", "yes", "doubt-unrelated-birch")
            self.assertEqual(ws.current_values(SCOPE_UNRESOLVED),
                             {self._scope_fact_id(ws, "cedar"): "sli.statement-inclusion.scope-unresolved"})
            self._assert_pair_state(ws, "statement-inclusion", "spring", "birch", "affirmed")
            # A later doubt about Birch is its own fact; Cedar's stays.
            self._unknown_borrowing(ws, "birch", "doubt-unrelated-birch-2")
            self.assertEqual(set(ws.current_values(SCOPE_UNRESOLVED)),
                             {self._scope_fact_id(ws, "cedar"), self._scope_fact_id(ws, "birch")})

    def test_a_statement_doubt_needs_a_current_statement(self) -> None:
        from packages.tax.sli_relationship_recording import RelationshipRecordingRefused, record_submission_durably

        ws = _Workspace()
        with ws.raw:
            revision = ws.log.read().revision
            with self.assertRaisesRegex(RelationshipRecordingRefused, "1098-E box-1 source is missing"):
                record_submission_durably(ws.log, {
                    "submission_id": "demo.track3.submission.stale-doubt",
                    "evidence_id": "demo.evidence.track3.stale-doubt", "actor": USER,
                    "at": "2026-10-02T11:07:00Z", "borrowing_ref": None, "schooling_fact_id": None,
                    "statement_fact_id": "tax.us.2025.f1098e.box1-student-loan-interest|lender=x,statement=y,tax-year=2025",
                    "financing_response": "unanswered", "inclusion_response": "cannot-tell"}, ws.registry)
            self.assertEqual(ws.log.read().revision, revision)

    def test_genuine_absence_writes_no_outcome(self) -> None:
        ws = _Workspace()
        with ws.raw:
            self._save(ws, "financing", "autumn", "autumn", "yes", "absent-financing")
            self._save(ws, "statement-inclusion", "autumn", "cedar", "yes", "absent-inclusion")
            # The spring schooling and the Birch statement are never mentioned.
            self.assertEqual(self._outcomes_in_log(ws), {})
            self._assert_pair_state(ws, "financing", "autumn", "spring", None)
            self._assert_pair_state(ws, "statement-inclusion", "autumn", "birch", None)

    def test_an_unrelated_statement_and_borrowing_are_unaffected(self) -> None:
        ws = _Workspace()
        with ws.raw:
            autumn_inclusion = self._save(ws, "statement-inclusion", "autumn", "cedar", "yes", "u-a-inc")
            spring_inclusion = self._save(ws, "statement-inclusion", "spring", "birch", "yes", "u-s-inc")
            autumn_financing = self._save(ws, "financing", "autumn", "autumn", "yes", "u-a-fin")
            spring_financing = self._save(ws, "financing", "spring", "spring", "yes", "u-s-fin")
            self._apply_outcome(ws, "statement-inclusion", "autumn", "cedar", "cannot-tell",
                          autumn_inclusion["claims"]["statement-inclusion"]["finding_id"], "u-a-inc-unsure")
            self._apply_outcome(ws, "financing", "autumn", "autumn", "withdrawn",
                          autumn_financing["claims"]["financing"]["finding_id"], "u-a-fin-withdraw")
            state, current = ws.recovered()
            self.assertIn(spring_inclusion["claims"]["statement-inclusion"]["finding_id"], current)
            self.assertIn(spring_financing["claims"]["financing"]["finding_id"], current)
            self._assert_pair_state(ws, "statement-inclusion", "spring", "birch", "affirmed")
            self._assert_pair_state(ws, "financing", "spring", "spring", "affirmed")
            self._assert_pair_state(ws, "statement-inclusion", "autumn", "cedar", INCLUSION_UNRESOLVED)
            self._assert_pair_state(ws, "financing", "autumn", "autumn", FINANCING_WITHDRAWN)
            self.assertEqual({t: len(rows) for t, rows in self._outcomes_in_log(ws).items()},
                             {INCLUSION_UNRESOLVED: 1, FINANCING_WITHDRAWN: 1})

    def test_reviewed_statement_correction_writes_the_production_facts(self) -> None:
        from packages.tax.sli_relationship_review import apply_statement_correction_review

        for scope, fact_type_id in (("inclusion-removed", INCLUSION_DENIED),
                                    ("inclusion-uncertain", INCLUSION_UNRESOLVED)):
            with self.subTest(scope=scope):
                ws = _Workspace()
                with ws.raw:
                    affirmed = self._save(ws, "statement-inclusion", "autumn", "cedar", "yes", f"{scope}-yes")
                    result = apply_statement_correction_review(
                        ws.log, ws.registry, review=self._review(ws, f"{scope}-review"),
                        statement_fact_id=ws.statement["cedar"], scope=scope,
                        borrowing_ref=ws.borrowing["autumn"],
                        finding_id=affirmed["claims"]["statement-inclusion"]["finding_id"],
                        corrected_box1_total=1300.0, source_correction_id=f"demo.track3.correction.{scope}",
                        actor=USER, at="2026-10-02T11:05:00Z",
                        submission_id=f"demo.track3.submission.{scope}",
                        evidence_id=f"demo.evidence.track3.{scope}")
                    state, current = ws.recovered()
                    self.assertIn(result["source_correction"]["source_finding_id"], current)
                    self.assertEqual(ws.current_values("tax.us.2025.f1098e.box1-student-loan-interest")
                                     [ws.statement["cedar"]], 1300.0)
                    self._assert_pair_state(ws, "statement-inclusion", "autumn", "cedar", fact_type_id)
                    self.assertNotIn(SAMPLE_UNRESOLVED, self._outcomes_in_log(ws))

    def test_an_interrupted_answer_or_withdrawal_saves_nothing(self) -> None:
        # Track 7: the outcome and the end of the affirmation are one batch. An
        # interruption at the retraction leaves neither: the pair is as before.
        from unittest import mock

        from packages.kernel.act_log import ActLogError

        for outcome in ("cannot-tell", "no", "withdrawn"):
            with self.subTest(outcome=outcome):
                ws = _Workspace()
                with ws.raw:
                    affirmed = self._save(ws, "statement-inclusion", "autumn", "cedar", "yes", f"i-{outcome}")
                    predecessor = affirmed["claims"]["statement-inclusion"]["finding_id"]
                    before = ws.log.path.read_bytes()
                    real_line = ActLog._write_pending_line

                    def fail_retraction(log: ActLog, handle: Any, line: bytes) -> None:
                        row = json.loads(line)
                        if row.get("kind") == "finding-retracted" and row["payload"]["finding_id"] == predecessor:
                            raise ActLogError("synthetic interruption before the affirmation ends")
                        real_line(log, handle, line)

                    with mock.patch.object(ActLog, "_write_pending_line", fail_retraction), \
                            self.assertRaisesRegex(ActLogError, "synthetic interruption"):
                        self._apply_outcome(ws, "statement-inclusion", "autumn", "cedar", outcome, predecessor,
                                            f"i-{outcome}-answer")
                    self.assertEqual(ws.log.path.read_bytes(), before)
                    _state, current = ws.recovered()
                    self.assertIn(predecessor, current)
                    self.assertEqual(ws.current_values(OUTCOME_TYPES["statement-inclusion"][outcome]), {})


    def test_a_v1_only_workspace_records_link_outcomes_as_before(self) -> None:
        from packages.tax.sli_relationship_recording import RelationshipRecordingRefused

        ws = _Workspace(bundle=json.loads(V1_BUNDLE.read_text("utf-8")))
        with ws.raw:
            financing = self._save(ws, "financing", "autumn", "autumn", "yes", "v1-fin")
            self._apply_outcome(ws, "financing", "autumn", "autumn", "cannot-tell",
                            financing["claims"]["financing"]["finding_id"], "v1-fin-unsure")
            inclusion = self._save(ws, "statement-inclusion", "autumn", "cedar", "yes", "v1-inc")
            with self.assertRaisesRegex(RelationshipRecordingRefused, "not adopted"):
                self._apply_outcome(ws, "statement-inclusion", "autumn", "cedar", "cannot-tell",
                                inclusion["claims"]["statement-inclusion"]["finding_id"], "v1-inc-unsure")
            self.assertEqual(self._outcomes_in_log(ws), {})


class WorkspacesWithoutTheNewFacts(unittest.TestCase):
    def test_a_workspace_with_no_relationship_claims_is_unchanged(self) -> None:
        from packages.kernel.facts import facts_of
        from packages.tax.sli_relationship_recording import current_claim_applicability
        import tests.test_sli_relationship_recording as track14

        observed = []
        for bundle in (json.loads(V1_BUNDLE.read_text("utf-8")), load_sli_relationship_source_bundle()):
            ws = _Workspace(bundle=bundle)
            with ws.raw:
                state, _ = ws.recovered()
                keys = tuple(facts_of(state.fact_state)[ws.statement["cedar"]].keys)
                track14._append_source(ws.log, ws.registry, "tax.us.2025.f1098e.box1-student-loan-interest",
                                       keys, 1410.0, "track3-direct-append")
                state, current = ws.recovered()
                acts = ActLog(ws.log.path.parent, ws.registry).read().acts
                observed.append((
                    sorted(current),
                    ws.current_values("tax.us.2025.f1098e.box1-student-loan-interest"),
                    current_claim_applicability(acts, ws.registry),
                    [row["kind"] for row in acts],
                ))
        self.assertEqual(observed[0], observed[1])
        self.assertEqual(observed[1][1][ws.statement["cedar"]], 1410.0)


if __name__ == "__main__":
    unittest.main()
