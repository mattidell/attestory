<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "tax-concept-derivation",
  "milestone_state": "track-3",
  "status": "Opening milestone planned on 2026-08-27; in closeout as of 2026-08-27. The work is bounded to one synthetic 2025 Form 1099-INT box-1 item and one accrued-interest-at-purchase contrast. OUTCOME: a completed executable vertical slice. Two rival representation shapes — distributed, and explicit item-level determination — were built and run on all six cases through the real engine evaluator (exhibit exhibits/reported-interest-tax-concept/it1). Both produce every required number, so arithmetic discriminates nothing; the static ten-requirement rubric discriminates nothing either once the distributed shape has authority attached. Two dynamic probes decide it: the distributed shape can go silently incoherent under partial refresh and cannot detect it, and its carried basis consequence cannot state the reported or includible amount it is consistent with in a later year. RECOMMENDATION: the explicit determination shape, on that narrow ground only, conditional on one open product question — must a consequence that outlives the tax year be self-checkable. TWO CLAIMS ARE WITHDRAWN AND MUST NOT BE RE-ASSERTED: that the incumbent produces the correct number in all six cases (it is silently wrong on TI-A1; the package has no section 135 or Form 8815 content), and that a tax-year {yes, no} fact plus a line-2b guard passes the cases (never built or executed, and it does not follow: TI-B2 needs the circumstance, its amount, and item linkage, and TI-N1 must separate yes-with-amount from yes-without). The objective and scope text written at planning time is superseded by docs/milestones/reported-interest-tax-concept/ and docs/prototypes/reported-interest-tax-concept/.",
  "current_role": "Milestone lead — executable slice complete and durable documents reconciled; awaiting fresh whole-candidate independent review",
  "current_prompt": "docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md#Tracks",
  "scope": [
    "establish the official-source treatment for one reported-interest item and one accrued-interest-at-purchase contrast",
    "exercise evidence, reported fact, ordinary circumstance, tax classification, tax-concept aggregation, return projection, and explanation as distinct layers",
    "compare the explicit item-determination slice with the current direct aggregation path and reduce the result to bounded production-contract questions"
  ],
  "non_goals": [
    "no exhaustive taxable-interest coverage, tax ontology, Schedule B implementation, or additional interest category",
    "no source-family closure, provisional-return, scenario, filing, or user-interface redesign",
    "no production schema, citizen, ADR, or prototype-code adoption without a later owner decision"
  ],
  "deep_reads": {
    "implementation": [
      "docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md#Objective",
      "docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md#Scope",
      "docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md#Non-goals",
      "docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md#Semantic questions",
      "docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md#Synthetic cases",
      "docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md#Tracks",
      "docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md#Stop conditions",
      "docs/phases/tax-concept-derivation/tax-concept-derivation-overview.md#Principles for bounded modeling",
      "docs/milestones/taxable-interest-model-sufficiency/tax-modeling-foundation.md#The chain",
      "docs/milestones/taxable-interest-model-sufficiency/taxable-interest-concept.md#Where the architecture strains",
      "AGENTS.md#Data Safety Rules"
    ],
    "new_milestone": [
      "docs/phases/tax-concept-derivation/tax-concept-derivation-overview.md",
      "docs/phases/tax-concept-derivation/tax-concept-derivation-roadmap.md",
      "docs/milestones/taxable-interest-model-sufficiency/README.md",
      "docs/milestones/taxable-interest-model-sufficiency/claim-boundaries-and-modeling.md",
      "docs/milestones/taxable-interest-model-sufficiency/representation-reconnaissance.md"
    ]
  }
}
-->

# Reported Interest to Tax Concept Vertical Slice

