<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "student-loan-deduction-completion",
  "status": "Closed. In one plain, fully supported case, recorded loan and statement links and two ordinary answers decide whether reported student-loan interest counts, through package core-calculations v41; correcting a link changes the deduction and restoring it returns it, and a blocked line 21 names the statement and a reason the person can act on.",
  "scope": [
    "one plain supported student-loan case whose relationships decide a rule-owned qualification conclusion",
    "the existing worksheet consumes that conclusion without changing its arithmetic",
    "explicit refusal for partial or unresolved cases",
    "production statement-correction and multi-record save safety on the path this result depends on"
  ],
  "non_goals": [
    "no mixed-period treatment or ADR 0076 Part 3 selection",
    "no person-supplied scoped values, institutional catalog or general explanation reader",
    "no change to the worksheet's phase-out or limit arithmetic"
  ],
  "deep_reads": {
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-03-student-loan-deduction-completion.md",
      "docs/phases/tax-concept-derivation/milestones/student-loan-deduction-completion.md",
      "docs/adr/0077-shared-key-count-basis-same-run-read-and-presence-selection.md"
    ],
    "implementation": [
      "docs/phases/tax-concept-derivation/milestones/student-loan-deduction-completion.md",
      "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/relationship-capability-handoff.md",
      "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/track18-relationship-correction-report.md",
      "AGENTS.md#Data Safety Rules",
      "AGENTS.md#Schema Publication Protocol"
    ],
    "review": [
      "docs/roles/qualitative-review.md",
      "docs/phases/tax-concept-derivation/milestones/student-loan-deduction-completion.md",
      "AGENTS.md#Data Safety Rules"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-10-03-student-loan-deduction-completion.md"
}
-->

# Student Loan Deduction Completion

Milestone key: `student-loan-deduction-completion`.
Result: **closed** 2026-10-03. Retrospective: [2026-10-03](../../../milestone-retrospectives/2026-10-03-student-loan-deduction-completion.md).
Primary branch: `milestone/student-loan-deduction-completion-bounded-route`.

## Objective

A person who paid interest on a student loan says ordinary things: this loan
paid for this schooling, and this interest statement covers this loan. In one
plain, fully supported case, those statements, not a yes/no answer to a tax
question, decide whether the reported interest counts. The result flows
through the existing deduction worksheet to Schedule 1. If the person corrects
an answer, the deduction changes, and the reason can be traced.

Three earlier milestones built the pieces: the method, the relationship
records, and their correction. None of them changed the deduction. This
milestone is done when one does.

## How this plan is written

The plan starts as eight plain sentences describing what we will do. Each
sentence gets more detail as work makes it concrete. Detail that depends on
investigation not yet done is left open and named as open. Each track's
findings may revise later sentences. Such revisions are expected and are made
in this file as separate planning commits.

## Current state

- The 2025 package (`package.core-calculations.v38`) computes the Student Loan
  Interest Deduction from Form 1098-E box 1 through a worksheet to Schedule 1
  and AGI. Its eligibility inputs are five tax-labelled yes/no facts on the
  Form 1098-E bundle. One example is "no non-qualified loan component." A
  person answering them supplies the tax conclusion.
- The previous milestone records two ordinary relationships with their own
  evidence and standing. The first says a loan financed a schooling
  circumstance. The second says a statement includes interest on that loan.
  Both can be corrected, withdrawn or left uncertain. A neutral consumer reads
  them from saved state through both runners. The
  [capability handoff](student-loan-circumstance-association-evidence/relationship-capability-handoff.md)
  sets what a consumer may rely on.
- ADR 0075 (`link_coverage`) and ADR 0076 Parts 1–2 (per-subject dispatch with
  declared relationships) are accepted. ADR 0076 Part 3 is open: it would decide
  what several statuses for one loan do to its interest.
- Two save-path gaps are known. A direct statement write bypasses the reviewed
  correction scope and can leave an old inclusion usable. Multi-record saves
  fail closed when interrupted but are not atomic.

