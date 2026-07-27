# Retrospective — Presentation L2 Integration Grounding

- Merged: PR #86, merge commit `1f3bb9a`

## What differed from the plan

The first Builder stopped before implementation because the inherited demo
manifest required line 2a and guard-inapplicable line 9 states absent from the
resolved production package. The amendment correctly split renderer-regression
coverage from production-shaped coordinator evidence.

Independent review found one coordinator-level failure path missed by the
Builder's unit probes: projection rejection could strand reserved artifacts.
The plan's one repair and focused recheck closed it without changing caller or
record-stream semantics.

## What it cost

One clean charter stop, one amended build, one independent review, one focused
repair, and one focused recheck. The cap held.

Foreman custody added avoidable friction: the initial review charter omitted a
commit requirement; a merged amendment worktree remained current while the
build lived elsewhere; and removing the Builder's active worktree stranded its
Claude session. The temporary path alias restored that session.

Final CI also caught three repository-wide mypy `no-any-return` failures that
the focused review commands did not exercise. The owner directed a narrow,
type-only repair (`cc0dcc9`); the milestone then merged with `verify` green.

## Follow-ups

- Correct the planning protocol when the owner schedules process work: tracks
  are build/review units inside one milestone branch, while the milestone PR
  opens only after Tracks 0–N and their reviews are complete.
- Give every Reviewer charter an output path, target branch, and explicit
  commit handoff. Reactivate on the next Reviewer charter.
- Never remove a worktree used by a live session; make the hook launcher fail
  open if its project script disappears. Reactivate at the next hook/process
  maintenance change.
- Presentation L2→L3 remains unselected. Reactivate only when the owner chooses
  to design and verify a live invocation boundary and then exercise it under
  the existing non-descriptive attestation rule.

## What should change in the next plan

Start from the maturity matrix's six-row capability state. Separate “the
projector and renderer are ready” from “a safe live browser vehicle exists,”
and do not describe a real exercise as immediately executable until the latter
is mechanically evidenced.
