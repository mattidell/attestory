# Track 0 — Term Boundary and Bounded Corpus

- Phase: Grammar Census
- Milestone: Engine Language Map (`grammar-census`)
- Track: 0 — Term boundary and bounded corpus
- Status: complete
- Revision history (this file only):
  - original (boundary map and bounded corpus): `990888c2`
  - round 1 (Layer 4 corpus corrections): `ad2bbe27`
  - round 2 (boundary map re-derivation): `9104aa48`
  - round 3 (Foreman ruling on 5b-ii; two flagged inconsistencies): this commit

This deliverable does not read
`docs/phases/claim-boundary-exploration/` (charter constraint). Where this
document independently rediscovers something that phase is reported to have
found (e.g. no canonical current core-package designation), the finding
below was reached from this repository's own evidence, not from that
phase's artifacts.

## Half one — the boundary map

**Repair note (round 2, 2026-08-19/20).** The previous revision of this
section carried a binary grammar-proper/grammar-adjacent label reasoned from
at least five different, unstated criteria applied inconsistently across the
eight entries, and it resolved two source-contradicted entries silently. This
revision states one primary criterion, applies it evenly, records five
orthogonal axes per surface in a table so downstream readers inherit the
axes and not only the label, and splits surface 6 into its three unlike
components. While re-verifying the citation for surface 5's mini-language
(required because the previous revision's citation for that surface was
directly load-bearing for its classification), this revision found that
citation was itself wrong in a way neither the original map nor the
external critique's source verification caught — see surface 5b below. That
is the one classification change in this round that neither the charter nor
the critique anticipated; it is reported prominently rather than folded
in silently, per the standard this repair exists to enforce.

**Repair note (round 3, 2026-08-20).** The Foreman ruled 5b-ii
(`MAX_PREDICATE_DEPTH = 6`) grammar proper; that is the only
classification change in this round. Representational-gaps item 4 was
wrong and is replaced with a discoverability point. A new
tension-catalog candidate records that the depth bound is two
independent literals plus ADR prose. Round 2's other classifications
are untouched.

The plan's `#Term boundary` names seven surfaces in the abstract. Below,
each is named against concrete repository paths, classified against one
stated criterion, and its axes recorded.

### The primary criterion

**A surface is grammar proper when it is declared in a schema-typed,
separately versioned citizen, and that citizen either (a) constrains what a
rule-artifact — or a citizen that composes or extends rule-artifacts, such
as a package, an attachment-rule/form-field citizen, or a source-family
declaration — may accept as well-formed or express as compositional
structure, or (b) is the schema-typed shape a rule-artifact's execution is
contractually required to produce as its own record. A surface is
grammar-adjacent when no schema-typed citizen declares it at all, or when
the citizen it does have is instead the data substrate — the store: acts,
facts, entities, horizons — that such content reads or writes without being
reshaped by it.**

This is one criterion in two clauses, not two criteria: "schema-typed
citizen" alone is necessary but not sufficient, because the store side
(surface 8) can be exactly as rigorously schema-typed and ADR-contracted as
the language side and still not be part of what the clause language itself
can express. The module-versus-store distinction the round-2 charter asked
this document to evaluate explicitly is folded into the criterion itself
(clause (a) vs. the store exception), rather than bolted on afterward to
rescue a naive schema-only test. Applied naively (schema-typed citizen,
full stop, no store exception), the test would call surface 8 proper and
would leave surfaces 7 and 8 indistinguishable, since both have schema-typed
citizens; **this document does not adopt that naive form**, for the stated
reason. The cost of not adopting it: "is there a schema" is not, by itself,
a sufficient answer, so a reader cannot mechanically classify a new surface
from a schema listing alone — they must also decide which side of the
module/store line it sits on, which is a judgment this document makes
explicitly per surface below rather than leaving implicit.

### Axes table

Recorded for every surface and sub-surface, per the round-2 charter's
minimum axis set. "Rel." is the surface's relationship to a rule-artifact:
**expressed** (the citizen itself is the expression tree or a declared
field of one), **presupposed** (a rule reads against it but never declares
its shape), or **produced** (it is the schema-typed record a rule's
execution is contractually required to leave behind).

| # | Surface | Schema-typed citizen? | Rel. | Changes value/disposition? | Closed expr. grammar? | ADR-fixed? | Label |
| - | --- | --- | --- | --- | --- | --- | --- |
| 1 | Core clause/expression language | Yes — `rule-artifact.v1..v6` | expressed | Yes | Yes | ADR-0006, ADR-0025, ADR-0064 | **proper** |
| 2 | Dependency/guard/role/blocking | Yes — `rule-artifact.vN` fields; blocking codes in `derivation-record.v2..v7`/`npe-walk.v1..v3`/`checked-conclusion-binding.v1` | expressed | Yes | Yes (closed named set) | ADR-0006/0007/0009/0024/0037 | **proper** |
| 3 | Operation-semantics | Yes — `operation-semantics.v1`, `.v2` | presupposed by a rule's op name, expressed as its own citizen | Yes | Yes (closed op set) | ADR-0006 decision 4 | **proper** |
| 4 | Package selection/binding/closure | Yes — `artifact-package.v1..v25` | expressed by the package citizen; presupposed by any one rule-artifact inside it | Yes | No (constraint set, not an expression syntax) | ADR-0006 decisions 6-7, ADR-0027, ADR-0033 | **proper** (module side) |
| 5a | attachment-rule/form-field family | Yes — `attachment-rule.v1..v8`, `form-field.v1..v3` | expressed | Yes | Yes | ADR-0036/0055/0056/0066 | **proper** |
| 5b-i | declarative_validation.py term/predicate vocabulary | **Yes — `source-family.v2.schema.json` `$defs/term`, `$defs/predicate`** | expressed (as `member_constraints[].violated_when` / `identity_exclusivity[].components` of a source-family declaration) | Yes | Yes (own bounded op set) | ADR-0066 decision 2 | **proper (reversed)** |
| 5b-ii | declarative_validation.py depth bound (`MAX_PREDICATE_DEPTH=6`) | **No — enforced at resolver admission by contract, not by JSON Schema (ADR-0066 decision 2, deliberate)** | presupposed by schema (not a declared field); well-formedness bound on 5b-i at package admission and at evaluation | Yes (admission `MEMBER_CONSTRAINT_TOO_DEEP`; evaluation `MemberConstraintTooDeep`) | N/A (a limit, not a vocabulary) | ADR-0066 decision 2 (names the number 6 in prose) | **proper (Foreman ruling)** |
| 6i | Domain axioms (`findings.py` invariant pairs) | No | presupposed generically, kernel "never naming a domain" | Yes | No (data pairs, not expression syntax) | none found | **adjacent** |
| 6ii | Currency/projection displacement-closure | No — `DECLARED_EDGE_KINDS` is a Python frozenset | produced around already-published findings; store-side | Yes | No (two fixed edge kinds) | ADR-0010 decisions 3, 5, 6 | **adjacent** (store side) |
| 6iii | Rounding-mode dispatch | **Yes — `operation-semantics.v1.schema.json`, same citizen as #3** | presupposed by a rule's `round` op name | Yes | Yes (closed enum) | ADR-0006 decision 4 | **proper (reversed, contradiction fixed)** |
| 7 | Provenance/disposition/explanation record | Yes — `npe-walk.v1..v3`, `derivation-record.v1..v7` | **produced** — this is the plan's own definition of surface 7 | Yes (walk failure/nonpublication is itself a recorded disposition) | Yes | ADR-0009, ADR-0020 | **proper** |
| 8 | Kernel act/fact/entity/horizon substrate | Yes — `act.v1`, `act-assertion.vN`, `act-entity-introduced.v1`, `act-member-transition.vN`, `act-horizon-genesis.v1`, `fact-type.v1..v3`, `family-horizon.v1`, **and `act-package-adoption.v1`, corrected below** | presupposed — a rule's `ref`/`collect` reads against it, never declares its shape | No (it is the input domain, not itself a value-changing behavior) | No | ADR-0002, ADR-0011, ADR-0017, ADR-0023, ADR-0033 (for adoption acts) | **adjacent** (store side, despite satisfying the schema clause alone) |

