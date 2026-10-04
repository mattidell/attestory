"""Track 1e (second half): replay omission and the applicability marker.

ADR 0077 Part 5, "Replay of a history that already holds the rewrite". A log
written before the new-write step, or by a test-only log, can hold an unscoped
box 1 rewrite while an old inclusion is current. ``marshal_run_context`` omits
every current statement inclusion that ``current_claim_applicability`` does
not report ``current`` and supplies one system marker source in its place,
keyed by the inclusion's identity and pinning the inclusion's finding. The box
1 finding stays. Every start state is built with the real recorder, a
test-only log for the unscoped write, and fresh recovery.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

import packages.derivation.live as live_module
from packages.derivation.live import (
    _resolve_run_authorization,
    _resolved_run_material,
    live_coordinate_run,
)
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.marshal import marshal_live_run_context
from packages.derivation.production_resolver import PublicationSurface, Refusal, resolve_production_package
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import RunContext, SourceFact, run
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for, facts_of
from packages.kernel.findings import project
from packages.tax.loader import install_domain_scoped_supersession
from packages.tax.sli_relationship_recording import (
    INCLUSION_APPLICABILITY_UNESTABLISHED,
    SCHOOLING,
    STATEMENT_INCLUSION,
    STATEMENT_TYPE,
    current_claim_applicability,
    introduce_borrowing_reference_durably,
    record_submission_durably,
)
from packages.tax.sli_relationship_review import apply_statement_correction_review, prepare_review
import tests.test_sli_relationship_recording as track14
import tests.test_sli_track17_relationship_applicability as track17
from tests.support import act, demo_entity

ROOT = Path(__file__).resolve().parents[1]
USER = track17.USER
SCOPE = track17.SCOPE
MARKER = INCLUSION_APPLICABILITY_UNESTABLISHED
MARKER_VALUE = "sli.statement-inclusion.applicability-unestablished"
FIRST_STATEMENT_KEYS = (("lender", "demo.track14.lender.cedar"),
                        ("statement", "demo.track14.statement.2025"), ("tax-year", "2025"))
BOX2 = "tax.us.2025.f1098e.box2-checked-authority"


def _coordinator_scenario() -> tuple[tempfile.TemporaryDirectory[str], ActLog, Any, dict[str, Any]]:
    """Two statements with their box 2 companions, one inclusion each.

    The production coordinator installs the domain companion-presence map, so
    every box 1 needs its box 2 companion first. Otherwise this is the Track
    17 scenario: the real recorder, a real ActLog.
    """
    raw = tempfile.TemporaryDirectory(prefix="sli-track1e2-")
    schemas = DerivationSchemas()
    install_domain_scoped_supersession(schemas.registry)
    registry = schemas.registry
    log = ActLog(Path(raw.name) / "workspace", registry)
    for name in ("f1098e.bundle.json", "sli-relationship-source.bundle.json"):
        revision = log.read().revision
        bundle = json.loads((track14.CONTENT / name).read_text("utf-8"))
        log.append(act(revision, "bundle-adoption", {"bundle": bundle}), expected_revision=revision)
    subjects: dict[str, Any] = {}
    for tag, amount in (("first", 1250.0), ("second", 850.0)):
        borrowing = f"demo.track1e2.borrowing.{tag}"
        introduce_borrowing_reference_durably(
            log, registry, reference_id=borrowing, description=f"{tag} study borrowing",
            actor=USER, at="2026-10-02T11:00:00Z",
        )
        entities = [
            (f"demo.track1e2.period.{tag}", "Autumn 2024", "tax.us.educational-period"),
            (f"demo.track1e2.institution.{tag}", "Riverside College", "tax.us.educational-institution"),
            (f"demo.track1e2.programme.{tag}", "BSc", "tax.us.educational-programme"),
            (f"demo.track1e2.lender.{tag}", "Cedar Servicing", "tax.us.student-loan-lender"),
            (f"demo.track1e2.statement.{tag}", "2025 Form 1098-E", "tax.us.1098e-statement"),
        ]
        for identity, label, kind in entities:
            revision = log.read().revision
            log.append(act(revision, "entity-introduced", {"entity": demo_entity(identity, label, kind)}),
                       expected_revision=revision)
        school = track14._append_source(
            log, registry, SCHOOLING,
            (("period", entities[0][0]), ("institution", entities[1][0]), ("programme", entities[2][0])),
            f"Riverside College, BSc, {tag}", f"track1e2-{tag}-school",
        )
        statement_keys = (("lender", entities[3][0]), ("statement", entities[4][0]), ("tax-year", "2025"))
        track14._append_source(log, registry, BOX2, statement_keys, False, f"track1e2-{tag}-box2")
        statement = track14._append_source(log, registry, STATEMENT_TYPE, statement_keys, amount,
                                           f"track1e2-{tag}-box1")
        claims = record_submission_durably(log, {
            "submission_id": f"demo.track1e2.answer.{tag}",
            "evidence_id": f"demo.evidence.track1e2.answer.{tag}",
            "actor": USER, "at": "2026-10-02T11:01:00Z", "borrowing_ref": borrowing,
            "schooling_fact_id": school, "statement_fact_id": statement,
            "financing_response": "yes", "inclusion_response": "yes", "interest_portion_response": "unknown",
        }, registry)["claims"]
        subjects[tag] = {"borrowing": borrowing, "school": school, "statement": statement,
                         "statement_keys": statement_keys, **claims}
    track17._append_adoption(log, registry, track17.V35_PACKAGE, track17.V35_RELEASE)
    return raw, log, registry, subjects


def _surface() -> PublicationSurface:
    return PublicationSurface(track17.FIXTURE / "publication_surface/releases", track17.V35_REGISTRY,
                              ROOT / "packages")


def _context(acts: tuple[dict[str, Any], ...], run_id: str, *, applicability: bool = True) -> RunContext:
    """Marshal the adopted v35 graph from recovered acts, as the coordinator does.

    ``applicability=False`` is the comparison without the replay rule: the
    reading reports every current claim ``current``, so every inclusion is
    joined. (Marshalling a current inclusion with no reading is refused.)
    """
    schemas = DerivationSchemas()
    resolved = resolve_production_package(
        acts, run_scope=SCOPE, scope_user=USER, workspace_revision=len(acts),
        surface=_surface(), schemas=schemas,
    )
    if isinstance(resolved, Refusal):
        raise AssertionError(f"v35 relationship package refused: {resolved!r}")
    state = project(acts, schemas.registry)
    currency = compute_currency(state)
    material = _resolved_run_material(resolved)
    rules, parameters, families, mappings, fact_types, bindings, collect_names = material
    authorization = _resolve_run_authorization(
        acts, run_scope=SCOPE, scope_user=USER, rules=rules,
        corpus={member["id"]: member for member in resolved.resolved_members},
        package=resolved.package,
    )
    rows = current_claim_applicability(acts, schemas.registry)
    if not applicability:
        rows = [dict(row, applicability="current") for row in rows]
    context = marshal_live_run_context(
        run_id=run_id, state=state, currency=currency, rules=rules, parameters=parameters,
        canon=load_canon(schemas),
        adoption_pin={"role": "adoption", "id": track17.PACKAGE_ID, "version": "v3"},
        governance_pins=[], family_declarations=families, closure_mappings=mappings,
        fact_types=fact_types, input_bindings=bindings, collect_source_names=collect_names,
        emission_only_source_names=list(material.emission_only_names),
        authorization=authorization, reporting_year=2025,
        parameter_index=material.parameter_index,
        claim_applicability=rows,
    )
    return context._context


def _recovered(log: ActLog, registry: Any) -> tuple[dict[str, Any], ...]:
    return ActLog(log.path.parent, registry).read().acts


def _markers(context: RunContext) -> list[SourceFact]:
    return [source for source in context.sources if source.name == MARKER]


def _source_ids(context: RunContext, name: str) -> set[str]:
    return {source.finding_id for source in context.sources if source.name == name}


def _keys(acts: tuple[dict[str, Any], ...], registry: Any, fact_id: str) -> tuple[tuple[str, str], ...]:
    return tuple(facts_of(project(acts, registry).fact_state)[fact_id].keys)


def _current_statement_id(acts: tuple[dict[str, Any], ...], registry: Any, fact_id: str) -> str:
    return str(track17._current_source_finding(acts, registry, fact_id)["id"])


class ReplayMarker(unittest.TestCase):
    def _unscoped_rewrite(self) -> tuple[tempfile.TemporaryDirectory[str], ActLog, Any, dict[str, Any]]:
        """Two statements, each with its own inclusion; the first gets an unscoped 1800."""
        raw, log, registry, subjects = track17.Track17RelationshipApplicability()._scenario()
        track17._append_adoption(log, registry, track17.V35_PACKAGE, track17.V35_RELEASE)
        subjects["before"] = _recovered(log, registry)
        # ADR 0077 Part 5 refuses this on the recorder's log; a history written
        # before the step holds it.
        track14._append_source(track17._pre_step_writer(log), registry, STATEMENT_TYPE,
                               FIRST_STATEMENT_KEYS, 1800.0, "track1e2-unscoped-1800")
        return raw, log, registry, subjects

    def _assert_marker_for(self, marker: SourceFact, inclusion: dict[str, str],
                           acts: tuple[dict[str, Any], ...], registry: Any) -> None:
        keys = _keys(acts, registry, inclusion["fact_id"])
        self.assertEqual(marker.finding_id, inclusion["finding_id"])
        self.assertEqual(marker.value, MARKER_VALUE)
        self.assertEqual(marker.keys, keys)
        self.assertEqual(marker.fact_id, fact_id_for(MARKER, keys))

    def _assert_only_omission_changed(self, with_rule: RunContext, without_rule: RunContext,
                                      omitted: set[str]) -> None:
        """Nothing but the omitted inclusions and their markers differs."""
        self.assertEqual(with_rule.inputs, without_rule.inputs)
        kept = [source for source in without_rule.sources if source.finding_id not in omitted]
        self.assertEqual([source for source in with_rule.sources if source.name != MARKER], kept)
        self.assertEqual({source.finding_id for source in _markers(with_rule)}, omitted)
        self.assertEqual(_markers(without_rule), [])

    def test_owners_mixed_case_marks_a_and_keeps_b(self) -> None:
        raw, log, registry, subjects = self._unscoped_rewrite()
        with raw:
            first, second = subjects["first"], subjects["second"]
            b = record_submission_durably(log, {
                "submission_id": "demo.track1e2.answer.b-on-first",
                "evidence_id": "demo.evidence.track1e2.answer.b-on-first",
                "actor": USER, "at": "2026-10-02T12:00:00Z",
                "borrowing_ref": second["borrowing"], "schooling_fact_id": second["school"],
                "statement_fact_id": first["statement"], "financing_response": "unanswered",
                "inclusion_response": "yes", "interest_portion_response": "unknown",
            }, registry)["claims"]["statement-inclusion"]
            acts = _recovered(log, registry)
            a = first["statement-inclusion"]
            applicability = {row["finding_id"]: row["applicability"]
                             for row in current_claim_applicability(acts, registry)}
            self.assertEqual(applicability[a["finding_id"]], "unresolved-applicability")
            self.assertEqual(applicability[b["finding_id"]], "current")

            context = _context(acts, "demo.track1e2.mixed")
            markers = _markers(context)
            self.assertEqual(len(markers), 1)
            self._assert_marker_for(markers[0], a, acts, registry)
            inclusions = _source_ids(context, STATEMENT_INCLUSION)
            self.assertNotIn(a["finding_id"], inclusions)
            self.assertIn(b["finding_id"], inclusions)
            self.assertIn(second["statement-inclusion"]["finding_id"], inclusions)
            # The box 1 finding stays: the unscoped 1800 is still read.
            box1 = _current_statement_id(acts, registry, first["statement"])
            self.assertIn(box1, {source.finding_id for source in context.sources} |
                          {item.finding_id for item in context.inputs})
            self._assert_only_omission_changed(
                context, _context(acts, "demo.track1e2.mixed", applicability=False), {a["finding_id"]})

            forward, reference = run(context, DerivationSchemas()), run_reference(context, DerivationSchemas())
            self.assertEqual(track17._surface(forward), track17._surface(reference))
            published = track17._published(forward)
            self.assertNotIn(f"{track17.INCLUSION_OUTPUT}|{a['fact_id']}", published)
            self.assertIn(f"{track17.INCLUSION_OUTPUT}|{b['fact_id']}", published)

    def test_sole_omitted_link_and_unrelated_statement_unchanged(self) -> None:
        raw, log, registry, subjects = self._unscoped_rewrite()
        with raw:
            first, second = subjects["first"], subjects["second"]
            a, other = first["statement-inclusion"], second["statement-inclusion"]
            before = _context(subjects["before"], "demo.track1e2.sole.before")
            acts = _recovered(log, registry)
            context = _context(acts, "demo.track1e2.sole")
            markers = _markers(context)
            self.assertEqual(len(markers), 1)
            self._assert_marker_for(markers[0], a, acts, registry)
            self.assertNotIn(a["finding_id"], _source_ids(context, STATEMENT_INCLUSION))
            self._assert_only_omission_changed(
                context, _context(acts, "demo.track1e2.sole", applicability=False), {a["finding_id"]})

            # The unrelated statement: its inclusion and box 1 are the same sources.
            def unrelated(ctx: RunContext) -> list[SourceFact]:
                return [source for source in ctx.sources
                        if source.finding_id == other["finding_id"]
                        or source.fact_id == second["statement"]]
            self.assertTrue(unrelated(context))
            self.assertEqual(unrelated(context), unrelated(before))
            self.assertEqual(_markers(before), [])

            forward, reference = run(context, DerivationSchemas()), run_reference(context, DerivationSchemas())
            self.assertEqual(track17._surface(forward), track17._surface(reference))
            published = track17._published(forward)
            before_published = track17._published(run(before, DerivationSchemas()))
            other_symbol = f"{track17.INCLUSION_OUTPUT}|{other['fact_id']}"
            self.assertNotIn(f"{track17.INCLUSION_OUTPUT}|{a['fact_id']}", published)
            self.assertEqual(published[other_symbol], before_published[other_symbol])

    def test_reviewed_correction_rebinds_a_and_no_marker_remains(self) -> None:
        raw, log, registry, subjects = self._unscoped_rewrite()
        with raw:
            first, second = subjects["first"], subjects["second"]
            a = first["statement-inclusion"]
            self.assertEqual(len(_markers(_context(_recovered(log, registry), "demo.track1e2.pre"))), 1)
            review = prepare_review(
                log, registry, review_id="demo.track1e2.review.amount-only",
                shown_at="2026-10-02T12:10:00Z", borrowing_refs=(first["borrowing"],),
                schooling_fact_ids=(first["school"],), statement_fact_ids=(first["statement"],),
            )
            apply_statement_correction_review(
                log, registry, review=review, statement_fact_id=first["statement"],
                scope="amount-only", borrowing_ref=None, finding_id=None, actor=USER,
                at="2026-10-02T12:11:00Z", submission_id="demo.track1e2.amount-only-scope",
                evidence_id="demo.evidence.track1e2.amount-only-scope",
                corrected_box1_total=1850.0, source_correction_id="demo.track1e2.amount-only-correction",
            )
            acts = _recovered(log, registry)
            applicability = {row["finding_id"]: row["applicability"]
                             for row in current_claim_applicability(acts, registry)}
            self.assertEqual(applicability[a["finding_id"]], "current")
            context = _context(acts, "demo.track1e2.reviewed")
            self.assertEqual(_markers(context), [])
            self.assertIn(a["finding_id"], _source_ids(context, STATEMENT_INCLUSION))
            self.assertEqual(context, _context(acts, "demo.track1e2.reviewed", applicability=False))
            published = track17._published(run(context, DerivationSchemas()))
            self.assertIn(f"{track17.INCLUSION_OUTPUT}|{a['fact_id']}", published)
            self.assertIn(f"{track17.INCLUSION_OUTPUT}|{second['statement-inclusion']['fact_id']}", published)

    def test_workspace_without_relationship_claims_marshals_identically(self) -> None:
        raw, log, registry, refs = track14.OrdinaryRelationshipRecording()._workspace()
        with raw:
            track17._append_adoption(log, registry, track17.V35_PACKAGE, track17.V35_RELEASE)
            # No dependent names the statement, so the recorder's log admits it.
            track14._append_source(log, registry, STATEMENT_TYPE, FIRST_STATEMENT_KEYS, 1410.0,
                                   "track1e2-no-claims-1410")
            acts = _recovered(log, registry)
            self.assertEqual([row for row in current_claim_applicability(acts, registry)
                              if row["relationship_type"] == STATEMENT_INCLUSION], [])
            with_rule = _context(acts, "demo.track1e2.no-claims")
            without_rule = _context(acts, "demo.track1e2.no-claims", applicability=False)
            self.assertEqual(with_rule, without_rule)
            self.assertEqual(_markers(with_rule), [])

    def test_coordinator_marshals_the_same_sources_for_both_runners(self) -> None:
        raw, log, registry, subjects = _coordinator_scenario()
        with raw:
            first = subjects["first"]
            a = first["statement-inclusion"]
            track14._append_source(track17._pre_step_writer(log), registry, STATEMENT_TYPE,
                                   first["statement_keys"], 1800.0, "track1e2-coordinator-unscoped-1800")
            acts = _recovered(log, registry)
            direct = _context(acts, "demo.track1e2.coordinator")
            captured: list[Any] = []

            def spy(**kwargs: Any) -> Any:
                marshalled = marshal_live_run_context(**kwargs)
                captured.append(marshalled._context)
                return marshalled

            with mock.patch.object(live_module, "marshal_live_run_context", side_effect=spy), \
                    tempfile.TemporaryDirectory(prefix="track1e2-live-") as work:
                outcome = live_coordinate_run(
                    WorkspaceCapability(Path(work) / "workspace"), repo_root=ROOT,
                    authoritative_acts=acts, workspace_revision=len(acts), run_scope=SCOPE,
                    scope_user=USER, request={"schema": "run-request.v1"},
                    run_id="demo.track1e2.coordinator", governance_pins=[], surface=_surface(),
                    output_name="track1e2-coordinator.json",
                )
            self.assertIsNone(outcome.refusal)
            self.assertEqual(len(captured), 1)
            coordinated = captured[0]
            self.assertEqual(coordinated.sources, direct.sources)
            self.assertEqual(coordinated.inputs, direct.inputs)
            self.assertEqual([marker.finding_id for marker in _markers(coordinated)], [a["finding_id"]])
            forward, reference = run(coordinated, DerivationSchemas()), run_reference(coordinated, DerivationSchemas())
            self.assertEqual(track17._surface(forward), track17._surface(reference))
            assert outcome.publications is not None
            self.assertNotIn(f"{track17.INCLUSION_OUTPUT}|{a['fact_id']}",
                             {row.finding["symbol"] for row in outcome.publications})


if __name__ == "__main__":
    unittest.main()
