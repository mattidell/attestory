"""Production-only evaluator fence for record-marshalled contexts (ADR-0032 F1)."""

from __future__ import annotations

from packages.derivation.loader import DerivationSchemas
from packages.derivation.marshal import MarshalledRunContext
from packages.derivation.records import RecordStream, closing_record, start_run
from packages.derivation.runner import RunResult, _execute


_LEDGER_EXCLUDED_PIN_ROLES = frozenset(
    {"computation", "applicability", "field-mapping", "cross-form-bridge"}
)


def _record_safe_result(result: RunResult) -> RunResult:
    """Normalize fixture-only inapplicable metadata for the v9 record ledger.

    The bounded fixture runner retains ``no_source_activity`` on the distinct
    nominee aggregate so its direct result can distinguish that outcome from
    a blocked or published aggregate.  The published derivation-record.v9
    schema represents that same outcome as an ordinary false guard and its
    ledger pin vocabulary excludes computation-role pins.  Normalize only at
    the production fence; the fixture-facing runner contract remains intact.
    """
    for row in result.dispositions:
        if row.get("disposition") != "inapplicable" or not row.pop(
            "no_source_activity", False
        ):
            continue
        row["guard_result"] = False
        row["pins"] = [
            pin
            for pin in row.get("pins", [])
            if pin.get("role") not in _LEDGER_EXCLUDED_PIN_ROLES
        ]
    return result


def execute_marshaled(context: MarshalledRunContext, schemas: DerivationSchemas) -> RunResult:
    """Evaluate only a context minted by the record-state marshaller.

    ``runner.run`` remains the explicitly fixture/test-facing entrypoint for
    pre-existing deterministic scenarios.  The live module imports neither it
    nor the fixture adapter, closing the accidental production route.
    """
    if type(context) is not MarshalledRunContext or not context._is_minted():
        raise TypeError("production execution requires a marshalled run context")
    return _record_safe_result(_execute(context._context, schemas))


def execute_and_record_marshaled(
    context: MarshalledRunContext,
    schemas: DerivationSchemas,
    stream: RecordStream,
    *,
    workspace_revision: int,
    adopted_packages: set[str],
    start_record_id: str,
    completion_record_id: str,
) -> RunResult:
    """Run the sealed live context with its mandatory paired record account.

    This is deliberately separate from the fixture-facing ``runner.run`` route.
    A resolver refusal is handled before this function is called, so it cannot
    create a start record.
    """
    if type(context) is not MarshalledRunContext or not context._is_minted():
        raise TypeError("production execution requires a marshalled run context")
    ctx = context._context
    start_run(
        stream,
        record_id=start_record_id,
        run_id=ctx.run_id,
        workspace_revision=workspace_revision,
        governance_pins=ctx.governance_pins,
        adoption_pin=ctx.adoption_pin,
        adopted_packages=adopted_packages,
        use_v2=True,
    )
    result = execute_marshaled(context, schemas)
    published = [
        {"symbol": pub.finding["symbol"], "finding_id": pub.finding["id"], "act_id": pub.act.get("act_id", pub.finding["id"])}
        for pub in result.publications
    ]
    stream.append(closing_record(
        record_id=completion_record_id,
        run_id=ctx.run_id,
        phase="completed",
        workspace_revision=workspace_revision,
        governance_pins=ctx.governance_pins,
        adoption_pin=ctx.adoption_pin,
        stop_reason=result.stop_reason,
        published=published,
        blocked=result.blocked,
        dispositions=result.dispositions,
        use_v2=True,
    ))
    return result
