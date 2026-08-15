# ADR 0063 — Migration Artifact as a Direct Supersession Root

- Status: **accepted** (Track 1 of fact-type-succession-neutral-schedule1)
- Tier: 2 — first migration schema family, authorizing act, and named
  supersession-root kind; future succession work is written against this
  contract. Instantiates Ontology §5 / §7; does not amend them.
- Date: 2026-08-14

## Context

Thirteen Schedule 1 Part II absence facts currently live as
literal-keyed `tax.us.2025.ss-benefits-scope.no-sch1-…` types, adopted
with the Social Security worksheet vocabulary. Nothing in the two
declared cascade edges reaches them: they have no derivation pins, and
their only identity key is the `{tax-year: 2025}` literal, so
`Fact.individuated_by` is empty. Currency's displacement roots are
correction findings, `_member_withdrawals`, and superseded-entity ids.
`apply_bundle_adoption` cannot retire an omitted id. Package adoption
is not a lattice act.

Adding a Schedule 1 contributor (Form 1098-E among them) therefore
cannot leave those thirteen answers silently current, cannot rename
them in place (fact identity ignores version), and cannot hide them
by omitting them from the current package dictionary. The owner
disposition for this milestone names the mechanism:

> Adoption of an explicit migration artifact is the succession act
> that names and retires the predecessor facts and creates their
> successors. This is a direct supersession root, not an
> individuation edge and not a new third cascade edge.

That disposition is the settlement this ADR instantiates. A reading
that treats the predecessor fact type as the citizen the thirteen
facts are "keyed on" is rejected: it is the reading review finding
F1 refused to bless, and it is not this decision.

## Decision

1. **Fourth named supersession root.** Adoption of a
   `migration-artifact.v1` citizen, recorded by an
   `act-migration-adoption.v1` act that captures the full artifact
   body, is a **direct supersession root**. It sits alongside the
   three roots `compute_currency` already takes from the record:
   correction findings, `_member_withdrawals`, and superseded-entity
   ids. Like withdrawal, the act contributes *roots*, never a new
   edge kind. `DECLARED_EDGE_KINDS` remains `{derivation,
   individuation}`.

2. **What the root does.** The root retires exactly the predecessor
   fact types the artifact names: those types leave current
   `state.fact_types`, so `facts_of` no longer projects their facts,
   and every finding answering a retired type is a displacement root
   with `DisplacementReason.kind == "supersession"` and `by` equal
   to the migration artifact id. Successor types named by the
   artifact must already be current (admitted by ordinary bundle
   adoption); the lattice then projects the successor facts.
   Consumers of the retired findings cascade through the **existing,
   unmodified derivation edge**.

3. **What the root is not.** It is not an individuation edge. It
   does not populate `Fact.individuated_by`. It does not treat a
   predecessor fact type as a keyed-on citizen. It is not a
   runner-resident filter of `F(P)` or of the current package
   dictionary. It is not a license to retire a fact type by any
   means other than an adopted migration artifact that names it.

4. **Finding half: presented successor claim.** For each named pair,
   if a predecessor fact has a then-current finding, the adoption
   presents a successor claim citing that finding, the pair, and
   the same `{yes, no}` value. The user asserts the presented
   claim. There is no silent conversion of a human finding. This is
   ADR-0025 decision 7 used as the *finding-half* precedent, not as
   the lattice mechanism.

5. **Re-admission.** A type id recorded as retired is not re-admitted
   by a later `bundle-adoption` that still lists it. Replay of the
   act log reproduces the same lattice, the same currency, and the
   same presented claims.

6. **This milestone's citizen.** One published artifact,
   `tax.us.2025.schedule1-adjustments-scope.succession` `v1`, names
   exactly the T0-1 thirteen predecessors and thirteen
   Schedule-1-native successors. It does not name
   `no-rrb-or-foreign-social-benefit` or the other nine
   `ss-benefits-scope` members. Those ten keep their existing ids.

