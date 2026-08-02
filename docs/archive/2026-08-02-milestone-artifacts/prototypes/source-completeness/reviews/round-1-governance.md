# Round 1 Review — Governance Fidelity

Date: 2026-07-12. Seat: governance-fidelity. Evidence rung: 1 (paper).

Authority used: governance set v0.1; ADR-0011; ADR-0012; approved plan,
iteration charters, round file, and the named it1/it2 exhibits. Production was
inspected only at the cited `collect`, `RunContext`, and pin-building seams.

## Measurements

### Check 1 — ADR-0011 decision 5: current true only

- **it1 — PASS (paper).** Result: admission is `IFF` a finding exists, is
  current, and its value is exact boolean `true`; false, absent, and displaced
  cases all withhold membership and block at Layer 2. Exhibit:
  `it1/sc-p1-mapping-design.md` lines 80–93, 126–137, 141–151.
- **it2 — PASS (paper).** Result: the projection requires one matching fact, a
  current finding, and value equal to literal `true`; false, absent, ambiguous,
  and displaced cases block. Exhibit: `it2/design.md` lines 57–71, 121–139.
- Measurement limit: neither paper exhibit proves the production adapter is
  value-sensitive. Both examinations disclose that Gate 3 execution question.

### Check 2 — no caller-supplied closed membership

- **it1 — PASS as proposed contract; production condition remains.** Result:
  the resolver over adopted mapping plus current findings replaces caller
  `closed_sets` and is the sole membership writer. Exhibit:
  `it1/sc-p1-mapping-design.md` lines 67–91, 153–168. Production inspection
  confirms the old seam still exists at `runner.py` lines 63–72, 134–140 and
  `runners/derive.py` line 31; the exhibit does not cite it as approved.
- **it2 — PASS as proposed contract.** Result: callers cannot supply or augment
  membership; an injection is rejected/ignored. Exhibit: `it2/design.md` lines
  57–71, 137–139. The same production seam remains an adoption condition.

### Check 3 — Article 1 identity and forced collision case

- **it1 — PASS.** Result: chosen key is payer citizen + account citizen + year,
  with evidence/document/statement excluded; two accounts of one payer produce
  distinct facts, while payer+year collides and a correction preserves the
  fact. Exhibit: `it1/sc-p2-identity-design.md` lines 8–30, 34–70.
- **it2 — PASS.** Result: chosen key uses a logical statement-instance citizen,
  explicitly peer to evidence; two same-payer account examples use distinct
  statement citizens, payer-only collides, and evidence-file identity is
  rejected. Exhibit: `it2/design.md` lines 169–236.

### Check 4 — Articles 9/10: schemas precede instances; shape negatives

- **it1 — FAIL.** Result: `source-closure-mapping.v1` is a new citizen family,
  but the exhibit gives only one candidate instance-shaped JSON block and prose
  fields; it provides no schema declaration and no schema-valid positive/
  isolated structural negatives. The new payer/account citizens are also used
  without declared schemas. Exhibit: `it1/sc-p1-mapping-design.md` lines 37–65;
  `it1/sc-p2-identity-design.md` lines 15–30. This is paper evidence, so no
  workspace instance has actually preceded a schema, but the candidate contract
  is not yet sufficient to demonstrate Articles 9/10.
- **it2 — FAIL.** Result: the embedded `closure_authority` changes the declared
  rule-artifact shape, and `form_1099_int_statement_instance` is a new citizen
  shape, but neither has a preceding schema declaration or structural positive/
  negative suite. Semantic outcome negatives do not test schema boundaries.
  Exhibit: `it2/design.md` lines 30–55, 169–185.

### Check 5 — Article 11: declared mapping, closure, citation meaning

- **it1 — PASS (paper).** Result: source-family ↔ closure-fact mapping and
  `current-true` admission live in the proposed adopted artifact; collect names
  the same declared family. The resolver applies those declarations and adds no
  rival tax meaning. Exhibit: `it1/sc-p1-mapping-design.md` lines 37–104;
  `it1/sc-p3-source-family.md` lines 8–23. No citation contract is introduced.
- **it2 — PASS (paper).** Result: each adopted collecting rule declares family,
  closure fact type, required identity, and admitted literal. Runner projection
  applies the parameter. Exhibit: `it2/design.md` lines 30–71, 157–167. External
  IRS references motivate SC-P2 but are not operative citation citizens.

### Check 6 — pins and empty-source-zero explanation

- **it1 — PASS as designed; production gap confirmed.** Result: the zero pins
  rule, mapping version, and exact closure finding and walks to its assertion
  act. Exhibit: `it1/sc-p1-mapping-design.md` lines 95–115. Production
  `pins_for` currently pins present collected findings only (`runner.py` lines
  143–160), matching the disclosed condition in `examination-it1.md` 45–50.
- **it2 — PASS as designed.** Result: the zero's explicit walk reaches the exact
  closure finding and assertion act, adopted rule/embedded parameter, adoption,
  and run. Exhibit: `it2/design.md` lines 73–99, 141–167.

### Check 7 — charter / Gate 2–3 scope

- **it1 — PASS, with observation.** Result: only static SC-P1/P2/P3 documents
  were produced; implementation details are candidate seams and rung climb is
  recommended, not performed. Exhibit: `examination-it1.md` lines 74–96. The
  coverage-read-model references in `it1/sc-p3-source-family.md` lines 18–25
  should remain non-operative context: implementing or deciding SC-D1 here
  would breach scope.
- **it2 — PASS.** Result: static SC-P1/P2/P3 only; no production substrate,
  rung climb, or SC-D1 contract is added. Exhibit: `examination-it2.md` lines
  46–78, 91–99.

## Observations (not measurements)

- The rivals make the intended lifecycle tradeoff legible: it1 independently
  versions/reuses a mapping citizen; it2 versions repeated mapping content with
  each collecting rule. Governance does not choose between those shapes once
  each is declared, adopted, pinned, and schema-bound.
- it2's statement-instance assertion boundary is a stated production condition,
  not an Article 1 failure on this evidence; its citizen is expressly logical,
  not documentary.

## Dissent and recommendation

**Explicit dissent:** neither design is governance-complete for ratification as
presented because both fail Check 4. I recommend retaining both as viable paper
rivals for SC-P1/P2 semantics, but requiring the eventual selected contract to
declare every new/extended citizen schema before production instances and add
meaningful schema-valid positives plus isolated structural negatives. This is a
recommendation only; Gate 5 classification and any next rung remain the
foreman's decision.
