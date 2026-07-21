# Foreman Handoff Note

A lightweight, living continuity note — **not a protocol and not a gate.** The
foreman keeps this current *enough* during multi-step work that, if a session
ends mid-task, a fresh foreman can resume without re-deriving everything. Update
it opportunistically; there is no required cadence and no ceremony. It describes
*now*, not history — overwrite stale content freely (durable history lives in
commits, retrospectives, and process logs).

## How the owner relaunches a foreman

Start a fresh session and say, roughly: *"Resume as foreman. Read
`docs/phase-state.md`, `docs/foreman-handoff.md`, and the active plan they point
to, then continue."* The new foreman reads those, reconciles the in-flight state
below against `git status` / `git log`, and proceeds. If the note looks stale
against git, trust git and say so.

**Discipline:** a step is not done until `phase-state.md`'s "Next" is advanced too — it is the re-entry pointer the next reader (foreman *or* clerk) anchors on, so updating only this handoff leaves them stale.

## Standing policy — relocated

The foreman's stable posture (boot read-set, PR-vs-branch rule, dispatch
staging discipline, verification floor, data boundary) now lives in
**`docs/roles/foreman.md`** — read it on boot. It was moved there so this
note can go back to being purely *describes-now* continuity (overwritten
freely) without carrying stable doctrine that risks going stale in a
volatile file. The binding ADRs are unchanged (0005, 0013, 0030, 0034;
routing via `docs/adr/INDEX.md`, ADR-0039).

## Current state (updated 2026-07-20; Track 3 PR #36 open — awaiting owner merge)

