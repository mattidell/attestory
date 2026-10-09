<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Evolving Workspace Accounts",
  "topic": "account-refinement",
  "status": "Closed 2026-10-08. One Form 1098-E can gain loan detail while another keeps its older answer; line 21 combines them per form (core calculations v42, worksheet v5) and the saved explanation separates what was said, used, assumed and recorded but not used.",
  "scope": [
    "one student-loan account gains detail while another preserves its older answer",
    "distinguish preserved statements, changed calculation support and assumptions",
    "test and implement bounded mixed-method handling if semantic and contract readiness is established"
  ],
  "non_goals": [
    "no automatic retraction merely to satisfy exclusive input-path selection",
    "no universal assumption-management or supersession framework",
    "no new tax coverage, allocation policy, institutional verification or broad intake UI"
  ],
  "deep_reads": {
    "new_milestone": [
      "docs/phases/evolving-workspace-accounts/evolving-workspace-accounts-overview.md",
      "docs/phases/evolving-workspace-accounts/evolving-workspace-accounts-roadmap.md",
      "docs/phases/evolving-workspace-accounts/milestones/account-refinement.md",
      "docs/phases/tax-concept-derivation/milestones/student-loan-result-explanation.md#Input transition (deferred design)",
      "docs/milestone-retrospectives/2026-10-06-student-loan-result-explanation.md#What should change in the next plan"
    ],
    "implementation": [
      "docs/phases/evolving-workspace-accounts/milestones/account-refinement.md",
      "docs/process/planning-and-development.md",
      "docs/adr/0077-shared-key-count-basis-same-run-read-and-presence-selection.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/phases/evolving-workspace-accounts/milestones/account-refinement.md",
      "docs/roles/qualitative-review.md",
      "docs/process/planning-and-development.md"
    ]
  }
}
-->

# Updating an Account Without Losing Its Meaning

Milestone key: `account-refinement`.
Branch: `milestone/account-refinement-student-loan`.
State: closed 2026-10-08.

## What we are trying to accomplish

A person has two interest statements, Cedar and Birch, with older eligibility
answers. Later they describe Cedar's borrowing and schooling. Birch has not
changed. The application should understand what the added detail contributes,
preserve the person's earlier account unless there is a reason to supersede
it, and leave Birch alone.

Today the calculation chooses one input method for the entire return. Old
answers beside newer relationship facts can therefore block the deduction even
if nothing the person said disagrees. Removing information merely to satisfy
that choice is not the intended product behavior.

The target is one production-supported transition, with a saved explanation
of its basis. Different statements using different supported input methods
should not by itself prevent calculation. Genuine missing or adverse
information still matters. Preserving an unrelated statement's account does
not promise an aggregate deduction while a required component is unresolved.

## Why this is not simply replacing one answer

The older answer says no non-qualified-loan component is included in the
statement's box 1. The newer account identifies a borrowing, schooling,
statement inclusion, and ordinary loan-cost and enrollment answers. It does
not establish everything the older answer asserted. The current support rule
also makes explicit assumptions, including that there is no unrecorded
borrowing in that amount.

Adding a link is not proof that the older assertion is now redundant. Nor
does stopping use of that assertion mean the person withdrew it.

An older "no" is not a mild challenge. The adopted content defines it as the
person's assertion that the excluded kind of loan is present in that
statement's box 1, and today it blocks the deduction for the whole return,
Birch included. It still does not tell us which ordinary circumstance
explains it. Do not equate it with an unrecorded second loan. Whether a "no"
on one statement should bar another statement is a tax question, not yet
checked against primary authority (see "Questions that remain open").

We need a short, revisable model that keeps distinct:

- the circumstances and subjects being described;
- what the person actually asserted and its scope;
- what the application concludes from information it uses;
- what the adopted method assumes or leaves with the person;
- how the engine represents and combines those results;
- what the saved explanation lets a person understand.

The model's purpose is comprehension and better design, not a new contractual
taxonomy. Specificity should grow only as the investigation supports it.

Terms used below:

- An **input method** is one of the two ways the adopted worksheet accepts a
  statement's eligibility: five yes/no answers, or loan links (borrowing and
  schooling details).
