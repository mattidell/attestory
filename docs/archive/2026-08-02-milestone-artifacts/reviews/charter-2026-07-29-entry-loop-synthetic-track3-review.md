# Charter — The Entry Loop (synthetic), Track 3 review

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Under review: `23b9e1f` — 11 files, 429 insertions, 17 deletions
- Build charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-29-entry-loop-synthetic-track3.md`
- Verdict: `READY` or `NOT READY` **for Track 3 as a whole**, with numbered
  findings, separating findings that block from findings that weaken.

## What this track was for

This milestone built a synthetic W-2 entry surface and scored it twice with four
independent evaluators. The surface was never the deliverable. The deliverable is
a statement of what an entry field must **declare about itself**, so the next
fact family does not rediscover the same lessons by failing an evaluation.

So the question this review answers is not "does the code work". The verification
holds — the foreman re-ran the builder's full sequence independently and it
reproduced exactly: 718 passed with 3231 subtests, mypy clean on 135 source
files, governance lint conformant, envelope scan clean. Do not re-spend the
review on that; confirm it and move on.

The question is whether `entry-field.v1` is a **model** or a schema-shaped
restatement of the one field that already existed.

## 1. Does the contract generalise? This is the main spend.

`packages/schemas/entry/entry-field.v1.schema.json` claims to model what any
entry field must declare, generalised from W-2 Box 1. Test that claim
adversarially, because it was extracted from a sample of one.

Every object in it sets `additionalProperties: false` and requires every
property. In particular `accepted_format` requires all ten of `field`,
`hintLabel`, `errorLabel`, `examples`, `commaGrouping`, `currencySymbol`,
`currencyPrefix`, `maxFractionDigits`, `requirePositive`, and `maxValue`.

Take fields this project will plausibly need and try to declare them against the
schema **without amending it**. Suggestions, not a closed list: a 1099-INT
interest amount (another currency field — should be easy, and if it is not, that
is a serious finding); a W-2 Box 13 retirement-plan checkbox; an employer name
or EIN; a date; a filing-status choice from a fixed set.

For each, say whether it fits, and if not, what the schema would have to change.
Then form a judgement: is the correct conclusion (a) the model generalises, (b)
`accepted_format` is really a *currency*-format model that should be one variant
among several, or (c) the whole thing is premature and honestly describes one
field? **Any of those three is an acceptable answer** — the milestone's job was
to find out, and "we learned this shape only covers money" is a real result. What
is not acceptable is a schema that claims generality it does not have.

`correction.kind` is an open enum with one member, `same-field-reuse`, and the
builder flagged that explicitly as the only shape observed. Judge whether being
open-but-single is honest modelling or a placeholder.

## 2. Are criteria 2.1 and 2.2 actually checkable against declarations now?

That was the charter's stated test of the model.

`entry_loop.py` serves the declaration at `GET /api/state` under
`field_contract`, and `EntryPage.svelte` now renders the source label, field
name, and purpose sentence from the declaration instead of repeating those words
as template literals.

- Confirm the rendered text is genuinely **derived** and not merely duplicated
  next to a declaration. The whole value is that the words a person reads and the
  words in the contract cannot disagree.
- `tests/test_entry_loop_t1.py:562-585` appears to assert this by checking for
  source-level substrings such as `W2_BOX1_FIELD.source.label` and an import
  block. Judge that technique. A test that asserts the presence of a string in a
  `.svelte` file is checking that someone wrote certain characters, not that the
  page renders from the declaration. Would it catch a re-hardcoded label
  somewhere it does not look? Is there a stronger check available, and does the
  existing Chrome-driven test reach this?
- Say plainly how much of 2.1 and 2.2 an evaluator could now score from
  `field_contract` alone, and what still needs eyes on a page.
- The builder claims 2.3 stays irreducibly a judgement call on the sufficiency of
  the examples. Agree or disagree, with reasoning. This matters: 2.3 was the
  disputed criterion of the first evaluation and the owner resolved it on exactly
  this distinction.

## 3. The schema and the loader state the same rules twice

`_load_w2_box1_field` hand-validates the declaration in Python: `schema`
constant, the three `source` strings, the two `destination` strings, `purpose`,
`format` equality, and `correction`. The JSON Schema states a superset —
including `version`'s `^v[0-9]+$` pattern, `examples`' `minItems: 2`, `id`, and
`additionalProperties: false` — and is applied by `jsonschema.validate` in
`test_field_contract_validates_against_its_schema`, at test time, against the one
fixture.

**This is the same defect class this milestone already fixed once.** Track 2c/2d
existed because the accepted format was stated three times — hint, validator,
error — with no derivation between them, so a person could comply with one and be
refused by another. Ask whether the same shape has reappeared one level up: a
schema and a hand-rolled runtime validator that can drift, with only a
single-fixture test holding them together.

Determine concretely: can a declaration exist that the loader accepts and the
schema rejects, or vice versa? Construct one if you can. Then judge whether
validating against the schema at load time — rather than restating a subset in
Python — is the right answer, or whether there is a reason not to (the schema is
deliberately not wired into the kernel `SchemaRegistry`, and the builder says so
in the schema's own description; consider whether that decision is sound and
whether it is the owner's to make).

Note that all loader failures raise `entry-field-unavailable`. Confirm they fail
closed and that nothing leaks a rejected value.

## 4. The seam got wider, by acknowledged design

Track 2d read a JS `export const` from Python by string-marker. Track 3
generalises that: it now indexes a marker, regex-substitutes
`"format": W2_BOX1_FORMAT` with serialised JSON, then decodes the remainder.

The builder names this as no less brittle than before and recommends a canonical
JSON document without marker parsing, per the charter, which explicitly said not
to build the migration.

Judge two things. First, whether the recommendation is the right one and
sufficiently specific to act on. Second — and this is the reviewable part —
whether *widening* a seam the track was told to name rather than fix was
justified, or whether the model could have been expressed without deepening the
dependency on parsing one language's source from another. Probe the substitution:
what happens with a `"format"` string appearing elsewhere in the file, a nested
`};`, or a comment containing the marker.

## 5. Did it record what it was told to record?

The charter required three records and two dispositions, all as records rather
than designs. Confirm each is present in
`docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-loop-synthetic.md` (129 added lines)
and that each is honest about being an observation:

- the per-control versus per-context focus-indicator finding, and why the
  accessibility row failed twice on the same element;
- that the harness cannot measure Tab/Shift+Tab or Enter/Space, so a mechanical
  criterion went partly unverified in both rounds;
- the bundled accessibility row and the conflated "without guessing" bar;
- disposition of the duplicate/out-of-order coverage finding (it passes via the
  kernel's contribution-id refusal, so it does not prove `entry_loop.py`'s own
  staleness check does any work);
- disposition of the `launchChrome()` orphaned-process and `mkdtemp` leak.

## 6. Scope and surface metadata

The charter drew hard boundaries. Confirm the build stayed inside them: **no**
criteria-document edit, **no** accessibility fix, **no** presentation model, no
ADR drafted, no maturity movement, no second fact family, no real data, no
residency locator.

Four surface metadata files changed (adoption, manifest, release, registry) for
two new content files. Recompute independently: every manifest entry against its
byte count and SHA-256, the manifest checksum against the registry and the
adoption pin, the release registry digest, and the adoption release checksum.
Confirm the 943-entry count and that nothing outside the two new files moved.

Run the data-safety scan, then read for what a scan cannot see.

## Boundaries

- **Do not fix anything.** Report findings.
- Do not score or re-score any usability criterion. Two rounds are on record and
  the cell verdict is FAIL; nothing here revisits it.
- Do not ratify or amend ADR-0049 or ADR-0051. Both are proposed and both are the
  owner's at the milestone close.
- If you conclude the model should be an ADR, say so as a note to the owner,
  separately from the verdict. Proposing an ADR is not yours or the builder's.
- No maturity claim.

## Verdict

`READY` or `NOT READY` for Track 3 as a whole. Number each finding, say what is
wrong and what would close it, and separate blocking from weakening.

Bear in mind what a `NOT READY` would mean here. This is the milestone's last
build track; the only work after it is a narrow focus-indicator repair and the
close. A blocking finding should be something that would leave a false claim in
the record — a schema asserting generality it does not have, a criterion claimed
checkable that is not — rather than a shape you would have chosen differently.

Orient with `python3 tools/foreman_context.py --ref HEAD --format markdown` and
`python3 tools/build_orientation_block.py --ref HEAD`. If either refuses, stop
and report it; it refused for both Track 2e evaluators because the foreman wrote
an invalid `milestone_state`, and that should not recur. No `.venv`; use system
`python3`. Ratified line `origin/main-ui`.

## Report back

The verdict; each measurement; which fields you tried to declare against the
schema and which fit; whether you could construct a declaration the loader and
the schema disagree about; how much of 2.1 and 2.2 is now checkable from data;
your judgement on the seam; and the single thing most likely to be wrong that you
could not prove either way.
