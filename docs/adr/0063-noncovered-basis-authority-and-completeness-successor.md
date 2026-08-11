# ADR 0063 — Broker-Furnished Noncovered Basis: Transaction Authority, Family Topology, Collision Generalization, and the Completeness Successor by Re-identification

- Status: **proposed** (drafted 2026-08-11; awaiting owner ratification)
- Tier: 2 — additive transaction-authority and completeness-successor contract
  for one breadth slice; reuses existing fact-type, family, supersession, and
  attachment substrate with no new schema kind, no new published schema
  version, and no new evaluator operator.
- Date: 2026-08-11

## Context

ADR-0061/ADR-0062 made **covered** Form 1099-B transactions computable: the
direct line-1a/8a route, and the code-W wash-sale route through Form 8949
boxes A/D to Schedule D lines 1b/8b. Both classes have basis **reported to the
IRS**. This milestone admits the adjacent class the 2025 Form 8949 puts in
boxes **B** and **E**: basis **shown to the recipient but not reported to the
IRS**, present on the statement and accepted as correct, with no adjustment
code and column (g) contractually zero.

Companion attachment, arithmetic, and Schedule D line-2/line-9 composition are
**ADR-0064**. This ADR settles authority, identity, family topology,
non-double-counting, and completeness.

Inspected commitments that force explicit decisions:

- **`source-family.v1` cannot value-filter.** Its `member_predicate` admits
  membership by bare `fact_type` id, so "the noncovered ones" cannot be a
  filtered view of the covered families. ADR-0061 Decision 1 (amended
  2026-08-05) already hit this and resolved it with a separate fact type plus
  an identity-key collision kill-test; this ADR inherits that resolution.
- **A fact-type id carries no version at the symbol boundary.**
  `packages/derivation/marshal.py` binds findings to symbols by fact-type **id**
  only (`_fact_type_id`, `_fact_id_has_type`), and `runner.py`'s completeness
  reads only `symbol`, `check`, and `equals` — never the `fact_type` version
  pin, which is carried but never matched (`runner.py:883–939`). Two versions
  of one id are **one symbol carrying one answer**. Zero fact-type ids appear
  at two versions across the 216 selected in
  `package.core-calculations.v29.json`.
- **The existing fifth boundary declaration is false for this class.**
  `tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments` v1's own
  committed title
  (`packages/content/tax/2025/schedule-d-boundary-form8949-w.bundle.json:11`)
  asserts "no Form 8949 adjustment codes other than W, no multi-code rows, and
  **no noncovered/basis-not-reported Form 8949 sources**". A return in this
  milestone's supported class makes it false, and its published text cannot be
  edited.
- **`attachment-rule` completeness can require only declared answers.**
  `packages/schemas/tax/attachment-rule.v4.schema.json:77–127` defines
  `required_answer` as a `oneOf` over presence and value checks keyed on a
  symbol; `branch_requirements[].adds_required` `$ref`s the same definition
  (lines 197–203). There is no family or closure predicate available to
  completeness.
- **`check: "value"` exists only at `attachment-rule.v4`.** The v5 and v6
  schema files contain no `"value"` const. `attachment.schedule-d.v5.json:264`
  is correctly on v4; `attachment.f8949.json` is on v6 and can carry only
  presence-checked answers. ADR-0062's context statement that v3–v6 are
  shape-identical is **inaccurate for v4** and is corrected here rather than by
  editing an accepted ADR.
- **The `derivation-record` block-code enum is closed at v6**
  (`packages/derivation/records.py:38–47`), and a new published schema version
  is an explicit milestone non-goal. The ADR-0061 Form 1098 precedent of adding
  an enum value (`F1098_SCOPE_CONTRADICTION`) is therefore **not** available.

Track 0's paper-first decision record settled these contracts against real
committed source and the 2025 Form 8949 / Schedule D instructions before this
ADR was drafted; it is distilled here and in the milestone plan
(`docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md`).

## Decision

1. **Two new transaction fact types, with the class constraint at the schema
   boundary.** Publish `tax.us.2025.f1099b.noncovered-st-txn` and
   `tax.us.2025.f1099b.noncovered-lt-txn` (`fact-type.v2`), each in its own
   bundle, mirroring `tax.us.2025.f1099b.covered-w-st-txn`
   (`packages/content/tax/2025/f1099b-covered-w-st.bundle.json`) **minus** the
   two box-1g fields, with two structural bindings:

   - `basis_reported_to_irs` narrowed to `"enum": ["no"]`. A statement whose
     basis *was* reported to the IRS cannot be asserted into this fact type at
     all.
   - `basis` **required** — as it already is on the mirrored covered fact
     types, so only the enum narrowing is novel here. A transaction with no
     basis cannot be asserted at all.

   Both are **schema-level refusals through the real validator**, not rule
   guards. A rule guard would admit the fact, then block a computation; a
   narrowed value schema means the false statement is never representable. The
   proposition admitted is exactly what box B/E means: *the broker furnished
   this basis on the recipient statement and did not report it to the IRS.*