- A **statement inclusion** is the person's statement that a given 1098-E
  statement's box 1 includes interest on a named borrowing.
- The **basis groups** are the support rule's declared lists of what the
  person said, what the rule derives, what it assumes, and what it leaves with
  the person.
- **Shared answers** are the four yes/no answers that both input methods read.
  They are distinct from answers the person's account *preserves*.
- **Track 0** is the gate where the selected behavior is attacked before
  production work is chartered.

## Starting evidence and contracts to examine

The base is merged PR #204. Production package `core-calculations` v41 has the
bounded deduction route; the reader now preserves and displays its explanation.
The predecessor's deferred input-transition account is context, not a selected
automatic-retirement mechanism. Its reader repairs are complete.

Trace these actual surfaces and neighboring consumers during investigation:

- `packages/content/tax/2025/f1098e.bundle.json`: the older answer's full
  meaning and identity, not just its name.
- `packages/content/tax/2025/rule.sli-statement-loan-support.json`: ordinary
  inputs, required relationships and the separate basis groups.
- `packages/content/tax/2025/rule.sli-worksheet.v4.json`: return-wide
  selection, per-statement reads, shared answers and aggregate arithmetic.
- `packages/content/tax/2025/sli-worksheet-inputs.bundle.json`: the
  person-facing sentences, including the both-present sentence that tells the
  person to remove an answer.
- `packages/tax/sli_relationship_recording.py`: entry, batch saves,
  correction, withdrawal and recovery; a reusable function is not evidence
  that its lifecycle meaning fits this transition.
- The live coordinator, both runners and saved presentation; existing
  worksheet integration and line 21 explanation tests supply synthetic cases.
- ADR 0077 for selection and basis, ADR 0073 for retraction, and ADR 0076
  Parts 1–2 if subject evaluation is reused. Read their actual decisions
  before proposing changes. Existing accepted decisions are not edited in place.

What the adopted worksheet does today (R0, from the v41 content and existing
tests):

- The yes/no method reads five answers per statement. The loan-links method
  reads four of them, the shared answers, plus each statement's
  `statement-line21-standing`. Both use the same return-level requirements
  and arithmetic.
- Only `no-non-qualified-loan-component` belongs to the yes/no method alone.
  Its presence, whether "yes" or "no", is the only thing that activates that
  method.
- The loan-links method activates on any of six statement-keyed facts:
  affirmed, unresolved, denied and withdrawn inclusions, unresolved scope, and
  a replay applicability marker that the system records, not the person.
- The refusal is return-wide and tests only whether those fact types are
  present, not their values. A denied link beside an older "yes" is refused
  today.
- Beyond the refusal, the loan-links method requires every statement to have
  a supporting link. Birch without one would be asked for loan details. So the
  restriction has two layers: selecting one method for the return, and
  requiring every statement to satisfy that method.
- ADR 0077 Part 4 describes the yes/no method as activated by all five
  answers; the adopted content uses one. Reason from the content.

Whether the target needs a content successor alone or a bounded contract or
engine change is unresolved. Do not silently change the meaning of existing
exclusive selection declarations. No schema or ADR successor is preselected.
The older maturity matrix has no student-loan account-transition cell; do not
infer a maturity upgrade or real-data demonstration from its broad rows.

## Required behavior before mechanism

1. Adding Cedar detail does not retract Birch's answer or require Birch to
   provide new detail merely to match Cedar's input method.
2. Statements are not automatically ended to make the current selector work.
   Changing the method and changing the person's assertion remain distinct.
3. A favorable assumption cannot silently bury adverse or unresolved
   information about the same matter. Preserving an answer only in history is
   not sufficient justification for no longer considering it.
4. Each amount is counted once. Statement-local support feeds the existing
   return-level arithmetic; caps, income limits and scope conditions must not
   accidentally be applied once per statement or bypassed on one path.
5. Corrections and withdrawals affect the subjects they actually bear on.
   Shared borrowing dependencies are traced, not presumed independent because
   statements differ. What the calculation should rely on after newer detail
   is withdrawn or corrected is open; an older answer that was never ended is
   still current, so relying on it again is not a "revival". It must not
   happen merely because a method switch is convenient.
