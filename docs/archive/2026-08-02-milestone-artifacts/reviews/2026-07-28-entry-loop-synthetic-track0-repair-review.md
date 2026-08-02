# Review — The Entry Loop (synthetic), Track 0 repair recheck

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-28-entry-loop-synthetic-track0-repair-review.md`
- Branch: `milestone/entry-loop-synthetic`, at `4cb7372`
- Under review: `4d8e7cb` — repair of
  `docs/phases/legible-entry/entry-usability-criteria.md`
- Prior review: `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-28-entry-loop-synthetic-track0-review.md`
  (`NOT READY`, F1–F8)

## Orientation and review object

`python3 tools/build_orientation_block.py --ref HEAD` resolved reviewer at
`4cb73724b857be96c778f6aa2309773626b7dbb6`, which matches `git rev-parse
HEAD`. After fetching, this branch is zero commits behind and eight commits
ahead of its derived ratified line, `origin/main-ui`. The opening-plan PR #109
is merged, but the branch is not spent.

The review object is exactly `4d8e7cb`: one documentation-file change, with no
product, schema, prototype, matrix, or phase-state change. This is a focused
delta recheck; the previous review remains the finding set.

## Verdict: NOT READY

F1–F4 and F6–F8 close, and none of the three measurements that previously
passed regressed. F5 closes only partially. The repair correctly says that an
evaluation fixture must make every expected-impact member change and every
untouched-comparison member remain unchanged, and that the evaluation cannot
run otherwise. That is a fourth run prerequisite, but the dependency list then
says the evaluation cannot run until its *three* listed dependencies are
demonstrated. The first listed dependency (all required non-W-2 facts seeded,
with W-2 the only missing family) does not imply the required mutation pattern.

The procedure therefore has an explicit fail-closed condition but an
incomplete list of its own dependencies. A Track 2 conductor could demonstrate
the three listed conditions, believe the instrument runnable, and only then
discover that the chosen fixture cannot satisfy criteria 3.2 and 4.2. Name the
fixture's required expected-impact/untouched-comparison mutation pattern as a
run dependency (or make it an explicit part of the seed dependency) before
rerunning this review.

## F1–F8 recheck

| Finding | Result | Evidence checked |
| --- | --- | --- |
| F1 — 3.3 mechanical but uncheckable | **Closed** | Criteria 3.2, 3.3, and 4.2 define fixed W-2 expected-impact and untouched-comparison sets. Criterion 3.3 now requires the surface to show each named comparison member as unchanged after accepted W-2 Box 1 input. Scoring needs no prediction of what a person might expect. The omission note honestly limits the claim to the fixed set rather than pretending to cover every possible expectation. |
| F2 — ambiguous aggregation | **Closed** | The five dictated aggregation rules appear once, verbatim in substance: evaluator-level Pass/Fail; split to Disputed; Pass/Pass for every mechanical and no Fail/Fail for judgement; disputed mechanical fails; disputed judgement escalates without failing. No other pass rule contradicts it. |
| F3 — incomplete ADR-0046 disposition | **Closed** | The document carries the complete blast-containment adaptation, accessibility baseline, and prohibition on derived or diagnostic values fed by invalid, blocked, or not-yet-accepted input. It still gives explicit entry-specific reasons for zero-authority and absence-of-key not carrying over. |
| F4 — under-specified mechanical criteria | **Closed** | 1.2 requires each missing item to take the evaluator directly to its input; 2.2 supplies a field-attached minimum; 3.2 and 4.2 use the fixed sets; 5.2 specifies no missing facts, no further required-fact prompts, a distinct review/done state, and retained correction access. |
| F5 — dependencies stated as facts | **Partially closed** | The three original unconfirmed dependencies are now clearly named and expressly not confirmed by Track 0. However, the new fixture mutation condition is independently load-bearing and is not included in that list; see verdict. |
| F6 — evaluator method only exemplified | **Closed** | Exactly two independent evaluators are required, with fixed Builder and Reviewer briefs, non-conference, common evidence pack, and transcript obligations. |
| F7 — missing builder verification record | **Closed** | `4d8e7cb` records its worked-from SHA, full verify sequence, repair-range safety scan, diff check, and omissions. Reviewer reruns below corroborate the static and safety claims. |
| F8 — submission posture out of scope | **Closed** | Criterion 5.2 now requires a review/done state and never calls for submission or filing. |

## Regression recheck

### Implementation independence — PASS

The fixed W-2 evaluation sets specify observable effects that the surface must
accomplish; they do not prescribe a component tree, layout, URL, widget,
interaction sequence, or explanation schema. Requiring visible change status
and resulting values for named lines is content-level evaluation evidence, not
a requirement that the surface contain a particular panel or representation.

### Scope — PASS

The repair remains documentation only. Its added specificity concerns scoring,
accessibility outcomes, and a synthetic evaluation fixture. It neither defines
a per-field explanation schema nor changes product, derivation, admission,
artifact, correction-authority, or maturity scope.

### Five-step coverage — PASS

The five original groups remain present: missing-fact guidance (1), field
context before input (2), accepted/change/unchanged evidence (3), correction
(4), and a zero-missing computed done state (5). The repairs add floors; they
do not remove a step or narrow W-2 coverage below the prior instrument.

## Runnability and standing question

Aside from the incomplete dependency enumeration above, the instrument is now
materially more executable by a fresh evaluator: it specifies independent
roles, a common evidence pack, transcripts, a binary evaluator score, a unique
aggregation rule, and a fail-closed fixture condition. The earlier likely
failure — a judgement split over criterion 3.3 — is no longer the likely point
of failure. The most likely Track 2 failure is fixture construction: it may
not make all five expected-impact lines change while preserving all four
comparison lines. Until that condition is recorded alongside the other run
dependencies, the instrument can fail too late and ambiguously.

## Verification and data safety

- Commit-message verification record: present in `4d8e7cb`, including base
  `bd7211c`, `pytest -n auto`, `python3 -m mypy`, governance lint, repair-range
  envelope scan, and whitespace check.
- Reviewer rerun: `python3 -m mypy` reported no issues in 131 source files;
  `python3 tools/governance_lint.py` reported conformant; the repair-range
  envelope scan exited 0 with no output; and `git diff --check 4d8e7cb^
  4d8e7cb` was clean.
- Reviewer test rerun: `pytest -n auto` collected 687 items and progressed
  through 94% during live capture. The runner yielded before returning the
  process exit status; its process subsequently exited and the local
  `lastfailed` cache was empty. This is corroboration, not a substitute for
  the commit's recorded full-suite result.
- Reviewer data-safety scan: `python3 tools/envelope_scan.py --range main..HEAD`
  exited 0 with no output.

No criteria were edited in this review.
