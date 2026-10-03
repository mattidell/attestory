"""Track 5: Schedule 1 line 21 follows the per-statement support results.

The 2025 Student Loan Interest Deduction Worksheet becomes an ADR 0077 Part 4
presence selection (``tax.us.2025.rule.sli-worksheet`` v2). The yes/no path
keeps v1's arithmetic over the five older answers, now read per statement with
coverage, so one statement's yes no longer lets another statement with no
answer through (the Track 0a fail-open fix). The loan-link path is the same
arithmetic gated on every current statement's support standing. Both present
refuses; neither publishes 0 for a closed empty family and refuses otherwise.

Every case here starts from a saved workspace with a full synthetic return:
the relationships are recorded through the real recorder and review flow,
the log is recovered fresh, and the run goes through package validation and
marshalling with the replay applicability reading. Forward and reference
runners must agree.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

import pytest

import packages.derivation.live as live_module
from packages.derivation.live import (
    _resolve_run_authorization,
    _resolved_run_material,
    _statement_inclusion_applicability,
    live_coordinate_run,
)
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas, load_canon, workspace_registry
from packages.derivation.marshal import marshal_live_run_context
from packages.derivation.package_validation import package_instance_checksum, validate_package
from packages.derivation.presentation_projection import build_presentation_model
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import RunResult, run
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for
from packages.kernel.findings import project
from packages.tax.loader import install_domain_scoped_supersession, load_sli_relationship_source_bundle
from packages.tax.sli_relationship_recording import introduce_borrowing_reference_durably
import tests.test_sli_relationship_recording as track14
import tests.test_sli_track4_support_chain as track4
from tests.support import act, demo_entity

# Integration by construction: every case builds a full synthetic return in a
# saved ActLog and runs the whole core calculations package on both runners.
pytestmark = pytest.mark.live

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
USER = track4.USER
SCOPE = track4.SCOPE

BOX1 = track4.BOX1
BOX2 = "tax.us.2025.f1098e.box2-checked-authority"
FAMILY = "tax.us.2025.f1098e.1"
LINE21 = "tax.us.2025.schedule1.line21-sli-deduction"
WORKSHEET = "tax.us.2025.rule.sli-worksheet"
STANDING = "tax.us.2025.sli.statement-line21-standing"
STANDING_RULE = "tax.us.2025.rule.sli-statement-line21-standing"
BOTH_TOKEN = "old-and-new-sli-inputs-both-present"
ANSWER_TAILS = (
    "no-related-person-interest",
    "no-qualified-employer-plan-interest",
    "no-non-qualified-loan-component",
    "no-employer-educational-assistance-interest",
    "no-qtp-earnings-used",
)
STATUS = {tail: f"tax.us.2025.sli.answer-status.{tail}" for tail in ANSWER_TAILS}
STATUS_RULE = {tail: f"tax.us.2025.rule.sli-answer-status-{tail}" for tail in ANSWER_TAILS}
TRACK5_FILES = (
    "sli-worksheet-inputs.bundle.json",
    *(f"rule.sli-answer-status-{tail}.json" for tail in ANSWER_TAILS),
    "rule.sli-statement-line21-standing.json",
)
WORKSHEET_V3 = "rule.sli-worksheet.v3.json"
V38_PACKAGE = CONTENT / "package.core-calculations.v38.json"
V40_PACKAGE = CONTENT / "package.core-calculations.v40.json"
V38_REGISTRY = CONTENT / "published-packages.v38.json"
RELEASE_DIR = ROOT / "packages" / "sample_data" / "student_loan_worksheet_integration" / "publication_surface" / "releases"
V38_RELEASE = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v38.json"
REPLACED = "no-non-qualified-loan-component"
COMMON = tuple(tail for tail in ANSWER_TAILS if tail != REPLACED)


def _load(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((CONTENT / name).read_text("utf-8"))
    return loaded


# ---------------------------------------------------------------------------
# A saved workspace: a full synthetic return plus recorded relationships
# ---------------------------------------------------------------------------

_BASES: dict[tuple[Any, ...], Path] = {}
_BASE_ROOT = tempfile.TemporaryDirectory(prefix="sli-track5-bases-")


def _registry() -> Any:
    return install_domain_scoped_supersession(workspace_registry())


def _base_log(wages: float, bundle_version: str, amounts: tuple[tuple[str, float], ...]) -> Path:
    """Build (once per process) the saved return every case starts from.

    A synthetic return whose total income is the wages; the Form 1098-E
    family closed on its genesis horizon; the relationship bundle; two
    borrowings, two schoolings and the named statements, each box 1 with its
    box 2 companion first. Cases copy the saved log and record from there.
    """
    key = (wages, bundle_version, amounts)
    if key in _BASES:
        return _BASES[key]
    from tests.test_f1098e_student_loan_interest_agi_track6 import _f1098e_acts

    directory = Path(_BASE_ROOT.name) / f"base-{len(_BASES)}" / "workspace"
    registry = _registry()
    log = ActLog(directory, registry)
    rows = _f1098e_acts(statements=[], close=True, wages=wages)
    rows.pop()  # the Track 6 adoption; each case adopts its own package
    for index, row in enumerate(rows):
        row = dict(row)
        row["committed_against"] = index
        row["act_id"] = f"demo.track5.base.{index:03d}"
        log.append(row, expected_revision=index)

    def append(kind: str, payload: dict[str, Any]) -> None:
        revision = log.read().revision
        log.append(act(revision, kind, payload), expected_revision=revision)

    bundle = load_sli_relationship_source_bundle() if bundle_version == "v2" else _load("sli-relationship-source.bundle.json")
    append("bundle-adoption", {"bundle": bundle})
    for name, reference in Return.BORROWING.items():
        introduce_borrowing_reference_durably(log, registry, reference_id=reference,
                                              description=f"{name.title()} study loan", actor=USER,
                                              at="2026-10-03T09:00:00Z")
    for identity, label, kind in Return.ENTITIES:
        append("entity-introduced", {"entity": demo_entity(identity, label, kind)})
    track14._append_source(log, registry, track4.SCHOOL, Return.SCHOOL_KEYS["autumn"],
                           "Riverside College, BSc, autumn 2024", "track5-school-autumn")
    track14._append_source(log, registry, track4.SCHOOL, Return.SCHOOL_KEYS["spring"],
                           "Riverside College, BSc, spring 2025", "track5-school-spring")
    for statement, amount in amounts:
        keys = Return.STATEMENT_KEYS[statement]
        track14._append_source(log, registry, BOX2, keys, False, f"track5-box2-{statement}")
        track14._append_source(log, registry, BOX1, keys, amount, f"track5-box1-{statement}")
    _adopt(log, V40_PACKAGE, V38_RELEASE)
    _BASES[key] = directory
    return directory


def _adopt(log: ActLog, package_path: Path, release_path: Path) -> None:
    """The person adopts a core calculations version through its release."""
    package = json.loads(package_path.read_text("utf-8"))
    release = json.loads(release_path.read_text("utf-8"))
    revision = log.read().revision
    item = act(revision, "package-adoption", {
        "package": {"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]},
        "release": {"id": release["id"], "version": release["version"],
                    "checksum": hashlib.sha256(release_path.read_bytes()).hexdigest()},
        "scope": SCOPE, "revision": 1,
    })
    item["actor"] = USER
    log.append(item, expected_revision=revision)


class Return(track4.Workspace):
    """Track 4's recorder-built workspace on top of a full synthetic return."""

    BORROWING = {"autumn": "demo.track5.borrowing.autumn", "spring": "demo.track5.borrowing.spring"}
    ENTITIES = (
        ("demo.track5.period.autumn24", "Autumn 2024", "tax.us.educational-period"),
        ("demo.track5.period.spring25", "Spring 2025", "tax.us.educational-period"),
        ("demo.track5.institution.river", "Riverside College", "tax.us.educational-institution"),
        ("demo.track5.programme.bsc", "BSc", "tax.us.educational-programme"),
        ("demo.track5.lender.cedar", "Cedar Servicing", "tax.us.student-loan-lender"),
        ("demo.track5.lender.birch", "Birch Servicing", "tax.us.student-loan-lender"),
        ("demo.track5.statement.cedar", "2025 Form 1098-E from Cedar", "tax.us.1098e-statement"),
        ("demo.track5.statement.birch", "2025 Form 1098-E from Birch", "tax.us.1098e-statement"),
    )
    SCHOOL_KEYS = {
        "autumn": (("period", ENTITIES[0][0]), ("institution", ENTITIES[2][0]), ("programme", ENTITIES[3][0])),
        "spring": (("period", ENTITIES[1][0]), ("institution", ENTITIES[2][0]), ("programme", ENTITIES[3][0])),
    }
    STATEMENT_KEYS = {
        "cedar": (("lender", ENTITIES[4][0]), ("statement", ENTITIES[6][0]), ("tax-year", "2025")),
        "birch": (("lender", ENTITIES[5][0]), ("statement", ENTITIES[7][0]), ("tax-year", "2025")),
    }

    def __init__(self, *, wages: float = 50000, amounts: dict[str, float] | None = None,
                 bundle_version: str = "v2") -> None:
        amounts = {"cedar": 3000.0} if amounts is None else amounts
        base = _base_log(wages, bundle_version, tuple(sorted(amounts.items())))
        self.raw = tempfile.TemporaryDirectory(prefix="sli-track5-")
        shutil.copytree(base, Path(self.raw.name) / "workspace")
        self.registry = _registry()
        self.log = ActLog(Path(self.raw.name) / "workspace", self.registry)
        self.borrowing = dict(self.BORROWING)
        self.school = {name: fact_id_for(track4.SCHOOL, keys) for name, keys in self.SCHOOL_KEYS.items()}
        self.statement_keys = {name: self.STATEMENT_KEYS[name] for name in amounts}
        self.statement = {name: fact_id_for(BOX1, keys) for name, keys in self.statement_keys.items()}
        self.claims: dict[tuple[str, str, str], str] = {}
        self._serial = 0
        self._common: set[str] = set()

    def plain(self, borrowing: str = "autumn", school: str = "autumn", statement: str = "cedar") -> None:
        """Track 4's plain case, plus the four retained answers the statement still needs."""
        super().plain(borrowing, school, statement)
        if statement not in self._common:
            self.common_answers(statement)

    def common_answers(self, statement: str = "cedar", *, skip: tuple[str, ...] = (),
                       values: dict[str, str] | None = None) -> None:
        """The four yes/no answers both paths keep asking."""
        self._common.add(statement)
        self.old_answers(statement, skip=(REPLACED, *skip), values=values)

    def old_answers(self, statement: str = "cedar", *, skip: tuple[str, ...] = (),
                    values: dict[str, str] | None = None) -> None:
        """The five older yes/no answers on one statement."""
        for tail in ANSWER_TAILS:
            if tail in skip:
                continue
            value = (values or {}).get(tail, "yes")
            track14._append_source(self.log, self.registry, f"tax.us.2025.f1098e.{tail}",
                                   self.statement_keys[statement], value,
                                   self._name(f"track5-{tail}-{statement}"))


