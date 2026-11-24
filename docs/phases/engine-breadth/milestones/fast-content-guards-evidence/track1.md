# Track 1 evidence: content guards run in the fast lane

## Inventory

`git grep -n st_size -- tests` finds every byte-size read. Five of those reads were content-file caps. Each of those modules is live because its source contains a live-lane token (`live_coordinate_run`, `live_workspace`, or `subprocess`), so conftest marks the whole module live and the fast lane skipped the cap.

| Module | Live | What it checked | Cap | Exceptions |
| --- | --- | --- | --- | --- |
| `tests/test_earned_income_credit_track1.py` `test_rule_files_stay_under_5kb` | yes | `rule.eic-*.json`, plus `rule.form1040-line27a.json`, `rule.form1040-lines28-31.json`, `rule.form1040-lines27-31-total.v2.json`, `rule.form1040-line32.v2.json` | 5,000 | two files at 7,000; reason below |
| `tests/test_eic_qualifying_children_track1.py` `test_rule_files_stay_under_5kb` | yes | `rule.eic-*.json` | 5,000 | the same two files at 7,000; the same reason |
| `tests/test_child_tax_credit_track1.py` `test_rule_files_stay_under_5kb` | yes | `rule.ctc-*.json` | 5,000 | none |
| `tests/test_other_dependents_credit_track1.py` `test_rule_files_stay_under_5kb` | yes | `rule.odc-*.json` | 5,000 | none |
| `tests/test_tax_on_taxable_income_track1.py` `test_worksheet_rules_stay_within_the_size_target` | yes | `rule.qdcg-worksheet.*.json`, and the names must equal `rule.qdcg-worksheet.line-N.json` for lines 4, 5, and 6 through 25 | 6,144 (`6 * 1024`) | none |

The reason written beside both earned-income checks:

> Core v99 writes the gate result v3 and the no-unsupported-situations answer v3 with indent=2; v2 of each was hand-compacted (the gate result v2 re-dumped the same way is 5,944 bytes). The growth is mostly formatting.

The other `st_size` reads are not content caps, and they stay in place:

| Location | Live | What it does |
| --- | --- | --- |
| `tests/test_line16_names_v95_package.py` | no | The citizen's byte length equals the recorded prototype row. |
| `tests/test_save_fold_equivalence.py` | no | The act log's length during a save. |
| `tests/test_member_reads_once.py` | no | A same-length rewrite keeps the same size. |
| `tests/test_f1099b_box4_only_v85.py` and `tests/test_f1099b_box7_loss_v84.py` | yes | A script main prints `fixture_bytes` for a generated fixture. |

## One fast guard

`tests/test_content_file_sizes.py` holds the union. Its source contains none of the live-lane tokens. One exception table records the file, the cap, and the reason:

| File | Cap | Reason |
| --- | --- | --- |
| `rule.eic-gate-result.v3.json` | 7000 | Core v99 writes the gate result v3 and the no-unsupported-situations answer v3 with indent=2; v2 of each was hand-compacted (the gate result v2 re-dumped the same way is 5,944 bytes). The growth is mostly formatting. |
| `rule.eic-answer.no-unsupported-situations.v3.json` | 7000 | Core v99 writes the gate result v3 and the no-unsupported-situations answer v3 with indent=2; v2 of each was hand-compacted (the gate result v2 re-dumped the same way is 5,944 bytes). The growth is mostly formatting. |

Every other file from the earned-income, child-tax-credit, and other-dependents globs, and the four named form lines, uses 5000. The worksheet names use 6144, and the glob must equal that name set (22 files). A file covered by more than one old guard would have to meet the smaller cap. No file was in two guards.

The five live modules no longer contain those tests.

## Union

The union has 148 files. The before list (the five guards above) and the after list (the fast module) are the same files at the same caps. Counts: 57 `rule.eic-*` files (55 at 5,000 and 2 at 7,000), 4 named form lines at 5,000, 50 `rule.ctc-*` files at 5,000, 15 `rule.odc-*` files at 5,000, and 22 worksheet files at 6,144.

