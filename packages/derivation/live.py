"""Live derivation entrypoint: runs consume facts, not inputs (ADR-0032 D3).

The production path admits only a closed ``run-request.v1`` (no value-bearing
members) and builds ``RunContext`` exclusively through the marshal-only
constructor from projected record state. The fixture adapter in
``runners/derive.py`` remains production-fenced: it is not importable as a
live path and cannot be reached through this module.
"""

from __future__ import annotations

import inspect
from typing import Any, Mapping, Sequence

from packages.derivation.loader import DerivationSchemas
from packages.derivation.marshal import marshal_run_context
from packages.derivation.runner import RunContext, RunResult, run
from packages.kernel.currency import CurrencyView
from packages.kernel.findings import FindingState

RUN_REQUEST_SCHEMA = "run-request.v1"


class LiveRunError(Exception):
    """A live run request or marshalling step is inadmissible."""


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
) -> RunResult:
    """Execute one live run from record state only.

    Signature deliberately omits ``inputs``, ``sources``, ``InputFinding``, and
    any raw-value channel. A caller cannot hand-assemble ghost findings into
    this entrypoint — the only path to evaluator input is
    :func:`marshal_run_context`.
    """
    validate_run_request(request, schemas)
    ctx = marshal_run_context(
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
    )
    return run(ctx, schemas)


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


# Re-export for type identity checks: RunContext is not run-request.v1.
__all__ = [
    "RUN_REQUEST_SCHEMA",
    "LiveRunError",
    "live_entrypoint_accepts_raw_inputs",
    "live_run",
    "validate_run_request",
    "RunContext",
]
