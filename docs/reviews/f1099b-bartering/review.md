# Review: a Form 1099-B bartering amount is not lost (core v97)

Reviewer: fresh context, author-independent. Object: `github/main..HEAD` on
milestone/f1099b-bartering-2025 at `1fc9fa35` (9 commits, 0 behind). Charter:
`docs/reviews/f1099b-bartering/charter-review.md`. Governance not read.

## Verdict

**READY with notes** on the semantics. The publication gate is not met yet:
`verify` has not run on `1fc9fa35` (BART-R1). The change does what Decision 1
says it does. Five byte-minimal question successors, nothing else in the
package, registry add-only, release changed only in version and digest, loader
v97 equal to v96. A filer who reads the unanswered question and answers yes
is refused, and the tests fail on each mutation the charter names. The
milestone's guarantee is narrower than the scope sentence: the sentence
reaches only a filer whose lines 2a-6 answers are still missing (BART-R2), and
after a yes the page does not say why the return stopped (BART-R3). Neither
makes a published number wrong. Both should be stated plainly before closeout.

## Findings (ordered by consequence)

**BART-R1 (gate, blocking publication only).** PR #292 is a draft. On head
`1fc9fa35` the `verify` check is FAILURE with "Draft PR: the full suite has not
run on this head". `quick` (fast lane, 1900 passed) is green. The full suite,
mypy and governance_lint have not run on this candidate. Repair: mark the PR
ready and merge only on a green exact-head `verify`. This record does not
anticipate that result.

**BART-R2 (medium, semantic/claim scope).** The new sentence reaches only a
filer whose five lines 2a-6 facts are not yet answered. The projection draws
an input question only as the reason for a `DEPENDENCY_ABSENT` root
(`packages/derivation/presentation_projection.py:664`). A return whose answers
already exist never shows the question. Failure scenario: a filer recorded
the lines 2a-6 answer as "absent" under v96's wording (or recorded every
scope answer before running, which is how all 775 recorded lists look). That
filer holds a box 13 amount and runs v97. The return computes line 9 50,000
and refund 625, the bartering income is still left out, and the sentence is
never seen (probe `alone/as-asked` on v97 is exactly this state). Separately,
the census claim "No recorded return is silently wrong by this milestone's
test" (`f1099b-bartering-evidence/p0.md:247-248`, echoed in
`f1099b-bartering.md:102`) is vacuous. Box 13 has no fact type, so no list
could carry one, and the census cannot tell whether a recorded filer held a
box 13 amount. Repair: state in the plan that v97 protects a filer only when
the question is first asked. Restate the census as "cannot be determined from
the recorded lists" instead of "none is wrong".

**BART-R3 (medium, communication; foreman-decided).** After a yes, the page
says only "No value is published because a completeness or guard condition is
not satisfied." (`packages/content/tax/2025/schedule1.line-10.form-field.v5.json:28`).
Lines 8 through 37 carry generic blocked sentences, and `reason_sentences` is
empty (`probe-v97-q.json`, `alone/business`, `sale/business`). The refusal is
honest because no number is shown. But nothing on the page says the return
stopped because the filer reported business or bartering income this engine
does not compute. Decision 1 declined variant qf for a stated reason. Repair:
record it as an open item (qf's line 10 sentence once its first clause is
verified). No change is needed in this milestone.

**BART-R4 (low, plan/parked list currency).** The parked list still reads
"Form 1099-B box 13 bartering, whose refusing answer is not established"
(`docs/phases/engine-breadth/engine-breadth-roadmap.md:1224`). The plan says
box 13 cannot be recorded (`f1099b-bartering.md:79`, `:115`) but does not name
it as remaining work. The gaps in R2 and R3 are not parked anywhere. Repair
at closeout: replace the parked line with three items. (a) Box 13 cannot be
recorded, so the engine cannot detect it. (b) Existing answers are not
re-asked. (c) The refusal sentence does not name the cause.

**BART-R5 (low, evidence).** The live test does not pin that the page draws
one sentence. `tests/test_f1099b_bartering_v97.py:95-96` keeps only sentences
that contain the new text. Measured in a scratch copy: the farm v2 question
without the sentence, with a consistent registry checksum and release digest.
The page then drew two near-identical sentences (the v1 wording and the v2
wording), and `test_box_13_unanswered_shows_the_new_sentence_on_the_page`
still passed. The fast test
(`test_each_successor_is_its_predecessor_plus_the_sentence_and_a_version`)
catches it, so this is defence in depth only. Repair: assert
`len([s for s in reasons if s.startswith("In 2025, did you receive alimony")]) == 1`.