6. Saved explanations distinguish recorded answers, the information used by
   the calculation, and assumptions. Earlier saved results remain historical.
7. A remaining implementation limitation is described as such, not as evidence
   that the person failed to supply a fact or must delete a valid answer.

## Develop the plan while doing the work

### P0 — establish the meaning of the transition

Write a compact before/after account for Cedar and Birch. For each older and
newer statement identify its subject, what it asserts, what overlaps, and what
it leaves open. Include one older "no" without inventing its cause. Describe
the current calculation basis. For the changed statement, list the facts a
calculation could rest on afterwards and what each would leave assumed; leave
the choice among them open. Keep changes to the calculation basis separate
from changes to the log.

The initial plan was independently reviewed (R0, sound with corrections,
applied here). An independent review of the P0 account (R1) records whether
the distinctions and the consequential unresolved questions are agreed before
anything becomes a mechanism specification. Success is that agreement, not a
rule for every possible combination.

Distinguish the meaning encoded by existing content from the underlying tax
rule. If a proposed distinction depends on a new tax proposition, verify it
against the relevant primary authority rather than treating a field title or
the predecessor's prose as proof. Do not expand into a general tax-law survey.

### P1 — locate the restriction and possible changes

Trace ordinary recording through replay, source selection, per-statement
support, aggregation and saved explanation. Reproduce the current mixed-method
refusal on a synthetic two-statement return. Name what the current engine
cannot combine, not just the error code it emits.

Separate a per-statement coexistence decision from the same-statement question
of what to do with both an earlier broad assertion and newer partial detail.
List materially different approaches only where they would change behavior.
Do not choose by code size or convention alone. Review consequential sections
while they are small; revise P0 when this tracing changes its basis.

### P2 — test consequential assumptions, then Track 0 selection

Use a small executable comparison when a representation choice changes an
observable result. Rival prototypes are conditional on such a real choice;
independent contexts author competing shapes. A single baseline-versus-candidate
probe is enough for a direct, already-justified change. Which of the two
applies is recorded by the independent review of P1, not by the author of a
candidate shape. State which parts are production, proposed, manually
supplied or omitted.

**P2 as recorded by R2 (2026-10-07).** P1 found three layers to the
restriction:
- one input method for the whole return;
- the worksheet's own requirement that every statement satisfy it;
- the projection, which recomputes the choice.

Line 1 adds every statement's box 1, so one refused statement blocks line 21
for the whole return. A statement that keeps its older answer and gains
detail therefore needs a defined per-statement result. Choosing the method
per statement alone cannot reach the target. R2 accordingly replaced rival
builds with one baseline-versus-candidate probe of Shape B: a per-statement
combined result, read by a successor worksheet with one live path and one
inert path.

**Owner clarification (2026-10-07).**

- **Scope of inputs.** The inputs in scope are the existing, bounded set of
  structured answers and relationships in P0's proposition map, and the
  saved states the actual workflow permits. Free-text statements, new kinds
  of input and a general uncertainty framework are out of scope.
- **Selection principle.** An answer is in scope for its material meaning:
  the defined distinction it makes about the borrowing, the schooling, or
  the Form 1098-E it concerns. A case is added only when it tests a
  consequential distinction in those inputs.
- **Form versus answer.** The Form 1098-E (the "form") is distinct from a
  person's answer or assertion about it. Explanations keep the two apart.
  The central question for each input is: when this answer changes, what
  changes about this particular borrowing or form, and why?
- **No single "adverse or unresolved" group.** P2 does not treat all
  non-supporting link states as one group. Each existing state is classified
  by whether it:
  - contradicts the older answer;
  - leaves a relationship unresolved; or
  - merely lacks detail the newer method needs.
  No class is presumed to invalidate the older answer. The older answer must
  not conceal materially contrary information. A treatment that remains
  unsettled stays explicit, for selection after the probe.
- **Diagnostics are not policies.** The interrupted build left two
  diagnostic rules (`p2-candidate/diagnostics/`). Their result is narrow:
  - the presence diagnostic sees whether an older answer exists, but not its
    value;
  - the requires diagnostic reads the value, but blocks any statement that
    has no older answer. It also maps an older "yes" to supported whatever
    the detail says, and passes detail through when the answer is "no".
  These diagnostics test only whether the engine can read an optional input.
  They do not implement or demonstrate any policy.

