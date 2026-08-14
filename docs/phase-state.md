<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "ssa-no-activity-applicability",
  "active_plan": "docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md",
  "milestone_state": "track-1",
  "status": "NOT YET CLOSED: a targeted independent re-review of this repair and a green exact-head CI run are still required. SHIPPED CONTRACT: rule.ss-benefits-worksheet v2 (rule-artifact.v4) is the SOLE producer of tax.us.2025.social-security.line6b. 11 unconditional requires = no-rrb-or-foreign-social-benefit, the seven derived numeric inputs, social-security.line6a, filing_status, rounding.convention. Guard = all[require_closed(ssa1099.benefits) BOTH routes; conditional_dependency_set of the 22 worksheet-only declarations gated on count>0; categorical_compare(no-rrb == yes) BOTH routes; any[count==0, all[22 conjuncts, MFS set]]]. Value = choose(count==0 -> 0, else -> the UNCHANGED v1 worksheet expression). Stated in full and ONCE at the plan's '## Track 0 settlement - final contract'. T0-1 ANSWERED 33 -> 1: no-rrb-or-foreign-social-benefit is load-bearing, retained on both routes, and recorded as a FOURTEENTH migration candidate for Milestone 2, not acted on here. A CHARTERED TWO-PRODUCER DESIGN WAS TRIED AND WITHDRAWN BEFORE ANY VERSION OF IT SHIPPED: line6b is form-field-bound, presentation_projection._one_row admits exactly one disposition row, and the runner records a row for every rule on every path. schedule-a.total is never form-field-bound, so the precedent never transferred. PR #175 generalizes the lesson as a sixth Track 0 adversarial-closure artifact (see the plan's '### 6. Integration-surface artifact'), satisfied by evidence already committed. PUBLICATION GENERATION IS v30: package.core-calculations.v30 / published-packages.v25 / demo.release.2025.v23 / adopt-core-v30-current - the LOWEST versions free on the ratified line (origin/main tops out at package v29 / published-packages v24 / release v22). ss-benefits-scope STAYS AT ITS BASE v1 - no vocabulary successor exists. A NOT-READY REVIEW FOUND A REAL DEFECT AND IT IS NOW REPAIRED AT THE ROOT: the withdrawn ss-benefits-scope.bundle.v2 existed only because package_validation check 10a required an exact value_schema shape {\"enum\": [...]} for the ADR-0038 {yes,no} domain guard, rejecting the corpus's equally-valid {\"type\": \"string\", \"enum\": [...]} spelling; the worksheet's 23 category_literal pins (plus rule.form1040-line6c's one) were never repointed to v2, so the shipped citizen validated against a fact-type version the package no longer selected - serialized property order/presence mistaken for semantic domain identity. Repaired by changing check 10a to recognize both spellings as the same closed domain (rejecting extra enum values, open string domains, booleans, and incompatible types) and by withdrawing the bundle succession entirely - ss-benefits-scope reverts to v1 everywhere, worksheet v2's pins are unchanged and now correct. A NEW package-validation check (CATEGORY_LITERAL_PIN_STALE) rejects any category_literal exact pin whose (id, version) is not an actual package member, with mutation tests for a stale version and a missing fact type; the real package.core-calculations.v30 now validates with zero issues. COORDINATION ITEM FOR MILESTONE 2 IS RETRACTED: its predecessor population is ss-benefits-scope v1, as it always was on the ratified line - not v2. THE STALE TARGETED-REVIEW RECORD AND THE DUPLICATIVE PROTOTYPE SUITE ARE BOTH REMOVED: docs/reviews/2026-08-13-ssa-no-activity-v4-targeted-rereview.md and tests/test_ssa_no_activity_prototype.py no longer exist; their durable findings (the six-of-seven dependency-cost claim; the numeric-inputs-unconditional guard) live entirely in the permanent 28-test tests/test_ssa_no_activity_line6b_track1.py, which is the sole executable evidence for this contract. THE MOST LOAD-BEARING FACT, and the one a future edit is most likely to break: the seven derived numeric inputs are NOT conditional-set members. requires is the engine's only sequencing gate, conditional-set membership is invisible to eligibility, and a blocked rule resolves permanently - so conditionalizing them makes the rule eligible before its inputs publish and permanently blocks the nonempty route. Held by test_conditionalizing_the_numeric_inputs_breaks_the_nonempty_route on the PUBLISHED citizen. NO ADR IS OWED for the worksheet content; the check-10a/10b package_validation repair is an engine-level fix, owner-directed, not milestone content. STANDING CONSTRAINTS: no seat reads tax-instruction PDFs; do not broaden presentation_projection._one_row; do not widen audit_collect_authority (durable deferral, deliberately left open); closure is required on both routes for the SEMANTIC reason (line 6b must not publish until the current SSA family is confirmed complete), never justified by the count limitation; this is an SSA worksheet contract decision, not a change to collect semantics and not a precedent that every nonempty family requires closure. HISTORY REWRITTEN AGAIN for this repair: commits carry no generated co-author trailers or session material; only the open milestone branch was rewritten; force-pushed with lease. OPEN FOR OWNER: PR #173 (this milestone, NOT ready - awaiting fresh independent re-review and green exact-head CI on the rewritten head), PR #175 (integration-surface gate, merged), PR #172 (split record), PR #169 (stopped 1098-E design exploration).",
  "current_role": "Foreman (validator repair applied; awaiting fresh independent re-review and green exact-head CI before closeout)",
  "current_prompt": "docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md#Track 0 settlement — final contract"
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
foreign tax credit, the merged IRA line-4b route, the bounded SSA-1099
Benefits Worksheet route through Form 1040 lines 6a/6b, and the bounded Form
1098 home-mortgage interest route through Schedule A and Form 1040 line 12e.
This branch opens no new tax route. It is **Milestone 1 of a two-milestone
prerequisite** standing between the engine and Form 1098-E student-loan interest.
It repairs an applicability defect already on the ratified line: a return with no
Social Security source cannot reach total income without answering 33 Social
Security declarations.

