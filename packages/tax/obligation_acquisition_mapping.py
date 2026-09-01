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

import math
from dataclasses import dataclass
from datetime import date, datetime
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
        "payer_name": {"type": "string", "minLength": 1, "pattern": r"\S"},
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
        # "Do you have the statement or account reference exactly as it
        # appears on the 1099-INT or account statement that reports this
        # interest?" (optional — a person may not have matched the
        # acquisition to a specific statement yet). This is the shared
        # discriminator Seam 2 uses to resolve the association with
        # confidence instead of guessing among several same-payer reports;
        # it is still an ordinary fact about the person's own paperwork,
        # never a tax classification.
        "reported_statement_reference": {"type": ["string", "null"], "minLength": 1},
        # "If there is exactly one report from this payer for this year,
        # do you confirm it is the one this acquisition concerns?"
        # (optional; a person only sees this question when no statement
        # reference was given and the interaction can name the single
        # candidate). A missing or false answer here is not a "no" about
        # tax treatment — it just means Seam 2 must not guess.
        "confirmed_report_match": {"type": "boolean"},
    },
    "required": [
        "payer_name",
        "obligation_description",
        "acquisition_date",
        "accrued_interest_paid_to_seller",
        "currency",
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
    (
        "reported_statement_reference",
        "Do you have the statement or account reference exactly as it "
        "appears on the 1099-INT or account statement that reports this "
        "interest? (optional)",
    ),
    (
        "confirmed_report_match",
        "If there is exactly one report from this payer for this year, do "
        "you confirm it is the one this acquisition concerns? (optional)",
    ),
)

# Fact-type identity for the canonical circumstance this module emits. This
# is real production identity, not a demo/spike literal: the acquisition
# circumstance is itself a canonical, source-independent, cross-year
# concept, following this module's own established `tax.us.<topic>`
# sibling-entity-kind convention below (``PAYER_ENTITY_KIND`` /
# ``OBLIGATION_ENTITY_KIND`` / ``STATEMENT_ENTITY_KIND``). The identity
# *shape* below is real entity-kind identity, not a closed literal
# enumeration.
OBLIGATION_ACQUISITION_FACT_TYPE_ID = "tax.us.obligation-acquisition-circumstance"

# Entity kinds this seam's identity now rests on. ``PAYER_ENTITY_KIND`` is
# the *same* entity kind Form 1099-INT box 1 uses
# (``packages/content/tax/2025/f1099int.bundle.json``), so payer entities
# correlate across both sides of Seam 2's association by construction, not
# by string equality on a name field. ``OBLIGATION_ENTITY_KIND`` is new: a
# real, arbitrary-cardinality entity kind for the obligation itself, so one
# bundle declaration can represent any number of payers and any number of
# obligations per payer, never a fixed enumerated demo list.
# ``STATEMENT_ENTITY_KIND`` is, again, the same entity kind box 1 already
# uses for its own ``statement`` identity component; this seam never
# declares it as one of its own identity keys (a person may not have
# matched an acquisition to a specific statement yet), but reuses it to
# name the *same* statement entity when a person does supply a reported
# statement reference (see ``derive_reported_statement_entity_id``).
PAYER_ENTITY_KIND = "tax.us.interest-payer"
OBLIGATION_ENTITY_KIND = "tax.us.interest-obligation"
STATEMENT_ENTITY_KIND = "tax.us.1099int-statement"


def derive_payer_entity_id(payer_name: str) -> str:
    """The entity id this seam uses for the payer named in an ordinary answer.

    Deliberately the identity function on the trimmed name, not an opaque
    minted id: two acquisitions naming the same payer text must resolve to
    the same payer entity so Seam 2's join keeps working. This is the same
    convention ``packages.tax.report_statement_identity`` (the document-
    side Form 1099-INT identity module) independently implements for the
    report side (``derive_reported_payer_entity_id``) — neither module
    calls the other; both resolve to the identical entity id for the same
    real-world payer name because both follow the same documented rule.
    Reconciling two different spellings of the same real-world payer is a
    disclosed, separate production condition — not a regression from this
    seam's prior literal-key join, which already only matched on exact
    string equality.
    """
    return payer_name.strip()


