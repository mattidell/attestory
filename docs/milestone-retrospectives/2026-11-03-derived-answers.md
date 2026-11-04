# Retrospective: The Return Answers What It Already Shows (2025)

Milestone key: derived-answers. Plan:
`docs/phases/engine-breadth/milestones/derived-answers.md`. Closed
2026-11-03.

## What happened

P0 sorted the six candidates and the other 74 facts by what the record
proves. Every candidate was at most partly derivable: a recorded statement
proves presence, and the answer that releases most lines is an absence.
Four partly derivable candidates went to Track 1 under one condition: no
return v73 publishes may newly block. Two failed it (line 2a and the other
dependent), because the proof reads a family closure that an answered
return never needed. Form 1098 and the Form 1116 cap landed on core v74.
The fresh review found no required fixes; its one recommendation, an
open Form 1098 family, turned out to ask fewer, better questions on v74
and was locked by a test.

## What worked

- Naming the direction first. "The record proves presence, never absence"
  removed 76 facts in P0 before any rule was written.
- A hold condition stated before the build. Track 1 measured it first and
  held two candidates without a foreman ruling, including a successor that
  would have published an unclosed box 8.
- Grok CLI agents in the foreman's worktree with file handoff ran all three
  units without a restart.

## What to change

- A proof that reads a closure costs answered returns. Check what the proof
  newly reads, not only what it releases, in P0, so the hold is seen before
  the build.
- `ref` raising on an absent name is the one engine limit behind both the
  holds and the lost contradiction blocks; an absent-tolerant read is the
  next lever if derived answers continue.

## Follow-ups

- Line 2a and the other-dependent answer, and the two contradiction blocks,
  behind an absent-tolerant read (engine change).
- A per-run sentence naming the question the record answered (schema).
