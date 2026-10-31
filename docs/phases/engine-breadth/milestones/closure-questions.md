<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "closure-questions",
  "status": "Open. Builds the closure-question design costed in the closure-question-wording P0: a source-closure-mapping.v3 schema with closure_question, its admission, 50 questions in plain words, and a projector reason.",
  "scope": [
    "a closure mapping can declare the question a filer answers to confirm a family complete (source-closure-mapping.v3, closure_question)",
    "the package validator, the closure authorization, the tax loader and the live coordinator admit v3 mappings alongside v2",
    "every closure in the latest core has a question in plain words",
    "a saved presentation names that question as the reason on every line blocked by an unconfirmed family"
  ],
  "non_goals": [
    "no change to any computed value, disposition or block code",
    "no reason composed in code; the sentence is declared content",
    "no edit to any published schema or citizen; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/closure-question-wording.md",
      "docs/phases/engine-breadth/milestones/closure-questions.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/closure-question-wording.md",
      "docs/phases/engine-breadth/milestones/closure-questions.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/closure-questions.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/closure-questions.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# A Blocked Line Names Its Question, Built (2025)

Milestone key: closure-questions.
Branch: milestone/closure-questions-2025, stacked on
`milestone/interest-cents-2025` (PR #246), so the successor package is core
v69, registry v67, release v67.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-31.

## What we are trying to accomplish

The closure-question-wording milestone (#239) closed on its P0: a line
blocked because a family is unconfirmed shows a generic "blocked" text and a
family id, and no closure declares the question the filer must answer. Its
costed design needs a schema successor and a live-coordinator admission
change; the owner approved building it (2026-10-31).

The useful outcome: a filer whose return is held by an unconfirmed family is
told, in plain words, the one question that releases it.

## Design (from #239's P0)

- **Schema.** `source-closure-mapping.v3`: v2 plus a required
  `closure_question` string. Published as a new file; v2 untouched.
- **Admission.** `package_validation.py`, `authorization_closure.py`,
  `packages/tax/loader.py` and the live coordinator (`live.py`, which today
  filters on exactly v2 and would drop v3 silently) accept v2 and v3.
- **Content.** One v3 successor per closure mapping in the latest core (50),
  each with a question in plain words, written from the family's title and
  claim, never the internal terms.
- **Projector.** For each blocked section, walk its missing chain to the
  `SOURCE_SET_UNCLOSED` roots; if every root has a question, attach each as
  a declared `{sentence}` reason (the shape the saved model and page already
  accept). A v2 mapping gives no reason, so earlier cores render as today.

## Actions the team will take

1. **Track 1 — schema and admission.** The schema, the four admission
   points, tests that a v3 mapping is admitted and a v2 one still is, and
   that nothing is dropped silently. One mapping successor as the proof.
2. **Track 2 — the questions.** The remaining mapping successors, each
   question checked against its family; core v69 with
   `tools/package_successor.py`.
3. **Track 3 — the reason.** The projector, tests on saved presentations for
   the line 25b and line 2b cases from #239's P0, and earlier cores unchanged.
4. **Close.** Fresh-reader review (including a plain-language read of all
   50 questions), curated history, retrospective, roadmap.

## Decisions

Foreman, 2026-10-31, after Track 2's stop:

1. **A package schema successor, `artifact-package.v37`, admits
   `source-closure-mapping.v3`.** `artifact-package.v36` enumerates the member
   schemas a package may carry and has only v2, so a package with a v3
   mapping is refused (`PACKAGE_SCHEMA_INVALID`). The owner approved the v3
   mapping schema; a package cannot carry it without this successor, so the
   foreman reads it as within that approval and records it here. It is v36
   with v3 added to the member-schema list and nothing else changed,
   published by the same protocol; core v69 conforms to it.

## Process

Dispatch to Sonnet 5.5 Agent sub-agents. Tracks 1 and 3 touch
`packages/derivation/`, so the full suite runs before each handoff. Stop
means stop.
