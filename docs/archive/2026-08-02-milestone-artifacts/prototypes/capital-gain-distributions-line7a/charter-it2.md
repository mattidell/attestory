# Charter: Iteration 2 — Component-Backed Direct-Route Authority

Audience: Builder

Date: 2026-07-28. Track 0 of Capital-Gain Distributions and Form 1040
Line 7a.

## Context Capsule

- **Source ref and resolved launch commit:** source ref
  `prototypes/capital-gain-distributions-line7a/it2`; resolve and record its
  commit at launch with
  `python3 tools/build_orientation_block.py --ref prototypes/capital-gain-distributions-line7a/it2`.
- **Exact object:** the clean-room rival Rung-1 paper design and examination
  required below. Existing repository contracts and content are evidence, not
  edit targets.
- **Role:** Clean-room Rival Builder, High capability / high effort.
- **Scope and evidence-rung ceiling:** P1–P3 under the plan's component-backed
  eligibility topology. Rung 1 static paper instantiation only.
- **Stop conditions:** exposure to incumbent or review material; any need for
  production code, a schema/content edit, a validator/evaluator probe,
  governance interpretation, a fourth proposition, real data, or Schedule D
  implementation.
- **Full reads before acting:** this charter; the topic `plan.md`; the
  milestone plan's Prototype Decision Inventory, Contracts, Fixtures, and Data
  Safety sections; ADR-0010; ADR-0014 through ADR-0017; ADR-0023; ADR-0032;
  ADR-0035; ADR-0038; the 2025 Form 1040 line-7a instruction linked by the
  plan; `packages/content/tax/2025/dividend-universe.json`;
  `packages/content/tax/2025/f1099div.bundle.json`;
  `packages/content/tax/2025/qdcg.bundle.json`;
  `packages/content/tax/2025/rule.form1040-line9.v2.json`;
  `packages/content/tax/2025/rule.form1040-line16.v2.json`;
  `packages/derivation/evaluator.py`;
  `packages/derivation/package_validation.py`;
  `packages/kernel/findings.py`; and `packages/tax/loader.py`.

## Clean-room seal

This branch is cut from the approved plan on `origin/main` and contains no
incumbent output or review. Do not seek, fetch, inspect, or receive:

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/it1/`;
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/reviews/`;
- the iteration-1 branch, commits, examination, thread, summary, findings, or
  any other builder's work.

Do not infer the incumbent shape beyond the abstract rival definition already
published in `plan.md`. If any sealed material reaches the context, stop
without writing and report the leak.

## Assignment

Design the **component-backed eligibility rival**:

1. **P1 — direct-route authority.** Represent the Form 1040 direct-reporting
   exception's component conditions as the smallest explicit set of
   contributed categorical assertions that can authorize the route without
   assumed absence. State whether ADR-0038's existing
   `schedule-d-required` declaration remains an input, becomes a checked
   conclusion, or is displaced by a successor contract. Define missing,
   affirmative/negative, correction, supersession, and internally
   inconsistent behavior. Every extra assertion is an explicit topology cost.
2. **P2 — box-2a family promotion.** Propose the smallest versioned successor
   statement/member/family/closure shape consistent with the component-backed
   authority. Prevent every rule and adopted package graph from collecting or
   trusting both successor box-2a source content and the historical
   recorded/non-composable representation. Preserve statement identity,
   horizon freshness, closed-empty honesty, correction/removal behavior, and
   ADR-0038's contradiction interlock.
3. **P3 — line-7a and QDCG handoff.** Propose declared bindings from the
   selected box-2a subtotal/publication to line 7a, line 9 exactly once, and
   QDCG. Trace how each component-authority state affects line 7a and the
   downstream line-9 → line-11 → line-15 → line-16 chain. A Schedule-D-required
   case remains honestly outside scope and produces no fabricated attachment.

The output is a contract design, not implementation pseudocode. State every
proposed successor contract sentence precisely enough that a later ADR can
adopt or reject it. Do not design a general capital-gains questionnaire or
expand the milestone to the excluded source families.

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
- topology cost relative to a conclusion-level declaration;
- production conditions; and
- unresolved questions.

Cases 3, 4, 5, 6, 8, and 9 are mandatory negative/lifecycle evidence. Every
case chooses exact component-fact values and exact QDCG-relevant inputs; “may
be present,” “as applicable,” or “the implementation checks this” is not
evidence.

## Rival constraints

- Component-backed eligibility is the topology under test. Do not collapse it
  to the existing `schedule-d-required` conclusion as the sole authority.
- Preserve the current owner-controlled contribution boundary. No absent
  component becomes false, zero, satisfied, or “not required” by inference.
- Preserve ADR-0038's capital-gain-distribution contradiction in both orders
  and same-batch contribution.
- Historical published schemas/content and accepted ADR text are immutable.
  Use proposed successor versions on paper.
- The box-2a subtotal enters line 9 exactly once. QDCG consumes a selected
  declared publication/binding, never raw statement content.
- A Schedule-D-required state publishes no direct route and produces no
  Schedule D or attachment artifact.
- If honest component authority requires source families outside the
  milestone's non-goals, report the topology as insufficient rather than
  silently widening scope.

## Outputs

Create exactly:

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/it2/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/it2/examination.md`

`design.md` contains the topology, concrete instances, maps, successor
sentences, topology costs, and production conditions. `examination.md` reports
P1, P2, and P3 separately as settled at Rung 1 or unresolved, with exact case
citations.

Do not edit this charter, the plan, phase state, SEAT file, production paths,
schemas, tests, ADRs, another prototype directory, or any process/review file.

## Completion and custody

Before writing, echo your understood scope, the Rung-1 ceiling, both output
paths, the clean-room exclusions, and every stop condition. Include an explicit
attestation that no sealed material was read.

Stop after the two outputs are complete and committed on the assigned branch.
Do not merge, rebase, open a PR, tag an exhibit, review the incumbent, compare
the shapes, begin a repair, or advance the repository pointer. Report the
commit SHA, files changed, proposition-by-proposition status, and clean-room
attestation to the foreman.

## Data safety

Every example is synthetic and publishable. Do not use or describe personal
source documents, real values, real identities, real dispositions, refusal
reasons, workspace locations, screenshots, or generated private output.
