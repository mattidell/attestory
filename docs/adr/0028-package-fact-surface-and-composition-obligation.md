# ADR 0028 — Package Fact-Surface Membership and Composition-Obligation Trigger

- Status: **proposed** (2026-07-15; decision 7 retyped after over-trigger review; awaiting scoped adversary confirmation then owner ratification)
- Tier: 2
- Date: 2026-07-15

## Context

ADR-0027 accepted the adopted-content membership **floor** (extend `artifact-package.v2`, typed closed graph, role canon, `admitted_schemas`, package-instance immutability, exclusive execution projection, form-field producer integrity, provenance-only `composition` pin) but left **Not Decided**:

- **N1** — fact-surface versioning ⋂ wholesale-adoption reconciliation (ACM-G1 / A4 / A7 from the main ACM round)
- **N2** — declared composition-obligation trigger (ACM-A3)

The residual micro-round produced two clean-room-separated designs and two independent committee reviews. Both reviewers **rejected** the rival (it2) on both propositions. The incumbent (it1) supplies the carry-forward mechanisms; the adversary proved two completeness holes (orphan individual pin for mapping; structural force-declare bypass for multi-source bare sums that avoid the family-subtotal shape). This decision settles N1/N2 by carrying it1's dual fact surface and non-circular obligation design **with those holes closed**: A4 inclusion completeness; A7 closed by **same-quantity** force-declare (not any-multi-input). An intermediate any-multi-input draft over-fired on line 9; see `review-feedback-adr0028.md` and the evaluation-analysis on-record correction. Evidence: `docs/prototypes/adopted-content-manifests/micro-round/evaluation-analysis.md`.

## Decision

1. **Fact-type and bundle citizens are versioned exact members.** `fact-type.v2` and `bundle.v2` require a `version` field consistent with other citizens (`^v[0-9]+$`). Historical `*.v1` fact types and bundles remain valid unversioned content for migration windows but are **not** valid targets of residual exact-membership pins. Claiming exact fact versions against unversioned citizens is rejected or inexpressible.

2. **Dual pin unit for the fact surface.**  
   - Packages pin vocabulary with member role **`fact-type-bundle`**: `{id, version}` naming a `bundle.v2` whose nested fact identities are exact `(id, version)` (pins or nested versioned objects under wholesale capture).  
   - Binding joins (`input_bindings` / `optional_default`) and mapping fact-type fields name exact fact-type `(id, version)`.  
   - The package closed fact surface `F(P)` is the set of nested fact identities of all package-pinned bundles, plus any individual `fact-type` members **only if** those identities are also covered by package⊆adoption inclusion (decision 3). Individual pins alone do **not** satisfy binding closure without bundle coverage.

3. **Wholesale adoption reconciled by nested-set equality.** `act-bundle-adoption.v2` remains wholesale (embeds the full `bundle.v2` body). At package adoption / run bind, every package `fact-type-bundle` pin must match an adopted entry with **identical nested fact-type identity set**. Generation swap, omit, or extra nested members → reject. Every fact identity used by bindings or mappings in `F(P)` must appear under that inclusion (closes orphan-pin mapping bypass).

4. **Mapping fact-type edges are exact.** `source-closure-mapping.v2` (or equivalent) upgrades `member_fact_type` and `closure_fact_type` to exact `{id, version}` pins that must lie in `F(P)`. Bare-id mapping fields are not residual-closed.

5. **Composition obligation is package-declared and non-circular.** An `artifact-package.v2` field `composition_obligations` (array of published symbols, or equivalent package-authoritative declaration) is the obligation authority. Discoverability **does not** require a composition citizen to already be present. A separate versioned obligation citizen, if used, may only **echo** package declarations; it must not be the sole path (rejects empty-obligation no-op designs).

6. **Per obligated symbol `S`, require full composition binding.** The package must contain: (a) a composition member whose `publishes == S`; (b) the producing rule's provenance-only `composition: {id, version}` pin resolving to that member; (c) slot bijection with the rule's constituents when the composition is present. Missing pin and missing member are both rejects even when one or the other is absent. No derivation edge from the composition pin (ADR-0026 decision 4; ADR-0010).

