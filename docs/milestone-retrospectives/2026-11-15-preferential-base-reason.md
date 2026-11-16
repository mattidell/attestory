# Retrospective: Lines Below Line 16 Name Their Question (2025)

Milestone key: preferential-base-reason. Plan:
`docs/phases/engine-breadth/milestones/preferential-base-reason.md`.
Closed 2026-11-15. Core v91, registry v89, release v89. Contract: ADR
0086 (unchanged). No schema, engine, projection or page change.

## What happened

A review note on blocked-names-question (BNQ-R7) said that on four
recorded returns, with Schedule D required and no sale, lines 24, 33 and
37 blocked with no question of their own. P0 measured 23 such fields, not
the note's list, all stopping at `selected-preferential-base`, whose
guard turned inapplicable. A v11 successor blocks there and names its
questions.

Track 0 asked whether the four sale questions were enough. They were
not: no answer to them unblocks a return with no sale to enter; changing
Exception 1 does. The successor names eight questions. A matching line
16 successor was gated on the ten blocked-names-question cases, changed
one, and was parked. The fresh review was ready; its note on test
strength was repaired.

Dispatch: grok throughout, one builder session resumed across P0, Track
0, Track 1 and the repair, and one fresh reviewer session.

## What worked

- Asking Track 0 a pointed question (are the named questions enough)
  changed the design before the build.
- A stop rule written into the Track 1 charter parked line 16 without a
  round trip.
- One replay part file served P0; the published replay took 23 minutes.

## What to change

- A headless builder that starts a long command in the background and
  ends its turn loses the command. Every brief now says foreground only
  and never end the turn while a command runs.
- Measure a review note's field list before planning against it.
- Tests should compare question text and line maps, not counts and
  producer signatures; say so in the Track 1 charter.

## Follow-ups

Parked: line 16 naming the eight questions; lines 25b and 25d (the box 4
amount has no question).