### 1. The core rule-artifact clause and expression language

- **Concrete surface:** `packages/schemas/derivation/rule-artifact.v1..v6.schema.json`
  (the `when`/`value` expression-tree shape); the closed operation
  vocabulary interpreted by `packages/derivation/evaluator.py` (`ref`,
  `collect`, `count`, `block`, `parameter`, `add`, `subtract`, `multiply`,
  `divide`, `max`, `compare`, `all`, `any`, `not`, `choose`, `round`,
  `range_lookup`, `bracket_fold`, `require_closed`, `categorical_compare`,
  `category_literal`, `collect_categorical_all_equal`,
  `conditional_dependency_set` — `packages/derivation/evaluator.py:108-246`).
- **Classification: grammar proper.**
- **Reason:** this is the closed expression tree ADR-0006 establishes and
  ADR-0025/ADR-0064 extend (arithmetic ops, categorical comparison); it is
  the thing every other surface below either constrains, interprets, or
  produces consequences from. It is the plan's own reference point for
  "the language."

### 2. Dependency, guard, applicability, value, publication, and blocking semantics

- **Concrete surface:** the `when` guard field and `role` values
  (`computation`, `applicability`, `field-mapping`, `cross-form-bridge`,
  `_RULE_ROLES` in `packages/derivation/package_validation.py:189`) declared
  in `rule-artifact.vN`; the blocking-code vocabulary
  (`BLOCK_ABSENT`/`DEPENDENCY_ABSENT`, `BLOCK_INVALID`/`DEPENDENCY_INVALID`,
  `BLOCK_CLOSURE`/`SOURCE_SET_UNCLOSED`, `BLOCK_LOOKUP_MISS`,
  `BLOCK_CATEGORICAL_DOMAIN_MISMATCH` — `packages/derivation/evaluator.py:22-27`);
  guard-false → `guard_result: False` / `inapplicable` disposition handling
  in `packages/derivation/runner.py:486-496,1212-1227`; publication act
  construction (`packages/derivation/runner.py`, ADR-0007).
- **Classification: grammar proper.**
- **Reason:** these are declared fields of the rule-artifact citizen itself
  (guard is part of the schema; role is a schema enum) whose meaning is
  fixed by ADR-0006/ADR-0007/ADR-0009/ADR-0024/ADR-0037, not incidental
  runtime plumbing. The blocking-code vocabulary is a closed, named set the
  schema and runner both carry, not an implementation detail invented at
  evaluation time.

### 3. Operation-specific semantic specifications

- **Concrete surface:** `packages/schemas/derivation/operation-semantics.v1.schema.json`,
  `operation-semantics.v2.schema.json`; the operation-semantics canon object
  passed into the evaluator's environment
  (`packages/derivation/evaluator.py:70`, `canon: dict[str, dict[str, Any]]`);
  loaded and pinned at `packages/derivation/loader.py:51,71,137-160`; pinned
  into every publication (`role: "operation-semantics"` at
  `packages/derivation/runner.py:388`).
- **Classification: grammar proper.**
- **Reason:** the plan's own `#Evidence layers` and `#Census unit` treat
  "separately versioned" semantics as a first-class question, and this
  citizen is exactly that: it is what ADR-0006 calls out as deferring an
  operation's *meaning* to a separately versioned, separately cited
  artifact rather than baking a convention into the evaluator. It is
  declared content with its own schema family, cited on every publication —
  not a runtime behavior.

### 4. Package selection, binding, closure, and output-ownership rules

- **Concrete surface:** `packages/schemas/derivation/artifact-package.v1..v25.schema.json`;
  `packages/derivation/package_validation.py` (closure checks, unique
  output ownership, reachability, universe guard, non-confusion invariants);
  `packages/derivation/production_resolver.py` (`select_current_adoption`,
  `resolve_production_package`, ADR-0033) as the runtime consumer of
  adoption facts.
- **Classification: grammar proper (module side).**
- **Reason:** ADR-0006 decisions 6–7 and ADR-0027/ADR-0033 treat package
  membership, closure, and exclusive-execution projection as declared
  contract, not incidental machinery — a package is itself a schema-typed
  citizen (`artifact-package.vN`) whose shape *is* part of what "the
  language" accepts as well-formed, governing how a set of rule-artifacts
  compose. It sits one layer above individual rules but is still declared,
  versioned content that the runtime enforces rather than merely executes.
- **Corrected citation.** The previous revision cited
  `packages/schemas/kernel/act-package-adoption.v1.schema.json` as a
  concrete surface for this entry. That schema's own title is "Package
  adoption act payload" — it is a member of the act family surface 8
  classifies grammar-adjacent, not a package-shape citizen. It is removed
  from this entry and correctly filed under surface 8 below. What remains
  proper here is the package *schema* (`artifact-package.vN`) and the
  closure/binding logic that reads it; the *adoption act* recording which
  package version is currently in force is a store-side fact about the act
  log, produced at runtime by `production_resolver.py:select_current_adoption`
  but not itself part of what a package or rule-artifact may express.

### 5. Adjacent declarative predicate or validation languages

- **Concrete surface — attachment-rule/form-field family:**
  `packages/schemas/tax/attachment-rule.v1..v8.schema.json` and
  `packages/schemas/tax/form-field.v1..v3.schema.json`.
- **Classification: grammar proper.**
- **Reason:** these are declared, schema-typed, separately versioned
  citizens with their own semantic effect
  (`packages/derivation/package_validation.py` role/schema checks;
  ADR-0036/ADR-0055/ADR-0056) — grammar proper by the same argument as #4.

- **Concrete surface — `declarative_validation.py`'s term/predicate
  vocabulary:** `packages/derivation/declarative_validation.py` — its own
  closed vocabularies `TERM_OPS = {field, literal, add, subtract,
  floor_zero}` and `PREDICATE_OPS = {field_present, field_absent,
  field_equals, field_not_equals, compare, all, any}`
  (`packages/derivation/declarative_validation.py:6-19`).
