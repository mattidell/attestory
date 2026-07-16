# Role: Adversary Reviewer — Non-Publication Explanations (Round 2)

Medium tier. Foreman-spawned sub-agent (standing authorization: owner-approved
plan, Gate 8; ADR-0013 reviewer-dispatch amendment).

Attack both iteration designs (`it1/design.md`, `it2/design.md`) with
counterexamples to walk accuracy: cyclic and multi-path blocks, guards whose
truth depends on values that changed after the run, multiple rules publishing
one symbol, deep cascades (line 16 blocked through five ancestors), stale
execution records versus current workspace state, and combinatorial growth of
whatever record structure each design proposes. State each attack as concrete
input state → expected lineage → where the design fails or survives. Classify
every finding; do not repair designs.

Output: `reviews/round-2-adversary.md`. Within-round independence: do not read
the governance reviewer's round-2 review.
