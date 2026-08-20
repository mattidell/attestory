# Track 2b-ii — Tension catalog

- Phase: Grammar Census
- Milestone: Engine Language Map (`grammar-census`)
- Track: 2b-ii — tension catalog
- Role: Builder
- Status: complete
- Source ref verified: `HEAD` `c889f7ca918cd39ed6fa1c5a1303a929979e1592`
  on `milestone/grammar-census-engine-language-map`
- Assigned path: this file only
- Primary input: `docs/phases/grammar-census/inquiries/track-2-reconciliation.md`
  (166 constructs at `f276cc5b`)
- Also read: Track 0 representational gaps 1–8 in
  `docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md`;
  Foreman correction
  `docs/reviews/2026-08-20-grammar-census-foreman-correction-5b-ii-ruling-reasoning.md`

This catalog is limited to tensions that could plausibly support later
action. It is not a defect list. Several census findings are deliberate
contract choices; those are named under `#Intentional, not catalogued as
tensions` rather than padded in. Entries the census surfaced that do not
support later action are named under `#Considered and dropped`.

Cite the reconciliation (`U-###`, `D#`, surviving questions) and source
checked against it. Do not cite the sibling traces deliverable.

## Method

1. Start from Track 2's 17 disagreements, eight surviving open questions,
   and Track 0's eight representational-gap records. Treat a reconciled
   row as a strong lead, not as established fact.
2. For anything placed at the centre of an entry, re-check source in this
   worktree and show the check under `#Source checks this stream ran`.
3. Rank by consequence, not by how surprising the finding is. The ranking
   question is: if Track 3 and the owner read only the top of this list,
   which mismatch would most change what they believe about the engine,
   or most change a later grammar/code/ADR unit?
4. Classify every admitted entry as one of:
   - **contract vs enforcement** — a published ADR or schema says
     something the running engine does not do. The project believes
     something untrue about itself. Remedy is: change the code to match
     the contract, or amend the contract to match the code. That is an
     owner call.
   - **two implementations** — two code paths (or a code path and a
     leftover constant) disagree. The contract may be silent or
     satisfied by one of them. Remedy is to pick a path, delete a
     leftover, or version the pair. Also an owner call, but a different
     one.
   - **expressiveness** — the language cannot say a thing the engine
     still needs, or one layer collapses a distinction another layer
     keeps. Not a disagreement. The phase exists in part to surface
     these.
5. Do not assume unused declared forms are dead weight. A reserved
   extension point is not a tension.

JSON Schema's refusal to encode recursive predicate depth is **not**
this catalog's T1. ADR-0066 decision 2 allocated that enforcement away
from JSON Schema on purpose (`docs/adr/0066-declarative-structured-validation-and-consumer-closure.md:54-56`).
T1 is the narrower, realised fact that admission does not do what that
same decision says admission does.

## Ranking

The charter named three candidates of visibly different weight. They
are not equally consequential, and they are not the only load-bearing
ones.

| Rank | Entry | Class | Why this rank |
| --- | ---: | --- | --- |
| 1 | T1 predicate-depth bound | contract vs enforcement | A published ADR sentence is false of admission for every arithmetic/comparison tree. Packages can admit trees the evaluator then refuses. Realised, not latent. The Foreman correction calls this the most consequential single finding of the milestone so far. |
| 2 | T2 attachment-rule.v5 `$id` collision | contract vs enforcement (published identity) | Two published schema files claim one `$id` with different bytes; the v5 file's constraints never validate an instance. ADR-0003 identity is broken for that pair. Ranked below T1 because no committed content hosts `attachment-rule.v5` (U-088), so current packages do not hit the catch-22 — the harm is to the published-schema contract and to any future instance that would name v5. |
| 3 | T3 blocking-code identity collapse | two implementations + expressiveness | Evaluator-native codes (`LOOKUP_MISS`, `FAMILY_VALIDATION_BLOCKED`) and later record codes (`SLI_*`) do not survive onto the walk the user-explanation path can legally carry. This is happening on every v2 ledger path, not waiting for a deep tree or a v5 instance. Ranked below T2 because the remap is an implemented, contained policy, not a published-identity collision — but it is more user-facing than a dead constant. |
| 4 | T4 `selected_producer` vs first-publisher-wins | two implementations (ADR reading uncertain) | Admission uses `selected_producer` to *permit* two publishers; the runner never reads the field. Current committed conflict is guard-partitioned, so production content may not presently race. The language still has two rules. |
| 5 | T5 `bracket_fold` canon unread | contract vs enforcement | ADR-0006 decisions 3–4 say versioned canon is the runtime authority for the fold; the evaluator loads `spec` and ignores every field. 95 committed occurrences. |
| 6 | T6 unread clause `blocked` field | two implementations (authored vs emitted) | Schema-required field the runner does not consume. Authors write two strings as if they were conditions. |
| 7 | T7 `OPERATION_VOCABULARY` leftover | two implementations (dead constant vs live dispatch) | The charter's third named candidate. 14 names, never called; the dispatcher is 23 ops. Misleading to a reader of `loader.py`. Not a gate. Lowest of the three named candidates, and below T3–T6, because nothing in the running engine consults it. |
| 8 | T8 tax-id kill-tests in Python | expressiveness | Package language has no content form for exclusive-graph axioms, so they live as Python frozensets of tax citizen ids. |
| 9 | T9 `ref`/`collect` names unconstrained by rule-artifact schema | expressiveness | Track 0 gap 5. Possibly intentional given surface 8 is grammar-adjacent. |

T7 is the leftover-vocabulary candidate the charter asked to weigh against
T1 and T2. It loses that comparison: a constant no code calls cannot
make the project wrong about a published contract (T1) or make a
published schema file unreachable (T2). It can only mislead a reader
who treats `loader.py:86-103` as the language.

## T1. ADR-0066 decision 2 is not enforced as written at admission (U-124, D4)

**Class:** contract vs enforcement.