2. **Authority scope is the single transaction.** The claim in Decision 1 is
   scoped to one transaction — broker, statement, transaction, tax-year — not
   to the return, the statement, or the tax year, even though its fact id
   carries a tax-year literal key. Storage identity is not authority scope. It
   is invalidated by supersession at the same identity and by nothing else; it
   is not a family-scoped or horizon-scoped claim. Transaction identity reuses
   the four ADR-0052 keys verbatim with **no document, file, upload, or
   evidence identity component** (ADR-0011/ADR-0052 precedent).

3. **Two new package-exclusive families with twin-scalar companions, and no
   adjustment companion.** Publish `tax.us.2025.f1099b.noncovered-st` /
   `noncovered-lt` whole-transaction families with their `source-closure`
   fact types, plus ADR-0054-style scalar companions
   `noncovered-*-txn.proceeds` / `.basis`, each its own family with its own
   closure and quantity. There is **no** `-adjustment` companion: column (g) is
   zero by contract for this class, and publishing an always-zero family would
   fabricate an authority nobody attests. Exclusivity from the covered and
   code-W families is **not structural** — `source-family.v1` cannot
   value-filter — so it is enforced by Decision 5.

4. **Correction versus member transition.** Correcting proceeds or basis at the
   same identity is ordinary ADR-0010 supersession and displaces, at minimum:
   that transaction's Form 8949 row, its box subtotal, Schedule D line 2 or 9,
   line 7 or 15, line 16, line 21, `selected-preferential-base`, and Form 1040
   line 7a/9, plus the family and scalar closures at the superseded horizon. A
   transaction that moves *between* families — a corrected statement now
   reporting basis to the IRS — is a **member transition**, not a correction:
   the noncovered fact is retracted and the covered fact asserted. Decision 5
   is what makes the half-done state fail closed rather than double-count.

5. **Generalized identity-key collision kill-test.**
   `_COVERED_W_IDENTITY_COLLISION_PAIRS` in
   `packages/derivation/package_validation.py` becomes **all fifteen unordered
   pairs across all six** transaction fact types — `covered-st-txn`,
   `covered-w-st-txn`, `noncovered-st-txn`, `covered-lt-txn`,
   `covered-w-lt-txn`, `noncovered-lt-txn` — in-term and cross-term, not the
   two pairs today and not merely the six in-term pairs this slice strictly
   needs. This is the owner's 2026-08-10 disposition and it closes a
   **pre-existing** gap: the same identity asserted as both short-term and
   long-term was never checked and would double-count the gain silently. The
   issue code generalizes from `COVERED_W_IDENTITY_KEY_COLLISION` to
   `F1099B_TRANSACTION_IDENTITY_COLLISION`.

   The run-path wiring must change with it.
   `_COVERED_W_IDENTITY_COLLISION_BOX_TYPES` (`runner.py:750–753`) maps each box
   key to a **2-tuple**, and `_LINE_GUARD_BOX_KEYS` (`runner.py:736–739`) scopes
   line 1b to `("st",)` and line 8b to `("lt",)`; cross-term collisions are
   structurally invisible at those call sites whatever the pair table contains.
   The live run path must pass the full six-fact-type set independent of box
   key.

6. **Completeness successor by re-identification, not by version.**
   `no-other-form8949-adjustments` **v1 stays published, unedited, and
   selected only by historical packages.** It is not superseded in place and is
   given no v2. The successor package selects a **newly identified** boundary
   declaration in its role:

   `tax.us.2025.schedule-d-boundary.no-unsupported-form8949-sources` v1,
   `fact-type.v2`, categorical `{yes,no}`, tax-year literal identity key, free
   supersession — the same shape as the other seven Schedule D boundary
   components. It declares: *this return has no Form 8949 source outside the
   supported covered code-W class and the supported broker-basis-furnished
   noncovered class, no unsupported adjustment code, and no multi-code row.*

   A same-id v2 was rejected as **mechanically impossible**, not merely
   undesirable: with no version at the symbol boundary, a widened v2 answer
   would also satisfy the narrow v1 check and reinstate v1's false claim.

   v1's retirement is **by non-selection**: the successor package omits the
   bundle member `tax.us.2025.schedule-d-boundary.form8949-w.vocabulary` v1 and
   adds a new bundle for the new declaration. Non-selection is an established
   retirement mechanism on this line — `package.core-calculations.v29.json`
   itself drops `tax.us.2025.rule.form1040-line12`, its citation, and its
   form-field in favour of the differently identified line-12e citizens. v1
   remains resolvable for v29 and every earlier package.

