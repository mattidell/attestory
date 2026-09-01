"""Live-path standing authorization.

``_resolve_run_authorization`` must derive its "calculation subject" from
the run's own scope, never from the grant it is checking -- otherwise a
grant for any wrong taxpayer would never be rejected -- and its
re-authorization boundary must root at the calculation's actual roots,
never at every resolved rule.

These tests enter exclusively through ``live_coordinate_run`` from an
authoritative act log -- never a preconstructed ``RunContext.authorization``
shortcut, since Integration's coverage alone would bypass
this exact path. All bodies are synthetic (mirrors
``tests/test_frrs_t4_w2_live_integration.py``'s v3 fixture, package
``tax.us.2025.package.core-calculations`` v3, single rule-schema entrypoint
``tax.us.2025.rule.form1040-line16``).
"""

from __future__ import annotations

import json
import unittest
from collections.abc import Callable
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from packages.derivation.authorization import (
    STATUS_ABSENT,
    STATUS_ADMITTED,
    STATUS_SUSPENDED,
    STATUS_TAXPAYER_MISMATCH,
    STATUS_WITHDRAWN,
    STATUS_YEAR_MISMATCH,
)
from packages.derivation.authorization_closure import package_boundary_digest
from packages.derivation.live import (
    LiveCoordinatorOutcome,
    live_coordinate_run,
    _resolve_run_authorization,
)
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import workspace_registry
from packages.derivation.production_resolver import PublicationSurface, ResolvedGraph, resolve_production_package
from packages.kernel.act_log import ActLog
from packages.kernel.schema_registry import SchemaValidationError

from tests.test_frrs_t4_w2_live_integration import CONTENT, T3, USER, _act, _live_act, _surface, _v3_authoritative_acts

WRONG_SUBJECT = "demo.subject.wrong"
SCOPE_YEAR = "2052"
RUN_SCOPE = {"jurisdiction": "us", "year": SCOPE_YEAR}


def _v3_universe() -> str:
    """The real production digest for the v3 package's single rule root.

    Independently recomputed (not copy-pasted from production) by asking
    ``resolve_production_package`` -- the same resolver ``live_coordinate_
    run`` uses -- for the actual resolved graph, then hashing exactly the
    closure ``_resolve_run_authorization`` will (package's declared
    entrypoints, restricted to resolved rule-schema members). This must
    stay independent of ``live.py``'s own digest call only in the sense
    that a defect in *that* call would make this helper and production
    disagree, not in the sense of hand-computing the closure by a
    different route (there is exactly one production closure algorithm,
    ``authorization_closure.py``, and duplicating it here would just test
    a second implementation of the same thing).
    """
    acts = _v3_authoritative_acts()
    graph = resolve_production_package(
        acts, run_scope=RUN_SCOPE, scope_user=USER, workspace_revision=len(acts), surface=_surface(),
    )
    assert isinstance(graph, ResolvedGraph)
    corpus = {member["id"]: member for member in graph.resolved_members}
    entrypoint_ids = {
        entry["id"] for entry in graph.package.get("entrypoints", [])
        if isinstance(entry, dict) and isinstance(entry.get("id"), str)
    }
    rule_ids = {
        member["id"] for member in graph.resolved_members
        if str(member.get("schema", "")).startswith("rule-artifact")
        or str(member.get("schema", "")).startswith("attachment-rule")
    }
    root = rule_ids & entrypoint_ids
    return package_boundary_digest(root, corpus, package=graph.package)


def _grant_act(index: int, *, grant_id: str, subject_id: str, tax_year: str, universe_id: str, supersedes: str | None = None) -> dict[str, Any]:
    citizen: dict[str, Any] = {
        "schema": "workspace-calculation-authorization.v1",
        "id": grant_id,
        "subject_id": subject_id,
        "tax_year": tax_year,
        "universe_id": universe_id,
    }
    if supersedes is not None:
        citizen["supersedes"] = supersedes
    return _live_act(index, "calculation-authorization", {"authorization": citizen})


def _end_act(index: int, *, grant_id: str, ending: str) -> dict[str, Any]:
    return _live_act(index, "calculation-authorization-end", {"authorization_id": grant_id, "ending": ending})


def _scope_act(index: int, *, scope_id: str, subject_id: str, tax_year: str, rule_ids: list[str]) -> dict[str, Any]:
    """Build a ``calculation-scope-declaration`` act around the scope
    citizen, ``workspace-calculation-scope.v1``: the declaration's named
    rule ids are unioned into the executed-entrypoint root, never replacing
    or narrowing it below what the run actually executes and publishes.
    """
    citizen: dict[str, Any] = {
        "schema": "workspace-calculation-scope.v1",
        "id": scope_id,
        "subject_id": subject_id,
        "tax_year": tax_year,
        "rule_ids": rule_ids,
    }
    return _live_act(index, "calculation-scope-declaration", {"scope": citizen})


