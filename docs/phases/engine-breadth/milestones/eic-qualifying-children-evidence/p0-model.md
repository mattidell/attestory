# P0 — the qualifying-child model (Foreman record)

This replaces the rejected first attempt (`82ef8f7f`). The model below rests on
`child_dispatch_probe.py` beside this file, which builds a throwaway
publication surface and runs synthetic children (`demo-child-N`) through the
real coordinator (`packages.derivation.live.live_coordinate_run`). It writes
nothing under the repository. Sources are the ignored downloads under
`temp/tax-on-taxable-income/sources/`; text lines are cited as `file:line`.

## Law the model must carry

| Rule | Effect | Source |
| --- | --- | --- |
| Step 1 AGI limits by children with a valid SSN | 1: $50,434 ($57,554 joint); 2: $57,310 ($64,430); 3 or more: $61,555 ($68,675); none: $19,104 ($26,214) | `i1040gi-2025.txt:2644-2656` |
| Step 3 question 1 | The child meets the relationship, age, residency and joint-return tests to be the filer's qualifying child | `i1040gi-2025.txt:2669-2673`; tests in Pub. 596 ch. 2 |
| Step 3 questions 2-5 | Joint return skips to Step 5. Married filing separately or head of household while married: must not have shared a principal residence with the spouse for the last 6 months of 2025, or be legally separated and living apart at year end; otherwise stop | `i1040gi-2025.txt:2676-2700` |
| Step 3 question 6 | If the filer could be a qualifying child of another person, stop | `i1040gi-2025.txt:2703-2712` |
| Child SSN | A child without an SSN issued by the due date cannot be counted in figuring the credit | `i1040gi-2025.txt:2995-3001` |
| Self-only credit | A filer whose qualifying child has no valid SSN, and who is otherwise eligible, can claim the self-only EIC | `f1040sei-2025.txt` ("Qualifying child doesn't have an SSN") |
| More than one person | Only one person may claim the child; tie-breaker rules decide; a filer who loses the child may take the EIC under the rules for filers without a qualifying child | `i1040gi-2025.txt:2964-2990`; `p596-2025.txt:875-885` |

## What the probe shows

Three shapes over the same recorded children, on the real coordinator:

| Case | Chain | Flat (Form 1098 shape, alone) | Combined answer |
| --- | --- | --- | --- |
| Two children pass | 2 | 2 | 2 |
| Child 2 fails age | 1 | blocks | 1 |
| Child 2 has no valid SSN | 1 | blocks | 1 |
| Another person may claim child 2 | blocks | **2** | 2 |
| Child 2's residency unanswered | blocks | **2** | 2 (no residency answer exists) |
| Child roster not closed | blocks | blocks | blocks |
| Closed empty roster | 0 | 0 | 0 |

- **Chain** (recommended): one per-child rule per test, each with its own
  answer as subject; a per-child combining rule with the relationship answer
  as subject and the other per-test results joined by the shared child and
  tax-year keys; a return-level count over the per-child results using the
  existing `selection` with `reads_subject_results` and `collect` over a
  closed child-roster family. Each test is its own finding, so the
  explanation names the failing test for each child. A yes to "another person
  may also claim this child" blocks; it is never a count of 0.
- **Flat** is unsafe: alone it counts a child whose residency is unanswered
  and a child another person may claim. This matches the run-wide input
  fallback in `packages/derivation/subject_dispatch.py`; a per-subject rule
  that lists other per-subject answers as ordinary inputs can bind another
  subject's answer. Not used.
- **Combined answer** is safe but explains less: a failing child shows only
  "does not meet the tests".

No engine, schema or expression change is needed for the chain shape.

## Consequences for the contract

- The return-level answer `tax.us.2025.eic.no-qualifying-child` is replaced
  by the count of qualifying children with a valid SSN. A count of 0 (no
  children, or only children without a valid SSN, or none passing) takes the
  existing childless route, with its Step 4 tests. A count of 1, 2 or 3 or
  more takes the child column and the Step 3 filer tests.
- A child another person may also claim blocks the route: outside the class.
- The child count changes which completed amount the existing $0 stops use;
  the AGI stop at $68,675 still covers every column.
