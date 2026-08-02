# Round 2 Governance Review — Source-Family Semantics

Date: 2026-07-12. Reviewer tier: Medium/medium. Evidence reviewed: `round-2.md`,
the governance-review charter, both paper rivals (`it1` and `it2`), repair 1's
design and examination, round-1 triage, the governance set, and ADR-0010,
ADR-0011, ADR-0014, and ADR-0015. No code, resolver, schema, or production
contract was tested. This review does not read or rely on a same-round peer
review.

## Declared measurements

The measurement is the required chain, separately for each paper design:
claim → member universe → mapping → calculation → coverage. A result passes
only if the chain stays within one declared universe, closure is affirmative
and determinable, evidence does not become identity, and no narrow family gains
undeclared broader tax authority.

### Incumbent paper (`it1`)

| Link | Measurement | Result |
|---|---|---|
| Claim | The declaration says every 2025 Form 1099-INT box-1 taxable-interest statement item for the taxpayer is accounted for, not all interest. | Pass. The proposed claim is narrow and coextensive with the stated family. `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/it1/design.md:7-25` |
| Member universe | Current findings are keyed to logical 1099-INT statement instances and box 1; two statements from one payer remain two members; evidence/file ids are excluded. | Pass. This follows ADR-0015 and preserves peerage. `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/it1/design.md:20-25`; `docs/adr/0015-1099-int-statement-instance-identity.md:17-27`; Constitution Article 1, `docs/governance/constitution.md:14-16` |
| Mapping | The adopted mapping names this family/scope, its member facts, and exactly one current literal-true closure finding. | Pass. It matches ADR-0014's independently versioned mapping and affirmative-only admission. `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/it1/design.md:12-19`; `docs/adr/0014-adopted-source-closure-mapping.md:13-21` |
| Calculation | The consumer is a box-1 subtotal and may publish an empty zero only through that narrow closure. | Pass. It does not turn the subtotal into line 2b. `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/it1/design.md:27-43` |
| Coverage | Coverage reports completion of box-1 statement items, never “all taxable interest.” | Pass, provided the exact declared claim remains the coverage subject. `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/it1/design.md:12-19,27-43` |

The incumbent's cases preserve the result: non-form interest and box-3 interest
are counterexamples to the broader claim, while a two-statement same-payer
case remains two members. `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/it1/design.md:45-84`
The late-member lifecycle still assumes a later withdrawal act, so it is not a
complete P3 mechanism. `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/it1/design.md:86-99`

### Clean-room paper (`it2`)

| Link | Measurement | Result |
|---|---|---|
| Claim | `C(B1)` is the affirmative claim that every member of the named 2025 box-1 statement-item family is accounted for. | Pass. The claim is not “all interest” or “line 2b.” `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/it2/design.md:5-20` |
| Member universe | One member per box-1 item on a logical source instance; evidence supports a finding but is not the fact identity. | Pass. The design explicitly keeps evidence and source-instance/fact identity separate. `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/it2/design.md:21-45`; ADR-0011, `docs/adr/0011-tax-fact-identity-and-source-closure.md:24-37`; ADR-0015, `docs/adr/0015-1099-int-statement-instance-identity.md:17-27` |
| Mapping | `M(B1)` consumes B1 item findings and uses `C(B1)` only for the B1 subtotal zero. | Pass. The mapping is not a caller-supplied broader closed set. `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/it2/design.md:82-110`; ADR-0014, `docs/adr/0014-adopted-source-closure-mapping.md:17-21` |
| Calculation | `S(B1)` is explicitly a subtotal; line 2b requires a declared taxable-interest input and may use B1 only as an explicit component. | Pass. Narrow-as-final substitution is rejected. `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/it2/design.md:62-80,89-110` |
| Coverage | `K(B1)` reports B1 claim/member completeness and does not report TI or L2B coverage. | Pass. The chain retains the exact narrow subject. `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/it2/design.md:89-110` |

Its six cases independently establish the same two negatives that matter here:
non-form interest and box 3 cannot be erased by a B1 closure; same-payer
statements cannot be collapsed; and narrow-closed/broad-open remains an honest
blocked final result. `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/it2/design.md:112-130`
The lifecycle correctly identifies the old zero as needing displacement, but
its step 4 still requires a later act withdrawing or superseding closure.
`docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/it2/design.md:132-151`

## SFS-P1 — convergence and disposition

**Measurement:** whether versioned claim plus canonical predicate is actual
semantic authority, rather than an id, title, label, rule symbol, or coverage
rollup.

Repair 1 closes the shared mislabel gap. Its `B1-2025` declaration gives the
exact claim, canonical current-member predicate, mapping subject, subtotal
subject, and coverage subject; the opaque id only locates that declaration.
`docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/repair1/design.md:7-27` A misleading
family id/title must therefore render the exact box-1 claim, while authoring an
“all taxable interest” claim over a box-1-only predicate must fail.
`docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/repair1/design.md:27-32`

This is genuine convergence with both rivals, not wording convergence. It
implements the governance direction that schemas/artifacts declare meaning and
consumers do not carry private meaning (Constitution Articles 9–11,
`docs/governance/constitution.md:44-48`; Engineering Constraint E10.1,
`docs/governance/engineering-constraints.md:48-52`). It also respects
ADR-0011's affirmative-only closure and ADR-0014's exact mapping/closure
admission. `docs/adr/0011-tax-fact-identity-and-source-closure.md:38-51`;
`docs/adr/0014-adopted-source-closure-mapping.md:13-21`

