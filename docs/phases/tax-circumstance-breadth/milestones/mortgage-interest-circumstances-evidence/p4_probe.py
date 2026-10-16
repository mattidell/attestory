"""P4 design-repair probe: build the P4-repaired successor arrangement in a
temporary registry and run it through ``live_coordinate_run`` and the real
presentation model, per P2/P3's throwaway-surface technique. Nothing here is
adopted; nothing is written into ``packages/content``.

This probe answers the charter's eight numbered items (``charter-p4-design-
repair.md``, action 8), by building exactly the arrangement
``p3-connected-design.md`` now specifies after the P4 repair:

1. the condition table's priority order, including the two new conditions
   (not-collateral, not-paid) read as decisive, and the new owner-not-on-note
   gate (choice 1's repair);
2. the two ordinary timing questions, asked only when the money did not buy
   the home, and their mapping to a conclusion (choice 3's repair) --
   including that they are safely *not* in ``requires``, so a purchase
   statement is never blocked by an unasked timing question;
3. the personal-expense zero computed without a grandfathering check
   (choice 3's deferred date prerequisite -- the boundary chosen, not the
   capability itself, which this probe does not build);
4. that each conclusion symbol still has exactly one producer (one rule,
   internal branches), and that two independently decisive adverse facts
   true at once still publish exactly one conclusion, by construction;
5. the reader gap this repair could not close with existing code: the
   "unresolved" field's single-favorable-value assumption
   (``presentation_projection._favorable_values``), reproduced live against
   the real, unmodified module, not argued;
6. the box 9 default under the production package-level arrangement
   (``input_bindings``), re-run against the revised rules;
7. the owner who paid without being on the note, now outside coverage
   instead of supported.

The recording operation (choice 10) is specified in ``p3-connected-design.md``
and is not built here. Every case below still uses direct synthetic
assertions, not the recording operation's save/correct/withdraw contract --
named as a remaining stand-in in the report below.

Run from the repository root:

    python3 docs/phases/tax-circumstance-breadth/milestones/mortgage-interest-circumstances-evidence/p4_probe.py
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.presentation_projection import PresentationModelError, build_presentation_model

_P0_PATH = Path(__file__).with_name("p0_current_path.py")
_P0_SPEC = importlib.util.spec_from_file_location("p0_current_path", _P0_PATH)
assert _P0_SPEC is not None and _P0_SPEC.loader is not None
p0 = importlib.util.module_from_spec(_P0_SPEC)
_P0_SPEC.loader.exec_module(p0)

from tests.test_f1098_mortgage_interest_line12e_track2 import (  # noqa: E402
    _attested,
    _load,
    _member_fact_id,
)

CONTENT = p0.CONTENT
PACKAGE_PATH = p0.PACKAGE_PATH
REGISTRY_PATH = p0.REGISTRY_PATH
RELEASE_PATH = p0.RELEASE_PATH
SCOPE = p0.SCOPE
USER = p0.USER
LINE8A_SYMBOL = "tax.us.2025.schedule-a.line8a"

FACT = "tax.us.2025.f1098."
BOX1 = FACT + "box1-mortgage-interest"
BOX2 = FACT + "box2-outstanding-principal"
BOX3 = FACT + "box3-origination-date"
BOX9 = FACT + "box9-number-of-properties"
REASON = FACT + "residence-interest-reason"
INERT = FACT + "inert-path-unwritten"
UNRESOLVED_SYMBOL = FACT + "residence-interest-unresolved"
LIMIT_PARAM = "tax.us.2025.f1098.mortgage-interest-limit"
BOX9_DEFAULT_PARAM = "tax.us.2025.parameter.f1098-box9-default-single-property"
# Structural defaults for the two timing facts (see the design note at
# ``_bundle``'s timing fact types): never read by a subject whose use isn't
# unrelated-personal-expense, needed only so a subject-scoped rule's
# exhaustive join set resolves for every subject.
TIMING_PURCHASE_DEFAULT_PARAM = "tax.us.2025.parameter.f1098-timing-purchase-structural-default"
TIMING_BUILDING_DEFAULT_PARAM = "tax.us.2025.parameter.f1098-timing-building-structural-default"

# The seven always-asked ordinary statements (choice 1). ``owes-the-loan`` is
# now a gate (P4 repair, choice 1), not informational-only.
NEW_YES_NO_FACTS = tuple(
    FACT + short
    for short in (
        "owns-the-home",
        "lives-there-most-of-the-time",
        "home-is-collateral",
        "owes-the-loan",
        "paid-the-interest",
        "no-one-else-owes-it",
        "this-is-the-original-loan",
    )
)
WHAT_FOR = FACT + "what-the-money-paid-for"
CERT = FACT + "mortgage-credit-certificate-received"

# The two new ordinary timing questions (choice 3, P4 repair). Deliberately
# *not* in any rule's ``requires`` -- see ``_reason_rule`` and ``_line8a_rule``
# for why that is safe here, unlike the retrospective's cross-pass hazard.
TIMING_PURCHASE = FACT + "loan-timing-relative-to-purchase"
TIMING_BUILDING = FACT + "loan-timing-relative-to-building-or-improving"

# The eleven reason categories after the P4 repair (was eight in P3).
REASON_VALUES = (
    "qualified",
    "not-collateral",
    "not-paid",
    "owner-not-on-note",
    "use-unrelated-personal-expense",
    "timing-exception-possible",
    "cannot-tell-timing",
    "cannot-tell-use",
    "certificate-received",
    "debt-limit-over",
    "outside-coverage",
)
# The condition table's "determined" conclusions (choice 8/9): the only
# categories a completed conclusion, not an open question, names. Everything
# else is unresolved or unsupported.
DETERMINED_REASONS = frozenset({
    "qualified", "not-collateral", "not-paid", "use-unrelated-personal-expense",
})
REASON_DESCRIPTIONS = {
    "qualified": "The interest qualifies as home mortgage interest for this statement.",
    "not-collateral": "The home is not collateral for this loan, so the debt is not secured acquisition indebtedness.",
    "not-paid": "The person said they do not owe this loan or did not pay this interest, so there is no deduction to publish for this statement.",
    "owner-not-on-note": "The person paid this interest but is not on the note. Treas. Reg. section 1.163-1(b) may still allow the deduction for an equitable owner, but this route does not compute a non-obligor's deduction. The treatment is left with the person.",
    "use-unrelated-personal-expense": "The borrowed money paid for a personal expense that was not buying, building, or improving the home, so this interest is not qualified residence interest. This route does not check whether the debt is grandfathered pre-October-13-1987 debt, which would be deductible regardless of use; that check is a named, deferred limitation.",
    "timing-exception-possible": "You took out this loan within 90 days of buying the home, or were building or improving it around that time. Publication 936's 90-day and building exceptions may still make this acquisition debt. This route does not compute that exception. The treatment is left with the person.",
    "cannot-tell-timing": "You said you cannot tell whether this loan was taken out within 90 days of buying the home, or whether you were building or improving it around that time. The application cannot reach a conclusion about this interest until that is known.",
    "cannot-tell-use": "You said you cannot tell what the borrowed money paid for. The application cannot reach a conclusion about this interest until that is known.",
    "certificate-received": "A mortgage credit certificate was reported for this loan. The reduced amount is left with the person; this route does not compute Form 8396.",
    "debt-limit-over": "The outstanding principal on this statement is over the limit this route uses. The prorated amount is left with the person.",
    "outside-coverage": "This statement's circumstances are outside what this route computes. The treatment is left with the person.",
}


def _identity_keys() -> list[dict[str, Any]]:
    return [
        {"name": "payer", "kind": "entity", "entity_kind": "tax.us.mortgage-lender"},
        {"name": "statement", "kind": "entity", "entity_kind": "tax.us.1098-statement"},
        {"name": "tax-year", "kind": "literal", "values": ["2025"]},
    ]


def _enum_fact(fact_id: str, title: str, values: tuple[str, ...]) -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": fact_id,
        "version": "v1",
        "title": title,
        "nature": "determinable",
        "identity_keys": _identity_keys(),
        "value_schema": {"enum": list(values)},
        "supersession": {"policy": "free"},
    }


def _bundle() -> dict[str, Any]:
    fact_types = [
        _enum_fact(fact_id, f"P4 probe ordinary statement: {fact_id.rsplit('.', 1)[-1]}", ("yes", "no", "cannot-tell"))
        for fact_id in NEW_YES_NO_FACTS
    ]
    fact_types.append(_enum_fact(
        WHAT_FOR, "P4 probe ordinary statement: what the money paid for",
        ("bought-the-home", "unrelated-personal-expense", "other", "cannot-tell"),
    ))
    fact_types.append(_enum_fact(
        CERT, "P4 probe ordinary statement: mortgage credit certificate (polarity-safe, P3 finding 7)",
        ("received", "not-received", "cannot-tell"),
    ))
    # The two new ordinary timing questions (choice 3, P4 repair), asked only
    # when use is unrelated-personal-expense. Both carry an
    # ``optional_default`` -- a *structural* default, not a box9-style
    # real-world one (see ``TIMING_DEFAULT_PARAMS`` and the design note it
    # points to): a subject-scoped rule's ``requires`` is its exhaustive join
    # set (``packages/derivation/subject_dispatch.py``), so a fact a
    # not-personal-expense subject was never asked still has to resolve to
    # *something* for that subject to join at all. The default value is
    # never read by any subject whose use isn't unrelated-personal-expense,
    # because the value tree's own use-gate is checked first.
    timing_purchase = _enum_fact(
        TIMING_PURCHASE,
        "P4 probe ordinary statement: how long after buying the home this loan was taken out",
        ("within-90-days", "more-than-90-days", "cannot-tell"),
    )
    timing_purchase["optional_default"] = {"parameter": {"id": TIMING_PURCHASE_DEFAULT_PARAM, "version": "v1"}}
    fact_types.append(timing_purchase)
    timing_building = _enum_fact(
        TIMING_BUILDING,
        "P4 probe ordinary statement: building or making major improvements around this loan",
        ("yes-shortly-before-or-after", "no", "cannot-tell"),
    )
    timing_building["optional_default"] = {"parameter": {"id": TIMING_BUILDING_DEFAULT_PARAM, "version": "v1"}}
    fact_types.append(timing_building)
    fact_types.append({
        "schema": "fact-type.v2",
        "id": BOX9,
        "version": "v1",
        "title": "Form 1098 box9-number-of-properties (P3/P4 probe successor: absent is one property)",
        "nature": "determinable",
        "identity_keys": _identity_keys(),
        "value_schema": {"type": "number"},
        "supersession": {"policy": "free"},
        "optional_default": {"parameter": {"id": BOX9_DEFAULT_PARAM, "version": "v1"}},
    })
    fact_types.append({
        "schema": "fact-type.v2",
        "id": REASON,
        "version": "v1",
        "title": "P4 probe: the one reason this statement's interest is or is not qualified residence interest",
        "nature": "determinable",
        "identity_keys": _identity_keys(),
        "value_schema": {
            "enum": list(REASON_VALUES),
            "oneOf": [{"const": value, "description": REASON_DESCRIPTIONS[value]} for value in REASON_VALUES],
        },
        "supersession": {"policy": "free"},
    })
    fact_types.append({
        "schema": "fact-type.v2",
        "id": INERT,
        "version": "v1",
        "title": "Named by the unresolved-field's inert second selection path. Nothing writes it.",
        "nature": "determinable",
        "identity_keys": [{"name": "marker", "kind": "literal", "values": ["unused"]}],
        "value_schema": {"type": "string", "enum": ["unused"], "oneOf": [{"const": "unused", "description": "This value is never written."}]},
        "supersession": {"policy": "free"},
    })
    return {
        "schema": "bundle.v2",
        "id": "tax.us.2025.f1098-successor.vocabulary",
        "version": "v2",
        "label": "P4 probe: respecified Form 1098 ordinary statements and reason",
        "fact_types": fact_types,
    }


def _box9_default_parameter() -> dict[str, Any]:
    return {
        "schema": "parameter-declaration.v1",
        "id": BOX9_DEFAULT_PARAM,
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax", "effective_from": "2025-01-01"},
        "values": 1,
    }


def _timing_default_parameter(param_id: str, value: str) -> dict[str, Any]:
    return {
        "schema": "parameter-declaration.v1",
        "id": param_id,
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax", "effective_from": "2025-01-01"},
        "values": value,
    }


def _ref(name: str) -> dict[str, Any]:
    return {"op": "ref", "name": name}


def _cat_eq(name: str, value: str) -> dict[str, Any]:
    return {
        "op": "categorical_compare", "cmp": "eq", "left": _ref(name),
        "right": {"op": "category_literal", "fact_type": {"id": name, "version": "v1"}, "value": value},
    }


def _reason_lit(value: str) -> dict[str, Any]:
    return {"op": "category_literal", "fact_type": {"id": REASON, "version": "v1"}, "value": value}


def _choose(when: Any, then: Any, otherwise: Any) -> dict[str, Any]:
    return {"op": "choose", "when": when, "then": then, "else": otherwise}


def _limit_ref() -> dict[str, Any]:
    return {"op": "parameter", "parameter_id": LIMIT_PARAM, "key": _ref("filing_status")}


def _qualified_conjunction() -> dict[str, Any]:
    """Choice 1's repair: ``owes-the-loan`` is now a gate on the supported arm."""
    return {
        "op": "all",
        "args": [
            _cat_eq(FACT + "owns-the-home", "yes"),
            _cat_eq(FACT + "lives-there-most-of-the-time", "yes"),
            _cat_eq(FACT + "home-is-collateral", "yes"),
            _cat_eq(FACT + "owes-the-loan", "yes"),
            _cat_eq(FACT + "paid-the-interest", "yes"),
            _cat_eq(FACT + "no-one-else-owes-it", "yes"),
            _cat_eq(WHAT_FOR, "bought-the-home"),
            _cat_eq(FACT + "this-is-the-original-loan", "yes"),
            _cat_eq(CERT, "not-received"),
            {"op": "compare", "cmp": "eq", "left": _ref(BOX9), "right": 1},
        ],
    }


