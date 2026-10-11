# Retrospective — Returning to a Saved Account

## What differed from the plan

The plan expected the hard question to be what durable records could prove
after a restart. P0 answered it quickly:

- **The log** survives a `SIGKILL` byte for byte. It carries each
  correction's predecessor.
- **A fresh process** can calculate from it without appending an act.
- **No saved result** can be shown to describe the current answers. Its
  revision is whatever its caller passed. Nothing records the calculation
  surface or a digest of the acts.

The selected route therefore never reuses a saved result as current. It shows
the latest one as an earlier result and offers a fresh calculation. That
needed an opener, a calculate action and session-bound tokens. It needed no
store, schema or ADR.

The plan was wrong in one place. It put persistent synthetic workspaces under
the repository's ignored paths, but the residency check refuses any location
inside the repository (ADR 0031). R1 confirmed the conflict, and the plan was
corrected.

Track 0 also met a naming problem. "Current" already means authorization
standing under ADR 0069, and every synthetic run records
`AUTHORIZATION_ABSENT`. A returning page that called a result "current" would
contradict its own output file.

The reviews changed the route in four ways:

- **R2.** It refused a draft that would have calculated the opening result
  from a caller-supplied revision. It found that the latest standing is not
  the latest completed run. It also found that the page would have shown
  "Not saved" for an old token whose correction had in fact been saved.
- **R3.** It ran the integrated interaction. It found that the session's own
  new result was headed as "earlier". It also found that an earlier result
  still labelled a superseded answer "Current".
- **R4.** It found that the second process ever to calculate on a workspace
  failed silently. Its output name came from a per-process serial that
  restarts at 1, and it collided with an earlier process's reserved file.
  The broad exception handler then reported it as "did not calculate".
- **R4's empty-file note.** An interrupted run's empty output reservation
  marked every later result in that workspace as damaged.
- **The owner's review of the curated candidate.** It found two more:
  - a calculation whose response was lost was reported as not done, though
    the session held its result;
  - an earlier explanation that parsed but could not be interpreted hid the
    whole account. A milder form of the same damage rendered an incomplete
    explanation as whole.

## What it cost

- **Reviews before production:** R1 on P0 and the plan, and R2 on the Track 0
  draft. No P1 probe was needed.
- **Track 1:** one build and the integrated review R3.
- **Track 2:** one build, R3's corrections, review R4 and one foreman repair.
- **Models:** P0, R1, R2, Track 1 and R3 ran on Grok, for about $8.40 in total.
  Track 2 and R4 ran as Sonnet agents, as the owner directed partway through.
  The Track 2 builder hit the weekly limit after its three commits. The
  foreman completed its checks without re-dispatching.
- **Full suite:** about 23–25 minutes locally. One neighboring headless-Chrome
  screenshot test timed out under load and passed alone.

## Follow-ups

- **Owner visual check and wording.** The owner has the screen-by-screen
  walkthrough. The static note "This reviews one saved result" and the
  first-run heading "Earlier result (line 21) — unchanged" were not revisited.
- **Independent reader assessment.** It is still not performed for this
  interaction or its predecessor.
- **A calculation that fails before its run starts** leaves no trace, so the
  reopened page cannot say it happened. Recording it would need a durable
  write this milestone did not select.
- **Real workspaces** still need the residency path and an owner decision.
- **AGENTS.md's test-lane timings** remain out of date. The full suite takes
  over twenty minutes.

## What should change in the next plan

Any identifier a process mints must be unique across the lifetime of the
files it names, not only the lifetime of the process. A per-process counter
is safe in memory and unsafe on disk. The defect was invisible to every test
that used one process per workspace. When an interaction crosses a restart,
test each action twice across two processes on the same files.

A broad exception handler that turns every failure into a calm sentence also
hides defects. Keep the fixed sentence for the person. Test the failure
classes that can occur, so a collision shows up as a test failure rather than
as "did not calculate".

Keep two pairs of failures apart all the way to what the person sees:
- failing to receive a result, and failing to produce it;
- failing to read an explanation, and failing to recover the account.

A transport error is not a refusal: ask the session what it holds before
saying anything. An explanation is evidence about one result. When it cannot
be read whole, show none of it and keep the account. Checking only that a
file parses is not enough.

Ask what a crashed process leaves behind, as well as what a completed one
does. Empty reservations, started records without a close, and partial files
are ordinary leftovers. A reader that treats them as damage degrades every
later state of the same workspace.
