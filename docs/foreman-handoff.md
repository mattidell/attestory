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

## Current state (updated 2026-07-18; `main` at `2a2440e` — **Track 4c merged, owner's quarantined real run is next**)

- **Seat:** principal foreman. The active milestone is First Real Return Slice.
  Tracks 0–4c are all merged (Track 4c: PR #18, merge `2a2440e`); no reset is
  pending.
- **Owner-held run tooling:** `tools/scaffold_live_acts.py` and
  `workspace-seed/` (synthetic seed + `build.py`) are **intentionally
  untracked** per the Track 4c charter — never commit them or any workspace
  output. `build.py <L> --seed <L>/personal-seed.json` seeds and preflights a
  private workspace; `python3 <L>/runner.py 1` (then 2, 3, …) performs run
  attempts; reports land under `<L>/outputs/`.
- **Boundary discipline for the run:** values, dispositions, refusal reasons,
  and the workspace location never enter the repository, a review, or a chat
  session. The only sentence that crosses back is the three-fact attestation:
  the owner ran the slice; dispositions were observed in quarantine; no
  artifact crossed the boundary. If a run refuses for what looks like a
  mechanism defect, characterize it by reproducing it *synthetically* in-repo
  — never by quoting the live refusal.
- **Real run done (2026-07-18):** the owner attested in the exact three-fact
  form; recorded in the milestone plan's Verification section ("Owner
  attestation"). A pre-flight act-log inconsistency during workspace prep was
  diagnosed via the synthetic seed (mechanism confirmed sound) and fixed
  owner-side; no live detail crossed. Envelope gates verified at recording.
- **➡️ NEXT ACTION: charter Track 5 — the completion records track
  (maturity-matrix + phase-state updates, retrospective, deferral ledger),
  itself reviewed and merged per ADR-0030.**

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
