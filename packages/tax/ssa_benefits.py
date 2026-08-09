"""Bounded 2025 Form SSA-1099 ordinary Social Security benefits source boundary.

This module admits only the ordinary SSA-1099 statement class selected by the
milestone: box 3, box 4, and box 5 reconciled and nonnegative; an authoritative
taxpayer/spouse beneficiary subject; an explicit ordinary statement-kind
witness (never RRB-1099, SSA-1042S, or another foreign social-benefit
statement); an explicit false lump-sum-election witness; and box-6 withholding
absent or zero. It deliberately does not compute the Social Security Benefits
Worksheet, line 6a, line 6b, or any withholding/payment path. A statement's
logical identity is its payer, tax year, and payer statement reference (the
box-8 claim number as printed); evidence ids are not part of the question
(ADR-0015).
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

from packages.tax import statements

ADMITTED_SUBJECTS = frozenset({"taxpayer", "spouse"})
ORDINARY_STATEMENT_KIND = "ssa-1099"
SSA_MEMBER_FACT_TYPE = "tax.us.2025.ssa1099.box5-net-benefits"
SSA_FAMILY_ID = "tax.us.2025.ssa1099.benefits"
SSA_FAMILY_VERSION = "v1"
SSA_CLOSURE_FACT_TYPE = "tax.us.2025.ssa1099.source-closure"
SSA_MAPPING_ID = "tax.us.2025.closure-mapping.ssa1099-benefits"
SSA_MAPPING_VERSION = "v1"
SSA_HORIZON_KEY = "family-horizon"
SUBTOTAL_SYMBOL = "tax.us.2025.ssa1099.benefits.box5-subtotal"


class SsaBenefitsError(ValueError):
    """The statement or source closure is outside the bounded class."""


@dataclass(frozen=True)
class SsaBenefitsStatement:
    payer_id: str
    tax_year: int
    statement_ref: str
    subject: str
    statement_kind: str
    box3: Decimal | int | float | None
    box4: Decimal | int | float | None
    box5: Decimal | int | float | None
    box6: Decimal | int | float | None
    lump_sum_election: bool | None
    finding_id: str = ""
    corrected: bool = False

    @property
    def identity(self) -> statements.StatementKey:
        return statements.statement_key(
            self.payer_id, str(self.tax_year), self.statement_ref
        )


@dataclass(frozen=True)
class FamilyClosure:
    family_id: str
    family_version: str
    horizon_id: str
    attested: bool


@dataclass(frozen=True)
class SubtotalPublication:
    value: Decimal
    mapping_id: str = SSA_MAPPING_ID
    mapping_version: str = SSA_MAPPING_VERSION
    horizon_id: str | None = None
    closure_finding_id: str | None = None
    statement_refs: tuple[str, ...] = ()


def validate_statement(statement: SsaBenefitsStatement) -> None:
    """Validate the exact ordinary-benefits admission witness."""
    if statement.tax_year != 2025:
        raise SsaBenefitsError("tax year must be 2025")
    if statement.subject not in ADMITTED_SUBJECTS:
        raise SsaBenefitsError(
            "beneficiary subject must be the taxpayer or joint-return spouse"
        )
    if statement.statement_kind != ORDINARY_STATEMENT_KIND:
        raise SsaBenefitsError(
            "statement kind must be ordinary Form SSA-1099; RRB-1099, "
            "SSA-1042S, and other foreign social-benefit statements are "
            "outside the bounded class"
        )
    if not isinstance(statement.lump_sum_election, bool):
        raise SsaBenefitsError("lump-sum-election witness must be explicitly boolean")
    if statement.lump_sum_election:
        raise SsaBenefitsError("a prior-year lump-sum election is outside the bounded class")
    if statement.box3 is None or statement.box4 is None or statement.box5 is None:
        raise SsaBenefitsError("box 3, box 4, and box 5 are all required")
    box3 = Decimal(str(statement.box3))
    box4 = Decimal(str(statement.box4))
    box5 = Decimal(str(statement.box5))
    if box3 < 0 or box4 < 0 or box5 < 0:
        raise SsaBenefitsError("box 3, box 4, and box 5 must be nonnegative")
    if box5 != box3 - box4:
        raise SsaBenefitsError("box 5 must equal box 3 minus box 4 exactly")
    if statement.box6 is not None and Decimal(str(statement.box6)) != 0:
        raise SsaBenefitsError(
            "box 6 withholding must be absent or zero in the bounded class"
        )


def current_statements(
    records: Iterable[SsaBenefitsStatement],
) -> tuple[SsaBenefitsStatement, ...]:
    """Apply originals, same-statement corrections, and reject replays."""
    current: dict[statements.StatementKey, SsaBenefitsStatement] = {}
    for record in records:
        validate_statement(record)
        classification = statements.classify_assertion(
            record.identity,
            frozenset(current),
            corrected=record.corrected,
        )
        if classification == statements.DUPLICATE:
            raise SsaBenefitsError("duplicate logical Form SSA-1099 statement")
        current[record.identity] = record
    return tuple(
        current[key]
        for key in sorted(current, key=lambda k: (k.payer_id, k.tax_year, k.payer_ref))
    )


def publish_subtotal(
    records: Iterable[SsaBenefitsStatement],
    *,
    closure: FamilyClosure | None,
    closure_finding_id: str | None = None,
    current_horizon_id: str | None = None,
) -> SubtotalPublication:
    """Aggregate the current bounded members' box 5 into the closed subtotal.

    Present-source aggregation does not pin closure authority. A zero from
    an empty source set is admitted only by one affirmative closure finding on
    the current family horizon (ADR-0014/0017). This subtotal is the source
    side only: it is not Form 1040 line 6a, line 6b, or any worksheet output.
    """
    current = current_statements(records)
    if not current:
        if closure is None or not closure.attested:
            raise SsaBenefitsError("empty source family requires affirmative closure")
        if closure.family_id != SSA_FAMILY_ID or closure.family_version != SSA_FAMILY_VERSION:
            raise SsaBenefitsError("closure family pin is not the adopted SSA-1099 family")
        if current_horizon_id is not None and closure.horizon_id != current_horizon_id:
            raise SsaBenefitsError("closure is stale for the current family horizon")
        return SubtotalPublication(
            value=Decimal(0),
            horizon_id=closure.horizon_id,
            closure_finding_id=closure_finding_id,
        )

    return SubtotalPublication(
        value=sum((Decimal(str(record.box5)) for record in current), Decimal(0)),
        statement_refs=tuple(record.statement_ref for record in current),
    )
