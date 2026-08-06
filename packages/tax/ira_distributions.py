"""Bounded 2025 Form 1099-R IRA distribution source boundary.

This module admits only the ordinary, fully taxable IRA-family class selected
by the milestone.  It deliberately does not calculate basis, eligibility,
rollovers, or any special distribution treatment.  A statement's logical
identity is its payer, tax year, and payer statement reference; evidence ids
are not part of the question (ADR-0015).
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

from packages.tax import statements

IRA_FAMILY_INDICATORS = frozenset({"traditional", "sep", "simple"})
NORMAL_DISTRIBUTION_CODE = "7"
IRA_MEMBER_FACT_TYPE = "tax.us.2025.f1099r.ira-box1-taxable-distribution"
IRA_FAMILY_ID = "tax.us.2025.f1099r.ira-fully-taxable"
IRA_CLOSURE_FACT_TYPE = "tax.us.2025.f1099r.ira-fully-taxable.source-closure"
IRA_MAPPING_ID = "tax.us.2025.closure-mapping.f1099r-ira-fully-taxable"
IRA_MAPPING_VERSION = "v1"
IRA_HORIZON_KEY = "family-horizon"
LINE4B_SYMBOL = "tax.us.2025.ira.distributions.line4b"


class IraDistributionError(ValueError):
    """The statement or source closure is outside the bounded class."""


@dataclass(frozen=True)
class IraDistributionStatement:
    payer_id: str
    tax_year: int
    statement_ref: str
    ira_indicator: str
    distribution_codes: tuple[str, ...]
    box1: Decimal | int | float
    box2a: Decimal | int | float | None
    box2b_not_determined: bool | None
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
class Line4bPublication:
    value: Decimal
    line4a: None = None
    mapping_id: str = IRA_MAPPING_ID
    mapping_version: str = IRA_MAPPING_VERSION
    horizon_id: str | None = None
    closure_finding_id: str | None = None
    statement_refs: tuple[str, ...] = ()


def validate_statement(statement: IraDistributionStatement) -> None:
    """Validate the exact fully-taxable admission witness."""
    if statement.tax_year != 2025:
        raise IraDistributionError("tax year must be 2025")
    if statement.ira_indicator not in IRA_FAMILY_INDICATORS:
        raise IraDistributionError("IRA-family indicator is outside the bounded class")
    if statement.distribution_codes != (NORMAL_DISTRIBUTION_CODE,):
        raise IraDistributionError("distribution code must be exactly code 7")
    if statement.box2a is None:
        raise IraDistributionError("box 2a is required")
    if not isinstance(statement.box2b_not_determined, bool):
        raise IraDistributionError("box 2b-not-determined must be explicitly boolean")
    if statement.box2b_not_determined:
        raise IraDistributionError("box 2b-not-determined must be false")
    box1 = Decimal(str(statement.box1))
    box2a = Decimal(str(statement.box2a))
    if box1 < 0 or box2a < 0:
        raise IraDistributionError("box 1 and box 2a must be nonnegative")
    if box1 != box2a:
        raise IraDistributionError("box 1 and box 2a must be exactly equal")


def current_statements(
    records: Iterable[IraDistributionStatement],
) -> tuple[IraDistributionStatement, ...]:
    """Apply originals, same-statement corrections, and reject replays."""
    current: dict[statements.StatementKey, IraDistributionStatement] = {}
    for record in records:
        validate_statement(record)
        classification = statements.classify_assertion(
            record.identity,
            frozenset(current),
            corrected=record.corrected,
        )
        if classification == statements.DUPLICATE:
            raise IraDistributionError("duplicate logical Form 1099-R statement")
        current[record.identity] = record
    return tuple(current[key] for key in sorted(current, key=lambda k: (k.payer_id, k.tax_year, k.payer_ref)))


def publish_line4b(
    records: Iterable[IraDistributionStatement],
    *,
    closure: FamilyClosure | None,
    closure_finding_id: str | None = None,
    current_horizon_id: str | None = None,
) -> Line4bPublication:
    """Aggregate the current bounded members and publish line 4b only.

    Present-source aggregation does not pin closure authority.  A zero from
    an empty source set is admitted only by one affirmative closure finding on
    the current family horizon (ADR-0014/0017).
    """
    current = current_statements(records)
    if not current:
        if closure is None or not closure.attested:
            raise IraDistributionError("empty source family requires affirmative closure")
        if closure.family_id != IRA_FAMILY_ID or closure.family_version != "v1":
            raise IraDistributionError("closure family pin is not the adopted IRA family")
        if current_horizon_id is not None and closure.horizon_id != current_horizon_id:
            raise IraDistributionError("closure is stale for the current family horizon")
        return Line4bPublication(
            value=Decimal(0),
            horizon_id=closure.horizon_id,
            closure_finding_id=closure_finding_id,
        )

    return Line4bPublication(
        value=sum((Decimal(str(record.box1)) for record in current), Decimal(0)),
        statement_refs=tuple(record.statement_ref for record in current),
    )
