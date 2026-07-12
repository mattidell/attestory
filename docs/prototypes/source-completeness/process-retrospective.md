# Source Completeness Prototype Process Retrospective

Date: 2026-07-12

Status: complete; ADR-0014 and ADR-0015 ratified. This is a prototype-process
retrospective, not the milestone retrospective.

## Outcome

The process earned two durable contracts:

- a reusable, independently adopted source-closure mapping with current-true
  authority, a single supported dispatch entry, and exact mapping/finding pins;
- logical Form 1099-INT statement-instance identity, peer to evidence.

It deliberately did not settle SC-P3: the natural-language closure claim and
the member, mapping, and coverage universes. That boundary must be decided
before interest closure-backed zero or coverage can ship.

## Cost and deviations

- Two clean-room paper rivals, four repair exhibits, and four committee rounds.
- 12 reviews: governance/adversary each round; expressiveness for executable
  rounds 2–4.
- Topic Markdown exceeded the ≤1,800 target, reaching well beyond it after
  additional repairs and reviews.
- The original one-repair cap was exceeded. Owner delegated progression and
  later explicitly preferred bounded additional iterations; the plan amendment
  was recorded only after governance identified the missing durable amendment.
- One shared-worktree race occurred before it2 artifact work; repaired with no
  context leak.
- One succeeding foreman recorded succession after its first mechanical read.
- One comparison-base mistake briefly attributed newer-main process changes to
  the repair1 builder; corrected before integration.
- Repair4 omitted its chartered computed-zero regression; the distinction was
  independently measured in round 2 and is a production condition.

The process was more economical than the prior prototype (~6,100 lines and four
large integration exhibits), but still exceeded its own fixed target. Bounded
questions prevented adjacent product scope from entering the repairs; repeated
construction-boundary defects drove the cost instead.

## What worked

- Clean-room rivalry distinguished reusable mapping from embedded rule
  parameters and account identity from statement identity.
- Per-finding triage rejected shape B and the incumbent identity without
  repairing losing designs.
- Mutation tests exposed presence-only, currency-blind, truthy, caller-union,
  fabricated-carrier, duck-carrier, and alternate-entry failures.
- Repairs advanced different questions independently; SC-P1 reached executable
  evidence while SC-P2 stopped at paper and SC-P3 remained unresolved.
- External-builder continuity preserved defect context across repairs.
- The repository entry chain and explicit builder completion contract made
  later handoffs substantially clearer.
- Partial ratification prevented SC-P3 from holding accepted SC-P1/SC-P2
  contracts hostage.

## What should change

### Model scope separately from evidence depth

An iteration may contain several tightly related questions, but reviews and
dispositions must report each question separately. A broad iteration does not
require every proposition to climb to its most expensive evidence level.

### State the accepted runtime surface early

Repair2 proved sole use but not sole construction; repair3 validated construction
but retained alternate callables. Future authority prototypes declare the
supported public dispatch surface before writing code and test bypass reachability
at that surface from the first executable pass.

### Treat review claims as measurements, not verdict prose

The owner-launched Medium-tier round 4 was mechanically disciplined and concise,
but less precise:

- two reviewers mislabeled throwaway evidence as persisted evidence;
- governance overstated Python privacy;
- adversary asserted unmeasured evolution behavior;
- expressiveness missed a required fixture while reporting full coverage.

Future review briefs require an explicit fixture checklist with `run`, `not
run`, or `N/A`, and a claim may be cited only when its command or exhibit is
named. Medium-tier reviewers remain appropriate for bounded reproduction, but
foreman conformance must audit one substantive measurement per review rather
than only file/line mechanics.

### Preserve fixed caps as stop signals

Owner-delegated continuation may authorize another bounded pass, but crossing a
cap must be recorded before dispatch, not reconciled afterward. Artifact volume
is a real cost even when each individual document is short.

## Production adoption boundary

Prototype code remains evidence only. Production reimplements accepted ADR
statements and must test:

- schema-first mapping and statement citizens;
- removal of every caller-supplied closed-membership seam;
- one adopted mapping and one supported dispatch path;
- current-true/false/absent/displaced/ambiguous/duplicate cases;
- exact closure and mapping pins;
- computed zero versus closure-backed zero;
- statement sameness/anti-duplication and correction;
- persisted withdrawal/displacement.

SC-P3 is not a production implementation detail. It is a separate decision
about what the user is claiming complete and what coverage means.