7. **Package admission.** A package that claims this succession
   (pins the migration citizen, the successor vocabulary bundle, or
   the worksheet successor that reads the successor ids) must pin
   all three: the migration citizen, the successor types, and the
   worksheet successor. A package whose nonempty worksheet still
   names a retired predecessor id is malformed. A migration whose
   predecessor list is not exactly the T0-1 thirteen — including
   any list that names `no-rrb-or-foreign-social-benefit` or another
   non-Schedule-1 `ss-benefits-scope` member — is rejected.
   `artifact-package.v23` admits the `migration-artifact.v1` schema
   and the `migration-artifact` member role. `F(P)` for such a
   package excludes the named predecessors (admission and binding,
   ADR-0028) and does not itself displace findings already in the
   lattice.

8. **No Ontology amendment.** §5 already names a migration artifact
   that may instantiate successor facts. §7 already lists "a
   migration reshapes the lattice — old facts displaced, successor
   facts instantiated, findings following by derivation" as a
   succession occasion beside keyed-on-citizen replacement. This
   ADR narrows those sentences into a published schema, an act, and
   a fourth named root. No governance version change.

## Consequences

- Kernel state grows a retired-type set and a record of adopted
  migration artifacts. Currency grows a `_migration_supersessions`
  root contributor parallel to `_member_withdrawals`. Derivation
  edges, individuation edges, and `Fact.individuated_by` are
  unchanged.
- A workspace that has not taken up the migration keeps predecessor
  findings current even if a later package's `F(P)` no longer lists
  those types. Omission from a bundle or from the current package
  is not retirement.
- Fresh successor-package workspaces adopt the successor types and
  take up the migration; predecessor types never remain current.
  Upgraded workspaces take up the same act; then-current predecessor
  findings become presented claims.
- The Social Security empty-route contract is unchanged:
  `no-rrb-or-foreign-social-benefit` stays on its existing id, and
  the eleven `requires`, `require_closed`, `count`, the `no-rrb`
  conjunct, and `choose(count==0 → 0)` are the Milestone 1
  contract. The nonempty worksheet's conditional set names the
  thirteen successors.
- Future migrations publish a new artifact that names their own
  pairs and are taken up by the same act kind. This ADR is not a
  precedent for retiring types without such an artifact.

## Alternatives considered

- **Predecessor fact type as individuation root.** Rejected by the
  owner disposition. These facts are not keyed on their type; calling
  the type a keyed-on citizen would collapse Ontology §2's two
  existence paths. Review finding F1 correctly refused to bless that
  reading.
- **Runtime dictionary / current-package filter.** Rejected by the
  milestone's rejection rule and re-tested against the kernel:
  removing a type from `state.fact_types` without a currency root
  leaves existing findings current. ADR-0028's `F(P)` is admission
  and binding, not displacement.
- **New neutral facts, predecessors left dormant.** Rejected:
  `apply_bundle_adoption` cannot retire omitted ids; obsolete
  questions remain current.
- **Same-identifier redeclaration.** Rejected: `_fact_id` ignores
  version; old findings would stay attached to a broadened meaning.
- **Adoption-level replacement of `ss-benefits-scope.vocabulary` or
  the package.** Rejected as too coarse: that bundle and package
  also carry `no-rrb-or-foreign-social-benefit` and nine other
  non-Schedule-1 types, which this succession must not touch.
  Package adoption is not a lattice act.

## Links

- Milestone:
  `docs/phases/engine-breadth/milestones/fact-type-succession-neutral-schedule1.md`,
  `## Owner disposition (binding on Track 1)` and `## Amended Track 1 charter`.
- Review finding F1 (STOP FOR ADVISOR on the individuation-root
  reading) is decided by this ADR and the plan's
  `## Owner disposition (binding on Track 1)`.
- Finding-half precedent: ADR-0025 decision 7 (presented successor
  claim; not the lattice mechanism).
- Currency and derivation: ADR-0010.
- Package fact surface: ADR-0028.
- Schemas: `migration-artifact.v1`, `act-migration-adoption.v1`,
  `artifact-package.v23`.
- Kernel: `packages/kernel/facts.py`, `packages/kernel/currency.py`,
  `packages/kernel/findings.py`.