def _append_and_reread(acts: list[dict[str, Any]], workspace_dir: Path) -> tuple[dict[str, Any], ...]:
    """Commit ``acts`` through a real ``ActLog`` (schema-validated on
    append, re-validated on read), then return the reread sequence.

    This is the record boundary that matters: a hand-built ``authoritative_acts``
    list is not evidence that an act can actually enter the authoritative
    log. ``acts`` must already carry sequential ``committed_against``
    indices starting at 0 (the shape ``_live_act``/``_grant_act``/
    ``_scope_act`` produce).
    """
    log = ActLog(workspace_dir, workspace_registry())
    for index, act in enumerate(acts):
        log.append(act, index)
    return log.read().acts


def _acts_with(*extra: Callable[[int], dict[str, Any]]) -> list[dict[str, Any]]:
    """The v3 fixture's complete authoritative log, plus extra acts appended
    after the adoption act (position is irrelevant to the fold; only the
    supplied ``committed_against`` ordering among authorization acts
    matters, and the caller supplies that via ``index``)."""
    acts = _v3_authoritative_acts()
    for factory in extra:
        acts.append(factory(len(acts)))
    return acts


class LiveAuthorizationCorrectAndWrongTaxpayer(unittest.TestCase):
    def _run(self, acts: list[dict[str, Any]], run_id: str) -> tuple[LiveCoordinatorOutcome, dict[str, Any] | None]:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = live_coordinate_run(
                WorkspaceCapability(root / "L"), repo_root=CONTENT.parent.parent.parent,
                authoritative_acts=acts, workspace_revision=len(acts), run_scope=RUN_SCOPE,
                scope_user=USER, request={"schema": "run-request.v1"}, run_id=run_id,
                governance_pins=[], surface=_surface(), output_name=f"{run_id}.json",
            )
            report = json.loads(result.output_path.read_text()) if result.output_path is not None else None
            return result, report

    def test_correct_taxpayer_and_year_admits_and_publishes(self) -> None:
        universe = _v3_universe()
        acts = _acts_with(
            lambda i: _grant_act(i, grant_id="demo.auth.g1", subject_id=USER, tax_year=SCOPE_YEAR, universe_id=universe),
        )
        result, report = self._run(acts, "demo.auth.admitted")
        assert report is not None
        self.assertIsNone(result.refusal)
        self.assertTrue(result.current)
        self.assertEqual(result.authorization_status, STATUS_ADMITTED)
        published = {row["symbol"] for row in report["dispositions"] if row["disposition"] == "published"}
        self.assertIn("tax.us.2025.tax.total-tax", published)

    def test_wrong_taxpayer_grant_is_a_real_mismatch_not_admitted(self) -> None:
        """A grant naming a wrong
        taxpayer must never be resolved by picking that same taxpayer out
        of the grant itself."""
        universe = _v3_universe()
        acts = _acts_with(
            lambda i: _grant_act(i, grant_id="demo.auth.g1", subject_id=WRONG_SUBJECT, tax_year=SCOPE_YEAR, universe_id=universe),
        )
        result, report = self._run(acts, "demo.auth.wrong-taxpayer")
        assert report is not None
        self.assertIsNone(result.refusal)
        self.assertFalse(result.current)
        self.assertEqual(result.authorization_status, STATUS_TAXPAYER_MISMATCH)
        # Same tax arithmetic as the admitted run: only currentness differs.
        published = {row["symbol"] for row in report["dispositions"] if row["disposition"] == "published"}
        self.assertIn("tax.us.2025.tax.total-tax", published)

    def test_wrong_year_is_a_distinct_mismatch_from_wrong_taxpayer(self) -> None:
        universe = _v3_universe()
        acts = _acts_with(
            lambda i: _grant_act(i, grant_id="demo.auth.g1", subject_id=USER, tax_year="2099", universe_id=universe),
        )
        result, _report = self._run(acts, "demo.auth.wrong-year")
        self.assertIsNone(result.refusal)
        self.assertFalse(result.current)
        self.assertEqual(result.authorization_status, STATUS_YEAR_MISMATCH)
        self.assertNotEqual(result.authorization_status, STATUS_TAXPAYER_MISMATCH)


