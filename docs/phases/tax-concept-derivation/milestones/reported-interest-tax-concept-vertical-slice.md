<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "tax-concept-derivation",
  "milestone_state": "track-3",
  "status": "Opening milestone planned on 2026-08-27; in closeout as of 2026-08-28. Bounded to one synthetic 2025 Form 1099-INT box-1 item and one accrued-interest-at-purchase contrast, plus a distinct box-3 TI-A1 fixture. OUTCOME: a completed executable vertical slice whose deciding evidence was repaired in a successor iteration. Three shapes — distributed (A), distributed with a partition edge (A+), and explicit item-level determination (B) — ran on all six cases through the real engine evaluator under one shared execution and currentness policy (exhibit exhibits/reported-interest-tax-concept/it2; it1 retained unchanged as historical prototype evidence). Arithmetic does not discriminate. The repaired provenance rubric and a six-task later-year consumer do not establish that a new citizen kind is necessary. Partial refresh is deleted as deciding evidence. The hard-coded cross-year verdict is deleted. RECOMMENDATION: none on necessity grounds. The remaining difference is an owner-held product requirement: when a later year needs the basis consequence, does it hold only the carried artifact, or may it re-open the source year? WITHDRAWN AND MUST NOT BE RE-ASSERTED: (1) that the incumbent produces the correct number in all six cases — it is silently wrong on TI-A1, where box 3 flows unreduced into selected line-2b v4 and no committed rule computes the section 135 exclusion; the package does contain Form 8815 content as tax.us.2025.ss-benefits-scope.no-form-8815, consumed by the Social Security Benefits Worksheet, not by line 2b; (2) that a tax-year {yes, no} fact plus a line-2b guard passes the cases (never built or executed, and it does not follow); (3) that two dynamic probes on it1 decide the representation, or that the explicit determination is recommended on that evidence; (4) that the prototype was never built, that Track 1 never ran, or that paper plus the incumbent answered the representation question. Durable record: docs/milestones/reported-interest-tax-concept/ and docs/prototypes/reported-interest-tax-concept/.",
  "current_role": "Milestone lead — repaired executable evidence and durable documents reconciled; awaiting fresh whole-candidate independent review",
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

> **Read this before relying on anything below.** This plan was written before
> the work. The deliverables in `docs/milestones/reported-interest-tax-concept/`
> and the executed record in `docs/prototypes/reported-interest-tax-concept/`
> are the record of what was found. Each named section below is also rewritten
> locally so that a section loaded on its own does not still carry a withdrawn
> claim.
>
> 1. **The authority is wrong wherever this plan implies Treas. Reg. § 1.61-7(c)
>    governs.** That paragraph is the traded-flat / defaulted-interest pattern.
>    The ordinary between-interest-dates purchase is governed by Pub. 550,
>    *Bonds Sold Between Interest Dates*, against IRC § 61(a)(4);
>    § 1.61-7(d) reaches only the seller.
> 2. **The executable slice was built.** Iteration 1 is retained as
>    `exhibits/reported-interest-tax-concept/it1`. Iteration 2 repaired its
>    deciding evidence and is the current exhibit,
>    `exhibits/reported-interest-tax-concept/it2`. Do not re-assert that the
>    prototype was never built, that Track 1 never ran, or that paper plus the
>    incumbent answered the representation question.
> 3. **No representation is recommended on necessity grounds.** Arithmetic
>    does not discriminate. Iteration 1's two probes do not decide the
>    representation: partial refresh was a manufactured discriminator, and the
>    cross-year verdict was hard-coded. See
>    `docs/prototypes/reported-interest-tax-concept/examination.md`.
> 4. **Two earlier claims remain withdrawn.** The incumbent is silently wrong
>    on TI-A1 (box 3 flows unreduced into selected line-2b v4; no committed
>    rule computes the § 135 exclusion; Form 8815 content exists as
>    `tax.us.2025.ss-benefits-scope.no-form-8815` on the Social Security
>    Benefits Worksheet, not on line 2b). A tax-year `{yes, no}` fact plus a
>    line-2b guard was never built or executed and does not follow from the
>    cases.

## Milestone identity

- Phase: Tax Concept Derivation
- Milestone key: `tax-concept-derivation`
- State: in closeout (planned 2026-08-27; executable evidence repaired 2026-08-28; not closed)
- Base: `origin/main` at `9159a13d261f5005523ad58f8893ffffd735f204`
- Branch: `milestone/tax-concept-derivation-phase-definition`
- Decision posture: executable exploration; no production representation is
  selected by the plan