def _personal_expense_timing_branch(zero_value: Any, reclassify_or_unresolved_only: bool) -> dict[str, Any]:
    """Choice 3's two ordinary timing questions, read only inside this branch.

    Deliberately omitted from ``requires``: a person who answered
    ``bought-the-home`` never reaches this branch, so ``ref`` on
    ``TIMING_PURCHASE``/``TIMING_BUILDING`` is never evaluated for them, and
    they are never blocked by a question they were never asked. This differs
    from the retrospective's "conditional dependency" hazard, which concerns
    a *derived* symbol another rule might publish on a later saturation
    pass; these two facts are leaf, person-supplied answers with no producer
    to wait for, so there is no cross-pass race to omit them into.

    ``zero_value`` is what each of the two branches (REASON's literal, or
    line8a's literal ``0``) returns once timing clears the exception. For
    the REASON rule, ``reclassify_or_unresolved_only`` is ignored (REASON
    always resolves to a specific category). For the line8a rule, the
    caller instead supplies the *next* step in its own value tree as
    ``zero_value`` so both rules share this one function.
    """
    within_90 = _cat_eq(TIMING_PURCHASE, "within-90-days")
    building = _cat_eq(TIMING_BUILDING, "yes-shortly-before-or-after")
    timing_cannot_tell = {
        "op": "any",
        "args": [_cat_eq(TIMING_PURCHASE, "cannot-tell"), _cat_eq(TIMING_BUILDING, "cannot-tell")],
    }
    return _choose(
        within_90, _reason_lit("timing-exception-possible") if reclassify_or_unresolved_only else zero_value[0],
        _choose(
            building, _reason_lit("timing-exception-possible") if reclassify_or_unresolved_only else zero_value[0],
            _choose(
                timing_cannot_tell, _reason_lit("cannot-tell-timing") if reclassify_or_unresolved_only else zero_value[1],
                zero_value[2],
            ),
        ),
    )