# ---------------------------------------------------------------------------
# Running a package over a fresh recovery
# ---------------------------------------------------------------------------


def _corpus() -> dict[tuple[str, str], dict[str, Any]]:
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("*.json"):
        body = json.loads(path.read_text("utf-8"))
        if isinstance(body, dict) and isinstance(body.get("id"), str) and isinstance(body.get("version"), str):
            corpus[(body["id"], body["version"])] = body
    return corpus


class _Graph:
    def __init__(self, resolved_members: Any, package: dict[str, Any]) -> None:
        self.resolved_members = resolved_members
        self.package = package


class Outcome:
    """One run: both runners' results and the line 21 presentation."""

    def __init__(self, forward: RunResult, reference: RunResult, model: dict[str, Any]) -> None:
        self.forward = forward
        self.reference = reference
        self.model = model

    @property
    def section(self) -> dict[str, Any]:
        [section] = [s for s in self.model["sections"] if s["field"]["id"] == "tax.us.2025.schedule1.line-21"]
        found: dict[str, Any] = section
        return found

    @property
    def line21(self) -> dict[str, Any]:
        resolved: dict[str, Any] = self.section["resolved"]
        return resolved

    def value(self) -> Any:
        return self.line21.get("value")

    def worksheet_row(self) -> dict[str, Any]:
        [row] = [r for r in self.forward.dispositions if r.get("artifact_id") == WORKSHEET]
        return row


