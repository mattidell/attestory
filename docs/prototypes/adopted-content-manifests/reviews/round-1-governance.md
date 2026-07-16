# Round 1 — Governance Review: Adopted-Content Manifests (it1 vs it2)

Date: 2026-07-14  
Role: Governance Reviewer (Medium tier), owner-launched independent context  
Charter: `roles/reviewer-governance.md`  
Advisory only — disposition is the owner's.

## Independence and reading boundary

**Read:** topic `plan.md`, `charter-it1.md`, `charter-it2.md`, `it1/design.md`,
`examination-it1.md`, `it2/design.md`, `examination-it2.md`, `docs/governance/`
(constitution, ontology, principles, engineering-constraints, commentary),
ratified ADRs 0002, 0003, 0006 (decisions 3/6/7/9), 0010–0012, 0014, 0016,
0025, 0026, and committed `packages/derivation/{package_validation.py,loader.py}`,
`packages/schemas/{derivation,kernel,tax}/*`, and
`packages/content/tax/2025/*` as reference shapes. Inert spike and proposed
ADR-0022 were consulted only as superseded prior art (both designs reject them).

**Did not read:** `reviews/round-1-adversary.md`, any ADR-0027 draft or notes
toward ADR-0027.

Method: every HEAD claim below was checked against committed schema, validator,
loader, and content files, not only against the designs' paraphrase of them.

---

## Independent convergence (strong positive signal)

Both designs, from clean-room-separated builders working the same public
contracts, independently land on these load-bearing claims:

1. **Extend, do not fork.** The closed content unit is `artifact-package.v2`
   extending ADR-0006 decisions 6–7/9. Neither invents a filesystem
   `manifest.json`, path inventory, directory walk, or second adoption citizen.
   Both explicitly supersede (do not inherit) the inert spike / ADR-0022.
2. **`composition` is provenance-only.** The pin role enters the shared
   vocabulary once and creates **no** standing-affecting derivation edge;
   displacement remains `input`/`choice` only (ADR-0010; ADR-0026 decision 4).
3. **Contained validation.** A bad member/edge is a recorded issue; the walk
   continues over unrelated members (ADR-0006 decision 3). Neither design
   aborts the whole package validation on the first defect.
4. **Schema-generation gate is explicit and non-silent.** Unadmitted `*.v2`
   (or other unlisted schema generations) reject at load rather than being
   skipped. Mixed historical `*.v1` and post-0025/0026 `*.v2` is allowed only
   when the package declares what it closes over.
5. **Floor bindings are non-vacuous.** Both reject dangling form-field
   `binds_symbol` (case 3), vacuous/mismatched composition (case 4), ELX
   binding holes including elective defaults (case 5), and assert package
   version immutability under Article 9 (case 7).

Independent convergence on all five is the strongest committee signal available
for ACM-P1's floor and ACM-P2's non-silent-partial-load requirement. The
findings below do not undo that floor; they qualify the mechanisms and the
shared fact-type gap.

---

## Findings

### ACM-G1 — Fact-type and bundle citizens are not version-pinnable at HEAD; both designs pin them as if they were

**Applies to:** it1 and it2  
**Classification:** decision-blocking (for ACM-P1's exact-member-version claim
over the fact-type surface; also a prerequisite for several ACM-P2
`input_bindings` / ELX joins)

**Evidence against HEAD:**

- `packages/schemas/kernel/fact-type.v1.schema.json` has properties
  `schema, id, title, nature, identity_keys, value_schema, supersession` —
  **no `version`**.
- `packages/schemas/kernel/bundle.v1.schema.json` has
  `schema, id, label, fact_types` — **no `version`**. Nested fact types are
  full `fact-type.v1` objects without instance versions.
- `act-bundle-adoption.v1` captures the bundle **wholesale** in the act; its
  description states the kernel validates the nested bundle against the schema
  version it names — i.e. vocabulary entry today is adoption of an unversioned
  bundle body, not per-instance `(id, version)` pins.
- Committed content matches: `w2.bundle.json` / `f1099int.bundle.json` carry
  `id` and no `version`; nested fact types have `id` only.

