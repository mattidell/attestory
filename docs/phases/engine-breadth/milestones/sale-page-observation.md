<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "sale-page-observation",
  "status": "Closed. Ten synthetic core-v79 saved pages have live Chrome regressions; all ten were reobserved on v80 after main synchronization. Chrome uses a short owned temp root; rendering findings remain explicitly bounded, not claimed repaired.",
  "retrospective": "docs/milestone-retrospectives/2026-11-06-sale-page-observation.md",
  "scope": [
    "observe six synthetic current-core return classes on the actual saved citation-walk page",
    "compare visible amounts, explanations, blocked reasons, once-only questions and attachments with the presentation model",
    "add live-lane browser regressions and small reproducible observation evidence without publishing content"
  ],
  "non_goals": [
    "no package, registry, release, tax-content, kernel or schema changes",
    "no computed-tax-class expansion or filing/real-data claim",
    "no presentation repair unless all existing goldens remain byte-identical and the full suite passes",
    "no changes to another milestone or its worktree"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/milestone-retrospectives/2026-10-15-mortgage-interest-circumstances.md",
      "docs/phases/engine-breadth/milestones/sale-page-observation.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/sale-page-observation.md",
      "docs/milestone-retrospectives/2026-10-15-mortgage-interest-circumstances.md"
    ],
    "review": [
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/sale-page-observation.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-06-sale-page-observation.md",
      "docs/phases/engine-breadth/milestones/sale-page-observation.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# What the Mortgage and Sale Pages Show (2025)

Milestone key: sale-page-observation.
Branch: milestone/sale-page-observation-2025.
Phase: Engine Breadth. Opening plan: 2026-11-06.
Base: github/main at 87b05daf, PR #261 merged; core v79.

## What we are trying to accomplish

The engine has computed mortgage and securities-sale returns, but the parked
browser-observation item has not established what a filer actually sees on
their saved page. A correct presentation-model amount does not by itself prove
the page shows it, explains it honestly, or tells the person why another line
is blocked. This milestone observes that path and leaves repeatable browser
checks, not another tax-content successor.

## What we know and need to learn

The mortgage retrospective explicitly says no browser observation was obtained.
Core v79 now supports noncovered Form 1099-B boxes B/E and one answer for eight
families; covered sales marked basis-not-reported must refuse with their own
sentence. Existing tests exercise saved presentation and Chrome lifecycle
pieces. The current-core helper still defaults to v67: a helper name is not
evidence of v79 adoption. Each run must verify its adopted package and resolved
release/registry before making current-core claims.

We need to distinguish what the adopted model says, what the saved HTML contains,
what Chrome displays after scripts/disclosures, and what the filer reasonably
understands. Duplicate question wording, blank reasons, misleading sentences
and missing/blocked attachments are findings, not acceptable model parity.
Every observed blocked line needs a true nonempty reason; code text alone is
not presumed a usable explanation.

## Actions the team will take

1. **P0: observe and inventory.** Build each synthetic return through
   live_coordinate_run on core v79, save its actual model/page, render in real
   headless Chrome using the existing harness, and record small DOM excerpts
   or screenshots. Inventory visible values, sentences, reasons, questions and
   attachment states against the model, including all blocked lines on the
   observed pages. Record how the observed controls/disclosures were reached.
2. **Decide.** From measured P0 choose stable selectors and expectations and
   disposition discrepancies. Content/package defects are evidenced and parked
   for the core-v80 line, never fixed here. Observation can close while an
   explicitly named defect remains parked; it cannot claim that page correct.
   A rendering-only defect may receive a separate bounded repair charter only
   if all existing goldens stay byte-identical and the full suite passes.
3. **Track 1: tests.** Mechanical regression tests reproduce all six cases,
   compare DOM and model, and assert the truthful reason/question/attachment
   properties established at P0. New browser tests are explicitly live lane.
   Do not freeze a false sentence as a correctness expectation; distinguish
   characterization evidence from passing product claims.
4. **Fresh-reader review and repair.** An independent reviewer checks the
   actual filer-visible meaning, case completeness, data safety and lifecycle,
   not merely that expected strings equal model strings.
5. **Close and publish.** Retrospective, plan outcome/review dispositions,
   roadmap/parked list and bounded coverage-frontier/README claims as needed.
   Remove working charters after distillation. Curate P0 / Track / Close with
   a dated safety snapshot and byte-identical final tree; independently confirm
   the exact range, push with lease, mark ready, and obtain exact-head green CI.
   The owner pre-approved agent merge only on that green exact-head gate.

Rival prototypes and the authority/lifecycle Track 0 closure gate do not apply:
this work observes existing contracts and publishes no contract or tax change.
Any newly required contract decision stops and returns to the owner.

## Cases that shape the observation

| Synthetic case | Principal observation |
| --- | --- |
| Form 1098 mortgage | Schedule A line 8a value and explanation; Schedule A attachment |
| Covered long-term Form 1099-B sale | Schedule D line 8a value and explanation; Schedule D/Form 8949 states |
| Noncovered box E sale | Schedule D line 9; supplied basis; attachment rows/states |
| Code W wash sale | Actual adopted wash-sale route, adjustment and attachment; identify box/term explicitly |
| Covered sale flagged basis-not-reported | Blocked covered line and exact sentence beginning “Record this sale as a noncovered sale” |
| Wage return with the single noncovered “no” | Closure-backed zeros, once-only shared question and no phantom required sale attachment |

Use related blocked/unanswered variants where needed to expose a reason or
question; do not substitute those variants for the six required returns.
One question's occurrence is counted in its user-facing question region, not
in hidden model JSON, citations or repeated explanation provenance. P0 must
identify those regions rather than silently choose a convenient whole-DOM count.

## Boundary, contracts and verification

Tests, tools and small synthetic evidence are the default write scope.
packages/content/, packages/kernel/ and packages/schemas/ are excluded entirely;
publish no package, registry or release anywhere. No runner attachment change.
New browser tests follow tests/test_presentation_chrome_lifecycle.py,
tests/test_explanation_saved_browser.py, tests/test_sli_saved_reader_page.py and
tests/test_chrome_test_resources.py; reuse launch coordination, owned process/
profile cleanup and bounded waits, with no timeout inflation or retries.

Preserve existing saved pages/goldens. Run focused new browser tests, applicable
fixture-safety checks, fast lane and python -m mypy. A derivation repair requires
byte-identical existing goldens and full suite before handoff. CI is the final
gate; no repeated full suite merely to confirm a deterministic result.
All inputs, DOM excerpts and screenshots are synthetic demo.* only; generated
scratch stays ignored, no absolute local paths or raw browser logs committed.
Do not read governance text; stop if interpretation is needed.

Parallel PR #262 may publish core v80. Never access its worktree. If it merges
first, synchronize the clean branch with main and reobserve all six pages on
v80 before final review/CI, keeping v79 observations clearly labeled. No claim
that a v79 observation proves v80 behavior.

## Exit criteria

All six saved pages have real-Chrome evidence and DOM/model comparisons;
blocked-line reasons and once-only questions are inventoried and regression
claims are truthful. Every discrepancy is repaired within the strict boundary
or evidenced and parked, never silently accepted. Independent review accepts
the final curated candidate, exact-head CI is green, and the old parked
browser-observation item is retired with any new specific defects kept visible.

## Decisions and review dispositions

P0 observed the original eight v79 pages, then added separate itemizing mortgage
observations without replaying the original capture. The $4,000 mortgage uses
the standard deduction; $20,000 makes itemization relevant. Its initially
blocked Schedule A names the missing no-other-line16 declaration; supplying
that explicit synthetic answer publishes the attachment. This was a fixture
gap, not grounds for a content or renderer repair. Keep both the negative and
completed positive case in regression coverage.

The six required cases have values/reasons/attachment states and small DOM
excerpts in the P0 evidence. The corrected-to-no covered sale visibly says
“Record this sale as a noncovered sale. The broker did not report its basis to
the IRS.” Blocked variants expose the shared question, but repeat it across
34/32 line-local reason lists. No once-only-question claim is made.

Decision: Track 1 remains tests/tools/evidence only. No presentation repair is
selected. The categorical line-6c instruction says not_elected where the page
requires checked; Schedule 1's top-entry field has no citation. Their safe
renderer alerts are observed defects requiring published-content/successor
work, parked for the core-v80 line. The question duplication originates in the
page's per-line rendering; fixing that outside the permitted derivation seam
is deferred to a separate presentation change. Ordinary Schedule A8a and its
attachment subtotal are absent while the special mortgage explanation shows
the amount; record that separate surface gap without assuming a contract that
requires a particular row layout.

Regression tests assert correct amounts, sentences, truthful nonempty blocked
reasons, explicit attachment states and complete-scope mortgage behavior.
Diagnostic tests must detect the parked alerts/duplicate questions as findings,
not bless their exact counts or absence of output. No skip/xfail or broad
allowlist may conceal new discrepancies. Independent fresh-reader review
checks this distinction and all six cases before publication.

Fresh-reader review accepted the actual adopted saved-page/Chrome path and
lifecycle boundaries, but found one checker defect: the parked Schedule 1
alert exemption also hid a model value changed from zero to 999. That is not
accepted characterization. Repair must independently constrain the expected
zero and source semantics before classifying the alert, with an explicit
mutation regression. The same review identified contradictory complete-scope
input prose; correct future manifests without rewriting historical captures.
No production repair or broader scope is selected by these findings.

Both findings were repaired and independently closed. The exact known zero,
source finding, explanation, instruction and adopted dependency pins constrain
the alert classification; changed-value/explanation/source/authority mutations
produce unexpected findings while retaining the visible diagnostic. Future
complete-case prose is accurate; historical observations remain separately
described. The reviewer independently executed these assertions against the
retained actual ten-case capture without repeating Chrome or broad suites.

## Outcome and verification

Subsequent Linux run 42719255831 passed all four full-suite shards and required
verify, including the real short-temp Chrome route. Its quick job failed only
the integration-checkpoint test's 7.2-second call. The bounded follow-up profile
isolated 6.953 of 6.958 cold seconds in schema meta-validation; the warmed call
was 0.010 seconds. Main's post-test schema-cache restoration was incorporated
by rebase; the checkpoint test and its assertions were left unchanged. The
focused test passed on that baseline. A single local fast lane had 1,769 passes,
eight skips and 11 other budget failures, all listed without waiver in
sale-page-observation-evidence/checkpoint-test-cost.md; mypy passed 484 files.
The latest main synchronization preserves further upstream changes and still
requires independent final acceptance and fresh exact-head CI.

The remaining-budget follow-up classifies the actual Git checkout cases and
the full-corpus generator rebuild individually as live, retaining inexpensive
unit checks in the fast lane. All still run in the full suite. The nominee
test now loads its complete corpus once inside the timed call and gives each
of its six real runtime/package-validation mutations a fresh deep copy. No
assertion, content coverage, budget or production behavior was removed.
Collection confirmed 30 live and 26 fast cases in the affected modules. All
56 focused tests passed; the single follow-up fast lane passed 1,763 with
eight skips and no budget failures in 15.96 seconds; mypy passed 487 files.
The earlier red timings remain historical observations in the cost account,
not waived failures or a green claim for the final Linux head.

The November 9 repair rebased onto main after the v80 through v82 successors,
preserving upstream content and the lattice test's live-lane correction. Old
v79 captures remain v79 evidence. All ten scenarios were reobserved on v80
through actual saved pages and Chrome; this is not a v82 observation claim.

The former workspace-nested TMPDIR produced a 103-byte CI temp root and an
approximately 145-byte singleton socket path, exceeding Linux's 107-byte limit.
Chromium makes that startup error fatal, consistent with the recorded 460 ms
SIGABRT; historic raw stderr was not retained, so the exact old abort is not
claimed directly reproduced. Chrome now gets a short private system-temp root
independent of a long inherited TMPDIR. The owner removes only that root in
finally; launch coordination, deadlines and process cleanup remain unchanged.
The real one-case v80 long-temp regression passed locally in 21.44 seconds,
including adoption, value and context/browser/root cleanup. Independent review
accepted the implementation. The subsequent Linux run above supplied platform
execution evidence; the final synchronized head still needs exact-head CI.
Neither local success nor that later pass recreates the historic abort stderr.

The corrected v80 account is in
sale-page-observation-evidence/v80-reobservation.md. It records the additional
Q2 absence answer, preserves the original unanswered/stale Q1 meaning, and
discloses the provisional incomplete capture and corrected metadata label.
After that adaptation, focused diagnostics passed six tests in 1.10 seconds,
one fast lane passed 1,737 with eight skips in 16.80 seconds, and configured
mypy passed 476 files. These are local checks, not a replacement for Linux CI.

The first ready-event CI run, 42333453979, passed quick/precheck and three
full-suite shards, but the new browser fixture errored before page assertions
in the fourth shard after 200.96 seconds. Its generic browser-observation-failed
message and retained artifacts do not establish the cause; the observer's
private launch trace was not uploaded. This is not a proven startup flake.
A bounded diagnostic iteration adds closed-vocabulary Node stage/category and
sanitized launch evidence to the exception retained in CI's pytest.xml. It
does not establish that the original failure is fixed. Independent delta review
accepted the diagnostic change after repairing one malformed-trace case:
undecodable optional evidence must not mask the primary failure. Four focused
diagnostic tests and mypy (469 files) passed after that repair. Fresh exact-head
CI remains required.

Diagnostic checks passed three focused tests, Node syntax and mypy (469 files).
One fast-lane run passed 1,677, skipped eight and failed ten existing tests on
the three-second budget. These failures are retained in ci-diagnostics.md,
not retried or waived as infrastructure. Prior passing measurements below
describe their original candidates, not the diagnostic candidate.

Track 1 runs ten actual coordinator/saved-page/Chrome cases in one live test,
with fresh contexts, shared launch coordination, bounded waits and owned
cleanup. Focused live verification passed in 70.87 seconds; fixture safety
passed 17 tests; final repair fast lane passed 1,687 with eight skips; configured
mypy passed 468 files. No production files or old goldens changed; no local
full suite was repeated for this tests/tools-only track. Final curated-range
review and exact-head CI remain publication gates, not implied by local checks.

The broad browser-observation parked item is retired in favor of specific
content/presentation findings in the phase roadmap. This milestone neither
publishes a tax successor nor claims the pages have no defects. Small excerpts
and the case matrix survive in the distilled P0 evidence; working charters and
redundant supplement reports are removed after distillation. The retrospective
records the fixture correction, review repair and remaining boundaries.
