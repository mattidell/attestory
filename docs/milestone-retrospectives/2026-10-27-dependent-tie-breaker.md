# Retrospective — A Child More Than One Person Could Claim (2025)

## Result

- **A child another person could also claim is resolved, not refused.** On
  core v58 a per-child tie-breaker rule decides whether the filer may treat
  the child as a qualifying child, and the earned income credit, child tax
  credit and credit for other dependents all follow it. A parent against a
  grandparent gets $1,475 on line 19, $725 on line 28 and $3,261 on line 27a;
  a grandparent who loses the only child to a parent gets the childless
  credit of $83.
- **Questions about the other person that a filer can answer:** ten yes/no
  questions, each asked only where it can decide. Every combination resolves
  through one step, shown by an 18-row table run through the real
  coordinator.
- **Outside the class by answer:** Form 8332 or a decree release, more than
  one other person who could claim, and the equal-AGI ties the sources do not
  settle.
- **One engine change (ADR-0081):** a per-subject rule may make its
  own subject's answers conditional, so a child's later tie-breaker answers
  are asked only when the earlier ones lead there. Earlier packages and
  goldens are unchanged; a v57 answer set on v58 is asked only the root
  question per child.

## What the evidence changed

- **The engine could not ask a child's answer only where it decides.** P0
  showed every tie-breaker question would be required on every contested
  child; family gating avoided that only with eight rosters whose membership
  encoded the answer. The owner chose an engine change over either.
- **Succession could not reuse the old answer.** Its published title says
  `yes` blocks, and the engine has no operator to fall back from an absent
  new answer to an old one, so v57 answer sets are asked one new question.
- **The first Track 1 run left no commits and reported files that did not
  exist.** The relaunch committed after each deliverable and checked
  `git log`; verify artifacts, never a report.
- **The review found two high-severity defects the table had passed.** The
  equal-AGI question came before "will the other person claim", so a filer
  the law gives the child was refused; and the credit for other dependents'
  count rule was never succeeded, so a lost child blocked line 19. The
  resolution-table script missed the second because its package stopped one
  rule short of the published line. A check is only as good as how far it
  follows the real path.
- **The engine change had two defects of its own:** a present conditional
  answer was pinned when the child blocked earlier, and a conditional answer
  could fall back to a return-level value. Both were fixed before the
  presentations were saved, and the saved explanations pin exactly the
  answers each decision read.
- **Asking the tie-breaker only of a child some credit can count is parked.**
  It needs a derived per-child result as a conditional member, which four
  engine layers refuse. A child who fails every credit is asked the root
  question; no line is wrong.
- **The final review found that lines 19 and 28 explain themselves as the
  earned income credit.** Their form-field text was copied from line 27a when
  the child tax credit was added on core v55. It predates this milestone and
  is parked; it is the first thing a filer reading a lost-child explanation
  would see.

## Process

- Every unit ran on agy Gemini Flash except the Track 0-1 review, which ran
  once on Gemini Argon at the owner's direction. Argon reviewed in 26
  minutes; the Flash repair of its findings took 4.3 hours and 5.6M tokens,
  mostly in repeated full-suite runs.

## Follow-ups

- Successor form-field text for lines 19 and 28, and a presentation line
  that names the tie-breaker step that decided each child.
- Derived per-subject results as conditional members (finding 5).
- Form 8332 and decree releases; more than one other claimant.
