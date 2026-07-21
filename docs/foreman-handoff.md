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

## Current state (updated 2026-07-20; Track 4 charter drafted, dispatch authorized)

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
  extension) — chartered, not yet dispatched.** Charter:
  `docs/reviews/charter-2026-07-20-dsbs-t4-dividend-live-integration.md`.
  Scope reconciliation (research pass, 2026-07-20) found the milestone
  plan's Track 4 line names three things, two of which are **already done**:
  the 1099-DIV closure-mapping content (`closure-mapping.f1099div-1a/1b
  .json`, landed `2a08d80`, structurally identical to the interest
  mappings) and line-9's absorption of 3b (`rule.form1040-line9.v2.json`,
  already pinned in `package.core-calculations.v6.json` alongside the
  Track 3 QDCG line-16 successor and the dividend closure mappings). Only
  the **live-run harness extension** is genuinely open: the owner-held,
  intentionally-untracked `tools/scaffold_live_acts.py` still pins a v3
  adoption fixture, has no 1099-DIV bundle/family/template entries, and
  there is no dividend analog of `tests/test_frrs_t4_w2_live_integration
  .py` (every prior source family — W-2, interest — has this live-
  integration precedent; dividends do not yet). Charter scopes exactly
  that gap: confirming goldens for the two already-done items (not
  rebuilds), the harness extension, the missing test, and a two-line
  `.gitignore` safety net for the owner-held paths. **Owner authorized
  builder + reviewer dispatch for this session, 2026-07-20** (ADR-0034);
  builder dispatch is the next action.
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
