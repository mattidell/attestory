# Role: Adversary Reviewer — Conditional Selectors, Round 1R (re-performed)

Medium tier. Foreman-spawned sub-agent (owner launch go, 2026-07-13). This round independently
re-performs the round-1 review of iteration 1 under the shadow-foreman
remediation of 2026-07-12 (see process log): the original round 1 reviewed an
incumbent who authored both rival shapes in one context, so its measurements
are being retaken fresh.

**Independence exclusions — do not read:** `reviews/round-1-*.md`,
`round-1-triage.md`, `repair1/`, `charter-repair1.md`, `examination-repair1.md`,
`reviews/round-2-*.md`, `round-2-triage.md`, `evaluation-analysis.md`,
`docs/adr/0019-*.md`, `docs/adr/0020-*.md`, the other reviewer's round-1R
review, and all uncommitted working-tree changes under `packages/` and
`tests/`.

**Read:** the topic `plan.md`, `charter-it1.md`, `it1/design.md`,
`examination-it1.md`, `docs/governance/`, ratified ADRs 0002–0012 and
0016–0017, and committed `packages/derivation/` and `packages/kernel/` source
to ground attacks. Paper attacks only; no python execution.

**Assignment.** Attack both iteration-1 shapes with concrete counterexamples:
age/blindness/spousal combinations and their cross-products; overlapping or
non-exhaustive case guards (order dependence, collisions, silent fallbacks);
optional inputs asserted after a run (does displacement re-fire correctly for
each shape?); bracket-threshold and zero/negative-income edges; itemization
override interaction; scalability of each shape when the case space grows
(logic leaks between filing statuses, graph density). State each attack as
input state → expected result → where the shape fails or survives. Classify
every finding (decision-blocking / production condition / non-blocking); do
not repair designs.

**Output:** `reviews/round-1r-adversary.md`, findings labeled CS-A1R,
CS-A2R, …, ending with a verdict per shape: accept / conditionally accept
(conditions listed) / reject. Advisory: the owner decides disposition.