def run_package(acts: tuple[dict[str, Any], ...], package: dict[str, Any], run_id: str) -> Outcome:
    """Validate, marshal as the coordinator does, run both runners, project line 21."""
    schemas = DerivationSchemas()
    validation = validate_package(package, _corpus(), schemas)
    if not validation.ok:
        raise AssertionError([(issue.member_id, issue.code, issue.detail) for issue in validation.issues])
    state = project(acts, schemas.registry)
    currency = compute_currency(state)
    resolved = _Graph(list(validation.resolved_members), package)
    material = _resolved_run_material(resolved)
    rules, parameters, families, mappings, fact_types, bindings, collect_names = material
    authorization = _resolve_run_authorization(
        acts, run_scope=SCOPE, scope_user=USER, rules=rules,
        corpus={member["id"]: member for member in resolved.resolved_members}, package=package,
    )
    context = marshal_live_run_context(
        run_id=run_id, state=state, currency=currency, rules=rules, parameters=parameters,
        claim_applicability=_statement_inclusion_applicability(acts, schemas.registry, state, currency),
        canon=load_canon(schemas),
        adoption_pin={"role": "adoption", "id": package["id"], "version": package["version"]},
        governance_pins=[], family_declarations=families, closure_mappings=mappings, fact_types=fact_types,
        input_bindings=bindings, collect_source_names=collect_names,
        emission_only_source_names=list(material.emission_only_names), authorization=authorization,
        reporting_year=2025, parameter_index=material.parameter_index,
    )._context
    forward, reference = run(context, schemas), run_reference(context, schemas)
    if track4.surface(forward) != track4.surface(reference):
        raise AssertionError("forward and reference runners disagree")
    model = build_presentation_model(run_id=run_id, resolved_members=resolved.resolved_members, state=state,
                                     publications=forward.publications, dispositions=forward.dispositions)
    return Outcome(forward, reference, model)


def run_live(acts: tuple[dict[str, Any], ...], run_id: str) -> Outcome:
    """The production path: release resolution, live_coordinate_run, its presentation.

    The coordinator's own marshalled context is captured and also run on the
    reference runner; both runners must agree. The line 21 presentation is
    the one the coordinator wrote.
    """
    captured: list[Any] = []

    def spy(**kwargs: Any) -> Any:
        marshalled = marshal_live_run_context(**kwargs)
        captured.append(marshalled._context)
        return marshalled

    with mock.patch.object(live_module, "marshal_live_run_context", side_effect=spy), \
            tempfile.TemporaryDirectory(prefix="sli-track5-live-") as work:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(work) / "workspace"), repo_root=ROOT, authoritative_acts=acts,
            workspace_revision=len(acts), run_scope=SCOPE, scope_user=USER,
            request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
            surface=PublicationSurface(RELEASE_DIR, V38_REGISTRY, CONTENT), output_name="track5.json",
        )
        if outcome.refusal is not None or outcome.presentation_path is None:
            raise AssertionError(f"core calculations v40 refused: {outcome.refusal!r}")
        model = json.loads(outcome.presentation_path.read_text("utf-8"))
    [context] = captured
    schemas = DerivationSchemas()
    forward, reference = run(context, schemas), run_reference(context, schemas)
    if track4.surface(forward) != track4.surface(reference):
        raise AssertionError("forward and reference runners disagree")
    assert outcome.publications is not None
    if sorted(json.dumps(p.finding, sort_keys=True) for p in outcome.publications) != sorted(
            json.dumps(p.finding, sort_keys=True) for p in forward.publications):
        raise AssertionError("the coordinator's publications differ from the forward runner's")
    return Outcome(forward, reference, model)


def line21_text(outcome: Outcome) -> list[str]:
    """What line 21 says, one line per reason: the statement, then its sentence."""
    lines: list[str] = []
    for reason in outcome.line21.get("reasons", []):
        label = reason.get("statementLabel", {})
        name = " / ".join(part for part in (label.get("statement"), label.get("lender")) if part)
        lines.append(f"{name}: {reason['sentence']}" if name else reason["sentence"])
    return lines


def published(result: RunResult, symbol: str) -> dict[str, str]:
    return {subject: str(row["value"]) for subject, row in track4.published(result, symbol).items()}


def values_by_symbol(result: RunResult) -> dict[str, str]:
    return {str(pub.finding["symbol"]): str(pub.finding["value"]) for pub in result.publications}


