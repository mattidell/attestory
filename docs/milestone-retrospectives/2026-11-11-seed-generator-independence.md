# Retrospective: The v70 Entry Seed Generates Without Test Helpers

Milestone key: seed-generator-independence. Plan:
`docs/phases/engine-breadth/milestones/seed-generator-independence.md`.
Closed 2026-11-11. Tooling only: no package, schema or content changed.

## What happened

The tool that writes the v70 W-2 entry seed built its complete return by
calling test helpers, and through them loaded 22 test modules. P0 traced
that chain and prototyped two ways out. Moving the helpers to a non-test
module matched the seed bytes but copied 1,870 lines and would retarget 56
test modules. Committing the complete return as a synthetic source file
matched too, at 294 lines and no test touched. The source file was chosen.

Track 1 committed `packages/sample_data/entry_loop_v70/complete-core-return.jsonl`,
pointed the generator at it, and added a check that fails if the generator
loads a test module. The seed bytes are unchanged.

The fresh review found the plan still claiming the byte test catches helper
drift (by design it no longer does), an import check that missed a `tests`
import the render path never runs, and a refresh recipe that could not be
run as written. All three were repaired: the plan sentence, a static parse
of the generator's imports beside the run-time check, and an exact recipe
that reproduces the source file byte for byte.

## What worked

- Prototyping both shapes in P0. The size difference made the decision
  without argument.
- A cheap milestone: about $12 of builder and reviewer time in total.

## What to change

- When a test pins one thing (seed bytes) that used to also pin another
  (helper output), write down in Decisions which coverage goes away, so
  the plan's scope line is updated in the same commit.
- A recipe in a docstring is a claim; run it before committing it.

## Follow-ups

None parked. Other golden generators under `tools/` still import test
modules; none feeds a runtime fixture, and they stay as they are.