By contrast, `rule-artifact.v1`, `parameter-declaration.v1`,
`operation-semantics.v1`, `form-field.v1`, `source-family.v1`, and
`source-closure-mapping.v1` all carry `version` with pattern `^v[0-9]+$`, and
committed instances populate it.

**Design behavior:**

- it1's member-kinds table: role `fact-type` "pins version-lock individual fact
  types"; Case 1 pins
  `tax.us.2025.w2.box1-wages@v1` / `tax.us.2025.w2.source-closure@v1`.
  Formalism: `M` is the set of pinned `(id, version)` keys resolved against
  `corpus[(id, version)]`.
- it2's paper contract: `input_bindings[].fact_type: {id, version}` and
  `bundle: {id, version}`; Case 1 pins `w2-vocabulary@v2` "containing"
  versioned fact types; lifecycle names fact-type-bundle pins at `@v2`.

Neither design states the schema diff required to make this true —
`version` on `fact-type.v2` (already foreshadowed by ADR-0025's paper
`fact-type.v2` / `optional_default`) and, if the pin unit is the bundle,
`version` on `bundle.v2` — nor reconciles pin-based per-instance closure with
today's wholesale bundle-adoption mechanism.

Concretely: given committed `w2.bundle.json`, a pin
`{role: fact-type, id: tax.us.2025.w2.box1-wages, version: v1}` cannot resolve
against a corpus keyed by `(id, version)` because the citizen carries no
version to match. ADR-0006 decision 6's "exact member versions" and the plan's
Gate 6 floor (close over form-fields **and** at least one post-0006 authority
family, with ELX bindings depending on fact-type identity) make this
load-bearing, not an edge case.

This is **independent convergent evidence of the same unexamined assumption**
in both rivals — weight it heavily because neither designed around it.

**Verdict contribution:** decision-blocking for ACM-P1 (and for ACM-P2 joins
that require exact fact-type version pins) in **both** designs until resolved
by one of: (a) explicit `fact-type.v2` / `bundle.v2` version-field diffs and
re-run of fact-type rows in Cases 1, 2, 5, 7; or (b) an explicit alternate
pin/identity rule for fact types that still satisfies exact-member-version
without pretending HEAD already has the field.

---

### ACM-G2 — it2's `schema_contracts[].sha256` reopens schema-publication checksums that the plan places out of scope

**Applies to:** it2  
**Classification:** production condition (mechanism overreach; not a floor
failure if dropped)

**Evidence:**

- Plan Gate 0: "Schema *publication* checksums (`published.json` per schema
  directory) already exist under ADR-0003; **this topic does not reopen
  them** — it decides content-unit closure that *consumes* published schemas."
- Committed reality: `packages/schemas/derivation/published.json` and
  `packages/schemas/kernel/published.json` already map schema filenames to
  sha256; ADR-0003 consequences: "The schema registry enforces immutability
  mechanically (checksum of published versions)."
- it2's `schema_contracts` requires each entry to carry `sha256` and states
  "its schema must have the listed immutable published checksum."

Package-level re-pinning of schema **bytes** creates a second authority for
schema immutability beside the registry. That is dual bookkeeping of Article 9
canon for schemas, not content-unit membership. The useful part of
`schema_contracts` for ACM-P2 is **which schema generations the unit admits**
and (optionally) `content_role` for historical schemas — not a second hash
registry.

it1's `admitted_schemas` (array of schema ids) correctly *consumes* published
schemas without re-checksumming them. That is the plan-aligned shape for the
admission list.

**Verdict contribution:** production condition on it2's ACM-P1/P2 mechanism —
carry generation admission; **drop** per-package schema-byte checksums in favor
of the existing `published.json` / `SchemaRegistry` path (or an explicit
single-line reference that the package validator *consults* the registry,
without embedding hashes in every package document).

---

### ACM-G3 — Bidirectional closure: it2's typed reachability is stronger; it1 is mostly outbound

**Applies to:** it1 (gap), it2 (strength, with entrypoint caveat)  
**Classification:** non-blocking relative to Gate 6 floor; material for which
surface better discharges ADR-0006 decision 6

ADR-0006 decision 6 requires "enforced closure in both directions." The
committed validator today resolves every pin to a corpus citizen and checks
outbound parameter/table refs and unique output ownership — not reverse
reachability from declared roots.

