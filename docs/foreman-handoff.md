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

## Current state (updated 2026-07-15; branch `milestone/core-tax-conditions` @ `85ce351` — **milestone REOPENED**)

- **Seat:** principal foreman.
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
- **R2 chartered:**
  `docs/reviews/charter-2026-07-15-core-tax-conditions-r2-member-byte-verification.md`
  bounds the required registry-verified member-byte check and its mutation
  golden. It expressly reserves full verification for R3 and stops on any new
  identity, membership, or registry contract question. The active remediation
  seat is `docs/reviews/SEAT.md`; any clerk or owner-launched builder starts
  there before the charter.
- **➡️ NEXT ACTION: R2 — extend published-byte verification to every resolved
  member citizen** (ADR-0027 ACM-A5), owner-paced. The owner launches the R2
  execution seat; the foreman retains branch and commit custody. Then R3→R5.
  Do not re-do the sound development code (review "keep" list).

- **Git/env hygiene:**
  - Run all tests via `.venv/bin/python3 -m unittest` (project `.venv`).
  - Validate conformance via `.venv/bin/python3 tools/governance_lint.py`; mypy via `-m mypy`.
  - Commit per logical unit; owner authorizes execution and launches seats.
