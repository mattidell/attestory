"""Live production wiring of ADR-0072's collision trigger AND the complete
migration-adoption sequence out of legacy/pairing coexistence.

Reproduces, through the real production coordinator (``live_coordinate_run``,
not a bespoke unit-test-only harness), four cases:

(a) legacy ``42`` + a new same-amount pairing must not silently double-
    subtract -- the collision trigger inside ``packages.tax.identity_
    association.associate()`` refuses the new pairing until the legacy
    finding is resolved via its own declared ``supersession.policy: "free"``
    (a same-fact-id correction), never a new displacement edge;
(b) a legacy-only workspace (no pairing ever created) is completely
    unaffected;
(c) two genuinely different obligations (different dollar amounts) still
    both correctly sum -- the amount-equality signal stays silent;
(d) the actual, complete,
    documented-in-ADR-0072 migration-adoption sequence executes end to end
    against the real, migrated ``package.core-calculations.v35`` -- legacy
    ``42`` plus a same-amount pairing ``42.0``, but with the successor bundle adopted
    and the migration-adoption act taken up *before* the pairing is
    evaluated. Retiring the legacy fact type this way clears the collision
    signal entirely (there is no longer any live legacy source to compare
    against), the presented successor claim is produced for the retired
    finding, the single-subtractand v6 line-2b rule computes 458 through
    only the pairing-scoped subtotal, and the real presentation/report path
    traces correct provenance (dispositions' declared pins, the line-2b
    citation section) for the migrated result.

``packages.kernel.facts.apply_migration_
adoption`` requires every successor fact type to already be current
(admitted by its own ``bundle-adoption`` act) before a migration-adoption
act naming it can apply. Case (d) below is that complete sequence,
verified for real.

Built on ``tests.test_package_membership_wiring``'s T2 fixture (the same
real acquisition/report/pairing machinery ADR-0068 established), with
one legacy Schedule B accrued-interest member injected into the
already-closed legacy family. The unmigrated cases resolve against the
real, currently published coexistence package
``package.core-calculations.v34`` (the same package
``tests.test_aggregate_supportability_live`` resolves); the migrated cases
resolve against its real, additive successor ``package.core-calculations.
v35``, which admits the migrated v6 line-2b rule and the migration content
this file exercises.
"""

from __future__ import annotations

import json
import unittest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.kernel.act_log import ActLog
from packages.kernel.findings import (
    MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM,
    FindingModelError,
    project,
)
from packages.kernel.schema_registry import SchemaRegistry, SchemaValidationError
from packages.tax.identity_association import (
    ASSOCIATION_MIGRATION_ADOPTION_REQUIRED,
    ASSOCIATION_SYMBOL,
)
from packages.tax.loader import tax_registry
from packages.tax.obligation_acquisition_mapping import (
    derive_obligation_acquisition_fact_id,
)
from packages.derivation.production_resolver import PublicationSurface
from packages.tax.loader import TAX_CONTENT_DIR
from packages.tax.pairing_consequences import CURRENT_YEAR_SUBTOTAL_SYMBOL
from tests.test_form1099g_box1_schedule1_line7 import _act, _attested
from tests.test_ssa1099_benefits_line6_track2 import SCOPE_KEY
from tests.test_package_membership_wiring import (
    FIXTURES,
    ROOT,
    USER,
    SCOPE,
    _load,
    _surface as _surface_v34,
    _t2_acts,
)

LEGACY_FAMILY = "tax.us.2025.scheduleb.adjustment.accrued-interest"
LEGACY_TYPE = "tax.us.2025.scheduleb.adjustment.accrued-interest.amount"
LEGACY_CLOSURE_TYPE = "tax.us.2025.scheduleb.adjustment.accrued-interest.source-closure"
LEGACY_SUBTOTAL_SYMBOL = "tax.us.2025.interest.scheduleb-accrued-interest-subtotal"

# The migrated successor generation (v35), additive over the coexistence
# v34 this fixture's own T2 base adopts.
MIGRATED_REGISTRY_FILE = "published-packages.v30.json"
MIGRATED_ADOPTION_FILE = "adopt-core-v35-current.json"


def _surface_v35() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        TAX_CONTENT_DIR / MIGRATED_REGISTRY_FILE,
        TAX_CONTENT_DIR,
    )


def _load_migrated_adoption() -> dict[str, Any]:
    return cast(
        dict[str, Any],
        json.loads((FIXTURES / "adoptions" / MIGRATED_ADOPTION_FILE).read_text("utf-8")),
    )

# ADR-0072/ADR-0063 successor citizens: the
# real bundle-adoption act the documented sequence requires, and the
# real migration-adoption act.
SUCCESSOR_BUNDLE_FILE = "scheduleb-accrued-interest-migrated.bundle.json"
MIGRATION_ARTIFACT_FILE = "scheduleb-accrued-interest.succession.json"
SUCCESSOR_TYPE = "tax.us.2025.interest.accrued-interest-migrated.presented-claim"
MIGRATION_ID = "tax.us.2025.scheduleb-accrued-interest.succession"
LINE2B_RULE_ID = "tax.us.2025.rule.form1040-line2b"


def _pairing_acquisition_fact_id() -> str:
    """The real, current fact_id of T2's ordinary-acquisition finding (the
    new pairing path's own re-established-obligation representation).

    A withdrawal's ``corresponds_to_fact_id`` naming this fact id has no
    effect on migration: a nonzero legacy claim blocks migration
    regardless of any named correspondence, because the legacy fact type
    carries no obligation, payer, or report identity for any
    correspondence to be checked against. This helper is retained to
    build the "genuine
    correspondence, still refused" and "real-but-wrong correspondence"
    regressions, which prove the field is inert for a nonzero claim
    either way."""
    from tests.test_package_membership_wiring import _t2_answers

    answers = _t2_answers()
    return derive_obligation_acquisition_fact_id(
        payer_name=answers["payer_name"],
        obligation_reference=answers.get("obligation_reference"),
        obligation_description=answers["obligation_description"],
        acquisition_date=answers["acquisition_date"],
    )