def _reason_value_tree() -> dict[str, Any]:
    """Choice 9's priority order, as one nested ``choose`` in one rule
    (choice 8/action 4: one rule per symbol, internal branches, so no
    double-match hazard can arise by construction):

    1. not-collateral (decisive regardless of use, refinance, or
       grandfathering -- Section 163(h)(3)(B)(i)(II))
    2. not-paid (decisive -- Treas. Reg. 1.163-1(b) requires the taxpayer
       claiming the deduction to have paid it)
    3. owner-not-on-note (choice 1 repair: paid but does not owe the loan --
       outside coverage, not a zero; Treas. Reg. 1.163-1(b) may still allow
       an equitable owner's deduction this route does not compute)
    4. personal-expense use, gated by the two timing questions (choice 3),
       then by original-loan and box9
    5. cannot-tell on use
    6. certificate received
    7. debt limit over
    8. the full qualified conjunction (including the new owes-the-loan
       gate), then the box 2 compare
    9. outside coverage (the residual)

    Both timing facts carry an ``optional_default`` (see ``_bundle``) rather
    than appearing conditionally in ``requires``: REASON is a subject-scoped
    rule (ADR 0077's per-subject dispatch primitive), and
    ``packages/derivation/subject_dispatch.py``'s shared-key join treats
    ``requires`` as the *exhaustive* set of types joined for every subject
    -- a type outside it is never available to any subject, not merely
    "available but possibly absent." A split into two disjoint-guarded
    rules (this corpus's own ``schedule-a-total``/``-closed-empty``
    precedent) was tried first and rejected: it breaks a second, separate
    constraint -- the unresolved field's declared read
    (``reads_subject_results``) requires *exactly one* rule publishing the
    read symbol for the subject type, which two REASON producers violate
    (probed: ``PresentationModelError: declared read ... has no single
    publisher``). The optional-default is a *structural* default, not a
    box9-style real-world one: it is never actually read by a subject whose
    use isn't personal-expense, because the use-gate below is checked
    before the timing branch.
    """
    outside_coverage = _reason_lit("outside-coverage")
    zero_after_timing = _choose(
        {
            "op": "all",
            "args": [
                _cat_eq(FACT + "this-is-the-original-loan", "yes"),
                {"op": "compare", "cmp": "eq", "left": _ref(BOX9), "right": 1},
            ],
        },
        _reason_lit("use-unrelated-personal-expense"),
        outside_coverage,
    )
    personal_expense_branch = _personal_expense_timing_branch(
        (None, None, zero_after_timing), reclassify_or_unresolved_only=True,
    )
    qualified_branch = _choose(
        {"op": "compare", "cmp": "gt", "left": _ref(BOX2), "right": _limit_ref()},
        _reason_lit("debt-limit-over"),
        _reason_lit("qualified"),
    )
    tail = _choose(_qualified_conjunction(), qualified_branch, outside_coverage)
    tail = _choose(_cat_eq(CERT, "received"), _reason_lit("certificate-received"), tail)
    tail = _choose(_cat_eq(WHAT_FOR, "cannot-tell"), _reason_lit("cannot-tell-use"), tail)
    tail = _choose(_cat_eq(WHAT_FOR, "unrelated-personal-expense"), personal_expense_branch, tail)
    tail = _choose(
        {
            "op": "all",
            "args": [_cat_eq(FACT + "owes-the-loan", "no"), _cat_eq(FACT + "paid-the-interest", "yes")],
        },
        _reason_lit("owner-not-on-note"), tail,
    )
    tail = _choose(_cat_eq(FACT + "paid-the-interest", "no"), _reason_lit("not-paid"), tail)
    tail = _choose(_cat_eq(FACT + "home-is-collateral", "no"), _reason_lit("not-collateral"), tail)
    return tail


