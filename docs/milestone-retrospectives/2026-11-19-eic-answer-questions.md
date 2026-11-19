# Retrospective: Every Earned Income Credit Answer Has a Question (2025)

Milestone key: eic-answer-questions. Plan:
`docs/phases/engine-breadth/milestones/eic-answer-questions.md`.
Closed 2026-11-19. Core v100, registry v98, release v98: four input
questions; no rule, bundle, engine, schema, projection, page or kernel
change.

## What happened

The hoh-eic review found the earned income credit's age and main-home
answers had no question. P0 (a Claude Opus builder) counted every credit
answer: four of ten had no question, and leaving any of them out blocked
the credit and refund lines with no sentence for single, joint, surviving
spouse and unmarried head of household filers. None could be derived
soundly from the record, so the design was four questions and nothing
else. The foreman checked the wording against the sources and a Claude
Sonnet builder published it. The fresh review (Claude Opus) found the age
question told a filer whose spouse died in 2025 before reaching 25 to
answer yes. Publication 596 says no on the same page the foreman had
checked. It also showed a reversed dependent question passed every test.
A Sonnet builder applied the foreman's corrected texts and pinned the
polarity with a test that fails when it is reversed.

## What worked

- Probes that left the answer under test unanswered, the lesson from
  hoh-eic. P0's reproduction was direct.
- Mutating polarity, not just presence. Dropping a question was caught;
  reversing one was not, until the review tried it.

## What to change

- When a source gives a rule and then an exception, the question needs
  both. The foreman checked the birth-date range and missed the exception
  three paragraphs below it. Read the whole rule section, not the
  sentence a draft cites.
- A question whose yes records the fact's no needs a test that says so,
  in the same track that publishes it.
