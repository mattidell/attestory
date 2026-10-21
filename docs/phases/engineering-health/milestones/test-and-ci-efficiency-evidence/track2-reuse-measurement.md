# Track 2 measurement — schema check and historical lattice

Audience: Builder, reviewer.

One ordinary run of each case before the code change, and one after. The before figures are the tree before the Track 2 change (`packages/` and `tests/` as at the P0 ranking). The after figures are the Track 2 tree. Python 3.14.3, pytest 9.1.1. Raw logs and the profile stay under `temp/test-and-ci-efficiency/`.

## Ordinary CPU

`/usr/bin/time -p python3 -m pytest -q <node id>`. CPU is user plus system.

Form 1098 production: `tests/test_f1098_production_review_repair.py::F1098ProductionReviewRepairTests::test_named_outside_cases_and_three_justified_zeros_keep_their_dispositions`

Student-loan correction session: `tests/test_sli_correction_session.py::Correction4AttributionByIdentity::test_d1_each_answer_carries_its_own_borrowing_before_and_after_correcting_autumn`

| Case | Point | Pytest | Wall | User | System | CPU |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Form 1098 | Before | 101.49s | 102.22s | 105.70s | 2.53s | 108.23s |
| Form 1098 | After | 49.31s | 49.91s | 53.97s | 2.13s | 56.10s |
| Correction session | Before | 29.38s | 30.06s | 34.73s | 1.43s | 36.16s |
| Correction session | After | 23.03s | 23.67s | 28.42s | 1.42s | 29.84s |

Form 1098 CPU fell by 52.13s (48.2%). The correction session fell by 6.32s (17.5%). Both runs passed. These two cases are not a whole-suite figure.

## Call counts

Single-process profile of the same Form 1098 test: `python3 -m cProfile -o <ignored path> -m pytest -n 0 -q <node id>`. Profiled time is diagnostic. It is not the ordinary CPU above.

| Count | Before | After |
| --- | ---: | ---: |
| `check_schema` from the fact-type check | 60732 | 36 |
| `_validate_fact_type` calls | 60732 | 60732 |
| `_declared_edges` / `compute_currency` calls | 26356 | 26356 |
| Historical lattice constructions | 26356 | 7920 |

Before, every `_declared_edges` call built a lattice through `facts_of`. After, that function is still called 26356 times. The historical memo built 7920 lattices (`_project_fact_lattice` from its `for_state`, which also covers the other 72 historical `facts_of` calls in this profile). Registry `check_schema` during schema load stayed 148.

The fact-type path still enters the check on every adoption. Only the successful `check_schema` call is skipped. Currency still walks the record on every call. Only the historical lattice build is skipped when the fact state is the same object.
