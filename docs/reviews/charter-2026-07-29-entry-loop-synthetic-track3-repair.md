# Charter — The Entry Loop (synthetic), Track 3 repair: make the contract honest

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Against: `docs/reviews/2026-07-29-entry-loop-synthetic-track3-review.md` (`NOT READY`)
- Review gate: yes, Reviewer, scoped to the repair.

## What the review found

Track 3's build is good work and the review says so: the extraction from W-2 Box
1 is useful, the evaluation record is complete, the surface genuinely renders from
the declaration, the metadata chain and data-safety checks are clean, and every
loader failure path fails closed with nothing leaked.

Two things make the record claim more than the code delivers, and both block.

## F1 — the schema claims to model any entry field, and can only model money

The reviewer tried to declare five plausible fields against `entry-field.v1`
without amending it. One fits: a 1099-INT interest amount. Four cannot — a W-2
Box 13 checkbox, an employer name or EIN, a date, and a filing-status choice.
Each of those can be made *schema-valid* only by carrying the irrelevant ten-key
currency object along, which is a syntactic escape rather than a declaration of
the field's accepted format.

`accepted_format` requires `currencySymbol`, `currencyPrefix`, `commaGrouping`,
`maxFractionDigits`, `requirePositive`, and `maxValue`, all of them, with
`additionalProperties: false`. It is a currency-format model wearing a generic
title.

**The fix is to narrow the claim, not to widen the schema.** Do not invent
format variants for dates, choices, booleans, or identifiers. There is no
evidence for their shape, and the owner has already ruled on exactly this
question once in this milestone: the presentation model was deferred because
generalising from a single example is inventing structure rather than extracting
it. The same reasoning governs here.

Concretely:

1. Introduce an explicit format **discriminator**, carrying exactly one variant:
   the currency shape, as built and as evaluated. The point of the discriminator
   is that a second variant becomes an addition rather than a breaking change,
   and that a reader can see the shape is one of a kind rather than the kind.
2. Make the schema's `title` and `description` say what it actually covers today
   — the money-field shape, extracted from W-2 Box 1 — and what it does not.
   Do not retain a generic title over a currency-only requirement.
3. Fix `correction.kind`. The prose calls it an open enum; `{"enum":
   ["same-field-reuse"]}` is closed. One observed member is honest. Calling a
   closed provisional shape open is not. Either make the JSON Schema match the
   prose, or make the prose match the schema — and say which observed evidence
   supports it.

Keep the shared core — `source`, `destination`, `purpose`, `correction` — as it
is. The reviewer's residual uncertainty is that this core may not survive a
non-money family, and that is genuinely unknown from one field. Do not
pre-emptively restructure it on speculation; record the uncertainty if it is not
already recorded.

## F2 — the loader accepts declarations the schema rejects

`field_contract` is served as an `entry-field.v1` instance, but nothing
guarantees it is one at runtime. The schema is applied only by a test, against a
single fixture.

The reviewer demonstrated the gap in both directions. A declaration omitting `id`
with `version` set to `not-a-version` was accepted by `_load_w2_box1_field` and
rejected by `jsonschema.validate`; the loader also accepts unknown top-level keys
the schema forbids. Conversely, a schema-valid declaration with a different but
valid accepted format was refused by the loader, because the loader demands
bytewise data equality with the separate W-2 format declaration.

**This is the defect this milestone already fixed once, one level up.** Tracks 2c
and 2d existed because the accepted format was stated three times with no
derivation between the statements, so a person could satisfy one and be refused
by another. A JSON Schema plus a hand-rolled Python subset of the same rules is
that shape again.

Close it the way the reviewer describes:

1. Validate the parsed declaration against `entry-field.v1` at load time, and
   delete the hand-rolled restatement of rules the schema already states.
2. Keep the W-2-specific format-equality constraint, but apply it **separately
   and explicitly**, as a constraint of this runtime rather than of the schema.
   The reviewer judged that constraint sensible; it is only the conflation that
   is wrong.
3. Keep failing closed. Every failure path still raises
   `entry-format-unavailable` or `entry-field-unavailable` and still leaks
   nothing — no rejected declaration, no rejected value, in any message or log.
   The review confirmed this holds today; it must still hold.

`jsonschema>=4.0` is already a declared runtime dependency in
`requirements.txt`, and `packages/kernel/facts.py`, `schema_registry.py`, and
`findings.py` already import it at module level. Use it directly. Do not build a
fallback path for its absence and do not add a dependency.

Leaving this schema outside the kernel `SchemaRegistry` remains right: it
validates no act, fact, or finding. That is not a licence to restate its rules in
Python.

## F3 — prove the rendered derivation, if you can do it cleanly

This is a weakening finding, not a block, but it is the central claim of the
track and it is worth spending on.

`EntryPage.svelte` does render all three visible pieces from the declaration —
the reviewer confirmed that by inspection. The *test* only searches for source
strings, so it would pass if someone added a hardcoded label while the required
expressions survived elsewhere in the file.

The reviewer's suggested close: a compiled or browser test that changes a fixture
declaration to distinct synthetic text and asserts the corresponding DOM text.
That is the right test — it proves derivation rather than the presence of
characters.

Attempt it. If the existing Chrome-driven path makes it awkward, or if it can
only be written in a way that skips on the machine of record, **stop and report
rather than landing a test that does not run.** A skipped test is not coverage,
and this milestone already carries several. Say what you tried.

## F4 — do not widen the seam further

The seam recommendation is recorded and the reviewer agrees it is right:
canonical JSON for the field and its accepted format, parsed directly by both
sides, no marker parsing. The migration is explicitly **not** in scope.

But do not extend the marker-and-regex convention any further while fixing F1 and
F2. If validating at load time lets you reduce the parsing rather than add to it,
take that; if it does not, leave the seam exactly as brittle as it is and let the
recommendation stand.

## Boundaries

- F1 and F2 close the verdict. F3 is best-effort with a report. F4 is a
  restriction, not a task.
- **Do not amend the criteria document.** Two evaluation rounds rest on it.
- **Do not fix the accessibility defect.** The amount input's focus indicator is a
  separate unit and the owner has not yet ordered it.
- Do not score or re-score anything. The cell verdict is FAIL and stays FAIL.
- Do not draft an ADR. If you conclude the contract should become one, say so and
  stop — that is the owner's at the milestone close, and ADR-0049 and ADR-0051 are
  already waiting there.
- No maturity movement. No second fact family. W-2 and synthetic throughout, no
  real data, no residency locator.

## Verification

The CI `verify` sequence, or a stated subset with each omission justified, plus
the data-safety scan and the commit you worked from — **in the commit message.**
Track 3's build recorded this properly and it reproduced exactly when re-run
independently; hold that standard.

Because you are changing a schema and a load path, say explicitly in your report
which previously-accepted declarations are now refused, and confirm the served
`field_contract` still validates against the amended schema.

Orient with `python3 tools/foreman_context.py --ref HEAD --format markdown` and
`python3 tools/build_orientation_block.py --ref HEAD`. If either refuses, stop and
report it. No `.venv`; use system `python3`. Ratified line `origin/main-ui`.

## Report back

What the discriminator looks like and what the schema now claims to cover; how
`correction.kind` was resolved and on what evidence; the declarations the loader
and the schema now agree and disagree about, if any remain; whether you got the
rendered-derivation test and what it asserts; and whether anything in F1 or F2
turned out to need an owner decision you were not authorised to make.