## Objective

> **Met, with a distinction the criterion did not anticipate.** Its *numeric*
> half is satisfied by the incumbent too on the two primary box-1 cases — the
> same reported amount produces $1,200 and $900 — and that is Schedule B
> arithmetic, which the second paragraph below expressly says is not success.
> The executed comparison confirms this sharply: **all three** candidate shapes
> produce every required number on all six cases, so arithmetic discriminates
> nothing.
>
> The *item-level and layer-ownership* half is where the slice did its work. The
> incumbent fails it — the subtraction is a return row that cannot name the item
> it reduces, the ordinary circumstance cannot be supplied at all, and the
> substantive proposition is labelled rather than asserted. All three prototype
> shapes meet it under one shared execution and currentness policy, with one
> exception that does not establish a new citizen kind. Iteration 1's two
> probes do not decide the representation. See
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

The milestone covers exactly:

1. one taxpayer subject, US-federal individual income tax, tax year 2025;
2. one synthetic logical Form 1099-INT statement with one box-1 amount, and a
   distinct second statement carrying a box-3 Series EE amount solely for the
   out-of-slice case;
3. the reported fact that the statement reports that amount;
4. one ordinary circumstance concerning accrued interest paid at purchase,
   represented independently of the reported fact;
5. the official-source proposition that determines how that circumstance
   affects the taxpayer's current-year includible interest, with its limits;
6. **whether** an item-level classification or determination that preserves
   both the reported amount and the derived includible amount is necessary —
   the slice tests this; it does not presuppose the answer. Execution did not
   establish necessity;
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

> **Answered, in `docs/milestones/reported-interest-tax-concept/` and the
> executed record in `docs/prototypes/reported-interest-tax-concept/`.** The
> slice was built and repaired. Where those documents and this list differ, the
> documents govern. Question 4 in particular is answered as *not established on
> this evidence*, not as "item-level."

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

All amounts and identities are obviously synthetic. Track 0 fixed exact values
after verifying that the fact pattern is legally coherent. All six cases were
then executed under three rival shapes through the real engine evaluator;
see `docs/milestones/reported-interest-tax-concept/synthetic-case-specification.md`
and `docs/prototypes/reported-interest-tax-concept/examination.md`. The
incumbent is **not** correct in all six: it is silently wrong on TI-A1.

| Case | Facts held constant | Distinguishing circumstance | Required observation |
| --- | --- | --- | --- |
| TI-B1 — ordinary reported interest | One logical 2025 Form 1099-INT reports one positive box-1 amount | No accrued-interest-at-purchase circumstance applies | The reported amount remains visible and the item-level includible amount equals it for the rule-grounded reason exercised by the case. |
| TI-B2 — accrued-interest contrast | Same logical statement and same box-1 amount | A bounded positive amount of accrued interest was paid at purchase and the verified treatment applies | The statement still reports the same amount; the circumstance and rule produce a separately recoverable, different includible amount. |
| TI-N1 — missing circumstance answer | Same statement; the product has detected that the accrued-interest branch is material but the necessary ordinary fact is unresolved | No answer is supplied | The prototype does not silently choose a branch. It identifies the ordinary factual question and preserves the reported fact. |
| TI-L1 — source correction | Case TI-B2, then the source report is corrected while the circumstance is unchanged | Corrected reported amount | The prior result is no longer current; the circumstance is not rewritten merely because the report changed. |
| TI-L2 — circumstance correction | Case TI-B2, then the accrued-interest amount is corrected while the source report is unchanged | Corrected circumstance amount | The prior result is no longer current; the reported fact remains unchanged. |
| TI-A1 — outside-slice probe | A distinct Form 1099-INT reports Series EE savings-bond interest in **box 3**, with qualified education expenses | The case is intentionally unsupported | The prototype cannot present success over the opening slice as evidence that this adjacent case is modeled. No implementation of the adjacent case follows. |

## Prototype evidence boundary

The primary proposition is:

> An item-level tax determination, separately recoverable from both the source
> report and the return projection, is necessary to preserve a legally material
> reported-versus-includible distinction through derivation.

