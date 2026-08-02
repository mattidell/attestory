# Capital-Gain Distributions / Line 7a — Track 4 Completion F1 Repair

Audience: Builder.

Status: **chartered for dispatch.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-track3-presentation` at completion
  review commit `ab458f870e617b9bf596fd4320bf2ea02d649451`.
  Resolve `HEAD` through the orientation command and verify it against Git.
- **Exact object:** repair only F1 in
  `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-31-capital-gain-distributions-line7a-track4-completion-review.md`:
  the new milestone ledger omitted the still-active Schedule B Part I
  multi-family interest deferral carried by the Dividends and Schedule B
  predecessor ledger.
- **Role:** Track-4 Completion Records Repair Builder, Low tier / medium effort.
- **Scope and evidence-rung ceiling:** one records-only edit to
  `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a-deferral-ledger.md`.
  Add the missing carried disposition with its exact predecessor reference and
  reactivation trigger. The committed predecessor ledger and F1 reproduction
  are the evidence ceiling. Every other completion-review measurement remains
  credited.
- **Stop conditions:** stop and report if repair requires changing any other
  file; retiring or reinterpreting the predecessor obligation; selecting an
  interest milestone; changing implementation, tests, tools, schemas, content,
  packages, fixtures, ADRs, governance, the Real Return matrix, or any other
  record; editing phase pointers; adding real/private material; or interpreting
  governance.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-31-capital-gain-distributions-line7a-track4-completion-review.md`;
  `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-31-capital-gain-distributions-line7a-track4-completion-records.md`;
  `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a-deferral-ledger.md`;
  `docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/dividends-schedule-b-slice-deferral-ledger.md`
  entry 5; and `AGENTS.md#Data Safety Rules`.

Before editing, echo F1, the one-file ceiling, the exact predecessor obligation
and trigger, credited measurements, evidence ceiling, and every stop condition.

## Required repair

Add one carried interest entry to the new deferral ledger that:

1. identifies the predecessor as the Dividends and Schedule B deferral ledger,
   entry 5;
2. preserves the exact outstanding obligation that Schedule B Part I currently
   ties only to the box-1/1099-INT family rather than a multi-family interest
   sum;
3. states that this milestone did not touch or retire it; and
4. preserves its reactivation trigger: an interest-breadth milestone admitting
   a second 1099-INT family, or any milestone that must prove Schedule B Part I
   against more than one family.

Do not renumber unrelated entries unless Markdown list continuity requires it;
do not rewrite their substance. Do not select or recommend the future interest
milestone.

## Verification

Run once:

```text
git diff --name-only <repair-charter-commit>..HEAD
git diff --check <repair-charter-commit>..HEAD
rg -n "Schedule B Part I|box-1/1099-INT|multi-family" docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a-deferral-ledger.md
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

The name-only result must be exactly the one ledger path. Do not run the full
suite for this one-record repair.

## Handoff

Commit one F1 repair commit after this charter/pointer commit. Leave the
worktree clean and report the SHA, exact inserted disposition, one-file range,
verification results, and any stop finding. Do not review, edit pointers, push,
open a PR, select future scope, or perform closeout.
