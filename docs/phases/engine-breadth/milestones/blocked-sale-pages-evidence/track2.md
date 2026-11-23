# Track 2: Group prompts by answer target

## Saved model and renderer

The writer now emits `presentation-model.v3`. A question group is keyed by the
canonical answer fact type, version, and complete identity keys. It retains all
declaring input-question and source-closure-mapping producer references.
Blocked rows refer to groups with typed family or fact scopes and the status
for each scope. The v3 schema is additive in the derivation registry; the
published v1 and v2 schema files remain unchanged.

The closure walk preserves an exact missing fact ID through its memoized
frames. It links only the matching target group, so another per-statement
question with the same fact type and wording cannot be pulled in by type
alone. A type-level binding links only when the projection has one distinct
answer target for that type. The synthetic producer-path regression covers an
exact missing target beside a different current answer, an ambiguous type-only
binding that keeps its declared reason without a group link, and a unique
type-only binding that links safely.

When an answer target has a current recorded statement or lender label, the
projector saves that existing display label and the renderer shows it as card
context. It never displays the identity-key IDs. If no current statement or
lender label exists, the group carries no invented label. In that case cards
for the same wording, same affected line, and same scope status can still look
alike; that is the remaining display limit. The current v99 sale answer is
tax-year scoped and has no statement label to show.

Grouped blocked reasons remain one list item per original reason. When a
Line 21 reason links to multiple groups, its one `line21-reason-*` anchor is
kept on that item and contains all group links. A Chrome regression confirms
the Line 21 explanation link resolves to exactly one anchor with two group
links inside it.

## Review repair: ambiguous family scopes and equal wording

The source-authority coordinator rejects a mapped family with current horizon
chains in multiple scopes (`test_multiple_scopes_for_same_version_refuses`).
The projector can still be called directly with two horizon targets for one
family, so it now suppresses family links when the family trace resolves to
more than one answer fact. Its regression confirms the declared closure reason
is retained without ambiguous row links or groups.

Closure-group references now retain the indices of the closure reasons that
created them. If a selection blocker already has the same wording, it remains
its own labeled reason and is not linked to the closure prompt by text equality.
A focused projection-helper regression checks that case, and a Chrome check
confirms two independently labeled same-worded blockers remain visible without
prompt links.

## Synthetic saved-page evidence

The current coordinator path was exercised with the late noncovered sale
fixture and published core v99 (registry v98, release v98). Its saved page
contains one group for the shared closure answer, with both the
`input-question.v1` and `source-closure-mapping.v4` producer references. The
line 9 reference remains stale; the page retains the original separate amount
check explanation. The amount-check disposition remains blocked with
`DEPENDENCY_INVALID`. No line 9 amount is published.

The same-worded distinct-target page control renders two cards, each with its
recorded synthetic statement label, and does not show their raw statement
IDs. An exact-pinned v2 saved model still validates and renders no question
cards. The v1 projection removes group metadata and retains original row
reasons for existing readers and correction consumers.

## Verification

- `python -m mypy`: success, no issues in 529 source files.
- `python -m pytest -m "not live" -q`: 1,922 passed, 8 skipped, 5,936
  subtests passed in 16.81 seconds.
- `python -m pytest tests/test_schema_registry.py -q`: 14 passed.
- The exact-target test passed after adding the unique type-only binding
  control.
- The family-scope and duplicate-sentence helper regressions passed (2 tests,
  5.85 seconds); the source-authority multiple-scope refusal passed (1 test,
  4.66 seconds). The full v3 saved-page module passed (8 tests, 39.55 seconds).
- The Line 12d and line 6b card-renderer regressions passed (2 tests); the
  line21 top-level compatibility assertion passed; the CGD projection-mock
  controls passed (2 tests, 3 subtests); and the earlier-core v1 reader parity
  control passed (36 subtests).
- `git diff --check`: clean.

The full local suite was run before the final compatibility-test updates and
reported 7,361 passed, 25 skipped, and 33 failures in 1,773.88 seconds. Those
failures were the two page assertions that expected grouped questions inline,
the v3 top-level-key assertion, and mocked projection functions that did not
accept the new writer arguments. The exact affected tests and subtests were
rerun successfully as listed above. The full suite was not rerun after these
final updates, so this note does not claim a clean full-suite result or CI
result.

All captures and labels use synthetic demo data. No user data or generated
captures are committed.