| File | Cap |
| --- | --- |
| `rule.ctc-child-count.json` | 5000 |
| `rule.ctc-child.citizen-met.json` | 5000 |
| `rule.ctc-child.claimed-met.json` | 5000 |
| `rule.ctc-child.counts.json` | 5000 |
| `rule.ctc-child.counts.v2.json` | 5000 |
| `rule.ctc-child.joint-return-met.json` | 5000 |
| `rule.ctc-child.lived-with-you-met.json` | 5000 |
| `rule.ctc-child.no-support-met.json` | 5000 |
| `rule.ctc-child.other-claimant-clear.json` | 5000 |
| `rule.ctc-child.ssn-met.json` | 5000 |
| `rule.ctc-child.under-17-met.json` | 5000 |
| `rule.ctc-filer-gate.json` | 5000 |
| `rule.ctc-filer-ssn-gate.json` | 5000 |
| `rule.ctc-form1040-line19.json` | 5000 |
| `rule.ctc-sch8812-line-1.json` | 5000 |
| `rule.ctc-sch8812-line-10.json` | 5000 |
| `rule.ctc-sch8812-line-11.json` | 5000 |
| `rule.ctc-sch8812-line-12.json` | 5000 |
| `rule.ctc-sch8812-line-13.json` | 5000 |
| `rule.ctc-sch8812-line-14.json` | 5000 |
| `rule.ctc-sch8812-line-16a.json` | 5000 |
| `rule.ctc-sch8812-line-16b.json` | 5000 |
| `rule.ctc-sch8812-line-17.json` | 5000 |
| `rule.ctc-sch8812-line-18a.json` | 5000 |
| `rule.ctc-sch8812-line-19.json` | 5000 |
| `rule.ctc-sch8812-line-20.json` | 5000 |
| `rule.ctc-sch8812-line-21.json` | 5000 |
| `rule.ctc-sch8812-line-21.v2.json` | 5000 |
| `rule.ctc-sch8812-line-22.json` | 5000 |
| `rule.ctc-sch8812-line-23.json` | 5000 |
| `rule.ctc-sch8812-line-24.json` | 5000 |
| `rule.ctc-sch8812-line-25.json` | 5000 |
| `rule.ctc-sch8812-line-26.json` | 5000 |
| `rule.ctc-sch8812-line-27.json` | 5000 |
| `rule.ctc-sch8812-line-2d.json` | 5000 |
| `rule.ctc-sch8812-line-3.json` | 5000 |
| `rule.ctc-sch8812-line-4.json` | 5000 |
| `rule.ctc-sch8812-line-5.json` | 5000 |
| `rule.ctc-sch8812-line-6.json` | 5000 |
| `rule.ctc-sch8812-line-6.v2.json` | 5000 |
| `rule.ctc-sch8812-line-7.json` | 5000 |
| `rule.ctc-sch8812-line-8.json` | 5000 |
| `rule.ctc-sch8812-line-9.json` | 5000 |
| `rule.ctc-sch8812-part-ii-b-needed.json` | 5000 |
| `rule.ctc-spouse-gate.json` | 5000 |
| `rule.ctc-worksheet-a.line-1.json` | 5000 |
| `rule.ctc-worksheet-a.line-2.json` | 5000 |
| `rule.ctc-worksheet-a.line-3.json` | 5000 |
| `rule.ctc-worksheet-a.line-4.json` | 5000 |
| `rule.ctc-worksheet-a.line-5.json` | 5000 |
| `rule.eic-answer.age-25-under-65.json` | 5000 |
| `rule.eic-answer.age-25-under-65.v2.json` | 5000 |
| `rule.eic-answer.age-25-under-65.v3.json` | 5000 |
| `rule.eic-answer.main-home-in-us.json` | 5000 |
| `rule.eic-answer.main-home-in-us.v2.json` | 5000 |
| `rule.eic-answer.main-home-in-us.v3.json` | 5000 |
| `rule.eic-answer.no-qualifying-child.json` | 5000 |
| `rule.eic-answer.no-unsupported-situations.json` | 5000 |
| `rule.eic-answer.no-unsupported-situations.v2.json` | 5000 |
| `rule.eic-answer.no-unsupported-situations.v3.json` | 7000 |
| `rule.eic-answer.not-claimable-as-dependent.json` | 5000 |
| `rule.eic-answer.not-claimable-as-dependent.v2.json` | 5000 |
| `rule.eic-answer.not-claimable-as-dependent.v3.json` | 5000 |
| `rule.eic-answer.not-married.json` | 5000 |
| `rule.eic-answer.not-nonresident-alien.json` | 5000 |
| `rule.eic-answer.not-qualifying-child-of-another.json` | 5000 |
| `rule.eic-answer.not-qualifying-child-of-another.v2.json` | 5000 |
| `rule.eic-answer.not-qualifying-child-of-another.v3.json` | 5000 |
| `rule.eic-answer.separated-spouse.json` | 5000 |
| `rule.eic-answer.spouse-valid-ssn.json` | 5000 |
| `rule.eic-answer.taxpayer-valid-ssn.json` | 5000 |
| `rule.eic-child.age-met.json` | 5000 |
| `rule.eic-child.counts.json` | 5000 |
| `rule.eic-child.counts.v2.json` | 5000 |
| `rule.eic-child.joint-return-met.json` | 5000 |
| `rule.eic-child.other-claimant-clear.json` | 5000 |
| `rule.eic-child.relationship-met.json` | 5000 |
| `rule.eic-child.residency-met.json` | 5000 |
| `rule.eic-child.ssn-met.json` | 5000 |
| `rule.eic-column-count.json` | 5000 |
| `rule.eic-column.completed.json` | 5000 |
| `rule.eic-column.completed.v2.json` | 5000 |
| `rule.eic-column.phaseout-threshold.json` | 5000 |
| `rule.eic-column.phaseout-threshold.v2.json` | 5000 |
| `rule.eic-early-stop.json` | 5000 |
| `rule.eic-early-stop.v2.json` | 5000 |
| `rule.eic-eligibility.json` | 5000 |
| `rule.eic-eligibility.v2.json` | 5000 |
| `rule.eic-gate-result.json` | 5000 |
| `rule.eic-gate-result.v2.json` | 5000 |
| `rule.eic-gate-result.v3.json` | 7000 |
| `rule.eic-investment-income.json` | 5000 |
| `rule.eic-investment-income.v2.json` | 5000 |
| `rule.eic-qualifying-child-count.json` | 5000 |
| `rule.eic-questions-required.json` | 5000 |
| `rule.eic-questions-required.v2.json` | 5000 |
| `rule.eic-status-class.json` | 5000 |
| `rule.eic-status-class.v2.json` | 5000 |
| `rule.eic-table-key.json` | 5000 |
| `rule.eic-worksheet-a.line-1.json` | 5000 |
| `rule.eic-worksheet-a.line-2.json` | 5000 |
| `rule.eic-worksheet-a.line-2.v2.json` | 5000 |
| `rule.eic-worksheet-a.line-3.json` | 5000 |
| `rule.eic-worksheet-a.line-5.json` | 5000 |
| `rule.eic-worksheet-a.line-5.v2.json` | 5000 |
| `rule.eic-worksheet-a.line-6.json` | 5000 |
| `rule.eic-worksheet-a.line-6.v2.json` | 5000 |
| `rule.form1040-line27a.json` | 5000 |
| `rule.form1040-line32.v2.json` | 5000 |
| `rule.form1040-lines27-31-total.v2.json` | 5000 |
| `rule.form1040-lines28-31.json` | 5000 |
| `rule.odc-child-count.json` | 5000 |
| `rule.odc-child-marked-conflict.json` | 5000 |
| `rule.odc-child.counts.json` | 5000 |
| `rule.odc-child.counts.v2.json` | 5000 |
| `rule.odc-child.identity-met.json` | 5000 |
| `rule.odc-child.other-tests-met.json` | 5000 |
| `rule.odc-child.other-tests-met.v2.json` | 5000 |
| `rule.odc-dependent-present.json` | 5000 |
| `rule.odc-relative-count.json` | 5000 |
| `rule.odc-relative-marked-conflict.json` | 5000 |
| `rule.odc-relative.counts.json` | 5000 |
| `rule.odc-relative.tests-a-met.json` | 5000 |
| `rule.odc-relative.tests-b-met.json` | 5000 |
| `rule.odc-return-gate.json` | 5000 |
| `rule.odc-spouse-gate.json` | 5000 |
| `rule.qdcg-worksheet.line-10.json` | 6144 |
| `rule.qdcg-worksheet.line-11.json` | 6144 |
| `rule.qdcg-worksheet.line-12.json` | 6144 |
| `rule.qdcg-worksheet.line-13.json` | 6144 |
| `rule.qdcg-worksheet.line-14.json` | 6144 |
| `rule.qdcg-worksheet.line-15.json` | 6144 |
| `rule.qdcg-worksheet.line-16.json` | 6144 |
| `rule.qdcg-worksheet.line-17.json` | 6144 |
| `rule.qdcg-worksheet.line-18.json` | 6144 |
| `rule.qdcg-worksheet.line-19.json` | 6144 |
| `rule.qdcg-worksheet.line-20.json` | 6144 |
| `rule.qdcg-worksheet.line-21.json` | 6144 |
| `rule.qdcg-worksheet.line-22.json` | 6144 |
| `rule.qdcg-worksheet.line-23.json` | 6144 |
| `rule.qdcg-worksheet.line-24.json` | 6144 |
| `rule.qdcg-worksheet.line-25.json` | 6144 |
| `rule.qdcg-worksheet.line-4.json` | 6144 |
| `rule.qdcg-worksheet.line-5.json` | 6144 |
| `rule.qdcg-worksheet.line-6.json` | 6144 |
| `rule.qdcg-worksheet.line-7.json` | 6144 |
| `rule.qdcg-worksheet.line-8.json` | 6144 |
| `rule.qdcg-worksheet.line-9.json` | 6144 |