## The plan

### 1. Pick one plain case and name what falls outside it

One loan, used only for qualifying schooling, during periods that count, with
one statement that covers only that loan. We fully support that case and
refuse everything else by name.

*Settled by Track 0a and the owner:* the links replace only the
non-qualified-loan fact, together with two new ordinary answers: the loan paid
only for school costs, and the student was enrolled at least half-time in a
degree or certificate program. The refused cases are listed in the
[route map](student-loan-deduction-completion-evidence/track0a-route-map.md),
section 4.

### 2. A rule turns the person's links into the tax conclusion

An adopted rule reads the current relationship records and the two ordinary
answers and derives, per statement, `plain-case-supported` or `not-supported`.
The person never states a tax conclusion. The result does not claim the loan
is a qualified education loan: per
[Track 0e](student-loan-deduction-completion-evidence/track0e-conclusion-basis.md),
it rests on what the person said and two derived counts, together with five
favorable assumptions and four conditions left as the person's
responsibility. Its provenance shows all four groups. Pins carry what was said
and derived; the rule declares the assumptions and responsibilities, since no
finding carries them.

*Settled by Tracks 0a and 0c:* the subject is the box 1 statement and the
result is a per-statement category, published for every statement. Counting a
statement's schooling links needs a new shared-key count operator with its own
ADR; existing operators either fail validation or join on one shared name.

### 3. The worksheet uses that conclusion instead of the tax-labelled answer

The worksheet's existing arithmetic stays as it is. Only the source of the
replaced eligibility fact changes. Workspaces that still use the old yes/no
answers either keep working or are refused with a stated reason. They never
silently get a different result.

*Settled by the owner:* exclusive regimes; both present blocks the return.

The regime discriminator is the replaced
`no-non-qualified-loan-component` answer, not the other four answers. Those
four remain per-statement requirements on either path. The worksheet must
check their coverage and values even when the relationship-derived support
is favorable. A selection prototype that leaves all five answers out of its
new-path fixture demonstrates the engine mechanism, not this product boundary.

### 4. Partial and unresolved cases are refused, never zeroed

When a statement covers interest from loans outside the plain case, or a link
is uncertain or withdrawn, the deduction is blocked with a reason the person
could act on. A missing answer is never treated as "no."

### 5. Statement corrections use the scope-checked path

The real save path for correcting a statement enforces what the correction
affects, so a direct write can no longer leave an old inclusion in use.

*Result:* a reviewed correction's scope evidence authorizes exactly one box 1
finding: the successor of the finding the review saw, at the reviewed amount,
with that correction's identity (Tracks 6 and 1a-3). `ActLog.append` refuses
every other new box 1 finding while a current link names the statement, and
every production `ActLog` carries that check (Track 1e). Histories written
before the check replay with the unestablished link omitted and a system
marker on its statement, which makes that statement `not-supported` (Track 1e,
ADR 0077 Part 5).

The coordinator computes applicability from the same saved history used for
the run. The state-only `live_run` entrypoint cannot do that check and refuses
a state containing a current statement inclusion; it does not accept a
caller-supplied substitute. The lower-level marshaller requires the history's
applicability reading when current inclusions exist.

### 6. Multi-record saves survive interruption

Saves that write several records either recover or continue after an
interruption, or are refused cleanly. A test interrupts at each step.

*Result:* every multi-record relationship save is one atomic batch, checked
before anything is written, so an interrupted or refused save leaves the log
as it was (Track 7).

Changing a borrowing's set of schooling links ends its existing enrollment
answer in the same save. The question was about that schooling. This also
applies when an answer preceded the first schooling link. An unchanged set
keeps the answer; statement-inclusion changes leave it alone. Restoring a
schooling link requires a fresh enrollment answer, not reuse of the ended one.

### 7. Every test runs the real path from saved data

Each consequential case starts from a saved log, reloads it fresh, resolves
the real package, and runs both runners. No hand-built run context. The last
milestone's defects all hid between the steps that unit tests skipped.

