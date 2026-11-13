# Retrospective — What the Mortgage and Sale Pages Show

## What differed from the plan

The work observed existing returns rather than publishing another tax package.
Real coordinator outputs on explicitly adopted core v79 were rendered as saved
citation-walk pages in Chrome. Six requested cases grew to ten regression
cases: unanswered and stale noncovered answers, plus itemizing mortgage returns
with one missing declaration and with that declaration recorded.

The original $4,000-interest mortgage used the larger $15,750 standard
deduction. Its Schedule A not-required status was not evidence of a defect.
The $20,000 case initially blocked Schedule A for exactly the missing
no-other-line16 declaration. Recording that truthful synthetic answer published
the attachment. A helper called current-core still defaulted to v67; explicit
adoption and actual source pins were more useful than the helper's name or
input-description prose. Supplemental captures retained the earlier runs rather
than silently relabeling them.

The observed amounts, covered-sale refusal sentence and attachment states
became live browser assertions. Model agreement alone did not settle meaning.
Two unrelated sections displayed safe-rendering alerts; the shared question
appeared on 34/32 blocked rows. Those defects are parked explicitly, not called
correct page behavior. The mortgage amount appears in its special explanation
region while the ordinary line row and Schedule A subtotal remain absent.
That surface gap is recorded separately from calculation and attachment status.

## What it cost

The original eight coordinator runs took 25.086 seconds combined, excluding
setup and Chrome. Three single-case mortgage supplements took 2.993, 3.036 and
3.157 seconds; the original eight were not rerun for those refinements. The
ten-case live regression passed in 70.87 seconds; it uses one browser with
fresh contexts. These are elapsed observations, not isolated process CPU or
billed CI minutes. Fixture-safety checks, fast lane and configured mypy passed;
exact-head CI remains the publication gate.

Fresh review found that a parked-alert exemption could conceal a model value
changed from zero to 999. The intended separation between diagnostic evidence
and supported parity had become too broad. The accepted repair constrains the
known zero, source semantics, explanation and pins independently and retains
negative mutations. Review closed it using the retained real browser capture.
Review also closed contradictory complete-mortgage prose after correction;
neither change required recapturing the browser. Final repair fast lane passed
1,687 tests with eight skips; mypy passed 468 files.

## Follow-ups

The first ready-event CI run (42333453979) failed only the new browser fixture,
before its assertions ran. Three full-suite shards and quick/precheck passed.
The retained generic error could not distinguish startup, CDP or page failure;
the private launch trace was absent from uploaded artifacts. The diagnostic
iteration carries a sanitized stage/category and launch summary into the
JUnit failure artifact. This improves evidence, not proof of a repaired flake.
Its focused checks and mypy passed; one fast lane had ten existing budget
failures, recorded without retry or infrastructure attribution in the evidence.
Fresh independent acceptance and exact-head green CI remain publication gates.

Diagnostic review found that malformed UTF-8 in optional launch evidence could
mask the primary failure. Treating that evidence as unavailable preserved the
original stage/reason; independent recheck closed the finding. Four focused
diagnostic tests and mypy (469 files) passed after repair, without repeating
the whole fast lane or recapturing the browser cases.

- Published-content successor work for line 6c's not-elected instruction and
  the Schedule 1 top-entry field's missing citation; do not change old bytes.
- Shared-question presentation that asks once while preserving each blocked
  line's true reason and connection to that question.
- The ordinary Schedule A8a/itemization surface gap beside a visible mortgage
  amount and published attachment status; establish the intended display before
  selecting a repair.

The phase roadmap owns the current parked list. This observation adds no tax
class, filing capability, real-data evidence or corrected-content claim.

## What should change in the next plan

The repaired Chrome route subsequently passed all four Linux full-suite shards
and required verify in run 42719255831. Quick instead exposed a cold schema
cache in an unchanged integration-checkpoint test: 6.953 seconds of its 6.958
cold seconds were schema validation, while a warmed call took 0.010 seconds.
Rebasing incorporated main's cache restoration between tests; no assertion or
lane change was warranted for that checkpoint. Exact old CI worker ordering
was not established. Eleven other local fast-lane budget failures remain
listed in the cost account, not retried or waived as infrastructure. These
observations do not substitute for fresh CI after the latest synchronization.

The remaining-budget follow-up kept cheap unit checks fast, explicitly routed
real Git checkout and full-corpus rebuild cases to live, and retained all tests
in the full suite. The nominee six-mutation test eliminated five redundant
full-corpus loads, using a full deep copy per validation rather than sharing
mutable input citizens. Its real runtime/package checks and assertions remain.
The 56 focused cases passed; the next single fast lane passed 1,763 with eight
skips and no budget failures in 15.96 seconds; mypy passed 487 files. These are
test-economy results, not measured production or whole-suite CPU savings.

After the v87 rebase, Linux quick run 43161978728 measured the nominee
test at 4.5 seconds against its 3-second budget. The unfinished full-suite
shards were cancelled. A local profile attributed 2.658 of 3.267 profiled
seconds to six deep copies. The repair retains the complete corpus, copies
the mapping for each validation and checks shared values against one deep
snapshot. Independent review compared all six mutations in both orders with
deep-isolated validation and found identical results with unchanged inputs.
The target passed locally in 2.32 seconds, all 19 module tests passed, the
fast lane passed 1,772 tests with eight skipped, and mypy passed 489 files.
The v88 rebase preserves upstream roadmap entries. Fresh Linux CI is required.

The November 9 path repair uses a short private system-temp directory rather
than nesting Chrome's TMPDIR beneath the workspace. Linux's singleton socket
path limit explains why checkout depth can break startup even when the profile
itself is valid; increasing a launch timeout cannot repair a fatal path error.
The observed immediate SIGABRT is consistent with that mechanism, but discarded
historic stderr is not recreated evidence. An actual v80 Chrome regression now
inherits a long TMPDIR and observes short-root launch and owned cleanup. Main
synchronization also brought the upstream lattice live-lane correction; the
milestone did not alter that test or its budget. All ten saved-page cases were
reobserved on v80, preserving original v79 labels; no v82 capture is implied.
The first v80 carry capture left its added source-family question unanswered;
the corrected capture explicitly records that distinct absence without
refreshing the original stale answer. The compact account discloses both that
fixture correction and a raw question-key metadata label correction. Final
local diagnostics passed six tests; one fast lane passed 1,737 with eight skips
in 16.80 seconds; mypy passed 476 files. No broad local suite was repeated.

Choose a fixture that reaches the attachment's required branch, and inspect the
exact missing dependency before declaring a product defect. Separate original
evidence from later completed-scope captures. A parked defect needs a narrowly
tested diagnostic boundary: it must not exempt newly wrong values or reasons.
Visible DOM observations and instrument-only mutations prove different claims.


## Owner review follow-up

All ten pages were reobserved on core v89 with explicit synthetic age and
blindness answers. The v89 carry retains unanswered families and records
exact repeated-question counts, missing row-local reason, and attachment
states. V79 and v80 are historical. Twenty serial and four concurrent local
replays did not reproduce the Linux post-launch stall. The 240-second
watchdog is restored, stage diagnostics remain, and the ten-case test is
live and opt-in. The narrower nominee guard passed Linux quick at 0.788s,
compared with a historical 4.5s failure on an earlier head. The budget
remains 3s. The two runs do not isolate the guard's individual effect.
