# Retrospective: The Separated-Spouse Question Is Asked Only of a Married Filer

Milestone key: eic-separated-married. Plan:
`docs/phases/engine-breadth/milestones/eic-separated-married.md`.
Closed 2026-11-24. Core v103, registry v101, release v101.

## What happened

eic-no-ssn-child's review noted that an unmarried head of household was
asked the earned income credit's separated-spouse question, which the 2025
instructions ask only of a married filer. A grok P0 found the record cannot
tell whether such a filer was married; a P0b designed a new Step 3 question
3 and showed no recorded list newly blocks. The foreman required that a
recorded separated-spouse "no" ask the new question, so the old $0 does not
survive. Track 1 published it. Three review rounds then found the
question's text wrong in turn: it omitted the decree rules, promised the
credit after "no", omitted the year-of-death rule, and let its "yes" list
be read over its "no" list. The foreman wrote the final text with the "no"
cases first, and a fast test now pins each clause.

## What worked

- Reviewing a question by asking how a filer who answers it literally
  ends up, case by case against the sources.
- Running this content milestone beside two tooling milestones.

## What to change

- A question that encodes a legal test should be drafted from the full
  list of the year's cases before the first build, with "no" cases first,
  not grown one review finding at a time.
- The schema's two-path minimum forced an inert path; a selection that
  needs only one present-answer branch has no clean shape today.