- **Classification: grammar proper — reversed from the previous revision
  and from the round-2 charter's own carried-forward finding.**
- **Reason, and the citation correction that drives it.** The previous
  revision (and the external critique's source verification, Q1) both
  stated this vocabulary is used for structured-member constraints inside
  `attachment-rule.v6`/`v8` and is "Python only," present in no
  attachment-rule schema. Neither claim survives checking the actual call
  site. `declarative_validation.py` has exactly one caller,
  `packages/derivation/runner.py:653-707`, and it evaluates
  `declaration["member_constraints"]` and `identity_exclusivity`, which
  come from `self.ctx.family_declarations` — **source-family declarations,
  not attachment-rule content.** ADR-0066 decision 1 states this in so many
  words: "Structured-member constraints belong to versioned source-family
  content" (`docs/adr/0066-declarative-structured-validation-and-consumer-closure.md:35-36`).
  The vocabulary itself is schema-declared: `source-family.v2.schema.json`'s
  `member_constraints[].violated_when` field is `$ref: "#/$defs/predicate"`,
  and `$defs/term`/`$defs/predicate` enumerate, as `const` values, exactly
  `field`, `literal`, `add`, `subtract`, `floor_zero` (term) and
  `field_present`, `field_absent`, `field_equals`, `field_not_equals`,
  `compare`, `all`, `any` (predicate) —
  `packages/schemas/derivation/source-family.v2.schema.json:66,97,171-469`
  (`member_constraints` at 66, `identity_exclusivity` at 97, `$defs` at
  171-469 with `term` at 172 and `predicate` at 278).
  ADR-0066 decision 2 confirms this is the intended, closed language: "The
  predicate language is closed and bounded," naming the same term and
  predicate forms verbatim
  (`docs/adr/0066-declarative-structured-validation-and-consumer-closure.md:47-53`).
  By this document's primary criterion (schema-typed, separately versioned
  citizen, expressed within a citizen that composes/extends rule-artifact
  content), this vocabulary is grammar proper. It is a second, smaller
  expression grammar nested inside the source-family citizen rather than
  reusing the core clause language from #1 — Track 1a/1b must still record
  it as its own construct family, not as additional `rule-artifact`
  operations, but "structurally distinct" is no longer the reason it is
  adjacent, because it is not adjacent.
- **Classification of the depth bound (`MAX_PREDICATE_DEPTH = 6`):
  grammar proper — Foreman ruling, 2026-08-20; reversed from
  `uncertain`.** ADR-0066 decision 2 states, in the same sentence
  introducing the closed language: "Resolver admission rejects predicate
  depth greater than six; JSON Schema is not claimed to enforce recursive
  depth by itself"
  (`docs/adr/0066-declarative-structured-validation-and-consumer-closure.md:54-56`).
  Round 2 marked this **uncertain**: the schema-typed-citizen axis said
  adjacent (the ADR disclaims schema enforcement) and the ADR-fixed axis
  said proper (the number 6 is a named decision). **Foreman ruling:
  proper.** The reasoning this entry must carry:

  - Clause (a) of the stated primary criterion asks whether the surface
    constrains what a rule-artifact — or a citizen that composes or
    extends one, such as a source-family declaration — may accept as
    well-formed or express as compositional structure. A depth bound of
    six on `member_constraints[].violated_when` is exactly a constraint
    on what a `source-family.v2` citizen may express. It meets that
    clause on its own terms.
  - The `uncertain` arose from reading the schema-typed-citizen axis as
    a test of *whether the rule is part of the declared language*, when
    it is a test of *which mechanism enforces it*. ADR-0066 decision 2
    states both facts in one sentence (quoted above), which is a
    deliberate allocation of enforcement, not a disclaimer of contract.
  - **Round 2 missed an enforcement site.** The bound is enforced at
    package admission: `packages/derivation/package_validation.py:2037`
    defines its own `MAX_PREDICATE_DEPTH = 6`, and `:2051-2056` rejects
    deeper predicates with issue code `MEMBER_CONSTRAINT_TOO_DEEP`. That
    is the same admission gate that makes surface 4 grammar proper — a
    package carrying an over-deep predicate is refused before it can
    execute. The bound is therefore enforced by contract, twice, on the
    module side of the module/store line: admission
    (`package_validation.py:2037,2051-2056`) and evaluation
    (`packages/derivation/declarative_validation.py:20`, raising
    `MemberConstraintTooDeep` at `:62` and `:87`).
  - Splitting 5b-i and 5b-ii would place a closed vocabulary and its
    own well-formedness rule on opposite sides of the boundary, on the
    strength of a mechanism difference the ADR made on purpose.

  The "Schema-typed citizen?" axis stays **No — enforced at resolver
  admission by contract, not by JSON Schema (ADR-0066 decision 2,
  deliberate)**. The label follows clause (a) of the primary criterion,
  not that axis. **This is a Foreman ruling on a question the axes did
  not settle by themselves, not a mechanical result.** A reader who
  rejects the enforcement-versus-declaration distinction would reach
  `adjacent` instead. Exit criterion 4 requires that disagreement stay
  visible, not that the ruling erase it.

### 6. Runtime behaviors that affect the meaning of a rule but may not themselves be grammar

This surface concatenated three unlike components in the previous revision.
Split here, each classified on its own evidence.

- **6i — Domain axioms.** `packages/kernel/findings.py` —
  `subset_invariant_pairs`, `declaration_signal_contradictions`,
  `companion_presence_pairs`, `companion_value_domains`,
  `companion_equality_pairs` (`packages/kernel/schema_registry.py:90-118`
  shows these as `SchemaRegistry` attributes a tax-layer registry populates
  and the kernel enforces generically).
  **Classification: grammar-adjacent (stands, confirmed).** These are
  semantic invariants (a box-1b ≤ box-1a subset rule, a companion-presence
  pair) that a *tax-layer registry populates as data* but that no
  `rule-artifact` citizen declares anywhere — the kernel enforces them
  generically, "never naming a domain"
  (`packages/kernel/schema_registry.py:95,105,109`). No schema anywhere
  carries this vocabulary; this is the one component the previous
  revision's stated reason actually fits.

- **6ii — Currency/projection displacement-closure folding.**
  `packages/derivation/projection.py` / `packages/kernel/currency.py`
  (ADR-0010 decisions 3, 5, 6); `DECLARED_EDGE_KINDS = frozenset({"derivation",
  "individuation"})` at `packages/kernel/currency.py:15`.
  **Classification: grammar-adjacent (store side).** No schema-typed
  citizen names these two edge kinds or the fold algorithm itself — they
  are a Python constant and a kernel algorithm, not declared content. Under
  this document's primary criterion, this is also the same store-side
  reasoning that keeps surface 8 adjacent: displacement-closure operates
  generically over the act log's derivation/individuation edges, regardless
  of which rule produced the input, the same way surface 8's substrate is
  read generically by `ref`/`collect` regardless of which rule reads it.
  It changes which findings are current — a strong signal on one axis — but
  it is not itself an expression vocabulary a rule composes; it is kernel
  machinery applied uniformly to the store.

