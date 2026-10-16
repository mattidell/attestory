"""P7 payment-and-fixture probe: build the corrected successor arrangement
in a temporary registry and run it through ``live_coordinate_run`` and the
real presentation model, per P2/P3/P4's throwaway-surface technique. Nothing
here is adopted; nothing is written into ``packages/content``.

This probe retains its established P5 filename and extends the design
correction arrangement for the P7 payment and fixture corrections.
The default invocation retains P6's broad probe; ``--p7-targeted`` runs
only this round's affected payment, correction, joint-filer, and investment
cases.

1. each P4 re-review finding:
   - uncertain ownership, residence, and the sole-obligor statement
     (``no-one-else-owes-it``) now route to their own uncertainty reasons,
     not the generic ``outside-coverage`` residual (choice 4);
   - a determined zero's carrier gap is specified as a third reader change
     (not built -- no production code changes; reproduced live against the
     real, unmodified module, same as P4);
   - the box 9 successor is a genuine new fact-type version (``v2``,
     ``optional_default`` added), not a same-version substitution -- the
     real, unmodified v1 Form 1098 bundle is left untouched this round;
   - the joint-return spouse wording is applied to liability, payment, and
     sole-obligor questions; a named joint-filer case pairs the ordinary
     interpretation with stored answers and the coordinator result;
   - third-party and partial payment now have an explicit exclusion outcome;
     recorder correction remains a specification, not a demonstrated path.
2. the grandfathering condition (choice 3): one ``date_compare`` check
   (``rule-artifact.v14``, ``artifact-package.v36``) against the reviewed
   operator's exact shape, nested inside the personal-expense zero's
   original-loan/box-9 branch.
3. the absent-timing repair (owner finding 1): the two timing facts'
   structural defaults are no longer a favourable value standing in for an
   assumption -- the ``optional_default`` is now the reserved sentinel
   ``not-asked``, routed to its own open-condition reason, never confused
   with ``cannot-tell``.
4. completion-relative timing, both purchase-window directions, and the
   Publication 936 (2025) page 12 examples, each paired with ordinary
   wording, stored answers, and the coordinator outcome.

Every case below still uses direct synthetic assertions, not the recording
operation's save/correct/withdraw contract -- named as a remaining stand-in
in the report below, same as every prior round.

Run from the repository root:

    python3 docs/phases/tax-circumstance-breadth/milestones/mortgage-interest-circumstances-evidence/p5_probe.py
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
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
# P5 repair (owner finding 1): the two timing facts' ``optional_default`` is
# no longer a favourable real-world assumption ("more than 90 days", "no
# building work") -- it is the reserved sentinel ``not-asked``, which the
# value tree routes to its own open-condition reason, never to the zero and
# never to ``cannot-tell-timing``. See ``_personal_expense_timing_branch``.
TIMING_PURCHASE_DEFAULT_PARAM = "tax.us.2025.parameter.f1098-timing-purchase-structural-default"
TIMING_BUILDING_DEFAULT_PARAM = "tax.us.2025.parameter.f1098-timing-building-structural-default"
# §163(h)(3)(D)(i)(II) / Pub. 936 (2025) p.13: grandfathered debt is debt
# "incurred on or before" this date and secured by the home on this date.
# "Before October 14, 1987" (the publication's own phrasing) is the same
# boundary, inclusive of the date itself -- date_compare's ``lte`` makes
# equality a possible-grandfathered-debt case, not a cleared one.
GRANDFATHER_CUTOFF = "1987-10-13"

# The seven always-asked ordinary statements (choice 1). ``owes-the-loan`` is
# a gate (P4 repair, choice 1), not informational-only. P5 adds no new fact
# here for the spouse finding -- see the design note at ``_qualified_conjunction``.
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

# The two ordinary timing questions (choice 3). P5 adds a fourth, reserved
# value to each enum: ``not-asked``, the package-level structural default,
# never a value the recording operation offers the person (section 8).
TIMING_PURCHASE = FACT + "loan-timing-relative-to-purchase"
TIMING_BUILDING = FACT + "loan-timing-relative-to-building-or-improving"

# Eighteen non-qualified reason categories, nineteen total including
# ``qualified`` (P6 had seventeen non-qualified categories).
REASON_VALUES = (
    "qualified",
    "not-collateral",
    "not-paid",
    "owner-not-on-note",
    "use-unrelated-personal-expense",
    "timing-exception-possible",
    "cannot-tell-timing",
    "timing-not-established",
    "possible-grandfathered-debt",
    "cannot-tell-use",
    "cannot-tell-ownership",
    "cannot-tell-residence",
    "cannot-tell-share",
    "cannot-tell-collateral",
    "cannot-tell-payment",
    "payment-outside-coverage",
    "certificate-received",
    "debt-limit-over",
    "outside-coverage",
)
# The condition table's "determined" conclusions (choice 8/9): the only
# categories a completed conclusion, not an open question, names. Unchanged
# by P6 -- the added uncertainty categories are open questions, not completed
# conclusions.
DETERMINED_REASONS = frozenset({
    "qualified", "not-collateral", "not-paid", "use-unrelated-personal-expense",
})
REASON_DESCRIPTIONS = {
    "qualified": "The interest qualifies as home mortgage interest for this statement.",
    "not-collateral": "The home is not collateral for this loan, so the debt is not secured acquisition indebtedness.",
    "not-paid": "Neither you nor your spouse, if filing jointly, paid any of this interest, and nobody paid any for you. This route does not publish a deduction for this statement.",
    "payment-outside-coverage": "Someone else paid some or all of this interest, or you paid only part. This route does not calculate an amount or decide the treatment; it is left with you.",
    "owner-not-on-note": "The person paid this interest but is not on the note. Treas. Reg. section 1.163-1(b) may still allow the deduction for an equitable owner, but this route does not compute a non-obligor's deduction. The treatment is left with the person.",
    "use-unrelated-personal-expense": "The borrowed money paid for a personal expense that was not buying, building, or improving the home, so this interest is not qualified residence interest.",
    "timing-exception-possible": "Your answers place this loan within 90 days before or after buying the home, or before completion of building or improving the home or within 90 days after completion. Publication 936's exceptions may still make this acquisition debt. This route does not compute the expense cap or decide whether the work was a substantial improvement. The treatment is left with you.",
    "cannot-tell-timing": "You said you cannot tell whether this loan was taken out within 90 days before or after buying the home, or before you finished building or improving the home or within 90 days after you finished. The application cannot reach a conclusion about this interest until that is known.",
    "timing-not-established": "You haven't yet said whether this loan was taken out around the time you bought, built, or improved the home. The application cannot reach a conclusion about this interest until that is answered.",
    "possible-grandfathered-debt": "This loan was originated on or before October 13, 1987, which may make it grandfathered debt under section 163(h)(3)(D), fully deductible home mortgage interest regardless of what the money paid for. This route only compares the origination date against that one cutoff; it does not check whether the debt stayed continuously secured by the home, or how a later refinancing would affect that status. The treatment is left with the person.",
    "cannot-tell-use": "You said you cannot tell what the borrowed money paid for. The application cannot reach a conclusion about this interest until that is known.",
    "cannot-tell-ownership": "You said you cannot tell whether you own this home. The application cannot reach a conclusion about this interest until that is known. This is an open question about your own account, not a circumstance the application does not support.",
    "cannot-tell-residence": "You said you cannot tell whether this is the home where you live most of the time. The application cannot reach a conclusion about this interest until that is known.",
    "cannot-tell-share": "You said you cannot tell whether anyone else owes this loan with you. The application cannot reach a conclusion about this interest until that is known.",
    "cannot-tell-collateral": "You said you cannot tell whether the home is collateral for this loan. The application cannot reach a conclusion about this interest until that is known.",
    "cannot-tell-payment": "You said you cannot tell which payment description applies. The application cannot reach a conclusion about this interest until that is known.",
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
        _enum_fact(
            fact_id,
            "P7 probe ordinary statement: who paid the reported interest" if fact_id == FACT + "paid-the-interest" else f"P5 probe ordinary statement: {fact_id.rsplit('.', 1)[-1]}",
            ("yes", "paid-by-others-or-partial", "no", "cannot-tell") if fact_id == FACT + "paid-the-interest" else ("yes", "no", "cannot-tell"),
        )
        for fact_id in NEW_YES_NO_FACTS
    ]
    fact_types.append(_enum_fact(
        WHAT_FOR, "P5 probe ordinary statement: what the money paid for",
        ("bought-the-home", "unrelated-personal-expense", "other", "cannot-tell"),
    ))
    fact_types.append(_enum_fact(
        CERT, "P5 probe ordinary statement: mortgage credit certificate (polarity-safe, P3 finding 7)",
        ("received", "not-received", "cannot-tell"),
    ))
    # P5 repair (owner finding 1): ``not-asked`` is a fourth, reserved value
    # -- the package-level structural default, never offered to the person
    # by the recording operation (section 8). It is not ``cannot-tell``: the
    # person never said anything. See ``_personal_expense_timing_branch``.
    timing_purchase = _enum_fact(
        TIMING_PURCHASE,
        "P6 probe ordinary statement: purchase timing answer",
        ("yes", "no", "cannot-tell", "not-asked"),
    )
    timing_purchase["optional_default"] = {"parameter": {"id": TIMING_PURCHASE_DEFAULT_PARAM, "version": "v1"}}
    fact_types.append(timing_purchase)
    timing_building = _enum_fact(
        TIMING_BUILDING,
        "P6 probe ordinary statement: building or improving completion timing answer",
        ("yes", "no", "cannot-tell", "not-asked"),
    )
    timing_building["optional_default"] = {"parameter": {"id": TIMING_BUILDING_DEFAULT_PARAM, "version": "v1"}}
    fact_types.append(timing_building)
    fact_types.append(_box9_successor_fact_type())
    fact_types.append({
        "schema": "fact-type.v2",
        "id": REASON,
        "version": "v1",
        "title": "P5 probe: the one reason this statement's interest is or is not qualified residence interest",
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
        "version": "v3",
        "label": "P5 probe: respecified Form 1098 ordinary statements and reason",
        "fact_types": fact_types,
    }


def _box9_successor_fact_type() -> dict[str, Any]:
    """P5 repair (finding 5, choice 11): a genuine new fact-type *version*,
    not a same-id-version substitution of the real, published v1. The real
    v1 ``f1098.bundle.json`` box 9 citizen is left byte-identical and
    untouched this round (``_build_surface`` no longer strips it). Existing
    recorded box 9 values resolve under this v2-admitting package because
    this corpus's finding-to-symbol binding
    (``packages/derivation/marshal.py``'s ``_fact_id_has_type``) matches a
    current finding to its symbol by the fact *id* alone -- read directly,
    not argued -- and ``_attested`` findings (this probe's own, and every
    adopted Form 1098 finding) carry no ``fact_type`` version pin at all.
    v2's own declaration is what newly supplies ``optional_default`` for an
    absent box 9; a value already on record, however it was asserted,
    resolves the same way either version is admitted.
    """
    return {
        "schema": "fact-type.v2",
        "id": BOX9,
        "version": "v2",
        "title": "Form 1098 box9-number-of-properties (P5 successor: absent is one property)",
        "nature": "determinable",
        "identity_keys": _identity_keys(),
        "value_schema": {"type": "number"},
        "supersession": {"policy": "free"},
        "optional_default": {"parameter": {"id": BOX9_DEFAULT_PARAM, "version": "v1"}},
    }


def _box9_default_parameter() -> dict[str, Any]:
    return {
        "schema": "parameter-declaration.v1",
        "id": BOX9_DEFAULT_PARAM,
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax", "effective_from": "2025-01-01"},
        "values": 1,
    }


def _timing_default_parameter(param_id: str) -> dict[str, Any]:
    """P5 repair: the declared default is the reserved sentinel
    ``not-asked``, never a favourable real-world value. See the module
    docstring and ``_personal_expense_timing_branch``."""
    return {
        "schema": "parameter-declaration.v1",
        "id": param_id,
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax", "effective_from": "2025-01-01"},
        "values": "not-asked",
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


def _not_grandfathered(box9_eq_one: bool = True) -> dict[str, Any]:
    """ADR 0078's reviewed ``date_compare`` operator, exactly as shaped
    there. ``cmp: "lte"`` -- box 3 on or before the cutoff -- is the
    possible-grandfathered side (choice 2: equality counts as grandfathered,
    matching Pub. 936 (2025) p.13's "before October 14, 1987" and
    section 163(h)(3)(D)(i)(II)'s "incurred on or before"). Nested only
    inside the original-loan-and-one-property branch (condition table row
    6/7): a refinance or multi-property statement is already outside
    coverage for a different, unrelated reason, and box 3 on this
    statement is not evidence about an *earlier* loan's origination date."""
    return {"op": "date_compare", "left": _ref(BOX3), "date": GRANDFATHER_CUTOFF, "cmp": "lte"}


def _qualified_conjunction() -> dict[str, Any]:
    """Choice 1's repair: ``owes-the-loan`` is a gate on the supported arm.

    P6 (spouse correction): a spouse who is also an obligor on a joint
    return does not change how these are answered. ``owes-the-loan`` and
    ``paid-the-interest`` ask about the filing unit on a joint return: if
    either spouse owes the loan or paid the interest, the answer is
    ``yes``. ``no-one-else-owes-it``'s "else" already excludes a spouse on
    a joint return -- the retired software-coverage bound
    ``not-shared-except-spouse`` is subsumed here, not separately asked.
    P6 clarified this joint-return interpretation. P7 keeps that yes-value
    for the other spouse's full payment and adds separate partial/third-party
    and genuine-no meanings on the existing payment fact. Every supported-
    arm case below exercises this conjunction; the targeted P7 case records
    an actual joint filing status."""
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


def _non_identity_favorable() -> dict[str, Any]:
    """The condition that must hold for an ownership/residence/share/
    collateral uncertainty to get its *own* reason, rather than the generic
    ``outside-coverage`` residual. Deliberately narrower than
    ``_qualified_conjunction`` above: it does not re-check
    ``home-is-collateral``/``owes-the-loan``/``paid-the-interest`` (already
    decisive or classified, and checked earlier in the priority order), and it does not
    check the answer fields themselves (that is what distinguishes
    the qualified conjunction's failure from a genuinely different,
    already-classified condition such as a refinance)."""
    return {
        "op": "all",
        "args": [
            _cat_eq(WHAT_FOR, "bought-the-home"),
            _cat_eq(FACT + "this-is-the-original-loan", "yes"),
            _cat_eq(CERT, "not-received"),
            {"op": "compare", "cmp": "eq", "left": _ref(BOX9), "right": 1},
        ],
    }


def _identity_uncertainty_branch(outside_coverage: dict[str, Any]) -> dict[str, Any]:
    """Route each remaining ``cannot-tell`` answer to its own reason. Only
    reached once ``_non_identity_favorable`` already holds, so
    a refinance or second property beside an uncertain identity answer
    still reaches the generic residual unchanged (``uncertain-ownership-
    against-refinance``, carried forward from P4)."""
    return _choose(
        _cat_eq(FACT + "home-is-collateral", "cannot-tell"), _reason_lit("cannot-tell-collateral"),
        _choose(
            _cat_eq(FACT + "owns-the-home", "cannot-tell"), _reason_lit("cannot-tell-ownership"),
            _choose(
                _cat_eq(FACT + "lives-there-most-of-the-time", "cannot-tell"), _reason_lit("cannot-tell-residence"),
                _choose(
                    _cat_eq(FACT + "no-one-else-owes-it", "cannot-tell"), _reason_lit("cannot-tell-share"),
                    outside_coverage,
                ),
            ),
        ),
    )


def _personal_expense_timing_branch(zero_value: Any, reclassify_or_unresolved_only: bool) -> dict[str, Any]:
    """Choice 3's two ordinary timing questions, read only inside this
    branch -- never in ``requires`` as a conditional dependency (a subject-
    scoped rule's ``requires`` is its exhaustive join set; see ADR-0037's
    ``conditional_dependency_set``, assessed and set aside because it
    operates only within ``value``'s own evaluation and does not change
    which types subject_dispatch joins into a subject's row at all).

    P5 repair (owner finding 1): a fourth branch, ``not-asked``, sits
    between ``cannot-tell`` and the cleared case. The package-level
    structural default resolves an unasked question to ``not-asked``, not
    to a favourable value and not to ``cannot-tell`` -- so an account where
    one or both timing answers are genuinely absent (never asked, or
    withdrawn after being given) reaches ``timing-not-established``
    (REASON) / blocks (LINE8A), never the zero and never a sentence
    claiming the person said "can't tell". If one timing answer is
    unfavourable and the other is ``not-asked``, the unfavourable answer
    still wins (checked first, unconditionally on the other question's
    state) -- one adverse timing fact is already enough to flag the
    exception, matching the condition table's existing priority.

    ``zero_value`` is a 4-tuple: what each of the
    (within-90, building, cannot-tell, not-asked) branches returns before
    falling to the cleared case. For the REASON rule,
    ``reclassify_or_unresolved_only`` is ignored (REASON always resolves to
    a specific category); for the LINE8A rule, the caller supplies the
    *next* step in its own value tree instead, so both rules share this one
    function."""
    within_90 = _cat_eq(TIMING_PURCHASE, "yes")
    building = _cat_eq(TIMING_BUILDING, "yes")
    timing_cannot_tell = {
        "op": "any",
        "args": [_cat_eq(TIMING_PURCHASE, "cannot-tell"), _cat_eq(TIMING_BUILDING, "cannot-tell")],
    }
    timing_not_asked = {
        "op": "any",
        "args": [_cat_eq(TIMING_PURCHASE, "not-asked"), _cat_eq(TIMING_BUILDING, "not-asked")],
    }
    return _choose(
        within_90, _reason_lit("timing-exception-possible") if reclassify_or_unresolved_only else zero_value[0],
        _choose(
            building, _reason_lit("timing-exception-possible") if reclassify_or_unresolved_only else zero_value[0],
            _choose(
                timing_cannot_tell, _reason_lit("cannot-tell-timing") if reclassify_or_unresolved_only else zero_value[1],
                _choose(
                    timing_not_asked, _reason_lit("timing-not-established") if reclassify_or_unresolved_only else zero_value[2],
                    zero_value[3],
                ),
            ),
        ),
    )


def _reason_value_tree() -> dict[str, Any]:
    """Choice 9's priority order, as one nested ``choose`` in one rule
    (choice 8/action 4: one rule per symbol, internal branches, so no
    double-match hazard can arise by construction):

    1. not-collateral (decisive regardless of use, refinance, or
       grandfathering -- Section 163(h)(3)(B)(i)(II))
    2. payment outside coverage (some/all paid by others, or filing unit
       paid only part; no amount is calculated)
    3. no payment by/for the filing unit (decisive under Treas. Reg.
       1.163-1(b))
    4. owner-not-on-note (choice 1 repair: paid but does not owe the loan --
       outside coverage, not a zero)
    5. personal-expense use, gated by the two timing questions (choice 3),
       then by original-loan, box9, and (P5, choice 3) grandfathering
    6. cannot-tell payment/use
    7. certificate received
    8. the full qualified conjunction (including the owes-the-loan gate),
       then the box 2 compare
    9. (P5/P6) other standalone uncertainties
    10. outside coverage (the true residual)
    """
    outside_coverage = _reason_lit("outside-coverage")
    grandfathering_checked = _choose(
        _not_grandfathered(), _reason_lit("possible-grandfathered-debt"),
        _reason_lit("use-unrelated-personal-expense"),
    )
    zero_after_timing = _choose(
        {
            "op": "all",
            "args": [
                _cat_eq(FACT + "this-is-the-original-loan", "yes"),
                {"op": "compare", "cmp": "eq", "left": _ref(BOX9), "right": 1},
            ],
        },
        grandfathering_checked,
        outside_coverage,
    )
    personal_expense_branch = _personal_expense_timing_branch(
        (None, None, None, zero_after_timing), reclassify_or_unresolved_only=True,
    )
    qualified_branch = _choose(
        {"op": "compare", "cmp": "gt", "left": _ref(BOX2), "right": _limit_ref()},
        _reason_lit("debt-limit-over"),
        _reason_lit("qualified"),
    )
    final_residual = _choose(
        _non_identity_favorable(), _identity_uncertainty_branch(outside_coverage), outside_coverage,
    )
    tail = _choose(_qualified_conjunction(), qualified_branch, final_residual)
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
    tail = _choose(_cat_eq(FACT + "paid-the-interest", "cannot-tell"), _reason_lit("cannot-tell-payment"), tail)
    tail = _choose(_cat_eq(FACT + "paid-the-interest", "no"), _reason_lit("not-paid"), tail)
    tail = _choose(_cat_eq(FACT + "paid-the-interest", "paid-by-others-or-partial"), _reason_lit("payment-outside-coverage"), tail)
    tail = _choose(_cat_eq(FACT + "home-is-collateral", "no"), _reason_lit("not-collateral"), tail)
    return tail


def _reason_rule() -> dict[str, Any]:
    # P5: box 3 joins ``requires`` for the first time on this rule -- it is
    # now read, for the grandfathering check, inside the personal-expense
    # branch only.
    requires = [*NEW_YES_NO_FACTS, WHAT_FOR, CERT, BOX2, BOX3, BOX9, TIMING_PURCHASE, TIMING_BUILDING, "filing_status"]
    return {
        "schema": "rule-artifact.v14",
        "id": "tax.us.2025.rule.f1098-residence-interest-reason",
        "version": "v3",
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
        "notes": "P5 probe only. Not an adopted rule. See the condition table.",
    }


def _line8a_value_tree() -> dict[str, Any]:
    """Mirrors ``_reason_value_tree``'s priority order and gates, publishing
    a dollar amount or a block instead of a category."""
    block = {"op": "block", "code": "DEPENDENCY_ABSENT"}
    qualified_branch = _choose(
        {"op": "compare", "cmp": "gt", "left": _ref(BOX2), "right": _limit_ref()},
        {"op": "block", "code": "VALUE_INVALID"},
        {"op": "add", "args": [{"op": "collect", "name": BOX1, "source_set": "tax.us.2025.f1098"}]},
    )
    final_residual = _choose(_non_identity_favorable(), block, block)
    tail = _choose(_qualified_conjunction(), qualified_branch, final_residual)
    tail = _choose(_cat_eq(CERT, "received"), block, tail)
    tail = _choose(_cat_eq(WHAT_FOR, "cannot-tell"), block, tail)
    grandfathering_checked = _choose(_not_grandfathered(), block, 0)
    zero_after_timing = _choose(
        {
            "op": "all",
            "args": [
                _cat_eq(FACT + "this-is-the-original-loan", "yes"),
                {"op": "compare", "cmp": "eq", "left": _ref(BOX9), "right": 1},
            ],
        },
        grandfathering_checked, block,
    )
    personal_expense_branch = _personal_expense_timing_branch(
        (block, block, block, zero_after_timing), reclassify_or_unresolved_only=False,
    )
    tail = _choose(_cat_eq(WHAT_FOR, "unrelated-personal-expense"), personal_expense_branch, tail)
    tail = _choose(
        {
            "op": "all",
            "args": [_cat_eq(FACT + "owes-the-loan", "no"), _cat_eq(FACT + "paid-the-interest", "yes")],
        },
        block, tail,
    )
    tail = _choose(_cat_eq(FACT + "paid-the-interest", "cannot-tell"), block, tail)
    tail = _choose(_cat_eq(FACT + "paid-the-interest", "paid-by-others-or-partial"), block, tail)
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
        "schema": "rule-artifact.v14",
        "id": rule_id,
        "version": "v3",
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
        "notes": "P5 probe only.",
    }


def _unresolved_rule() -> dict[str, Any]:
    """The existing engine's "unresolved field" shape, unrepaired this
    round (choice 8's reader change is specified, not built -- no
    production code changes). Favourable = {"qualified"} only, same as
    every prior round: every non-qualified reason, including the four now-
    determined-zero/outside-coverage reasons, still shows through this
    blocked field. See ``_probe_reader_gap`` for the live, negative proof
    that widening this declaration still hits the real, unmodified
    ``_favorable_values`` "exactly one" check."""
    gate_value = {
        "op": "collect_categorical_all_equal", "name": REASON,
        "value": _reason_lit("qualified"),
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
        "version": "v2",
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
        "notes": "P5 probe only. Second path is an inert placeholder, same technique as tax.us.2025.sli.inert-path-unwritten.",
    }


def _unresolved_rule_widened() -> dict[str, Any]:
    """Not the production shape -- a negative-evidence case only. Widens
    the declaration's favourable set to all four determined reasons, as
    choice 8's fix would, to reproduce the real reader's "exactly one"
    assumption live. See ``_probe_reader_gap``."""
    gate_value = {
        "op": "any",
        "args": [
            {"op": "collect_categorical_all_equal", "name": REASON, "value": _reason_lit(value)}
            for value in sorted(DETERMINED_REASONS)
        ],
    }
    rule = _unresolved_rule()
    rule = copy.deepcopy(rule)
    rule["version"] = "v3"
    rule["selection"]["paths"][0]["when"] = {"op": "not", "value": gate_value}
    return rule


def _unresolved_field() -> dict[str, Any]:
    return {
        "schema": "form-field.v3",
        "id": "tax.us.2025.form.f1098.residence-interest-unresolved",
        "version": "v1",
        "form": {"authority": "IRS", "form_id": "1040-SCH-A", "jurisdiction": "US-federal", "tax_year": 2025},
        "line": "f1098-unresolved",
        "label": "P5 probe: open condition on the home mortgage interest statement",
        "description": "P5 probe field. Inapplicable when line 8a published, or line 8a is a determined conclusion; otherwise names the open condition.",
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


def _build_surface(root: Path, *, include_duplicate: bool, unresolved_widened: bool) -> tuple[PublicationSurface, str, str, str, str]:
    member_dir = root / "members"
    member_dir.mkdir()
    old_line8a_file = "rule.schedule-a-line8a.json"
    for source in sorted(CONTENT.rglob("*.json")):
        if source.name == old_line8a_file:
            continue
        dest = member_dir / source.relative_to(CONTENT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        # These temporary citizens may be edited by this probe in later
        # rounds. Copy bytes so no write through a temporary path can mutate
        # the repository citizen via a shared inode.
        dest.write_bytes(source.read_bytes())

    # The real, published f1098.bundle.json (including its real v1 box
    # 9 citizen) is copied byte-identically and is NOT stripped or mutated.
    # Box 9's successor is a genuine
    # new version, added below, not a same-version substitution.

    registry = _read_json(REGISTRY_PATH)
    new_checksums: list[tuple[str, str, str]] = []  # (id, version, checksum)

    bundle_id, bundle_sum = _write_member(member_dir, "f1098-successor.bundle.json", _bundle())
    new_checksums.append((bundle_id, "v3", bundle_sum))

    param_id, param_sum = _write_member(member_dir, "parameter.f1098-box9-default-single-property.json", _box9_default_parameter())
    new_checksums.append((param_id, "v1", param_sum))

    timing_purchase_param_id, timing_purchase_param_sum = _write_member(
        member_dir, "parameter.f1098-timing-purchase-structural-default.json",
        _timing_default_parameter(TIMING_PURCHASE_DEFAULT_PARAM))
    new_checksums.append((timing_purchase_param_id, "v1", timing_purchase_param_sum))
    timing_building_param_id, timing_building_param_sum = _write_member(
        member_dir, "parameter.f1098-timing-building-structural-default.json",
        _timing_default_parameter(TIMING_BUILDING_DEFAULT_PARAM))
    new_checksums.append((timing_building_param_id, "v1", timing_building_param_sum))

    reason_id, reason_sum = _write_member(member_dir, "rule.f1098-residence-interest-reason.probe.json", _reason_rule())
    new_checksums.append((reason_id, "v3", reason_sum))

    line8a_id, line8a_sum = _write_member(member_dir, "rule.f1098-line8a.probe.json", _line8a_rule("tax.us.2025.rule.f1098-line8a-probe"))
    new_checksums.append((line8a_id, "v3", line8a_sum))

    unresolved_rule = _unresolved_rule_widened() if unresolved_widened else _unresolved_rule()
    unresolved_id, unresolved_sum = _write_member(member_dir, "rule.f1098-residence-interest-unresolved.probe.json", unresolved_rule)
    new_checksums.append((unresolved_id, unresolved_rule["version"], unresolved_sum))

    field_id, field_sum = _write_member(member_dir, "form1040.f1098-residence-interest-unresolved.form-field.probe.json", _unresolved_field())
    new_checksums.append((field_id, "v1", field_sum))

    duplicate_id = None
    if include_duplicate:
        dup = _line8a_rule("tax.us.2025.rule.f1098-line8a-duplicate-probe")
        dup["notes"] = "P5 probe only. Deliberate duplicate producer, to probe the one-producer constraint."
        duplicate_id, dup_sum = _write_member(member_dir, "rule.f1098-line8a-duplicate.probe.json", dup)
        new_checksums.append((duplicate_id, "v3", dup_sum))

    for cid, version, checksum in new_checksums:
        registry["citizens"].append({"id": cid, "version": version, "checksum": checksum})

    package = _read_json(PACKAGE_PATH)
    package["schema"] = "artifact-package.v36"
    if "rule-artifact.v14" not in package.get("admitted_schemas", []):
        package.setdefault("admitted_schemas", []).append("rule-artifact.v14")
    package["version"] = "v44"
    package.setdefault("input_bindings", []).extend([
        {"fact_type": {"id": BOX9, "version": "v2"}, "mode": "optional_default", "symbol": BOX9},
        {"fact_type": {"id": TIMING_PURCHASE, "version": "v1"}, "mode": "optional_default", "symbol": TIMING_PURCHASE},
        {"fact_type": {"id": TIMING_BUILDING, "version": "v1"}, "mode": "optional_default", "symbol": TIMING_BUILDING},
    ])
    package["members"] = [m for m in package["members"] if m["id"] != "tax.us.2025.schedule-a.line8a.rule"]
    package["entrypoints"] = [e for e in package["entrypoints"] if e["id"] != "tax.us.2025.schedule-a.line8a.rule"]
    package["entrypoints"].append({"id": line8a_id, "version": "v3"})
    if duplicate_id is not None:
        package["entrypoints"].append({"id": duplicate_id, "version": "v3"})
    package["members"].append({"id": bundle_id, "role": "fact-type-bundle", "schema": "bundle.v2", "version": "v3"})
    package["members"].append({"id": param_id, "role": "parameter", "schema": "parameter-declaration.v1", "version": "v1"})
    package["members"].append({"id": timing_purchase_param_id, "role": "parameter", "schema": "parameter-declaration.v1", "version": "v1"})
    package["members"].append({"id": timing_building_param_id, "role": "parameter", "schema": "parameter-declaration.v1", "version": "v1"})
    package["members"].append({"id": reason_id, "role": "computation", "schema": "rule-artifact.v14", "version": "v3"})
    package["members"].append({"id": line8a_id, "role": "computation", "schema": "rule-artifact.v14", "version": "v3"})
    package["members"].append({"id": unresolved_id, "role": "computation", "schema": "rule-artifact.v13", "version": unresolved_rule["version"]})
    package["members"].append({"id": field_id, "role": "form-field", "schema": "form-field.v3", "version": "v1"})
    if duplicate_id is not None:
        package["members"].append({"id": duplicate_id, "role": "computation", "schema": "rule-artifact.v14", "version": "v3"})
    package["conflict_semantics"] = [
        row for row in package["conflict_semantics"] if row.get("symbol") != LINE8A_SYMBOL
    ]
    if duplicate_id is not None:
        package["conflict_semantics"].append({"symbol": LINE8A_SYMBOL, "selected_producer": {"id": line8a_id, "version": "v3"}})
    package_path = member_dir / "package.core-calculations.v44.json"
    package["package_checksum"] = package_instance_checksum(package)
    package_path.write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    package_checksum = package["package_checksum"]
    registry.setdefault("packages", [])
    registry["packages"].append({"id": package["id"], "version": "v44", "checksum": package_checksum})

    registry_path = root / "published-packages.probe.json"
    registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")

    # P5: the design's successor release is renumbered v42, not v41 -- v41
    # is now the real, adopted release (the line 8a debt-limit fix). See the
    # revision note.
    release = _read_json(RELEASE_PATH)
    release["version"] = "v42"
    release_dir = root / "releases"
    release_dir.mkdir()
    release_path = release_dir / "demo.release.sli-worksheet-integration.2025.v42.json"
    release["package_registry_sha256"] = hashlib.sha256(registry_path.read_bytes()).hexdigest()
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
    """The proven P0/P2/P3/P4 base corpus plus this probe's ordinary
    statements, including the two timing questions when ``timing`` is
    supplied. A short-name key omitted from ``timing`` is never asserted --
    it resolves to the package's own ``not-asked`` default, not to a
    value this helper fabricates."""
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

    def add(kind: str, payload: dict[str, object]) -> str:
        act_id = f"demo.f1098.p5.act.{len(acts):03d}"
        acts.append({
            "schema": "act.v1", "act_id": act_id, "kind": kind,
            "actor": USER, "at": f"2026-10-14T13:{len(acts) // 60:02d}:{len(acts) % 60:02d}Z",
            "committed_against": len(acts), "payload": payload,
        })
        return act_id

    add("bundle-adoption", {"bundle": _bundle()})
    resolved_answers = dict(_FAVORABLE_ANSWERS)
    if answers:
        resolved_answers.update(answers)
    finding_ids: dict[str, str] = {}
    for short, value in resolved_answers.items():
        finding_id = f"demo.f1098.p5.{short}"
        add("assertion", {"finding": _attested(finding_id, _member_fact_id_here(FACT + short), value)})
        finding_ids[short] = finding_id
    if timing:
        for short, value in timing.items():
            finding_id = f"demo.f1098.p5.{short}"
            add("assertion", {"finding": _attested(finding_id, _member_fact_id_here(FACT + short), value)})
            finding_ids[short] = finding_id
    return acts


def _probe_acts_with_withdrawn_timing(
    *, withdraw: str, keep: dict[str, str] | None = None,
) -> list[dict[str, object]]:
    """A timing answer given, then withdrawn, within the same run (owner
    finding 1, action 5's "a timing answer withdrawn after it was given").
    ``withdraw`` is the short timing-fact name to assert favourably and then
    retract. The retracted fact must resolve to ``not-asked`` (the
    structural default), never to the missing row other ordinary statements
    fall to -- see section 5's lifecycle note."""
    answers = {"what-the-money-paid-for": "unrelated-personal-expense"}
    timing = {
        "loan-timing-relative-to-purchase": "no",
        "loan-timing-relative-to-building-or-improving": "no",
    }
    if keep:
        timing.update(keep)
    acts = _probe_acts(answers=answers, timing=timing)
    finding_id = f"demo.f1098.p5.{withdraw}"
    act_id = f"demo.f1098.p5.act.{len(acts):03d}"
    acts.append({
        "schema": "act.v1", "act_id": act_id, "kind": "finding-retracted",
        "actor": USER, "at": f"2026-10-14T14:{len(acts) // 60:02d}:{len(acts) % 60:02d}Z",
        "committed_against": len(acts), "payload": {"finding_id": finding_id},
    })
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
    release["version"] = "v42"
    release["checksum"] = release_checksum
    payload["audit"] = {"note": "synthetic P5 design-correction probe; throwaway surface, not adopted content"}
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
    """Case ``determined-zero-reader-gap``: attempt the four-favourable-value
    declaration against the real, unmodified ``build_presentation_model`` /
    ``_favorable_values`` and record what it does. Carried forward from P4,
    unchanged: choice 8's reader fix is specified (section 4, "the third
    reader change"), not built -- no production code changes this round
    either, so the gap this reproduces is unchanged by P5."""
    with TemporaryDirectory() as tmp:
        surface, release_checksum, package_id, package_version, package_checksum = _build_surface(
            Path(tmp), include_duplicate=False, unresolved_widened=True,
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
                    scope_user=USER, request={"schema": "run-request.v1"}, run_id="demo.f1098.p5.determined-zero-reader-gap",
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


def _ordinary_answers_in(acts: list[dict[str, object]]) -> dict[str, object]:
    """Report the ordinary-answer findings actually supplied to the probe."""
    known_answers = {item.removeprefix(FACT) for item in NEW_YES_NO_FACTS}
    known_answers.update({
        WHAT_FOR.removeprefix(FACT), CERT.removeprefix(FACT),
        TIMING_PURCHASE.removeprefix(FACT), TIMING_BUILDING.removeprefix(FACT),
    })
    answers: dict[str, object] = {}
    for row in acts:
        payload = row.get("payload")
        finding = payload.get("finding") if isinstance(payload, dict) else None
        if not isinstance(finding, dict):
            continue
        fact_id = finding.get("fact_id")
        if isinstance(fact_id, str) and fact_id.startswith("tax.us.2025.filing-status|"):
            answers["filing_status"] = finding.get("value")
            continue
        if not isinstance(fact_id, str) or not fact_id.startswith(FACT):
            continue
        short_name = fact_id[len(FACT):].split("|", 1)[0]
        if short_name in known_answers:
            answers[short_name] = finding.get("value")
    return answers


def _set_filing_status(acts: list[dict[str, object]], value: str) -> None:
    """Correct the synthetic filing-status input for the named joint case."""
    for row in acts:
        payload = row.get("payload")
        finding = payload.get("finding") if isinstance(payload, dict) else None
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith("tax.us.2025.filing-status|"):
            finding["value"] = value
            return
    raise AssertionError("the base return has no filing-status finding to correct")


def _append_payment_answer(acts: list[dict[str, object]], value: str, finding_id: str) -> None:
    """Add a same-fact assertion so the coordinator observes its current support."""
    index = len(acts)
    acts.append({
        "schema": "act.v1",
        "act_id": f"demo.f1098.p7.act.{index:03d}",
        "kind": "assertion",
        "actor": USER,
        "at": f"2026-10-14T15:{index // 60:02d}:{index % 60:02d}Z",
        "committed_against": index,
        "payload": {"finding": _attested(finding_id, _member_fact_id_here(FACT + "paid-the-interest"), value)},
    })


def _payment_finding_ids(acts: list[dict[str, object]]) -> list[str]:
    """Return input finding IDs for the exact statement-keyed payment fact."""
    payment_fact_id = _member_fact_id_here(FACT + "paid-the-interest")
    result: list[str] = []
    for row in acts:
        payload = row.get("payload")
        finding = payload.get("finding") if isinstance(payload, dict) else None
        if isinstance(finding, dict) and finding.get("fact_id") == payment_fact_id:
            finding_id = finding.get("id")
            if isinstance(finding_id, str):
                result.append(finding_id)
    return result


def _p7_summary(name: str, observed: dict[str, Any], *, expected: dict[str, Any], acts: list[dict[str, object]]) -> dict[str, Any]:
    """Keep the P7 capture compact while preserving the observations under test."""
    if "exception" in observed or "refusal" in observed:
        return {"case": name, "expected": expected, "observed": observed, "matches": False}
    line8a_values = [row.get("value") for row in observed.get("line8a_publications", [])]
    line8a_state = [
        {key: row[key] for key in ("disposition", "code", "activeCodes") if key in row}
        for row in observed.get("line8a_dispositions", [])
    ]
    support_ids: set[str] = set()
    for collection in ("line8a_publications", "reason_publications", "line8a_dispositions", "reason_dispositions"):
        for row in observed.get(collection, []):
            for pin in row.get("pins", []):
                pin_id = pin.get("id")
                if pin.get("origin") == "assertion" and isinstance(pin_id, str):
                    support_ids.add(pin_id)
    payment_ids = _payment_finding_ids(acts)
    current_payment_id = payment_ids[-1:]  # same fact_id: latest assertion is current
    got = {
        "reason": observed.get("reason_value"),
        "line8a_values": line8a_values,
        "line8a_state": line8a_state,
        "line12e_disposition": observed.get("line12e_disposition"),
        "line12e_value": observed.get("line12e_value"),
        "payment_current_support": sorted(support_ids.intersection(current_payment_id)),
        "displaced_payment_support_absent": sorted(set(payment_ids[:-1]).difference(support_ids)),
        "unresolved_disposition": (observed.get("unresolved_field_resolved") or {}).get("disposition"),
    }
    return {"case": name, "expected": expected, "observed": got, "matches": all(got.get(key) == value for key, value in expected.items())}


def _run_p7_targeted(*, correction_only: bool = False) -> None:
    """Run P7's bounded inputs, or only its same-fact correction sequence."""
    results: list[dict[str, Any]] = []
    with TemporaryDirectory() as tmp:
        surface, release_checksum, package_id, package_version, package_checksum = _build_surface(
            Path(tmp), include_duplicate=False, unresolved_widened=False,
        )

        def run_case(name: str, acts: list[dict[str, object]], *, expected: dict[str, Any], ordinary_answer: str) -> dict[str, Any]:
            built = _finish(
                acts, release_checksum=release_checksum, package_id=package_id,
                package_version=package_version, package_checksum=package_checksum,
            )
            observed = _run(built, f"demo.f1098.p7.{name}", surface)
            observed["ordinary_answer"] = ordinary_answer
            observed["stored_answers"] = _ordinary_answers_in(acts)
            compact = _p7_summary(name, observed, expected=expected, acts=acts)
            compact["ordinary_answer"] = ordinary_answer
            compact["stored_answers"] = observed["stored_answers"]
            return compact

        no_line8a = {"reason": "payment-outside-coverage", "line8a_values": [], "line12e_disposition": "blocked", "line12e_value": None, "unresolved_disposition": "blocked"}
        if not correction_only:
            for case, answer, ordinary in (
                ("payment-other-person-paid-all", "paid-by-others-or-partial", "Someone else paid all of this interest for me."),
                ("payment-partial", "paid-by-others-or-partial", "Someone else paid part of this interest, and I paid only part."),
            ):
                results.append(run_case(
                    case,
                    _probe_acts(answers={"paid-the-interest": answer}),
                    expected=no_line8a,
                    ordinary_answer=ordinary,
                ))
            results.append(run_case(
                "payment-none-by-or-for-filing-unit",
                _probe_acts(answers={"paid-the-interest": "no"}),
                expected={"reason": "not-paid", "line8a_values": ["0"], "line12e_disposition": "published_value", "line12e_value": 15000, "unresolved_disposition": "blocked"},
                ordinary_answer="Neither I nor my spouse paid any of it, and nobody paid any for us.",
            ))
            results.append(run_case(
                "payment-cannot-tell",
                _probe_acts(answers={"paid-the-interest": "cannot-tell"}),
                expected={"reason": "cannot-tell-payment", "line8a_values": [], "line12e_disposition": "blocked", "line12e_value": None, "unresolved_disposition": "blocked"},
                ordinary_answer="I can't tell which payment description applies.",
            ))

        correction_acts = _probe_acts()
        results.append(run_case(
            "payment-correction-supported-start",
            correction_acts,
            expected={"reason": "qualified", "line8a_values": ["20000.0"], "line12e_disposition": "published_value", "line12e_value": 20000, "payment_current_support": ["demo.f1098.p5.paid-the-interest"]},
            ordinary_answer="I paid all of the interest.",
        ))
        _append_payment_answer(correction_acts, "paid-by-others-or-partial", "demo.f1098.p7.payment-corrected-to-partial")
        results.append(run_case(
            "payment-correction-to-outside-coverage",
            correction_acts,
            expected={**no_line8a, "payment_current_support": ["demo.f1098.p7.payment-corrected-to-partial"], "displaced_payment_support_absent": ["demo.f1098.p5.paid-the-interest"]},
            ordinary_answer="Correction: someone else paid some of the interest, and I paid only part.",
        ))
        _append_payment_answer(correction_acts, "yes", "demo.f1098.p7.payment-corrected-back-to-supported")
        results.append(run_case(
            "payment-correction-back-to-supported",
            correction_acts,
            expected={"reason": "qualified", "line8a_values": ["20000.0"], "line12e_disposition": "published_value", "line12e_value": 20000, "payment_current_support": ["demo.f1098.p7.payment-corrected-back-to-supported"], "displaced_payment_support_absent": ["demo.f1098.p5.paid-the-interest", "demo.f1098.p7.payment-corrected-to-partial"]},
            ordinary_answer="Correction: I paid all of the interest.",
        ))

        if not correction_only:
            joint_acts = _probe_acts(answers={"owes-the-loan": "yes", "paid-the-interest": "yes", "no-one-else-owes-it": "yes"})
            _set_filing_status(joint_acts, "married_filing_jointly")
            results.append(run_case(
                "joint-filer-other-spouse-obligor-and-payer",
                joint_acts,
                expected={"reason": "qualified", "line8a_values": ["20000.0"], "line12e_disposition": "published_value", "line12e_value": 30000},
                ordinary_answer="On a joint return, the respondent is not on the note; the other spouse owes the loan and paid all the interest.",
            ))
            results.append(run_case(
                "pub936-example1-investment-other",
                _probe_acts(
                    answers={"what-the-money-paid-for": "other"},
                    timing={"loan-timing-relative-to-purchase": "yes", "loan-timing-relative-to-building-or-improving": "no"},
                ),
                expected={"reason": "outside-coverage", "line8a_values": [], "line12e_disposition": "blocked", "line12e_value": None},
                ordinary_answer="The home was bought 42 days before this loan; the money bought stocks. Stored use: other; purchase timing: yes.",
            ))
    print(json.dumps({"probe": "p7-payment-correction-current-support" if correction_only else "p7-payment-and-fixture-corrections", "results": results}, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p7-targeted", action="store_true", help="run only the P7 payment, MFJ, investment, and correction cases")
    parser.add_argument("--p7-correction-only", action="store_true", help="run only P7's same-fact correction/current-support sequence")
    args = parser.parse_args()
    if args.p7_targeted or args.p7_correction_only:
        _run_p7_targeted(correction_only=args.p7_correction_only)
        return
    results: dict[str, Any] = {}
    favorable_timing = {
        "loan-timing-relative-to-purchase": "no",
        "loan-timing-relative-to-building-or-improving": "no",
    }
    with TemporaryDirectory() as tmp:
        surface, release_checksum, package_id, package_version, package_checksum = _build_surface(
            Path(tmp), include_duplicate=False, unresolved_widened=False,
        )

        def run_case(
            name: str,
            acts: list[dict[str, object]],
            *,
            ordinary_answer: str | None = None,
        ) -> None:
            built = _finish(
                acts, release_checksum=release_checksum, package_id=package_id,
                package_version=package_version, package_checksum=package_checksum,
            )
            observed = _run(built, f"demo.f1098.p5.{name}", surface)
            if ordinary_answer is not None:
                observed["ordinary_answer"] = ordinary_answer
                observed["stored_answers"] = _ordinary_answers_in(acts)
            results[name] = observed

        # --- Baseline carryovers from P4, re-run against the P5-revised rules ---
        run_case("supported-purchase", _probe_acts())
        run_case("box2-over-limit", _probe_acts(box2=800000.0))
        run_case("box9-absent", _probe_acts(box9=None))
        run_case("cannot-tell-use", _probe_acts(answers={"what-the-money-paid-for": "cannot-tell"}))
        run_case("refinance", _probe_acts(answers={"this-is-the-original-loan": "no"}))
        run_case("zero-interest", _probe_acts(box1=0.0))
        run_case("closed-empty", _no_statement_acts())
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
            "owner-not-on-note",
            _probe_acts(answers={"owes-the-loan": "no", "paid-the-interest": "yes"}),
        )
        run_case("not-collateral", _probe_acts(answers={"home-is-collateral": "no"}))
        run_case("not-paid", _probe_acts(answers={"paid-the-interest": "no"}))
        run_case("certificate-received", _probe_acts(answers={"mortgage-credit-certificate-received": "received"}))
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
        run_case(
            "uncertain-ownership-against-refinance",
            _probe_acts(answers={"owns-the-home": "cannot-tell", "this-is-the-original-loan": "no"}),
        )

        # --- Publication 936 (2025) p.12 worked examples (owner finding 2, action 4) ---
        # Example 1: the actual use was to buy stocks. Record `other` and
        # leave the example outside this route; the separate personal-expense
        # cases below continue to probe the purchase timing exception.
        run_case(
            "pub936-example1-investment-other",
            _probe_acts(
                answers={"what-the-money-paid-for": "other"},
                timing={"loan-timing-relative-to-purchase": "yes",
                        "loan-timing-relative-to-building-or-improving": "no"},
            ),
            ordinary_answer="The home was bought 42 days before this loan; the money bought stocks. Stored use: other; purchase timing: yes.",
        )
        # Situation 2: mortgage taken out *before* the building
        # work is completed (dollars from elsewhere financed the work in the
        # meantime), within the 24-months-before-the-mortgage window.
        run_case(
            "pub936-situation2-building-before-completion",
            _probe_acts(
                answers={"what-the-money-paid-for": "unrelated-personal-expense"},
                timing={"loan-timing-relative-to-purchase": "no",
                        "loan-timing-relative-to-building-or-improving": "yes"},
            ),
            ordinary_answer="The loan money was released before the building work was complete. Answer: yes.",
        )
        # Situation 3: mortgage taken out *within 90 days after* the work is
        # completed. The application's single either/or building question
        # does not distinguish situation 2 from situation 3 -- a
        # deliberately wider, conservative window (section 1's design note);
        # both answer "yes" to the same question and reach the same
        # unresolved reason, leaving the precise 24-month expense-window cap
        # with the person either way.
        run_case(
            "pub936-situation3-mortgage-after-completion",
            _probe_acts(
                answers={"what-the-money-paid-for": "unrelated-personal-expense"},
                timing={"loan-timing-relative-to-purchase": "no",
                        "loan-timing-relative-to-building-or-improving": "yes"},
            ),
            ordinary_answer="The home was completed 22 days before this loan. Answer: yes, within 90 days after finishing.",
        )

        # --- P6 correction: exact ordinary completion and purchase wording ---
        for case_name, ordinary_answer, building_answer in (
            ("completion-18-months-before", "The work finished 18 months before this loan. Answer: no.", "no"),
            ("completion-26-months-before-expenses-start-30-months-before", "The work finished 26 months before this loan, though expenses started 30 months before the loan (4 months before completion). Answer: no.", "no"),
            ("work-under-way-at-loan", "The work was still under way when the loan money was released. Answer: yes.", "yes"),
            ("completion-40-months-before", "The work finished 40 months before this loan. Answer: no.", "no"),
            ("completion-exactly-90-days-before", "The work finished exactly 90 days before this loan. Answer: yes, within 90 days after finishing.", "yes"),
            ("completion-91-days-before", "The work finished 91 days before this loan. Answer: no.", "no"),
            ("paused-unfinished-project", "The project was paused and unfinished when this loan's money was released. Answer: yes.", "yes"),
            ("preparation-before-physical-work", "The loan money was released during preparation, before physical work began, and the project was unfinished. Answer: yes.", "yes"),
        ):
            run_case(
                case_name,
                _probe_acts(
                    answers={"what-the-money-paid-for": "unrelated-personal-expense"},
                    timing={"loan-timing-relative-to-purchase": "no",
                            "loan-timing-relative-to-building-or-improving": building_answer},
                ),
                ordinary_answer=ordinary_answer,
            )
        run_case(
            "building-earlier-written-application",
            _probe_acts(
                answers={"what-the-money-paid-for": "unrelated-personal-expense"},
                timing={"loan-timing-relative-to-purchase": "no",
                        "loan-timing-relative-to-building-or-improving": "cannot-tell"},
            ),
            ordinary_answer="An earlier written application could change the timing answer. Answer: can't tell.",
        )
        run_case(
            "purchase-within-90-days-before-home-buying",
            _probe_acts(
                answers={"what-the-money-paid-for": "unrelated-personal-expense"},
                timing={"loan-timing-relative-to-purchase": "yes",
                        "loan-timing-relative-to-building-or-improving": "no"},
            ),
            ordinary_answer="The loan was taken out 45 days before buying the home. Answer: yes, within 90 days before buying.",
        )
        run_case(
            "purchase-within-90-days-after-home-buying",
            _probe_acts(
                answers={"what-the-money-paid-for": "unrelated-personal-expense"},
                timing={"loan-timing-relative-to-purchase": "yes",
                        "loan-timing-relative-to-building-or-improving": "no"},
            ),
            ordinary_answer="The home was bought 45 days before taking out this loan. Answer: yes, within 90 days after buying.",
        )

        # On a joint return the respondent is not on the note, but the other
        # spouse owes the loan and paid the interest. The ordinary question
        # semantics make these filing-unit answers yes, so the existing
        # coordinator conjunction reaches qualified.
        run_case(
            "joint-filer-other-spouse-obligor-and-payer",
            _probe_acts(answers={
                "owes-the-loan": "yes",
                "paid-the-interest": "yes",
                "no-one-else-owes-it": "yes",
            }),
            ordinary_answer="On a joint return, the respondent is not on the note; the other spouse owes the loan and paid the interest. The filing-unit answers are yes, yes, yes.",
        )

        run_case(
            "cannot-tell-collateral-alone",
            _probe_acts(answers={"home-is-collateral": "cannot-tell"}),
            ordinary_answer="I can't tell whether the home is collateral for this loan.",
        )
        run_case(
            "cannot-tell-payment-alone",
            _probe_acts(answers={"paid-the-interest": "cannot-tell"}),
            ordinary_answer="I can't tell whether I or my spouse, if filing jointly, paid this interest.",
        )

        # --- P5 repair: grandfathering (choice 3, action 2) ---
        run_case(
            "personal-expense-grandfathered-on-cutoff",
            _probe_acts(
                answers={"what-the-money-paid-for": "unrelated-personal-expense"}, timing=favorable_timing,
                box3=GRANDFATHER_CUTOFF,
            ),
        )
        run_case(
            "personal-expense-grandfathered-before-cutoff",
            _probe_acts(
                answers={"what-the-money-paid-for": "unrelated-personal-expense"}, timing=favorable_timing,
                box3="1985-01-01",
            ),
        )
        run_case(
            "personal-expense-not-grandfathered-after-cutoff",
            _probe_acts(
                answers={"what-the-money-paid-for": "unrelated-personal-expense"}, timing=favorable_timing,
                box3="1987-10-14",
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

        # --- P5 repair: absent timing answers (owner finding 1, action 3) ---
        run_case(
            "personal-expense-no-timing-answers",
            _probe_acts(answers={"what-the-money-paid-for": "unrelated-personal-expense"}),
        )
        run_case(
            "personal-expense-one-timing-answer-missing",
            _probe_acts(
                answers={"what-the-money-paid-for": "unrelated-personal-expense"},
                timing={"loan-timing-relative-to-purchase": "no"},
            ),
        )
        run_case(
            "personal-expense-timing-withdrawn",
            _probe_acts_with_withdrawn_timing(withdraw="loan-timing-relative-to-purchase"),
        )
        run_case(
            "purchase-account-timing-questions-unasked",
            _probe_acts(),  # == supported-purchase; named separately for action 5's own coverage line
        )

        run_case(
            "personal-expense-uncertain-ownership",
            _probe_acts(
                answers={"what-the-money-paid-for": "unrelated-personal-expense", "owns-the-home": "cannot-tell"},
                timing=favorable_timing,
            ),
        )

        # --- P5 repair: uncertain ownership/residence/share (finding 2, choice 4) ---
        run_case("cannot-tell-ownership-alone", _probe_acts(answers={"owns-the-home": "cannot-tell"}))
        run_case("cannot-tell-residence-alone", _probe_acts(answers={"lives-there-most-of-the-time": "cannot-tell"}))
        run_case("cannot-tell-share-alone", _probe_acts(answers={"no-one-else-owes-it": "cannot-tell"}))

    with TemporaryDirectory() as tmp:
        surface, release_checksum, package_id, package_version, package_checksum = _build_surface(
            Path(tmp), include_duplicate=True, unresolved_widened=False,
        )

        def run_dup(name: str, acts: list[dict[str, object]]) -> None:
            built = _finish(
                acts, release_checksum=release_checksum, package_id=package_id,
                package_version=package_version, package_checksum=package_checksum,
            )
            results[name] = _run(built, f"demo.f1098.p5.{name}", surface)

        run_dup("double-match-zero", _probe_acts(answers={"what-the-money-paid-for": "unrelated-personal-expense"}, timing=favorable_timing))
        run_dup("double-match-qualifying", _probe_acts())

    # --- The reader change this round does not build, probed against the
    # real, unmodified code (unchanged gap from P4). ---
    with TemporaryDirectory() as tmp:
        results["determined-zero-reader-gap"] = _probe_reader_gap(Path(tmp))

    print(json.dumps({"probe": "p5-design-corrections", "results": results}, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
