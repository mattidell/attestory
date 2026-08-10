<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f1098-mortgage-interest-line12e",
  "active_plan": "docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md",
  "milestone_state": "track-2",
  "status": "**ENGINE BREADTH / FORM 1098 HOME-MORTGAGE INTEREST THROUGH SCHEDULE A AND FORM 1040 LINE 12E — CURATED FOR THE MILESTONE PR; AWAITING FINAL REVIEW + CI.** All findings from every review round are closed and independently re-verified (see `docs/milestone-retrospectives/2026-08-09-f1098-mortgage-interest-line12e.md` for the full account: five Track 1 repair rounds, three Track 2 repair rounds, two rebases). Curated per `PROJECT_PLANNING.md`, \"Milestone Publication Curation\": branch history squashed to atomic Plan / Track-1 / Track-2 commits on top of `origin/main` (48d46f9); the milestone plan doc trimmed to Track 0/1/2 charter content only; interim review docs and repair-round records removed, their lessons distilled into the retrospective; phase-state and coverage-frontier reconciled to the final result. Full suite 1218 passed / 0 failed / 20 skipped, mypy clean, governance_lint conformant, envelope_scan clean, git diff --check clean, additive-only against origin/main (only packages/schemas/derivation/published.json's manifest, one append, and this milestone's own new/edited citizens). Per PROJECT_PLANNING.md step 7, milestone_state stays at track-2 (not closed) until a fresh independent review of this exact curated range and a green CI run both bind the pushed head - that review has not yet happened against this curated head specifically. Pre-curation safety ref: snapshot/2026-08-09-f1098-mortgage-interest-line12e-pre-pr-curation.",
  "retrospective": "docs/milestone-retrospectives/2026-08-09-f1098-mortgage-interest-line12e.md",
  "current_role": "Reviewer (final curated range, owner-launch)",
  "current_prompt": "docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md#Contracts"
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
foreign tax credit, the merged IRA line-4b route, and the bounded SSA-1099
Benefits Worksheet route through Form 1040 lines 6a/6b. This branch is
building Form 1098 home-mortgage interest through Schedule A and Form 1040
line 12e on top of that integrated base.

## Operational State: Engine Breadth

* **Active milestone (this branch):** Form 1098 Home-Mortgage Interest
  through Schedule A and Form 1040 Line 12e — Track 1 built and review-clean
  (4 repair rounds closing successive latent runtime defects), rebased onto
  the SSA-1099 integration tip. Track 2 not yet chartered.
* **Base (post-rebase):** core-calculations **v28** / published **v23** /
  release **v21** / adoption **v28** — the merged IRA line-4b route plus the
  SSA-1099 Benefits Worksheet route, both landed on `milestone/form1040-ssa1099-line6-local`
  at `5a1a980` (SSA-1099 itself still a curated candidate on PR #163, DRAFT,
  awaiting its own final review — unrelated to this branch's own state).
* **Current result:** paper-first Track 0 settled in-doc; Track 1 (Form 1098
  family, singleton closure, seven taxpayer-authority facts, Schedule A line
  8a derivation, full completeness boundary, `count`/`MULTIPLE_F1098_OUT_OF_SCOPE`
  cardinality guard) implemented and verified end-to-end through
  `live_coordinate_run`. This milestone's own schema successors
  (`rule-artifact.v4`, and an `artifact-package` successor admitting it) were
  built against the pre-rebase base and need renumbering/rebuilding against
  the new v28/v23/v21/v28 base — see the status block above.
* **Plan:** `docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md`.
* **Retrospective:** none yet (milestone not closed).
* **Concurrent milestones (untouched, on their own branches/worktrees):**
  PR #163 `milestone/form1040-ssa1099-line6` (DRAFT, curated candidate,
  awaiting its own final review — this branch rebased onto its tip but did
  not alter it).
* **Contracts:** no new ADR yet; Track 0 concluded existing ADR-0015/0016/0017
  (identity/closure), ADR-0036 (attachment ontology), ADR-0020/0027/0029/0033/0046
  (explanation/package/citation/presentation) are sufficient by content-level
  reuse — no governance escalation needed.
* **Next:** reconcile this milestone's schema-version successors against the
  new base (mechanical renumbering, additive only), verify no destructive
  changes to any existing schema version, then continue to Track 2.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
