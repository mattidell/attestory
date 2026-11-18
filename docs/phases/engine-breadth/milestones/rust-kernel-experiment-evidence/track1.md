# Track 1: Python algorithmic fixes

Milestone: rust-kernel-experiment. Charter:
`docs/reviews/rust-kernel-experiment/charter-track1.md`. Core v96,
10-CPU machine, Python 3.14. Baseline commit `0763f572`. Every number is
read from a JSON file in this directory (named beside it).

## Result in one paragraph

Four Python fixes under `packages/derivation/` and no kernel, content or
schema change. All 775 recorded lists replay byte-identically (result hash,
page hash, error class and message). Total per-list time over the 775
lists fell from 5853 s to 2026 s of CPU (2.9x), the replay wall from 787 s
to 278 s, the median success from 7.8 s to 2.9 s and the slowest from
49.6 s to 3.5 s. What remains is file I/O plus JSON for the 7252 member
files, one package validation, and (about a fifth) the kernel. A kernel
port would now save at most about 0.5 s of a 2.6 s median list; it pays
only on kernel-shaped work such as K13.

## What was adopted and what was reworked

The first builder ran out of credits after commits 0668bbab, 6e9d5537,
02938ec7, 0217dfde and 5b3e1257 and left the item 5 evidence uncommitted.
This builder reviewed each diff and **adopted all five commits unchanged**:

- 6e9d5537 (validation index): read against the old scans for
  equivalence, see Item 1. Adopted.
- 02938ec7 (validation memo): reviewed, see Item 2. Adopted; the review
  found no stale-hit path.
- 0217dfde (closure-walk memo): proof read, see Item 3. Adopted.
- 5b3e1257 (marshal precompute): adopted, one theoretical difference noted
  under Item 4.
- 0668bbab (dump and baseline summary): adopted, but its **validation
  comparison was not trustworthy** and its baseline provenance was
  re-proven; see "Identity proof".

Reworked (this builder): the validation comparison and its proof; the
evidence scripts (`track1_timing.py` and `track1_profile.py` now clear the
memo before each list, `track1_compare.py` compares the error multiset and,
on request, the order); the unit tests (the first builder's reference walk
lacked the real function's closing refusal step and its member-meaning
scan, so it did not exercise `meaning_for`; both are in now, and the
source-family index test the old docstring promised did not exist). The
evidence JSONs and the tests were uncommitted and are committed here.

## The fixes

1. **Validation index** (`package_validation.py`, 6e9d5537). The
   source-family edges scanned every resolved member for every family and
   every pin. Bundles by id and closure mappings by listed fact type are
   now indexed once, in `resolved` order. Same errors: the indexed scans
   add the same ids to the same `adj` sets (a set, so the order of adds
   does not matter). Raising behaviour on malformed bodies is unchanged
   in practice because only schema-valid citizens reach `resolved`.
2. **Validate once per package bytes** (`production_resolver.py`,
   02938ec7). See Item 2 review.
3. **Closure-walk memo and member index** (`presentation_projection.py`,
   0217dfde). See Item 3 review.
4. **Marshal precompute** (`marshal.py`, 5b3e1257): each rule's required
   symbols are folded once, on first need, into one set; the per-finding
   test is `type_id in union`, equal to the old `any(...)`. A run with no
   fallback finding still computes none. Theoretical difference: the old
   `any` stopped at the first rule naming the symbol, so a rule whose
   `_rule_required_symbols` raised after that point was never reached; the
   union evaluates every rule. Rules are schema-validated before this
   point, and all 775 lists agree, so it is noted, not changed.

## Identity proof

**Lists.** `track1_dump.py` replays all 775 lists (9 workers) and hashes
per list the canonical result, the saved page bytes (and the presentation
bytes), and for erroring lists the exception class and message (temporary
directory masked).

- `track1-summary-baseline.json`: 775 lists, 691 success, 84 error
  (`FindingModelError`, `HorizonModelError`, `SourceAuthorityError`),
  per-list digest `3def5f6f...cab1`.
