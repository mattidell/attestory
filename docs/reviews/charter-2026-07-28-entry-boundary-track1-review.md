# Charter — Entry Boundary, Track 1 review: the retention probe

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-boundary.md`
- Builder charter: `docs/reviews/charter-2026-07-28-entry-boundary-track1.md`
- Branch: `milestone/entry-boundary`, reviewed commit `a33458a`
- Findings under review:
  `docs/phases/legible-entry/milestones/entry-boundary-retention-findings.md`
- Probe: `tools/entry_probe/`

## What the track claims

That a browser driven through the project's confined vehicle, typed into with
synthetic tokens, retained none of them on disk and sent none of them over the
network. Form history did not fire. Spellcheck did not contact a service.
Crash-recovery files were written but held no typed value.

Those observations feed Track 2, which decides whether a browser form is an
acceptable place for a person to enter real tax facts. If the observations are
sound, that decision has evidence. If they are artifacts of how the probe was
set up, the decision would rest on a false negative — the worst available
outcome, because a false negative here reads as permission.

## The measurement that matters most

**The foreman's charter named the wrong vehicle, and the Builder followed it
correctly.** This is a charter defect, not a build defect. Say so plainly in
your report and do not grade the Builder down for it.

There are two confined browser vehicles in this repository:

- `tools/presentation_harness/lib/chrome.mjs` — hardcodes `--headless=new`
  (line 80). This is the synthetic evaluation harness. The probe drove this one,
  because the charter named it.
- `packages/derivation/live_viewing.py` — the **headed** vehicle, which is what
  ADR-0047 defined and what a person actually looks at and would type into.

Headless Chrome disables or stubs a number of the exact features this probe was
built to detect — autofill and form history among them. So "form history:
observed not fired" may be a fact about headless mode rather than a fact about
the confinement, and the note's own reasoning cannot distinguish the two.

**Measurement 1.** Determine whether each "not fired" result is a property of
the confinement or an artifact of headless mode. Be concrete per channel — the
answer may differ between form history, spellcheck, and session restore. Where
you cannot settle it by reading, say that the channel is undetermined rather
than guessing in either direction.

**Measurement 2.** Determine whether `live_viewing.py`'s headed vehicle can be
driven against a **synthetic** workspace, with no real residency and no real
fact. Read it and report what you find: what it requires to launch, whether
those requirements can be met synthetically, and what would have to change if
they cannot. This is a read-only investigation. **Do not modify it, do not run
it against anything real, and do not build a second probe.** The question is
whether a corrected Track 1 is cheap, expensive, or blocked.

## The other measurements

**Measurement 3 — is the negative result trustworthy on its own terms?** The
Builder caught two method errors (a `grep -rlaI` flag combination that silently
suppressed binary-store matches, and a CDP typing artifact that double-inserted
characters) and used a positive control to verify the fix. Check that the
positive control actually proves what it is claimed to prove, and that every
finding in the note post-dates the correction. A probe that cannot find a token
it planted itself produces "not fired" for every channel.

**Measurement 4 — does the note stay inside its evidence ceiling?** It should
report observations and reach no conclusion about whether a browser form is
acceptable or which write path to use. Flag any sentence that leans toward a
verdict Track 2 has not made yet, including by implication or framing.

**Measurement 5 — boundary compliance.** No real workspace, no residency
locator, no path fragment or derived identifier anywhere in the probe, the note,
or the commit. Synthetic tokens must not resemble real personal data. The probe
must not be wired into CI or any existing suite. `chrome.mjs` and `server.mjs`
must be unmodified — verify against base rather than taking the claim.

**Measurement 6 — is "untested" honest?** Three items are recorded as untested:
the restore-session prompt on relaunch, cloud spellcheck, and dictation. Confirm
each is genuinely untestable within charter scope rather than merely
inconvenient, and that nothing else was quietly left out.

## Verdict

`READY` requires measurements 3 through 6 to pass and measurements 1 and 2 to be
answered — answered, not passed. Measurement 1 may legitimately conclude that
the results are artifacts; that is a useful answer and does not by itself make
the track `NOT READY`, because the Builder built what it was chartered to build.

State clearly which of these the foreman is facing:

- The findings stand as evidence for Track 2 as they are.
- The findings stand only for headless mode, and Track 1 needs a second run
  against the headed vehicle before Track 2 can use them.
- The headed vehicle cannot be driven synthetically, so the milestone has a
  question it did not anticipate.

Write your review to
`docs/reviews/2026-07-28-entry-boundary-track1-review.md`. Do not repair
anything yourself.