- **6iii — Rounding-mode dispatch.** `packages/derivation/evaluator.py:29-34`
  (`half_up`/`half_even`/`down`/`up` mapped to Python `Decimal` rounding
  constants).
  **Classification: grammar proper — reversed, contradiction fixed.** The
  previous revision classed this grammar-adjacent on the stated ground that
  it lives in "registry-populated Python dictionaries, not a
  schema-validated citizen." That ground is false for this component:
  `packages/schemas/derivation/operation-semantics.v1.schema.json:26`
  enumerates exactly `half_up`, `half_even`, `down`, `up` as the `round`
  operation's mode enum — the identical citizen surface 3 above classifies
  grammar proper. `evaluator.py:29-34`'s dict is the runtime's mapping from
  the schema-declared enum name to a Python `Decimal` constant, not an
  independent, unschematised vocabulary; the previous revision read the
  runtime mapping and missed the schema it implements. This was one of two
  contradictions the round-2 charter identified as decided against source;
  fixed here by moving this component to proper rather than by marking it
  uncertain, since the schema citation settles it.

### 7. Provenance, disposition, and explanation consequences produced by execution

- **Concrete surface:** `packages/schemas/derivation/npe-walk.v1..v3.schema.json`
  (hardcoded target `"schema": "npe-walk.v3"` at
  `packages/derivation/explanation.py:332`); `packages/derivation/explanation.py`
  (`ExplanationNode`, the pin-traversal walker); disposition rows and
  `act_id` construction in `packages/derivation/runner.py:496,546,851,1148`;
  `packages/schemas/derivation/derivation-record.v1..v7.schema.json` and
  `packages/derivation/records.py` (`CURRENT_RECORD_SCHEMA`).
