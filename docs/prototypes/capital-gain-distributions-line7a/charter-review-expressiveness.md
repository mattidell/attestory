# Review Charter — Expressiveness and Recoverability

Audience: Reviewer

Date: 2026-07-28. Track 0 of Capital-Gain Distributions and Form 1040
Line 7a.

## Context Capsule

- **Source ref and resolved launch commit:** use the current local
  `prototypes/capital-gain-distributions-line7a/it2` branch and verify its
  commit at launch.
- **Exact objects:** incumbent Builder output at
  `1a7530faa68cd382f5216e2a4f1373416632a3ae` and clean-room rival Builder
  output at `099882e`; measure only their chartered `design.md` and
  `examination.md` artifacts.
- **Role:** Expressiveness Reviewer, Medium–High capability / medium effort.
- **Scope and evidence-rung ceiling:** recover P1–P3 case-by-case from both
  Rung-1 paper designs and judge whether paper distinguishes the topologies.
  Do not run a Rung-2 probe.
- **Stop conditions:** missing or mismatched objects; exposure to another
  review or foreman finding; need for governance interpretation, artifact
  mutation, a validator/evaluator probe, real data, or scope beyond P1–P3.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`; the
  topic `plan.md`; both Builder charters; both exact Builder artifact sets;
  the milestone plan's Prototype Decision Inventory, Contracts, Fixtures,
  Review Gates, and Data Safety sections; ADR-0035; ADR-0038; and the
  committed expression semantics in `packages/derivation/evaluator.py`.

## Independence boundary

Do not read:

- `docs/prototypes/capital-gain-distributions-line7a/reviews/contract-adversary.md`;
- the foreman's early incumbent check;
- either Builder's thread, summary, or uncommitted work; or
- any future triage, repair, or disposition.

If another review or finding reaches the context, stop and report the
independence breach.

Read the incumbent artifacts without switching the working branch:

```sh
git show 1a7530faa68cd382f5216e2a4f1373416632a3ae:docs/prototypes/capital-gain-distributions-line7a/it1/design.md
git show 1a7530faa68cd382f5216e2a4f1373416632a3ae:docs/prototypes/capital-gain-distributions-line7a/it1/examination.md
```

The rival artifacts are present under
`docs/prototypes/capital-gain-distributions-line7a/it2/`.

## Measurement

For each of the ten shared cases, and separately for each design, recover from
the committed artifact alone:

1. the authoritative producer;
2. why the direct route applies, blocks, or is inapplicable;
3. the exact current source set, horizon, and closure;
4. every downstream consumer through line 7a, line 9, taxable income, and
   line 16;
5. the fact, transition, or supersession that displaces the result; and
6. the exact failure or non-publication state.

Record each answer as:

- `recovered` with an exact section/case citation;
- `contradictory` with both conflicting citations; or
- `missing` without reconstructing the answer from repository knowledge.

Failure means a required answer:

- is absent or available only by inference;
- changes between equivalent cases without a stated contract reason;
- uses alternative prose such as “may,” “as applicable,” or an unspecified
  input where the result depends on that choice;
- names a publication or pin without a producer and displacement path;
- cannot distinguish blocked, closure-backed zero, and
  `guard_inapplicable`; or
- appears to require a more expensive evidence rung only because the paper
  contract is underspecified.

Then compare the two authority topologies without choosing on taste:

- Which topology is recoverable with fewer contributed facts and fewer
  conditional states?
- Which topology makes missing, contradiction, and correction states explicit
  rather than inferred?
- Does either topology fail to close P2 or P3 independently of its P1 choice?
- Does paper already distinguish the alternatives?
- Is the plan's single Rung-2 validator question still necessary, and if so,
  what exact unresolved mechanical distinction would it measure?

Do not perform contract/adversary review by proxy. Report observable
recoverability failures and proposition-level sufficiency; the foreman will
compare both committee records later.

## Output

Create exactly:

`docs/prototypes/capital-gain-distributions-line7a/reviews/expressiveness.md`

The review must contain:

- object verification and independence attestation;
- a 20-row recovery matrix: ten cases × two designs;
- exact `recovered` / `contradictory` / `missing` results for the six required
  questions;
- findings with stable IDs, proposition, citation, and recommended Gate-5
  classification;
- P1, P2, and P3 sufficiency for each design;
- the topology comparison and Rung-2 judgment; and
- a final `READY` or `NOT READY` recommendation.

Before writing, echo the exact objects, scope, Rung-1 ceiling, independence
boundary, recovery questions, and stop conditions.

## Completion

Run:

```sh
python3 tools/envelope_scan.py --range origin/main..099882e
python3 tools/envelope_scan.py --range origin/main..1a7530faa68cd382f5216e2a4f1373416632a3ae
```

Commit only the review output locally and stop. Do not edit either design,
phase state, SEAT file, charter, plan, process log, ADR, schema, test, or
production file. Do not read the other review, prepare a repair, reconcile
dissent, open a PR, push, merge, or advance the pointer. Return the review
commit SHA and verdict.

## Data safety

Use only committed synthetic paper evidence. No personal values, identifiers,
dispositions, refusal reasons, workspace locations, documents, screenshots,
or private artifacts may enter the review.
