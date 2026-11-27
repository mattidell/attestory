<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "same-label-ordinal",
  "status": "Closed 2026-11-26. Projection and page change (ADR 0090); no package version.",
  "retrospective": "docs/milestone-retrospectives/2026-11-26-same-label-ordinal.md",
  "scope": [
    "when two roster members of one kind share a recorded label, each member question says which one it means by entry order",
    "member questions on a line are grouped by member, so a filer can pair each answer with a person",
    "every recorded return keeps its numbers, dispositions and block codes"
  ],
  "non_goals": [
    "no kernel change; no published file or schema change; no content",
    "no question-group link for member questions (ADR 0087 Decision 3)"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/adr/0090-same-label-members-entry-order.md",
      "docs/phases/engine-breadth/milestones/same-label-ordinal.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/adr/0090-same-label-members-entry-order.md",
      "docs/phases/engine-breadth/milestones/same-label-ordinal.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/same-label-ordinal.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-26-same-label-ordinal.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Same-Named Members Are Told Apart by Entry Order (2025)

Milestone key: same-label-ordinal.
Branch: milestone/same-label-ordinal-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-26.
Starting point: main at `b9d529f7` (core v108).
Expected target: a projection and page change under ADR 0090.

## What we are trying to accomplish

same-label-members gave each roster member who misses an answer their own
question, but two children both entered as "Sam" still read "Sam" and
"Sam". The owner accepted ADR 0090 on 2026-11-26: a shared label carries
the member's place in entry order, shown as "Demo Sam (the second one you
added with this name)". This milestone builds that, and takes the two
review notes same-label-members parked for it (SLM-R3, SLM-R4).

## Stages

Track 1 (build), fresh review, repair, closeout, final review, merge. No
P0: same-label-members P0 designed and proved this on a scratch build
(`same-label-members-evidence/p0.md` §7, `scratch-projection.diff`,
`scratch-page.diff`).

## Decisions

1. **Contract.** ADR 0090 Decision 2, as accepted.
2. **Order of member reasons (SLM-R4, foreman), amended (Repair 1, SLM-O1).**
   ADR 0090 counts a member's position among current entities of the same
   kind with the same label. Member reasons on a line sort by label, then
   kind, then ordinal, then sentence. Using kind before ordinal keeps each
   person's questions together when two kinds share a label and their
   ordinal sequences restart. **Repair 2 (SLM-F2).** A line with no
   `memberOrdinal` retains the order of reasons from before this milestone.
3. **Sentence-only matching (SLM-R3, foreman).** `_reasons_beside` and
   `_finalize_question_references` match closure reasons by sentence
   only. A member reason must not be dropped or given another question's
   `reasonIndices` because its sentence equals a selection or fact
   reason; Track 1 makes the match account for the member, with a test,
   or shows on the code that no member reason can reach those paths and
   says why.

## Track 1 result

The curated build (`71581e54b`) implements and tests the shared-label
ordinal. Member reasons are ordered as specified in Decision 2. A
selection or fact question with the same sentence leaves the member reason
visible and outside the question link's reason indices. Saved-model
validation also rejects a link directed to a member reason.

Repair 2 preserves the previous reason order on closure-only lines that
carry no ordinal (`b7c7ce2d8`). The comparator resolves the replay baseline
as the parent of the curated build commit (`4fa33021a`). Both projections
therefore include the statement-label changes from ADR 0089.

The replay of `4fa33021a` against `08ed3bebe` matched all 775 recorded
lists. Of 23 probes, six matched exactly and 17 differed only in member
ordinals and order. The report-value control failed as expected.
See the [per-case summary](same-label-ordinal-evidence/repair2-replay.json)
and [Track 1 evidence](same-label-ordinal-evidence/track1.md).

## Closeout

Closed 2026-11-26. Retrospective:
`docs/milestone-retrospectives/2026-11-26-same-label-ordinal.md`.
The fresh review (NOT READY) found that ordinals restart for each kind,
so one member's questions could be split (SLM-O1); that the validator
accepted a fact question linked to a member reason (SLM-O2); that the
replay claim had no committed comparator (SLM-O3); and that lines with no
shared label were reordered (SLM-O4). Repair 1 addressed these findings.
The final review identified a closure-only ordering case and a stale replay
baseline after curation. Repair 2 is recorded in the Track 1 result. The
foreman then rebased onto main after statement-question-labels (ADR 0089)
merged, resolved the shared `_closure_question_reasons` docstring and
the ADR index, and ran the walk and live tests of both milestones
together. Historical commit ids in the evidence note identify the revisions
from before the rebase and curation. Those revisions are kept under
`refs/snapshot/2026-11-26-same-label-ordinal-pre-rebase` (Track 1 and
Repair 1) and `refs/snapshot/2026-11-26-same-label-ordinal-pre-pr-curation`
(after the rebase). The original replay baseline `b9d529f7d` is a merge on
main. The roadmap item is retired.
