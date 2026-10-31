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

P = "tax.us.2025."

# Known gap: line 2b v8 validator restriction, owner-held. Line 2b v8 publishes the
# taxable-interest total with when=true, and the package validator authorizes a selection
# rule only as line 2b @ v8 with a top-level when of true, so a guard needs a validator
# change first. Nine interest sets still publish a partial sum on v62 (confirmed live in
# tests/test_collect_closure.py). Remove an entry when the guard lands.
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

# Known gap: attachment reads the subtotal directly; next milestone. An attachment citizen
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


def test_safe_by_construction_cases_are_the_counted_sets() -> None:
    for package in (PACKAGE_V61, PACKAGE_V62):
        out = survey(package)
        counted = {e["source_set"] for e in out["inventory"] if e["auto_class"] == "guarded-by-own-count-in-when"}
        assert counted == SAFE_BY_CONSTRUCTION
