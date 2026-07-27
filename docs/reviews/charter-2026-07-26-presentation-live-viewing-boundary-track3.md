# Charter — Track 3: capability-state records and handoff

- Role: **Builder** (`docs/roles/builder.md`), records only
- Milestone: `docs/phases/real-return/milestones/presentation-live-viewing-boundary.md`
- Base: `main` after the Track 2 PR merges. Verify the commit SHA before starting.

## Goal

Record the state this milestone actually reached — no more. The central
discipline of this milestone has been not claiming more than was proven, in
both directions; the closing records are where that discipline is easiest to
lose, because a milestone that shipped a working vehicle reads like a milestone
that lifted a level.

**It did not.** Presentation stays **L2**. The data boundary stays **L3**.

## What must be recorded

1. **Maturity matrix** (`docs/phases/real-return/maturity-matrix.md`).
   Presentation's row stays at L2 with its footnote updated to state what now
   exists and what still does not: a confined headed invocation vehicle and a
   fail-closed preflight exist and are synthetic-tested; no real workspace has
   been exercised, no viewing session has been performed, no owner attestation
   has been made. Do not edit the level. Footnote 8 (ADR-0044's absent
   mechanical authority separation) is unchanged and still holds the
   data-boundary row.

   Update the "frontier reading" item that said the repository "has no
   data-boundary-safe live browser invocation vehicle" — that clause is now
   false, and the remaining gap is real operation plus attestation, not the
   vehicle.

2. **ADR-0047's residuals carried forward.** The named Class C residual —
   no enforcement substrate selected, prototyped, or verified, with Seatbelt an
   unevaluated candidate — belongs in whatever ledger the project uses for
   reactivation triggers, routed to ADR-0044's future implementation gate
   rather than to Presentation.

3. **Retrospective.** File it where this phase's retrospectives live. The two
   findings worth carrying are substantive, not procedural: (a) the plan's
   original vehicle-first shape was rejected on security first principles
   *before* building, at the owner's prompting, which is the correction the
   Guarded Transport milestone paid for the hard way; and (b) the milestone
   twice caught claim-discipline errors — once an overclaim in the negative
   direction (asserting platform impossibility where the platform was merely
   unevaluated), once a missing regression guard on the input where a caveat
   looks like dead weight.

4. **Phase-state and roadmap pointers.** Advance to milestone-complete, clear
   the active charter pointer, and remove the milestone capsule per the usual
   close-out. Leave the next milestone unselected — that is the owner's call.

## Hard constraints

- **No maturity lift.** Any edit that raises a level, or that reads as raising
  one, is out of scope. If the evidence seems to support a lift, stop and say
  so rather than making it.
- **No implementation change.** Records only. If you find a defect, report it;
  do not repair it under this charter.
- **No next-milestone selection or recommendation framed as a decision.**
- **No locator, path fragment, or machine detail** in any record.

## Verification

```text
python3 -m unittest tests.test_presentation_live_viewing_vehicle
python3 -m unittest tests.test_presentation_l2_integration
python3 tools/envelope_scan.py --range main..HEAD
git diff --check
```

Every commit SHA cited in a record must resolve. Check them; the execution
record's evidence chain is the milestone's durable value and a broken link in
it is a real defect.

## Data safety

Synthetic Git/CI evidence only. Range envelope scan before hand-off.
