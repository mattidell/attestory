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
  And Interest Slice** — Track 0 begun on owner go (2026-07-12): topic directory
  created at `docs/prototypes/source-completeness/` with the ADR-0013 prototype
  plan drafted, foreman seat taken by this session.
- **What I'm mid-doing:** plan.md drafted and committed as **draft — awaiting
  solo owner approval**. No charter written, no seats beyond foreman filled;
  that is the gate, not an omission.
- **Done this stretch (all committed to `main`):** created
  `docs/prototypes/source-completeness/` — `plan.md` (Gates 0–8 instantiated:
  SC-P1 closure→collect mapping primary at score 7; SC-P2 1099-INT identity and
  SC-P3 source-family definition as dependent secondaries; SC-D1 coverage read
  model split out to milestone Track 4 at score 2; rung 1 paper-first; caps: two
  builders incl. rival, two default reviewers, expressiveness conditional on
  rung ≥ 3, ≤ 1,800 total process-doc lines), `SEAT.md`, `process-log.md`, and
  six role files (foreman specialized from the canonical template; no starved
  legibility seat per ADR-0013 amendment). Governance lint conformant; 232
  tests pass.
- **Next action:** owner reviews `plan.md` (solo, per ADR-0013). On approval:
  foreman writes `charter-it1.md` inside the Gate 2 paper scope, then asks
  owner confirmation to spawn the it1 builder (High tier). Reviewer spawns are
  standing-authorized by plan approval; builder/clerk spawns are not.
- **In-flight / uncommitted:** tree clean after commit; no prototype branches
  yet (first one will be `prototypes/source-completeness/it1`).
- **Pending owner decisions / flags:** (1) **approve/amend plan.md** — key
  judgment calls to sanity-check: SC-D1 routed out of the prototype entirely,
  expressiveness reviewer made conditional, and the 1,800-line process-doc cap;
  (2) Legibility Audit allowed-slice and cadence tuning (carried from last
  stretch, untouched).