class DurableRunOutputCarriesAuthorization(unittest.TestCase):
    """The durable run
    output and presentation model must carry ``current``,
    authorization status, and grant identity, not only the in-memory
    ``LiveCoordinatorOutcome``. A reader of
    the actual written files (not the in-memory return value) must be able
    to recover the standing authority, its status, and which grant it came
    from."""

    def _run(self, acts: list[dict[str, Any]], run_id: str) -> tuple[LiveCoordinatorOutcome, dict[str, Any], dict[str, Any]]:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = live_coordinate_run(
                WorkspaceCapability(root / "L"), repo_root=CONTENT.parent.parent.parent,
                authoritative_acts=acts, workspace_revision=len(acts), run_scope=RUN_SCOPE,
                scope_user=USER, request={"schema": "run-request.v1"}, run_id=run_id,
                governance_pins=[], surface=_surface(), output_name=f"{run_id}.json",
            )
            assert result.output_path is not None
            assert result.presentation_path is not None
            report = json.loads(result.output_path.read_text())
            presentation = json.loads(result.presentation_path.read_text())
            return result, report, presentation

    def test_durable_run_output_carries_current_status_and_grant_identity(self) -> None:
        universe = _v3_universe()
        acts = _acts_with(
            lambda i: _grant_act(i, grant_id="demo.auth.g1", subject_id=USER, tax_year=SCOPE_YEAR, universe_id=universe),
        )
        result, report, presentation = self._run(acts, "demo.auth.durable-admitted")
        self.assertIsNone(result.refusal)
        # The in-memory outcome and the durable file must agree exactly.
        self.assertEqual(report["current"], result.current)
        self.assertEqual(report["authorization_status"], result.authorization_status)
        self.assertTrue(report["current"])
        self.assertEqual(report["authorization_status"], STATUS_ADMITTED)
        self.assertEqual(report["authorization_grant_id"], "demo.auth.g1")
        # And the production presentation root, not just the durable run
        # file, also carries the resolved authorization.
        self.assertIn("authorization", presentation)
        self.assertEqual(presentation["authorization"]["status"], STATUS_ADMITTED)
        self.assertEqual(presentation["authorization"]["grant_id"], "demo.auth.g1")
        self.assertTrue(presentation["authorization"]["admitted"])

    def test_durable_run_output_carries_non_current_status_and_grant_identity(self) -> None:
        """The same properties hold for a non-current disposition -- a
        reader must be able to tell from the durable file alone that this
        run's authorization is not current, and which grant it was
        resolved against."""
        universe = _v3_universe()
        acts = _acts_with(
            lambda i: _grant_act(i, grant_id="demo.auth.g1", subject_id=USER, tax_year=SCOPE_YEAR, universe_id=universe),
            lambda i: _end_act(i, grant_id="demo.auth.g1", ending="suspend"),
        )
        result, report, presentation = self._run(acts, "demo.auth.durable-suspended")
        self.assertIsNone(result.refusal)
        self.assertFalse(report["current"])
        self.assertEqual(report["authorization_status"], STATUS_SUSPENDED)
        self.assertEqual(report["authorization_grant_id"], "demo.auth.g1")
        self.assertEqual(presentation["authorization"]["status"], STATUS_SUSPENDED)
        self.assertFalse(presentation["authorization"]["admitted"])


class LiveAuthorizationSuspendWithdraw(unittest.TestCase):
    def _run(self, acts: list[dict[str, Any]], run_id: str) -> tuple[LiveCoordinatorOutcome, dict[str, Any] | None]:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = live_coordinate_run(
                WorkspaceCapability(root / "L"), repo_root=CONTENT.parent.parent.parent,
                authoritative_acts=acts, workspace_revision=len(acts), run_scope=RUN_SCOPE,
                scope_user=USER, request={"schema": "run-request.v1"}, run_id=run_id,
                governance_pins=[], surface=_surface(), output_name=f"{run_id}.json",
            )
            report = json.loads(result.output_path.read_text()) if result.output_path is not None else None
            return result, report

    def test_suspension_and_withdrawal_change_currentness_not_tax_arithmetic(self) -> None:
        universe = _v3_universe()
        admitted, admitted_report = self._run(
            _acts_with(lambda i: _grant_act(i, grant_id="demo.auth.g1", subject_id=USER, tax_year=SCOPE_YEAR, universe_id=universe)),
            "demo.auth.suspend.baseline",
        )
        suspended, suspended_report = self._run(
            _acts_with(
                lambda i: _grant_act(i, grant_id="demo.auth.g1", subject_id=USER, tax_year=SCOPE_YEAR, universe_id=universe),
                lambda i: _end_act(i, grant_id="demo.auth.g1", ending="suspend"),
            ),
            "demo.auth.suspend.suspended",
        )
        withdrawn, withdrawn_report = self._run(
            _acts_with(
                lambda i: _grant_act(i, grant_id="demo.auth.g1", subject_id=USER, tax_year=SCOPE_YEAR, universe_id=universe),
                lambda i: _end_act(i, grant_id="demo.auth.g1", ending="withdraw"),
            ),
            "demo.auth.suspend.withdrawn",
        )
        assert admitted_report is not None
        assert suspended_report is not None
        assert withdrawn_report is not None
        self.assertTrue(admitted.current)
        self.assertEqual(admitted.authorization_status, STATUS_ADMITTED)
        self.assertFalse(suspended.current)
        self.assertEqual(suspended.authorization_status, STATUS_SUSPENDED)
        self.assertFalse(withdrawn.current)
        self.assertEqual(withdrawn.authorization_status, STATUS_WITHDRAWN)

        admitted_pub = sorted(
            (row["symbol"], row["disposition"]) for row in admitted_report["dispositions"] if "symbol" in row
        )
        suspended_pub = sorted(
            (row["symbol"], row["disposition"]) for row in suspended_report["dispositions"] if "symbol" in row
        )
        withdrawn_pub = sorted(
            (row["symbol"], row["disposition"]) for row in withdrawn_report["dispositions"] if "symbol" in row
        )
        self.assertEqual(admitted_pub, suspended_pub)
        self.assertEqual(admitted_pub, withdrawn_pub)


