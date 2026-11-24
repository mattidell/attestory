# Review: a refused head of household status does not set the worksheet ceilings

Reviewer, fresh context. Charter:
`docs/reviews/hoh-no-worksheet-ceilings/charter-review.md`. Object:
`github/main..HEAD` on `milestone/hoh-no-worksheet-ceilings-2025` at
`cd60ad006` (6 commits). Orientation block SHA matched `git rev-parse HEAD`.
Ratified line `origin/main` at `6dcec44f`: behind 0, ahead 6, not spent.
Draft PR #305. Governance was not read.

Scope understood: after a head of household or qualifying surviving spouse
"no", Qualified Dividends and Capital Gain Tax Worksheet lines 6 and 13 do
not show that status's ceiling, and every line that uses them follows the
2025 instructions for that filer. Every other recorded return keeps its
numbers. Non-goals: no change to which status a filer may claim or to the
tests, no kernel or engine change, no page change.

## Verdict

**READY with notes.** A refused or unanswered head of household or
qualifying surviving spouse blocks lines 6 and 13 and names the same answer
standard-deduction line 3 names. Yes keeps that status's 2025 ceiling.
Single, married filing jointly, and married filing separately keep v103's
published amounts and are not asked the test. Lines that read the ceilings
stay blocked. The page on a refused return still shows the status question,
and the refused ceiling digits are gone. The 775 recorded lists, all
single, replay with no unexpected difference and no number change.

Mechanical gate: PR #305 is a draft. On `cd60ad006`, `quick` passed and
`verify` stopped at "Draft PRs do not run the full gate", so the full suite
has not run on this head. This review does not anticipate that result.
`envelope_scan --range github/main..HEAD` exited 0.

## Findings

None.

## The box

What enters is the filing status and, only when that status is head of
household or qualifying surviving spouse, the filer's answer that the
status's tests are met. The authority for the ceiling amounts is the 2025
worksheet text, stored in the existing parameter tables. The authority for
using a head of household or surviving-spouse ceiling is that answer, the
same fact line 3 already requires. The rules may publish the status's own
ceiling, or block. They may not publish another status's ceiling. Single,
joint, and separate returns, and a "yes" on either tested status, keep the
numbers they had on v103.

A "no" and an unanswered answer are different states. "No" is a refusal
(`DEPENDENCY_INVALID`). An absent answer is not established
(`DEPENDENCY_ABSENT`). Both name the test fact. Neither publishes a ceiling.

## Sources

Fetched `https://www.irs.gov/pub/irs-prior/i1040gi--2025.pdf`. sha256
`482e9c487c608f1bbeaceef35bc3c0933e8b35443cfff447e4279d590468364a`, the
same digest `law.json` records. `pdftotext` without layout, then read:

- Filing status, lines 967-982: check only the status that applies; choose
  among the ones for which you qualify.
- Head of household, lines 1126-1146: check the box only if unmarried (or
  considered unmarried) and Test 1 or Test 2 applies.
- Qualifying surviving spouse, lines 1270-1291: the box, and joint-return
  rates, apply if all of the listed conditions apply. A spouse who died in
  2025 cannot file as qualifying surviving spouse.
- Worksheet lines 6 and 13, lines 4057-4073.

Line 6 is $48,350 single or married filing separately, $96,700 married
filing jointly or qualifying surviving spouse, $64,750 head of household.
Line 13 is $533,400 single, $300,000 married filing separately, $600,050
married filing jointly or qualifying surviving spouse, $566,700 head of
household. The worksheet names no other amount for a checked status the
filer does not qualify for. A block that names the existing question is the
instruction. Another status's ceiling is not.

`parameter.preferential-zero-ceiling.json:11-17` and
`parameter.preferential-fifteen-ceiling.json:11-17` hold those five
amounts. No other 2025 rule reads either parameter.

## Each successor

`rule.qdcg-worksheet.line-6.v2.json` and
`rule.qdcg-worksheet.line-13.v2.json` are `rule-artifact.v17`, version v2,
`requires` only `filing_status` (lines 11-13). Their `value` trees match
`rule.dependents-worksheet-line-3.v2.json` except the parameter id: head of
household compares `tax.us.2025.hoh.tests-met` to yes and otherwise blocks
`DEPENDENCY_INVALID` naming that fact (line 6 at lines 60-66); qualifying
surviving spouse does the same with `tax.us.2025.qss.tests-met` (lines
112-118); every other status keeps the v1 parameter lookup. An absent
answer fails the comparison and the live row is `DEPENDENCY_ABSENT` naming
the fact, the same codes line 3 produces.

Live pins on v104: a head of household or surviving spouse "yes" pins the
test answer; single, married filing jointly, and married filing separately
pin filing status and the parameter only. Published symbol values on those
five returns (yes, single, joint, separate, and a "no" later corrected to
"yes") are identical on v103 and v104, including the tax:

