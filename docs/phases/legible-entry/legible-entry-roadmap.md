# Legible Entry Phase — Roadmap

Audience: Product (roadmap); Shared (status)

Status: **draft — not yet accepted.** Nothing in this phase is chartered.

## Thesis

This phase is about usability: getting the owner from a pile of tax documents
to a computed return without hand-editing JSON. We're relying on the
project's existing principles to guide it, the same way those principles
already make every computed value explain itself with a citation. Applied to
the interface, that means every form field should explain itself too: what
it's asking for, why, and what happened when it was filled in.

Real Return proved the product works: it holds and computes the owner's real
data, cites every published figure, and closed with every cell of its
maturity matrix at L3 or better. What it left behind is entry. The owner
still gets data into the system by hand-editing JSON, and still learns what
is missing by reading a machine's account of it. This phase closes that gap.

Its subject is the loop a person actually performs. The person sees what is
missing, enters that fact, watches it land, and repeats until the return
computes. The missing-facts account is not a separate screen in this phase. It
is the guide through entry, because a data-entry form paired with a diagnostic
page the user must reconcile by hand is the legibility failure this phase
exists to fix.

## Standing test

**Can the owner take a pile of tax documents to a complete, computed return
without opening a text editor?**

One test, falsifiable, and answerable only by the owner performing it. This is
not a test of whether the UI is polished. It is a test of whether the owner
can get through entry without dropping into JSON.

## What changes structurally, and why it is the hard part

Every boundary contract this project has ratified describes a read. The
preflight, the confined invocation vehicle, the loopback surface, and the
non-descriptive attestation all assume the session displays something already
resident in the workspace and leaves nothing behind.

Entry inverts that. **The browser becomes an origin of real data rather than a
viewer of it.** The content that must not escape now passes through an input
surface before it lands. The concrete consequence is a class of workstation
preconditions the current preflight does not observe and was never designed
to: form autofill and form history, saved-form crash recovery, draft
persistence, spellcheck-to-cloud, dictation and IME learning, and undo
buffers. Several of those retain typed content by default. That is the shape
ADR-0047 already calls a Class D condition: a precondition the mechanism
cannot see.

This is the phase's first question and its first milestone. It is a decision,
not a build. The Live Viewing Boundary milestone rejected its own obvious
shape after a first-principles check, and was right to. The equivalent
mistake here is to build a form and confine it afterward.

## Open questions this phase must resolve

1. **The write path.** Does the surface write facts directly, or emit
   **contribution events** through the existing boundary? Contribution is
   already a first-class product event distinct from a run, which is a real
   asset. But nothing states that a human-operated surface may originate one
   against the real residency.
2. **Input-surface preconditions.** Does the preflight grow to cover them, or
   does typed input disqualify the browser and force a different surface? An
   answer of "the browser is not a safe input surface" is acceptable and must
   not be foreclosed by starting from a web form.
3. **Packaging.** Putting a UI in the workspace is a Developer/Supply →
   Live-Run Data crossing (ADR-0044), whose sanctioned form is the current
   owner-adopted, byte-verified package. That package carries derivation
   rules today. Does the UI ship inside it, inheriting byte verification and
   the supply-chain weight that implies, or as a separate artifact with its
   own adoption? Is a build step tolerable at all against a byte-verified
   package?
4. **Correction has no face.** ADR-0041's supersession policy is the most
   hardened mechanism in the system and is unreachable by any human. Every
   fact type shipped today declares `free`, so its interesting refusals
   cannot yet occur. But the first UI that lets a person change an answered
   fact is where a refusal to correct becomes a legibility problem rather
   than a mechanism.
5. **Done.** The standing test says "complete, computed return." It does not
   say *filed*. Whether filing enters this phase's scope is an owner decision
   and is left open rather than assumed either way.

## How usability is measured in this phase

**By context-starved agents, not by the owner's taste.** This is an owner
decision (2026-07-28). It inverts the assumption that a one-user product
must evaluate its surface by asking that user.

The owner is the worst-positioned reader in the project. Legibility is a
property of what a person can recover and complete without prior knowledge,
and the owner cannot stop knowing how the system works. In a prior case, an
agent given the Real Return session runbook produced alternative instructions
that worked better than the author's, because it read them without the
author's context.

This phase extends the existing instrument rather than inventing one.
`docs/legibility-audits/` already ratifies the method: an owner-spawned,
deliberately context-starved reader; a declared allowed slice and a forbidden
answer key; falsifiable tasks scored `recovered` / `partial` / `wrong` /
`unrecoverable`; a bar of zero `wrong`, because a confident wrong answer means
the artifacts actively misled a careful reader; and advisory findings that the
owner dispositions. The foreman does not spawn it, for the reason that
instrument already gives: the foreman is maximally context-rich and cannot
construct a starved reader without contaminating it.

