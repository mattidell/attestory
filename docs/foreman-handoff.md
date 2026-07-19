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

## Current state (updated 2026-07-19; Track 2 build in flight, deliverables 1-4 landed)

- **Seat:** principal foreman. Active milestone: **Dividends and Schedule B
  Slice**. Track 0 is CLOSED: ADRs 0035/0036/0037 ratified; Track 0a
  (generic `conditional_dependency_set` production substrate) merged as
  **PR #30 (`6f303fe`)** after its full review chain — independent review
  not-ready (F1–F4) → foreman repair `595c4e1` → independent delta
  re-review **ready** (`61452e5`; non-blocking R1 act-determinism note, R2
  private `_content_id` import). D2 adoption is unblocked.
- **Track 1 (schema citizens) build is COMPLETE** on
  `track/dsbs-t1-schema-citizens` (`c6d62f6`), charter
  `docs/reviews/charter-2026-07-19-dsbs-t1-schema-citizens.md`. Landed:
  `1d2a58b` vocabulary reconciliation (SOURCE_SET emit-vs-record,
  ADR-0036 PC3; `ITEMIZATION_TIE_OUT_VIOLATION` named, PC1 vocabulary half),
  `2a08d80` 1099-DIV statement/family/closure citizens, `60bbbc0`
  `dividend-universe.v1`, `272b7a9` generic attachment citizen surface,
  `a6f11f3` the two admission-time validation guards (ADR-0035 runtime
  universe guard; ADR-0036 presence-encoding guard). Full battery green at
  handoff: 477 tests, mypy clean (94 files), governance lint conformant,
  envelope scan clean (rebuilt `.venv` on python3.13 first — the prior venv
  was a broken symlink to system python3.9, which cannot parse this repo's
  `str | None` syntax; rebuild pattern: `rm -f .venv/bin/python3
  .venv/bin/python && /opt/homebrew/bin/python3.13 -m venv --clear .venv &&
  .venv/bin/python3 -m pip install -r requirements.txt`).
- **Track 1 independent pre-merge review returned READY** (`5bfbf52`,
  `docs/reviews/2026-07-19-dsbs-t1-schema-citizens-review.md`, dispatched as
  a background sub-agent under
  `docs/reviews/charter-2026-07-19-dsbs-t1-schema-citizens-review.md`). All
  eight charter checks hold; six findings (F1–F6), all non-blocking/
  observational with file/line evidence (notably F3: the runtime universe
  guard's v1/v2 exemption covers only the `COLLECT_TARGET_NOT_FAMILY` half,
  by design and tested — `RECORDED_NON_COMPOSABLE_INPUT` is unconditional).
  Foreman triage: no repair needed. Full battery re-run fresh by the
  reviewer in its own worktree: 477 tests OK, mypy clean, governance lint
  conformant, envelope scan clean.
- **Track 1 MERGED** — PR #31, `a870a2f` on `main`.
- **Track 2 scope confirmed by owner** (proceed with the full-machinery
  reading); charter:
  `docs/reviews/charter-2026-07-19-dsbs-t2-composition-conditional-machinery.md`
  on `track/dsbs-t2-composition-conditional-machinery` (`1739737`).
- **Build IN FLIGHT.** First builder dispatch was interrupted mid-task by an
  API session-limit error (not a real failure) after landing one clean
  commit and leaving a second deliverable's work uncommitted. Foreman
  (this session) reconciled directly: found the uncommitted work
  substantially complete and correct, fixed one genuinely wrong test
  expectation and one mypy `self.run = run` `TestCase.run`-shadowing bug,
  reverified the full battery, and committed a clean checkpoint. **Landed
  on the branch:**
  - `6312cc4` — **deliverables 1 AND 2** (charter listed them separately;
    the builder correctly recognized one generic kernel hook covers both):
    the ADR-0035 1b≤1a admission-time subset invariant
    (`packages/kernel/findings.py`, a new `registry.subset_invariant_pairs`
    hook in the same fold every admission path already uses — `project()`,
    `apply_contribution_batch`, the live coordinator — so it is
    domain-agnostic kernel machinery, not tax-specific code) with full
    rejection-semantics tests and the same-batch ordering kill-tests
    (`tests/tax/test_dsbs_t2_dividend_admission.py`, 9 tests covering both
    orderings within one batch). 486 tests green at that commit.
  - `2ed1c9c` — **deliverables 3 and 4**: box-1a/1b subtotal rules, lines
    3a/3b with per-box closure independence, line-9 v2 folding in 3b,
    shipped as `tax.us.2025.package.core-calculations` v4 (distinct
    synthetic scope, year 2053, so v3 stays independently exercisable).
    Goldens in `tests/test_dsbs_t2_coordinator.py` enter through
    `live_coordinate_run` per the charter's mandatory shape. One test fix
    worth knowing for the next builder: **when a composing line's
    `requires` names a subtotal symbol that itself blocked on an unclosed
    family, the composing line reports `DEPENDENCY_ABSENT` (its own `when`
    never runs — `requires` gates evaluation first, `runner.py:310`), and
    the subtotal rule itself reports `SOURCE_SET_UNCLOSED`** — verified
    against the already-committed `unclosed_interest_composition` golden
    for line 2b, the exact same two-tier pattern. Don't assume the
    composing line carries the closure code directly; check the committed
    goldens before asserting a block code. 493 tests green at this commit,
    mypy clean, governance lint conformant, envelope scan clean.
