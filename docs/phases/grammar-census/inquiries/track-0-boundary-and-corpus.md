# Track 0 — Term Boundary and Bounded Corpus

- Phase: Grammar Census
- Milestone: Engine Language Map (`grammar-census`)
- Track: 0 — Term boundary and bounded corpus
- Status: complete
- Produced against: `HEAD` on `milestone/grammar-census-engine-language-map`,
  resolved at commit `0f8e078e37781a6d2a532b6cc638d0034b248b02`

This deliverable does not read
`docs/phases/claim-boundary-exploration/` (charter constraint). Where this
document independently rediscovers something that phase is reported to have
found (e.g. no canonical current core-package designation), the finding
below was reached from this repository's own evidence, not from that
phase's artifacts.

## Half one — the boundary map

The plan's `#Term boundary` names seven surfaces in the abstract. Below,
each is named against concrete repository paths, classified, and reasoned.

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
  `resolve_production_package`, ADR-0033); `packages/schemas/kernel/act-package-adoption.v1.schema.json`.
- **Classification: grammar proper.**
- **Reason:** ADR-0006 decisions 6–7 and ADR-0027/ADR-0033 treat package
  membership, closure, and exclusive-execution projection as declared
  contract, not incidental machinery — a package is itself a schema-typed
  citizen (`artifact-package.vN`) whose shape *is* part of what "the
  language" accepts as well-formed. It sits one layer above individual
  rules but is still declared, versioned content that the runtime enforces
  rather than merely executes.

### 5. Adjacent declarative predicate or validation languages

- **Concrete surface:** `packages/derivation/declarative_validation.py` —
  its own closed vocabularies `TERM_OPS = {field, literal, add, subtract,
  floor_zero}` and `PREDICATE_OPS = {field_present, field_absent,
  field_equals, field_not_equals, compare, all, any}`
  (`packages/derivation/declarative_validation.py:6-19`), with its own
  `MAX_PREDICATE_DEPTH` and its own error types (`GrammarError`,
  `MemberConstraintTooDeep`); used for structured-member constraints inside
  `attachment-rule.v6`/`v8` per ADR-0066, invoked only from
  `packages/derivation/runner.py`. Also: `packages/schemas/tax/attachment-rule.v1..v8.schema.json`
  and `packages/schemas/tax/form-field.v1..v3.schema.json` more broadly.
- **Classification: grammar proper for the attachment-rule/form-field
  citizen families themselves; grammar-adjacent for the
  `declarative_validation.py` term/predicate sub-vocabulary specifically.**
- **Reason:** attachment-rule and form-field are declared, schema-typed,
  separately versioned citizens with their own semantic effect
  (`packages/derivation/package_validation.py` role/schema checks;
  ADR-0036/ADR-0055/ADR-0056) — they are grammar proper by the same
  argument as #4. But the *internal* term/predicate mini-language
  `declarative_validation.py` defines is a second, smaller, independently
  closed expression grammar (its own op sets, its own depth limit, its own
  exception hierarchy) layered inside those citizens rather than reusing
  the core clause language from #1. It is grammar-adjacent because it is
  declarative and semantically load-bearing but is a structurally distinct
  vocabulary the census must not silently fold into surface #1's op list —
  Track 1a/1b must record it as its own construct family, not as
  additional `rule-artifact` operations.

### 6. Runtime behaviors that affect the meaning of a rule but may not themselves be grammar

- **Concrete surface:** `packages/kernel/findings.py` — `subset_invariant_pairs`,
  `declaration_signal_contradictions`, `companion_presence_pairs`,
  `companion_value_domains`, `companion_equality_pairs`
  (`packages/kernel/schema_registry.py:90-118` shows these as
  `SchemaRegistry` attributes a tax-layer registry populates and the kernel
  enforces generically); `packages/derivation/projection.py` /
  `packages/kernel/currency.py` displacement-closure folding
  (ADR-0010 decision 3); rounding-mode dispatch in
  `packages/derivation/evaluator.py:29-34`
  (`half_up`/`half_even`/`down`/`up`).
- **Classification: grammar-adjacent.**
- **Reason:** these are semantic invariants (a box-1b ≤ box-1a subset rule,
  a companion-presence pair, a currency-displacement fold) that a
  *tax-layer registry populates as data* but that no `rule-artifact`
  citizen declares — the kernel enforces them generically "never naming a
  domain" (`packages/kernel/schema_registry.py:95,105,109`). The meaning of
  a published finding depends on them, but they are not expressed in the
  clause language itself; they live in registry-populated Python
  dictionaries, not in a schema-validated citizen. That is exactly the
  plan's own phrasing for this surface, and the evidence supports it
  directly rather than needing to be inferred.

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
  incidental logging. What survives execution is itself declared, versioned
  shape — the census's `#Census unit` field "what provenance or explanation
  information survives its execution" presumes exactly this surface exists
  as a citable artifact, and it does.