P2 therefore runs in two increments, with a review between them.

- **P2a** classifies the existing states and settles whether existing
  constructs can read an optional older answer's value.
- **R3a** independently reviews P2a.
- **P2b** implements complete policies defined over P2a's classes, and runs
  them on the real path. If no existing construct can read the optional
  value, P2b may use a stand-in operator in the temporary copy only. The
  stand-in is labelled proposed, following ADR 0077 Part 1's stand-in
  precedent. Its concrete dependency goes to the owner before any production
  change depends on it.
- **R3** reviews P2b before Track 0.

The prototype gates are discharged here, not in a separate prototype plan:

- **Proposition:** whether a per-statement combined result lets
  different statements use different methods, and what a statement holding
  both yields.
- **Paper:** R2's follow-up eliminated statement-scoped selection.
- **Rung:** persisted end to end on a temporary repository copy.
- **Caps:** P2a and P2b, each with one repair, and R3a and R3.
- **Triage:** owned by the Foreman.
- **Production:** the probe's candidate content is never production. It is
  reimplemented after Track 0.

The choice between the v13 inert path and a rule-artifact successor has no
observable difference. It is settled at Track 0 on contract honesty.

Independently review the evidence and the selected behavior before production
chartering. Track 0 adversarial closure is recorded below and was reviewed by R4 (settled with corrections, applied). Resolve authority,
lifecycle, missing/adverse inputs, identity, changed assumptions and aggregation
for the selected slice. Unknowns that could change this slice's result are not
made favorable by declaring them out of scope.

### Track 0 selection (Foreman recommendation, 2026-10-07)

The evidence is P2b's 205-run matrix: 41 cases, each run under the
baseline and four policies. R3 reviewed it ("adequate with corrections"; the
correction is applied). The selection
below is the Foreman's recommendation. The owner may revise it.

**Selected policy: V-cover-detail.** For one form whose older
`no-non-qualified-loan-component` answer is current beside loan-link
detail, the form's class comes from its current answers, never from the
published standing reason. The result for each class:

- **Agrees:** supported.
- **Lacks detail, or a link that was withdrawn or denied:** supported. The
  person's older "yes" covers the matters the detail leaves open. Nothing
  current bears against it. Withdrawing a link is not withdrawing the older
  answer, so reading it that way would supersede a statement for an engine
  reason (K5, K9-after, L7–L10a, denied-loan-no).
- **Leaves a relationship unresolved:** not supported, and the unresolved
  answer is named. A later, specific "cannot tell" from the person is not
  outweighed by an earlier broad "yes" (U3, U4, U9b, U10b).
- **Contradicts:** not supported, and the contradicting answer is named.
- **An older "no":** not supported, with the "no" named and no cause assumed.

**Each existing state, as classified (P2a, after R3a and its confirmation).**
The form's class comes from its current answers. When the answers fall in
more than one class, a current contradicting answer decides the class.

| State on the form | Beside an older "yes" | Beside an older "no" |
| --- | --- | --- |
| Plain-case support (`none`) | agrees | unresolved: the "no" is contrary information that the detail does not explain |
| `loan-cost-no`, `enrollment-no` on a borrowing this form includes | contradicts | agrees in result, not necessarily in cause |
| `statement-loan-cannot-tell`, `inclusion-cannot-tell`, `financing-cannot-tell`, `loan-cost-cannot-tell`, `enrollment-cannot-tell` | unresolved | not supported |
| `inclusion-withdrawn`, `financing-withdrawn`, `no-loan-link` (silence, or an inclusion denial), `no-schooling-link`, `more-than-one-loan`, `more-than-one-schooling`, `loan-cost-answer-missing`, `enrollment-answer-missing` | lacks detail | not supported |
| A "no" on a borrowing whose inclusion on this form is cannot-tell or withdrawn | unsettled; blocked | not supported |

A "no" on a borrowing whose inclusion this form *denied* is outside this
form, because the person closed that pair.