def derive_obligation_entity_id(
    *,
    payer_name: str,
    obligation_reference: str | None,
    obligation_description: str,
) -> str:
    """The entity id for the specific obligation an acquisition names.

    Scoped under the payer so the same reference or description from two
    different payers never collides. When no reference was given, the
    (still payer-scoped) description is the disambiguator — the mapper's
    own subject statement already requires it to "tell it apart from
    another one from the same payer".
    """
    payer_entity_id = derive_payer_entity_id(payer_name)
    if obligation_reference:
        disambiguator = f"reference:{obligation_reference.strip()}"
    else:
        disambiguator = f"{_UNREFERENCED}:{obligation_description.strip()}"
    return f"{payer_entity_id}::{disambiguator}"


def derive_reported_statement_entity_id(
    *, payer_name: str, reported_statement_reference: str | None
) -> str | None:
    """The box-1 ``statement`` entity id a reported reference resolves to.

    Returns ``None`` when no reference was supplied — Seam 2 then falls
    back to its coarser payer join (scoped to the run's own reporting-year
    context) rather than treating an absent reference as a match against
    nothing.

    **The shared convention, followed independently on the document side.**
    This function implements the same canonicalization
    ``packages.tax.report_statement_identity`` (the document-side/1099-INT
    identity module) independently implements for the report side: the
    trimmed payer name is the payer entity id, and the statement entity id
    is ``f"{payer_entity_id}::statement::{reference.strip()}"``. This
    function does not import or call anything in
    ``report_statement_identity``, and that module does not import or call
    anything here — the two sides resolve to the identical entity id for
    the same real-world payer and reference because both follow the same
    documented rule, the way two independently-filed EINs match because
    both filers follow the IRS's own format, not because one copied the
    other's code.
    """
    if not reported_statement_reference:
        return None
    payer_entity_id = derive_payer_entity_id(payer_name)
    return f"{payer_entity_id}::statement::{reported_statement_reference.strip()}"


class OrdinaryInputError(ValueError):
    """The ordinary-language answer set is missing, malformed, or over-broad."""


_VALIDATOR = jsonschema.Draft202012Validator(ORDINARY_ANSWERS_SCHEMA)

# Every schema property typed as a JSON Schema number/integer, computed once
# so a newly added numeric field is covered automatically.
_NUMERIC_FIELDS: tuple[str, ...] = tuple(
    name
    for name, spec in ORDINARY_ANSWERS_SCHEMA["properties"].items()
    if spec.get("type") in ("number", "integer")
)


def _reject_non_finite_numbers(answers: Mapping[str, Any]) -> None:
    """Reject ``inf``, ``-inf``, and ``nan`` for any numeric ordinary field.

    JSON Schema's ``"type": "number"``/``"integer"`` constraint does not, by
    itself, exclude IEEE-754 non-finite values: Python's ``jsonschema``
    validator treats ``float('inf')`` and ``float('nan')`` as numbers that
    satisfy a ``minimum`` bound like any other. Left unchecked, a non-finite
    amount would pass ``validate_ordinary_answers`` and be admitted end to
    end as a `"completed"` fact — a fail-*open* result the charter's
    fail-closed requirement does not permit. This check runs before any
    finding is built, so a non-finite value never reaches contribution
    admission.
    """
    for name in _NUMERIC_FIELDS:
        if name not in answers:
            continue
        value = answers[name]
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)) and not math.isfinite(value):
            raise OrdinaryInputError(
                f"ordinary answer set is invalid: {name!r} must be a finite "
                f"number, not {value!r} (path: [{name!r}])"
            )