**Intentional?** The *allocation* of depth enforcement away from JSON
Schema is intentional. ADR-0066 decision 2
(`docs/adr/0066-declarative-structured-validation-and-consumer-closure.md:54-56`):
"Resolver admission rejects predicate depth greater than six; JSON Schema
is not claimed to enforce recursive depth by itself." Track 0 gap 8's
original wording treated duplicated literals as a latent hazard. The
Foreman correction and Track 2 S2/V4 established that the two *algorithms*
already diverge. Nothing in the ADR, the schema, or a comment on
`_predicate_depth` claims that walking only `args` is the intended
admission rule. This stream treats the allocation as intentional and the
algorithm split as **not established as intentional**.

**Evidence.**

- Contract: ADR-0066 decision 2, quoted above. No issue code is named.
  `source-family.v2.schema.json` `$defs/predicate` has no max-depth keyword
  (grep of that file for `maxDepth` / `max_depth` is empty). That absence
  matches the ADR.
- Admission: `packages/derivation/package_validation.py:182-188`
  `_predicate_depth` recurses through `args` only; a node without a list
  `args` returns 1. The gate at `:2037-2056` compares that number to a
  local `MAX_PREDICATE_DEPTH = 6` and emits `MEMBER_CONSTRAINT_TOO_DEEP`.
- Evaluation: `packages/derivation/declarative_validation.py:20,61-88`
  starts at depth 1 and increments on nested `add`/`subtract`/`floor_zero`
  (`left`/`right`/`value`) and on nested predicates. Same integer, different
  tree walk.
- Observed: content max depth 2 (U-124). A committed test already documents
  the split:
  `tests/derivation/test_declarative_validation_runtime.py:243-250`
  (`test_deeply_nested_term_blocks_not_raises`) states that
  `_predicate_depth` "does not recurse into a `compare` predicate's
  `left`/`right` *term* tree" and that a chain nested past the bound
  "passes content validation undetected and only raises at evaluation time."
- This stream re-ran `compare(add^n(field, 1), 0)` against member `{x: 1}`
  (shown under `#Source checks this stream ran`). Admission depth stays 1
  for every n; the evaluator raises `MemberConstraintTooDeep` at n≥5.

**Affected layer.** Surface 5b (term/predicate language) and the
admission gate that Track 0 used to classify 5b-ii as grammar-proper.
Net census label does not move (Foreman correction: 5b-ii stays
`proper`). The supporting sentence that admission "refuses [an over-deep
predicate] before it can execute" is false for term trees.

**Possible user or maintenance consequence.** A package author can
commit a `violated_when` tree that package admission accepts and that
evaluation then refuses with `CONSTRAINT_EVALUATION_FAILED` /
`MemberConstraintTooDeep`. Reviewers who trust the ADR sentence will
believe such a tree cannot enter a package. Committed content does not
presently exercise the hole (max observed depth 2), so this is not a
current-content incident; it is a false contract about a gate.

**Remaining uncertainty.** Whether admission should walk `left`/`right`/`value`
the way the evaluator does, or the evaluator should only count `args`, is
Track 2 surviving question 5. This census does not choose. Whether any
historical package instance already carries a tree deeper than six on the
term axis was not exhaustively re-walked here; Track 1c's content-max-2
and this stream's spot re-run are the evidence.

**Plausible next action.** Owner-selected unit: either change
`_predicate_depth` to walk the same keys the evaluator walks, or amend
ADR-0066 decision 2 to describe what admission actually does (depth of
`all`/`any` `args` nesting, not term-tree depth). Do not do either in
this milestone. A shared constant would still be insufficient by itself —
that is the methodological point of the Foreman correction.

## T2. Two published schema files claim one `$id` with different bytes (U-089)

**Class:** contract vs enforcement of published identity (ADR-0003 /
Article 9), not a two-implementation disagreement. The registry's
filename-keyed dispatch is internally consistent. What is false is the
implication that the file named `attachment-rule.v5.schema.json` is the
schema whose `$id` and instance discriminator are `attachment-rule.v5`.

**Intentional?** Not established as intentional. Track 2 V8 and the
Foreman-verified facts treat this as a finding. No ADR names a
deliberate `$id` reuse across published files.

**Evidence.**

- `packages/schemas/tax/attachment-rule.v3.schema.json` `$id` is
  `tax/attachment-rule.v3` (file line 116).
- `packages/schemas/tax/attachment-rule.v5.schema.json` `$id` is
  `tax/attachment-rule.v3` (file line 120). Its
  `properties.schema.const` is `attachment-rule.v3` (line 229).
- The files are not byte-identical.
  `packages/schemas/tax/published.json` records distinct checksums:
  v3 `5b3f219879095db2…`, v5 `aecd3bf51c16fac9…`. This stream hashed
  both files; they match those prefixes and differ.
- Registry keys by filename stem (`packages/kernel/schema_registry.py:152`,
  `path.name.removesuffix(".schema.json")`). `validate_declared`
  (`:234-244`) dispatches on the instance `schema` string. `$id` is
  dropped in-memory for `$ref` resolution (`:172-175`) and is not the
  dispatch key.
- Consequence of that dispatch, already settled by Track 2 resolved
  question 6 / V8: an instance naming `attachment-rule.v3` validates
  against the **v3 file**. An instance naming `attachment-rule.v5`
  validates against the v5 file, whose const requires `attachment-rule.v3`
  — a catch-22. The v5 bytes never run. `_SUPPORTED_SEMANTIC_SCHEMAS`
  still lists `attachment-rule.v5` (U-076).
- Observed: 15 attachment-rule content files; **no content host v5**
  (U-088). Hosts are v4×7, v6×2, v8×2, v2×2, v3×1, v1×1. There is no v7
  (S6). Never classify by filename; parse `schema`.

**Affected layer.** Surface 5a (attachment-rule citizen) and the
published-schema identity contract. Not a runtime evaluator split.