def _reason_rule() -> dict[str, Any]:
    requires = [*NEW_YES_NO_FACTS, WHAT_FOR, CERT, BOX2, BOX9, TIMING_PURCHASE, TIMING_BUILDING, "filing_status"]
    return {
        "schema": "rule-artifact.v13",
        "id": "tax.us.2025.rule.f1098-residence-interest-reason",
        "version": "v2",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation",
        "subject": {"id": BOX1, "version": "v1"},
        "requires": requires,
        "pins": [{"role": "parameter", "id": LIMIT_PARAM, "version": "v1"}],
        "when": True,
        "value": _reason_value_tree(),
        "publishes": REASON,
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "citations": [],
        "notes": "P4 probe only. Not an adopted rule. See the condition table.",
    }


def _line8a_value_tree() -> dict[str, Any]:
    """Mirrors ``_reason_value_tree``'s priority order and gates, publishing a
    dollar amount or a block instead of a category. The two timing facts and
    the qualified conjunction's ``owes-the-loan`` gate are read in exactly
    the same branches, for exactly the same reason."""
    block = {"op": "block", "code": "DEPENDENCY_ABSENT"}
    qualified_branch = _choose(
        {"op": "compare", "cmp": "gt", "left": _ref(BOX2), "right": _limit_ref()},
        {"op": "block", "code": "VALUE_INVALID"},
        {"op": "add", "args": [{"op": "collect", "name": BOX1, "source_set": "tax.us.2025.f1098"}]},
    )
    tail = _choose(_qualified_conjunction(), qualified_branch, block)
    tail = _choose(_cat_eq(CERT, "received"), block, tail)
    tail = _choose(_cat_eq(WHAT_FOR, "cannot-tell"), block, tail)
    zero_after_timing = _choose(
        {
            "op": "all",
            "args": [
                _cat_eq(FACT + "this-is-the-original-loan", "yes"),
                {"op": "compare", "cmp": "eq", "left": _ref(BOX9), "right": 1},
            ],
        },
        0, block,
    )
    personal_expense_branch = _personal_expense_timing_branch(
        (block, block, zero_after_timing), reclassify_or_unresolved_only=False,
    )
    tail = _choose(_cat_eq(WHAT_FOR, "unrelated-personal-expense"), personal_expense_branch, tail)
    tail = _choose(
        {
            "op": "all",
            "args": [_cat_eq(FACT + "owes-the-loan", "no"), _cat_eq(FACT + "paid-the-interest", "yes")],
        },
        block, tail,
    )
    tail = _choose(_cat_eq(FACT + "paid-the-interest", "no"), 0, tail)
    tail = _choose(_cat_eq(FACT + "home-is-collateral", "no"), 0, tail)
    return tail


def _line8a_rule(rule_id: str) -> dict[str, Any]:
    requires = [BOX9, BOX2, BOX3, "filing_status", *NEW_YES_NO_FACTS, WHAT_FOR, CERT, TIMING_PURCHASE, TIMING_BUILDING]
    when = {
        "op": "all",
        "args": [
            {"op": "require_closed", "source_set": "tax.us.2025.f1098"},
            _choose(
                {"op": "compare", "cmp": "gt", "left": {"op": "count", "name": BOX1, "source_set": "tax.us.2025.f1098"}, "right": 1},
                {"op": "block", "code": "MULTIPLE_F1098_OUT_OF_SCOPE"},
                {"op": "compare", "cmp": "eq", "left": {"op": "count", "name": BOX1, "source_set": "tax.us.2025.f1098"}, "right": 1},
            ),
        ],
    }
    return {
        "schema": "rule-artifact.v13",
        "id": rule_id,
        "version": "v2",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation",
        "requires": requires,
        "pins": [{"role": "parameter", "id": LIMIT_PARAM, "version": "v1"}],
        "when": when,
        "value": _line8a_value_tree(),
        "publishes": LINE8A_SYMBOL,
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "citations": [],
        "composition": {"id": "tax.us.2025.schedule-a", "version": "v1"},
        "notes": "P4 probe only.",
    }


def _unresolved_rule(*, single_favorable: bool) -> dict[str, Any]:
    """The existing engine's "unresolved field" shape.

    ``single_favorable=True`` reproduces the *unrepaired* shape (favorable =
    {"qualified"} only, the same as P3): every non-qualified reason,
    including the three now-determined zero reasons, still shows through
    this blocked field. ``single_favorable=False`` is the P4-repaired intent
    -- favorable = all four determined reasons -- built to demonstrate that
    the *existing, unmodified* ``_favorable_values``/``_selection_blocked_reasons``
    code refuses it (``determined-zero-reader-gap``'s probe case).
    """
    if single_favorable:
        gate_value = {
            "op": "collect_categorical_all_equal", "name": REASON,
            "value": _reason_lit("qualified"),
        }
    else:
        # Four ``collect_categorical_all_equal`` nodes over REASON, matching
        # the four determined values. This is exactly what
        # ``presentation_projection._favorable_values`` is built to scan for
        # and exactly what its "exactly one favorable value" check (line 375)
        # then refuses.
        gate_value = {
            "op": "any",
            "args": [
                {"op": "collect_categorical_all_equal", "name": REASON, "value": _reason_lit(value)}
                for value in sorted(DETERMINED_REASONS)
            ],
        }
    active_path = {
        "id": "statement",
        "activity": {"kind": "source_nonempty", "member_fact_types": [{"id": BOX1, "version": "v1"}]},
        "reads_subject_results": [{"symbol": REASON, "subject": {"id": BOX1, "version": "v1"}}],
        "requires": [],
        "pins": [],
        "when": {"op": "not", "value": gate_value},
        "value": {"op": "block", "code": "DEPENDENCY_ABSENT"},
    }
    inert_path = {
        "id": "inert",
        "activity": {"kind": "source_nonempty", "member_fact_types": [{"id": INERT, "version": "v1"}]},
        "reads_subject_results": [],
        "requires": [],
        "pins": [],
        "when": True,
        "value": {"op": "block", "code": "DEPENDENCY_ABSENT"},
    }
    return {
        "schema": "rule-artifact.v13",
        "id": "tax.us.2025.rule.f1098-residence-interest-unresolved",
        "version": "v2" if single_favorable else "v3",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation",
        "requires": [],
        "pins": [],
        "when": True,
        "selection": {
            "mode": "exclusive_presence",
            "conflict": "refuse",
            "paths": [active_path, inert_path],
            "default": {"id": "neither", "reads_subject_results": [], "requires": [], "pins": [], "when": False, "value": False},
            "refusal": {"code": "DEPENDENCY_INVALID", "missing": ["f1098-residence-interest-unresolved-inert-path-conflict"], "pins": []},
        },
        "publishes": UNRESOLVED_SYMBOL,
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "citations": [],
        "notes": "P4 probe only. Second path is an inert placeholder, same technique as tax.us.2025.sli.inert-path-unwritten.",
    }


