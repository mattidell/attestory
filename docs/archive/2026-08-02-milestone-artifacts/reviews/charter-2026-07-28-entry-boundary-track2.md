# Charter — Entry Boundary, Track 2: ADR-0048

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-boundary.md`
- Branch: `milestone/entry-boundary` (Track 1 `a33458a`, review `367de61`,
  Track 1b `513ff93`)
- Deliverable: `docs/adr/0048-entry-boundary.md`, plus its `docs/adr/INDEX.md`
  row. Proposed, not ratified — ratification is the owner's.

## The two questions

**1. Is a browser form an acceptable place for a person to type real tax
facts?**

**2. Does an entry surface write facts directly, or emit contribution events
through the existing boundary (ADR-0032)?**

"No" to question 1 is a real answer. If you reach it, say it. The milestone is
not a failure in that case — it is a decision that saves building the wrong
thing.

## What the evidence says, and what it does not

Read `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-boundary-retention-findings.md`
and `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-28-entry-boundary-track1-review.md` in full.

The probe found nothing retained and nothing sent, in both headless and headed
mode. Do not lean on that as hard as it invites. Two channels are narrowed but
not closed:

- Chrome generally saves form data only after a user accepts a "Save this
  info?" prompt. The probe never drove that prompt to a yes.
- Enhanced spellcheck sends typed text to a service. It is opt-in and was off.

So "not fired" partly means "the conditions that make it fire were not
created." An ADR resting on those observations would rest on a false negative,
and a false negative here reads as permission.

## The argument the owner has directed you to make instead

**Rest the decision on confinement, not on observed browser restraint.**

The foreman verified the following and you should verify it again rather than
taking it from this charter:

- `packages/derivation/live_viewing.py` creates the browser profile inside a
  confined session root (`_ConfinedDestinations`), under the workspace.
- `LiveViewingSession.close()` calls `_remove_session()`, which `rmtree`s that
  session root.
- A teardown that fails raises `BROWSER_TEARDOWN_FAILED` rather than passing
  quietly.

Two consequences to reason about, and they are not the same:

**Disposal.** Anything the browser writes about typed text dies with the
profile on a normal close. This does not depend on Chrome choosing not to
retain, which is what makes it a better foundation than the probe results.

**Confinement, which is the stronger of the two.** The profile is inside the
residency. So even text that *is* retained was retained inside the boundary the
product already defines and already treats as the place real data lives. It
never crossed anything. Work out whether that is right, and if it is, say it
plainly — it is a much simpler claim than anything the probe can support.

**Where the argument fails, which you must state.** Disposal runs on `close()`.
A SIGKILL, a power loss, or a crash means `close()` never runs and the profile
survives. Determine what that leaves behind and where. If a surviving profile is
still inside the residency, say whether that is an escape or merely untidy.
Reason it through rather than asserting either.

**Spellcheck is a different problem and must not inherit this argument.** A
disposable profile stops nothing that leaves over the network. Treat network
egress of typed content separately. Consider whether it should be affirmatively
disabled by a launch flag rather than observed to be off — an observation that a
default was off is not a guarantee it stays off.

## Question 2

Decide the write path. The product already treats a contribution as its own
kind of event, distinct from a run (ADR-0032). Nothing currently says a person
at a keyboard may originate one against the real residency.

Read ADR-0032 and ADR-0031 before deciding. State what changes if a human
becomes an origin of contributions: what the event must carry, what it may not,
and what a later reviewer of the record would need in order to tell a
human-originated contribution from a machine-originated one — or whether that
distinction should exist at all.

## What this ADR is not

- Not a packaging decision. How a UI reaches the workspace is the next
  milestone. If you find the two cannot be separated, that is a finding to
  report, not a licence to decide packaging here.
- Not a correction decision. ADR-0041's supersession policy has no human face,
  which is real and belongs to the milestone that builds an editable surface.
- Not a design. No form, no framework, no component, no wireframe.
- Not a maturity claim. Nothing moves on any matrix.

## How to write it

Someone should be able to read only this ADR, a year from now, and know whether
a browser form is permitted and what write path it must use, without
reconstructing this milestone.

Write plainly. State the decision, the reasoning, and what it costs. Say what
you are *not* confident about in its own words rather than hedging every
sentence. Where the evidence is weak, name the weakness instead of writing
around it — the review will find it anyway, and the record is more useful with
it stated.

Match the structure of a recent ADR (`0047` is the closest analogue in
subject). Follow the INDEX conventions for the digest row.

## Boundaries

- Synthetic and documentary only. No real workspace, no residency locator
  anywhere.
- Do not modify product code. This track writes a decision.
- Do not ratify. Status is proposed; the owner ratifies.
- Do not revise the probe or the findings note. If you believe a finding is
  wrong, say so in the ADR and report it — do not edit the evidence.

## Stop conditions

- The evidence does not support a decision either way. Say that; do not
  manufacture confidence.
- Deciding question 1 or 2 turns out to require deciding packaging or
  correction.
- You find something in the probe evidence that contradicts the confinement
  argument above. Report it rather than working around it — the charter's
  argument is not privileged over what you find.

## Report back

The ADR, the INDEX row, a plain statement of both answers, the weakest point in
your own reasoning, and anything you had to leave undecided.
