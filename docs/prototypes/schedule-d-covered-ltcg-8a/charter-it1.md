# Charter: Iteration 1 — Nested-Identity, Synthesized-Conclusion Incumbent

Audience: Builder

Date: 2026-08-01. Track 0 of Covered Long-Term Gains, Schedule D Line 8a.

## Context Capsule

- **Source ref:** `prototypes/schedule-d-covered-ltcg-8a/it1`; resolve and
  record its commit at launch with
  `python3 tools/build_orientation_block.py --ref prototypes/schedule-d-covered-ltcg-8a/it1`.
- **Exact object:** the incumbent Rung-1 paper design and examination
  required below. Existing repository contracts and content are evidence,
  not edit targets.
- **Role:** Incumbent Builder, High capability / high effort.
- **Scope and evidence-rung ceiling:** P1, P2, and P3 under the plan's
  incumbent topology. Rung 1 static paper instantiation only.
- **Stop conditions:** any need for production code, a schema/content edit,
  a validator/evaluator probe, governance interpretation, a fourth
  proposition, real data, or an edit to ADR-0036 or ADR-0050.
- **Full reads before acting:** this charter; the topic `plan.md`; the
  milestone plan's Supported Source Class, Completeness Boundary, Prototype
  Decision Inventory, and Contracts sections
  (`docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md`);
  ADR-0036; ADR-0050; ADR-0015; ADR-0016; the 2025 Schedule D line-8a
  instructions and Form 1099-B instructions linked by the milestone plan;
  `packages/content/tax/2025/rule.schedule-d-required.conclusion.json`;
  `packages/content/tax/2025/schedule-d-required.conclusion-binding.json`;
  `packages/content/tax/2025/exception1.bundle.json`;
  `packages/content/tax/2025/qdcg.bundle.json`;
  `packages/content/tax/2025/rule.form1040-line7a.json`;
  `packages/content/tax/2025/rule.form1040-line7b.json`; and
  `packages/tax/loader.py`.

## Assignment

Design the **nested-identity, synthesized-conclusion incumbent**:

1. **P1 — transaction source family and identity.** Extend the existing
   statement-instance pattern (ADR-0015/0016): model the transaction as a
   member fact nested under the broker-and-statement family, keyed by tax
   year + broker + logical statement entity + logical transaction entity,
   mirroring how K-1 and market-discount members nest under their statement
   families. Define missing, present, corrected, and multi-transaction/
   multi-broker behavior. Two sales from one broker must remain distinct
   members; correction must supersede at the transaction identity, not the
   statement identity.
2. **P2 — completeness-boundary declaration shape.** Generalize ADR-0050's
   C1-C4 pattern to a single checked conclusion over nine contributed/
   derived component predicates, one per absent-source claim named in the
   milestone plan's Completeness Boundary section, with presence-before-
   value and no default. Define missing, `"yes"`/`"no"`, correction, and
   supersession behavior for each component.
3. **P3 — Schedule D content and QDCG/line-16 binding (paper spike).**
   Instantiate Schedule D line 8a (columns (d)/(e)/(h)), Part II line 15,
   and Part III line 16 as content on the existing ADR-0036 attachment
   ontology. Propose a line-16 successor that extends ADR-0050 decision 7's
   branch structure with an additional Schedule-D-sourced case, without
   editing ADR-0050. State explicitly how the box-2a QDCG path and the
   Schedule D QDCG path coexist without double-counting when both, either,
   or neither is present.

The output is a contract design, not implementation pseudocode. State every
proposed successor contract sentence precisely enough that a later ADR could
adopt or reject it.

## Required paper evidence

Instantiate all eleven shared cases from `plan.md` using concrete
`demo.*`/`demo-*` facts, identities, horizons, amounts, declarations,
publications, and pins:

1. eligible single broker, single transaction;
2. eligible single broker, multiple transactions;
3. eligible multiple brokers;
4. transaction correction (same identity supersedes; distinct original
   unaffected);
5. completeness component missing, each of the nine, in turn;
6. box-2a interaction, present and nonzero;
7. box-2a interaction, closed empty;
8. family lifecycle (closed-empty, open, undeclared, stale-horizon);
9. historical/raw-member reach-around and incomplete-universe attack;
10. downstream double-count attack (box-2a and Schedule D both contributing
    the same gain, or QDCG reading raw transaction content); and
11. non-covered / adjustment-code transaction rejected from the eligible
    family.

For each P1, P2, and P3 provide:

- two positive instances;
- two meaningful negatives;
- one lifecycle trace;
- a producer → authority → consumer → failure map;
- accepted contracts consumed unchanged (including ADR-0050 and ADR-0036);
- proposed successor contract sentences;
- production conditions; and
- unresolved questions.

Cases 4, 5, 6, 7, 9, 10, and 11 are mandatory negative/lifecycle evidence.
Show exact current/displaced states and pins; "the implementation checks
this" is not evidence.

## Incumbent constraints

- The nested-member identity shape and the synthesized checked-conclusion
  shape are the topologies under test. You may find either insufficient, but
  you may not silently replace them with the rival's independent-family or
  direct-multi-read shapes.
- ADR-0050 and ADR-0036 are immutable history. Every P2/P3 sentence is a
  proposed *successor*, never an in-place edit — state exactly which
  ADR-0050 clause the successor supersedes and how.
- Two transactions from one broker remain distinct members; correction
  displaces only the corrected transaction's identity.
- The completeness boundary must be honest under a missing component: no
  absent condition becomes `"no"`/zero/false by inference, and Schedule D
  never publishes `required-and-complete` while any of the nine components
  is missing or violated.
- The eligible long-term family's subtotal enters Schedule D line 8a exactly
  once; Schedule D line 16 enters line 7a exactly once; QDCG consumes a
  selected declared publication/binding, never raw transaction or statement
  content.
- Gain-only, no-adjustment, and no-special-rate remain source-class
  conditions established by contributed/attested fact presence, not derived
  by the engine computing proceeds minus basis.

## Outputs

Create exactly:

- `docs/prototypes/schedule-d-covered-ltcg-8a/it1/design.md`
- `docs/prototypes/schedule-d-covered-ltcg-8a/it1/examination.md`

`design.md` contains the topology, concrete instances, maps, successor
sentences, and production conditions. `examination.md` reports P1, P2, and
P3 separately as settled at Rung 1 or unresolved, with exact case citations.

Do not edit this charter, the plan, phase state, SEAT file, process log,
production paths, schemas, tests, ADRs, or another prototype directory.

## Completion and custody

Before writing, echo your understood scope, Rung-1 ceiling, output paths,
and stop conditions.

Stop after the two outputs are complete and committed on the assigned
branch. Do not merge, rebase, open a PR, tag an exhibit, review the rival,
or begin a repair. Report the commit SHA, files changed, and
proposition-by-proposition status to the foreman.

## Data safety

Every example is synthetic and publishable. Do not use or describe personal
source documents, real values, real identities, real dispositions, refusal
reasons, workspace locations, screenshots, or generated private output.
