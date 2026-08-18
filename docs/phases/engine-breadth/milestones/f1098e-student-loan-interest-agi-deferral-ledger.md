# Deferral Ledger: 2025 Form 1098-E Student-Loan Interest through Schedule 1 Lines 21/26 and AGI

Closing 2026-08-18. See the retrospective
(`docs/milestone-retrospectives/2026-08-18-f1098e-student-loan-interest-agi.md`)
for the full evidence account.

## Retired for this bounded class

- 2025 Form 1098-E student-loan interest is deductible on the Student Loan
  Interest Deduction Worksheet, subject to the $2,500 cap and the MAGI
  phaseout, and carried through Schedule 1 line 21, Schedule 1 line 26
  (total adjustments), and Form 1040 line 10 into AGI (lines 11a/11b).
- Twelve eligibility components (five universal per-statement witnesses,
  three SLI-scope universal tokens, two legal-zero tokens, plus box-1/box-2
  themselves) gate the deduction; a "no" answer on any universal component
  blocks the whole route (`SLI_UNIVERSAL_COMPONENT_VIOLATION`) rather than
  silently zeroing it.
- MFS filing status is honestly ineligible (`SLI_MFS_INELIGIBLE`), matching
  the statutory rule.
- Schedule 1 Part II completeness is the first application of ADR-0016
  decision 4 to a mixed absent/present/structural-zero total (twelve
  absences, one present line-21 amount, one structural zero); any genuine
  Part II adjustment this milestone cannot compute correctly blocks
  (`SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE`) rather than underweighting MAGI.
- The expression-language extension (`multiply`, `divide`,
  `collect_categorical_all_equal`) is additive; existing op semantics are
  unchanged.

## Carried forward (named future work, not addressed here)

- **P1 — hand-maintained rule-artifact/attachment-rule capability
  allowlists**, carried forward again from the `declarative-validation-
  substrate-f8949` deferral ledger. Confirmed twice more within this
  milestone alone: 8 sites across `live.py`/`marshal.py`/
  `package_validation.py`/`runner.py` needed fixes during the rebase to
  admit `rule-artifact.v6` (including one, `runner.py`'s disposition
  `record_codes` closed set, that is a genuinely new mechanism the
  concurrent milestone introduced); then the bisectable-rebase curation
  that followed re-broke one of those same sites (`runner.py`'s
  `run_and_record` `use_v2` set) plus three related comments, caught only
  by independent review of PR #178, not by the suite. First instance in
  this corpus where the mechanism was re-broken after being fixed rather
  than missed on first build. Scoped, not built:
  `milestones/rule-artifact-capability-table-consolidation.md`. Trigger:
  owner selects it as its own milestone.
- **`no-rrb-or-foreign-social-benefit` succession** (the fourteenth
  migration candidate named by the SSA no-activity and fact-type-succession
  prerequisites) remains deferred; unchanged from those milestones' own
  deferral state, not touched here.
- **Schedule 1 Part II lines 11/12/13/14/15/16/17/18/19/20/23/25** (educator
  expenses, business expenses, HSA, moving, deductible SE tax, SE
  retirement, SE health insurance, penalty on early withdrawal, alimony
  paid, IRA deduction, Archer MSA, other adjustments) have no producer.
  Any return with a genuine adjustment on one of those lines correctly
  blocks with `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE`; building any of those
  producers is a distinct future candidate, not scoped here.
- **Multiple Form 1098-E statements composing correctly under disagreement**
  is covered by Track 6's path (j) and the Track 6b repair, but only for
  the five universal per-statement witnesses read through
  `collect_categorical_all_equal`. Any future per-statement categorical
  witness added to this worksheet must use the same op, not a bare `ref`,
  or the same order-dependence class of defect recurs.

## Discharged events, not deferrals

- **Independent review, performed after this ledger was first drafted.** An
  independent review of PR #178 at the curated object `64c540ce` returned
  `CHANGES REQUESTED` on two defects introduced by the bisectable-rebase
  curation itself (`runner.py`'s `run_and_record` `use_v2` set regressing
  the closed rule-artifact.v6 divergence, and three comments silently
  narrowing v6's described capability). Both fixed at `29971813`; gate
  re-verified green. See the retrospective's "Independent review findings"
  section for the full account. This satisfies the plan's exit criterion
  as of this update; it was not satisfied at original closeout.
- The marshal.py order-dependence defect surfaced by Track 6's path (j) —
  fully repaired in Track 6b per the owner's itemized disposition and
  re-verified: both assertion orderings now correctly block.
- The Track 4 itemization-cap ordering bug (a false Schedule 1 attachment
  block for filers over $2,500 in interest) — repaired in Track 4b, worksheet
  arithmetic verified byte-identical before and after.
- The `artifact-package.v24` version collision with the concurrent
  `declarative-validation-substrate-f8949` milestone, found during Track 6's
  own review — corrected to v25 (schema file, manifest checksum, every
  call site) before this milestone's PR was ever opened.
- The `artifact-package.v25` schema having been authored as v23's own
  successor rather than v24's (silently dropping the concurrent milestone's
  `attachment-rule.v8`/`source-family.v2`/`rule-artifact.v5` admissions once
  rebased onto real `main`) — regenerated as v24's true additive successor
  during the rebase-and-rebuild, verified by tree-hash and by re-running
  the full suite at multiple points in the rebuilt history.
- The Track 7 ADR draft missing its Consequences/Alternatives-considered/
  Links sections — repaired same-round, verified byte-identical against the
  original Context/Decision content.
- `tools/build_orientation_block.py`'s `current_prompt` anchor being
  silently ignored past `max_bytes` — fixed with a regression test.
- A duplicate-heading defect in this milestone's own plan document causing
  the orientation tool's first-match-wins section resolution to silently
  return the wrong, shorter content for every T0-N deep-read anchor —
  disambiguated.
