# Track 1: worksheet ceilings on core v104

Of the scripts and JSON files this note names, only `trace.py` and `design.py`
are kept (the tests load them); the others and their raw output were
working artifacts and are not kept. The numbers below are their record.

Published core v104, registry v102, release v102, from published v103.
The two successors are the P0 content route. A claimed head of household
or qualifying surviving spouse that does not meet that status's tests, or
that has not answered, blocks worksheet lines 6 and 13 and names the
existing answer. Yes keeps the published lookup. Single, married filing
jointly, and married filing separately keep the v1 lookup. No engine,
schema, projection, or page change.

## Files

New citizens, under the 2025 content directory:

| File | Bytes | sha256 |
| --- | --- | --- |
| `rule.qdcg-worksheet.line-6.v2.json` | 4,224 | `84e0093914d162830cb391d8fd808dee1200803c8c8ba457bde62baa87c665b9` |
| `rule.qdcg-worksheet.line-13.v2.json` | 4,251 | `1c01c3eeccd59d4ab61dee9cc6f646ffabca62455e0c6b534946e8fee25e630e` |

Both are under the 6,144 worksheet cap. The size guard's exact filename
set now includes these two names. The unversioned v1 files stay published
history and were not edited.

`package.core-calculations.v104.json` is 241,297 bytes, file sha256
`a0fa81f0b3c51e8ee0ab566b2509ac2ffa8b624ab109a761a99b8b3cd1118eb4`,
package checksum
`a0674a370d8e966df2bff3044269fae39b524192500f2bc579c37d3887f7fc5e`.
`published-packages.v102.json` is 321,646 bytes, sha256
`e2a1d0755359c82a6302c969349a79adc6135b2c218d4cf0f946c0ed4b45d566`.
Both are larger than 200 KB because v103 and v101 already are. The
registry adds the two v2 citizens and the v104 package row. Older rows
are unchanged. Release
`demo.release.sli-worksheet-integration.2025.v102.json` is 211 bytes,
sha256
`8a4a861b4b43f2be3df23dcf8812a1927420108b5b4f5d38a53decbe3bbc6450`,
and differs from v101 only in version and the v102 registry digest.
Package v104's members equal v103 except lines 6 and 13, which move from
v1 on rule-artifact v14 to v2 on rule-artifact v17. The v104 loader
entries carry v103's covered-flag map and companion declaration. No
schema manifest changed. Published v103, v101, and the v1 rules were not
edited.

## Trace

`trace.py --core v104` writes `trace-v104.json`. Nine synthetic demo
returns: wages 50,000, withholding 4,500, the standard deduction, no
qualified dividends and no sale. Every run stops saturated. Rule ids
below are `tax.us.2025.rule.` plus the short name.

| Return | Line 6 | Line 13 | Line 7 | Line 14 | Line 3 | Form 1040 line 16 |
| --- | --- | --- | --- | --- | --- | --- |
| hoh, yes | 64,750 | 566,700 | 26,375 | 26,375 | 23,625 | 2,825 |
| hoh, no | `DEPENDENCY_INVALID`, `hoh.tests-met` | same | blocked; missing adds line 6 | blocked; missing adds line 13 | `DEPENDENCY_INVALID`, `hoh.tests-met` | blocked |
| hoh, unanswered | `DEPENDENCY_ABSENT`, `hoh.tests-met` | same | blocked; missing adds line 6 | blocked; missing adds line 13 | `DEPENDENCY_ABSENT`, `hoh.tests-met` | blocked |
| qss, yes | 96,700 | 600,050 | 18,500 | 18,500 | 31,500 | 1,853 |
| qss, no | `DEPENDENCY_INVALID`, `qss.tests-met` | same | blocked; missing adds line 6 | blocked; missing adds line 13 | `DEPENDENCY_INVALID`, `qss.tests-met` | blocked |
| qss, unanswered | `DEPENDENCY_ABSENT`, `qss.tests-met` | same | blocked; missing adds line 6 | blocked; missing adds line 13 | `DEPENDENCY_ABSENT`, `qss.tests-met` | blocked |
| single | 48,350 | 533,400 | 34,250 | 34,250 | 15,750 | 3,875 |
| married filing jointly | 96,700 | 600,050 | 18,500 | 18,500 | 31,500 | 1,853 |
| married filing separately | 48,350 | 300,000 | blocked, taxable income absent | blocked, taxable income absent | 15,750 | blocked |

On a refused or unanswered status, Form 1040 line 16 is blocked on
taxable income, worksheet line 24, and worksheet line 25. Lines 7 and 14
stay blocked and now also name the ceiling. Married filing separately
still publishes its own ceilings and blocks lines 7 and 14 only on
taxable income. No traced return changes a published number from the P0
yes and control rows.

The page still carries the existing status question. The trace cuts each
stored sentence at 500 characters, before "cannot file as", so
`question_on_page` is empty. The full page text contains the phrase 20
times on a "no" and 19 times when the answer is missing. The
married-filing-separately page shows the comma forms 48,350 and 300,000
once each.

## Replay

`replay_track1.py` compares published v103 with published v104
(`replay-v104.json`). Expectations are line 6 v1 to v2, line 13 v1 to v2,
and the package v103 to v104. A numeric change does not match them.

All 775 recorded lists pass. 691 are success on both cores and carry the
expected version changes. 84 are error on both cores with the same
snapshot. Zero lists fail. Zero expectations are unused. Zero lists change
a number.

## Tests

`tests/test_hoh_no_worksheet_ceilings_v104_package.py` checks that the
published successors match the P0 design, that v104 replaces only those
two pins, that the registry is add-only, that the release digest is the
v102 registry file, and that the v104 loader entries equal v103.
`tests/test_content_file_sizes.py` admits the two v2 names at the
worksheet cap and still requires the filename set to match exactly.
`tests/test_noncovered_sales_v78_switch.py` includes v104 in the
covered-flag list because the loader entry carries v103's map.
`tests/test_hoh_no_worksheet_ceilings_v104.py` runs the nine cases through
`live_coordinate_run`.

Three scratch mutants of the published successors fail those checks. A
refused head of household that publishes its own ceilings shows 64,750 and
566,700. A refused head of household that falls back to the single ceiling
shows 48,350 and 533,400. A single return whose lookup blocks shows both
lines blocked.

The package, size, and covered-flag tests passed together (11 passed).
The live module passed (12 passed). `pytest -m "not live"` passed (1,979
passed, 8 skipped, 5,997 subtests). `python3 -m mypy` reported no issues
in 543 source files.
