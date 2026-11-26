<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "same-label-ordinal",
  "status": "Open 2026-11-26. ADR 0090 accepted by the owner; Track 1 chartered.",
  "retrospective": null,
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
      "docs/milestone-retrospectives/2026-11-26-same-label-members.md",
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
2. **Order of member reasons (SLM-R4, foreman).** Member reasons on a line
   sort by label, then ordinal, then sentence, so each person's questions
   sit together.
3. **Sentence-only matching (SLM-R3, foreman).** `_reasons_beside` and
   `_finalize_question_references` match closure reasons by sentence
   only. A member reason must not be dropped or given another question's
   `reasonIndices` because its sentence equals a selection or fact
   reason; Track 1 makes the match account for the member, with a test,
   or shows on the code that no member reason can reach those paths and
   says why.

## Track 1 result

`0d688c2fc`, `3a4c2ac02`, and `66149e088` implement and test the shared-label
ordinal. Member reasons are ordered by label, ordinal, and sentence. A
selection or fact question with the same sentence leaves the member reason
visible and outside the question link's reason indices.

All 775 recorded lists matched the starting main projection. Of 23
synthetic probes, six matched exactly and 17 differed only in member
ordinals and order. All three browser tests that timed out in the first
local suite shard passed on retry. The foreman directed the builder to
finish on the tested commit and defer the remaining local suite shards to
CI `verify`. See [Track 1 evidence](same-label-ordinal-evidence/track1.md)
for the replay and test results.