## Proof

`rule.ctc-worksheet-a.line-4.json` was 735 bytes, under the 5,000 cap. A scratch copy of those bytes was kept, and the content file was grown to 5,002 bytes. `pytest -m "not live" tests/test_content_file_sizes.py` failed:

```
AssertionError: rule.ctc-worksheet-a.line-4.json
assert 5002 <= 5000
```

The original bytes were written back. The file was 735 bytes again, and the same command passed.

`pytest -m "not live" --collect-only -q tests/test_content_file_sizes.py` collected `test_content_rule_files_stay_within_their_caps` (1 test). `pytest -m live --collect-only -q tests/test_content_file_sizes.py` deselected that test.

## Observer fix

`test_node_observer_emits_safe_manifest_stage_without_starting_chrome` still requires return code 2, empty stdout, `json.loads` of the whole stderr equal to the manifest failure record, and a formatted message that contains `stage=case-manifest` and `category=manifest`.

The child environment drops `FORCE_COLOR` and `NO_COLOR`. On Node v22.23.2 a warning is written on stderr ahead of the JSON when both variables are set, and also when `FORCE_COLOR` is empty and `NO_COLOR` is set. `FORCE_COLOR=1` alone leaves stderr as the single JSON object. `NO_COLOR=1` alone does the same. This session's environment had both set, which is the failure the test was hitting. Clearing the two variables in the child keeps the exact-stderr assertion. Taking only the JSON line out of stderr would have allowed the warning to remain, so that was not the change.

The test passed with `FORCE_COLOR=1`, with `NO_COLOR=1`, and with both.

## Checks

- Fast lane `pytest -m "not live"`: 1953 passed, 8 skipped, 5973 subtests passed in 17.42s.
- Edited live modules `tests/test_earned_income_credit_track1.py`, `tests/test_eic_qualifying_children_track1.py`, `tests/test_child_tax_credit_track1.py`, `tests/test_other_dependents_credit_track1.py`, `tests/test_tax_on_taxable_income_track1.py`, and `tests/test_sale_page_observation_diagnostics.py`: 139 passed, 195 subtests passed in 69.03s.
- `python3 -m mypy` on those seven test files: Success, no issues found in 7 source files.
- `python3 tools/envelope_scan.py --range github/main..HEAD`: exit 0.