- **it1** walks outbound edges (parameter/table, family, composition pin,
  mapping→family, form-field→symbol, input_bindings→fact-type, composition
  slot peers) plus ownership/bijection integrity. It **explicitly leaves**
  reverse-reachability of unused pins unresolved and not required for its
  floor claim.
- **it2** builds a typed directed graph and requires every edge to resolve to
  an exact member **and** every member to be reachable from package
  `entrypoints`. That catches omitted peers *and* inert passengers. It also
  names `ACM_ENTRYPOINT_MEMBER_ABSENT` so entrypoints cannot invent members
  outside `members[]` — entrypoints are roots, not a second inventory.

**Caveat on it2:** the paper example only shows `entrypoints.form_fields`. If
the only legal roots are form-fields, a non-presentation authority package
(subtotal rules + families + mappings without a form-field) cannot close under
strict reverse-reachability. Production must either admit additional root kinds
(computation, composition, package-level declared roots) or define when
reverse-reachability applies.

**Verdict contribution:** it2 better discharges a strong reading of decision 6;
it1 still meets the plan floor (outbound + binding integrity). Prefer it2's
typed graph for carry-forward, with entrypoint-root kinds as a production
condition.

---

### ACM-G4 — Pin-role dual meaning: it1 is process-only; it2 is load-time but has a per-package escape hatch

**Applies to:** it1 and it2  
**Classification:** production condition (both)

Plan Case 6 and ACM-P2 require rejection when two members share a pin-role
token with divergent meanings across schema generations — not only when a token
is unknown.

- **it1:** Case 6's dual-meaning defense is "vocabulary monotony + schema
  review." The issue table has `PIN_ROLE_UNKNOWN` for unrecognized tokens, not
  a load-time check that the same token means the same thing across every
  admitted schema generation. That is human process at ADR-drafting time, not
  a contained load reject.
- **it2:** Names `ACM_ROLE_SEMANTIC_DIVERGENCE` and a versioned
  `role_vocabulary` / `canon.content-roles` pin, plus `content_role` on schema
  contracts. Historical schemas that cannot grow a `content_role` field declare
  it in the package's `schema_contracts` entry. That last escape hatch is
  package-local: without a cross-package or registry-level monotony check, two
  packages could in principle assign different `content_role` values to the
  same historical schema id. Design text says schemas may not privately
  redefine tokens; the mechanism that enforces that across packages is not
  fully closed on paper.

**Verdict contribution:** production condition for both ACM-P2 verdicts —
mechanize dual-meaning rejection (prefer it2's named check + single role
canon), and close the per-package `content_role` escape so historical schemas
have one global permitted role, not a package-authored one.

---

### ACM-G5 — Package-version immutability (Case 7): it2 names a testable mechanism; it1 asserts policy

**Applies to:** it1 (thin), it2 (concrete)  
**Classification:** production condition (neither blocks paper settlement of
Article 9 intent; it1 should be tightened before implementation)

Case 7 is mandatory. Article 9 / ADR-0003 require immutable published versions;
an illegal partial upgrade that keeps `U@v1` while changing the member set must
reject.

- **it1:** "Illegal partial: `PACKAGE_SCHEMA_INVALID` or adoption-time
  `PACKAGE_VERSION_CONFLICT` (production condition: registry enforces hash of
  published package citizen). … If presented only to validator without
  registry, treat as a **different** unpublished instance." That is a policy
  statement. Nothing in the paper `artifact-package.v2` schema diff or
  validator behavior table actually performs a comparison. As written, the
  illegal case is **asserted**, not shown.
- **it2:** Offered manifest bytes are compared against a **published checksum
  of the package instance itself**, yielding `ACM_PACKAGE_VERSION_REWRITE`.
  This is distinct from ACM-G2 (schema-byte checksums). A package-content
  checksum registry is a legitimate undecided extension of the ADR-0003 pattern
  to package *citizens*, not a duplication of anything already committed.

**Verdict contribution:** non-blocking for paper Rung-2 settlement of either
design's Article 9 intent, but it1's treatment of a **mandatory** case is
materially thinner. Carry it2's package-instance-checksum mechanism (or an
equivalent named comparison) into production conditions for whoever implements
Track 4.

