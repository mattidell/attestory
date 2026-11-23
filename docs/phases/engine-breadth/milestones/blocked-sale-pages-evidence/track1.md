# Track 1: Restore the stale Schedule D line 9 reason

## Bounded projection behavior

The projection now preserves the declared basis-not-reported closure question
beside the form field's existing blocked explanation only when all of these
conditions hold:

- The run adopted `tax.us.2025.package.core-calculations` v91 or later. The
  check uses the existing `adopted_package` input and has no upper version cap.
- The blocked field and producing rule are Schedule D line 9, and the line's
  complete missing-root set is the three noncovered long-term subtotals and
  their amount-check symbol.
- Each subtotal reaches the noncovered long-term member validation, which is
  blocked by `SOURCE_SET_UNCLOSED` for that family.
- The amount-check row is blocked by `DEPENDENCY_INVALID` and contains exactly
  one unresolved noncovered long-term transaction fact.
- The mixed dependency walk has no other unknown leaf, missing-list shape, or
  cycle.

The question text comes from the existing closure mapping. The second reason
is copied from the field's existing blocked explanation, so it continues to
explain that the amount check must pass. The existing memoized dependency walk
is retained. Other lines, other blockers, and runs on core v80–v90 keep their
previous reason behavior. No saved-model schema, content, rule, kernel,
renderer, or page-grouping change was needed.

The focused regression exercises the guard, rejects another transaction fact
and extra same-type transaction leaves, rejects empty or absent `missing`
lists and dependency cycles, and calls `build_presentation_model` for v90,
v91, and v99. It checks that v90 keeps no mixed reason while v91 and v99 show
both declared sentences.

## Coordinator and Chrome observations

These synthetic one-case observations used the real coordinator, saved model,
existing citation-walk renderer, and headless Chrome. They completed cleanup
in every run (Chrome `157.0.8103.79`, Node `22.23.2`). The current latest
published core in the branch is v99, adopted from `published-packages.v98`
and release v98.

| Run | Adopted core | Case | Schedule D result |
| --- | --- | --- | --- |
| `20261121T222731685006Z` | v91 / registry v89 / release v89 | `sale-answer-needs-reconfirmation` | Line 9 remains blocked. Model and DOM show the basis-not-reported question and the existing “waits for your answers … or for a recorded long-term sale … to pass its checks” explanation. The amount-check child remains blocked with `DEPENDENCY_INVALID` on the current `demo.ns.late` transaction. |
| `20261121T222708952947Z` | v99 / registry v98 / release v98 | `sale-answer-needs-reconfirmation` | Same two visible reasons and same unresolved amount-check child as v91. |
| `20261121T225814551605Z` | v99 / registry v98 / release v98 | `wage-unanswered-question` | Line 9 remains blocked with only the declared basis question. |
| `20261121T225839193874Z` | v99 / registry v98 / release v98 | `covered-basis-not-reported` | The covered-basis refusal remains unchanged. |
| `20261121T225901903314Z` | v99 / registry v98 / release v98 | `wage-single-noncovered-no` | Line 9 remains `closure_backed_zero` and renders `0`. |
| `20261121T225924544294Z` | v99 / registry v98 / release v98 | `covered-long-term-sale` | Line 8a remains `published_value` and renders `4000`. |

The stale-case model keeps the exact dependency records: Schedule D line 9 is
blocked with `DEPENDENCY_ABSENT` on the three subtotals and amount-check
symbol; the amount-check child is blocked with `DEPENDENCY_INVALID` on
`tax.us.2025.f1099b.noncovered-lt-txn|broker=demo.ns.late.broker,statement=demo.ns.late.statement,transaction=demo.ns.late.transaction,tax-year=2025`.
The page publishes no line 9 amount.

The current adopted-package threshold is tested through v100 so a future
version is not accidentally excluded. The actual v99 capture uses the latest
published core available on this branch; v100 is not currently bound by that
published registry.

## Verification and compatibility evidence

- `python -m mypy`: success, no issues in 528 source files.
- `pytest tests/test_noncovered_sales_admission.py`: 18 passed before the final
  extra same-type-leaf assertion; the final full suite below includes that
  assertion and the strict root-shape guard.
- The previously failing historical parity case
  `test_v82_matches_track0[t1_s1/honest]` passed in isolation (1 passed,
  16.96s).
- Final full suite on the corrected tree: 7,362 passed, 25 skipped in
  1,795.82 seconds.

An earlier full run on an intermediate tree, before the adopted-version gate
and exact-leaf checks, reported 38 failures, 6,938 passes, and 25 skips in
5,233.42 seconds. All 38 failures were historical projection parity
expectations from core v80–v88 that gained the new line-9 sentence. That run
identified the compatibility leak; the adopted-package gate corrected it.
The corrected full run and the isolated historical parity check are the
results for the present implementation.

All cases and transaction identities above are synthetic. The saved pages,
models, and browser traces remain under ignored `temp/sale-page-observation/`
run directories.
