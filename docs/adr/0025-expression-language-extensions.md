# ADR 0025 — Expression Language Extensions: Declared Optional Defaults and Categorical Comparison

- Status: proposed
- Tier: 2
- Date: 2026-07-14

## Context

ADR-0024 settled conditional selection in the existing rule language but left
two contract gaps explicitly delegated to this topic (its decisions 5–6): rules
have no declared way to default an optional scalar input (demographic flags must
be asserted even as zero), and guards cannot compare categorical values without
coercing them to decimals (filing status is carried as numeric-string codes
"1"–"5"). The `expression-language-extensions` prototype addressed both.

Two independently authored, clean-room-separated designs (incumbent exhibit
`a9e4b9c`, rival exhibit `b2b9022`) converged on the shape and diverged only on
mechanism. Two independent-context committee reviewers (Governance ELX-G1–G6,
Adversary ELX-A1–A8) unanimously carried the **rival** design forward for both
propositions and rejected the incumbent's two distinctive mechanisms on
concrete governance and counterexample grounds. Evidence:
`docs/prototypes/expression-language-extensions/evaluation-analysis.md` and the
reviews and exhibits it cites.

## Decision

**ELX-P1 — declared optional default for scalar inputs.**

1. **A `determinable` optional scalar fact type may declare one adopted
   parameter default.** The default is versioned, declared content
   (`optional_default` on `fact-type.v2`, pinning a `parameter-declaration`) —
   never runner-resident policy (Article 11). Static cross-validation requires
   `nature: "determinable"`, a single scalar `value_schema`, a default parameter
   value valid under that schema, and the fact type's normal free supersession
   policy. An **elective** fact cannot declare a default; that is an intentional
   schema rejection preserving Article 3 / E3.1, not a fallback.

2. **The default is published as a marked derived finding sharing the input's
   `fact_id`.** At a run's fixed revision the generic input resolver installs a
   current asserted finding if one exists (`origin: "assertion"`); otherwise, for
   an `optional_default` binding, it validates the declared parameter, publishes
   a default-resolution finding (a closed `resolved_input` branch on
   `derived-finding.v2` carrying the `fact_id` and `origin: "declared_default"`),
   and installs it; otherwise it emits the ordinary `DEPENDENCY_ABSENT` block.
   An asserted input is never overwritten.

3. **Displacement uses the existing correction fold — no new root class and no
   third edge.** Because the default-resolution finding shares the input's
   `fact_id`, a later assertion is an ordinary correction root that displaces it,
   and its consumers displace through the existing `input` derivation edges only.
   The rejected incumbent alternative (a `default_superseded` displacement root
   class) is not adopted: it required runner-resident symbol→fact mapping and
   left two default findings current on a package-upgrade default-value change
   (ELX-A1).

4. **Package bindings are adopted content.** `artifact-package.v2` declares one
   unambiguous `input_bindings` entry per symbol/fact type, `mode: "required"`
   (blocks on absence, as today) or `mode: "optional_default"` (valid only for
   the fact-type contract above). The generic runner supplies no field-name,
   tax-year, or value policy.

**ELX-P2 — categorical comparison.**

5. **A closed `categorical_compare` op compares two values of one declared
   string-enum domain, never as decimals.** Its operands are an existing fact
   type's versioned `value_schema` enum and a typed `category_literal` naming
   that fact type; package validation requires the same fact-type id/schema
   version and enum membership. Decimal `compare` remains numeric-only and gains
   no second interpretation. Supported operators are enum eq/ne only; ordering,
   case folding, aliases, and arbitrary strings are out of scope. One
   `operation-semantics.v2` citizen ships the op's semantics. The rejected
   incumbent alternative (a generic string `match` op) is not adopted: it
   silently returned false on invalid or cross-domain operands, violating E9.1
   (ELX-A3/A4).

6. **Mismatch is a contained, explained failure.** A run-time assertion outside
   the declared enum blocks `DEPENDENCY_INVALID`; a value whose domain differs
   from its categorical operand blocks `CATEGORICAL_DOMAIN_MISMATCH`; a
   statically knowable categorical-vs-numeric comparison is rejected at package
   validation (`MEMBER_SCHEMA_INVALID`). No coercion, fallback, or repair.

7. **ADR-0024's interim numeric codes migrate by governed successor claim.**
   Migration is append-only: publish the label fact type and a versioned
   code-to-label mapping artifact; present a successor label claim citing the old
   code and the mapping; the user asserts the presented successor (no silent
   conversion of a human finding, Article 2); ordinary succession displaces the
   legacy fact and its dependents. New categorical rules reject legacy code
   bindings rather than dual-reading them.

## Consequences

- ADR-0024 content written under its interim decisions 5–6 upgrades under this
  ADR: demographic optional scalars gain declared defaults, and filing status
  moves from numeric-string codes to a first-class categorical domain via the
  decision-7 migration.
- New schema versions are introduced (`fact-type.v2`, `artifact-package.v2`,
  `derived-finding.v2` `resolved_input` branch, pin-schema `default` role and
  `input`-pin `origin` field, `rule-artifact.v2` categorical forms,
  `operation-semantics.v2`); v1 content remains valid historical content.
- **PC1.** The `input`-pin `origin` field is required and copied transitively so
  any consumer states default-vs-assertion provenance locally (ELX-G3/ELX-A2).
- **PC2.** `CATEGORICAL_DOMAIN_MISMATCH` is a new disposition reason; adding it
  (and confirming `DEPENDENCY_INVALID` covers enum-invalid assertions) amends the
  ADR-0012 disposition vocabulary and the disposition/explanation contracts.
- **PC3.** This is paper-settled at HEAD, not executed. Production remains
  conditional on mixed-family correction-fold validation for default-resolution
  findings, two-runner parity, schema/package negatives, and the five Gate 2
  cases as synthetic fixtures.

## Alternatives Considered

- **`default_superseded` displacement root class (incumbent it1).** Rejected:
  runner-resident symbol→fact mapping (Article 11); multi-default collision on
  package upgrade (ELX-A1).
- **Separate `optional-input-declaration.v1` citizen (incumbent it1).**
  Rejected: duplicative, weaker static enforcement than `fact-type.v2` (ELX-G2).
- **Generic string `match` op (incumbent it1).** Rejected: tolerant-reader
  silent-false on invalid/cross-domain operands, violating E9.1 (ELX-A3/A4).
- **Unspecified milestone-time categorical migration (incumbent it1).**
  Rejected: admits silent conversion / dual-reading of human findings (Article
  2) (ELX-A5).

## Links

- Evidence: `docs/prototypes/expression-language-extensions/evaluation-analysis.md`;
  `reviews/round-1-governance.md`, `reviews/round-1-adversary.md`; exhibits
  `it1/design.md` (`a9e4b9c`), `it2/design.md` (`b2b9022`).
- Resolves the interim decisions 5–6 delegated by ADR-0024.
- Contracts: ADR-0006 (rule language), ADR-0007–0010, ADR-0012 (dispositions),
  ADR-0009 (derived findings). Governance: Articles 2, 3, 7, 11; E3.1, E9.1.
