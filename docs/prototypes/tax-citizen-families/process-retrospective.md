# Tax Citizen Families Prototype Process Retrospective

Date: 2026-07-11

Status: round 4 complete; owner disposition pending. This is a prototype-process
retrospective, not the First Tax Slice milestone retrospective. The milestone
has not entered implementation.

## Executive Conclusion

The modeling questions were consequential, but Track 0 became uneconomical
because it combined several distinct Tier 2 decisions and then used production-
path integration as the acceptance standard for all of them. Review findings
expanded the prototype from citizen-family shape into package closure,
projection authority, coverage semantics, explanation APIs, citation
resolution, tax-method conditions, and persistence ordering. That is much of
Tracks 1-5 performed speculatively inside Track 0.

Do not adopt the rival builder implementation wholesale. Prototype code is
throwaway evidence, and the committee found unresolved authority boundaries in
every later refinement. Do preserve and cite the convergent design evidence.
The work supports a narrower evaluation analysis and one or more smaller ADRs;
it does not support ratifying the full it4 corpus as one contract.

## Cost Record

- Four prototype exhibits: it1 23 files/56,846 bytes; it2 16 files/79,265
  bytes; it3 46 files/163,383 bytes; it4 64 files/191,412 bytes.
- Four committee rounds with four reviews each: 16 reviews and 3,294 review
  lines.
- 37 mainline process/document commits since the first builder dispatch.
- Approximately 6,100 lines under the process document tree.
- Two builder handoffs returned for missing charter evidence.
- One iteration beyond the default three-iteration cap, authorized as a bounded
  integration proof.
- Track 1 production implementation has not started.

These figures understate model cost because they exclude discarded reasoning,
tool output, owner-launched sessions, and repeated independent reproduction.

## Benefits Earned

The effort produced evidence that would have been expensive to discover after
publishing schemas:

- W-2 slip identity must be peer to evidence and can support same-fact
  correction, downstream displacement, and re-derivation.
- Source-set closure is determinable and attested, not an elective tax choice.
- Existing `fact-type.v1` can express the bounded tax facts exercised here;
  companion content citizens are preferable to inflating the kernel fact type.
- A form field has useful first-class identity and rendering/explanation
  semantics distinct from a rule output symbol.
- Computed zero, closure-backed zero, blocked absence, invalidity, and false
  guard are distinct states that must remain visible.
- Line 1z, standard-deduction eligibility, line-16 method selection, and
  all-open saturation exposed real honesty boundaries in the tax slice.
- The persisted ActLog -> projection -> run/record -> publication -> composed
  currency path works for a real synthetic tax scenario.
- The process exposed machinery and contract gaps before production content
  depended on them.

Those benefits justify a prototype. They do not justify every iteration or the
full scope eventually accumulated.

## Why Cost Expanded

### Too many decisions in one gate

The original gate asked five questions, but they were not one decision:

1. tax fact-type sufficiency and identity;
2. form-field citizenship and rendering absence;
3. source-set closure nature and lifecycle;
4. citation placement and semantic attachment; and
5. coverage/read-model shape.

Reviews then added package/provenance closure, correction lifecycle, condition
projection, explanation traversal, and production adoption/pinning. Each is a
separate architectural boundary with a different cheapest proof.

### Prototype and implementation evidence were conflated

A schema-shape decision can often be tested with hand-written instances and
mutations. Instead, later charters required the complete persisted execution
path. That was justified for correction and authority flow, but excessive for
form-field shape, citation inertness, and rendered-absence vocabulary.

### Adjacent defects expanded the charter

Reviewers correctly found real defects. The process treated nearly every defect
as a reason to enlarge the next iteration rather than classify it as:

- blocking the decision under review;
- a production ratification condition;
- a separate machinery patch; or
- deferred breadth.

This converted review thoroughness into unbounded scope growth.

### Green-check incentives displaced decision evidence

Builders optimized for declared gates by adding checks. Several checks were
helper-local, tautological, or exercised a hand-built projection rather than the
claimed authority boundary. Later charters corrected this, but at high cost.
The better early gate is a one-page evidence map naming the authoritative
producer, consumer, and failure mutation before any harness is built.

### The milestone premise was partly false

First Tax Slice was planned as pure content on finished machinery. The content
exposed unfinished or underspecified machinery: package adoption identity,
`closed_sets`, content-manifest closure, non-publication explanations, and
publication/record ordering. Once that happened, Track 0 was no longer only a
citizen-family prototype.

## Consequence Assessment

| Decision | Consequence | Prototype depth justified |
|---|---|---|
| Fact identity and supersession keys | Very high; every future finding and migration depends on it | End-to-end lifecycle proof |
| Closure authority and source-family mapping | Very high; determines when absence may become zero | End-to-end authority and pin proof |
| Fact-type reuse versus kernel schema version | High; all future tax content authors against it | Rival schemas plus worked instances |
| Form-field citizen shape | Medium-high; broad content surface but versionable | Static rival instances and renderer walk |
| Package/adopted-content boundary | High, but separate from form fields | Separate machinery/content-manifest decision |
| Eligibility and tax-method condition structure | High tax meaning; not merely serialization | Focused condition-model prototype |
| Citation attachment/resolver | Medium; versionable and non-authoritative to derivation | Static resolver contract plus semantic negatives |
| Coverage read model | Medium; derived and rebuildable | Record examples and consumer contract, not full tax run |
| Rendering labels and fixture breadth | Low-medium; content-versioned | Implementation tests, not independent prototype rounds |

