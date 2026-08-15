"""Live derivation entrypoint: runs consume facts, not inputs (ADR-0032 D3).

The production path admits only a closed ``run-request.v1`` (no value-bearing
members) and builds ``RunContext`` exclusively through the marshal-only
constructor from projected record state. The fixture adapter in
``runners/derive.py`` remains production-fenced: it is not importable as a
live path and cannot be reached through this module.
"""

from __future__ import annotations

import inspect
import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable, Mapping, Sequence

from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.marshal import marshal_live_run_context
from packages.derivation.presentation_projection import PresentationModelError, build_presentation_model
from packages.derivation.production_executor import execute_and_record_marshaled, execute_marshaled
from packages.derivation.production_resolver import PublicationSurface, Refusal, resolve_production_package
from packages.derivation.records import RecordStream
from packages.kernel.currency import CurrencyView
from packages.kernel.currency import compute_currency
from packages.kernel.findings import FindingState, project
from packages.tax.loader import (
    domain_companion_presence_pairs,
    install_domain_companion_equalities,
    install_domain_companion_presence,
    install_domain_declaration_signal_contradictions,
)
from packages.tax.ssa_benefits import validate_projected_source_boundary
from packages.derivation.live_workspace import LiveWorkspace, WorkspaceCapability, bootstrap_workspace

if TYPE_CHECKING:
    from packages.derivation.runner import RunResult

RUN_REQUEST_SCHEMA = "run-request.v1"


class LiveRunError(Exception):
    """A live run request or marshalling step is inadmissible."""


@dataclass(frozen=True)
class LiveCoordinatorOutcome:
    """A capability-gated live attempt, with no repository-facing payload."""

    refusal: Refusal | None
    output_path: Path | None
    run_id: str | None
    # Additive: the confined presentation-model.v1 artifact path (Presentation
    # L2 Integration Grounding, Track 1). None on refusal, same as output_path.
    presentation_path: Path | None = None


def _iter_collect_categorical_names(expr: Any) -> Iterable[str]:
    """Yield ``name`` values from every ``collect_categorical_all_equal`` node.

    Track 6b repair (f1098e-student-loan-interest-agi): a rule reading a
    per-member categorical witness via this op needs its fact type
    registered as a collect source name the same way a `source-family.v1`
    member predicate is, or ``marshal.py`` would never populate
    ``env.sources`` for it. Unlike a family's member predicate, this is a
    per-rule declaration inside `when`/`value`, so it is discovered by
    walking the rule content directly rather than from a family citizen.
    """
    if isinstance(expr, dict):
        if expr.get("op") == "collect_categorical_all_equal" and isinstance(expr.get("name"), str):
            yield expr["name"]
        for value in expr.values():
            yield from _iter_collect_categorical_names(value)
    elif isinstance(expr, list):
        for item in expr:
            yield from _iter_collect_categorical_names(item)


def _resolved_run_material(graph: Any) -> tuple[
    list[dict[str, Any]], dict[str, dict[str, Any]], list[dict[str, Any]],
    list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[str],
]:
    """Derive runner material solely from the resolver's exclusive graph."""
    members = list(graph.resolved_members)
    # ADR-0036: an attachment citizen is interpreted directly from its
    # declarative requirement/itemizations/completeness structure (by
    # `_Run.attempt_attachment`, not `evaluate()`) but shares the same
    # saturation loop and ledger as every rule-artifact schema, so it
    # belongs in the same `rules` material the runner saturates over.
    rules = [
        member for member in members
        if member.get("schema") in {"rule-artifact.v1", "rule-artifact.v2", "rule-artifact.v3", "rule-artifact.v4", "rule-artifact.v5", "rule-artifact.v6", "attachment-rule.v1", "attachment-rule.v2", "attachment-rule.v3", "attachment-rule.v4", "attachment-rule.v5", "attachment-rule.v6", "attachment-rule.v8"}
    ]
    parameters = {member["id"]: member for member in members if member.get("schema") == "parameter-declaration.v1"}
    families = [member for member in members if member.get("schema") in {"source-family.v1", "source-family.v2"}]
    mappings = [member for member in members if member.get("schema") == "source-closure-mapping.v2"]
    fact_types = [fact for member in members if member.get("schema") in {"bundle.v1", "bundle.v2"} for fact in member.get("fact_types", [])]
    collect_names = [family["member_predicate"]["fact_type"] for family in families]
    # Companion authorities for collected members must be marshaled as sources
    # so derivation pins can form ADR-0010 displacement edges (box-13 / box-9).
    # Fail closed: a loader or pair-map failure must not silently drop companions
    # and leave dependent derivations unpinned (box-9 / box-13 displacement).
    from packages.tax.loader import domain_companion_presence_pairs
    pairs = domain_companion_presence_pairs()
    if not isinstance(pairs, dict):
        raise LiveRunError(
            f"domain companion-presence pairs must be a mapping; got {type(pairs)!r}"
        )
    extra: list[str] = []
    for sub, comp in pairs.items():
        if sub not in collect_names:
            continue
        companions = [comp] if isinstance(comp, str) else list(comp or ())
        for companion in companions:
            if (
                isinstance(companion, str)
                and companion
                and companion not in collect_names
                and companion not in extra
            ):
                extra.append(companion)
    collect_names = list(collect_names) + extra
    # Track 6b repair: any rule reading a per-member categorical witness via
    # collect_categorical_all_equal needs its fact type registered as a
    # collect source name too, or marshal.py would never populate
    # env.sources for it (see _iter_collect_categorical_names above).
    for rule in rules:
        for name in _iter_collect_categorical_names(rule.get("when")):
            if name not in collect_names:
                collect_names.append(name)
        for name in _iter_collect_categorical_names(rule.get("value")):
            if name not in collect_names:
                collect_names.append(name)
    return rules, parameters, families, mappings, fact_types, list(graph.package["input_bindings"]), collect_names