**That proposition is not established.** Three rival shapes were built and run
on all six cases through the engine's real expression evaluator, under one
shared execution and currentness policy, on exhibit
`exhibits/reported-interest-tax-concept/it2`. Arithmetic does not discriminate.
The repaired provenance rubric and a six-task later-year consumer do not
establish that a new citizen kind is necessary. Iteration 1's two probes —
partial refresh, and a hard-coded cross-year verdict — do **not** decide the
representation and are withdrawn as deciding evidence. See
`docs/prototypes/reported-interest-tax-concept/examination.md`.

Two dependent questions remain permitted: whether executable coverage needs a
separate declaration in this slice, and which lifecycle inputs must displace a
result. All other representation questions are deferred.

The current distributed line-2b path is the incumbent. The candidates are a
distributed representation, the same representation carrying one durable
partition edge, and an explicit item-level determination. All three are
exercised against the same cases. No persisted end-to-end production
integration is authorized.

The stop-before-prototype clause below was exercised for most of this
milestone, and that was an error: paper plus the incumbent did **not** answer
the representation question. Track 1 ran. Two claims made during the paper
period remain withdrawn: that the incumbent produces the correct number in all
six cases, and that a `{yes, no}` declaration plus a line-2b guard passes the
discriminating ones.

If a separate executable probe is needed, use an isolated prototype whose code
is not a production candidate. The owner decides whether the evidence warrants
a contract milestone.

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

> **Execution order differed from the plan, then the deciding evidence was
> repaired.** Track 0 completed and its stop-before-prototype clause fired, so
> Track 1 was deferred and Track 2 ran first as adversarial review of paper
> analysis. That ordering produced a conclusion that repeated review could not
> repair, because the defect was missing evidence. Track 1 then ran under owner
> direction (`exhibits/reported-interest-tax-concept/it1`). Independent review
> found that iteration's deciding probes and provenance rubric defective.
> Iteration 2 repaired the executable evidence
> (`exhibits/reported-interest-tax-concept/it2`) and the durable documents were
> reconciled to it. Track 1 ran. Paper plus the incumbent did not answer the
> representation question. No representation is recommended on the repaired
> evidence. The durable output is the four documents in
> `docs/milestones/reported-interest-tax-concept/` and the executed record in
> `docs/prototypes/reported-interest-tax-concept/`.

### Track 0 — Source and semantic boundary

Verify the selected treatment from official sources; fix the exact fact
pattern, propositions, subject, period, and boundary; instantiate all six cases
on paper; and determine whether the primary proposition remains unresolved
after comparison with the current artifact graph.

Stop before new prototype code if paper plus the incumbent execution answers
the representation question. **That stop fired, and it was wrong to treat it as
an answer:** paper plus the incumbent did not answer the representation
question, and Track 1 subsequently ran. Do not replace the selected case with a
broader one merely because adjacent authority is interesting.

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

> **The paper-period stop fired, and it was not an answer.** Paper analysis
> plus execution of the incumbent did **not** answer the representation
> question. Track 1 ran. The current exhibit is
> `exhibits/reported-interest-tax-concept/it2`. The milestone is in closeout
> awaiting a fresh whole-candidate independent review, then an owner decision.
> It is not closed. Do not resume a third prototype iteration from this section
> alone.

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

The milestone is complete when:

1. the six synthetic cases are source-grounded and internally coherent;
2. the same reported fact survives both primary cases while the applicable
   tax treatment changes for an explicit reason;
3. the work shows whether a separately recoverable item-level determination is
   necessary, with candidates evaluated on identical evidence — **shown: not
   established**;
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

Criteria 1–7 are met by the repaired executable record. Criterion 3 reads:
the comparison that mattered is among three *candidate* shapes, not between
the incumbent and one candidate. The incumbent cannot be posed the six cases
at all — it has no representation of the ordinary purchase question — so
"identical evidence" is satisfied among the rival shapes, and the incumbent
is characterised at three distinct grades of evidence (exact execution of its
own tests, a structural analogue at different amounts, and artifact
inspection) rather than pretended to have run the cases. Criterion 5 is met
by executed lifecycle observations under one shared currentness policy, not
by argument, and not by iteration 1's partial-refresh probe. See
`docs/prototypes/reported-interest-tax-concept/examination.md`.

This is a **completed executable vertical slice whose deciding evidence was
repaired**, not an exploratory finding and not a closed milestone. No
representation is recommended on necessity grounds. Criterion 8 waits on a
fresh whole-candidate independent review, then the owner.