def _unresolved_field() -> dict[str, Any]:
    return {
        "schema": "form-field.v3",
        "id": "tax.us.2025.form.f1098.residence-interest-unresolved",
        "version": "v1",
        "form": {"authority": "IRS", "form_id": "1040-SCH-A", "jurisdiction": "US-federal", "tax_year": 2025},
        "line": "f1098-unresolved",
        "label": "P4 probe: open condition on the home mortgage interest statement",
        "description": "P4 probe field. Inapplicable when line 8a published, or line 8a is a determined conclusion; otherwise names the open condition.",
        "binds_symbol": UNRESOLVED_SYMBOL,
        "dispositions": {
            "blocked": {"codes": ["DEPENDENCY_ABSENT", "DEPENDENCY_INVALID"], "explain": "An open condition on the Form 1098 statement is still unresolved.", "render": ""},
            "guard_inapplicable": {"explain": "No open condition: line 8a already published a determined conclusion, or there is no statement.", "render": ""},
            "published_value": {"explain": "Not used: this field never publishes a value.", "render": ""},
            "computed_zero": {"explain": "Not used: this field never publishes a value.", "render": ""},
            "closure_backed_zero": {"explain": "Not used: this field never publishes a value.", "render": ""},
        },
    }


# ---------------------------------------------------------------------------
# Throwaway surface
# ---------------------------------------------------------------------------


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text("utf-8"))


def _write_member(member_dir: Path, name: str, citizen: dict[str, Any]) -> tuple[str, str]:
    path = member_dir / name
    path.write_text(json.dumps(citizen, indent=2) + "\n", encoding="utf-8")
    stored = _read_json(path)
    return citizen["id"], citizen_checksum(stored)