def _registry_with_migration_resolution_policy() -> SchemaRegistry:
    """A registry with the domain migration-resolution-policy map installed
    (ADR-0072 Decision 4): the
    same ``tax_registry()`` other direct-``project()`` tests in this
    milestone already use, which installs
    ``install_domain_companion_presence`` -- the exact function
    ``live_coordinate_run`` already calls unconditionally, and which now
    also folds in the migration-resolution-policy map."""
    return tax_registry()


def _find_legacy_closure(acts: list[dict[str, object]]) -> tuple[int, str]:
    """The already-closed-empty legacy family's closure act and horizon id.

    The shared base fixture (``tests.test_f1098e_student_loan_interest_agi_
    track6._f1098e_acts`` -> ``tests.test_ssa1099_benefits_line6_track2.
    _ssa_acts`` -> ``tests.test_form1099g_box1_schedule1_line7._ug_acts``)
    already closes this family empty so line-2b's ``require_closed`` is
    satisfied. Injecting a real member means reopening that same horizon
    lineage with one more member, then re-closing on a successor horizon --
    never asserting a second, competing closure at the same horizon id.
    """
    for index, act in enumerate(acts):
        if act.get("kind") != "assertion":
            continue
        payload = cast(dict[str, Any], act["payload"])
        finding = cast(dict[str, Any], payload.get("finding") or {})
        fact_id = str(finding.get("fact_id", ""))
        if fact_id.startswith(LEGACY_CLOSURE_TYPE + "|"):
            horizon_id = fact_id.split("family-horizon=")[1].split(",")[0]
            return index, horizon_id
    raise AssertionError("legacy accrued-interest closure act not found in base fixture")


def _inject_legacy_accrued_interest(
    acts: list[dict[str, object]],
    *,
    amount: float,
    instance: str,
    finding_id: str,
) -> list[dict[str, object]]:
    """Reopen the already-closed-empty legacy family with one real member.

    Mirrors ``tests.test_schedule_b_interest_adjustments._adjustment_acts``'s
    own member-then-reclose pattern: introduce the adjustment-instance
    entity, assert the member via ``member-transition`` onto a successor
    horizon, then move the closure assertion onto that successor horizon --
    never a second competing closure at the original (now-stale) horizon.
    """
    acts = [dict(a) for a in acts]
    closure_idx, horizon_id = _find_legacy_closure(acts)
    new_horizon = f"{horizon_id}.legacy.{instance.rsplit('.', 1)[-1]}"
    entity_act = _act(
        closure_idx,
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": instance,
                "kind": "tax.us.scheduleb-adjustment-instance",
                "label": f"Synthetic legacy accrued-interest instance {instance}",
            }
        },
    )
    member_act = _act(
        closure_idx + 1,
        "member-transition",
        {
            "family": {"id": LEGACY_FAMILY, "version": "v1"},
            "scope": SCOPE_KEY,
            "member": {
                "action": "assert",
                "finding": _attested(
                    finding_id,
                    f"{LEGACY_TYPE}|tax-year=2025,adjustment-instance={instance}",
                    amount,
                ),
            },
            "successor": {"id": new_horizon, "predecessor": horizon_id},
        },
    )
    closure_act = dict(acts[closure_idx])
    closure_payload = dict(cast(dict[str, Any], closure_act["payload"]))
    closure_finding = dict(cast(dict[str, Any], closure_payload["finding"]))
    closure_finding["id"] = f"{closure_finding['id']}.{instance.rsplit('.', 1)[-1]}"
    closure_finding["fact_id"] = f"{LEGACY_CLOSURE_TYPE}|family-horizon={new_horizon},tax-year=2025"
    closure_payload["finding"] = closure_finding
    closure_act["payload"] = closure_payload
    acts[closure_idx] = closure_act
    acts.insert(closure_idx, member_act)
    acts.insert(closure_idx, entity_act)
    return acts