Five states are blocked under every policy, with their own reason: the replay
marker, the financing denial, the unresolved-plus-lacks mix, and a contrary
answer on an open or withdrawn inclusion. Their
blocking is this slice's conservative treatment. It is not a claim that
blocking is the right long-term meaning, so they stay deferred design.

Not selected:

- **V-cover-both**, which lets an earlier broad answer bury the person's
  later uncertainty;
- **V-detail-governs**, which treats the newer method's needs as
  invalidating the older answer;
- **V-refuse**, the control.

**Still open for Track 0 closure, before production chartering:**

- **The contract shape.** A v13 inert path validates and fails closed, but
  declares a path that can never activate. A rule-artifact successor is
  honest, but costs a published schema, package admission, runner,
  projection and an ADR successor. To be settled on measured touchpoints, not
  preference.
- **The explanation.** The existing projection cannot yet show three things:
  an older "yes" credited on a supported form; a matter recorded but not
  used; and a denial distinct from silence (R3). Required behavior 6 needs
  all three. This is presentation scope for the implementation units.
- **The six Track 0 artifacts**, for the selected policy, recorded under
  "Track 0 adversarial closure" once their evidence exists.

### Implementation and closeout — charter only after readiness

Provisional units: (1) any necessary contract/content decision and the bounded
recording/evaluation change; (2) saved explanation and integrated compatibility
demonstration. After Track 0 (2026-10-08) these are **Track 1**, production
content and evaluation, then **Track 2**, the saved explanation. Split or combine on evidence; do not add a series of new tracks
to absorb a general assumption framework. Review a needed contract before code
depends on it. Independently review the first integrated production transition
and the final curated candidate. Ordinary in-scope repairs stay in their unit.

If a larger prerequisite is genuinely necessary, bring the owner the concrete
failure and choices before expanding. An explicit partial result is available,
but is not selected in advance and must not be presented as a working transition.
A partial close also says what happens to the both-present sentence that asks
the person to remove an answer. (Not a partial close: see "Outcome", Limits.)

## Track 0 adversarial closure

Working charters, probes and interim reviews (R0–R6, P0–P2b, T0, T0b) were
removed when the branch was curated. Their conclusions are recorded in this
plan, and their decisive cases are production tests.

For the selected policy, V-cover-detail. The evidence comes from two
evidence units, T0 and T0b. Both were run on a temporary copy through
`live_coordinate_run` with both runners, with the saved output reloaded from
disk. Their decisive cases are now production tests:
`tests/test_sli_track1_combined_standing.py`,
`tests/test_sli_track2_explanation.py` and
`tests/test_sli_track2_repair.py`.

- **Authority-lifecycle table: PASS.** T0 section 1 has one row per fact,
  rule publication and declaration. Section 3 executes it.
- **Empty/nonempty authority matrix: PASS.** T0 section 2:
  - empty: closure-backed 0;
  - unclosed: blocked with `SOURCE_SET_UNCLOSED`;
  - old-only, new-only and mixed: 2500;
  - one form ineligible: blocked with `DEPENDENCY_INVALID`.
  Line 26 and Form 1040 line 10 follow their own references; wages are
  unaffected. The paper trace for a closed-empty family with no closure
  fails if the default's `when` were `true`.
- **Late-member lifecycle: PASS.** T0 section 3 covers four changes:
  - a form added after a run, then reclosed;
  - a link withdrawn;
  - a shared borrowing's answer corrected;
  - the older answer corrected.
  Every publication whose inputs changed gets a new id, and the old id is
  gone. The older "yes" keeps its id when only a link is withdrawn.
- **Neighboring capability dependency diff: PASS.** T0 section 5. No
  neighbour gains a prerequisite. A return with no student-loan activity
  still publishes 0 through the closed-empty default.
- **Reused-claim semantic/lifecycle equivalence: PASS after T0b.** T0
  section 4 failed: a covered form's explanation reused the support rule's
  basis and the standing text. T0b section 4 passes with the patched
  explanation:
  - cover and older-method rows cite the combined rule's own basis and say
    what the older "yes" stands in for;
  - plain-case rows keep the support rule's basis;
  - an unused older "yes" is "recorded, not used";
  - a denial is shown as the person's answer, not as silence.
  The derived older-answer publication has its own id and a wider domain
  (`absent`, `unreadable`), and is never presented as the person's
  statement.
