# Review: validation reuses member checksums

Charter: `docs/reviews/validation-checksum-reuse/charter-review.md`. Reviewer,
fresh context. Oriented with `tools/build_orientation_block.py --ref HEAD
--role reviewer` at `b24e13ca05d4dbfa136056b4726ee8e3c5ea968b` on
`milestone/validation-checksum-reuse-2025`. That SHA matches Git. Range
`github/main..HEAD`: 5 commits, behind 0, ahead 5. Governance was not read.

## Verdict

**READY with notes.** On the paths a caller actually uses, a reused checksum
stands for the bytes being validated. A file edited after a cached read is
refused until the registry is republished, and then the memo key moves. Two
paths with the same bytes share one cache entry and one digest. An entry
taken from another directory is reused only for those same bytes. Clearing,
half-clearing, and keeping the caches all leave the digest equal to the
body. Mutating a nested value returned by the member view leaves the shared
parse, the next corpus, and the memo key alone. A sample of 111 recorded
lists is byte-identical to the code before this change. The paired timings
in the evidence support the stated gain, and the added code is small enough
to be worth it. One low note (VCR-R1): a digest that is supplied, or that
stays cached after the shared parse is mutated through `view._body`, is
trusted as the body's digest.

The box. Member-file bytes, package pins, and the published registry
checksums enter. The registry checksum is what admits a body. The member
cache may supply that body's canonical checksum only for a parse of bytes
whose SHA-256 is the cache key. The box publishes the same validation
verdict and resolved members as recomputing the checksum. Kernel code,
package content, schemas, projections, and the set of what is validated or
refused stay outside. Recorded-list output stays as it was.

## Findings

### VCR-R1 (low, lifecycle): a reused digest is trusted for the body it is handed with

`packages/derivation/package_validation.py:1863` uses
`(corpus_checksums or {}).get(key)` as the member digest.
`packages/derivation/production_resolver.py:137` puts that same value in
the memo key. `packages/derivation/production_resolver.py:232` stores the
shared parse on the view object (`_body`), and
`production_resolver.py:271` keeps the first `citizen_checksum` of that
parse.

The docstring at `package_validation.py:1814` says the argument changes no
verdict. Two measurements on the synthetic `demo.vcr` members:

1. After a normal admit of `demo.vcr.b`, `candidate.view._body["n"] = 12345`.
   The next resolve accepts the mutated parse. The reused digest is the
   cached one (`f1a31429…`), and `citizen_checksum` of the copied body is a
   different digest (`f11490fb…`). `validate_package` returns ok with no
   issues. The memo key built from the reused digest differs from the key
   built by recomputing the body.
2. `validate_package` of a `demo.vcr.a` body with `demo_tamper` set, passing
   `corpus_checksums` from the resolver, returns ok. The same call without
   that argument returns `MEMBER_CHECKSUM_MISMATCH` for `demo.vcr.a`.

`view[name]` and `view.get` copy nested objects
(`production_resolver.py:237`). Assigning a top-level key on the view
raises `TypeError`. The production readers take scalar fields from the
view and call `body()` for a copy they keep. The disk, path, other-directory,
and clear cases below all hold. So this is a private-attribute and
caller-trust hole, and the supported read API holds.

Smallest repair: say in the docstring that a supplied digest is trusted and
that a digest of different bytes changes the verdict, and keep the shared
parse off the object the public `view` property returns.

## What I ran

Cases, on a synthetic `demo.*` directory through `_resolve_member_corpus`,
`_validation_memo_key`, and `validate_package`:

- File changed on disk after a cached read, same size and modification
  time (`b.json`, `"n": 2` to `"n": 9`). Admission returns
  `MEMBER_ABSENT_OR_MISMATCH`. After the registry is rebuilt from the new
  bytes, the reused digests equal `citizen_checksum` of the bodies, the
  memo key changes in its corpus part, and validation runs again and passes.
