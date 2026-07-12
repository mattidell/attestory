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
  integration, and exhibit preservation are complete for both rivals. Committee
  round 1 reviews are integrated and Gate 5 triage is recorded in
  `round-1-triage.md`; owner disposition is next.
- **Exhibit state:** it1's four chartered documents are merged to `main`; immutable tag
  `exhibits/source-completeness/it1` points to `d47d12c`, and the concluded
  branch is deleted. It2 is likewise preserved at
  `exhibits/source-completeness/it2` (`82ffb7f0`). Builder iterations used 2 of
  2. Both examinations recommend that SC-P1's
  affirmative-only enforcement may need a later rung climb, but the foreman
  has made no artifact-quality disposition.
- **Done this stretch (committed to `main`):** topic scaffolding + draft plan
  (`e4d1bcc`); then plan approval edit, `charter-it1.md`, SEAT/log updates,
  this note (commit at/after this write). Governance lint conformant, 232
  tests pass as of `e4d1bcc`.
- **Next actions in order:** owner decides the triage recommendation: partially
  continue SC-P1/SC-P2, defer SC-P3, and authorize rung 2 for SC-P1 only. If
  authorized, issue a bounded rung-2 charter; do not open rung 3 or a repair
  pass implicitly.
- **Budget state (Gate 4):** builder iterations used: 2 of 2. Repair passes
  used: 0 of 1. Reviewer rounds: 0. Process-doc lines so far: plan+charter+
  seat+log+roles ≈ 570 of the ≤ 1,800 target.
- **Pending owner decisions / flags:** (1) accept/reject the partial disposition
  and SC-P1 rung-2 climb; (2) Legibility Audit
  allowed-slice and cadence tuning (carried, untouched).
