# Review Charter — Contract and Adversary Fidelity

Audience: Reviewer

Date: 2026-08-01. Track 0 of Covered Long-Term Gains, Schedule D Line 8a.

## Context Capsule

- **Source ref and resolved launch commit:** use the current local
  `prototypes/schedule-d-covered-ltcg-8a/it2` branch and verify its commit at
  launch.
- **Exact objects:** incumbent Builder output at
  `d4e220376cfa29785447fe8cc183355532eb168f` and clean-room rival Builder
  output at `bbecd3f` (rival tip, including the P3-S4/S6 cycle fix); compare
  only their two chartered `design.md` and `examination.md` artifacts against
  the approved plan and accepted contracts.
- **Role:** Contract/adversary Reviewer, High capability / high effort.
- **Scope and evidence-rung ceiling:** measure P1-P3 for both designs against
  the same eleven paper cases. Rung 1 inspection only; identify but do not run
  a Rung-2 probe.
- **Stop conditions:** missing or mismatched review objects; exposure to the
  other reviewer's work; need for governance interpretation; need to mutate a
  design, run a validator/evaluator probe, inspect real data, or widen beyond
  P1-P3.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`; the
  topic `plan.md`; both Builder charters (`charter-it1.md`, `charter-it2.md`);
  both exact Builder artifact sets; the milestone plan's Supported Source
  Class, Completeness Boundary, Prototype Decision Inventory, Contracts,
  Review Gates, and Data Safety sections; ADR-0010; ADR-0011; ADR-0012;
  ADR-0015; ADR-0016; ADR-0017; ADR-0023; ADR-0032; ADR-0036; ADR-0038;
  ADR-0050; `packages/content/tax/2025/rule.schedule-d-required.conclusion.json`;
  `packages/content/tax/2025/schedule-d-required.conclusion-binding.json`;
  `packages/content/tax/2025/exception1.bundle.json`;
  `packages/content/tax/2025/qdcg.bundle.json`;
  `packages/content/tax/2025/rule.form1040-line7a.json`;
  `packages/content/tax/2025/rule.form1040-line7b.json`;
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
git show d4e220376cfa29785447fe8cc183355532eb168f:docs/prototypes/schedule-d-covered-ltcg-8a/it1/design.md
git show d4e220376cfa29785447fe8cc183355532eb168f:docs/prototypes/schedule-d-covered-ltcg-8a/it1/examination.md
```

The rival artifacts are present in the current tree at
`docs/prototypes/schedule-d-covered-ltcg-8a/it2/`.

## Measurements

Attack each design independently, then compare proposition-level sufficiency.
For every attack, cite the exact case, contract sentence, current/displaced
state, or committed mechanism that supports the result.

Failure means at least one of:

1. accepted history (ADR-0036 or ADR-0050) is edited or semantically weakened
   instead of extended by an explicit successor;
2. two sales from one broker can merge, or transaction correction can
   displace an unrelated transaction's identity;
3. the completeness boundary can publish Schedule D `required-and-complete`
   while any of the nine named components is missing, absent-but-unread, or
   violated;
4. an absent completeness component becomes `"no"`/zero/false by inference
   rather than an explicit named block;
5. box-2a and Schedule D can both contribute the same gain to line 9 or QDCG,
   or either route can be reached around;
6. a non-covered, wash-sale, market-discount, ordinary, or QOF-indicated
   transaction, or one with proceeds less than basis, can enter the eligible
   family;
7. correction, removal, horizon succession, or authority supersession leaves
   a stale downstream result current;
8. a required member, closure, authority fact, parameter, citation, or
   displacement edge lacks an exact pin;
9. either design's proposed successor introduces a circular dependency (a
   publication defined in terms of a value that itself consumes that
   publication) — check this specifically against the it2 rival's revised
   P3-S4/S6 selected-preferential-base definition;
10. any mandatory shared case (4, 5, 6, 7, 9, 10, 11) is alternative prose
    rather than one concrete, reproducible paper state; or
11. the design requires interpreting governance text or expanding into an
    excluded capital-gain source family (short-term, losses, carryovers,
    Form 8949, other Schedule D sources) to complete its claim.

Specifically test the cross-products that paper designs often hide:

- box-2a present-and-nonzero against Schedule D closed-nonempty (both-gain
  case 6), and whether each design's resolution of this interaction is a
  genuine successor sentence or a silent assumption — the rival's
  examination names this a "plan-boundary tension resolved on paper"
  (P2-S5); assess whether that resolution is sound and whether the
  incumbent's design addresses the same tension explicitly or leaves it
  implicit;
- missing authority / affirmative / negative against closed, open, and stale
  eligible-family and box-2a states;
- Q=0 and Q-positive against missing completeness authority and an incomplete
  boundary;
- forward and reverse correction with line 8a, line 15, line 16, line 7a,
  line 9, taxable income, and line 16 tax traced end to end; and
- the named schema gaps in each design (the incumbent's `attachment-rule.v3`
  categorical-requirement need; the rival's production-substrate condition
  for exactly-one-producer symbol representation) — confirm each is honestly
  named as a production condition and not silently worked around on paper.

Do not reward extra component facts or extra topology complexity merely for
being finer grained. Measure whether each is necessary authority,
correction-safe, explicitly contributed, and worth its stated topology cost.

## Output

Create exactly:

`docs/prototypes/schedule-d-covered-ltcg-8a/reviews/contract-adversary.md`

The review must contain:

- review-object verification and independence attestation;
- one attack table covering both designs and all eleven shared cases;
- findings with stable IDs, proposition, evidence, and a recommended Gate-5
  classification (the foreman owns final classification);
- P1, P2, and P3 sufficiency judgments for each design;
- whether paper distinguishes the identity and completeness topologies, and
  whether P3's two rival shapes (line-16 state-partition extension vs. shared
  selected-preferential-base) are both viable or one is decision-blocking
  against the other;
- whether either design's named schema gap or Rung-2 question remains
  genuinely open; and
- a final `READY` or `NOT READY` recommendation without enlarging scope.

Before writing, echo the exact objects, scope, Rung-1 ceiling, independence
boundary, measurements, and stop conditions.

## Completion

Run:

```sh
python3 tools/envelope_scan.py --range origin/main..bbecd3f
python3 tools/envelope_scan.py --range origin/main..d4e220376cfa29785447fe8cc183355532eb168f
```

Commit only the review output and stop. Do not edit either design, phase
state, SEAT file, charter, plan, process log, ADR, schema, test, or
production file. Do not prepare a repair, reconcile dissent, review the other
reviewer, open a PR, push, merge, or advance the pointer. Return the review
commit SHA and verdict.

## Data safety

Use only the committed synthetic paper evidence. No personal values,
identifiers, dispositions, refusal reasons, workspace locations, documents,
screenshots, or private artifacts may enter the review.
