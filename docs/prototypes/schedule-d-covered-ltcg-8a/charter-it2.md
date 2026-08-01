# Charter: Iteration 2 — Independent-Family, Direct-Multi-Read Rival

Audience: Builder

Date: 2026-08-01. Track 0 of Covered Long-Term Gains, Schedule D Line 8a.

## Clean-room seal

This branch was cut directly from `origin/main` at `a05d637`. It contains no
incumbent (`it1`) branch, commit, output, design, examination, or summary.
Do not fetch, read, or ask about `prototypes/schedule-d-covered-ltcg-8a/it1`
or any description of what it contains. Work only from the plan and the
accepted repository contracts named below.

## Context Capsule

- **Source ref:** `prototypes/schedule-d-covered-ltcg-8a/it2`; resolve and
  record its commit at launch with
  `python3 tools/build_orientation_block.py --ref prototypes/schedule-d-covered-ltcg-8a/it2`.
- **Exact object:** the rival Rung-1 paper design and examination required
  below. Existing repository contracts and content are evidence, not edit
  targets.
- **Role:** Rival Builder, High capability / high effort, clean-room.
- **Scope and evidence-rung ceiling:** P1, P2, and P3 under the plan's rival
  topology. Rung 1 static paper instantiation only.
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

Design the **independent-family, direct-multi-read rival**:

1. **P1 — transaction source family and identity.** Model the
   broker-and-statement identity as a contributed anchor fact and the
   transaction identity as its own closed family keyed to that anchor, so
   correction and closure operate at transaction grain independently of
   statement-level correction. Define missing, present, corrected, and
   multi-transaction/multi-broker behavior. Two sales from one broker must
   remain distinct members; correction must supersede at the transaction
   identity, not the statement or anchor identity.
2. **P2 — completeness-boundary declaration shape.** No synthesizing
   conclusion citizen. The Schedule D attachment and line-16 rules each
   `require_closed` the composable families (eligible long-term family,
   box-2a family) directly and read a set of independently presence-checked
   contributed absence declarations for the non-composable sources (K-1
   gains, Forms 2439/4684/4797/6252/6781/8824, lines 18/19, 1099-DA/QOF),
   reusing the Schedule-B Part-III presence-semantics idiom ADR-0036 already
   generalizes instead of inventing a new conclusion shape.
3. **P3 — Schedule D content and QDCG/line-16 binding (paper spike).**
   Instantiate Schedule D line 8a (columns (d)/(e)/(h)), Part II line 15,
   and Part III line 16 as content on the existing ADR-0036 attachment
   ontology. Propose a shared "selected preferential-base" publication that
   either route (box-2a direct or Schedule D) produces exactly one of,
   consumed by a single line-16 rule unchanged in shape from the existing
   QDCG state partition's structure, differing only in which producer is
   currently selected. Push the branch decision upstream of line 16 rather
   than enumerating a Schedule-D-sourced case inside it.

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

## Rival constraints

- The independent-family identity shape and the direct-multi-read
  completeness shape are the topologies under test. You may find either
  insufficient, but you may not silently replace them with a synthesizing
  conclusion citizen or a nested-member identity merely because it seems
  simpler — if the rival shape genuinely cannot close, say so and name why.
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
- You may not win the comparison by silently expanding production scope;
  any extra facts your shape needs are part of its cost and must be
  explicit in the paper instances.

## Outputs

Create exactly:

- `docs/prototypes/schedule-d-covered-ltcg-8a/it2/design.md`
- `docs/prototypes/schedule-d-covered-ltcg-8a/it2/examination.md`

`design.md` contains the topology, concrete instances, maps, successor
sentences, and production conditions. `examination.md` reports P1, P2, and
P3 separately as settled at Rung 1 or unresolved, with exact case citations.

Do not edit this charter, the plan, phase state, SEAT file, process log,
production paths, schemas, tests, ADRs, or another prototype directory.

## Completion and custody

Before writing, echo your understood scope, Rung-1 ceiling, output paths,
and stop conditions.

Stop after the two outputs are complete and committed on the assigned
branch. Do not merge, rebase, open a PR, tag an exhibit, review the
incumbent, or begin a repair. Report the commit SHA, files changed, and
proposition-by-proposition status to the foreman.

## Data safety

Every example is synthetic and publishable. Do not use or describe personal
source documents, real values, real identities, real dispositions, refusal
reasons, workspace locations, screenshots, or generated private output.
