# Retrospective — The 2025 Credit for Other Dependents

## Result

- **Schedule 8812 is complete for the engine's class on core v56.** A joint
  return with a child under 17 and a child aged 18 gets $2,700 on line 19; a
  single filer supporting a parent gets $500.
- **Dependents beyond qualifying children** are recorded from answers about
  each: a second family over the child kind for children marked for this
  credit, and a relatives family over a new kind.
- No schema, expression operation or engine change. Earlier packages and
  their goldens are unchanged.

## What the evidence changed

- **The engine's family rules shaped the model.** A child who fails the child
  tax credit tests cannot move rosters, because a fact belongs to one family;
  the form's own per-dependent "credit for other dependents" checkbox became
  the second family's member.
- **A per-subject rule cannot make one child's answer conditional on
  another's, or on the same child's other answers,** so the roster's member
  became the child's "marked for this credit" answer.
- **Reuse was checked by meaning and by when each answer is asked.** P0
  declined four reuses whose asked-when conditions did not fit, the defect
  the child tax credit's final review had found three times.
- **The final review still found the same class, path-dependent.** As first
  built, the new families' closures and return-level answers were required on
  every return, so a v55 child tax credit family with no other dependent was
  blocked on v56 until it answered questions that could not change its
  result; the static required-versus-read check could not see it, because
  each answer is referenced, just not on that path. The existing "no other
  dependent" answer now switches the new rosters on, and a test runs the v55
  answer set on v56. A regression test with the previous version's answers is
  the check that catches this class.
- **The first repair overshot.** Making the new answers conditional
  disconnected line 6 from the filer gates, so a nonresident alien filer, a
  Form 2555 filer or one without an identification number still got line 19,
  with only the gate row blocked; the test asserted the gate row, not line 19.
  The re-review found it, and its regression test had skipped every new
  artifact. Line 6 now reads both gates, tests assert line 19 itself, and the
  regression test has no exemptions. Assert on the published line, never an
  intermediate row, and never filter the artifacts a regression test checks.
- **Only children marked for this credit are on its roster,** so a child whose
  box is "no" is never asked its identification number.
- **"Not married" is not the law's test.** The relative question first asked
  whether the relative was married; the law excludes only a relative who files
  a joint return. Fourth question-wording defect across the credit
  milestones.

## Process

- Every unit ran on one resumed Haiku 5.5 builder; the final review on a
  fresh Haiku 5.5 reviewer.

## Follow-ups

- Disabled relatives with gross income of $5,200 or more, and multiple
  support agreements.
- The tie-breaker rules for a dependent another person may also claim.
