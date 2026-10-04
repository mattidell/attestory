"""Track 4: the student-loan support chain.

Per financing link, per statement inclusion and per Form 1098-E statement,
the chain decides from the person's recorded relationships and two ordinary
answers whether a statement is ``plain-case-supported`` or ``not-supported``,
and why. Every case here is recorded with the real recorder and review flow,
recovered fresh from the ActLog, validated as a package, marshalled from the
recovered state (with the replay applicability reading the coordinator
supplies), and run through both runners, which must agree.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.live import _resolve_run_authorization, _resolved_run_material
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.marshal import marshal_live_run_context, marshal_run_context
from packages.derivation.package_validation import citizen_checksum, package_instance_checksum, validate_package
from packages.derivation.production_resolver import PublicationSurface, Refusal, resolve_production_package
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import RunResult, run
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for, facts_of
from packages.kernel.findings import project
from packages.tax.loader import install_domain_scoped_supersession, load_sli_relationship_source_bundle
from packages.tax.sli_relationship_recording import current_claim_applicability, introduce_borrowing_reference_durably
import tests.test_sli_relationship_recording as track14
import tests.test_sli_track17_relationship_applicability as track17
from tests.support import act, demo_entity

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
USER = "demo.user.filer"
SCOPE = {"jurisdiction": "us", "year": "2025"}

BOX1 = "tax.us.2025.f1098e.box1-student-loan-interest"
SCHOOL = "tax.us.2025.sli.schooling-situation"
FIN = "tax.us.2025.sli.financing-relationship"
INCL = "tax.us.2025.sli.statement-inclusion-relationship"
LOAN = "tax.us.2025.sli.loan-paid-only-school-costs"
ENROLL = "tax.us.2025.sli.enrolled-at-least-half-time"
MARKER = "tax.us.2025.sli.statement-inclusion-applicability-unestablished"

FIN_LINK = "tax.us.2025.sli.financing-schooling-link"
INCL_REASON = "tax.us.2025.sli.inclusion-support-reason"
SUPPORT = "tax.us.2025.sli.inclusion-support"
CONCLUSION = "tax.us.2025.sli.statement-loan-support"
REASON = "tax.us.2025.sli.statement-support-reason"
FIN_LINK_RULE = "tax.us.2025.rule.sli-financing-schooling-link"
INCL_REASON_RULE = "tax.us.2025.rule.sli-inclusion-support-reason"
SUPPORT_RULE = "tax.us.2025.rule.sli-inclusion-support"

SUPPORT_BUNDLE = "sli-support-chain.bundle.json"
SLICE_PARAMETERS = ("parameter.sli-statement-support-no-inclusion.json",)
INCLUSION_RULE_FILES = (
    "rule.sli-financing-schooling-link.json",
    "rule.sli-inclusion-financing-count.json",
    "rule.sli-inclusion-financing-unresolved-count.json",
    "rule.sli-inclusion-financing-withdrawn-count.json",
    "rule.sli-inclusion-loan-cost-answer-count.json",
    "rule.sli-inclusion-enrollment-answer-count.json",
    "rule.sli-inclusion-support-reason.json",
    "rule.sli-inclusion-support.json",
)
PACKAGE_ID = "tax.us.2025.package.core-calculations"
V39_PACKAGE = CONTENT / "package.core-calculations.v39.json"
V38_PACKAGE = CONTENT / "package.core-calculations.v38.json"
V37_REGISTRY = CONTENT / "published-packages.v37.json"
V36_REGISTRY = CONTENT / "published-packages.v36.json"
RELEASE_DIR = ROOT / "packages" / "sample_data" / "student_loan_support_chain" / "publication_surface" / "releases"
V37_RELEASE = RELEASE_DIR / "demo.release.sli-support-chain.2025.v37.json"
CONCLUSION_RULE = "tax.us.2025.rule.sli-statement-loan-support"
REASON_RULE = "tax.us.2025.rule.sli-statement-support-reason"
STATEMENT_RULE_FILES = (
    "rule.sli-statement-inclusion-count.json",
    "rule.sli-statement-inclusion-unresolved-count.json",
    "rule.sli-statement-inclusion-withdrawn-count.json",
    "rule.sli-statement-applicability-marker-count.json",
    "rule.sli-statement-scope-unresolved-count.json",
    "rule.sli-statement-loan-support.json",
    "rule.sli-statement-support-reason.json",
)
QUESTIONS = {"loan": "loan-paid-only-school-costs", "enroll": "enrolled-at-least-half-time"}


def _load(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((CONTENT / name).read_text("utf-8"))
    return loaded


# ---------------------------------------------------------------------------
# A saved workspace built only through the recorder and review flow
# ---------------------------------------------------------------------------


class Workspace:
    """Two borrowings, two schoolings, two statements, recorded durably."""

    def __init__(self, *, relationship_bundle: dict[str, Any] | None = None) -> None:
        self.raw = tempfile.TemporaryDirectory(prefix="sli-track4-")
        schemas = DerivationSchemas()
        self.registry = install_domain_scoped_supersession(schemas.registry)
        self.log = ActLog(Path(self.raw.name) / "workspace", self.registry)
        bundle = relationship_bundle if relationship_bundle is not None else load_sli_relationship_source_bundle()
        for adopted in (_load("f1098e.bundle.json"), bundle):
            revision = self.log.read().revision
            self.log.append(act(revision, "bundle-adoption", {"bundle": adopted}), expected_revision=revision)
        self.borrowing = {"autumn": "demo.track4.borrowing.autumn", "spring": "demo.track4.borrowing.spring"}
        for name, reference in self.borrowing.items():
            introduce_borrowing_reference_durably(
                self.log, self.registry, reference_id=reference, description=f"{name.title()} study loan",
                actor=USER, at="2026-10-03T09:00:00Z")
        entities = [
            ("demo.track4.period.autumn24", "Autumn 2024", "tax.us.educational-period"),
            ("demo.track4.period.spring25", "Spring 2025", "tax.us.educational-period"),
            ("demo.track4.institution.river", "Riverside College", "tax.us.educational-institution"),
            ("demo.track4.programme.bsc", "BSc", "tax.us.educational-programme"),
            ("demo.track4.lender.cedar", "Cedar Servicing", "tax.us.student-loan-lender"),
            ("demo.track4.lender.birch", "Birch Servicing", "tax.us.student-loan-lender"),
            ("demo.track4.statement.cedar", "2025 Form 1098-E from Cedar", "tax.us.1098e-statement"),
            ("demo.track4.statement.birch", "2025 Form 1098-E from Birch", "tax.us.1098e-statement"),
        ]
        for identity, label, kind in entities:
            revision = self.log.read().revision
            self.log.append(act(revision, "entity-introduced", {"entity": demo_entity(identity, label, kind)}),
                            expected_revision=revision)
        self.school = {
            "autumn": track14._append_source(
                self.log, self.registry, SCHOOL,
                (("period", entities[0][0]), ("institution", entities[2][0]), ("programme", entities[3][0])),
                "Riverside College, BSc, autumn 2024", "track4-school-autumn"),
            "spring": track14._append_source(
                self.log, self.registry, SCHOOL,
                (("period", entities[1][0]), ("institution", entities[2][0]), ("programme", entities[3][0])),
                "Riverside College, BSc, spring 2025", "track4-school-spring"),
        }
        self.statement_keys = {
            "cedar": (("lender", entities[4][0]), ("statement", entities[6][0]), ("tax-year", "2025")),
            "birch": (("lender", entities[5][0]), ("statement", entities[7][0]), ("tax-year", "2025")),
        }
        self.statement = {
            "cedar": track14._append_source(self.log, self.registry, BOX1, self.statement_keys["cedar"],
                                            1250.0, "track4-statement-cedar"),
            "birch": track14._append_source(self.log, self.registry, BOX1, self.statement_keys["birch"],
                                            1800.0, "track4-statement-birch"),
        }
        self.claims: dict[tuple[str, str, str], str] = {}
        self._serial = 0

    def _name(self, tag: str) -> str:
        self._serial += 1
        return f"{tag}-{self._serial}"

    def _review(self, name: str) -> dict[str, Any]:
        from packages.tax.sli_relationship_review import prepare_review

        return prepare_review(self.log, self.registry, review_id=f"demo.track4.review.{name}",
                              shown_at="2026-10-03T10:00:00Z",
                              borrowing_refs=tuple(self.borrowing.values()),
                              schooling_fact_ids=tuple(self.school.values()),
                              statement_fact_ids=tuple(self.statement.values()))

    def _clause(self, kind: str, borrowing: str, target: str, response: str) -> dict[str, Any]:
        financing = kind == "financing"
        return {"borrowing_ref": self.borrowing[borrowing],
                "schooling_fact_id": self.school[target] if financing else None,
                "statement_fact_id": None if financing else self.statement[target],
                "financing_response": response if financing else "unanswered",
                "inclusion_response": "unanswered" if financing else response}

    def link(self, kind: str, borrowing: str, target: str, response: str = "yes") -> None:
        """Save one financing or statement-inclusion answer through the review."""
        from packages.tax.sli_relationship_review import save_review

        name = self._name(f"{kind}-{borrowing}-{target}-{response}")
        saved = save_review(self.log, self.registry, self._review(name),
                            **self._clause(kind, borrowing, target, response),
                            actor=USER, at="2026-10-03T10:01:00Z",
                            submission_id=f"demo.track4.submission.{name}",
                            evidence_id=f"demo.evidence.track4.{name}")
        if kind in saved["claims"]:
            self.claims[(kind, borrowing, target)] = saved["claims"][kind]["finding_id"]

    def outcome(self, kind: str, borrowing: str, target: str, outcome: str) -> None:
        """Answer cannot-tell or no on an affirmed link, or withdraw it."""
        from packages.tax.sli_relationship_review import answer_review_claim, withdraw_review_claim

        finding_id = self.claims.pop((kind, borrowing, target))
        if outcome == "withdrawn":
            withdraw_review_claim(self.log, self.registry, finding_id=finding_id, actor=USER,
                                  at="2026-10-03T10:02:00Z")
            return
        name = self._name(f"{kind}-{borrowing}-{target}-{outcome}")
        answer_review_claim(self.log, self.registry, finding_id=finding_id, review=self._review(name),
                            **self._clause(kind, borrowing, target, outcome),
                            actor=USER, at="2026-10-03T10:02:00Z",
                            submission_id=f"demo.track4.submission.{name}",
                            evidence_id=f"demo.evidence.track4.{name}")

    def answer(self, question: str, borrowing: str, response: str) -> None:
        """Answer one of the two ordinary borrowing questions."""
        from packages.tax.sli_relationship_review import (
            prepare_borrowing_answer_review,
            save_borrowing_answer_review,
        )

        name = self._name(f"{question}-{borrowing}-{response}")
        review = prepare_borrowing_answer_review(
            self.log, self.registry, review_id=f"demo.track4.review.{name}", shown_at="2026-10-03T10:00:00Z",
            borrowing_refs=tuple(self.borrowing.values()))
        save_borrowing_answer_review(
            self.log, self.registry, review, borrowing_ref=self.borrowing[borrowing],
            question=QUESTIONS[question], response=response, actor=USER, at="2026-10-03T10:03:00Z",
            submission_id=f"demo.track4.submission.{name}", evidence_id=f"demo.evidence.track4.{name}")

    def plain(self, borrowing: str = "autumn", school: str = "autumn", statement: str = "cedar") -> None:
        """One loan, one schooling, one statement, both answers yes."""
        self.link("financing", borrowing, school)
        self.link("statement-inclusion", borrowing, statement)
        self.answer("loan", borrowing, "yes")
        self.answer("enroll", borrowing, "yes")

    def retract_source(self, fact_id: str) -> str:
        """End the current finding of a source under ADR 0073; returns its finding id."""
        finding_id = str(track17._current_source_finding(self.acts(), self.registry, fact_id)["id"])
        revision = self.log.read().revision
        self.log.append(act(revision, "finding-retracted", {"finding_id": finding_id}), expected_revision=revision)
        return finding_id

    def adopt_v39(self) -> None:
        """The person adopts core calculations v39 through the v37 release."""
        package = json.loads(V39_PACKAGE.read_text("utf-8"))
        release = json.loads(V37_RELEASE.read_text("utf-8"))
        revision = self.log.read().revision
        item = act(revision, "package-adoption", {
            "package": {"id": package["id"], "version": package["version"],
                        "checksum": package["package_checksum"]},
            "release": {"id": release["id"], "version": release["version"],
                        "checksum": hashlib.sha256(V37_RELEASE.read_bytes()).hexdigest()},
            "scope": SCOPE, "revision": 1,
        })
        item["actor"] = USER
        self.log.append(item, expected_revision=revision)

    def doubt(self, statement: str) -> None:
        """The person names a statement but cannot tell which loan it covers."""
        from packages.tax.sli_relationship_review import save_review

        name = self._name(f"doubt-{statement}")
        save_review(self.log, self.registry, self._review(name), borrowing_ref=None,
                    schooling_fact_id=None, statement_fact_id=self.statement[statement],
                    financing_response="unanswered", inclusion_response="cannot-tell",
                    actor=USER, at="2026-10-03T10:04:00Z",
                    submission_id=f"demo.track4.submission.{name}", evidence_id=f"demo.evidence.track4.{name}")

    def unscoped_rewrite(self, statement: str, amount: float) -> None:
        """A box 1 rewrite written before the ADR 0077 Part 5 step existed."""
        track14._append_source(track17._pre_step_writer(self.log), self.registry, BOX1,
                               self.statement_keys[statement], amount, self._name(f"track4-unscoped-{statement}"))

    def reviewed_amount_only(self, statement: str, amount: float) -> None:
        from packages.tax.sli_relationship_review import apply_statement_correction_review

        name = self._name(f"amount-only-{statement}")
        apply_statement_correction_review(
            self.log, self.registry, review=self._review(name), statement_fact_id=self.statement[statement],
            scope="amount-only", borrowing_ref=None, finding_id=None, actor=USER, at="2026-10-03T10:05:00Z",
            submission_id=f"demo.track4.submission.{name}", evidence_id=f"demo.evidence.track4.{name}",
            corrected_box1_total=amount, source_correction_id=f"demo.track4.correction.{name}")

    def acts(self) -> tuple[dict[str, Any], ...]:
        """A fresh recovery of the saved log."""
        return ActLog(self.log.path.parent, self.registry).read().acts

    def inclusion_fact_id(self, borrowing: str, statement: str) -> str:
        return fact_id_for(INCL, self.statement_keys[statement] + (("borrowing", self.borrowing[borrowing]),))

    def current_finding(self, fact_type: str, keys: tuple[tuple[str, str], ...]) -> str:
        return str(track17._current_source_finding(self.acts(), self.registry, fact_id_for(fact_type, keys))["id"])


# ---------------------------------------------------------------------------
# Running the chain from a fresh recovery
# ---------------------------------------------------------------------------


def _slice_citizens() -> list[tuple[dict[str, Any], str]]:
    """The per-financing and per-inclusion rules with what they read."""
    citizens: list[tuple[dict[str, Any], str]] = [
        (_load("f1098e.bundle.json"), "fact-type-bundle"),
        (_load("sli-relationship-source.bundle.v2.json"), "fact-type-bundle"),
        (_load(SUPPORT_BUNDLE), "fact-type-bundle"),
        (_load("family.f1098e-1.json"), "source-family"),
        (_load("closure-mapping.f1098e.1.json"), "source-closure-mapping"),
    ]
    citizens.extend((_load(name), "parameter") for name in SLICE_PARAMETERS)
    citizens.extend((_load(name), "computation") for name in INCLUSION_RULE_FILES)
    return citizens


def _slice_package(citizens: list[tuple[dict[str, Any], str]]) -> dict[str, Any]:
    package: dict[str, Any] = {
        "schema": "artifact-package.v35",
        "id": "demo.package.track4-inclusion-chain",
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "admitted_schemas": sorted({citizen["schema"] for citizen, _role in citizens}),
        "members": [{"role": role, "schema": c["schema"], "id": c["id"], "version": c["version"]}
                    for c, role in citizens],
        "input_bindings": [],
        # A test-assembled package has no form field; every member is a root.
        "entrypoints": [{"id": c["id"], "version": c["version"]} for c, _role in citizens],
        "composition_obligations": [],
    }
    package["package_checksum"] = package_instance_checksum(package)
    return package


class _Graph:
    def __init__(self, resolved_members: Any, package: dict[str, Any]) -> None:
        self.resolved_members = resolved_members
        self.package = package


def run_inclusion_chain(acts: tuple[dict[str, Any], ...], run_id: str) -> tuple[RunResult, RunResult]:
    """Validate the slice, marshal the recovered state, run both runners."""
    schemas = DerivationSchemas()
    citizens = _slice_citizens()
    package = _slice_package(citizens)
    validation = validate_package(package, {(c["id"], c["version"]): c for c, _ in citizens}, schemas)
    if not validation.ok:
        raise AssertionError([issue.detail for issue in validation.issues])
    state = project(acts, schemas.registry)
    material = _resolved_run_material(_Graph(list(validation.resolved_members), package))
    rules, parameters, families, mappings, fact_types, bindings, collect_names = material
    context = marshal_run_context(
        run_id=run_id, state=state, currency=compute_currency(state), rules=rules, parameters=parameters,
        canon=load_canon(schemas), adoption_pin={"role": "adoption", "id": package["id"], "version": "v1"},
        governance_pins=[], family_declarations=families, closure_mappings=mappings, fact_types=fact_types,
        input_bindings=bindings, collect_source_names=collect_names,
        emission_only_source_names=list(material.emission_only_names),
        parameter_index=material.parameter_index,
        claim_applicability=current_claim_applicability(acts, schemas.registry),
    )
    return run(context, schemas), run_reference(context, schemas)


def run_v39(acts: tuple[dict[str, Any], ...], run_id: str) -> tuple[RunResult, RunResult]:
    """The adopted v39 graph through release resolution, as the coordinator marshals it."""
    schemas = DerivationSchemas()
    resolved = resolve_production_package(
        acts, run_scope=SCOPE, scope_user=USER, workspace_revision=len(acts),
        surface=PublicationSurface(RELEASE_DIR, V37_REGISTRY, CONTENT), schemas=schemas,
    )
    if isinstance(resolved, Refusal):
        raise AssertionError(f"core calculations v39 refused: {resolved!r}")
    if (resolved.package["id"], resolved.package["version"]) != (PACKAGE_ID, "v39"):
        raise AssertionError("resolver did not select core calculations v39")
    state = project(acts, schemas.registry)
    material = _resolved_run_material(resolved)
    rules, parameters, families, mappings, fact_types, bindings, collect_names = material
    authorization = _resolve_run_authorization(
        acts, run_scope=SCOPE, scope_user=USER, rules=rules,
        corpus={member["id"]: member for member in resolved.resolved_members}, package=resolved.package,
    )
    context = marshal_live_run_context(
        run_id=run_id, state=state, currency=compute_currency(state), rules=rules, parameters=parameters,
        canon=load_canon(schemas), adoption_pin={"role": "adoption", "id": PACKAGE_ID, "version": "v39"},
        governance_pins=[], family_declarations=families, closure_mappings=mappings, fact_types=fact_types,
        input_bindings=bindings, collect_source_names=collect_names,
        emission_only_source_names=list(material.emission_only_names), authorization=authorization,
        reporting_year=2025, parameter_index=material.parameter_index,
        claim_applicability=current_claim_applicability(acts, schemas.registry),
    )
    return run(context._context, schemas), run_reference(context._context, schemas)


def surface(result: RunResult) -> str:
    """Values, pins and blocked rows, without publication order."""
    published = sorted(json.dumps(pub.finding, sort_keys=True) for pub in result.publications)
    blocked = sorted(json.dumps(row, sort_keys=True) for row in result.blocked)
    dispositions = sorted(json.dumps(row, sort_keys=True) for row in result.dispositions)
    return json.dumps([published, blocked, dispositions])


def published(result: RunResult, symbol: str) -> dict[str, dict[str, Any]]:
    """Keyed publications of one per-subject symbol, by subject fact id."""
    rows: dict[str, dict[str, Any]] = {}
    for pub in result.publications:
        name, _, subject = str(pub.finding["symbol"]).partition("|")
        if name == symbol and subject:
            rows[subject] = pub.finding
    return rows


def blocks(result: RunResult, rule_id: str) -> dict[str, tuple[str, list[str]]]:
    return {str(row.get("subject_fact_id")): (row["code"], list(row["missing"]))
            for row in result.blocked if row["artifact_id"] == rule_id}


def pin_ids(finding: dict[str, Any]) -> set[str]:
    return {pin["id"] for pin in finding["pins"]}


# ---------------------------------------------------------------------------
# Slice 1: per financing link and per inclusion
# ---------------------------------------------------------------------------


class InclusionSupport(unittest.TestCase):
    def _run(self, ws: Workspace, tag: str) -> RunResult:
        forward, reference = run_inclusion_chain(ws.acts(), f"demo.run.track4.{tag}")
        self.assertEqual(surface(forward), surface(reference))
        return forward

    def _reason(self, ws: Workspace, result: RunResult, borrowing: str = "autumn",
                statement: str = "cedar") -> tuple[str, str]:
        """The inclusion's reason and its support, or the support's block."""
        incl = ws.inclusion_fact_id(borrowing, statement)
        support = published(result, SUPPORT).get(incl)
        if support is None:
            code, missing = blocks(result, SUPPORT_RULE)[incl]
            return (published(result, INCL_REASON)[incl]["value"], f"blocked {code} {' '.join(missing)}")
        return (published(result, INCL_REASON)[incl]["value"], support["value"])

    def test_plain_case_supports_and_pins_what_was_said(self) -> None:
        ws = Workspace()
        with ws.raw:
            ws.plain()
            result = self._run(ws, "plain")
            self.assertEqual(self._reason(ws, result), ("none", "1"))
            incl = ws.inclusion_fact_id("autumn", "cedar")
            reason = published(result, INCL_REASON)[incl]
            pins = pin_ids(reason)
            borrowing = (("borrowing", ws.borrowing["autumn"]),)
            # The inclusion, its current box 1 and both answers.
            self.assertIn(ws.claims[("statement-inclusion", "autumn", "cedar")], pins)
            self.assertIn(ws.current_finding(BOX1, ws.statement_keys["cedar"]), pins)
            self.assertIn(ws.current_finding(LOAN, borrowing), pins)
            self.assertIn(ws.current_finding(ENROLL, borrowing), pins)
            # Support pins the reason and the financing-schooling link.
            [link] = published(result, FIN_LINK).values()
            self.assertIn(link["id"], pin_ids(published(result, SUPPORT)[incl]))
            # The financing link pins the financing and the schooling it names.
            self.assertIn(ws.claims[("financing", "autumn", "autumn")], pin_ids(link))
            school = str(track17._current_source_finding(ws.acts(), ws.registry, ws.school["autumn"])["id"])
            self.assertIn(school, pin_ids(link))
            self.assertIn(reason["id"], pin_ids(published(result, SUPPORT)[incl]))

    def test_missing_answers_are_named_missing_never_no(self) -> None:
        for answered, expected in ((("enroll",), "loan-cost-answer-missing"),
                                   (("loan",), "enrollment-answer-missing"),
                                   ((), "loan-cost-answer-missing")):
            with self.subTest(answered=answered):
                ws = Workspace()
                with ws.raw:
                    ws.link("financing", "autumn", "autumn")
                    ws.link("statement-inclusion", "autumn", "cedar")
                    for question in answered:
                        ws.answer(question, "autumn", "yes")
                    self.assertEqual(self._reason(ws, self._run(ws, f"missing-{expected}")), (expected, "0"))

    def test_no_and_cannot_tell_answers_do_not_support(self) -> None:
        for question, label in (("loan", "loan-cost"), ("enroll", "enrollment")):
            for response in ("no", "cannot-tell"):
                with self.subTest(question=question, response=response):
                    ws = Workspace()
                    with ws.raw:
                        ws.link("financing", "autumn", "autumn")
                        ws.link("statement-inclusion", "autumn", "cedar")
                        ws.answer(question, "autumn", response)
                        other = "enroll" if question == "loan" else "loan"
                        ws.answer(other, "autumn", "yes")
                        self.assertEqual(self._reason(ws, self._run(ws, f"{question}-{response}")),
                                         (f"{label}-{response}", "0"))

    def test_two_schoolings_do_not_support(self) -> None:
        ws = Workspace()
        with ws.raw:
            ws.plain()
            ws.link("financing", "autumn", "spring")
            result = self._run(ws, "two-schoolings")
            self.assertEqual(self._reason(ws, result), ("more-than-one-schooling", "0"))

    def test_financing_outcomes_beside_a_remaining_affirmation(self) -> None:
        # Track 0d evidence 8: a second schooling's cannot-tell or withdrawal
        # keeps the loan out; an explicit no closes that pair and does not.
        for outcome, expected in (("cannot-tell", ("financing-cannot-tell", "0")),
                                  ("withdrawn", ("financing-withdrawn", "0")),
                                  ("no", ("none", "1"))):
            with self.subTest(outcome=outcome):
                ws = Workspace()
                with ws.raw:
                    ws.plain()
                    ws.link("financing", "autumn", "spring")
                    ws.outcome("financing", "autumn", "spring", outcome)
                    # Each schooling change ended the enrollment answer; it is given again.
                    ws.answer("enroll", "autumn", "yes")
                    self.assertEqual(self._reason(ws, self._run(ws, f"fin-{outcome}")), expected)

    def test_the_only_financing_cannot_tell_or_withdrawn_still_publishes_a_reason(self) -> None:
        # With no current financing there is no schooling link for support to
        # join; the reason is still published, and it is what the statement reads.
        no_link = f"blocked DEPENDENCY_ABSENT {FIN_LINK}"
        for outcome, expected in (("cannot-tell", "financing-cannot-tell"),
                                  ("withdrawn", "financing-withdrawn"),
                                  ("no", "no-schooling-link")):
            with self.subTest(outcome=outcome):
                ws = Workspace()
                with ws.raw:
                    ws.plain()
                    ws.outcome("financing", "autumn", "autumn", outcome)
                    self.assertEqual(self._reason(ws, self._run(ws, f"sole-fin-{outcome}")), (expected, no_link))

    def test_no_financing_link_is_a_missing_link(self) -> None:
        ws = Workspace()
        with ws.raw:
            ws.link("statement-inclusion", "autumn", "cedar")
            ws.answer("loan", "autumn", "yes")
            ws.answer("enroll", "autumn", "yes")
            self.assertEqual(self._reason(ws, self._run(ws, "no-financing")),
                             ("no-schooling-link", f"blocked DEPENDENCY_ABSENT {FIN_LINK}"))

    def test_a_stale_schooling_blocks_its_link_and_the_inclusion_support(self) -> None:
        ws = Workspace()
        with ws.raw:
            ws.plain()
            ws.retract_source(ws.school["autumn"])
            result = self._run(ws, "stale-schooling")
            financing = fact_id_for(FIN, (("borrowing", ws.borrowing["autumn"]),) + tuple(
                facts_of(project(ws.acts(), ws.registry).fact_state)[ws.school["autumn"]].keys))
            self.assertEqual(blocks(result, FIN_LINK_RULE), {financing: ("DEPENDENCY_ABSENT", [SCHOOL])})
            self.assertEqual(published(result, FIN_LINK), {})
            # Track 0f item 1: the stale-target join blocks; nothing supports.
            self.assertEqual(self._reason(ws, result), ("none", f"blocked DEPENDENCY_ABSENT {FIN_LINK}"))

    def test_an_unrelated_borrowing_is_unaffected(self) -> None:
        ws = Workspace()
        with ws.raw:
            ws.plain()
            ws.plain("spring", "spring", "birch")
            ws.outcome("financing", "autumn", "autumn", "withdrawn")
            result = self._run(ws, "unrelated")
            self.assertEqual(self._reason(ws, result),
                             ("financing-withdrawn", f"blocked DEPENDENCY_ABSENT {FIN_LINK}"))
            self.assertEqual(self._reason(ws, result, "spring", "birch"), ("none", "1"))
            spring = published(result, INCL_REASON)[ws.inclusion_fact_id("spring", "birch")]
            self.assertNotIn(ws.current_finding(LOAN, (("borrowing", ws.borrowing["autumn"]),)), pin_ids(spring))

    def test_a_second_loan_needs_its_own_answers(self) -> None:
        ws = Workspace()
        with ws.raw:
            ws.plain()
            ws.link("financing", "spring", "autumn")
            ws.link("statement-inclusion", "spring", "birch")
            ws.answer("loan", "spring", "yes")
            result = self._run(ws, "second-loan")
            self.assertEqual(self._reason(ws, result), ("none", "1"))
            self.assertEqual(self._reason(ws, result, "spring", "birch"), ("enrollment-answer-missing", "0"))


# ---------------------------------------------------------------------------
# Slice 2: per statement, adopted in core calculations v39
# ---------------------------------------------------------------------------


class StatementSupport(unittest.TestCase):
    def _run(self, ws: Workspace, tag: str) -> RunResult:
        forward, reference = run_v39(ws.acts(), f"demo.run.track4.{tag}")
        self.assertEqual(surface(forward), surface(reference))
        return forward

    def _statement(self, ws: Workspace, result: RunResult, statement: str = "cedar") -> tuple[str, str]:
        fact_id = ws.statement[statement]
        return (published(result, CONCLUSION)[fact_id]["value"], published(result, REASON)[fact_id]["value"])

    def _workspace(self) -> Workspace:
        ws = Workspace()
        ws.adopt_v39()
        return ws

    def test_plain_case_is_supported_with_its_basis_and_pins(self) -> None:
        ws = self._workspace()
        with ws.raw:
            ws.plain()
            result = self._run(ws, "statement-plain")
            self.assertEqual(self._statement(ws, result), ("plain-case-supported", "none"))
            conclusion = published(result, CONCLUSION)[ws.statement["cedar"]]
            pins = pin_ids(conclusion)
            incl = ws.inclusion_fact_id("autumn", "cedar")
            self.assertIn(ws.current_finding(BOX1, ws.statement_keys["cedar"]), pins)
            self.assertIn(ws.claims[("statement-inclusion", "autumn", "cedar")], pins)
            self.assertIn(published(result, SUPPORT)[incl]["id"], pins)
            self.assertIn(CONCLUSION_RULE, pins)
            # The rule the pin names declares the four basis groups.
            rule = _load("rule.sli-statement-loan-support.json")
            self.assertEqual(set(rule["basis"]), {"said", "derived", "assumed", "left_with_person"})
            self.assertTrue(rule["basis"]["assumed"] and rule["basis"]["left_with_person"])
            # A statement with no relationship claims is outside the case.
            self.assertEqual(self._statement(ws, result, "birch"), ("not-supported", "no-loan-link"))

    def test_every_current_statement_gets_a_result(self) -> None:
        ws = self._workspace()
        with ws.raw:
            result = self._run(ws, "statement-no-claims")
            self.assertEqual(set(published(result, CONCLUSION)), set(ws.statement.values()))
            self.assertEqual(set(published(result, REASON)), set(ws.statement.values()))
            self.assertEqual({value for value, _ in (self._statement(ws, result, name) for name in ws.statement)},
                             {"not-supported"})

    def test_mixed_scope_beside_an_unrelated_statement(self) -> None:
        # Track 0d evidence 8, after fresh recovery: the primary (Cedar) once
        # had a second link; the sibling (Birch) is plain throughout.
        cases = (
            ("financing", "cannot-tell", ("not-supported", "financing-cannot-tell")),
            ("financing", "no", ("plain-case-supported", "none")),
            ("financing", "withdrawn", ("not-supported", "financing-withdrawn")),
            ("statement-inclusion", "cannot-tell", ("not-supported", "inclusion-cannot-tell")),
            ("statement-inclusion", "no", ("plain-case-supported", "none")),
            ("statement-inclusion", "withdrawn", ("not-supported", "inclusion-withdrawn")),
            ("financing", "absence", ("plain-case-supported", "none")),
            ("statement-inclusion", "absence", ("plain-case-supported", "none")),
        )
        for kind, outcome, expected in cases:
            with self.subTest(kind=kind, outcome=outcome):
                ws = self._workspace()
                with ws.raw:
                    ws.plain()
                    ws.plain("spring", "spring", "birch")
                    if outcome != "absence":
                        if kind == "financing":
                            ws.link("financing", "autumn", "spring")
                            before = self._statement(ws, self._run(ws, f"mixed-{kind}-{outcome}-before"))
                            self.assertEqual(before, ("not-supported", "more-than-one-schooling"))
                            ws.outcome("financing", "autumn", "spring", outcome)
                            # Each schooling change ended the enrollment answer; it is given again.
                            ws.answer("enroll", "autumn", "yes")
                        else:
                            ws.link("statement-inclusion", "spring", "cedar")
                            before = self._statement(ws, self._run(ws, f"mixed-{kind}-{outcome}-before"))
                            self.assertEqual(before, ("not-supported", "more-than-one-loan"))
                            ws.outcome("statement-inclusion", "spring", "cedar", outcome)
                    result = self._run(ws, f"mixed-{kind}-{outcome}")
                    self.assertEqual(self._statement(ws, result), expected)
                    self.assertEqual(self._statement(ws, result, "birch"), ("plain-case-supported", "none"))

    def test_two_loans_and_two_schoolings(self) -> None:
        ws = self._workspace()
        with ws.raw:
            ws.plain()
            ws.plain("spring", "spring", "cedar")
            self.assertEqual(self._statement(ws, self._run(ws, "two-loans")), ("not-supported", "more-than-one-loan"))
        ws = self._workspace()
        with ws.raw:
            ws.plain()
            ws.link("financing", "autumn", "spring")
            self.assertEqual(self._statement(ws, self._run(ws, "two-schoolings-statement")),
                             ("not-supported", "more-than-one-schooling"))

    def test_missing_answers_reach_the_statement_as_missing(self) -> None:
        ws = self._workspace()
        with ws.raw:
            ws.link("financing", "autumn", "autumn")
            ws.link("statement-inclusion", "autumn", "cedar")
            ws.answer("loan", "autumn", "yes")
            self.assertEqual(self._statement(ws, self._run(ws, "statement-missing")),
                             ("not-supported", "enrollment-answer-missing"))
            ws.answer("enroll", "autumn", "no")
            self.assertEqual(self._statement(ws, self._run(ws, "statement-enroll-no")),
                             ("not-supported", "enrollment-no"))

    def test_the_person_cannot_tell_which_loan_the_statement_covers(self) -> None:
        ws = self._workspace()
        with ws.raw:
            ws.plain()
            ws.doubt("cedar")
            result = self._run(ws, "statement-doubt")
            # A later identified answer on Cedar ends the doubt; here none came.
            self.assertEqual(self._statement(ws, result), ("not-supported", "statement-loan-cannot-tell"))
        ws = self._workspace()
        with ws.raw:
            ws.doubt("cedar")
            ws.plain()
            self.assertEqual(self._statement(ws, self._run(ws, "statement-doubt-answered")),
                             ("plain-case-supported", "none"))

    def test_a_stale_schooling_blocks_the_statement_and_leaves_the_sibling(self) -> None:
        ws = self._workspace()
        with ws.raw:
            ws.plain()
            ws.plain("spring", "spring", "birch")
            ws.retract_source(ws.school["autumn"])
            result = self._run(ws, "statement-stale-schooling")
            # Track 0f item 1: the chain blocks rather than publishing a result.
            incl = track17._current_source_finding(ws.acts(), ws.registry, ws.inclusion_fact_id("autumn", "cedar"))
            self.assertNotIn(ws.statement["cedar"], published(result, CONCLUSION))
            self.assertEqual(blocks(result, CONCLUSION_RULE),
                             {ws.statement["cedar"]: ("DEPENDENCY_INVALID", [incl["id"]])})
            self.assertEqual(blocks(result, REASON_RULE),
                             {ws.statement["cedar"]: ("DEPENDENCY_ABSENT", [CONCLUSION])})
            self.assertEqual(self._statement(ws, result, "birch"), ("plain-case-supported", "none"))

    def test_a_stale_statement_publishes_nothing_for_it_and_leaves_the_sibling(self) -> None:
        ws = self._workspace()
        with ws.raw:
            ws.plain()
            ws.plain("spring", "spring", "birch")
            ws.retract_source(ws.statement["cedar"])
            result = self._run(ws, "statement-stale-statement")
            self.assertNotIn(ws.statement["cedar"], published(result, CONCLUSION))
            self.assertNotIn(ws.inclusion_fact_id("autumn", "cedar"), published(result, INCL_REASON))
            self.assertEqual(self._statement(ws, result, "birch"), ("plain-case-supported", "none"))

    def test_without_relationship_bundle_v2_a_claimed_statement_is_not_supported(self) -> None:
        # A v1-only workspace cannot record the two answers or any link outcome.
        v1 = _load("sli-relationship-source.bundle.json")
        ws = Workspace(relationship_bundle=v1)
        ws.adopt_v39()
        with ws.raw:
            ws.link("financing", "autumn", "autumn")
            ws.link("statement-inclusion", "autumn", "cedar")
            ws.link("financing", "autumn", "spring")
            ws.outcome("financing", "autumn", "spring", "withdrawn")
            result = self._run(ws, "statement-v1-only")
            self.assertEqual(self._statement(ws, result), ("not-supported", "loan-cost-answer-missing"))


class ApplicabilityMarker(unittest.TestCase):
    """ADR 0077 Part 5 replay: an omitted inclusion refuses its own statement."""

    def _statement(self, ws: Workspace, result: RunResult, statement: str = "cedar") -> tuple[str, str]:
        fact_id = ws.statement[statement]
        return (published(result, CONCLUSION)[fact_id]["value"], published(result, REASON)[fact_id]["value"])

    def _run(self, ws: Workspace, tag: str) -> RunResult:
        forward, reference = run_v39(ws.acts(), f"demo.run.track4.{tag}")
        self.assertEqual(surface(forward), surface(reference))
        return forward

    def test_sole_omitted_link(self) -> None:
        ws = Workspace()
        ws.adopt_v39()
        with ws.raw:
            ws.plain()
            ws.plain("spring", "spring", "birch")
            a = ws.claims[("statement-inclusion", "autumn", "cedar")]
            ws.unscoped_rewrite("cedar", 1900.0)
            result = self._run(ws, "marker-sole")
            self.assertEqual(self._statement(ws, result), ("not-supported", "applicability-unestablished"))
            conclusion = published(result, CONCLUSION)[ws.statement["cedar"]]
            self.assertIn(a, pin_ids(conclusion))
            self.assertIn(ws.current_finding(BOX1, ws.statement_keys["cedar"]), pin_ids(conclusion))
            self.assertNotIn(ws.inclusion_fact_id("autumn", "cedar"), published(result, INCL_REASON))
            self.assertEqual(self._statement(ws, result, "birch"), ("plain-case-supported", "none"))
            # The reviewed route re-binds the inclusion and the plain case returns.
            ws.reviewed_amount_only("cedar", 1950.0)
            self.assertEqual(self._statement(ws, self._run(ws, "marker-sole-reviewed")),
                             ("plain-case-supported", "none"))

    def test_owners_mixed_case(self) -> None:
        ws = Workspace()
        ws.adopt_v39()
        with ws.raw:
            ws.plain()
            a = ws.claims[("statement-inclusion", "autumn", "cedar")]
            ws.unscoped_rewrite("cedar", 1800.0)
            # B is confirmed against the new box 1 and is fully plain by itself.
            ws.link("financing", "spring", "spring")
            ws.link("statement-inclusion", "spring", "cedar")
            ws.answer("loan", "spring", "yes")
            ws.answer("enroll", "spring", "yes")
            result = self._run(ws, "marker-mixed")
            self.assertEqual(published(result, INCL_REASON)[ws.inclusion_fact_id("spring", "cedar")]["value"], "none")
            self.assertEqual(self._statement(ws, result), ("not-supported", "applicability-unestablished"))
            self.assertIn(a, pin_ids(published(result, CONCLUSION)[ws.statement["cedar"]]))
            # Re-bound by the reviewed route, the statement holds two loans.
            ws.reviewed_amount_only("cedar", 1850.0)
            self.assertEqual(self._statement(ws, self._run(ws, "marker-mixed-reviewed")),
                             ("not-supported", "more-than-one-loan"))


class Publication(unittest.TestCase):
    def test_v39_and_registry_v37_add_only_new_entries(self) -> None:
        v38 = json.loads(V38_PACKAGE.read_text("utf-8"))
        v39 = json.loads(V39_PACKAGE.read_text("utf-8"))
        self.assertEqual(v39["package_checksum"], package_instance_checksum(v39))
        self.assertEqual((v39["schema"], v39["version"]), ("artifact-package.v35", "v39"))
        self.assertLessEqual({(m["id"], m["version"]) for m in v38["members"]},
                             {(m["id"], m["version"]) for m in v39["members"]})
        added = {(m["id"], m["version"]) for m in v39["members"]} - {(m["id"], m["version"]) for m in v38["members"]}
        new_rules = {(_load(name)["id"], "v1") for name in (*INCLUSION_RULE_FILES, *STATEMENT_RULE_FILES)}
        self.assertEqual(added, new_rules | {
            ("tax.us.2025.sli-relationship-source", "v2"), ("tax.us.2025.sli-support-chain", "v1"),
            ("tax.us.2025.parameter.sli-statement-support-no-inclusion", "v1")})
        old = json.loads(V36_REGISTRY.read_text("utf-8"))
        new = json.loads(V37_REGISTRY.read_text("utf-8"))
        for section in ("citizens", "packages"):
            self.assertEqual(new[section][:len(old[section])], old[section])
        by_key = {(row["id"], row["version"]): row["checksum"] for row in new["citizens"]}
        for name in (*INCLUSION_RULE_FILES, *STATEMENT_RULE_FILES, SUPPORT_BUNDLE, *SLICE_PARAMETERS,
                     "sli-relationship-source.bundle.v2.json"):
            citizen = _load(name)
            self.assertEqual(by_key[(citizen["id"], citizen["version"])], citizen_checksum(citizen))
        release = json.loads(V37_RELEASE.read_text("utf-8"))
        self.assertEqual(release["package_registry_sha256"], hashlib.sha256(V37_REGISTRY.read_bytes()).hexdigest())

    def test_existing_package_results_are_unchanged(self) -> None:
        """v38's every result is in v39 unchanged, run over the same saved workspace."""
        ws = Workspace()
        with ws.raw:
            ws.plain()
            ws.plain("spring", "spring", "birch")
            acts = ws.acts()
            corpus: dict[tuple[str, str], dict[str, Any]] = {}
            for path in CONTENT.glob("*.json"):
                body = json.loads(path.read_text("utf-8"))
                if isinstance(body, dict) and isinstance(body.get("id"), str) and isinstance(body.get("version"), str):
                    corpus[(body["id"], body["version"])] = body
            results = {}
            for path in (V38_PACKAGE, V39_PACKAGE):
                package = json.loads(path.read_text("utf-8"))
                validation = validate_package(package, corpus, DerivationSchemas())
                self.assertTrue(validation.ok, [issue.detail for issue in validation.issues])
                results[package["version"]] = _run_graph(acts, package, list(validation.resolved_members))
            new_rules = {_load(name)["id"] for name in (*INCLUSION_RULE_FILES, *STATEMENT_RULE_FILES)}
            v38_rows, v39_rows = (_rows(results[version]) for version in ("v38", "v39"))
            self.assertTrue(v38_rows)
            self.assertLessEqual(v38_rows, v39_rows)
            for row in v39_rows - v38_rows:
                kind, body = json.loads(row)
                owner = body.get("artifact_id") if kind != "publication" else str(body["symbol"]).partition("|")[0]
                self.assertTrue(owner in new_rules or str(owner).startswith("tax.us.2025.sli."), row)


