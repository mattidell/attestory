# Retrospective: A Child Without a Valid SSN Routes the Earned Income Credit

Milestone key: eic-no-ssn-child. Plan:
`docs/phases/engine-breadth/milestones/eic-no-ssn-child.md`.
Closed 2026-11-23. Core v102, registry v100, release v100.

## What happened

hoh-eic Decision 5 had parked a $0 credit: the engine counted a qualifying
child only with a valid SSN, so a separated married filer whose child had
none never reached the separated-spouse test. A grok P0 read the 2025
instructions and Publication 596, found that the SSN decides only the
amount column, and built a content route of two new rules and seven
successors that matched 50 hand-credited synthetic cases. The foreman
widened the scope to every filing status on the condition that no source
sends such a filer to Step 4; Track 1 searched and found the Schedule EIC
sentence that settles it ("you can claim the self-only EIC"). A fresh grok
review re-derived credits at seven incomes and found one low note, which is
the existing shape for a head of household.

## What worked

- Asking the builder to search the sources for a contrary sentence before
  widening the scope, instead of widening on the P0's reading alone.
- Mutants that move the SSN test between the two rules: each lands on a
  different wrong credit, so the tests pin which rule carries it.

## What to change

- The plan named the separated-spouse test "Step 4"; the 2025 instructions
  put it in Step 3. Name a step only after reading the year's text.
