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

## Current state (updated 2026-07-12)

- **Active milestone / phase:** Foundation phase; milestone **Source Completeness
  And Interest Slice**, Track 0 running under the **owner-approved**
  `docs/prototypes/source-completeness/plan.md` (approved 2026-07-12, solo).
- **What I'm mid-doing:** Foreman succession, git reconciliation, iteration 1
  integration, and exhibit preservation are complete. The process is paused
  before rival-builder dispatch under the owner's explicit instruction.
- **it1 state:** four chartered documents are merged to `main`; immutable tag
  `exhibits/source-completeness/it1` points to `d47d12c`, and the concluded
  branch is deleted. Builder iterations used 1 of 2. The examination recommends that SC-P1's
  affirmative-only enforcement may need a later rung climb, but the foreman
  has made no artifact-quality disposition.
- **Done this stretch (committed to `main`):** topic scaffolding + draft plan
  (`e4d1bcc`); then plan approval edit, `charter-it1.md`, SEAT/log updates,
  this note (commit at/after this write). Governance lint conformant, 232
  tests pass as of `e4d1bcc`.
- **Next actions in order:** (1) pause until the owner explicitly instructs a
  builder spawn; then it2 clean-room
  rival on the same charter, kept starved of it1 outputs;
  (3) committee round 1 (governance + adversary only — standing-authorized
  foreman spawns, no per-spawn ask), attack parity across both designs;
  (4) foreman triage (Gate 5), then evaluation analysis and ADR drafting if
  paper converged — the plan's Gate 2 expectation is SC-P2/P3 settle at
  paper, SC-P1 maybe needs rung 2/3; any climb is one rung, logged, and only
  for the affirmative-only-enforcement question.
- **Budget state (Gate 4):** builder iterations used: 1 of 2. Repair passes
  used: 0 of 1. Reviewer rounds: 0. Process-doc lines so far: plan+charter+
  seat+log+roles ≈ 570 of the ≤ 1,800 target.
- **Pending owner decisions / flags:** (1) explicit instruction before any
  it2 rival builder spawn (the owner's latest direction forbids an implicit
  dispatch); (2) confirmation path for the it2 rival (foreman spawn
  or owner-launched via the role-file launch line); (3) Legibility Audit
  allowed-slice and cadence tuning (carried, untouched).