def live_coordinate_run(
    capability: WorkspaceCapability,
    *,
    repo_root: Path,
    authoritative_acts: Sequence[Mapping[str, Any]],
    workspace_revision: int,
    run_scope: Mapping[str, str],
    scope_user: str,
    request: Mapping[str, Any],
    run_id: str,
    governance_pins: Sequence[Mapping[str, Any]],
    surface: PublicationSurface,
    output_name: str,
    schemas: DerivationSchemas | None = None,
) -> LiveCoordinatorOutcome:
    """Run the one production path from capability, record, and resolved graph.

    There is intentionally no caller package, catalog, path, raw context,
    fixture adapter, or direct ``runner.run`` parameter. A resolver refusal
    returns before the record stream is opened, so it cannot manufacture a
    run account. All durable output remains below ``LiveWorkspace``.
    """
    schemas = schemas or DerivationSchemas()
    workspace: LiveWorkspace = bootstrap_workspace(capability, repo_root=repo_root)
    guards = workspace.install_envelope_guards()
    # A live coordinator cannot silently choose a --no-verify/raw-transport
    # route: both installed gates are entered before any run record or output.
    workspace.guarded_commit(guards, ())
    workspace.guarded_push(guards, ())
    resolved = resolve_production_package(
        authoritative_acts, run_scope=run_scope, scope_user=scope_user,
        workspace_revision=workspace_revision, surface=surface, schemas=schemas,
    )
    if isinstance(resolved, Refusal):
        return LiveCoordinatorOutcome(refusal=resolved, output_path=None, run_id=None)
    validate_run_request(request, schemas)
    # Resolve the declared destinations before execution or opening the record
    # stream.  An invalid/escaping request is a residency refusal, not a run
    # that can create a started/completed account.
    output_path = workspace.reserve_live_output_path(Path("outputs") / output_name)
    presentation_path = workspace.reserve_live_output_path(
        Path("outputs") / f"{Path(output_name).stem}.presentation.json"
    )
    # Domain companion-presence pairs (B12-C3 box-13; B8-C2 box-9) and
    # declaration/signal contradictions (including Path A no-f1099int vs box-8)
    # live on tax_registry(); production projection must install the same maps
    # so live-path admission matches the domain registry.
    install_domain_companion_presence(schemas.registry)
    install_domain_companion_equalities(schemas.registry)
    install_domain_declaration_signal_contradictions(schemas.registry)
    state = project(tuple(dict(act) for act in authoritative_acts), schemas.registry)
    validate_projected_source_boundary(state.findings.values(), state.withdrawn_fact_ids)
    currency = compute_currency(state)
    rules, parameters, families, mappings, fact_types, bindings, collect_names = _resolved_run_material(resolved)
    retired = state.fact_state.retired_fact_type_ids
    if retired:
        fact_types = [ft for ft in fact_types if ft.get("id") not in retired]
    context = marshal_live_run_context(
        run_id=run_id, state=state, currency=currency, rules=rules, parameters=parameters,
        canon=load_canon(schemas),
        adoption_pin={"role": "adoption", "id": resolved.package["id"], "version": resolved.package["version"]},
        governance_pins=[dict(pin) for pin in governance_pins],
        family_declarations=families, closure_mappings=mappings, fact_types=fact_types,
        input_bindings=bindings, collect_source_names=collect_names,
        companion_presence_pairs=domain_companion_presence_pairs(),
    )
    stream = RecordStream(workspace.live_output_path(Path("records")), schemas)
    result = execute_and_record_marshaled(
        context, schemas, stream, workspace_revision=workspace_revision,
        adopted_packages={resolved.package["id"]},
        start_record_id=f"record:{run_id}:started", completion_record_id=f"record:{run_id}:completed",
    )
    # Construct and validate the presentation model before writing any durable
    # output. A projector rejection (missing/ambiguous join, unknown
    # disposition, invalid numeric publication, untraceable lineage) must not
    # leave a completed-looking result file or a stranded empty presentation
    # artifact behind (Track 1 repair, Finding 1) — the derivation record
    # stream may still accurately retain the run it recorded; only these two
    # reserved output files are this repair's concern.
    try:
        model = build_presentation_model(
            run_id=result.run_id,
            resolved_members=resolved.resolved_members,
            state=state,
            publications=result.publications,
            dispositions=result.dispositions,
        )
    except PresentationModelError:
        output_path.unlink(missing_ok=True)
        presentation_path.unlink(missing_ok=True)
        raise

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps({
        "run_id": result.run_id, "stop_reason": result.stop_reason,
        "dispositions": result.dispositions,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    presentation_path.write_text(json.dumps(model, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return LiveCoordinatorOutcome(
        refusal=None, output_path=output_path, run_id=run_id, presentation_path=presentation_path
    )


def validate_run_request(request: Mapping[str, Any], schemas: DerivationSchemas) -> None:
    """Admit a closed run-request.v1. Value-bearing members are schema-rejected."""
    schemas.validate(RUN_REQUEST_SCHEMA, dict(request))


def live_run(
    request: Mapping[str, Any],
    *,
    run_id: str,
    state: FindingState,
    currency: CurrencyView,
    rules: Sequence[dict[str, Any]],
    parameters: Mapping[str, dict[str, Any]],
    canon: Mapping[str, dict[str, Any]],
    adoption_pin: Mapping[str, Any],
    governance_pins: Sequence[Mapping[str, Any]],
    schemas: DerivationSchemas,
    family_declarations: Sequence[dict[str, Any]] | None = None,
    closure_mappings: Sequence[dict[str, Any]] | None = None,
    fact_types: Sequence[dict[str, Any]] | None = None,
    input_bindings: Sequence[Mapping[str, Any]] | None = None,
    collect_source_names: Sequence[str] | None = None,
    companion_presence_pairs: Mapping[str, str] | None = None,
) -> RunResult:
    """Execute one live run from record state only.

    Signature deliberately omits ``inputs``, ``sources``, ``InputFinding``, and
    any raw-value channel. A caller cannot hand-assemble ghost findings into
    this entrypoint — the only path to evaluator input is
    :func:`marshal_run_context`.
    """
    validate_run_request(request, schemas)
    ctx = marshal_live_run_context(
        run_id=run_id,
        state=state,
        currency=currency,
        rules=list(rules),
        parameters=dict(parameters),
        canon=dict(canon),
        adoption_pin=dict(adoption_pin),
        governance_pins=[dict(p) for p in governance_pins],
        family_declarations=list(family_declarations or ()),
        closure_mappings=list(closure_mappings or ()),
        fact_types=list(fact_types or ()),
        input_bindings=[dict(b) for b in (input_bindings or ())],
        collect_source_names=list(collect_source_names or ()),
        companion_presence_pairs=dict(companion_presence_pairs or {}),
    )
    return execute_marshaled(ctx, schemas)


def live_entrypoint_accepts_raw_inputs() -> bool:
    """Structural probe: does the live signature admit a raw-input parameter?

    Used by the ADR-0032 reachability kill-test. Returns False when the live
    entrypoint has no parameter that could carry hand-assembled InputFinding
    / SourceFact / raw value payloads.
    """
    params = inspect.signature(live_run).parameters
    forbidden = {
        "inputs",
        "sources",
        "raw_inputs",
        "input_findings",
        "source_facts",
        "values",
        "scenario",
    }
    return bool(forbidden.intersection(params))


__all__ = [
    "RUN_REQUEST_SCHEMA",
    "LiveRunError",
    "LiveCoordinatorOutcome",
    "live_coordinate_run",
    "live_entrypoint_accepts_raw_inputs",
    "live_run",
    "validate_run_request",
]