# ---------------------------------------------------------------------------
# Slice 1: the worksheet selection and the yes/no path with coverage
# ---------------------------------------------------------------------------


class WorksheetSelection(unittest.TestCase):
    def _run(self, ws: Return, tag: str) -> Outcome:
        return run_live(ws.acts(), f"demo.run.track5.{tag}")

    def test_v40_validates_and_the_worksheet_is_a_v13_selection(self) -> None:
        validation = validate_package(json.loads(V40_PACKAGE.read_text("utf-8")), _corpus(), DerivationSchemas())
        self.assertTrue(validation.ok, [issue.detail for issue in validation.issues])
        worksheet = _load(WORKSHEET_V3)
        self.assertEqual((worksheet["schema"], worksheet["version"]), ("rule-artifact.v13", "v3"))
        paths = {path["id"]: path for path in worksheet["selection"]["paths"]}
        self.assertEqual(set(paths), {"yes-no-answers", "loan-links"})
        self.assertEqual(worksheet["selection"]["refusal"]["missing"], [BOTH_TOKEN])
        # Only the replaced answer selects the old path (owner decision 2).
        self.assertEqual([pin["id"] for pin in paths["yes-no-answers"]["activity"]["member_fact_types"]],
                         [f"tax.us.2025.f1098e.{REPLACED}"])
        new_members = {pin["id"] for pin in paths["loan-links"]["activity"]["member_fact_types"]}
        self.assertEqual(new_members, {
            "tax.us.2025.sli.statement-inclusion-relationship",
            "tax.us.2025.sli.statement-inclusion-unresolved",
            "tax.us.2025.sli.statement-inclusion-denied",
            "tax.us.2025.sli.statement-inclusion-withdrawn",
            "tax.us.2025.sli.statement-inclusion-scope-unresolved",
            "tax.us.2025.sli.statement-inclusion-applicability-unestablished",
        })
        # Both paths read the four retained answers per statement with coverage.
        reads = {path_id: {read["symbol"] for read in path["reads_subject_results"]} for path_id, path in paths.items()}
        self.assertEqual(reads["yes-no-answers"], set(STATUS.values()))
        self.assertEqual(reads["loan-links"], {STANDING, *(STATUS[tail] for tail in COMMON)})

    def test_the_worksheet_arithmetic_is_v1_byte_for_byte(self) -> None:
        v1 = _load("rule.sli-worksheet.json")
        paths = {path["id"]: path for path in _load(WORKSHEET_V3)["selection"]["paths"]}

        def normalise(node: Any) -> Any:
            if isinstance(node, list):
                return [normalise(item) for item in node]
            if not isinstance(node, dict):
                return node
            if node.get("op") == "collect_categorical_all_equal":
                return {"collect-yes": str(node["name"]).rsplit(".", 1)[-1]}
            return {key: normalise(item) for key, item in node.items()}

        expected = normalise(v1["value"]["else"])
        self.assertEqual(normalise(paths["yes-no-answers"]["value"]), expected)
        # The loan-link path: only the replaced answer leaves the universal
        # check, and the standing check refuses right after it.
        new = normalise(paths["loan-links"]["value"])
        universal = new["value"]["else"]
        standing_check = universal["else"]
        self.assertEqual(standing_check["when"], {"op": "not", "value": {"collect-yes": "statement-line21-standing"}})
        self.assertEqual(standing_check["then"], {"op": "block", "code": "DEPENDENCY_INVALID"})
        universal["else"] = standing_check["else"]
        args = expected["value"]["else"]["when"]["value"]["args"]
        expected["value"]["else"]["when"]["value"]["args"] = [a for a in args if a != {"collect-yes": REPLACED}]
        self.assertEqual(new, expected)

    def test_old_only_complete_workspaces_keep_their_v38_results(self) -> None:
        for wages, amount, expected in ((50000, 3000.0, "2500"), (90000, 2000.0, "1334")):
            with self.subTest(wages=wages):
                ws = Return(wages=wages, amounts={"cedar": amount})
                with ws.raw:
                    ws.old_answers("cedar")
                    acts = ws.acts()
                    v38 = run_package(acts, json.loads(V38_PACKAGE.read_text("utf-8")), "demo.run.track5.v38")
                    v40 = self._run(ws, f"old-only-{expected}")
                    self.assertEqual(v38.value(), int(expected))
                    self.assertEqual(v40.value(), int(expected))
                    self.assertEqual(v40.line21["disposition"], "published_value")
                    before, after = values_by_symbol(v38.forward), values_by_symbol(v40.forward)
                    self.assertEqual({k: v for k, v in after.items() if k in before}, before)
                    added = set(after) - set(before)
                    self.assertTrue(all(name.startswith("tax.us.2025.sli.") for name in added), added)
                    # The line reads each statement's five statuses, pinned as derived.
                    finding = v40.line21["act"]["finding"]
                    derived = {pin["id"] for pin in finding["pins"] if pin.get("origin") == "derived"}
                    self.assertEqual(len(derived), 5)

    def test_old_only_with_a_statement_missing_an_answer_now_blocks(self) -> None:
        # The Track 0a fail-open defect: v39 deducts because Cedar's yes stands
        # in for Birch's missing answer. v3 refuses and names Birch.
        ws = Return(amounts={"cedar": 1500.0, "birch": 800.0})
        with ws.raw:
            ws.old_answers("cedar")
            ws.old_answers("birch", skip=("no-qtp-earnings-used",))
            v39 = run_package(ws.acts(), json.loads(track4.V39_PACKAGE.read_text("utf-8")), "demo.run.track5.v39-open")
            self.assertEqual(v39.value(), 2300)
            outcome = self._run(ws, "old-missing")
            self.assertEqual(outcome.line21["disposition"], "blocked")
            row = outcome.worksheet_row()
            self.assertEqual((row["code"], row["missing"]), ("DEPENDENCY_INVALID", [ws.statement["birch"]]))
            self.assertEqual(track4.blocks(outcome.forward, STATUS_RULE["no-qtp-earnings-used"]),
                             {ws.statement["birch"]: ("DEPENDENCY_ABSENT", ["tax.us.2025.f1098e.no-qtp-earnings-used"])})
            # A missing answer is never read as no.
            self.assertNotEqual(row["code"], "SLI_UNIVERSAL_COMPONENT_VIOLATION")

    def test_old_only_with_a_no_keeps_the_violation(self) -> None:
        ws = Return()
        with ws.raw:
            ws.old_answers("cedar", values={"no-related-person-interest": "no"})
            row = self._run(ws, "old-no").worksheet_row()
            self.assertEqual(row["code"], "SLI_UNIVERSAL_COMPONENT_VIOLATION")

    def test_new_path_plain_case_publishes_2500_from_the_standing_and_four_answers(self) -> None:
        ws = Return()
        with ws.raw:
            ws.plain()
            outcome = self._run(ws, "new-plain")
            self.assertEqual(outcome.value(), 2500)
            self.assertEqual(published(outcome.forward, STANDING), {ws.statement["cedar"]: "none"})
            standing = track4.published(outcome.forward, STANDING)[ws.statement["cedar"]]
            finding = outcome.line21["act"]["finding"]
            derived = {pin["id"] for pin in finding["pins"] if pin.get("origin") == "derived"}
            self.assertIn(standing["id"], derived)
            commons = {track4.published(outcome.forward, STATUS[tail])[ws.statement["cedar"]]["id"] for tail in COMMON}
            self.assertEqual(derived, {standing["id"], *commons})
            # The standing pins the statement's conclusion it relays.
            conclusion = track4.published(outcome.forward, track4.CONCLUSION)[ws.statement["cedar"]]
            self.assertIn(conclusion["id"], track4.pin_ids(standing))
            # The replaced answer was never asked, and its status is not read.
            self.assertEqual(published(outcome.forward, STATUS[REPLACED]), {})

    def test_the_four_retained_answers_do_not_select_the_old_path(self) -> None:
        ws = Return()
        with ws.raw:
            ws.common_answers("cedar")
            outcome = self._run(ws, "common-only")
            # Neither path: the statement needs its loan link.
            self.assertEqual(outcome.line21["disposition"], "blocked")
            self.assertEqual(published(outcome.forward, STANDING), {ws.statement["cedar"]: "no-loan-link"})

    def test_a_missing_retained_answer_cannot_be_bypassed_on_the_new_path(self) -> None:
        for tail in COMMON:
            with self.subTest(tail=tail):
                ws = Return()
                with ws.raw:
                    ws.link("financing", "autumn", "autumn")
                    ws.link("statement-inclusion", "autumn", "cedar")
                    ws.answer("loan", "autumn", "yes")
                    ws.answer("enroll", "autumn", "yes")
                    ws.common_answers("cedar", skip=(tail,))
                    outcome = self._run(ws, f"new-missing-{tail}")
                    # Relationship support is favorable; the missing answer still refuses.
                    self.assertEqual(published(outcome.forward, STANDING), {ws.statement["cedar"]: "none"})
                    row = outcome.worksheet_row()
                    self.assertEqual((row["code"], row["missing"]), ("DEPENDENCY_INVALID", [ws.statement["cedar"]]))
                    self.assertEqual(track4.blocks(outcome.forward, STATUS_RULE[tail]),
                                     {ws.statement["cedar"]: ("DEPENDENCY_ABSENT", [f"tax.us.2025.f1098e.{tail}"])})

    def test_a_negative_retained_answer_cannot_be_bypassed_on_the_new_path(self) -> None:
        for tail in COMMON:
            with self.subTest(tail=tail):
                ws = Return()
                with ws.raw:
                    ws.link("financing", "autumn", "autumn")
                    ws.link("statement-inclusion", "autumn", "cedar")
                    ws.answer("loan", "autumn", "yes")
                    ws.answer("enroll", "autumn", "yes")
                    ws.common_answers("cedar", values={tail: "no"})
                    outcome = self._run(ws, f"new-no-{tail}")
                    self.assertEqual(published(outcome.forward, STANDING), {ws.statement["cedar"]: "none"})
                    self.assertEqual(outcome.worksheet_row()["code"], "SLI_UNIVERSAL_COMPONENT_VIOLATION")

    def test_a_second_statement_beside_a_supported_one_needs_its_own_retained_answers(self) -> None:
        ws = Return(amounts={"cedar": 1500.0, "birch": 800.0})
        with ws.raw:
            ws.plain()
            ws.link("financing", "spring", "spring")
            ws.link("statement-inclusion", "spring", "birch")
            ws.answer("loan", "spring", "yes")
            ws.answer("enroll", "spring", "yes")
            ws.common_answers("birch", skip=("no-related-person-interest",))
            outcome = self._run(ws, "second-missing")
            self.assertEqual(published(outcome.forward, STANDING),
                             {ws.statement["cedar"]: "none", ws.statement["birch"]: "none"})
            row = outcome.worksheet_row()
            self.assertEqual((row["code"], row["missing"]), ("DEPENDENCY_INVALID", [ws.statement["birch"]]))
            # Birch's no is not rescued by Cedar's yes either.
            ws.old_answers("birch", skip=(REPLACED, *[t for t in COMMON if t != "no-related-person-interest"]),
                           values={"no-related-person-interest": "no"})
            self.assertEqual(self._run(ws, "second-no").worksheet_row()["code"], "SLI_UNIVERSAL_COMPONENT_VIOLATION")
            ws.old_answers("birch", skip=(REPLACED, *[t for t in COMMON if t != "no-related-person-interest"]))
            self.assertEqual(self._run(ws, "second-yes").value(), 2300)

    def test_both_present_blocks_on_the_replaced_answer(self) -> None:
        ws = Return()
        with ws.raw:
            ws.plain()
            ws.old_answers("cedar", skip=COMMON)
            row = self._run(ws, "both").worksheet_row()
            self.assertEqual((row["code"], row["missing"]), ("DEPENDENCY_INVALID", [BOTH_TOKEN]))

    def test_a_denied_link_alone_is_the_new_path(self) -> None:
        # Any statement-keyed link outcome makes the loan-link path present.
        ws = Return()
        with ws.raw:
            ws.plain()
            ws.old_answers("cedar", skip=COMMON)
            ws.outcome("statement-inclusion", "autumn", "cedar", "no")
            row = self._run(ws, "both-denied").worksheet_row()
            self.assertEqual(row["missing"], [BOTH_TOKEN])

    def test_closed_empty_publishes_zero(self) -> None:
        ws = Return(amounts={})
        with ws.raw:
            outcome = self._run(ws, "closed-empty")
            self.assertEqual(outcome.value(), 0)
            self.assertEqual(outcome.line21["disposition"], "closure_backed_zero")

    def test_nonempty_with_neither_blocks(self) -> None:
        ws = Return()
        with ws.raw:
            outcome = self._run(ws, "neither")
            self.assertEqual(outcome.line21["disposition"], "blocked")
            self.assertEqual(outcome.worksheet_row()["code"], "DEPENDENCY_INVALID")
            self.assertEqual(published(outcome.forward, STANDING), {ws.statement["cedar"]: "no-loan-link"})

    def test_an_unrelated_supported_statement_never_rescues_a_blocked_one(self) -> None:
        ws = Return(amounts={"cedar": 1500.0, "birch": 800.0})
        with ws.raw:
            ws.plain()
            ws.link("financing", "spring", "spring")
            ws.link("statement-inclusion", "spring", "birch")
            ws.answer("loan", "spring", "yes")
            ws.common_answers("birch")
            outcome = self._run(ws, "unrelated")
            self.assertEqual(outcome.line21["disposition"], "blocked")
            self.assertEqual(published(outcome.forward, STANDING),
                             {ws.statement["cedar"]: "none", ws.statement["birch"]: "enrollment-answer-missing"})
            ws.answer("enroll", "spring", "yes")
            self.assertEqual(self._run(ws, "unrelated-answered").value(), 2300)

    def test_a_stale_schooling_refuses_naming_its_statement(self) -> None:
        ws = Return(amounts={"cedar": 1500.0, "birch": 800.0})
        with ws.raw:
            ws.plain()
            ws.plain("spring", "spring", "birch")
            ws.retract_source(ws.school["autumn"])
            outcome = self._run(ws, "stale-schooling")
            row = outcome.worksheet_row()
            self.assertEqual((row["code"], row["missing"]), ("DEPENDENCY_INVALID", [ws.statement["cedar"]]))
            self.assertEqual(published(outcome.forward, STANDING), {ws.statement["birch"]: "none"})