**Possible user or maintenance consequence.** Anyone authoring
`"schema": "attachment-rule.v5"` cannot produce a valid instance. Anyone
reading the v5 file as the v5 contract is reading unreachable bytes. The
published set contains a file whose constraints are not selectable by
the instance discriminator the rest of the engine uses. Current 2025
content does not name v5, so this is not a present-package incident.

**Remaining uncertainty.** How the v5 file was published with a v3 `$id`
and const is not recoverable from the census. Whether a later unused
version should carry the v5 *bytes* under a unique `$id`, or whether v5
should remain unreachable published history, is the owner call. This
milestone must not edit, move, or replace either published file.

**Plausible next action.** Finding, not a repair. A later unit may
publish a new unused version filename (with matching `$id` and `schema`
discriminator) if the v5 bytes are still wanted as a live contract, or
may document v5 as unreachable published history. Do not mutate
`attachment-rule.v3.schema.json` or `attachment-rule.v5.schema.json`.
Do not hand-edit `published.json`.

## T3. Evaluator blocking codes do not survive onto the walk (U-045, U-046, U-047, U-132, U-135, D5, D14)

**Class:** two implementations (evaluator/runner codes vs ledger/walk
enums) **and** expressiveness (what user explanation cannot say). The
remap is real policy, not a misread. The walk family stopping at v3
while the record family runs to v7 is a grammar choice that limits
provenance.

**Intentional?** Partially. Derivation-record versions are additive
successors that widen the block-code enum (v7 description at
`derivation-record.v7.schema.json:285` names the three `SLI_*` codes as
the reason for that generation). npe-walk.v3
(`npe-walk.v3.schema.json:2-3`) is the last published walk generation
and explicitly "mirroring derivation-record.v4" for
`COMPLETENESS_VALUE_VIOLATION`. The v2 ledger remap of unknown codes to
`DEPENDENCY_INVALID` (`runner.py:1165-1183`) is implemented with a
comment that internal family-validation codes stay on `self.blocked`.
What is **not** established as intentional: that `LOOKUP_MISS` should
never appear on a ledger or walk (no ADR names the token — Track 2
surviving question 2); that `SLI_*` kept on the ledger should be
illegal on the walk.

**Evidence.**

- Evaluator emits `LOOKUP_MISS` (`evaluator.py:27`, alias
  `BLOCK_LOOKUP_MISS`). Runner emits `FAMILY_VALIDATION_BLOCKED` (U-047).
  Neither string is in `derivation-record.v7` enum
  (`derivation-record.v7.schema.json:123-136`, 12 codes) nor in
  `npe-walk.v3` `code` enum (`npe-walk.v3.schema.json:7`, 7 codes:
  `DEPENDENCY_ABSENT`, `DEPENDENCY_INVALID`,
  `CATEGORICAL_DOMAIN_MISMATCH`, `SOURCE_SET_UNCLOSED`, `VALUE_INVALID`,
  `ITEMIZATION_TIE_OUT_VIOLATION`, `COMPLETENESS_VALUE_VIOLATION`).
- On `use_v2`, `_record_blocked` keeps `code` only if it is in
  `record_codes`; otherwise writes `DEPENDENCY_INVALID`
  (`runner.py:1169-1183`). `self.blocked` keeps the internal code.
  Track 2 V7 remap, re-confirmed by reading that block in this
  worktree: `LOOKUP_MISS` → `DEPENDENCY_INVALID`;
  `FAMILY_VALIDATION_BLOCKED` → `DEPENDENCY_INVALID`;
  `SLI_MFS_INELIGIBLE` kept.
- Walker hardcodes `"schema": "npe-walk.v3"` (`explanation.py` per
  U-133). A v7 record code such as `SLI_MFS_INELIGIBLE` is not a legal
  walk `code`. Codes remapped to `DEPENDENCY_INVALID` *are* walk-legal.
- Tests assert `BLOCK_LOOKUP_MISS` (`test_runner.py:133-145` per U-046).
  Zero content files contain the `BLOCK_*` aliases (V9).
- ADR-0020 decision 7 (`docs/adr/0020-non-publication-explanation-walking.md:51`):
  walk-payload dispositions use the ADR-0012 vocabulary exactly, and
  `invalid` is a refinement of blocked, not a sibling. U-134:
  `invalid` is **not** an npe-walk `node_kind`. The walk `node_kind`
  enum is `published, blocked, guard_inapplicable, no_disposition_recorded`.

**Affected layer.** Surface 1/2 blocking (evaluator), surface 7
(derivation-record, npe-walk, explanation). User-explanation
consequence is the load-bearing part.

**Possible user or maintenance consequence.** A lookup miss and a
family-validation block both present as ledger/walk
`DEPENDENCY_INVALID`. An SLI hard-block that the ledger keeps as
`SLI_MFS_INELIGIBLE` cannot legally appear on the walk the explanation
surface publishes. A test that asserts the evaluator alias against a
v2 disposition row is asserting the pre-remap name. Maintainers adding
a new `block` op code must widen **both** the record enum and the walk
enum, or accept silent collapse / walk-illegality; nothing in the
schema families ties those two series together (D14: the pairing is
real and undeclared as a pair).

**Remaining uncertainty.** Surviving question 2: should `LOOKUP_MISS`
be added to derivation-record / npe-walk, or is remap the contract?
Surviving question 7 is the 5b-ii criterion residue, not this entry.
This stream did not re-run the walker against an SLI block; Track 2
resolved question 5 records that the walker emits whatever blocked code
it finds after remapping and does not `validate_declared` its result.

**Plausible next action.** Owner-selected unit: either publish npe-walk.v4
(or a named pairing contract) whose `code` enum is the current
derivation-record.v7 set, and decide whether `LOOKUP_MISS` /
`FAMILY_VALIDATION_BLOCKED` join that set or stay remapped; or amend
ADR-0020 to say the walk vocabulary is a *subset* of the ledger and
name the collapse. A golden that asserts the ledger code, not the
evaluator alias, would settle the test-side half of surviving
question 2.

