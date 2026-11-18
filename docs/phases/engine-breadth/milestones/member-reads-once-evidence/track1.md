# Track 1: member files are read once

Milestone: member-reads-once. Charter: `docs/reviews/member-reads-once/charter-track1.md`.
Core v96, 10-CPU machine, Python 3.14. Base commit `3e10a275`. Numbers are read
from the JSON files named beside them in this directory. The machine was shared
and busy during every timing run (load average 12 to 13 on 10 CPUs); before and
after runs were taken minutes apart, so compare ratios, not absolute seconds
against the rust-kernel-experiment evidence.

## Result in one paragraph

A recorded list resolved the production package twice (the Social Security
handover, then the run) and each resolution listed the member directory twice
(once to find the package, once to build the member corpus), so each of the
1,813 member files was read, parsed and, for the 1,719 with a string id,
canonically checksummed four times per list (7,252 reads; two times, 3,626
reads, in K13). Each distinct file content is now parsed and checksummed once
per process, keyed on the bytes the call read. All 775 recorded lists replay
byte-identically (per-list digest equal to the baseline). The median replay
fell from 4.64 s to 3.83 s with the cache cleared before every list (-18 %)
and to 3.37 s with it kept across the lists a worker runs (-27 %); in a single
process the median fell 3.37 s to 2.12 s cold and 1.92 s warm (-37 %, -43 %).
The before and after runs above were taken at different times under load,
so their percentages are indicative only. The fresh review's paired,
interleaved run in one process (median list, five rounds, uncached, cold and
warm in turn) gives the figure to quote: uncached 2.12 s, cold 1.67 s
(-21 %), warm 1.62 s (-24 %); one listing of the 2025 content directory
0.277 s uncached and 0.060 s warm (review MRO-R2). The saving clears the
charter's 10 % stop line in every measurement. No kernel,
content or schema file changed.

## 1. Read counts (before the change)

`mro_counts.py` wraps `Path.read_bytes/read_text` under the content directory,
`_json_candidates` (by caller), `_load_json` and `citizen_checksum`, after one
warm-up list. Files: `counts-before-{median,slowest,k13}.json`.

| | median list | slowest list | K13 |
| --- | --- | --- | --- |
| `_json_candidates` calls | 4 | 4 | 2 |
| member-directory reads | 7,259 | 7,259 | 3,630 |
| distinct files | 1,813 | 1,813 | 1,813 |
| reads per file | 4 (two files 5 and 10) | same | 2 (two files 3 and 5) |
| `_load_json` parses | 7,252 | 7,252 | 3,626 |
| `citizen_checksum` calls, `_resolve_member_corpus` | 3,438 | 3,438 | 1,719 |
| ... memo key (`_validation_memo_key`) | 2,106 | 2,106 | 422 |
| ... `validate_package` | 1,053 | 1,053 | 422 |

Callers of `_json_candidates`: `resolve_production_package` (finds the package;
2 calls) and `_resolve_member_corpus` (2 calls); `surface_resolver` is the
third caller (surface artifact, not on these workloads). The seven extra reads
are the registry and the release files, not member files. The only other
member-directory readers are `_verify_release_and_registry` and
`resolve_adopted_surface`, which read a handful of release/registry files and
are untouched.

## 2. Design

`packages/derivation/production_resolver.py`:

- `_read_member(path)` reads the file once, computes `sha256(raw)`, and looks
  that digest up in `_MEMBER_CACHE` (an `OrderedDict`, LRU). A hit returns the
  entry; a miss decodes UTF-8, `json.loads`, requires an object, stores it.
  Failures (unreadable, not UTF-8, not JSON, not an object) raise exactly as
  before, are never cached, and the caller skips the file as before.
- An entry holds the shared parse and, lazily, `citizen_checksum` of it. Two
  paths holding identical bytes share one entry.
- `_member_candidates(directory)` is the new neutral inventory. A
  `MemberCandidate` exposes `view` (a `MappingProxyType` over the shared parse,
  for reading id, version, schema and package checksum), `checksum()` (cached)
  and `body()` (a private copy). Callers copy only what they keep: the matching
  package body, the 1,053 pinned corpus bodies. The three loops that used
  `_json_candidates` now use `_member_candidates`; `_json_candidates` remains as
  the copying wrapper (every body private) and is the uncached contract.
