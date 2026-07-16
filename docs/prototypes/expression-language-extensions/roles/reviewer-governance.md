# Role: Governance Reviewer — Expression Language Extensions (Committee)

Medium tier. Owner-launched external context (2026-07-13). This is the committee
round over **two independent designs** of the same two propositions: the
incumbent (`it1/`) and the clean-room rival (`it2/`). You measure both and make
their convergence and divergence explicit — that comparison is the point of the
round, not a tie-break to be avoided.

**Independence exclusions — do not read:** the Adversary reviewer's output
(`reviews/round-1-adversary.md`), any draft or notes toward ADR-0025, and any
uncommitted working-tree changes under `packages/` or `tests/` (judge the
designs, not an implementation). There is no prior ELX review to exclude.

**Read:** the topic `plan.md`, `charter-it1.md`, `charter-it2.md`,
`it1/design.md`, `examination-it1.md`, `it2/design.md`, `examination-it2.md`,
`docs/governance/` (constitution, ontology, principles, engineering
constraints), ratified ADRs 0002, 0004, 0006–0012, 0016, 0017, 0023, and
**0024 (accepted 2026-07-13)**, and committed `packages/derivation/` and
`packages/kernel/` contracts and schemas. The conditional-selectors
`evaluation-analysis.md` is in scope for grounding the three refuted workarounds
these designs must defeat.

**Assignment.** For **each design**, measure both propositions against the
governance set:

- **ELX-P1 (declared optional default).** No third edge kind (Article 7); the
  default is versioned, declared content, not runner-resident policy (Article
  11); an asserted input is never overwritten; a later assertion displaces the
  default and its consumers through the two existing edge kinds only; pins
  record whether a value came from the default or an assertion; the disposition
  vocabulary (ADR-0012) stays intact. Judge each design's displacement
  mechanism specifically: the incumbent proposes a `default_superseded`
  displacement **root class** refining ADR-0010 decision 5; the rival extends
  the existing **correction fold** to derived-finding answers sharing a
  `fact_id` with no new root class. State which is more conformant to Article 7
  and ADR-0010, and whether either quietly introduces standing-affecting state.
- **ELX-P2 (categorical comparison).** Contract shape conformance: the incumbent
  proposes a `match` op; the rival proposes `categorical_compare` +
  `category_literal` over an existing fact type's declared string enum. Judge
  citizen/schema conformance, whether decimal coercion is truly avoided, whether
  the mismatch disposition is a contained explained failure using existing
  vocabulary, and whether the ADR-0024 numeric-code migration each proposes is
  an append-only ordinary succession (no silent conversion of a human finding).

Classify every finding (decision-blocking / production condition / non-blocking).
Do not repair designs. Where the two designs converge on a mechanism, say so —
convergence under independent authorship is the strongest signal available.

**Output:** `reviews/round-1-governance.md`, findings labeled ELX-G1, ELX-G2, …,
each naming the design(s) it applies to, ending with a verdict **per proposition
per design**: accept / conditionally accept (conditions listed) / reject, plus a
one-line recommendation on which design's mechanism to carry into ADR-0025 (or a
hybrid, naming the parts). Advisory: the owner decides disposition.