class LinkLifecycle(unittest.TestCase):
    """Sentence 8: a corrected answer changes the deduction, through the production path."""

    def _run(self, ws: Return, tag: str) -> Outcome:
        return run_live(ws.acts(), f"demo.run.track5.{tag}")

    def test_plain_case_and_phase_out(self) -> None:
        for wages, amount, expected in ((50000, 3000.0, 2500), (90000, 2000.0, 1334)):
            with self.subTest(wages=wages):
                ws = Return(wages=wages, amounts={"cedar": amount})
                with ws.raw:
                    ws.plain()
                    outcome = self._run(ws, f"plain-{expected}")
                    self.assertEqual(outcome.value(), expected)
                    self.assertEqual(outcome.line21["disposition"], "published_value")

    def test_an_amount_only_correction_changes_the_deduction(self) -> None:
        ws = Return()
        with ws.raw:
            ws.plain()
            self.assertEqual(self._run(ws, "before-correction").value(), 2500)
            ws.reviewed_amount_only("cedar", 1000.0)
            self.assertEqual(self._run(ws, "amount-only").value(), 1000)

    def test_correcting_a_link_away_blocks_and_restoring_it_returns_the_deduction(self) -> None:
        ws = Return()
        with ws.raw:
            ws.plain()
            self.assertEqual(self._run(ws, "linked").value(), 2500)
            ws.outcome("statement-inclusion", "autumn", "cedar", "no")
            away = self._run(ws, "link-away")
            self.assertEqual(away.line21["disposition"], "blocked")
            self.assertEqual(published(away.forward, STANDING), {ws.statement["cedar"]: "no-loan-link"})
            ws.link("statement-inclusion", "autumn", "cedar", "yes")
            self.assertEqual(self._run(ws, "link-restored").value(), 2500)

    def test_withdrawing_a_link_blocks_and_restoring_it_returns_the_deduction(self) -> None:
        ws = Return()
        with ws.raw:
            ws.plain()
            ws.outcome("statement-inclusion", "autumn", "cedar", "withdrawn")
            withdrawn = self._run(ws, "link-withdrawn")
            self.assertEqual(published(withdrawn.forward, STANDING), {ws.statement["cedar"]: "inclusion-withdrawn"})
            self.assertEqual(withdrawn.line21["disposition"], "blocked")
            ws.link("statement-inclusion", "autumn", "cedar", "yes")
            self.assertEqual(self._run(ws, "withdrawn-restored").value(), 2500)

    def test_the_owners_mixed_applicability_case_blocks(self) -> None:
        ws = Return(amounts={"cedar": 1500.0})
        with ws.raw:
            ws.plain()
            ws.unscoped_rewrite("cedar", 1800.0)
            ws.link("financing", "spring", "spring")
            ws.link("statement-inclusion", "spring", "cedar")
            ws.answer("loan", "spring", "yes")
            ws.answer("enroll", "spring", "yes")
            outcome = self._run(ws, "mixed-applicability")
            self.assertEqual(outcome.line21["disposition"], "blocked")
            self.assertEqual(published(outcome.forward, STANDING),
                             {ws.statement["cedar"]: "applicability-unestablished"})

    def test_a_workspace_without_relationship_bundle_v2_blocks(self) -> None:
        ws = Return(bundle_version="v1")
        with ws.raw:
            ws.link("financing", "autumn", "autumn")
            ws.link("statement-inclusion", "autumn", "cedar")
            ws.common_answers("cedar")
            outcome = self._run(ws, "bundle-v1")
            self.assertEqual(outcome.line21["disposition"], "blocked")
            self.assertEqual(published(outcome.forward, STANDING), {ws.statement["cedar"]: "loan-cost-answer-missing"})


