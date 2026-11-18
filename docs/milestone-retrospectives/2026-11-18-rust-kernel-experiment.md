# Retrospective: Rust Kernel Experiment (2025)

Milestone key: rust-kernel-experiment. Plan:
`docs/phases/engine-breadth/milestones/rust-kernel-experiment.md`.
Closed 2026-11-18. No package version change. Four algorithmic fixes in
`packages/derivation/`; no kernel, content or schema change.

## What happened

The owner asked whether the engine should move to Rust. The milestone
measured before porting. P0 timed all 775 recorded lists on core v96 and
profiled the median, the slowest and the long recorder test K13. The
kernel was about 6 % of the median replay and 1 % of the slowest; rule
evaluation about 2 %. Half the median went to a member-inside-member
scan in package validation, run twice on the same package, and 84 % of
the slowest to a blocked-line question walk that re-walked shared rows
once per path.

The foreman redirected Track 1 to fix those in Python first, with every
recorded list required to stay byte-identical. The median list went
from 7.76 s to 2.94 s and the slowest from 49.6 s to 3.55 s. The fresh
review was READY with three low notes (an untested cycle guard, a
validation memo key that trusted its caller, and a table row); the
repair closed them and showed one guard is output-neutral. The Rust
port is parked with its slice and both owner gates.

Dispatch ran on budgets again: a Claude Opus sub-agent (P0), agy Sonnet
(Track 1 items 0-4, until its credits ran out), a Claude Sonnet
sub-agent (Track 1 item 5 and the repair), agy Gemini 4 Argon (review).
The Sonnet sub-agent adopted the interrupted builder's commits after
reviewing them and caught that its validation-order evidence compared
runs under different hash seeds.

## What worked

- Profiling before porting. A port of the kernel would have sped up the
  6 % that was not slow.
- A pristine export of the pre-change commit as the identity baseline,
  rather than a baseline run in a tree that was being edited.
- The fresh reviewer mutated the memo code in memory to test whether
  the tests would notice, and found a guard they did not cover.

## What to change

- The pristine validator already ordered some errors by hash seed. An
  identity contract that says "same order" must name the seed, or it
  compares noise.
- A random-graph test can miss the one shape that matters. Pair it with
  the specific counterexample a reviewer can construct.
