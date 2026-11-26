<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "question-filter",
  "status": "Open 2026-11-26. Track 1 (evidence tooling) chartered.",
  "retrospective": null,
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