CEDAR = "2025 Form 1098-E from Cedar / Cedar Servicing"
BIRCH = "2025 Form 1098-E from Birch / Birch Servicing"


def _declared_sentences() -> set[str]:
    """Every sentence the line 21 reasons may show: declared on a citizen, never composed."""
    sentences: set[str] = set()
    for fact_type in _load("sli-worksheet-inputs.bundle.json")["fact_types"]:
        sentences.update(entry["description"] for entry in fact_type["value_schema"].get("oneOf", [])
                         if "description" in entry)
    for name in (*TRACK5_FILES[1:], WORKSHEET_V3):
        sentences.add(_load(name)["wording"])
    return sentences


class LineReasons(unittest.TestCase):
    """What a person reads on a blocked line 21, from the coordinator's presentation."""

    def _text(self, ws: Return, tag: str) -> list[str]:
        outcome = run_live(ws.acts(), f"demo.run.track5.reasons.{tag}")
        self.assertEqual(outcome.line21["disposition"], "blocked")
        declared = _declared_sentences()
        for reason in outcome.line21["reasons"]:
            self.assertIn(reason["sentence"], declared)
        return line21_text(outcome)

    def test_every_track4_reason_and_the_refusal_token_have_a_sentence(self) -> None:
        bundle = {ft["id"]: ft for ft in _load("sli-worksheet-inputs.bundle.json")["fact_types"]}
        described = {entry["const"] for entry in bundle[STANDING]["value_schema"]["oneOf"] if "description" in entry}
        reasons = next(ft for ft in _load("sli-support-chain.bundle.json")["fact_types"]
                       if ft["id"] == track4.REASON)["value_schema"]["enum"]
        self.assertEqual(described, {*reasons, BOTH_TOKEN} - {"none"})
        self.assertEqual(set(bundle[STANDING]["value_schema"]["enum"]), {*reasons, BOTH_TOKEN})
        for tail in ANSWER_TAILS:
            [entry] = [e for e in bundle[STATUS[tail]]["value_schema"]["oneOf"] if "description" in e]
            self.assertEqual(entry["const"], "no")

    def test_old_path_missing_answers_name_the_statement_and_never_read_as_no(self) -> None:
        ws = Return(amounts={"cedar": 1500.0, "birch": 800.0})
        with ws.raw:
            ws.old_answers("cedar")
            ws.old_answers("birch", skip=("no-qtp-earnings-used", "no-related-person-interest"))
            self.assertEqual(self._text(ws, "old-missing"), [
                f"{BIRCH}: This statement has no answer yet to: is any of this interest on a loan from a relative "
                "or other related person? Answer it for this statement. A missing answer is not treated as no.",
                f"{BIRCH}: This statement has no answer yet to: were earnings from a qualified tuition program "
                "(a 529 plan) used to pay any of this interest? Answer it for this statement. "
                "A missing answer is not treated as no.",
            ])

    def test_both_present(self) -> None:
        ws = Return()
        with ws.raw:
            ws.plain()
            ws.old_answers("cedar", skip=COMMON)
            self.assertEqual(self._text(ws, "both"), [
                f"{CEDAR}: This return records the older answer about a non-qualified loan component together "
                "with links between statements and loans, and this statement has one of them. The two cannot be "
                "used together, even when they agree. Remove that older answer or remove the loan links; keep "
                "the other four yes/no answers.",
            ])

    def test_neither_and_a_link_corrected_away(self) -> None:
        no_link = (f"{CEDAR}: No student loan is linked to this statement. "
                   "Say which student loan this statement covers.")
        ws = Return()
        with ws.raw:
            self.assertEqual(self._text(ws, "neither"), [no_link])
            ws.plain()
            ws.outcome("statement-inclusion", "autumn", "cedar", "no")
            self.assertEqual(self._text(ws, "away"), [no_link])

    def test_the_owners_mixed_applicability_case(self) -> None:
        ws = Return(amounts={"cedar": 1500.0})
        with ws.raw:
            ws.plain()
            ws.unscoped_rewrite("cedar", 1800.0)
            ws.link("financing", "spring", "spring")
            ws.link("statement-inclusion", "spring", "cedar")
            ws.answer("loan", "spring", "yes")
            ws.answer("enroll", "spring", "yes")
            self.assertEqual(self._text(ws, "mixed"), [
                f"{CEDAR}: The statement this link was confirmed against changed or was removed. "
                "Confirm the link again.",
            ])

    def test_a_stale_schooling_names_only_its_statement(self) -> None:
        ws = Return(amounts={"cedar": 1500.0, "birch": 800.0})
        with ws.raw:
            ws.plain()
            ws.plain("spring", "spring", "birch")
            ws.retract_source(ws.school["autumn"])
            self.assertEqual(self._text(ws, "stale"), [
                f"{CEDAR}: No result could be reached for this statement because something its loan link relies "
                "on changed or was removed, such as the schooling the loan paid for. Check the schooling and the "
                "loan linked to this statement.",
            ])

    def test_a_retained_answer_missing_or_no_on_a_second_statement(self) -> None:
        ws = Return(amounts={"cedar": 1500.0, "birch": 800.0})
        with ws.raw:
            ws.plain()
            ws.link("financing", "spring", "spring")
            ws.link("statement-inclusion", "spring", "birch")
            ws.answer("loan", "spring", "yes")
            ws.answer("enroll", "spring", "yes")
            ws.common_answers("birch", skip=("no-related-person-interest",))
            self.assertEqual(self._text(ws, "common-missing"), [
                f"{BIRCH}: This statement has no answer yet to: is any of this interest on a loan from a relative "
                "or other related person? Answer it for this statement. A missing answer is not treated as no.",
            ])
            ws.old_answers("birch", skip=(REPLACED, *[t for t in COMMON if t != "no-related-person-interest"]),
                           values={"no-related-person-interest": "no"})
            self.assertEqual(self._text(ws, "common-no"), [
                f"{BIRCH}: You answered that some of this interest is on a loan from a relative or other related "
                "person. The deduction is not worked out here when that is so. If that answer is wrong, change it.",
            ])

    def test_an_unrelated_supported_statement_is_not_named(self) -> None:
        ws = Return(amounts={"cedar": 1500.0, "birch": 800.0})
        with ws.raw:
            ws.plain()
            ws.link("financing", "spring", "spring")
            ws.link("statement-inclusion", "spring", "birch")
            ws.answer("loan", "spring", "yes")
            ws.common_answers("birch")
            self.assertEqual(self._text(ws, "unrelated"), [
                f"{BIRCH}: The loan on this statement has no answer yet to: was the student enrolled at least "
                "half-time in a degree or certificate program during the schooling it paid for? Answer that "
                "question. A missing answer is not treated as no.",
            ])

    def test_a_workspace_that_cannot_record_the_answers_is_told_so(self) -> None:
        # Not asked to answer: relationship bundle v2 was never adopted here.
        ws = Return(bundle_version="v1")
        with ws.raw:
            ws.link("financing", "autumn", "autumn")
            ws.link("statement-inclusion", "autumn", "cedar")
            ws.common_answers("cedar")
            self.assertEqual(self._text(ws, "bundle-v1"), [
                f"{CEDAR}: This workspace was set up before the student loan questions were added, so it cannot "
                "record the answers this statement needs yet. The deduction stays blocked until the workspace is "
                "updated; nothing is assumed in the meantime.",
            ])

    def test_a_published_line_carries_no_reasons(self) -> None:
        ws = Return()
        with ws.raw:
            ws.plain()
            outcome = run_live(ws.acts(), "demo.run.track5.reasons.published")
            self.assertNotIn("reasons", outcome.line21)