7. **Structural force-declare (same-quantity source aggregation — non-omittable net).** Independent of the obligation list being authored first, package validation **requires** that a published symbol `S` appear in `composition_obligations` when the producing rule has **two or more** distinct adopted inputs that are **alternative sources or subtotals of `S`'s own tax quantity** — that is: source-family `authorizes_subtotal` values for that quantity, **or** raw source amounts (including ELX of source facts) of that **same** quantity. Undeclared → reject.

   This preserves the residual incumbent's force-declare architecture and still catches the adversary MR-A7 construction (raw multi-amount line-2b that omits family pins). It does **not** fire merely because a rule aggregates ≥2 inputs of **different** quantities (ordinary downstream arithmetic: Form 1040 line 9 = line 1a + line 2b; lines 11/15/16). Those cross-quantity folds must validate **without** a `composition_obligations` entry.

   **Quantity identity** is declared content (on source-family / fact-type / mapping surfaces as needed for the join) — not runner-resident symbol tables (Article 11). Implementation must make the same-quantity join schema-authoritative (ADR-0006 decision 3).

   **History:** an earlier draft broadened to "any ≥2 multi-input aggregation," which closes A7 but over-fires on line 9 et al. Owner-requested review (`micro-round/review-feedback-adr0028.md`) rejected that draft as ratification-unready; this decision uses the same-quantity retype. A scoped adversary confirmation pass on both trigger directions is required before acceptance.

8. **Schema authority, not prose.** Package and rule schema successors admit the obligation field and composition pin with versions; admitted_schemas must list residual schema generations used (ADR-0027 decision 3). Form-fields remain presentation-only (ADR-0012). No runner-resident symbol-name table (Article 11).

## Consequences

- ADR-0027 Not Decided N1/N2 are **closed** by this decision once accepted.
- Track 4 may implement full membership closure over the fact surface and composition obligation under ADR-0027 + this ADR.
- **PC1.** Goldens (reject direction): unversioned fact pin; pin/bundle/adoption drift; mapping fact unpinned; bare multi-source **same-quantity** sum without obligation (family-subtotal fold **and** MR-A7 raw multi-amount line-2b); obligation without pin; orphan individual pin cannot close mapping without adoption cover.
- **PC1b.** Golden (accept / non-trigger direction): Form 1040 line 9 = line 1a + line 2b (cross-quantity total income) **validates without** a `composition_obligations` entry; similarly lines 11/15/16-style cross-quantity folds must not be force-declared as composition-governed solely for having ≥2 inputs.
- **PC2.** Migration of committed v1 bundles to v2 is implementation work; residual pins target only versioned citizens.
- **PC3.** Issue-code strings are implementation detail.
- Supersedes nothing in ADR-0027's accepted decisions 1–7; amends only the residual carve-out.

## Alternatives Considered

- **Rival residual surface (it2): individual fact-type pins + any-adopted-bundle scan + composition-obligation.v1 as sole discoverability.** Rejected: decision-blocking committee findings (incomplete A7, id-only mapping, empty-obligation bare sum, dead bundle pin role, weak adoption reconciliation).
- **Incumbent residual surface unchanged.** Rejected as complete N1/N2: orphan individual pin mapping hole (MR-A4); structural force-declare bypass (MR-A7).
- **Hardcoded symbol lists in the runner for composition-governed lines.** Rejected: Article 11.
- **Form-field as obligation authority.** Rejected: ADR-0012 presentation-only.
- **Leaving N2 open for another builder round.** Considered; not chosen in the draft — the adversary hole is a net-completeness gap on an accepted direction; the broadened force-declare is the same mechanism completed. Owner-requested review (2026-07-15) found any-multi-input broadening over-fires on cross-quantity arithmetic; decision 7 retyped to same-quantity source aggregation; scoped adversary confirmation required before acceptance (default further review for foreman-authored patches — proposed ADR-0013 amendment).

## Links

- Evidence: `docs/prototypes/adopted-content-manifests/micro-round/evaluation-analysis.md`; `reviews/round-1-governance.md`, `reviews/round-1-adversary.md`; exhibits `it1/design.md` (`85af87a`), `it2/design.md` (`cd0cdc8`).
- Parent: ADR-0027 (accepted floor; N1/N2 were Not Decided).
- Related: ADR-0003, 0006, 0010, 0012, 0014, 0025, 0026.
- Milestone: Core Tax Conditions Track 0.b residual; Track 4 full membership closure after acceptance.