def _build_surface(root: Path, *, include_duplicate: bool, single_favorable: bool) -> tuple[PublicationSurface, str, str, str, str]:
    member_dir = root / "members"
    member_dir.mkdir()
    old_line8a_file = "rule.schedule-a-line8a.json"
    old_f1098_bundle_file = "f1098.bundle.json"
    for source in sorted(CONTENT.rglob("*.json")):
        if source.name in (old_line8a_file, old_f1098_bundle_file):
            continue
        dest = member_dir / source.relative_to(CONTENT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.link(source, dest)
        except OSError:
            dest.write_bytes(source.read_bytes())

    registry = _read_json(REGISTRY_PATH)
    new_checksums: list[tuple[str, str, str]] = []  # (id, version, checksum)

    old_f1098_bundle = _read_json(CONTENT / old_f1098_bundle_file)
    old_f1098_bundle["fact_types"] = [
        ft for ft in old_f1098_bundle["fact_types"] if ft.get("id") != BOX9
    ]
    f1098_bundle_id, f1098_bundle_sum = _write_member(member_dir, old_f1098_bundle_file, old_f1098_bundle)
    replaced = 0
    for entry in registry["citizens"]:
        if entry.get("id") == f1098_bundle_id and entry.get("version") == "v1":
            entry["checksum"] = f1098_bundle_sum
            replaced += 1
    if replaced != 1:
        raise AssertionError(f"expected exactly one f1098.vocabulary registry entry, replaced {replaced}")

    bundle_id, bundle_sum = _write_member(member_dir, "f1098-successor.bundle.json", _bundle())
    new_checksums.append((bundle_id, "v2", bundle_sum))

    param_id, param_sum = _write_member(member_dir, "parameter.f1098-box9-default-single-property.json", _box9_default_parameter())
    new_checksums.append((param_id, "v1", param_sum))

    timing_purchase_param_id, timing_purchase_param_sum = _write_member(
        member_dir, "parameter.f1098-timing-purchase-structural-default.json",
        _timing_default_parameter(TIMING_PURCHASE_DEFAULT_PARAM, "more-than-90-days"))
    new_checksums.append((timing_purchase_param_id, "v1", timing_purchase_param_sum))
    timing_building_param_id, timing_building_param_sum = _write_member(
        member_dir, "parameter.f1098-timing-building-structural-default.json",
        _timing_default_parameter(TIMING_BUILDING_DEFAULT_PARAM, "no"))
    new_checksums.append((timing_building_param_id, "v1", timing_building_param_sum))

    reason_id, reason_sum = _write_member(member_dir, "rule.f1098-residence-interest-reason.probe.json", _reason_rule())
    new_checksums.append((reason_id, "v2", reason_sum))

    line8a_id, line8a_sum = _write_member(member_dir, "rule.f1098-line8a.probe.json", _line8a_rule("tax.us.2025.rule.f1098-line8a-probe"))
    new_checksums.append((line8a_id, "v2", line8a_sum))

    unresolved_rule = _unresolved_rule(single_favorable=single_favorable)
    unresolved_id, unresolved_sum = _write_member(member_dir, "rule.f1098-residence-interest-unresolved.probe.json", unresolved_rule)
    new_checksums.append((unresolved_id, unresolved_rule["version"], unresolved_sum))

    field_id, field_sum = _write_member(member_dir, "form1040.f1098-residence-interest-unresolved.form-field.probe.json", _unresolved_field())
    new_checksums.append((field_id, "v1", field_sum))

    duplicate_id = None
    if include_duplicate:
        dup = _line8a_rule("tax.us.2025.rule.f1098-line8a-duplicate-probe")
        dup["notes"] = "P4 probe only. Deliberate duplicate producer, to probe the one-producer constraint."
        duplicate_id, dup_sum = _write_member(member_dir, "rule.f1098-line8a-duplicate.probe.json", dup)
        new_checksums.append((duplicate_id, "v2", dup_sum))

    for cid, version, checksum in new_checksums:
        registry["citizens"].append({"id": cid, "version": version, "checksum": checksum})

    package = _read_json(PACKAGE_PATH)
    package["version"] = "v44"
    package.setdefault("input_bindings", []).extend([
        {"fact_type": {"id": BOX9, "version": "v1"}, "mode": "optional_default", "symbol": BOX9},
        {"fact_type": {"id": TIMING_PURCHASE, "version": "v1"}, "mode": "optional_default", "symbol": TIMING_PURCHASE},
        {"fact_type": {"id": TIMING_BUILDING, "version": "v1"}, "mode": "optional_default", "symbol": TIMING_BUILDING},
    ])
    package["members"] = [m for m in package["members"] if m["id"] != "tax.us.2025.schedule-a.line8a.rule"]
    package["entrypoints"] = [e for e in package["entrypoints"] if e["id"] != "tax.us.2025.schedule-a.line8a.rule"]
    package["entrypoints"].append({"id": line8a_id, "version": "v2"})
    if duplicate_id is not None:
        package["entrypoints"].append({"id": duplicate_id, "version": "v2"})
    package["members"].append({"id": bundle_id, "role": "fact-type-bundle", "schema": "bundle.v2", "version": "v2"})
    package["members"].append({"id": param_id, "role": "parameter", "schema": "parameter-declaration.v1", "version": "v1"})
    package["members"].append({"id": timing_purchase_param_id, "role": "parameter", "schema": "parameter-declaration.v1", "version": "v1"})
    package["members"].append({"id": timing_building_param_id, "role": "parameter", "schema": "parameter-declaration.v1", "version": "v1"})
    package["members"].append({"id": reason_id, "role": "computation", "schema": "rule-artifact.v13", "version": "v2"})
    package["members"].append({"id": line8a_id, "role": "computation", "schema": "rule-artifact.v13", "version": "v2"})
    package["members"].append({"id": unresolved_id, "role": "computation", "schema": "rule-artifact.v13", "version": unresolved_rule["version"]})
    package["members"].append({"id": field_id, "role": "form-field", "schema": "form-field.v3", "version": "v1"})
    if duplicate_id is not None:
        package["members"].append({"id": duplicate_id, "role": "computation", "schema": "rule-artifact.v13", "version": "v2"})
    package["conflict_semantics"] = [
        row for row in package["conflict_semantics"] if row.get("symbol") != LINE8A_SYMBOL
    ]
    if duplicate_id is not None:
        package["conflict_semantics"].append({"symbol": LINE8A_SYMBOL, "selected_producer": {"id": line8a_id, "version": "v2"}})
    package_path = member_dir / "package.core-calculations.v44.json"
    package["package_checksum"] = package_instance_checksum(package)
    package_path.write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    package_checksum = package["package_checksum"]
    registry.setdefault("packages", [])
    registry["packages"].append({"id": package["id"], "version": "v44", "checksum": package_checksum})

    registry_path = root / "published-packages.probe.json"
    registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")

    release = _read_json(RELEASE_PATH)
    release["package_registry_sha256"] = hashlib.sha256(registry_path.read_bytes()).hexdigest()
    release_dir = root / "releases"
    release_dir.mkdir()
    release_path = release_dir / RELEASE_PATH.name
    release_path.write_text(json.dumps(release, indent=2) + "\n", encoding="utf-8")
    release_checksum = hashlib.sha256(release_path.read_bytes()).hexdigest()
    return (
        PublicationSurface(release_dir, registry_path, member_dir),
        release_checksum,
        package["id"],
        "v44",
        package_checksum,
    )


# ---------------------------------------------------------------------------
# Acts
# ---------------------------------------------------------------------------


def _member_fact_id_here(fact_type: str) -> str:
    return _member_fact_id(fact_type, "demo.f1098.lender.a", "demo.f1098.stmt.a")


_FAVORABLE_ANSWERS = {
    "owns-the-home": "yes", "lives-there-most-of-the-time": "yes", "home-is-collateral": "yes",
    "owes-the-loan": "yes", "paid-the-interest": "yes", "no-one-else-owes-it": "yes",
    "what-the-money-paid-for": "bought-the-home", "this-is-the-original-loan": "yes",
    "mortgage-credit-certificate-received": "not-received",
}


def _probe_acts(
    *,
    box1: float = 20000.0,
    box2: float = 200000.0,
    box3: str = "2020-06-01",
    box9: float | None = 1.0,
    answers: dict[str, str] | None = None,
    timing: dict[str, str] | None = None,
) -> list[dict[str, object]]:
    """The proven P0/P2/P3 base corpus plus this probe's ordinary statements,
    including the two new timing questions when ``timing`` is supplied."""
    acts = p0._f1098_acts(interest=box1, wages=90000, box2=box2, box3=box3, box9=(box9 if box9 is not None else 1.0))
    if box9 is None:
        acts = [
            row for row in acts
            if not (
                isinstance(row.get("payload"), dict)
                and isinstance(row["payload"].get("finding"), dict)
                and str(row["payload"]["finding"].get("fact_id", "")).startswith(BOX9 + "|")
            )
        ]
    acts.pop()  # drop the v29 adoption; _finish appends this probe's own
    acts.extend(p0._selected_current_dependency_acts())

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append({
            "schema": "act.v1", "act_id": f"demo.f1098.p4.act.{len(acts):03d}", "kind": kind,
            "actor": USER, "at": f"2026-10-13T13:{len(acts) // 60:02d}:{len(acts) % 60:02d}Z",
            "committed_against": len(acts), "payload": payload,
        })

    add("bundle-adoption", {"bundle": _bundle()})
    resolved_answers = dict(_FAVORABLE_ANSWERS)
    if answers:
        resolved_answers.update(answers)
    for short, value in resolved_answers.items():
        add("assertion", {"finding": _attested(f"demo.f1098.p4.{short}", _member_fact_id_here(FACT + short), value)})
    if timing:
        for short, value in timing.items():
            add("assertion", {"finding": _attested(f"demo.f1098.p4.{short}", _member_fact_id_here(FACT + short), value)})
    return acts


def _no_statement_acts() -> list[dict[str, object]]:
    acts = p0._path_a_acts(wages=90000)
    acts.pop()
    acts.extend(p0._selected_current_dependency_acts())
    return acts


def _finish(
    acts: list[dict[str, object]],
    *,
    release_checksum: str,
    package_id: str,
    package_version: str,
    package_checksum: str,
) -> list[dict[str, object]]:
    built = copy.deepcopy(acts)
    adoption = p0._current_adoption(p0._load_fixture_adoption(), len(built))
    payload = adoption["payload"]
    assert isinstance(payload, dict)
    payload["package"] = {"id": package_id, "version": package_version, "checksum": package_checksum}
    release = payload["release"]
    assert isinstance(release, dict)
    release["checksum"] = release_checksum
    payload["audit"] = {"note": "synthetic P4 design-repair probe; throwaway surface, not adopted content"}
    built.append(adoption)
    for index, row in enumerate(built):
        row["committed_against"] = index
    return built


# ---------------------------------------------------------------------------
# Run + report
# ---------------------------------------------------------------------------


def _run(acts: list[dict[str, object]], run_id: str, surface: PublicationSurface) -> dict[str, Any]:
    started = time.monotonic()
    with TemporaryDirectory() as tmp:
        try:
            result = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "workspace"), repo_root=ROOT,
                authoritative_acts=acts, workspace_revision=len(acts), run_scope=SCOPE,
                scope_user=USER, request={"schema": "run-request.v1"}, run_id=run_id,
                governance_pins=[], surface=surface, output_name="out.json",
            )
        except Exception as exc:  # a composition defect is a probe result, not a script failure
            return {"run_id": run_id, "seconds": round(time.monotonic() - started, 1), "exception": {"type": type(exc).__name__, "message": str(exc)}}
        elapsed = round(time.monotonic() - started, 1)
        if result.refusal is not None:
            return {"run_id": run_id, "seconds": elapsed, "refusal": {"reason": result.refusal.reason, "detail": result.refusal.detail, "issues": [dict(i) for i in result.refusal.issues]}}
        assert result.output_path is not None and result.presentation_path is not None
        report = json.loads(result.output_path.read_text("utf-8"))
        model = json.loads(result.presentation_path.read_text("utf-8"))
        findings = p0._publication_rows(result)
        line8a_rows = [r for r in report.get("dispositions", []) if r.get("symbol") == LINE8A_SYMBOL or "line8a" in str(r.get("artifact_id", ""))]
        reason_pubs = [f for f in findings if str(f.get("symbol", "")).startswith(REASON)]
        reason_rows = [r for r in report.get("dispositions", []) if "residence-interest-reason" in str(r.get("artifact_id", ""))]
        unresolved_rows = [r for r in report.get("dispositions", []) if "residence-interest-unresolved" in str(r.get("artifact_id", ""))]
        line8a_pubs = [f for f in findings if f.get("symbol") == LINE8A_SYMBOL]
        line12e_section = next((s for s in model.get("sections", []) if s["id"] == "line-12e"), None)
        unresolved_field = next(
            (
                s for s in model.get("sections", [])
                if (s.get("field") or {}).get("id") == "tax.us.2025.form.f1098.residence-interest-unresolved"
            ),
            None,
        )
        reason_value = reason_pubs[0].get("value") if reason_pubs else None
        return {
            "run_id": run_id,
            "seconds": elapsed,
            "line8a_dispositions": line8a_rows,
            "line8a_publications": line8a_pubs,
            "reason_publications": reason_pubs,
            "reason_value": reason_value,
            "reason_description": REASON_DESCRIPTIONS.get(reason_value) if isinstance(reason_value, str) else None,
            "reason_is_determined": reason_value in DETERMINED_REASONS if isinstance(reason_value, str) else None,
            "reason_dispositions": reason_rows,
            "unresolved_dispositions": unresolved_rows,
            "unresolved_field_resolved": (unresolved_field or {}).get("resolved"),
            "line12e_value": (line12e_section or {}).get("resolved", {}).get("value"),
            "line12e_disposition": (line12e_section or {}).get("resolved", {}).get("disposition"),
        }