def _run_graph(acts: tuple[dict[str, Any], ...], package: dict[str, Any], members: list[Any]) -> RunResult:
    """One package over one recovered state, with a shared adoption pin."""
    schemas = DerivationSchemas()
    state = project(acts, schemas.registry)
    material = _resolved_run_material(_Graph(members, package))
    rules, parameters, families, mappings, fact_types, bindings, collect_names = material
    context = marshal_run_context(
        run_id="demo.run.track4.compare", state=state, currency=compute_currency(state), rules=rules,
        parameters=parameters, canon=load_canon(schemas),
        adoption_pin={"role": "adoption", "id": "demo.package.track4-compare", "version": "v1"},
        governance_pins=[], family_declarations=families, closure_mappings=mappings, fact_types=fact_types,
        input_bindings=bindings, collect_source_names=collect_names,
        emission_only_source_names=list(material.emission_only_names),
        parameter_index=material.parameter_index,
        claim_applicability=current_claim_applicability(acts, schemas.registry),
    )
    forward, reference = run(context, schemas), run_reference(context, schemas)
    if surface(forward) != surface(reference):
        raise AssertionError("runners disagree")
    return forward


def _rows(result: RunResult) -> set[str]:
    rows = {json.dumps(["publication", pub.finding], sort_keys=True) for pub in result.publications}
    rows |= {json.dumps(["blocked", row], sort_keys=True) for row in result.blocked}
    rows |= {json.dumps(["disposition", row], sort_keys=True) for row in result.dispositions}
    return rows


if __name__ == "__main__":
    unittest.main()