What this phase adds is a second task family. The existing audit measures
**recovery**: what a number means and where it came from. Entry needs
**completion**: given only the surface and a synthetic document, can a cold
agent get the fact in correctly, and know that it landed? The scores carry
over, and `wrong` has a sharper meaning here: the agent confidently entered
the wrong thing, or believed it had succeeded when it had not. A surface that
lets a user confidently do the wrong thing is the most serious defect this
phase can produce, and it is exactly what a starved completion task is built
to catch.

**The data boundary does not constrain this.** Completion audits run against
a synthetic workspace, so usability is measured entirely at L2, before real
data is anywhere near the surface. Findings can be recorded in full, specific
detail in the repository with no attestation constraint at all. The owner's
real session then carries the meaning it has always carried, that the
capability operated, and nothing more is asked of it.

**Where the owner remains ground truth.** Agents generate and test; the owner
ratifies. The runbook case was validated by the owner judging the result
good, and the audit instrument already has the owner spot-check one attempt
for whether its scoring is real. That division moves the owner from author of
clarity to acceptor of it.

**The honest limit, stated once.** A starved agent proxies a cold reader. It
does not carry fatigue, divided attention, or a physical document whose boxes
are laid out confusingly. Findings about comprehension and completability are
strong. Findings about affect are not claimed. Any milestone in this phase
that claims a usability result must say how it knows, and "it looked right"
is not an answer, from the owner either.

The unclosed runbook unclarity carried in from Real Return is the first item
this method should be pointed at.

## How milestones are selected in this phase

This phase replaces Real Return's maturity matrix rather than extending it.
That matrix's columns are tax-content domains, which are the wrong axis for a
phase whose variation is what stage of the entry loop a surface serves and
which fact families it can carry. The Real Return matrix stands as the closed
instrument of its own phase.

The instrument uses the same L0–L4 levels, read the same way (L2 synthetic
end-to-end, L3 the capability really operated on real data under owner
attestation, L4 hardened with mechanical proof):

- **Rows, the entry loop:** know what is missing, enter a fact, see it land,
  correct an entered fact, know the return is complete.
- **Columns, the fact families a person actually enters:** W-2, 1099-INT,
  1099-DIV, taxpayer assertions.

A cell reaches **L2 on a passing starved completion audit**, not on a
builder's or reviewer's inspection. See "How usability is measured in this
phase." That is the substantive difference from the Real Return matrix, where
L2 meant the synthetic path executed correctly. Here it must also be usable
by a reader who knows nothing, which is a strictly harder bar and the one
this phase exists for.

All process machinery is retained unchanged: owner-approved milestone plans
before any charter, prototype-driven Tier 2/3 decisions with rival evidence,
per-track review gates, no-ff merges to a continuous `main-ui`, retrospectives,
the data-safety scan, and a charter verification block that is the CI
`verify` sequence or a stated subset with the omission justified.

## Proposed milestone sequence

1. **The Entry Boundary.** Decide what changes when the browser becomes an
   origin: the write path, the input-surface precondition classes, and
   whether a browser form is admissible at all. An ADR, no product build.
   Explicitly permitted to conclude that the obvious shape is inadmissible.
2. **Packaging the Surface.** Decide and implement how a UI reaches the live
   workspace across the Developer/Supply boundary.
3. **The Entry Loop, synthetic.** Build the guided loop end to end against a
   synthetic workspace, to L2, with no real data and no maturity claim. This
   milestone also extends `docs/legibility-audits/` with the completion task
   family and its launch prompt, and its own L2 claim is scored by a starved
   completion audit rather than by inspection. The instrument must exist
   before the surface it judges is called good.
4. **Real Entry.** The owner enters a real fact through the surface and
   attests. Owner-operated; the only milestone that can raise a row to L3. By
   then every usability question has already been answered on synthetic
   data.

**Due now, outside the sequence.** The legibility-audit README's own cadence
triggers an audit at each phase boundary, before the transition plan is
finalized. That trigger is live. It is owner-spawned by design and the
foreman must not launch it.

## Inherited open items

Carried from Real Return's phase close and not lost with it:

- The classified-refusal path has no human confirmation. The oldest open item
  on the presentation path, needing a session to exercise.
- The session runbook has an unidentified unclarity, reported by its first
  human user with the sentence unnamed.
- The named deferral ledger and the shims listed in the phase-state product
  briefing.

## Status

Nothing completed. The phase definition is not yet accepted.