class LiveAuthorizationAbsentIsExplicitAndNonCurrent(unittest.TestCase):
    def test_no_authorization_acts_resolves_to_explicit_absent_not_current(self) -> None:
        """Absence must resolve to an
        explicit, named disposition (AUTHORIZATION_ABSENT), never silently
        supply currentness. The calculation still proceeds -- tax arithmetic
        is unaffected, the same suspend/withdraw invariant this milestone
        already established -- but ``current`` must be False, not True."""
        acts = _v3_authoritative_acts()
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = live_coordinate_run(
                WorkspaceCapability(root / "L"), repo_root=CONTENT.parent.parent.parent,
                authoritative_acts=acts, workspace_revision=len(acts), run_scope=RUN_SCOPE,
                scope_user=USER, request={"schema": "run-request.v1"}, run_id="demo.auth.absent",
                governance_pins=[], surface=_surface(), output_name="absent.json",
            )
            assert result.output_path is not None
            report = json.loads(result.output_path.read_text())
        self.assertIsNone(result.refusal)
        self.assertFalse(result.current)
        self.assertEqual(result.authorization_status, STATUS_ABSENT)
        # Same tax arithmetic as an admitted run: only currentness differs.
        published = {row["symbol"] for row in report["dispositions"] if row["disposition"] == "published"}
        self.assertIn("tax.us.2025.tax.total-tax", published)


class ReauthorizationBoundaryThroughTheLivePath(unittest.TestCase):
    """Exercises ``_resolve_run_authorization`` directly (the
    live path's own authorization function) against a synthetic corpus
    mirroring ``tests/derivation/test_authorization_closure.py``, proving
    ``root_rule_ids`` (package entrypoints, not every
    resolved rule) preserves both counterexamples ADR-0069 Decision 5
    requires."""

    def _corpus(self) -> dict[str, dict[str, Any]]:
        return {
            "demo.rule.ordinary-subtotal": {
                "id": "demo.rule.ordinary-subtotal", "version": "v1", "schema": "rule-artifact.v3",
                "requires": ["demo.scale.convention"], "publishes": "demo.ordinary.subtotal", "when": True,
                "value": {"op": "ref", "name": "demo.scale.convention"},
            },
            "demo.scale.convention": {
                "id": "demo.scale.convention", "version": "v1", "schema": "rule-artifact.v3",
                "publishes": "demo.scale.convention", "requires": [], "when": True,
                "value": {"op": "literal", "value": "half-up"},
            },
        }

    def _package(self) -> dict[str, Any]:
        return {"version": "v2", "entrypoints": [{"id": "demo.rule.ordinary-subtotal", "version": "v1"}]}

    def test_unrelated_resolved_rule_outside_entrypoints_does_not_force_reauth(self) -> None:
        corpus = self._corpus()
        package = self._package()
        root = {"demo.rule.ordinary-subtotal"}
        universe = package_boundary_digest(root, corpus, package=package)
        acts = [_grant_act(0, grant_id="demo.auth.g1", subject_id="demo.subject.a", tax_year="2025", universe_id=universe)]
        rules = [corpus["demo.rule.ordinary-subtotal"], corpus["demo.scale.convention"]]
        baseline = _resolve_run_authorization(
            acts, run_scope={"year": "2025"}, scope_user="demo.subject.a", rules=rules,
            corpus=corpus, package=package,
        )
        self.assertTrue(baseline.admitted)

        # An unrelated rule the package resolved (e.g. for a separate
        # line) is NOT one of the package's declared entrypoints -- adding
        # it to this run's resolved rule set must not change the digest.
        corpus_after = dict(corpus)
        corpus_after["demo.rule.unrelated-subtotal"] = {
            "id": "demo.rule.unrelated-subtotal", "version": "v1", "schema": "rule-artifact.v3",
            "requires": [], "publishes": "demo.unrelated.subtotal", "when": True,
            "value": {"op": "literal", "value": "0"},
        }
        rules_after = rules + [corpus_after["demo.rule.unrelated-subtotal"]]
        after = _resolve_run_authorization(
            acts, run_scope={"year": "2025"}, scope_user="demo.subject.a", rules=rules_after,
            corpus=corpus_after, package=package,
        )
        self.assertTrue(after.admitted)
        self.assertEqual(after.grant_id, baseline.grant_id)

    def test_edit_inside_the_entrypoint_closure_forces_reauth(self) -> None:
        corpus = self._corpus()
        package = self._package()
        root = {"demo.rule.ordinary-subtotal"}
        universe = package_boundary_digest(root, corpus, package=package)
        acts = [_grant_act(0, grant_id="demo.auth.g1", subject_id="demo.subject.a", tax_year="2025", universe_id=universe)]
        rules = [corpus["demo.rule.ordinary-subtotal"], corpus["demo.scale.convention"]]
        baseline = _resolve_run_authorization(
            acts, run_scope={"year": "2025"}, scope_user="demo.subject.a", rules=rules,
            corpus=corpus, package=package,
        )
        self.assertTrue(baseline.admitted)

        corpus_edited = dict(corpus)
        corpus_edited["demo.scale.convention"] = dict(corpus["demo.scale.convention"])
        corpus_edited["demo.scale.convention"]["value"] = {"op": "literal", "value": "half-even"}
        rules_edited = [corpus_edited["demo.rule.ordinary-subtotal"], corpus_edited["demo.scale.convention"]]
        edited = _resolve_run_authorization(
            acts, run_scope={"year": "2025"}, scope_user="demo.subject.a", rules=rules_edited,
            corpus=corpus_edited, package=package,
        )
        self.assertFalse(edited.admitted)


