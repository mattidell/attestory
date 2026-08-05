# ADR 0061 — Covered Wash-Sale (Code W) Transaction Authority, Family Topology, and Completeness Successor

- Status: **accepted** (ratified by the owner 2026-08-04). **Amended
  2026-08-05** (owner-approved, pre-merge): Decision 1's transaction-
  identity mechanism and Decision 2's non-double-count enforcement,
  after independent Track 1 review found the originally-named mechanisms
  unsafe given a real `source-family.v1` schema constraint.
- Tier: 2 — additive transaction-authority and completeness-successor
  contract for one breadth slice; reuses existing fact-type, family, and
  supersession substrate without a new schema kind.
- Date: 2026-08-04

## Context

The Current-Year Capital Losses milestone (ADR-0057/ADR-0058) made covered,
basis-reported, no-adjustment Form 1099-B transactions — short-term or
long-term, gain or loss — synthetic complete via direct Schedule D line
1a/8a reporting. Schedule D completeness item
(`packages/content/tax/2025/attachment.schedule-d.v4.json`) still
value-checks `tax.us.2025.schedule-d-boundary.no-form8949-sources` = `"yes"`
as a blanket block on every Form 8949 case.

The transaction identity in scope for extension,
`tax.us.2025.f1099b.covered-st-txn` / `covered-lt-txn`
(`packages/content/tax/2025/f1099b-covered-st.bundle.json` /
`f1099b-covered-lt.bundle.json`, fact-type.v2), already carries a **yes/no**
`box_1g_wash_sale_adjustment` field with no scalar amount. This milestone
must admit the broker-reported box-1g **amount**, route the affected
transaction to Form 8949 instead of the direct line, and succeed
`no-form8949-sources` for exactly the supported code-W case without
retiring it for every other Form 8949 source.

Track 0's paper-first decision record settled this ADR's fact-identity,
family-topology, and completeness contracts against real committed source
and the 2025 Form 8949/Schedule D instructions before this ADR was drafted;
it is distilled here and in the milestone plan
(`docs/phases/engine-breadth/milestones/schedule-d-form8949-covered-wash-sale.md`).

Companion attachment, arithmetic, validation, and Schedule D 1b/8b
composition are **ADR-0062**.

## Decision

1. **Accompanying scalar box-1g amount, on a separate wash-sale fact type
   (amended 2026-08-05).** `source-family.v1`'s `member_predicate` admits
   membership by bare `fact_type` id only — it has no value-filtering
   capability, and a fact-type id carries no version component either. That
   means the two mechanisms this Decision originally named (a `v3`
   successor of `covered-st-txn`/`covered-lt-txn`, or the same `v2` identity
   with an added field) both fail: either would force `covered-w-st`'s
   member predicate to name the *same* fact-type id `covered-st` already
   admits, making every direct-reporting assertion of that id an automatic
   member of both families at once — guaranteeing double-counting for every
   transaction, not just wash-sale ones, and directly contradicting Decision
   2's package-exclusivity requirement. Discovered during Track 1's repair
   (independent review Finding 2); no schema change is warranted for one
   bounded slice.

   The mechanism is instead: publish wholly separate, independently-
   identified fact types `tax.us.2025.f1099b.covered-w-st-txn` /
   `covered-w-lt-txn` (own bundle, own `member_predicate`), carrying:

   ```text
   box_1g_wash_sale_disallowed_amount: number, minimum 0, optional
   ```

   alongside a `box_1g_wash_sale_adjustment: enum ["yes","no"]` field of
   their own. The two fields are **independently contributable**, so "flag
   yes, no amount" and "amount present, flag not yes" are each
   representable and each independently blockable (required fixtures 11/12
   in the plan) — a single merged field could not express that asymmetry.

   Because membership is now by wholly separate fact-type id rather than a
   version of a shared id, non-double-counting is **not** automatic from
   family topology alone (Decision 2) — see Decision 2's identity-key
   collision requirement below.

2. **Two new package-exclusive families.** Publish
   `tax.us.2025.f1099b.covered-w-st` and `tax.us.2025.f1099b.covered-w-lt`
   (whole-transaction families), each with ADR-0054-style twin-scalar
   companions (`...proceeds`, `...basis`) and a third scalar companion for
   the box-1g adjustment amount (`...adjustment`) — three independent
   scalar quantities from one object-valued member, the same pattern
   ADR-0054 already established, not a new mechanism.

   Membership: a transaction is eligible for `covered-w-st`/`covered-w-lt`
   if and only if it is otherwise eligible for `covered-st`/`covered-lt`
   **and** `box_1g_wash_sale_adjustment = "yes"` **and** a nonnegative
   amount is contributed. A transaction with a contributed W amount is
   **package-exclusive** against `covered-st`/`covered-lt` — it cannot be
   adopted into both the direct-reporting family and the wash-sale family.

   **Identity-key collision requirement (amended 2026-08-05).** Because
   `covered-w-st-txn`/`covered-w-lt-txn` are separate fact types from
   `covered-st-txn`/`covered-lt-txn` (Decision 1), package-exclusivity is
   not structurally guaranteed by family topology the way ADR-0057
   Decision 4's same-id-different-version exclusion was. Package validation
   must kill-test: no two members — one from `covered-st`/`covered-lt`, one
   from `covered-w-st`/`covered-w-lt` — may share the same identity keys
   (broker, statement, transaction, tax-year). This is the actual
   enforcement of "a transaction cannot be adopted into both families,"
   checked directly against contributed identity, not inferred from
   version supersession.

