# Track 1: published box 4 no handling

Source: HEAD `3c0527689d21e34c35ed2a3a8b302ebe74eedf3c` at orientation.
The block matched Git; the branch was 0 behind and 10 ahead of origin/main,
with no merged PR. The builder executed the five numbered charter items
in order, with a commit after each. No forbidden directory edit or
recording change was needed. No push or spawn occurred.

## Content and publication

Twenty content files are added: the 19 accepted prototype artifacts
(17 helpers, one vocabulary bundle and line 25b v9), byte-identical to
the final P0 scratch files, plus input-question.f1099b-box4 v2 with
Decision 7's exact words. The existing question fact type and answer
shape are unchanged. No published citizen was edited.

Core v94, registry v92 and release v92 were constructed with
`python3 -m tools.package_successor` on published v93. The registry is
add-only: 20 new citizens and one package. There are 18 added package
members and two replacements (line 25b and the amount question); the
entrypoint edits are the new vocabulary and the question replacement.
No inherited inconsistencies were reported. V94's companion and covered-
flag loader declarations equal v93's. The core allowlist test now includes
v94. All 96 frozen historical publication byte witnesses still match.
The publication chain is in track1-build.json and the explicit successor
edits are in track1-changes.json.

## Full replay and neighbours

The foreground command was `python3 tools/recorded_replay.py neighbour
v93 v94`, with 9 workers (CPU count minus one), an external part file and
track1-replay.json as output. Both cores were run anew on all 775 lists;
no P0 pins were substituted. Wall time: 1408.692 seconds.

| Classification | Lists |
| --- | ---: |
| Identical successful pins | 295 |
| Same error on both cores | 84 |
| Amount sentence only | 125 |
| Accepted no-without-amount next question | 271 |

There are zero changed numerical line values, row dispositions or
refusal codes; zero changed attachments, tax bases or presentation-validity
fields; and zero unexpected changes. The 271 next-question changes are
exactly P0's accepted class. Normalizing only the old amount sentence to
Decision 7's text gives P0-equivalent counts of 420 identical successes,
84 same errors and 271 next-question changes. The tool's numbers_changed
class for those 271 refers to a missing-list change on the line-25b row,
not a tax-value change. track1-classification.json retains each list's
classification and changed row/line names.

Track 0's nine computing neighbours were rerun in parallel on published
v93 vs published v94 with `track0.py --core v94 --neighbours-only`.
All nine pass, with 86 fields per page: 774 comparisons of value,
disposition and reason sentences, zero differences or added questions.
Wall time: 34.651 seconds. Full field snapshots
are in track1-neighbours.json. The new mode leaves P0's saved replay
and its metadata untouched. The machine report identifies the new
external Track 1 part for future reuse.

## Tests

`tests/test_box4_no_prompt_v94.py` has eight distinct act lists, each
run once on published v94 through live_coordinate_run, its presentation
projection and the saved HTML page's embedded model. It covers all eight
chartered scenarios, with hand payment values from the recorded 4500 W-2
withholding and zero or 200 of Form 1099-B withholding. It checks that
finishing the input list invents no amount or answer, and compares the
no-1099-B page with the saved v93 neighbour. It does not simulate the
projection or reconstruct the saved model.

The eight tests are marked live with measured calls of 6.59-21.13 seconds.
`tests/test_box4_no_prompt_v94_package.py` has seven fast tests for byte
identity, exact question words/shape, exact members/entrypoints, registry
add-only publication, release/loader integrity, historical bytes and the
16 subject-dispatch allowlist entries. The final isolated package run's
slowest reported call was 0.01 seconds, below the 3.0 second budget.

Both new modules ran with line6b-reason-evidence first on PYTHONPATH.
The live harness preloads the legacy line-12d probe/prototype names by
path through tests/evidence_loader.py before loading the independent
sale-family harness. The static module reads frozen JSON evidence and
imports no evidence code. The initial targeted command passed 34 tests:
8 live, 6 package, 5 touched core-allowlist, and 15 data-safety tests.
The later static-gate repair passed 14 targeted tests (the static checker
and all seven final package tests). The final seven-test package module
also passed with the unrelated evidence directory first on PYTHONPATH.
No live act list was repeated merely to confirm a deterministic result.

## Checks and deviation

The first fast lane found the 16 new subject-scoped helpers' subject
requirements. The expression-only checker intentionally ignores subject
metadata. These exact P0 rules retain the required subject for dispatch,
identity-key matching and the subject pin, while their expressions read
statement counts or joined answers instead of the sale value.

The dispatcher appends the subject input pin explicitly at
packages/derivation/subject_dispatch.py:555; the static scanner excludes
that top-level subject metadata from expression reads.

The additional file beyond the named core allowlist is
`tools/required_versus_read_allowlist.json`: 16 exact rule/version/symbol
entries with explicit reasons. The existing checker policy allows
by-design requirements; no wildcard, checker-code edit, content edit or
recording change was made. A package test enforces the narrow entries.
This is the recorded deviation, preserving the charter's required byte
identity. The first fast-lane result is retained in track1-checks.json.

Final checks:

- Initial targeted modules and touched allowlist: 34 passed in 29.36 s,
  including the new live module, with unrelated evidence first on PYTHONPATH.
- Static-gate repair: 14 passed in 1.37 s.
- Final package import-isolation check: 7 passed in 1.09 s.
- Fast lane: 1823 passed, 8 skipped in 15.48 s.
- `python3 -m mypy`: no issues in 507 source files.
- `python3 tools/envelope_scan.py --range github/main..HEAD`: passed.
- JSON/local-path, syntax and whitespace checks: passed at handoff.

CI verify remains the full-suite gate. No local result is presented as
a replacement for that required check. No full-suite re-run, release
merge or production readiness decision is claimed by this builder unit.
The addition-only currency boundary remains parked by Decision 8;
Track 1 changes neither that behavior nor the return-level question.