- Copies use `_copy_json`, a dict/list/scalar recursive copy; parses are pure
  JSON, so it equals `deepcopy` and is 2.3x faster (see below).
- Bound: `_MEMBER_CACHE_LIMIT = 4096` distinct contents, about 2.3x the
  published corpus (1,813 files). The limit has to exceed the working set or a
  sequential scan evicts every entry before its reuse. A full cache of the
  published corpus holds about 79 MiB of parses (measured resident growth).
- `clear_member_cache()` empties it, as `clear_validation_memo()` does.
- Text mode vs bytes: the old read used `read_text("utf-8")` (universal
  newlines); the new decodes bytes. Between JSON tokens `\r` and `\n` are
  both whitespace and a raw line break inside a string is invalid in both, so
  results are equal; the unit test includes a CRLF file and a BOM file.

### Key choice: bytes against stat (Decision 1)

`mro_key.py` -> `key-measurements.json`. One listing of the content directory:

| | one listing | per list (4 listings) |
| --- | --- | --- |
| uncached: read, parse, checksum | 0.424 s | 1.70 s |
| byte key, cache warm: read, SHA-256, reuse | 0.087 s | 0.35 s |
| stat key, cache warm: stat only | 0.015 s | 0.06 s |
| directory walk alone | 0.011 s | |
| read and hash all files alone | 0.093 s | |

The byte key saves 1.35 s of the 1.70 s per list; a stat key would save 0.29 s
more (about 8 to 9 % of a warm median) by skipping the read. It is not taken:
the same experiment shows a same-size, same-mtime edit leaves the stat tuple
(path, size, mtime_ns, inode) unchanged
(`stat_key_unchanged_after_same_size_same_mtime_edit: true`), so a stat key
serves a stale parse, while the byte key sees the edit (`byte_key_sees_edit:
true`). A proof that no filesystem the project runs on can do that was not
attempted; Decision 1 prefers the key that needs none. The remaining read and
hash is the largest piece of what the cache still costs.

Copy cost: 1,053 corpus-sized bodies cost 0.107 s with `deepcopy`, 0.046 s with
`_copy_json`, and 0.119 s to reparse; a full deepcopy of every candidate (the
naive "return copies" shape) would have cost more than the parse it saved,
which is why candidates expose a read-only view and copy only what is kept.

## 3. Identity proof

- `summary-after.json`: all 775 recorded lists replayed on core v96 with the
  rust-kernel-experiment `track1_dump.py` hashing (result, page and
  presentation bytes, error class and message): 691 success, 84 error, per-list
  digest `3def5f6f845f2c0bee7500a17f6cdda0f0577a84de0331144b10a26f5356cab1`,
  equal to `track1-summary-baseline.json` (`equal_to_baseline: true`).
- `validation-after.json` (PYTHONHASHSEED=0): the five validation error lists
  equal `track1-validation-baseline.json` exactly. (Validation reads its corpus
  through `tools.package_successor`, not through this cache; it is kept as a
  guard that nothing upstream of validation moved.)
- Tests, `tests/test_member_reads_once.py`: the cached path equals a verbatim
  copy of the old implementation on a synthetic `demo.*` member directory
  (miss then hits; views, checksums, copies, key order); each distinct content
  parses once (failures are re-attempted, never cached); a file whose bytes
  change with the same size and the same modification time is re-parsed; a
  file that turns malformed or disappears is dropped; mutating returned bodies
  (top level and nested) cannot reach a later call; the shared view is
  read-only; `clear_member_cache` and the bound work.

## 4. Timing and layers

### All 775 lists (9 workers; `timing-{before,after-cold,after-warm}.json`)

`cold` clears the member cache before each list (the saving inside one list);
`warm` keeps it for the lists one worker runs (a long-lived process: the test
suite, CI). Each list also starts with an empty validation memo, as before.

| | before | after, cold | after, warm |
| --- | --- | --- | --- |
| median list (s) | 4.64 | 3.83 (-17.6 %) | 3.37 (-27.4 %) |
| slowest success (s) | 5.56 | 4.71 | 4.53 |
| sum of all lists (s) | 3410 | 2821 | 2473 |
| replay wall (s) | 411.9 | 347.4 | 307.6 |

### One workload per process (`profile-*`, `sample-*`; unprofiled total)

