# Prototype Evaluation Analysis - Narrow Tax Citizen Families

Foreman, 2026-07-11. This is the prototype evaluation analysis required by
ADR-0005 for the bounded conclusions below. Every conclusion cites a followable
exhibit or review. Conclusions outside this document are not supported for ADR
ratification by this analysis.

Status: complete for owner disposition and narrow ADR drafting. This analysis
does not claim that the full it4 corpus or the broad tax citizen-family contract
is ratification-ready.

## 1. Decision Under Evidence

This analysis answers five propositions only:

1. whether existing kernel `fact-type.v1` is sufficient for the exercised core
   tax facts, without a specialized tax-fact-type schema;
2. how a W-2 wage fact is individuated relative to evidence and corrected;
3. the nature and assertion shape of source-set closure facts;
4. whether an official form field is a first-class content citizen distinct
   from a derivation output symbol; and
5. which rendered-absence dispositions that form-field content must distinguish.

It does not decide package/adopted-content closure, `closed_sets`, condition
projection for standard-deduction eligibility or tax method, coverage-family
identity, non-publication explanation traversal, citation resolver authority,
or production artifact ids and versions.

## 2. Evidence Base

| Exhibit | Contribution |
|---|---|
| `exhibits/tax-citizen-families/it1` at `88f0139` | First design: specialized `tax-fact-type.v1`, first-class form fields, explicit rendered-absence states, W-2 peerage pressure |
| `exhibits/tax-citizen-families/it2` at `989d9fe` | Clean-room rival: existing kernel `fact-type.v1`, concrete form-field citizens across the slice, determinable content exercised by two runners |
| `exhibits/tax-citizen-families/it3` at `be72d63` | Targeted repair: W-2 slip key, determinable/attested closure, line-1z boundary, committed form-field examples |
| `exhibits/tax-citizen-families/it4` at `9debc4d` | Persisted integration evidence: W-2 same-fact correction, derived displacement, re-derivation, adopted symbol projections, explicit machinery escalation |
| `reviews/round-1*` through `reviews/round-4*` | Four independent review instruments per round, including fresh-reader legibility and successful/failed attacks |
| `process-log.md` | Round dispositions, conformance verdicts, incidents, and broad-loop close |
| `process-retrospective.md` | Cost analysis and reason for narrowing the decision rather than extending the prototype |

ADR-0005's rival requirement is satisfied. It1 and it2 were genuinely different
designs built under separate builder contexts against the same original fixture
charter. It3 and it4 are repair/integration evidence, not additional rivals.

## 3. Supported Conclusions

### C1 - Reuse kernel `fact-type.v1` for the exercised core tax facts

The exercised W-2 wage, interest-by-box, filing-status, rounding, itemization,
and true-only source-set-closure questions fit the existing kernel fact-type
contract: declared identity keys, determinable/elective nature, value schema,
and supersession policy.

Evidence:

- The clean-room rival uses the unchanged kernel family in
  `it2/content/bundle.tax-2025.json`; its harness validates the full bundle
  against published kernel schemas (`examination-it2.md`, Q1/Q4 and reproduced
  round-2 expressiveness results).
- It3 repeats that result after adding W-2 slip identity and correcting closure
  nature (`it3/content/bundle.tax-2025.json`; `examination-it3.md`, R1/R2).
- It4 materializes those fact types through real bundle-adoption and assertion
  acts and kernel projection (`examination-it4.md`, I1; round-4 governance I1,
  mechanical-path evidence).
- No review identifies a missing kernel fact-type field for these bounded facts.
  Later failures concern companion relationships, projections, and adopted
  content, not the kernel fact-type schema itself.

This rejects it1's specialized `tax-fact-type.v1` as a required replacement or
subtype for the bounded facts. Tax meaning remains in ordinary fact-type content
and companion citizens. This conclusion does not include it4's aggregate scalar
eligibility or tax-method facts; every round-4 unstarved reviewer disputed that
rewrite.

### C2 - W-2 wage fact identity keys on the W-2 slip as a thing, never evidence

A W-2 wage fact is individuated by employee/workspace context, employer, tax
year, and a W-2-slip citizen. The slip citizen is peer to submitted evidence.
Two slips from the same employer and year are distinct facts; replacing or
removing evidence does not change fact identity.

Evidence:

- It1's negative document-child example rejects evidence-owned fact identity:
  `it1/examples/negative/tax-fact-type.document-child-identity.json`.
- It3 adds `w2-instance` to the fact identity and exercises two same-employer,
  same-year slips (`it3/content/bundle.tax-2025.json` and
  `it3/fixtures/scenarios.json`, `two_w2_same_employer`; examination R1).
- Round-3 legibility independently recovers the two control-number-distinct
  slip identities while noting that correction was not yet demonstrated.
