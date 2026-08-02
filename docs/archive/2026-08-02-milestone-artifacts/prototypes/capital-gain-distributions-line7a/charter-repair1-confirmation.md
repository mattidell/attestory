# Repair 1 Confirmation Charter — Component Authority and QDCG Handoff

Audience: Reviewer

Date: 2026-07-28. Track 0 of Capital-Gain Distributions and Form 1040
Line 7a.

## Context Capsule

- **Source ref and resolved launch commit:** use the current local
  `prototypes/capital-gain-distributions-line7a/it2` branch and verify its
  commit at launch.
- **Exact object:** repair commit `a60e2d1`, measured only against
  `charter-repair1.md`, findings T-F1/T-F2 in `round-1-triage.md`, and the
  retained P2/P3 boundaries of the selected design at `099882e`.
- **Role:** author-independent focused Confirmation Reviewer, High capability /
  high effort.
- **Scope and evidence-rung ceiling:** confirm T-F1 and T-F2 and check that
  their repair does not regress the already-settled P2/P3 boundaries. Rung 1
  static paper evidence only.
- **Stop conditions:** any need to repair the design, synthesize the contract,
  draft an ADR, inspect another agent's thread, run validator/evaluator probes,
  edit schemas/content/tests/production, interpret governance, implement
  Schedule D or boxes 2b/2c/2d source families, use real data, or broaden beyond
  the named findings and regression boundaries.
- **Full reads before acting:** this charter; `charter-repair1.md`;
  `round-1-triage.md`; `repair1/design.md`; `repair1/examination.md`;
  `it2/design.md`; `it2/examination.md`; the topic `plan.md`;
  ADR-0035 and ADR-0038; the milestone plan's Contracts, Fixtures, and Data
  Safety sections; the linked official 2025 Form 1040 instructions for lines
  7a, 7b, and 16 and the Qualified Dividends and Capital Gain Tax Worksheet;
  and `packages/content/tax/2025/rule.form1040-line16.v2.json`.

## Assignment

Attempt to falsify the repair. Do not improve or complete it. A claimed rule is
not sufficient paper evidence unless the repaired cases make its facts,
authority, pins, state transitions, and dispositions recoverable.

### T-F1 confirmation

Confirm whether the repaired component-backed topology:

1. explicitly represents all four conditions in 2025 Form 1040 Exception 1;
2. gives the boxes-2b/2c/2d absence condition a contributed `{yes, no}`
   categorical assertion with no default and presence-before-value;
3. keeps that assertion independently correctable and pinned, names its
   absence exactly, and does not pretend the excluded boxes have source
   families;
4. keeps it distinct from box-2a family closure;
5. requires all four current `"yes"` components for direct eligibility and
   derives the checked Schedule-D-required conclusion consistently; and
6. demonstrates the eligible, missing, current `"no"`, forward correction, and
   reverse correction states with exact synthetic facts and downstream
   dispositions.

### T-F2 confirmation

Confirm directly against the cited 2025 worksheet instructions whether the
repair:

1. selects QDCG when qualified dividends are positive **or** an applicable
   direct-route line 7a is positive;
2. binds worksheet line 3 to the selected line-7a publication when Schedule D
   is not filed;
3. demonstrates preferential treatment for Q=0 with positive line 7a;
4. preserves the qualified-dividend path for Q>0 with closure-backed line
   7a=0;
5. reduces to ordinary tax only when both inputs are closure-backed zero;
6. never converts blocked or guard-inapplicable line 7a to zero, reads raw
   box-2a members, or depends on incidental conditional-operand ordering; and
7. demonstrates exact current/displaced states and pins through line 7a,
   line 9, taxable income, and line 16.

### Regression boundary

Confirm only that the repair leaves intact:

- successor/historical box-2a graph exclusivity;
- the non-null box-2a presence signal and contradiction interlock;
- closure-backed zero rather than assumed absence;
- no raw downstream box-2a reads; and
- honest non-publication when Schedule D is required or component authority is
  missing.

Do not reopen the owner's topology selection or reassess unrelated it2
material.

## Verdict and output

Create exactly:

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/reviews/repair1-confirmation.md`

Report:

1. `T-F1: CONFIRMED` or `NOT CONFIRMED`;
2. `T-F2: CONFIRMED` or `NOT CONFIRMED`;
3. `REGRESSION BOUNDARY: INTACT` or `REGRESSED`;
4. numbered, falsifiable findings with exact file/section evidence and the
   unmet charter clause;
5. one overall verdict: `READY` only if both findings are confirmed and the
   regression boundary is intact; otherwise `NOT READY`; and
6. whether any uncertainty remains that Rung 1 cannot distinguish. Do not
   climb a rung.

For every required repaired case, state whether the artifact itself contains
enough exact facts, pins, current/displaced states, and dispositions to support
the claim. Do not treat `repair1/examination.md`'s self-reported status as
evidence.

Commit only the review locally and stop. Do not push, merge, repair, synthesize
the contract, draft an ADR, begin production, or advance the pointer. Return
the commit SHA and the three status lines plus overall verdict.

## Data safety

All evidence stays synthetic and publishable. No personal values, identifiers,
dispositions, refusal reasons, workspace locations, documents, screenshots, or
private artifacts may enter the review.
