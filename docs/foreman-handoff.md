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
- **What I'm mid-doing:** `charter-it1.md` is issued (rung 1 paper,
  SC-P1/P2/P3 only) and stands **unworked**. The first it1 builder dispatch
  was **halted on owner direction** before producing anything (grounding
  reads only); its empty branch ref was deleted and the halt is logged. The
  owner did not state a reason before the session boundary — do not assume
  the charter or plan is at fault; ask.
- **it1 state on resume:** no `prototypes/source-completeness/it1` branch and
  no `examination-it1.md` should exist. If they do, they postdate this note —
  trust git and the process log over this paragraph. Gate 4 budget: builder
  iterations used 0 of 2 (the halted dispatch produced no iteration).
- **Done this stretch (committed to `main`):** topic scaffolding + draft plan
  (`e4d1bcc`); then plan approval edit, `charter-it1.md`, SEAT/log updates,
  this note (commit at/after this write). Governance lint conformant, 232
  tests pass as of `e4d1bcc`.
- **Next actions in order:** (1) on owner go (fresh per-spawn confirmation),
  re-dispatch the it1 builder on the standing charter; (2) it2 clean-room rival
  on the same charter — per-spawn owner confirmation, or owner pastes the
  launch line from `roles/builder-rival.md`; keep it2 starved of it1 outputs;
  (3) committee round 1 (governance + adversary only — standing-authorized
  foreman spawns, no per-spawn ask), attack parity across both designs;
  (4) foreman triage (Gate 5), then evaluation analysis and ADR drafting if
  paper converged — the plan's Gate 2 expectation is SC-P2/P3 settle at
  paper, SC-P1 maybe needs rung 2/3; any climb is one rung, logged, and only
  for the affirmative-only-enforcement question.
- **Budget state (Gate 4):** builder iterations used: 0 of 2. Repair passes
  used: 0 of 1. Reviewer rounds: 0. Process-doc lines so far: plan+charter+
  seat+log+roles ≈ 570 of the ≤ 1,800 target.
- **Pending owner decisions / flags:** (1) **why the it1 builder was halted**
  and whether/when to re-dispatch (fresh per-spawn confirmation needed);
  (2) confirmation path for the it2 rival when its turn comes (foreman spawn
  or owner-launched via the role-file launch line); (3) Legibility Audit
  allowed-slice and cadence tuning (carried, untouched).
