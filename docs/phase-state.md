<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f1098e-student-loan-interest-line21",
  "active_plan": "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md",
  "milestone_state": "closed",
  "status": "**ENGINE BREADTH / 2025 FORM 1098-E \u2014 STOPPED AT DESIGN. STOP CONDITION FIRED; TREAT AS COMPLETED DESIGN EXPLORATION.** Owner ruled 2026-08-10 that the shared Schedule 1 absence vocabulary may NOT be repaired inside this milestone. Both remaining shapes were rejected: parallel neutral vocabulary with dormant predecessors (twelve permanent orphans in open_fact_ids with no retirement mechanism \u2014 a one-way door), and a successor bundle re-declaring the same twelve ids with neutral titles (would cause existing findings to answer a BROADER question than the user asserted; the kernel mechanically permitting re-adoption is not semantic licence; the w2/1099-div precedents are inapposite because those successions preserved meaning). Root cause: there is NO cross-fact-type succession in the kernel \u2014 apply_bundle_adoption (facts.py:84-101) has no deletion path, compute_currency (currency.py:137-174) admits only same-fact correction, member withdrawal and superseded entities as displacement roots, and supersession policy 'free' (findings.py:556-576) fires only on the same fact_id. The foreman had asserted succession as available without verifying it. PREREQUISITE MILESTONE REQUIRED, framed as fact-type succession and optional-route applicability, NOT deletion or retirement \u2014 history must remain: (1) minimal declared migration/succession mechanism that displaces old fact questions, instantiates new neutral ones, and leaves them OPEN for re-attestation without copying or reinterpreting old answers; (2) mint honestly named neutral identifiers including the thirteenth proposition no-schedule1-line24z-writein, and repoint the nonempty SSA worksheet route; (3) repair the SSA no-activity route so a return with no Social Security source publishes its legal zero without the 33 worksheet-scope declarations \u2014 rule.form1040-line9.v7 unconditionally requires social-security.line6b and the SSA worksheet is its only producer, but that existing burden is NOT a precedent; (4) prove fresh adoption and upgrade behaviour separately; (5) inventory implementation and governance cost BEFORE chartering the build, and if generic substrate is needed treat it openly as the prerequisite's architectural decision. The schedule1-part1-scope.bundle.json vocabulary defect stays a recorded deferral unless the mechanism necessarily touches it. THIS BRANCH: T0c-4 and T0c-5 held; 1098-E implementation NOT chartered; no version numbers allocated; no code written. Settled design survives in the plan's non-chronological Durable findings register. After the prerequisite merges, prepare a concise handoff and RE-CUT 1098-E from current main on the first dependency-safe Schedule 1 Part II to Form 1040 AGI vertical slice; the Track 0a/0b/0c narrative is NOT carried forward. Branch rebased onto origin/main; PR #169 is docs-only and open.",
  "retrospective": null,
  "current_role": "Foreman (1098-E stopped at design; prerequisite milestone unplanned, owner-selection pending)",
  "current_prompt": "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md#Owner ruling \u2014 stop condition fires; this branch is completed design exploration"
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
interest through Schedule A and Form 1040 line 12e. All are on the ratified line.

Every one of those is an **income** or **deduction** route. This branch opens
the first **adjustment to income**: Form 1098-E student-loan interest through
Schedule 1 line 21. It is therefore the first work that ever puts a value on
Form 1040 line 10 and makes adjusted gross income differ from total income.

## Operational State: Engine Breadth

* **Active milestone (this branch):** 2025 Form 1098-E Student-Loan Interest
  through Schedule 1 Line 21 and Form 1040 AGI — **stopped at design**. The stop
  condition fired on the shared Schedule 1 absence vocabulary. The owner ruled
  this branch **completed design exploration**: T0c-4 and T0c-5 are held,
  implementation is **not** chartered, and no code was ever written.
* **Blocking prerequisite (unplanned):** a **fact-type succession and
  optional-route applicability** milestone. Framed as succession, **not**
  deletion or retirement — history must remain. Five items are stated in the
  plan under "The prerequisite is succession, not deletion"; item 5 requires an
  implementation-and-governance cost inventory **before** the build is
  chartered, and any generic substrate must be owned openly as that milestone's
  architectural decision.
* **Why it stopped:** the kernel has **no cross-fact-type succession**
  (`facts.py:84-101` has no deletion path; `currency.py:137-174` admits only
  same-fact correction, member withdrawal, and superseded entities;
  `findings.py:556-576` fires only on the same `fact_id`). Both remaining
  shapes were rejected — dormant predecessors leave twelve permanent orphans,
  and re-declaring the same ids with neutral wording would make existing
  findings answer a **broader question than the taxpayer asserted**.
* **What survives:** the plan's non-chronological **Durable findings register** —
  substrate facts, tax-domain results, standing defects on the ratified line,
  and method results. The replacement plan inherits that register and **not**
  the Track 0a/0b/0c narrative.
* **Re-cut instruction:** after the prerequisite merges, prepare a concise
  handoff and re-cut 1098-E **from current `main`**, scoped to the first
  dependency-safe Schedule 1 Part II → Form 1040 AGI vertical slice.
* **Branch / worktree:** `milestone/f1098e-student-loan-interest-line21` in
  `engine-1098e`.
* **Base:** `origin/main` (`ff25d42`). Rebased `--onto origin/main` from the
  original base `b25562f`, which was **not** an ancestor of `main` because the
  mortgage milestone was curated before merge. Nine commits replayed; one
  `docs/phase-state.md` conflict resolved. Version tips on this base:
  core-calculations **v29**, published **v24**, release **v22**,
  `rule-artifact.v4`, `attachment-rule.v6`, `form-field.v3`, line-9 rule
  **v7**; highest *allocated* fact-type schema is `fact-type.v3`, though all
  content still declares `fact-type.v2`.
* **Dependencies:** discharged. **PR #163** (SSA-1099 lines 6a/6b) merged
  2026-08-10; **PR #168** (Form 1098 mortgage interest) merged 2026-08-10. Both
  are on the ratified line.
* **Rebase delta (verified):** the evaluator operator set is unchanged — still
  no `multiply`, `divide`, or `min`, and still no categorical or boolean
  aggregate; `rule.form1040-line11.json` is unchanged and still publishes AGI
  as a bare `ref` passthrough of total income; the twelve `ss-benefits-scope`
  Schedule 1 absences are present and unchanged. Two post-settlement changes
  Track 1 must respect: `CURRENT_RECORD_SCHEMA` advanced to
  **`derivation-record.v6`** (was v5), and `packages/tax/ssa_benefits.py` was
  substantially reduced, its test-only enforcement surface removed.
* **Plan:** `docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md`.
* **Retrospective:** none yet (milestone not closed).
* **Open items on the ratified line:** the `attachment-rule.v5` provenance
  defect (T0-7); the `schedule1-part1-scope.bundle.json` consumer-scoped-title
  defect (recorded deferral); and cited federal sources absent from the repo
  (five load-bearing citations spot-checked and all verified — an availability
  defect, not an evidence-integrity one).
* **PR:** #169 (draft, docs-only), based on `main`. Carries the design
  exploration; owner to decide whether it merges as the record.
* **Next:** owner selects the prerequisite milestone. Nothing proceeds on
  1098-E until it is settled and merged.

## Re-entry


Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
