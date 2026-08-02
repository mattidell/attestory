# Charter: Track 3 F1 Repair — Invalid Release Inventory Must Fail Closed

Date: 2026-07-18. Owner-authorized narrow continuation repair following the
author-independent Track-3 review at
`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-18-frrs-t3-resolver-bootstrap-premerge-review.md`.
Branch: `repair/frrs-t3-f1-release-inventory`. The owner holds any merge.

## Objective

Repair review finding **F1** only. A co-located JSON release document that shares
the adoption-pinned `id` and `version` but fails `release-registry.v1` validation
must never crash authority resolution. The resolver must ignore that invalid
candidate and continue to resolve the independently verified honest release; if
no honest release remains, it must return a typed `Refusal`, never leak
`SchemaValidationError`.

## Authorized change

1. In `packages/derivation/production_resolver.py`, handle the schema-validation
   failure raised while inventorying release candidates. Catch the specific
   validation exception (or an equally narrow existing validation base) alongside
   the existing malformed-document cases, then continue the inventory.
2. In `tests/test_frrs_t3_resolver_bootstrap.py`, add an **executed** regression
   golden that places an invalid, identity-matching release beside the honest
   adoption-pinned release and proves resolution returns `ResolvedGraph` without
   an exception. The test must make the invalidity explicit (for example, omit
   the required registry checksum) rather than merely use malformed JSON.

## Scope fence

- Do not alter ADRs, schemas, fixtures, fixture generation, package content, or
  the selection/registry/member algorithms.
- Do not repair F2/F4/F5/F6 or any Track-4 production condition in this change.
- No real or personal data. Do not touch the unrelated untracked Track-1 review
  record.
- One implementation commit after this charter commit. Do not merge or open the
  PR from the builder seat.

## Verification

Run and report:

- `python3 -m unittest tests.test_frrs_t3_resolver_bootstrap`
- `python3 -m unittest`
- `python3 -m mypy packages tools tests`
- `python3 tools/governance_lint.py`
- a focused data-safety scan of the repair diff

## Handoff and review

The builder reports the commit SHA, changed files, command results, and any
deviation. A fresh author-independent delta review is required before the owner
merges; it measures only this F1 repair against this charter and the review
finding. The owner has authorized dispatch for that review in this session, but
the reviewer is not authorized to merge or repair.
