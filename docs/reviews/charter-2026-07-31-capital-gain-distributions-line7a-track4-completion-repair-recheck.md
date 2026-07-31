# Capital-Gain Distributions / Line 7a — Track 4 F1 Repair Recheck

Audience: Reviewer.

Status: **chartered for dispatch.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-track3-presentation` at repair
  commit `c2d6c1a2fe1f63c8904da59ad565767cf561db0a`. The recheck-charter/pointer
  commit is context and must be its direct successor.
- **Exact object or commit range:** focused repair range
  `c2e52338cca3ea58e72db1ba6efbd796746047bc..c2d6c1a2fe1f63c8904da59ad565767cf561db0a`.
  It must contain exactly one commit and the one deferral-ledger file.
- **Role:** the original author-independent Track-4 Completion Reviewer
  continues its own review lineage, High tier / medium effort. This is a
  focused F1 recheck, not a second completion review.
- **Scope and evidence-rung ceiling:** determine only whether the one-file
  repair closes F1 by carrying the exact active Schedule B Part I multi-family
  interest obligation and trigger without changing unrelated ledger
  substance. Every other completion-review measurement remains credited. The
  committed predecessor ledger, original review, and repair diff are the
  evidence ceiling.
- **Stop conditions:** stop and report if the range, tip, or direct charter
  ancestry differs; if any file other than the new milestone deferral ledger
  changed; if unrelated entry substance changed beyond list renumbering; if
  the repair retires, narrows, reinterprets, or selects the future interest
  obligation; if closure requires implementation, schema, content, package,
  test, ADR, governance, matrix, or other records changes; if governance
  interpretation is required; or if any real/private material is encountered.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`;
  `docs/reviews/2026-07-31-capital-gain-distributions-line7a-track4-completion-review.md`;
  `docs/reviews/charter-2026-07-31-capital-gain-distributions-line7a-track4-completion-repair.md`;
  the exact repair diff;
  `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a-deferral-ledger.md`;
  `docs/phases/real-return/milestones/dividends-schedule-b-slice-deferral-ledger.md`
  entry 5; and `AGENTS.md#Data Safety Rules`.

Before reviewing, echo the exact repair range, F1 closure question, credited
measurements, one-file ceiling, evidence ceiling, and every stop condition.

## Focused measurements

1. Confirm the range contains one commit and changes only
   `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a-deferral-ledger.md`.
2. Confirm the new entry explicitly cites the Dividends and Schedule B
   deferral ledger entry 5; preserves the current box-1/1099-INT-only Schedule
   B Part I tie-out limitation; says the obligation is untouched and not
   retired; and preserves both reactivation triggers: a second 1099-INT family
   or any need to prove Part I against more than one family.
3. Compare every other ledger entry across the range. Only numbering changes
   needed for list continuity are allowed; all substance, classification, and
   triggers must be byte-equivalent after normalizing those ordinal prefixes.
4. Confirm the repair does not select or recommend the interest milestone,
   reinterpret the obligation, add implementation claims, or introduce
   real/private material.

## Verification

Run once:

```text
git rev-list --count c2e52338cca3ea58e72db1ba6efbd796746047bc..c2d6c1a2fe1f63c8904da59ad565767cf561db0a
git diff --name-only c2e52338cca3ea58e72db1ba6efbd796746047bc..c2d6c1a2fe1f63c8904da59ad565767cf561db0a
git diff --check c2e52338cca3ea58e72db1ba6efbd796746047bc..c2d6c1a2fe1f63c8904da59ad565767cf561db0a
rg -n "Schedule B Part I|box-1/1099-INT|multi-family" docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a-deferral-ledger.md
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

Do not run the full suite or repeat the already-credited PR/CI and records
measurements.

## Review record and verdict

Write
`docs/reviews/2026-07-31-capital-gain-distributions-line7a-track4-completion-repair-recheck.md`
and commit only that record. Return exactly one verdict:

- `READY` — F1 is closed and every credited completion-review measurement
  remains intact; or
- `NOT READY` — a numbered, reproducible residual explains why F1 remains open
  or the repair exceeded its boundary.

Do not edit the ledger, records, implementation, prior reviews, charters,
pointers, plan, frontier, roadmap, retrospective, or README. Do not design
another repair, push, open or merge a PR, select future scope, or perform
closeout. Stop after committing the recheck record and return custody.