def _reject_future_acquisition_date(answers: Mapping[str, Any]) -> None:
    """Reject an ``acquisition_date`` that has not happened yet.

    The one circumstance this module names ("I acquired this obligation ...
    and paid the seller the interest that had already accrued") is
    inherently retrospective — a person cannot ordinarily state it about an
    acquisition that has not occurred. A future date is therefore not a
    legitimate instance of this circumstance, not merely an unlikely one;
    see `examination.md` for the one-line decision record.
    """
    raw = answers.get("acquisition_date")
    if not isinstance(raw, str):
        return
    try:
        acquisition_date = datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        # The regex-shaped schema check alone accepts lexically-shaped but
        # calendrically impossible dates (e.g. "2025-99-99", "2025-02-29"
        # in a non-leap year); this is where those are actually caught.
        raise OrdinaryInputError(
            "ordinary answer set is invalid: 'acquisition_date' is not a "
            f"real calendar date, got {raw!r} (path: ['acquisition_date'])"
        ) from None
    if acquisition_date > date.today():
        raise OrdinaryInputError(
            "ordinary answer set is invalid: 'acquisition_date' cannot be in "
            f"the future, got {raw!r} (path: ['acquisition_date'])"
        )


def validate_ordinary_answers(answers: Mapping[str, Any]) -> None:
    """Fail closed on anything that is not one of the named ordinary facts.

    This is the subject/scope guarantee made structural: an answer set with
    an extra key (a tax classification, an election, a computed adjustment)
    is rejected here, before it can reach a canonical fact, rather than
    being silently ignored or silently admitted. This also rejects
    non-finite numeric values (``inf``, ``-inf``, ``nan``) that the JSON
    Schema `"type": "number"` check alone does not exclude — see
    `_reject_non_finite_numbers` — and a future `acquisition_date`, since
    this circumstance is inherently retrospective — see
    `_reject_future_acquisition_date`.
    """
    _reject_non_finite_numbers(answers)
    _reject_future_acquisition_date(answers)
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
# silently disagree about key order. ``payer`` and ``obligation`` are now
# entity-kind keys (see ``PAYER_ENTITY_KIND`` / ``OBLIGATION_ENTITY_KIND``
# above), not literal enumerations: the fact-id rendering is unchanged
# (ADR-0011 ``key=value``), but the *value* bound to each name is now an
# entity id, individuated over currently-introduced entities rather than a
# fixed declared list. ``acquisition-year`` is the calendar year of the
# acquisition *event* itself (``acquisition_date[:4]``) — an ordinary fact
# the person can state without knowing tax law, never asked for
# separately, and never a request for a tax-year/reporting-year
# classification. It is a genuinely different concept from the report's
# own real ``tax-year`` identity component (unchanged, on the report side)
# and from the run's own reporting-year context
# (``packages.tax.identity_association``'s ``reporting_year``, sourced
# from ``run_scope``) — the three must never be conflated.
_IDENTITY_KEY_ORDER = ("payer", "obligation", "acquisition-year")


def _identity_key_values(
    *,
    payer_name: str,
    obligation_reference: str | None,
    obligation_description: str,
    acquisition_date: str,
) -> tuple[tuple[str, str], ...]:
    values = {
        "payer": derive_payer_entity_id(payer_name),
        "obligation": derive_obligation_entity_id(
            payer_name=payer_name,
            obligation_reference=obligation_reference,
            obligation_description=obligation_description,
        ),
        "acquisition-year": acquisition_date[:4],
    }
    return tuple((name, values[name]) for name in _IDENTITY_KEY_ORDER)