- **Integration surface: PASS after T0b.** T0 section 6 enumerates the
  bindings:
  - the line 21 field (exactly one section per return);
  - the package entrypoint (one publisher);
  - `line21Explanation` (one row per current form);
  - the projection's recomputation of selection (at most one active path).
  It also built a model for each disposition: published, closure-backed
  zero, computed zero, and blocked with `DEPENDENCY_INVALID`,
  `SLI_UNIVERSAL_COMPONENT_VIOLATION`, `SLI_MFS_INELIGIBLE` and
  `SOURCE_SET_UNCLOSED`. It also dumped the successor's pins. The
  presentation-model probe failed in T0 and passes in T0b: eleven cases, each
  saved presentation accepted by the patched validator. No published schema
  changes; `line21Explanation` is validated in code.
- **Known limitations affecting correctness: none.** Each limitation below
  fails closed, with its reason named; none publishes a favorable value it
  should not.
  - **The five deferred states block conservatively:**
    - the replay marker;
    - the financing denial;
    - the unresolved-plus-lacks mix;
    - a contrary answer on an open inclusion;
    - a contrary answer on a withdrawn inclusion.
  - **A "no" on a shared answer still blocks the whole return,** unchanged
    from v4. Whether that reach has tax authority remains P0 question 1, and
    this design leaves it as it is.
  - **The explanation's wording is provisional,** pending the owner's review.

R4 found the closure **settled with corrections**.
It confirmed all six artifacts and the selection's fidelity to the owner's
rules, and its reruns matched. Its two required corrections are recorded:

- the production explanation must not list the Form 1098-E's box 2 witness
  among what the person said;
- the v14 touchpoints include `authorization_closure.py`.

**Owner choice before production chartering: the contract shape.** T0
section 7 measures both options. The v13 inert path needs no new schema or
ADR, but declares a selectable path that nothing can activate. A
`rule-artifact.v14` with one live path is honest, but needs four things:

- a new published schema;
- admission in package validation, the runner, the live path, marshalling,
  the projection and the authorization boundary
  (`authorization_closure.py`, added by R4);
- a new ADR superseding ADR 0077's "at least two paths" sentence.

Neither changes an observable result. The Foreman recommended v14 for
contract clarity.

**Owner decision (2026-10-08): keep v13 with an inert path.** The successor
worksheet is a `rule-artifact.v13` rule. It has one live path and one inert
path, whose activity names a declared fact type that nothing writes. It
fails closed if that fact type ever becomes current. There is no new
published schema and no new ADR. The inert path's notes say plainly that it
never activates and why it exists. ADR 0077 gains an amendment line in its
existing pattern, recording that the successor worksheet replaces the
both-present refusal with per-form combination. Its decision text is not
edited. A rule-artifact successor remains available later.

## Outcome

**What changed, in plain terms.** A person can tell the application more
about one Form 1098-E without losing what they said about it or about
another form. When Cedar gains borrowing and schooling details, Cedar's
older eligibility answer is kept, not retired. Birch's older answer is left
alone. Line 21 no longer refuses the return because the two forms use
different kinds of input.

For each form, the application reads the person's current answers and puts
the form in one of these classes:

| The form's current answers | Line 21 for that form |
| --- | --- |
| The detail agrees with the older answer | Supported |
| The detail is missing or limited, or a link was withdrawn or denied | Supported; the older "yes" covers the matters the detail leaves open |
| The person cannot tell about a matter the older answer bears on | Not supported; that answer is named |
| A current answer contradicts the older answer, or the older answer is "no" | Not supported; the contrary answer is named, and no cause is assumed |

Each form's amount is counted once. The cap, the phase-out and the scope
limits apply once to the return's total, as before. A saved result shows,
for each form:

- what the person said;
- what the calculation used;
- what it assumed;
- what was recorded but not used.

The box 1 and box 2 witnesses on the form are not listed as things the
person said.

**Delivered.**

- Track 1 (`core-calculations` v42, `rule.sli-worksheet` v5): the per-form
  combined result and its helpers. 45 cases run through
  `live_coordinate_run` with both runners. Nine cases change from v41 and
  were shown blocked on v41. The compatibility cases are unchanged.
