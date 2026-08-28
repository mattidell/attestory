"""Ordinary-fact layer and the six synthetic cases.

Nothing here classifies. The user supplies what they can see on a statement and
what they did: that they bought an obligation between interest payment dates,
and what they paid the seller for interest that had already accrued. The words
"taxable", "includible", and "adjustment" do not appear in a fact a user
supplies.

Every identity is a demonstration value under `demo.*`.

TI-A1 has its own box-3 Series EE fixture on a second statement. The fixture
records the reported amount, the obligation kind, and an education-expense
answer. It does not record issuance year, owner age, filing status, modified
AGI, qualified expenses after reductions, or redemption proceeds, so it cannot
establish a positive § 135 exclusion.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from decimal import Decimal
from typing import Any

from packages.derivation.evaluator import Environment

# --- Box-1 fixture: the accrued-interest slice ------------------------------

REPORTED_BOX1 = "demo.f1099int.stmt-a.box1-interest"
REPORTED_PAYER = "demo.f1099int.stmt-a.payer"
REPORTED_OBLIGATION = "demo.f1099int.stmt-a.obligation"

BOUGHT_BETWEEN_DATES = "demo.circumstance.obligation-1.bought-between-interest-dates"
ACCRUED_PAID_TO_SELLER = "demo.circumstance.obligation-1.accrued-interest-paid-to-seller"
ACCRUED_RELATES_TO = "demo.circumstance.obligation-1.relates-to-obligation"

OBLIGATION_KIND = "demo.obligation-1.kind"
EDUCATION_EXPENSES_CLAIMED = "demo.circumstance.obligation-1.qualified-education-expenses"

OBLIGATION_ID = "demo.obligation-1"

# --- Box-3 fixture: the outside-slice savings-bond case ---------------------
# A different statement, a different reported box, a different obligation. The
# amount is deliberately not 1200, so a result that leaks in from the box-1
# fixture is visible rather than plausible.

REPORTED_BOX3 = "demo.f1099int.stmt-b.box3-savings-bond-interest"
REPORTED_PAYER_B = "demo.f1099int.stmt-b.payer"
REPORTED_OBLIGATION_B = "demo.f1099int.stmt-b.obligation"

BOUGHT_BETWEEN_DATES_B = "demo.circumstance.obligation-2.bought-between-interest-dates"
ACCRUED_PAID_TO_SELLER_B = "demo.circumstance.obligation-2.accrued-interest-paid-to-seller"
ACCRUED_RELATES_TO_B = "demo.circumstance.obligation-2.relates-to-obligation"

OBLIGATION_KIND_B = "demo.obligation-2.kind"
EDUCATION_EXPENSES_CLAIMED_B = "demo.circumstance.obligation-2.qualified-education-expenses"

OBLIGATION_ID_B = "demo.obligation-2"


@dataclass(frozen=True)
class FactNames:
    """Which fact names a fixture uses. Both fixtures answer the same questions
    about different holdings on different statements."""

    reported_amount: str
    reported_payer: str
    reported_obligation: str
    bought_between_dates: str
    accrued_paid_to_seller: str
    accrued_relates_to: str
    obligation_kind: str
    education_expenses: str
    reported_box: str

    def all_names(self) -> tuple[str, ...]:
        return (
            self.reported_amount,
            self.reported_payer,
            self.reported_obligation,
            self.bought_between_dates,
            self.accrued_paid_to_seller,
            self.accrued_relates_to,
            self.obligation_kind,
            self.education_expenses,
        )


BOX1_NAMES = FactNames(
    reported_amount=REPORTED_BOX1,
    reported_payer=REPORTED_PAYER,
    reported_obligation=REPORTED_OBLIGATION,
    bought_between_dates=BOUGHT_BETWEEN_DATES,
    accrued_paid_to_seller=ACCRUED_PAID_TO_SELLER,
    accrued_relates_to=ACCRUED_RELATES_TO,
    obligation_kind=OBLIGATION_KIND,
    education_expenses=EDUCATION_EXPENSES_CLAIMED,
    reported_box="box 1",
)

BOX3_NAMES = FactNames(
    reported_amount=REPORTED_BOX3,
    reported_payer=REPORTED_PAYER_B,
    reported_obligation=REPORTED_OBLIGATION_B,
    bought_between_dates=BOUGHT_BETWEEN_DATES_B,
    accrued_paid_to_seller=ACCRUED_PAID_TO_SELLER_B,
    accrued_relates_to=ACCRUED_RELATES_TO_B,
    obligation_kind=OBLIGATION_KIND_B,
    education_expenses=EDUCATION_EXPENSES_CLAIMED_B,
    reported_box="box 3",
)

# An obligation identity is one fact *type* supplied by two different sources:
# the statement says which holding it covers, and the taxpayer says which
# holding they bought. Giving both symbols the same fact type is what lets the
# engine compare them -- `categorical_compare` blocks on a domain mismatch, so
# two identities of different declared types cannot be compared at all. This is
# how the relation becomes operational rather than decorative.
OBLIGATION_IDENTITY_TYPE = "demo.fact-type.obligation-identity"

OBLIGATION_ID_THIRD = "demo.obligation-3"

CATEGORICAL_DOMAINS: dict[str, list[str]] = {
    BOUGHT_BETWEEN_DATES: ["yes", "no"],
    EDUCATION_EXPENSES_CLAIMED: ["yes", "no"],
    OBLIGATION_KIND: ["corporate-bond", "series-ee-savings-bond"],
    BOUGHT_BETWEEN_DATES_B: ["yes", "no"],
    EDUCATION_EXPENSES_CLAIMED_B: ["yes", "no"],
    OBLIGATION_KIND_B: ["corporate-bond", "series-ee-savings-bond"],
    OBLIGATION_IDENTITY_TYPE: [OBLIGATION_ID, OBLIGATION_ID_B, OBLIGATION_ID_THIRD],
}

# Symbols whose declared fact type is not their own name.
SHARED_FACT_TYPES: dict[str, str] = {
    REPORTED_OBLIGATION: OBLIGATION_IDENTITY_TYPE,
    ACCRUED_RELATES_TO: OBLIGATION_IDENTITY_TYPE,
    REPORTED_OBLIGATION_B: OBLIGATION_IDENTITY_TYPE,
    ACCRUED_RELATES_TO_B: OBLIGATION_IDENTITY_TYPE,
}


@dataclass(frozen=True)
class Fact:
    """One ordinary fact, versioned so a correction is observable."""

    name: str
    value: Any
    version: int = 1
    # What the user was actually asked, in ordinary words. Present so the
    # prototype can show it never asked for a legal conclusion.
    question: str = ""

    def corrected_to(self, value: Any) -> "Fact":
        return replace(self, value=value, version=self.version + 1)


@dataclass(frozen=True)
class Workspace:
    """The ordinary facts on record, plus which fact names this fixture uses."""

    facts: dict[str, Fact]
    names: FactNames = BOX1_NAMES
    closed_sets: frozenset[str] = frozenset()

    def with_correction(self, name: str, value: Any) -> "Workspace":
        facts = dict(self.facts)
        facts[name] = facts[name].corrected_to(value)
        return replace(self, facts=facts)

    def without(self, name: str) -> "Workspace":
        facts = {k: v for k, v in self.facts.items() if k != name}
        return replace(self, facts=facts)

    def versions(self) -> dict[str, int]:
        return {name: fact.version for name, fact in self.facts.items()}

    def environment(self) -> Environment:
        symbols: dict[str, Any] = {}
        symbol_fact_types: dict[str, str] = {}
        for name, fact in self.facts.items():
            symbols[name] = (
                Decimal(str(fact.value)) if isinstance(fact.value, (int, float)) else fact.value
            )
            if name in SHARED_FACT_TYPES:
                symbol_fact_types[name] = SHARED_FACT_TYPES[name]
            elif name in CATEGORICAL_DOMAINS:
                symbol_fact_types[name] = name
        return Environment(
            symbols=symbols,
            sources={},
            closed_sets=self.closed_sets,
            parameters={},
            canon={},
            symbol_fact_types=symbol_fact_types,
            categorical_domains=CATEGORICAL_DOMAINS,
        )


# --- Box-1 fixture builders -------------------------------------------------


def _statement_facts(box1: float = 1200) -> dict[str, Fact]:
    return {
        REPORTED_BOX1: Fact(REPORTED_BOX1, box1, question="Box 1 of the Form 1099-INT"),
        REPORTED_PAYER: Fact(
            REPORTED_PAYER, "demo.payer.bank-1", question="Who sent the statement"
        ),
        REPORTED_OBLIGATION: Fact(
            REPORTED_OBLIGATION, OBLIGATION_ID, question="Which holding the statement covers"
        ),
    }


def _ordinary_defaults() -> dict[str, Fact]:
    return {
        OBLIGATION_KIND: Fact(
            OBLIGATION_KIND, "corporate-bond", question="What kind of holding is it?"
        ),
        EDUCATION_EXPENSES_CLAIMED: Fact(
            EDUCATION_EXPENSES_CLAIMED,
            "no",
            question="Did you cash savings bonds to pay qualified education expenses?",
        ),
    }


def case_ti_b1() -> Workspace:
    """No accrued-interest-at-purchase circumstance. $1,200 is the whole story."""
    facts = _statement_facts() | _ordinary_defaults()
    facts[BOUGHT_BETWEEN_DATES] = Fact(
        BOUGHT_BETWEEN_DATES,
        "no",
        question="Did you buy this holding between its interest payment dates?",
    )
    return Workspace(facts, BOX1_NAMES)


def case_ti_b2() -> Workspace:
    """Bought mid-period; $300 of the $1,200 was the seller's interest."""
    facts = _statement_facts() | _ordinary_defaults()
    facts[BOUGHT_BETWEEN_DATES] = Fact(
        BOUGHT_BETWEEN_DATES,
        "yes",
        question="Did you buy this holding between its interest payment dates?",
    )
    facts[ACCRUED_PAID_TO_SELLER] = Fact(
        ACCRUED_PAID_TO_SELLER,
        300,
        question="How much did you pay the seller for interest already built up?",
    )
    facts[ACCRUED_RELATES_TO] = Fact(
        ACCRUED_RELATES_TO, OBLIGATION_ID, question="Which holding did you buy?"
    )
    return Workspace(facts, BOX1_NAMES)