### 8. Done when a corrected answer changes the deduction

A synthetic person's Schedule 1 student-loan deduction appears for the plain
case. It disappears or blocks when they correct or withdraw a link, and
returns when they restore it. Each result can be traced to the answers and the
rule that produced it.

## Scope

Sentences 1–8 above, for tax year 2025, on synthetic data.

## Non-goals

- Mixed-period treatment, interest allocation across loans, or an ADR 0076
  Part 3 decision.
- Person-supplied scoped values where automation stops. This is a likely next
  milestone, not this one.
- Changes to the worksheet's limit, phase-out or MAGI arithmetic.
- An institutional catalog, a general explanation reader, or a user interface.
- Favorable eligibility beyond the plain case.

## Contracts

Expected, subject to Track 0:

- Adopted rules producing a per-statement `plain-case-supported` or
  `not-supported` result with a reason (the original wording here said
  "qualified-loan conclusion"; Track 0e retired that name).
- A new `package.core-calculations` version that includes it. Existing
  package, release and schema bytes stay unchanged. Any schema change follows
  `AGENTS.md`, "Schema Publication Protocol," and the schema-intent ledger.
- The production correction entry point from sentence 5.
- An ADR only if Track 0 or Track 1 fixes a contract that later content will be
  written against.

## Fixtures

Synthetic `demo-*` workspaces: the plain case; a statement that also covers an
outside loan; uncertain, withdrawn and restored links; an old yes/no
workspace; both old and new inputs present; and a second, unaffected
statement.

## Verification

Focused tests per track, then the full suite, because the work touches
`packages/derivation/` and live paths. CI `verify` is the gate of record.

## Data safety

All fixtures are synthetic. No personal documents, values or paths enter the
repository. `envelope_scan` runs at review.

## Exit criteria

- Sentence 8 is demonstrated through saved recovery and both runners.
- Every refused case in Track 0's list has a test showing the refusal and its
  reason.
- Old-input workspaces behave as the coexistence policy says.
- Sentences 5 and 6 are enforced on the deduction path.
- A curated PR passes independent final review and CI.

## Tracks

Tracks after Track 0 are provisional. Track 0's report may split, merge or
reorder them.

