<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "improvised-prototype",
  "status": "Closed 2026-08-01 on main-ui. The unflattened, navigable explanation now covers all nine evaluation lines, with dependency-chip prediction and a non-collapsing trail.",
  "scope": [
    "prototype a walkable explanation for a changed return line in the existing synthetic W-2 entry surface",
    "reuse the existing presentation model and lineage rather than derive tax meaning again",
    "let what the running prototype reveals determine the next useful change"
  ],
  "non_goals": [
    "no fixed track sequence or predetermined definition of done",
    "no maturity claim or broad criteria exercise",
    "no real personal data unless the owner separately chooses a real-data exercise"
  ],
  "deep_reads": {
    "implementation": [
      "docs/phases/legible-entry/milestones/improvised-prototype.md",
      "packages/derivation/entry_loop.py",
      "packages/derivation/presentation_projection.py",
      "packages/sample_data/entry_loop_t1/surface/content/app/src/EntryPage.svelte",
      "AGENTS.md#Owner-directed mode",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/phases/legible-entry/milestones/improvised-prototype.md",
      "AGENTS.md#Owner-directed mode",
      "AGENTS.md#Data Safety Rules"
    ],
    "merge_or_records": [
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ]
  }
}
-->
# Improvised Prototype

Status: **closed 2026-08-01 on `main-ui`.**

## Goal

Make the entry surface a place where a person can follow the record, not just
see disconnected status rows. Start with one changed Form 1040 line in the
synthetic W-2 loop and expose the meaning the existing presentation model
already carries.

The prototype should let the person move from the changed line toward the rule
that produced it, the accepted input and evidence behind it, and the available
correction action. The UI must not calculate or invent a second explanation.

## How we will work

This is owner-directed work. Make one small useful change, run it, inspect what
it teaches us, and choose the next move from there. Builders, reviewers, and
written criteria are optional when they answer a question we actually have.

There are no fixed tracks or precommitted exit test. The owner decides when the
prototype is useful enough, what observations matter, and whether to continue,
redirect, or close the milestone.

## First card

Render an unflattened explanation for Form 1040 line 1a in the existing
synthetic W-2 entry loop. Reuse the current presentation and lineage data. Add
entry-specific interaction state only where navigation requires it.

The work stays synthetic by default and does not add tax logic.

## Outcome

Closed 2026-08-01. The explanation now covers all nine evaluation lines
(not just 1a), each honestly classified as leaf, composite, or unsupported.
Dependency chips carry a reachability predicate so a reader can see which
branch leads back to the entered fact before clicking it, and the trail
does not collapse as the reader navigates deeper — every panel opened stays
open and stays current across a correction. A holistic fresh-eyes review
confirmed the walk holds together as one coherent object; the same review
found one unfixed defect (a correction resets scroll position, silently
relocating the reader) carried forward rather than fixed under this close.
Full account: `docs/milestone-retrospectives/2026-08-01-improvised-prototype.md`.