class NewEntrypointGrowthAgainstDeclaredCalculationScope(unittest.TestCase):
    """The real growth case is a new
    *entrypoint* being added to the package, not merely an unrelated rule
    already present in the resolved graph. ``_resolved_run_material``
    resolves every member of the whole adopted package each run (there is
    no run-request field able to select one calculation, ADR-0032 Decision
    3), so a package-entrypoint-set root that grows with the package grows
    the digest even when the new entrypoint is genuinely unrelated to this
    calculation.

    A ``calculation-scope-declaration`` act naming the rule(s) a
    workspace's calculation actually composes (ADR-0069 Decision 5
    successor) can still *widen* that root, but -- since production has no
    mechanism that actually narrows execution to a declared scope, and
    still resolves and publishes every entrypoint in the adopted package --
    a declaration can never shield an entrypoint this run actually
    executes and publishes from the reauthorization boundary."""

    def _corpus(self) -> dict[str, dict[str, Any]]:
        return {
            "demo.rule.ordinary-subtotal": {
                "id": "demo.rule.ordinary-subtotal", "version": "v1", "schema": "rule-artifact.v3",
                "requires": ["demo.scale.convention"], "publishes": "demo.ordinary.subtotal", "when": True,
                "value": {"op": "ref", "name": "demo.scale.convention"},
            },
            "demo.scale.convention": {
                "id": "demo.scale.convention", "version": "v1", "schema": "rule-artifact.v3",
                "publishes": "demo.scale.convention", "requires": [], "when": True,
                "value": {"op": "literal", "value": "half-up"},
            },
        }

    def _package(self) -> dict[str, Any]:
        return {"version": "v2", "entrypoints": [{"id": "demo.rule.ordinary-subtotal", "version": "v1"}]}

    def _new_topic_entrypoint(self) -> dict[str, Any]:
        return {
            "id": "demo.rule.new-topic-subtotal", "version": "v1", "schema": "rule-artifact.v3",
            "requires": [], "publishes": "demo.new-topic.subtotal", "when": True,
            "value": {"op": "literal", "value": "0"},
        }

    def test_new_entrypoint_forces_reauth_without_a_declared_scope(self) -> None:
        """Names the gap plainly: with no scope declaration, growing the
        package's entrypoint set still forces reauthorization even though
        the new entrypoint is unrelated to this calculation -- this is the
        boundary that stays over-broad for any caller that never declares
        its calculation scope."""
        corpus = self._corpus()
        package = self._package()
        root = {"demo.rule.ordinary-subtotal"}
        universe = package_boundary_digest(root, corpus, package=package)
        acts = [_grant_act(0, grant_id="demo.auth.g1", subject_id="demo.subject.a", tax_year="2025", universe_id=universe)]
        rules = [corpus["demo.rule.ordinary-subtotal"], corpus["demo.scale.convention"]]
        baseline = _resolve_run_authorization(
            acts, run_scope={"year": "2025"}, scope_user="demo.subject.a", rules=rules,
            corpus=corpus, package=package,
        )
        self.assertTrue(baseline.admitted)

        new_topic = self._new_topic_entrypoint()
        corpus_after = dict(corpus)
        corpus_after[new_topic["id"]] = new_topic
        package_after = {
            "version": "v2",
            "entrypoints": package["entrypoints"] + [{"id": new_topic["id"], "version": "v1"}],
        }
        # Whole-package resolution now resolves the new entrypoint's rule too
        # (there is no run-request field able to select just one line).
        rules_after = rules + [new_topic]
        after = _resolve_run_authorization(
            acts, run_scope={"year": "2025"}, scope_user="demo.subject.a", rules=rules_after,
            corpus=corpus_after, package=package_after,
        )
        self.assertFalse(after.admitted)
        self.assertEqual(after.status, "AUTHORIZATION_UNIVERSE_SUPERSEDED")

    def test_declared_scope_does_not_shield_an_entrypoint_the_run_actually_executes(self) -> None:
        """A
        calculation-scope-declaration that OMITS an entrypoint the package
        still resolves and executes must not shield that entrypoint from
        the reauthorization boundary. Production has no run-request field
        able to select one calculation (ADR-0032 Decision 3), so it
        resolves and publishes every adopted-package entrypoint regardless
        of any declared scope. A new entrypoint added to the executed
        package while the declared scope excludes it must not be treated
        as still admitted -- the run must not publish output for a
        calculation the declared scope does not cover while authorization
        is reported as current. The required property: since the new
        entrypoint is genuinely executed and published this run, the
        boundary must include it and force reauthorization, exactly as it
        would with no declared scope at all."""
        corpus = self._corpus()
        package = self._package()
        root = {"demo.rule.ordinary-subtotal"}
        universe = package_boundary_digest(root, corpus, package=package)
        acts = [
            _grant_act(0, grant_id="demo.auth.g1", subject_id="demo.subject.a", tax_year="2025", universe_id=universe),
            _scope_act(1, scope_id="demo.scope.s1", subject_id="demo.subject.a", tax_year="2025", rule_ids=["demo.rule.ordinary-subtotal"]),
        ]
        rules = [corpus["demo.rule.ordinary-subtotal"], corpus["demo.scale.convention"]]
        baseline = _resolve_run_authorization(
            acts, run_scope={"year": "2025"}, scope_user="demo.subject.a", rules=rules,
            corpus=corpus, package=package,
        )
        self.assertTrue(baseline.admitted)

        new_topic = self._new_topic_entrypoint()
        corpus_after = dict(corpus)
        corpus_after[new_topic["id"]] = new_topic
        package_after = {
            "version": "v2",
            "entrypoints": package["entrypoints"] + [{"id": new_topic["id"], "version": "v1"}],
        }
        # The new entrypoint is genuinely resolved and executed by this run
        # (there is no execution-scoping mechanism -- the declared scope
        # names only the calculation the workspace composes, it does not
        # narrow what the whole-package resolver actually runs).
        rules_after = rules + [new_topic]
        after = _resolve_run_authorization(
            acts, run_scope={"year": "2025"}, scope_user="demo.subject.a", rules=rules_after,
            corpus=corpus_after, package=package_after,
        )
        self.assertFalse(after.admitted)
        self.assertEqual(after.status, "AUTHORIZATION_UNIVERSE_SUPERSEDED")

    def test_declared_scope_still_widens_boundary_for_a_rule_outside_entrypoints(self) -> None:
        """A declared scope can still add to the boundary (e.g. naming a
        dependency the resolver would not otherwise root on), it simply
        can never remove an entrypoint this run actually executes. This
        preserves Decision 5's original intent -- declaring the exact
        calculation composed -- without ever letting the boundary fall
        below the actually-published result."""
        corpus = self._corpus()
        package = self._package()
        root = {"demo.rule.ordinary-subtotal"}
        universe_without_declaration = package_boundary_digest(root, corpus, package=package)
        acts_without_scope = [
            _grant_act(0, grant_id="demo.auth.g1", subject_id="demo.subject.a", tax_year="2025", universe_id=universe_without_declaration),
        ]
        rules = [corpus["demo.rule.ordinary-subtotal"], corpus["demo.scale.convention"]]
        no_scope = _resolve_run_authorization(
            acts_without_scope, run_scope={"year": "2025"}, scope_user="demo.subject.a", rules=rules,
            corpus=corpus, package=package,
        )
        self.assertTrue(no_scope.admitted)

        # A declaration naming a genuinely unrelated rule (no dependency
        # relationship to the entrypoint closure, so it is not already
        # folded into the boundary through ordinary reachability) widens
        # the digest -- a grant computed against the narrower, undeclared
        # universe is now stale, not admitted.
        corpus_with_extra = dict(corpus)
        corpus_with_extra["demo.rule.declared-only"] = {
            "id": "demo.rule.declared-only", "version": "v1", "schema": "rule-artifact.v3",
            "requires": [], "publishes": "demo.declared-only.value", "when": True,
            "value": {"op": "literal", "value": "0"},
        }
        acts_with_scope = [
            _grant_act(0, grant_id="demo.auth.g2", subject_id="demo.subject.a", tax_year="2025", universe_id=universe_without_declaration),
            _scope_act(1, scope_id="demo.scope.s1", subject_id="demo.subject.a", tax_year="2025", rule_ids=["demo.rule.ordinary-subtotal", "demo.rule.declared-only"]),
        ]
        with_scope = _resolve_run_authorization(
            acts_with_scope, run_scope={"year": "2025"}, scope_user="demo.subject.a", rules=rules,
            corpus=corpus_with_extra, package=package,
        )
        self.assertFalse(with_scope.admitted)

    def test_declared_scope_still_forces_reauth_on_edit_inside_scope(self) -> None:
        """A declared scope only ever widens the executed-entrypoint
        boundary; it never narrows it. An edit to the one rule the
        declaration names must still force reauthorization."""
        corpus = self._corpus()
        package = self._package()
        root = {"demo.rule.ordinary-subtotal"}
        universe = package_boundary_digest(root, corpus, package=package)
        acts = [
            _grant_act(0, grant_id="demo.auth.g1", subject_id="demo.subject.a", tax_year="2025", universe_id=universe),
            _scope_act(1, scope_id="demo.scope.s1", subject_id="demo.subject.a", tax_year="2025", rule_ids=["demo.rule.ordinary-subtotal"]),
        ]
        rules = [corpus["demo.rule.ordinary-subtotal"], corpus["demo.scale.convention"]]
        baseline = _resolve_run_authorization(
            acts, run_scope={"year": "2025"}, scope_user="demo.subject.a", rules=rules,
            corpus=corpus, package=package,
        )
        self.assertTrue(baseline.admitted)

        corpus_edited = dict(corpus)
        corpus_edited["demo.scale.convention"] = dict(corpus["demo.scale.convention"])
        corpus_edited["demo.scale.convention"]["value"] = {"op": "literal", "value": "half-even"}
        rules_edited = [corpus_edited["demo.rule.ordinary-subtotal"], corpus_edited["demo.scale.convention"]]
        edited = _resolve_run_authorization(
            acts, run_scope={"year": "2025"}, scope_user="demo.subject.a", rules=rules_edited,
            corpus=corpus_edited, package=package,
        )
        self.assertFalse(edited.admitted)