## T4. `selected_producer` permits two publishers; the runner does not select (U-044, U-072, U-073, D1)

**Class:** two implementations (admission vs runner). Whether it is
also contract vs enforcement depends on how ADR-0027 decision 5's
"selects" is read; that reading is not settled here.

**Intentional?** Control flow is settled (Track 2 resolved question 11):
ADR-0006 decision 7 (`docs/adr/0006-rule-artifact-language.md:21`)
requires unique output ownership unless the package *declares* conflict
semantics as content. ADR-0027 decision 5
(`docs/adr/0027-adopted-content-manifests.md:36`) requires that a
form-field's `binds_symbol` have exactly one reachable producer **or**
a conflict-semantics rule that **selects** an adopted member producer,
and rejects a conflict entry that merely names a symbol. Neither
sentence says the runner must evaluate `selected_producer` as the
runtime winner. The runner does not (`runner.py` contains zero
occurrences of `conflict_semantics` or `selected_producer`; this stream
re-grepped). Whether that silence is a defect is surviving question 1.

**Evidence.**

- Admission unique-ownership: `package_validation.py:2020-2026` allows
  two publishers of a symbol when that symbol is in
  `declared_conflicts` (the set of `conflict_semantics[].symbol`).
  Form-field producer integrity at `:1076-1080` requires
  `selected_producer` to name a member id when multiple producers
  exist.
- Runtime: `runner.py:470-484` — if the output symbol is already in
  `self.symbols`, the later eligible producer is `inapplicable` (with
  `superseded_by` on the v2 path). Saturate iterates `for rule in
  ctx.rules` (`runner.py:1347-1356`). First eligible publisher wins.
- Observed: five package files (core-calculations v29–v33) write one
  `conflict_semantics` entry selecting
  `tax.us.2025.rule.schedule-a-total` for
  `tax.us.2025.schedule-a.total` (U-072). This stream opened
  `package.core-calculations.v33.json:47-54` and the two producers:
  `rule.schedule-a-total.json` `when` is `count != 0`;
  `rule.schedule-a-total-closed-empty.json` `when` is `count == 0`;
  both require `require_closed` on `tax.us.2025.f1098`. The closed-empty
  rule's notes state the split is two mutually-exclusive-guard rules.

**Affected layer.** Surface 4 (package conflict semantics) vs surface 2
(publication). Not a schema/runtime parse disagreement.

**Possible user or maintenance consequence.** If two producers of the
same symbol are ever both eligible in one run, member/`ctx.rules` order
picks the winner and `selected_producer` is not consulted. The field
is then an admission permit, not a selector. Current committed conflict
is guard-partitioned (`count == 0` vs `count != 0`), so this stream
does not claim a present-content race on schedule-a.total. A later
package that declares a selected producer whose guard is *not*
exclusive with the other publisher would silently depend on list order.

**Remaining uncertainty.** Surviving question 1 (intent). This stream
did not trace how production marshal orders `ctx.rules` relative to
package `members` order; the attempt loop is list order of `ctx.rules`.
Whether any historical package instance has two simultaneously eligible
publishers was not exhaustively searched.

**Plausible next action.** Owner-selected grammar decision: either
make the runner evaluate `selected_producer` (and fail closed if the
selected producer is inapplicable while another is eligible), or amend
ADR-0027 decision 5 / the field description to say the pin is an
admission permit and runtime is first-eligible-wins. A test that
places the selected producer second in `ctx.rules` with both guards
true would make the split unmissable.

## T5. `bracket_fold` loads canon `spec` and does not read it (U-019, U-056, D10)

**Class:** contract vs enforcement.

**Intentional?** Not established as intentional. ADR-0006 decision 3
(`docs/adr/0006-rule-artifact-language.md:17`): "The schema is the
runtime authority. … A schema document not wired to enforcement does
not satisfy this ADR." Decision 4 (`:18`): `bracket_fold` (fold
arithmetic) carries its own versioned semantic specification; an enum
name alone is not canon. The current fold is an enum name plus a
hardcoded formula whose spec fields are not consulted.

**Evidence.**

- Schema: `operation-semantics.v1` requires `method, boundary, open_top,
  on_miss, row_shape` on the `bracket_fold` spec (U-056).
- Runtime: `evaluator.py:345-360` binds
  `canon = env.canon["bracket_fold"]["spec"]` and never reads `canon`.
  The fold is `(min(value, upper) - lower) * rate` over `value > lower`.
  Missing canon **key** is still `KeyError` (presence required).
  Track 2 resolved question 18: constrains load, not fold.
- Observed: 95 occurrences / 8 files (U-019). No `evaluate()` unit test
  for the fold (schema path-exercise only, per D10).
- This stream re-read `_bracket_fold`; `canon` is assigned at line 346
  and not referenced again in that function. By contrast `_round`
  (`:297`) and `_range_lookup` (`:329`) do read the spec they load.

**Affected layer.** Surface 3 (operation-semantics) vs surface 1
(evaluator). 6iii rounding is a different dual-gate (D9) and is not
this entry.

**Possible user or maintenance consequence.** An author who changes
`boundary` / `on_miss` / `method` on the canon citizen will not change
the fold. A missing canon citizen still crashes. Reviewers who trust
ADR-0006 decision 4 will believe the spec fields bind. They do not.

**Remaining uncertainty.** Whether any committed canon `spec` *disagrees*
with the hardcoded formula was not byte-compared here; the tension is
that the fields are unwired, not that a known disagreement of values
was found. No primary-content `range_lookup` exists to analogise
(U-018).

**Plausible next action.** Owner-selected unit: wire `_bracket_fold` to
the spec fields it already requires to be present, or shrink the
published spec to the fields the fold actually uses (presence of the
citizen as a load key). Either is a code-or-contract change.

## T6. Required clause `blocked` is authored, not consumed (U-035, U-036, D6)