| | before | after, cold | after, warm |
| --- | --- | --- | --- |
| median (p0 list) | 3.37 s | 2.12 s (-37 %) | 1.92 s (-43 %) |
| slowest (p0 list) | 3.30 s | 1.91 s (-42 %) | 1.72 s (-48 %) |
| K13 | 5.80 s | 4.80 s (-17 %) | 4.60 s (-21 %) |

The "before" profiles were taken from a pristine export of the base commit with
these same scripts, not copied from the rust-kernel-experiment files, so the
machine load is comparable.

### Layer table, stack sampler, own time (share and seconds)

Median list:

| layer | before | after, cold | after, warm |
| --- | --- | --- | --- |
| file I/O | 42.5 % (1.21 s) | 21.4 % (0.39 s) | 18.2 % (0.30 s) |
| kernel: fact store | 17.2 % (0.49 s) | 22.6 % (0.42 s) | 25.6 % (0.42 s) |
| package validation | 17.2 % (0.49 s) | 19.3 % (0.35 s) | 19.8 % (0.32 s) |
| live coordination/resolution | 1.5 % (0.04 s) | 7.2 % (0.13 s) | 5.5 % (0.09 s) |
| jsonschema validation | 5.9 % (0.17 s) | 9.7 % (0.18 s) | 8.3 % (0.14 s) |
| JSON (de)serialization | 4.5 % (0.13 s) | 5.1 % (0.09 s) | 5.1 % (0.08 s) |
| evaluator/runner | 3.7 % (0.11 s) | 4.7 % (0.09 s) | 4.4 % (0.07 s) |
| copy.deepcopy | 2.9 % (0.08 s) | 3.7 % (0.07 s) | 4.4 % (0.07 s) |
| run total | 2.85 s | 1.84 s | 1.63 s |

Slowest list: file I/O 45.8 % (1.60 s) -> 19.1 % (0.37 s) cold, 15.8 %
(0.27 s) warm; kernel fact store 17.6 % (0.61 s) -> 26.2 % (0.51 s) cold, 29.7 %
(0.51 s) warm; package validation 15.0 % (0.52 s) -> 18.9 % (0.37 s) -> 16.3 %
(0.28 s); run total 3.49 s -> 1.93 s -> 1.73 s.

K13: kernel fact store 51.0 % (3.07 s) -> 59.6 % (2.90 s) cold, 62.3 % (2.93 s)
warm; file I/O 17.6 % (1.06 s) -> 7.2 % (0.35 s) -> 5.4 % (0.25 s); JSON
13.2 % (0.79 s) -> 14.5 % (0.70 s) -> 14.3 % (0.67 s); run total 6.01 s ->
4.86 s -> 4.70 s.

Full tables are in the `sample-*` files (and cProfile layers in `profile-*`).
The layer shares are of different totals, so a share can rise while its seconds
fall (the fact store is flat in seconds).

### Read counts after (`counts-after-{cold,warm}-*.json`)

Starting cold, the median list parses 1,813 member files once (`json.loads`
from `_read_member`) and checksums 1,719 once (was 7,252 and 3,438); starting
warm it parses none and checksums none from `checksum()`. The 7,259 member-
directory reads remain, by design: the byte key reads each file to learn its
content (four times per file per list).

## 5. What now dominates

- Median and slowest lists: the kernel fact store (about 0.4 to 0.5 s, 23 to
  30 %), package validation (0.3 to 0.35 s, 16 to 20 %), and still file I/O
  (0.3 to 0.4 s, 16 to 21 %), which is the 7,259 byte-key reads. The remaining
  `_member_candidates` listing (walk, read, SHA-256, view, bookkeeping) is
  about 19 % of a warm median by inclusive sample.
- `citizen_checksum` is still called 2,106 times in the validation memo key
  and 1,053 in `validate_package` per median list; the memo-key digest could
  take the cache's checksums if corpus bodies carried them (not done: the
  corpus is handed to the validator as bare dicts).
- K13 is a kernel workload: the fact store is 60 % of it and the cache did not
  touch it. The per-save re-projection lever stays parked for the owner.

## Files

Scripts load the rust-kernel-experiment evidence scripts by path under unique
names and redirect their output here: `mro_counts.py`, `mro_timing.py`,
`mro_dump.py`, `mro_profile.py`, `mro_key.py`. Summaries are the JSON files
named above. The full per-list dump stays in the (uncommitted) scratch
directory.
