# Conditional Selectors Prototype — Process Log

## 2026-07-12

- Draft prototype plan created for `conditional-selectors` with one primary (CS-P1) and one dependent (CS-P2) proposition.
- Plan approved by owner. Incumbent builder completes Iteration 1 design proposal and examination under the active branch `prototypes/conditional-selectors/it1`.
- Round 1 reviews completed by Governance and Adversary reviewers.
- Foreman triages findings in `round-1-triage.md`. Shape B rejected in current form due to Article 7, 11, 12, and CS-P2 violations.
- Iteration 1 exhibit preserved at tag `exhibits/conditional-selectors/it1` and local branch deleted.
- Repair 1 branch `prototypes/conditional-selectors/repair1` created from tagged exhibit.
- `charter-repair1.md` issued for Shape B repair (addressing logic/parameter separation, optional defaults, displacement tracking, and edge cases). Handoff prepared.
- Incumbent builder completes the Repair 1 design proposal (revising Shape B) and examination on the branch.
- [Reconstructed; not logged at the time] Round 2 Governance and Adversary reviews completed over Repair 1; foreman triaged in `round-2-triage.md`; `evaluation-analysis.md` written recommending revised Shape B (first-class selector citizen); ADR-0019 drafted as proposed.
- Shadow foreman (owner-directed, 2026-07-12) governance conformance review. Findings: (1) plan Gates 4/8 require a clean-room rival builder, but `charter-it1.md` assigned both shapes to the incumbent — the rival seat was never filled; (2) the Repair 1 pass was not pre-authorized by the plan (Gate 4: "No repair pass pre-authorized") and no owner authorization was logged; (3) SEAT.md was stale and rounds were unlogged; (4) several documents are dated 2026-07-13, ahead of the actual date. Note: Track 3 implementation of the selector shape is already underway in the working tree against proposed (not ratified) ADR-0019.
- Owner directs the same rival remediation as non-publication-explanations, taken one step at a time with no foreman-spawned agents. Step 1: independently re-perform the round-1 review of iteration 1. Evaluation analysis reopened. Round 1R prepared with owner-launched Medium governance and adversary seats; role files at `roles/reviewer-governance.md` and `roles/reviewer-adversary.md` deny all round-1/repair/round-2/evaluation/ADR-0019 material and the uncommitted Track 3 implementation; outputs `reviews/round-1r-governance.md` and `reviews/round-1r-adversary.md` with CS-G#R/CS-A#R numbering. Rival charter deferred until round 1R lands.

## 2026-07-13

- Claude assumes principal foreman seat (owner-appointed), relieving the previous Codex foreman.
- Round 1R governance review found already completed: owner-launched thread wrote `reviews/round-1r-governance.md` on 2026-07-12 (evening), under the role file's exclusions. Headline finding CS-G1R (decision-blocking, both shapes): categorical filing-status guards are not executable under the committed evaluator's comparison contract. Integrated by foreman.
- Owner launch go for the remaining seat: round-1R adversary reviewer dispatched as a foreman-spawned sub-agent at Medium tier, independent context (round-1r-governance.md added to its exclusions), under the role file. Track 3 implementation of the disputed selector shape was parked on `wip/track3-core-conditions` (c8be492) and removed from the milestone branch by owner-directed reset, so reviewers judge the design, not an implementation.
- Round 1R adversary review integrated (CS-A1R–A9R). Gate 5 triage in `round-1r-triage.md`. Both independent seats: Shape A conditionally accept; Shape B reject as specified — inverting the tainted process's outcome. CS-P1 not settled by it1 (categorical guards and canon operation citizens do not execute under committed evaluator contracts). Foreman recommends: ADR-0019 to `rejected` status (retained), clean-room rival charter in the Shape A family, evaluation-analysis rewrite. Owner decisions pending.

