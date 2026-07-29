# Repair Charter 1 — Complete Component Authority and QDCG Handoff

Audience: Builder

Date: 2026-07-28. Track 0 of Capital-Gain Distributions and Form 1040
Line 7a.

## Context Capsule

- **Source ref and resolved launch commit:** use the current local
  `prototypes/capital-gain-distributions-line7a/it2` branch and verify its
  commit at launch.
- **Exact object:** a findings-only repair of the selected component-backed
  design at `099882e`, bounded by `round-1-triage.md` findings T-F1 and T-F2.
- **Role:** Repair Builder, Medium–High capability / medium effort; resume the
  selected rival design for continuity.
- **Scope and evidence-rung ceiling:** P1 authority completeness and P3 QDCG
  activation only. Rung 1 static paper evidence.
- **Stop conditions:** any need for production code, schema/content edits,
  validator/evaluator probes, governance interpretation, Schedule D
  implementation, boxes 2b/2c/2d source-family implementation, a fourth
  proposition, real data, or scope beyond T-F1/T-F2.
- **Full reads before acting:** this charter; `round-1-triage.md`; the topic
  `plan.md`; `charter-it2.md`; the selected `it2/design.md` and
  `it2/examination.md`; ADR-0010; ADR-0032; ADR-0035; ADR-0037; ADR-0038;
  the milestone plan's Contracts, Fixtures, and Data Safety sections; the
  linked official 2025 Form 1040 instructions for line 7a, line 7b, line 16,
  and the Qualified Dividends and Capital Gain Tax Worksheet; and
  `packages/content/tax/2025/rule.form1040-line16.v2.json`.

## Assignment

Repair the selected component-backed topology without reopening its selection.

### T-F1 — Complete Exception-1 component authority

The repaired authority must explicitly establish every condition in 2025 Form
1040 Exception 1:

1. no capital-gain deferral through a qualified opportunity fund;
2. no capital losses;
3. only capital gains are Form 1099-DIV box-2a capital-gain distributions; and
4. no Form 1099-DIV or substitute statement has an amount in box 2b, 2c, or
   2d.

Choose the smallest explicit contributed categorical assertion shape for item
4. It may be one return-level assertion covering the three named boxes or a
smaller justified component set, but it must:

- use `{yes, no}`, no default, and presence-before-value;
- be independently correctable and pinned;
- name missing authority exactly;
- avoid pretending the excluded boxes have implemented source families; and
- remain distinct from the box-2a family closure claim.

Update predicate E, the checked Schedule-D-required conclusion, topology cost,
successor sentences, maps, and correction behavior accordingly.

### T-F2 — Correct the QDCG selection and binding

The repaired line-16 successor must:

- select the QDCG worksheet when qualified dividends are positive **or**
  direct-route line 7a is positive;
- when Schedule D is not filed, bind the worksheet's capital-gain input to the
  selected line-7a publication, corresponding to worksheet line 3;
- apply the preferential computation when Q=0 and line 7a is positive;
- preserve the ordinary-tax reduction only when both Q=0 and line 7a=0;
- never default a blocked or inapplicable line-7a path to zero;
- never read raw box-2a members or historical recorded content; and
- preserve honest non-publication when component authority is missing or any
  component makes Schedule D required.

Use a declared conditional structure whose result does not depend on incidental
`all`/`any` operand ordering.

## Required repaired evidence

Reinstantiate only the affected evidence, with exact synthetic facts, pins,
current/displaced states, and dispositions:

1. eligible single payer with every repaired component current;
2. authority missing specifically for the new boxes-2b/2c/2d condition;
3. that condition current `"no"` so Schedule D is required and no direct route
   publishes;
4. forward and reverse supersession of that component, tracing line 7a, line 9,
   taxable income, and line 16;
5. Q=0 with positive line 7a, showing the QDCG worksheet and preferential
   capital-gain input;
6. Q>0 with line 7a=0, preserving the qualified-dividend worksheet path;
7. Q=0 with closed-empty line 7a=0, preserving ordinary reduction; and
8. regression statements for P2 mixed-graph exclusivity, the non-null box-2a
   presence signal, and no raw downstream reads.

For each repaired state, distinguish `blocked`, `guard_inapplicable`,
closure-backed zero, and published value. Alternative prose such as “may,” “as
applicable,” or an unspecified Q/input state is not evidence.

## Outputs

Create exactly:

- `docs/prototypes/capital-gain-distributions-line7a/repair1/design.md`
- `docs/prototypes/capital-gain-distributions-line7a/repair1/examination.md`

`design.md` contains only the replacement/additional successor sentences,
repaired topology fragments, and concrete affected cases. It explicitly states
which selected it2 sentences remain unchanged.

`examination.md` reports T-F1 and T-F2 separately as resolved or unresolved,
then reports P1/P2/P3 status after repair with exact citations.

Do not rewrite `it2/`, either review, triage, charter, plan, phase state, SEAT,
ADR, schema, test, production file, or another prototype directory.

## Completion

Before writing, echo the exact repair object, T-F1/T-F2 scope, Rung-1 ceiling,
outputs, official-instruction checks, and stop conditions.

Commit only the two repair outputs locally and stop. Do not push, merge, open a
PR, draft the ADR, perform confirmation, begin production, or advance the
pointer. Return the commit SHA and T-F1/T-F2 status.

## Data safety

Every example is synthetic and publishable. No personal values, identifiers,
dispositions, refusal reasons, workspace locations, documents, screenshots,
or private artifacts may enter the repair.
