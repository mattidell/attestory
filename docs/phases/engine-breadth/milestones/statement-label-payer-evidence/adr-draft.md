# Proposed amendment to ADR 0089 — Name the payer beside a repeated statement label

Status: **proposed**. Milestone: statement-label-payer.

Two statements of the same form can have the same recorded label. The saved
page already keeps separate reasons for their unanswered questions. A
distinct recorded payer or broker label can help identify each statement,
including when its peer's question has already been answered.

## Proposed decision

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

## Consequences

The projection, its validator, the page renderer and its text observer can
carry the display field. The published presentation-model schema already
admits reason objects without constraining their fields. The runtime
validator must admit the string only beside a statement label on an
unlinked statement reason.

The cohort can remain indistinguishable when the available names repeat
or a name is missing. Ordinals and other identifying details would require
their own decision.