**Class:** two implementations (authored envelope vs emitted ledger
code). Not contract vs enforcement of an ADR sentence that says the
runner must read the field — ADR-0006 decision 1 includes `blocked`
in the clause shape (`docs/adr/0006-rule-artifact-language.md:15`)
without saying the runner copies it through.

**Intentional?** Absence of a read is settled (Track 2 resolved
question 27; V9 `clause blocked field reads in derivation/` → 0).
This stream re-grepped `packages/derivation/` for `rule["blocked"]`
and `rule.get("blocked")`: no matches. Intent of the required field
is surviving question 6: documentation, a default the runner used to
read, or a still-owed input.

**Evidence.**

- Schema: `{code, missing}` required on every rule-artifact version.
  `code` is pattern `^[A-Z][A-Z0-9_]+$`, not an enum (U-035).
- Runtime: missing `requires` → `DEPENDENCY_ABSENT` from the runner
  (`runner.py:465-467`). `require_closed` raises
  `EvalBlocked(SOURCE_SET_UNCLOSED, …)` (U-024). The envelope field is
  not the mechanism.
- Observed: 81 files write `DEPENDENCY_ABSENT`; 33 files write
  `OPEN_DEPENDENCY` (often `missing: ["rounding.convention"]`) (V9).
  `OPEN_DEPENDENCY` is not an evaluator constant; on the v2 ledger it
  would remap to `DEPENDENCY_INVALID` (U-036, V7). The two strings are
  not two runtime conditions (D6).

**Affected layer.** Surface 2 (clause shape) vs runner. Content authors
see a required field that looks like the block they will get.

**Possible user or maintenance consequence.** Authors maintain two
vocabularies that look like blocking conditions and are not. A file
that writes `OPEN_DEPENDENCY` on the envelope and actually blocks
`SOURCE_SET_UNCLOSED` (the schedule-a-total pair above writes
`SOURCE_SET_UNCLOSED` on the envelope, which happens to match
`require_closed`) can look like a mechanism and be a coincidence of
vocabulary. Drift between authored `blocked.code` and emitted ledger
code cannot be caught by schema.

**Remaining uncertainty.** Surviving question 6. Whether some historical
runner did read the field is not in this corpus.

**Plausible next action.** Owner-selected unit: drop the field from a
new rule-artifact generation, or have the runner fail closed when the
emitted code does not match the authored code, or document the field as
author-facing commentary the engine does not interpret. Do not treat
`OPEN_DEPENDENCY` vs `DEPENDENCY_ABSENT` as two runtime conditions in
any later census or repair.

## T7. `loader.OPERATION_VOCABULARY` is a 14-name leftover (U-027, U-063, D2)

**Class:** two implementations (dead constant vs live dispatcher).
Not contract vs enforcement of ADR-0006 decision 2. That decision's
"closed schema-enumerated vocabulary"
(`docs/adr/0006-rule-artifact-language.md:16`) is the schema `oneOf`,
not this frozenset (Track 2 D2, resolved question 13).

**Intentional?** Track 2 answered 1b Q3: leftover. Defined, never
called. `role_vocabulary_report` is the sibling that *is* used. This
stream re-grepped `*.py` for `OPERATION_VOCABULARY`: the definition at
`packages/derivation/loader.py:86-103` is the only hit. Comment on that
definition still calls it "The closed operation vocabulary (ADR-0006
decision 2)".

**Evidence.**

- Dispatcher: 23-op if-chain `evaluator.py:108-267` (U-027). This
  stream's `inspect.getsource(evaluate)` listed, in order:
  `ref, collect, count, block, parameter, add, subtract, multiply,
  divide, max, compare, all, any, not, choose, round, range_lookup,
  bracket_fold, require_closed, categorical_compare, category_literal,
  collect_categorical_all_equal, conditional_dependency_set`.
- Constant: 14 names `{ref, collect, parameter, add, subtract, max,
  compare, all, any, not, choose, range_lookup, bracket_fold, round}`.
  Omits `count, block, multiply, divide, require_closed,
  categorical_compare, category_literal, collect_categorical_all_equal,
  conditional_dependency_set`.
- Observed: all 23 ops appear in content except `range_lookup` in the
  primary corpus (D2 / U-018).

**Affected layer.** Surface 1. A reader of `loader.py`, not a running
evaluation.

**Possible user or maintenance consequence.** A reader who treats the
frozenset as the language will miss nine implemented ops, all of which
appear in committed primary content. No package is admitted or
rejected by this constant. Ranked last among the three charter-named
candidates for that reason.

**Remaining uncertainty.** None about control flow. Whether deleting
the constant would surprise any out-of-tree importer is outside this
corpus.

**Plausible next action.** Delete the unused frozenset, or regenerate it
from the dispatcher (and stop citing ADR-0006 decision 2 on it). A
comment-only fix would still leave a 14-name object that looks like a
gate. Lowest-cost later unit of the catalog.

## T8. Exclusive-graph axioms live as Python tax ids (U-085, surviving question 3)

**Class:** expressiveness. Tax-specific encodings that may conceal a
general language need. Not a disagreement between schema and runtime
about a shared form — the form does not exist as a versioned citizen.

**Intentional?** Unsettled. Track 0 put generic package rules on
surface 4 and domain axioms on 6i; this file sits on both (U-085).
Track 2 left the 4-vs-6i cut unable to decide a Python frozenset of
tax ids. The comments on the sites name ADRs (0061 decision 5, 0059
decision 7, 0050 decision 3) as the requirements being preserved, so
the *invariants* are contractual. The *locus* (Python literals vs a
package-language form) is the tension.

**Evidence.**

- `package_validation.py:197-206` `_LINE_1A_8A_NON_CONFUSION_IDS`
  names `tax.us.2025.rule.schedule-d-line1a-gain` and
  `tax.us.2025.rule.schedule-d-line8a-gain`.
- `:1635-1662` rejects mixed historical/successor graphs with issue
  codes `MIXED_BOX2A_GRAPH`, `MIXED_BOX12_GRAPH`, `MIXED_BOX7_GRAPH`,
  `MIXED_LINE2A_GRAPH`, each testing specific fact-type and rule ids.
