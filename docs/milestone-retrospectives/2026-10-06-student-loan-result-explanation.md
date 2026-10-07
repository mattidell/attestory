# Retrospective — Student Loan Result Explanation

## What differed from the plan

The plan expected that a reader would need new information. The
investigation found almost none. The projector already received each
statement's amount, support result and the rule's declared basis, then
discarded them. So most of the work was copying data, not creating it.

The design review changed the core idea. A statement's support result is not
its standing on line 21, because the worksheet also reads other answers. Row
status therefore comes only from line 21's own reasons.

Two defects surfaced during the display build, both in data that Track 1a had
already saved:

- a recorded answer without its question wording meant no presentation
  was saved for the run;
- with two statements refused together, the reasons lost which statement
  they named. Both rows then showed favorable basis detail.

The first repair then compared raw record ids. That made one statement's
reason appear twice, because it was reached through two different records.

The owner's design check on the old and new loan inputs ended as deferred
design, not a requirement. The foreman's first draft would have retired an
older "yes" automatically to suit exclusive path selection. That would have
superseded a person's statement for an engine reason.

## What it cost

The work took:

- three investigation and review units;
- two builder units, the second interrupted twice by usage limits;
- three independent reviews of the display;
- one foreman repair.

The full suite was left to CI. CI then caught a test stand-in for the
projection that rejected its new argument. A local fast-lane run had missed
it, because the new data module was not routed to the live lane. Browser
tooling failed repeatedly, and the owner inspected the pages directly.

## Follow-ups

- **Mixed-method input and assumption management.** These are in the plan's
  deferred design. Reactivate when the next phase selects an intake or
  assumption milestone.
- **Both-present sentence.** The adopted worksheet tells the person to
  remove an answer to fit an engine limitation. Reword it with mixed-method
  support.
- **Page placement.** The line 21 explanation sits low on a long page, below
  Form 1040 line 10's identical amount. Reactivate with any reader
  navigation work.
- **Fast-lane routing.** Modules that drive the coordinator through a helper
  are not marked live. These include `test_sli_track4_support_chain.py`,
  `test_sli_track13_explicit_relationship_recording.py` and
  `test_f1098e_student_loan_interest_track8_presentation.py`. As a result,
  `pytest -m "not live"` fails them on duration. Fix in `tests/conftest.py`.
- **Raw values on the page.** Relationship answers show recorded values such
  as `sli.financing.affirmed`, and the limits show parameter ids. Neither has
  a declared label. Reactivate with a phase-boundary legibility audit or
  reader wording work.
- **Identity fallback.** A reason without a statement identity is given to
  the sole statement on the line. That cannot occur on worksheet v4. Remove
  the fallback or make it fail closed if a rule ever emits such a reason.
- **Carried from earlier milestones:** the saved "no" stays unpinned. The
  torn-log, runner-default and entrypoint follow-ups are unchanged.

## What should change in the next plan

Test any presentation join with two affected subjects. Include two subjects
that share a display label and one subject that is reached through two
records. When a change adds an argument to a function, search the tests for
stand-ins of that function before relying on focused tests.
