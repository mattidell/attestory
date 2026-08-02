# Source-Family Semantics Prototype — Process Log

## 2026-07-12

- Topic split from Source Completeness SC-P3 after partial ratification of
  ADR-0014/0015. The prior committee found both source-family definitions
  misaligned with their natural-language closure claims and coverage universe.
- Draft plan created with one primary and one dependent proposition, paper-only
  starting evidence, two clean-room rivals, Medium-tier owner-launched reviews,
  and a ≤900-line target. Owner approval pending; no charter or builder work.
- Owner approved the plan. `charter-it1.md` issued for an incumbent paper design
  covering all six declared universe-alignment cases; High/high builder tier;
  no code or evidence climb. External builder handoff prepared.
- It1 conformance: commit `5ef3435` changes only design/examination; examination
  53/120 lines; all six cases, lifecycle, universe map, positives/negatives, and
  per-proposition dispositions present; paper boundary held. Integrated and
  preserved as `exhibits/source-family-semantics/it1`; branch/worktree deleted.
- `charter-it2.md` issued for a clean-room paper rival on the same cases.
  Incumbent artifacts/process log explicitly denied; High/high external builder
  handoff prepared.
- It2 conformance: commit `f48a102` changes only design/examination; examination
  67/120 lines; all six cases and per-proposition dispositions present; paper
  boundary and clean-room exclusions held. Integrated and preserved as
  `exhibits/source-family-semantics/it2`; branch/worktree deleted.
- Committee round 1 prepared with owner-launched Medium/medium governance and
  adversary seats, equal cases across both rivals, no code or taxonomy expansion.
- Owner removed review-document line caps after observing wasted reviewer effort
  spent trimming valid evidence. Active roles/round updated: review cost is
  bounded by declared measurements, and reviewers stop when those are complete.
- Round 1 reviews integrated. Governance passes both paper alignments; adversary
  finds shared consistent-mislabel and late-discovery-trigger failures. Gate 5
  triage recorded in `round-1-triage.md`.
- Plan amended with SFS-P3, a tightly dependent late-member freshness/currency
  proposition forced by the declared lifecycle. `charter-repair1.md` authorized:
  SFS-P1/P2 paper repair plus an SFS-P3 static state table; no code/depth climb.
- Repair1 conformance: commit `b38f131` changes only design/examination;
  examination 59/120 lines. SFS-P1/P2 settle at paper; SFS-P3 state table shows
  ADR-0010 cannot reach a later previously unknown member and declines to invent
  machinery. Integrated/preserved as `exhibits/source-family-semantics/repair1`.
- Foreman boundary call: a family frontier/horizon capable of changing derived
  currency may touch the governance-reserved derived-finding authority boundary.
  No code climb authorized. Round 2 will measure the escalation before a
  separate Tier-3 decision plan is considered.
- Round 2 reviews integrated: governance 180 lines, adversary 211 lines, both
  complete declared measurements without line trimming. Governance wrote to a
  repository-root `reviews/` path; foreman mechanically relocated it during
  integration without content changes. Logged as reviewer path defect.
- Final triage: SFS-P1/P2 converged; SFS-P3 is a separate Tier-3 boundary under
  reserved T1/Article 7 constraints. `evaluation-analysis.md` and proposed
  ADR-0016 drafted. No further build in this topic; owner ratification pending.
- Owner ratified ADR-0016 on 2026-07-12. Source-Family Semantics topic complete;
  SFS-P3 remains explicitly unresolved and moves to a separate Tier-3 process.
