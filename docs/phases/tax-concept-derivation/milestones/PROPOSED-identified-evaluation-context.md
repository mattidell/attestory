# Proposed Milestone: Identified Evaluation Context

**Status: PROPOSED 2026-09-14.** Not planned, not selected. Prerequisite to
resuming `student-loan-interest-deduction-translation`.

## Why this exists

The Student Loan Interest Deduction Translation milestone closed as a bounded
investigation with no production path. Its executable probe established a bounded
result: no committed path can currently use every current Form 1098-E box-1
statement as the iteration subject, require exactly one usable statement
association, resolve the heterogeneous related facts this case needs, fail closed
on an unassociated statement, and preserve statement-isolated dependencies. The
actual pairing dispatcher iterates existing pairing records, so an unpaired box-1
statement is never visited and produces neither a publication nor a blocked row.

`evaluate_pairing_scoped_rule` iterates `for pairing in pairing_sources` and
binds exactly `left_fact_id` and `right_fact_id`. That is a demonstrated property
of the committed dispatcher, not a general claim about the evaluator.

Three verticals have now each needed their own exact-rule authorization to
evaluate per-item: ADR-0071's two pairing rules, ADR-0074's one bound-sources
rule, and the box-1 case that would have been a third. **No further one-off
exact-rule coordinator is authorized.**

## What this milestone establishes

The smallest reusable **identified evaluation context** contract. It declares:

- the **subject** that drives iteration;
- the **required related facts** for each subject instance;
- **cardinality and completeness** — how many of each, and what it means for a
  subject to be unaccounted for;
- **local bindings** available to the declared rule;
- **complete subject accounting** — every declared subject produces an
  identifiable outcome: either a supported publication or a specific blocked or
  unresolved outcome. No subject is silently absent;
- **failure behavior**, including how a failure is attributed to its own subject
  and survives for later use;
- **declared rule evaluation** — the tax determination stays in rule content;
- **subject-specific dependency isolation** — each subject's outcome carries its
  own dependencies and no other subject's. Note that a **blocked subject may
  have no publication at all**, so this cannot be stated only in terms of pins.
  The requirement is that an identifiable causal relationship is preserved for
  supported **and** blocked outcomes; whether that is carried by pins,
  disposition records, or another declared mechanism is for the contract to
  decide, not for this proposal to preselect.

That is the whole of the reusable contract: **identified per-subject
evaluation.** It accounts for every declared subject, produces an identifiable
supported or blocked outcome for each, preserves subject-specific dependencies,
and never silently omits a subject. Nothing beyond that is established here.

### This contract is not an aggregation policy

Subject evaluation and aggregate disposition are **separate operations**, and
this milestone establishes only the first.

- The **identified-evaluation context** determines and preserves each subject's
  outcome and dependencies.
- A **downstream aggregation contract** decides what a set of those outcomes
  produces: whole-set blocking, partial aggregation, or another declared result.

"A failure stays specific to its subject" is about **attribution**. It does not
license a consumer to publish the successful subset, and it does not settle what
any consumer should do with a set of outcomes.

**What the student-loan fixture supplies.** That consumer has already selected a
**whole-set-blocking** policy: any relevant box-1 statement that is
unassociated, unresolved, or otherwise blocked prevents publication of the
eligible-student-supported aggregate and of Schedule 1 line 21, and the
successful statements are not summed around it. That policy is an **input** to
this milestone's compatibility test, not an output of it.

**On what the probe actually showed.** The probe demonstrated that
association-driven dispatch **silently omitted** the unassociated statement and
produced no blocked row for it. It did **not** execute a downstream aggregate
that published the successful subset. No-partial-publication is therefore the
selected student-loan consumer requirement **exposed by** that omission — not an
aggregate misbehavior anyone observed.

That policy is this consumer's. It is **not** a universal rule this contract
imposes. Pairing and nominee grouping are comparison cases precisely because
their local-outcome and aggregate policies may legitimately differ; do not force
one aggregation policy onto all three.

### Provenance topology at both levels

Structural provenance, not reader-facing explanation.

- A **per-subject outcome** carries only that subject's own dependencies.
- An **aggregate** may reference the per-subject outcomes it consumes without
  flattening their distinct lineage.
- The **durable computational outcome must preserve a trace** from an aggregate
  disposition to the responsible subject-specific outcome.

Whether a reader is ever *shown* that trace is the separately deferred
explanation-carrier work, which this milestone does not do.

## Forcing consumer

**The student-loan box-1 case.** It serves two distinct roles, and the boundary
between them is the boundary of this milestone.

### Definition of done — the contract itself

1. every relevant box-1 statement is visited — a statement with no association
   cannot be silently omitted;
2. each statement's required related facts are resolved under declared
   cardinality;
3. every relevant statement yields an identifiable outcome — a supported
   publication or a specific blocked or unresolved outcome — with each failure
   attributed to its own statement;
4. each subject's dependencies are preserved and isolated, by whatever declared
   mechanism the contract adopts, for supported and blocked outcomes alike.

