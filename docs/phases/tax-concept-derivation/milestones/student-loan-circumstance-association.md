<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "student-loan-circumstance-association",
  "status": "PLANNED. Replace the prior experiment's stipulated statement-to-loan-and-period relationship with a bounded recorded ordinary-fact path and a tested consumer. Start with an independently reviewed product and evidence outline before settling the representation or chartering implementation.",
  "scope": [
    "record and recover ordinary schooling circumstances and their explicit connection to identified student-loan interest",
    "preserve document evidence, source-independent subjects, attribution, and relationship lifecycle",
    "exercise the recorded relationship through a bounded consumer of the prior adverse-direction experiment",
    "prepare a concrete handoff for later worksheet integration"
  ],
  "non_goals": [
    "no complete student-loan eligibility or production deduction integration in this milestone",
    "no institutional catalog or blanket favorable default policy",
    "no general Evaluation Context selected by assumption",
    "no deep conversational UI, cross-year basis work, or broad tax coverage"
  ],
  "deep_reads": {
    "planning": [
      "OWNER_MODEL.md#The Product Model",
      "OWNER_MODEL.md#The Domain Model Model",
      "docs/phases/tax-concept-derivation/tax-concept-derivation-overview.md",
      "docs/milestone-retrospectives/2026-09-15-student-loan-interest-bounded-method-transfer.md",
      "docs/phases/tax-concept-derivation/milestones/student-loan-interest-bounded-method-transfer-evidence/track-0-adversarial-closure.md#5.5 Deferral ledger",
      "docs/phases/tax-concept-derivation/milestones/student-loan-interest-deduction-translation-evidence/p3-partial-design.md#2c. A statement-scoped association that earns its scope — discharged"
    ],
    "implementation": [
      "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association.md",
      "docs/adr/0067-canonical-acquisition-field-ref-access.md",
      "docs/adr/0073-assertion-standing-and-retraction-lifecycle.md",
      "AGENTS.md#Data Safety Rules",
      "PROJECT_PLANNING.md#Payload Instantiation Gate"
    ],
    "review": [
      "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association.md",
      "docs/roles/qualitative-review.md",
      "AGENTS.md#Data Safety Rules"
    ]
  }
}
-->

# Student Loan Circumstance Association

Milestone key: `student-loan-circumstance-association`.
Primary branch: `milestone/student-loan-circumstance-association`.
Primary worktree: `engine-worktree-1`.
State: planned; no implementation or contract selected. Opened 2026-09-18.

## Product purpose

A lender reports interest. A person describes their schooling. The application
needs to know which borrowing and education period that account concerns before
it can apply the circumstance to any reported interest.

The previous experiment supplied that relationship itself. This milestone builds
a bounded way to obtain and retain it from ordinary information, so the next
calculation need not be handed a prearranged connection. The user supplies facts
about their circumstances, not a conclusion about deductibility.

The stakes are concrete: attaching a true circumstance to the wrong interest
can produce a wrong result even when every individual value and rule is correct.
A matching name, equal amount, or convenient statement identifier must not
silently stand for the relationship we need.

## Starting evidence and what remains open

