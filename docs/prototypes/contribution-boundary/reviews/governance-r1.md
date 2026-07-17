# Governance Review — R1 (D2 Contribution Boundary)

Seat: Governance reviewer (Medium). Date: 2026-07-16. Mandate: conformance, not preference. Both builds judged against committed contracts: Constitution Arts. 1/7/9/10/12/14, Ontology §0/§8, ADR-0010/0017/0023/0031, and the committed kernel/derivation schemas. All examples synthetic. Findings per measure marked **decision-blocking** or **not-blocking**, then per-build verdicts.

## Measure 1 — Contribution as a declared citizen (Art. 10, Art. 9)
- Both declare all new nouns before instances and edit no committed schema version — finding.v2 is a new version, finding.v1 stays published. Schema-as-canon holds for both. **not-blocking.**
- **it2** models `contribution.v1` as a distinct *thing*-citizen carried by `act-contribution.v1`, exactly parallel to `evidence.v1` / `act-evidence-submitted.v1`, and registers three Ontology nouns (thing/act/record). Faithful to Ontology §0's citizen/act/record kinds. **it1** (§2.1) conflates the contribution citizen *with* its act envelope. Awkward against Ontology's thing/act split but still declared before instances. **not-blocking** for it1; it2 conforms better.
- **it2 declaration gap (named).** it2 routes finding.v2 (with `contribution_id`) through the *existing* `member-transition`/`assertion` acts, but committed `act-member-transition.v1` and `act-assertion.v1` const-pin `member.finding.schema == "finding.v1"`. A finding.v2 cannot ride those carriers, and it2 declares no successor carrier act schema — an Art. 10 / Art. 9 incompleteness. Additive, mechanical, decision-surface intact → **not-blocking**, but it2 must name `act-member-transition.v2` / `act-assertion.v2` before the ADR. **it1** avoids this by self-declaring `member_transitions[]`/`assertions[]` carrying finding.v2 inside `act-contribution.v1`, at the cost of the composite-container shape (E10.1 re-nesting concern, declared as a specialized non-generic act, **not-blocking**).

## Measure 2 — Provenance linkage (the divergence)
- **Governing clause caveat.** Art. 12 literally governs *derived*-finding lineage. The contribution pin rides an *asserted* (human) finding, so the controlling contracts are Art. 1 (evidence is provenance, standing-only) and Art. 15 (explanation), with Art. 12's pin-immutability/exact-version applied by analogy. Stated because no committed clause imposes Art. 12's pin-shape on a human finding.
- **it1** *replaces* committed `finding.evidence_ids` with a bespoke `provenance.documents` pin-set — discards the committed Art. 1 documentary channel and reconstructs it, enlarging blast radius (read-models/currency consumers of `evidence_ids`). Pins are immutable/exact-version but the schema-version subfield is vestigial.
- **it2** *retains* `evidence_ids`, adds optional `contribution_id`, and enforces at admission that the contribution's `evidence_id` is a member of the finding's `evidence_ids`. "Version" of the source document is the immutable evidence id (replacement mints a successor id).
- **Conformance condition:** (a) pin an immutable exact-version evidence reference; (b) retain `evidence_ids` as the Art. 1 channel; (c) enforce contribution↔evidence consistency at admission. **it2 meets (a)(b)(c); it1 meets (a) only.** it1's `evidence_ids` removal is a divergence, not an Art. 9/10 violation. **not-blocking** for both; **it2 strictly better-conforms** — the genuine committee signal on the divergence.

## Measure 3 — Provenance is not a standing edge (Art. 7, ADR-0010/0017)
- Both keep the contribution/document pin out of `finding.pins.finding_ids` (the only field ADR-0010 D4 extracts as a derivation edge). A contribution has no `fact_id` and no supersession, so it can never be a correction or individuation root. No third edge originates at a pin. Two-edge doctrine preserved. **not-blocking** for both.

## Measure 4 — Correction by supersession (Art. 7, ADR-0023)
- Both route a value correction through ordinary `assertion`. Family horizon does **not** advance (ADR-0017 D4, ADR-0023 D2), closure authority survives, both findings remain on record, no edit / withdrawal / third mechanism. it1's admission canon rejects a family-member `assertion` unless that fact is already current (ADR-0023 SC-R1); it2 relies on committed routing and probed SC-R1/SC-R2. **not-blocking** for both.

## Measure 5 — Runs consume facts, not inputs (Art. 13/14)
- The run request/context carries no value-bearing member in either build. it1 adds a closed `run-request.v1` (`additionalProperties:false`); it2 leans on the committed `RunContext` shape + an E14.2 extension excluding the contribution kind as a rule dependency. A missing current finding blocks `DEPENDENCY_ABSENT`, recorded, never silent. **Both name the same residual:** the committed synthetic-fixture adapter / hand-assembled `InputFinding` can inject an unprojected value (it1 Case 6 published `777`), deferred to production as an explicit condition, not an accepted exception. **not-blocking** at Rung 2, contingent on that named production condition.

## Measure 6 — D1 interlock (Case 5, ADR-0031)
- Both confine contribution writes to residency `L`, repo read-only. **it2** is explicit: every contribution artifact has personal provenance → `NEVER_CROSSES` per ADR-0031 Decisions 2/7 (sensitivity by description). **it1** requires the `L` write capability and returns no descriptive artifact across the boundary — adequate but less explicit that the contribution *record* inherits `NEVER_CROSSES` by description. **not-blocking** for both; it1 should make that explicit (noted).

## Verdicts (Rung 2)
- **Incumbent (it1): D2-P1 conformant, D2-P2 conformant — no decision-blocking gap.** Non-blocking divergences: `evidence_ids` removal weakens the Art. 1 channel (M2); composite batch-carrying act shape (M1); Decision-7 by-description explicitness (M6).
- **Rival (it2): D2-P1 conformant, D2-P2 conformant — no decision-blocking gap**, with one named Art. 10 gap to close before the ADR: successor carrier act schemas (`act-member-transition.v2` / `act-assertion.v2`) admitting finding.v2 (M1). Stronger on M2 and M6.
- **On the central divergence (M2):** both hold the two-edge doctrine (M3); neither has a decision-blocking defect; on conformance grounds the **rival provenance basis is preferable** (retained Art. 1 evidence channel + enforced contribution↔evidence consistency + evidence-id-as-version), subject to closing its carrier-schema declaration gap.

No repo changes made; read-only. The one authority-by-analogy (Art. 12 onto a human finding's provenance) is flagged in M2.
