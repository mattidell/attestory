# Charter: Iteration 1 — Conclusion-Level Direct-Route Authority

Audience: Builder

Date: 2026-07-28. Track 0 of Capital-Gain Distributions and Form 1040
Line 7a.

## Context Capsule

- **Source ref:** `prototypes/capital-gain-distributions-line7a/it1`; resolve
  and record its commit at launch with
  `python3 tools/build_orientation_block.py --ref prototypes/capital-gain-distributions-line7a/it1`.
- **Exact object:** the incumbent Rung-1 paper design and examination required
  below. Existing repository contracts and content are evidence, not edit
  targets.
- **Role:** Incumbent Builder, High capability / high effort.
- **Scope and evidence-rung ceiling:** P1–P3 under the plan's
  conclusion-level incumbent topology. Rung 1 static paper instantiation only.
- **Stop conditions:** any need for production code, a schema/content edit,
  a validator/evaluator probe, governance interpretation, a fourth
  proposition, real data, or Schedule D implementation.
- **Full reads before acting:** this charter; the topic `plan.md`; the
  milestone plan's Prototype Decision Inventory, Contracts, Fixtures, and Data
  Safety sections; ADR-0035; ADR-0038; the 2025 Form 1040 line-7a instruction
  linked by the plan; `packages/content/tax/2025/dividend-universe.json`;
  `packages/content/tax/2025/f1099div.bundle.json`;
  `packages/content/tax/2025/qdcg.bundle.json`;
  `packages/content/tax/2025/rule.form1040-line9.v2.json`;
  `packages/content/tax/2025/rule.form1040-line16.v2.json`; and
  `packages/tax/loader.py`.

## Assignment

Design the **conclusion-level authority incumbent**:

1. **P1 — direct-route authority.** Reuse ADR-0038's current contributed
   categorical `schedule-d-required` fact as the authority for direct
   reporting. Define missing, `"yes"`, `"no"`, correction, and supersession
   behavior. Do not invent finer eligibility facts.
2. **P2 — box-2a family promotion.** Propose the smallest versioned successor
   statement/member/family/closure shape that makes box 2a composable while
   preventing any rule or package from collecting both it and the historical
   recorded/non-composable representation.
3. **P3 — line-7a and QDCG handoff.** Propose declared bindings from the box-2a
   subtotal to line 7a, line 9, and QDCG. Schedule-D-required must remain an
   honest inapplicable/non-publication route; nothing fabricates Schedule D.

The output is a contract design, not implementation pseudocode. State every
proposed successor contract sentence precisely enough that a later ADR could
adopt or reject it.

## Required paper evidence

Instantiate all ten shared cases from `plan.md` using concrete
`demo.*`/`demo-*` facts, identities, horizons, amounts, declarations,
publications, and pins:

1. eligible single payer;
2. eligible multiple payers;
3. authority missing;
4. Schedule D required;
5. contradiction in both temporal orders and the same batch;
6. authority correction/supersession in both directions;
7. closed-empty, open, undeclared, stale, corrected, and removed family states;
8. historical/successor reach-around and mixed-graph attack;
9. downstream double-count and direct-read attack; and
10. qualified-zero neighbor.

For each P1–P3 provide:

- two positive instances;
- two meaningful negatives;
- one lifecycle trace;
- a producer → authority → consumer → failure map;
- accepted contracts consumed unchanged;
- proposed successor contract sentences;
- production conditions; and
- unresolved questions.

Cases 3, 4, 5, 6, 8, and 9 are mandatory negative/lifecycle evidence. Show
exact current/displaced states and pins; “the implementation checks this” is
not evidence.

## Incumbent constraints

- The conclusion-level `schedule-d-required` declaration is the topology under
  test. You may find it insufficient, but you may not silently replace it with
  the rival's component assertions.
- Preserve ADR-0038's capital-gain-distribution contradiction in both orders
  and same-batch contribution.
- Historical published schemas/content and accepted ADR text are immutable.
  Use proposed successor versions on paper.
- The box-2a subtotal enters line 9 exactly once. QDCG consumes a selected
  declared publication/binding, never raw statement content.
- A `"yes"` Schedule-D-required answer does not publish the direct route and
  does not produce an attachment.
- No absent condition becomes zero or false by inference.

## Outputs

Create exactly:

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/it1/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/it1/examination.md`

`design.md` contains the topology, concrete instances, maps, successor
sentences, and production conditions. `examination.md` reports P1, P2, and P3
separately as settled at Rung 1 or unresolved, with exact case citations.

Do not edit this charter, the plan, phase state, SEAT file, process log,
production paths, schemas, tests, ADRs, or another prototype directory.

## Completion and custody

Before writing, echo your understood scope, Rung-1 ceiling, output paths, and
stop conditions.

Stop after the two outputs are complete and committed on the assigned branch.
Do not merge, rebase, open a PR, tag an exhibit, review the rival, or begin a
repair. Report the commit SHA, files changed, and proposition-by-proposition
status to the foreman.

## Data safety

Every example is synthetic and publishable. Do not use or describe personal
source documents, real values, real identities, real dispositions, refusal
reasons, workspace locations, screenshots, or generated private output.