7. **Two completeness paths; no third path and no taxpayer discriminator.**
   `attachment.schedule-d` v6 (staying on `attachment-rule.v4`, per the
   value-check constraint) keeps the existing branch shape:

   ```text
   Path A: no-form8949-sources == "yes"
           AND no supported Form 8949 family is genuinely nonempty  (Decision 8)

   Path B: no-form8949-sources == "no"
           AND no-unsupported-form8949-sources == "yes"             (new id)
           AND all four supported families closed                   (Decision 9)
   ```

   Which supported classes a return actually contains is read from **which
   families close nonempty**, never from a declared answer. A W-only return
   closes both noncovered families empty; a noncovered-only return closes both
   code-W families empty. That is contributed authority, and it is the same
   closed-empty pattern every prior family milestone uses.

   A chained taxpayer discriminator ("are any of your Form 8949 sources
   noncovered?") was rejected by the owner on 2026-08-11: the distinction is
   already established by the contributed fact type and its family, so asking
   again duplicates authority and manufactures a contradiction case — a return
   could declare "no noncovered sources" while carrying a noncovered member.

8. **Path A contradiction guard.** Path A must not satisfy completeness when
   any supported Form 8949 family is genuinely nonempty. Without it a taxpayer
   who records a supported transaction and also answers "no Form 8949 sources"
   gets a silently wrong, silently complete return — the worst failure
   available in this milestone. The guard emits `BLOCK_INVALID`
   (`DEPENDENCY_INVALID`, `packages/derivation/evaluator.py:25`) with a named
   `tax.us.2025.block.*` symbol in `missing`, exactly as
   `GUARD_IDENTITY_KEY_COLLISION` does (`runner.py:195`, emitted at
   `runner.py:871–877`). **No `derivation-record` enum value is added.** Both
   inputs are already in scope at the guard site: the declaration's value from
   `self.symbols` (`runner.py:887`) and per-family member counts from
   `self.sources` (`runner.py:657`, `694`).

   The guard covers **all four** supported families, so it closes a
   pre-existing hole for the code-W class as well: today the Path A branch of
   `attachment.schedule-d.v5.json` (lines 54–71) adds only a value check on
   `no-form8949-sources` itself and nothing consults membership, so a return
   with covered-w members and `no-form8949-sources = "yes"` reads *complete* on
   Schedule D. No committed test exercises that state
   (`tests/test_schedule_d_form8949_covered_wash_sale_t1.py:164` selects
   `BOUNDARY_PATH_A` only when there are no W members). The guard is added in
   the successor package only; no historical adoption's disposition changes.

   Recorded asymmetry, deliberately accepted: like the collision guard, this
   guard is runner code keyed on `rule_id` (`runner.py:863`) rather than
   declarative attachment content. It introduces no new mechanism, but the
   attachment citizen does not state it, and a future substrate milestone
   should find this note.

9. **How family closure becomes load-bearing, since completeness cannot
   express it.** Completeness can require only declared answers (see Context),
   so Decision 7's "all four supported families closed" is **not** written into
   `adds_required`. It is carried by two already-published mechanisms:

   - **Completeness** — the four scalar companion closures, through
     `attachment.schedule-d` v6's `requirement.subtotals` (which gains the two
     noncovered proceeds subtotals; `runner.py:791–796` blocks
     `DEPENDENCY_ABSENT` on any absent subtotal symbol, unconditionally and
     before the threshold comparison) and through the new box-B/box-E
     itemization parts (`runner.py:834–855`). A subtotal symbol exists only if
     its family is closed: the subtotal rules are `collect` with
     `blocked.code = SOURCE_SET_UNCLOSED`
     (`rule.f1099b-covered-w-st-proceeds-subtotal.json:17–32`).
   - **Arithmetic** — the two whole-transaction family closures, through
     `require_closed` in the ADR-0064 line-2/line-9 rules, exactly as
     `rule.schedule-d-line1b.json`'s `when.all` requires `covered-w-st` plus
     its three scalar families.

   A closed-**empty** family publishes an explicit zero rather than nothing;
   verified in committed output, on a return with no capital activity at all,
   where `tax.us.2025.schedule-d.line-1b` carries finding value `"0"` at
   `sections/18` of
   `packages/sample_data/form1099g_box1_schedule1_line7/presentation/form1099g-box1-line8.presentation-model.v1.json`.

10. **Coexistence is admitted and needs no mechanism.** Code-W and noncovered
    transactions may appear in one return. Boxes A/D and B/E are independent,
    the families are independent, and Schedule D lines 1b/8b and 2/9 are
    independent addends; there is no arithmetic or authority interaction. Both
    classes sit on the same Path B.

## Production conditions (owed to Track 1; never allowlisted)

