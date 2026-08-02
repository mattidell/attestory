# Charter — The Entry Loop (synthetic), Track 1 review: the W-2 entry loop

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Under review: `2a00193` — 14 files, ~7,170 insertions
- Builder charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-29-entry-loop-synthetic-track1.md`
- Verdict: `READY` or `NOT READY`, with numbered findings.

## What landed

The first product build of the phase: a five-step W-2 entry loop on a synthetic
workspace, shipped through its own published surface artifact, with a loopback
runtime that admits browser-originated `act-contribution.v1` events through the
existing contribution applicator and act log and recomputes through
`live_coordinate_run`.

## What you are not doing

**You are not scoring the usability criteria.** That is Track 2, it uses two
independent evaluators under a fixed procedure, and doing it here would preempt
it and contaminate the result. Read
`docs/phases/legible-entry/entry-usability-criteria.md` for context on what the
surface is trying to be, then leave the scoring alone.

Your job is whether the thing is correct, honest, and inside its boundaries.

## Measurements

**1. Are the Phase A dependency tests non-vacuous?**
`tests/test_entry_loop_t1.py` carries four tests named for the four run
dependencies. They are the milestone's protection against building on an
unchecked premise, and a test that passes without proving its claim is worse
than no test — it converts an open question into a false confirmation. For each:
does it prove what its name says? Try to make each fail by mutating the thing it
guards. Dependency 4 in particular asserts a mutation pattern across nine named
Form 1040 lines; check it would actually catch a line that failed to move.

**2. Does anything write a fact?** ADR-0048's core decision is that an entry
surface emits `act-contribution.v1` through the existing admission path and
never writes facts itself. Trace the write path from the browser POST to the act
log. Look specifically for a shortcut — a direct write, a bypassed validation, a
second admission route added for convenience. This is the decision the milestone
rests on.

**3. Is the ADR-0049 route reused or reimplemented?** The surface ships in a
published surface artifact with its own adoption, off the same release and
registry chain. Check it reuses `surface_resolver` rather than carrying a
parallel verification path, and that `artifact-package.v4` is untouched.

**4. The novel boundary: a loopback endpoint that accepts typed input.** This is
new to the project. Everything before it displayed; this accepts a POST from a
browser and turns it into a contribution. Spend real effort here. Does it bind
loopback only? What happens to malformed, oversized, wrongly-typed, duplicated,
or out-of-order input? Does it fail closed? Is a rejected value echoed back
anywhere — ADR-0046's blanket redaction, which the criteria carried over to
entry? Can anything reach the act log that did not pass the existing applicator?

**5. Data safety.** Synthetic only, and no residency locator in any surface:
logs, request paths, subprocess arguments, diagnostics, error text, or test
names. Run the scan, then read for what a scan cannot see. The generated
manifest is large; confirm what is in it is what it claims to be.

**6. Did the preflight get quietly extended?** The builder charter forbade it and
said an extension is a finding for a later milestone. Check whether the entry
session relies on a viewing preflight guarantee that does not actually bind at
entry time, and whether ADR-0048's undesigned spellcheck flag was addressed,
noted, or silently skipped.

**7. Scope.** No per-field explanation schema designed up front — the fields may
be built, but the representation is Track 3's to record. No refusal UI for
corrections, which cannot be refused while every fact type ships `free`. W-2
only. No new tax rule, no derivation package change, no matrix movement.

**8. Test coverage against the size of the change.** Roughly 1,550 lines of
hand-written source arrived with 316 lines of tests. Say whether the coverage is
proportionate and name what is untested that matters.

**9. Verification.** `2a00193` records the full sequence with no omissions.
Re-run it and say whether the claims hold.

## Boundaries

- Do not fix anything. Report findings; repair is a separate charter.
- Do not score usability criteria.
- Do not extend the surface or its tests.
- No maturity claim; nothing moves on any matrix.

## Verdict

`READY` or `NOT READY`. Number each finding, state what is wrong and what would
close it, and separate findings that block from findings that weaken.

## Report back

The verdict; each measurement; which dependency tests you tried to break and
how; what you found at the POST boundary; and the single thing most likely to
be wrong that you could not prove either way.