- It4 closes that mechanical gap through the real act log: a later finding for
  the same fact displaces the original finding and dependent line 1a; the
  second slip remains current; re-derivation publishes the corrected total
  (`it4/tools/harness.py`, I3; `it4/instances/positive/finding.w2-correction.json`;
  round-4 governance I3; round-4 expressiveness I3).
- The round-4 adversary's same-fact correction/cascade attack fails. Its separate
  documentary-provenance attack succeeds and is retained below as an exclusion.

This supports the identity and mechanical correction contract. It does not
settle W-2c evidence replacement, previously-reported/corrected-value capture,
or documentary provenance for a legal correction workflow.

### C3 - Source-set closure is a one-sided determinable, attested fact

The question is whether the user has completed the named source family for the
scope, a condition the world/user record determines rather than a tax election.
Authority enters through an attested asserted finding. A current true finding
means closed; open or not-yet-closed is represented by absence of a current
closure finding, not by an asserted authoritative `false` closure.

Evidence:

- It2's elective closure shape drew governance/adversary dissent in round 2.
- The it3 mini-spike compares elective-fact reuse, a new family, and a projection
  contract, then adopts ordinary `fact-type.v1` with `nature=determinable` and
  `basis=attested` (`it3/spikes/closure-semantics.md`;
  `it3/instances/positive/finding.closure-attested.json`; examination R2).
- Round-3 governance treats the semantic choice as materially stronger than it2
  and sufficient conditional on the projection boundary.
- It4 asserts the closure through the kernel and publishes a pinned symbol
  projection from the attested finding (`examination-it4.md`, I1/I2; round-4
  governance I1/I2 reproduced evidence).
- Round-4 expressiveness demonstrates why asserted false must not carry closure:
  the adapter can place a false closure fact into `closed_sets` and report the
  family closed. This is negative evidence for one-sided true-only assertion,
  not support for a boolean false state.

This conclusion settles fact nature, basis, and one-sided assertion shape only.
The source-family mapping, empty-collect authority, `closed_sets`, adoption, and
pinning remain unresolved.

### C4 - An official form field is a first-class content citizen

A form field is not identical to the derivation symbol whose value it displays.
It has stable content identity and version, authority/form/year/jurisdiction and
line locator, a declared binding to an output symbol, source citation reference,
and rendering/explanation instructions. Publication is immutable by version;
later form-year or meaning changes produce a new content citizen/version.

Evidence:

- Both rivals independently introduce a `form-field.v1` companion family:
  `it1/schemas/form-field.v1.schema.json` and
  `it2/schemas/form-field.v1.schema.json`.
- It1's positive line-2b instance and bare-line-11 negative pressure identity and
  required rendering states (`it1/examples/positive/form-field.form1040.line2b.json`;
  `it1/examples/negative/form-field.bare-line11.json`).
- It2 instantiates all included 2025 lines in
  `it2/content/form-fields.2025.json`; round-2 legibility recovers form/line,
  version, bound symbol, citation, and rendering behavior with certainty.
- It3 adds strict version/property negatives and a line-1z positive
  (`it3/instances/positive/form-field.line1z.json` and form-field negatives),
  and tests cross-year symbol mismatch.
- Across rounds, reviewers distinguish form fields from output symbols even
  when package/provenance enforcement remains disputed.

This supports the citizen-family concept and minimum meaning. It does not adopt
the prototype schema bytes, stale `it2`/`it3` `$id` values, package membership,
or the citation resolver contract.

### C5 - Form-field content distinguishes five output dispositions

For a requested form field, content must distinguish:

1. a published nonzero value;
2. a published numeric zero grounded in present source findings;
3. a published closure-backed zero grounded in a true closure finding;
4. blocked/unavailable because required state is absent or invalid; and
5. non-existence because a declared guard is false/inapplicable.

The display may group some blocked states visually, but their explanation and
machine disposition remain distinct. Blank/non-existence must not masquerade as
zero; zero must not imply source absence.

Evidence:

- It1 makes rendered-absence states explicit in
  `it1/scenarios/synthetic-slice.json` and the form-field positive example.
- It2 carries per-field rendering instructions for computed zero,
  closure-backed zero, blocked-unclosed, blocked-invalid, and guard absence in
  `it2/content/form-fields.2025.json`; round-2 legibility calls the distinction
  unusually recoverable.
- It3 fixtures separately exercise present zero, closure zero, no source/no
  closure, invalid source, and false guard; round-3 legibility recovers the
  intended distinctions without harness knowledge.
- It4's persisted path strongly supports the two published-zero pin distinctions
  (`examination-it4.md`, I6; round-4 governance/expressiveness I6), while all
  three unstarved round-4 reviewers correctly reject the claim that every
  non-publication state already has an end-to-end explanation walk.

