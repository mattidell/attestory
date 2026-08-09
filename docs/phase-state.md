<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f1098e-student-loan-interest-line21",
  "active_plan": "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md",
  "milestone_state": "track-0",
  "status": "**ENGINE BREADTH / 2025 FORM 1098-E STUDENT-LOAN INTEREST THROUGH SCHEDULE 1 LINE 21 AND FORM 1040 AGI — TRACK 0 SETTLED.** All ten paper-scope items are settled and committed on `milestone/f1098e-student-loan-interest-line21` (worktree `engine-1098e`), cut from `b25562f`: T0-1/2/3/9/10 as `track-0a` (f05dc6e); T0-4/5/6/7 and T0-8 as `track-0b` (f9228ed, 64f267d, be556af, e6b5d70, 124918d, d22400b). Draft PR #169, based on `milestone/f1098-mortgage-interest-line12e` until #163 and #168 land. Track 1 (implementation) is not yet chartered. Settlement highlights: the evaluator has no `multiply`/`divide` and no categorical or boolean aggregate either (`collect` is numeric-only, `packages/derivation/evaluator.py:118`), so eligibility components are return-scoped rather than per-statement; Form 1098-E account number is not an identity key; the SLID worksheet is i1040gi p.99 not p.98; T0-5 reuses `ss-benefits-scope`'s twelve MAGI absences rather than minting a parallel vocabulary, which is what makes T0-8 cheap — line 26 imposes no requirement on a return that line-9 v7 did not already impose; there is already no `return with no Schedule 1` in this engine, so line 10 yields a computed authorized zero with no new absence authority; no existing fixture or packaged computation changes. Two open items carried out of Track 0: the `attachment-rule.v5` provenance defect (T0-7) and the B1 `not-claimed-as-dependent` coupling (T0-8), where a truthful `no` blocks AGI for a return with no student loans. ADR budget spent — T0-4 claims the single allowed ADR for the multiply/divide extension. Integration order unchanged: merge #163, merge #168, rebase, rebuild every successor and generated publication, run the three-way semantic-ledger diagnostic, verify the delta, only then implementation review or publication. No version numbers allocated.",
  "retrospective": null,
  "current_role": "Foreman (Track 0 settled; Track 1 implementation not yet chartered)",
  "current_prompt": "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md#Track 0a settlement"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Curated history and architectural decisions live in retrospectives
and `docs/adr/`; historical execution records live under `docs/archive/`.

## High Level Milestone Briefing

The engine computes the closed Engine Breadth synthetic routes through Form
1099-DIV box 2a and box 12, Schedule K-1 box-5 interest, market-discount
interest, Schedule B adjustments, covered Form 1099-B capital paths including
inbound carryovers and Form 8949 wash-sale (code W) lines 1b/8b, Form 1099-INT
box 8 tax-exempt interest on line 2a, Form 1099-G box-1 unemployment through
Schedule 1 into Form 1040 line 8, the bounded Form 1099-DIV box-7 direct
foreign tax credit, the merged IRA line-4b route, the bounded SSA-1099 Benefits
Worksheet route through Form 1040 lines 6a/6b, and Form 1098 home-mortgage
interest through Schedule A and Form 1040 line 12e.

Every one of those is an **income** or **deduction** route. This branch opens
the first **adjustment to income**: Form 1098-E student-loan interest through
Schedule 1 line 21. It is therefore the first work that ever puts a value on
Form 1040 line 10 and makes adjusted gross income differ from total income.

## Operational State: Engine Breadth

* **Active milestone (this branch):** 2025 Form 1098-E Student-Loan Interest
  through Schedule 1 Line 21 and Form 1040 Adjusted Gross Income — **in
  progress**. Track 0 (paper-first scope contract) is **settled**: all ten
  items T0-1 through T0-10 are committed. Track 1 (implementation) is not yet
  chartered.
* **Branch / worktree:** `milestone/f1098e-student-loan-interest-line21` in
  `engine-1098e`, cut clean from `b25562f`.
* **Base:** `b25562f`, tip of `milestone/f1098-mortgage-interest-line12e`.
  Selected by the owner so version allocation sees the true highest allocated
  numbers: core-calculations **v29**, published **v24**, `rule-artifact.v4`,
  `attachment-rule.v6`, `form-field.v3`, `fact-type.v3`, line-9 rule **v7**.
* **Dependencies:** this base carries two unratified milestones. **PR #163**
  (SSA-1099 lines 6a/6b) supplies the Social Security Benefits Worksheet, the
  `ss-benefits-scope` vocabulary, and line-9 v5–v7. **PR #168** (Form 1098
  mortgage interest) supplies `form1040.line-12e`, lines 13a/13b/14, line-15
  v2, the Schedule A attachment, `rule-artifact.v4`, and the `count`/`block`
  operators. Both must merge before this milestone rebases and allocates
  version numbers.
* **Integration order:** merge #163 → merge #168 → rebase this branch onto the
  resulting ratified line → rebuild every successor and generated publication
  from that base → run the ephemeral three-way semantic-ledger diagnostic and
  verify the rebased semantic delta → only then implementation review or
  publication.
* **Plan:** `docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md`.
* **Retrospective:** none yet (milestone not closed).
* **Concurrent milestones (untouched, on their own branches/worktrees):**
  PR #163 `milestone/form1040-ssa1099-line6` and PR #168
  `milestone/f1098-mortgage-interest-line12e`. Neither worktree was altered,
  cleaned, staged, switched, or reused by this milestone's planning.
* **Contracts:** SLI-C1–C10 proposed in the plan; Track 0 owns them. At most
  one new ADR is expected — an ADR-0025-line expression extension adding the
  `multiply` and `divide` operators the worksheet phaseout requires.
* **Open items out of Track 0:** the `attachment-rule.v5` provenance defect
  recorded by T0-7, and the B1 `not-claimed-as-dependent` coupling recorded by
  T0-8 — unquantified, so a truthful `no` blocks AGI for a return with no
  student loans.
* **PR:** #169 (draft), based on `milestone/f1098-mortgage-interest-line12e`;
  retargets to `main` after #163 and #168 merge.
* **Next:** ratify the Track 0 settlement, then charter Track 1. The ADR budget
  is spent — T0-4 claims the milestone's single allowed ADR for the
  `multiply`/`divide` expression extension.

## Re-entry


Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
