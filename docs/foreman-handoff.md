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
- **CS topic:** round 1R (independent re-performance of the it1 review) is
  prepared for **owner-launched** seats from `roles/reviewer-governance.md` /
  `roles/reviewer-adversary.md`; outputs `reviews/round-1r-*.md`, CS-G#R/CS-A#R
  numbering. Evaluation reopened; ADR-0019 on hold; rival charter deferred
  until round 1R lands.
- **Git:** Track 3 implementation parked on `wip/track3-core-conditions`
  (`c8be492`), not for merge. Milestone branch working tree holds only
  uncommitted remediation docs (both topics' SEAT/log/evaluation edits, NPE
  it2 + round-2 files, CS round-1R role files) — owner holds commit go.
  History still contains Track 1 conditional-structure schemas (`df847f1`) and
  Track 2 (`660102d`) built on proposed ADRs; owner deciding reset scope
  (candidate reset point if chosen: `c415b10`, then re-land retained
  prototype/remediation docs and amended ADRs).
- **Standing owner directives:** every prototype round gets rival
  (independent) reviews and a rival builder; agents must treat non-accepted
  ADRs as non-binding (mark rejected ADRs rather than delete — formalization
  of this instruction pending, likely an ADR-0013 amendment or AGENTS.md line).
- **Pending owner decisions:** see phase-state correction block and the
  decision brief given 2026-07-13 — commit go for remediation docs; CS
  round-1R launch; ADR-0020 redraft go; ADR-0019 disposition; history reset
  scope for Tracks 1/2; rejected-ADR instruction formalization.
