"""Hand a workspace's Social Security family chain over to the version its package declares.

Core v59 succeeds ``tax.us.2025.ssa1099.benefits`` to v2: the closure claim the filer
attests no longer says box-6 withholding is absent or zero, because v59 counts that
withholding on Form 1040 line 25b. A workspace recorded under core v58 or earlier has
its Social Security statements on a v1 horizon chain, and a chain is bound to one
family version, so moving to v59 needs the ADR-0079 family handover: the v1 chain is
retired, a v2 chain starts, and the statements recorded on v1 stand. Nothing is
attested by the move. The re-confirmation that every Form SSA-1099 is recorded is the
ordinary closure attestation on the successor horizon, which the filer makes afterwards.

This follows ``_stage_family_handover`` and ``f1099k_family_version_for_workspace`` in
``packages/tax/f1099k_statement_recording.py``. It is written beside them rather than
sharing them: both are Form 1099-K specific (family id, horizon naming, act ids), and
generalizing them would touch every 1099-K recording path for no behavior gain.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from packages.kernel.act_log import ActLog, ActLogError
from packages.kernel.findings import apply_act, project
from packages.tax.f1099k_statement_recording import _default_production_surface_for_adoption

FAMILY_ID = "tax.us.2025.ssa1099.benefits"
FAMILY_VERSION = "v1"
DEFAULT_FAMILY_SCOPE: dict[str, str] = {"tax-year": "2025", "subject": "demo.primary"}


class SsaHandoverRefused(ValueError):
    """The Social Security family cannot be handed over on this log."""


def _version_number(version: str) -> int:
    if version.startswith("v") and version[1:].isdigit():
        return int(version[1:])
    raise ValueError(f"unrecognized version format: {version!r}")


def ssa_family_version_from_package(package_or_path: Mapping[str, Any] | Path | str) -> str:
    """The Social Security family version an adopted package declares (v1 if it lists none)."""
    if isinstance(package_or_path, (str, Path)):
        package_data: Mapping[str, Any] = json.loads(Path(package_or_path).read_text("utf-8"))
    else:
        package_data = package_or_path
    for member in package_data.get("members", []):
        if isinstance(member, dict) and member.get("id") == FAMILY_ID and member.get("role") == "source-family":
            version = member.get("version")
            if isinstance(version, str):
                return version
    return FAMILY_VERSION


def ssa_family_version_for_acts(
    acts: Sequence[Mapping[str, Any]],
    *,
    actor: str,
    run_scope: Mapping[str, str] | None = None,
    workspace_revision: int | None = None,
    surface: Any | None = None,
    schemas: Any | None = None,
    content_dir: Path | None = None,
    tax_year: str = "2025",
) -> str:
    """Resolve the Social Security family version from the adopted package in an act sequence.

    Same authority as the runs (``select_current_adoption`` and ``resolve_production_package``).
    A workspace with no adoption in scope keeps v1; an adoption that cannot be resolved is
    refused, never read as v1.
    """
    from packages.derivation.loader import DerivationSchemas
    from packages.derivation.production_resolver import (
        Refusal,
        resolve_production_package,
        select_current_adoption,
    )

    schemas = schemas or DerivationSchemas()
    if workspace_revision is None:
        workspace_revision = len(acts)
    if run_scope is None:
        run_scope = {"jurisdiction": "us", "year": tax_year}
    selected = select_current_adoption(
        acts, run_scope=run_scope, scope_user=actor, workspace_revision=workspace_revision, schemas=schemas
    )
    if isinstance(selected, Refusal):
        if selected.reason == "ADOPTION_NONE_CURRENT":
            return FAMILY_VERSION
        raise SsaHandoverRefused(f"current adoption selection refused: {selected.reason} ({selected.detail})")
    if surface is None:
        surface = _default_production_surface_for_adoption(selected["payload"], content_dir)
    resolved = resolve_production_package(
        acts,
        run_scope=run_scope,
        scope_user=actor,
        workspace_revision=workspace_revision,
        surface=surface,
        schemas=schemas,
    )
    if isinstance(resolved, Refusal):
        raise SsaHandoverRefused(
            f"adopted package in scope could not be resolved: {resolved.reason} ({resolved.detail})"
        )
    return ssa_family_version_from_package(resolved.package)


def ssa_family_version_for_workspace(log: ActLog, **kwargs: Any) -> str:
    """``ssa_family_version_for_acts`` on a workspace log's current acts."""
    return ssa_family_version_for_acts(log.read().acts, **kwargs)


