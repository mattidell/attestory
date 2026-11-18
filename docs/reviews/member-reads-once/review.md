# Review: member files are read once

Reviewer: fresh context, author-independent. Charter:
`docs/reviews/member-reads-once/charter-review.md`. Object: `github/main..HEAD`
at `08bfd9e5` (code in `84d4ce70` and `280bd36e`; the rest is plan, charters
and evidence). Base is current: 0 behind, 7 ahead of `github/main`. PR #286 is
open as a draft at this head.

## Verdict

**READY with notes.** The semantics hold: no caller can get a parse or a
checksum for bytes it did not read in that call, no caller can reach the shared
parse through anything it is given, and all 775 recorded lists replay
byte-identically (I reran this). The findings below are about evidence and
gates, not behaviour.

Gate state at this head, recorded as measured: `verify` (the only required
check) has not run, because the PR is a draft. The non-required `quick` lane is
red on a fast-lane budget overrun that the cache does not cause (MRO-R1). This
review does not stand in for a green `verify` on the exact head.

## Findings

**MRO-R1 (Low, publication gate).** `quick` is red at `08bfd9e5`:
`tests/test_market_discount_interest_contracts.py:161`
`test_md_n6_missing_closure_read_ref_or_pin_rejects` took 3.1 s against the
3.0 s fast-lane budget (1 failed, 1864 passed; the run took 61 s, while the last
`main` fast lane took 44 s). That test builds its corpus with its own `_load`
and calls `validate_package` directly, so it never touches
`_member_candidates`. One way the cache could still slow it is cyclic-GC
traversal of a full cache in the same worker. I measured that in-process: with
the cache empty and then holding 2,291 entries, the test took 0.868 s and
0.888 s on Python 3.13 (the CI version), and 0.595 s and 0.614 s on 3.14.
That is about a 2 % difference. Consequence: the head has no green
fast lane, and `verify` has not run. Repair: no code change is indicated.
Re-trigger CI. If the overrun recurs, make the test faster or make it an
honest integration test, as `AGENTS.md` requires. Do not raise the budget.

**MRO-R2 (Low, evidence).** The timing ratios are not paired, so they overstate
the saving. `track1.md:147` reports a single-process median of 3.37 s before,
2.12 s cold (-37 %) and 1.92 s warm (-43 %). The before figure came from a
separate export run at a different time under load 12 to 13. The `timing-*.json`
files (`track1.md:138`) record neither load nor commit. I ran an interleaved
comparison in one process: the median list
(`v83/returns/case/t2_stage0/recorded`), 5 rounds, each round running
uncached, cold and warm in turn. "Uncached" was `_read_member` swapped for
the old `read_text` + `json.loads` path with a fresh entry per read, which
is slightly slower than the true pre-change code because it also copies
the corpus bodies. Medians: uncached 2.12 s, cold 1.67 s (-21 %), warm
1.62 s (-24 %). One listing of `packages/content/tax/2025` took 0.277 s
uncached and 0.060 s warm. The charter's 10 % stop line is still cleared
by a wide margin. Consequence: the headline percentages in `track1.md`
should not be quoted as the saving. Repair: restate them from paired,
interleaved runs, or record load per run and treat cross-run ratios as
indicative only.

**MRO-R3 (Low, evidence).** The new unit tests do not detect a checksum that is
stale for changed content with an unchanged id. I ran an in-memory mutant that
cached `_MemberEntry.checksum()` per `(id, version)` instead of per content.
It passed all 8 tests in `tests/test_member_reads_once.py`.
`test_changed_bytes_are_reparsed_even_with_same_size_and_mtime` (line 88)
edits the id itself, so a per-id key also misses. The existing boundary test
`tests/test_frrs_t3_resolver_bootstrap.py:216`
(`test_changed_member_bytes_under_honest_registry_refuses`) does catch the
mutant when its process has resolved the clean corpus first (1 of 31 failed).
That protection depends on test order within a worker. The implementation is
correct, because the checksum lives on the content-keyed entry. Repair: in the
same-size/same-mtime test, also change a non-id field and assert
`checksum() == citizen_checksum(body())` for the edited file.

