# ADR 0089 — A per-statement question names the statement it asks about

- Status: **proposed** (owner disposition required before Track 1)
- Tier: 2. A presentation-projection contract that later content is
  written against (sibling of ADR 0087).
- Date: 2026-11-25

## Context

On core v106, the Form 1099-B box 4 amount and box 7 questions are asked
once for each statement. Each one blocks its lines through a
`require_paired` block. That block records only the bare fact type in
`missing`, never the statement. So a return with two statements shows one
unlabelled sentence on each blocked line, and the filer cannot tell which
statement it means. Content cannot name a statement, because a question is
static text and the label is the filer's. The reason shape already admits
`statementLabel` (projection validator; renderer
`citation-walk.v1.html:1459-1465`). Evidence:
`docs/phases/engine-breadth/milestones/statement-question-labels-evidence/p0.md`.

## Decision

1. **Attribution by recomputed pairing.** Suppose a blocked line's question
   walk reaches the input question of a fact type individuated on one
   `statement` entity key plus literal keys, through rows that name that
   type bare. The projection then recomputes each such row's
   `require_paired` from the current facts. The statements it asks about
   are the `key` values of current income rows that no current answer
   covers.
2. **Declared need narrows a gated pairing.** Where content gates a
   pairing and runs it over every statement (line 25b on v106), a
   tax-domain table names the per-subject results that mark the need (the
   per-sale `box4-amount-needed` results). Only statements with a
   published need above zero are named. The table is gated to the cores
   that publish those results.
3. **One reason per statement, labelled.** The one sentence is replaced,
   in place, by one reason per statement. Each carries that statement's
   recorded label as `statementLabel` `{statement, taxYear}`. Identity is
   the fact id, never the label. Two statements with the same label give
   two reasons.
4. **One pairing test, shared with the evaluator.** The projection does
   not keep its own copy of the pairing. It calls the same function the
   evaluator uses for `require_paired` (extracted to a shared helper if
   needed), so the attribution cannot drift from what blocked the line.
5. **Scope: Form 1099-B.** This decision applies to the Form 1099-B
   per-statement questions (box 4 amount and box 7). Other `statement`
   pairings (Forms 1099-INT, -DIV, -R, -G, SSA-1099) join by amendment
   after a probe shows their pages. A single statement is labelled too, as
   ADR 0087 labels a single child.
6. **Fail closed, explanation only.** A row whose pairing yields no
   statement, or a statement with no single current label, leaves today's
   unlabelled sentence. No number, disposition, code, report row, pin,
   schema or content changes. Question groups are unchanged.

## Consequences

Track 1 changes `_closure_question_reasons` and its walk frame in
`packages/derivation/presentation_projection.py`, and passes it the
published values. It adds the need table in `packages/tax`. On the
recorded corpus, 141 of 775 saved pages gain labels on the lines that show
these questions, and nothing else changes. A future per-statement question
is labelled if it blocks through `require_paired`, or through a pairing the
need table covers.

## Alternatives considered

- **The engine records keyed fact ids in `missing`.** Names box 7 exactly,
  but for box 4 it would also name statements the filer answered "no", and
  it changes report rows for every blocked pairing (a derivation
  contract).
- **A question schema successor declaring its own scope.** Works, but adds
  a published schema for what the reason field already carries.
- **Content.** A question is static text; the label is the filer's.

## Parked

Other statement pairings; the broker label beside a duplicate statement
label; per-statement question wording; naming the sale on questions for
sales without a Form 1099-B.

## Links

- Plan: `docs/phases/engine-breadth/milestones/statement-question-labels.md`
- ADR 0087 (roster member labels), ADR 0046 (presentation surface contract)
