<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f1098e-student-loan-interest-line21",
  "active_plan": "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md",
  "milestone_state": "track-0",
  "status": "**ENGINE BREADTH / 2025 FORM 1098-E STUDENT-LOAN INTEREST THROUGH SCHEDULE 1 LINE 21 AND FORM 1040 AGI \u2014 TRACK 0 REOPENED.** The Track 0 settled declaration is WITHDRAWN. Owner review returned three findings, all accepted: (F1, P1) sixteen of the seventeen eligibility components are statement-set-dependent but keyed by tax-year alone, so a late statement is silently authorized by an attestation never made about it; (F2, P1) a closed-empty 1098-E family lets B1 not-claimed-as-dependent block line 21, line 26, line 10 and therefore AGI, which is semantically wrong; (F3, P2) the T0-5 reuse of the twelve ss-benefits-scope Schedule 1 absences was priced against an unratified PR #163 that has now merged, and the reused facts declare Social Security Benefits Worksheet scope in their own titles, so reuse fails the claim-reuse proof on declared authority scope. Pricing: F1 does NOT fire the stop condition \u2014 the identity-key vocabulary already admits {kind: entity, name: family-horizon} and the ratified line uses it 37 times on every *.source-closure fact type, so horizon-binding substantive declarations is content-level reuse needing no evaluator change and no ADR; the alternative (per-statement authority plus a real aggregate) WOULD need new substrate, since the evaluator has no categorical or boolean aggregate at all. F2 resolves to a closed-empty canonical-zero branch carrying closure and C2 provenance, and exposes a second correction: B1=no is a legal zero, not an unsupported block, so every component must be decided individually. F3 blast radius is three files (ss-benefits-scope.bundle.json, rule.ss-benefits-worksheet.json, tests/test_ssa1099_benefits_line6_track2.py); disposition is a shared return-level successor with the SSA-scoped originals superseded, a bridging rule being rejected as repairing upstream scope with a downstream note. Track 0c is chartered with five work items T0c-1..T0c-5 and five now-mandatory Track 0 outputs (authority-lifecycle table, empty/nonempty authority matrix, late-authority counterexample walk, claim-reuse proof, neighboring-capability dependency diff) plus a required Track 0 adversarial-closure declaration, currently four FAILs. Standing rule adopted: Track 0 may not be marked settled while it contains a known semantic coupling unless the plan carries a counterexample showing the coupling is correct. INTEGRATION DONE: PR #163 and PR #168 both merged; this branch rebased --onto origin/main from b25562f (the old base was not an ancestor, the mortgage milestone having been curated before merge), nine commits replayed, one docs/phase-state.md conflict resolved; PR #169 retargeted to main. Delta verified: evaluator operator set unchanged, rule.form1040-line11 still a bare AGI passthrough, the twelve absences present and unchanged; but CURRENT_RECORD_SCHEMA advanced to derivation-record.v6 and packages/tax/ssa_benefits.py was substantially reduced. Track 1 is not chartered. No version numbers allocated. The attachment-rule.v5 provenance defect from T0-7 remains open and untouched.",
  "retrospective": null,
  "current_role": "Foreman (Track 0 reopened; Track 0c chartered, not yet performed)",
  "current_prompt": "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md#Track 0c work items"
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
  through Schedule 1 Line 21 and Form 1040 Adjusted Gross Income — **in
  progress**. Track 0's settled declaration is **withdrawn**; owner review
  returned three findings (two P1), all accepted. **Track 0c** is chartered to
  re-settle. Track 1 (implementation) is not chartered.
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
* **Contracts:** SLI-C1–C10; Track 0c must restate C2, C5, C6, and C8. The
  `multiply`/`divide` expression extension still claims the milestone's single
  expected ADR. F1 and F2 are priced as needing **no** ADR; F3 may need one.
* **Open findings (Track 0c):** F1 statement-set-dependent authority keyed only
  by tax year — disposition is `['family-horizon', 'tax-year']` re-keying, which
  is content-level reuse of substrate the ratified line already uses 37 times,
  so the stop condition does **not** fire. F2 closed-empty family lets B1
  suppress AGI — disposition is a closed-empty canonical-zero branch with
  closure and C2 provenance, plus a per-component legal-zero-vs-block decision.
  F3 the SSA-scoped absence reuse fails the claim-reuse proof on declared
  authority scope — disposition is a shared return-level successor; blast radius
  is three files.
* **Open item, unchanged:** the `attachment-rule.v5` provenance defect recorded
  by T0-7.
* **PR:** #169 (draft), based on `main`.
* **Next:** perform Track 0c, discharge the five mandatory Track 0 outputs and
  the adversarial-closure declaration (currently four FAILs), then re-settle
  Track 0 before Track 1 is chartered.

## Re-entry


Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
