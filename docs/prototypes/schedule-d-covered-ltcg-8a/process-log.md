# Covered Long-Term Gains, Schedule D Line 8a — Process Log

## 2026-08-01

- Owner merged the milestone and prototype plans in PR #136 (`a05d637`),
  activating Track 0.
- Foreman filed the incumbent charter, topic seat file, and branch-local
  re-entry pointer together on
  `prototypes/schedule-d-covered-ltcg-8a/it1`.
- Iteration 1 covers P1 and P2 at Rung 1 paper only, plus the P3 paper spike.
  No Builder has launched, no artifact result exists, and no process
  incident is recorded.
- Incumbent (`it1`) returned: P1/P2 settled at Rung 1; P3 paper spike named
  the `attachment-rule.v2` categorical-requirement gap (later CA-05) and two
  design forks.
- Clean-room rival (`it2`) chartered on a branch cut clean from `main`, no
  incumbent exposure. Returned: all three propositions settled at Rung 1;
  self-corrected a P3 line7a-`P` circularity (commit `bbecd3f`) before
  committee review; a later non-substantive grounding-citation commit
  (`e52710c`) landed on the branch after the review objects were pinned and
  was correctly excluded from both reviews' evidence.
- Two independent committee reviews ran sequentially on the continuing
  branch: contract/adversary (`NOT READY`, four decision-blocking findings
  CA-01 through CA-04, three separate-decision prerequisites CA-05 through
  CA-07) and expressiveness (`READY` for the rival topology, silent on
  CA-04 — recorded as a genuine measurement-scope difference, not
  wordsmithed away).
- Foreman Gate-5 triage (`round-1-triage.md`) recorded reviewer agreement,
  the CA-04 dissent, and a recommended repair scope. Owner disposition
  2026-08-01: rival topology selected, incumbent not carried forward;
  CA-02/P2-S5 adopted as the completeness-boundary successor; CA-04 repair
  authorized, spending the plan's single fixed repair pass.
- Repair 1, assigned to the rival Builder for design continuity, supplied
  P2-S5A (explicit adopted successor sentence) and P3-S8 (exact per-producer
  pin contract). An independent, author-independent confirmation reviewer
  verified both against the artifact text (not the self-reported
  examination) and returned overall verdict `READY`.
- Contract synthesis chartered on a fresh `decisions/schedule-d-covered-ltcg-8a`
  branch (cut clean from `main`), assigned to a fresh Builder context rather
  than the rival Builder, to independently verify the evidence chain stands
  on its own in writing. Returned proposed ADR-0052, an evaluation analysis
  routing every clause to its exhibit, and one advisory `docs/adr/INDEX.md`
  row. No process incident recorded across the full Track 0 loop.
