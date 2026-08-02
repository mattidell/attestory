# Capital-Gain Distributions / Line 7a — Closing CI Type Recheck

Charter:
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-31-capital-gain-distributions-line7a-closing-ci-types-recheck.md`

Role: original author-independent Track-3 Repair Reviewer, Medium tier /
medium effort. This is a focused CI type recheck, not another Track-3
behavior review.

## Object and boundary

- Orientation resolved `HEAD` to
  `67ae897a8c722c57f490992a686b482c788b1b59`; `git rev-parse HEAD`
  independently matched it.
- Exact repair range:
  `ba581ad02ae99ba91dcc3f3b610d6377650e0f69..9d3627fd0cebe5092de1025a3d2ef62ffeefc8cd`.
  It contains exactly one commit. The repair commit's parent is exactly
  `ba581ad02ae99ba91dcc3f3b610d6377650e0f69`, and the current recheck-charter
  commit is its direct successor.
- After fetching, the branch was 21 commits ahead and 0 behind
  `origin/main`; the worktree was clean and not spent. PR #128 remained open
  at its pre-repair head.
- Scope ceiling: the exact diff, focused six-test module, and repository mypy
  command. No full-pytest rerun or broader Track-3 behavior review was
  performed.
- Independence: the committed repair, failed CI log, focused test, and prior
  `READY` record were measured directly. Builder reasoning and
  self-assessment were not consulted.
- Stop conditions checked: range/tip/ancestry drift; another changed file;
  changed JSON path/read/decoding/runtime value, fixture, assertion, test
  count, or semantics; global/module suppression, `type: ignore`, `Any`
  return widening, production-code change, or broad untyped escape;
  unattributable failure; governance interpretation; and real/private
  material. None fired.

## Credited evidence and original failure

PR #128 `verify` run `30615579462` at closing head
`2683a795c6e279aa37e65ec5d4e9ab03bc44ae83` records:

```text
Tests (pytest -n auto)  success
Types (mypy)            failure
Governance lint         skipped
Data-boundary scan      skipped
```

The failed mypy step reported exactly four errors in one file:

```text
tests/test_capital_gain_distributions_line7a_t3_presentation.py:20:
  Returning Any from function declared to return "dict[str, Any]"
  [no-any-return]
tests/test_capital_gain_distributions_line7a_t3_presentation.py:24:
  Returning Any from function declared to return "dict[str, Any]"
  [no-any-return]
tests/test_capital_gain_distributions_line7a_t3_presentation.py:28:
  Returning Any from function declared to return "dict[str, Any]"
  [no-any-return]
tests/test_capital_gain_distributions_line7a_t3_presentation.py:32:
  Returning Any from function declared to return "dict[str, Any]"
  [no-any-return]
Found 4 errors in 1 file (checked 141 source files)
```

The passed pytest step and the prior Track-3 F1/F2/F3 `READY` record remain
credited. This recheck does not reopen their behavior, mutation, golden,
harness, or safety measurements.

## 1. Exact range and one-file ceiling

The repair range contains one commit and one changed file:

```text
tests/test_capital_gain_distributions_line7a_t3_presentation.py
```

The diff is 5 insertions and 5 deletions:

- add `cast` to the existing `typing` import; and
- wrap each of the four existing `json.loads(...)` return expressions in
  `cast(dict[str, Any], ...)`.

No production file, other test, fixture, golden, content file, schema,
package, record, charter, pointer, or CI configuration changed.

## 2. Runtime equivalence

Each helper retains the same content path, `read_text("utf-8")`, and
`json.loads` call:

| Helper | Content file |
| --- | --- |
| `_field` | `form1040.line-7b.form-field.v2.json` |
| `_citation` | `citation.form1040.line-7b.json` |
| `_numeric_field` | `form1040.line-7a.form-field.json` |
| `_numeric_citation` | `citation.form1040.line-7a.json` |

An independent runtime probe patched `Path.read_text` and `json.loads` at
their existing call seams. For each helper it confirmed:

```text
same expected Path
encoding == "utf-8"
Path.read_text called once
json.loads called once with the read payload
helper returned the exact object supplied by json.loads
```

A sentinel measurement also confirmed
`typing.cast(dict[str, Any], sentinel) is sentinel`. `cast` therefore adds
static type information only; it performs no runtime conversion, copy,
validation, decoding, or mutation.

## 3. Test semantics and type closure

AST comparison between the repair base and repair tip found:

```text
test-inventory-identical count=6
assertion/control-structure-AST-identical
```

The exact diff contains no fixture, model helper, mutation, assertion, test
case, or test-name change. Direct search found no `type: ignore`, mypy or
module suppression, `noqa`, `# type` escape, or helper return widened to
`Any`. The sole new import is `typing.cast`; no production import or
production code changed.

Independent verification closed all four original errors:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t3_presentation
# Ran 6 tests in 4.717s — OK

python3 -m mypy
# Success: no issues found in 141 source files
```

The six tests still exercise the credited F1/F2/F3 categorical, citation,
numeric, legacy, golden, and disposition assertions unchanged.

## 4. Boundary and safety verification

The remaining charter commands produced:

```text
git rev-list --count \
  ba581ad02ae99ba91dcc3f3b610d6377650e0f69..9d3627fd0cebe5092de1025a3d2ef62ffeefc8cd
# 1

git diff --name-only \
  ba581ad02ae99ba91dcc3f3b610d6377650e0f69..9d3627fd0cebe5092de1025a3d2ef62ffeefc8cd
# tests/test_capital_gain_distributions_line7a_t3_presentation.py

git diff --check \
  ba581ad02ae99ba91dcc3f3b610d6377650e0f69..9d3627fd0cebe5092de1025a3d2ef62ffeefc8cd
# clean

python3 tools/governance_lint.py
# governance lint: conformant

python3 tools/envelope_scan.py --range main..HEAD
# clean (exit 0)
```

No full-suite or real-data operation was performed.

## Verdict

**READY**

All four `no-any-return` errors are closed by explicit local casts that are
runtime identity. The four helpers retain the same paths, UTF-8 reads,
decoding calls, and decoded objects; the six tests, fixtures, assertions, and
F1/F2/F3 semantics are unchanged; every file outside the focused test is
byte-identical across the repair; and mypy, focused tests, diff hygiene,
governance lint, and envelope safety are clean. No residual finding is
recorded.
