# Retrospective: Member Files Are Read Once (2025)

Milestone key: member-reads-once. Plan:
`docs/phases/engine-breadth/milestones/member-reads-once.md`.
Closed 2026-11-18. No package version change. One cache in
`packages/derivation/production_resolver.py` and its consumers; no
kernel, content or schema change.

## What happened

The rust-kernel-experiment re-profile named the largest remaining cost:
every recorded list read, parsed and checksummed all 1,813 member files
four times. The plan skipped P0 and Track 0, since that evidence already
located the cost and the change had a byte-identical contract rather
than rival designs. Decision 1 ruled out a key on path, size or
modification time alone.

A Claude Sonnet builder counted the reads, built a cache keyed on the
SHA-256 of the bytes read (an LRU of 4,096 entries with read-only views
and private copies), proved all 775 lists byte-identical and measured
the byte key against a stat key: the stat key would save about 0.29 s
more per list but serves a stale parse when an edit keeps size and
modification time. A fresh Claude Opus review found the code correct and
the evidence overstated: before and after had been timed at different
times under load. Its paired run gave -21 % cold and -24 % warm instead
of -37 % and -43 %. It also showed the new tests would pass a checksum
cached per id; the foreman added a test that edits a non-id field and
checked that it kills that mutant.

## What worked

- Skipping P0 when the previous milestone's evidence already named the
  cost by file and line.
- The reviewer mutating the cache in a separate process to see which
  tests notice, rather than reading the tests and trusting them.

## What to change

- Timing on a shared, loaded machine must be paired and interleaved in
  one process, or the ratios are noise. Charter that in the next speed
  milestone.
