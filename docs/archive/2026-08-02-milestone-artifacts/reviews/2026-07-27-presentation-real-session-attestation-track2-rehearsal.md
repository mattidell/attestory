# Track 2 rehearsal record — real browser, synthetic workspace

- Track: 2 of `docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/presentation-real-session-attestation.md`
- Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-27-presentation-real-session-attestation-track2.md`
- Operated by: the **owner**, on the owner's machine. No agent performed this
  track and no agent launched a headed process.
- Date: 2026-07-27
- Code under exercise: `30e502c` on
  `milestone/presentation-real-session-attestation-tracks`
- Workspace: **synthetic.** Description is unrestricted here by charter, and this
  record is written accordingly.
- Filed by the foreman from the owner's report.

## Verdict

**CLEAN PASS.** Track 3's gate opens.

## Both rehearsal gaps are closed

These are the two gaps the Live Session Path milestone recorded honestly and
could not close itself. They are the reason this track exists.

1. **A real headed browser was launched by `open_presentation_session`** — the
   real code path, not a test double of it. Before today, every exercise of this
   path stopped short of a headed process.
2. **The product page was rendered by one.** Not the evaluation fixture:
   `packages/presentation/pages/citation-walk.v1.html`, the file that until now
   was backed only by a normalized diff against the fixture page and a
   `node --check`.

Matrix footnote 5's "Browser path" and "Rehearsal" rows, and the Live Session
Path retrospective's two named gaps, are answered by this track.

## The interrupt path, measured

Track 1's second review found the defect that made this the most valuable thing
Track 2 could do: before `36317be`, Ctrl-C at the prompt left an orphaned headed
browser still displaying the render, plus a `.live-view/session-*` directory
holding that browser's profile and disk cache — residue outliving the preflight's
backup-and-indexing guarantee, which binds only at session *start*.

The owner exercised both endings with the `with` block intact:

| Path | Browser gone | `.live-view` gone |
| --- | --- | --- |
| Happy path teardown | yes | yes |
| Ctrl-C at the prompt | yes | yes |

This is the first human confirmation of that repair. The reviewer had
demonstrated it programmatically against real `launch`; this is the same claim
observed on a real desktop, which is the thing the owner will be relying on
during the real session.

## Nothing found in the page

The product page was read as a reader rather than as a tester — the charter's
third deliberate exercise, and the last opportunity to find a render defect in a
context where it could be described. **No page defects.** No residuals beyond
the four already named in Track 1's second recheck.

That matters more than a clean line usually does. Under ADR-0047 precondition 5
the owner cannot describe a render defect seen during the real session, so a
page defect found *there* would arrive unactionable. This track is where such a
defect was supposed to surface, and none did.

## The one item not covered

**Item 5, the browser-start-failure exercise, was skipped.** The charter offered
it conditionally — "if you can arrange it cheaply" — so this is permitted, not a
deviation. It is recorded as a **named gap** rather than passed over:

> The classified-refusal path has no human confirmation. That a browser that
> fails to start arrives as a stable reason code rather than as a traceback is
> established by tests and by Track 1's review, and not by observation.

This is the vocabulary's own escape hatch, and it remains the least-exercised
part of the session path. It carries forward.

## The one finding

**The runbook is "not very clear, but fine."** The owner is the first human to
use it, and this is exactly the class of finding the charter said was worth as
much as a render defect. It did not obstruct the sitting — the runbook was
followed start to finish and the session completed — so it does not block.

The specific unclarity was **not identified**, and the foreman asked and did not
receive an answer before the records were filed. It is carried as an open
residual rather than closed by guesswork, because a rewrite aimed at the wrong
sentence would be worse than leaving the sentence alone. The next person to use
this runbook — plausibly the owner again, for a second column — should note where
it reads badly at the moment it reads badly.

## Residuals carried in from Track 1, none observed

All four were named to the owner before the sitting so they would not be
rediscovered as defects. None was observed:

1. Teardown failure on an already-failing path is invisible by construction.
2. A genuine programming error during teardown reports as
   `presentation-session-teardown-failed` rather than as itself.
3. A signal landing between `launch` returning and the session object being
   stored is an irreducible Python race.
4. The render/server-start block classifies only expected error types — narrow,
   probably unreachable, not demonstrated impossible.

Plus the owner-held pair that nothing this repository writes can close:
invocation discipline and the `cd` history entry.
