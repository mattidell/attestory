# Charter — The Entry Loop (synthetic), Track 3 repair 2 review

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Under review: `1889b99` — 4 files, 194 insertions, 63 deletions
- Repair charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-29-entry-loop-synthetic-track3-repair-2.md`
- Prior review: `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-29-entry-loop-synthetic-track3-repair-review.md` (`NOT READY`, F1 and F2 blocking)
- Verdict: `READY` or `NOT READY` **for Track 3 as a whole**.

This is the milestone's last build gate, on its third pass. Both prior findings
were to be closed by **deletion**, and the diff is net-subtractive in the places
that matter. Keep the review proportionate to that.

## Already verified by the foreman — confirm, do not re-derive

- Full verification reproduced at this commit: 722 passed with 3238 subtests,
  mypy clean on 135 source files, governance lint conformant, envelope scan clean
  over `origin/main-ui..HEAD`.
- No content-tree, manifest, registry, or adoption file changed in this range, so
  the claim that no surface-metadata regeneration was needed is true. You do not
  need to recompute the 943-entry chain again.
- **The F2 regressions now bite.** The foreman independently stubbed
  `_entry_field_validator` to an always-valid validator in a throwaway worktree
  and confirmed all three subcases of
  `test_loader_now_rejects_what_the_schema_rejects` fail without real schema
  validation. That was the prior review's central complaint and it is closed.

So do not re-spend on those. Three things remain genuinely open.

## 1. Does the record now say only true things?

F1 closed by correcting a claim rather than changing behaviour, so this review is
mostly a reading task — and the reading is the finding.

The true statement is meant to be: `entry-field.v1` checks that a declaration is
well-formed and that `format` names a supported variant; it does **not** check
that the variant is correct for the field's own subject. A declaration naming an
employer while carrying a currency format is *false*, not *malformed*, and
nothing in this milestone catches that.

- Read the schema's `title`, `description`, and `format` `$def`, and the
  milestone record's F1 section. Does every statement hold? Specifically: is
  there anywhere left claiming or implying that the four non-money fields are
  **refused**, **uncovered**, or **not expressible**? That claim was the blocking
  finding; a surviving instance anywhere in the record reinstates it.
- `test_schema_does_not_relate_format_to_source_or_destination` is a test that
  asserts a limitation rather than a guarantee. Judge that. Is it honest
  documentation of a real boundary, or does it entrench a defect by making it a
  passing expectation? Say which, and whether the test would notice if a future
  change *did* add the semantic link.
- The charter forbade adding a semantic discriminator, new schema keywords, or a
  new validation layer. Confirm none appeared.

## 2. What now guarantees the property the deleted check asserted?

This is the sharpest thing left, and it is the one the prior review could not
have raised because the check still existed.

The format-equality check was correctly identified as a tautology and deleted.
But the *property* it purported to enforce — that the format the runtime serves
is the runtime's own format — still matters. It now rests entirely on the
substitution seam: the loader replaces exactly one `"format": W2_BOX1_FORMAT`
expression with the already-parsed spec, and refuses when the count is not one.

So the milestone may have traded a tautological check for an **untested
structural guarantee**. Determine:

- Is the `count != 1` guard itself covered by a test that bites? Try zero
  occurrences and two occurrences.
- Can a declaration reach the served `field_contract` carrying a `format` that is
  not this runtime's format — by any route, including a `"format"` key appearing
  in an unexpected position, a nested structure, or a comment? If you find one,
  that is a blocking finding and the deletion went too far.
- If the guarantee holds but is untested, say whether that is acceptable or a
  weakening finding. Deleting dead code is right; leaving the live guarantee
  unguarded may not be.

## 3. Did the deletions remove any real coverage?

Subtractive changes are the ones that quietly lose things.

- A test was deleted along with the equality check. Confirm nothing it covered is
  now uncovered, and that its deletion is recorded rather than silent.
- Confirm the things the prior review verified as holding are untouched and still
  hold: the `oneOf` discriminator and its rejection of an unknown `kind`,
  load-time schema validation, the absence of the hand-rolled checks, the F3
  derivation test, the fail-closed generic-error behaviour with nothing leaked,
  and Track 2d's format regressions.
- `_write_field_declaration` now copies the real schema into the temporary root.
  Check that this cannot mask a genuine schema-availability failure — the prior
  round's fixtures passed for the wrong reason twice, and a fixture that supplies
  its own schema is a plausible third way.
- Confirm the seam condition is recorded: that the marker-and-regex seam
  structurally guarantees the deleted check's property today, and that the
  guarantee disappears under the canonical-JSON migration, at which point a real
  equality constraint becomes necessary. Judge whether that is stated clearly
  enough for whoever performs the migration to act on.

## Boundaries

- **Do not fix anything.** Report findings.
- Do not score or re-score. The cell verdict is FAIL and stays FAIL.
- Do not amend the criteria document.
- Do not ratify or amend ADR-0049 or ADR-0051; both are the owner's at the close.
- No maturity claim.

## Verdict

`READY` or `NOT READY` for Track 3 as a whole.

Be deliberate about the bar, because this is the third pass and the two prior
rejections were both correct. A blocking finding is a **false claim left in the
record** or a **live guarantee that can be violated** — not a shape you would have
chosen, not a test you would have written differently, and not the acknowledged
limitation that this contract is extracted from one money field. That limitation
is the honest result of the milestone and is recorded as such.

If F1 and F2 are closed, say so plainly and let the milestone move to its close.
If something is still false, name it precisely and say what deletion or
correction closes it.

Orient with `python3 tools/foreman_context.py --ref HEAD --format markdown` and
`python3 tools/build_orientation_block.py --ref HEAD`. If either refuses, stop and
report it. No `.venv`; use system `python3`. Ratified line `origin/main-ui`.

## Report back

The verdict; whether any statement in the record still overclaims and where; your
judgement on a test that asserts a limitation; what guards the substitution
guarantee now that the equality check is gone, and whether you could violate it;
whether any coverage was lost with the deleted test; and the single thing most
likely to be wrong that you could not prove either way.