> **Superseded in part. Read this before relying on anything below.**
>
> This plan was written before the work. The deliverables in
> `docs/milestones/reported-interest-tax-concept/` and the executed record in
> `docs/prototypes/reported-interest-tax-concept/` are the record of what was
> found; this plan is the record of what was attempted.
>
> 1. **The authority is wrong wherever this plan implies Treas. Reg. § 1.61-7(c)
>    governs.** That paragraph is the traded-flat / defaulted-interest pattern.
>    The ordinary between-interest-dates purchase is governed by Pub. 550,
>    *Bonds Sold Between Interest Dates*, against IRC § 61(a)(4);
>    § 1.61-7(d) reaches only the seller.
> 2. **The executable slice was built, and it was built late.** For seven review
>    rounds this plan and its deliverables carried a conclusion reached on paper:
>    that the necessity proposition was defeated because the incumbent produced
>    the correct number in all six cases and a `{yes, no}` fact type plus a
>    line-2b guard passed the discriminating ones. **Both halves of that were
>    wrong.** The incumbent is silently wrong on TI-A1, and the `{yes, no}`
>    design was never built or executed and does not follow from the cases. Both
>    claims are withdrawn and must not be re-asserted anywhere.
> 3. **The Objective's success criterion was met**, by an executed comparison of
>    two rival representation shapes rather than by the single slice this plan
>    imagined. The recommendation is the explicit determination shape, on the
>    narrow ground of two dynamic probes, conditional on one open product
>    question. See `docs/prototypes/reported-interest-tax-concept/examination.md`.
>
> Where the text below says no candidate implementation was exercised, or that
> the primary proposition did not survive, it is superseded by point 3.

## Milestone identity

- Phase: Tax Concept Derivation
- Milestone key: `tax-concept-derivation`
- State: in closeout (planned 2026-08-27; executable slice complete)
- Base: `origin/main` at `9159a13d261f5005523ad58f8893ffffd735f204`
- Branch: `milestone/tax-concept-derivation-phase-definition`
- Decision posture: executable exploration; no production representation is
  selected by the plan

## Objective

> **Met, with a distinction the criterion did not anticipate.** Its *numeric*
> half is satisfied by the incumbent too — the same reported box-1 amount
> produces $1,200 and $900 across the two primary cases — and that is Schedule B
> arithmetic, which the second paragraph below expressly says is not success.
> The executed comparison confirms this sharply: **both** candidate shapes
> produce every required number on all six cases, so arithmetic discriminates
> nothing.
>
> The *item-level and layer-ownership* half is where the slice did its work. The
> incumbent fails it — the subtraction is a return row that cannot name the item
> it reduces, the ordinary circumstance cannot be supplied at all, and the
> substantive proposition is labelled rather than asserted. Both prototype
> shapes meet it. Choosing between them required two dynamic probes beyond the
> criterion as written. See
> `docs/prototypes/reported-interest-tax-concept/examination.md`.

Determine, through one bounded executable slice, what the engine must represent
to derive a tax-concept result from a source report plus an ordinary factual
circumstance, and then project that result to a simulated return without making
the source document, the classification, the tax concept, and the form line
mean the same thing.

The milestone is successful if two cases with the same reported Form 1099-INT
box-1 amount can produce different item-level tax treatments for an explicit,
source-grounded reason while preserving what the statement reported. The work
must expose the smallest production-contract decisions required to carry that
distinction into the existing record and derivation system.

It is not successful merely because a calculation reproduces Schedule B
arithmetic. The result must show which layer owns each proposition and how the
layers connect.

## Current state

The repository already has:

- logical statement identity independent of evidence-file identity;
- Form 1099-INT reported fact types and source-family aggregation;
- three Schedule B adjustment families, including accrued interest;
- a ten-slot Form 1040 line-2b rule and a separate seven-slot positive-interest
  composition;
- versioned rule, citation, package, derivation, and presentation machinery;
- synthetic interest fixtures; and
- a completed exploratory account showing that the current concept meaning is
  distributed across computation and reporting artifacts and that the
  subtractive-adjustment contract was never settled.

The current engine therefore supplies a useful incumbent path. It does not
supply the answer in advance. In particular, the presence of an accrued-
interest subtraction row does not establish that the engine represents the
reported item, economic circumstance, substantive classification, and
reporting operation separately.

## Scope

> **Superseded in part.** Item 6 presupposes what the milestone was meant to
> test and was not established: the six cases do not show that an item-level
> determination preserving both amounts is needed. Items 7 through 9 were
> exercised against the incumbent only. See
> `docs/milestones/reported-interest-tax-concept/README.md`.