- **Baseline provenance, re-proven.** The committed baseline's timestamps
  could not show it ran on unchanged code, so it was regenerated from a
  pristine export of `0763f572` (`git archive` into a scratch directory
  outside the repository, the same dump script run there). The pristine
  re-run gave the same per-list digest and the same 691/84 split.
- `track1-summary-after.json`, rerun on the final code: same per-list
  digest, 775 of 775 lists identical list by list against the pristine
  dump (`track1_compare.py`). Replay wall 114.6 s against 705.9 s.

**Validation error lists** (published v96 package plus four mutations:
remove every source-family pin, drop every seventh pin, two unknown
versions, four tampered bodies). Files: `track1-validation-baseline.json`
(pristine, `PYTHONHASHSEED=0`), `track1-validation-after.json` (changed,
seed 0), `track1-validation-seeds.json` (seeds 0, 1, 2, pristine against
changed).

- **The old comparison was not valid.** The `issues_digest` values in the
  two `track1-summary-*.json` files disagree for three mutations because
  those runs used a random hash seed and the issue **order** depends on
  it. They are not evidence either way and should be ignored; the seeded
  files are the comparison.
- **On the pristine code the error order is seed-dependent** for
  `mutation_remove_source_families` and `mutation_drop_every_seventh`
  (issue order follows set iteration). The other three cases are stable.
  The contract is therefore: the same multiset of errors always, and the
  same order under any fixed seed.
- Result: under seeds 0, 1 and 2 the changed code's complete output (ok
  flag, ordered issue list, output owners, resolved members) equals the
  pristine code's exactly, for all five cases; the sorted multiset of
  errors is equal for all. The committed unit test
  `tests/test_track1_validation_index.py` pins the multiset, output owners
  and resolved members from the pristine code.

## Item 2 review: the validation memo

- **Where.** Module globals of `production_resolver.py`
  (`_VALIDATION_MEMO`, an `OrderedDict`), used only by `_validate_once`,
  which `resolve_production_package` calls in place of `validate_package`.
- **Lifetime.** The life of the process; bounded to the last 4 keys;
  `clear_validation_memo()` empties it. A hit returns a `deepcopy`, and
  the stored verdict is itself a deepcopy, so no caller shares mutable
  members.
- **Key** (all must match): the validator's code object, SHA-256 of the
  canonical package bytes, the exact `(id, version, checksum)` of every
  member pin, the sorted `(id, version, checksum)` of every body in the
  corpus handed to the validator (computed from the bodies themselves, added
  by the repair of RKE-R2), and SHA-256 of every schema document in the
  registry.
- **A changed file cannot hit a stale entry.** Member bodies enter
  `validate_package` only through `_resolve_member_corpus`, which admits a
  body only when its canonical SHA-256 equals the registry checksum for
  that pin, so a body is fixed by its checksum, and a changed file is
  either refused before validation or has a different checksum in the key.
  A changed package changes the package digest; a changed schema changes
  the schema digest; a replaced validator changes the code object. The
  checksum comparison itself runs on every call (it precedes the memo), so
  the memo cannot skip it. I/O is not memoized: member files are still
  read and hashed each time. `validate_package` reads no files and no
  environment; the only other input is `corpus`, which is now in the key
  directly, so a direct caller (or a test) that passes a different corpus
  under the same checksums misses instead of hitting. Cost, measured on the
  median list (1053 corpus members): 0.021 s per key, two keys per replay,
  about 0.04 s, 1 to 2 % of that replay. Verifying the corpus against
  `citizen_checksums` inside `_validate_once` would hash the same bodies,
  so it is no cheaper; the digest in the key was chosen because it needs
  no second rule.
- **Limit.** The key does not see a monkeypatch of a helper inside
  `package_validation` other than `validate_package` itself. No test or
  tool does that; tests that patch `validate_package` (as the new tests do)
  change the code-object part of the key.
