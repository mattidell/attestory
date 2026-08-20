# Track 2b-ii — Tension catalog

- Phase: Grammar Census
- Milestone: Engine Language Map (`grammar-census`)
- Track: 2b-ii — tension catalog
- Role: Builder
- Status: in progress
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
