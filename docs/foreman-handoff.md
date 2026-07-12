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
  And Interest Slice** — planned (`docs/phases/foundation/milestones/source-completeness-and-interest-slice.md`),
  Track 0 is an owner-gated prototype process, **not yet launched**.
- **What I'm mid-doing:** nothing in flight — a run of prototype-process protocol
  amendments just completed and is fully committed.
- **Done this stretch (all committed to `main`):** verified First Tax Slice
  completion (`c548766`); planned Source Completeness (`4f8b9f9`); ratified the
  prototype economic gates + prototype plan + role capability budget (ADR-0013);
  added the optional foreman clerk; made the foreman spawn committee reviewers by
  default; added the periodic owner-spawned Legibility Audit and moved starved
  legibility rigor out of prototype iterations. Latest commit at write time:
  `3a77929` (plus this note).
- **Next action:** on owner go, draft `docs/prototypes/source-completeness/plan.md`
  (the owner-approved prototype plan required before Track 0's first charter),
  instantiating the economic gates including the seat/tier table.
- **In-flight / uncommitted:** tree clean; no open branches beyond `main` and the
  usual historical refs; no open worktrees.
- **Pending owner decisions / flags:** (1) whether to launch Source Completeness
  Track 0; (2) Legibility Audit allowed-slice is "realistically starved" (Ontology
  allowed) vs a harder "schemas+scenario only" bar — owner may tune; (3) audit
  cadence proposed as phase boundaries + new-vocabulary milestones — owner may
  tune.