- Track 2: the saved explanation in `presentation_projection.py` and the
  citation-walk page.
- R5 found the integrated transition ready. It reran the cases on v42 and
  showed two deliberate regressions caught by the tests.
- Track 2 repair, after the owner's pre-curation review of the closed
  milestone:
  - **Denial wording.** It applied to every form with a denial. It now
    applies only to the borrowing whose inclusion was denied, decided from
    carried borrowing identity. The affirmed borrowing's missing detail is
    named as what the older "yes" covers.
  - **History.** A corrected borrowing answer dropped out of history while
    its inclusion stayed current. It now stays in history, noncurrent,
    through the form's current or historical links. An earlier saved run
    keeps its own account.
  - R6 reviewed the repair independently and found it ready. It reproduced
    both defects on the pre-repair explanation, and it tested three
    variations of its own. Mutations restoring each defect fail the tests.

**What is demonstrated, and how firmly.** These are two separate claims.

- **The calculation transition** (Track 1) is the milestone's demonstrated
  result. Its results were fixed by the reviewed probe, implemented in v42,
  rerun independently by R5, and left unchanged by the repair.
- **The explanation** (Track 2) needed two repairs after its first
  integrated review, both found by the owner's review rather than by R5. It
  now passes its own regression cases and R6's review. Its wording is still
  provisional, and no context-starved reader has assessed it. Treat it as a
  repaired, bounded explanation of the new result, not yet as evidence of
  lay legibility.

**Completion criteria.** Every item in the minimum set passes on the real
path:

- same-form older "yes" with detail (K1);
- same-form older "no" with detail (K2, blocked, with the "no" named);
- Birch unchanged (K1, K3);
- the cap and phase-out (K7: 2500 and 1668);
- one withdrawal (K9-after: 2500, older "yes" still current).

Old-only and new-only compatibility and once-only aggregation hold.

**Limits.**

- The explanation's wording is provisional and has not had the owner's
  review. On old-only rows, a shared "assumed" sentence still says the
  older "yes" "stands in for" link matters; the row's own sentence says it
  is the method. No context-starved reader assessment was run.
- Five states block conservatively, each with its reason named, as deferred
  design:
  - the replay marker;
  - a financing denial;
  - an unresolved-plus-lacks mix;
  - a contrary answer on an open inclusion;
  - a contrary answer on a withdrawn inclusion.
- A "no" on one of the four shared answers still blocks the whole return,
  as in v4. Whether tax authority supports that reach is open (P0
  question 1).
- The v13 inert path's own refusal token has no sentence a person would
  see. It can fire only if the unwritten fact type became current.
- The both-present sentence in `sli-worksheet-inputs.bundle.json` remains.
  v42 never emits it; it still describes saved v41 results (R5, F1).

**Phase assessment (recommendation, not a decision).** The phase's exit
goals are met in bounded form:

- one production transition preserves the person's account while changing
  its use, without disturbing an unrelated form;
- its tests distinguish added detail, correction, adverse information and
  unresolved information;
- a saved explanation separates said, used and assumed.

The short model above is the phase's model of that transition. The
calculation side is firmly demonstrated. The explanation side is repaired
but unassessed by a fresh reader. Whether that is enough to conclude the
phase is the owner's decision. This milestone does not propose another
milestone to extend the phase.

## Questions that remain open

| Question | Why it matters | Evidence and decision point |
| --- | --- | --- |
| What overlaps between the old assertion and the new detail? | Determines whether either can replace or corroborate the other | P0 proposition map; reviewed before selecting a mechanism |
| Which current assertions matter when the calculation uses the new method? | Prevents preserved information from being silently ignored | Same-statement yes/no/incomplete cases in P1/P2; settle before build |
| Can statements use different methods with existing declared composition? | Determines the actual contract and implementation cost | Trace and live comparison in P1/P2; settle at Track 0 |
| Which assumptions need different treatment in this bounded transition? | A numerical pass can conceal a changed or unsupported basis | Before/after basis comparison; implement only what the selected slice needs |
| What does withdrawal or correction mean for the selected method? | Prevents stale revival or unrelated displacement | Lifecycle cases before production readiness |
| Should a "no" on one statement (the older answer or a shared answer) still block another statement's deduction? | Today it blocks the whole return; leaving Birch alone may or may not be what the tax rule supports | P0 checks the tax basis against primary authority; whether this milestone changes the effect is settled at Track 0, and may honestly remain unchanged |

