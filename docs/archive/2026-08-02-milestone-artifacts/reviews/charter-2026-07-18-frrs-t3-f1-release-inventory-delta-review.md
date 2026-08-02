# Charter: Track 3 F1 Repair — Author-Independent Delta Review

Date: 2026-07-18. Owner-authorized in this session for one fresh,
author-independent reviewer. Branch: `repair/frrs-t3-f1-release-inventory`.
Review delta: `b31bc46` → `0001e74` (one implementation commit). The owner
holds merge authority. **Do not merge, repair, push, or open GitHub review
objects.**

## Purpose

Measure whether the narrow repair closes Track-3 review finding F1 without
changing resolver authority semantics or widening scope. The original review
record is
`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-18-frrs-t3-resolver-bootstrap-premerge-review.md`.

## Falsifiable checks

1. **Exception closure:** Place a schema-invalid release document sharing the
   adoption-pinned `id` and `version` alongside the honest pinned release. The
   resolver must return a `ResolvedGraph` (or a typed `Refusal` if no honest
   release exists), never leak `SchemaValidationError`.
2. **Authority preservation:** The invalid document cannot become authority;
   the honest release remains byte-pinned, and the existing forged-release and
   replaced-registry kills still fail closed.
3. **Narrowness:** Only the release-inventory handling and its executed golden
   are changed. No ADR, schema, fixture/generator, package content, F2/F4/F5/F6,
   or Track-4 work enters the delta.
4. **Verification:** Re-run the focused Track-3 suite, full suite, mypy,
   governance lint, and a data-safety scan of `b31bc46..0001e74`.

## Output

Write exactly one durable review record:

`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-18-frrs-t3-f1-release-inventory-delta-review.md`

State `merge-ready` or `not merge-ready` plainly. Classify every finding as
blocking, scope defect, production condition (with owning track), or
non-blocking. Report the command outcomes, the counter-probe, and a brief
recommendation. Do not reopen or redesign ratified ADR-0031/0032/0033.