def _active_family_chain(state: Any, scope: Mapping[str, str]) -> tuple[str, str] | None:
    """(version, horizon id) of the current Social Security family chain for a scope."""
    scope_tuple = tuple(sorted(scope.items()))
    for (family_id, version, chain_scope), horizon_id in state.horizon_state.current_by_chain.items():
        if family_id == FAMILY_ID and chain_scope == scope_tuple:
            return version, horizon_id
    return None


def stage_ssa_family_handover(
    acts: Sequence[Mapping[str, Any]],
    registry: Any,
    *,
    actor: str,
    at: str,
    family_version: str,
    family_scope: Mapping[str, str] | None = None,
) -> tuple[dict[str, Any], Any]:
    """Build the ADR-0079 handover act for ``acts`` and fold it; return (act, state).

    Refused when the chain is already on ``family_version`` (nothing to hand over, which is also
    what a second handover meets), when ``family_version`` is older, or when there is no chain.
    """
    staged = [copy.deepcopy(dict(row)) for row in acts]
    state = project(tuple(copy.deepcopy(row) for row in staged), registry)
    scope = dict(family_scope or DEFAULT_FAMILY_SCOPE)
    active = _active_family_chain(state, scope)
    if active is None:
        raise SsaHandoverRefused("no active Social Security family chain found for scope")
    current_version, current_horizon = active
    if _version_number(current_version) == _version_number(family_version):
        raise SsaHandoverRefused(
            f"nothing to hand over: the Social Security chain is already on {current_version}"
        )
    if _version_number(current_version) > _version_number(family_version):
        raise SsaHandoverRefused(
            f"cannot handover to older family version: current chain is {current_version}, adopted package declares {family_version}"
        )
    count = len(state.horizon_state.horizons)
    successor = f"demo.ssa.handover.h{count}"
    while successor in state.horizon_state.horizons:
        count += 1
        successor = f"demo.ssa.handover.h{count}"
    act = {
        "schema": "act.v1",
        "act_id": f"ssa.handover.{len(staged)}",
        "kind": "family-handover",
        "actor": actor,
        "at": at,
        "committed_against": len(staged),
        "payload": {
            "predecessor": {
                "family": {"id": FAMILY_ID, "version": current_version},
                "scope": dict(scope),
                "horizon_id": current_horizon,
            },
            "successor": {
                "family": {"id": FAMILY_ID, "version": family_version},
                "scope": dict(scope),
                "horizon_id": successor,
            },
        },
    }
    return act, apply_act(state, act, registry)


def hand_over_ssa_family_durably(
    log: ActLog,
    registry: Any,
    *,
    submission_id: str,
    actor: str,
    at: str,
    expected_revision: int,
    family_scope: Mapping[str, str] | None = None,
    family_version: str | None = None,
    surface: Any | None = None,
    tax_year: str = "2025",
) -> dict[str, Any]:
    """Record the handover of the current Social Security chain to the adopted package's version.

    The statements recorded on the retired chain stand. No closure is attested here: the filer
    re-confirms on the returned horizon. Refused when the log revision moved.
    """
    if not all(isinstance(v, str) and v.strip() for v in (submission_id, actor, at)):
        raise SsaHandoverRefused("submission identity, actor, and timestamp are required non-empty strings")
    before = log.read()
    if before.incomplete_tail is not None:
        raise SsaHandoverRefused("ActLog has an incomplete tail")
    if before.revision != expected_revision:
        raise SsaHandoverRefused(
            f"reviewed ActLog revision changed before save: expected {expected_revision}, got {before.revision}"
        )
    if family_version is None:
        family_version = ssa_family_version_for_acts(
            before.acts,
            actor=actor,
            run_scope={"jurisdiction": "us", "year": tax_year},
            workspace_revision=expected_revision,
            surface=surface,
            tax_year=tax_year,
        )
    act, state = stage_ssa_family_handover(
        before.acts, registry, actor=actor, at=at, family_version=family_version, family_scope=family_scope
    )
    try:
        revision = log.append_batch([act], expected_revision=expected_revision)
    except ActLogError as exc:
        raise SsaHandoverRefused(f"handover save refused: {exc}") from exc
    return {
        "revision": revision,
        "horizon": act["payload"]["successor"]["horizon_id"],
        "state": state,
        "actor": actor,
        "at": at,
    }
