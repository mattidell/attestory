# Repair Charter 1 — Exact P3 Pin Contract and P2-S5 Adoption

Audience: Builder

Date: 2026-08-01. Track 0 of Covered Long-Term Gains, Schedule D Line 8a.

## Context Capsule

- **Source ref and resolved launch commit:** use the current local
  `prototypes/schedule-d-covered-ltcg-8a/it2` branch and verify its commit at
  launch.
- **Exact object:** a findings-only repair of the selected rival design at
  `bbecd3f3aae6777cf06e4bdbe58d91545f4faedd` (the pinned review object; note
  that the working tree has since advanced with a non-substantive grounding
  addition), bounded by `round-1-triage.md` findings CA-02 and CA-04. The
  owner selected the rival topology and adopted CA-02 on 2026-08-01.
- **Role:** Repair Builder, Medium-High capability / medium effort; resume the
  selected rival design for continuity.
- **Scope and evidence-rung ceiling:** P3's pin contract and the explicit
  statement of P2-S5 as an adopted successor sentence only. Rung 1 static
  paper evidence.
- **Stop conditions:** any need for production code, schema/content edits,
  validator/evaluator probes, governance interpretation, a fourth
  proposition, real data, or scope beyond CA-02/CA-04. Do not reopen P1. Do
  not address CA-05 or CA-06 (separate-decision prerequisites, not this
  repair's scope).
- **Full reads before acting:** this charter; `round-1-triage.md`; the topic
  `plan.md`; `charter-it2.md`; the selected `it2/design.md` and
  `it2/examination.md`; `reviews/contract-adversary.md` (CA-02 and CA-04
  specifically); ADR-0036; ADR-0050 (Decisions 1, 5, 6, 7, 8); the milestone
  plan's Completeness Boundary and Contracts sections; and the linked 2025
  Schedule D and Form 1099-B instructions.

## Assignment

Repair the selected rival topology without reopening its selection.

### CA-02 — State P2-S5 as an explicit adopted successor sentence

The repaired design must state, as a numbered successor sentence (not a
resolution folded into a worked example), that:

1. `B2` (the box-2a family) must be **closed** — closed-empty or
   closed-nonempty — for the completeness boundary to be satisfied; this
   supersedes the milestone plan's original "closed empty" wording for this
   bounded class;
2. a closed-empty `B2` contributes zero, exactly as before;
3. a closed-nonempty `B2` contributes its current subtotal exactly once, on
   Schedule D line 13, when the Schedule-D route is the current producer of
   `P`; and
4. this successor sentence does not expand the transaction source class,
   does not edit ADR-0050, and does not create a second capital-gain path
   into line 9 or QDCG.

State this alongside the existing P2 successor sentences (P2-S1 through
P2-S8), numbered so a fresh reader can cite it directly, not only as
narrative inside the case-6 worked example.

### CA-04 — Exact pin contract for the route-neutral `P` symbol

The repaired P3 design must state, as an exact successor sentence, where
ADR-0050's route-specific direct pins attach when `P` — not the direct
line-7a publication itself — is what Form 1040 line 16 consumes. At minimum,
resolve:

1. when the direct producer is current (box-2a route, checked conclusion
   `"no"`), which exact pins does `TAX16` carry — the checked conclusion,
   C1-C4, and the box-2a family/closure authority behind `P`, or some subset,
   and why;
2. when the Schedule-D producer is current, which exact pins does `TAX16`
   carry — `LD16`, the completeness-boundary authorities (`B1`-`B9`), `ATT-D`,
   or some subset, and why;
3. whether `P` itself needs a **route-tag** (which producer is current) as a
   first-class part of its publication, or whether the route is always
   recoverable from which upstream authority is current without a tag; and
4. an exact statement of ADR-0050 Decision 7's continuing branch-specific
   pin table (the four Q/L rows), rewritten in terms of `P` instead of
   `selected_line7a`, showing which of ADR-0050's original declaration/
   conclusion pins survive unchanged, which move, and which are new.

The repair may not resolve this by asserting "the same pins apply
automatically" without naming the exact pin set per branch. If the paper
evidence shows the route-neutral shape genuinely cannot state this without a
route-tag or a Rung-2 substrate question, say so exactly and name the
narrowest possible successor sentence that is true without one — do not
silently expand into CA-06's exactly-one-producer representation question,
which remains out of scope for this repair.

## Required repaired evidence

Reinstantiate only the affected evidence, with exact synthetic facts, pins,
current/displaced states, and dispositions:

1. direct-route-only case (box-2a positive, no eligible Schedule D
   transaction) with the exact `TAX16` pin set stated per CA-04's resolution;
2. Schedule-D-route-only case (eligible transaction, box-2a closed-empty)
   with the exact `TAX16` pin set stated;
3. both-gain case (shared case 6) with the exact `TAX16` pin set stated,
   showing which conclusion/declaration pins are and are not carried;
4. forward and reverse correction across the direct-to-Schedule-D and
   Schedule-D-to-direct route transitions, tracing `P`, line 7a, line 9,
   taxable income, and line 16 pins through the transition; and
5. the P2-S5 successor sentence cited as a standalone numbered item, plus a
   regression restatement of shared case 7 (box-2a closed-empty) confirming
   it is unaffected by the P2-S5 wording change.

For each repaired state, distinguish `blocked`, `guard_inapplicable`,
closure-backed zero, and published value with an exact pin list — not "the
applicable pins" or "as before."

## Outputs

Create exactly:

- `docs/prototypes/schedule-d-covered-ltcg-8a/repair1/design.md`
- `docs/prototypes/schedule-d-covered-ltcg-8a/repair1/examination.md`

`design.md` contains only the replacement/additional successor sentences,
repaired topology fragments, and concrete affected cases. It explicitly
states which selected `it2` sentences remain unchanged.

`examination.md` reports CA-02 and CA-04 separately as resolved or
unresolved, then reports P1/P2/P3 status after repair with exact citations.

Do not rewrite `it2/`, either review, the triage record, another charter,
the plan, phase state, SEAT, an ADR, a schema, a test, a production file, or
another prototype directory.

## Completion

Before writing, echo the exact repair object, CA-02/CA-04 scope, Rung-1
ceiling, outputs, official-instruction checks, and stop conditions.

Commit only the two repair outputs on the assigned branch and stop. Do not
push, merge, open a PR, draft the ADR, perform confirmation, begin
production, or advance the pointer. Return the commit SHA and CA-02/CA-04
status.

## Data safety

Every example is synthetic and publishable. No personal values, identifiers,
dispositions, refusal reasons, workspace locations, documents, screenshots,
or private artifacts may enter the repair.
