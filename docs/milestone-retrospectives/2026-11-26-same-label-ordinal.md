# Retrospective: Same-Named Members Are Told Apart by Entry Order

Milestone key: same-label-ordinal. Plan:
`docs/phases/engine-breadth/milestones/same-label-ordinal.md`.
Closed 2026-11-26. Projection and page change (ADR 0090).

## What happened

same-label-members gave each roster member who misses an answer their own
question, but two members entered as "Sam" still both read "Sam". The
owner accepted ADR 0090: a label shared within a kind carries the
member's place in entry order. One build track added `memberOrdinal`, the
page wording, member grouping and the sentence-matching fix parked as
SLM-R3. All 775 recorded lists replay identical; of 23 synthetic probes,
17 differ only in ordinals and order.

The build was adopted across a Claude session limit and then a Codex
usage limit. It ran in parallel with statement-question-labels, which
changes the same projection function. The foreman merged that one first
and rebased this one onto it.

## What worked

- Running both milestones' walk and live tests together after the rebase
  checked the one place they meet, instead of trusting a clean rebase.

## What to change

- A sort key written from the ADR's example (label, ordinal) missed that
  the ordinal counts within a kind (SLM-O1). When a contract scopes a
  counter, test a case where the scope matters: two kinds with one label.