- Tests: `tests/test_track1_memos.py` (identical bytes validate once and
  equal the plain call; a hit shares no mutable members; changed package,
  member checksum, schema document and validator each miss; the same
  checksums with a different corpus miss; bounded). A separate synthetic
  test pins the `marshal.py` precompute: the once-computed union of rule
  required symbols binds exactly the types the per-rule check bound
  (`ordinary requires`, rule-artifact `when`/`value` refs, attachment-rule
  subtotals and answers; an unrequired type stays unbound).

## Item 3 review: the closure-walk memo

A walk of one blocked row depends on `seen` only through the keys it
examines. Each walk records the keys it examined, which of them it skipped
as already seen, and what it added to the family, fact and extra sets. A
walk that returned true and skipped nothing it was handed is reused under
any `seen` containing none of the keys it examined. A false walk ends the
whole closure and is never reused. The memo lives inside one
`_closure_question_reasons` call, keyed by `(walk kind, id(row))`, so
nothing outlives the call and a changed row graph is a new call.
Correctness is exercised by 1500 random blocked-row graphs with cycles,
shared rows, synthesized member-validation rows with their own meanings,
and refusal sentences: the memoized function equals both the reference
walk in the test and the **actual pristine function** (checked once
outside the suite). Plus a 40-layer diamond (2^40 paths) that finishes
instantly, and a changed-row test. The identity dump covers the real
lists.

**Cycle guards (repair of RKE-R1).** The random graphs do not exercise the
guards, so one deterministic case does:
`test_two_paths_to_a_synthesized_row_keep_both_cycle_guards_honest`. A
synthesized member-validation row `C` is reached first through
`P -> K -> C` (key `K` in `seen`, so `C` is walked without explaining `K`
and returns true through the family) and second through `Q -> C` (`K` not in
`seen`, so `C` explains `K` and adds the family meaning). Mutation checks
(in memory on a scratch copy; nothing mutated is committed):

- dropping `frame.hits.isdisjoint(seen)` from the store condition: the test
  **fails** (the meaning sentence is lost);
- dropping `seen.isdisjoint(known.examined)` from the reuse condition: the
  test passes, and so does everything else, including 60 000 random graphs
  compared with the reference walk (0 mismatches). It is an equivalent
  mutation, not a gap in the test: a false walk aborts the whole closure, so
  every true walk's additions reach the final sets whichever way it is
  reached, and a reused walk can only add what its first run already added;
  skipping a key under a larger `seen` can only turn a walk toward true. The
  guard keeps the memo's reuse condition exact (and its absorbed
  `examined`/`hits` sets equal to a fresh walk's) but cannot change the
  reasons. I could not construct a graph that observes it.

## Timing

Method as P0: all 775 lists in parallel (9 workers, each warmed once),
sorted by per-list wall time. Each list now starts with an empty validation
memo, as a fresh process would, so the saving counted is the second
validation inside one list and not a hit from the previous list a warm
worker happened to run (without that, per-list prep fell a further
0.3 s; see "Memo and warm workers"). Files: `track1-timing.json`
against `p0-timing.json`.

| | P0 | Track 1 |
| --- | --- | --- |
| replay wall, 775 lists | 787 s | 278 s |
| sum of per-list total, successes | 5853 s | 2026 s |
| median per list (prep + run + render) | 7.76 s | 2.94 s |
| quartiles | 7.45 / 7.70 / 8.02 s | 2.82 / 2.93 / 3.00 s |
| slowest | 49.6 s | 3.55 s |
| prep median / run median | 3.24 s / 4.46 s | 1.31 s / 1.60 s |

The 28-list tail above 10 s is gone (the slowest list now takes about the
median plus 0.6 s). The three P0 workloads, one process each
(`track1-profile-*.json`, `track1-sample-*.json`, `track1-centres-*.json`):

| Workload | P0 total | Track 1 total | Largest change |
| --- | --- | --- | --- |
| median | 6.73 s (prep 2.63, run 4.08) | 2.61 s (prep 1.01, run 1.58) | validation 3.78 s (2 calls) to 0.27 s (1 call); marshal 0.52 to 0.04 s |
| slowest | 38.49 s (run 35.83) | 2.69 s (run 1.63) | `_closure_question_reasons` 32.9 s to 0.02 s |
| K13 | 5.25 s | 5.03 s | `run_v42` 1.19 to 0.95 s; the rest is untouched kernel work |