def _renumber(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    for index, act in enumerate(acts):
        act["committed_against"] = index
        act["act_id"] = f"demo.legacy-coexistence.act.{index:03d}"
        act["actor"] = USER
    return acts


def _successor_bundle_act(index: int) -> dict[str, Any]:
    """The bundle-adoption act ADR-0072's and the generator's documented
    sequence requires: admits the
    presented-claim successor fact type as current, which
    ``packages.kernel.facts.apply_migration_adoption`` requires before the
    migration-adoption act below may name it as a successor."""
    return _act(index, "bundle-adoption", {"bundle": _load(SUCCESSOR_BUNDLE_FILE)})


def _migration_act(index: int) -> dict[str, Any]:
    return _act(index, "migration-adoption", {"migration": _load(MIGRATION_ARTIFACT_FILE)})


def _resolve_legacy_act(index: int, *, instance: str) -> dict[str, Any]:
    """Same-identity correction to zero -- ADR-0072's own established
    amount-collision resolution mechanism, generalized by the
    ``resolved-required`` migration-resolution policy: a second assertion
    at the SAME legacy fact_id, the
    fact type's own declared ``supersession.policy: "free"``, never a new
    displacement edge.

    Valid ONLY when the amount genuinely became zero: asserting this for a claim that is still true would
    itself be a false historical proposition. The migration-adoption tests
    below use ``_withdraw_legacy_accrued_interest`` instead for the
    same-obligation-re-established scenario; this function remains for the
    narrower genuinely-zero case."""
    return _act(
        index,
        "assertion",
        {
            "finding": _attested(
                f"demo.legacy.finding.{instance}.superseded",
                f"{LEGACY_TYPE}|tax-year=2025,adjustment-instance={instance}",
                0,
            )
        },
    )


def _withdraw_legacy_accrued_interest(
    acts: list[dict[str, object]],
    *,
    instance: str,
    corresponds_to_fact_id: str | None = None,
) -> list[dict[str, object]]:
    """Withdraw a previously injected legacy finding via an ordinary
    member-transition removal (ADR-0017) -- the honest resolution
    mechanism for the "same obligation re-established on the new pairing
    path" scenario. This retires the
    finding's computational role (it becomes displaced via currency.py's
    ``_member_withdrawals``, a "withdrawal" reason, never a "correction")
    while leaving the finding and its true historical ``value`` in
    ``state.findings`` completely unmodified -- unlike ``_resolve_legacy_
    act``, no second finding is ever written for this fact_id.

    ``corresponds_to_fact_id`` (act-member-transition.v3): names the fact_id of whatever current
    finding actually took over the withdrawn fact's computational role.
    Omitted by default -- a bare removal is still a schema-conformant
    withdrawal, it simply cannot resolve a ``resolved-required``
    migration's unresolved predecessor claim on its own; a caller must
    supply the real correspondence to prove a genuine same-obligation
    resolution.

    Mirrors ``_inject_legacy_accrued_interest``'s own reopen-then-reclose
    pattern in reverse: remove the member onto a successor horizon, then
    move the closure assertion onto that same successor horizon -- never
    a second, competing closure at the stale horizon.
    """
    acts = [dict(a) for a in acts]
    closure_idx, horizon_id = _find_legacy_closure(acts)
    new_horizon = f"{horizon_id}.withdrawn"
    fact_id = f"{LEGACY_TYPE}|tax-year=2025,adjustment-instance={instance}"
    member: dict[str, Any] = {"action": "remove", "fact_id": fact_id}
    if corresponds_to_fact_id is not None:
        member["corresponds_to_fact_id"] = corresponds_to_fact_id
    member_act = _act(
        closure_idx,
        "member-transition",
        {
            "family": {"id": LEGACY_FAMILY, "version": "v1"},
            "scope": SCOPE_KEY,
            "member": member,
            "successor": {"id": new_horizon, "predecessor": horizon_id},
        },
    )
    closure_act = dict(acts[closure_idx])
    closure_payload = dict(cast(dict[str, Any], closure_act["payload"]))
    closure_finding = dict(cast(dict[str, Any], closure_payload["finding"]))
    closure_finding["id"] = f"{closure_finding['id']}.withdrawn"
    closure_finding["fact_id"] = (
        f"{LEGACY_CLOSURE_TYPE}|family-horizon={new_horizon},tax-year=2025"
    )
    closure_payload["finding"] = closure_finding
    closure_act["payload"] = closure_payload
    acts[closure_idx] = closure_act
    acts.insert(closure_idx, member_act)
    return acts


def _acts_with_legacy(
    *,
    amount: float,
    instance: str = "demo.sbia.legacy.instance.0",
    with_pairing: bool,
    migrate: bool = False,
    resolve_legacy_before_migration: bool = False,
    resolve_via_zero_correction: bool = False,
    withdrawal_corresponds_to_fact_id: str | None = None,
) -> list[dict[str, object]]:
    """T2's real production pairing fixture, plus one injected legacy finding.

    ``with_pairing=False`` drops the ordinary-acquisition contribution and
    the pairing package-adoption context entirely: a legacy-only workspace
    where Seam 2 never even runs (case (b)).

    ``migrate=True`` inserts the complete corrected migration sequence
    (case (d)): the successor bundle-adoption act, then the real
    migration-adoption act, both committed before the final package-
    adoption act -- so the legacy fact type is already retired by the
    time the workspace's pairing is evaluated for the collision signal.

    ``resolve_legacy_before_migration=True`` resolves the legacy claim
    immediately before the successor bundle-adoption act, so migration
    attempted afterward finds no unresolved legacy claim and succeeds
    under the ``resolved-required`` policy. By default this withdraws the finding via an ordinary
    member-transition removal (``_withdraw_legacy_accrued_interest``) -- the honest mechanism for "the
    same obligation was independently re-established on the new pairing
    path" -- which never touches the finding's true historical value.
    ``resolve_via_zero_correction=True`` instead uses the narrower,
    same-identity zero correction (``_resolve_legacy_act``), valid only
    when the amount genuinely became zero.

    ``withdrawal_corresponds_to_fact_id`` is forwarded to the withdrawal act's optional
    ``corresponds_to_fact_id``. Omitted by default: a bare withdrawal
    naming no correspondence at all is insufficient on its own to resolve a
    ``resolved-required`` migration's predecessor claim.
    """
    acts = _t2_acts()
    original_adoption = acts.pop()  # T2 fixture's own v34 (coexistence) package-adoption act
    if not with_pairing:
        acts = [
            act
            for act in acts
            if not (
                act.get("kind") == "contribution"
                or (
                    act.get("kind") == "assertion"
                    and str(
                        cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("finding", {})).get(
                            "fact_id", ""
                        )
                    ).startswith("tax.us.obligation-acquisition-circumstance|")
                )
            )
        ]
    acts = _inject_legacy_accrued_interest(
        acts, amount=amount, instance=instance, finding_id=f"demo.legacy.finding.{instance}"
    )
    if migrate:
        if resolve_legacy_before_migration:
            if resolve_via_zero_correction:
                acts.append(_resolve_legacy_act(len(acts), instance=instance))
            else:
                acts = _withdraw_legacy_accrued_interest(
                    acts,
                    instance=instance,
                    corresponds_to_fact_id=withdrawal_corresponds_to_fact_id,
                )
        # The complete sequence: admit the successor type, THEN adopt the migration -- both
        # committed before the real package-adoption act, so the legacy
        # fact type is already retired by the time the pairing itself is
        # evaluated.
        acts.append(_successor_bundle_act(len(acts)))
        acts.append(_migration_act(len(acts)))
        adoption = _load_migrated_adoption()
    else:
        # An unmigrated workspace stays on the coexistence v34 package: an
        # unmigrated, legacy-only workspace is untouched and continues
        # resolving against v5's legacy subtotal rule, which the migrated
        # v35 successor no longer admits at all.
        adoption = original_adoption
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return _renumber(acts)


