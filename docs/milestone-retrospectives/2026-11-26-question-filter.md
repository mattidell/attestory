# Retrospective: Evidence Probes Find Questions by Structure

Milestone key: question-filter. Plan:
`docs/phases/engine-breadth/milestones/question-filter.md`.
Closed 2026-11-26. Evidence tooling only.

## What happened

The roadmap parked a defect: two evidence probes counted a sentence as a
question only if it had a question mark. One build track added a shared
rule that reads the saved model's question links
(`questionRefs[].reasonIndices`, falling back to "?" before v3) and
switched both probes to it. A temporary comparison over 2,976 blocked
reason lists in the six tests that load the probes found the old and new
lists identical, so nothing was re-pinned.

## What worked

- Measuring both rules side by side before re-pinning anything turned
  "no count changes" into a checked claim.

## What to change

- The comparison found one prompt the model never links (the
  per-statement box 4 amount question). A probe defect can hide a page
  defect; when replacing a heuristic, list what the structural rule and
  the heuristic disagree on, even when the counts match.