The preceding milestone closed with a validated adverse-direction method and
production deferred. Its disposable candidate uses real engine machinery but
stipulates the student/statement/loan/period relationships. Its
[deferral ledger](student-loan-interest-bounded-method-transfer-evidence/track-0-adversarial-closure.md#55-deferral-ledger)
separates relationship representation (E1), favorable-route premises (E2),
multi-statement handling (E3), worksheet integration (E4), and broader invalidation.

The earlier [P3 association proposal](student-loan-interest-deduction-translation-evidence/p3-partial-design.md#2c-a-statement-scoped-association-that-earns-its-scope--discharged)
is a paper candidate, not an adopted shape or implemented producer. Its
single-loan/single-period restriction must be examined as a product choice,
not inherited as though it were the definition of a student loan.

Useful committed starting artifacts:
- `packages/content/tax/2025/f1098e.bundle.json`: existing report identity and values.
- `packages/tax/nominee_allocation_recording.py` and
  `nominee_allocation_recovery.py`: ordinary evidence, recording, and recovery precedent.
- `packages/tax/obligation_acquisition_mapping.py` and
  `identity_association.py`: source-independent circumstance and association precedent.
- `tests/test_sli_bounded_method_transfer_p1.py`: the prior disposable consumer,
  including amount dependence, adverse support, and lifecycle tests.
- ADR-0067, ADR-0068, and ADR-0073: consult the exact decisions where relied upon.

These are routes to inspect, not proof that their mechanisms transfer unchanged.
The initial outline must identify the actual fields, identity and currency
behavior, and consumers on which the chosen route depends.

## Intended result and build boundary

Deliver an adopted, bounded recording and recovery path for ordinary schooling
circumstances and the relationship needed to apply them to identified reported
interest. Use a source-independent account of the borrowing and education period;
a document's identity is not automatically the identity of either.

The initial design must make explicit:
- what the person actually says and what they can reasonably know;
- what evidence records that answer and what canonical proposition it supports;
- how the report, borrowing, person, and period are distinguished;
- whether the relationship covers the whole reported amount or a stated portion;
- what remains unknown when the person cannot establish the connection.

Start with the filer as student and a bounded single-loan/single-period case,
but test its boundary against multiple statements, loans, and periods before
adopting it. A narrow implementation is acceptable when its limits are detectable
and it leaves the surrounding model intelligible. Do not ask users to certify
a simple composition merely because it fits the engine.

A loan entity, a relationship fact, and the scope of an asserted relationship
are design questions to settle against the actual consumer. Do not relabel a
statement as a loan; equally, do not invent a comprehensive loan-account system
without a use for it. No final schema or association mechanism is selected here.

The production recording/recovery path must feed a bounded executable consumer
that exercises the already-tested adverse translation. Candidate tax artifacts
may remain disposable for this connection test; use the newly recorded and
recovered relationship, not an injected replacement. Say exactly which part is
adopted production capability and which part is experimental.

This does not integrate the full deduction worksheet, grant favorable eligibility,
or change the existing worksheet's treatment of unlinked statements. Return
integration is a subsequent milestone. Existing production behavior remains
unchanged until explicitly selected and reviewed.

## Initial planning and early review

Begin with a short outline: the ordinary interaction, the proposition it would
record, the downstream decision it supports, and how the relationship could be
wrong despite individually correct inputs. State what would make a design
unacceptable before choosing it.

Have an independent reviewer examine that outline and its load-bearing source
claims before elaborating the full design. Develop the uncertain sections with
small concrete payloads and traced consumers; review a material change where it
affects another section. Do not write a large, apparently settled specification
and defer all challenge until Track 0.

Make these choices visible:
1. What evidence can support the relationship without asking the user for a
   tax conclusion or knowledge they are unlikely to possess?
2. Does the consumer need a separately identified borrowing now, and what
   correspondence can actually be asserted or checked?
3. How does correction of a report or period affect continued applicability?
   Identity continuity alone does not settle whether the asserted composition
   remains supported.
4. What happens when several records refer to one borrowing, or one record
   includes several borrowings? Which distinctions must be represented now?
5. What is the smallest consumer that can reveal a wrong or stale association?

The owner has expressed an intention to permit reasonable application reliance
on evidence under a standing user authorization. That is product context, not
an adopted rule granting a specific favorable finding in this milestone.
Do not turn this build into an institutional-verification project or an effort
to settle every default. If a concrete reliance choice changes what the producer
would assert, bring that choice to the owner in ordinary language.

## Cases to carry through design and execution

Use synthetic identities and evidence, with source values left intact.

- An identified report, one borrowing, one period, and an ordinary adverse
  schooling circumstance: record, reload, resolve, and consume the connection.
- The same report with the relationship absent: no invented connection.
- Correct the circumstance, correct the association's target, retract support,
  and reassert it: distinguish each and use only the applicable current findings.
- Correct the report amount without silently changing which circumstance applies;
  test the selected response to a change in report composition separately.
- Two statements with different circumstances: no unkeyed value leaks across them.
  The recording path must recover both separately even if the bounded tax consumer
  handles one at a time; that is not proof of whole-return integration.
- Similar names or equal amounts without relationship evidence: no inferred match.
- Two statements concerning one borrowing; one statement covering more than one
  borrowing or period: exercise the selected representation or honest unsupported
  behavior. An unsupported shape must not disappear from the test by construction.
- A missing or retracted target: no surviving association treated as sufficient
  merely because its reference still exists.
- Rebuild from the recorded workspace without the original caller's in-memory
  state. The consumer gets its actual inputs from that recovered state.

Select exact expected behavior during design, then implement tests that can
distinguish it from a plausible shortcut. Count equality alone cannot prove
per-statement association; a surviving provenance id alone cannot prove the
calculation used the amount. Include a changed-amount case and a wrong-target
case capable of breaking the intended behavior.

## Work sequence

1. **Product and evidence outline.** Independent early review, then focused
   source and payload investigation. The foreman plans and charters this work.
2. **Track 0 — bounded design and consumer evidence.** Prototype only choices
   whose consequences the named consumer can distinguish. Rival builders are
   appropriate when competing shapes genuinely remain; otherwise explain why a
   direct build is sufficient. Independently review the design and evidence.
3. **Contract unit, if needed.** Consolidate the selected propositions, identity,
   lifecycle, and consumer obligations. Determine whether accepted ADRs already
   suffice or a new decision/schema is needed. Review new contract work before
   implementation relies on it; preserve published history.
4. **Production recording and recovery.** Charter coherent implementation units.
   Test the actual producer, record, currency projection, and recovery path.
5. **Consumer integration evidence and final review.** Feed recovered inputs to
   the bounded consequence consumer, verify the cases and declared limitations,
   and independently review the candidate before curation and closeout.

The foreman can split implementation units after the design makes the dependencies
clear. Do not split by arbitrary document count or create a general grouping
framework to avoid evaluating a specific requirement.

## Exit and stop conditions

The intended completion is working recording/recovery plus an executed connection
to the bounded consumer, not another paper proposal. Completion requires that:
- the ordinary proposition and relationship are recorded from a defined input path;
- stable subject identity is distinguished from report identity and current support;
- correction, retraction, missing support, and multi-record isolation work at the
  actual boundary claimed;
- fresh recovery supplies the consumer without the old relationship stipulation;
- provenance distinguishes user-provided support, association, and rule inference;
- no claim of full deduction support or favorable eligibility is made; and
- the next worksheet-integration milestone has explicit inputs and remaining choices.

If the evidence shows that the person cannot reasonably supply the selected
relationship, the consumer cannot use it, or an unselected product decision
changes its meaning, return that specific obstacle and alternatives. Do not
force a convenient assertion into the product to satisfy the plan. A partial
result requires an explicit disposition, not an unnoticed retreat to documents.

No general Evaluation Context, external institutional catalog, cross-year basis
system, deep explanation UI, or blanket default policy is commissioned here.
Retain those alternatives where relevant without treating them as prerequisites.

Use the normal focused tests and schema/data-safety checks appropriate to the
implementation; substrate changes require the full lane. CI remains the final
gate. Curate durable units and closeout according to PROJECT_PLANNING.md.
