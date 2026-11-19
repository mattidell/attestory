<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "hoh-eic",
  "status": "Closed 2026-11-19. Core v99, registry v97, release v97.",
  "retrospective": "docs/milestone-retrospectives/2026-11-19-hoh-eic.md",
  "scope": [
    "an unmarried head of household with no qualifying child is figured the earned income credit as the 2025 instructions allow, instead of being given $0 because of the filing status",
    "a married head of household (considered unmarried) without a qualifying child still gets no credit, and every other filer keeps their numbers"
  ],
  "non_goals": [
    "no change to the earned income credit tables, the qualifying-child tests or the credit for other filing statuses",
    "no engine, schema, projection, page or kernel change unless P0 shows content cannot do it, and then only after the foreman decides",
    "no change to the head of household questions published in core v98"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/hoh-eic.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/hoh-eic.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/hoh-eic.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/hoh-eic.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# The Earned Income Credit for a Head of Household (2025)

Milestone key: hoh-eic.
Branch: milestone/hoh-eic-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-19.
Starting point: main at `d3a65aff` (core v98, registry v96, release v96).
Expected target: core v99, registry v97, release v97.

## What we are trying to accomplish

The hoh-qualifying-person P0 found that `rule.eic-status-class` puts
every head of household in class 0, with married filing separately, so
a head of household with no qualifying child gets no earned income
credit. The 2025 Form 1040 line 27a instructions stop only a *married*
taxpayer filing as head of household or separately (Step 4, question 1).
An unmarried head of household whose qualifying person is, for example,
a dependent parent can be entitled to the credit with no qualifying
child. The engine gives that filer $0, which errs against the filer
(hoh/relative/low: 0 where single gets 542 on v97).

Core v98 now asks every head of household whether the status's tests
are met, and that question separates "unmarried on December 31" from
"married but considered unmarried" only in its wording, not in the
recorded answer. The engine may need a further answer to tell them
apart.

## Stages

1. **P0.** Trace the credit for each filing status and qualifying-child
   case on v98. Read the 2025 line 27a instructions and Publication 596
   (if in the local sources) for how a married head of household is
   treated, with and without a qualifying child, including the
   separated-spouse rule. Name the smallest honest design and prototype
   it as a scratch successor with the full-surface replay.
2. **Track 1.** Publish it.
3. **Fresh review**, repair, closeout.

## Decisions

1. No change to the head of household or surviving spouse questions
   published in core v98; a new fact, if needed, is a new question.
2. The P0 design: a new return-level answer `tax.us.2025.eic.not-married`
   and its question, asked only of a head of household with no counted
   qualifying child when the credit could be above zero;
   `rule.eic-answer.not-married`, `rule.eic-status-class` v2 and
   `rule.eic-gate-result` v3. Core v99, registry v97, release v97. This
   narrows the earned-income-credit milestone's Contract 1 clause ("$0
   for every head of household without a qualifying child") to a married
   head of household.
3. The question names every way to be unmarried on December 31, 2025:
   never married, a spouse who died before 2025 with no remarriage, a final
   divorce or annulment, or a decree of divorce or separate maintenance.
   P0's draft left out the earlier death and the annulment. A spouse who
   died in 2025 is not named, because v98's head of household question
   already excludes that filer.
4. The separated-spouse answer (`rule.eic-answer.separated-spouse`, Step 3
   questions 3-5) has no input question. A head of household or married
   filing separately filer with a counted child who leaves it unanswered
   is blocked with no sentence. Track 1 adds that question, worded from the
   2025 line 27a instructions.
5. Parked: a qualifying child without a valid SSN is not counted, so a
   married head of household in that case gets the new question and $0,
   where the instructions route them to the separated-spouse test (an
   existing gap that also affects married filing separately).
6. Track 1 keeps P0's two added replay checks (the inserted answer and
   finding ids downstream of it) rather than declaring broader
   expectations.
7. Repair before merge (review EIC-R1 to R4). A married head of household
   who answers "no" is stopped at Step 4 question 1, as the instructions
   say: the credit is $0 and none of the Step 4 question 2-6 answers is
   required. The not-married question's "no" list names a written
   separation agreement without a decree. The rule-size comments give the
   true reason for the 7,000-byte exception. The fast-lane test that
   overran its budget is made fast or marked live, never given a larger
   budget. v99 is not on main, so its files are regenerated in place.
8. Parked: the age (`eic.age-25-under-65`) and main-home
   (`eic.main-home-in-us`) answers have no input question, so any filer
   who must give them and has not is blocked with no sentence (review
   EIC-R1; already true for single filers on v98).

## P0 result

Evidence: `hoh-eic-evidence/p0.md` (2026-11-19, on published core v98).

- **The defect is real.** On v98 `rule.eic-status-class` gives every head of
  household class 0, and the early stop gives class 0 with no counted
  qualifying child $0 before anything is asked. A head of household whose
  qualifying person is a dependent parent, or a child too old for the credit,
  gets $0 where the same single return gets 537 (wages 7,000) or 236 (16,000).
- **Sources.** Step 4 question 1 stops only a *married* taxpayer filing as
  head of household; married is judged at December 31 (Pub. 596 checklist
  question 3; Pub. 501 Marital Status), and a married filer who is
  "considered unmarried" for head of household is still married for the
  credit (Pub. 596, "married, but qualify to file as head of household ...
  under special rules for married taxpayers living apart"). No accepted ADR
  bounds it; the earned-income-credit milestone's Contract 1 recorded the $0
  for every head of household.
- **The record does not prove it.** `hoh.tests-met` yes covers unmarried and
  considered unmarried; the separated-spouse answer is asked only with a
  counted child and its yes covers both; a counted child is not Step 4.
- **Design (variant m), content only:** one bundle with
  `tax.us.2025.eic.not-married`, its input question, a new
  `rule.eic-answer.not-married`, `rule.eic-status-class` v2 (head of household
  with no counted child is class 1, as single; with a child stays 0) and
  `rule.eic-gate-result` v3 (a married answer is $0). Asked only of a head of
  household with no counted child when the credit could be more than $0.
- **Replay:** all 775 recorded lists are single; 775 pass, 0 unexpected
  (691 expected structural changes, 84 identical errors); no recorded return
  newly blocks or changes a number. Paired probes: yes gives the single
  amounts (537, 236), no keeps v98's $0 with zero substantive differences,
  unanswered blocks lines 27a and 32-37 and shows the question; every head of
  household with a counted child, or at 50,000, and every control is
  unchanged.
- **Recommendation:** publish as core v99, registry v97, release v97; Track 1
  pins the probe cases live. No engine, schema, projection, page or kernel
  change, and no new ADR.
- **Decisions for the foreman:** p0.md section 6 (the earned-income-credit
  contract clause this narrows; decree of separate maintenance counted as
  unmarried; spouse died in 2025 left to v98's question; a child without a
  valid SSN; the separated-spouse answer has no input question; the replay's
  two added checks).

## Closeout

Closed 2026-11-19. A head of household with no counted qualifying child
is now asked whether they were unmarried at the end of 2025 (core v99).
Yes figures the credit as for a single filer; no stops at Step 4 question
1 with a $0 credit and asks nothing more; unanswered asks the question.
The separated-spouse answer, asked of a head of household or married
filing separately filer with a counted child, now has a question too.
Every other filer keeps v98's values. The fresh review found a married
"no" still required the Step 4 question 2-6 answers, two of which have no
question; five answer-rule successors now skip them. The review also
found two slow fast-lane tests, which were made fast. Parked: the age
and main-home answers have no question for any filer, and a child
without a valid SSN is not counted.
