"""Record-derived source-coverage read model.

ADR-0016 decision 3: coverage presents the exact authoritative closure
claim, never shorthand, and a rollup cannot silently report a broader
universe complete. This model is derived entirely from projected record
state plus the adopted declarations and mappings — no second
authoritative store — and it reuses the runner's own admission
resolution, so coverage can never call a family closed that a run would
block on, or vice versa.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from packages.derivation.marshal import marshal_closure_authority
from packages.derivation.source_authority import resolve_closure_admissions
from packages.kernel.currency import CurrencyView
from packages.kernel.findings import FindingState

CLOSED = "closed"
OPEN = "open"


@dataclass(frozen=True)
class FamilyCoverage:
    """One family's coverage: the exact claim and its freshness state.

    ``status`` is CLOSED only while a current literal-true closure
    finding stands on the family's current horizon; a later membership
    transition reopens the family without any manual withdrawal
    (ADR-0017). The claim text is the declaration's, verbatim.
    """

    family_id: str
    exact_claim: str
    authorizes_subtotal: str
    current_horizon: str | None
    status: str
    closure_finding_id: str | None


def coverage_report(
    state: FindingState,
    currency: CurrencyView,
    families: dict[str, dict[str, Any]],
    mappings: dict[str, dict[str, Any]],
) -> list[FamilyCoverage]:
    """Every declared family's coverage, in family-id order."""
    mapping_list = list(mappings.values())
    records, current_horizons = marshal_closure_authority(
        state, currency, mapping_list
    )
    admissions = resolve_closure_admissions(
        mapping_list, list(families.values()), records, current_horizons
    )
    report: list[FamilyCoverage] = []
    for family_id in sorted(families):
        family = families[family_id]
        admission = admissions.get(family_id)
        report.append(
            FamilyCoverage(
                family_id=family_id,
                exact_claim=family["closure_claim"],
                authorizes_subtotal=family["authorizes_subtotal"],
                current_horizon=current_horizons.get(family_id),
                status=CLOSED if admission is not None else OPEN,
                closure_finding_id=(
                    admission.closure_finding_id if admission is not None else None
                ),
            )
        )
    return report