| Return | Line 6 | Line 13 | Tax |
| --- | --- | --- | --- |
| head of household, yes | 64,750 | 566,700 | 2,825 |
| qualifying surviving spouse, yes | 96,700 | 600,050 | 1,853 |
| single | 48,350 | 533,400 | 3,875 |
| married filing jointly | 96,700 | 600,050 | 1,853 |
| married filing separately | 48,350 | 300,000 | blocked |

The status question's phrase count on a refused page is 20 for "no" and 19
when the answer is missing, on both cores. Single, joint, separate, and
"yes" pages show it zero times. A filer is not asked a new question.

Changing the answer displaces the ceiling. On v104, yes-then-no blocks both
lines and drops 64,750 and 566,700 from current publications. No-then-yes
publishes 64,750, 566,700, and tax 2,825. An unanswered head of household
log that later asserts yes publishes the same three amounts.

## Downstream

On a refused or unanswered return the only disposition changes from v103
are lines 6, 7, 13, and 14. Lines 6 and 13 block as above. Lines 7 and 14
stay `DEPENDENCY_ABSENT` and add the ceiling symbol to `missing`
(`rule.qdcg-worksheet.line-7.json:11-14` requires taxable income and line
6; line 14 requires taxable income and line 13). Lines 8, 22, 24, and 25,
and `rule.form1040-line16` v9, keep v103's blocks. Line 16 remains blocked
on taxable income, worksheet line 24, and worksheet line 25. Standard
deduction v3 still requires line 3, which is blocked on the same answer, so
taxable income is absent on these returns. No traced number changes.

The rendered page for Form 1040 lines 12e and 16 on a refused return
contains the status question and does not contain the refused ceiling
digits. On v103 those digits occur once each (64,750 and 566,700, or
96,700 and 600,050). Married filing separately still shows its own 48,350
and 300,000 once, on both cores.

## Nothing else moved

Core v104's members equal v103 except lines 6 and 13, which move from v1
on `rule-artifact.v14` to v2 on `rule-artifact.v17`. Entrypoints and the
other package fields match. Registry v102 adds those two citizens and the
v104 package row; every older row is unchanged. Release v102 differs from
v101 in `version` and `package_registry_sha256`, and that digest is the
v102 registry file. No schema file and no previously published content file
is modified. The v1 rule files are untouched.

`packages/tax/loader.py:278` and `loader.py:853` add v104 entries.
`test_v104_loader_entries_carry_v103_unchanged` passed: the companion
declaration, the covered-flag map, and the three package switches equal
v103. `tests/test_content_file_sizes.py:53-54` names both successors. The
worksheet filename set equals the on-disk `rule.qdcg-worksheet.*.json`
glob (`test_content_file_sizes.py:96-98`). Both files are under the 6,144
cap (4,224 and 4,251 bytes).

`version_change` in `tools/recorded_replay.py` matches only a `version` or
`pinVersion` attribute moving from the old version to the new one. A value
change does not match it, so the declared expectations cannot hide one.
Census of the recorded lists: 775, all single. Independent replay of
published v103 against published v104, all 775 lists: 691
`expected_changes` (success/success), 84 identical (error/error), 0
failing, 0 unexpected differences, `number_change_lists` empty. Expectation
counts: package version 358,053, line 6 version 2,073, line 13 version
2,073.

## Tests

`tests/test_hoh_no_worksheet_ceilings_v104.py` runs the nine returns through
`live_coordinate_run` and checks disposition, code, missing fact, and
published amount. Three scratch mutants of the published successors, the
mutations in that file, each failed the check they target:

- A refused head of household whose block is replaced by the lookup
  publishes 64,750 and 566,700.
- The same refusal pointed at the single key publishes 48,350 and 533,400.
- Replacing the single, joint, and separate lookup with a block leaves both
  lines blocked on a single return.

`tests/test_hoh_no_worksheet_ceilings_v104_package.py`,
`tests/test_content_file_sizes.py`, and
`tests/test_noncovered_sales_v78_switch.py`: 11 passed.

## What I ran

- `tools/build_orientation_block.py --ref HEAD --charter docs/reviews/hoh-no-worksheet-ceilings/charter-review.md --role reviewer`
- `git fetch origin --prune`; `tools/foreman_context.py --ref HEAD --format json`
- IRS 2025 Form 1040 instructions, sha256 above, `pdftotext` without layout
- `python3 tools/envelope_scan.py --range github/main..HEAD` (exit 0)
- `pytest tests/test_hoh_no_worksheet_ceilings_v104_package.py tests/test_content_file_sizes.py tests/test_noncovered_sales_v78_switch.py` (11 passed)
- Nine `live_coordinate_run` returns on v103 and v104, plus yes-then-no,
  no-then-yes, and an unanswered head of household log that later asserts
  yes. Wages 50,000, withholding 4,500, standard deduction, no qualified
  dividends and no sale. Demo ids only.
- The three mutant checks in `tests/test_hoh_no_worksheet_ceilings_v104.py`
- `replay_track1.py` over all 775 recorded lists (wall 440.6s)
- `gh pr checks 305` and the failed `verify` log