## Operational State: Engine Breadth

* **Active milestone (this branch):** SSA no-activity applicability repair —
  **not yet ready.** A NOT READY review found a real package-validation defect
  (below); it is now repaired at the root, but a fresh independent re-review
  of the repair and a green exact-head CI run are still required before
  closeout. Milestone 1 of the owner-approved two-milestone split. Milestone 2
  (`fact-type-succession-neutral-schedule1`) is chartered only after this merges,
  on its own branch and PR. **They do not share a PR.**
* **Objective, met:** a return with no applicable Social Security source publishes
  the legally authorized line-6 zero and proceeds through line 9 without
  satisfying worksheet-only scope declarations.
* **The defect, repaired:** `rule.ss-benefits-worksheet` was the **only** producer
  of `tax.us.2025.social-security.line6b` corpus-wide and carried **33**
  `requires`, while `rule.form1040-line9.v7` requires line 6b **unconditionally** —
  so every return in the engine had to satisfy 33 Social Security declarations to
  reach total income.
* **The shipped contract:** `rule.ss-benefits-worksheet` **v2** under
  `rule-artifact.v4`, the **sole** producer of line 6b. Eleven unconditional
  `requires` (the retained declaration, the seven derived numeric inputs,
  `social-security.line6a`, `filing_status`, `rounding.convention`); an ADR-0037
  `conditional_dependency_set` of **22** worksheet-only declarations gated on
  `count > 0`; unconditional `require_closed` on **both** routes; a value-level
  `choose` selecting canonical `0` or the **unchanged** v1 worksheet expression.
  Full statement: the plan's `## Track 0 settlement — final contract`. The
  notes state directly, and correctly, that `rule.form1040-line9` requires
  **six**, not all seven, of the unconditional numeric inputs; the seventh,
  `tax-exempt-interest.line2a-total`, was already required by worksheet **v1**,
  so the cost of requiring it here is pre-existing, not new.
  `TestDependencyCostWitness` in `tests/test_ssa_no_activity_line6b_track1.py`
  is the durable regression witness for that claim.
* **T0-1 answered 33 → 1:** `no-rrb-or-foreign-social-benefit` is load-bearing and
  is retained, active on both routes — the closure claim's own text disclaims
  RRB-1099, SSA-1042S and foreign systems, and a zero that silently ignored a
  disclaimed neighbouring class would be a default wearing the clothes of an
  authority. It is recorded as a **fourteenth** migration candidate for
  Milestone 2 and **not acted on here**.
