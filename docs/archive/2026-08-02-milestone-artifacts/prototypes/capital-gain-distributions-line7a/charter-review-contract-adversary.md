# Review Charter — Contract and Adversary Fidelity

Audience: Reviewer

Date: 2026-07-28. Track 0 of Capital-Gain Distributions and Form 1040
Line 7a.

## Context Capsule

- **Source ref and resolved launch commit:** use the current local
  `prototypes/capital-gain-distributions-line7a/it2` branch and verify its
  commit at launch.
- **Exact objects:** incumbent Builder output at
  `1a7530faa68cd382f5216e2a4f1373416632a3ae` and clean-room rival Builder
  output at `099882e`; compare only their two chartered `design.md` and
  `examination.md` artifacts against the approved plan and accepted contracts.
- **Role:** Contract/adversary Reviewer, High capability / high effort.
- **Scope and evidence-rung ceiling:** measure P1–P3 for both designs against
  the same ten paper cases. Rung 1 inspection only; identify but do not run a
  Rung-2 probe.
- **Stop conditions:** missing or mismatched review objects; exposure to the
  other reviewer's work; need for governance interpretation; need to mutate a
  design, run a validator/evaluator probe, inspect real data, or widen beyond
  P1–P3.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`; the
  topic `plan.md`; both Builder charters; both exact Builder artifact sets;
  the milestone plan's Prototype Decision Inventory, Contracts, Fixtures,
  Review Gates, and Data Safety sections; ADR-0010; ADR-0014 through ADR-0017;
  ADR-0023; ADR-0032; ADR-0035; ADR-0036; ADR-0038;
  `packages/content/tax/2025/dividend-universe.json`;
  `packages/content/tax/2025/f1099div.bundle.json`;
  `packages/content/tax/2025/qdcg.bundle.json`;
  `packages/content/tax/2025/rule.form1040-line9.v2.json`;
  `packages/content/tax/2025/rule.form1040-line16.v2.json`;
  `packages/derivation/evaluator.py`;
  `packages/derivation/package_validation.py`;
  `packages/kernel/findings.py`; and `packages/tax/loader.py`.

## Independence boundary

Do not read the foreman's early incumbent check, either Builder's thread or
summary, any uncommitted artifact, or the expressiveness review. The committed
Builder designs and examinations are the complete review objects. If another
review reaches the context, stop and report the independence breach.

Read the incumbent artifacts without switching the working branch:

```sh
git show 1a7530faa68cd382f5216e2a4f1373416632a3ae:docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/it1/design.md
git show 1a7530faa68cd382f5216e2a4f1373416632a3ae:docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/it1/examination.md
```

The rival artifacts are present in the current tree at
`docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/it2/`.

## Measurements

Attack each design independently, then compare proposition-level sufficiency.
For every attack, cite the exact case, contract sentence, current/displaced
state, or committed mechanism that supports the result.

Failure means at least one of:

1. accepted history is edited or semantically weakened instead of extended by
   an explicit successor;
2. direct-route authority can be absent, internally inconsistent,
   contradicted, or superseded while line 7a or a dependent result remains
   current;
3. historical recorded/non-composable box 2a and its successor family can
   both become live authority or contribute to one result;
4. the capital-gain-distribution contradiction can be sequenced around in
   declaration-first, statement-first, or same-batch order;
5. a Schedule-D-required state publishes the direct route, silently substitutes
   zero, or fabricates Schedule D or an attachment;
6. line 9 counts box 2a more than once, or line 9/QDCG reaches raw statement
   content instead of the selected publication;
7. correction, removal, horizon succession, or authority supersession leaves
   a stale downstream result current;
8. a required member, closure, authority fact, parameter, citation, or
   displacement edge lacks an exact pin;
9. any mandatory shared case is alternative prose rather than one concrete,
   reproducible paper state; or
10. the design requires interpreting governance text or expanding into an
    excluded capital-gain source family to complete its claim.

Specifically test the cross-products that paper designs often hide:

- authority missing / affirmative / negative against closed, open, and stale
  box-2a families;
- Q=0 and Q-positive against missing authority and Schedule D required;
- zero-valued present box 2a against the existing presence-based contradiction
  signal;
- forward and reverse authority correction with line 7a, line 9, taxable
  income, and line 16 traced end to end; and
- mixed historical/successor package and workspace states.

Do not reward extra component facts merely for being finer grained. Measure
whether each is necessary authority, correction-safe, explicitly contributed,
and worth its stated topology cost.

## Output

Create exactly:

`docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/reviews/contract-adversary.md`

The review must contain:

- review-object verification and independence attestation;
- one attack table covering both designs and all ten shared cases;
- findings with stable IDs, proposition, evidence, and a recommended Gate-5
  classification (the foreman owns final classification);
- P1, P2, and P3 sufficiency judgments for each design;
- whether paper distinguishes the authority topologies;
- whether the plan's single Rung-2 validator question remains genuinely open;
  and
- a final `READY` or `NOT READY` recommendation without enlarging scope.

Before writing, echo the exact objects, scope, Rung-1 ceiling, independence
boundary, measurements, and stop conditions.

## Completion

Run:

```sh
python3 tools/envelope_scan.py --range origin/main..099882e
python3 tools/envelope_scan.py --range origin/main..1a7530faa68cd382f5216e2a4f1373416632a3ae
```

Commit only the review output and stop. Do not edit either design, phase state,
SEAT file, charter, plan, process log, ADR, schema, test, or production file.
Do not prepare a repair, reconcile dissent, review the other reviewer, open a
PR, push, merge, or advance the pointer. Return the review commit SHA and
verdict.

## Data safety

Use only the committed synthetic paper evidence. No personal values,
identifiers, dispositions, refusal reasons, workspace locations, documents,
screenshots, or private artifacts may enter the review.