def _run(
    acts: list[dict[str, object]], run_id: str, *, migrated: bool = False
) -> tuple[Any, dict[str, Any], dict[str, Any]]:
    """``migrated=True`` resolves against the real migrated v35
    package-adoption surface; otherwise the real coexistence v34 surface
    every other case's unmigrated workspace still adopts."""
    surface = _surface_v35() if migrated else _surface_v34()
    with TemporaryDirectory() as tmp:
        result = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope=SCOPE,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        if result.refusal is not None:
            return result, {}, {}
        report = json.loads(cast(Path, result.output_path).read_text("utf-8"))
        presentation = json.loads(cast(Path, result.presentation_path).read_text("utf-8"))
        return result, report, presentation


def _publications_by_prefix(result: Any, prefix: str) -> list[dict[str, Any]]:
    return [
        pub.finding
        for pub in (result.publications or ())
        if str(pub.finding.get("symbol", "")).startswith(prefix)
    ]


def _symbol_value(result: Any, symbol: str) -> Any:
    for pub in result.publications or ():
        if pub.finding.get("symbol") == symbol:
            return pub.finding["value"]
    return None


def _symbol_finding_id(result: Any, symbol: str) -> str | None:
    for pub in result.publications or ():
        if pub.finding.get("symbol") == symbol:
            return cast(str, pub.finding["id"])
    return None


class CaseAReproductionCaughtThenResolved(unittest.TestCase):
    """(a) legacy 42 + a new same-amount pairing: no silent double-subtraction."""

    def test_collision_blocks_the_new_pairing_with_a_traceable_disposition(self) -> None:
        acts = _acts_with_legacy(amount=42.0, with_pairing=True)
        result, report, _presentation = _run(acts, "demo.run.legacy-coexistence.case-a.blocked")
        self.assertIsNone(result.refusal, result.refusal)

        pairings = _publications_by_prefix(result, ASSOCIATION_SYMBOL)
        self.assertEqual(pairings, [], pairings)
        current_year = _publications_by_prefix(result, "tax.us.2025.interest.current-year-adjustment.pairing-scoped|")
        self.assertEqual(current_year, [], current_year)

        blocked_rows = [
            row
            for row in report.get("dispositions", [])
            if row.get("disposition") == "blocked"
            and row.get("code") == ASSOCIATION_MIGRATION_ADOPTION_REQUIRED
        ]
        self.assertEqual(len(blocked_rows), 1, report.get("dispositions"))
        self.assertIn(
            f"{LEGACY_TYPE}|tax-year=2025,adjustment-instance=demo.sbia.legacy.instance.0",
            blocked_rows[0]["missing"],
        )

        subtotal = _symbol_value(result, CURRENT_YEAR_SUBTOTAL_SYMBOL)
        self.assertEqual(subtotal, "0")
        taxable = _symbol_value(result, "tax.us.2025.interest.taxable-total")
        self.assertIsNotNone(taxable)
        self.assertEqual(Decimal(str(taxable)), Decimal("458"))

    def test_same_identity_correction_resolves_and_pairing_then_publishes(self) -> None:
        """Resolution: a second assertion at the SAME legacy fact_id (its own
        declared ``supersession.policy: "free"``), not a new displacement
        edge. The next run sees the corrected (zero) legacy amount, the
        collision signal clears, and the pairing publishes normally.
        """
        acts = _acts_with_legacy(amount=42.0, with_pairing=True)
        superseding = _act(
            len(acts) - 1,
            "assertion",
            {
                "finding": _attested(
                    "demo.legacy.finding.demo.sbia.legacy.instance.0.superseded",
                    f"{LEGACY_TYPE}|tax-year=2025,adjustment-instance=demo.sbia.legacy.instance.0",
                    0,
                )
            },
        )
        adoption = acts.pop()
        acts.append(superseding)
        acts.append(adoption)
        acts = _renumber(acts)

        result, report, _presentation = _run(acts, "demo.run.legacy-coexistence.case-a.resolved")
        self.assertIsNone(result.refusal, result.refusal)

        pairings = _publications_by_prefix(result, ASSOCIATION_SYMBOL)
        self.assertEqual(len(pairings), 1, pairings)
        current_year = _publications_by_prefix(result, "tax.us.2025.interest.current-year-adjustment.pairing-scoped|")
        self.assertEqual(len(current_year), 1, current_year)
        self.assertEqual(current_year[0]["value"], "42.0")

        blocked_rows = [
            row
            for row in report.get("dispositions", [])
            if row.get("disposition") == "blocked"
            and row.get("code") == ASSOCIATION_MIGRATION_ADOPTION_REQUIRED
        ]
        self.assertEqual(blocked_rows, [], blocked_rows)

        legacy_subtotal = _symbol_value(result, LEGACY_SUBTOTAL_SYMBOL)
        self.assertEqual(Decimal(str(legacy_subtotal)), Decimal("0"))
        subtotal = _symbol_value(result, CURRENT_YEAR_SUBTOTAL_SYMBOL)
        self.assertEqual(subtotal, "42.0")
        taxable = _symbol_value(result, "tax.us.2025.interest.taxable-total")
        self.assertEqual(Decimal(str(taxable)), Decimal("458"))


class CaseBLegacyOnlyUnaffected(unittest.TestCase):
    """(b) legacy-only workspace, no pairing ever created: fully unaffected."""

    def test_legacy_only_workspace_total_matches_todays_result(self) -> None:
        acts = _acts_with_legacy(amount=42.0, with_pairing=False)
        result, report, _presentation = _run(acts, "demo.run.legacy-coexistence.case-b")
        self.assertIsNone(result.refusal, result.refusal)

        pairings = _publications_by_prefix(result, ASSOCIATION_SYMBOL)
        self.assertEqual(pairings, [], pairings)
        blocked_rows = [row for row in report.get("dispositions", []) if row.get("disposition") == "blocked"]
        self.assertEqual(
            [row for row in blocked_rows if row.get("code") == ASSOCIATION_MIGRATION_ADOPTION_REQUIRED], []
        )

        legacy_subtotal = _symbol_value(result, LEGACY_SUBTOTAL_SYMBOL)
        self.assertEqual(Decimal(str(legacy_subtotal)), Decimal("42"))
        taxable = _symbol_value(result, "tax.us.2025.interest.taxable-total")
        self.assertEqual(Decimal(str(taxable)), Decimal("458"))


