# Retrospective: A Refused Head of Household Status Does Not Set the Worksheet Ceilings

Milestone key: hoh-no-worksheet-ceilings. Plan:
`docs/phases/engine-breadth/milestones/hoh-no-worksheet-ceilings.md`.
Closed 2026-11-24. Core v104, registry v102, release v102.

## What happened

hoh-qualifying-person review HOH-R5 found the capital gain worksheet's
lines 6 and 13 read only the claimed filing status, so a refused head of
household or surviving spouse still showed that status's ceiling. A grok
P0 found the standard-deduction line 3 pattern already reads the status
tests, quoted the worksheet's per-status ceilings (so no fallback status),
and replayed a content successor with no number change. Track 1 published
it as core v104 after eic-separated-married's v103; a fresh grok review
found nothing.

## What worked

- Reusing an existing rule's reading of the same answer instead of a new
  shape: the review had nothing to find.
- Writing decisions while the previous content milestone was in CI, and
  starting Track 1 the moment it merged, so versions stacked cleanly.

## What to change

- Nothing new. The size guard now runs in the fast lane, and Track 1 added
  the two successors to it without a CI round trip.
