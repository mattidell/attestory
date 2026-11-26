# Retrospective: The Sale Block Explanations Read Plainly

Milestone key: sale-explanation-wording. Plan:
`docs/phases/engine-breadth/milestones/sale-explanation-wording.md`.
Closed 2026-11-25. Core v107, registry v105, release v105.

## What happened

The foreman's review of ADR 0088 found its 30 sale block explanations
correct but hard to read: two clauses joined by a semicolon, a formula in
parentheses, and inverted phrases. The plan set a wording bar, and one
build track first proved that a new version of an explanation or question
unpins no saved record, then published v2 of the 30 explanations and the 8
sale adjustment questions in core v107. A full-surface replay checked the
new sentences by substitution, so a reordered reason list could not hide a
real change.

The fresh review found seven wording problems, two of them medium: the
code B sentences dropped "with the correct basis", so "this sale has no
loss" could read as false next to the form; and the covered wash-sale
question said to enter 0 for a blank box 1g, which contradicts the box 1g
explanations and would set off another block. The foreman decided the box
1g rule, first too broadly (applying "change your answer" to a case where
the filer never gave that answer) and then corrected it.

## What worked

- Checking pins before writing any successor kept the milestone to
  content.
- Substitution in the replay, with committed controls that must fail,
  made "only words moved" a checked claim.
- A fresh reviewer reading every sentence against the form caught the two
  real errors; mechanical bar tests could not.

## What to change

- When a wording decision covers several sentences, check each sentence's
  case separately. The box 1g instruction fit two cases and not the third.
- Send the reviewer's report text, not a summary, to a repair builder.
  The builder had to reconstruct three sentences from a description.
