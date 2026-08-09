"""Bounded 2025 Form SSA-1099 ordinary Social Security benefits source boundary.

Admits only the ordinary SSA-1099 statement class: box 3/4/5 reconciled and
nonnegative; authoritative taxpayer/spouse beneficiary; ordinary statement-kind
witness; explicit false lump-sum-election; box-6 withholding absent or zero.
Does not compute the Social Security Benefits Worksheet, line 6a, or line 6b.
Logical identity is statement entity + tax year (ADR-0015); evidence ids are
not part of the question.
"""

from __future__ import annotations

from collections.abc import Collection, Iterable, Mapping
from dataclasses import dataclass
from decimal import Decimal

from packages.tax import statements

ADMITTED_SUBJECTS = frozenset({"taxpayer", "spouse"})
ORDINARY_STATEMENT_KIND = "ssa-1099"
SSA_MEMBER_FACT_TYPE = "tax.us.2025.ssa1099.box5-net-benefits"
SSA_FAMILY_ID = "tax.us.2025.ssa1099.benefits"
SSA_FAMILY_VERSION = "v1"
SSA_CLOSURE_FACT_TYPE = "tax.us.2025.ssa1099.source-closure"
SSA_MAPPING_ID = "tax.us.2025.closure-mapping.ssa1099-benefits"
SSA_MAPPING_VERSION = "v1"
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
        raise SsaBenefitsError(
            "a prior-year lump-sum election is outside the bounded class"
        )
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


def validate_projected_source_boundary(
    findings: Iterable[Mapping[str, object]],
    withdrawn_fact_ids: Collection[str] = (),
) -> None:
    """Validate SSA source relationships at the live production boundary.

    The content helper above is useful for unit-level paper examples, but live
    runs consume projected findings. This check therefore repeats the two
    relationships that determine whether a projected SSA member is admissible:
    box 5 equals box 3 minus box 4, and a spouse recipient requires an
    authoritative married-filing-jointly status. Values are read after
    correction projection, so a filing-status correction cannot leave an old
    spouse admission usable.
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
            filing_status = current.get(
                f"tax.us.2025.filing-status|tax-year={tax_year or '2025'}"
            )
            if filing_status != "married_filing_jointly":
                raise SsaBenefitsError(
                    "production SSA admission permits a spouse recipient only on "
                    "a married-filing-jointly return"
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
    """Aggregate current members' box 5 into the closed source subtotal.

    Present-source aggregation does not pin closure. Empty-source zero requires
    affirmative closure on the current family horizon (ADR-0014/0017). This
    subtotal is not Form 1040 line 6a/6b or worksheet output.
    """
    current = current_statements(records)
    if not current:
        if closure is None or not closure.attested:
            raise SsaBenefitsError("empty source family requires affirmative closure")
        if (
            closure.family_id != SSA_FAMILY_ID
            or closure.family_version != SSA_FAMILY_VERSION
        ):
            raise SsaBenefitsError(
                "closure family pin is not the adopted SSA-1099 family"
            )
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
