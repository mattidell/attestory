# Review: content guards run in the fast lane

Reviewer: fresh context. Charter:
`docs/reviews/fast-content-guards/charter-review.md`. Object:
`github/main..HEAD` at `c9312013056d86679e63794430367ea7411b0c7b`
(verified against Git). Branch `milestone/fast-content-guards-2025`,
0 behind and 6 ahead of `github/main`. The range also carries the
plan, the track evidence, and the charters. The review object is the
test diff. Governance was not read.

## The box

Rule-file bytes under `packages/content/tax/2025` enter through four
globs and four named files. The authority for each cap is the guard
that `github/main` already ran in a live module. The box may fail a
test. It publishes no tax result. Package, rule, schema, projection,
kernel, and page behavior stay outside, as do the live-marker
heuristic and the fast-lane budget in `tests/conftest.py`. The other
`st_size` uses in tests stay where they are.

## Verdict

**READY with notes.** The fast module checks the same 148 files at
the same caps, with both raised-cap reasons kept. It is collected
under `-m "not live"`, and it fails when a covered file grows past
its cap and when a new `rule.qdcg-worksheet.*` file appears. Clearing
`FORCE_COLOR` and `NO_COLOR` in the observer child leaves the
assertions on the manifest record as they were. One low evidence note
is below.

Publication gate, measured on this head: PR #303 is a draft.
`quick` succeeded. `verify` is red because the job stops at "Draft
PRs do not run the full gate" and does not run the suite. This record
does not predict a later `verify`.

## Findings

**FCG-R1 (Low, evidence).** The new comment at
`tests/test_sale_page_observation_diagnostics.py:134-137` says the
assertions require the JSON record to be the whole stderr. They do
not. `json.loads` at line 157 accepts trailing whitespace. A scratch
copy of `tools/presentation_harness/sale-page-observation.mjs` that
writes a second newline after the record (the script's own write is
line 93) still passes. Extra stderr text `EXTRA` fails with
`JSONDecodeError: Extra data` at line 2. Stdout `noise` fails
`assert result.stdout == ""` at line 156. Clearing the two color
variables does not change those assertions. With both variables set,
Node writes a warning ahead of the JSON and `json.loads` of that
combined stderr fails; the test removes both names from the child so
that warning is absent. Consequence: the test still rejects a second
message, and it accepts whitespace after the one record. Repair:
compare stderr to the canonical JSON plus the one newline the script
writes, or narrow the comment to that.

## Same guard

Reconstructed from `github/main` and compared with
`tests/test_content_file_sizes.py` `covered_caps()` on the current
tree. The maps are equal: 148 files, no name only on one side, no cap
mismatch.

| Guard on `github/main` | Files | Cap |
| --- | --- | --- |
| `tests/test_earned_income_credit_track1.py:288-303` `rule.eic-*.json`, plus the four named Form 1040 files | 57 glob matches, 4 named | 5,000; the two names below at 7,000 |
| `tests/test_eic_qualifying_children_track1.py:350-360` `rule.eic-*.json` | the same 57 | the same 5,000 / 7,000 |
| `tests/test_child_tax_credit_track1.py:320-322` `rule.ctc-*.json` | 50 | 5,000 |
| `tests/test_other_dependents_credit_track1.py:295-297` `rule.odc-*.json` | 15 | 5,000 |
| `tests/test_tax_on_taxable_income_track1.py:553-560` `rule.qdcg-worksheet.*.json` | the closed line set | 6,144 |

The two exceptions are `rule.eic-gate-result.v3.json` and
`rule.eic-answer.no-unsupported-situations.v3.json`. Both reasons in
`tests/test_content_file_sizes.py:17-32` match the `github/main`
comment text in the earned-income guard, including the 5,944-byte
note. The qualifying-children guard used the same exception tuple.
`_WORKSHEET_LINES` on `github/main` is `(4, 5, *range(6, 26))`, and
`WORKSHEET_LINES` is that tuple. The on-disk
`rule.qdcg-worksheet.*.json` set equals those 22 names. No glob
overlaps another. Counts by cap: 124 at 5,000, 22 at 6,144, 2 at
7,000. Every covered file is present and within its cap.