class ScopeDeclarationProducerFoldAndLiveResolutionAgree(unittest.TestCase):
    """``workspace-calculation-scope.v1``/``act-calculation-scope-declaration.
    v1`` state ADR-0069's accepted contract: a declaration's named rule ids
    are unioned into the executed-entrypoint authorization root and can only
    widen it, never replace or narrow it below what the run actually
    executes and publishes.

    Validating the payload directly with
    ``DerivationSchemas.validate`` and then injecting the hand-built act
    straight into ``authoritative_acts`` bypasses ``ActLog.append`` and
    ``ActLog.read`` entirely -- exactly the boundary the act log's own
    payload-schema selector (``packages/kernel/act_log.py:
    _payload_schema_id``) enforces on every real append and read. These
    tests exercise all three parties together through the real record
    boundary: a producer citizen appended to and reread from a real
    ``ActLog``; the fold (``authorization.project``/
    ``resolve_for_composition``); and live resolution
    (``live_coordinate_run``) against the real v3 fixture.
    """

    def test_scope_declaration_validates_against_its_published_schema(self) -> None:
        """Producer conformance: the act this suite builds is schema-valid
        against the citizen and act payload contracts."""
        from packages.derivation.loader import DerivationSchemas

        schemas = DerivationSchemas()
        scope_act = _scope_act(
            0, scope_id="demo.scope.v1", subject_id=USER, tax_year=SCOPE_YEAR,
            rule_ids=["demo.rule.unrelated-widen"],
        )
        schemas.validate("act-calculation-scope-declaration.v1", scope_act["payload"])
        schemas.validate("workspace-calculation-scope.v1", scope_act["payload"]["scope"])

    def test_scope_declaration_appends_and_rereads_through_a_real_act_log(self) -> None:
        """A real ``ActLog.append`` followed by a real ``ActLog.read``,
        not direct schema validation plus injected ``authoritative_acts``.
        The reread act must round-trip byte-for-byte on the fields that
        matter (kind, and the nested citizen's schema and content)."""
        scope_act = _scope_act(
            0, scope_id="demo.scope.v1", subject_id=USER, tax_year=SCOPE_YEAR,
            rule_ids=["demo.rule.unrelated-widen"],
        )
        with TemporaryDirectory() as tmp:
            reread = _append_and_reread([scope_act], Path(tmp) / "ws")
        self.assertEqual(len(reread), 1)
        self.assertEqual(reread[0]["kind"], "calculation-scope-declaration")
        self.assertEqual(reread[0]["payload"], scope_act["payload"])
        self.assertEqual(reread[0]["payload"]["scope"]["schema"], "workspace-calculation-scope.v1")

    def test_malformed_scope_declaration_fails_closed_on_append(self) -> None:
        """Negative control: a payload whose nested citizen omits the
        schema's own required field (``rule_ids``) must be rejected by
        ``ActLog.append`` with a clear validation error -- never silently
        coerced and never crashing somewhere downstream instead."""
        malformed_act = _live_act(0, "calculation-scope-declaration", {"scope": {
            "schema": "workspace-calculation-scope.v1",
            "id": "demo.scope.malformed",
            "subject_id": USER,
            "tax_year": SCOPE_YEAR,
            # rule_ids omitted: required by the citizen schema.
        }})
        with TemporaryDirectory() as tmp:
            log = ActLog(Path(tmp) / "ws", workspace_registry())
            with self.assertRaises(SchemaValidationError) as ctx:
                log.append(malformed_act, 0)
            self.assertIn("act-calculation-scope-declaration.v1", str(ctx.exception))
            # And it must not have been partially committed.
            self.assertEqual(log.read().acts, ())

    def test_scope_declaration_omitting_the_real_entrypoint_does_not_narrow_the_live_boundary(self) -> None:
        """A declared scope that names no rule overlapping the run's real
        entrypoint must not be able to shrink the reauthorization boundary
        away from what this run actually executes and publishes -- runtime
        unions rather
        than replaces. The declared rule id here is not in the v3 package's
        corpus at all, so it contributes nothing to the digest; the live
        boundary must still equal the no-declaration boundary exactly, and
        the run must still admit and publish.

        Both act sequences are
        appended to and reread from a real ``ActLog`` before being fed to
        ``live_coordinate_run`` -- not hand-built and injected directly."""
        universe = _v3_universe()
        acts_no_scope = _acts_with(
            lambda i: _grant_act(i, grant_id="demo.auth.g1", subject_id=USER, tax_year=SCOPE_YEAR, universe_id=universe),
        )
        acts_with_scope = _acts_with(
            lambda i: _grant_act(i, grant_id="demo.auth.g1", subject_id=USER, tax_year=SCOPE_YEAR, universe_id=universe),
            lambda i: _scope_act(
                i, scope_id="demo.scope.v1", subject_id=USER, tax_year=SCOPE_YEAR,
                rule_ids=["demo.rule.unrelated-widen"],
            ),
        )

        def _run(acts: list[dict[str, Any]], run_id: str) -> tuple[LiveCoordinatorOutcome, dict[str, Any]]:
            with TemporaryDirectory() as tmp:
                root = Path(tmp)
                reread_acts = _append_and_reread(acts, root / "log")
                result = live_coordinate_run(
                    WorkspaceCapability(root / "L"), repo_root=CONTENT.parent.parent.parent,
                    authoritative_acts=reread_acts, workspace_revision=len(reread_acts), run_scope=RUN_SCOPE,
                    scope_user=USER, request={"schema": "run-request.v1"}, run_id=run_id,
                    governance_pins=[], surface=_surface(), output_name=f"{run_id}.json",
                )
                assert result.output_path is not None
                report = json.loads(result.output_path.read_text())
                return result, report

        no_scope_result, no_scope_report = _run(acts_no_scope, "demo.auth.scope.baseline")
        with_scope_result, with_scope_report = _run(acts_with_scope, "demo.auth.scope.declared")

        # The declaration omits the real entrypoint entirely, yet the
        # declaration must never narrow the boundary below it: both runs
        # resolve identically.
        self.assertEqual(with_scope_result.authorization_status, no_scope_result.authorization_status)
        self.assertEqual(with_scope_result.authorization_status, STATUS_ADMITTED)
        self.assertTrue(with_scope_result.current)
        self.assertEqual(with_scope_result.authorization_status, with_scope_report["authorization_status"])
        # Execution itself is never narrowed by the declaration either --
        # the real entrypoint's output still publishes in both runs.
        no_scope_published = {row["symbol"] for row in no_scope_report["dispositions"] if row["disposition"] == "published"}
        with_scope_published = {row["symbol"] for row in with_scope_report["dispositions"] if row["disposition"] == "published"}
        self.assertEqual(no_scope_published, with_scope_published)
        self.assertIn("tax.us.2025.tax.total-tax", with_scope_published)


class ProductionResolverStillResolvesTheV3Package(unittest.TestCase):
    """A sanity check that the fixture used above is a real,
    independently resolvable package (not itself a test artifact)."""

    def test_v3_resolves(self) -> None:
        acts = _v3_authoritative_acts()
        graph = resolve_production_package(
            acts, run_scope=RUN_SCOPE, scope_user=USER, workspace_revision=len(acts), surface=_surface(),
        )
        self.assertIsInstance(graph, ResolvedGraph)


if __name__ == "__main__":
    unittest.main()
