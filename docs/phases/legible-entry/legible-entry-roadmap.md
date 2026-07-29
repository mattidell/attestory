# Legible Entry Phase — Roadmap

Audience: Product (roadmap); Shared (status)

Status: **accepted 2026-07-28** (PR #100). Milestone 1, The Entry Boundary, is
closed. Milestone 2, Packaging the Surface, is approved and its first track is
chartered.

## Thesis

This phase is about usability: getting the owner from a pile of tax documents
to a computed return without hand-editing JSON. We're relying on the
project's existing principles to guide it, the same way those principles
already make every computed value explain itself with a citation. Applied to
the interface, that means every form field should explain itself too: what
it's asking for, why, and what happened when it was filled in.

We'll capture that as a schema: a loosely bound representation of the
explanation, context, and navigation each point of entry needs. It's a
working representation, not a fixed one — the shape is still being found.

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

This phase also addresses the language agents use to describe the project and
the work in it. We're targeting plain, direct language: problems and
solutions stated in plain terms, not the indirect phrasing that's crept into
prior drafts.

## Standing test

**Can the owner take a pile of tax documents to a complete, computed return
without opening a text editor?**

That's the outcome test, answered only by the owner performing it. It's not
the only measure this phase uses. Granular, qualitative evaluations run
throughout, described in "How usability is measured in this phase." The
standing test is the final check that those evaluations added up to
something real.

## How usability is measured in this phase

**Agents author and evaluate, against usability criteria this phase
establishes as it goes. Those criteria hold across review cycles, whether the
schema is still being formed or already complete.**

This doesn't depend on starving an agent of context. It depends on a mix of
viewpoints and background: different agents bring different experience to
the same material, and where they agree or disagree is itself useful signal.
The owner reviews what the agents produce, the criteria used, and the
evidence behind a result, and decides. Exactly how the criteria get scored is
worked out inside the phase rather than fixed here.

The unclosed runbook unclarity carried in from Real Return is a first
candidate for this kind of evaluation.

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

A cell reaches **L2 when its usability evaluation passes**, not on a
builder's or reviewer's inspection alone. See "How usability is measured in
this phase." In the Real Return matrix, L2 just meant the synthetic path
worked. Here it also has to pass that evaluation, a harder bar.

This phase keeps all existing process machinery: owner-approved milestone
plans before any charter, prototype-driven Tier 2/3 decisions with rival
evidence, per-track review gates, no-ff merges to a continuous `main-ui`,
retrospectives, the data-safety scan, and a charter verification block that
is the CI `verify` sequence or a stated subset with the omission justified.

## Proposed milestone sequence

1. **The Entry Boundary.** Decide what changes when the browser becomes an
   origin: the write path, the input-surface precondition classes, and
   whether a browser form is admissible at all. An ADR, no product build.
   It's fine to conclude the obvious shape doesn't work.
   **Closed 2026-07-28** (PR #102). ADR-0048 accepted: a browser form is
   acceptable on stated conditions, and an entry surface emits contribution
   events rather than writing facts directly. It also found that the vehicle's
   confinement is not total. Plan:
   `docs/phases/legible-entry/milestones/entry-boundary.md`; retrospective:
   `docs/milestone-retrospectives/2026-07-28-entry-boundary.md`.
2. **Packaging the Surface.** Get UI code across the Developer/Supply
   boundary into the live workspace, in a second adopted artifact separate
   from the rule package: ship one trivial Svelte page and its vendored
   dependency tree, build it at the workspace offline, then write down the
   rule. **Approved 2026-07-28**, Track 1 chartered; plan:
   `docs/phases/legible-entry/milestones/packaging-the-surface.md`.
3. **The Entry Loop, synthetic.** Build the guided loop end to end against a
   synthetic workspace, to L2, with no real data and no maturity claim. This
   milestone also works out the usability evaluation criteria for entry, and
   its own L2 claim is scored by that evaluation rather than by inspection.
4. **Real Entry.** The owner enters a real fact through the surface and
   attests. Owner-operated; the only milestone that can raise a row to L3. By
   then every usability question has already been answered on synthetic
   data.

**Due now, outside the sequence.** The legibility-audit README's own cadence
triggers an audit at each phase boundary, before the transition plan is
finalized. That trigger is live. It is owner-spawned by design and the
foreman must not launch it.

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
   does typed input disqualify the browser and force a different surface?
   "The browser is not a safe input surface" is an acceptable answer, and
   starting from a web form must not rule it out before we check.
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
5. ~~**Done.**~~ **Settled 2026-07-28: filing is out of scope for this phase.**
   The phase ends at a complete, computed return. Filing brings its own
   boundary questions and belongs to a later phase.

## Inherited open items

Carried over from Real Return's phase close:

- The classified-refusal path has no human confirmation. The oldest open item
  on the presentation path, needing a session to exercise.
- The session runbook has an unclear passage. The person who first used it
  flagged the confusion but didn't name which sentence caused it.
- The named deferral ledger and the shims listed in the phase-state product
  briefing.

## Status

Milestone 1 (The Entry Boundary) closed 2026-07-28, ADR-0048 accepted. No
maturity cell has moved — that milestone was a decision, and the instrument
measures capability. Milestone 2 (Packaging the Surface) is approved and its
first track is chartered.

The phase-boundary legibility audit is still due. It is owner-spawned; the
foreman must not launch it.