class CaseCTwoDifferentObligationsNoFalseCollision(unittest.TestCase):
    """(c) legacy 15 + a different-amount pairing (42): both correctly sum."""

    def test_different_amounts_never_collide(self) -> None:
        acts = _acts_with_legacy(amount=15.0, with_pairing=True)
        result, report, _presentation = _run(acts, "demo.run.legacy-coexistence.case-c")
        self.assertIsNone(result.refusal, result.refusal)

        blocked_rows = [
            row
            for row in report.get("dispositions", [])
            if row.get("disposition") == "blocked"
            and row.get("code") == ASSOCIATION_MIGRATION_ADOPTION_REQUIRED
        ]
        self.assertEqual(blocked_rows, [], blocked_rows)

        pairings = _publications_by_prefix(result, ASSOCIATION_SYMBOL)
        self.assertEqual(len(pairings), 1, pairings)
        legacy_subtotal = _symbol_value(result, LEGACY_SUBTOTAL_SYMBOL)
        self.assertEqual(Decimal(str(legacy_subtotal)), Decimal("15"))
        subtotal = _symbol_value(result, CURRENT_YEAR_SUBTOTAL_SYMBOL)
        self.assertEqual(subtotal, "42.0")
        taxable = _symbol_value(result, "tax.us.2025.interest.taxable-total")
        self.assertEqual(Decimal(str(taxable)), Decimal("443"))


class CaseDCompleteMigrationSequenceExecutesEndToEnd(unittest.TestCase):
    """(d) The actual, complete
    migration sequence -- successor bundle-adoption, then migration-
    adoption, then the real, migrated v35 package-adoption -- executes without error
    and (absent a blocking domain policy) produces the genuinely migrated,
    correctly computed result.

    ``test_migration_adoption_applies_without_error_and_retires_the_legacy_
    type`` below folds acts through a bare ``SchemaRegistry()`` with no
    domain maps installed (no ``resolved-required`` migration-resolution
    policy in effect), documenting migration-artifact structure and the
    v1 artifact's own unconditional-adoption behavior when no policy
    applies.
    ``CaseFResolutionGuardBlocksSameObligationCollisionMigration`` and this
    class's second test both prove that, under the real, domain-installed
    ``resolved-required`` policy, this same same-amount scenario
    refuses outright rather than
    completing via withdrawal -- a real, current correspondence is not
    sufficient authority to retire a nonzero legacy claim."""

    def _acts(self) -> list[dict[str, object]]:
        return _acts_with_legacy(amount=42.0, with_pairing=True, migrate=True)

    def test_migration_adoption_applies_without_error_and_retires_the_legacy_type(self) -> None:
        """Query the real post-migration fact state directly (not merely the
        absence of an exception): the legacy type is retired, the successor
        type is current, and a presented successor claim was produced from
        the then-current legacy finding. A bare registry installs no domain
        migration-resolution policy, so this documents the v1 artifact's
        own structure unaffected by the opt-in policy."""
        acts = self._acts()
        state = project(tuple(dict(act) for act in acts), SchemaRegistry())
        self.assertNotIn(LEGACY_TYPE, state.fact_state.fact_types)
        self.assertIn(LEGACY_TYPE, state.fact_state.retired_fact_type_ids)
        self.assertIn(SUCCESSOR_TYPE, state.fact_state.fact_types)
        self.assertTrue(
            any(m["id"] == MIGRATION_ID for m in state.fact_state.adopted_migrations),
            state.fact_state.adopted_migrations,
        )

        claims = [
            claim
            for claim in state.presented_successor_claims
            if claim["migration_id"] == MIGRATION_ID
            and claim["predecessor_fact_id"].startswith(LEGACY_TYPE + "|")
        ]
        self.assertEqual(len(claims), 1, claims)
        self.assertEqual(claims[0]["proposed_value"], 42.0)
        self.assertEqual(claims[0]["successor_fact_type_id"], SUCCESSOR_TYPE)

    def test_migration_with_the_real_domain_policy_now_refuses_this_scenario(self) -> None:
        """A real, current correspondence is not
        evidence the named finding actually took over the claim's role,
        since the predecessor fact type has no obligation identity to
        check it against. Under the real, domain-installed
        ``resolved-required`` policy this fixture refuses, identically
        to ``CaseFResolutionGuardBlocksSameObligationCollisionMigration``
        (this is the same underlying scenario). The bare-registry test
        above still proves the mechanical bundle-adoption /
        migration-adoption / package-adoption sequence itself executes
        without error when no domain policy blocks it; proving that same
        sequence completes *with* the policy active, for a nonzero legacy
        claim, is not currently possible without the owner decision named
        in ADR-0072 and ``docs/phase-state.md``."""
        acts = _acts_with_legacy(
            amount=42.0,
            with_pairing=True,
            migrate=True,
            resolve_legacy_before_migration=True,
            withdrawal_corresponds_to_fact_id=_pairing_acquisition_fact_id(),
        )
        with self.assertRaises(FindingModelError) as ctx:
            project(tuple(dict(act) for act in acts), _registry_with_migration_resolution_policy())
        self.assertIn(MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM, str(ctx.exception))

        with self.assertRaises(FindingModelError):
            _run(acts, "demo.run.legacy-coexistence.case-d.still-refuses", migrated=True)


