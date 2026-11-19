# Retrospective: Replays Compare the Whole Saved Return (2025)

Milestone key: full-surface-replay. Plan:
`docs/phases/engine-breadth/milestones/full-surface-replay.md`.
Closed 2026-11-18. Tooling only: `tools/recorded_replay.py` and its
tests. No package change.

## What happened

The line16-names review showed that the shared replay pin let a changed
line 12e value or an unwatched row's code pass byte-equal, and each
content milestone since had written its own stricter classifier. A
Claude Sonnet builder added a full-surface snapshot, a typed diff and
declared expectations to the shared tool, with controls that mutate the
saved output before the snapshot. Its first v95-against-v96 run failed
366 lists on attachment titles copied into `citationGroups`; it widened
the sentence expectation to cover that copy. A fresh Claude Opus review
confirmed that was a fix, not a loosening (exactly the 366 lists fail
with the old kinds), and found the larger limit: recorded lists reach
only one of six optional model blocks, so "nothing else changed" holds
only for what the corpus reaches. The repair added a synthetic mortgage
list, which itself exposed two unaliased generated ids in the
explanation block, and controls that fail when the graph, other model
keys or typed comparison are dropped.

## What worked

- Reproducing the reviewer's L16-R1 controls as permanent controls.
- A synthetic case for an uncovered block found a real tool defect the
  775 recorded lists never could.

## What to change

- A replay corpus is evidence only for the shapes it contains. Name the
  coverage alongside the claim, and add a synthetic case when a
  milestone changes something the corpus does not reach.
