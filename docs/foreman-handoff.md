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

## Current state (updated 2026-07-21; Track 4 reviewed READY, PR opened)

- **Seat:** principal foreman. Active milestone: **Dividends and Schedule B
  Slice**. All four milestone ADRs ratified: ADR-0035 (D3), ADR-0036 (D1),
  ADR-0037 (`conditional_dependency_set`, merged as Track 0a, PR #30),
  ADR-0038 (D2, ratified 2026-07-19).
- **Merged tracks:** Track 0a (PR #30, `6f303fe`), Track 1 (PR #31,
  `a870a2f`), Track 2 (PR #32, `c39c6c7` — review found blocking F1,
  repaired `854c71a`, delta re-review READY), **Track 3 (PR #36, `e25cc11`)**
  — the QDCG worksheet, both declared-absence citizens, the bidirectional
  admission-locus interlock (kill-tested all three orders), and the
  structural no-reach-around demonstration; two independent re-review
  rounds (F1: two unrelated FRRS-era tests were tampering a rule file
  selected by unfiltered glob order, not a Track 3 content defect, fixed
  `1247b89`; R1: narrowed the same fix from first-sorted-match to an
  explicit named target, fixed `c1cd01f`) both confirmed genuinely
  discharged before merge — full history in
  `docs/reviews/2026-07-20-dsbs-t3-*.md`. Process: ADR-0030 amendment
  (PR #33), ADR-0039 (PR #34), ADR-0040 trusted-advisor seat (PR #35),
  canonical role seed files under `docs/roles/` (PR #37), retirement of the
  old foreman role template in favor of `docs/roles/foreman.md` as the
  single source (PR #38). Track-by-track detail lives in the review records
  under `docs/reviews/` and git history, no longer restated here.
- **➡️ Track 4 (1099-DIV closure confirmation and live-run harness
  extension) — reviewed READY, PR open, awaiting owner merge.** Build
  charter: `docs/reviews/charter-2026-07-20-dsbs-t4-dividend-live-integration.md`
  (`56ae7af` on `track/dsbs-t4-dividend-live-integration`). Scope
  reconciliation found the milestone plan's Track 4 line names three
  things, two already done before this track (1099-DIV closure-mapping
  content, line-9's 3b absorption — both already pinned in
  `package.core-calculations.v6.json`); only the live-run harness
  extension was genuinely open. Builder landed `fcbf70b`: confirming
  goldens for the two already-done items, extended
  `tools/scaffold_live_acts.py` locally (v6 adoption fixture, dividend
  bundles/families/templates — including `scheduleb.bundle.json`/
  `qdcg.bundle.json` beyond the charter's literal text, load-bearing for
  the Schedule B/QDCG declared-absence citizens, flagged as a review
  finding), the new `tests/test_dsbs_t4_dividend_live_integration.py`
  proving Schedule B disposition and QDCG line-16 resolve together in one
  `live_coordinate_run`, a `.gitignore` safety net for
  `tools/scaffold_live_acts.py`/`workspace-seed/`, and a closing note.
  Review charter `54f581d`; author-independent reviewer dispatched 2026-07-20
  (owner authorization from that session, ADR-0034) re-derived every
  charter claim from scratch rather than trusting the builder's report —
  reproduced the "already done" scope-reconciliation claims, reproduced
  the 546-test/mypy/lint/scan-clean battery independently, and
  independently confirmed the `BUNDLE_FILES` discrepancy is genuinely
  load-bearing (not scope creep) by reproducing the kernel
  `FindingModelError` that occurs without it. **Verdict: READY**, commit
  `9898c07` (`docs/reviews/2026-07-20-dsbs-t4-dividend-live-integration-review.md`)
  — one production condition (F1, the bundle-list discrepancy, not
  blocking) and one non-blocking observation (F2), zero blocking findings.
  **PR opened 2026-07-21**: NEXT ACTION owner reviews/merges. After Track 4
  merges: the only remaining live-data action is the owner's quarantined
  real 1099-DIV run and its permitted three-fact attestation (ADR-0031
  Decision 7); Track 5 then closes the milestone records.
  **Process note:** during this track's dispatch, a shared-`.git`-refs race
  between a foreman foreground command and a concurrently-dispatched
  agent's worktree setup twice caused the primary checkout's `main` branch
  pointer to be clobbered onto the track branch's tip (once pushed to
  `origin/main` before being caught and reverted). No commits were lost
  (all reflog-recoverable), and the track branch itself was never at risk
  — only `main`'s pointer. Lesson for future dispatches: avoid running
  foreground git mutations on the primary checkout while a background
  agent's worktree isolation is still being set up; prefer a dedicated
  worktree for foreman-side commits too, not the primary checkout's `main`
  branch, when other dispatches are in flight.
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
