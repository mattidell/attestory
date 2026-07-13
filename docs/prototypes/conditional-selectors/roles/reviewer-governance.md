# Role: Governance Reviewer — Conditional Selectors, Round 1R (re-performed)

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
`tests/` (Track 3 implements the disputed shape; judge the design, not the
implementation).

**Read:** the topic `plan.md`, `charter-it1.md`, `it1/design.md`,
`examination-it1.md`, `docs/governance/` (constitution, ontology, principles,
engineering constraints), ratified ADRs 0002–0012 and 0016–0017, and committed
`packages/derivation/` and `packages/kernel/` contracts.

**Assignment.** Measure both iteration-1 shapes (Shape A: rule-driven
derivation in the existing rule language; Shape B: first-class selector
citizen) against CS-P1 and CS-P2 and the governance set: logic/parameter
separation, displacement and dependency-edge integrity (Article 7 and
ADR-0010), no implicit runner-resident defaulting or hidden state (Articles
11/12), citizen/schema conformance, and whether either shape requires a new
edge kind or runner pathway the contracts do not license. Classify every
finding (decision-blocking / production condition / non-blocking); do not
repair designs.

**Output:** `reviews/round-1r-governance.md`, findings labeled CS-G1R,
CS-G2R, …, ending with a verdict per shape: accept / conditionally accept
(conditions listed) / reject. Advisory: the owner decides disposition.