The milestone covers exactly:

1. one taxpayer subject, US-federal individual income tax, tax year 2025;
2. one synthetic logical Form 1099-INT statement with one box-1 amount;
3. the reported fact that the statement reports that amount;
4. one ordinary circumstance concerning accrued interest paid at purchase,
   represented independently of the reported fact;
5. the official-source proposition that determines how that circumstance
   affects the taxpayer's current-year includible interest, with its limits;
6. an item-level classification or determination that preserves both the
   reported amount and the derived includible amount;
7. aggregation of the classified item into the slice's taxable-interest
   result;
8. projection of that result to the simulated Form 1040 line-2b position; and
9. a recoverable explanation of the path and a comparison with the current
   direct aggregation route.

The milestone may use an isolated executable prototype. Prototype shapes are
evidence, not production citizens, and prototype code does not merge as
production code.

## Non-goals

- No claim to complete taxable-interest or Schedule B coverage.
- No second interest source, multiple statement aggregation, or mixed interest
  family fixture.
- No §135 education exclusion, original issue discount, nominee allocation,
  bond-premium amortization, market-discount election, previously reported
  savings-bond interest, frozen-deposit timing, seller-financed mortgage, K-1,
  or non-form interest implementation.
- No joint-return, community-property, beneficial-owner, or multi-person
  authority model.
- No Schedule B attachment-trigger or foreign-account/trust question work.
- No redesign of workspace completeness, source-family closure, zero from
  absence, provisional results, action-scoped assumptions, saved scenarios, or
  return status.
- No filing, transmission, liability determination, or professional-attestation
  behavior.
- No production UI or final user-facing copy.
- No accepted ADR, governance change, published schema, new citizen family, or
  production migration unless the owner selects a later milestone after
  reviewing this evidence.
- No census of every taxable-interest category. Cases outside the selected pair
  may invalidate an overbroad conclusion but may not enlarge implementation
  scope.

## Semantic questions

> **Answered, in `docs/milestones/reported-interest-tax-concept/`.** The
> "executable representation" half was not produced: no slice was built. Where
> those documents and this list differ, the documents govern. Question 4 in
> particular was answered as *not established on this evidence*, not as
> "item-level."

The slice must answer these questions in ordinary language and in its
executable representation:

1. What proposition belongs to the logical statement, and what identifies that
   statement independently of a file?
2. What proposition describes the accrued-interest circumstance, who or what
   is its subject, and what evidence or user act could support it?
3. Which adopted tax proposition turns the reported amount and circumstance
   into an includible amount?
4. Is the classification item-level, aggregate-level, or both, and what is lost
   if only the aggregate survives?
5. What identifies the derived tax concept: subject, jurisdiction, tax year,
   quantity, and modeled operation?
6. Where is executable coverage declared without redefining taxable interest
   as whatever this slice happens to cover?
7. What does the return projection assert beyond correspondence between the
   concept result and a form line?
8. Which changes make the derived result stale or displaced: source correction,
   circumstance correction, rule succession, or reporting-artifact succession?
9. What can a reader recover from committed artifacts without reading Python or
   reconstructing the authoring conversation?

The milestone records concrete answers and unresolved alternatives. It does
not create vocabulary merely to make the answers sound systematic.

## Contracts and authority posture

Existing governance, accepted ADRs, and immutable published schemas remain
binding. The completed Taxable Interest Modeling milestone is exploratory
evidence and supplies no selected citizen or schema.

Official sources are used to establish the tax treatment exercised by the
fixture and the meaning of the reporting position. IRS instructions may
establish reporting operations; the lead must separately determine whether
controlling law or other official guidance is needed for the substantive
classification. Citations attach to the propositions they support, not to the
result as decoration.

The product's aim is to model how a conclusion is reached and how it can be
examined. It is not to manufacture institutional authority. The user supplies
ordinary facts about the statement and transaction; the user is not asked to
assert the legal conclusion “taxable interest.”

If the slice requires interpreting or changing governance, inventing a citizen
kind, or revising an accepted product contract, the work stops with a precise
owner decision. A convenient prototype shape is never treated as permission to
publish it.

