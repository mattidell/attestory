# Retrospective: Validation Reuses Member Checksums

Milestone key: validation-checksum-reuse. Plan:
`docs/phases/engine-breadth/milestones/validation-checksum-reuse.md`.
Closed 2026-11-23. Tooling only (`packages/derivation/package_validation.py`,
`packages/derivation/production_resolver.py`); no package version change.

## What happened

The member-reads-once milestone had parked a lever: the validation memo key
and `validate_package` recomputed the canonical checksum of every corpus
body on each run, though the member cache had already computed it for the
same bytes. A Claude Opus builder measured it (about 3,192 checksums, 3.8
percent of a median list), made both reuse the cached value keyed by the
SHA-256 of the bytes read, proved all 775 recorded lists byte-identical,
and timed a 5 to 6 percent gain on the median list. It then stopped on the
account's weekly Claude limit before its final checks. A grok builder
ran them, the first grok unit since the owner's switch, and a grok
reviewer (READY with notes) reran 111 lists and four mutants.

## What worked

- Keying reuse by the bytes' own hash, so a changed byte cannot reuse a
  stale value.
- Committing evidence before final checks: the interrupted builder lost
  nothing.

## What to change

- A gain of a few percent is real but small. The larger replay levers left
  (re-projecting the act log per save; fact-lattice rebuilds) are in the
  kernel and need the owner.
