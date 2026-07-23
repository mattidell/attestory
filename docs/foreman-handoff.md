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

## Current state (updated 2026-07-23; live-run trust-domain planning prepared)

- **Owner-directed process prerequisite:** Foreman Context Loading now has a
  separate planning draft at
  `docs/phases/real-return/milestones/foreman-context-loading.md`. It is an
  advisory context-routing/process-maintenance milestone that must not be
  mistaken for a live-run charter or standing seat authority. Live-Run Trust
  Domains remains planning-only; its first charter and every dispatch still
  require immediate, explicit owner approval.

- **Planning only:** the owner appointed Codex as foreman and selected the
  Live-Run Trust-Domain Definition topic. The draft milestone plan is
  `docs/phases/real-return/milestones/live-run-trust-domain-definition.md` and
  its prototype plan/seat record are under
  `docs/prototypes/live-run-trust-domains/`. No prototype charter or dispatch
  is authorized yet; ADR-0034 requires immediate owner approval for each.
  Scope is synthetic-only domain/crossing evidence. No real run or owner
  attestation is required; schema-publication and agent-scope controls are
  tabled.
- **Closed rescope:** Track 1 merged as PR #45: the synthetic audit proves
  hook refusal when Git runs it and reports `--no-verify` bypass reachability
  plus credential confinement `unestablished`. It does not protect an owner
  push. Track 2 records passed independent review with no blocking finding and
  merged as PR #46 (`9cc6e89`); the milestone close and final retrospective
  merged as PR #47 (`5cad595`). Deferrals 1/2 remain, as does the L3
  data-boundary posture.
- **Stopped predecessor:** Guarded Transport H1 stopped after its one
  permitted repair. Both independent delta reviewers could not reproduce a
  completing clean actual-Git probe; H1-P1/P2 remain unratified. H2/H3 are
  conditional forms only, not separate decisions. Exact records:
  `round-1-triage.md`, `repair1-triage.md`, and the four review records under
  `docs/prototypes/guarded-transport/reviews/`. Do not use the similarly named
  in-progress feature-plan branch as evidence or state.

## Prior milestone handoff (historical detail)

- **Seat:** principal foreman. Milestone **Dividends and Schedule B Slice**
  content-complete; only the Track 5 records remain to close it. All four
  milestone ADRs ratified: ADR-0035 (D3), ADR-0036 (D1), ADR-0037
  (`conditional_dependency_set`, merged as Track 0a, PR #30), ADR-0038 (D2,
  ratified 2026-07-19).
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
- **Real run done (2026-07-21):** the owner attested in the exact
  three-fact form; recorded in the milestone plan's Verification section
  ("Owner attestation") and merged to `main` as PR #40 (`4f0645c` /
  `c971e30`). The owner's first workspace attempt predated Track 4's
  harness extension and refused `RELEASE_ABSENT_OR_MISMATCH` (a stale
  package-adoption pin against a publication surface regenerated several
  times since); diagnosed structurally from the repo's own fixtures (no
  live detail crossed) and resolved by rebuilding the workspace fresh from
  the updated `tools/scaffold_live_acts.py` / `workspace-seed/build.py` —
  see those files' current state for the v6 pin and the full
  dividend/Schedule-B/QDCG template set. Repo-side checks at recording
  time: `git status` clean, `envelope_scan.py --verify` reported the
  envelope gates installed and byte-intact.
- **Track 5 built (2026-07-21) on `track/dsbs-t5-completion`:** charter and
  companion review charter (`ede3849`); all six deliverables now committed
  — maturity matrix (Dividends/Schedule-attachments columns L0→L3 across
  all eight aspects, footnotes 9–12 added), roadmap status, milestone plan
  per-exit-criterion closure, new
  `dividends-schedule-b-slice-deferral-ledger.md` (14 entries: 3 new, 1
  prior-ledger entry re-affirmed touched-not-retired, 10 carried
  untouched; nothing silently closed), retrospective
  (`docs/milestone-retrospectives/2026-07-21-dividends-and-schedule-b-slice.md`),
  and this phase-state/handoff rewrite. Records only — no code, schema,
  content, or test changes on the branch. The owner authorized dispatch
  for this track in-session ("proceed with each charter, I authorize you
  to dispatch agents as needed"); the foreman built the records directly
  rather than dispatching a builder sub-agent, since the charter's own
  framing treats records authorship as foreman-in-session work — the one
  seat this track genuinely needs is the independent *reviewer*, who by
  construction cannot be the records' author.
- **➡️ NEXT ACTION: run the verification floor on the branch (should be a
  no-op for a records-only change, but the floor still applies), then
  dispatch the independent reviewer** per
  `docs/reviews/charter-2026-07-21-dsbs-t5-completion-review.md`
  (ADR-0034 — the owner holds this dispatch), then the owner merges. This
  closes the milestone.
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
