# Track 3 repair 2 — foreman inspection

- Inspected by: **Foreman**, 2026-07-29
- Object: `1889b99` — Track 3 repair 2
- Charter that was not executed:
  `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-29-entry-loop-synthetic-track3-repair-2-review.md`
- Status: **Foreman inspection, not a review verdict.** No `READY` is issued here.

## Why this exists

The chartered reviewer did not file. Its worktree was left at the charter commit
`40f6ebc` and is now prunable; no review was committed and its work is gone. Rather
than spend a fourth pass on a repair whose two findings both closed by deletion,
the foreman resolved the three questions the charter left open. Two were cheap and
decisive; one is a reading task.

This is recorded as inspection rather than as a passed gate, which is the same
distinction the Track 2a launcher verification and the Track 0 close acceptance
were held to in this milestone.

## Verification reproduces

722 passed with 3238 subtests, mypy clean on 135 source files, governance lint
conformant, envelope scan clean over `origin/main-ui..HEAD`. No content-tree,
manifest, registry, or adoption file changed in the range, so the claim that no
surface-metadata regeneration was needed is true.

## The F2 regressions bite

This was the prior review's central complaint: the fixtures wrote
`W2_BOX1_FORMAT};` where the loader seeks `\n};\n`, so every case raised at the
marker step before schema validation ran, and would have passed with that
validation deleted.

Stubbing `_entry_field_validator` to an always-valid validator in a throwaway
worktree makes **all three subcases** of
`test_loader_now_rejects_what_the_schema_rejects` fail — `missing_id_bad_version`,
`unknown_top_level_key`, and `unknown_correction_kind`. Restoring real validation
makes them pass. The tests now distinguish the behaviour they guard from an
unrelated earlier failure. **Closed.**

## The record's statements hold

The schema's title is `Entry field contract -- money fields (one discriminated
format variant)`. Its description states the boundary explicitly: the schema
validates that a declaration is well-formed and that `format` names a *supported*
variant, and does **not** verify that the declared format is the correct one for
the named `source`/`destination` — so a declaration naming an employer, a
checkbox, a date, or a filing-status choice while claiming `currency-amount` is
schema-valid, and is a false declaration rather than a malformed one. The
`format` `$def` repeats the same limitation at the point of use.

No surviving statement claims the four non-money fields are refused, uncovered, or
inexpressible. The milestone record's F1 section says the repair "did not make the
schema refuse" them. The one reference to the deleted equality test names it as
deleted. **The blocking F1 claim is gone.**

## The substitution guarantee holds, and is untested

The charter's sharpest open question: with the tautological equality check
deleted, the property it purported to enforce — that the served `format` is this
runtime's own format — rests entirely on the seam substituting exactly one
`"format": W2_BOX1_FORMAT` expression and refusing when the count is not one.

Probed directly against the real loader, with the schema present:

| Attempt | Outcome |
| --- | --- |
| Foreign currency-amount format inlined in place of the marker (zero matches) | refused, `entry-field-unavailable` |
| Two genuine `"format": W2_BOX1_FORMAT` matches | refused, `entry-field-unavailable` |
| A second bare `W2_BOX1_FORMAT` under another key | refused, `entry-field-unavailable` |
| Unchanged declaration (control) | accepted, `format.kind = "currency-amount"` |

No route was found by which a foreign `format` reaches the served
`field_contract`. Every violation attempt fails closed with the generic error and
leaks nothing. **The guarantee is real, so the deletion did not go too far.**

**Weakening finding, not blocking:** the `count != 1` guard has no test of its
own. The milestone has traded dead code for a live structural guarantee that
holds but is unguarded, so a future change to the substitution could silently
remove it. This is recorded rather than fixed; it should be closed by whoever
performs the canonical-JSON migration, which is already the point at which a real
equality constraint becomes necessary.

## Not inspected

The charter also asked for a judgement on
`test_schema_does_not_relate_format_to_source_or_destination` — a test that
asserts a limitation rather than a guarantee. The foreman's reading is that it is
honest documentation of a boundary the record now states in prose as well, and
that it would fail if a future change added the semantic link, which is the
correct behaviour for a test of this kind. That is a reading, not an independent
review, and it is the one item here a fresh reviewer would have added value on.

## Disposition

No blocking finding survives inspection. One weakening finding is recorded above.
Whether Track 3 is accepted on this inspection, or held for a fresh review pass,
is the owner's call.
