# Rule-Language Prototype — Seat File

This is the execution state of the prototype process. A fresh agent resuming this project takes the seat assigned below; it does not self-assign the foreman seat unless that seat is marked vacant (then it records the succession in `process-log.md`).

Context-starved seats (rival builder, legibility reviewer) are NOT filled by generic resumption: the owner pastes the launch line from the role file into a fresh session.

## Current step

Iteration 1 — build. Charter v2 is approved (round 0 complete; dissent withdrawn). One seat is open **now**: builder it1. A fresh agent resuming this project takes that seat per `roles/builder.md`: work only on branch `prototypes/rule-language/it1`; draft F1–F14 per `charter-it1.md`; throwaway evaluator with double-run, shuffled-order, and F13 stage-divergence runs; examination note answering Q1–Q11 (negative results are first-class). The examination note is handed to the foreman for commit; nothing merges to `main` from the prototype branch.

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | claude (session lineage of milestone planning, 2026-07-10) | active |
| Builder it1 | `roles/builder.md` | — | **open now** (charter v2; branch `prototypes/rule-language/it1`) |
| Rival builder | `roles/builder-rival.md` | — | not yet open (starved seat; launch line in role file) |
| Reviewer: governance | `roles/reviewer-governance.md` | codex (resume session, 2026-07-10) | complete (round 0, charter review: `reviews/round-0-governance.md`) |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | — | not yet open (needs artifacts) |
| Reviewer: legibility | `roles/reviewer-legibility.md` | — | not yet open (starved seat; launch line in role file) |
| Reviewer: adversary | `roles/reviewer-adversary.md` | codex (resume session, 2026-07-10) | complete (round 0 delta-confirmation: `reviews/round-0-adversary-delta.md`) |

## Next action

Fill the builder it1 seat (fresh session; generic resumption dispatches here). When the examination note lands: foreman assembles round 1 (all four reviewer seats; legibility is owner-launched via its role file's launch line).

## Evidence exhibits

- `prototypes/rule-language/it0` — pre-process derivation spike, admitted as exhibit by owner disposition 2026-07-10. Mined by the harvest; not a process-conformant iteration.
