# ADR 0089 — A per-statement question names the statement it asks about

- Status: **accepted** (owner, 2026-11-26, before Track 1)
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

## Amendment (2026-11-27) — Five withholding questions name their statements

Status: **accepted** (owner, 2026-11-27, before Track 1). Milestone:
statement-labels-forms.

On core v109, the Form 1040 line 25b rule already uses `require_paired`
to check whether each covered statement has its own withholding answer.
Its block names the answer type. The saved page can recover the individual
statements from the current findings the blocked row read, using the same
pairing test as the evaluator.

1. Extend Decision 5 to the five adopted line 25b withholding questions:
   box 4 for Forms 1099-INT, 1099-DIV, IRA-family 1099-R and 1099-G, and
   box 6 for Form SSA-1099. Label a single statement as well. Limit the
   extension to these five fact types on core-calculations v109 and later
   cores that retain the same pairing and identity contracts. The Form
   1099-B path keeps its existing eligibility, version gate and need table.
2. For these questions, extend Decision 1 to admit the exact answer
   identity of each form. SSA-1099 uses `statement` and literal `tax-year`.
   The other four also carry a `payer` entity. Use the rule's `statement`
   key for matching and the complete declared answer key for identity.
   Recover that key only when the input findings the row read yield a
   single complete identity per uncovered statement.
3. Apply Decisions 2 through 4 to these five pairings. The existing
   withholding-family and income-family closure gates decide whether a
   pairing runs. Every income row in a pairing that runs needs coverage,
   so these five have no per-statement need-table entry. For an unlinked
   generic reason, use one reason per uncovered answer identity in its
   place. When the reason carries a question link, retain that reason and
   put the display-only reasons immediately after it. Sort those reasons
   by recorded statement label and then full answer fact id.
   Include `statementLabel` with the recorded `statement` and `taxYear`.
   Keep a separate reason for each identity when labels are identical.
4. Apply Decision 6. Keep the existing sentence whenever the walk cannot
   attribute the question to the paired row, an identity is missing or
   ambiguous, or one of the targeted statements lacks a current label.
   Use the labels for display only. Preserve question wording, groups,
   answer targets, and the meaning of existing references, including when
   their reason indices move after a split. Keep the same report rows,
   pins, dispositions, block codes and amounts.

The projection and its tax-domain eligibility can implement the amendment.
The evaluator, kernel, published schemas, and adopted content keep
their existing behavior. The saved page already renders an unlinked
statement label beside the question. The P0 evidence (`docs/phases/engine-breadth/milestones/statement-labels-forms-evidence/p0.md`) gives the
coverage and the limits of the replay.

W-2 box 2 uses `w2-slip` on line 25a and stays outside this amendment.
If a different box does not participate in an existing pairing, this
amendment adds no question for it.

## Amendment (2026-11-27, second) — A repeated statement label names its payer

Status: **accepted** (owner, 2026-11-27, before Track 1). Milestone:
statement-label-payer.

Two statements of the same form can have the same recorded label. The saved
page already keeps separate reasons for their unanswered questions. A
distinct recorded payer or broker label can help identify each statement,
including when its peer's question has already been answered.

1. On core-calculations v109, add the optional display-only string
   `statementPayerLabel` to reasons already attributed under ADR 0089
   for Form 1099-B box 4 amount and box 7 and Forms 1099-INT, 1099-DIV,
   IRA-family 1099-R and 1099-G box 4. Extend eligibility to later cores
   when they retain the same source and attribution contracts.
2. Compare the exact recorded statement labels of distinct current
   statements of the same form and tax year. Include a statement when a
   current income finding records it. For Form 1099-B, a current sale
   or statement anchor records it. A statement with a recorded answer
   still participates. Case and spacing differences in statement labels
   keep them distinct.
3. For the four payer-keyed forms, take the payer from the existing
   attributed answer identity. For Form 1099-B, take the broker from the
   matching current sale findings read by the originating pairing block.
   All contributing rows must identify the same broker for that statement
   and year. Use the current entity's recorded label and require a match
   with the party identified by the cohort's source findings.
4. Add the name only when every statement in the repeated-label group
   identifies one current party of the expected kind with a nonblank
   recorded label, and the party labels are pairwise distinct after
   case folding and collapsing whitespace. Display the recorded spelling
   and spacing. A missing, stale, conflicting, equal or near-equal party
   name leaves the group's existing statement labels. SSA-1099 keeps
   its statement labels because its answer identity has no payer.
5. The page renders the prefix as “statement label, payer or broker
   label” followed by the existing question. The reason stays display-only.
   Preserve the reason order, question wording, question groups and
   references, answer identities, calculations, report rows, dispositions,
   block codes and pins.

The projection, its validator, the page renderer and its text observer can
carry the display field. The published presentation-model schema already
admits reason objects without constraining their fields. The runtime
validator must admit the string only beside a statement label on an
unlinked statement reason.

The cohort can remain indistinguishable when the available names repeat
or a name is missing. Ordinals and other identifying details would require
their own decision.

## Parked

Other statement pairings; per-statement question wording; naming the sale on questions for
sales without a Form 1099-B.

## Links

- Plan: `docs/phases/engine-breadth/milestones/statement-question-labels.md`
- Amendment plan: `docs/phases/engine-breadth/milestones/statement-labels-forms.md`
- Second amendment plan: `docs/phases/engine-breadth/milestones/statement-label-payer.md`
- ADR 0087 (roster member labels), ADR 0046 (presentation surface contract)
