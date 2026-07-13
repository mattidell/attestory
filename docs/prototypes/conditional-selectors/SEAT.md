# Conditional Selectors Prototype — Seat File

## Current step

Shadow-foreman remediation, step 1: **Round 1R** — independent re-performance of the round-1 review of iteration 1 (see process log, 2026-07-12). Evaluation analysis reopened; draft ADR-0019 ratification on hold. Rival builder charter deferred until round 1R lands. No foreman-spawned agents; all seats owner-launched.

## Seats

| Role | Holder | Status |
|---|---|---|
| Foreman | Claude, principal foreman (owner-appointed 2026-07-13, relieving previous Codex foreman) | active; owner-paced, no unapproved spawns |
| Incumbent builder | owner-launched external context | completed; it1 exhibit `exhibits/conditional-selectors/it1`, repair1 branch `prototypes/conditional-selectors/repair1` |
| Rival builder | vacant | deferred; charter follows round 1R |
| Governance reviewer (round 1R) | owner-launched, from `roles/reviewer-governance.md` | ready to launch |
| Adversary reviewer (round 1R) | owner-launched, from `roles/reviewer-adversary.md` | ready to launch |

## Next action

Owner launches the two round-1R reviewer threads from the role files. Each reviews `it1/design.md` + `examination-it1.md` only, under the role files' independence exclusions (no original round-1 reviews/triage, no repair1/round-2 material, no evaluation analysis, no ADR-0019, no uncommitted Track 3 code), and writes `reviews/round-1r-governance.md` / `reviews/round-1r-adversary.md` with CS-G#R / CS-A#R finding numbering. Foreman triage of round 1R follows, then the rival-charter decision.
