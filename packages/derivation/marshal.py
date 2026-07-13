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

from typing import Any

from packages.derivation.source_authority import (
    ClosureFindingRecord,
    SourceAuthorityError,
)
from packages.kernel.currency import CurrencyView
from packages.kernel.findings import FindingState


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
        horizon_key = mapping["closure_horizon_key"]
        prefix = f"{fact_type}|"
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
                    fact_type=fact_type,
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
