# Charter — Track 2: real-browser rehearsal against a synthetic workspace

- Role: **Owner-operated.** No agent performs this track and no agent launches a headed process.
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/presentation-real-session-attestation.md`
- Base: `milestone/presentation-real-session-attestation-tracks`, Track 1 complete
- Runbook: `docs/runbooks/presentation-real-session.md`

## Purpose

Close the two rehearsal gaps the previous milestone recorded honestly and could
not close itself:

1. **No real browser has ever been launched by this path.**
2. **The product page has never been rendered by one** — it is a
   three-text-change copy of the evaluation fixture page, and only a normalized
   diff and a `node --check` stand behind it.

This track exists so that the first real render is not also the real session.
**Everything here runs against a synthetic workspace**, where anything found is
fully describable and fully repairable. That is the whole point: this is where
render defects are supposed to be caught, because here you may say exactly what
you saw.

## What to do

Follow `docs/runbooks/presentation-real-session.md` start to finish, pointed at
a **synthetic** workspace rather than the real residency. The runbook is
rehearsed alongside the session — if an instruction is wrong, unclear, or
arrives in the wrong order, that is a finding of this track and is worth as much
as a render defect.

Then, beyond a clean pass, deliberately exercise the paths Track 1's review
turned up, because none of them have been exercised by a human:

- **Interrupt it.** Ctrl-C at the prompt, with the `with` block intact. Confirm
  what Step 5 says you should confirm: no surviving browser window, no surviving
  `.live-view` directory. The previous milestone's rehearsal drove the happy
  path and three designed refusals; it never drove a human ending the program
  early, and that turned out to be where the defect was.
- **Let the browser fail to start**, if you can arrange it cheaply, and check
  the refusal arrives as a stable reason code rather than a traceback.
- **Read the product page as a reader, not as a tester.** It has never been
  looked at by a person in a browser. Does it say what it should? Is anything
  mislabelled, missing, or misleading? This is the last opportunity to find that
  in a context where you can describe it.

## What this track is not

- **Not the real session.** No real residency, no real data, no attestation.
- **Not a gate you may skip.** Track 3 does not begin unless this passes
  cleanly. If it does not, the finding is repaired and this track is repeated —
  that gate is the reason the track exists.

## Data safety

Synthetic workspace only. Because nothing here is the owner's real data,
**description is unrestricted** — the non-descriptive vocabulary does not apply
to this track, and you should describe freely and in detail. Note that the
runbook's own rules about not putting an absolute local path into Git, a review,
or a PR still apply to the synthetic workspace's path as ordinary hygiene, but
no boundary is at stake.

## What to report

Enough that the record proves something:

- That a real headed browser was launched by `open_presentation_session`, and
  that it rendered the **product** page — not the evaluation fixture.
- What the interrupt path actually left behind, measured rather than assumed.
- Any defect in the page, the runbook, or the session path, described in full.
- Anything the runbook told you to do that you could not do, or that read
  differently in the moment than it did on the page.

The foreman files the rehearsal record from your report.

## Residuals carried in from Track 1

Named so they are not rediscovered as defects:

- Teardown failure on an already-failing path is invisible by construction.
- A genuine programming error during teardown reports as
  `presentation-session-teardown-failed` rather than as itself.
- A signal landing between `launch` returning and the session object being
  stored is an irreducible Python race.
- The render/server-start block classifies only expected error types; narrow,
  probably unreachable, not demonstrated impossible.
- Invocation discipline and the `cd` history entry are owner-held and not
  closeable by anything this repository can write.
