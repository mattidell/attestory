"""Ordinary-language input mapping for the bond-acquisition circumstance.

Seam 6 (`document-ordinary-fact-translation` milestone). This module maps a
**structured** ordinary-language answer set — never free text — about an
identified bond (or other interest-bearing obligation) acquisition and an
accrued-interest payment made to the seller, into a canonical circumstance
fact.

Subject and scope, stated once so they cannot silently drift:

- **Subject.** Exactly one real-world circumstance: "I acquired this
  obligation between interest payment dates and paid the seller the interest
  that had already accrued." Nothing about disposition, premium
  amortization, market discount, or any other neighboring circumstance.
- **Scope of the output.** Exactly one canonical circumstance fact per
  mapped answer set, carrying only the ordinary quantities and identifying
  information a person can state without knowing tax law: who paid the
  interest (as it would appear on their statement), enough identifying
  information about the specific obligation to distinguish it from another
  one from the same payer, the acquisition date, and the amount paid to the
  seller for interest that had already accrued. It does **not** decide, and
  never carries, the tax treatment those facts eventually support — that is
  Seam 5's job, downstream of an adopted rule, not this seam's.

No tax classification is ever requested from or supplied by the user. The
input schema below (`ORDINARY_ANSWERS_SCHEMA`) is closed
(`additionalProperties: false`): a field that does not correspond to an
ordinary fact in the list above cannot be smuggled through it, whatever a
caller intends. This is a structural guarantee, not a naming convention —
`validate_ordinary_answers` fails closed on any unrecognized field.

Contribution admission — `packages.kernel.contribution.apply_contribution_batch`,
the real, general manual-entry admission path (ADR-0032 D2) — is what
validates the mapper's output. This module does not reimplement or shortcut
that boundary: `contribute_ordinary_acquisition` builds the same
`contribution` / `assertion` acts any other manual-entry fact would use and
hands them to the real applicator.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

import jsonschema

from packages.kernel.contribution import (
    ContributionBatchResult,
    apply_contribution_batch,
)
from packages.kernel.findings import FindingState
from packages.kernel.schema_registry import SchemaRegistry

# ---------------------------------------------------------------------------
# The structured ordinary-language input projection.
# ---------------------------------------------------------------------------

# Every field here is answerable by a person from ordinary knowledge of their
# own affairs and their own statements — never a tax-law judgment. The
# right-hand comments are the plain-language question surface a real
# interaction would show; they are captured here as data (not comments) in
# `ORDINARY_QUESTIONS` below so a test can inspect them directly, and are
# repeated as comments for a human reader of this schema.
ORDINARY_ANSWERS_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        # "Who paid or reported this interest?" (as it appears on your
        # statement or 1099-INT — not a legal-entity lookup)
        "payer_name": {"type": "string", "minLength": 1},
        # "What obligation is this? Describe it well enough that you could
        # tell it apart from another one from the same payer."
        "obligation_description": {"type": "string", "minLength": 1},
        # "Do you have an account or reference number for this obligation?"
        # (optional — many ordinary statements do not surface one)
        "obligation_reference": {"type": ["string", "null"], "minLength": 1},
        # "On what date did you acquire it?"
        "acquisition_date": {
            "type": "string",
            "pattern": r"^\d{4}-\d{2}-\d{2}$",
        },
        # "How much did you pay the seller for interest that had already
        # accrued before you owned it?" (a dollar figure the buyer and
        # seller settled between themselves, not a tax adjustment)
        "accrued_interest_paid_to_seller": {"type": "number", "minimum": 0},
        "currency": {"const": "USD"},
        # "Which tax year does this apply to?"
        "tax_year": {"type": "integer", "minimum": 2000, "maximum": 2100},
    },
    "required": [
        "payer_name",
        "obligation_description",
        "acquisition_date",
        "accrued_interest_paid_to_seller",
        "currency",
        "tax_year",
    ],
    "additionalProperties": False,
}

# The plain-language question surface, named so a reviewer (or a test) can
# confirm no question asks for a tax classification, election, or treatment.
ORDINARY_QUESTIONS: tuple[tuple[str, str], ...] = (
    ("payer_name", "Who paid or reported this interest?"),
    (
        "obligation_description",
        "What obligation is this? Describe it well enough to tell it apart "
        "from another one from the same payer.",
    ),
    (
        "obligation_reference",
        "Do you have an account or reference number for this obligation? "
        "(optional)",
    ),
    ("acquisition_date", "On what date did you acquire it?"),
    (
        "accrued_interest_paid_to_seller",
        "How much did you pay the seller for interest that had already "
        "accrued before you owned it?",
    ),
    ("tax_year", "Which tax year does this apply to?"),
)

# Fact-type identity for the canonical circumstance this module emits.
# Registration in a production bundle is out of this seam's scope (Seam 1/2/3
# own the canonical shape adopted rules eventually read); this constant only
# names what this module itself produces, honestly.
OBLIGATION_ACQUISITION_FACT_TYPE_ID = "demo.tax.obligation-acquisition-circumstance"


class OrdinaryInputError(ValueError):
    """The ordinary-language answer set is missing, malformed, or over-broad."""


_VALIDATOR = jsonschema.Draft202012Validator(ORDINARY_ANSWERS_SCHEMA)


def validate_ordinary_answers(answers: Mapping[str, Any]) -> None:
    """Fail closed on anything that is not one of the named ordinary facts.

    This is the subject/scope guarantee made structural: an answer set with
    an extra key (a tax classification, an election, a computed adjustment)
    is rejected here, before it can reach a canonical fact, rather than
    being silently ignored or silently admitted.
    """
    errors = sorted(_VALIDATOR.iter_errors(dict(answers)), key=lambda e: e.path)
    if errors:
        first = errors[0]
        raise OrdinaryInputError(
            f"ordinary answer set is invalid: {first.message} "
            f"(path: {list(first.path)})"
        )


_UNREFERENCED = "unreferenced"

# Names, and their order, of the identity keys used below. Kept as one
# constant so the bundle declaration and the fact-id composer can never
# silently disagree about key order.
_IDENTITY_KEY_ORDER = ("payer", "reference", "tax-year")


def _identity_key_values(
    *, payer_name: str, obligation_reference: str | None, tax_year: int
) -> tuple[tuple[str, str], ...]:
    reference = obligation_reference or _UNREFERENCED
    values = {"payer": payer_name, "reference": reference, "tax-year": str(tax_year)}
    return tuple((name, values[name]) for name in _IDENTITY_KEY_ORDER)


def derive_obligation_acquisition_fact_id(
    *, payer_name: str, obligation_reference: str | None, tax_year: int
) -> str:
    """A stable, source-independent fact id for one obligation's acquisition.

    Identity rests on the payer and the reference the person supplied (or,
    absent a reference, the payer alone plus the tax year) — never on a
    document row, a form line, or an internal sequence number. Seam 2 (not
    this seam) is responsible for resolving *ambiguity* when this identity is
    not enough to distinguish two real obligations from the same payer; this
    function only names what it was given.
    """
    keys = _identity_key_values(
        payer_name=payer_name, obligation_reference=obligation_reference, tax_year=tax_year
    )
    bound = ",".join(f"{name}={value}" for name, value in keys)
    return f"{OBLIGATION_ACQUISITION_FACT_TYPE_ID}|{bound}"


_CIRCUMSTANCE_VALUE_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "obligation": {
            "type": "object",
            "properties": {
                "payer_name": {"type": "string"},
                "description": {"type": "string"},
                "reference": {"type": ["string", "null"]},
            },
            "required": ["payer_name", "description", "reference"],
            "additionalProperties": False,
        },
        "acquisition_date": {"type": "string"},
        "accrued_interest_paid_to_seller": {"type": "number"},
        "currency": {"const": "USD"},
        "tax_year": {"type": "integer"},
    },
    "required": [
        "obligation",
        "acquisition_date",
        "accrued_interest_paid_to_seller",
        "currency",
        "tax_year",
    ],
    "additionalProperties": False,
}


def build_obligation_acquisition_bundle(answers: Mapping[str, Any]) -> dict[str, Any]:
    """A one-off ``bundle.v1`` declaring this circumstance's fact type.

    A kernel literal identity key must enumerate its admissible values at
    declaration time (``fact-type.v1``). This module's own admission
    fixture therefore declares a bundle whose literal domain is exactly the
    payer, reference, and tax year the person just supplied, rather than an
    open-ended domain — a minimal, honest way to let this seam's contribution
    prove out through the real fact lattice without pre-deciding the
    entity/association shape Seam 2 and Seam 1 are still choosing. A
    production integration may adopt a richer, entity-keyed vocabulary
    instead; this bundle is scoped to proving *this* seam's admission path,
    not to fixing that later choice.
    """
    validate_ordinary_answers(answers)
    keys = _identity_key_values(
        payer_name=answers["payer_name"],
        obligation_reference=answers.get("obligation_reference"),
        tax_year=answers["tax_year"],
    )
    identity_keys = [
        {"name": name, "kind": "literal", "values": [value]} for name, value in keys
    ]
    return {
        "schema": "bundle.v1",
        "id": f"demo.vocabulary.{OBLIGATION_ACQUISITION_FACT_TYPE_ID}",
        "label": "Obligation-acquisition circumstance (synthetic, ordinary-language)",
        "fact_types": [
            {
                "schema": "fact-type.v1",
                "id": OBLIGATION_ACQUISITION_FACT_TYPE_ID,
                "title": "Ordinary bond-acquisition and accrued-interest circumstance",
                "nature": "determinable",
                "identity_keys": identity_keys,
                "value_schema": _CIRCUMSTANCE_VALUE_SCHEMA,
                "supersession": {"policy": "free"},
            }
        ],
    }


def map_ordinary_acquisition_answers(
    answers: Mapping[str, Any],
    *,
    finding_id: str,
    evidence_id: str,
    contribution_id: str,
    fact_id: str | None = None,
) -> dict[str, Any]:
    """Map validated ordinary answers to one canonical circumstance finding.

    The returned object is a ``finding.v2`` instance (see
    ``packages/schemas/kernel/finding.v2.schema.json``) whose ``value`` is the
    canonical circumstance fact — an object carrying only the acquisition
    date, the accrued-interest amount paid to the seller, and enough
    identifying information about the obligation and its payer to support
    later association (Seam 2) and constraint (Seam 3) work. No field here
    states or implies a tax conclusion; ``basis`` is ``"attested"`` because
    this is what the person stated about their own circumstance, not what a
    document reported.
    """
    validate_ordinary_answers(answers)

    resolved_fact_id = fact_id or derive_obligation_acquisition_fact_id(
        payer_name=answers["payer_name"],
        obligation_reference=answers.get("obligation_reference"),
        tax_year=answers["tax_year"],
    )

    circumstance_value: dict[str, Any] = {
        "obligation": {
            "payer_name": answers["payer_name"],
            "description": answers["obligation_description"],
            "reference": answers.get("obligation_reference"),
        },
        "acquisition_date": answers["acquisition_date"],
        "accrued_interest_paid_to_seller": answers["accrued_interest_paid_to_seller"],
        "currency": answers["currency"],
        "tax_year": answers["tax_year"],
    }

    return {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": resolved_fact_id,
        "value": circumstance_value,
        "basis": "attested",
        "evidence_ids": [evidence_id],
        "contribution_id": contribution_id,
    }


@dataclass(frozen=True)
class OrdinaryAcquisitionContribution:
    """The synthetic acts one ordinary-answer contribution batch produces."""

    contribution_act: dict[str, Any]
    assertion_act: dict[str, Any]
    finding: dict[str, Any]


def build_ordinary_acquisition_contribution(
    answers: Mapping[str, Any],
    *,
    act_index: int,
    contribution_id: str,
    evidence_id: str,
    finding_id: str,
    committed_against: int,
    fact_id: str | None = None,
) -> OrdinaryAcquisitionContribution:
    """Build the contribution + assertion acts for one ordinary answer set.

    This does not itself decide admissibility — it only assembles the exact
    act shapes ``apply_contribution_batch`` (the real contribution boundary)
    requires, so a caller can pass them straight through. Kept separate from
    ``map_ordinary_acquisition_answers`` so the pure mapping function has no
    dependency on act envelopes or act numbering.
    """
    finding = map_ordinary_acquisition_answers(
        answers,
        finding_id=finding_id,
        evidence_id=evidence_id,
        contribution_id=contribution_id,
        fact_id=fact_id,
    )
    contribution_act = {
        "schema": "act.v1",
        "act_id": f"demo-act-{act_index:03d}",
        "kind": "contribution",
        "actor": "user",
        "at": f"2026-01-01T00:00:{act_index % 60:02d}Z",
        "committed_against": committed_against,
        "payload": {
            "contribution": {
                "schema": "contribution.v1",
                "id": contribution_id,
                "evidence_id": evidence_id,
                "content": {"mode": "ordinary-language-entry", "synthetic": True},
            }
        },
    }
    assertion_act = {
        "schema": "act.v1",
        "act_id": f"demo-act-{act_index + 1:03d}",
        "kind": "assertion",
        "actor": "user",
        "at": f"2026-01-01T00:00:{(act_index + 1) % 60:02d}Z",
        "committed_against": committed_against + 1,
        "payload": {"finding": finding},
    }
    return OrdinaryAcquisitionContribution(
        contribution_act=contribution_act,
        assertion_act=assertion_act,
        finding=finding,
    )


def contribute_ordinary_acquisition(
    state: FindingState,
    answers: Mapping[str, Any],
    *,
    registry: SchemaRegistry,
    record_id: str,
    act_index: int,
    contribution_id: str,
    evidence_id: str,
    finding_id: str,
    committed_against: int,
    fact_id: str | None = None,
) -> ContributionBatchResult:
    """Map ordinary answers and admit them through the real contribution
    boundary in one step.

    This is the seam's load-bearing guarantee: the mapper's own validation
    (``validate_ordinary_answers``) narrows what can be *proposed*, but the
    finding is not treated as real until
    ``packages.kernel.contribution.apply_contribution_batch`` — the same
    machinery every other manual-entry fact goes through — admits it. A
    malformed or over-broad answer set fails at ``validate_ordinary_answers``
    before an act is even built; a well-formed one still runs the full
    admission path and can still be rejected there (e.g. evidence mismatch)
    like any other contribution.
    """
    built = build_ordinary_acquisition_contribution(
        answers,
        act_index=act_index,
        contribution_id=contribution_id,
        evidence_id=evidence_id,
        finding_id=finding_id,
        committed_against=committed_against,
        fact_id=fact_id,
    )
    return apply_contribution_batch(
        state,
        contribution_act=built.contribution_act,
        successor_acts=[built.assertion_act],
        registry=registry,
        record_id=record_id,
        workspace_revision=committed_against,
    )
