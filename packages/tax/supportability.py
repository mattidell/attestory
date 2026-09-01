"""Accrued-amount supportability as a per-pairing adopted tax rule (ADR-0070).

Seam 3 of the Document and Ordinary-Fact Translation Vertical. The
constraint "the accrued amount cannot exceed the associated reported
amount" is an adopted ``rule-artifact.v7`` citizen, not a field on the
ADR-0068 pairing record and not a generic relationship-validation
mechanism.

Dispatch is per pairing finding via
``evaluate_pairing_scoped_rule``: each ADR-0068 pairing is evaluated
independently, the report is resolved by the pairing's own pinned
``right_fact_id`` (masking-prevention), and a correction is visible the
next marshal because there is no cache.

The inequality itself is the real evaluator's ``compare`` / ``choose`` /
``block`` grammar. Accrued amount is read through ADR-0067 field-ref
access (``ref`` + ``field``) off the acquisition object; the associated
report is the scalar box-1 amount the pairing names.
"""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from typing import Any, Mapping

from packages.derivation.evaluator import (
    AccessLog,
    Environment,
    EvalBlocked,
    evaluate,
)
from packages.derivation.pairing_dispatch import (
    PairingBinding,
    PairingBlock,
    PairingPublish,
)
from packages.tax.identity_association import (
    ACQUISITION_FACT_TYPE,
    ASSOCIATION_SYMBOL,
    REPORT_FACT_TYPE,
)

RULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "content"
    / "tax"
    / "2025"
    / "rule.relationship.accrued-supported.json"
)

RULE_ID = "tax.us.2025.rule.relationship.accrued-supported"
SUPPORTABILITY_SYMBOL = "tax.us.2025.relationship.accrued-supported"
ACCRUED_EXCEEDS_ASSOCIATED_REPORT = "ACCRUED_EXCEEDS_ASSOCIATED_REPORT"
ACQUISITION_FIELD = "accrued_interest_paid_to_seller"

PAIRING_TYPE = ASSOCIATION_SYMBOL
COLLECT_SOURCE_NAMES: tuple[str, ...] = (
    ACQUISITION_FACT_TYPE,
    REPORT_FACT_TYPE,
    PAIRING_TYPE,
)


def load_rule() -> dict[str, Any]:
    """Load the checksum-published supportability rule citizen."""
    loaded: dict[str, Any] = json.loads(RULE_PATH.read_text(encoding="utf-8"))
    return loaded


def is_supportability_rule(rule: Mapping[str, Any]) -> bool:
    return rule.get("id") == RULE_ID


def symbol_for(binding: PairingBinding) -> str:
    return f"{SUPPORTABILITY_SYMBOL}|{binding.pairing_fact_id}"


def evaluate_one(
    binding: PairingBinding,
    *,
    rule: Mapping[str, Any],
    base_env: Environment,
) -> PairingPublish | PairingBlock:
    """Evaluate the adopted rule once for one resolved pairing.

    Binds the acquisition object and the named report scalar into a
    pairing-local Environment (the run's Environment with only those
    two symbols) and runs the citizen's ``value`` tree through the real
    evaluator. An unrelated report of the same type is never a symbol
    here — only the pairing's pinned right fact is bound.
    """
    env = replace(
        base_env,
        symbols={
            ACQUISITION_FACT_TYPE: binding.left_value,
            REPORT_FACT_TYPE: binding.right_value,
        },
        sources={},
    )
    try:
        value = evaluate(rule["value"], env, AccessLog())
    except EvalBlocked as exc:
        return PairingBlock(code=exc.category, missing=tuple(exc.missing))
    return PairingPublish(value=value)


def try_dispatch(run_state: Any, rule: Mapping[str, Any]) -> str | None:
    """If ``rule`` is the supportability citizen, dispatch it; else ``None``.

    Called from ``_Run.attempt`` so a real run that includes this rule
    fires per pairing rather than once per rule id. Returns the attempt
    outcome string, or ``None`` when this is some other rule.
    """
    if not is_supportability_rule(rule):
        return None
    base_env = run_state.env()
    result = run_state.evaluate_pairing_scoped_rule(
        pairing_type=PAIRING_TYPE,
        left_type=ACQUISITION_FACT_TYPE,
        right_type=REPORT_FACT_TYPE,
        rule_id=rule["id"],
        rule_version=rule["version"],
        rule_role=rule.get("role", "computation"),
        symbol_for=symbol_for,
        evaluate_one=lambda binding: evaluate_one(
            binding, rule=rule, base_env=base_env
        ),
    )
    if result.blocked and not result.publications:
        return "blocked"
    return "published"
