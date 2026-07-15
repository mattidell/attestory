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
- **Tracks 1–4 Status:** ✅ Completed & committed: schemas `3c0eed5`; line 2b `1759cf7`; core tax conditions `3e4def1`; manifests/quantity validation `b05ffde`.
- **Track 5 Status:** ✅ Completed & committed (`ea1c167`): structural, adoption-only citation resolution and the ADR-0020 durable v2 run-disposition ledger plus NPE walker. Verification: full unittest suite, focused strict mypy, and governance lint.
- **➡️ NEXT ACTION: execute Track 6 (Integration and Lifecycle Verification)** — add the milestone’s six named synthetic scenarios, CLI goldens, and forward/reference parity. Before treating Track 4 as closed at milestone completion, address its discovered ADR-0027 package-instance/member-byte immutability debt: `package_checksum` values remain placeholders and load-time verification is not implemented. This is a production condition, not silently satisfied by Track 5.

- **Git/env hygiene:**
  - Run all tests via `.venv/bin/python3 -m unittest`.
  - Validate conformance via `.venv/bin/python3 tools/governance_lint.py`.
  - Staged files should be committed per-track.
