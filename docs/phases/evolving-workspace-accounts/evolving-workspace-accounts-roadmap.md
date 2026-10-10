# Evolving Workspace Accounts Roadmap

## Current direction

The first milestone merged in PR #205. The next milestone is planned:
[Reviewing and Correcting the Account Behind a Result](milestones/account-review-correction.md).
It deliberately takes up one bounded interaction, not another tax vertical.
Later milestones are not commitments.
Experience and owner and agent feedback should change the sequence when they
reveal a more useful question.

## 1. Updating an Account Without Losing Its Meaning — closed 2026-10-08

[Plan](milestones/account-refinement.md) ·
[Retrospective](../../milestone-retrospectives/2026-10-08-account-refinement.md).
Delivered: line 21 combines each form's older answer and current loan detail
(core calculations v42), and the saved explanation separates what was said,
used and assumed.

Use Cedar and Birch student-loan interest statements to establish how adding
details about one statement should affect its earlier answer, its calculation
basis and the other statement. Aim to support different established input
methods on different statements without erasing answers to satisfy the engine.
Investigate coexistence on the same statement before selecting a precedence
or supersession rule. Build only after that distinction is understood.

## 2. Reviewing and Correcting the Account Behind a Result — planned

Start from a saved student-loan deduction explanation. Let a person identify
and correct one existing loan-cost answer, save through the established
recording boundary, and inspect the recalculated result. Preserve unrelated
answers and the prior saved result. Investigate the actual surface connection
before selecting a build; do not develop a general intake system.

The plan includes early independent review of the concrete walkthrough,
the implementation boundary, and the integrated interaction. At closeout,
reassess phase completion rather than automatically choosing another case.

## Remaining phase questions

The first milestone supported a bounded phase exit. The owner has requested
another milestone; the second question below now has the narrow scope above.

- How should an assumption stop being relied on when information bears on it,
  and how should the application explain what replaced it?
- How should the person review and correct an existing answer from its
  result without needing to understand competing input methods?

Do not convert these questions into automatic follow-on tracks. A bounded
result may justify concluding the phase, pursuing a different capability, or
isolating a prerequisite. Keep the evidence and unresolved questions useful
without committing to a general framework.

## Carried boundaries

Interest allocation, mixed-period treatment, person-supplied scoped results,
institutional verification and a general user journey remain unselected.
Readability and engineering follow-ups from the previous phase are retrieved
when they bear on this work, not bundled into it by default.