- U-084: 83 distinct `MemberIssue.code` strings, unversioned,
  Python-only. No single schema enum enumerates them.
- Track 2 surviving question 3: an owner call on whether those belong
  in a versioned citizen would settle it. This census leaves them
  **active** as implemented admission rules with tax-shaped operands.

**Affected layer.** Surface 4 admission with surface-6i operands.

**Possible user or maintenance consequence.** A later tax year or a
successor citizen id must change Python, not content. The package
language cannot declare "these two graphs are exclusive" as a
versioned artifact, so exclusive-graph history accumulates as
unversioned kill-tests. A reader of artifact-package schema will not
find them.

**Remaining uncertainty.** Whether a general exclusive-graph /
non-confusion form is wanted, or whether Python kill-tests are the
accepted locus for ADR-named invariants that are too tax-shaped to
lift. Surviving question 3.

**Plausible next action.** Owner call: keep them as commented
ADR-backed Python (and classify them grammar-adjacent, surface 6i),
or add a versioned package-language form for exclusive-graph axioms
so a new year does not require a validator edit. Do not treat the
frozenset as evidence that the package schema is incomplete against
its own declared vocabulary — it has no such vocabulary.

## T9. Rule-artifact schema does not constrain `ref`/`collect` names (Track 0 gap 5, U-153, surviving question 8)

**Class:** expressiveness. A distinction the store keeps (fact vs
finding vs parameter vs publication symbol) that the expression
schema collapses to an unconstrained string.

**Intentional?** Plausibly. Track 0 recorded the gap as consistent
with surface 8 being grammar-adjacent rather than proper, and as a
declared-vs-implemented *question* rather than a defect. ADR-0006
decision 2 closes the *operation* vocabulary, not the name domain.
This stream does not upgrade the question into a defect.

**Evidence.**

- Track 0 gap 5: nothing in
  `packages/schemas/derivation/rule-artifact.vN.schema.json`
  constrains which fact-type ids a `ref` may legally name.
- Binding, Track 2 resolved question 9: `ref` → `env.symbols[name]`
  (marshalled current findings / publications);
  `collect` → `env.sources.get(name, [])`. This stream re-read
  `evaluator.py:108-121`; `ref` of a missing symbol blocks
  `DEPENDENCY_ABSENT` naming that symbol. Neither schema-constrains
  `name` to a fact-type id.
- Surviving question 8: what `ref.name` denotes as a store kind is
  answered as a binding and not as a closed taxonomy of the 216
  distinct names. A per-name classification against surface 8 would
  be a different census unit.

**Affected layer.** Surface 1 names vs surface 8 store.

**Possible user or maintenance consequence.** An author can write a
`ref` to a string that will never be a symbol; the failure is
`DEPENDENCY_ABSENT` at evaluation, not a schema rejection. Maintainers
cannot read the rule-artifact schema and know the legal name domain.
That may be the point of keeping surface 8 adjacent: the store is not
the expression grammar.

**Remaining uncertainty.** Surviving question 8 (taxonomy). Whether
runtime validation in `source_authority.py` / `package_validation.py`
already closes some of the name domain was not re-walked beyond
Track 2's confirmation that the *schema* does not.

**Plausible next action.** Only if a later grammar unit wants
schema-level name-domain closure (a fact-type / publication-symbol
enum, or a package-level name index). Otherwise leave the collapse;
record it as a comparison dimension for Track 3's brief (external
systems that type rule names against a fact schema). Not a repair.

## Track 2's eight surviving questions, sorted

Several are tension entries in disguise; several are genuinely just
unknowns. This stream also closed one that Track 2 left open.

| # | Track 2 surviving question | Kind | Where it went |
| --- | --- | --- | --- |
| 1 | Should `selected_producer` be the runtime winner? | tension in disguise | T4. Control flow is first-publisher-wins; intent is the owner call named there. |
| 2 | Should `LOOKUP_MISS` join derivation-record / npe-walk, or is remap the contract? | tension in disguise | T3. No ADR names the token. |
| 3 | Are the tax-id kill-tests package-language or content? | tension in disguise | T8. |
| 4 | Does any runtime path *read* checked-conclusion-binding `truth_table`? | unknown, now answered from source | This stream grepped `packages/derivation/` for `truth_table`: **no matches.** Tests in `tests/test_capital_gain_distributions_line7a_t1_citizens.py` assert the committed citizen's table shape; they do not assert a runner read. The v1 schema description already disclaims execution (U-146). Settled as: no derivation-package call site. Not catalogued — see `#Considered and dropped`. |
| 5 | Should admission `_predicate_depth` walk `left`/`right`, or should the evaluator only count `args`? | tension in disguise | T1. Choosing one is a grammar/code change. |
| 6 | Is the required clause `blocked` field documentation, a former default, or a still-owed input? | tension in disguise | T6. Absence of a read is settled; intent is not. |
| 7 | Track 0 5b-ii criterion: a reader who requires the depth bound itself in JSON Schema still reaches `adjacent`. | genuine unknown (classification axis) | Not a catalog entry. The Foreman correction leaves 5b-ii `proper` and does not re-open the ruling. U-124's "uncertain as one bound" is the construct-level residue. A later owner call on the criterion is process, not a language tension. |
| 8 | Closed taxonomy of `ref.name` store kinds across 216 names. | genuine unknown (would be a different census) | Points at T9 but is larger than T9. T9 is the schema-unconstrained-name fact. A per-name classification is out of scope. |

## Intentional, not catalogued as tensions

These are census findings that look like gaps and are not admitted,
because the evidence supports a deliberate contract choice.

- **JSON Schema does not encode recursive predicate depth.** ADR-0066
  decision 2 says so. The tension is T1 (admission vs that decision),
  not the schema's silence.
- **Predicate language has no `not`.** ADR-0066 decision 2. Rule-artifact
  `not` (U-016) is a different construct. Unused predicate `any`
  (U-123) is declared and implemented; treating it as dead weight
  would ignore a reserved closed-grammar slot.