**MRO-R4 (Info, evidence scope).** `validation-after.json` does not test the
cache: validation reads its corpus through `tools.package_successor`
(`track1.md:115` says so). The identity proof has 0 refused lists, so
`MEMBER_ABSENT_OR_MISMATCH` and `MEMBER_UNPUBLISHED` through the cache are
covered only by existing resolver tests (for example the one in MRO-R3), not by
the 775-list dump. This is not a defect. It means "validation errors unchanged"
should not be read as evidence about the cache.

**MRO-R5 (Info, bounds).** The bound at `production_resolver.py:174` counts
entries, not bytes. On this tree, `packages/` holds 2,471 JSON files with 2,467
distinct contents (47.5 MiB raw; the largest file is 1.01 MiB). By the
evidence's ratio (79 MiB resident for 30 MiB raw), a worker that loads all of
them would hold roughly 125 MiB, and ten xdist workers about 1.25 GB in the
worst case. The CI runner can absorb that. The only growth path the count
bound leaves open is per-entry size. Entries live for the whole process,
including the long-lived `ThreadingHTTPServer` sessions in `entry_loop.py` and
`correction_session.py`. In those sessions `_read_member`'s `get` followed by
`move_to_end` (`production_resolver.py:235`) is not atomic across threads. It
could raise `KeyError` only if another thread evicts the same key in between,
and eviction needs more than 4,096 distinct contents, which this tree does not
reach. The validation memo uses the same pattern. Acceptable as is; noted in
case the corpus grows past the bound.

**MRO-R6 (Info, sharing).** `MemberCandidate.view` is read-only only at the top
level. Nested containers in the shared parse can be changed through it, and only
the docstring stops that. I checked every consumer. Each reads only the scalars
`id`, `version` and `schema` from the view
(`production_resolver.py:511`, `:576`; `surface_resolver.py:128`) and keeps only
`body()` copies (`production_resolver.py:528`, the matching package bodies in
both resolvers). `_copy_json` copies dicts and lists recursively, and
`json.loads` produces nothing else mutable, so the copy is deep enough for every
consumer that mutates. `citizen_checksum` only serialises its input.

## Charter questions

1. **Staleness.** None found. The key is the SHA-256 of the bytes this call
   read (`production_resolver.py:235`). A parse of identical bytes is
   deterministic, and the checksum is stored on the content-keyed entry.
   Failures are never cached. The behaviour of `read_text` (universal newlines)
   and of bytes decoding is equal for JSON, and the BOM and CRLF cases are
   tested. All three consumers, including `surface_resolver.py`, go through
   `_member_candidates`. The validation memo keys on `citizen_checksum` of the
   private corpus copies and is independent of this cache.
2. **Sharing and mutation.** No path found; see MRO-R6.
3. **Bounds.** Acceptable; see MRO-R5.
4. **Identity and timing.** I reproduced identity myself: 775 lists, 691
   success, 84 error, 0 refused, per-list digest `3def5f6f…cab1`, equal to the
   baseline. The timing claims are overstated; see MRO-R2.
5. **Tests.** Mutants run in memory against `tests/test_member_reads_once.py`:
   stat-only key (path, size, mtime) caught by 2 tests; path-only key caught
   by 4; unbounded cache caught by 1; no-op `clear_member_cache` caught by 2;
   `body()` returning the shared parse caught by 1; shallow `body()` copy
   caught by 1; plain-dict view caught by 1; checksum keyed by id survived
   (MRO-R3).

## What I ran

- `build_orientation_block.py --ref HEAD --role reviewer` (SHA verified),
  `git fetch` plus `rev-list` against `github/main`.
- Read the full code diff, the tests, `track1.md`, `charter-track1.md`, the
  evidence JSON headers, and the resolver tamper tests.
- Identity: `mro_dump.py` driven from a scratch wrapper outside the repo that
  redirected its output there (wall time 166 s, 9 workers).
- Mutation checks: in-memory monkeypatches in a separate Python process; no
  edits to the worktree.
- Interleaved A/B timing (MRO-R2) and the GC check (MRO-R1) on Python 3.14
  and on Python 3.13 via `uv`.
- `python3 tools/envelope_scan.py --range github/main..HEAD` (exit 0),
  `python3 -m mypy` (no issues in 515 files), `tools/governance_lint.py`
  (conformant), `gh pr checks 286`, and the failed-run log.
- No pytest suite run: the only failing claim was CI's, and it was examined
  from the CI log and an in-process timing.