General assumption management remains deferred. Investigate only enough of it
to avoid an unsound transition here; if that is not separable, report the
dependency rather than inventing local exceptions.

## Cases and evidence

Use synthetic `demo.*` identities and ordinary public recording APIs. Expected
tax outcomes below are properties to establish against adopted rules, not
executed evidence. Mechanism-dependent outcomes remain open until P0–P2.

| Case | What the case must discriminate |
| --- | --- |
| Cedar and Birch both older-only; both newer-only (still with their four shared answers each) | Baselines and unchanged supported routes |
| Cedar gains details; Birch stays older-only | Mixed methods alone must not be treated as a contradiction or require deleting Birch's answer |
| Cedar keeps its older "yes" alongside complete new detail | Same subject is not double-counted; preservation is distinguished from reliance |
| Cedar's older answer is "no" beside complete favorable detail | No favorable fallback hides it; its cause is not assumed; Birch's expected property is stated |
| Cedar's older "yes" beside adverse or denied detail | Adverse detail is not overridden by the older answer; Birch's expected property is stated |
| A shared answer on Cedar is "no" after the transition | The current whole-return effect, or a justified change to it, is explicit for Birch |
| Cedar on loan links without its four shared answers | Mirror of behavior 1: the new method does not silently drop answers it still needs |
| New detail is incomplete, withdrawn or later corrected | Do not drop it from consideration or switch method merely for convenience |
| Replay applicability marker on Cedar beside Birch's older answers | A system marker is not treated as something the person said |
| Two subjects share labels; one subject is reached through two records | Attribution and deduplication use subject identity, not labels or raw record count |
| Two statements share a borrowing | Real shared dependencies change together; unrelated ones do not; allocation remains unselected |
| Two individually supported amounts cross the existing cap together, and the income phase-out, married-filing-separately and out-of-scope blocks | Aggregate and apply existing return-level arithmetic once, with truthful pins |
| Same saved result reopened after a later change | Historical answers and calculation basis stay those of that run |

Refine into small positive, negative and compatibility fixtures before each
build. Trace current-state behavior after correction/retraction and replay,
not only a manually constructed evaluator environment. Validate the adopted
package, enter through `live_coordinate_run`, compare both runners and inspect
saved output after discarding in-memory results. Show that each decisive
regression fails for the intended reason on the base when practical.

Use the repository's test lanes and schema/data-safety checks. The builder
performs applicable typing and substrate verification; final CI binds the
curated candidate. Do not repeat deterministic suites just to confirm them.
Browser-tool failures do not authorize repeated troubleshooting: report the
unverified visual check and let the owner inspect the saved synthetic page.
No personal workspace or private output is needed for this milestone.

## Completion and handoff

A completed implementation demonstrates the bounded transition through the
real recording and calculation path and preserves unrelated accounts and the
person's answers. At minimum it passes: same-statement older "yes" with new
detail; same-statement older "no" with new detail, without favorable
substitution; Birch unchanged; aggregation with the cap and phase-out; and one
withdrawal. Track 0 may add to that set, not shrink it. Its saved explanation
distinguishes what was recorded, what the calculation used and what it
assumed. Old-only and new-only compatibility and once-only aggregation hold.

Publish the executable behavior, necessary contracts, and a short plain-language
model of what changed and why. Carry general assumption management and other
unresolved design forward explicitly. A partial close instead names the exact
unmet condition, evidence and prerequisite; it does not turn an implementation
limit into intended behavior. Final review and CI remain required for publication.

## Not selected

Automatic retirement of an older "yes" on the first affirmed inclusion;
return-wide removal of older answers; newer-information-wins precedence;
an older "no" being treated as proof of an additional borrowing; general
assumption truth maintenance; mixed-period or allocation treatment; new tax
coverage; free-text interpretation; institutional checks; broad intake or reader
navigation work. No PR push or creation is part of this planning handoff.