- Two paths, same bytes (`a.json` and a copy). One cache entry, same
  corpus, same digests, memo key unchanged.
- Another directory with the same bytes. The second admit computes no
  citizen checksum and returns the same digests. The same directory with
  `b.json` changed is refused against the old registry. With a registry
  rebuilt from those bytes, `b`'s digest is the new body's digest and the
  memo key moves.
- Cache kept: a warm admit computes no citizen checksum, and two resolves
  call `validate_package` once. One content key deleted: that content is
  recomputed and every reused digest still equals the body. `clear_member_cache`
  empties `_MEMBER_CACHE` and the next admit recomputes one checksum per
  file. `clear_validation_memo` empties `_VALIDATION_MEMO`, leaves the
  member cache, and the following validation still computes no citizen
  checksum.
- In-memory view. Mutating every nested dict or list returned by the view,
  and assigning through a top-level key, leaves the next corpus equal to
  the files on disk and leaves the digests unchanged.

Byte identity. Every 7th recorded list, 111 of 775, replayed through the
rust-kernel-experiment per-list digest (canonical report and published
values, saved page bytes, presentation bytes; error class and message
otherwise). The before replay loaded the two derivation modules from the
parent of the build commit (`330b472cb`, identical to `github/main` for
those files), confirmed in the worker by the absence of `_MemberView`. The
after replay loaded this HEAD, confirmed by the presence of `_MemberView`.
Both sides: 103 success, 8 error, 0 refused. Lists compared: 111.
Differing lists: 0. Walls, after run first: 39.7 s after, 40.7 s before.
That is the same direction as the claim. It is one pair of sharded walls,
so it does not by itself establish the percentage.

Speed. Recomputed from `timing-paired.json`, six rounds, median of each
round's three repetitions, every round faster after:

| cell | before s | after s | paired change | saved s |
| --- | ---: | ---: | ---: | ---: |
| median cold | 1.7907 | 1.7063 | −4.8% | 0.084 |
| median warm | 1.5579 | 1.4567 | −6.4% | 0.101 |
| slowest cold | 1.8872 | 1.8244 | −3.9% | 0.063 |
| slowest warm | 1.6617 | 1.5719 | −5.7% | 0.090 |

Those figures match the table in `track1.md`. The behavior change is the
two derivation modules plus the new test. About a tenth of a second on
every recorded list, paid on replay and on the suite, is worth that local
change. I did not repeat the six-round interleaved protocol.

Scope. `git diff --name-only github/main..HEAD` includes no
`packages/kernel/` path, no schema, no content file, and no projection.
The new state lives on the member-cache entry and in the validation memo.
`clear_member_cache` (`production_resolver.py:204`) and
`clear_validation_memo` (`production_resolver.py:115`) empty those two
structures, measured above.

Tests. `python3 -m pytest -q tests/test_validation_checksum_reuse.py`:
9 passed, 3 subtests passed, 1.31 s. Scratch copies of
`production_resolver.py`, loaded in place of the module:

- Cache key set to the path, so a byte change is ignored. Fails
  `test_a_file_edited_after_a_cached_read_is_refused`,
  `test_changed_bytes_validate_again_instead_of_hitting`, and the memo-key
  subtests.
- Corpus part of the memo key records `None` instead of each member
  checksum. Fails the three subtests of
  `test_the_memo_key_changes_when_any_members_bytes_change` at
  `tests/test_validation_checksum_reuse.py:212`.
- `clear_member_cache` returns immediately. Fails
  `test_the_clear_hooks_clear_the_reused_checksums` at line 239
  (`0 != 4`): the cache still holds a previous test's entries.
- The view returns the shared nested object. Fails
  `test_mutating_views_and_returned_bodies_cannot_reach_the_shared_parse`.

`python3 tools/envelope_scan.py --range github/main..HEAD` exited 0.
Pull request 298 is draft, at this HEAD. Its verify check stops on the
step "Draft PRs do not run the full gate". Its quick check succeeded. I
did not run the full suite.