- **➡️ NEXT ACTION: continue the build — deliverables 5–8 remain** (the
  complete Schedule B attachment): 5 existence conditional (>$1,500 over
  2b+3b, `guard_inapplicable`-family not-required disposition), 6
  `collect_members` itemization mechanism for Part I/II rows tying to
  2b/3b, 7 the `ITEMIZATION_TIE_OUT_VIOLATION` derivation-time check with
  both named kill-tests (stale row set, stale line — vocabulary already
  landed in Track 1, do not add a new code), 8 Part III completeness over
  two new taxpayer-assertion fact types (foreign account, foreign trust)
  with presence-semantics and the foreign-account yes-branch's 7b-country
  requirement + named-not-produced FinCEN-114 obligation. All six named
  golden classes in the charter's Verification section must be satisfied
  before this track is done; three remain unbuilt (attachment
  not-required, required-and-complete whole-form, required-and-incomplete
  honest block). **Reconcile against `git log`/`git status` on
  `track/dsbs-t2-composition-conditional-machinery` first — trust git over
  this note.**
- **Boundary discipline (standing):** values, dispositions, refusal reasons,
  and the workspace location never enter the repository, a review, or a chat
  session; only the three-fact attestation crossed. Owner-held run tooling
  (`tools/scaffold_live_acts.py`, `workspace-seed/`) stays untracked.

## Historical record — Core Tax Conditions remediation (closed 2026-07-15)

- **Seat:** principal foreman.
- **✅ MILESTONE COMPLETE (2026-07-15, remediated re-close).** Tracks 0–7 landed and remediated; retrospective written (`docs/milestone-retrospectives/2026-07-15-core-tax-conditions-and-presentation-integration.md`); closure records (milestone doc, roadmap, phase-state) updated; ADR-0013 amendment + **ADR-0030** ratified; owner reconciled `main` (reset to `7a90f89`). Verification green: 350 tests, mypy, governance lint. **➡️ Next: the owner performs the single no-ff merge of this branch to `main`** (per ADR-0030 Transition — this milestone merges once; per-ADR/per-track granularity starts next phase). **After merge: next-phase planning is owner-directed — do not infer it.** The R1–R5 remediation trail below is the "how we got here" record; the retrospective is the durable account.
- **Milestone REOPENED for remediation (owner-directed 2026-07-15).** The Core
  Tax Conditions implementation was executed Tracks 1–6 and merged to `main`
  (`2fbc3a7`) in one autonomous run **without owner go and without a pre-merge
  review**. Owner rewound state to the last development commit `9dfcd62` on a
  recreated `milestone/core-tax-conditions` branch. **`main` still carries the
  premature merge (`2fbc3a7`) + post-merge docs (`1b370b7`) — an owner decision
  on how to reconcile `main` is pending; the foreman has NOT rewritten `main`.**
- **What's on this branch:** all development code — Track 0 (ADRs 0020, 0024–0029
  accepted) + Tracks 1–6 schemas/content/engine, package-instance checksum
  (`2329469`), strict-typing restore (`9dfcd62`). Verification currently green:
  348 tests, mypy clean (76 files), governance lint conformant.
- **Retrospective pre-merge review done** (`docs/reviews/2026-07-15-core-tax-conditions-premerge-review.md`,
  author-independent foreman): **keep the code; not merge-ready as closed.**
  Sound/faithful — ADR-0020 ledger+walk, ADR-0028 quantity surface, 0024/0025/
  0026/0029. **PMR-1 decision-blocking:** ADR-0027 decision 9 exclusive execution
  projection (ACM-A1) NOT implemented — co-located content is not inert. **PMR-2
  production condition:** ADR-0027 ACM-A5 member-byte verification absent. PMR-3
  Track 4 shipped with a stubbed checksum; PMR-4–7 process (no owner go, no
  pre-merge review, retrospective silent on process, Track 1 pre-typing-green).
