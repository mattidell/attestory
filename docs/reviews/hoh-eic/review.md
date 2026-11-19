# Review: the earned income credit for a head of household (core v99)

Reviewer, fresh context. Charter: `docs/reviews/hoh-eic/charter-review.md`.
Object: `github/main..HEAD` on milestone/hoh-eic-2025, head `d0a9a87f`
(orientation block SHA verified against Git; 0 behind, 6 ahead of
`github/main` `d3a65aff`; draft PR #295, not merged). Governance was not read.

## Verdict: NOT READY

The arithmetic is right and well tested: a married head of household with no
counted child cannot reach a credit above $0, an unmarried one gets the single
amounts, the other statuses keep v98's numbers, and every mutant I built was
caught. Two things stop it. First, v99 newly requires a head of household
with no counted child to answer the other Step 4 questions too, and a married
one who answers "no" still has line 27a and the refund lines blocked until
they also answer age and main home. The page shows no question for either
(EIC-R1). Second, the gate of record has not passed on this head (EIC-R2).

## Findings

### EIC-R1 (Medium; semantic and compatibility): a married head of household who answers "no" is blocked, with no sentence, until they also answer Step 4 questions 2-6

- Claim violated: "a married head of household (considered unmarried)
  without a qualifying child still gets no credit" (plan scope), and P0's
  "ordering them needs more successors for no change in any number"
  (`hoh-eic-evidence/p0.md:288-291`). Step 4 question 1 is a STOP (i1040gi
  2025, Step 4, question 1): a married head of household is never asked
  questions 2-6.
- Where: `rule.eic-status-class.v2.json:64-80` moves a head of household with
  no counted child to class 1. That makes `eic.questions-required` 1 at
  credit-possible incomes, so `rule.eic-answer.age-25-under-65`,
  `main-home-in-us`, `not-claimable-as-dependent`,
  `not-qualifying-child-of-another` and `no-unsupported-situations` are all
  required. `rule.eic-gate-result.v3.json:83-95` requires every one of them,
  including after `eic.answer.not-married` is 0.
- Reproduced (published v99, P0's probe return through `live_coordinate_run`
  and the saved page, with one answer removed):
  - hoh/parent/7000 answered no, `eic.age-25-under-65` absent: lines 27a and
    34 blocked. 11 rules are blocked (`eic-answer.age-25-under-65`, gate,
    eligibility, line 27a, lines 32-37, the 27-31 total), and the page has
    **no sentence**.
  - The same with `eic.main-home-in-us` absent: the same result.
  - On v98 this return computes line 27a $0 and line 34 350 with nothing
    asked. So a filer the instructions stop at question 1 goes from a
    computed refund to a silently blocked one.
  - Unmarried (yes) with age absent also blocks silently. A single filer
    behaves the same way on v99 (same blocked set, no sentence), so the
    missing age and main-home questions are an existing gap. v99 newly
    extends it to every head of household with no counted child.
- Why the evidence missed it: `hoh-eic-evidence/probe.py:115` pre-answers
  age and main home on every case. All 775 recorded lists are single filers,
  who already had to give these answers (`census.json`). So neither P0's
  paired probes nor the replay could see the new requirement. On charter
  question 2 ("is anyone newly asked a question ... besides the two intended
  cases?"): yes. A head of household with no counted child at an income where
  the credit could be above $0 is now required to give five more credit
  answers. Two of them (age, main home) have no input question.
- Smallest repair that closes it at the property level: when
  `eic.answer.not-married` is 0, the Step 4 question 2-6 answers must not be
  required. For example, successors of those answer rules publish 1 (not
  required) when the not-married answer is 0, the way they already do for
  "not required". That is a foreman scope decision: more successors. The
  alternative is to accept the behaviour as a recorded decision, correct
  p0.md and track1.md, and pin it in a live test (married-no with age absent
  shows the blocked lines). Either way, add a live test that leaves an
  answer the probe currently pre-fills unanswered.

### EIC-R2 (Medium; publication gate): no green gate on the reviewed head

- PR #295 at `d0a9a87f`: `quick` failed with two fast-lane budget overruns in
  tests the range does not touch:
  - `tests/derivation/test_bounded_nominee_selection_contract.py::BoundedNomineeRuntime::test_path_pin_version_origin_and_identity_are_admission_contracts`
    (3.5 s)
  - `tests/test_market_discount_interest_contracts.py::SuccessorPackageContracts::test_md_n10_mixed_successor_graph_rejects_older_fields`
    (3.0 s)
- `verify` did not run ("Draft PRs do not run the full gate").
- Track 1 ran the full suite before the size re-pin and only the two
  affected modules after it (`track1.md:98-110`).
- Locally both tests pass (4.08 s and 1.67 s with `-n 0`). The first is over
  the 3.0 s budget even locally, so it may be load growth from another
  package version rather than noise. This is not a semantic defect, but the
  candidate cannot be READY until `verify` is green on the exact head.

### EIC-R3 (Low; evidence accuracy): the size-cap raise is needed, but its stated reason is wrong

- Where: `tests/test_earned_income_credit_track1.py:300-301`,
  `tests/test_eic_qualifying_children_track1.py:357-358` and
  `hoh-eic-evidence/track1.md:113-114` attribute the 6,742 bytes to "one
  more level in the else-chain, which indents every level below it".
- Measured:
  - v2 (4,747 bytes) was hand-compacted, with one pin object per line.
    `design.py` `dump()` writes v3 with `json.dumps(indent=2)`.
  - v2 re-dumped the same way is 5,944 bytes, already over 5,000.
  - The semantic addition costs about 800 bytes at that format
    (5,944 to 6,741).
  - Minified, v3 is 3,870 bytes.
  - In v2's compact style, v3 would still be about 5.3-5.7 KB (estimated
    with a line-width formatter).
- Which: the raise is honest in substance. A ten-answer chain does not fit
  5,000 bytes in either house style, and the rule should not be made smaller
  for its own sake. The stated cause should be corrected (mostly
  formatting). A smaller design was available: the not-married check could
  sit in an `eic-eligibility-result` successor (v2 is 1,921 bytes) and leave
  gate v2 untouched. It would not fix EIC-R1, because eligibility requires
  the gate result.

### EIC-R4 (Low; wording): the not-married question does not tell a filer separated only by a written agreement to answer no

- Where: `packages/content/tax/2025/input-question.eic-not-married.v1.json:7`.
  The yes list says "legally separated ... under a decree of divorce or
  separate maintenance". The no list names living apart and "considered
  unmarried", but not a written separation agreement without a decree.
- Source: Pub. 501 (2025), Marital Status, "Considered married" test 3:
  "married and living apart but not legally separated under a decree of
  divorce or separate maintenance".
- Scenario: the sibling separated-spouse question
  (`input-question.eic-separated-spouse.v1.json:7`) and Step 3 question 5
  both call a written separation agreement "legally separated according to
  your state law". A filer with only such an agreement can read "legally
  separated" as yes and receive a credit they are not entitled to.
- Repair: add "or you were separated under a written separation agreement
  but no decree" to the no list. The fact title can carry the same.

## Charter questions

**1. The two questions against the sources.** Source PDFs match P0's sha256
values (i1040gi `482e9c48...`, Pub. 501 `288b62a4...`, Pub. 596 `29e8c669...`).

- Step 4 question 1: matches the instructions (i1040gi line 27a, Step 4,
  question 1, a STOP for a "married taxpayer" filing separately or as head
  of household).
- The separated-spouse question restates Step 3 questions 3-5 accurately.
  It also agrees with "Special rule for separated spouses" (i1040gi,
  Definitions) and Pub. 596 Rule 3. Its "no" says "you cannot take the
  credit, so it is $0".
- Pub. 501 (Head of Household, after "Considered Unmarried") says directly:
  "You may be considered unmarried for the purpose of using head of
  household status but not for other purposes, such as claiming the EIC."
  That is a sharper source for the married-head-of-household rule than the
  Pub. 596 community-property sentence P0 cites.
- Cases:
  - Spouse died in 2023, not remarried: yes, matching Pub. 501's
    year-of-death rule by implication.
  - Annulment: yes (Pub. 501 "Annulled marriages").
  - Decree of separate maintenance: yes (Pub. 501 "Unmarried persons"). The
    instructions' Step 3 question 5 wording is the tension P0 recorded, and
    Decision 3 settles it.
  - Married, living apart under no agreement: no, named explicitly.
  - Interlocutory decree: no, in the fact title. The question covers it by
    "divorce ... was final".
  - Nonresident-alien spouse (considered unmarried for head of household by
    Pub. 501): married, so no. The question's general "no" ("file as head of
    household because you are considered unmarried") covers it, though it
    does not name it.
  - Married filing separately with a counted child: asked the
    separated-spouse question only, which is correct. With no child: $0,
    asked nothing (live control).
  - Written separation agreement only: EIC-R4.
- The not-married "no" says "cannot take the earned income credit without a
  qualifying child".

**2. Too favourable or against the filer.**

- A married head of household with no counted child cannot exceed $0. The
  answer rule publishes 0 only when questions are required, no child is
  counted, the status is head of household and the answer is no. The gate
  returns 0 on it. `eic.questions-required` = 0 holds exactly when the early
  stop is 1: I checked the conjuncts of `rule.eic-questions-required.v2.json`
  against `rule.eic-early-stop.v2.json` term by term, so the "not required"
  publish-1 branch never reaches a credit.
- An unmarried head of household gets class 1 and the single path (the table
  column reads filing status, other). $0 remains only through a genuine
  Step 4 failure, or the parked no-SSN child (Decision 5).
- Single, married filing jointly, qualifying surviving spouse and married
  filing separately: v2 publishes v1's expression unchanged, and the new
  answer publishes 1 for them. A stray answer changes nothing (live: single
  with a "no" answer still 537 / 887; married filing separately with a "yes"
  still 0 / 350; head of household with a child and "no" still 2,389).
- Every consumer of the status class already required the column count,
  directly or through `eic.questions-required`, so no new blocking reach.
- Newly asked: yes, see EIC-R1.

**3. Size cap.** EIC-R3: keep the 7,000-byte exception for that one file and
correct the stated reason.

**4. Publication.**
- `git diff --name-status` shows only added files plus `packages/tax/loader.py`
  and three test files. No published file and no schema were modified.
- A clean rebuild with `build.py` from v98 reproduces every committed byte:
  the six content files, package v99, registry v97 and release v97.
- The loader's v99 entries are the same expressions as v98's (the test
  asserts equality). No other exact-version table names v98.
- `_successor_graphs` falls back to `v96` (interest members only, none
  touched), so no entry is needed.

**5. Replay and tests.**
- The two added checks only rewrite list-order, `children` and `missing`
  attributes, and the alias digest of single-finding symbols. Values stay
  keyed and compared, and edges are still compared, so neither check can
  hide a value change. The status-class "moved row" allowance is order only.
- The replay's limit is its corpus. All 775 lists are single filers, so it
  says nothing about head of household, married or surviving-spouse
  returns. Those rest on the live controls and the structural reading above,
  and EIC-R1 is invisible to it.
- Mutants, each built with `build.py` from a mutated `design.py` in a scratch
  copy and validated by `generate_to_directory`; two test modules re-run:
  - Married "no" publishes 1: 6 failed.
  - Status class v2 keeps head of household at 0 (unmarried gets $0): 10
    failed.
  - The answer rule drops its head-of-household condition (single, joint
    and surviving spouse are asked): 9 failed.
  - v99 adds a further entrypoint: 1 failed (the package test).
- Baseline on the unmutated copy: 34 passed.

## What I ran

- `python3 tools/build_orientation_block.py --ref HEAD --charter docs/reviews/hoh-eic/charter-review.md --role reviewer`
- `git fetch github --prune`; `git rev-list --left-right --count github/main...HEAD` (0, 6)
- `python3 tools/envelope_scan.py --range github/main..HEAD` and `--range main..HEAD`: both exit 0
- `gh pr checks 295` and `gh run view 44589215930 --log-failed`
- Read every source line cited above in local `pdftotext` copies; sha256 of
  the three PDFs
- In a scratch `git archive` copy of HEAD:
  - `pytest tests/test_hoh_eic_v99.py tests/test_hoh_eic_v99_package.py`
    (34 passed)
  - clean `build.py` rebuild and byte comparison
  - four mutants as above
  - adversarial live runs of the probe returns on published v99 (EIC-R1 and
    the stray-answer controls)
  - the two CI-failing tests with `-n 0 --durations`
- Size measurements of `rule.eic-gate-result` v2 and v3 under several JSON
  formats.

No code was edited, no mutation was committed, nothing was pushed or spawned.
