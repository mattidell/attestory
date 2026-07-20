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

## Standing policy (read before acting; stable across handoffs)

- **Read-set on boot:** `docs/phase-state.md` → this note → the active
  milestone plan → `docs/adr/INDEX.md` (role cores and routing; ADR-0039).
- **PR vs. branch commit (owner rule, 2026-07-19):** a PR is cut for a
  *complete, independently reviewable unit* — milestone plan approvals,
  process changes, **ratified** ADRs with their evidence, completed track
  development. Everything inside a unit (charters, landed builder outputs,
  reviews, evaluations, *proposed* ADR drafts, status flips) is a plain
  commit on the unit's branch. Pointer/inconsequential phase-state edits
  need no PR. Owner merges (ADR-0030).
- **Dispatch (ADR-0034):** every sub-agent dispatch needs explicit owner
  approval, except committee reviewer seats named in an owner-approved
  prototype plan (standing authorization). Builders are always gated.
- **Verification floor:** full battery (`.venv/bin/python3 -m unittest`,
  mypy, governance lint, envelope scan) before claiming done; named golden
  classes enter through `live_coordinate_run`, never a `RunContext`
  shortcut; verify load-bearing citations against source before relying on
  them.
- **Boundary:** values, dispositions, refusal reasons, workspace location
  never enter repo/reviews/chat; only the three-fact attestation form
  crosses; owner-held run tooling stays untracked.

## Current state (updated 2026-07-19; Track 3 chartered — awaiting owner builder release)

- **Seat:** principal foreman. Active milestone: **Dividends and Schedule B
  Slice**. All four milestone ADRs ratified: ADR-0035 (D3), ADR-0036 (D1),
  ADR-0037 (`conditional_dependency_set`, merged as Track 0a, PR #30),
  ADR-0038 (D2, ratified 2026-07-19 after the full Round 1 → Repair 1 →
  Confirmation R1 → Repair 2 → Confirmation R2 arc; disposition:
  `docs/prototypes/qdcg-worksheet/evaluation-analysis.md`).
- **Merged tracks:** Track 0a (PR #30, `6f303fe`), Track 1 (PR #31,
  `a870a2f`), Track 2 (PR #32, `c39c6c7` — review found blocking F1, the
  Part I tie-out targeting line 2b's four-family total instead of
  `b1-subtotal`; repaired `854c71a`, delta re-review READY). Process:
  ADR-0030 amendment (PR #33), ADR-0039 (PR #34), ADR-0040 trusted-advisor
  seat (PR #35). Track-by-track detail lives in the review records under
  `docs/reviews/` and git history, no longer restated here.
- **➡️ Track 3 (line 16 under D2) CHARTERED** — `ebec569` on
  `track/dsbs-t3-qdcg-line16`:
  `docs/reviews/charter-2026-07-19-dsbs-t3-qdcg-line16.md`. Scope is
  exactly ADR-0038's five production conditions; the charter carries the
  standing golden-class discipline (six named classes through
  `live_coordinate_run`, grep-confirmed), the Track 2 block-code-split
  lesson, and the package-versioning pattern (next version, next synthetic
  scope year after v5's 2054, checksum cascade, `entrypoints` listing
  sanctioned where the reachability walker lacks adjacency).
  **NEXT ACTION: owner releases the builder (ADR-0034); dispatch is not
  authorized by the charter itself.** After Track 3: Track 4 (1099-DIV
  closure content and live integration) closes the milestone.
- **Lessons a Track 3 builder needs** (also baked into the charter):
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
