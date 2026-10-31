"""Regression: no new ``collect`` can publish a partial sum on a bound line.

Runs the static survey (``tools/collect_closure_survey.py``, lifted from the milestone's
P0 survey) over a core package. A ``collect`` is acceptable when its source set is
required closed at its own site, or when every path from the subtotal it feeds to a
form-field-bound symbol or attachment citizen passes a rule held for that set (the rule's own ``when``
requires the set closed, or one of its hard ``requires`` is published by a held rule),
or when it is on one of the commented allowlists below. Anything else fails: argue the
new path (guard it or allowlist it with the reason), do not silently allow it.

The check must flag the seven gaps core v62 closed on core v61, and flag none of them on
v62. No run is made; the live cases are in tests/test_collect_closure.py.
"""

from __future__ import annotations

from pathlib import Path

from tools.collect_closure_survey import CONTENT, survey

PACKAGE_V61 = CONTENT / "package.core-calculations.v61.json"
PACKAGE_V62 = CONTENT / "package.core-calculations.v62.json"
PACKAGE_V63 = CONTENT / "package.core-calculations.v63.json"

P = "tax.us.2025."

# Known gap on v62 (pinned history): line 2b v8 publishes the taxable-interest total with
# when=true and cannot take a guard, so nine interest sets still publish a partial sum on v62
# (confirmed live in tests/test_collect_closure.py). Core v63 guards the subtotal rules line
# 2b reads, so the list is empty on v63 (test_core_v63_has_no_unexplained_path_to_a_bound_line).
KNOWN_GAP_LINE_2B = {
    P + s for s in (
        "f1099int.b1", "f1099int.b3", "f1099int.b10", "f1099oid.b1", "f1099oid.b5",
        "non-form-interest", "form1065-k1.box5",
        "scheduleb.adjustment.nominee", "scheduleb.adjustment.abp-adjustment",
    )
}

# The static graph over-approximates (it follows refs in branches that may not run); it
# flags these four although a rule downstream of each appears held on the unclosed set.
# Evidence is uneven, and it is not a compared partial sum for any of them:
#  - f1099k: run live in P0; schedule1-line10 and schedule1-top-entry block
#    SOURCE_SET_UNCLOSED and no bound value moves (reviewer re-ran it).
#  - f1099div.7, f1098e.1: root block only (the harness could not complete an answered
#    return, so no value was compared); they rest on the static reading and that
#    observation. The reviewer could not re-run them (missing same-statement companion).
#  - f1099int.b8: P0 saw line 2a held, with a flipped declaration; the reviewer could not
#    re-run it. It rests on the static reading and that observation.
HELD_DOWNSTREAM = {
    P + "f1099int.b8",   # form1040-line2a
    P + "f1099div.7",    # schedule3-line1-direct-ftc
    P + "f1099k",        # schedule1-line10, schedule1-top-entry
    P + "f1098e.1",      # sli-worksheet
}

# Known gap on v62 (pinned history), closed on v63 except KNOWN_GAP_ATTACHMENTS_V63 below.
# An attachment citizen
# (attachment.schedule-d, schedule-1, schedule-b, f8949) is a published output like a
# form-field-bound line, and it reads these subtotals without the closure guard the bound
# lines now carry. Found by the extended survey on core v62 (24 source sets). The
# nine line 2b interest sets also appear here, through Schedule B and Schedule 1.
KNOWN_GAP_ATTACHMENTS = {
    P + s for s in (
        # Schedule D reads the four non-wash 1099-B basis and proceeds subtotals
        "f1099b.covered-lt-basis", "f1099b.covered-lt-proceeds",
        "f1099b.covered-st-basis", "f1099b.covered-st-proceeds",
        # Form 8949 / Schedule D read the wash-sale sets (closure forced by member
        # validation, but the attachment itemization is not checked)
        "f1099b.covered-w-lt-adjustment", "f1099b.covered-w-lt-basis", "f1099b.covered-w-lt-proceeds",
        "f1099b.covered-w-st-adjustment", "f1099b.covered-w-st-basis", "f1099b.covered-w-st-proceeds",
        # Schedule 1 reads unemployment compensation (box 1)
        "f1099g.1",
        # Schedule B reads dividend box 1a
        "f1099div.1a",
        # Schedule 1 and Schedule B read the interest sets and the adjustments
        "f1099int.b1", "f1099int.b3", "f1099int.b10", "f1099int.b8", "f1099oid.b1", "f1099oid.b5",
        "non-form-interest", "form1065-k1.box5",
        "scheduleb.adjustment.nominee", "scheduleb.adjustment.abp-adjustment",
        # Schedule 1 reads Form 1099-K and the student loan interest worksheet
        "f1099k", "f1098e.1",
    )
}

