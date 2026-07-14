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

## Current state (updated 2026-07-13, governance remediation)

- **Seat:** Claude is principal foreman (owner-appointed 2026-07-13), relieving
  the previous Codex foreman. The 2026-07-12/13 shadow-foreman review found the
  previous foreman's Track 0 runs skipped the clean-room rival seats both
  approved plans required, left SEATs/logs stale, and drafted ADRs 0019/0020
  from single-context evidence; the owner directed remediation, owner-paced,
  **no foreman-spawned agents without a fresh owner go**.
- **Milestone:** Core Tax Conditions And Presentation Integration, **paused for
  remediation**. ADRs 0018–0022 are all *proposed*, none ratified
  (phase-state corrected).
- **NPE topic:** remediation complete through round 2. Clean-room rival it2
  built; round-2 governance/adversary reviews and `round-2-triage.md` done.
  Converged shape: durable Run Disposition Ledger in the ADR-0008 closing
  record + it1's multi-rule nodes + cycle detection, under five
  decision-blocking repairs (NPE-A4, G6, A5, A6, A7). ADR-0020 as drafted
  (transient Execution Map) does not match; redraft pending owner go.
- **CS topic:** round 1R complete and triaged (`round-1r-triage.md`,
  2026-07-13). Both independent seats: Shape A conditionally accept, Shape B
  reject as specified — inverting the tainted outcome draft ADR-0019 rests on.
  CS-P1 not settled by it1 (categorical guards / canon operation citizens do
  not execute under committed evaluator contracts).
- **Git:** owner-directed reset done 2026-07-13 — milestone branch rebuilt
  from `c415b10` as `fc9a855` (all Track 0 docs + remediation retained; Track
  1/2 implementation dropped). Pre-reset history at
  `archive/core-tax-conditions-pre-reset`; Track 3 WIP at
  `wip/track3-core-conditions` (`c8be492`). Verified at `fc9a855`: 314 tests
  OK (use the project `.venv`, not system python), governance lint conformant.
- **Standing owner directives (formalized):** ADR-0013 amendment + AGENTS.md
  lines (2026-07-13) — rival evidence every round; non-accepted ADRs are
  inert; rejected ADRs retained, never deleted.
- **Commissioned review:** owner commissioned a post-merge reconciliation
  review of Source Completeness And Interest Slice (`382a7af`) — charter at
  `docs/reviews/charter-2026-07-13-source-completeness-reconciliation.md`,
  owner-launched seat, output
  `docs/reviews/2026-07-13-source-completeness-reconciliation.md`. A patch
  branch off `main` follows only if the review's verdict warrants one.
- **Pending:** (1) owner launches the CS it2 clean-room rival builder
  (`charter-it2.md`, `roles/builder-rival.md`; ADR-0019 flipped to rejected
  2026-07-13); (2) after it2: foreman conformance check, committee review
  round, triage, CS evaluation-analysis rewrite; (3) NPE ADR-0020
  post-redraft review round (redraft landed in `fc9a855`); (4) eventual
  re-run of Tracks 1–3 after ratifications.