## Synthetic cases

> **The expectations below describe a prototype that was never built.** All
> six cases were instantiated on paper and run against the incumbent instead.
> The incumbent produces the correct number in every one of them. Read the
> outcomes in `docs/milestones/reported-interest-tax-concept/`
> `synthetic-case-specification.md`, which also corrects TI-B2's authority and
> TI-L1's amounts.

All amounts and identities are obviously synthetic. Track 0 fixes exact values
after verifying that the fact pattern is legally coherent.

| Case | Facts held constant | Distinguishing circumstance | Required observation |
| --- | --- | --- | --- |
| TI-B1 — ordinary reported interest | One logical 2025 Form 1099-INT reports one positive box-1 amount | No accrued-interest-at-purchase circumstance applies | The reported amount remains visible and the item-level includible amount equals it for the rule-grounded reason exercised by the case. |
| TI-B2 — accrued-interest contrast | Same logical statement and same box-1 amount | A bounded positive amount of accrued interest was paid at purchase and the verified treatment applies | The statement still reports the same amount; the circumstance and rule produce a separately recoverable, different includible amount. |
| TI-N1 — missing circumstance answer | Same statement; the product has detected that the accrued-interest branch is material but the necessary ordinary fact is unresolved | No answer is supplied | The prototype does not silently choose a branch. It identifies the ordinary factual question and preserves the reported fact. |
| TI-L1 — source correction | Case TI-B2, then the source report is corrected while the circumstance is unchanged | Corrected reported amount | The prior determination is no longer current; the circumstance is not rewritten merely because the report changed. |
| TI-L2 — circumstance correction | Case TI-B2, then the accrued-interest amount is corrected while the source report is unchanged | Corrected circumstance amount | The prior determination is no longer current; the reported fact remains unchanged. |
| TI-A1 — outside-slice probe | A synthetic fact pattern from §135, OID, nominee, timing, or election territory | The case is intentionally unsupported | The prototype cannot present success over the opening slice as evidence that this adjacent case is modeled. No implementation of the adjacent case follows. |

## Prototype evidence boundary

> **The primary proposition below is supported, on a narrow executed ground.**
> Two rival representation shapes were built and run on all six cases through
> the engine's real expression evaluator. Both produce every required number, so
> arithmetic decides nothing; the static requirement set decides nothing either
> once the distributed shape has authority attached. Two dynamic probes decide
> it — silent incoherence under partial refresh, and the inability of a carried
> basis consequence to check itself in a later year. The recommendation is
> conditional on one open product question. See
> `docs/prototypes/reported-interest-tax-concept/examination.md`.
>
> The stop-before-prototype clause below **was** exercised for most of this
> milestone, and that was the error the executed round corrects. Two claims made
> during that period are withdrawn and must not be re-asserted: that the
> incumbent produces the correct number in all six cases, and that a `{yes, no}`
> declaration plus a line-2b guard passes the discriminating ones.

The primary proposition is:

> An item-level tax determination, separately recoverable from both the source
> report and the return projection, is necessary to preserve a legally material
> reported-versus-includible distinction through derivation.

Two dependent questions are permitted: whether executable coverage needs a
separate declaration in this slice, and which lifecycle inputs must displace
the determination. All other representation questions are deferred.

The current distributed line-2b path is the incumbent. The explicit item-level
determination is the candidate. Both are exercised against the same cases. The
initial evidence ceiling is a paper instantiation plus the cheapest executable
probe that can demonstrate source correction and circumstance correction; no
persisted end-to-end production integration is authorized.

If paper examples show that the existing artifact graph already preserves and
declares the distinction, stop before **new** prototype code and exercise the
incumbent path against the selected cases. Record the missing linkage precisely.
If a separate executable probe is needed, use an isolated prototype whose code
is not a production candidate. One build iteration and one bounded repair are
the default cap. The owner decides whether the evidence warrants a contract
milestone.

Working review notes and process metadata are not final deliverables. Repairs
are applied to the durable artifacts; any material unresolved dissent is
captured in the final comparison by substance rather than by track history.

