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

## Current state (updated 2026-07-13, end of remediation session; branch `milestone/core-tax-conditions` at `d13d1fb`)

- **Seat:** Claude is principal foreman (owner-appointed 2026-07-13, relieving
  the previous Codex foreman after the governance remediation — full history in
  the two topics' process logs). Standing owner directives, formalized in the
  ADR-0013 amendment and AGENTS.md (2026-07-13): rival evidence every round;
  non-accepted ADRs are inert; rejected ADRs retained, never deleted; **no
  foreman-spawned agents without a fresh owner go** (owner has been launching
  seats from foreman-issued prompts; integrate their outputs from the working
  tree, commit with foreman custody, and always split unrelated deliveries
  into separate commits).
- **Milestone:** Core Tax Conditions And Presentation Integration — remediation
  essentially complete; implementation not restarted. ADR status: 0019
  rejected (retained); 0023 **accepted** (ratified at patch merge `bf23517`);
  0018/0020/0021/0022/0024 proposed; 0024 awaiting owner ratification call.
- **Source Completeness reconciliation: CLOSED.** Review → patch → pre-merge
  review → corrections → owner non-ff merge `bf23517` → ADR-0023 ratified and
  roadmap updated on `main` (`7a90f89`). 316 tests/lint/mypy green post-merge.
  Optional follow-up SC-PR3 (thicken the committed SC-R1 probe end-to-end)
  can ride any future kernel track.
- **CS topic: closed for decision.** it2 accepted with CS-A10R/A11R errata;
  `evaluation-analysis.md` rewritten (complete); **ADR-0024** (Conditional
  Structures in the Rule Language) drafted as proposed — owner ratification
  pending. Track 3 rebuild is gated on ADR-0024 + the ELX topic outcome.
  Track 3's old implementation stays parked at `wip/track3-core-conditions`
  (`c8be492`), reference only.
- **ELX topic (expression-language-extensions): OPEN, in flight.** Owner-
  approved plan + `charter-it1.md` committed (`d13d1fb`); the **owner has the
  incumbent-builder launch prompt** — expect `it1/design.md` +
  `examination-it1.md` to appear in the working tree. On arrival: foreman
  conformance check (two files only, exam ≤120, five Gate 2 cases, Rung 2
  boundary), commit as its own exhibit, then charter the clean-room rival
  (it2), then committee round. Candidate ADR number 0025.
- **NPE topic: round 3 in flight.** ADR-0020 redraft (durable Run Disposition
  Ledger) is under review — **owner has both round-3 prompts**
  (`roles/reviewer-governance-r3.md`, `roles/reviewer-adversary-r3.md`);
  expect `reviews/round-3-governance.md` (NPE-G9+) and
  `reviews/round-3-adversary.md` (NPE-A12+) in the working tree. On arrival:
  foreman triage (`round-3-triage.md`), rewrite the reopened
  `evaluation-analysis.md`, then owner ratification call on ADR-0020.
- **Git hygiene notes:** use the project `.venv` (system python lacks
  jsonschema); owner-launched threads drop uncommitted files into this
  working tree — check `git status` before any `git add -A` and split
  deliveries from your own doc changes. Milestone roadmap/handoff will
  conflict with `main`'s at merge; resolve toward the milestone versions.
- **Pending owner decisions:** (1) ratify ADR-0024; (2) ratify ADR-0020 after
  round 3; (3) eventual milestone-plan revision + Tracks 1–3 re-run after
  ratifications (Track 1 conditional-structure schemas rebuild under 0024,
  not the rejected 0019); (4) milestone-level process retrospective on the
  delegation experiment (rich material in the process logs), timing owner's.
- **Side thread (not foreman scope):** product naming — front-runner
  "Attestory"; `attestory.com` is a 2026-01-30 GoDaddy registration with a
  "Launching Soon" page and no other footprint; owner's USPTO check decides.