# What still reaches an attachment unguarded on v63, each with its reason. Core v63 guards the
# subtotal rules the other 20 sets feed (tests/test_attachment_closure.py).
KNOWN_GAP_ATTACHMENTS_V63 = {
    # Schedule B reads dividend box 1a; its requirement reads dividends.ordinary-total, which
    # the guarded line 3b rule holds. Pinned live (test_held_set_publishes_no_attachment_amount_on_v63).
    P + "f1099div.1a",
    # Schedule 1 reads Form 1099-K; its requirement reads schedule1.top-entry (guarded). Pinned live.
    P + "f1099k",
    # Schedule 1 reads the student loan worksheet; its deduction rule is held by the guarded
    # sli-worksheet. Pinned live.
    P + "f1098e.1",
    # Form 1099-INT box 8: no attachment amount. Schedule 1 itemizes only f1099g.1, f1098e.1
    # and f1099k; box 8 reaches it through the SLI deduction chain that line 2a and the
    # worksheet already hold. Rests on the static read only: a live box 8 case blocks the whole
    # return with DEPENDENCY_ABSENT on both cores, so it is unconfirmed either way.
    P + "f1099int.b8",
}

# Safe by construction: the rule's own when evaluates a count over the set first, and count
# raises SOURCE_SET_UNCLOSED unless the set is closed.
SAFE_BY_CONSTRUCTION = {P + "w2-box2", P + "w2-box4", P + "w2-box6"}

CLOSED_BY_V62 = {
    P + s for s in (
        "f1099div.2a", "f1099r.ira-fully-taxable", "ssa1099.benefits",
        "f1099b.covered-lt-basis", "f1099b.covered-lt-proceeds",
        "f1099b.covered-st-basis", "f1099b.covered-st-proceeds",
    )
}


def _flagged(package: Path) -> set[str]:
    """Source sets whose subtotal reaches a bound field without passing a held rule."""
    out = survey(package)
    return {
        e["source_set"] for e in out["inventory"]
        if e["auto_class"] == "unguarded" and e["reaches_bound_fields_unguarded"]
    }


def _flagged_attachments(package: Path) -> set[str]:
    """Source sets whose subtotal reaches an attachment citizen without passing a held rule."""
    out = survey(package)
    return {e["source_set"] for e in out["inventory"] if e["reaches_attachments_unguarded"]}


def _unexplained(flagged: set[str]) -> set[str]:
    return flagged - KNOWN_GAP_LINE_2B - HELD_DOWNSTREAM


def test_the_check_finds_the_seven_gaps_on_core_v61() -> None:
    assert _unexplained(_flagged(PACKAGE_V61)) == CLOSED_BY_V62


def test_core_v62_has_no_unexplained_path_to_a_bound_line() -> None:
    assert _unexplained(_flagged(PACKAGE_V62)) == set()


def test_the_check_finds_new_attachment_paths_on_core_v61() -> None:
    # 2a and the 1099-R line 4b family reach Schedule D / Schedule 1 on v61 and are held on v62.
    found = _flagged_attachments(PACKAGE_V61) - KNOWN_GAP_ATTACHMENTS
    assert found == {P + "f1099div.2a", P + "f1099r.ira-fully-taxable"}


def test_core_v62_has_no_unexplained_path_to_an_attachment() -> None:
    assert _flagged_attachments(PACKAGE_V62) - KNOWN_GAP_ATTACHMENTS == set()


def test_the_allowlists_have_not_gone_stale() -> None:
    flagged = _flagged(PACKAGE_V62)
    assert KNOWN_GAP_LINE_2B <= flagged
    assert HELD_DOWNSTREAM <= flagged
    assert _flagged_attachments(PACKAGE_V62) == KNOWN_GAP_ATTACHMENTS


def test_core_v63_has_no_unexplained_path_to_a_bound_line() -> None:
    # The line 2b known-gap list is empty on v63: nothing but the held-downstream sets remains.
    assert _flagged(PACKAGE_V63) - HELD_DOWNSTREAM == set()
    assert HELD_DOWNSTREAM <= _flagged(PACKAGE_V63)


def test_core_v63_attachment_known_gaps_are_exactly_what_remains() -> None:
    assert _flagged_attachments(PACKAGE_V63) == KNOWN_GAP_ATTACHMENTS_V63
    assert KNOWN_GAP_ATTACHMENTS_V63 < KNOWN_GAP_ATTACHMENTS


def test_safe_by_construction_cases_are_the_counted_sets() -> None:
    for package in (PACKAGE_V61, PACKAGE_V62, PACKAGE_V63):
        out = survey(package)
        counted = {e["source_set"] for e in out["inventory"] if e["auto_class"] == "guarded-by-own-count-in-when"}
        assert counted == SAFE_BY_CONSTRUCTION
