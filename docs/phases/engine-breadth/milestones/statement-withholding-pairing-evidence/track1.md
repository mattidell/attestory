# Track 1: pair each statement with its own withholding answer

Core v77. This file is the record of the operation, the schema, the rules,
and the cases.

## What landed

`require_paired` is a guard in `packages/derivation/evaluator.py`. It reads
the identity keys of the current rows of the named income fact types and of
the named withholding fact type. It reads no values. A withholding row with
no income row is not a failure. A null or missing key blocks
`DEPENDENCY_INVALID` and names that finding id. An uninstalled row slot
blocks `DEPENDENCY_INVALID` with `link-coverage-scope-unbound`. An income
row whose key has no withholding row blocks `DEPENDENCY_ABSENT` and names
the withholding fact type, so the existing input question for that amount
still shows. The rows it read are recorded on
`AccessLog.require_paired_findings` and pinned as inputs. The runner
installs the row slot from current sources, including sources appended
during the run.

`rule-artifact.v15` adds only the `require_paired` node.
`artifact-package.v40` admits that schema. The derivation manifest adds
those two filenames and leaves every earlier checksum in place. ADR 0083
records the contract at status proposed.

Line 25b v5 and line 25a v3 are `rule-artifact.v15` successors. Each keeps
the prior version's value, requires, pins, blocked, citations, and scope.
The when closures stay, and the count comparisons are now `require_paired`
on `statement` (line 25b, ten income fact types) and `w2-slip` (line 25a).
Core v77, registry v75, and release v75 admit them. The loader shares v76's
companion declaration.

## Cases

Amounts are line 25b, except the W-2 rows, which are line 25a. A block
names the withholding fact type. The question shown is that fact's existing
input question, on the line's section. v76 figures are the recorded probe.
Three v76 rows were run again on this engine and matched that record:
`int.both-answered`, `int.offset`, and `w2.second-slip-unanswered`.

| Row | v76 | v77 | Question shown |
| --- | --- | --- | --- |
| `cross.int-answered-div-open` | block f1099div.box4-withholding | block f1099div.box4-withholding | 1099-DIV box 4 |
| `div.answered-plus-orphan` | 67.0 | 67.0 | — |
| `div.both-answered` | 60.0 | 60.0 | — |
| `div.box12.answered` | 7.0 | 7.0 | — |
| `div.box12.unanswered` | 0.0 | block f1099div.box4-withholding | 1099-DIV box 4 |
| `div.box2a.answered` | 7.0 | 7.0 | — |
| `div.box2a.unanswered` | 0.0 | block f1099div.box4-withholding | 1099-DIV box 4 |
| `div.box7.answered` | 7.0 | 7.0 | — |
| `div.box7.unanswered` | block f1099div.box4-withholding | block f1099div.box4-withholding | 1099-DIV box 4 |
| `div.offset` | 47.0 | block f1099div.box4-withholding | 1099-DIV box 4 |
| `div.one-unanswered` | block f1099div.box4-withholding | block f1099div.box4-withholding | 1099-DIV box 4 |
| `div.same-statement-second` | unreachable | unreachable | — |
| `g.answered-plus-orphan` | 1007.0 | 1007.0 | — |
| `g.both-answered` | 1000.0 | 1000.0 | — |
| `g.offset` | 607.0 | block f1099g.box4-withholding | 1099-G box 4 |
| `g.one-unanswered` | block f1099g.box4-withholding | block f1099g.box4-withholding | 1099-G box 4 |
| `g.same-statement-second` | unreachable | unreachable | — |
| `int.answered-plus-orphan` | 87.0 | 87.0 | — |
| `int.both-answered` | 80.0 | 80.0 | — |
| `int.box10.answered` | 7.0 | 7.0 | — |
| `int.box10.unanswered` | 0.0 | block f1099int.box4-withholding | 1099-INT box 4 |
| `int.box3.answered` | 7.0 | 7.0 | — |
| `int.box3.unanswered` | 0.0 | block f1099int.box4-withholding | 1099-INT box 4 |
| `int.box8.answered` | 7.0 | 7.0 | — |
| `int.box8.unanswered` | 0.0 | block f1099int.box4-withholding | 1099-INT box 4 |
| `int.offset` | 57.0 | block f1099int.box4-withholding | 1099-INT box 4 |
| `int.one-unanswered` | block f1099int.box4-withholding | block f1099int.box4-withholding | 1099-INT box 4 |
| `int.same-statement-assert` | 7.0 | 7.0 | — |
| `int.same-statement-second` | unreachable | unreachable | — |
| `int.zero-is-an-answer` | 50.0 | 50.0 | — |
| `ira.answered-plus-orphan` | 2007.0 | 2007.0 | — |
| `ira.both-answered` | 2000.0 | 2000.0 | — |
| `ira.offset` | 1207.0 | block f1099r.ira-box4-withholding | 1099-R box 4 |
| `ira.one-unanswered` | block f1099r.ira-box4-withholding | block f1099r.ira-box4-withholding | 1099-R box 4 |
| `ira.same-statement-second` | unreachable | unreachable | — |
| `ssa.answered-plus-orphan` | 1307.0 | 1307.0 | — |
| `ssa.both-answered` | 1300.0 | 1300.0 | — |
| `ssa.offset` | 807.0 | block ssa1099.box6-voluntary-withholding | SSA-1099 box 6 |
| `ssa.one-unanswered` | block ssa1099.box6-voluntary-withholding | block ssa1099.box6-voluntary-withholding | SSA-1099 box 6 |
| `ssa.same-statement-second` | unreachable | unreachable | — |
| `w2.both-answered` | 5300.0 | 5300.0 | — |
| `w2.offset` | 4600.0 | block w2.box2-withholding | W-2 box 2 |
| `w2.same-slip-second` | 9999.0 | 9999.0 | — |
| `w2.second-slip-unanswered` | block w2.box2-withholding | block w2.box2-withholding | W-2 box 2 |
| `no-1099` | line 25a 4500.0, line 25b 0.0 | same | — |
| `joint-one-statement-per-spouse` | line 25b 80.0 | same | — |

A second withholding member on the same keys is still rejected before the
run. An ordinary later assertion on those keys still publishes the current
amount.

## Suite

`python3 -m mypy` on the 13 changed Python files: Success, no issues found.
Fast lane `pytest -m "not live"`: 1650 passed, 8 skipped, 3942 subtests passed.
Full suite `pytest`: 4308 passed, 24 skipped, 8066 subtests passed. No earlier
golden or byte output moved.

## Limitations

Pins are the finding ids the guard examined. They do not add the companion
pins a `count` or `collect` would have added. An unclosed family still blocks
as `SOURCE_SET_UNCLOSED` and does not also name the withholding ref. The
measured rows were already closed, so the question shown is the withholding
question. ADR 0083 is proposed.

## Review repair

`test_two_income_boxes_one_answer_publishes_forty` runs box 1 and box 3 on
`demo.fw.int.stmt.0` with box 4 of 40, on v76 and v77. Both publish line 25b
40.0 with no line 25 block. On v77 the finding that carries that box 3 fact
id is an input pin of the published line 25b finding.
`test_closed_empty_income_family_publishes_the_withholding`
runs no box 1 row, that family closed, and one box 4 of 7, on both cores.
Both publish line 25b 7.0 with no line 25 block. ADR 0083 now says a pass or
an absent-withholding block records every examined finding id, and a null or
missing key records only the offending ids.
