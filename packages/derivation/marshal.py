"""Marshal closure authority from projected record state.

The persistence boundary between the kernel projection and the runner:
given immutable projected state and its computed currency, extract the
closure findings and current horizons the runner's dispatch resolves
admission from (ADR-0014 decision 4). Nothing here decides authority —
a caller gets exactly what the record says, and the runner alone judges
it. Only *current* findings are marshalled, so a displaced closure
finding is indistinguishable from an absent one downstream.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from packages.derivation.source_authority import (
    ClosureFindingRecord,
    SourceAuthorityError,
)
from packages.kernel.currency import CurrencyView
from packages.kernel.findings import FindingState

if TYPE_CHECKING:
    from packages.derivation.runner import RunContext


_MARSHAL_SEAL = object()


@dataclass(frozen=True, init=False)
class MarshalledRunContext:
    """Opaque product of record-state marshalling for the live executor.

    The contained context intentionally has no public accessor.  Fixture code
    may continue to construct ``RunContext`` for scenario coverage, but a live
    execution must first pass through ``marshal_live_run_context``.
    """

    _context: RunContext
    _seal: object = field(repr=False, compare=False)

    def __init__(self, context: RunContext, seal: object) -> None:
        if seal is not _MARSHAL_SEAL:
            raise TypeError("MarshalledRunContext may only be minted by marshal_live_run_context")
        object.__setattr__(self, "_context", context)
        object.__setattr__(self, "_seal", seal)

    def _is_minted(self) -> bool:
        return self._seal is _MARSHAL_SEAL


def _rule_required_symbols(rule: dict[str, Any]) -> list[str]:
    """Every symbol a rule's own eligibility/completeness surface names.

    Ordinary rule-artifact schemas declare `requires` directly. An
    attachment-rule.v1 citizen (ADR-0036) has no such field - its analogous
    symbol surface is its requirement conditional's subtotals plus every
    completeness answer symbol, base and branch-triggered alike.
    """
    if rule.get("schema") == "attachment-rule.v1":
        symbols = list(rule["requirement"]["subtotals"])
        completeness = rule["completeness"]
        symbols.extend(a["symbol"] for a in completeness["required_answers"])
        for branch in completeness.get("branch_requirements", []):
            symbols.append(branch["when_answer"]["symbol"])
            symbols.extend(a["symbol"] for a in branch.get("adds_required", []))
        return symbols
    return list(rule.get("requires", []))


def _fact_keys(fact_id: str) -> dict[str, str]:
    """Parse the canonical fact id rendering: ``type|name=value,...``."""
    _, _, bound = fact_id.partition("|")
    keys: dict[str, str] = {}
    for pair in bound.split(","):
        name, _, value = pair.partition("=")
        keys[name] = value
    return keys


def marshal_closure_authority(
    state: FindingState,
    currency: CurrencyView,
    mappings: list[dict[str, Any]],
) -> tuple[list[ClosureFindingRecord], dict[str, str]]:
    """Extract closure findings and current horizons for the run context.

    For each adopted mapping: every *current* finding answering the
    mapped closure fact type becomes a record, with the horizon read
    from the identity key the mapping names. The current horizon per
    family comes from the projected horizon chains; a family spanning
    multiple scope chains in one workspace is a marshalling error, not
    a guess.
    """
    records: list[ClosureFindingRecord] = []
    for mapping in mappings:
        fact_type = mapping["closure_fact_type"]
        fact_type_id = fact_type["id"] if isinstance(fact_type, dict) else fact_type
        horizon_key = mapping["closure_horizon_key"]
        prefix = f"{fact_type_id}|"
        for finding_id in sorted(currency.current_finding_ids):
            finding = state.findings.get(finding_id)
            if finding is None or not finding["fact_id"].startswith(prefix):
                continue
            keys = _fact_keys(finding["fact_id"])
            horizon_id = keys.get(horizon_key)
            if horizon_id is None:
                raise SourceAuthorityError(
                    f"closure finding {finding_id} has no {horizon_key!r} "
                    f"identity key; mapping {mapping['id']} cannot read it"
                )
            records.append(
                ClosureFindingRecord(
                    finding_id=finding_id,
                    fact_type=fact_type_id,
                    horizon_id=horizon_id,
                    value=finding["value"],
                )
            )

    current_horizons: dict[str, str] = {}
    for (family_id, _version, _scope), horizon_id in sorted(
        state.horizon_state.current_by_chain.items()
    ):
        if family_id in current_horizons:
            raise SourceAuthorityError(
                f"family {family_id} has horizon chains in multiple scopes; "
                "one run marshals exactly one scope"
            )
        current_horizons[family_id] = horizon_id
    return records, current_horizons


def marshal_run_context(
    *,
    run_id: str,
    state: FindingState,
    currency: CurrencyView,
    rules: list[dict[str, Any]],
    parameters: dict[str, dict[str, Any]],
    canon: dict[str, dict[str, Any]],
    adoption_pin: dict[str, Any],
    governance_pins: list[dict[str, Any]],
    family_declarations: list[dict[str, Any]] | None = None,
    closure_mappings: list[dict[str, Any]] | None = None,
    fact_types: list[dict[str, Any]] | None = None,
    input_bindings: list[dict[str, Any]] | None = None,
    collect_source_names: list[str] | None = None,
) -> RunContext:
    """Build a RunContext from current record state only (ADR-0032 MUST).

    This is the sole production constructor path for evaluator input. It
    never accepts caller-supplied InputFinding / SourceFact values: every
    input and source is projected from *current* findings. The fixture
    adapter in ``runners/derive.py`` remains a separate, production-fenced
    path and is not used here.
    """
    # Local imports keep the kernel↔derivation cycle shallow at module load.
    from packages.derivation.runner import InputFinding, RunContext, SourceFact

    bindings = list(input_bindings or [])
    mappings = list(closure_mappings or [])
    families = list(family_declarations or [])
    ftypes = list(fact_types or [])
    collect_names = set(collect_source_names or [])

    current_findings = [
        state.findings[fid]
        for fid in sorted(currency.current_finding_ids)
        if fid in state.findings
    ]

    inputs: list[InputFinding] = []
    used_finding_ids: set[str] = set()
    for binding in bindings:
        symbol = binding["symbol"]
        fact_type_id = binding["fact_type"]["id"]
        mode = binding.get("mode", "required")
        prefix = f"{fact_type_id}|"
        matches = [f for f in current_findings if f["fact_id"].startswith(prefix)]
        if not matches:
            if mode == "required":
                # Absent current finding: leave unbound; runner records
                # DEPENDENCY_ABSENT rather than inventing a value.
                continue
            continue
        # One binding → one current finding for that fact type. If several
        # members exist (collectable families), they feed sources instead.
        if len(matches) == 1 or symbol not in collect_names:
            finding = matches[0]
            role = "choice" if finding.get("basis") == "elective" else "input"
            inputs.append(
                InputFinding(
                    symbol=symbol,
                    value=finding["value"],
                    finding_id=finding["id"],
                    role=role,
                )
            )
            used_finding_ids.add(finding["id"])

    sources: list[SourceFact] = []
    for name in sorted(collect_names):
        for finding in current_findings:
            # Collectable sources match by fact type id prefix or exact type.
            fact_id = finding["fact_id"]
            type_id = fact_id.split("|", 1)[0]
            if type_id == name or fact_id.startswith(f"{name}|"):
                sources.append(
                    SourceFact(
                        name=name,
                        value=str(finding["value"]),
                        finding_id=finding["id"],
                    )
                )
                used_finding_ids.add(finding["id"])

    # Also marshal unbound current findings whose fact type equals a rule
    # input symbol (legacy demo path: symbol == fact type id).
    bound_symbols = {i.symbol for i in inputs}
    for finding in current_findings:
        if finding["id"] in used_finding_ids:
            continue
        type_id = finding["fact_id"].split("|", 1)[0]
        if type_id in bound_symbols:
            continue
        # Only surface as input when some rule requires this type id as a
        # symbol — keeps marshalling from flooding the context with noise.
        # An attachment-rule.v1 citizen has no `requires` field; its own
        # analogous symbol surface is requirement.subtotals plus every
        # completeness answer symbol (base and branch-triggered) - the
        # legacy-path fallback must see those too, or a live Part III
        # answer assertion would never reach the run at all.
        required_by_rules = any(
            type_id in _rule_required_symbols(rule) for rule in rules
        )
        if not required_by_rules:
            continue
        role = "choice" if finding.get("basis") == "elective" else "input"
        inputs.append(
            InputFinding(
                symbol=type_id,
                value=finding["value"],
                finding_id=finding["id"],
                role=role,
            )
        )

    closure_records, current_horizons = marshal_closure_authority(
        state, currency, mappings
    )

    return RunContext(
        run_id=run_id,
        rules=list(rules),
        parameters=dict(parameters),
        canon=dict(canon),
        inputs=inputs,
        sources=sources,
        adoption_pin=dict(adoption_pin),
        governance_pins=[dict(p) for p in governance_pins],
        family_declarations=families,
        closure_mappings=mappings,
        closure_findings=list(closure_records),
        current_horizons=dict(current_horizons),
        fact_types=ftypes,
        input_bindings=bindings,
    )


def marshal_live_run_context(
    *,
    run_id: str,
    state: FindingState,
    currency: CurrencyView,
    rules: list[dict[str, Any]],
    parameters: dict[str, dict[str, Any]],
    canon: dict[str, dict[str, Any]],
    adoption_pin: dict[str, Any],
    governance_pins: list[dict[str, Any]],
    family_declarations: list[dict[str, Any]] | None = None,
    closure_mappings: list[dict[str, Any]] | None = None,
    fact_types: list[dict[str, Any]] | None = None,
    input_bindings: list[dict[str, Any]] | None = None,
    collect_source_names: list[str] | None = None,
) -> MarshalledRunContext:
    """Create the opaque marshalling result accepted by the production executor."""
    return MarshalledRunContext(
        marshal_run_context(
            run_id=run_id,
            state=state,
            currency=currency,
            rules=rules,
            parameters=parameters,
            canon=canon,
            adoption_pin=adoption_pin,
            governance_pins=governance_pins,
            family_declarations=family_declarations,
            closure_mappings=closure_mappings,
            fact_types=fact_types,
            input_bindings=input_bindings,
            collect_source_names=collect_source_names,
        ),
        _MARSHAL_SEAL,
    )
