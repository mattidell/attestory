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

**Discipline:** a step is not done until `phase-state.md`'s "Next" is advanced too — it is the re-entry pointer the next reader (foreman *or* clerk) anchors on, so updating only this handoff leaves them stale.

## Standing policy — relocated

The foreman's stable posture (boot read-set, PR-vs-branch rule, dispatch
staging discipline, verification floor, data boundary) now lives in
**`docs/roles/foreman.md`** — read it on boot. It was moved there so this
note can go back to being purely *describes-now* continuity (overwritten
freely) without carrying stable doctrine that risks going stale in a
volatile file. The binding ADRs are unchanged (0005, 0013, 0030, 0034;
routing via `docs/adr/INDEX.md`, ADR-0039).

## Current state (updated 2026-07-21; Track 4 merged — milestone content complete)

- **Seat:** principal foreman. Active milestone: **Dividends and Schedule B
  Slice**. All four milestone ADRs ratified: ADR-0035 (D3), ADR-0036 (D1),
  ADR-0037 (`conditional_dependency_set`, merged as Track 0a, PR #30),
  ADR-0038 (D2, ratified 2026-07-19).
- **Merged tracks:** Track 0a (PR #30, `6f303fe`), Track 1 (PR #31,
  `a870a2f`), Track 2 (PR #32, `c39c6c7` — review found blocking F1,
  repaired `854c71a`, delta re-review READY), Track 3 (PR #36, `e25cc11`)
  — the QDCG worksheet, both declared-absence citizens, the bidirectional
  admission-locus interlock (kill-tested all three orders), and the
  structural no-reach-around demonstration; two independent re-review
  rounds (F1, R1) both confirmed genuinely discharged before merge — full
  history in `docs/reviews/2026-07-20-dsbs-t3-*.md`. **Track 4 (PR #39,
  `e15bd39`)** — closed the milestone plan's remaining Track 4 gap (the
  live-run harness extension for 1099-DIV; two of its three named items
  turned out to already be done by Tracks 1–3) with confirming goldens, an
  extended `tools/scaffold_live_acts.py`, the new
  `tests/test_dsbs_t4_dividend_live_integration.py` (Schedule B + QDCG
  resolving together in one `live_coordinate_run`), and a `.gitignore`
  safety net for the owner-held paths — reviewed READY (`9898c07`, zero
  blocking findings, full history in
  `docs/reviews/2026-07-20-dsbs-t4-*.md`) before merge. Process: ADR-0030
  amendment (PR #33), ADR-0039 (PR #34), ADR-0040 trusted-advisor seat
  (PR #35), canonical role seed files under `docs/roles/` (PR #37),
  retirement of the old foreman role template in favor of
  `docs/roles/foreman.md` as the single source (PR #38). Track-by-track
  detail lives in the review records under `docs/reviews/` and git
  history, no longer restated here.
- **➡️ All milestone content is merged. Next is the owner's real 1099-DIV
  run and attestation (owner-only, out-of-repo), then Track 5** (records:
  matrix, phase-state, retrospective, deferral ledger — itself reviewed
  and merged as a records track, per the milestone plan). No builder or
  reviewer dispatch is needed until one of those two things happens; this
  is not a foreman-actionable step right now.
- **Process note (still relevant for future dispatches):** during Track
  4's dispatch, a shared-`.git`-refs race between a foreman foreground
  command and a concurrently-dispatched agent's worktree setup twice
  clobbered the primary checkout's `main` branch pointer onto the track
  branch's tip (once briefly reached `origin/main` before being caught and
  corrected; no commits were lost, all reflog-recoverable). Lesson: avoid
  foreground git mutations on the primary checkout's `main` while a
  background agent's worktree isolation is still being set up; prefer a
  dedicated worktree for foreman-side commits too when other dispatches
  are in flight.
- **Lessons a Track 3 builder needed** (record kept for the Track 4
  builder — same package/resolver machinery applies):
  bundle-adoption, not bare `fact-type.v2` members (kernel registry
  rejects assertions referencing bare members — Track 2 hit this);
  `conditional_dependency_set` is v3-only by schema; the guard node goes
  first and unconditionally in the outer `all` (confirmed Repair 2 shape);
  a composing rule's `requires` gate reports `DEPENDENCY_ABSENT` while the
  blocked rule carries its own code — check committed goldens before
  asserting block codes.
- **Env note:** if mypy/unittest fail on `str | None` syntax parse errors,
  the `.venv` symlink degraded to system python3.9 — rebuild:
  `rm -f .venv/bin/python3 .venv/bin/python && /opt/homebrew/bin/python3.13
  -m venv --clear .venv && .venv/bin/python3 -m pip install -r
  requirements.txt`.
- **Boundary discipline (standing):** values, dispositions, refusal reasons,
  and the workspace location never enter the repository, a review, or a chat
  session; only the three-fact attestation crossed. Owner-held run tooling
  (`tools/scaffold_live_acts.py`, `workspace-seed/`) stays untracked.

## Historical record

The Core Tax Conditions remediation (closed 2026-07-15) trail formerly kept
here lives in `docs/milestone-retrospectives/2026-07-15-core-tax-conditions-and-presentation-integration.md`,
the `docs/reviews/charter-2026-07-15-*` chain, and git history.

- **Git/env hygiene:**
  - Run all tests via `.venv/bin/python3 -m unittest` (project `.venv`).
  - Validate conformance via `.venv/bin/python3 tools/governance_lint.py`; mypy via `-m mypy`.
  - Commit per logical unit; owner authorizes execution and launches seats.
