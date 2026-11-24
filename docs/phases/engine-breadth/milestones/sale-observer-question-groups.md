<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "sale-observer-question-groups",
  "status": "Open 2026-11-23. Track 1 done; closeout next.",
  "retrospective": null,
  "scope": [
    "the real-Chrome sale page observer expects, for each blocked reason, exactly what the saved page renders: the question-group link for a reason a question group names (presentation-model v3, blocked-sale-pages), the bold member label prefix (ADR 0087), and the statement label prefix",
    "the opt-in ten-case browser fixture (SALE_PAGE_OBSERVATION_BROWSER=1) passes on main"
  ],
  "non_goals": [
    "no page, model, package, rule or schema change; tools and tests only",
    "no change to which page/model disagreements the observer reports, beyond reading the reason rendering the page actually uses"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/sale-observer-question-groups.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/sale-observer-question-groups.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/sale-observer-question-groups.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/sale-observer-question-groups.md"
    ]
  }
}
-->

# The Sale Page Observer Reads Question Groups

Milestone key: sale-observer-question-groups.
Branch: milestone/sale-observer-question-groups-2025.
Phase: Engine Breadth, tooling. Opening plan: 2026-11-23.
Starting point: main at `94c3f02f` (core v102, registry v100, release v100).
Expected target: tools and tests only; no package version change.

## What we are trying to accomplish

page-plain-words parked a mismatch: `tools/sale_page_observation.py`
`_expected_reason_text` still expects each blocked reason's raw sentence,
but since blocked-sale-pages (#299) the saved page renders a reason that a
question group names as the link "See the question and affected lines
above", and since ADR 0087 it prefixes a member's reason with its bold
`memberLabel`. The opt-in real-Chrome fixture fails on
`sale-answer-needs-reconfirmation`.

## Stages

1. **Track 1** (no P0). Make the observer's expected reason follow the
   page's rendering rules exactly (read `renderBlocked` in
   `packages/presentation/pages/citation-walk.v1.html`), add fast unit
   tests for each branch, and run the opt-in fixture in real Chrome.
2. **Fresh review**, repair, closeout.

## Decisions

1. Review SOQ-R1 and SOQ-R2 (low) are accepted. Both concern a malformed
   model the page refuses: a question ref the page cannot read clears the
   line into the section error, and one group without an id. In each the
   observer reports a difference, which is the right outcome for a page it
   cannot trust; it only words the expected text differently from the
   page's error.

## Track 1 result

The observer expects the blocked-reason text the saved page renders. A presentation-model v3 reason that a question group names is the link, including the semicolon when several groups name one reason. Other reasons use the member label, then the statement and lender prefix, then the plain sentence. A raw sentence where that page would show the link is still a difference. Disposition, value, explanation, and attachment checks are unchanged.

Fast unit tests cover each branch and a mismatch in each direction. The opt-in real-Chrome fixture passed all ten cases. The fast lane, mypy on the touched Python, and the envelope scan passed. The record is `docs/phases/engine-breadth/milestones/sale-observer-question-groups-evidence/track1.md`.
