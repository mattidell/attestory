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
- **What I'm mid-doing:** iteration 1 is dispatched. `charter-it1.md` is issued
  (rung 1 paper, SC-P1/P2/P3 only) and the it1 builder was spawned as a
  foreman sub-agent (High tier; owner's "approved, begin" recorded as the
  per-spawn confirmation in `process-log.md`). The session limit was expected
  to cut this session mid-iteration — this note is written for that.
- **How to reconcile it1 state on resume:** check whether branch
  `prototypes/source-completeness/it1` exists and whether
  `docs/prototypes/source-completeness/examination-it1.md` exists. Both
  present and committed → it1 landed; verify against the charter's
  pre-declared checks (process conformance only, not quality), update
  `SEAT.md`, log it, and move to the it2 rival. Branch absent or half-done →
  the builder was cut off; re-dispatch a fresh it1 builder on the same
  charter (owner confirmation needed again unless the owner pre-authorizes),
  discarding any partial branch (log the discard).
- **Done this stretch (committed to `main`):** topic scaffolding + draft plan
  (`e4d1bcc`); then plan approval edit, `charter-it1.md`, SEAT/log updates,
  this note (commit at/after this write). Governance lint conformant, 232
  tests pass as of `e4d1bcc`.
- **Next actions in order:** (1) land or re-run it1; (2) it2 clean-room rival
  on the same charter — per-spawn owner confirmation, or owner pastes the
  launch line from `roles/builder-rival.md`; keep it2 starved of it1 outputs;
  (3) committee round 1 (governance + adversary only — standing-authorized
  foreman spawns, no per-spawn ask), attack parity across both designs;
  (4) foreman triage (Gate 5), then evaluation analysis and ADR drafting if
  paper converged — the plan's Gate 2 expectation is SC-P2/P3 settle at
  paper, SC-P1 maybe needs rung 2/3; any climb is one rung, logged, and only
  for the affirmative-only-enforcement question.
- **Budget state (Gate 4):** builders used after it1: 1 of 2. Repair passes
  used: 0 of 1. Reviewer rounds: 0. Process-doc lines so far: plan+charter+
  seat+log+roles ≈ 560 of the ≤ 1,800 target.
- **Pending owner decisions / flags:** (1) confirmation to spawn the it2
  rival when it1 lands (or owner-launch it via the role-file launch line);
  (2) Legibility Audit allowed-slice and cadence tuning (carried, untouched).
