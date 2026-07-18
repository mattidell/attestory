"""Production-only evaluator fence for record-marshalled contexts (ADR-0032 F1)."""

from __future__ import annotations

from packages.derivation.loader import DerivationSchemas
from packages.derivation.marshal import MarshalledRunContext
from packages.derivation.runner import RunResult, _execute


def execute_marshaled(context: MarshalledRunContext, schemas: DerivationSchemas) -> RunResult:
    """Evaluate only a context minted by the record-state marshaller.

    ``runner.run`` remains the explicitly fixture/test-facing entrypoint for
    pre-existing deterministic scenarios.  The live module imports neither it
    nor the fixture adapter, closing the accidental production route.
    """
    if type(context) is not MarshalledRunContext:
        raise TypeError("production execution requires a marshalled run context")
    return _execute(context._context, schemas)