- **Rule-artifact roles `applicability` and `cross-form-bridge` are
  unused on the 134 files** (U-030, U-150). They live in `role-canon.v1`.
  Evaluation does not branch on role. A declared-and-unused role value
  may be a reserved extension point; nothing shows it is accidental.
- **Term `add` unused in 48 source-family files** (U-114). Declared and
  implemented; binary `left`/`right`, not rule-artifact n-ary `add`.
  Same reserved-slot posture as predicate `any`.

## Considered and dropped

A Track 0 gap or Track 2 disagreement that does not plausibly support
later action, and why.

- **Track 0 gap 1 / D11 universe guard (v3–v17, source-family.v1 only).**
  Current core-calculations hosts are artifact-package.v18–v25 with
  source-family.v2 content (U-078, V9). The collect-target check does
  not apply to the present engine. A historical feature-matrix citizen
  would help a reader of old packages; it would not change v25
  semantics. Dropped as documentation-of-history, not a load-bearing
  language tension. If a later unit *wants* the check on v2 families,
  that is a new requirement.
- **Track 0 gap 2 (no committed adoption record).** Track 0 already
  defined a bounded corpus instead of "the package presently in force."
  An adoption-record gap is production-resolver/ops, not a construct
  disagreement. Dropped.
- **Track 0 gap 3 (unversioned `package.core-calculations.json` is v1).**
  Naming-convention risk for future content; Track 0 already warned.
  No grammar action. Dropped.
- **Track 0 gap 4 (term/predicate discoverability in source-family.v2).**
  The schema-absence wording was wrong and was corrected. Remaining
  discoverability is a naming fact Track 0/1/2 already carried. Dropped.
- **Track 0 gap 6 (filename prefixes do not identify families).**
  Standing working rule: parse the `schema` field. The optional census
  tool was a Track 1 proposal path, not a tension. Dropped.
- **Track 0 gap 7 / U-164 (two version axes).** Already a census row.
  Next action would be "do not conflate them," which every later reader
  of Track 0 already has. Dropped.
- **D3 `accounts_for` on rule-artifact.v5, absent in v6, present on
  attachment-rule.v8.** Generation choice plus a parallel site (U-041,
  U-100). No ADR sentence requires the field on rule-artifact.v6.
  Dropped.
- **D7 `SOURCE_SET_OPEN` vs `SOURCE_SET_UNCLOSED`.** A rename
  (ADR-0036 PC3). One leftover v2 form-field. Not two conditions.
  Dropped.
- **D8 `collect` vs `count` vs `collect_categorical_all_equal` closure.**
  Correctly distinct ops (ADR-0064 rejects collapsing the third).
  Author-education is not a later grammar action until someone proposes
  unification, which this census does not. Dropped.
- **D9 round dual-gate vs `divide` modes vs content refs.** All three
  layer descriptions are true of their layer (D9). Production `round.mode`
  is always a `ref` to `rounding.convention`; bundle enum is `{half_up}`.
  Not a false contract. Dropped.
- **D12 quantity-vocabulary supported set (v1–v12) vs index (v1–v3);
  non-monotone enums (U-151).** Real, and Track 0 missed the drops.
  Present content consequence was not shown to be a user-facing
  failure. Dropped rather than padded; a later package that members
  v4–v12 as the quantity index would reopen it.
- **D13 `form-field.v1` admitted, not in `FIELD_SCHEMAS`.** 2025 content
  is v2/v3; v1 is sample_data. Historical. Dropped.
- **D15 `rule-artifact.v1` runtime-accepted, omitted from package enums.**
  Production members the wages rule as v2. Historical leftover file.
  Dropped.
- **D16 empty `max` uncontained.** Schema `minItems: 1`; observed arity 2.
  Crash is real in the evaluator and gated for validated packages.
  Dropped as production-content risk; remaining evaluator-boundary
  hygiene is not load-bearing next to T1–T7.
- **D17 Track 0 primary criterion fitted after the 5b-ii ruling.**
  Already visible in Track 2 and the Foreman correction. Not a language
  tension. See surviving question 7.
- **U-018 `range_lookup` unused in the primary corpus.** Declared,
  implemented, present in sample_data. Unused is a status, not a
  tension, unless a later unit wants to retire the op.
- **U-146 checked-conclusion-binding `truth_table` unread by
  `packages/derivation`.** Closed from source in this stream (surviving
  question 4). The schema description disclaims execution. One content
  file. Rules duplicate the table. Not a missed interpreter on the
  evidence; a later unit *could* interpret it, but admitting it here
  would pad the catalog with a reserved-documentation citizen.
- **U-129 closure-backed zero drops citation leaves.** Presentation
  policy (`presentation_projection.py:177-188`), adjacent to grammar.
  CQ-1 independently observed that presentation citation pins are a
  narrower set than the finding's `pins` (see `#CQ-1 lens`). Not
  originated as a catalog entry.

## Source checks this stream ran

Reconciled rows were treated as leads. Anything centred in T1–T9 was
re-checked in this worktree. Nothing in the reconciliation failed the
check; one surviving unknown (question 4) was closed.

### C1. Predicate depth admission vs evaluation (T1 / D4 / V4)

Same tree as Track 2 V4 and the Foreman correction: `compare(add^n(field,1), 0)`
against member `{x: 1}`. Ran `packages.derivation.package_validation._predicate_depth`
and `Evaluator.evaluate_predicate`.

```
n_adds  admission  evaluator
     0          1  ok
     1          1  ok
     3          1  ok
     4          1  ok
     5          1  MemberConstraintTooDeep
     8          1  MemberConstraintTooDeep
    20          1  MemberConstraintTooDeep
```

`MAX_PREDICATE_DEPTH` from `declarative_validation.py` printed `6`.
`source-family.v2.schema.json` has no `maxDepth` / `max_depth` keyword.

### C2. attachment-rule.v5 / v3 identity (T2 / V8)