| Track | Purpose | Sentences |
| --- | --- | --- |
| 0a | Route map. **Done:** [report](student-loan-deduction-completion-evidence/track0a-route-map.md) | 1, 2, 3 (decisions) |
| 0c | Link count options and probe. **Done:** [recommends a new shared-key count operator](student-loan-deduction-completion-evidence/track0c-link-count.md), needing `rule-artifact.v13`, `artifact-package.v35` and a new ADR | 2, 4 |
| 0b | Adversarial-closure artifacts. **Done:** [evidence](student-loan-deduction-completion-evidence/track0b-closure-evidence.md); three rows FAIL | 1–4 |
| 0d | Closure repair plus owner-directed mixed scope. **Done:** [evidence](student-loan-deduction-completion-evidence/track0d-closure-repair.md) | 1–4 |
| 0e | Basis of the favorable conclusion and route map update. **Done:** [basis](student-loan-deduction-completion-evidence/track0e-conclusion-basis.md); result renamed `plain-case-supported` | 1, 2 |
| 0f | Mechanism rows. **Done:** [evidence](student-loan-deduction-completion-evidence/track0f-mechanism-rows.md); two rows closed, integration surface needs three engine capabilities | 1–4 |
| 1a | ADR draft for the engine capabilities. **Accepted** 2026-10-02: [ADR 0077](../../../adr/0077-shared-key-count-basis-same-run-read-and-presence-selection.md) Parts 1–5, with the condition that every production `ActLog` carries the Part 5 declaration | 2, 4 |
| 1a-2 | ADR 0077 Part 5: refuse an unscoped statement rewrite at admission while a link depends on it. **Done:** drafted, including the retract-then-reassert repair; accepted with ADR 0077 | 5 |
| 1a-3 | **Done:** correction evidence bound to the one correction it reviewed, implemented in the recorder and read-side check ([report](student-loan-deduction-completion-evidence/track1a3-correction-binding.md)) | 5 |
| 1a-4 | **Done:** one worksheet declaration composing Parts 3 and 4 ran correctly for old-only, new-only, both, closed-empty and neither ([report](student-loan-deduction-completion-evidence/track1a4-worksheet-composition.md)) | 3, 4 |
| 1a-5 | **Done:** three tests that encoded the old gap fixed; Part 5's new-write step separated from replay; Parts 3–4 applied with derived-pin and presence repairs ([report](student-loan-deduction-completion-evidence/track1a5-adr-integration.md)) | 3–5 |
| 1a-6 | **Done:** an inclusion omitted on replay becomes a system applicability marker on its statement; any marker makes that statement `not-supported`; kept distinct from the person's "cannot tell" ([report](student-loan-deduction-completion-evidence/track1a6-omitted-inclusion-support.md)) | 5 |
| 1b | **Done:** four schema versions (`rule-artifact.v13`, `artifact-package.v35`, `derived-finding.v3`, `derivation-record.v10`); shared-key count; declared basis | 2, 4 |
| 1c | **Done:** ADR 0077 Parts 3 and 4 runtime (merged with planned 1d); the Track 1a-4 worksheet's five cases pass through the real path on both runners | 3, 4, 7 |
| 1e | **Done:** ADR 0077 Part 5 — the `ActLog.append` new-write step and production-registry condition; replay omission with the applicability marker on the production run path (`live_coordinate_run`) | 5 |
| 2 | Merged into Track 5: presence selection needs two paths and per-statement reads live on a selection path, so the old-path coverage fix ships with the worksheet integration | 4 |
| 3 | **Done:** relationship bundle v2 with the two ordinary questions, financing and inclusion unresolved/denied/withdrawn facts, a statement-level scope-unresolved fact, and the declared applicability marker; the recorder writes them | 1, 4 |
| 4 | **Done:** per-statement support chain with reasons, adopted in package `core-calculations` v39; every v38 result unchanged; nominee cross-checks and entrypoint-pin checks now run for v39 / `artifact-package.v35` | 2, 4 |
| 5 | **Done:** worksheet v4 adopted in package `core-calculations` v41; only the replaced answer selects the old path and the four retained answers are required per statement on both paths; coverage on both paths (the old-path fail-open fix); line 21 names the blocking statement and its reason. A corrected link changes the deduction and restoring it returns it (plan sentence 8, through `live_coordinate_run`) | 3, 4, 8 |
| 6 | Scope-checked statement correction entry path. Read-side tie and correction binding implemented; write-side refusal and replay completed by Track 1e | 5 |
| 7 | **Done:** every multi-record relationship save is one atomic batch (`ActLog.append_batch`), checked before writing; an interrupted save recovers to the state before it, never more favorable. The readiness check found three interrupted states that had published a more favorable line 21. Bundle v2 is adopted on a person's first new answer ([report](student-loan-deduction-completion-evidence/track7-interruption-safety.md)) | 6 |
| 8 | **Done:** end-to-end demonstration through `live_coordinate_run` and the rendered page; carried cleanups; closeout and retrospective. Publication curation and the independent final review follow on owner request | 7, 8 |

Independent review stages: the final curated candidate. Track 0's choice of
replaced fact and coexistence policy gets owner review before Track 1 starts,
because it changes what a person is asked.

## Track 0a results and pending owner decisions

The [route map](student-loan-deduction-completion-evidence/track0a-route-map.md)
answered sentences 1–3 and found three things the plan did not anticipate:

- **The recorded links do not establish a qualified loan by themselves.** They
  say a loan paid for a schooling and a statement covers that loan. They say
  nothing about eligible-student status, qualifying expenses, or use only for
  school. The replaced fact is `no-non-qualified-loan-component` alone; the
  other four stay as asked.
