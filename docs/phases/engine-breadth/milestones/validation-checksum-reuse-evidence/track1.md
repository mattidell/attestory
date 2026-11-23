# Track 1: validation reuses member checksums

Milestone: validation-checksum-reuse. Charter:
`docs/reviews/validation-checksum-reuse/charter-track1.md`. Published core
v100 (registry and release v98), 10-CPU machine, Python 3.14, base commit
`330b472c`. Every number below is read from the JSON file named beside it in
this directory. The machine was shared (load average 3 to 8 during the runs),
so the timing that counts is the paired, interleaved run in section 4.

## Result in one paragraph

On every recorded list, the validation memo key recomputed the canonical
checksum of all 1,064 corpus bodies twice (once per resolution) and
`validate_package` recomputed it once more on the memo miss: 3,192
checksums, about 0.063 s of a 1.65 s median list (3.8 %), though the member
cache already held each of them, keyed on the SHA-256 of the bytes read.
Both now take the cache's checksum: a warm list computes no citizen
checksum at all, a cold list only the cache's own 1,747 (one per distinct
content). For that to be sound the shared parse behind a cached checksum
must be unreachable, so the member view now hands out nested values as
private copies. All 775 recorded lists replay byte-identically. Paired and
interleaved, the median list is 6.4 % faster warm and 4.8 % faster cold; the
slowest list 5.7 % warm and 3.9 % cold. No kernel, package, content, schema
or projection file changed.

## 1. Measurement (before the change)

`vcr_measure.py` wraps `citizen_checksum` where production code looks it up
(the resolver module and the validator module), attributes each call to its
calling function and line, and times `_validation_memo_key` and
`validate_package`. One process per workload: a warm-up on the base return,
then the list with the member cache kept ("warm": every list after a
worker's first, the test suite, CI) and with it emptied ("cold"); each run
starts with an empty validation memo, as a recorded list does. Files:
`measure-before-{median,slowest}.json`. The median and slowest lists are the
ones rust-kernel-experiment P0 chose, so the figures compare with the earlier
speed milestones.

| site (base commit) | per list | median, s | slowest, s |
| --- | --- | --- | --- |
| `production_resolver.py:129`, memo key, `corpus_digest` | 2,128 (1,064 x 2 resolutions) | 0.043 | 0.043 |
| `package_validation.py:1854`, `validate_package` member check | 1,064 (memo miss only) | 0.020 | 0.020 |
| recomputed, total | 3,192 | 0.063 (3.8 % of 1.648 s) | 0.063 (3.7 % of 1.727 s) |
| `production_resolver.py:205`, member cache (cold only, once per content) | 1,747 | 0.098 | 0.098 |
| `_validation_memo_key`, inclusive (2 calls) | | 0.066 | 0.066 |
| `validate_package`, inclusive (1 call) | | 0.280 | 0.276 |

The plan's "about 3,159" was counted on core v96 (1,053 members); v100 pins
1,064. The two resolutions per list are the Social Security handover and the
run. No other caller computes a citizen checksum on these workloads.

## 2. Design

`packages/derivation/production_resolver.py` and
`packages/derivation/package_validation.py`; nothing under `packages/kernel/`.

- `_resolve_member_corpus` already admits a body only when the cache's
  checksum of the candidate equals the registry checksum. It now returns,
  beside the corpus, the checksum of each body it copies:
  `matches[0].checksum()`, the cache entry the copy was just made from.
- `_validate_once` and `_validation_memo_key` take that mapping
  (`corpus_checksums`, optional). The memo key's corpus digest uses a given
  checksum for a key and computes `citizen_checksum` for any key it does not
  name, so a corpus that did not come from the resolver is keyed exactly as
  before. The test fakes and the other callers are unchanged: without the
  mapping `validate_package` is called with the same four arguments as
  before.
- `validate_package` gains a keyword-only `corpus_checksums`; for a key it
  names, the member check compares that checksum to the published one instead
  of recomputing; any key it does not name is checksummed as before.
  `runners/derive.py`, `tools/package_successor.py` and the presentation
  example do not pass it and behave as before.

Why the reused checksum stands for the bytes:

- The cache entry is keyed on the SHA-256 of the bytes read, its parse is
  what `json.loads` returned for those bytes, and its checksum is computed
  from that parse.
- Before this change the shared parse was reachable: the candidate's `view`
  was a `MappingProxyType`, read-only at the top level only, so a nested
  object could be mutated through it (member-reads-once review MRO-R6). That
  was tolerable while `validate_package` recomputed the checksum of every
  corpus body, because a corrupted parse would have failed the check. With
  the check reusing the cache's checksum it would not, so the view is now a
  `_MemberView`: scalars are returned as they are, nested objects and arrays
  as private copies. Nothing outside the module can reach `_body`; `body()`
  copies it, as before. The three readers (`resolve_production_package`,
  `_resolve_member_corpus`, `surface_resolver`) read only scalar fields from
  the view.
- The corpus bodies are private copies made inside `_resolve_member_corpus`
  and handed, with their checksums, straight to `_validate_once`; no code
  runs between.
- A file edited after a cached read has new bytes, hence a new entry and a
  new checksum, and admission refuses it unless the registry names that
  checksum; then the memo key changes and validation runs again.

## 3. Identity proof

`vcr_dump.py`: the 775 recorded lists are materialized once
(`recorded_lists()`, 56 s) into one scratch file that every shard of both
runs reads. Three shards of about 258 lists, nine workers each, about 68 s a
shard. Per list, rust-kernel-experiment's `track1_dump.per_list`: SHA-256 of
the canonical report and published values, of the saved page bytes and of the
presentation bytes; for an erroring list the exception class and message.

- `summary-before.json` (base code) and `summary-after.json`: 691 success, 84
  error (FindingModelError, HorizonModelError, SourceAuthorityError, as on
  earlier cores), per-list digest
  `03113fb0eca7488e89f706928d6a4dc8730a027a41a02b4ff9fcee7538d3f0bf` in both.
- `compare-before-after.json`: 775 lists compared, 0 differ.

Tests, `tests/test_validation_checksum_reuse.py` (synthetic `demo.*` member
directory, fast lane):

- the reused checksums equal `citizen_checksum` of the corpus bodies and the
  registry's, on a miss and on a hit, and the memo key built from them equals
  the key built by recomputing;
- a warm resolution plus validation computes no checksum and gives the same
  verdict as the plain `validate_package` call, which still checksums every
  member;
- `validate_package` uses a given checksum (a forged one is reported as
  `MEMBER_CHECKSUM_MISMATCH`) and computes a missing one (a tampered body
  without a given checksum is caught);
- a citizen changed after a cached read is still caught: a file edited at the
  same size and modification time is refused at admission
  (`MEMBER_ABSENT_OR_MISMATCH`); mutating every nested value read through the
  view and every returned corpus body leaves the next corpus, its checksums
  and every cached parse equal to the bytes on disk; a mutated corpus handed
  to `_validate_once` without the resolver's checksums fails validation;
- the memo key changes when any one member's bytes change (each of three
  members edited in turn and republished; the corpus part of the key moves,
  not only the registry part), and changed bytes validate again rather than
  hit;