---

### ACM-G6 — Structural divergence ruling (membership admission + binding surface)

**Applies to:** both (required structural comparison)  
**Classification:** comparative judgment for carry-forward (not a defect code)

Both claim `artifact-package.v2` extension. Mechanisms diverge as the charter
required this seat to judge:

| Dimension | it1 (incumbent) | it2 (rival) |
|---|---|---|
| Schema-generation admission | `admitted_schemas` string list of schema ids | `schema_contracts` with id + **sha256** + `content_role` |
| Fact-type surface | Individual `fact-type` member pins | `fact-type-bundle` member kind + nested exact fact-type versions |
| Role monotony | Shared vocabulary growth; dual-meaning via review | `role_vocabulary` canon pin + `ACM_ROLE_SEMANTIC_DIVERGENCE` |
| Closure shape | Outbound edges + ownership/bijection integrity | Typed graph: outbound + inbound from `entrypoints` |
| Form-field roots | Form-fields are ordinary members | `entrypoints.form_fields` as declared roots |
| Issue codes | `FORM_FIELD_*`, `COMPOSITION_*`, `ELX_*`, `MEMBER_SCHEMA_UNADMITTED` | `ACM_*` including rewrite and role divergence |
| Immutability (Case 7) | Policy / deferred registry | Named package-instance checksum reject |

**Ruling against ADR-0006 decisions 6–7, the plan floor, Article 11, and
dual-meaning prevention:**

1. **Floor discharge:** Both designs meet Gate 6 — extend not fork; close over
   form-fields and post-0006 authority (source-family/mapping **and**
   composition); reject case 3 and cases 4–5. Decision 7 (unique output
   ownership / declared conflict semantics) is retained by both.
2. **Decision 6 (exact versions + bidirectional closure):** Exact versions are
   blocked for fact-types in **both** by ACM-G1. On the *package-level*
   mechanism, it2's typed bidirectional graph is the fuller discharge of
   "closure in both directions"; it1 is adequate for the floor but thinner.
3. **Article 11 (no runner-resident policy):** Both put ELX defaults and
   bindings in declared package/fact-type content (aligned with already-accepted
   ADR-0025 `input_bindings`). Neither smuggles tax meaning into the runner.
4. **Dual pin-role meanings:** it2's load-time check is the better paper shape;
   it1 leaves it to process (ACM-G4).
5. **Schema admission without dual canon authority:** it1's `admitted_schemas`
   list is better aligned with the plan and ADR-0003 than it2's embedded schema
   sha256 (ACM-G2). it2's `content_role` idea is useful only if globally
   monotonous (ACM-G4).
6. **Fact-type pin unit:** Bundle-as-member (it2) matches today's wholesale
   adoption act; individual fact-type pins (it1) match ADR-0025's binding
   target (`fact_type` on `input_bindings` / `optional_default`). After ACM-G1
   is resolved, the carry-forward surface should allow **bundle membership for
   vocabulary adoption** and **exact fact-type identity in bindings** — not
   force a false choice.

**Net structural preference (advisory):** carry **it2's typed closed-graph rule,
package-instance immutability check, and load-time role-divergence check**,
but **replace it2's schema-byte `schema_contracts[].sha256` with it1's simpler
`admitted_schemas` (schema-id admission)** that rides on the existing registry.
Treat ACM-G1 as a joint prerequisite before either fact-type pin unit is
ratified.

---

### ACM-G7 — Shared positive: neither resurrects a second membership authority

**Applies to:** both  
**Classification:** non-blocking (positive / confirmatory)

HEAD probes independently confirm the builders' P1–P5 / validator-gap claims:

- `artifact-package.v1` member `role` enum admits rules/parameters/lineage-style
  tokens and `operation-semantics` only — **not** `form-field`,
  `source-family`, `source-closure-mapping`, `composition`, or `fact-type`.
- `package_validation.py` checks schema validity, pin presence, role agreement
  (rules/parameters), scope match, parameter/table expression refs, and output
  ownership — **not** `binds_symbol`, family/mapping, composition, or ELX
  bindings.
