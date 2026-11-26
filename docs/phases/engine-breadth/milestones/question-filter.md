<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "question-filter",
  "status": "Closed 2026-11-26. Evidence tooling only.",
  "retrospective": "docs/milestone-retrospectives/2026-11-26-question-filter.md",
  "scope": [
    "the blocked-names-question and preferential-base-reason evidence probes identify a question by the saved model's question structure, not by a question mark in the sentence",
    "every test that loads these probes still checks what it checked, and any count it pins changes only where an imperative question was missed"
  ],
  "non_goals": [
    "no change under packages/ and no published file or schema",
    "no change to any page, question or explanation wording"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/question-filter.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/question-filter.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/question-filter.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Evidence Probes Find Questions by Structure, Not Punctuation (2025)

Milestone key: question-filter.
Branch: milestone/question-filter-2025.
Phase: Engine Breadth, hardening. Opening plan: 2026-11-26.
Starting point: main at `b9d529f7` (core v108).
Expected target: evidence tooling and tests only.

## What we are trying to accomplish

The roadmap parks this: "The blocked-names-question and
preferential-base-reason evidence probes count a sentence as a question
only if it has a question mark, so an imperative prompt is missed. Replace
the filter before reusing them." The filters are
`blocked-names-question-evidence/common.py` (`asked = [s for s in
sentences if "?" in s]`) and `preferential-base-reason-evidence/probe.py`
(`_questions`). Since then, question prompts have become imperative in
places (for example "If box 1g is wrong, enter the correct amount"), and
the saved presentation model (v3) says which reasons are questions through
its question links. A probe that later milestones reuse should read that,
not punctuation.

## Stages

Track 1 (build), fresh review, repair, closeout, final review, merge. No
P0: the change is two filter functions and the tests that load them.

## Decisions

1. **The rule (foreman).** A blocked line's reason counts as a question
   when the saved model links it to a question (the presentation-model v3
   question-group references and their reason indices, or whatever v3
   field the projection uses to mark a reason as asking for an answer).
   The builder confirms the exact field from
   `packages/derivation/presentation_projection.py` and the v3 schema, and
   falls back to the "?" test only for models older than v3, saying so.
2. **Pinned outputs.** Where a committed evidence output or a test pins
   question counts produced by these probes, the builder regenerates or
   re-pins only what the new rule changes, and lists each change with the
   sentence that was newly counted (or no longer counted) and why.

## Track 1 result

Built. Both probes now use one helper,
`blocked-names-question-evidence/question_links.py`. On
presentation-model.v3 it counts a reason as a question when
`resolved.questionRefs[].reasonIndices` points at it. The "?" test is used
only for models older than v3.

In a one-off comparison the builder ran with temporary logging (not
committed), on all 2976 blocked-line reason lists the six probe tests
reach (all v3), the new rule gave exactly the old lists. No count or committed output
changes, and nothing was re-pinned.

Finding for review: the box 4 withholding prompt ("Enter the federal
income tax withheld in box 4 of each Form 1099-B ...") appears unlinked.
On v89 lines 25b and 25d it is the only reason, so the probe counts those
lines as asking nothing, under either rule. Linking it would be an engine
change, outside this milestone.

Evidence: `question-filter-evidence/track1.md`.

## Closeout

Closed 2026-11-26. Retrospective:
`docs/milestone-retrospectives/2026-11-26-question-filter.md`. Because the
track changed no output, one independent review after curation stood for
both the fresh and the final review (foreman). The roadmap item is
replaced by a narrower one for the probes that still use "?".
The combined review (NOT READY) found the roadmap overstated ADR 0089 and
that unlinked asking reasons are a class, not one prompt (QF-R1, QF-R2);
the foreman fixed the roadmap, parked the class, widened the helper to v3
onward (QF-R3) and marked the comparison as builder-measured (QF-R4).