- the checksums live only in the member cache: after `clear_member_cache` the
  next resolution recomputes one per distinct content, and
  `clear_validation_memo` empties the memo.

Mutant check: restoring the `MappingProxyType` view (nested values shared)
fails the view-mutation test.

## 4. Timing

### Paired and interleaved (`vcr_timing.py`, `timing-paired.json`)

Six rounds. Each round runs one process of the base tree (a pristine export
of `330b472c`) and one of this tree, the order flipped every round, so both
see the same machine load. In each process: a warm-up, then three
interleaved repetitions of median cold, median warm, slowest cold and
slowest warm (each with an empty validation memo; cold also empties the
member cache). A round's figure is the median of its three; the table gives
the median over rounds and the median of the per-round paired ratio.

| | before, s | after, s | change | paired change |
| --- | --- | --- | --- | --- |
| median list, cold | 1.791 | 1.706 | -4.7 % | -4.8 % |
| median list, warm | 1.558 | 1.457 | -6.5 % | -6.4 % |
| slowest list, cold | 1.887 | 1.824 | -3.3 % | -3.9 % |
| slowest list, warm | 1.662 | 1.572 | -5.4 % | -5.7 % |

Every one of the six rounds is faster after in every cell (warm median:
1.546 to 1.563 s before, 1.449 to 1.472 s after). The saving, about 0.09 s
warm, is a little above the 0.063 s the instrumented counter attributed to
the recomputed checksums; the inclusive timers in `measure-after-*.json`
show `_validation_memo_key` falling from 0.066 s to 0.019 s per list and
`validate_package` from 0.280 s to 0.250 s.

### Replay wall

Three shards of the identity dump, nine workers: 68.1, 67.7, 68.3 s before;
67.0, 67.3, 67.4 s after. These ran minutes apart on a shared machine and
include worker start-up, so they are indicative only.

### After (`measure-after-{median,slowest}.json`)

Warm: 0 citizen checksums per list (was 3,192). Cold: 1,747, all in the
member cache, once per distinct content (`production_resolver.py:271`).

The full suite's wall time is reported in the track's handoff, not here.

## 5. What remains

- On a cold list the member cache's own 1,747 checksums (0.098 s) remain;
  they are needed once per content and are shared by every later list.
- What is left of the memo key (the canonical package digest and the digest
  of every schema document; about 0.009 s per call in all) is recomputed per
  call; neither is a member checksum, so both were left alone.
- `validate_package` itself is about 0.25 s of a list; what dominates beyond
  it (kernel fact store, the byte reads of the member cache) is as
  member-reads-once reported.

## Files

`vcr_common.py` (workload on v100, loads the rust-kernel-experiment scripts
by path), `vcr_measure.py`, `vcr_dump.py`, `vcr_timing.py`; summaries:
`measure-*.json`, `summary-{before,after}.json`, `compare-before-after.json`,
`timing-paired.json`. The materialized lists, the full per-list dumps and the
base export stay in an uncommitted scratch directory.

## Final checks

Fast lane (`pytest -m "not live"`):

```
======================= 1929 passed, 8 skipped in 15.56s =======================
```

Full suite (`pytest`), one command covering every test file (no chunks):

```
=========== 1 failed, 7368 passed, 25 skipped in 1771.51s (0:29:31) ============
```

Wall time (`time` real): 1772.40 s.

mypy (`python3 -m mypy`):

```
Success: no issues found in 529 source files
```

The one full-suite failure is
`tests/test_sale_page_observation_diagnostics.py::test_node_observer_emits_safe_manifest_stage_without_starting_chrome`.
The test and `tools/presentation_harness/sale-page-observation.mjs` are
identical to base `330b472c`; this branch did not touch them. It fails when
both `FORCE_COLOR` and `NO_COLOR` are set, because node writes a warning onto
stderr before the JSON the test parses; with those variables unset the same
test passes. Left unfixed.
