# Proposed amendment to ADR 0089 — Five withholding questions name their statements

Status: **proposed**

On core v109, the Form 1040 line 25b rule already uses `require_paired`
to check whether each covered statement has its own withholding answer.
Its block names the answer type. The saved page can recover the individual
statements from the current findings the blocked row read, using the same
pairing test as the evaluator.

## Proposed decision

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

## Consequences

The projection and its tax-domain eligibility can implement the amendment.
The evaluator, kernel, published schemas, and adopted content keep
their existing behavior. The saved page already renders an unlinked
statement label beside the question. The [P0 evidence](p0.md) gives the
coverage and the limits of the replay.

W-2 box 2 uses `w2-slip` on line 25a and stays outside this amendment.
If a different box does not participate in an existing pairing, this
amendment adds no question for it.
