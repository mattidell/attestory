# Governance review — taxable-interest composition, round 1

Date: 2026-07-14  
Role: Governance Reviewer (Medium tier)  
Scope: TIC-P1 and TIC-P2 in `it1/` and `it2/`, measured against the ratified
governance set and ADR-0016 decisions 3, 4, and 5; Article 7; ADR-0010; and
ADR-0017. This review is advisory.

## Independence and evidence boundary

I read the materials named by the Governance Reviewer charter, including both
designs and examinations, the committed derivation/kernel/source-completeness
surface, and the ratified ADRs. I did **not** read the excluded adversary
review or any draft or notes toward ADR-0026.

For the boundary measurement, the official 2025 Form 1040 instructions say to
enter total taxable interest on line 2b and expressly name Forms 1099-INT and
1099-OID; they also call out OID, market discount, and premium adjustments.
The Schedule B instructions likewise direct reporting all taxable interest,
including items reported on 1099-INT, 1099-OID, or substitute statements, and
exclude tax-exempt interest. [Form 1040 instructions](https://www.irs.gov/instructions/i1040gi)
and [Schedule B instructions](https://www.irs.gov/instructions/i1040sb).

## Findings

### TIC-G1 — `it1`: the stated line-2b composition is not coextensive

**Classification: decision-blocking.**

`it1` declares `U_2b^v1 = {B1, B3, non-form}` but expressly defers taxable
OID and related reported taxable-interest classes to later versioned-surface
growth. That is a candid account of the prototype's limited content surface,
but it is incompatible with its present claim to be the Form 1040 line-2b
composition: taxable OID is inside the official line's stated boundary and is
neither B1 nor B3 nor `non-form` as `it1` defines that residual.

ADR-0016 decision 4 permits a broader result only where the required universe
is identical or an explicit composition is *established as coextensive*. It
does not permit a rule to define a smaller required universe and thereby make
that universe coextensive with the official line. Decision 5 is directly on
point: closure-backed authority from a narrow family cannot be promoted to
line-2b authority. Calling the three-family union “complete under the
constituents I chose,” while binding the result to line 2b and its coverage,
is the same forbidden narrow promotion in composition form.

Versioning is necessary when the tax surface changes; it is not a qualifier on
the fixed meaning of a particular form line. `it1` may truthfully describe a
three-family, scoped interest rollup, but it cannot honestly publish or cover
that rollup as coextensive Form 1040 line 2b.

### TIC-G2 — `it1`: V5 defeats a proper-subset reference, but the binding is not yet complete

**Classification: production condition.**

For its declared three-family universe, V5 is a real narrow-substitution
defeat: a line rule that references only B1 cannot validate because every
constituent subtotal must be referenced. V6 prevents a collect-over-family
shortcut, V7 prevents an undeclared subtotal, and V8 requires all constituent
admissions before coverage can say the composition is closed. Thus this design
does not leave a B1/B3/NF reference-subset or coverage hole.

It does not yet establish a fully enforceable binding mechanism in the
committed contracts. The design leaves the package member role for the new
composition citizen “TBD” and describes a dedicated composition pin as
optional. The published package and derived-finding schemas admit only the
closed shared role vocabulary; neither contains `composition`, and the current
package validator only has explicit role agreement for rules and parameters.
Also, “references every constituent” is not a one-to-one check: it does not by
itself reject repeated references to one constituent. Those are implementation
conditions for a declared composition contract, not evidence that package
placement alone currently binds a line rule to its composition.

### TIC-G3 — `it2`: the four-slot boundary meets the line-2b test at the declared class level

**Classification: production condition.**

`it2` independently converges with `it1` on B1, B3, and a residual
unreported-taxable-interest class, excludes tax-exempt interest, and adds the
mandatory taxable-OID slot. That addition is required for an honest line-2b
claim. Its stated distinction between taxable OID and tax-exempt OID also
respects the line-2a/line-2b partition.

The boundary can be carried forward only with the stated condition: before
production can report this universe complete, it must declare the OID,
market-discount, and applicable premium/adjustment predicates and their
arithmetic as adopted content. The review does not treat a natural-language
slot label as completed production taxonomy. This is a condition on
implementation of the correct boundary, not a license to omit OID meanwhile.

### TIC-G4 — `it2`: slot bijection and mandatory closure are stronger, but the proposed pin role is unlicensed

**Classification: production condition.**

The rival's constituent-to-slot bijection is stronger than V5 for ADR-0016
decision 4: it rejects omission, duplication, substitution, and extras, and
requires the line rule's subtotal and closure lists to be the same bijection.
It therefore has neither a reference-subset hole nor a coverage hole, provided
coverage names the same universe as proposed. `require_closed(source_set)` is
generic in the relevant sense: its tax meaning comes from the declared source
set/mapping and it reuses the current-horizon, literal-true admission path.
It is not runner-resident line-2b meaning. As a new operation it must still be
schema-enumerated and have adopted, versioned operation semantics, as ADR-0006
requires.

The proposed required `composition:{id,version}` pin is not in the committed
closed pin-role vocabulary. ADR-0006 decision 9 requires one vocabulary across
artifact, package-member, and pin positions; ADR-0010 makes only `input` and
`choice` pins derivation edges, with the other admitted roles provenance only.
As written, a `composition` role is unlicensed. The design's separate proposal
to record the composition and universe as `package` pins is within the current
vocabulary, but it does not cure the stated new required role. Any eventual
composition provenance must be explicitly licensed by the shared schemas and
must remain non-edge provenance unless a ratified decision says otherwise.

### TIC-G5 — both designs: the lifecycle trace uses the two permitted edges

**Classification: non-blocking.**

Both designs converge on the essential lifecycle: a member transition advances
the affected family's horizon; the predecessor-horizon closure finding leaves
current state through individuation; and input pins displace the subtotal and
then line result through derivation. Neither proposes manual withdrawal,
stored staleness, a member-to-line edge, or a third standing-affecting edge.
Both also require a new true closure attestation and explicit rerun, so the old
zero cannot resurrect after removal.

`it2` makes the closure dependency explicit both through each empty subtotal
and directly at the line rule, which correctly keeps the line dependent on
each mandatory closure read. `it1`'s same mechanics are sound only for its
three-family scoped rollup; TIC-G1 prevents treating its resulting zero as an
honest line-2b zero when taxable OID is absent from the horizon/constituent
set.

## Verdicts

| Design | TIC-P1 — coextensive universe + declaration | TIC-P2 — honest zero + lifecycle |
| --- | --- | --- |
| `it1` | **Reject.** TIC-G1: a B1/B3/non-form universe omitting taxable OID cannot claim Form 1040 line-2b coextensiveness under ADR-0016 decision 4. TIC-G2 also remains a production condition. | **Conditionally accept** only as the lifecycle of the scoped three-family rollup. It is not acceptable as an honest line-2b zero unless TIC-G1 is resolved; then TIC-G2 remains a production condition. |
| `it2` | **Conditionally accept.** Conditions: satisfy TIC-G3's concrete adopted OID/adjustment taxonomy before any complete claim, and TIC-G4's licensed shared-vocabulary binding/operation requirements. | **Conditionally accept.** Conditions: the same TIC-G3 and TIC-G4 conditions; otherwise its mandatory all-slot closure and Article-7 lifecycle trace conform. |

## Carry-forward recommendation

Carry forward a hybrid: `it2`'s four-slot line-2b boundary, slot-bijection,
and mandatory per-slot closure/lifecycle; retain `it1`'s useful package-level
provenance direction only if ADR-0026 makes the composition binding mandatory
and licensed in the shared closed vocabulary, rather than optional.
