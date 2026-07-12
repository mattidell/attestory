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
- **Follow-on decision:** Source Completeness Track 0 is closed with ADR-0014/
  0015 ratified. SC-P3 is split into `docs/prototypes/source-family-semantics/`;
  source-family evaluation is complete and ADR-0016 ratified. SFS-P3 is routed
  to a separate Tier-3 late-member freshness decision.
- **Current plan gate:** closure-freshness plan approved; incumbent
  `charter-it1.md` ready at `/tmp/finances-closure-freshness-it1`.
- **What I'm mid-doing:** Foreman succession, git reconciliation, iteration 1
  integration, and exhibit preservation are complete for both rivals. Committee
  round 1 reviews are integrated; owner ratified `round-1-triage.md` and
  authorized SC-P1 progression. Repair1–3 and round 3 are complete; shape A is
  selected. Repair4 and round 4 are complete. Owner ratified ADR-0014/0015;
  Track 0 is complete under partial ratification. SC-P3 remains unresolved.
- **Delegated authority:** foreman decides iteration continuation and rung
  progression within the approved plan/caps. Solicit owner input only when the
  process is genuinely blocked or an intentionally unspawned builder in another
  thread needs to resume.
- **Iteration preference:** when a central uncertainty remains and another
  round can state a bounded question, cost, artifacts, and pass/fail result,
  prefer iterating over deferring the problem. Do not absorb adjacent or
  open-ended work.
- **Review length:** reviews have no line cap. Bound them through explicit
  measurements and stop conditions; do not make reviewers compress valid
  evidence to satisfy arbitrary length targets.
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
- **Next actions in order:** owner resumes closure-freshness incumbent builder;
  foreman integrates/preserves and prepares clean-room rival.
- **Budget state (Gate 4):** builder iterations used: 2 of 2. Repair passes
  used: 0 of 1. Reviewer rounds: 0. Process-doc lines so far: plan+charter+
  seat+log+roles ≈ 570 of the ≤ 1,800 target.
- **Pending owner decisions / flags:** (1) owner launch/resumption of original
  it1 builder; (2) Legibility Audit
  allowed-slice and cadence tuning (carried, untouched).