- **An engine gap.** No current operator can count, from a statement, how many
  schooling links its loan has. Without that count a loan tied to two schooling
  periods would pass. Every option below needs it.
- **A shipped fail-open defect.** The worksheet's check of the five yes/no facts
  tests only the rows that exist. With two statements, one statement's `yes`
  lets another statement with no answer through. Confirmed by reading the
  operator; not yet run live.

Owner decisions, 2026-10-01 (all four recommendations approved):

1. **Two ordinary questions replace the tax question.** For the plain case the
   person is asked whether the loan paid only for school costs, and whether
   the student was enrolled at least half-time in a degree or certificate
   program during that schooling. The rule, not the person, draws the
   qualified-loan conclusion from those answers and the two links. The other
   four yes/no facts stay as asked.
2. **Old and new inputs are exclusive.** A return with the old
   `no-non-qualified-loan-component` answer on any statement and any loan link
   on any statement is blocked with a stated reason, even if they agree.
   Old-only returns keep today's results.
3. **The plain case deducts the whole box 1 amount.** No question hunts for a
   loan the person never mentioned. A second recorded loan on the statement
   still blocks.
4. **The fail-open defect is fixed on the old path.** Every box 1 statement
   must carry its own answer for each of the five facts. A statement without
   one blocks the deduction.

## Final publication review charter

Audience: Reviewer.

An author-independent Reviewer inspects the exact curated range
`origin/main..HEAD` after closeout. Review the complete diff and each durable
commit against this plan, ADR 0077 Parts 1–5 and its acceptance condition,
ADR 0075 and ADR 0076 Parts 1–2, and `docs/roles/qualitative-review.md`.

Trace one person's answers through recording, correction, withdrawal, saved
recovery, replay, the support chain, the worksheet and line 21 presentation.
Check that `plain-case-supported` claims no more than its declared basis; that
only the replaced answer selects the old path and the four retained answers
cannot be bypassed; that a missing answer never reads as "no"; that an
unscoped statement rewrite is refused at the write and safely replayed; that
an interrupted save never recovers to a more favorable result; and that
workspaces with no relationship claims are unchanged.

Verify additive published-schema versions and manifest entries, package,
registry and release checksums, removal of working records, reference
integrity, the closed phase state and data safety. Report falsifiable findings
and the exact reviewed commit. Do not edit or expand the candidate. CI is a
separate publication gate.

## Track 0 adversarial closure

Foreman judgment, 2026-10-01, from Tracks
[0b](student-loan-deduction-completion-evidence/track0b-closure-evidence.md),
[0d](student-loan-deduction-completion-evidence/track0d-closure-repair.md),
[0e](student-loan-deduction-completion-evidence/track0e-conclusion-basis.md) and
[0f](student-loan-deduction-completion-evidence/track0f-mechanism-rows.md).
The two repairs the owner directed before closure, the conclusion's basis and
mixed supported and unresolved scope, are complete. **Settled by owner disposition (path A).**

- Authority-lifecycle table: PASS — basis classified (0e); stale schooling or
  statement blocks the chain through required containment joins and the
  worksheet refuses rather than deducting (0f item 1).
- Empty/nonempty authority matrix: PASS — closed-empty still 0; mixed scope has
  deliberate, distinct consequences after fresh recovery (0d evidence 6–8); the
  worksheet refuses unless every current statement has a supporting result,
  including a statement whose chain blocked and published nothing, on both
  paths (0f item 2, `SLI_STATEMENT_COVERAGE`).
- Late-member lifecycle: PASS — unchanged from 0b.
- Neighboring capability dependency diff: PASS — unchanged from 0b.
- Reused-claim semantic/lifecycle equivalence: PASS — `plain-case-supported`
  claims only its stated basis (0e).