## Layer table (sampled own time, percent of wall; P0 to Track 1)

| Layer | median | slowest | K13 |
| --- | --- | --- | --- |
| kernel: fact store | 6.3 to 19.7 | 1.4 to 22.8 | 54.8 to 58.2 |
| kernel: finding model | 0.2 to 0.0 | 0.1 to 0.3 | 4.2 to 4.7 |
| derivation: evaluator/runner | 8.7 to 4.9 | 1.6 to 3.3 | 3.8 to 1.8 |
| derivation: package validation | 59.0 to 18.9 | 10.5 to 18.0 | 5.6 to 2.8 |
| derivation: live coordination | 0.6 to 2.0 | 0.1 to 2.1 | 0.3 to 0.5 |
| presentation projection | 8.0 to 1.7 | 83.4 to 1.1 | 0.1 to 0.2 |
| jsonschema validation | 2.5 to 7.1 | 0.4 to 7.6 | 2.0 to 1.9 |
| JSON (de)serialization | 1.8 to 5.6 | 0.3 to 5.2 | 13.3 to 15.1 |
| file I/O | 11.9 to 34.0 | 2.1 to 33.7 | 9.7 to 9.0 |
| copy.deepcopy | 0.3 to 3.2 | 0.1 to 3.1 | 1.2 to 1.6 |

Shares of a much smaller whole, so a share going up is not a cost going
up. Inclusive kernel (finding model plus fact store, any frame on the
stack): about 17 to 21 % on the median and slowest, 59 to 61 % on K13.

## What dominates now

On a recorded replay, in this order: **file I/O and JSON (about 34 % plus
6 %)**, from reading and hashing the 7252 member files (`_json_candidates`
is 0.67 s over 4 calls on a 2.6 s list, twice per list because prep and the
run each resolve the package); **one package validation (about 19 %,
0.27 s)**; **the kernel (about 20 %)**, mostly `findings.project`
(0.44 s over 2 calls) and `facts._lattice_metadata`; then jsonschema
(7 %) and deepcopy (3 %). On K13-shaped recorder stories the kernel is
still about 60 %, unchanged.

## Does a kernel port pay now?

Not for the recorded-list workload. The kernel is about 20 % of a 2.6 s
median list, so a port that made it free would save about 0.5 s (about
20 %); a port that made it 5x faster saves about 0.4 s. The larger
remaining lever on those lists is Python again: stop reading and hashing
the same member files twice per list (about 40 % of the list sits in file
I/O and JSON), which needs no kernel edit and was outside Track 1's charter.
A port pays where the kernel is the whole story: K13 spends about 60 % of
5 s in `findings.project` and `_lattice_metadata`, and that cost is
algorithmic too (every save re-projects the whole log; see p0.md), so the
Python fix for it is still unmade and should precede any port. Whether to
fix that, or the file reads, or port, is the owner's decision.

## Memo and warm workers (a measurement caveat)

The validation memo is per process. A long-lived worker that replays many
lists on one package validates once, not once per list. The per-list times
above deliberately clear it. Left in place, the same replay measures prep
about 0.3 s lower per list; that is a real saving for a worker process but
not one a one-shot run sees, so it is not counted here.

## Repair of the review notes (RKE-R1 to RKE-R3)

Identity dump rerun on all 775 lists after the repair
(`track1-summary-repair.json`): `per_list_digest` equals the baseline,
`3def5f6f845f2c0bee7500a17f6cdda0f0577a84de0331144b10a26f5356cab1`
(691 success, 84 error, 0 refused). The changes are the corpus in the
validation memo key, three tests, and this document.

## Gate

Run on the final code, before the report commit:

- `pytest`: 7069 passed, 25 skipped, 10947 subtests passed (36 min 57 s
  wall on this machine while other work shared the CPUs). After the
  repair: 7072 passed, 25 skipped, 10947 subtests passed (37 min 7 s).
- `python3 -m mypy`: Success: no issues found in 514 source files.