def _probe_reader_gap(root: Path) -> dict[str, Any]:
    """Case ``determined-zero-reader-gap``: attempt the four-favorable-value
    declaration against the real, unmodified ``build_presentation_model`` /
    ``_favorable_values`` and record what it does.

    This is the live, probed form of choice 8's remaining gap: the existing
    reader's single-favorable-value assumption
    (``presentation_projection._favorable_values``, and the ``len(favorable)
    != 1`` check inside ``_selection_blocked_reasons``) has no way to express
    "inapplicable unless the reason is one of these four," so the three
    now-determined zero reasons cannot yet be excluded from the blocked
    field using existing code alone. Not building the fix; naming it exactly.

    The act below uses ``cannot-tell`` on use, not a personal-expense
    answer: with the four-favorable declaration, a personal-expense
    statement's path is correctly *inapplicable* (its own value is one of
    the four favorables, so the active-path guard is false and
    ``_selection_blocked_reasons`` is never called at all -- probed first,
    and found NOT to reproduce the gap, exactly because the path never
    activates). ``cannot-tell-use`` is not one of the four declared
    favorables, so the path activates (blocked), and
    ``_selection_blocked_reasons`` is reached, where the single-favorable
    assumption actually lives.
    """
    with TemporaryDirectory() as tmp:
        surface, release_checksum, package_id, package_version, package_checksum = _build_surface(
            Path(tmp), include_duplicate=False, single_favorable=False,
        )
        acts = _finish(
            _probe_acts(answers={"what-the-money-paid-for": "cannot-tell"}),
            release_checksum=release_checksum, package_id=package_id,
            package_version=package_version, package_checksum=package_checksum,
        )
        started = time.monotonic()
        try:
            with TemporaryDirectory() as ws_tmp:
                result = live_coordinate_run(
                    WorkspaceCapability(Path(ws_tmp) / "workspace"), repo_root=ROOT,
                    authoritative_acts=acts, workspace_revision=len(acts), run_scope=SCOPE,
                    scope_user=USER, request={"schema": "run-request.v1"}, run_id="demo.f1098.p4.determined-zero-reader-gap",
                    governance_pins=[], surface=surface, output_name="out.json",
                )
            if result.refusal is not None:
                return {"outcome": "refused-before-presentation", "reason": result.refusal.reason,
                        "detail": result.refusal.detail,
                        "issues": [dict(i) for i in result.refusal.issues],
                        "seconds": round(time.monotonic() - started, 1)}
            return {"outcome": "built-presentation-model-without-error", "note": "unexpected: the gap may already be closed",
                    "seconds": round(time.monotonic() - started, 1)}
        except PresentationModelError as exc:
            return {"outcome": "PresentationModelError", "message": str(exc),
                    "seconds": round(time.monotonic() - started, 1)}
        except Exception as exc:  # pragma: no cover - reported, not asserted
            return {"outcome": f"unexpected {type(exc).__name__}", "message": str(exc),
                    "seconds": round(time.monotonic() - started, 1)}


