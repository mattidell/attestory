# Track 2 measurement — before and after, long history

Audience: Builder, reviewer.

Before: the tree before Track 2's code change (production code as at P0).
After: the Track 2 tree (the reuse plus its regressions).
Python 3.14.3. CPU is `time.process_time` (user plus system); wall is
`time.perf_counter`. Each figure is one in-process pass, once, in the order
shown, on the same long (307-act) history P0 built
(`temp/projection-reuse/histories/long`, reused unchanged).

Command: `python3 temp/projection-reuse/measure_track2.py before` /
`... after`. The script reuses `temp/projection-reuse/measure_p0.py`'s
histories, its `project`/`append`/`append_batch` counting wrapper, and its
`long_operations` builders unchanged; it adds one untimed, uncounted warm-up
call (`record-statement` on a throwaway copy) before the CPU loop, so the
first measured operation does not pay the cold package-validation cost P0's
own `build_short`/`build_long` already absorbed in-process. Raw output is
`temp/projection-reuse/track2-before.json` and `track2-after.json`.

## Project calls and acts folded

| Operation | Before calls | Before acts | After calls | After acts |
| --- | ---: | ---: | ---: | ---: |
| Record a statement | 4 | 1238 | 2 | 618 |
| Save or answer | 4 | 1273 | 1 | 307 |
| Correct an answer | 4 | 1231 | 1 | 307 |
| Withdraw an answer | 3 | 923 | 1 | 307 |
| Remove a statement | 4 | 1232 | 2 | 615 |
| Read a saved presentation | 1 | 307 | 1 | 307 |
| Live coordinate run | 1 | 307 | 1 | 307 |

The "before" row matches P0's own long-history table exactly (`p0-fold-attribution.md`,
"Project calls and acts folded"). Read a saved presentation and live
coordinate run are unchanged, as designed: neither touches a named Track 2
site (the one read-path call is `prepare_f1099k_statement_review`'s own
single fold through `review_f1099k_statement_with_saved_presentation`, which
already folded once before this track; the coordinator's own fold is Track 1
territory).

Record and remove each still show two calls: the one necessary fold for this
operation (`_ensure_bundles`'s own, or `prepare_f1099k_statement_review`'s own
fold reused by `retract_f1099k_statement_durably` for remove), plus
`append_batch`'s own checked prefix fold inside `ActLog.append_batch`
(`packages/kernel/act_log.py`) — Track 1, not touched by this track.

## CPU on the long history

Order is the table order (matches P0's).

| Operation | Before CPU s | Before wall s | After CPU s | After wall s |
| --- | ---: | ---: | ---: | ---: |
| Record a statement | 1.202 | 1.207 | 0.870 | 0.872 |
| Save or answer | 0.910 | 0.928 | 0.362 | 0.363 |
| Correct an answer | 0.785 | 0.789 | 0.224 | 0.225 |
| Withdraw an answer | 0.572 | 0.573 | 0.216 | 0.217 |
| Remove a statement | 0.757 | 0.758 | 0.407 | 0.408 |
| Read a saved presentation | 0.232 | 0.232 | 0.221 | 0.222 |
| Live coordinate run | 0.892 | 0.897 | 0.931 | 0.940 |

Wall stays within a few milliseconds of CPU on every row, so these figures
are compute, as in P0. The sum of the five touched operations' CPU is 4.226s
before and 2.079s after, about a 51% reduction. The sum of all seven
(matching P0's own "sum of the unrounded CPU figures") is 5.350s before
(P0 recorded 5.301s on its own pass; the two warm, in-process passes agree to
within run-to-run noise) and 3.231s after. Read a saved presentation and live
coordinate run — the two untouched rows — account for the small
run-to-run noise (0.011s and +0.039s) between before and after; neither is
attributable to this track's change.

## Limits

- One warm in-process pass each, same as P0's own CPU section. Not a share of
  suite CPU; the full suite was not run for this measurement (it is the
  merge gate, run separately).
- The acts-folded counts come from the same counting wrapper P0 used,
  unmodified; this script does not instrument anything beyond what P0 already
  built.
- Record and remove's two remaining folds are the save path's own checked
  prefix (Track 1) plus one necessary cold fold; Track 1 is out of scope for
  this unit and is not measured further here.