def derive_obligation_acquisition_fact_id(
    *,
    payer_name: str,
    obligation_reference: str | None,
    obligation_description: str,
    acquisition_date: str,
) -> str:
    """A stable, source-independent fact id for one obligation's acquisition.

    Identity rests on the payer entity and the obligation entity the
    person's answer resolves to (never on a document row, a form line, or
    an internal sequence number): the obligation entity is disambiguated
    by the reference the person supplied or, absent a reference, by the
    description — which the mapper's own subject statement already
    requires to "tell it apart from another one from the same payer".
    ``acquisition-year`` is read straight off the acquisition's own
    ``acquisition_date`` (never a separately-asked classification) — see
    ``_IDENTITY_KEY_ORDER``'s docstring for why it is distinct from a
    report's own tax-year or the run's reporting-year context. Seam 2
    (not this seam) is responsible for resolving *ambiguity* against the
    reported side when this identity is not enough to select one
    real-world report; this function only names what it was given.
    """
    keys = _identity_key_values(
        payer_name=payer_name,
        obligation_reference=obligation_reference,
        obligation_description=obligation_description,
        acquisition_date=acquisition_date,
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
        "reported_statement_reference": {"type": ["string", "null"]},
        "confirmed_report_match": {"type": "boolean"},
        # Mandatory and non-empty whenever ``confirmed_report_match`` is
        # true, at either tier (see the ``if``/``then`` below and
        # ``map_ordinary_acquisition_answers``'s docstring). ``null``/absent
        # only when ``confirmed_report_match`` is ``false``.
        "confirmed_report_fact_id": {"type": ["string", "null"]},
    },
    "required": [
        "obligation",
        "acquisition_date",
        "accrued_interest_paid_to_seller",
        "currency",
        "reported_statement_reference",
        "confirmed_report_match",
    ],
    "additionalProperties": False,
    # A confirmation always names its target, at either tier: the
    # confirming interaction always resolves exactly one candidate (coarse
    # or statement-narrowed) before asking for confirmation (see
    # ``map_ordinary_acquisition_answers``'s docstring), so it always has a
    # target to name. This schema makes that structural, not merely
    # conventional: a ``true`` confirmation with a missing or blank
    # ``confirmed_report_fact_id`` is not schema-valid, regardless of
    # whether ``reported_statement_reference`` is present
    # (``packages.tax.identity_association.associate`` reads this field
    # uniformly at both tiers).
    "if": {
        "properties": {
            "confirmed_report_match": {"const": True},
        },
        "required": ["confirmed_report_match"],
    },
    "then": {
        "properties": {
            "confirmed_report_fact_id": {"type": "string", "minLength": 1}
        },
        "required": ["confirmed_report_fact_id"],
    },
}


def build_obligation_acquisition_bundle(answers: Mapping[str, Any]) -> dict[str, Any]:
    """A ``bundle.v1`` declaring this circumstance's real, production identity.

    **Real, arbitrary-cardinality identity — not a closed demo fixture.**
    ``payer`` and ``obligation`` are entity-kind identity keys
    (``PAYER_ENTITY_KIND`` / ``OBLIGATION_ENTITY_KIND``): the fact lattice
    individuates one fact per *currently-introduced* entity of that kind
    (``packages/kernel/facts.py:facts_of``), the same mechanism Form
    1099-INT box 1 uses for its own ``payer``/``statement`` identity — not
    a parallel, invented resolution path. A caller must therefore introduce
    the payer and obligation entities (``entity-introduced`` acts; see
    ``build_ordinary_acquisition_entity_acts``) before asserting the
    circumstance finding this module maps, exactly as box-1 ingestion
    introduces its own payer and statement entities before asserting box 1.
    This bundle can represent any number of payers and any number of
    obligations per payer without a fresh bundle declaration — the closed
    literal enumeration this function previously produced is gone.
    """
    validate_ordinary_answers(answers)
    return {
        "schema": "bundle.v1",
        "id": f"demo.vocabulary.{OBLIGATION_ACQUISITION_FACT_TYPE_ID}",
        "label": "Obligation-acquisition circumstance (ordinary-language)",
        "fact_types": [
            {
                "schema": "fact-type.v1",
                "id": OBLIGATION_ACQUISITION_FACT_TYPE_ID,
                "title": "Ordinary bond-acquisition and accrued-interest circumstance",
                "nature": "determinable",
                "identity_keys": [
                    {"name": "payer", "kind": "entity", "entity_kind": PAYER_ENTITY_KIND},
                    {
                        "name": "obligation",
                        "kind": "entity",
                        "entity_kind": OBLIGATION_ENTITY_KIND,
                    },
                    {
                        "name": "acquisition-year",
                        "kind": "literal",
                        "values": [str(answers["acquisition_date"])[:4]],
                    },
                ],
                "value_schema": _CIRCUMSTANCE_VALUE_SCHEMA,
                "supersession": {"policy": "free"},
            }
        ],
    }


