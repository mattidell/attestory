# Retrospective — Current-Year Capital Losses and Schedule D Line 21

## What differed from the plan

- The owner's initial framing assumed a separately ratified short-term-
  gain-only slice existed as a prerequisite. It did not exist on `main`;
  the owner confirmed this milestone should establish short-term coverage
  and current-year losses together in one bounded slice instead of
  splitting a short-term-gain-only milestone out first. The plan was
  written to that corrected scope.
- Track 0 (paper-first) settled all six named contract questions (D1-D6:
  source families, route selection, signed downstream split, completeness
  successor, line-21 arithmetic, bounded claim) against real committed
  source before any implementation charter existed, per the owner's
  explicit instruction that no Builder should have to choose among
  competing shapes mid-implementation. No rival shape surfaced; both
  successor ADRs (0057, 0058) were ratified as proposed, with no
  amendment.
- Track 1's independent review verified the arithmetic and routing correct
  by direct inspection of the committed rule JSON (the line-21 cap
  formula, the signed line 7a split, the producer-side floor, package
  v14's exclusion of the historical gain-only stack) rather than trusting
  the test suite's own assertions — and found a real mypy error in the
  process (a loop-variable name collision across two differently-typed
  dict iterations in one function, the same bug shape as a prior
  milestone's CI gap). The review also found the test suite itself
  under-covered the charter's own required fixture battery: an untested
  Q>0-with-net-loss QDCG interaction (the specific case ADR-0058's own
  Decision 5 argues for), an undisclosed workaround for a pre-existing
  gap in the demo bracket-tables (MFS/HOH/QSS rows absent), several
  missing named fixtures, and one dead helper.
- One findings-only repair round closed all four findings with
  substantive fixtures — a pin-membership check proving no double-count
  between Schedule D line 16 and the box-2a subtotal, distinct codes for
  present-but-violated versus present-but-missing completeness
  declarations, explicit family-closure-staleness blocking — rather than
  disposition-only rubber-stamping. The recheck was `READY`.
- Track 2 needed no production-code change at all: the existing
  `binds_symbol` presentation projection already carried negative and
  floored-zero values honestly. Its goldens assert actual projected
  numeric values (not just dispositions) for every signed/loss/gain case,
  and the prior milestone's presentation regression suite reran
  unmodified and passed, proving no regression rather than merely
  asserting it. No findings.
- Unlike the prior milestone, no new architecture gap surfaced mid-track;
  Track 0's paper-first discipline (settling contracts before
  implementation, per the owner's explicit instruction after the prior
  milestone) appears to have absorbed the design uncertainty earlier,
  leaving Track 1/2 to implement and to find test-coverage gaps rather
  than design gaps.
- Per explicit owner instruction, the entire milestone stayed local — no
  push, no PR — until this closeout, in contrast to the prior milestone's
  draft-PR-then-curate flow.

## What it cost

- Two ADRs (0057, 0058) drafted and ratified from one paper-first Track 0,
  both Tier 2, both accepted with no amendment.
- Two production tracks (Track 1 with one findings-only repair, Track 2
  clean), each independently reviewed `READY`.
- Final state: the bounded covered, basis-reported, short-term-or-
  long-term, gain-or-loss 2025 Form 1099-B class is synthetic complete —
  signed Schedule D lines 1a/7/8a/15/16, the §1211 current-year loss cap
  (line 21), Form 1040 line 7a/9, the Schedule D-bound QDCG line-16 path
  at any sign of Schedule D's result, package resolution, explanation, and
  presentation — with the historical gain-only family from the prior
  milestone left byte-unchanged and every one of its regression fixtures
  still passing unmodified.

## Follow-ups

- Inbound capital-loss carryovers, Form 8949/noncovered securities/
  adjustments, and other Schedule D sources remain separately selectable
  candidates (deferral ledger entries 5-8). Reactivate each only through
  its own selected source and completeness boundary.
- The demo `tax-brackets`/`qdcg-preferential-brackets` parameter tables
  cover only `single`/`married_filing_jointly`. Any future milestone that
  needs a full live-run golden for another filing status will hit the
  same `LOOKUP_MISS` this milestone's MFS fixture worked around with a
  static parameter-value check. Expanding those tables is a distinct,
  narrow, likely-Tier-1 data-completeness task, not tied to any one
  breadth slice.
- The "settle contracts on paper before chartering implementation"
  discipline (this milestone's Track 0) is worth keeping as the default
  shape for a milestone whose own decision matrix has several genuine
  open questions, rather than letting them surface piecemeal as
  mid-track architecture gaps the way the prior milestone's ADR-0055/0056
  did. It traded a slightly longer planning stage for zero design churn
  during Track 1/2.

## What should change in the next plan

- Independent review continues to catch things foreman-run verification
  alone would not: this milestone's Track 1 review found both a real
  mypy gap the builder's own verification missed and fixture-coverage
  gaps against the charter's own named battery, neither of which a
  passing `pytest` run would have surfaced on its own.
- When a review names findings that are fixture-coverage or disclosure
  gaps rather than design defects, a single findings-only repair round
  with a tightly scoped charter (naming each finding, not just "fix the
  review") closed all of them in one pass with substantive assertions,
  not weaker rubber-stamping — worth keeping as the default repair shape.