**BART-R6 (low, semantic, accepted by Decision 2/3).** The facts are absence
facts ("yes asserts the named excluded source ... is absent",
`schedule1-part1-scope.bundle.json` titles). The question asks "did you ...?",
and the sentence adds "answer yes". The filer's yes must be recorded as the
fact's "no". No code makes that mapping. The probe hand-encodes it
(`f1099b-bartering-evidence/probe.py:137`, `_set(acts, BUSINESS, "no", ...)`).
Measured: flipping that one literal to "yes" makes `alone/business` and
`sale/business` compute line 10 = 0 (live test fails at
`tests/test_f1099b_bartering_v97.py:83`). That is a silently short return. The
same inversion is the convention across all `no-*` scope questions, so it
predates this milestone, but the milestone's guarantee rests on it. Related
accepted semantics:
- The same sentence appears on the alimony, other-gains, rental and farm
  questions. If one of those is the only one left unanswered, a yes records
  "alimony present" (or another wrong class) for a barter. Only refusal reads
  it, so no number is wrong.
- A non-business barter is recorded through a line 2a-6 fact rather than the
  line 8z answer.
- Barter reported on "a similar statement" (Pub. 525) or not on any form is
  not named. A business barter is still covered by the question's existing
  "income from a business", and a non-business one by the 8a-8z question.

Repair: none in scope. Name the mapping in the plan so any future entry
surface for these questions inverts it deliberately.

## The charter's questions

1. **The sentence.** It is true in every drawn state checked. Box 13 of 0 is
   "no" ("above zero" matches the Form 1099-B instruction not to report
   negatives). A barter beside a sale refuses the whole return, sale included,
   which is honest. A non-business barter is covered ("even if you do not
   think of it as a business"). A barter not on a Form 1099-B is not named,
   but the existing wording covers it (R6). Shown in every page state, it
   appears once when the five are identical. In a partially answered state it
   appears on whichever sibling is missing (R6). After the refusal the page
   does not say why (R3).
2. **Silently wrong.** Yes, through recorded or pre-v97 answers (R2) and
   through an uninverted recording of the answer (R6). The box 13 gap is
   stated in the plan but not in the parked list (R4).
3. **Publication.** Verified. Only `A` paths under `packages/content` and the
   release directory, plus the `M` loader and the re-pinned switch test. No
   published file is modified. The successor-graph fallback for v97 selects
   the v96 entry (`packages/derivation/package_validation.py:2902-2906`). v97
   changes none of its four interest members, so no new entry is needed. The
   loader's v97 covered-flag map and companion declaration are textually
   identical to v96's. No other exact-version key mentions v96.
4. **Replay and tests.** `replay-published-v97.json`: 775 pass, 0 unexpected.
   One expectation was used (package version, narrow `identity` and exact
   before/after). Six expectations went unused, all exact-string or exact-id
   patterns, so none could swallow an unrelated change. This supports
   "nothing else changed" for the 691 lists that compute. The 84 lists that
   error identically on both cores never reach the page, so they are not
   evidence. The replay cannot exercise the change itself (no list leaves
   these facts unanswered). The probe covers that. Mutations are listed below.

## What I ran

- `python3 tools/build_orientation_block.py --ref HEAD --charter ... --role reviewer`.
  The SHA `1fc9fa35` matches `git rev-parse HEAD`. After
  `git fetch github`, `git rev-list --left-right --count github/main...HEAD`
  reported 0 behind and 9 ahead.
- `git diff --name-status github/main..HEAD`. Read all five v1/v2 question
  pairs, the loader diff, both new test files, `probe.py`, `p0.md`,
  `track1.md`, `census.json`, the replay summary and expectations, the
  presentation question walk and the successor-graph table.
- `pytest tests/test_f1099b_bartering_v97.py tests/test_f1099b_bartering_v97_package.py tests/test_noncovered_sales_v78_switch.py tests/test_schema_registry.py`:
  37 passed.
- `python3 tools/envelope_scan.py --range github/main..HEAD`: exit 0, no
  output.
- `gh pr view 292`: draft. `verify` FAILURE (draft guard), `quick` SUCCESS.
- Mutations, all in a `git archive` scratch copy outside the repository and
  none committed:
  - M1, farm v2 question without the sentence. Fast:
    `test_each_successor_...` and `test_registry_v95_is_add_only` fail.
    Live, with the checksum and digest made consistent: the unanswered test
    passes and the page draws two sentences (R5).
  - M2, the business yes recorded as fact "yes": both `sale/business` and
    `alone/business` refusal tests fail (`computed_zero`, 0) (R6).
  - M3a, v97 pins `rule.schedule1-line10` v2 with the checksum recomputed:
    `test_core_v97_replaces_exactly_...` fails.
  - M3b, an extra registry citizen: the registry and release tests fail.
  - M3c, an extra v97 entrypoint with the checksum recomputed: the members
    and entrypoints test fails.
  - The full suite was not run (CI is the gate of record, R1).