def build_ordinary_acquisition_entity_acts(
    answers: Mapping[str, Any], *, act_index: int
) -> list[dict[str, Any]]:
    """Two ``entity-introduced`` acts: the payer and the obligation.

    Entity introduction is its own act kind, outside the contribution
    batch's successor-carrier acts (``assertion`` / ``member-transition``
    only — ``packages.kernel.contribution.apply_contribution_batch``), so a
    caller applies these acts first, exactly as this repo's box-1 fixtures
    introduce their payer/statement entities before asserting box 1. Skips
    introducing an entity id already known to be current is the caller's
    responsibility (a second acquisition from the same payer must not
    re-introduce that payer's entity) — this helper always names both
    entities for a single answer set; the caller filters duplicates.
    """
    validate_ordinary_answers(answers)
    payer_entity_id = derive_payer_entity_id(answers["payer_name"])
    obligation_entity_id = derive_obligation_entity_id(
        payer_name=answers["payer_name"],
        obligation_reference=answers.get("obligation_reference"),
        obligation_description=answers["obligation_description"],
    )
    payer_act = {
        "schema": "act.v1",
        "act_id": f"demo-act-{act_index:03d}",
        "kind": "entity-introduced",
        "actor": "user",
        "at": f"2026-01-01T00:00:{act_index % 60:02d}Z",
        "committed_against": act_index,
        "payload": {
            "entity": {
                "schema": "entity.v1",
                "id": payer_entity_id,
                "kind": PAYER_ENTITY_KIND,
                "label": f"Payer named in an ordinary acquisition answer: {answers['payer_name']}",
            }
        },
    }
    obligation_act = {
        "schema": "act.v1",
        "act_id": f"demo-act-{act_index + 1:03d}",
        "kind": "entity-introduced",
        "actor": "user",
        "at": f"2026-01-01T00:00:{(act_index + 1) % 60:02d}Z",
        "committed_against": act_index + 1,
        "payload": {
            "entity": {
                "schema": "entity.v1",
                "id": obligation_entity_id,
                "kind": OBLIGATION_ENTITY_KIND,
                "label": f"Obligation named in an ordinary acquisition answer: {answers['obligation_description']}",
            }
        },
    }
    return [payer_act, obligation_act]