Coverage cannot broaden the authority when it is bound to the same exact claim
and predicate. Repair 1 expressly forbids an alias from being the asserted
claim or coverage-complete conclusion. `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/repair1/design.md:21-27`
The result is therefore:

**SFS-P1: settled at paper level, with production validation as a condition.**
The semantic authority is the versioned declaration's exact claim plus
canonical predicate. Consumer names and shortened coverage labels cannot
broaden it. Schema/authoring validation, exact claim presentation or reference,
and coverage-subject checks remain production work; they are not unresolved
paper semantics.

## SFS-P2 — convergence and disposition

**Measurement:** whether a narrow B1 subtotal can be wired as a broader final
taxable-interest result, including a zero, without an explicit composition.

The repair distinguishes the B1 family subtotal from the Form 1040 line-2b
final result. A final result must declare its required input universe and either
consume an exactly matching subtotal or consume an explicit composition whose
component predicates are proven coextensive. A validator rejects omitted/extra
predicates and label- or symbol-based substitution. `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/repair1/design.md:34-52`

That rule is supported by both rivals' cases: non-form interest and box-3
amounts disprove B1/TI coextensiveness, and a closed B1 subtotal may not occupy
the line-2b universe slot. `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/it1/design.md:27-43,55-84`;
`docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/it2/design.md:62-80,112-130` The repair's
case table preserves the distinction: B1 can be fresh and closed while the
broader final universe remains open. `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/repair1/design.md:110-123`

This is compatible with Article 12's requirement that derived findings pin the
exact findings and artifacts that produced them, and with Article 11's rule
legibility requirement. `docs/governance/constitution.md:60-64` The repair does
not pretend to define the full taxable-interest taxonomy; it only settles the
bounded B1/line-2b relationship, as the plan permits. `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/plan.md:14-20,88-106`

**SFS-P2: settled at paper level, bounded to B1 versus line 2b.** Explicit
composition blocks narrow-subtotal substitution. Full taxable-interest
membership and any future composition remain separate decisions; their absence
does not leave the tested convergence question open.

## SFS-P3 — frontier/horizon boundary

**Measurement:** whether the proposed late-member frontier/horizon can make the
old closure-backed zero noncurrent under existing governance, without manual
withdrawal or invented machinery.

The static state table correctly specifies the observable truth: empty-family
closure → current B1 zero → later relevant member → stale closure,
noncurrent zero, and open coverage → new affirmative closure and explicit
rerun. It also correctly distinguishes a member correction from a new member
and prevents member removal/opening from resurrecting the old zero.
`docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/repair1/design.md:56-90`

ADR-0010 is sufficient for a correction of a known pinned member: its
derivation-edge cascade can displace a present-member subtotal, and a
superseded closure finding can displace a derived result that pins that closure.
`docs/adr/0010-derived-finding-projection-and-currency.md:35-50` It is not
sufficient for the critical late-member transition. The empty zero pins the
closure and mapping, not a member that did not yet exist; the repair says so
explicitly. `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/repair1/design.md:91-106`

The proposed smallest mechanism is not already authorized as an implementation
detail. It needs a record-derived membership frontier/horizon whose succession
reaches closure authority and every zero that used it. That reaches the
reserved T1 boundary if the frontier is a derived freshness citizen or if a
derived finding is made to carry the authority that invalidates the closure:
the Ontology defines derived findings but reserves their fuller authority
construction, and specifically lists T1 as open work. `docs/governance/ontology.md:94-107,218-225`;
ADR-0009, `docs/adr/0009-derived-finding-shape.md:20-53,93-103`

There is also a separate Article 7 problem even if the design avoids T1. The
Constitution permits displacement only through declared derivation or
individuation edges and says “no third edge”; currency must be derived from the
record, not stored. `docs/governance/constitution.md:25-27` The same rule is
made operational by E7.1 and E7.2. `docs/governance/engineering-constraints.md:38-40`
The repair deliberately does not say whether the frontier is a new citizen, a
new declared individuation relation, or another conforming mechanism.
`docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/repair1/design.md:100-106` That is an
unresolved governance/architecture choice, not a settled paper contract.

Accordingly, P3's *required semantic outcome* is clear, but its *authority and
currency machinery* is not converged or authorized:

**SFS-P3: unresolved; escalate before production contract work.** Accept the
observable requirement that a relevant later member makes the old closure and
closure-backed zero noncurrent, with no resurrection and with explicit rerun.
Do not accept the frontier/horizon as an implementation-ready mechanism. A
choice that gives derived freshness state authority must surface a Tier-3 T1
resolution; a choice using a new standing-affecting relation/edge must resolve
the Article 7 “no third edge” boundary and be recorded at the appropriate
architectural tier. Neither may be smuggled in as ordinary SFS-P3 wording.

## Final disposition

- **SFS-P1:** settled at paper. Versioned exact claim + canonical predicate
  carry the family meaning; coverage and names cannot broaden it.
- **SFS-P2:** settled at paper for the bounded B1/subtotal versus line-2b
  question. Explicit composition is required; the full TI taxonomy is deferred.
- **SFS-P3:** semantic failure mode and required state are established, but the
  late-member invalidation machinery crosses the reserved/architectural
  boundary and remains unresolved. Existing ADR-0010 edges alone cannot reach
  a previously unknown member's old zero.

No implementation, resolver, schema, UI, persistence, or production rule
proposal is made here.