This conclusion adopts the disposition vocabulary and rendering honesty rule.
It does not claim that the current explanation API closes all five walks.

## 4. Alternatives Rejected

### Specialized tax fact-type schema for the bounded facts

It1's `tax-fact-type.v1` made useful domain pressure visible, but the rival and
later integration show no required kernel-field difference. Companion citizens
carry form, citation, binding, and rendering meaning without duplicating the
kernel fact-type contract.

### Document-owned W-2 facts

Rejected by Article 1 peerage, it1's negative example, the two-slip collision
pressure, and it4's same-fact correction evidence. Evidence may change while the
question remains the same.

### Bare output symbols as form fields

Rejected because symbols do not carry official-form identity, independent
versioning, citation, or rendering dispositions. Both rivals independently
introduced a companion form-field citizen.

### Elective closure

Rejected because closure reports completeness; it does not constitute a tax-law
choice. Round-2 dissent and the it3 closure mini-spike resolve this distinction.

### Asserted false closure

Rejected because it creates a standing answer that can be mistaken for closed
membership and complicates the meaning of open. Round-4 false-closure mutation
demonstrates the failure. Closure is a one-sided true assertion; absence means
open/not established.

### One undifferentiated blank/zero state

Rejected because it would make incomplete, inapplicable, invalid, present-zero,
and closure-zero states observationally equivalent. Every iteration and all
fresh-reader reviews found the distinctions meaningful.

## 5. Explicit Exclusions And Future Decisions

The following are not ratification conditions silently delegated to
implementation; they are outside this analysis and require separately scoped
decisions or evidence before adoption:

1. the closure-fact-to-source-family relationship and native empty-collect
   authority (`closed_sets`);
2. whether standard-deduction eligibility and tax method are aggregate facts,
   structured facts, or derivations over component condition facts;
3. the adopted manifest that closes over fact types, rules, parameters, symbol
   bindings, form fields, citations, attachments, and resolver contracts;
4. coverage-family identity and record-derived coverage semantics;
5. a normal explanation entry point for blocked, invalid, and inapplicable
   output dispositions;
6. citation attachment semantic authority, resolver schema, adoption, and pins;
7. package adoption version/content integrity and publication/record crash
   ordering;
8. W-2c documentary correction provenance; and
9. 1099-INT source-instance identity beyond payer/year/box.

No ADR citing this analysis may imply those questions are settled.

## 6. Production Ratification Conditions For The Supported Scope

These conditions implement the five conclusions without expanding them:

- publish production schemas/examples with canonical ids and versions; do not
  copy prototype `$id` values;
- instantiate every new schema with hand-written positive and isolated negative
  examples before runner consumption;
- preserve W-2 peer identity and same-fact correction/displacement as golden
  contract fixtures;
- define closure value schema so only a true assertion can become a current
  closure finding; false/missing remains open;
- keep form-field identity separate from output-symbol identity and reject
  cross-year or wrong-line bindings;
- preserve the five disposition kinds in form-field content and runner records,
  without claiming explanation traversal that does not yet exist;
- pin the complete ratified governance set with its actual v0.1 identities; and
- reimplement accepted contracts on the milestone branch rather than merging
  prototype code.

## 7. Dissent Record

The committee unanimously rejects ratifying the full it4 corpus. This analysis
honors that dissent by narrowing the decision.

- Round-4 governance closes W-2 correction (I3), accepts the mechanical
  authoritative path, and says the closure fact shape may proceed as evidence;
  it disputes scalar conditions, `closed_sets`, package closure, coverage,
  explanation, and citation authority.
- Round-4 expressiveness closes I1/I3 but disputes or fails I2/I4-I9; its
  false-closure probe supplies a boundary condition adopted in C3.
- Round-4 adversary's same-fact correction attack fails, while documentary
  provenance succeeds; C2 is limited accordingly.
- Round-4 legibility recovers form-field identity, rule/output distinction,
  closure intent, and absence vocabulary, while declining to infer unseen
  execution and identifying stale prototype schema ids.

No reviewer position is converted into consent for the excluded decisions.
The context-starved reviewer is not asked to sign this synthesis because doing
so would invalidate its instrument.

## 8. Sufficiency And ADR Scope

The evidence is sufficient to draft a narrow Tier 2 ADR for C1-C5, provided the
ADR repeats the exclusions and production conditions above. If the ADR cannot
state the five conclusions without importing an excluded relationship, split
it into:

- fact identity/nature (`fact-type.v1`, W-2 slip identity, closure assertion);
  and
- presentation content (form-field citizenship and disposition vocabulary).

The evidence is not sufficient for an ADR adopting any prototype implementation
or the full tax citizen-family corpus. Owner ratification of an ADR remains a
separate step.
