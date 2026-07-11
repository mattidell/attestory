# Rule-Language Prototype — Seat File

This is the execution state of the prototype process. A fresh agent resuming this project takes the seat assigned below; it does not self-assign the foreman seat unless that seat is marked vacant (then it records the succession in `process-log.md`).

Context-starved seats (rival builder, legibility reviewer) are NOT filled by generic resumption: the owner pastes the launch line from the role file into a fresh session.

## Current step

Round 2 — review of the it2 rival build and the comparison against it1. The rival build is complete (branch `prototypes/rule-language/it2`, tip `623957c`); the examination is on `main` (`examination-it2.md`). **Round 2 is complete.** All four reviews landed and conformance-checked; legibility scored (`reviews/round-2-legibility-scoring.md`); round-close outcome summaries in the process log. The process now waits on the **owner disposition**: conclude to the evaluation analysis and ADRs, or an it3 convergence build (iteration cap allows one more before mandatory owner check-in). No seats are open; do not self-assign review work.

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | claude (resume session, 2026-07-10) | active (succession logged in `process-log.md`) |
| Builder it1 | `roles/builder.md` | codex (resume session, 2026-07-10) | complete (branch `prototypes/rule-language/it1` @ `362f8a3`; `examination-it1.md`) |
| Rival builder | `roles/builder-rival.md` | owner-launched clean room (2026-07-10) | complete (branch `prototypes/rule-language/it2` @ `623957c`; `examination-it2.md`) |
| Reviewer: governance | `roles/reviewer-governance.md` | claude (resume session, 2026-07-10) | complete (round 2: `reviews/round-2-governance.md`) |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | codex (resume session, 2026-07-10) | complete (round 2: `reviews/round-2-expressiveness.md`; process disclosure recorded in review) |
| Reviewer: legibility | `roles/reviewer-legibility.md` | owner-launched fresh session (2026-07-10) | complete (round 2: `reviews/round-2-legibility.md`; foreman scoring `round-2-legibility-scoring.md`) |
| Reviewer: adversary | `roles/reviewer-adversary.md` | claude (resume session, 2026-07-10) | complete (round 2: `reviews/round-2-adversary.md`) |

## Next action

Owner disposition on round 2: conclude (evaluation analysis + ADR proposals) vs it3 convergence build. Owner sampling audit has not yet occurred in any round — invited at this disposition. On conclude: tag `exhibits/rule-language/it2`, remove the branch ref per the exhibit-tag refinement, open the evaluation-analysis work.

## Evidence exhibits

- Tag `exhibits/rule-language/it0` — pre-process derivation spike, admitted as exhibit by owner disposition 2026-07-10. Mined by the harvest; not a process-conformant iteration.
- Tag `exhibits/rule-language/it1` — iteration 1 (primary design, expression trees) @ `362f8a3`; concluded by owner disposition 2026-07-10 after round 1. Examination on `main`; reviews under `reviews/round-1*`.
- Branch `prototypes/rule-language/it2` — active rival iteration under review (clean-room build; guarded single-publication clauses, schema-enumerated operations, closed packages, start/completion records); becomes tag `exhibits/rule-language/it2` when the iteration concludes.