def case_ti_n1() -> Workspace:
    """The circumstance applies and the amount has not been answered."""
    return case_ti_b2().without(ACCRUED_PAID_TO_SELLER)


def case_ti_l1() -> Workspace:
    """Source correction: the statement is reissued at $1,000."""
    return case_ti_b2().with_correction(REPORTED_BOX1, 1000)


def case_ti_l2() -> Workspace:
    """Circumstance correction: the taxpayer actually paid the seller $250."""
    return case_ti_b2().with_correction(ACCRUED_PAID_TO_SELLER, 250)


# --- Box-3 fixture builder --------------------------------------------------


def case_ti_a1() -> Workspace:
    """Outside-slice coverage probe: box-3 Series EE interest plus an education answer.

    The fixture is sufficient to refuse coverage. It is not a complete § 135
    fact pattern (no issuance year, owner age, filing status, modified AGI,
    qualified expenses after reductions, or redemption proceeds), so it cannot
    prove that full inclusion is wrong for this taxpayer.
    """
    facts = {
        REPORTED_BOX3: Fact(REPORTED_BOX3, 840, question="Box 3 of the Form 1099-INT"),
        REPORTED_PAYER_B: Fact(
            REPORTED_PAYER_B, "demo.payer.treasury-direct-1", question="Who sent the statement"
        ),
        REPORTED_OBLIGATION_B: Fact(
            REPORTED_OBLIGATION_B,
            OBLIGATION_ID_B,
            question="Which holding the statement covers",
        ),
        OBLIGATION_KIND_B: Fact(
            OBLIGATION_KIND_B,
            "series-ee-savings-bond",
            question="What kind of holding is it?",
        ),
        EDUCATION_EXPENSES_CLAIMED_B: Fact(
            EDUCATION_EXPENSES_CLAIMED_B,
            "yes",
            question="Did you cash savings bonds to pay qualified education expenses?",
        ),
        BOUGHT_BETWEEN_DATES_B: Fact(
            BOUGHT_BETWEEN_DATES_B,
            "no",
            question="Did you buy this holding between its interest payment dates?",
        ),
    }
    return Workspace(facts, BOX3_NAMES)


CASES: dict[str, Any] = {
    "TI-B1": case_ti_b1,
    "TI-B2": case_ti_b2,
    "TI-N1": case_ti_n1,
    "TI-L1": case_ti_l1,
    "TI-L2": case_ti_l2,
    "TI-A1": case_ti_a1,
}