The milestone was large because it combined most rows in this table, not because
every Tier 2 ADR requires four iterations.

## Rival Builder Disposition

Adopt evidence, not code.

Use it2/it3/it4 as cited exhibits for conclusions that survived independent
attack. Do not merge or mechanically port the rival implementation. Production
work should re-express accepted contracts in `packages/` with the milestone's
normal tests and commit structure.

Candidate conclusions for a narrow evaluation analysis:

- W-2-slip-based fact identity and correction behavior;
- determinable/attested closure fact nature;
- existing `fact-type.v1` sufficiency for the bounded facts;
- first-class form-field citizens distinct from output symbols; and
- explicit rendered-absence dispositions.

Do not ratify yet:

- caller-supplied `closed_sets` or its undeclared source-family mapping;
- aggregate scalar eligibility/method facts as a substitute for condition
  structure;
- the it4 package as the complete adopted content boundary;
- harness-local coverage-family meaning;
- non-publication explanation traversal;
- the citation resolver's citizen/adoption/pin relationship; or
- prototype content ids/versions as production artifacts.

Prior work is not wasted if the decision is narrowed. It becomes waste only if
effort is used as a reason to adopt unresolved code.

## Economic Gates For Future Prototypes

### Gate 0 - Decision inventory

Before chartering, list each independent proposition that could become an ADR
sentence. One prototype topic may contain only one primary proposition and at
most two tightly dependent secondary propositions. Split the rest.

### Gate 1 - Prototype eligibility score

Score 0-2 on four axes: future blast radius, migration cost, uncertainty after
worked examples, and inability to test cheaply during implementation.

- 0-3: implement normally; retrospective or Tier 1 record.
- 4-5: paper spike plus ADR draft; no committee prototype by default.
- 6-8: prototype eligible.

Tier 2 status alone does not automatically authorize the most expensive
evidence level. Contract-foundational reach plus unresolved uncertainty does.

### Gate 2 - Paper instantiation

Before code, require two positive instances, two meaningful negatives, one
lifecycle trace, and a producer -> authority -> consumer -> failure map. If
these distinguish the alternatives, stop at paper evidence. If they expose a
missing production substrate, route that substrate as a separate patch or
decision before domain prototyping.

### Gate 3 - Evidence ladder

Authorize one level at a time:

1. static schema/content examples;
2. resolver or validator mutations;
3. throwaway evaluator;
4. persisted end-to-end integration.

Climb only when the decision cannot be made at the cheaper level. Do not demand
level 4 evidence for every citizen shape in the same charter.

### Gate 4 - Fixed economic budget

Every charter declares before dispatch:

- maximum builder iterations: two, including one rival;
- maximum repair pass: one, owner-authorized only;
- committee: two reviewers by default;
- third specialist reviewer only for a named uncertainty;
- context-starved legibility only when recoverability is itself a decision;
- maximum artifact/check growth and a model/token budget when the platform
  exposes one; and
- an owner checkpoint when prototype cost reaches 25% of the estimated
  implementation milestone.

Crossing the budget forces stop-and-decide, not automatic charter expansion.

### Gate 5 - Review triage

Every finding is classified before another iteration:

- `decision-blocking`;
- `production-condition`;
- `separate-decision`;
- `deferred-breadth`; or
- `non-blocking defect`.

Only decision-blocking findings may amend the active prototype charter. Separate
decisions receive their own eligibility score; production conditions go into
the milestone plan.

### Gate 6 - Partial ratification

An evaluation analysis may accept a coherent subset and explicitly defer the
rest. Do not keep a large prototype open until every adjacent integration
boundary is solved. ADR scope must match the evidence actually converged upon.

### Gate 7 - Production adoption

Prototype implementations never become production candidates by effort or
similarity. Accepted contracts are reimplemented on the milestone branch.
Prototype code may be cited and selectively translated only after each piece is
mapped to an accepted ADR statement and a production test.

## Recommended Disposition

1. Close the broad prototype process after round 4; do not build it5.
2. Write an evaluation analysis for the converged narrow conclusions only.
3. Draft a small Tier 2 ADR for those conclusions, or split identity/closure
   from form-field/rendering if the ADR becomes compound.
4. Return unresolved package, projection, coverage, explanation, and citation
   authority questions to separately scored decisions or production conditions.
5. Amend `PROJECT_PLANNING.md` only after owner ratification of the economic
   gates above.
6. Re-scope First Tax Slice Track 0 so it cannot consume implementation Tracks
   1-5 again.

The correct optimization is not less rigor. It is paying for the cheapest
evidence capable of changing the decision, then stopping.
