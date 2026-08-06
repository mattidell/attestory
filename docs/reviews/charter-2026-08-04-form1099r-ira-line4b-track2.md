# Owner-Launch Charter — Form 1099-R IRA Line 4b Downstream Integration

Status: completed by dispatched Builder; handoff commit `3274044`.

## Context Capsule

- Source ref and resolved launch commit: the completed Track 1 commit on
  `milestone/form1099r-ira-distributions-line4b`, `efe09929a1bbbb6f7c034303efd3bb1d8cfaf1bd`,
  based on ratified `origin/main` `20a67ce162fe0e41d80dd0132619e24008beccf5`.
- Exact object: Track 2 of `docs/phases/engine-breadth/milestones/form1099r-ira-distributions-line4b.md`.
- Role: Builder, Luna, Medium/medium.
- Branch/worktree: the same milestone branch and dedicated worktree.
- Evidence ceiling: production integration, package/adoption resolution,
  explanation, presentation, and focused compatibility tests.
- Stop conditions: any missing Track 1 authority, package collision or lost
  upstream member/selection/schema admission/composition obligation, need for
  basis or special-distribution logic, or a new product decision.

## Work packet

Implement only the downstream and surface boundary:

- an additive successor line-9 rule that consumes line 4b exactly once, keeps
  line 4a blank, and does not read raw Form 1099-R members;
- verification of the existing line-11 AGI, line-15 taxable-income, and
  line-16 regular-tax path, including a qualified-dividend compatibility case;
- additive package, published registry, release, and adoption successors after
  a fresh version inventory; retain all historical package bytes and entries;
- durable explanation walks with statement/family/closure/line-4b/line-9/AGI/
  taxable-income/regular-tax pins and exact IRS citation identity;
- one canonical positive production-shaped presentation model with line 4a
  blank and lines 4b, 9, 11, 15, and 16 resolved, plus compact
  blocked/redacted mutations;
- focused tests for P5–P6 and N5–N7, and all existing income-domain regressions.

Before rebase and before final packaging, run the temporary three-way
semantic-ledger diagnostic with a negative control. Treat lost upstream
members, altered selections, lost schema admissions, and lost composition
obligations as blocking. Do not commit the diagnostic. Run focused tests only
while iterating and leave a clean committed handoff.

## Owner launch prompt

Paste this prompt into a fresh Luna builder context after Track 1:

> Pick up the current task as the Track 2 Builder for the Form 1099-R IRA
> Line 4b milestone. Read `AGENTS.md`, run orientation with `--ref HEAD`,
> verify the commit, then read the Track 2 charter and cited sources. Echo
> scope, evidence ceiling, and stop conditions. Integrate only the Track 1
> source path: line 4b enters successor line 9 once, line 4a stays blank, and
> existing line 11/15/16 consume the ordinary downstream symbols; the package,
> exact explanation
> pins, citations, and presentation resolve. Inventory versions after rebase;
> preserve all published history. Run the ephemeral three-way semantic-ledger
> diagnostic before rebase and final PR preparation. Use synthetic demo data,
> never add basis or special-distribution treatment, stop on semantic loss or
> a new decision, and leave a clean committed Track 2 handoff.
