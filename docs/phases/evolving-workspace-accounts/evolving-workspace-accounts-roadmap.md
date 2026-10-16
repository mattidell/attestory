# Evolving Workspace Accounts Roadmap

## Phase disposition — 2026-10-12

The phase is concluded at its bounded result through PR #207. Product work
continues in [Tax Circumstance Breadth](../tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md).
The intervening Shared Understanding experiments remain on their shelved
branch. The recorded milestones and product deferrals below remain evidence
for the new work.

## Current direction

The first two milestones support the bounded phase exit described in
[Reviewing and Correcting the Account Behind a Result](milestones/account-review-correction.md#outcome).
The owner-requested third milestone, **Returning to a Saved Account**, closed
2026-10-11. It added the returning-user path, and the foreman recommends
concluding the phase
([assessment](milestones/saved-account-resumption.md#outcome)). That is the
owner's decision.
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

## 2. Reviewing and Correcting the Account Behind a Result — closed 2026-10-09

[Plan](milestones/account-review-correction.md) ·
[Retrospective](../../milestone-retrospectives/2026-10-09-account-review-correction.md).
Delivered: a synthetic correction session on a saved line 21 result. It
corrects one borrowing's loan-cost answer through the reviewed recorder,
recalculates, and explains the change beside the unchanged earlier result.

Start from a saved student-loan deduction explanation. Let a person identify
and correct one existing loan-cost answer, save through the established
recording boundary, and inspect the recalculated result. Preserve unrelated
answers and the prior saved result. Investigate the actual surface connection
before selecting a build; do not develop a general intake system.

The plan includes early independent review of the concrete walkthrough,
the implementation boundary, and the integrated interaction. At closeout,
reassess phase completion rather than automatically choosing another case.

## 3. Returning to a Saved Account — closed 2026-10-11

[Plan](milestones/saved-account-resumption.md) ·
[Retrospective](../../milestone-retrospectives/2026-10-11-saved-account-resumption.md).
Delivered: a synthetic correction account that a new process reopens from its
files alone. The reopened page shows each answer with its predecessor and the
latest earlier result, calculates without saving again, and continues the
correction.

Continue the existing borrowing-answer correction interaction after its process
has ended. Reopen the same synthetic workspace, recover the saved answer and
history, distinguish a matching calculation from an older result, and calculate
or correct again without reseeding the account. Start with an independently
reviewed trace of the durable records before selecting a recovery mechanism.

Keep this bounded to the existing question and synthetic workspace. Using
personal workspaces and a general transaction-recovery system remain separate
decisions. Recommend phase closure after this milestone rather than adding
another tax case automatically.

## Remaining phase questions

The first milestone supported a bounded phase exit. The second milestone
answered the second question below for one supported answer.

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