def map_ordinary_acquisition_answers(
    answers: Mapping[str, Any],
    *,
    finding_id: str,
    evidence_id: str,
    contribution_id: str,
    fact_id: str | None = None,
    confirmed_report_fact_id: str | None = None,
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

    ``confirmed_report_fact_id``: when the confirming interaction resolved a single
    candidate report (at either tier — coarse or statement-narrowed) and the
    person confirmed it, the caller passes that report's own fact id here so
    the confirmation names the specific report it was made against, not
    merely a bare "yes". This is never derived by this pure-mapping function
    itself (it has no access to the current source facts) — the confirming
    interaction already knows which candidate it showed the person, exactly
    as ``ORDINARY_ANSWERS_SCHEMA``'s ``confirmed_report_match`` docstring
    already describes ("the interaction can name the single candidate").
    Omitted (``None``, the default) whenever there was no candidate to name
    — the key is then left out of ``circumstance_value`` entirely, which the
    adopted vocabulary bundle's ``additionalProperties: false`` schema still
    validates. ``packages.tax.identity_association`` re-checks this recorded
    id against the current sole candidate, at that same tier, at association
    time and refuses (stale) rather than retargeting when they no longer
    match, and refuses just the same, uniformly at both tiers, when no
    target was ever recorded at all: an omitted target is never honored as
    if it were a scoped confirmation.

    **This is why any ``confirmed_report_match: true`` confirmation now
    requires this argument, uniformly at both tiers.** A confirming
    interaction that sets ``answers["confirmed_report_match"]`` to ``True``
    — whether the coarse tier (no ``reported_statement_reference``) or the
    statement-narrowed tier (a ``reported_statement_reference`` present) —
    must always have resolved exactly one candidate report before asking
    the person to confirm it (see ``ORDINARY_ANSWERS_SCHEMA``'s
    ``confirmed_report_match`` docstring); it therefore always has that
    candidate's fact id to pass here. Omitting it is not a smaller,
    differently-scoped confirmation — it is an unscoped confirmation, which
    is never constructible, so this function fails closed
    (``OrdinaryInputError``) instead of building it.
    """
    validate_ordinary_answers(answers)
    if (
        bool(answers.get("confirmed_report_match", False))
        and confirmed_report_fact_id is None
    ):
        raise OrdinaryInputError(
            "ordinary answer set is invalid: a "
            "'confirmed_report_match: true' confirmation, at either tier, "
            "must name the report it confirms — pass "
            "'confirmed_report_fact_id' naming the single candidate the "
            "confirming interaction showed the person "
            "(path: ['confirmed_report_match'])"
        )

    resolved_fact_id = fact_id or derive_obligation_acquisition_fact_id(
        payer_name=answers["payer_name"],
        obligation_reference=answers.get("obligation_reference"),
        obligation_description=answers["obligation_description"],
        acquisition_date=answers["acquisition_date"],
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
        "reported_statement_reference": answers.get("reported_statement_reference"),
        "confirmed_report_match": bool(answers.get("confirmed_report_match", False)),
    }
    if confirmed_report_fact_id is not None:
        circumstance_value["confirmed_report_fact_id"] = confirmed_report_fact_id

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
    confirmed_report_fact_id: str | None = None,
) -> OrdinaryAcquisitionContribution:
    """Build the contribution + assertion acts for one ordinary answer set.

    This does not itself decide admissibility — it only assembles the exact
    act shapes ``apply_contribution_batch`` (the real contribution boundary)
    requires, so a caller can pass them straight through. Kept separate from
    ``map_ordinary_acquisition_answers`` so the pure mapping function has no
    dependency on act envelopes or act numbering. ``confirmed_report_fact_id``
    passes straight through to ``map_ordinary_acquisition_answers`` — see its
    docstring for what it carries.
    """
    finding = map_ordinary_acquisition_answers(
        answers,
        finding_id=finding_id,
        evidence_id=evidence_id,
        contribution_id=contribution_id,
        fact_id=fact_id,
        confirmed_report_fact_id=confirmed_report_fact_id,
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
    confirmed_report_fact_id: str | None = None,
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
    like any other contribution. ``confirmed_report_fact_id`` passes straight
    through — see ``map_ordinary_acquisition_answers``'s docstring.
    """
    built = build_ordinary_acquisition_contribution(
        answers,
        act_index=act_index,
        contribution_id=contribution_id,
        evidence_id=evidence_id,
        finding_id=finding_id,
        committed_against=committed_against,
        fact_id=fact_id,
        confirmed_report_fact_id=confirmed_report_fact_id,
    )
    return apply_contribution_batch(
        state,
        contribution_act=built.contribution_act,
        successor_acts=[built.assertion_act],
        registry=registry,
        record_id=record_id,
        workspace_revision=committed_against,
    )
