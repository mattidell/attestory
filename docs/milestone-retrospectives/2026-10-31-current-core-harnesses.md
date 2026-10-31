# Retrospective — Complete Current-Core Returns for Tests

## Result

- **One place builds complete current-core returns.** Base return, Form
  1099-INT box 8, Form 1099-DIV box 12, Form 1098-E, and a three-child Part
  II-B return, all on core v66 with every closure and answer.
- **The structural-only checks now run live** and pass: line 2a, Schedule
  8812 line 21 and Schedule 1 line 21 with cents, and the correction
  session's line 21 view on v66. No product defect was found.

## What the evidence changed

- **The missing piece was the base return, not the lines.** Each earlier
  attempt failed on an unrelated block (a Social Security chain, a scope
  answer, a closure). A base return that answers everything made each line
  one adder away.
- **A helper must not repair itself.** The first version quietly withdrew a
  contradicted declaration; it had never fired, but it would have hidden a
  broken helper. It now fails.

## Follow-ups

- The helpers import private functions from older test modules; a shared
  recorder module would remove that coupling.
