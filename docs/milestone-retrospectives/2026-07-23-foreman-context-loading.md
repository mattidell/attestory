# Retrospective — Foreman Context Loading

Status: **draft — verification passed; independent review and owner merge remain
required.** This becomes final only when the milestone's reviewed units reach
`main`.

## Milestone

Foreman Context Loading is an interstitial Real Return process-maintenance
milestone. It reduces routine foreman re-entry cost without making a summary a
new authority or weakening the full reads that govern a proposed action.

## Prepared capability

- ADR-0042 records the Tier 2 process contract, supported by a paper Gate
  analysis and plain-language companion.
- `tools/foreman_context.py` renders an advisory capsule from one explicit
  committed Git ref, reports source blobs and worktree drift, and refuses
  missing, malformed, or contradictory re-entry metadata.
- Volatile re-entry records carry compact JSON front matter. The active plan
  owns scope/non-goals/deep reads; phase state owns the pointer; handoff owns
  current status/next action; a prototype seat owns role/rung/stop conditions.
- The handoff now describes current state and durable pointers rather than
  duplicating historical accounts already held in retrospectives, reviews, and
  Git.
- Before review, the owner expanded the scope: builder/reviewer context now
  lives in compact charter capsules, and clerks receive a bounded mechanical
  task capsule. The Python renderer remains foreman-only; trusted-advisor
  context remains unchanged.

## Verification

The role-capsule revision requires the final documentation verification and full
verification-floor rerun before review. Earlier renderer verification remains
evidence for the unchanged Python surface, not a substitute for the revised
process record.

## Decisions

- **Tier 2:** [ADR-0042](../adr/0042-foreman-context-capsule.md) keeps context
  routing advisory, explicit-ref-bound, provenance-bearing, and fail-closed.
- **Tier 1:** renderer internals use standard-library JSON front matter and
  support both a prototype context with a seat and an ordinary milestone context
  without one. This is an implementation consequence of ADR-0042, not a second
  process decision.

## Deviations

The plan initially described four volatile sources as though every active
milestone has a prototype seat. The process milestone itself is an ordinary
milestone, which exposed that false assumption before any records claimed
success. Track 1 was corrected before review to support an optional seat and
proves both shapes with synthetic repositories.

The owner then correctly identified that foreman-only optimization leaves the
other operational roles paying broad context cost. The extension uses charters
and clerk task records rather than a second Python routing surface, preserving
role-local authority and avoiding a generic agent-context mechanism.

## Data safety

All tests construct disposable synthetic Git repositories. The renderer reads
only tracked relative paths from a selected ref plus relative porcelain status;
it does not access a workspace, credential, remote configuration, personal
output, or absolute local path.

## Follow-ups

- Run the full verification floor and render the foreman capsule from this
  branch's `HEAD` before requesting review.
- Obtain the owner-approved independent review required by the active process,
  then merge the reviewed units before presenting ADR-0042 as a `main` record.
- On merge, return phase state from this interstitial milestone to the selected
  Live-Run Trust-Domain Definition pointer; its first charter remains owner
  gated.

## Planning lessons

The context protocol itself must be able to describe an ordinary process
milestone as well as a prototype topic. Metadata should make an absent seat an
explicit, valid state rather than inferring a seat from the presence of a plan.
