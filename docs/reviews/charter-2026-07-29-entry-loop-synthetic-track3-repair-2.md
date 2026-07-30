# Charter — The Entry Loop (synthetic), Track 3 repair 2: delete the two false claims

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Against: `docs/reviews/2026-07-29-entry-loop-synthetic-track3-repair-review.md` (`NOT READY`)
- Prior repair: `0c9df17`
- Review gate: yes, Reviewer, scoped to this repair.

## Read this first

**Both findings close by deleting something, not by building something.** The
previous round's instinct was to add machinery — a discriminator, a validator, an
equality check — and the review found that two of those additions assert things
that are not true. Do not add a third layer. The work here is to make the record
say what the code actually does.

The review confirmed a great deal holds: the runtime order is right, the
hand-rolled checks are genuinely gone, all three F2 refusals really do happen,
missing and corrupt schema files fail closed, nothing leaks, the schema is
reachable on every supported runtime path, the derivation test demonstrably
bites, the metadata chain recomputes to the byte, and Track 2d's format
regressions still pass. None of that needs revisiting.

## F1 — the schema does not refuse the four non-money fields, and the record says it does

The discriminator is real: `format.oneOf` has one `currency_amount_format`
branch, an unknown `kind` is rejected, and adding a second branch later would be
additive rather than breaking. The narrowed title and description are honest. The
reviewer confirmed all of that.

What does not hold is the milestone record's claim that the four non-money fields
are uncovered. The reviewer constructed all five candidate declarations — 1099-INT
amount, W-2 Box 13 checkbox, employer name/EIN, date, filing-status choice — and
**all five validated**, because each was accepted while carrying the ten-key
`currency-amount` object. The schema relates nothing about `source` or
`destination` to `format.kind`, so it cannot tell an employer-name field that
falsely claims a dollar format from a genuine money field.

**Close this by deleting the claim, not by building a semantic discriminator.**

There is no evidence for a value-type taxonomy. One money field cannot tell us
what a checkbox, a date, or a bounded choice needs to declare, and inventing that
relationship now is the same premature generalisation the owner already declined
twice in this milestone — once for the presentation model, once for the format
variants. A third invention would not be better founded than the first two.

State the boundary precisely instead, and draw the distinction the review's
wording invites:

- `entry-field.v1` validates that a declaration is **well-formed** and that its
  format is a **supported variant**. Today the only supported variant is a
  currency amount, so every valid declaration is shaped like a money field.
- It does **not** verify that the declared format is the *correct* format for the
  named source. A declaration that names an employer and claims a currency format
  is a false declaration, not a malformed one, and no schema of this kind catches
  a lie about its own subject.
- Say what does catch that, if anything does. Be honest if the answer is
  "evaluation, or nothing yet."

Then correct the milestone record wherever it says the four fields are uncovered
or refused. The true statement is narrower: the schema supports one format
variant, so a non-money field has no honest format to declare — while noting that
nothing stops a declaration from dishonestly carrying the money one.

## F2 — the regression tests are vacuous, and the equality check cannot be false

Two separate defects behind one finding. Both are real; the foreman reproduced
both.

**The fixtures never reach validation.** `_write_field_declaration` writes
`..., "format": W2_BOX1_FORMAT};\n`, and the loader looks for `"\n};\n"`. So
every one of these tests raises `entry-field-unavailable` at the marker step,
before schema validation runs at all — and would still pass with schema
validation deleted entirely. They also write no schema at the temporary root,
which is a second independent way to pass for the wrong reason.

Fix the fixtures so they are **parser-valid and schema-present**, then confirm
each test fails when schema validation is removed. A regression that cannot
distinguish the behaviour it guards from an unrelated earlier failure is not
coverage. Say in your report how you confirmed each one now bites.

**The equality check is a tautology.** `_load_w2_box1_field` substitutes the
caller-supplied `format_spec` into the declaration's `"format": W2_BOX1_FORMAT`
expression, then compares the resulting value to that same `format_spec`. It is
necessarily equal on every parseable declaration. A literally different format
fails earlier at the regex-count guard, for a parsing reason rather than the
documented runtime reason.

**Delete the check and the claim.** Do not contrive a code path that makes it
false. The right observation to record is the interesting one: the substitution
seam *structurally guarantees* the property the check was trying to verify, which
is why the check can never fire. That guarantee is a property of the seam, and it
disappears the moment the seam becomes a canonical JSON document — at which point
a real equality constraint becomes both meaningful and necessary. Record that as
a condition attached to the existing seam recommendation, so whoever performs the
migration knows they are removing an implicit guarantee.

If deleting it turns out to leave some genuinely non-tautological residue —
something the check catches that nothing else does — keep exactly that residue,
show why it can be false, and test it. Report either way.

## Boundaries

- **Subtract.** No new schema keywords, no semantic discriminator, no new
  validation layer, no new abstraction. If you find yourself adding a concept,
  stop and report instead.
- Do not undo anything the review confirmed holds. In particular leave the
  `oneOf` discriminator, the load-time schema validation, the deletion of the
  hand-rolled checks, and the F3 derivation test alone.
- Do not widen the marker-and-regex seam. Do not build the canonical-JSON
  migration; it stays a recommendation.
- **Do not amend the criteria document.** Two evaluation rounds rest on it.
- **Do not fix the accessibility defect.** Separate unit, not yet ordered.
- Do not score or re-score. The cell verdict is FAIL and stays FAIL.
- Do not draft an ADR. Both ADR-0049 and ADR-0051 are the owner's at the close.
- No maturity movement, no second fact family, W-2 and synthetic only, no real
  data, no residency locator.

## Verification

The CI `verify` sequence, or a stated subset with each omission justified, plus
the data-safety scan and the commit you worked from — **in the commit message.**
The last two rounds recorded this properly and both reproduced exactly when
re-run independently; hold that standard.

Because this round is about tests that did not test what they claimed, your report
carries a specific burden: **for each regression you touch, say how you proved it
fails when the behaviour it guards is broken.** Assertions that it "now exercises
the real path" are what the last round said.

Orient with `python3 tools/foreman_context.py --ref HEAD --format markdown` and
`python3 tools/build_orientation_block.py --ref HEAD`. If either refuses, stop and
report it. No `.venv`; use system `python3`. Ratified line `origin/main-ui`.

## Report back

What the schema's stated boundary now is, and every place in the record you
corrected to match it; how you proved each F2 regression now bites; what happened
when you deleted the equality check, and whether any non-tautological residue
survived; the condition you attached to the seam recommendation; and anything you
were tempted to add and did not.