3. **Correction and displacement.** Superseding the box-1g flag, the
   box-1g amount, or any other field of a `covered-w-st`/`covered-w-lt`
   member displaces, via existing ADR-0010 edges, at minimum: that
   transaction's Form 8949 row (ADR-0062), the enclosing box subtotal,
   Schedule D lines 1b/7 or 8b/15, line 16/21, `selected-preferential-base`,
   and Form 1040 line 7a/9 — the same displacement shape ADR-0057/ADR-0059
   already use for their own families.

4. **Completeness successor — two satisfaction paths, one declaration.**
   `no-form8949-sources` is **not retired**. Successor Schedule D
   completeness item "form8949" is satisfied by exactly one of:

   - **Path A (declared absence).** `no-form8949-sources = "yes"`
     (unchanged meaning).
   - **Path B (supported W-family only).** `covered-w-st` **CLOSED** and
     `covered-w-lt` **CLOSED** and a new fifth boundary declaration
     `tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments = "yes"`.

   The discriminator is the same `conditional_dependency_set` pattern
   ADR-0059 Decision 5 already uses. `no-other-form8949-adjustments` blocks
   every non-W code, every multi-code row, and every noncovered/basis-not-
   reported Form 8949 transaction from silently passing through this slice
   — it is a **named, honest boundary**, not a relaxation of
   `no-form8949-sources`'s original meaning.

5. **Non-confusion invariant.** Only Form 8949 attachment content
   (ADR-0062) and the successor Schedule D itemization it feeds may read
   `covered-w-st`/`covered-w-lt` symbols on Schedule D's own line 1b/8b
   producers; the direct line 1a/8a producers continue to read only
   `covered-st`/`covered-lt`. Package validation kill-tests any line
   1a/8a rule that pins a `covered-w-*` symbol, mirroring ADR-0059
   Decision 7's non-confusion invariant.

## Production conditions (owed to Track 1; never allowlisted)

1. Additive transaction-authority successor (Decision 1) with Payload
   Instantiation positives and named negatives (flag yes/no amount,
   amount/no flag, both absent).
2. `covered-w-st`/`covered-w-lt` families, closures, and twin/triple-scalar
   companions (Decision 2); a package-validation kill-test proving no two
   members sharing identity keys are adopted one into `covered-st`/
   `covered-lt` and the other into `covered-w-st`/`covered-w-lt`.
3. Successor Schedule D attachment completeness content adding the Path
   A/B gate on `no-form8949-sources` plus the new
   `no-other-form8949-adjustments` boundary declaration (Decision 4),
   without changing either existing declaration's meaning.
4. Goldens: Path A (unchanged); Path B missing W-family authority
   (blocked); Path B present with a closed-empty W family (zero result);
   correction of the box-1g amount and flag independently, each
   displacing the Decision 3 list; every prior-milestone regression
   fixture (current-year-losses, inbound carryovers, Schedule B)
   unmodified.
5. Structural proof that Schedule D line 1a/8a producers do not pin
   `covered-w-*` symbols.

## Consequences

- Wash-sale-adjusted transactions become representable and routable to
  Form 8949 without disturbing the direct-reporting families or their
  historical citizens.
- The blanket Form 8949 absence declaration stays honest for every
  unsupported adjustment code and noncovered case while the supported
  code-W case is unblocked.
- Independent flag/amount contribution lets every required "indication
  without amount" / "amount without indication" fixture be expressed and
  blocked without inventing a combined validation schema.

## Alternatives considered

- **Retire `no-form8949-sources` entirely.** Rejected: would silently
  claim completeness for every unsupported Form 8949 source and
  adjustment code, not just the supported W case — the same usability-
  vs-honesty tension ADR-0059 already resolved for inbound carryovers,
  resolved the same way here.
- **Add the box-1g amount directly onto the existing `covered-st`/
  `covered-lt` families instead of a new family.** Rejected (owner-
  confirmed in plan review): a transaction with a contributed W amount
  must route to Form 8949, not the direct line-1a/8a itemization, which
  has no column (g)/(h) concept; a new package-exclusive family keeps the
  direct and Form-8949 paths structurally distinct, mirroring ADR-0057's
  ST/LT split rationale.
- **A version successor of `covered-st-txn`/`covered-lt-txn` sharing the
  direct family's fact-type id (Decision 1's original framing).**
  Rejected 2026-08-05: `source-family.v1` membership is fact-type-id-only
  with no value filter, so this would make every direct assertion an
  automatic member of both families — the opposite of the intended
  exclusivity. Superseded by the separate-fact-type mechanism plus an
  explicit identity-key collision kill-test.
- **A `source-family.v2` schema adding value-filtered membership
  predicates.** Rejected: a real substrate gap worth solving in general,
  but disproportionate to one bounded milestone; the identity-key
  collision kill-test achieves the same non-double-count guarantee without
  a new schema kind.
- **A single combined flag+amount field with cross-validation at the
  presentation layer only.** Rejected: the required fixture battery needs
  "flag without amount" and "amount without flag" to be independently
  blockable at the completeness/production layer, not just flagged in
  presentation.

## Links

- Track 0's decision record settled this ADR's contracts before drafting;
  distilled here and in the milestone plan.
- Plan:
  `docs/phases/engine-breadth/milestones/schedule-d-form8949-covered-wash-sale.md`
- IRS authority: 2025 Instructions for Form 8949; 2025 Instructions for
  Schedule D (Form 1040); 2025 Form 8949
- Builds on: ADR-0003, ADR-0010, ADR-0011, ADR-0032, ADR-0036, **ADR-0052**,
  **ADR-0054**, **ADR-0057**, **ADR-0059**
- Companion: **ADR-0062** (Form 8949 attachment, arithmetic, Schedule D
  1b/8b composition)
