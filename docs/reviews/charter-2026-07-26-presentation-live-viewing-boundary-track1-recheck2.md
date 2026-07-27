# Charter — Track 1 second focused recheck: ADR-0047 consistency residual

- Role: **Reviewer** (`docs/roles/reviewer.md`) — same Reviewer
- Milestone: `docs/phases/real-return/milestones/presentation-live-viewing-boundary.md`
- Branch: `track/presentation-live-viewing-boundary-track1`
- Repair commit: `08eecb6` (recheck was `a476c40`; first repair `52ef7b0`)

The owner authorized exceeding the plan's stated repair cap for this residual.
No design question was open; the recheck itself characterized it as a
single-line, non-substantive text correction.

## Scope

Measurement 5 only, plus anything the one-paragraph diff directly touches. Do
not re-derive measurements 1–4; the recheck passed them.

## What changed

`docs/adr/0047-live-viewing-environment.md`, threat-posture section:

- "the two silently fatal machine conditions are refused rather than assumed
  away" → states **three**, and separates the two the preflight can always
  decide (backup inclusion, content indexing — refused unconditionally) from
  clipboard-history retention (refused where detectable, owner responsibility
  where not).
- "Class C is open by construction" → "Class C remains open, no substrate having
  been selected or evaluated", matching the framing adopted in the first repair.

## Measurements

`READY` requires both.

1. **Residual closed.** The threat-posture summary now counts the silently fatal
   conditions correctly and states clipboard-history's disposition consistently
   with the Class D and precondition-disposition sections. No surface retains
   the two-condition count.
2. **No new inconsistency or drift.** The reworded paragraph introduces no claim
   absent from the decision sections it summarizes, and the Class C rewording
   does not imply a substrate is available, endorsed, or scheduled. Presentation
   remains L2; the data boundary remains L3.

## Data safety

`python3 tools/envelope_scan.py --range main..HEAD` and `git diff --check`.

## Verdict

`READY` or `NOT READY` with the smallest exact residual. Record at
`docs/reviews/2026-07-26-presentation-live-viewing-boundary-track1-recheck2.md`.
