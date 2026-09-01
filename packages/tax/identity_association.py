"""Acquisition-to-report identity association (ADR-0068).

Seam 2 of the Document and Ordinary-Fact Translation Vertical. This module
is the dedicated one-sided pairing producer: a new, independently-published
``derived-finding.v2`` record, not a repurposed ``identity_exclusivity``
collision check and not a field on either source fact. The acquisition
names the report it corresponds to.

A matching payer + statement, within the run's own reporting-year scope,
is not, by itself, genuine evidence of same-obligation correspondence: a
real Form 1099-INT statement/account can aggregate interest from *several*
obligations into one box-1 number (there is no general box-1 CUSIP or
per-obligation identifier on the form), so a statement match proves only
*which report* the acquisition's interest was reported through — never, by
itself, that a specific obligation is the one that report's amount
concerns.

**Reporting-year context, not an asked-for tax-year answer.** Which
report-year bucket an acquisition belongs to is a reporting/tax-consequence
judgment, never an ordinary fact Seam 6 asks for (see
``packages.tax.obligation_acquisition_mapping``'s module docstring). Both
join tiers below restrict candidate reports to the run's own
``reporting_year`` (``associate()``'s parameter, sourced from
``run_scope["year"]`` via ``try_publish_on_run`` — never from the
acquisition's own identity or attested value). The acquisition side
carries its own, genuinely different, ``acquisition-year`` identity
component (the acquisition event's own calendar year, read straight off
``acquisition_date``); the report side carries its own real ``tax-year``
identity component. All three — acquisition-year, the report's own
tax-year, and the run's reporting-year context — are distinct and must
never be conflated.

The join is now two-tiered, and **confirmation is mandatory at both
tiers, always** — not a fallback-only requirement:

1. **Statement-narrowed.** When the acquisition supplies a reported
   statement/account reference (Seam 6's optional
   ``reported_statement_reference`` ordinary answer), it resolves —
   through the *same documented convention* Seam 6's
   ``obligation_acquisition_mapping.derive_reported_statement_entity_id``
   and ``packages.tax.report_statement_identity``'s independent report-side
   functions both implement — to a specific box-1 ``statement`` entity.
   Exactly one report bearing that payer/statement, in the reporting-year
   scope, narrows *which*
   report the acquisition's attestation targets; it still requires the
   acquisition's own ``confirmed_report_match: true``, naming that same
   candidate's fact id as ``confirmed_report_fact_id``, to actually
   associate — exactly the same exact-target confirmation the coarse tier
   below requires. Absent or stale confirmation, refuse
   ``ASSOCIATION_UNCONFIRMED``, naming the narrowed candidate. Zero: no
   match (the reference names no known statement in scope); the
   acquisition is left unassociated, silently, exactly like today's
   zero-candidate case.
2. **Coarse.** When no statement reference was given, grouping falls back
   to payer alone, still restricted to the reporting-year scope. Two or
   more candidates: refuse ``ASSOCIATION_AMBIGUOUS``, naming every
   candidate — a missing statement reference cannot resolve *which* one.
   Exactly one candidate still requires the acquisition's explicit,
   separately-answered ``confirmed_report_match`` ordinary fact to be true.
   Absent that confirmation, refuse ``ASSOCIATION_UNCONFIRMED``, naming the
   single candidate. Zero candidates: no match, silently, as before.

**A confirmation at either tier is scoped to the report it named, not to
"whichever report is sole right now".** A bare Boolean is
not enough: a workspace can retire and replace the sole same-payer/year (or
same-payer/statement) report between the confirmation and a later
association attempt, with no new act on the acquisition side, and a
Boolean alone cannot tell the replacement apart from the report it was
actually confirmed against. A contribution built through the current
``obligation_acquisition_mapping.map_ordinary_acquisition_answers`` can
therefore record which report fact id the confirming interaction actually
showed the person, as the acquisition's own
``confirmed_report_fact_id`` (mandatory whenever ``confirmed_report_match``
is true, at either tier — see that function's docstring). When a
confirmation names a target this way, ``associate()`` only honors it while
the *current* sole candidate at that same tier is still that same fact id;
if the sole candidate has changed (the named report was retired/replaced,
or superseded by a different one), the confirmation is treated as stale
and refused as ``ASSOCIATION_UNCONFIRMED`` — the same code as a missing
confirmation, never a new code — rather than silently retargeted onto
whatever candidate happens to be sole now.

**An absent target is not a smaller, unprotected confirmation; it is
refused, always, at either tier.** A confirmation that never named a
target — whether because the confirming interaction had no candidate to
name, or because a caller defaulted the field to ``None`` — carries no
target to go stale against, but that is not license to fall back to
unprotected behavior: treating an absent target as staleness-exempt would
leave the original authority-retargeting defect reachable through any path
that can produce this shape. A confirmation with **no recorded target at
all**, at either tier, is refused ``ASSOCIATION_UNCONFIRMED`` exactly like a
stale one — the same code, the same named candidate — never silently
honored, regardless of provenance.
``packages.tax.obligation_acquisition_mapping``'s mapper makes an untargeted
``true`` confirmation impossible to construct through the real mapping
path (schema ``if``/``then`` plus an explicit mapper-level check), and the
same ``if``/``then`` is declared on the adopted fact type's own
``value_schema`` (``obligation-acquisition.bundle.json``), so the real
kernel admission boundary (``packages.kernel.findings._validate_finding``,
run for every assertion regardless of which caller produced it) refuses
this shape before it can ever enter a workspace's content log — an
untargeted ``true`` confirmation cannot reach production association
through any real contribution path. This module's refusal is defense in
depth for direct, in-process ``SourceFact`` construction or a caller that
invokes ``associate()`` directly, bypassing the kernel admission boundary
entirely (as, for example, this module's own unit tests do) — not handling
for content that was validly admitted some other way.

A canonical statement/account reference is therefore never, by itself,
proof of obligation correspondence at either tier — it only identifies
*which report* a person's explicit, accountable attestation is being made
against, and (when given) narrows ambiguity among several same-payer
statements. The attestation is what selects the specific obligation; the
statement reference only narrows the candidate set the attestation is
checked against.

Grouping is by exact reported-side fact-id count under the declared
identity components, never by a coarser set of identity tuples — that
set-collapse is the defect that sank Candidate A. This still holds at
both tiers above.

The producer is derived, not cached: every call recomputes from the
current marshaled ``SourceFact`` list. A correction, addition, or
removal is visible the next time the same pairing is evaluated; there
is no stored association object to invalidate.

Identity extraction reuses ``declarative_validation.identity_tuple`` /
``extract_component``. Pin sorting and content-addressing reuse
``runner._sorted_pins`` / ``runner._content_id``, the same helpers every
other derived finding in this codebase uses.

``ASSOCIATION_AMBIGUOUS`` and ``ASSOCIATION_UNCONFIRMED`` are named
refusal codes wired into ``runner.RECORD_CODES``.

**ADR-0072 production condition: the legacy/pairing collision trigger.**
A workspace may still hold a live, pre-migration
``tax.us.2025.scheduleb.adjustment.accrued-interest.amount`` finding (the
form-row Schedule B accrued-interest adjustment) for what a person believes
is the *same* real obligation a new acquisition/report pairing is about to
name. Publishing that pairing without checking would let
``rule.form1040-line2b`` v5 double-subtract the same accrued-interest
circumstance under two different fact types. This module's ``associate()``
is the one production call site where a new pairing is about to be
created, so the collision check lives here, not as spike-local code.

**Correlating signal, re-checked against ADR-0068's identity decision
(not kept by inertia):** ADR-0068 gives the acquisition side a genuine
entity-kind obligation identity (``tax.us.interest-obligation``, scoped
under a real payer entity) and a statement-level discriminator. Neither
helps here: the legacy fact type is immutable production content
(``scheduleb-adjustment.accrued-interest.bundle.json``) whose
``identity_keys`` are exactly ``{tax-year, opaque adjustment-instance
entity}`` — no payer, obligation, or report field at all, on the legacy
side, before or after ADR-0068. A better signal needs *both* sides to
carry a shared discriminator; the legacy side still carries none. The
only signal actually present on both sides remains the dollar **amount**:
the legacy finding's attested value against the new pairing's own
``accrued_interest_paid_to_seller`` ordinary answer. This reproduces
``docs/archive/.../prototypes/legacy-pairing-coexistence/spike/trigger.py``'s
finding, re-verified here against the same unmodified legacy bundle.

**Named limits, carried forward, not concealed (ADR-0072 Decision 2 /
Production Conditions):** a false positive (two genuinely different
obligations that happen to share a dollar amount) costs only a forced
one-time resolution, never a silent change — see
``ASSOCIATION_MIGRATION_ADOPTION_REQUIRED`` below. A false negative (the
same obligation entered twice at different amounts, e.g. a typo) is not
detected by this signal and remains a named residual risk, not decided
here.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping, Sequence

from packages.derivation.declarative_validation import (
    IdentityBindingError,
    extract_bound_keys,
    identity_tuple,
)
from packages.derivation.runner import SourceFact, _content_id, _sorted_pins
from packages.kernel.schema_registry import SchemaRegistry
from packages.tax.obligation_acquisition_mapping import (
    OBLIGATION_ACQUISITION_FACT_TYPE_ID,
    derive_reported_statement_entity_id,
)

# ADR-0072: the legacy, pre-migration Schedule B accrued-interest fact type
# and the ordinary answer naming an acquisition's own accrued-interest
# amount. Re-validated against real, unmodified production content
# (``packages/content/tax/2025/scheduleb-adjustment.accrued-interest.bundle.json``,
# ``packages/tax/obligation_acquisition_mapping.py``'s
# ``ORDINARY_ANSWERS_SCHEMA``), not assumed.
LEGACY_ACCRUED_INTEREST_FACT_TYPE = "tax.us.2025.scheduleb.adjustment.accrued-interest.amount"
ACCRUED_INTEREST_ANSWER_FIELD = "accrued_interest_paid_to_seller"

# Production fact-type ids, re-validated against committed content:
# ``packages/content/tax/2025/f1099int.bundle.json`` (box 1) and Seam 6's
# ordinary-acquisition circumstance (``obligation_acquisition_mapping``).
ACQUISITION_FACT_TYPE = OBLIGATION_ACQUISITION_FACT_TYPE_ID
REPORT_FACT_TYPE = "tax.us.2025.f1099int.box1-interest"

# Coarsest identity both sides always support: payer (ADR-0068 Decision 3),
# scoped to the run's own reporting-year context (``reporting_year``,
# sourced from ``run_scope`` -- see ``associate()`` and
# ``try_publish_on_run`` below), never from either side's own fact id. The
# acquisition side no longer carries a "tax-year" identity component at all
# (it carries its own genuine "acquisition-year", the event year -- see
# ``packages.tax.obligation_acquisition_mapping``); the report side's own
# real "tax-year" identity component is unchanged and is what
# ``_reports_in_reporting_year`` filters against. Still used as the
# fallback tier and for naming every ambiguous candidate.
LEFT_COMPONENTS: tuple[dict[str, str], ...] = (
    {"fact_id_bound_key": "payer"},
)
RIGHT_COMPONENTS: tuple[dict[str, str], ...] = (
    {"fact_id_bound_key": "payer"},
)

# The finer identity box 1 already carries on its own fact id: payer +
# statement (also scoped to the run's reporting-year context, the same way
# as the coarse tier above). Grouping reports this way lets a statement-
# confirmed acquisition select one specific report among several
# same-payer statements, rather than only ever refusing ambiguity.
RIGHT_STRICT_COMPONENTS: tuple[dict[str, str], ...] = (
    {"fact_id_bound_key": "payer"},
    {"fact_id_bound_key": "statement"},
)

ASSOCIATION_SYMBOL = "tax.us.2025.identity-association.acquisition-to-box1"
DERIVED_FINDING_SCHEMA = "derived-finding.v2"

ASSOCIATION_AMBIGUOUS = "ASSOCIATION_AMBIGUOUS"
# Refusal: exactly one same-payer/year candidate
# exists (or a statement reference narrows to exactly one candidate), but
# the acquisition's own explicit ``confirmed_report_match`` attestation is
# absent. Distinct from ASSOCIATION_AMBIGUOUS (several candidates, no way to
# pick) — here there is one candidate, but a payer/statement/year match
# alone is never evidence of *obligation* correspondence (a statement can
# aggregate several obligations' interest into one box-1 number); picking
# it without the person's own accountable confirmation is a guess, not a
# derivation. This now fires uniformly at both tiers — a statement match no
# longer bypasses it.
ASSOCIATION_UNCONFIRMED = "ASSOCIATION_UNCONFIRMED"

# ADR-0072 Decision 2/3: a new pairing about to be created against a
# workspace that already holds a live legacy accrued-interest finding at
# the SAME dollar amount is not published silently. Naming every colliding
# legacy finding id, exactly like the other two refusal codes above — this
# is a forced one-time resolution question, never an automatic
# supersession. Resolution is a same-identity correction at the legacy
# fact's own already-declared ``supersession.policy: "free"`` (a second
# ``assertion`` act at the same ``fact_id``); once resolved, the next
# association attempt sees the corrected (non-colliding) amount and
# proceeds normally. This introduces no new displacement-edge kind
# (Article 7 / E7.2 unaffected): the resolution is a generic, existing,
# cross-fact-type-agnostic same-identity correction
# (``packages.kernel.currency._finding_corrections``), not a new edge.
ASSOCIATION_MIGRATION_ADOPTION_REQUIRED = "ASSOCIATION_MIGRATION_ADOPTION_REQUIRED"


@dataclass(frozen=True)
class AssocRefusal:
    """A named refusal. Never accompanied by a published pairing record."""

    code: str
    left_fact_id: str
    candidate_right_fact_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class AssocResult:
    publications: tuple[dict[str, Any], ...]
    refusals: tuple[AssocRefusal, ...]


def _right_by_identity(
    sources: Sequence[SourceFact],
    *,
    name: str,
    components: Sequence[Mapping[str, Any]],
) -> dict[tuple[str, ...], dict[str, SourceFact]]:
    """Group reported-side sources by identity tuple, keyed by fact id.

    The inner mapping is the load-bearing structure: two statements that
    share the same identity tuple under ``components`` (e.g. the same
    ``payer``, at the coarse tier) remain two fact-id entries. A ``set`` of
    tuples would collapse them to one, which is Candidate A's defect.
    """
    groups: dict[tuple[str, ...], dict[str, SourceFact]] = {}
    for source in sources:
        if source.name != name or source.fact_id is None:
            continue
        try:
            tup = identity_tuple(
                fact_id=source.fact_id,
                member_value=None,
                components=components,
            )
        except IdentityBindingError:
            continue
        groups.setdefault(tup, {})[source.fact_id] = source
    return groups


def _reports_in_reporting_year(
    sources: Sequence[SourceFact], *, right_type: str, reporting_year: int | None
) -> list[SourceFact]:
    """Reported-side sources whose own ``tax-year`` identity component
    matches the caller-supplied reporting-year context.

    ``reporting_year`` is sourced from the run's own ``run_scope`` (via
    ``try_publish_on_run``), never from the acquisition's own identity or
    attested value -- picking which report-year bucket an acquisition
    belongs to is a reporting/tax-consequence judgment, not an ordinary
    fact the acquisition side is ever asked to supply (see
    ``packages.tax.obligation_acquisition_mapping``'s module docstring).
    ``reporting_year is None`` means no reporting-year context was
    available at all: the honest result is the same as any other
    zero-candidate case below -- no report is ever in scope, so every
    acquisition silently fails to associate, exactly like today's ordinary
    "no match" outcome, never a guess and never a new refusal code.
    """
    if reporting_year is None:
        return []
    target = str(reporting_year)
    in_scope: list[SourceFact] = []
    for source in sources:
        if source.name != right_type or source.fact_id is None:
            continue
        try:
            bound = extract_bound_keys(source.fact_id)
        except IdentityBindingError:
            continue
        if bound.get("tax-year") == target:
            in_scope.append(source)
    return in_scope


def _decoded_value(source: SourceFact) -> Mapping[str, Any]:
    """Best-effort decode of a marshaled ``SourceFact.value``.

    Acquisition circumstance values are always JSON-encoded objects
    (``_encode_source_value`` / ``marshal.py`` both render dict-valued
    findings as JSON text). A source that fails to decode as an object
    carries no statement reference or confirmation, which is treated the
    same as an acquisition that simply omitted those optional ordinary
    answers — never an error.
    """
    try:
        decoded = json.loads(source.value)
    except (TypeError, ValueError):
        return {}
    return decoded if isinstance(decoded, Mapping) else {}


def _acquisition_statement_entity_id(left: SourceFact) -> str | None:
    """The box-1 ``statement`` entity id ``left``'s own reference resolves to.

    ``None`` when the acquisition supplied no ``reported_statement_reference``
    (the ordinary answer is optional) or its own payer bound key cannot be
    read (malformed fact id — the coarse tier below will also fail closed
    for the same acquisition).
    """
    assert left.fact_id is not None
    bound = extract_bound_keys(left.fact_id)
    payer_entity_id = bound.get("payer")
    if payer_entity_id is None:
        return None
    reference = _decoded_value(left).get("reported_statement_reference")
    if not isinstance(reference, str) or not reference:
        return None
    return derive_reported_statement_entity_id(
        payer_name=payer_entity_id, reported_statement_reference=reference
    )


def _acquisition_confirmed_report_match(left: SourceFact) -> bool:
    return bool(_decoded_value(left).get("confirmed_report_match", False))


def _acquisition_confirmed_report_fact_id(left: SourceFact) -> str | None:
    """The report fact id ``left``'s confirmation names, at either tier, if any.

    ``None`` covers
    two distinct, deliberately-unified cases: the confirming interaction had
    no candidate to name (there was no sole candidate at that tier at
    contribution time), and a caller omitted the field entirely — a shape
    the real mapper and the adopted fact type's own ``value_schema`` both
    refuse to construct or admit (see ``map_ordinary_acquisition_answers``'s
    docstring), reachable here only through direct, in-process construction
    that bypasses kernel admission. ``associate()`` below refuses
    ``ASSOCIATION_UNCONFIRMED`` in *both* of those cases, exactly as it does
    for a stale (mismatched) target — an absent target is never honored as
    an unscoped-but-valid confirmation, regardless of provenance.
    """
    value = _decoded_value(left).get("confirmed_report_fact_id")
    return value if isinstance(value, str) and value else None


def _acquisition_accrued_amount(left: SourceFact) -> Decimal | None:
    """The acquisition's own attested accrued-interest-paid-to-seller amount.

    ``None`` when the ordinary answer is absent or not a real number —
    both cases mean the collision trigger below has nothing to compare and
    must not fire (a missing amount is not evidence of a collision).
    """
    value = _decoded_value(left).get(ACCRUED_INTEREST_ANSWER_FIELD)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    try:
        return Decimal(str(value))
    except InvalidOperation:
        return None


def _live_legacy_collision_fact_ids(
    legacy_sources: Sequence[SourceFact], *, amount: Decimal
) -> tuple[str, ...]:
    """Currently-marshaled legacy findings whose amount exactly matches.

    ``legacy_sources`` is already currency-filtered: ``marshal.py`` only
    ever collects *current* findings (``currency.current_finding_ids``), so
    a legacy finding already superseded by a same-fact-id "free"-policy
    correction (the resolution this trigger asks for) is not seen here —
    the collision clears itself the run after resolution, with no
    additional code path.
    """
    colliding: list[str] = []
    for source in legacy_sources:
        if source.fact_id is None:
            continue
        try:
            legacy_amount = Decimal(str(source.value))
        except InvalidOperation:
            continue
        if legacy_amount == amount:
            colliding.append(source.fact_id)
    return tuple(sorted(colliding))


def _pairing_finding(
    *,
    left: SourceFact,
    right: SourceFact,
    adoption_pin: Mapping[str, Any],
    symbol: str,
    registry: SchemaRegistry,
) -> dict[str, Any]:
    value = {
        "left_fact_id": left.fact_id,
        "right_fact_id": right.fact_id,
    }
    pins = _sorted_pins(
        [
            {
                "role": "input",
                "id": left.finding_id,
                "version": "v1",
                "origin": "assertion",
            },
            {
                "role": "input",
                "id": right.finding_id,
                "version": "v1",
                "origin": "assertion",
            },
            dict(adoption_pin),
        ]
    )
    body = {"symbol": symbol, "value": value, "pins": pins}
    finding = {
        "schema": DERIVED_FINDING_SCHEMA,
        "id": _content_id("finding:derived:", body),
        "symbol": symbol,
        "value": value,
        "version": "v2",
        "pins": pins,
    }
    registry.validate(DERIVED_FINDING_SCHEMA, finding)
    return finding


def associate(
    *,
    sources: Sequence[SourceFact],
    registry: SchemaRegistry,
    adoption_pin: Mapping[str, Any],
    reporting_year: int | None = None,
    left_type: str = ACQUISITION_FACT_TYPE,
    right_type: str = REPORT_FACT_TYPE,
    left_components: Sequence[Mapping[str, Any]] | None = None,
    right_components: Sequence[Mapping[str, Any]] | None = None,
    right_strict_components: Sequence[Mapping[str, Any]] | None = None,
) -> AssocResult:
    """Publish one-sided pairing records from current marshaled sources.

    One-sided from the acquisition (``left_type``): each current
    acquisition independently names the report it corresponds to, or
    refuses. Recomputed from ``sources`` every call.

    ``reporting_year``: the run's own reporting-year context, sourced from
    ``run_scope`` (see ``try_publish_on_run``), never from the
    acquisition's own identity or attested value. It selects which
    reports are in scope for *both* tiers' join below (``right_type``
    sources whose own real ``tax-year`` identity component matches it --
    see ``_reports_in_reporting_year``). It is a genuinely different
    concept from the acquisition's own ``acquisition-year`` identity
    component (the acquisition event's own calendar year) and from the
    report's own ``tax-year`` identity component (the report's own real,
    attributed contribution) -- the three must never be conflated.
    ``reporting_year is None`` means no report is ever in scope: every
    acquisition then silently fails to associate, the same honest
    zero-candidate result as any other case below, never a guess and
    never a new refusal code.

    Two-tiered join. Confirmation is
    mandatory at both tiers, always, never a fallback-only requirement:

    1. If the acquisition supplies a reported statement reference, it is
       resolved to a specific box-1 ``statement`` entity and matched
       against the strict (payer, statement) grouping, itself restricted
       to reports in the ``reporting_year`` scope. Exactly
       one candidate narrows *which* report the attestation targets, but
       still requires the acquisition's own ``confirmed_report_match``
       ordinary fact to be true to associate — a statement match is not,
       by itself, evidence of *obligation* correspondence, since one
       statement can aggregate several obligations' interest. Absent
       confirmation, refuse ``ASSOCIATION_UNCONFIRMED``, naming the
       narrowed candidate. Zero: silently no match (the reference names no
       known statement in scope).
    2. Otherwise, fall back to the coarse payer grouping, restricted the
       same way to reports in the ``reporting_year`` scope. Two
       or more candidates: refuse ``ASSOCIATION_AMBIGUOUS``, naming every
       candidate — never resolvable by a coarser-tier confirmation. Exactly
       one candidate: associate only if the acquisition's own
       ``confirmed_report_match`` ordinary fact is true; otherwise refuse
       ``ASSOCIATION_UNCONFIRMED``, naming the single candidate. Zero:
       silently no match.
    """
    left_comps = left_components if left_components is not None else LEFT_COMPONENTS
    right_comps = (
        right_components if right_components is not None else RIGHT_COMPONENTS
    )
    right_strict_comps = (
        right_strict_components
        if right_strict_components is not None
        else RIGHT_STRICT_COMPONENTS
    )
    right_sources_in_scope = _reports_in_reporting_year(
        sources, right_type=right_type, reporting_year=reporting_year
    )
    right_groups = _right_by_identity(
        right_sources_in_scope, name=right_type, components=right_comps
    )
    right_groups_strict = _right_by_identity(
        right_sources_in_scope, name=right_type, components=right_strict_comps
    )
    legacy_sources = [s for s in sources if s.name == LEGACY_ACCRUED_INTEREST_FACT_TYPE]

    publications: list[dict[str, Any]] = []
    refusals: list[AssocRefusal] = []

    left_sources = [s for s in sources if s.name == left_type and s.fact_id is not None]
    left_sources.sort(key=lambda s: s.fact_id or "")

    def _publish_or_refuse_collision(left: SourceFact, right: SourceFact) -> None:
        """Publish the pairing, unless it collides with live legacy content.

        ADR-0072: checked immediately before a new pairing would actually be
        created (report already selected, one way or another) — never
        before, since an acquisition that would end up unassociated anyway
        creates no new pairing and has nothing to force a resolution about.
        """
        assert left.fact_id is not None
        accrued_amount = _acquisition_accrued_amount(left)
        if accrued_amount is not None:
            colliding = _live_legacy_collision_fact_ids(
                legacy_sources, amount=accrued_amount
            )
            if colliding:
                refusals.append(
                    AssocRefusal(
                        ASSOCIATION_MIGRATION_ADOPTION_REQUIRED,
                        left.fact_id,
                        colliding,
                    )
                )
                return
        symbol = f"{ASSOCIATION_SYMBOL}|{left.fact_id}"
        publications.append(
            _pairing_finding(
                left=left,
                right=right,
                adoption_pin=adoption_pin,
                symbol=symbol,
                registry=registry,
            )
        )

    for left in left_sources:
        assert left.fact_id is not None  # filtered above

        statement_entity_id = _acquisition_statement_entity_id(left)
        if statement_entity_id is not None:
            try:
                left_payer = extract_bound_keys(left.fact_id)["payer"]
            except KeyError:
                continue
            # No acquisition-side year component enters this tuple: the
            # right-hand groups are already restricted to reports in the
            # run's own ``reporting_year`` scope (see
            # ``_reports_in_reporting_year`` above), never matched against
            # the acquisition's own ``acquisition-year`` identity.
            strict_tuple = (left_payer, statement_entity_id)
            strict_candidates = right_groups_strict.get(strict_tuple, {})
            if len(strict_candidates) == 0:
                continue
            if len(strict_candidates) > 1:
                refusals.append(
                    AssocRefusal(
                        ASSOCIATION_AMBIGUOUS,
                        left.fact_id,
                        tuple(sorted(strict_candidates)),
                    )
                )
                continue
            # A matching statement/account only narrows *which* report
            # the acquisition's attestation is being made against. A Form
            # 1099-INT statement/account can aggregate interest from several
            # obligations into one box-1 number, so the statement match by
            # itself is not evidence that this specific obligation is the
            # one that report's amount concerns — the person's own,
            # separately-answered ``confirmed_report_match`` is required
            # here too, exactly as the coarse tier below already requires
            # it. A statement match never auto-associates without
            # confirmation. Confirmation is also scoped to the report it
            # named, exactly like the coarse tier below: a bare Boolean is
            # not enough, since a workspace can retire and replace the sole
            # strict-tier candidate between the confirmation and a later
            # association attempt. A confirmation that never recorded a
            # target, or whose recorded target no longer matches the
            # current sole strict-tier candidate, is refused
            # ``ASSOCIATION_UNCONFIRMED`` exactly like a missing
            # confirmation — never silently retargeted onto whatever
            # candidate happens to be sole now. See
            # ``_acquisition_confirmed_report_fact_id``.
            (only_fact_id,) = tuple(strict_candidates)
            recorded_fact_id = _acquisition_confirmed_report_fact_id(left)
            if not _acquisition_confirmed_report_match(left) or (
                recorded_fact_id is None or recorded_fact_id != only_fact_id
            ):
                refusals.append(
                    AssocRefusal(
                        ASSOCIATION_UNCONFIRMED,
                        left.fact_id,
                        (only_fact_id,),
                    )
                )
                continue
            right = next(iter(strict_candidates.values()))
            _publish_or_refuse_collision(left, right)
            continue

        try:
            left_tuple = identity_tuple(
                fact_id=left.fact_id,
                member_value=None,
                components=left_comps,
            )
        except IdentityBindingError:
            continue
        candidates = right_groups.get(left_tuple, {})
        if len(candidates) == 0:
            continue
        if len(candidates) > 1:
            refusals.append(
                AssocRefusal(
                    ASSOCIATION_AMBIGUOUS,
                    left.fact_id,
                    tuple(sorted(candidates)),
                )
            )
            continue
        (only_fact_id,) = tuple(candidates)
        if not _acquisition_confirmed_report_match(left):
            refusals.append(
                AssocRefusal(
                    ASSOCIATION_UNCONFIRMED,
                    left.fact_id,
                    (only_fact_id,),
                )
            )
            continue
        # A confirmation that named its target report (``confirmed_report_
        # fact_id``, see ``map_ordinary_acquisition_answers``) is only
        # honored while the current sole coarse-tier candidate is still
        # that same report. A report retirement/replacement changes which
        # fact id is sole here with no new act on the acquisition side; the
        # stored confirmation must go stale, not silently retarget onto
        # whatever candidate is sole now. Refuses with the same
        # ASSOCIATION_UNCONFIRMED code as a missing confirmation — a stale
        # confirmation is not evidence of correspondence to the new
        # candidate either. A confirmation that never recorded a target at
        # all — reachable only through direct, in-process construction that
        # bypasses kernel admission, since the real mapper and the adopted
        # fact type's own value_schema both refuse this shape — is refused
        # the same way, not honored: an absent target is treated as
        # maximally stale, never as an unscoped-but-valid confirmation. See
        # ``_acquisition_confirmed_report_fact_id``.
        recorded_fact_id = _acquisition_confirmed_report_fact_id(left)
        if recorded_fact_id is None or recorded_fact_id != only_fact_id:
            refusals.append(
                AssocRefusal(
                    ASSOCIATION_UNCONFIRMED,
                    left.fact_id,
                    (only_fact_id,),
                )
            )
            continue
        right = next(iter(candidates.values()))
        _publish_or_refuse_collision(left, right)

    return AssocResult(
        publications=tuple(publications),
        refusals=tuple(refusals),
    )


def collect_source_names() -> tuple[str, ...]:
    """Fact-type names marshal must collect for association to see both sides.

    Includes the legacy accrued-interest fact type (ADR-0072): the
    collision trigger inside ``associate()`` needs to see any currently
    live legacy finding, or it would silently never fire — a package that
    never wired this collection would leave a genuine same-amount legacy/
    pairing collision undetected and silently double-subtracted.
    """
    return (ACQUISITION_FACT_TYPE, REPORT_FACT_TYPE, LEGACY_ACCRUED_INTEREST_FACT_TYPE)


def try_publish_on_run(run: Any) -> None:
    """Derive pairing records onto this run from current live sources.

    Isolation tests that already marshaled pairing findings keep those
    records; association does not double-publish on top of them. A composed
    run with only acquisition and report sources (the production shape)
    derives pairings here, once, before pairing-scoped rules dispatch.

    ``reporting_year`` is read off ``run.ctx.reporting_year`` -- the run's
    own reporting-year context, threaded from ``run_scope["year"]``
    through ``packages.derivation.live.live_coordinate_run`` ->
    ``marshal_live_run_context`` -> ``RunContext`` (never asked of, or
    derived from, the acquisition side). ``getattr`` defaults to ``None``
    for fixture/test ``RunContext`` instances built before this field
    existed; ``None`` is itself a legitimate, honest "no reporting-year
    context" value (see ``associate()``'s docstring), not a bug to work
    around.
    """
    live = getattr(run, "live_sources", run.ctx.sources)
    if any(source.name == ASSOCIATION_SYMBOL for source in live):
        return
    if not any(source.name == ACQUISITION_FACT_TYPE for source in live):
        return
    result = associate(
        sources=live,
        registry=run.schemas.registry,
        adoption_pin=run.ctx.adoption_pin,
        reporting_year=getattr(run.ctx, "reporting_year", None),
    )
    run.absorb_association_result(result)