The removed functions checked only those rule globs and the four
named rule files. No removed guard checked a non-rule file or a
different glob. `git grep st_size -- tests` on this head also hits
`tests/test_line16_names_v95_package.py:50` (byte identity of two
prototype rules), `tests/test_f1099b_box4_only_v85.py:606` and
`tests/test_f1099b_box7_loss_v84.py:541` (a printed fixture size),
`tests/test_member_reads_once.py:98` (same size after an edit), and
`tests/test_save_fold_equivalence.py:163` (the save path's length).
Those are unchanged from `github/main` and are not content caps. The
same `git grep` on `github/main` shows the five guards above and
those same other uses.

A new `rule.eic-*.json` is inside the glob. A 3-byte
`rule.eic-review-probe.json` passes. The same name at 5,002 bytes
fails `assert 5002 <= 5000`. The child-tax and other-dependents globs
are the same kind of loop (`tests/test_content_file_sizes.py:67-74`).

## Fast and honest

`tests/test_content_file_sizes.py` contains none of the live-source
tokens in `tests/conftest.py:41-46`. On the worktree,
`pytest -m "not live" tests/test_content_file_sizes.py` collected and
passed that one test, with the fast-lane budget hook active. The call
stayed inside the 3.0s budget, because a longer call would have
failed the run. `pytest -m live tests/test_content_file_sizes.py`
collected nothing (pytest exit 5).

A scratch copy of the module and the covered files, selected with
`-m "not live"`, passed. Growing `rule.eic-early-stop.json` from
4,930 bytes to 5,001 bytes failed at
`tests/test_content_file_sizes.py:85` with `AssertionError:
rule.eic-early-stop.json` and `assert 5001 <= 5000`. Adding a 3-byte
`rule.qdcg-worksheet.line-99.json` failed the set equality at line 81.
The worktree files were not modified. The scratch run used
`--noconftest` so the worktree autouse harness was not imported; the
assertion that failed is the body of this test. The marker result
above is from the worktree conftest.

## Observer test

`tests/test_sale_page_observation_diagnostics.py:138-152` copies the
environment and drops `FORCE_COLOR` and `NO_COLOR` before the same
Node command. The return code, empty stdout, `json.loads` of stderr,
the four-field record, and the formatter checks at lines 155-172 are
the assertions that were already on `github/main`.

In this environment both variables are set to `1`. Running the
manifest command directly then prints Node's `NO_COLOR` / `FORCE_COLOR`
warning and then the JSON record, and exits 2. `json.loads` of that
combined stderr fails. With both names unset, stderr is the one JSON
record plus a newline and stdout is empty. The worktree test, run
with both variables still set in the parent, passed: 1 passed. A
scratch copy of the unchanged script passed the same test. FCG-R1 is
the whitespace case. Extra stderr text and any stdout fail, as
measured above.

## Nothing else moved

`git diff --name-only github/main..HEAD` is the plan, the track
evidence, the two charters, `tests/test_content_file_sizes.py`, the
observer test, and deletion of the five guards from the live modules.
`tests/conftest.py` has an empty diff. No path under `packages/`
changed. The caps and the exception reasons match the reconstruction
above. `python3 tools/envelope_scan.py --range github/main..HEAD`
exited 0.

The full fast lane and the full suite were not rerun here. The
builder's pass count is not this review's measurement.

## What I ran

- `git rev-parse HEAD`, `git status --short`, `git rev-list --left-right --count github/main...HEAD`, `git merge-base --is-ancestor github/main HEAD`
- `git diff --stat` and `git diff --name-only github/main..HEAD`, and the test diff
- `git grep -n st_size` on `HEAD` and on `github/main` for `tests`, plus `git grep` for `6 * 1024`, `stay_under_5kb`, `over_5kb_formatting`, and `assertLessEqual` with `st_size` on `github/main` under `tests`, `packages`, and `tools`
- A reconstruction of the five guards compared with `covered_caps()`
- `python3 tools/envelope_scan.py --range github/main..HEAD` (exit 0)
- `pytest -m "not live" tests/test_content_file_sizes.py` (1 passed) and `pytest -m live tests/test_content_file_sizes.py` (no tests collected, exit 5)
- `pytest tests/test_sale_page_observation_diagnostics.py::test_node_observer_emits_safe_manifest_stage_without_starting_chrome` with `FORCE_COLOR=1` and `NO_COLOR=1` in the parent (1 passed)
- The Node manifest command with both color variables set, and again with both unset
- Scratch copies, `--noconftest -m "not live"`, of the size module: unchanged tree (pass); `rule.eic-early-stop.json` at 5,001 bytes (fail); new 3-byte `rule.qdcg-worksheet.line-99.json` (fail); new 3-byte `rule.eic-review-probe.json` (pass); that probe at 5,002 bytes (fail)
- Scratch copies of the observer test: unchanged script (pass); extra stderr text (fail); stdout `noise` (fail); a second trailing newline (pass)
- `gh pr list` and the `verify` job steps for PR #303 at this head