## Deliverables

Durable milestone documents must stand on their own and carry no track number,
commit number, role-fulfillment metadata, review status, or execution diary.
The milestone produces:

- a source-grounded taxable-interest item model for the selected cases;
- a synthetic fixture specification covering the six cases above;
- an executable prototype exhibit, retained only under the repository's
  prototype/archive rules if code was necessary;
- a comparison of the incumbent and candidate paths against the same cases;
- a concise production-contract decision brief naming what the evidence
  settles, what remains open, and the smallest next milestone; and
- roadmap and phase-state updates reflecting the owner disposition.

Independent reviews are measurements, not publication artifacts. They do not
remain in the final milestone source unless unresolved material evidence cannot
be recovered another way; in that case the final comparison captures the
substance without preserving review-process metadata.

## Verification

Before close, the lead must establish:

- every substantive treatment in the synthetic cases traces to a named official
  source and the exact proposition the source supports;
- both primary cases use the same reported fact and differ only through the
  named circumstance;
- both correction cases demonstrate independent lifecycle behavior;
- the missing-answer case cannot silently take either tax branch;
- the outside-slice probe cannot be mistaken for covered success;
- the incumbent and candidate are compared against identical cases;
- the result, rule, source facts, coverage boundary, and form projection are
  recoverable without relying on review prose;
- all fixtures use demo identities and obviously synthetic values;
- `python3 tools/governance_lint.py` is conformant;
- `git diff --check` is clean; and
- any code path runs the cheapest focused tests appropriate to its location,
  with the full suite reserved for CI unless substrate work makes it mandatory.

CI `verify` on the final candidate remains the merge gate of record.

## Data safety

Only public tax authorities and committed, obviously synthetic data may be
used. No real tax document, personal fact, private output, workspace path,
disposition, or refusal reason enters the repository or an agent account.
Synthetic ids use `demo.*` or `demo-*`, and generated scratch output stays in
ignored paths.

## Track 0 adversarial closure

**Status: COMPLETE.** The first gate initially recorded a FAIL — the sources did not support the treatment as originally attributed — and the repair to Pub. 550 against IRC § 61(a)(4) was confirmed. The gate outcomes are carried in the deliverables. Two gates were later re-answered by execution: "the incumbent and candidate can be exercised on identical propositions and values" resolves to **no** (the incumbent cannot be given the ordinary circumstance at all), and "the prototype evidence boundary is sufficient to resolve the primary proposition" resolves to **yes, but only with prototype code**, which is why the stop-before-prototype clause should not have fired. The original gate list follows. Before any executable-build charter, Track 0 must record a
pass, fail, or explicit deferral for each of these gates:

- the official sources support the exact substantive treatment used by TI-B1
  and TI-B2 rather than only the reporting notation;
- the selected fact pattern does not silently depend on an election, instrument
  category, timing rule, or second person outside scope;
- the ordinary circumstance can be stated without asking the user for a legal
  classification;
- the incumbent and candidate can be exercised on identical propositions and
  values;
- source correction and circumstance correction are independently observable;
- the candidate's subject, period, jurisdiction, quantity, authority, coverage,
  and reporting consumer are all named;
- no existing accepted contract already answers the primary proposition; and
- the prototype evidence boundary is sufficient to resolve the primary
  proposition without production integration.

If separate prototype code remains necessary after this gate, Track 0 creates
the owner-approved prototype plan required by `PROJECT_PLANNING.md` before a
prototype charter. A `FAIL` blocks executable work; it does not authorize a
broader replacement case.

## Tracks

> **Execution order differed from the plan.** Track 0 completed and its
> stop-before-prototype clause fired, so Track 1 was deferred and Track 2 ran
> first, as adversarial review of paper analysis rather than as a comparison of
> two executed paths. That ordering produced a conclusion that repeated review
> could not repair, because the defect was missing evidence rather than
> imprecise prose. Track 1 was then run under owner direction, with the rival
> shape supplied by the plan's own primary proposition. The durable output is
> the four documents in `docs/milestones/reported-interest-tax-concept/` and the
> executed record in `docs/prototypes/reported-interest-tax-concept/`.