def main() -> None:
    results: dict[str, Any] = {}
    favorable_timing = {
        "loan-timing-relative-to-purchase": "more-than-90-days",
        "loan-timing-relative-to-building-or-improving": "no",
    }
    with TemporaryDirectory() as tmp:
        surface, release_checksum, package_id, package_version, package_checksum = _build_surface(
            Path(tmp), include_duplicate=False, single_favorable=True,
        )

        def run_case(name: str, acts: list[dict[str, object]]) -> None:
            built = _finish(
                acts, release_checksum=release_checksum, package_id=package_id,
                package_version=package_version, package_checksum=package_checksum,
            )
            results[name] = _run(built, f"demo.f1098.p4.{name}", surface)

        # --- Baseline carryovers from P3, re-run against the revised rules ---
        run_case("supported-purchase", _probe_acts())
        run_case("box2-over-limit", _probe_acts(box2=800000.0))
        run_case("box9-absent", _probe_acts(box9=None))
        run_case("cannot-tell-use", _probe_acts(answers={"what-the-money-paid-for": "cannot-tell"}))
        run_case("refinance", _probe_acts(answers={"this-is-the-original-loan": "no"}))
        run_case("zero-interest", _probe_acts(box1=0.0))
        run_case("closed-empty", _no_statement_acts())

        # --- Action 8, item 1: personal expense beside each preventing condition ---
        run_case(
            "personal-expense-clean",
            _probe_acts(answers={"what-the-money-paid-for": "unrelated-personal-expense"}, timing=favorable_timing),
        )
        run_case(
            "personal-expense-refinance",
            _probe_acts(
                answers={"what-the-money-paid-for": "unrelated-personal-expense", "this-is-the-original-loan": "no"},
                timing=favorable_timing,
            ),
        )
        run_case(
            "personal-expense-two-properties",
            _probe_acts(answers={"what-the-money-paid-for": "unrelated-personal-expense"}, timing=favorable_timing, box9=2.0),
        )
        run_case(
            "personal-expense-timing-window",
            _probe_acts(
                answers={"what-the-money-paid-for": "unrelated-personal-expense"},
                timing={"loan-timing-relative-to-purchase": "within-90-days",
                        "loan-timing-relative-to-building-or-improving": "no"},
            ),
        )
        run_case(
            "personal-expense-building-window",
            _probe_acts(
                answers={"what-the-money-paid-for": "unrelated-personal-expense"},
                timing={"loan-timing-relative-to-purchase": "more-than-90-days",
                        "loan-timing-relative-to-building-or-improving": "yes-shortly-before-or-after"},
            ),
        )
        run_case(
            "personal-expense-cannot-tell-timing",
            _probe_acts(
                answers={"what-the-money-paid-for": "unrelated-personal-expense"},
                timing={"loan-timing-relative-to-purchase": "cannot-tell",
                        "loan-timing-relative-to-building-or-improving": "no"},
            ),
        )
        run_case(
            "personal-expense-grandfathered-box3",
            _probe_acts(
                answers={"what-the-money-paid-for": "unrelated-personal-expense"}, timing=favorable_timing,
                box3="1985-01-01",
            ),
        )

        # --- Action 8, item 2: personal expense with uncertain ownership ---
        run_case(
            "personal-expense-uncertain-ownership",
            _probe_acts(
                answers={"what-the-money-paid-for": "unrelated-personal-expense", "owns-the-home": "cannot-tell"},
                timing=favorable_timing,
            ),
        )

        # --- Action 8, item 3: uncertain ownership alone, against an unsupported circumstance ---
        run_case(
            "uncertain-ownership-against-refinance",
            _probe_acts(answers={"owns-the-home": "cannot-tell", "this-is-the-original-loan": "no"}),
        )

        # --- Action 8, item 6: owner who paid without being on the note ---
        run_case(
            "owner-not-on-note",
            _probe_acts(answers={"owes-the-loan": "no", "paid-the-interest": "yes"}),
        )

        # --- Integration-surface artifact: the three zero/outside-coverage
        # reasons the first round's closure named as "design reading only,
        # not separately probed" -- closed here as standalone cases, not
        # only in combination with another adverse fact. ---
        run_case("not-collateral", _probe_acts(answers={"home-is-collateral": "no"}))
        run_case("not-paid", _probe_acts(answers={"paid-the-interest": "no"}))
        run_case("certificate-received", _probe_acts(answers={"mortgage-credit-certificate-received": "received"}))

        # --- Action 8, item 5: two independently decisive adverse facts at once ---
        run_case(
            "not-collateral-and-personal-expense",
            _probe_acts(
                answers={"home-is-collateral": "no", "what-the-money-paid-for": "unrelated-personal-expense"},
                timing=favorable_timing,
            ),
        )
        run_case(
            "personal-expense-and-certificate-received",
            _probe_acts(
                answers={"what-the-money-paid-for": "unrelated-personal-expense",
                         "mortgage-credit-certificate-received": "received"},
                timing=favorable_timing,
            ),
        )

    with TemporaryDirectory() as tmp:
        surface, release_checksum, package_id, package_version, package_checksum = _build_surface(
            Path(tmp), include_duplicate=True, single_favorable=True,
        )

        def run_dup(name: str, acts: list[dict[str, object]]) -> None:
            built = _finish(
                acts, release_checksum=release_checksum, package_id=package_id,
                package_version=package_version, package_checksum=package_checksum,
            )
            results[name] = _run(built, f"demo.f1098.p4.{name}", surface)

        run_dup("double-match-zero", _probe_acts(answers={"what-the-money-paid-for": "unrelated-personal-expense"}, timing=favorable_timing))
        run_dup("double-match-qualifying", _probe_acts())

    # --- Action 8, item "reader gap": the determined-zero reader change this
    # round does not build, probed against the real, unmodified code. ---
    with TemporaryDirectory() as tmp:
        results["determined-zero-reader-gap"] = _probe_reader_gap(Path(tmp))

    print(json.dumps({"probe": "p4-design-repair", "results": results}, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