class CaseFResolutionGuardBlocksSameObligationCollisionMigration(unittest.TestCase):
    """Same-
    obligation-shaped collision, amount 42 == 42: the domain-installed
    ``resolved-required`` migration-resolution policy (``packages.tax.
    loader.domain_migration_resolution_policies``, enforced generically by
    ``packages.kernel.findings.apply_migration_adoption``) refuses
    adoption outright while the legacy 42 remains live and unresolved --
    Case D's bare-registry success above only holds with no domain policy
    installed.

    A real, current correspondence is not evidence the named finding
    actually took over this claim's role -- the predecessor fact type
    carries no obligation identity to check the correspondence against,
    so even Case F's own *genuinely correct* correspondence cannot be
    kernel-verified as correct, only as real and current, which is
    insufficient (see Case G's
    real-but-wrong regression below, built from this class's own target).
    Withdrawal -- named or bare -- never resolves a nonzero
    legacy claim at all, and no `corresponds_to_fact_id` is
    consulted; only a genuine zero-correction (Case H) or an owner-decided
    mechanism not yet built (ADR-0072's named residual) can. Every test in
    this class proves refusal, uniformly via
    `MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM` regardless of whether a
    correspondence was named."""

    def test_migration_refuses_while_the_legacy_claim_is_unresolved(self) -> None:
        acts = _acts_with_legacy(amount=42.0, with_pairing=True, migrate=True)
        with self.assertRaises(FindingModelError) as ctx:
            project(tuple(dict(act) for act in acts), _registry_with_migration_resolution_policy())
        self.assertIn(MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM, str(ctx.exception))
        self.assertIn(LEGACY_TYPE, str(ctx.exception))

    def test_migration_refuses_through_the_live_path(self) -> None:
        """Same refusal, reproduced through the real production coordinator
        (``live_coordinate_run``), not only a direct ``project()`` call."""
        acts = _acts_with_legacy(amount=42.0, with_pairing=True, migrate=True)
        with self.assertRaises(FindingModelError) as ctx:
            _run(acts, "demo.run.legacy-coexistence.case-f.blocked", migrated=True)
        self.assertIn(MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM, str(ctx.exception))

    def test_bare_withdrawal_naming_no_correspondence_still_refuses(self) -> None:
        """Withdrawal alone -- even of the genuine same-obligation
        collision -- never resolves a nonzero claim. Its own true value
        (42) is nonzero, so `_refuse_unresolved_nonzero_withdrawals`
        refuses regardless of any `corresponds_to_fact_id`; no
        correspondence is even consulted, exactly like Case G's
        genuinely-distinct obligation."""
        acts = _acts_with_legacy(
            amount=42.0,
            with_pairing=True,
            migrate=True,
            resolve_legacy_before_migration=True,
        )
        with self.assertRaises(FindingModelError) as ctx:
            project(tuple(dict(act) for act in acts), _registry_with_migration_resolution_policy())
        self.assertIn(MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM, str(ctx.exception))

    def test_genuine_correspondence_no_longer_resolves_migration(self) -> None:
        """Even Case F's own genuinely
        correct correspondence -- the real, current pairing-path finding
        that actually did take over this claim's role -- does not
        resolve migration:
        `corresponds_to_fact_id` is never consulted for a nonzero claim at
        all. Migration refuses uniformly, through both ``project()`` and
        the live path, regardless of whether the named correspondence
        happens to be correct."""
        acts = _acts_with_legacy(
            amount=42.0,
            with_pairing=True,
            migrate=True,
            resolve_legacy_before_migration=True,
            withdrawal_corresponds_to_fact_id=_pairing_acquisition_fact_id(),
        )
        with self.assertRaises(FindingModelError) as ctx:
            project(tuple(dict(act) for act in acts), _registry_with_migration_resolution_policy())
        self.assertIn(MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM, str(ctx.exception))

        with self.assertRaises(FindingModelError) as live_ctx:
            _run(acts, "demo.run.legacy-coexistence.case-f.still-refuses", migrated=True)
        self.assertIn(MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM, str(live_ctx.exception))