- **Seat:** principal foreman. Active milestone: **Dividends and Schedule B
  Slice**. All four milestone ADRs ratified: ADR-0035 (D3), ADR-0036 (D1),
  ADR-0037 (`conditional_dependency_set`, merged as Track 0a, PR #30),
  ADR-0038 (D2, ratified 2026-07-19 after the full Round 1 → Repair 1 →
  Confirmation R1 → Repair 2 → Confirmation R2 arc; disposition:
  `docs/prototypes/qdcg-worksheet/evaluation-analysis.md`).
- **Merged tracks:** Track 0a (PR #30, `6f303fe`), Track 1 (PR #31,
  `a870a2f`), Track 2 (PR #32, `c39c6c7` — review found blocking F1, the
  Part I tie-out targeting line 2b's four-family total instead of
  `b1-subtotal`; repaired `854c71a`, delta re-review READY). Process:
  ADR-0030 amendment (PR #33), ADR-0039 (PR #34), ADR-0040 trusted-advisor
  seat (PR #35). Track-by-track detail lives in the review records under
  `docs/reviews/` and git history, no longer restated here.
- **➡️ Track 3 (line 16 under D2) — reviewed NOT READY 2026-07-20, F1 fix
  in flight** — charter `ebec569`, builder commits `3b3db78`/`a0574a5`/
  `7732cc5`/`f12e7a1`, review charter `d858172`, review verdict `c0731f4`
  (`docs/reviews/2026-07-20-dsbs-t3-qdcg-line16-review.md`) on
  `track/dsbs-t3-qdcg-line16` (worktree `../finances-t3-qdcg`). Review
  independently confirmed all 9 content/design checks pass — including
  real scrutiny (not rubber-stamp) of the builder's two self-flagged
  judgment calls: the domain-guard scoping (deliverable 1, confirmed sound
  and not under-enforcing) and the `marshal.py` `_rule_required_symbols`
  collateral extension (confirmed load-bearing and additive-only).
  **Blocking: F1** — the builder's claim that 2 failing unittest cases
  pre-date the branch was wrong; the reviewer independently reran the base
  comparison and found both genuinely regress on this branch.
  Root cause: two unrelated FRRS-era tests
  (`test_frrs_t3_resolver_bootstrap.py`,
  `test_frrs_t4_w2_live_integration.py`) select a rule file to tamper via
  unfiltered `glob("rule.*.json")[0]`, relying on incidental ordering to
  land on a file that's actually a member of the package/release each test
  resolves — Track 3's new `rule.form1040-line16.v2.json` now sorts first
  and isn't a member of those tests' target packages, so the tamper goes
  undetected and the expected `Refusal` never fires. Not a Track 3 content
  defect. Fix charter `c9e8544`
  (`docs/reviews/charter-2026-07-20-dsbs-t3-f1-remediation.md`): make both
  tests select their target member deterministically from their own
  package/release manifest, not directory order; scope is additive-only,
  does not touch DSBS content or the resolver implementation unless a
  charter-stop is hit. **Fixed, commit `1247b89`**: both tests now match
  target files by `(id, version)` membership in
  `package.interest-slice.json`, mirroring
  `production_resolver.py`'s own match key — not glob order. Battery
  confirmed green by the fix builder: 541/541 unittest, mypy clean,
  governance lint conformant, envelope scan clean; no DSBS/kernel/resolver
  file touched, only the two test files. No escalation needed. Delta
  re-review committed `5aa47b5`
  (`docs/reviews/2026-07-20-dsbs-t3-f1-delta-rereview.md`): **verdict not
  ready**, but F1 itself confirmed genuinely discharged (reviewer read
  `production_resolver.py`'s actual match key and confirmed the fix
  targets it) and zero DSBS/kernel/resolver files touched. Two residual
  findings: **R2** — the re-review charter's diff range literally
  included the review-charter commit `c9e8544` alongside the two test
  files; a charter-drafting artifact on the foreman's part (the
  reviewer's own Check 3 confirms the real fix commit and
  `c9e8544..1247b89` are exactly two files) — triaged as resolved, no
  code involved. **R1** — the fix still breaks on the first sorted match
  among five qualifying package members rather than naming one explicit
  target; deterministic today but the same implicit-first-match shape
  that caused F1, just narrowed. Fix charter committed `1636110`
  (`docs/reviews/charter-2026-07-20-dsbs-t3-r1-remediation.md`): both
  tests to select `tax.us.2025.rule.form1040-line2b` v1 explicitly by id,
  asserting loudly if it's ever missing/renamed rather than silently
  substituting. **Fixed, commit `c1cd01f`**: both tests now open
  `rule.form1040-line2b.json` directly by known filename, assert package
  membership (`role: "computation"`, confirmed at
  `package.interest-slice.json:37`) and loaded-body identity match before
  tampering — no scan-and-break-on-first-match left. Battery green per
  fix builder: 541/541 unittest, mypy clean, governance lint conformant,
  envelope scan clean; diff is exactly the two test files. Final delta
  re-review charter committed `cf08e37`
  (`docs/reviews/charter-2026-07-20-dsbs-t3-r1-delta-rereview.md`) —
  explicitly scopes the object to commit `c1cd01f` alone (charter commit
  `1636110` called out as administrative, to avoid repeating R2's
  charter-range mistake) and folds in confirming R2's resolution.
  **Final verdict: READY**, commit `ec6d296`
  (`docs/reviews/2026-07-20-dsbs-t3-r1-delta-rereview.md`) — all 7 checks
  passed outright, zero findings (S1... series empty). Track 3 as a whole
  (original build + F1 fix + R1 fix) is confirmed mergeable: five
  ADR-0038 production conditions, six named golden classes, two rounds of
  independent re-review with real scrutiny (not rubber-stamped — both
  prior rounds found genuine issues the builder's own self-report missed
  or under-specified). Pushed and **PR #36 opened** 2026-07-20:
  https://github.com/mattidell/attestory/pull/36. **NEXT ACTION: owner
  reviews/merges PR #36.** After Track 3 merges: Track 4 (1099-DIV
  closure content and live integration) closes the milestone.
- **Lessons a Track 3 builder needs** (also baked into the charter):
  bundle-adoption, not bare `fact-type.v2` members (kernel registry
  rejects assertions referencing bare members — Track 2 hit this);
  `conditional_dependency_set` is v3-only by schema; the guard node goes
  first and unconditionally in the outer `all` (confirmed Repair 2 shape);
  a composing rule's `requires` gate reports `DEPENDENCY_ABSENT` while the
  blocked rule carries its own code — check committed goldens before
  asserting block codes.
- **Env note:** if mypy/unittest fail on `str | None` syntax parse errors,
  the `.venv` symlink degraded to system python3.9 — rebuild:
  `rm -f .venv/bin/python3 .venv/bin/python && /opt/homebrew/bin/python3.13
  -m venv --clear .venv && .venv/bin/python3 -m pip install -r
  requirements.txt`.
- **Boundary discipline (standing):** values, dispositions, refusal reasons,
  and the workspace location never enter the repository, a review, or a chat
  session; only the three-fact attestation crossed. Owner-held run tooling
  (`tools/scaffold_live_acts.py`, `workspace-seed/`) stays untracked.

## Historical record

The Core Tax Conditions remediation (closed 2026-07-15) trail formerly kept
here lives in `docs/milestone-retrospectives/2026-07-15-core-tax-conditions-and-presentation-integration.md`,
the `docs/reviews/charter-2026-07-15-*` chain, and git history.

- **Git/env hygiene:**
  - Run all tests via `.venv/bin/python3 -m unittest` (project `.venv`).
  - Validate conformance via `.venv/bin/python3 tools/governance_lint.py`; mypy via `-m mypy`.
  - Commit per logical unit; owner authorizes execution and launches seats.
