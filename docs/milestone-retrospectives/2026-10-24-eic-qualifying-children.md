# Retrospective — The 2025 Earned Income Credit with Qualifying Children

## Result

- **The 2025 earned income credit with one, two, or three or more qualifying
  children computes on core v54.** An unmarried head of household with two
  children and $15,000 of wages gets $6,010; a joint return with $35,000 of
  wages and one qualifying child gets $3,600.
- **Each child is counted from six answers about that child** on a closed
  child roster, through a per-child chain of rules, and the explanation names
  each child and the test it fails.
- **The engine refuses where the law needs another taxpayer's facts:** a
  child another person may also claim blocks the credit. A filer whose only
  qualifying children lack a valid SSN takes the self-only credit.
- No schema, expression operation or engine change. Earlier packages and
  their goldens are unchanged.

## What the evidence changed

- **The probe decided the model.** Run through the real coordinator, the
  per-child chain counted correctly and blocked on a missing answer or another
  claimant. The Form 1098 "flat" per-subject shape counted a child whose
  residency was unanswered and a child another person may claim: it can bind
  another subject's answer. That is an engine finding beyond this milestone.
- **The law corrected a planning assumption.** The plan first said a filer
  whose child lacks an SSN cannot take the childless credit. The Schedule EIC
  instructions say the opposite; the Foreman read them before the build.
- **A question has to be answerable by the people asked.** The separated-
  spouse question assumed a spouse, but it was required on every head of
  household return with a child, most of whom are unmarried. Every figure in
  the tests matched the printed table; only reading the title against who
  answers it found this.

## Process

- **Dispatch changed five times** at the owner's direction: grok, Haiku,
  Sonnet, Sonnet through agy (which ran out of quota after committing the
  probe), Haiku, then Gemini Flash through agy.
- **Haiku failed both units it ran.** Its P0 invented table cells and reversed
  the no-SSN rule. Its child-column parameter stopped each column at the
  childless limit and then paid the maximum at any higher income, and its own
  test fixed that layout as the expectation; the formula check it reported
  was real but checked the formula, not the file. The Foreman wrote the model
  decisions from the probe and regenerated the columns, with a coverage test
  that fails on the broken file.
- **Flash built Track 1b and Track 2 correctly** against an explicit charter
  that named its traps: copy the chain shape, take every figure from the
  printed table, and list required-versus-read.
- **The first ready CI run failed on mypy** in three new test files: no unit
  and none of the Foreman's checks ran the full `mypy` before ready. Each
  charter lists it; it now runs with the full lane before a PR is marked
  ready.
- **Verify the artifact, not the report.** Each unit's tests were run, its
  figures checked against the printed table, and its package diffed by the
  Foreman before acceptance.

## What it cost

The grok, Sonnet and first Haiku P0 runs were stopped or rejected; the agy
Sonnet P0 used the whole Claude 5-hour bucket and committed the probe. Track
1a ran on Haiku (29 tool calls) and was repaired by the Foreman. Track 1b and
Track 2 ran in one agy Flash conversation (about 1.9M and 2.2M tokens, most
of it cached). The final review ran in a fresh agy Flash conversation.

## Follow-ups

- The EIC tie-breaker rules, for a child another person may also claim.
- The flat per-subject shape's cross-subject binding (the mortgage rules use
  per-statement rules).
- A corpus-wide required-versus-read check; `explain()` re-expansion of
  shared inputs.
