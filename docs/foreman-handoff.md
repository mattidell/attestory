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

## Current state (updated 2026-07-15; branch `milestone/core-tax-conditions`)

- **Seat:** principal foreman.
- **Milestone:** Core Tax Conditions And Presentation Integration (see `docs/phases/foundation/milestones/core-tax-conditions-and-presentation-integration.md`).
- **Track 0 Status:** ✅ Completed (5/5 contract ADRs ratified: 0020, 0024, 0025, 0026, 0027, 0028, 0029 accepted).
- **Track 1 Status:** ✅ Completed & committed (`3c0eed5`): "schema: publish Track 1 contract schemas and payload instances".
- **Track 2 Status:** ✅ Completed & committed (`1759cf7`): "content: implement Track 2 taxable interest composition and Form 1040 line 2b".
- **➡️ NEXT ACTION: execute Track 3 (Core Tax Conditions)** —
  This implements standard deduction selection (Single, MFJ) and tax computation brackets under ADR-0024 + ADR-0025 (rebuilding the parked WIP at `wip/track3-core-conditions` to match).
  - Add standard deduction amount lookups (`p.standard-deduction`, `p.additional-deduction`) and rules.
  - Add tax table lookups (`p.brackets`) and bracket-fold select rule.
  - Implement Form 1040 lines 9, 11, 12, 15, and 16.
  - Verify two-runner parity and Gate-2 cases.

- **Git/env hygiene:**
  - Run all tests via `.venv/bin/python3 -m unittest`.
  - Validate conformance via `.venv/bin/python3 tools/governance_lint.py`.
  - Staged files should be committed per-track.