- Integration surface: **FAIL** — the chain produces the favorable row and the
  worksheet reaches 2500, 1334 and 1000 through the real presentation consumer,
  but three engine capabilities are missing, each with an executed failing
  case:
  1. *Same-run reading.* A return-level rule cannot read per-statement results
     in the same run. Declaring the dependency blocks it; omitting it makes
     the forward and reference runners disagree (a defect in the current
     engine). 0f item 2 ran the coverage check only with the results supplied
     as the worksheet run's sources.
  2. *Presence selection.* The `exclusive_presence` / `refuse` selection is
     bound at runtime only for the Form 1040 line 2b rule
     (`packages/derivation/runner.py`); a validated worksheet clone blocks every
     case `v9-declarative-binding-unauthorized` (0f item 3).
  3. *Person-visible reason.* Coverage, both-present and missing-answer
     refusals all display the same generic line 21 sentence.
- Known limitations affecting correctness: none beyond the integration-surface
  row. Its three items are fully specified engine requirements, not open
  design questions.

**Owner disposition, 2026-10-02: path A.** The integration-surface row's three
items are accepted as implementation scope, not open design. Track 0 is
settled on that basis. Track 1 delivers them with the shared-key count and the
declared basis, under one ADR the owner accepts before engine code changes. The
line 21 person-visible reasons move into worksheet integration.

Settled design inputs for the build, from this closure work:

- Chain: inclusion-level support (shared-key financing count, loan-cost and
  enrollment answers by containment, scope marks) feeds statement-level
  `plain-case-supported` via `link_count` and ADR 0075 `link_coverage`.
- Enrollment is keyed by borrowing; the question wording is unchanged. A
  second loan for the same schooling needs its own answer and blocks until
  given. Foreman decision; schooling keying would need a further operator.
- Recorder obligations (Track 3): current facts for financing cannot-tell,
  production inclusion cannot-tell, explicit no on either link, and
  withdrawn-without-successor. A missing scope fact means `complete` only for
  genuine absence.
- Both-present refusal: `DEPENDENCY_INVALID` with a named missing token, as
  line 2b; the person-facing reason on line 21 is a build obligation.
- New-path presence counts the affirmed inclusion and the statement-keyed
  unresolved, denied and withdrawn inclusion facts Track 3 adds, and an
  inclusion omitted on replay (ADR 0077 Parts 4 and 5).
- A missing answer publishes `not-supported` with a reason that says it is
  missing, never that the person said no.
- An inclusion whose applicability the system cannot establish carries its
  own person-visible reason on line 21 ("the statement this link was
  confirmed against changed or was removed; confirm the link again"),
  distinct from the person's "cannot tell". It covers both an unreviewed
  rewrite and a withdrawn statement.
- Worksheet v4 checks unresolved applicability markers directly through a
  declared per-marker blocked result before arithmetic. This check remains
  effective when the statement itself is no longer current and another
  supported statement remains. Counting only current statements, as v40 did,
  misses that case. Package v41 adopts the repair; v40 remains unchanged.
- The end-to-end demonstration (Track 8) runs through `live_coordinate_run`,
  the path that applies the replay omission.
- Carried engine defect (not on this deduction's path): an optional default on
  a symbol a per-subject rule also publishes makes the reference runner skip
  that rule, so the runners disagree. Track 4 avoided it; record it for a
  separate fix.
- A workspace that never adopted relationship bundle v2 cannot record the two
  answers; adopt v2 when a person first answers (Track 7), and word the line
  21 reason plainly until then (Track 5).
- Carried validation gap (pre-existing): packages on `artifact-package.v32`–`v34`
  skip the exact entrypoint-pin check. Enabling it could reject already
  published packages; decide separately.
- Carried kernel defect (pre-existing, affects every workspace):
  `ActLog.append` writes onto a torn last line and corrupts the log; decide
  separately whether to refuse the write or set the torn line aside.
- Carried limits from Track 7: a v1-era history holding a no, cannot-tell or
  withdrawal is refused rather than upgraded; the batch assumes one writer per
  workspace; a crash can leave an `acts.jsonl.pending` file until the next
  save.