1. Every fact-type refusal in Decision 1 is exercised **through the real
   validator** on the production path — `basis_reported_to_irs = "yes"`
   refused, absent `basis` refused, any adjustment field refused — never
   asserted in prose.
2. The Decision 5 kill-test is exercised through `live_coordinate_run` on all
   fifteen pairs, with at least one **cross-term** pair among them, and the one
   existing test asserting the old issue code is updated (a test change, not a
   fixture change).
3. Structural proof that `no-other-form8949-adjustments` v1 is absent from the
   successor package's members and unreferenced by every successor citizen —
   `attachment.schedule-d` v6, `attachment.f8949` v2, and
   `selected-preferential-base` v5 are the only three citizens that reference
   it today (`attachment.schedule-d.v5.json:77–88`,
   `attachment.f8949.json:33–43`,
   `rule.selected-preferential-base.v4.json:210, 302, 307`) — while it still
   resolves under `adopt-core-v18-current.json`.
4. Goldens for each closed-empty discrimination: a W-only return at the
   successor package producing line 1b/8b arithmetic identical to the
   v18-pinned regression case, and a noncovered-only return with both code-W
   families closed empty.
5. The Decision 8 guard is exercised in **both** classes — a noncovered member
   under Path A and a code-W member under Path A.
6. Every prior-milestone regression fixture passes unmodified at its own
   pinned adoption.

## Consequences

- The box-B/box-E class becomes representable and routable without disturbing
  the direct-reporting or code-W families, their historical citizens, or any
  published schema.
- A published boundary declaration is retired for the first time by
  **non-selection with re-identification** rather than by in-place widening.
  The pattern is now explicit: when a supported universe widens, the boundary
  question widens with it and gets a **new id**; the old claim keeps exactly
  the meaning it was published with, forever.
- A code-W-only return rebuilt at the successor package answers a different
  boundary question than it did at v29. Its answer *count* is unchanged, and
  the new question is the true one for that package.
- A pre-existing correctness hole — Path A declared while supported Form 8949
  members are on record — is closed for both supported classes, and cross-term
  identity collisions become detectable for the first time.
- The engine still computes no basis, reconstructs none, validates none, and
  determines no security's covered status.

## Alternatives considered

- **A same-id `no-other-form8949-adjustments` v2.** Rejected as mechanically
  inert and then unsafe: a fact id carries no version at the symbol boundary,
  so v1 and v2 are one symbol with one answer and a widened answer would
  satisfy the narrow v1 check. This is what stopped the first Track 0 on
  2026-08-10.
- **A sixth parallel declaration alongside v1.** Rejected: two overlapping
  declarations about the same subject can be answered inconsistently, and
  nothing says which wins.
- **A chained taxpayer discriminator plus a third path.** Rejected by the owner
  2026-08-11: duplicated authority. The class is already established by the
  contributed fact type and family membership, and re-asking manufactures a new
  contradiction case.
- **Editing v1's title in place.** Rejected: mutation of a published citizen's
  meaning, and an explicit milestone non-goal.
- **Moving the class discrimination into rule content instead of completeness.**
  Rejected: regresses ADR-0055 — the attachment would read complete while a
  value-checking consumer correctly blocks.
- **A `source-family.v2` with value-filtered membership.** Rejected again, for
  ADR-0061's reason: a real substrate gap worth solving in general, but
  disproportionate to one bounded milestone; the generalized collision
  kill-test achieves the non-double-count guarantee without a new schema kind.
- **Guarding the class constraint in rule content instead of the value
  schema.** Rejected: a rule guard admits the false statement and then blocks a
  computation; a narrowed value schema means it is never representable.
- **A new `derivation-record` enum value for the Decision 8 guard**, copying
  the Form 1098 `F1098_SCOPE_CONTRADICTION` precedent. Rejected: the enum is
  closed at v6 and a new published schema version is an explicit non-goal and
  stop condition; the named-block-symbol mechanism carries the same
  information.
- **An `-adjustment` scalar companion holding a contractual zero.** Rejected:
  it would publish an authority nobody attests.

## Links

- Plan:
  `docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md`
  (Topic 6, "The chosen shape", "Expressibility of the chosen shape",
  "Track 0 adversarial closure")
- IRS authority: 2025 Instructions for Form 8949; 2025 Instructions for
  Schedule D (Form 1040); 2025 Form 8949
- Builds on: ADR-0010, ADR-0011, ADR-0017, ADR-0032, ADR-0036, ADR-0052,
  ADR-0054, ADR-0055, ADR-0057, ADR-0059, **ADR-0061**
- Companion: **ADR-0064** (Form 8949 boxes B/E, Schedule D lines 2/9
  composition)
- Owner decisions: plan approval and collision-kill-test scope 2026-08-10;
  completeness shape 2026-08-11
