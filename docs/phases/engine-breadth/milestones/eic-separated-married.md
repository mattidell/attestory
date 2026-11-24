<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "eic-separated-married",
  "status": "Open 2026-11-23. Track 1 done; review NOT READY; repair next.",
  "retrospective": null,
  "scope": [
    "the earned income credit asks the separated-spouse question (Step 3 questions 4 and 5 of the 2025 Form 1040 instructions) only of a married filer whose status is head of household or married filing separately, as the instructions do",
    "an unmarried head of household with a qualifying child is not asked it and keeps the credit the sources give",
    "every other recorded return keeps its numbers"
  ],
  "non_goals": [
    "no change to the credit tables, the other credits, or which answers an unrelated path needs",
    "no kernel or engine change; a new question only if P0 shows the record cannot tell whether a head of household was married, and then from the 2025 instructions",
    "no page change"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/eic-separated-married.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/eic-separated-married.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/eic-separated-married.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/eic-separated-married.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# The Separated-Spouse Question Is Asked Only of a Married Filer (2025)

Milestone key: eic-separated-married.
Branch: milestone/eic-separated-married-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-23.
Starting point: stacked on the eic-no-ssn-child branch (#301); rebased onto
main at `974cb1a1` (core v102, registry v100, release v100) after it merged.
Expected target: core v103, registry v101, release v101 if content can do
it; otherwise a P0 decision for the foreman.

## What we are trying to accomplish

eic-no-ssn-child parked ENS-R1. On core v101 and v102 a head of household
with a qualifying child is asked the earned income credit's
separated-spouse question, whose "yes" includes "not married at the end of
2025". The 2025 instructions ask Step 3 questions 4 and 5 only of "a
married taxpayer whose filing status is married filing separately or head
of household" (Step 3 question 3). An unmarried head of household who
answers the question as worded "no" (they were not separated; they were
never married) gets $0. The record may already say whether the filer was
married (for example the head-of-household or not-married answers); if it
does, the question can be skipped for an unmarried filer.

## Stages

1. **P0.** Quote Step 3 questions 3 to 5 and the special rule for
   separated spouses (2025 Form 1040 instructions, line 27a) and the
   matching Publication 596 text. Trace published core v102 on synthetic
   demo.* returns: head of household married or not married, with a
   qualifying child with and without a valid SSN, separated or not; and
   married filing separately. Name which recorded answer, if any, already
   says the head of household was married at the end of 2025, and where
   it comes from. Find a content route that asks questions 4 and 5 only of
   a married filer; if the record cannot tell, name the smallest question
   from the instructions and stop. Full-surface replay of a scratch
   successor against v102 with expected changes declared.
2. **Decisions** by the foreman.
3. **Track 1.** Publish it.
4. **Fresh review**, repair, closeout.

## P0 result

Evidence: `docs/phases/engine-breadth/milestones/eic-separated-married-evidence/p0.md`.

Published core v102 cannot tell whether a head of household with a qualifying
child was married at the end of 2025. `eic.not-married` is asked only when no
qualifying child is present, and its words do not match Step 3 question 3.
`hoh.tests-met` yes covers an unmarried filer and a married filer who lived
apart for the last six months. The separated-spouse question is asked of
every head of household with a qualifying child. Twenty-one synthetic
demo.* returns on the live coordinator match the 2025 table except the two
unmarried head-of-household returns that answer that question no: line 27a
is $0 where the instructions give 2,389 (valid SSN) or 537 (no valid SSN)
at wages of 7,000. The other four unmarried returns with a qualifying child
keep those table amounts only because the published yes includes "not
married," and they are still asked.

No scratch successor was built and the 775 recorded lists were not replayed.
The smallest new question is Step 3 question 3, asked of a head of household
who has a qualifying child. Married filing separately is already a married
taxpayer by filing status. A yes continues to questions 4 and 5. A no skips
them and keeps the table credit. No engine change and no new ADR.

## Decisions

1. Accept the P0 stop: no fact on a v102 return says whether a head of
   household with a qualifying child was married at the end of 2025
   (`eic.not-married` is withheld when a qualifying child is present and
   counts a decree as "yes"; `hoh.tests-met` "yes" covers both). The route
   is a new input question taken from Step 3 question 3 of the 2025
   instructions, asked only of a head of household with a qualifying
   child, with its own fact type. Married filing separately needs no new
   fact. No engine change and no ADR.
2. A return must not newly block on the new question when it already
   carries an answer that decides the credit the same way: a recorded
   separated-spouse "yes" passes on v102 and must still pass. P0b designs
   the successors so the separated-spouse question is asked only after a
   "married" answer, and so that a recorded separated-spouse "yes" without
   the new answer still passes if the rule language can express it
   (selection on which answers are present). If it cannot, P0b measures
   how many of the 775 recorded lists, and which kinds of filer, would
   newly block, and stops for a foreman decision.
3. P0b reports each new or successor rule file's size against the
   5,000-byte cap, and runs the live size tests.

4. Publish the P0b design (new fact `eic.married-taxpayer` and its input
   question from Step 3 question 3, `rule.eic-married-taxpayer-recorded`,
   `rule.eic-answer.married-taxpayer`, separated-spouse v3) as core v103,
   registry v101, release v101, with one change: a recorded separated-spouse
   "no" from a head of household with a qualifying child does not decide
   the credit on its own. That filer is asked the new question; "no" (not
   married) gives the credit the sources give, "yes" keeps $0. A recorded
   separated-spouse "yes" still passes without the new answer. No recorded
   list carries a separated-spouse answer, so nothing in the corpus newly
   blocks; a saved return with a recorded "no" newly asks one question.
5. The inert path keyed on a fact nothing asks
   (`eic.married-taxpayer-inert`) is removed if the rule language allows
   the design without it; if it does not, Track 1 says exactly which
   validation requires it, and the fact type is never offered as a
   question.
6. The question's wording is checked against Step 3 question 3 and
   Publication 596 Rule 3; it is shortened where it repeats the
   separated-spouse question that follows.
7. Track 1 runs `pytest -m "not live" tests/test_content_file_sizes.py`
   (the size guards now run in the fast lane, #303) and, until #303 merges,
   the two live size tests.
8. Repair before merge (review ESM-R1 to R3). The question states the
   instructions' marital test, not only "married at the end of 2025": an
   interlocutory decree is still married; a final decree of divorce or of
   separate maintenance at the end of 2025 is not married for Step 3
   question 3; a head of household who lived apart and is "considered
   unmarried" for filing status is still married for the credit
   (Publication 596 Rule 3). A "no" skips questions 4 and 5 and continues to
   question 6; the question does not promise the credit. The second
   selection path stays (the schema needs two) but can never change the
   result: a stored `eic.married-taxpayer-inert` fact publishes what the
   default publishes, or is refused at the assertion boundary, and never
   trips the exclusive-presence refusal together with a separated-spouse
   answer. v103 is not on main, so its files are regenerated in place.

## P0b result

Evidence: `docs/phases/engine-breadth/milestones/eic-separated-married-evidence/p0b.md`.

The new fact is `tax.us.2025.eic.married-taxpayer`. It is Step 3 question 3,
asked only of a head of household with a qualifying child when no
separated-spouse answer is already recorded. A recorded separated-spouse yes
still passes: one `exclusive_presence` path is active when that answer is
present and does not read the new fact. An inert second path is never
recorded. The default asks the new question only in that head-of-household
population; married filing separately never reads the new fact.

Twenty-seven synthetic demo.* returns on the scratch successor match the
hand credit and the asked flags. An unmarried no keeps 2,389 or 537 and is
not asked questions 4 and 5. A married yes with those questions unanswered
blocks on the separated-spouse fact. A recorded yes with no new answer keeps
the table credit.

The 775 recorded lists are all filing status single, and none carries a
separated-spouse answer. None changes outcome and none changes a number.
Eighty-four error on both cores with the same snapshot. Three hundred seventy
add a blocked disposition on the two new rules because
`eic.questions-required` is absent; the separated-spouse disposition was
already blocked on that fact and stays blocked. That is not a newly blocked
return.

Rule files are 4,923, 2,386, and 4,305 bytes, all under the 5,000-byte cap.
The live 5kb tests passed. No engine change and no ADR.

## Track 1 result

Evidence: `docs/phases/engine-breadth/milestones/eic-separated-married-evidence/track1.md`.

Published core v103, registry v101, and release v101. A recorded
separated-spouse no from a head of household with a qualifying child asks
`eic.married-taxpayer`. No keeps the table credit, 2,389 or 537 at wages of
7,000. Yes keeps $0. A recorded separated-spouse yes still passes without
the new answer. Married filing separately is unchanged.

The inert path stays. One path is rejected: `MEMBER_SCHEMA_INVALID`,
`instance does not conform to rule-artifact.v14: selection/paths:` and the
single path `is too short`. `selection.paths` has `minItems` 2. The inert
fact is never an input question.

Thirty-one synthetic returns match the hand credit and the asked flags. The
775 recorded lists, all single and none with a separated-spouse answer, show
691 success on both cores and 84 identical errors. None newly block and none
change a number. Rule files are 4,733, 4,797, 2,422, and 4,305 bytes. No
engine change and no ADR.
