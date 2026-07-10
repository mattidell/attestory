# Rule-Language Prototype — Seat File

This is the execution state of the prototype process. A fresh agent resuming this project takes the seat assigned below; it does not self-assign the foreman seat unless that seat is marked vacant (then it records the succession in `process-log.md`).

Context-starved seats (rival builder, legibility reviewer) are NOT filled by generic resumption: the owner pastes the launch line from the role file into a fresh session.

## Current step

Track 1 — evidence harvest and fixture charter. Foreman is producing `harvest-notes.md` and `charter-it1.md`. Next disposition: committee review of the charter.

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | claude (session lineage of milestone planning, 2026-07-10) | active |
| Builder it1 | `roles/builder.md` | — | not yet open (opens after charter disposition) |
| Rival builder | `roles/builder-rival.md` | — | not yet open (starved seat; launch line in role file) |
| Reviewer: governance | `roles/reviewer-governance.md` | — | next: charter review (see below) |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | — | not yet open (needs artifacts) |
| Reviewer: legibility | `roles/reviewer-legibility.md` | — | not yet open (starved seat; launch line in role file) |
| Reviewer: adversary | `roles/reviewer-adversary.md` | — | next: charter review (see below) |

## Next action

When `charter-it1.md` is committed: charter review round. The charter (not code) is the artifact under review — governance reviewer checks it against the governance set and milestone plan; adversary attacks its coverage (attack surface 1 applies to charters directly). Round stub: `reviews/round-0.md`. Owner disposition follows.

## Evidence exhibits

- `prototypes/rule-language/it0` — pre-process derivation spike, admitted as exhibit by owner disposition 2026-07-10. Mined by the harvest; not a process-conformant iteration.