* **A chartered two-producer design was tried and withdrawn, before any
  version of it ever shipped.** Track 0 chartered two disjoint producers
  copying `rule.schedule-a-total-closed-empty`; Track 1's build proved that
  unbuildable, because line 6b is form-field-bound,
  `presentation_projection._one_row` admits exactly one disposition row, and the
  runner records a row for **every** rule on **every** path.
  `tax.us.2025.schedule-a.total` is never form-field-bound, so the precedent never
  transferred. The reusable lesson — *a precedent is silent about the properties
  it never had to satisfy, and that silence is not permission* — is generalized by
  PR #175 as a sixth Track 0 adversarial-closure artifact (the plan's
  `### 6. Integration-surface artifact`), satisfied by evidence already
  committed.
* **Publication generation:** `package.core-calculations.v30` /
  `published-packages.v25` / `demo.release.2025.v23` / `adopt-core-v30-current`
  — the **lowest** versions free on the ratified line (`origin/main` tops out
  at package `v29` / registry `v24` / release `v22`). `ss-benefits-scope`
  stays at its base **v1** everywhere: no vocabulary successor exists.
* **The validator defect, and its repair.** `ss-benefits-scope.bundle.v2`
  existed only because `package_validation` check 10a required an exact
  `value_schema` shape (`{"enum": [...]}`) for ADR-0038's `{yes, no}` domain
  guard, rejecting the corpus's equally valid `{"type": "string", "enum":
  [...]}` spelling. The worksheet's 23 `category_literal` pins (plus
  `rule.form1040-line6c`'s one) were never repointed to `v2`, so the shipped
  citizen validated against a fact-type version the package no longer
  selected — serialized property order/presence mistaken for semantic domain
  identity. Repaired at the root: check 10a now recognizes both spellings as
  the same closed domain (still rejecting extra enum values, open string
  domains, booleans, and incompatible types), and the bundle succession is
  withdrawn entirely. A new check, `CATEGORY_LITERAL_PIN_STALE`, rejects any
  `category_literal` exact pin whose `(id, version)` is not an actual package
  member, with mutation tests for a stale version and a missing fact type.
  `package.core-calculations.v30` now validates with **zero** issues.
* **Coordination item for Milestone 2 is retracted.** Its predecessor
  population is `ss-benefits-scope` **v1**, as it always was on the ratified
  line — not v2.
* **The stale targeted-review record and the duplicative prototype suite are
  both removed.** `docs/reviews/2026-08-13-ssa-no-activity-v4-targeted-
  rereview.md` and `tests/test_ssa_no_activity_prototype.py` no longer exist;
  their durable findings live entirely in the permanent 28-test
  `tests/test_ssa_no_activity_line6b_track1.py`, the sole executable evidence
  for this contract.
* **Posture:** content-level for the worksheet contract itself. The check-10a
  / check-10b `package_validation` repair is an owner-directed engine-level
  fix, not milestone content. No new schema family, no ledger entry, **no ADR
  owed**.
* **Standing constraints:** no seat reads tax-instruction PDFs; do not broaden
  `presentation_projection._one_row`; do not widen `audit_collect_authority`
  (durable deferral, deliberately left open); closure is required on both routes
  for the **semantic** reason, never justified by the `count` limitation.
* **Branch / worktree:** `milestone/ssa-no-activity-applicability-repair`, cut
  from and rebased 2026-08-13 onto `origin/main` (`71ea50e`, includes PR
  #175's integration-surface gate). Curated the same day: reset to that base
  and rebuilt as one commit per track, collapsing the accreted v2/v3/v4 and
  v29–v32 development chain to the lowest free versions. A subsequent NOT
  READY review found the version-pin defect above; repaired and the branch
  rewritten again, with no generated co-author trailers or session material.
  **PR #173** (draft, not ready).
* **Plan:** `docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md`.
* **Split record:** `docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md` (PR #172).
* **Open for the owner:** PR #173 (this milestone), PR #175 (integration-surface
  gate), PR #172 (split record), PR #169 (stopped 1098-E design exploration).


## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