class Publication(unittest.TestCase):
    def test_v40_is_v39_with_the_worksheet_successor_and_its_inputs(self) -> None:
        v39 = json.loads(track4.V39_PACKAGE.read_text("utf-8"))
        v40 = json.loads(V40_PACKAGE.read_text("utf-8"))
        self.assertEqual(v40["package_checksum"], package_instance_checksum(v40))
        self.assertEqual((v40["schema"], v40["version"]), ("artifact-package.v35", "v40"))
        before = {(m["id"], m["version"]) for m in v39["members"]}
        after = {(m["id"], m["version"]) for m in v40["members"]}
        added = {(_load(name)["id"], _load(name)["version"]) for name in (*TRACK5_FILES, WORKSHEET_V3)}
        self.assertEqual(after - before, added)
        self.assertEqual(before - after, {(WORKSHEET, "v1")})
        # The committed v2, which dropped the four retained answers, is never published.
        self.assertNotIn((WORKSHEET, "v2"), after)

    def test_registry_v38_appends_only_and_the_release_pins_it(self) -> None:
        from packages.derivation.package_validation import citizen_checksum

        old = json.loads((CONTENT / "published-packages.v37.json").read_text("utf-8"))
        new = json.loads(V38_REGISTRY.read_text("utf-8"))
        for section in ("citizens", "packages"):
            self.assertEqual(new[section][:len(old[section])], old[section])
        by_key = {(row["id"], row["version"]): row["checksum"] for row in new["citizens"]}
        for name in (*TRACK5_FILES, WORKSHEET_V3):
            citizen = _load(name)
            self.assertEqual(by_key[(citizen["id"], citizen["version"])], citizen_checksum(citizen))
        self.assertNotIn((WORKSHEET, "v2"), by_key)
        v40 = json.loads(V40_PACKAGE.read_text("utf-8"))
        self.assertEqual(new["packages"][len(old["packages"]):],
                         [{"checksum": v40["package_checksum"], "id": v40["id"], "version": "v40"}])
        release = json.loads(V38_RELEASE.read_text("utf-8"))
        self.assertEqual(release["package_registry_sha256"], hashlib.sha256(V38_REGISTRY.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
