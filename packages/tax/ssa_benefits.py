"""Bounded 2025 Form SSA-1099 ordinary Social Security benefits source boundary.

Admits only the ordinary SSA-1099 statement class: box 3/4/5 reconciled;
authoritative taxpayer/spouse beneficiary; ordinary statement-kind witness;
explicit false lump-sum-election witness; box-6 withholding absent or zero.
Box 5 nonnegativity is enforced by the admitted fact type's own value schema
(``tax.us.2025.ssa1099.box5-net-benefits``'s ``"minimum": 0``
in ``ssa1099.bundle.v2.json``), not by this module: this module's
``validate_projected_source_boundary`` checks only the box 3/4/5
reconciliation relationship and the spouse-recipient guard, which no
value-schema constraint can express. Does not compute the Social Security
Benefits Worksheet, line 6a, or line 6b.

Logical identity for this family is the SSA-1099 statement entity plus tax
year — never payer. This is a deliberate, milestone-scoped divergence from
ADR-0015's payer-bearing 1099-INT statement key (recorded in the milestone
plan, "Ratified decision — statement identity"): SSA is the single issuer for
this admitted ordinary class, so a payer component would be degenerate and
would not distinguish any two admissible facts. The entity itself individuates
the logical statement (``packages/kernel/facts.py`` binds each admitted
``tax.us.ssa1099-statement`` entity to its own fact id via the fact type's
declared identity keys); no separate payer/reference sameness key is needed or
used here. Evidence ids are never part of the question.

This module previously carried a second, test-only enforcement surface
(``SsaBenefitsStatement``, ``validate_statement``, ``current_statements``,
``publish_subtotal``, ``FamilyClosure``, ``SubtotalPublication``) that
restated these same rules against the ADR-0015 payer-bearing
``packages.tax.statements`` key rather than the production entity-based
identity, and that no production path ever called. It has been removed: its
cases now exist as production-shaped equivalents exercising the real
admission boundary below (and the kernel's entity/finding/currency machinery
directly) in ``tests/test_ssa1099_benefits_line6_track2.py``, so a second
surface that could silently drift from production is no longer carried. Only
``validate_projected_source_boundary`` is production-reachable (called from
``packages/derivation/live.py`` inside ``live_coordinate_run``); this module
is now unambiguously production.
"""

from __future__ import annotations

from collections.abc import Collection, Iterable, Mapping
from decimal import Decimal

SSA_MEMBER_FACT_TYPE = "tax.us.2025.ssa1099.box5-net-benefits"


class SsaBenefitsError(ValueError):
    """The statement or source closure is outside the bounded class."""


def validate_projected_source_boundary(
    findings: Iterable[Mapping[str, object]],
    withdrawn_fact_ids: Collection[str] = (),
) -> None:
    """Validate SSA source relationships at the live production boundary.

    Live runs consume projected findings, so this checks the relationships
    that determine whether a projected SSA member is admissible: box 5 equals
    box 3 minus box 4, and a spouse recipient requires an authoritative
    married-filing-jointly status. Values are read after correction
    projection (last-inserted-wins per the fact type's ``free`` supersession
    policy, matching ``packages/kernel/findings.py``'s
    ``_current_value_for_fact``), so a filing-status correction or a
    statement-value correction cannot leave a stale admission usable.
    """
    current: dict[str, object] = {}
    withdrawn = set(withdrawn_fact_ids)
    for finding in findings:
        fact_id = finding.get("fact_id")
        if not isinstance(fact_id, str) or fact_id in withdrawn:
            continue
        current[fact_id] = finding.get("value")

    for box5_id, box5 in current.items():
        if not box5_id.startswith(f"{SSA_MEMBER_FACT_TYPE}|"):
            continue
        suffix = box5_id.split("|", 1)[1]
        box3 = current.get(f"tax.us.2025.ssa1099.box3-benefits-paid|{suffix}")
        box4 = current.get(f"tax.us.2025.ssa1099.box4-repayment|{suffix}")
        if box3 is None or box4 is None:
            continue  # companion-presence admission reports missing witnesses
        try:
            reconciled = Decimal(str(box3)) - Decimal(str(box4))
            reported = Decimal(str(box5))
        except Exception as exc:
            raise SsaBenefitsError("SSA box 3, box 4, and box 5 must be numeric") from exc
        if reported != reconciled:
            raise SsaBenefitsError(
                "production SSA admission requires box 5 to equal box 3 minus box 4"
            )

        recipient = current.get(f"tax.us.2025.ssa1099.recipient|{suffix}")
        if recipient == "spouse":
            tax_year = next(
                (part.split("=", 1)[1] for part in suffix.split(",") if part.startswith("tax-year=")),
                None,
            )
            if tax_year is None:
                # Every fact id admitted for this member fact type carries a
                # tax-year key by construction (the fact type's declared
                # identity keys always include it; packages/kernel/facts.py
                # renders every key into the fact id, so a valid admitted
                # fact id can never omit it). A missing tax-year segment here
                # therefore means the suffix cannot be trusted to identify
                # the correct filing-status fact - failing closed instead of
                # silently defaulting to a specific tax year, which could
                # read the wrong filing-status fact and wrongly admit or
                # reject a spouse recipient.
                raise SsaBenefitsError(
                    "production SSA admission requires an explicit tax-year "
                    "key on the recipient suffix; cannot resolve filing status"
                )
            filing_status = current.get(
                f"tax.us.2025.filing-status|tax-year={tax_year}"
            )
            if filing_status != "married_filing_jointly":
                raise SsaBenefitsError(
                    "production SSA admission permits a spouse recipient only on "
                    "a married-filing-jointly return"
                )
