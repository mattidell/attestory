"""A second, demand-driven runner for portability re-proof (ADR-0007 §5.4).

The primary runner (`runner.run`) is forward and data-driven: it fires every
eligible rule until a fixpoint. This reference runner is backward and
demand-driven: for each output symbol it recursively resolves the producing
rule's dependencies, then fires it. The two schedule rules in different orders
and by different control flow.

They deliberately share the pure evaluator (the operation-semantics canon is
the single reference semantics — re-deriving arithmetic would test a copy, not
portability) and the per-rule step (`_Run.attempt`, which owns finding
assembly, pins, and content-addressed ids). What differs is traversal. So a
byte-identical published-finding set across both runners proves the derived
record is a function of (artifacts, canon, inputs) alone — independent of
evaluation order (E11.3) and serialization strategy (E11.2). A divergence
would mean a scheduler is smuggling meaning the artifacts do not carry.
"""

from __future__ import annotations

from typing import Any

from packages.derivation.loader import DerivationSchemas
from packages.derivation.runner import ATTACHMENT_SCHEMAS, RunContext, RunResult, _Run


def run_reference(ctx: RunContext, schemas: DerivationSchemas) -> RunResult:
    state = _Run(ctx, schemas)
    producers: dict[str, list[dict[str, Any]]] = {}
    for rule in ctx.rules:
        producers.setdefault(rule["publishes"], []).append(rule)

    resolving: set[str] = set()

    def resolve(symbol: str) -> None:
        """Ensure `symbol` is derived if any producer can fire from current state."""
        if symbol in state.symbols:
            return
        if symbol in resolving:
            return  # cyclic demand; the fixpoint pass below still terminates
        resolving.add(symbol)
        for rule in producers.get(symbol, []):
            if rule["id"] in state.resolved:
                continue
            for req in state._requires(rule):
                resolve(req)
            if state.is_eligible(rule):
                if rule.get("schema") in ATTACHMENT_SCHEMAS:
                    state.attempt_attachment(rule)
                else:
                    state.attempt(rule)
                if symbol in state.symbols:
                    break
        resolving.discard(symbol)

    # Demand every declared output. A second pass catches any rule made eligible
    # only after a sibling published (guarded exclusivity, late dependencies).
    changed = True
    while changed:
        before = len(state.resolved)
        for target in sorted(producers):
            resolve(target)
        changed = len(state.resolved) > before

    state.finalize_unreached()
    return state.result()
