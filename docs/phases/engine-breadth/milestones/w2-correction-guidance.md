<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "w2-correction-guidance",
  "status": "Prepared. P0 will trace why a saved W-2 correction may leave a result unavailable; production design is not selected.",
  "scope": [
    "plain-language guidance when a W-2 correction cannot produce a usable result on the supported v6 and v70 entry profiles",
    "distinguish rejected input, a saved correction awaiting calculation, missing answers and authorization currentness using actual recorded outcomes",
    "preserve first-entry, correction history and successful calculation behavior"
  ],
  "non_goals": [
    "no new tax coverage, content package, schema or kernel change",
    "no general explanation framework or v70 usability scorecard",
    "no automatic assertion of missing facts or grant of authorization"
  ],
  "deep_reads": {
    "planning": ["docs/process/planning-and-development.md", "docs/phases/engine-breadth/milestones/w2-correction-guidance.md"],
    "implementation": ["docs/process/planning-and-development.md", "docs/phases/engine-breadth/milestones/w2-correction-guidance.md"],
    "review": ["docs/roles/qualitative-review.md", "docs/phases/engine-breadth/milestones/w2-correction-guidance.md"],
    "new_milestone": ["docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"]
  }
}
-->

# When a W-2 Correction Cannot Recalculate (2025)

Milestone key: w2-correction-guidance.
Branch: milestone/w2-correction-guidance-2025.
Base: merged PR #249, core v70. This milestone publishes no core package.

## Purpose

A person corrects their wages and expects to see what changed. If the
application cannot calculate, they need to know whether their correction was
saved, what prevents the result, and what they can do next. A blank amount or
an engine refusal code does not answer those questions.

The entry loop now supports its legacy v6 and current v70 profiles. This
milestone makes a bounded unsuccessful correction understandable without
changing tax rules or asking the person to diagnose the engine.

## What we need to understand

Saving an answer, calculating a figure and having authority to rely on that
figure are different events. A correction can be rejected before saving,
accepted while another answer is missing, or calculated without current
authorization. The application must not describe these as the same failure.
Nor should an internal fault be presented as a question the person can answer.

We have not yet established which of these outcomes the current reader can
observe or explain faithfully. P0 must trace that before choosing fields,
messages or transport. It should identify the smallest useful set of cases,
not catalogue every possible engine refusal.

## Actions the team will take

1. **Trace the experience.** Follow one successful correction and bounded
   unsuccessful cases through saving, live coordination, saved output and
   display. Separate supplied answers, defaults, derived results and authority.
2. **Establish what can be said.** For each demonstrated outcome, identify
   what was saved, what is known to prevent calculation or reliance, and the
   next action the evidence supports. Identify information lost on the path.
3. **Choose a connected design.** Compare reusing existing presentation
   reasons with any small entry-layer addition. Record costs and decisions
   after evidence; stop for a kernel, published-schema or content change.
4. **Build and test the chosen path.** Preserve accepted values and history.
   Test messages against actual coordinator outcomes and recovered saved
   state, not manually constructed stand-ins. Charter the exact cases first.
5. **Review and close.** Obtain independent fresh-reader review, repair
   findings, then curate plan/evidence, implementation and closeout commits.
   CI verifies the final candidate; the owner merges.

Each investigation step produces enough understanding to plan the next.
P0 is evidence only. No production implementation is authorized by this plan
until its design and Track 1 charter have been recorded and the owner has
approved the initial scope.

## Success and boundaries

In the selected cases a person can distinguish an unsaved correction from a
saved one, understand why the result is unavailable or not current, and see
an honest next step. A valid result does not become an error merely because
authority is absent, and a saved correction does not become lost merely
because calculation is blocked. Successful v6/v70 results remain unchanged.

This does not promise complete diagnosis of every refusal. P0 will state
which cases are supported and how unknown internal faults remain honest.
No free text, tax-rule expansion, new core publication, generic explanation
redesign, or change to runner attachment code is included.

## Planning sources and next step

- Engine Breadth roadmap, parked correction-guidance item.
- `docs/milestone-retrospectives/2026-11-01-entry-loop-rescope.md`: keep
  computation separate from authorization and trace contextual identifiers.

Next: approve this bounded scope, then execute P0 under
`docs/reviews/w2-correction-guidance/charter-p0.md`. Builders/reviewers use
Luna Max under the standing owner dispatch authorization. Derivation changes
require the full suite before handoff; mypy is `python -m mypy`.
