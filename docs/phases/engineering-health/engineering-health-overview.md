# Engineering Health

## Purpose

Make the application and its development checks cheaper to run without making
their answers less trustworthy. Begin with the repeated reconstruction of a
workspace's history that now dominates long tests and threatens real-workspace
responsiveness.

## How we will proceed

1. Separate waiting for feedback from the CPU work that produces it.
2. Measure representative work and identify what is repeated unnecessarily.
3. Preserve the meaning of recording, validation, calculation and explanation
   while choosing smaller amounts of work to produce the same result.
4. Compare the result with the original behavior and cost, then decide what
   further test-design work is worth doing.

This is a working direction, not a complete program of infrastructure changes.
The opening milestone will inform the next choice. Existing product contracts
and data-safety boundaries remain unchanged. New tax coverage is not its aim.

## Relationship to product work

The Tax Circumstance Breadth consolidation merged as PR #211. Its phase
assessment found its provisional endpoint met. Engineering health is now the
owner-selected focus; this does not silently settle its remaining product
limitations or require an additional tax vertical.
