# Retrospective: Head of Household Needs a Qualifying Person (2025)

Milestone key: hoh-qualifying-person. Plan:
`docs/phases/engine-breadth/milestones/hoh-qualifying-person.md`.
Closed 2026-11-19. Core v98, registry v96, release v96: a vocabulary
bundle with two return-level answers, two input questions and one rule
successor (`rule.dependents-worksheet-line-3` v2 on `rule-artifact.v17`).
No engine, schema, projection, page or kernel change.

## What happened

The cf-loss-limit P0 had noticed that head of household and qualifying
surviving spouse were accepted with no qualifying person. P0 (a Claude
Opus builder) measured it: with $50,000 of wages and nobody else on the
return, the refund was 1,675 as head of household and 2,647 as surviving
spouse against 625 as single. Every larger amount flows through one rule,
the standard deduction lookup, so one question per status, read only on
that status, closes it. A Claude Sonnet builder published it. The fresh
review (Claude Opus) passed the rule, packages and tests (six mutants all
caught) but found the head of household question's examples let a married
filer supporting only a parent, or a filer with a member-of-household
dependent, answer yes. The foreman rewrote both questions from the
instructions and Publication 501, and a Sonnet builder regenerated v98 in
place before merge.

P0 also found an error against the filer: the earned income credit is $0
for every head of household without a qualifying child. It is parked.

## What worked

- Tracing every larger amount to a single rule before designing. It made
  the change one rule successor and two questions.
- A review question that asked for the cases where the wording misleads.
  The tests could not have found it, because they test the answer, not
  the sentence.

## What to change

- A question that lists legal tests needs the same adversarial reading
  as a rule, before Track 1 publishes it. Examples in a question are
  claims; each one needs a source line.
- Two sub-agents stalled today on a command that never ran. Check a
  running agent's last tool call at every heartbeat.