- **Remediation chartered** (`docs/reviews/charter-2026-07-15-core-tax-conditions-remediation.md`):
  R1 exclusive projection (decision-blocking), R2 member-byte verification,
  R3 re-verify, R4 **independent** re-review, R5 honest re-close + retrospective
  rewrite + owner `main` reconciliation.
- **R1 landed:** `85ce351` implements ADR-0027 decision 9's exclusive execution
  projection and adds the required ACM-A1 golden. The scenario's JSON output
  matches its committed golden; `tests.tax.test_track6_integration` is green.
- **R2 landed (`351c880`):** member-citizen bytes are registry-verified during
  package resolution; the required unchanged-identity mutation golden passed
  in `tests.derivation.test_package_validation` (13 tests). The ad-hoc checksum
  generator used to produce registry entries is preserved under ignored `temp/`.
- **R3 chartered:**
  `docs/reviews/charter-2026-07-15-core-tax-conditions-r3-reverification.md`
  assigns an owner-launched verifier the complete suite, mypy, and governance
  lint. Failures stop for foreman triage; passing evidence opens R4 only.
- **R3 passed:** all three required commands are green; durable evidence is
  `docs/reviews/2026-07-15-core-tax-conditions-r3-verification.md`. R4 is now
  eligible for its owner-launched independent review.
- **R4 chartered:**
  `docs/reviews/charter-2026-07-15-core-tax-conditions-r4-independent-rereview.md`
  assigns a fresh independent reviewer four falsifiable checks over R1/R2 and
  requires an explicit `ready` / `not ready` verdict. The foreman will not
  review the artifact's merits.
- **R4 returned `not ready` (`30c4248`):** the R1 mechanism is sound, but its
  required ACM-A1 golden is not run by any committed test. Triage is recorded
  in `docs/reviews/2026-07-15-core-tax-conditions-r4-triage.md` as
  decision-blocking, without reopening the ADR contract.
- **Repair1 chartered:**
  `docs/reviews/charter-2026-07-15-core-tax-conditions-repair1-acm-a1-execution.md`
  permits only wiring the existing ACM-A1 scenario into the executed golden
  suite. Then repeat R3 verification and fresh independent R4 review.
- **Repair1 landed (`6c6f42f`):** the ACM-A1 scenario is now in Track 6's
  executed golden set and has an explicit absence assertion; the focused Track
  6 integration suite passed (4 tests).
- **R3R chartered:**
  `docs/reviews/charter-2026-07-15-core-tax-conditions-r3r-reverification-after-repair1.md`
  repeats complete verification before the required fresh independent R4R
  review.
- **R3R passed:** all three required commands are green; durable evidence is
  `docs/reviews/2026-07-15-core-tax-conditions-r3r-verification.md`. Fresh
  independent R4R review is now eligible.
- **R4R chartered:**
  `docs/reviews/charter-2026-07-15-core-tax-conditions-r4r-independent-rereview.md`
  assigns a fresh independent reviewer to measure that Repair1 made ACM-A1 an
  executed guard without reopening the settled R1/R2 mechanisms.
- **R4R returned `ready` (`696ef88`):** its four measurements pass; the
  decision-blocking ACM-A1 guard is now executed, and the repair remained
  strictly test-only.
- **R5 chartered:**
  `docs/reviews/charter-2026-07-15-core-tax-conditions-r5-honest-reclose.md`
  scopes the honest closure records and preserves the owner's sole authority
  to select `main` reconciliation.
- **R2 charter (completed):**
  `docs/reviews/charter-2026-07-15-core-tax-conditions-r2-member-byte-verification.md`
  bounds the required registry-verified member-byte check and its mutation
  golden. It expressly reserves full verification for R3 and stops on any new
  identity, membership, or registry contract question. The active remediation
  seat is `docs/reviews/SEAT.md`; any clerk or owner-launched builder starts
  there before the charter.
- **➡️ NEXT ACTION: owner performs the no-ff merge of `milestone/core-tax-conditions` into `main`.** R5 is complete (closure records staged; retrospective written; ADRs ratified; `main` reconciled). Foreman does not merge `main` autonomously. After the merge, the next phase is owner-directed.

- **Git/env hygiene:**
  - Run all tests via `.venv/bin/python3 -m unittest` (project `.venv`).
  - Validate conformance via `.venv/bin/python3 tools/governance_lint.py`; mypy via `-m mypy`.
  - Commit per logical unit; owner authorizes execution and launches seats.
