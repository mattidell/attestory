# Rule-Language Prototype — Seat File

This is the execution state of the prototype process. A fresh agent resuming this project takes the seat assigned below; it does not self-assign the foreman seat unless that seat is marked vacant (then it records the succession in `process-log.md`).

Context-starved seats (rival builder, legibility reviewer) are NOT filled by generic resumption: the owner pastes the launch line from the role file into a fresh session.

## Current step

**Process closed.** ADRs 0006/0007/0008 ratified by owner disposition 2026-07-10 (0007 amended pre-ratification to resolve the governance sign-off dispute — see process log). The evaluation analysis is the milestone's evidence document; all three iterations are exhibit tags. No seats are open and none will reopen; a fresh agent resuming this project should not take a seat here — see `docs/phase-state.md` for the active milestone. Remaining foreman item: milestone retrospective (`docs/milestone-retrospectives/`).

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | claude (resume session, 2026-07-10) | active (succession logged in `process-log.md`) |
| Builder it1 | `roles/builder.md` | codex (resume session, 2026-07-10) | complete (branch `prototypes/rule-language/it1` @ `362f8a3`; `examination-it1.md`) |
| Rival builder | `roles/builder-rival.md` | owner-launched clean room (2026-07-10) | complete (branch `prototypes/rule-language/it2` @ `623957c`; `examination-it2.md`) |
| Reviewer: governance | `roles/reviewer-governance.md` | claude (resume session, 2026-07-10); delta-confirmation: codex (resume session, 2026-07-11) | complete; delta-confirmation complete 2026-07-11 with bounded dispute (round 2: `reviews/round-2-governance.md`) |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | codex (resume session, 2026-07-10) | complete; sign-off complete 2026-07-11 (round 2: `reviews/round-2-expressiveness.md`; process disclosure recorded in review) |
| Reviewer: legibility | `roles/reviewer-legibility.md` | owner-launched fresh session (2026-07-10) | complete (round 2: `reviews/round-2-legibility.md`; foreman scoring `round-2-legibility-scoring.md`) |
| Reviewer: adversary | `roles/reviewer-adversary.md` | claude (resume session, 2026-07-10); delta-confirmation: codex (resume session, 2026-07-11) | complete; sign-off complete 2026-07-11 (round 2: `reviews/round-2-adversary.md`) |

## Next action

None in this process. Milestone retrospective, phase-state, and milestone-status updates are foreman work outside this seat file; Derivation Machinery re-planning follows ratification as its own milestone.

## Evidence exhibits

- Tag `exhibits/rule-language/it0` — pre-process derivation spike, admitted as exhibit by owner disposition 2026-07-10. Mined by the harvest; not a process-conformant iteration.
- Tag `exhibits/rule-language/it1` — iteration 1 (primary design, expression trees) @ `362f8a3`; concluded by owner disposition 2026-07-10 after round 1. Examination on `main`; reviews under `reviews/round-1*`.
- Tag `exhibits/rule-language/it2` — iteration 2 (clean-room rival; guarded single-publication clauses, schema-enumerated operations, closed packages, start/completion records) @ `623957c`; concluded by owner disposition 2026-07-10 after round 2. Examination on `main`; reviews under `reviews/round-2*`.