- **Classification: grammar proper.**
- **Reason:** ADR-0009's derived-finding shape puts authority in the
  attribution chain, and ADR-0020 makes every non-publication block a
  walkable ledger entry; both are contract decisions with their own
  schema-typed citizens (`npe-walk.vN`, `derivation-record.vN`), not
  incidental logging. Under this document's primary criterion, this surface
  satisfies clause (b) specifically: it is not content a rule-artifact
  composes from, it is the schema-typed record shape a rule-artifact's
  execution is contractually required to produce. The plan's own definition
  of this surface — "consequences **produced by** execution" — names exactly
  this relationship, distinct from surface 8's "presupposed by" relationship
  below. On the schema-typed-citizen axis alone, surfaces 7 and 8 tie (both
  have schema-typed citizens); the produced/presupposed distinction is what
  separates them, and it is not incidental phrasing — it is the same
  distinction the plan's own `#Term boundary` text draws between item 6
  ("runtime behaviors that affect meaning") and item 7 ("consequences
  produced by execution").

### An eighth surface the seven do not name

- **Concrete surface:** `packages/schemas/kernel/act.v1.schema.json` and the
  fact/entity/horizon act-kind family (`act-assertion.vN`,
  `act-entity-introduced.v1`, `act-entity-superseded.v1`,
  `act-member-transition.vN`, `act-horizon-genesis.v1`,
  `fact-type.v1..v3`, `family-horizon.v1`), **and
  `packages/schemas/kernel/act-package-adoption.v1.schema.json`** (moved
  here from surface 4, see the correction there — its own schema title is
  "Package adoption act payload," making it a member of this act family,
  not of the package-schema family) — the kernel act-log substrate
  ADR-0002/ADR-0011/ADR-0017/ADR-0023 define (ADR-0033 specifically for
  adoption acts), which every rule's `collect` and `ref` read against.
- **Classification: grammar-adjacent — decided by the store side of the
  primary criterion, not by absence of a schema.**
- **Reason.** This surface is schema-typed, exactly as rigorously as
  surfaces 4 and 7 — the naive form of a "declared in a schema" test alone
  would call it proper, which is exactly the collision the round-2 charter
  asked this document to resolve rather than default into. This document
  does not adopt that naive form. The reason it stays adjacent: none of the
  seven named surfaces is "how a fact enters currency in the act log at
  all" — the plan's boundary is written from the rule-artifact side
  outward — and the kernel act/fact/entity/horizon substrate is the data
  domain a rule-artifact's `ref`/`collect` reads against, not content the
  rule-artifact (or a package, or an attachment-rule/source-family citizen)
  composes or is contractually required to produce. It is presupposed, in
  the same sense surface 6ii's displacement-closure fold presupposes the
  act log without reshaping it. Track 1a should not ignore it on account of
  the adjacent label — `#Census unit`'s "input and output types or domains"
  field cannot be answered without it.
- **What adopting the module/store cut costs, stated explicitly per the
  round-2 charter's instruction.** A fully schema-typed, ADR-contracted
  citizen family (the acts) is classified adjacent here. "Declared in a
  schema" is therefore necessary but not sufficient under this document's
  criterion — a reader cannot classify a new surface from a schema listing
  alone; they must also decide which side of the module/store line it sits
  on. The alternative (schema-typed citizen, full stop) is simpler and
  would make surfaces 4, 7, and 8 all proper, but it would also erase the
  distinction between "content that shapes what a rule may express" and
  "content a rule merely reads," which is exactly the distinction Track 2's
  eventual declared-vs-implemented-vs-used reconciliation needs intact.
  This document judges that cost acceptable and the module/store cut
  worth adopting; it is a documented judgment call, not a repository fact,
  and a downstream reader who disagrees can recover the naive-test answer
  directly from the "schema-typed citizen" column of the axes table above.

### Uncertain classifications

**Half one now carries zero `uncertain` entries, by Foreman ruling
rather than by silence.** Distinguish that from the original map's zero,
which resolved collisions silently with no axes and no residual
disagreement. The round-2 revision of this section left exactly one
entry uncertain — 5b-ii, the depth bound — and resolved every other
contested pair with a stated tiebreak (module/store for 4-vs-8 and
6ii-vs-8; produced/presupposed for 7-vs-8; the corrected schema
citation for rounding; the corrected `source-family.v2` citation for
5b-i). It did not claim a total of zero; it asked for a Foreman ruling
on 5b-ii. That ruling landed in round 3: 5b-ii is **grammar proper**.
The remaining axis disagreement is still visible in the 5b-ii row
(schema-typed citizen: No; ADR-fixed: Yes) and in the entry's note that
a reader who rejects the enforcement-versus-declaration distinction
would reach `adjacent` instead. Exit criterion 4 (`#Exit criteria`
item 4 of this milestone's plan) requires that disagreement stay
visible, not that the ruling erase it.

No entry is now marked `uncertain`. Track 1 sub-tracks may still
encounter individual constructs *within* these families whose
classification is less clear (for example a single field inside a
`rule-artifact.v3` citizen that reads like presentation metadata) —
that is a construct-level judgment for Track 1/2, not a boundary-level
one for Track 0.

## Half two — the bounded corpus

### Layer 1 — Accepted contracts and ADR decisions (`docs/adr/`)

- **In-scope artifacts:** `docs/adr/0001-*.md` through `docs/adr/0066-*.md`
  (**66** numbered files; method: `ls docs/adr/*.md | grep -v INDEX | wc -l`)
  plus `docs/adr/INDEX.md` and `docs/adr/analyses/`.
  Per `docs/adr/INDEX.md:7-8,13-18`, only ADRs with `status: accepted` bind;
  `rejected`/`superseded`/`proposed`/`retired` are explicitly inert and
  never load as authority. The index itself flags: `0004` rejected; `0005`,
  `0013`, `0030`, `0039`, `0040`, `0042`, `0043` retired (process,
  consolidated by ADR-0045); `0018`, `0022`, `0034` superseded; `0019`,
  `0021` rejected/superseded. ADR-0045 (`docs/adr/INDEX.md:79`) states
  process ADRs have left the corpus entirely; product/contract ADRs are the
  only ones this census should read as authority.
- **Canonical current designation:** **yes, exactly, and explicitly.** The
  status column in `docs/adr/INDEX.md` *is* the committed adoption record
  for this layer — it names every ADR's current status and, per its own
  text, is the "normative home for its own routing rules." Cite:
  `docs/adr/INDEX.md` lines 35–100 (the 66 status-table rows; line 33 is
  the table header). Tallied from that table: **53 accepted, 7 retired,
  3 superseded, 2 rejected, 1 proposed** — 66 total.
- **Bounded corpus for the census:** every ADR marked `accepted` in
  `docs/adr/INDEX.md` — currently 0001–0003, 0006–0012, 0014–0017, 0020,
  0023–0029, 0031–0033, 0035–0038, 0041, **0044–0066** (53 ADRs; note
  ADR-0045 is `accepted`, not retired: it is the *last* process ADR and it
  retired the other seven, so it binds while they do not). The complement,
  never cited as present-tense authority, is exactly: 0004 and 0019
  (rejected); 0018, 0022, 0034 (superseded); 0021 (proposed); 0005, 0013,
  0030, 0039, 0040, 0042, 0043 (retired). Retired/rejected/
  superseded ADRs remain readable as history (several are cited by number
  above in the boundary map, e.g. as "ADR-0033" naming the mechanism
  ADR-0066 partially superseded) but are never cited as present-tense
  authority for a construct's current meaning.

### Layer 2 — Every published rule-artifact and operation-semantics schema version relevant to the current engine

- **In-scope artifacts:** `packages/schemas/derivation/*.schema.json` (rule
  language: `rule-artifact.v1..v6`; `operation-semantics.v1..v2`; plus the
  neighboring families `artifact-package.v1..v25`, `derivation-record.v1..v7`,
  `derived-finding.v1..v2`, `dividend-universe.v1..v4`, `npe-walk.v1..v3`,
  `source-closure-mapping.v1..v2`, `source-family.v1..v2`, and the
  singly-versioned citizens); `packages/schemas/kernel/*.schema.json`
  (`fact-type.v1..v3`, `quantity-vocabulary.v1..v12`, `act-*.vN`, etc.);
  `packages/schemas/tax/*.schema.json` (`attachment-rule.v1..v6,v8` — note
  v7 does not exist, confirmed by directory listing;
  `form-field.v1..v3`). Every version enumeration in this paragraph was
  re-verified by globbing the schema directories and parsing the version
  integer out of each filename; all are contiguous from v1 except
  `attachment-rule`, whose gap at v7 is real.

  **Two independent version axes (read this before Track 1a or 1b builds a
  construct history).** A content citizen carries *both* its own `version`
  field *and* a `schema` field naming the schema version it validates
  against, and these move independently. The clearest case is the package
  family: `package.core-calculations` runs `version` v1→v33 (33 instances,
  32 successive steps) while its `schema` moves separately
  `artifact-package.v2`→`v25`, changing at only **19 of those 32 steps**
  and touching **20 distinct** schema versions (e.g. package v22–v25 all
  sit on `artifact-package.v19`; package v1, v2 and v3 all sit on
  `artifact-package.v2`). A census that reads "v33" as "artifact-package
  version 33" — or that assumes the two counters advance together — will
  produce a wrong construct history. Always state which axis a version
  number is on.
  checksum/publication manifest (`packages/kernel/schema_registry.py:68-155`):
  it verifies every `*.schema.json` file present is listed and every listed
  file's bytes are unmutated; a file present-but-unlisted or listed-but-
  missing is a hard registry error at load time. It is a **completeness and
  immutability manifest, not a current-version selector** — it lists every
  published version, not one chosen version.
- **Canonical current designation: does not exist as a single version per
  family, with one named exception.**
  - **No single-version selection for `rule-artifact`:** runtime code
    accepts the full six-version set simultaneously as a closed literal
    (`_RULE_ARTIFACT_SCHEMAS` / `_SUPPORTED_SEMANTIC_SCHEMAS` in
    `packages/derivation/package_validation.py:188-190,283-288`;
    identical acceptance sets repeated in `packages/derivation/marshal.py:105`,
    `packages/derivation/live.py:101`, `packages/derivation/runner.py:187-188,1414-1415`).
    `SchemaRegistry.validate_declared` (`packages/kernel/schema_registry.py:234-244`)
    validates every instance against **the version it names itself** — there
    is no "current" schema version a rule is validated against; the
    instance's own `schema` field selects the validator. This matches the
    plan's caution about the core package (`#Current state`,
    `docs/phases/grammar-census/milestones/engine-language-map.md:129-134`)
    and independently extends the same finding to `rule-artifact` schema
    versions specifically.
  - **No single-version selection for `artifact-package`:** twenty-five
    schema versions exist; `package_validation.py:1320-1321,1534-1548`
    hard-codes acceptance ranges that are not simply "the latest" (a
    universe-guard check applies to v3–v17 only, at
    `packages/derivation/package_validation.py:1527-1548`, because that
    guard postdates ADR-0035 and predates whatever later versions changed
    the check). Production adoption (`packages/derivation/production_resolver.py:134-208`,
    `select_current_adoption`, ADR-0033) selects a **current user
    adoption act** at runtime from the act log — an operational, per-run
    fact, not a static "this package version is current" designation
    committed anywhere in the repository. No committed
    `act-package-adoption.v1` fixture in `packages/sample_data/` or
    `tests/` names `tax.us.2025.package.core-calculations` as adopted
    (checked: `grep -rl "act-package-adoption" packages/sample_data tests`
    returns only `packages/sample_data/frrs_t1/examples/fixture-provenance-manifest.v1.json`
    and `tests/test_frrs_t1_boundary_contribution_schemas.py`, neither
    naming that package). This independently confirms, from this
    repository's own evidence and without reading the Claim Boundary
    corpus, that no committed artifact designates a current core package.
  - **Named exception — `derivation-record`:** `packages/derivation/records.py:40`
    declares `CURRENT_RECORD_SCHEMA = "derivation-record.v7"` as an actual
    committed constant, with an inline changelog explaining what each of
    v3–v7 added (`packages/derivation/records.py:33-39`). This *is* a
    genuine, citable, per-artifact current-version designation — the one
    place in the schema/semantics layer where "current" is a real, single
    answer rather than an accepted set. Cite exactly:
    `packages/derivation/records.py:40`.
  - **Do not infer the unversioned filename is current, either.** A
    plausible trap this census must name explicitly:
    `packages/content/tax/2025/package.core-calculations.json` (no version
    suffix) **is package version v1** — not by comparison against a
    `.v1.json` file, because **no `package.core-calculations.v1.json`
    exists**. The versioned-filename series begins at v2 and runs
    contiguously to v33 (32 files), so the unversioned filename *is* the
    v1 slot: the file declares `"version": "v1"` and
    `"schema": "artifact-package.v2"` internally. Method: parse the
    `version` and `schema` fields out of every
    `package.core-calculations*.json` rather than reading filenames.
    The unversioned filename is therefore not a "current" marker at all;
    it is the *oldest* member of the series under a bare name, because the
    versioning convention started one version late. This is exactly the
    trap the charter's "do not infer highest-numbered is current"
    instruction warns against, met in the opposite direction — a name that
    looks like a "latest" alias and is in fact the earliest instance.
- **Bounded corpus for the census:** for `rule-artifact` and
  `attachment-rule`, the census's declared/implemented construct sets
  (Tracks 1a/1b) should read **every version currently accepted by runtime
  code**, i.e. the literal sets named above
  (`_SUPPORTED_SEMANTIC_SCHEMAS` and its sibling literals in
  `package_validation.py`, `marshal.py`, `live.py`, `runner.py`) — this is
  the actually-executable grammar, and it is defensible because it is
  exactly what the runtime will accept, not a guess. For `operation-
  semantics`, both `v1` and `v2` (both accepted per
  `package_validation.py:267-268,980-983`). For `artifact-package`, the
  full v1–v25 family with the version-range caveats named above (the
  universe-guard v3–v17 boundary in particular) recorded as a
  representational note for Track 1a, not resolved here. For
  `derivation-record`, `derivation-record.v7` (`CURRENT_RECORD_SCHEMA`) as
  the one genuinely current version, with v1–v6 recorded as superseded
  history per the inline changelog. `form-field.v1..v3` and
  `quantity-vocabulary.v1..v12` are in scope in full; no code inspected in
  this track singles out a current version for either, so absent further
  evidence Track 1a should read all published versions of each and record
  the same "no current designation found" note this track records for
  `rule-artifact`.

### Layer 3 — Runtime evaluators, validators, resolvers, and other consumers

- **In-scope artifacts:** `packages/derivation/evaluator.py`,
  `declarative_validation.py`, `package_validation.py`,
  `production_resolver.py`, `production_executor.py`, `marshal.py`,
  `runner.py`, `reference_runner.py`, `loader.py`, `source_authority.py`,
  `projection.py`, `presentation_projection.py`, `surface_resolver.py`,
  `explanation.py`, `records.py`, `entry_loop.py`, `live.py`,
  `live_session.py`, `live_viewing.py`, `live_workspace.py`, and
  `packages/derivation/runners/derive.py`,
  `packages/derivation/runners/entry_loop_evaluation.py`; plus
  `packages/kernel/act_log.py`, `contribution.py`, `currency.py`,
  `facts.py`, `findings.py`, `horizons.py`, `read_models.py`,
  `schema_registry.py`, and `packages/kernel/runners/inspect_workspace.py`.
- **Canonical current designation:** **not applicable in the schema-version
  sense** — this layer is code, not versioned content, so "current" means
  "what is on this branch at the resolved commit," which is exactly what
  `git rev-parse HEAD` (`0f8e078e37781a6d2a532b6cc638d0034b248b02`) already
  fixes. There is no separate adoption record needed or expected for code.
- **Bounded corpus for the census:** every file listed above, as of the
  resolved commit. Track 1b should not additionally scope by directory
  wildcard at read time (e.g. "everything under `packages/derivation/`") —
  the presentation layer under `packages/presentation/pages` and the
  `packages/derivation/live*.py` family are runtime consumers of the
  grammar's *effects* (rendering, session/viewing machinery) more than of
  the grammar's *forms*; Track 1b should read them for completeness against
  `#Census unit`'s "runtime consumer" field but should expect thinner
  grammar content there than in `evaluator.py`/`package_validation.py`.

### Layer 4 — Actual committed rule content and packages (`packages/`)

- **In-scope artifacts:** `packages/content/tax/2025/*.json` — **538 files
  total**, of which **134** carry a parsed `schema` field beginning
  `rule-artifact` and **15** carry one beginning `attachment-rule`.
  **Method, so Track 1c can re-run it:** load each file as JSON and read
  its `schema` key; do not classify by filename (see the corpus definition
  below for why). The remaining files are the other citizen families in the
  same directory (74 `citation`, 53 `bundle`, 50 `form-field`, 49
  `source-closure-mapping`, 48 `source-family`, 35 `artifact-package`, 23
  `quantity-vocabulary`, 18 `parameter-declaration`, 4 `dividend-universe`,
  4 `taxable-interest-composition`, 1 each `role-canon`,
  `checked-conclusion-binding`, `migration-artifact`, plus 28 files with no
  top-level `schema` key at all).

  The package family is `package.core-calculations.json` plus
  `package.core-calculations.v2..v33.json` — **33 files, not 34**, because
  the versioned-filename series starts at v2 and the unversioned file
  occupies the v1 slot (see Layer 2). Also present:
  `package.first-tax-slice.json` and `package.interest-slice.json`, two
  package instances outside the `core-calculations` name entirely —
  evidence of at least three independently-named package lineages, not one
  accumulating series.

  `packages/sample_data/**` (**32** top-level scenario directories; method:
  `find packages/sample_data -maxdepth 1 -mindepth 1 -type d | wc -l` —
  e.g. `dsbs_t1`, `frrs_t1`, `core_tax_conditions`,
  `capital_gain_distributions_line7a_t1`) carries fixture/example content
  distinct from `packages/content/`.
- **Canonical current designation:** **does not exist**, for the same
  reason established in Layer 2: no committed adoption act pins any one
  `package.core-calculations.vN` as the package in force, and the
  unversioned `package.core-calculations.json` is (independently
  discovered here) the *oldest* version's content under a bare filename,
  not a "current" stand-in. Say this plainly rather than guessing from the
  highest version number (`v33`) or the unversioned name.
- **Bounded corpus for the census — define it by parsed `schema` field,
  never by filename glob.** The obvious shortcut,
  `packages/content/tax/2025/rule.*.json`, is **wrong for this census**,
  and wrong in precisely the place the boundary map cares about. That glob
  returns 140 files, which is exactly 134 `rule-artifact` + 6
  `attachment-rule` — the six being
  `rule.attachment.schedule-1.json`, `rule.attachment.schedule-1.v2.json`,
  `rule.attachment.schedule-b.json`, `.v2.json`, `.v3.json`, and
  `.v4.json` (schemas `attachment-rule.v4, v4, v1, v2, v2, v6`). Those six
  belong to the adjacent predicate/validation family that surface 5 of the
  boundary map insists must stay distinct from the core clause language.
  Using the glob would silently merge the two families in the one stream
  that is forbidden to cross-check this packet.

  The filename convention is unreliable in both directions: the
  `attachment-rule` family is split across *two* naming conventions — 6
  files named `rule.attachment.*.json` and 9 named `attachment.*.json`
  (`attachment.f8949.json`, `.v2`, `attachment.schedule-a.json`,
  `attachment.schedule-d.json`, `.v2`–`.v6`). Neither prefix identifies the
  family; only the parsed `schema` field does.

  So: **Track 1c's primary observed-usage corpus for core clause-language
  constructs is the 134 files whose parsed `schema` begins
  `rule-artifact`.** The 15 files whose parsed `schema` begins
  `attachment-rule` are a **separate, separately-reported corpus**,
  recorded under the adjacent-language surface (boundary map #5) and never
  merged into the `rule-artifact` construct counts. Track 1c should also
  record `package.core-calculations.v33.json` — the highest-numbered
  *package* version (its schema is `artifact-package.v25`; see the
  two-axes note in Layer 2), but
  cited as "highest-numbered, not claimed current" — as the package-shape
  reference for questions about closure/membership *if* a package-level
  reading is needed, with the caveat spelled out above attached wherever it
  is cited. `packages/sample_data/**` is a secondary, explicitly synthetic
  corpus (declared in `#Fixtures`: "no fixtures created" by this milestone,
  reusing what exists) — Track 1c may cite it for representative usage but
  should distinguish it from `packages/content/` in every citation, since
  one is production-shaped tax content and the other is test scaffolding.

### Layer 5 — Tests and synthetic executions that demonstrate observable behavior

- **In-scope artifacts:** `tests/` in full — **5** top-level subdirectories
  (exactly: `tests/conformance/`, `tests/derivation/`, `tests/helpers/`,
  `tests/source_completeness/`, `tests/tax/`) plus **76** top-level
  `test_*.py` files (79 top-level `.py` files in total; the other three are
  `tests/__init__.py`, `tests/conftest.py`, and `tests/support.py`, which
  are scaffolding, not tests). **127** `.py` files exist under `tests/`
  recursively. Examples: (`tests/test_dsbs_t1_schema_citizens.py`,
  `tests/test_core_tax_conditions_track1_contract_schemas.py`,
  `tests/test_schema_registry.py`,
  `tests/test_frrs_t1_boundary_contribution_schemas.py`); the golden/fixture
  generator scripts under `tools/generate_*.py` (**31** files —
  re-confirmed unchanged, e.g.
  `tools/generate_schedule_d_presentation_t3_goldens.py`,
  `tools/generate_dsbs_t2_content.py`) that produce committed synthetic
  execution output cited by tests.
- **Canonical current designation:** not applicable in the version sense —
  tests are not schema-versioned citizens; "current" is again "what is on
  this branch," same as Layer 3.
  A representational note, not a gap: `pytest.ini` at the repository root
  governs collection and is itself committed, so the corpus boundary
  ("what counts as a test") is not this track's invention — it is whatever
  `pytest.ini`'s configuration collects from `tests/`.
- **Bounded corpus for the census:** the full `tests/` tree plus
  `tools/generate_*.py`. Track 1c should distinguish, per file, whether a
  test exercises the runner end-to-end (an executed evaluation Track 2's
  representative traces can cite as "executed evidence") versus a static
  schema/contract check (structurally valid but not a semantic execution) —
  that distinction is exactly what `#Representative traces` needs and this
  track does not attempt to draw it file-by-file here, since doing so would
  begin the construct-level work reserved for Track 1c.

### Layer 6 — Historical extensions (ADRs, retrospectives, roadmap entries)

- **In-scope artifacts:** `docs/adr/` (same corpus as Layer 1, read here
  for its *history*, i.e. including retired/superseded/rejected entries,
  rather than for present authority); `docs/milestone-retrospectives/`
  (**46** files — re-confirmed unchanged); the **6** phase roadmap files
  under `docs/phases/*/` (re-confirmed unchanged), of which **5 are in
  scope** per the Foreman ruling below:
  `docs/phases/claim-boundary-exploration/claim-boundary-exploration-roadmap.md`,
  `docs/phases/engine-breadth/engine-breadth-roadmap.md`,
  `docs/phases/foundation/foundation-roadmap.md`,
  `docs/phases/grammar-census/grammar-census-roadmap.md`,
  `docs/phases/legible-entry/legible-entry-roadmap.md`,
  `docs/phases/real-return/real-return-roadmap.md`.
- **Canonical current designation:** not applicable — this layer is
  explicitly historical by the plan's own framing ("how the present
  language accumulated"); there is no "current retrospective" concept to
  look for.
- **Bounded corpus for the census:** all of the above, minus one explicit
  exclusion.

  **Foreman ruling (2026-08-19), recorded here as the Foreman's decision,
  not this track's.** Track 0 flagged the status of
  `docs/phases/claim-boundary-exploration/claim-boundary-exploration-roadmap.md`
  as an open question and declined to resolve it. The Foreman ruled:
  that file is **excluded from Layer 6 and from all of Track 1**. The
  reasoning given: Layer 6 exists to explain how the *grammar* accumulated,
  and that phase concerned explanation design and says nothing about
  grammar accumulation, so it earns no Layer 6 place on the merits; the
  Track 1 independence rule settles the remainder. It becomes available to
  **Tracks 2 and 3 only**, under the plan's bounded validation lens
  (`#Claim-boundary evidence posture`).

  Consistent with that ruling and with the charter,
  `docs/phases/claim-boundary-exploration/` was not read by this track at
  all. Layer 6's in-scope roadmap set is therefore the **5** remaining
  files: `engine-breadth`, `foundation`, `grammar-census`, `legible-entry`,
  and `real-return`.

## Representational gaps (recorded, not stop conditions)

1. **`artifact-package` version-acceptance ranges are not contiguous with
   the schema-file series.** `package_validation.py`'s universe guard
   applies only to `artifact-package.v3`–`v17` (**15** versions), while other
   checks in the same file range up to `v25`
   (`package_validation.py:1320-1321`). The corpus as defined (all
   published versions) cannot by itself tell a reader *which* semantic
   checks apply to which version without reading the validator's literal
   sets version by version — there is no single declared "feature matrix"
   citizen naming which checks apply to which package schema version. A
   later track could plausibly want such a matrix; recording it here as a
   tension-catalog candidate for Track 2, not resolving it.
2. **No committed adoption record for any `packages/content/` package.**
   Layer 4 above establishes this from local evidence. If a later census
   task needs to reason about "the package presently in force," the corpus
   has no artifact to point to; that gap is real and is recorded, not
   invented around.
3. **The unversioned `package.core-calculations.json` filename is
   misleading by construction** — it declares `"version": "v1"` internally
   and is the oldest member of the series, because the versioned-filename
   convention started at v2 and no `.v1.json` file was ever written. It is
   not a "latest" alias. Nothing in the schema or tooling enforces that an
   unversioned filename tracks any particular version; this is a naming
   convention risk for future content, not a defect this track can fix
   (out of scope — no production content change permitted).
4. **Discoverability: the term/predicate vocabulary lives in a citizen
   whose name does not suggest it.** The previous wording of this item
   was **wrong**. It said `declarative_validation.py`'s term/predicate
   vocabulary "has no published schema of its own" and instructed Track
   1a to expect no schema-level enumeration and to read the code instead.
   Round 2 established the opposite: the vocabulary is schema-typed at
   `packages/schemas/derivation/source-family.v2.schema.json` `$defs/term`
   (line 172) and `$defs/predicate` (line 278), referenced from
   `member_constraints[].violated_when` (lines 83-85,
   `"$ref": "#/$defs/predicate"`). Track 1a **should** find this
   vocabulary in `packages/schemas/`, under `source-family.v2` rather
   than under any `attachment-rule` schema, which is where a reader
   would naively look. No schema-absence gap survives. What remains is
   discoverability: the closed expression grammar sits inside
   `source-family.v2`, a citizen whose name does not suggest a
   term/predicate language, and it does not appear under
   `attachment-rule`. Recorded so Track 1a does not miss it by looking
   in the obvious place.
5. **No schema-level enumeration was found for the kernel act/fact/entity
   substrate's relationship to rule-artifact `ref`/`collect` targets** —
   i.e., nothing in `packages/schemas/derivation/rule-artifact.vN.schema.json`
   itself constrains which `fact-type` ids a `ref` may legally name; that
   constraint, if it exists, lives in runtime validation
   (`source_authority.py`, `package_validation.py`) rather than in the
   rule-artifact schema. This is consistent with the boundary map's eighth
   surface being marked grammar-adjacent rather than proper, and is
   recorded as a tension-catalog candidate (a declared-vs-implemented
   question) for Track 2, not resolved here.
6. **Filename prefixes do not identify citizen families in
   `packages/content/tax/2025/`.** The `attachment-rule` family is split
   across two naming conventions (`rule.attachment.*.json` and
   `attachment.*.json`), and the `rule.*.json` prefix spans two distinct
   families (`rule-artifact` and `attachment-rule`). Any tooling or stream
   that classifies this content by filename will mis-bin it; only the
   parsed `schema` field is authoritative. Recorded as a tension-catalog
   candidate — a plausible next action is the optional census tool the plan
   permits (`tools/grammar_census.py`), which would make the schema-field
   classification reproducible rather than re-derived per stream.
7. **Two independent version axes on every content citizen** (`version` vs
   `schema`), documented in Layer 2. Nothing mechanically ties them, and
   nothing warns a reader that "v33" names the package axis rather than the
   schema axis. Recorded as a tension-catalog candidate for Track 2; the
   consequence is a wrong construct history if a stream conflates them.
8. **`MAX_PREDICATE_DEPTH = 6` is declared twice as two unrelated
   literals, plus a third time in ADR prose.**
   `packages/derivation/declarative_validation.py:20` defines the
   evaluator's runtime guard (raising `MemberConstraintTooDeep` at `:62`
   and `:87`). `packages/derivation/package_validation.py:2037` defines
   its own `MAX_PREDICATE_DEPTH = 6` at the admission gate (rejection at
   `:2051-2056`, issue code `MEMBER_CONSTRAINT_TOO_DEEP`). ADR-0066
   decision 2 names the number a third time in prose
   (`docs/adr/0066-declarative-structured-validation-and-consumer-closure.md:54-56`:
   "Resolver admission rejects predicate depth greater than six").
   Nothing ties the three together — they are not a shared constant —
   so the admission gate and the evaluator can silently diverge.
   Track 2 tension-catalog candidate. Not fixed here; this milestone
   changes no production code.

## What this track suggests may be wrong, missing, or unworkable for Tracks 1a–1c

- The plan's `#Term boundary` numbering (seven surfaces) does not name the
  kernel act/fact/entity/horizon substrate at all, even though `#Census
  unit`'s "input and output types or domains" field cannot be answered for
  any rule construct without it. This track adds it as an eighth,
  grammar-adjacent surface (see above) rather than silently folding it into
  one of the seven; Tracks 1a–1c should expect to cite it and should not
  read its absence from the plan's list as license to skip it.
- The plan's Layer 2 wording ("every published rule-artifact and
  operation-semantics schema version relevant to the current engine")
  presupposes a "current engine" concept that, per this track's findings,
  does not correspond to a single schema version per family for either
  `rule-artifact` or `artifact-package`. "Relevant to the current engine"
  is workable only under the reading this track adopts here: *relevant* =
  *accepted by the runtime's own literal acceptance sets*, not *most
  recent*. Tracks 1a/1b should use that reading explicitly rather than
  re-deriving it, since the plan's phrasing alone would not settle it.
- The plan's `#Claim-boundary evidence posture` did not say whether that
  phase's *roadmap file* (as opposed to its inquiry corpus) fell inside
  this milestone's Layer 6. This track declined to resolve it; **the
  Foreman has since ruled it excluded** from Layer 6 and all of Track 1,
  available to Tracks 2–3 only. See the ruling recorded under Layer 6. No
  further action is needed from Track 1 streams beyond honoring it.
- The plan's `#Census unit` asks for "representative committed uses
  (citations, not paraphrase)" per construct, but the content directory
  offers no reliable way to bin files by family short of parsing each one
  (gap 6). Tracks 1a and 1c should budget for a parse pass rather than a
  glob, or propose the optional census tool to the Foreman as the plan's
  `#Parallel Work Manifest` requires (streams propose it; they do not
  commit `tools/grammar_census.py` themselves).
- Nothing else in the plan's read sections appears wrong or unworkable from
  this track's reading; the corpus bounded above is sufficient to produce a
  trustworthy census, with the caveats named above.

## Verification note on this document's counts

Every count in this document was produced by a command stated alongside it
and re-verified against the tree at the repair commit. Counts of committed
JSON content are taken from the **parsed `schema` field**, never from
filenames; counts of files are taken from `ls`/`find` with the exact
predicate shown. An earlier revision of this document reported three counts
that did not reproduce (a rule-artifact file count, a package-family file
count, and a claim of byte-identity against a file that does not exist);
those are corrected above, and the surrounding numbers were re-checked by
the same method rather than assumed. Where a number is awkward to
reproduce, the method is stated inline so a cold reader can re-run it
instead of trusting it.
