<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "student-loan-result-explanation",
  "status": "Closed 2026-10-06. Schedule 1 line 21 explains its saved result on the existing reader: each statement, its amount and loan, what the person said, what the application assumed, what is left with the person, how the amount was worked out, and which statement a blocking reason names.",
  "scope": [
    "one Schedule 1 line 21 explanation using the completed bounded route",
    "reported amounts, ordinary answers, derived results, assumptions and responsibilities kept distinguishable",
    "statement-specific reasons for changed or blocked results recovered from saved output"
  ],
  "non_goals": [
    "no new tax coverage, allocation policy or manual-result input route",
    "no general explanation framework, input wizard or free-text interpretation",
    "no ADR 0076 Part 3 decision or institutional verification service"
  ],
  "deep_reads": {
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-06-student-loan-result-explanation.md",
      "docs/phases/tax-concept-derivation/milestones/student-loan-result-explanation.md",
      "docs/phases/tax-concept-derivation/tax-concept-derivation-overview.md"
    ],
    "implementation": [
      "docs/phases/tax-concept-derivation/milestones/student-loan-result-explanation.md",
      "docs/adr/0077-shared-key-count-basis-same-run-read-and-presence-selection.md",
      "AGENTS.md#Data Safety Rules",
      "AGENTS.md#Schema Publication Protocol"
    ],
    "review": [
      "docs/phases/tax-concept-derivation/milestones/student-loan-result-explanation.md",
      "docs/roles/qualitative-review.md",
      "AGENTS.md#Data Safety Rules"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-10-06-student-loan-result-explanation.md"
}
-->

# Student Loan Result Explanation

Milestone key: `student-loan-result-explanation`.
Primary branch: `milestone/student-loan-result-explanation-bounded-reader`.
State: **closed 2026-10-06.** Tracks 0, 1a and 2 are complete, and the owner
approved the presentation. The milestone explains the current engine's results
without changing them. Input-transition and assumption-management design is
deferred ("Input transition (deferred design)").

## Actions

These are the milestone's actions in order, with their outcomes.

1. Produce real saved results through the existing coordinator for the
   supported, blocked and mixed cases, and open the actual page for each.
   **Done in Track 0a**: ten cases, thirteen saved runs.