class CaseGDistinctLegacyObligationNoLongerSilentlyDiscarded(unittest.TestCase):
    """Gross interest 500,
    an unrelated *live* legacy adjustment of 15 (a distinct obligation from
    any paired one, no collision), and a paired/attested adjustment of 42
    (a different obligation, genuinely associated and supported).

    Before migration, Case C above already proves the correct coexistence
    result is 443 (500 - 42 - 15). Migration must not silently retire the
    legacy 15 with no refusal and publish
    458; a *bare* member-transition
    removal of the 15 -- naming no replacement at all -- must not be
    accepted as an honest resolution, since withdrawal alone gives no
    evidence that anything genuinely took over the 15's computational
    role.

    There is no real correspondence for the 15 to name, and it would not
    matter if there were: it is a
    distinct, unrelated obligation from the paired 42 by this fixture's
    own construction, and `corresponds_to_fact_id` is not consulted
    for a nonzero claim at all. This class proves 458 is unreachable from
    this fixture's setup by any withdrawal shape -- bare, naming a
    fabricated correspondence, or naming Case F's own real, current
    target -- because the claim's own true value (15) is nonzero. Case F
    above proves the same holds even for a *genuine* same-obligation
    collision: withdrawal never resolves a nonzero claim, named or not.
    Case H proves the narrower same-identity zero-correction path remains
    available when the amount genuinely became zero -- not applicable
    here, since 15 is genuinely nonzero and true."""

    def _acts(
        self,
        *,
        resolve_legacy_before_migration: bool = False,
        withdrawal_corresponds_to_fact_id: str | None = None,
    ) -> list[dict[str, object]]:
        return _acts_with_legacy(
            amount=15.0,
            with_pairing=True,
            migrate=True,
            resolve_legacy_before_migration=resolve_legacy_before_migration,
            withdrawal_corresponds_to_fact_id=withdrawal_corresponds_to_fact_id,
        )

    def test_migration_refuses_instead_of_silently_producing_458(self) -> None:
        acts = self._acts()
        with self.assertRaises(FindingModelError) as ctx:
            project(tuple(dict(act) for act in acts), _registry_with_migration_resolution_policy())
        self.assertIn(MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM, str(ctx.exception))
        self.assertIn(LEGACY_TYPE, str(ctx.exception))

    def test_migration_refuses_through_the_live_path_too(self) -> None:
        acts = self._acts()
        with self.assertRaises(FindingModelError):
            _run(acts, "demo.run.legacy-coexistence.case-g.blocked", migrated=True)

    def test_bare_withdrawal_naming_no_correspondence_still_refuses(self) -> None:
        """Withdrawing the 15 with no ``corresponds_to_fact_id`` at all
        does not resolve the claim: `_present_successor_claims` excludes
        the withdrawn fact_id (it is genuinely no longer live), but
        `_refuse_unresolved_nonzero_withdrawals` separately refuses
        adoption because the claim's own true value (15) is still
        nonzero -- no correspondence is required, checked, or missed;
        it is simply irrelevant. 458 is never reached merely because the
        legacy member was removed."""
        acts = self._acts(resolve_legacy_before_migration=True)
        with self.assertRaises(FindingModelError) as ctx:
            project(tuple(dict(act) for act in acts), _registry_with_migration_resolution_policy())
        self.assertIn(MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM, str(ctx.exception))

        with self.assertRaises(FindingModelError) as live_ctx:
            _run(acts, "demo.run.legacy-coexistence.case-g.bare-withdrawal", migrated=True)
        self.assertIn(MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM, str(live_ctx.exception))

    def test_withdrawal_naming_a_nonexistent_correspondence_still_refuses(self) -> None:
        """A ``corresponds_to_fact_id`` that does not resolve to any
        current finding is no longer specially detected as dishonest --
        it is never consulted at all. This refuses identically to the
        bare case above, for the same reason (the claim's own value, 15,
        is nonzero), proving a fabricated pointer changes nothing."""
        acts = self._acts(
            resolve_legacy_before_migration=True,
            withdrawal_corresponds_to_fact_id=(
                "tax.us.obligation-acquisition-circumstance|"
                "payer=demo.payer.no-such-bank,obligation=demo.no-such-obligation,"
                "acquisition-year=2025"
            ),
        )
        with self.assertRaises(FindingModelError) as ctx:
            project(tuple(dict(act) for act in acts), _registry_with_migration_resolution_policy())
        self.assertIn(MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM, str(ctx.exception))

        with self.assertRaises(FindingModelError) as live_ctx:
            _run(acts, "demo.run.legacy-coexistence.case-g.false-correspondence", migrated=True)
        self.assertIn(MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM, str(live_ctx.exception))

    def test_real_but_wrong_correspondence_still_never_reaches_458(self) -> None:
        """Reproduces this case (the legacy 15, genuinely unrelated
        to the paired 42) while naming Case F's own real, current pairing
        acquisition fact as the withdrawal's ``corresponds_to_fact_id`` --
        a correspondence that is entirely real and current, just wrong for
        *this* legacy claim. This correspondence is never even inspected:
        `_refuse_unresolved_
        nonzero_withdrawals` refuses solely because the claim's own value
        (15) is nonzero. 458 must never be reachable, and it is not."""
        acts = self._acts(
            resolve_legacy_before_migration=True,
            withdrawal_corresponds_to_fact_id=_pairing_acquisition_fact_id(),
        )
        with self.assertRaises(FindingModelError) as ctx:
            project(tuple(dict(act) for act in acts), _registry_with_migration_resolution_policy())
        self.assertIn(MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM, str(ctx.exception))

        with self.assertRaises(FindingModelError) as live_ctx:
            _run(acts, "demo.run.legacy-coexistence.case-g.real-but-wrong", migrated=True)
        self.assertIn(MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM, str(live_ctx.exception))


class CaseHZeroCorrectionRemainsValidOnlyWhenGenuinelyZero(unittest.TestCase):
    """The same-identity zero correction (``_resolve_legacy_act``)
    remains a valid,
    narrower resolution mechanism for a claim that genuinely became zero
    (e.g. a data-entry correction), never for a claim that is still true.
    This reproduces the same-obligation-collision shape (legacy 42) with
    the zero-correction mechanism explicitly opted into
    (``resolve_via_zero_correction=True``), distinguishing it from the
    withdrawal path Cases D/F/G use by default.

    A required regression is proven
    separately below: a bare, zero-*valued* withdrawal (as opposed to a
    zero-*correction*) migrates without naming any
    ``corresponds_to_fact_id`` -- a withdrawn predecessor is only ever
    gated on its own true value, never on a replacement relationship,
    which was never meaningful for a claim that carried no live
    computational role to transfer in the first place."""

    def test_zero_correction_still_resolves_and_publishes_the_correct_total(self) -> None:
        acts = _acts_with_legacy(
            amount=42.0,
            with_pairing=True,
            migrate=True,
            resolve_legacy_before_migration=True,
            resolve_via_zero_correction=True,
        )
        state = project(tuple(dict(act) for act in acts), _registry_with_migration_resolution_policy())
        legacy_fact_id = (
            f"{LEGACY_TYPE}|tax-year=2025,adjustment-instance=demo.sbia.legacy.instance.0"
        )
        # Unlike withdrawal, the zero correction is a second finding at the
        # same fact_id: a claim IS presented, carrying the corrected (zero)
        # value, and the fact_id is never in withdrawn_fact_ids.
        self.assertNotIn(legacy_fact_id, state.withdrawn_fact_ids)
        claims = [
            claim
            for claim in state.presented_successor_claims
            if claim["migration_id"] == MIGRATION_ID and claim["predecessor_fact_id"] == legacy_fact_id
        ]
        self.assertEqual(len(claims), 1, claims)
        self.assertEqual(Decimal(str(claims[0]["proposed_value"])), Decimal("0"))

        result, _report, _presentation = _run(
            acts, "demo.run.legacy-coexistence.case-h.resolved", migrated=True
        )
        self.assertIsNone(result.refusal, result.refusal)
        taxable = _symbol_value(result, "tax.us.2025.interest.taxable-total")
        self.assertEqual(Decimal(str(taxable)), Decimal("458"))

    def test_bare_zero_valued_withdrawal_migrates_without_naming_a_replacement(self) -> None:
        """A legacy claim whose own true value is genuinely zero
        migrates cleanly on a *bare* withdrawal -- no
        ``corresponds_to_fact_id`` at all: no correspondence check
        demands a replacement relationship for a computational role that
        never existed (the claim was already zero; nothing needed to
        transfer). Gross interest is 500 here (no pairing), so a
        zero-valued, migrated legacy claim leaves the total unchanged."""
        acts = _acts_with_legacy(
            amount=0.0,
            with_pairing=False,
            migrate=True,
            resolve_legacy_before_migration=True,
        )
        legacy_fact_id = (
            f"{LEGACY_TYPE}|tax-year=2025,adjustment-instance=demo.sbia.legacy.instance.0"
        )
        state = project(tuple(dict(act) for act in acts), _registry_with_migration_resolution_policy())
        self.assertIn(legacy_fact_id, state.withdrawn_fact_ids)
        self.assertNotIn(LEGACY_TYPE, state.fact_state.fact_types)
        self.assertIn(LEGACY_TYPE, state.fact_state.retired_fact_type_ids)

        result, _report, _presentation = _run(
            acts, "demo.run.legacy-coexistence.case-h.bare-zero-withdrawal", migrated=True
        )
        self.assertIsNone(result.refusal, result.refusal)
        taxable = _symbol_value(result, "tax.us.2025.interest.taxable-total")
        self.assertEqual(Decimal(str(taxable)), Decimal("500"))