Condition 1 is the defect the prior milestone's probe demonstrated against real
code. Conditions 2–4 are the properties its design needed and could not obtain.

These four are about **per-subject evaluation only**. None of them says what a
consumer does with a set of outcomes.

### Bounded executable compatibility test

A second, narrower deliverable: one executable test using the student-loan
forcing case, supplied with **that fixture's already-selected
whole-set-blocking policy**. It must demonstrate that:

- one unresolved box-1 statement prevents the aggregate and Schedule 1 line 21
  from publishing;
- the successful statements are not silently summed around it;
- the blocked statement and its specific cause remain **structurally
  recoverable** from the durable outcome.

**What this test proves, and what it does not.** It proves the
evaluation-context output is *sufficient to support* a consumer policy of this
kind. It does **not** establish a universal aggregation policy, does **not**
publish a general aggregation contract, and does **not** implement the
student-loan vertical. The policy is an input supplied by the fixture; the
milestone's product is the evaluation context underneath it.

## Adversarial comparison cases

The **pairing** path (ADR-0071) and **nominee grouping** (ADR-0074) are
comparison cases, used adversarially. They test two things:

- whether the proposed contract is **genuinely reusable**, or only describes the
  box-1 case in general-sounding words;
- whether existing specialized machinery **can remain specialized**.

**One implementation is not required to absorb all three patterns.** A result
that says the contract covers box-1 and nominee grouping while pairing stays
specialized is a legitimate and possibly correct outcome. The prior milestone
found three times that cases which look alike at the sentence level differ at
the mechanism level; that history is the reason this constraint is written down.

The box-1 case must not be used to justify another exact-rule exception. If the
contract cannot be stated without one, that is a finding to return, not a shape
to adopt.

## Explicitly out of scope

- **The authoritative institutional catalog.** See below — a separate blocker.
- **The explanation carrier.** Deferred with the student-loan milestone; it
  waits on both the computation and the catalog inputs.
- **A general aggregation contract.** What a consumer does with a set of subject
  outcomes is not established here. The student-loan whole-set-blocking policy
  is supplied to the compatibility test as a fixture input, never derived or
  generalized.
- **Reader-facing rendering** of an aggregate's cause. The requirement here is
  that the durable outcome preserve the trace; showing it to a reader is the
  deferred explanation-carrier work.
- Any student-loan production content, and any resumption of that milestone's
  tracks.

## Separate required blocker: the institutional catalog

This contract will **not** establish who authoritatively determines institution
eligibility, program classification, or half-time status. A `fact-type.v2`
citizen declares vocabulary and supplies no current finding; the `parameter`
operator returns `_as_decimal` and cannot carry a categorical determination. The
open choice is between an evidence or producer path that makes authoritative
determinations current findings, and an adopted categorical catalog grammar.

That work is deferred **for sequencing reasons only**. It is not conceptually
dependent on this contract. Once this prerequisite lands, the catalog and
evidence path is the next explicit decision, before production implementation of
the student-loan vertical resumes.

## Starting evidence

Route directly to these. Do **not** absorb the full student-loan tax analysis,
and do **not** treat the P3 design as a selected implementation.

| Source | Use it for | Limits |
| --- | --- | --- |
| `docs/prototypes/sli-eligible-student/probes/feasibility.py` and `docs/prototypes/sli-eligible-student/findings.md` | The reproducible demonstration of the dispatcher and coverage failure this milestone exists to fix. Start here. | Hand-built environment, authored pins, projection over synthetic rows; box-1 completeness is conceptual and hand-computed; `VALUE_EXPR` is a partial mechanics witness; pin isolation is not proven. |
| `student-loan-interest-deduction-translation-evidence/p2-source-and-entry.md` items 2-4, and `student-loan-interest-deduction-translation-evidence/p2-computation-and-consumers.md` item 2.4 | The engine observations that bound the solution space: how collect sources carry values without identity, what the committed per-item intercepts authorize, and which subtotal shapes collide with the attachment tie-out. | A map of committed behavior at the examined source state. **Revalidate against current code** before relying on a specific claim. |
| `student-loan-interest-deduction-translation.md`, *P3 outcome* and *Scope decision* | The forcing consumer's bounded meaning and its four success conditions. | The narrow promise defines what the consumer needs; it is not a spec for this contract. |
| `student-loan-interest-deduction-translation-evidence/p3-partial-design.md` | A requirements record — what a per-statement path had to do and why each candidate shape failed. | **Not an accepted contract.** Obligations 2a and 2b are undischarged; its proposed mechanisms are unproven. |
| `student-loan-interest-deduction-translation-evidence/` | Only if the bounded meaning of the forcing consumer is in question. | Tax-boundary evidence for the resumed student-loan vertical, not an input to this contract. |

## Suggested shape

Planning gates before implementation, on the pattern the prior milestone used —
with the lesson applied: an **executable discrimination deliverable is planned
from the start**, not added after a documentary design proves unable to
discriminate. A contract whose value is that rules can be evaluated a new way
should be proved by evaluating a rule that new way.