- `loader.ROLE_VOCABULARY` matches that enum set (no form-field / composition /
  source-family tokens).
- Committed packages pin rules only:
  `package.first-tax-slice` → wages rule only;
  `package.interest-slice` → B1 subtotal rule only; co-located form-field and
  B1 family/mapping sit outside membership.

Both designs close **those** gaps by extending the pin table and validator
dispatch, not by inventing a parallel path manifest. That is the correct
governance posture for ACM-P1 relative to ADR-0006 and Article 4/9 (adoption of
versioned declared machinery).

---

### ACM-G8 — ADR-0025 already fixed `input_bindings` shape; both designs correctly inherit it

**Applies to:** both  
**Classification:** non-blocking (confirmatory; prevents re-litigation)

ADR-0025 decision 4 already requires `artifact-package.v2` to declare
unambiguous `input_bindings` with `mode: "required" | "optional_default"`, and
decision 1 places `optional_default` on `fact-type.v2` (determinable scalar
only; elective rejects). Both designs implement that surface rather than
redesigning ELX package bindings. ACM must not re-open ELX mechanism choices;
it only owns **membership closure and load-time joins** over those bindings.
Both do.

---

## Verdicts

| Proposition | Design | Verdict |
|---|---|---|
| **ACM-P1** | **it1** | **Conditionally accept.** Extend-not-fork is sound and correctly grounded in HEAD package/validator gaps. Conditions: resolve **ACM-G1** (fact-type/bundle version-pinning prerequisite); tighten **ACM-G5** Case-7 immutability from policy assertion to a named comparison mechanism. |
| **ACM-P1** | **it2** | **Conditionally accept.** Same extend-not-fork strength; stronger bidirectional closure (**ACM-G3**) and concrete package-instance immutability (**ACM-G5**). Conditions: resolve **ACM-G1**; drop or reconcile schema-byte checksum duplication (**ACM-G2**); define entrypoint root kinds for non-presentation packages (**ACM-G3** caveat). |
| **ACM-P2** | **it1** | **Conditionally accept.** Binding table covers every named join in the charter (form-field→symbol; composition pin→composition+bijection; family↔mapping↔subtotal; input_bindings→fact-type/parameter; rule refs→peers; admitted schema reject). Conditions: **ACM-G1** (fact-type pin resolution underpins ELX/form bindings); **ACM-G4** (mechanize role dual-meaning rejection). |
| **ACM-P2** | **it2** | **Conditionally accept.** Same binding-table strength; inbound reachability and named role-divergence codes are bonuses above the floor. Conditions: **ACM-G1**; **ACM-G4** (close per-package `content_role` escape); **ACM-G2** if schema contracts remain the admission vehicle. |

Neither design is rejected. Neither is production-ready without the shared
ACM-G1 prerequisite and the listed production conditions.

---

## Carry-forward recommendation

Carry a **hybrid**, not a clean pick of either exhibit:

- **From both (convergent floor):** `artifact-package.v2` extension of
  ADR-0006; form-field, source-family, source-closure-mapping, composition,
  operation-semantics, and fact-type/bundle surface in the closed pin graph;
  `composition` provenance-only; contained per-defect validation; non-silent
  schema-generation admission; non-vacuous composition and ELX joins.
- **From it2:** typed bidirectional closed-graph rule (outbound +
  entrypoint-rooted inbound); package-instance checksum immutability
  (`ACM_PACKAGE_VERSION_REWRITE` or equivalent); load-time role-semantic
  divergence check against a single role canon.
- **From it1:** simple `admitted_schemas` schema-id list (no embedded schema
  sha256); individual fact-type identity in binding joins once ACM-G1 lands.
- **Joint prerequisite before ADR-0027 ratifies the fact-type membership
  surface:** resolve ACM-G1 (`fact-type.v2` / `bundle.v2` version fields or an
  explicit alternate exact-identity rule reconciled with wholesale bundle
  adoption).

Treat ACM-G1, ACM-G2, and ACM-G4 as **open questions for the ADR-0027 author**,
not as settled by this round. Exact issue-code strings remain Gate-5 deferred.

Advisory only — the owner decides disposition.
