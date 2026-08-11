# ADR 0063 — Broker-Furnished Noncovered Basis: Transaction Authority, Family Topology, Collision Generalization, and the Completeness Successor by Re-identification

- Status: **proposed** (drafted 2026-08-11; revised 2026-08-11 against the
  owner's second ruling, blockers B1–B5; awaiting owner ratification)
- Tier: 2 — additive transaction-authority and completeness-successor contract
  for one breadth slice; reuses existing fact-type, family, and supersession
  substrate with no new schema kind, no new evaluator operator, and no
  `source-family.v2`. The attachment-substrate successor this ADR's
  completeness shape now rests on is **ADR-0065**
  (`attachment-rule.v7`), decided separately rather than folded in here.
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
**ADR-0064**; the attachment substrate both of them stand on is **ADR-0065**.
This ADR settles authority, identity, family topology, non-double-counting,
and completeness.

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
- **No *published* `attachment-rule` version can express this milestone's
  completeness honestly.** Completeness at v1–v6 reads only declared answers
  (`packages/schemas/tax/attachment-rule.v4.schema.json:77–127`;
  `runner.py:881–937`), applicability at v5/v6 is an amount threshold, and
  `check: "value"` exists at **v4 only** — the v5 and v6 files contain no
  `"value"` const. `attachment.schedule-d.v5.json:264` is on v4;
  `attachment.f8949.json` is on v6 and can carry only presence-checked answers.
  ADR-0062's context statement that v3–v6 are shape-identical is **inaccurate
  for v4** and is corrected here rather than by editing an accepted ADR.

  The owner's 2026-08-11 second ruling lifted the standing non-goal and
  authorized an additive published successor. **ADR-0065 publishes
  `attachment-rule.v7`**, which adds family-occupancy applicability,
  `completeness.required_closures`, and
  `branch_requirements[].asserts_families_empty` on top of v6's row model and
  v4's value check. Decisions 7, 8, and 9 below are written against v7 and are
  not expressible without it; the earlier draft of this ADR, which tried to
  carry them on v4/v6 plus a runner guard, is what the owner rejected.
- **The `derivation-record` block-code enum is closed at v6**
  (`packages/derivation/records.py:38–47`). The ADR-0061 Form 1098 precedent of
  adding an enum value (`F1098_SCOPE_CONTRADICTION`) is **not** followed:
  ADR-0065's constructs reuse `DEPENDENCY_ABSENT` and `BLOCK_INVALID`
  (`packages/derivation/evaluator.py:25`), so no enum value is added anywhere in
  this milestone.
- **Closure admission reads member identities, never member values.**
  `resolve_closure_admissions`
  (`packages/derivation/source_authority.py:99–166`) admits a family when
  exactly one closure finding exists at the family's **current** horizon and is
  boolean `true`; nothing in it reads a member's amounts. This is the
  mechanical basis of Decision 4.

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

4. **Correction versus membership transition — the boundary, stated as a rule
   rather than by example.** A `source-closure` finding claims *the member set
   of this family is complete as of this recorded horizon*. Its subject is the
   set of member **identities**. Therefore:

   > **A closure is displaced by a change to a family's set of member
   > identities, and never by a change to a member's values.**

   - **Value correction.** A supersession at the *same* fact identity inside
     the *same* fact type — corrected proceeds, corrected basis — leaves every
     family's member-identity set unchanged. The recorded horizon does **not**
     advance, no `source-closure` finding is displaced, and the family and
     scalar closures keep their exact finding ids and pins. This is mechanical,
     not conventional: `resolve_closure_admissions` selects the closure finding
     by fact type and current horizon only
     (`packages/derivation/source_authority.py:139–152`) and reads no member
     value, so a value correction cannot reach it.

     What *is* displaced, by ordinary ADR-0010 dependency edges, is every
     derived finding that read the corrected value: that transaction's Form
     8949 row, its box (d)/(e) subtotals, Schedule D line 2 or line 9, line 7
     or 15, line 16, line 21, `selected-preferential-base`, Form 1040 line 7a
     and line 9, taxable income, regular tax, and both attachment dispositions
     — whose pins name the superseded input finding. The recomputation runs at
     the **unchanged** horizon against the **same** current closures.

   - **Membership or identity transition.** Any change to the set of member
     identities: a new member asserted, a member retracted, a member's *identity
     keys* corrected (which is a retraction plus an assertion, not a value
     correction), or a member moved between families — a corrected statement
     now reporting basis to the IRS retracts the noncovered fact and asserts the
     covered one. Here the closure claim's subject genuinely changed. The
     recorded horizon advances, and the closure keyed to the prior horizon stops
     being current, so the family drops out of the admitted set
     (`source_authority.py:141–153`) and every `collect` / `require_closed` over
     it blocks rather than zeroing, until the family is reclosed at the new
     horizon.

     Only the families whose member-identity set changed are affected. A
     cross-family transition changes **two** families and requires reclosure of
     both; a return that reclosed only one is exactly the half-done state
     Decision 5's kill-test makes fail closed rather than double-count.

   The engine does not infer the transition: the horizon is a contributed
   entity (ADR-0017). What the engine guarantees is that a closure keyed to a
   superseded horizon is indistinguishable from an absent one on the dispatch
   path, so a return whose members moved and whose horizon did not is blocked,
   never quietly stale.

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
   `attachment.schedule-d` v6 moves to `attachment-rule.v7` (ADR-0065) and
   keeps the existing two-branch shape:

   ```text
   accounts_for (Decision 9, ADR-0065 Decision 8):
           form 1040-SCH-D and every Schedule D line symbol in the package

   required_closures (unconditional, and evaluated before applicability
   resolves, so it gates "inapplicable" too — Decision 9):
           every 1099-B whole-transaction family AND every scalar companion
           AND f1099div.2a

   Path A: no-form8949-sources == "yes"
           AND asserts_families_empty over the four Form-8949-routed
               whole-transaction families                           (Decision 8)

   Path B: no-form8949-sources == "no"
           AND no-unsupported-form8949-sources == "yes"             (new id)
   ```

   The "all four supported families closed" condition is no longer a Path B
   clause: it is unconditional under `required_closures`, because a return
   cannot know which path it is on until those families are closed. Which
   supported classes a return actually contains is then read from **which
   families close nonempty**, never from a declared answer. A W-only return
   closes both noncovered families empty; a noncovered-only return closes both
   code-W families empty. That is contributed authority, and it is the same
   closed-empty pattern every prior family milestone uses.

   The direct `covered-st` / `covered-lt` families are deliberately **not** in
   the Path A emptiness list: a basis-reported transaction with no adjustment
   may be reported directly on Schedule D line 1a/8a, so `no-form8949-sources
   = "yes"` is a true statement about a return that holds them.

   A chained taxpayer discriminator ("are any of your Form 8949 sources
   noncovered?") was rejected by the owner on 2026-08-11: the distinction is
   already established by the contributed fact type and its family, so asking
   again duplicates authority and manufactures a contradiction case — a return
   could declare "no noncovered sources" while carrying a noncovered member.

8. **The Path A contradiction is declared, not guarded.** Path A must not
   satisfy completeness when any Form-8949-routed family is genuinely nonempty.
   Without that, a taxpayer who records a supported transaction and also
   answers "no Form 8949 sources" gets a silently wrong, silently complete
   return — the worst failure available in this milestone.

   The `attachment.schedule-d` v6 Path A branch therefore carries an
   `asserts_families_empty` list (ADR-0065 Decision 4) naming
   `f1099b.covered-w-st`, `covered-w-lt`, `noncovered-st`, and `noncovered-lt`.
   An unadmitted family there blocks `DEPENDENCY_ABSENT` (emptiness unknown is
   not emptiness); an admitted family with members blocks `BLOCK_INVALID`
   naming the occupied family ids. **No `derivation-record` enum value is
   added**, and — the point of the owner's B5 ruling — **the behaviour lives in
   the citizen**: delete `attachment.schedule-d` v6 and it is gone. The
   `GUARD_IDENTITY_KEY_COLLISION` pattern of a `rule_id`-keyed runner branch
   (`runner.py:863`, `195`) is explicitly **not** followed. The earlier draft of
   this ADR proposed exactly that and recorded the citizen/runner asymmetry as
   an accepted cost; the owner ruled the cost unacceptable.

   Because the list is declared, the same check covers the code-W class and so
   closes a **pre-existing** hole: today the Path A branch of
   `attachment.schedule-d.v5.json` (lines 54–71) adds only a value check on
   `no-form8949-sources` itself and nothing consults membership, so a return
   with covered-w members and `no-form8949-sources = "yes"` reads *complete* on
   Schedule D and computes line 1b from real members. No committed test
   exercises that state
   (`tests/test_schedule_d_form8949_covered_wash_sale_t1.py:164` selects
   `BOUNDARY_PATH_A` only when there are no W members). The list is added in
   the successor package only; no historical adoption's disposition changes.

   Form 8949 needs no separate contradiction list: under Decision 9 its own
   applicability is family occupancy, so on the contradictory return it is
   **required**, and its completeness value-checks `no-form8949-sources` at
   `"no"`. It blocks `COMPLETENESS_VALUE_VIOLATION` on the same facts that
   block Schedule D. The two attachments cannot split.

9. **Family closure is load-bearing on completeness declaratively, for the
   whole transaction family and not merely its scalar projections.** This is
   the owner's B3 blocker, and the earlier draft's answer — scalar companions
   carry completeness, whole families carry only arithmetic — was insufficient
   exactly because lines 2 and 9 require whole-family closure that no
   completeness surface named. The correction:

   - **`completeness.required_closures`** (ADR-0065 Decision 3) on
     `attachment.schedule-d` v6 names every family the schedule's lines depend
     on: the six 1099-B whole-transaction families
     (`covered-st`, `covered-lt`, `covered-w-st`, `covered-w-lt`,
     `noncovered-st`, `noncovered-lt`), their scalar companions (two each for
     the direct and noncovered families, three each for the code-W families),
     and `f1099div.2a` for line 13. On `attachment.f8949` v2 it names the four
     Form-8949-routed whole-transaction families and their ten scalar
     companions.
   - **The set is the union of what the lines require**, per ADR-0065
     Decision 3's content obligation: every `source_set` named by a
     `require_closed` in a composed line's `when` (as
     `rule.schedule-d-line1b.json` does over `covered-w-st` plus its three
     scalar companions) and every `source_set` named by a `collect` in the
     subtotal rules those lines read (as
     `rule.f1099b-covered-w-st-proceeds-subtotal.json:17–32` does, blocking
     `SOURCE_SET_UNCLOSED`). Which lines those are is **declared**, not
     inferred: both successors carry ADR-0065 Decision 8's `accounts_for`, and
     the set above is exactly `families(accounts_for.line_symbols)` under that
     decision's traversal. `attachment.schedule-d` v6 declares
     `form_id: "1040-SCH-D"` and every Schedule D line symbol the package
     publishes; `attachment.f8949` v2 declares Form 8949 and the four line
     symbols `schedule-d.line-1b`, `line-2`, `line-8b`, `line-9` — which
     ADR-0065 Decision 8's obligation O4 forces on it independently, since each
     of those lines' rules `require_closed`s one of Form 8949's occupancy
     families.
   - **The check is evaluated before applicability resolves** (ADR-0065
     Decision 3's normative ordering, at the `runner.py:820`/`822` boundary), so
     it gates the `inapplicable` disposition as well as the complete one. Under
     the first draft it ran only after the attachment was required, and
     `runner.py:822–830` returns `inapplicable` before completeness is read at
     `runner.py:882` — leaving the state B3 names alive: all six whole-
     transaction families closed **empty**, one scalar companion unclosed,
     Schedule D `inapplicable`, line 2 blocked `SOURCE_SET_UNCLOSED`. Scalar
     companions are the exposed case because they appear only in
     `required_closures` and never in the occupancy list.
   - **Therefore "Schedule D is complete or inapplicable" entails "no Schedule D
     line blocks for closure"**, because both sides read the same admitted set:
     the runner passes `closed_sets=frozenset(self.admissions)` to the evaluator
     at `runner.py:336`. That entailment is the whole content of B3, and it did
     not hold before — for lines 1a, 1b, 8a, or 8b either.

   Applicability is likewise family-shaped rather than amount-shaped
   (ADR-0065 Decision 2, this milestone's B4): the Schedule D and Form 8949
   requirements count members, so a member with zero proceeds and positive
   basis, or a zero/zero member, makes both forms required. The residual
   threshold terms are the two capital-loss-carryover symbols, which are rule
   output with no family to occupy.

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
5. The Decision 8 `asserts_families_empty` list is exercised in **both**
   classes — a noncovered member under Path A and a code-W member under Path A —
   and in the unadmitted-family case, where emptiness is unknown and the block
   must be `DEPENDENCY_ABSENT`, not `BLOCK_INVALID`.
6. Decision 4's boundary is exercised in **both** directions at the production
   boundary: a same-member value correction that leaves every closure finding id
   unchanged while every dependent derived finding is displaced, and a
   membership transition that advances the horizon and makes the prior closure
   non-current. A fixture that merely observes a changed number does not
   discharge this; the closure finding ids and the currentness of each closure
   are what is asserted.
7. Decision 9's `required_closures` set is proved to equal
   `families(accounts_for.line_symbols)` by the mechanical check ADR-0065
   production conditions 5, 5a, and 5b owe, not by inspection — and the checker
   contains no `tax.us.2025.` string.
7a. Decision 9's ordering is exercised at the production boundary by ADR-0065
   production condition 3a: all six whole-transaction families closed empty,
   one scalar companion unclosed, both attachments `blocked` with the companion
   named and neither `inapplicable`, and line 2 blocked
   `SOURCE_SET_UNCLOSED` in the same run.
8. Every prior-milestone regression fixture passes unmodified at its own
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
- Three further pre-existing disagreements are closed as a side effect of
  standing on `attachment-rule.v7`: Schedule D can no longer read complete
  while a whole-transaction family is unclosed and its line blocks (true today
  for lines 1a/1b/8a/8b); a zero-proceeds transaction can no longer leave a
  required form reporting itself unnecessary; and the Form 8949 and Schedule D
  attachments can no longer reach opposite verdicts on the same boundary
  declaration.
- The milestone now publishes a schema version, which the plan originally
  forbade. That is the owner's 2026-08-11 ruling, and the cost is recorded in
  ADR-0065 rather than minimized here.
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
- **A new `derivation-record` enum value for the Decision 8 check**, copying
  the Form 1098 `F1098_SCOPE_CONTRADICTION` precedent. Rejected: the enum is
  closed at v6, and `BLOCK_INVALID` plus the occupied family ids in `missing`
  carries the same information without one.
- **A `rule_id`-keyed runner guard for the Decision 8 check**, on the
  `GUARD_IDENTITY_KEY_COLLISION` precedent. This was the earlier draft's
  decision, with the citizen/runner asymmetry recorded as an accepted cost.
  Rejected by the owner 2026-08-11 (blocker B5): deleting the artifact would
  not remove the behaviour, so the citizen would not be the account of the form
  it claims to be.
- **Leaving whole-transaction-family closure to `require_closed` in the line
  rules alone**, with scalar-companion closure carrying completeness. This was
  the earlier draft's Decision 9. Rejected by the owner 2026-08-11 (blocker
  B3): lines 2 and 9 separately require whole-family closure, so Schedule D
  could read complete while those lines block — and, on inspection, that state
  is already reachable today for lines 1a/1b/8a/8b.
- **Keeping the `proceeds > 0` requirement threshold** and treating the
  zero-proceeds transaction as a curiosity. Rejected by the owner 2026-08-11
  (blocker B4): a broker-furnished basis with zero proceeds is an ordinary
  worthless-security disposition, and a form that reports itself unnecessary
  while its own arithmetic produces a real loss is the same defect class as
  every other item here.
- **An `-adjustment` scalar companion holding a contractual zero.** Rejected:
  it would publish an authority nobody attests.

## Links

- Plan:
  `docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md`
  (Topic 6, "The chosen shape", "Attachment substrate decision (B2)",
  "Track 0 adversarial closure")
- IRS authority: 2025 Instructions for Form 8949; 2025 Instructions for
  Schedule D (Form 1040); 2025 Form 8949
- Builds on: ADR-0010, ADR-0011, ADR-0017, ADR-0032, ADR-0036, ADR-0052,
  ADR-0054, ADR-0055, ADR-0057, ADR-0059, **ADR-0061**
- Companions: **ADR-0064** (Form 8949 boxes B/E, Schedule D lines 2/9
  composition), **ADR-0065** (`attachment-rule.v7`, the substrate Decisions 7–9
  stand on)
- Owner decisions: plan approval and collision-kill-test scope 2026-08-10;
  completeness shape 2026-08-11; second ruling 2026-08-11 (blockers B1–B5,
  lifting the schema-version non-goal)