### Track 0 — Source and semantic boundary

Verify the selected treatment from official sources; fix the exact fact
pattern, propositions, subject, period, and boundary; instantiate all six cases
on paper; and determine whether the primary proposition remains unresolved
after comparison with the current artifact graph.

Stop before new prototype code if paper plus the incumbent execution answers
the representation question. Do not replace the selected case with a broader
one merely because adjacent authority is interesting.

### Track 1 — Bounded executable slice

If Track 0 leaves the primary proposition unresolved, exercise the incumbent
and explicit item-determination candidate against the same cases at the lowest
useful evidence rung. Demonstrate the two independent corrections and the
missing-answer behavior. Keep prototype code outside the production candidate.

### Track 2 — Adversarial comparison and decision reduction

Have an independent reviewer attack layer collapse, legal overreach, false
generality, lifecycle mistakes, and artifacts whose meaning is recoverable only
from prose or Python. Apply repairs to durable work. Reduce the evidence to the
smallest production-contract questions and a recommendation about whether to
proceed, repeat one bounded probe, or stop.

### Track 3 — Owner disposition and curation

Record the owner's substantive decisions, update the roadmap and phase state,
remove working reviews and process-only artifacts, archive or discard prototype
evidence under the repository rules, and curate the branch for merge. Do not
convert a prototype shape into a production contract during curation.

## Stop conditions

> **Already fired.** The stop-before-new-prototype-code condition in the
> prototype evidence boundary was exercised: paper analysis plus execution of
> the incumbent answered the representation question, so Track 1 never ran.
> The milestone is in closeout awaiting an owner decision, not mid-probe. Do
> not resume an executable slice from this section alone.

Stop and return to the owner when:

- official-source review shows that the accrued-interest fact pattern cannot be
  bounded without adding another substantive category or unresolved election;
- the work requires a new citizen kind, published schema, governance
  interpretation, or change to an accepted ADR;
- a multi-person, joint-return, or authority-allocation question becomes
  load-bearing;
- the executable probe would require production-path migration merely to answer
  the primary proposition;
- the outside-slice probe becomes implementation scope;
- the lead cannot state what observable decision another iteration would
  resolve; or
- personal or non-synthetic data would be needed.

At a stop, preserve the verified facts and name the narrow decision. Do not
fill the gap with an inferred architecture.

## Exit criteria

> **All eight criteria are met.** Criterion 3 reads differently after execution
> than it did on paper: the comparison that mattered turned out to be between
> two *candidate* shapes rather than between the incumbent and one candidate.
> The incumbent cannot be posed the six cases at all — it has no representation
> of the ordinary purchase question — so "identical evidence" is satisfied
> between the two rival shapes, and the incumbent is characterised at three
> distinct grades of evidence (exact execution of its own tests, a structural
> analogue at different amounts, and artifact inspection) rather than pretended
> to have run the cases. Criterion 5 is met by executed lifecycle observations,
> not by argument. See
> `docs/prototypes/reported-interest-tax-concept/examination.md`.
>
> This is a **completed executable vertical slice**, not an exploratory finding.
> The distinction matters: an exploratory finding would license carrying the
> conclusion forward as settled context, whereas the recommendation here is
> conditional on one named product question and rests on one fixture.

The milestone is complete when:

1. the six synthetic cases are source-grounded and internally coherent;
2. the same reported fact survives both primary cases while the applicable
   tax treatment changes for an explicit reason;
3. the work shows whether a separately recoverable item-level determination is
   necessary, with the incumbent and candidate evaluated on identical evidence;
4. subject, period, jurisdiction, quantity, rule, source facts, authority, and
   reporting projection are located without collapsing them;
5. the lifecycle consequences of correcting the source and correcting the
   circumstance are independently demonstrated;
6. executable coverage is distinguished from the meaning of taxable interest
   without attempting a taxable-interest census;
7. the final documents state the bounded production-contract questions in
   high-level plain language and contain no review/process metadata; and
8. the owner can select the representation-contract milestone, request one
   named additional probe, or stop the phase without needing to reconstruct
   the authoring conversation.
