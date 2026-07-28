# Retrospective: Presentation — Completing the Row

Phase: Real Return. Completed 2026-07-28.
Plan: `docs/phases/real-return/milestones/presentation-row-completion.md`.

**Result: the Presentation row is L3 across all five columns, and every cell in
the maturity matrix is now L3 or better.** No session was performed, no browser
launched, no real data touched, and no code changed.

## What this milestone actually did

It raised four cells by asking the owner one question the repository cannot
answer: *which columns did you observe during the session you already ran?*

All four were named, so all four moved. The whole milestone is one owner
statement and one records pass.

## The interesting decision was the owner's, and I argued the wrong side

Offered four frontiers, the owner picked finishing the Presentation row. My
recommendation was a "define the outcome frontier" milestone — work out what
*done* means for the user's real job, filing, and whether the matrix needed a row
it did not have.

The owner's rebuttal was better than the proposal: **the phase is Real Return
with a defined slice, and completing the slice you defined before starting a new
one is the coherent move.** Both of my alternatives quietly changed the phase's
scope — breadth by widening the slice, "outcome frontier" by redefining the axes
mid-phase. Filing is a next-phase question, which is where the owner put it.

The argument for finishing that I failed to make: **completing the row leaves the
matrix uniformly L3, which is a legible phase boundary.** A half-lifted row is a
bad place to start a new phase from. That is a stronger case than either option I
pitched, and it came from taking the phase's own definition seriously rather than
looking for a more interesting question.

Worth keeping: a planning instrument's completeness is itself a product signal.
Leaving a row ragged because the remaining cells look like ceremony trades a
clean boundary for a small saving.

## Where the care went

Almost all of it into one failure mode: **a row filled in over two days by two
milestones invites the reading that several sessions occurred.** There has been
exactly one, on 2026-07-27.

That reading is foreclosed in four places rather than left to inference — the
matrix header, footnote 15's opening line, the attestation amendment, and this
retrospective. It is the kind of thing that is free to prevent now and impossible
to correct later, because the misreading would be reasonable: nothing about the
shape of a completed row says how many acts filled it.

## The control that did not fire

The plan specified that **a column the owner did not name would not move**, and
that closing with three cells raised would be a success rather than a failure.

All four were named, so the control never fired. It was still real, and it is
the reason the milestone asked for four sentences instead of inferring
observation from the render. ADR-0031 Decision 7's shape includes that the owner
**observed dispositions in quarantine** — naming a column asserts observation of
it, and no amount of rendering establishes that a person looked.

The distinction that keeps this honest: **observing a column is not auditing
it.** L3 asserts the capability operated. Footnotes 7 and 11 have said so since
2026-07-18, and an amendment is exactly where that would erode if nobody
restated it.

## One check made rather than inherited

The plan verified directly that the surface covers all five columns — the
production-shaped fixture's sections and its Schedule B Parts I/II citation
group, and `_resolve_attachment` projecting attachments into the model — instead
of accepting the previous milestone's "no build gap."

That previous closeout said the same thing, and Track 1 then found three code
defects. The check cost two commands. It confirmed the claim this time, which is
the outcome that makes it tempting to skip next time.

## What did not close

Both need a session to exercise, and this milestone performed none:

1. **The classified-refusal path has no human confirmation.** That a browser
   which fails to start arrives as a stable reason code rather than a traceback
   rests on tests and independent review only. It is now **the oldest open item
   on this path**, first named when Track 2's browser-start-failure exercise was
   skipped on 2026-07-27.
2. **The session runbook has an unidentified unclarity**, reported by its first
   human user with the sentence unnamed.

Neither concerns the capability that operated; both concern the failure path and
the instructions. They follow into the next phase named, so they are not lost
along with the row that carried them.

## Phase recommendation

**Real Return should close.** Its roadmap sets no ladder and one standing test —
*"does the product now do something for its user that it could not do before?"*
— and that test is met: the system holds and computes the owner's real data,
explains it with citations, and now shows it to them on a human surface that has
really operated.

Every cell is L3 or better, so frontier-driven selection has no frontier left
inside these five columns. The matrix's silence is the argument.

**Read the completion accurately.** It is breadth- and hardening-limited by
construction: five income/return domains, one implemented schedule, one human
surface, one real viewing session behind the entire Presentation row. It is not a
claim that the product is finished for its user — the user still cannot file
anything. That gap is invisible to every cell in the grid, because no row is
named for it, and it is the natural subject of whatever comes next.

The decision is the owner's (Tier 3).

## Pointers

- Attestation and its amendment:
  `docs/reviews/2026-07-27-presentation-real-session-attestation-track3-attestation.md`.
- Maturity movement: `docs/phases/real-return/maturity-matrix.md`, footnote 15.
- Prior milestone (the session itself):
  `docs/milestone-retrospectives/2026-07-27-presentation-real-session-attestation.md`.