### An eighth surface the seven do not name

- **Concrete surface:** `packages/schemas/kernel/act.v1.schema.json` and the
  fact/entity/horizon act-kind family (`act-assertion.vN`,
  `act-entity-introduced.v1`, `act-entity-superseded.v1`,
  `act-member-transition.vN`, `act-horizon-genesis.v1`,
  `fact-type.v1..v3`, `family-horizon.v1`) — the kernel act-log substrate
  ADR-0002/ADR-0011/ADR-0017/ADR-0023 define, which every rule's `collect`
  and `ref` read against.
- **Classification: grammar-adjacent.**
- **Reason:** none of the seven named surfaces is "how a fact enters
  currency in the act log at all" — the plan's boundary is written from the
  rule-artifact side outward. The kernel act/fact/entity/horizon substrate
  is declared, schema-typed content that a rule-artifact's `ref`/`collect`
  presupposes but does not itself express (a rule never declares an act
  shape). It is closer to "the ground the language stands on" than to the
  language itself, so grammar-adjacent rather than proper — but Track 1a
  should not ignore it, since `#Census unit`'s "input and output types or
  domains" field cannot be answered without it.

### Uncertain classifications

None of the eight entries above is marked `uncertain`. Each had committed,
citable evidence (a schema family, a closed vocabulary in code, or an
ADR decision) sufficient to place it on one side of the grammar-proper /
grammar-adjacent line with a stated reason. Track 1 sub-tracks may
encounter individual constructs *within* these families whose
classification is less clear (for example a single field inside a
`rule-artifact.v3` citizen that reads like presentation metadata) — that is
a construct-level judgment for Track 1/2, not a boundary-level one for
Track 0.

## Half two — the bounded corpus

### Layer 1 — Accepted contracts and ADR decisions (`docs/adr/`)

- **In-scope artifacts:** `docs/adr/0001-*.md` through `docs/adr/0066-*.md`
  (67 numbered files) plus `docs/adr/INDEX.md` and `docs/adr/analyses/`.
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
  `docs/adr/INDEX.md` lines 33–101 (the status table).
- **Bounded corpus for the census:** every ADR marked `accepted` in
  `docs/adr/INDEX.md` (currently 0001–0003, 0006–0012, 0014–0017, 0020,
  0023–0029, 0031–0033, 0035–0038, 0041, 0044, 0046–0066, excluding the
  rejected/superseded/retired numbers named above). Retired/rejected/
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
  `form-field.v1..v3`). Each directory's `published.json` is the
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
    plausible trap this census must name explicitly: `packages/content/tax/2025/package.core-calculations.json`
    (no version suffix) is byte-identical to
    `packages/content/tax/2025/package.core-calculations.v1.json`'s
    *content* — `diff` against `package.core-calculations.v33.json` shows
    it is **not** the highest-numbered version; its internal `"version":
    "v1"` field and `"schema": "artifact-package.v2"` confirm it is the
    *first*, not the latest, package instance under an unversioned
    filename. The unversioned filename is therefore not a "current"
    marker at all; it is an old, differently-named copy of v1. This is
    exactly the trap the charter's "do not infer highest-numbered is
    current" instruction warns against, discovered in the opposite
    direction (an unversioned name that turns out to be the *oldest*, not
    a stand-in for the newest).
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

- **In-scope artifacts:** `packages/content/tax/2025/*.json` — 197 files
  whose `"schema"` field starts with `"rule-artifact` (confirmed by direct
  grep), plus `package.core-calculations.json` and
  `package.core-calculations.v1..v33.json` (34 files describing the same
  package family across versions), plus `package.first-tax-slice.json` and
  `package.interest-slice.json` (two package instances outside the
  `core-calculations` name entirely — evidence of at least three
  independently-named package lineages, not one accumulating series).
  `packages/sample_data/**` (34 top-level scenario directories, e.g.
  `dsbs_t1`, `frrs_t1`, `core_tax_conditions`,
  `capital_gain_distributions_line7a_t1`) carries fixture/example content
  distinct from `packages/content/`.
- **Canonical current designation:** **does not exist**, for the same
  reason established in Layer 2: no committed adoption act pins any one
  `package.core-calculations.vN` as the package in force, and the
  unversioned `package.core-calculations.json` is (independently
  discovered here) the *oldest* version's content under a bare filename,
  not a "current" stand-in. Say this plainly rather than guessing from the
  highest version number (`v33`) or the unversioned name.