Parsed both published files (never classified by filename).

```
attachment-rule.v3.schema.json $id -> tax/attachment-rule.v3
attachment-rule.v5.schema.json $id -> tax/attachment-rule.v3
v5 properties.schema.const         -> attachment-rule.v3
v3 properties.schema.const         -> attachment-rule.v3
same bytes                         -> False
sha256 v3 prefix                   -> 5b3f219879095db2  (matches published.json)
sha256 v5 prefix                   -> aecd3bf51c16fac9  (matches published.json)
```

### C3. Evaluator dispatch 23; `OPERATION_VOCABULARY` 14 (T7 / V1)

`inspect.getsource(evaluate)` if-op chain, 23 names, same order Track 2
recorded. `len(OPERATION_VOCABULARY) == 14`. Grep of `*.py` for
`OPERATION_VOCABULARY` returns only `loader.py:86`.

### C4. `selected_producer` absent from the runner (T4 / V9)

Grep of `packages/derivation/runner.py` for `selected_producer` and
`conflict_semantics`: no matches. Attempt loop is `for rule in
ctx.rules` at `runner.py:1349`. Opened v33 `conflict_semantics` and
the two `schedule-a.total` producers; guards are `count != 0` vs
`count == 0`.

### C5. `_bracket_fold` binds `canon` and does not read it (T5)

Read `evaluator.py:345-360`. Line 346 assigns `canon`; subsequent
lines use `param`, `key`, `value`, `row`. `_round` and `_range_lookup`
do read their spec.

### C6. Clause `blocked` unread; `truth_table` unread in derivation (T6; surviving question 4)

Grep of `packages/derivation/` for `rule["blocked"]` / `rule.get("blocked")`:
no matches. Grep of `packages/derivation/` for `truth_table`: no matches.

### C7. Ledger remap set and walk enum (T3 / V7)

Read `runner.py:1169-1182` `record_codes` (12 names, includes `SLI_*`,
excludes `LOOKUP_MISS`). Read `npe-walk.v3.schema.json` `code` enum (7
names, no `SLI_*`, no `LOOKUP_MISS`). Read
`derivation-record.v7.schema.json:123-136` (12 names, matches
`record_codes`). Walker emits `"schema": "npe-walk.v3"` at
`explanation.py:332`.

### C8. ADR sentences cited as contracts (T1, T4, T5, T7)

Opened the ADR files, not the index digests, for the quoted clauses:
ADR-0066 decision 2 (`:54-56`); ADR-0006 decisions 1–4 and 7
(`:15-21`); ADR-0027 decision 5 (`:36`); ADR-0020 decision 7 (`:51`);
ADR-0003 decision (`:13`).

Nothing above falsified a Track 2 control-flow claim. Track 2 S2's
failed three-way agreement is independently reproduced as C1.

## CQ-1 lens

Used once, as a bounded validation lens, not as authority, on merged
CQ-1 artifacts already on this tree:

- `docs/phases/claim-boundary-exploration/inquiries/track-0-inquiry-frame.md`
  Hop 2 (lines 127–141)
- `docs/phases/claim-boundary-exploration/inquiries/track-1-lens-d-system-provenance.md`
  lines 76–94

**Where.** Cross-check of T3's claim that explanation surfaces collapse
evaluator-native and record-native distinctions, against what CQ-1
independently observed about provenance pins.

**What those artifacts independently observed.** A derived finding's
`pins` array is a larger set than the citation pins the presentation
surface shows; `pinLabels` is empty in that fixture.

**What it changed.** Nothing originated. It corroborated U-139 / U-143
/ Track 2's CQ-1 note that surviving provenance is not the
rule-artifact `pins` field, and it is why U-129 was considered and
dropped rather than admitted as a tenth entry. T3 itself is grounded
in D5/D14 and C7, not in CQ-1.

Unmerged CQ-2 work was not read.

## What this reading suggests is wrong

Say plainly. None of these stopped the catalog.

1. **Track 0 gap 8's original wording** treated duplicated `6` literals
   as a latent hazard. They already diverge in algorithm. The 2026-08-20
   annotation on that gap, the Foreman correction, and Track 2 S2/V4/D4
   all say this. This catalog carries the stronger form as T1. The
   closed Track 0 text is otherwise left as history.
2. **The round-3 ruling's emphasised clause** (a package carrying an
   over-deep predicate is refused before it can execute) is false for
   term trees. The Foreman correction already struck it. Independently
   reproduced here as C1.
3. **Track 2 surviving question 4** can be closed from a grep Track 2
   did not finish: no `truth_table` read in `packages/derivation/`.
   That is a completeness gap in the reconciliation, not a false
   control-flow claim.
4. **`loader.py:84-85` still attributes `OPERATION_VOCABULARY` to
   ADR-0006 decision 2.** Track 2 D2 already said the ADR names the
   schema `oneOf`. The comment is leftover, like the frozenset (T7).
5. **Plan `#Term boundary` still names seven surfaces.** Track 0 added
   an eighth. Inherited; not re-opened.
6. **Plan Track 2 vs the original Track 2 charter on deliverable count.**
   Already recorded in the reconciliation. This unit is the catalog
   the plan named; it does not resolve that historical split.

Nothing in the reconciliation was unusable as a primary input. Stop
condition "the tension classes the plan names have no instances" does
not apply.

## What this track does not claim

- No grammar change, ADR, or repair. T1 and T2 in particular are
  findings.
- No ranking of *tax* importance. Ranking is consequence for a later
  grammar/code/ADR unit and for what the project believes about itself.
- No claim that unused declared forms are defects.
- No traces (sibling stream). This file does not cite that deliverable.
- No claim that nine entries are the complete set of observations —
  only that these nine are the load-bearing tensions, with drops
  recorded.

## Verification

- Material claims cite a committed path and version, a reconciled
  construct id, or an execution shown above.
- Diff of this assignment is this one file.
- `python3 tools/governance_lint.py` is run at handoff.