class RealActLogRoundTripForMemberTransitionV3(unittest.TestCase):
    """A v3-shaped member-transition
    act (carrying ``corresponds_to_fact_id``) must actually enter the
    authoritative act log through ``ActLog.append``/``.read()`` -- every
    test above this class builds acts and feeds them straight to
    ``project()``/``live_coordinate_run(authoritative_acts=...)``, which
    never exercises ``packages/kernel/act_log.py``'s payload-schema
    selector. That selector (a v3-shaped
    ``remove``/``reclassify`` member, discriminated by the presence of
    ``corresponds_to_fact_id``, selects ``act-member-transition.v3``
    instead of falling through to the always-v1 default) needs its own
    real-record-boundary proof, not an inference from the fixtures above
    passing."""

    def _log(self) -> tuple[ActLog, Path]:
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        workspace = Path(tmp.name) / "workspace"
        return ActLog(workspace, tax_registry()), workspace

    @staticmethod
    def _reindexed(acts: list[dict[str, object]]) -> list[dict[str, object]]:
        """``_withdraw_legacy_accrued_interest`` inserts its member-
        transition act into the fixture list by position, without
        renumbering every later act's own ``committed_against`` -- fine for
        ``project()``, which only reads acts in list order, but
        ``ActLog.append`` strictly enforces ``committed_against`` equal to
        the log's current revision at append time. Renumber sequentially so
        this real-log test proves the payload-schema selector, not an
        indexing artifact of the fixture builder."""
        out = []
        for index, act in enumerate(acts):
            act = dict(act)
            act["committed_against"] = index
            out.append(act)
        return out

    def test_v3_shaped_withdrawal_round_trips_through_a_real_act_log(self) -> None:
        acts = self._reindexed(_withdraw_legacy_accrued_interest(
            _acts_with_legacy(amount=15.0, with_pairing=True),
            instance="demo.sbia.legacy.instance.0",
            corresponds_to_fact_id=_pairing_acquisition_fact_id(),
        ))
        log, _workspace = self._log()
        for index, act in enumerate(acts):
            revision = log.append(dict(act), expected_revision=index)
            self.assertEqual(revision, index + 1)
        reread = log.read().acts
        self.assertEqual(len(reread), len(acts))
        member_acts = [
            act for act in reread
            if act["kind"] == "member-transition"
            and isinstance(act["payload"].get("member"), dict)
            and act["payload"]["member"].get("action") == "remove"
        ]
        self.assertEqual(len(member_acts), 1, member_acts)
        self.assertEqual(
            member_acts[0]["payload"]["member"]["corresponds_to_fact_id"],
            _pairing_acquisition_fact_id(),
        )

    def test_bare_v1_shaped_withdrawal_still_round_trips(self) -> None:
        """Backward compatibility, proven, not merely preserved by
        construction: a removal with no ``corresponds_to_fact_id`` at all
        must still select and validate against ``act-member-transition.v1``
        through the real log."""
        acts = self._reindexed(_withdraw_legacy_accrued_interest(
            _acts_with_legacy(amount=15.0, with_pairing=True),
            instance="demo.sbia.legacy.instance.0",
        ))
        log, _workspace = self._log()
        for index, act in enumerate(acts):
            log.append(dict(act), expected_revision=index)
        reread = log.read().acts
        self.assertEqual(len(reread), len(acts))
        member_acts = [
            act for act in reread
            if act["kind"] == "member-transition"
            and isinstance(act["payload"].get("member"), dict)
            and act["payload"]["member"].get("action") == "remove"
        ]
        self.assertEqual(len(member_acts), 1, member_acts)
        self.assertNotIn("corresponds_to_fact_id", member_acts[0]["payload"]["member"])

    def test_malformed_empty_correspondence_fails_closed_on_append(self) -> None:
        """A ``corresponds_to_fact_id`` present but empty violates v3's own
        ``minLength: 1`` -- append must reject it, not silently coerce or
        fall back to v1 (v1 would reject the extra key outright anyway;
        the point is the failure is a clean schema rejection, not a crash
        or a silent no-op)."""
        acts = self._reindexed(_withdraw_legacy_accrued_interest(
            _acts_with_legacy(amount=15.0, with_pairing=True),
            instance="demo.sbia.legacy.instance.0",
            corresponds_to_fact_id="placeholder",
        ))
        member_index = next(
            i for i, act in enumerate(acts)
            if act["kind"] == "member-transition"
            and isinstance(cast(dict[str, Any], act["payload"]).get("member"), dict)
            and cast(dict[str, Any], act["payload"])["member"].get("action") == "remove"
        )
        acts[member_index] = dict(acts[member_index])
        payload = dict(cast(dict[str, Any], acts[member_index]["payload"]))
        member = dict(cast(dict[str, Any], payload["member"]))
        member["corresponds_to_fact_id"] = ""
        payload["member"] = member
        acts[member_index]["payload"] = payload

        log, _workspace = self._log()
        with self.assertRaises(SchemaValidationError):
            for index, act in enumerate(acts):
                log.append(dict(act), expected_revision=index)


if __name__ == "__main__":
    unittest.main()