- **Bounded corpus for the census:** Track 1c should treat
  `packages/content/tax/2025/rule.*.json` as the primary observed-usage
  corpus for individual rule constructs (197 files, one rule per file,
  named by their own `id`/`schema`/`version` fields — no package-level
  filtering needed for construct-level observation), and should record
  `package.core-calculations.v33.json` — the highest-numbered version, but
  cited as "highest-numbered, not claimed current" — as the package-shape
  reference for questions about closure/membership *if* a package-level
  reading is needed, with the caveat spelled out above attached wherever it
  is cited. `packages/sample_data/**` is a secondary, explicitly synthetic
  corpus (declared in `#Fixtures`: "no fixtures created" by this milestone,
  reusing what exists) — Track 1c may cite it for representative usage but
  should distinguish it from `packages/content/` in every citation, since
  one is production-shaped tax content and the other is test scaffolding.

### Layer 5 — Tests and synthetic executions that demonstrate observable behavior

- **In-scope artifacts:** `tests/` in full — 6 top-level subdirectories
  (`tests/derivation/`, `tests/source_completeness/`, and four more) plus
  79 top-level `test_*.py` files (e.g. `tests/test_dsbs_t1_schema_citizens.py`,
  `tests/test_core_tax_conditions_track1_contract_schemas.py`,
  `tests/test_schema_registry.py`,
  `tests/test_frrs_t1_boundary_contribution_schemas.py`); the golden/fixture
  generator scripts under `tools/generate_*.py` (31 files, e.g.
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
  (46 files); the six phase roadmap files under `docs/phases/*/`:
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
- **Bounded corpus for the census:** all of the above. One explicit
  exclusion, restated from the charter rather than newly discovered here:
  `docs/phases/claim-boundary-exploration/` is out of bounds for this
  track by charter instruction, and Track 1 sub-tracks are told by the plan
  itself (`#Claim-boundary evidence posture`) not to read that phase's
  inquiry corpus either. Its *roadmap* file
  (`docs/phases/claim-boundary-exploration/claim-boundary-exploration-roadmap.md`)
  was not read by this track, consistent with that instruction, even though
  the plan's Layer 6 language ("roadmap entries") would otherwise include
  it; Track 2/3, which the plan permits to use merged Claim Boundary
  artifacts as a bounded validation lens, should decide whether that
  roadmap file counts as "the inquiry corpus" the posture excludes or as
  ordinary Layer-6 history — this track takes no position and flags it as
  an open question rather than resolving it unilaterally, since the plan
  says Track 0 does not own that call.

## Representational gaps (recorded, not stop conditions)

1. **`artifact-package` version-acceptance ranges are not contiguous with
   the schema-file series.** `package_validation.py`'s universe guard
   applies only to `artifact-package.v3`–`v17` (17 versions), while other
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
   misleading by construction** — it is v1's content under a bare name,
   not a "latest" alias. Nothing in the schema or tooling enforces that an
   unversioned filename tracks the newest version; this is a naming
   convention risk for future content, not a defect this track can fix
   (out of scope — no production content change permitted).
4. **`declarative_validation.py`'s term/predicate vocabulary has no
   published schema of its own.** It is a closed vocabulary in Python
   (`TERM_OPS`, `PREDICATE_OPS`), not a JSON Schema citizen the way
   `rule-artifact`'s operation vocabulary is implicitly bounded by its
   schema's `enum`/`$defs`. Track 1a (schema reading) should expect to find
   no schema-level enumeration of this vocabulary and should read the code
   directly instead, per the boundary-map entry above; recorded here so
   that absence is not mistaken for an oversight when Track 1a goes
   looking for it in `packages/schemas/`.
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
- The plan's `#Claim-boundary evidence posture` names Track 1 sub-tracks as
  independent of Claim Boundary Exploration's *conclusions* but does not
  say whether that phase's *roadmap file* (as opposed to its inquiry
  corpus under `docs/phases/claim-boundary-exploration/inquiries/` or
  similar) is in or out of bounds for this milestone's Layer 6. This track
  declined to read it and flags the ambiguity rather than resolving it
  (see Layer 6 above); the Foreman or Track 2/3 should settle it
  explicitly rather than leaving each future stream to guess.
- Nothing else in the plan's read sections appears wrong or unworkable from
  this track's reading; the corpus bounded above is sufficient to produce a
  trustworthy census, with the caveats named above.