2. Write down, for each of the five reader questions, what the page already
   answers, what the saved result holds but the page does not show, and what
   is not saved anywhere. **Done in Track 0a** ("What the investigation
   established").
3. Have an independent reviewer follow the data into the rendered page and
   check that account before any build is selected. **Done in Track 0b**:
   accurate with corrections, which are folded into the account below.
4. Show the owner the current display and our recommended changes before
   settling wording or interaction. **Shown 2026-10-04.**
5. Decide what appears on line 21 itself and what goes in its supporting
   detail, and trace every sentence to a saved value, pin or adopted
   declaration. **Design P1–P9 below, revised after the Track 0c review.**
6. Supply the explanation data the page needs but the saved result lacks,
   without changing any calculation. **Done in Track 1a**: `line21Explanation`
   in the saved presentation, covered by real-path cases.
   - Answers saved without their question wording keep their response and
     identity.
   - Blocking reasons keep each statement's structured identity. A row a
     reason names therefore carries no basis, including for two affected
     statements and for two statements with identical display labels.
   - A sentence reached through two reads of one statement appears once.
7. Present that data in the existing reader and walk through the rendered
   page with the owner. **Done in Track 2. The owner approved the
   presentation on 2026-10-06.** Two independent reviews of the display
   passed after repair.
8. Check that old-only workspaces and unrelated lines read as before and that
   both runners still agree. **Done.**
   - The Track 5 worksheet integration, deduction end-to-end, Track 8
     presentation-golden and presentation modules pass. They require runner
     agreement in every case.
   - The frozen evaluation copy under `tools/presentation_harness/` is
     unchanged. It therefore intentionally diverges from the production page,
     and its tests do not exercise the new display.
9. Close the milestone and assess whether the phase's exit criteria are met,
   rather than adding another tax category. **Done**: see "Outcome and phase
   assessment".

## Purpose

The application can now use a person's loan and schooling answers to work out
a bounded student-loan deduction. The next task is to let that person understand
the result without reading engine records or asking an agent to interpret them.

Starting at Schedule 1 line 21, a reader should see which statements contributed,
which answers mattered, how the reported amounts became the deduction, and what
the application assumed rather than established. If calculation stops, the
reader should identify the affected statement and understand whether an answer
is missing, a relationship changed, or the circumstance is outside the supported
calculation.

This is the bounded next step in roadmap item 13, not a full user journey. It
tests whether the distinctions built during the phase help a person inspect an
actual result. Success supplies a concrete example of the phase's explanation
step, without requiring broader tax coverage.

## Starting point and readiness

Student Loan Deduction Completion merged in PR #203. Its v41 package connects
the plain supported relationship case to the worksheet and line 21. The
committed end-to-end story covers corrections, withdrawal, interrupted saves
and re-answering. The page already shows blocked-line reasons; do not rebuild
that capability under a new name.

The support rule declares four kinds of basis: what the person said, what rules
derived, favorable assumptions, and conditions left with the person. That is
not proof that all four reach the page. Trace each intended explanation through
the actual coordinator, saved presentation and page before claiming it exists.

Two prior follow-ups matter directly: the no-link standing does not pin a denied
statement inclusion, and a blocked line still exposes a technical dependency-code
message. Establish what each prevents the reader from understanding. Neither
automatically warrants a general provenance or renderer redesign.

The prior retrospective also reports torn-log append corruption, a runner/default
disagreement and an entrypoint-validation gap. These remain engineering
follow-ups, not dismissed defects. Readiness must determine whether any
invalidates the selected execution path. A reproduced dependency defect must be
repaired or change the scope before accepting affected evidence. Unrelated
repairs are not bundled into this reader milestone.

## What the reader needs to understand

1. What was reported, and which statement does each amount belong to?
2. What did I tell the application about that statement, borrowing and schooling?
3. What did the application conclude and calculate from those answers?
4. What did it take as given, and what conditions remain my responsibility?
5. If it cannot calculate, what is unresolved or unsupported, and what can I do?

Answers should be short initially, with supporting detail available nearby.
The worksheet's limit or phase-out differs from a statement's support decision.
Show their actual contribution when relevant, using the adopted calculation,
not a second calculation in the reader.

An assumption is not an answer the person gave. A responsibility notice is not
a missing input or a request for certification. An unsupported case is not a
legal ruling that the deduction is unavailable. A past result describes its
run, not the workspace's current state after later edits.

Refine these distinctions against examples rather than first drafting a
comprehensive explanation vocabulary or contract.

## Scope and boundaries

Build the smallest necessary addition to the existing projection and reader for
this one line. Include narrow rule-content provenance repairs if the reader
cannot trace an answer it explicitly attributes to the person. Adopt successors
where published artifacts must change; preserve old bytes. No new schema or ADR
is presumed necessary.

Keep tax arithmetic, answer meanings, relationship lifecycle and coverage
unchanged. No interest allocation, manual override, mixed-period policy,
institutional catalog, interactive correction editor, free-text intake,
cross-year workspace or general run-comparison service. Before/after examples
may show two saved runs without building a run-diff product.

The display can explain an existing question or point to an existing correction
route. It must not promise an unbuilt UI action. No new substantive tax claim
is needed merely to explain an adopted result; if investigation needs one,
verify its controlling primary source separately.

## Plan development and review

### Opening investigation — inspect before prescribing

Track 0a is chartered as one Builder unit, which inspects and records but
changes no product code. An independent Reviewer then checks the resulting
account (Track 0b) before the Foreman recommends a design to the owner.

Generate real saved results from the existing synthetic fixtures and inspect
the current page. Begin with supported and blocked cases, then the mixed case
below. For each reader question, name what the page already answers, what the
saved output carries but does not show, and what needs new information. Keep
this in the plan or one bounded working evidence file, not another specification.

Independently review this map before Track 0 selects a build. Follow the data
into the rendered result, not the description alone. Review consequential
sections while small rather than waiting for a finished large plan. Show the
owner the actual initial display before freezing wording or interaction choices.

### What the investigation established

Track 0a produced ten cases (thirteen saved runs) through the real path.
Track 0b reproduced them and corrected the account's view of what is saved.
The decisive facts:

- **The page shows a final number and blocked reasons, and little else.** A
  published line 21 shows the number, a stock sentence ("…under complete
  eligibility authority") and 48 source chips. Most chips are wage,
  capital-gain and other Schedule 1 records. Opening a student-loan chip
  shows a pin id and nothing a person can read. Blocked reasons are specific
  and actionable, but sit under "Missing dependency code(s):
  DEPENDENCY_INVALID".
- **No statement is shown on a published line, and no supported statement on
  a blocked one.** Two statements produce one combined "Reported subtotal" in
  the Schedule 1 attachment. When one statement blocks, the supported one is
  never mentioned.
- **The explanation data exists at run time and is then discarded.**
  `build_presentation_model` receives the following, and drops all of it:
  - the adopted rules, including the support rule's four basis groups;
  - the run's findings, which hold each statement's box 1 amount;
  - the run's publications, which hold each statement's support and
    standing values.

  The saved output keeps dispositions and pins but no values. So "not shown"
  here is a projection omission, not missing upstream information.
- **Two things are genuinely not saved.**
  - A statement link corrected to "no" leaves no pinned finding in the run.
    It reads exactly like a link never answered.
  - The worksheet's limit and phase-out amounts are computed inside one
    expression and never published. Only worksheet line 1, the interest
    subtotal, is published.
- **Labels are borrowed from evidence.** A chip's label is whatever the
  evidence was submitted with. The fixtures label box 1 amounts "Synthetic
  Track 14 answer", so a reported amount reads as an answer.
- **Readiness.** None of the retrospective's engineering follow-ups touches
  this path:
  - Package v41 is inside the entrypoint check's enabled set.
  - Both runners agreed on all thirteen runs.
  - A run does not append to the log.

### Design (P1–P9)

These recommendations were applied under the owner's direction of 2026-10-04
to proceed on recommended choices. The owner approved the rendered
presentation on 2026-10-06. Track 0c independently reviewed the first version
and found it sound with changes, which are incorporated here.

A statement's support result is not its standing on line 21. The worksheet's
selected path also reads the four retained answers, scope and filing facts.
A statement can be `plain-case-supported` while line 21 blocks on that same
statement, and the old path publishes a deduction while every statement reads
`not-supported`. So the reader never derives a statement's status from its
support or standing values alone.

- **P1. Statements on line 21.** On published, zero and blocked lines, list
  every statement the run used, plus any statement named by a line 21 reason.
  Each row shows:
  - the statement label;
  - the loan or loans its current inclusion links it to, by their recorded
    description;
  - its amount: the box 1 finding that the worksheet's line 1 subtotal pins
    for that statement, so the rows add up to line 1. A removed statement has
    none.
  - its status, saved as `named-by-reason` or `no-reason`. A row a reason
    names says "See the reason above" and links to it; other rows add
    nothing. Status comes from the reasons the projection already produces,
    not from a new status vocabulary.
- **P2. Why a statement's loan link holds.** Show this detail only on a row
  where both conditions hold:
  - the run published `tax.us.2025.sli.statement-loan-support` =
    `plain-case-supported` for that statement;
  - no line 21 reason names it.

  It is labelled as support for the statement's loan link, not as the
  deduction. It has three parts:
  - **What you told us.** The run's findings reached from that support
    finding through its published intermediate findings. Keep only the four
    fact types its `said` group describes:
    - `financing-relationship`;
    - `statement-inclusion-relationship`;
    - `loan-paid-only-school-costs`;
    - `enrolled-at-least-half-time`.

    Never select findings by evidence label. Each shows the response and the
    proposition the person was asked, as saved in that answer's review
    evidence. The durable recorder permits answers without that wording.
    Such an answer keeps its response and identity, omits the proposition,
    and says "Question wording was not saved with this answer." The page
    never infers a historical question from today's question constants, and
    never fails the whole presentation over this gap.
  - **What the application took as given.** The rule's `assumed` group.
  - **Conditions left with you.** The rule's `left_with_person` group.

  Both groups are copied from the exact rule version the run adopted. The four
  retained yes/no answers fall outside this walk, and this version does not
  show them.
- **P3. How the amount was worked out.** Show only on a published or
  computed-zero line 21:
  - worksheet line 1 (reported interest);
  - the total income the worksheet read;
  - only the parameters that line 21's own finding pins, each at the run's
    filing status;
  - the deduction.

  The page says it does not state which limit applied. Nothing saved records
  that, and the reader does no arithmetic. A zero line that pins no parameter
  shows no limits, because a scope answer, not a limit, made it zero.
  Publishing the worksheet's intermediate amounts would need a worksheet
  successor and is not built.
- **P4. Run identity.** Show the run id and the workspace revision the run
  read. `live_coordinate_run` already holds the revision.
- **P5. Technical code.** Drop "Missing dependency code(s)" from line 21 when
  specific reasons are present. The Schedule 1 attachment's own
  `DEPENDENCY_ABSENT` notice is neighboring presentation; it is recorded, not
  changed.
- **P6. Source chips.** On line 21, move the existing chips into a collapsed
  "All records this line depends on" group below the statement list. Other
  lines are unchanged.
- **P7. Saved "no".** No content successor. The no-link sentence is accurate,
  and attributing the "no" to the person would need new rule pins. The
  follow-up stays carried.
- **P8. Contract.**
  - `presentation-model.v1` has no published schema. The new data is one
    optional top-level block with its own strict validator, the same pattern
    as `provenanceGroups` and `authorization`.
  - It is emitted only when the adopted package carries the statement-support
    rule, so package v33's committed goldens are unchanged.
  - Its reasons match rows only by the statement's
    `(lender, statement, tax-year)` identity, never by display label.
  - It is separate from the experimental `calculationView` and shares no
    validator path with it.
  - Old saved models validate and render as before. A validator from before
    this change would reject a new model; no such reader runs separately from
    this repository.
- **P9. One answer, two statements.** Two statements on one loan, with
  enrollment answered no, produce two identical sentences. P1's rows show each
  statement's loan, so the shared answer is visible. Reasons are not merged.

### Track 0 — settle the bounded reader design

Select what appears on the line and in its supporting detail. Trace each
sentence to a value, pin, disposition or exact adopted declaration. If
provenance is unavailable, do not invent a personal answer or legal cause.

Use a disposable rendered probe only for a consequential unresolved choice.
Rivals are conditional on an observable difference between competing designs,
not mandatory. Demonstrate the selected shape through saved output before
declaring implementation ready. Independently review explanation semantics and
any contract change before building.

### Implementation — two units

1. **Track 1a.** Copy P1–P4's data from run time into the saved
   presentation, through the production path. Test the reloaded output and
   that calculations are unchanged. No content or calculation change.
2. **Track 2.** Present it in the existing reader (P1–P6). Inspect the page
   with the owner, and complete end-to-end and compatibility checks.

Both units were built as planned: Track 1a holds the saved data and its
validator, and Track 2 holds the page.

## Synthetic cases and evidence

Reuse prior committed fixtures. Do not hand-author the decisive presentation
model and call its successful render an end-to-end result.

| Case | What the reader must distinguish |
| --- | --- |
| Supported case, including the existing 3,000-to-2,500 example | Reported interest versus deduction; actual answers and rules versus assumptions and responsibilities |
| Two supported statements | Each amount and its own relationships; no cross-attributed account |
| Missing enrollment answer versus explicit no | Missing information versus an answered circumstance outside the supported route |
| Inclusion corrected to no | Current relationship state; saved answer traced if text attributes it to the person |
| Schooling link withdrawn, restored, then enrollment re-answered | Restoring the relationship does not revive its ended answer; each saved result describes its own inputs |
| Removed or applicability-unestablished statement beside a supported statement | Aggregate blocked; unresolved statement still visible; supported statement not falsely blamed |
| Old-only workspace and unrelated return line | Existing calculation and explanation remain valid, with no new student-loan prerequisites |

Use `live_coordinate_run`, reload its durable presentation after discarding the
in-memory run, then render the real page. Check relevant visible text and inspect
layout. Test provenance separately: a legible sentence does not prove its
attribution true. Preserve calculation expectations and both-runner comparisons
where the changed surface reaches them.

## Decisions

| Question | Disposition |
| --- | --- |
| What belongs on the line versus in detail? | P1–P6, approved by the owner with the rendered pages |
| Does declared basis reach saved output, or must projection change? | The projection copies it; the projector already received it |
| What pins must change to attribute a denial? | None in this milestone (P7); the saved "no" stays a carried follow-up |
| Does the change alter a published contract? | No published schema; one optional block with its own strict validator (P8) |
| Is the asked wording saved with each answer? | Reviewed entry saves it. The lower-level recorder may omit it, and the page then says so |
| Show the four retained answers beside P2? | Not in this version |

## Input transition (deferred design)

The owner asked for this design check alongside the reader work. It selects
no mechanism and makes no intake or engine change. Nothing here waits on an
owner choice.

**The case examined.** One Form 1098-E statement already has the older
tax-labelled answer `tax.us.2025.f1098e.no-non-qualified-loan-component`. The
person later records borrowing and schooling details for it through the
relationship recorder:

- the borrowing, and the schooling it paid for;
- that the statement includes that borrowing;
- whether the loan paid only school costs;
- whether the student was enrolled at least half-time.

### Intended behavior (owner direction, 2026-10-06)

New information changes the conclusions and assumptions it bears on. It does
not automatically erase earlier statements or change unrelated subjects.
Recorded answers are preserved unless a justified, scoped reason supersedes
them.

- **Different statements, different input methods.** Giving Cedar loan
  details does not invalidate Birch's older answer. It does not require Birch
  to supply new details either. Birch's answer is preserved.
- **Four distinct changes, kept distinct:**
  - retiring an old input method;
  - superseding a person's statement;
  - changing which information supports a conclusion;
  - changing which assumptions the application relies on.

  The newer details are not equivalent to the older answer. The support rule
  `said` group shows that they establish some matters directly. Its `assumed`
  group shows that the application assumes others, among them that "Box 1
  holds no loan the person did not record".
- **Assumptions adjust as information arrives.** That adjustment should be
  flexible but systematic, as relevant information arrives.
- **An older "no" never disappears silently beneath favorable assumptions.**

### Current limitations (what the engine does today)

- **The both-present refusal.** Since owner decision 2 of 2026-10-01, a return
  with the older answer on any statement and a loan link on any statement
  refuses line 21 with `old-and-new-sli-inputs-both-present`, even when they
  agree. This is an implementation limitation, not the desired behavior. It is
  not missing information for the person to provide.
- **The sentence that refusal shows.** The declared sentence in the adopted
  worksheet content tells the person to "Remove that older answer or remove
  the loan links". So today's page asks for a recorded answer to be removed to
  fit that limitation.
  - The reader shows that sentence faithfully, because it is the current
    engine's stated reason.
  - Changing it is a rule-content (package) change, which is outside this
    reader milestone. Revisit it with mixed-method support.
- **No assumption adjustment.** The recorder does not adjust assumptions when
  information arrives, and keeps every recorded answer current until the
  person changes it.

### Deferred design

- **Mixed-method support.** A return in which different statements use
  different input methods. The question is how line 21 should combine them
  instead of refusing.
- **Assumption management.** How a conclusion's assumptions change as
  relevant statements arrive, and how the explanation shows which
  information supports a conclusion and which the application assumes.
- **What an older "no" establishes.** What the "no" actually establishes,
  and what stays unresolved beside newer details. Only after that is
  understood can any clarification question be chosen.
- **Unselected possibility, not adopted.** A recorder step could end a
  statement's older "yes" when that statement gains an affirmed loan link.
  It would end the answer in the same save and keep the history, using the
  pattern of `_stage_enrollment_follows_schooling`. It is withdrawn as a
  selected design, because it would supersede a person's statement merely to
  satisfy exclusive-path selection.

## Track 0 adversarial closure

The design only displays results; it adds no fact, rule or calculation. The
gate applies through claim reuse (showing a rule's basis beside a statement)
and neighboring presentation. Track 0c attacked the first version and its
corrections are folded in. The three items that were conditions at design time
are now demonstrated by Track 1a's and Track 2's saved-model tests.

- **Authority-lifecycle table: PASS.** Every displayed item is a value or
  declaration of the run it describes, captured when that run builds its
  presentation:

  | Item | Meaning | Scope | Depends on | Invalidated by |
  | --- | --- | --- | --- | --- |
  | Statement amount | Box 1 that line 1 counted for that statement | One statement, one run | The box 1 finding the line 1 subtotal pins | A later correction; the saved run keeps its own |
  | Row status | Whether a line 21 reason names the statement | One statement, one run | That run's line 21 reasons | A later run |
  | Basis groups | Declared basis of `plain-case-supported` | That rule version | The adoption pin in the run | A rule successor; the run names its version |
  | Answers shown | Answers of four fact types reached from the support finding | One statement's inclusion and loan, one run | The support finding, transitively | A later answer; the saved run keeps its own |
  | Working | Line 1, the income the worksheet read, the pinned parameters | One run | Line 21's own pins | A later run |

- **Empty/nonempty authority matrix: PASS.** Each row is covered by a saved
  model from the real path.

  | Return state | Line 21 | Rows | P2 | P3 |
  | --- | --- | --- | --- | --- |
  | No statement | 0, closed empty | none | — | — |
  | All supported, retained answers yes | published | no reason named | shown | shown |
  | Supported, retained answer missing or "no" | blocked | named by reason | not shown | — |
  | Old and new inputs both present | blocked | named by reason | not shown | — |
  | Old path only | published | no reason named | not shown (`not-supported`) | shown |
  | Claimed as a dependent | computed zero | no reason named | shown if supported | line 1 and zero, no limits |
  | Schedule 1 Part II out of scope; unclosed family | blocked, no reasons | no reason named | shown if supported | — |
  | One blocked (removed or replay-marked) beside one supported | blocked | blocked one named; other not | the other only | — |
  | Support itself blocked (stale schooling) | blocked | named by reason | not shown | — |
  | Removed statement only | blocked | named, no amount | — | — |

- **Late-member lifecycle: PASS.** A run, a second statement, then another
  run: the first saved model is unchanged, and the second includes the new
  statement.
- **Neighboring capability dependency diff: PASS.**
  - Other lines gain nothing.
  - The block is emitted only for packages carrying the support rule, so the
    v33 goldens are unchanged.
  - Old-path-only rows carry no reason and never show "no loan link".
  - The page change is scoped to line 21's section.
- **Reused-claim semantic/lifecycle equivalence: PASS.** The basis
  describes `plain-case-supported` on one statement, which requires exactly
  one current inclusion. P2 shows it only where that exact publication exists
  and no reason names the statement. The negatives are tested: the old path
  only, a retained answer missing, and both paths present, for one statement
  and for two.
- **Integration surface: N/A.** No producer of a bound symbol changes. The
  presentation join is read-only and the new block is optional.
- **Limits of the explanation, not of its correctness:**
  - P2 omits the retained answers.
  - P3 does not say which limit applied.
  - P7 leaves the saved "no" unpinned.

## Completion

The selected saved cases must support the five reader questions, the real page
must show them without false attribution or broader tax claims, and the owner
must have a chance to inspect the result. Readability feedback and executable
correctness are separate evidence. Missing browser access must be reported,
not counted as a successful render check.

Run focused projection/page/content tests, applicable typing and safety checks,
and the required full suite for substrate changes. Final independent review
binds the curated branch; CI binds its final head. Use synthetic demo data only
and keep scratch renders ignored. Publish behavior, tests, necessary contracts
and a short account of what the person can now understand, not a repair diary.

At closeout, assess the phase's existing exit criteria against delivered
capabilities and present a bounded closure recommendation. Do not automatically
add another tax category or user-journey milestone. Manual scoped values,
mixed-period treatment and a broader guided application remain later choices.

## Outcome and phase assessment

A person reading Schedule 1 line 21 on the existing page can now see:

- each statement, its loan and the amount it reported;
- for a supported statement, what they said, what the application took as
  given, and the conditions left with them, each as a separate group;
- how the amount was worked out from line 1, the income the worksheet read
  and the limits it pinned;
- which run and workspace revision the explanation describes;
- on a blocked line, which statement each reason names, with no favorable
  detail shown for a statement a reason names.

No calculation changed.

**Phase exit criteria** (`tax-concept-derivation-overview.md`):

- **Criteria 1–7** were met by the earlier milestones:
  - a production derivation from reported and ordinary facts through
    adopted rules;
  - classification that changes with circumstances;
  - a return field consuming the derived concept through the worksheet;
  - meaning separated from executable coverage;
  - identified subject, period, rule version, facts and authority;
  - deliberate refusal of unsupported adjacent cases;
  - a contrasting concept: a relationship-decided adjustment beside
    interest income.
- **Criterion 8**, a fresh reader recovering what the result means, how it
  was derived, where it appears and what the model does not establish, is
  met for line 21's bounded route on the owner's inspection.
  - No context-starved reader has checked it.
  - A phase-boundary legibility audit (`docs/legibility-audits/`) is the
    evidence that would settle it.

Its limits are recorded rather than hidden:

- the explanation sits low on a long page, below Form 1040 line 10's
  identical amount;
- the both-present refusal tells the person to remove an answer to fit an
  engine limitation;
- the retained answers, the limit that applied, and a saved "no" are not
  shown;
- relationship answers display their recorded values, such as
  `sli.financing.affirmed`, and the limits display their parameter ids,
  because neither has a declared label.

**Recommendation:** the phase's exit criteria are met in bounded form. The
next selection should weigh closing the phase over adding another vertical
inside it. Several items are better framed as candidates for a later phase:

- mixed-method input;
- assumption management;
- mixed periods;
- person-supplied scoped values;
- a broader explanation and question journey.

This is a recommendation for the owner's selection, not a decision taken
here.
