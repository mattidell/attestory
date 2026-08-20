# Track 3b — Bounded external-comparison brief

- Phase: Grammar Census
- Milestone: Engine Language Map (`grammar-census`)
- Track: 3b — bounded external-comparison brief
- Role: Builder
- Status: in progress
- Source ref verified: `HEAD` `af766540adbc5a1963e0a8f6a6100fc39909bdb8`
  on `milestone/grammar-census-engine-language-map`
- Assigned path: this file only
- Primary inputs: Track 2 reconciliation `f276cc5b` (166 constructs),
  representative traces `3dba1a80` (6 traces), tension catalog `5ba385c1`
  (9 entries); Track 0 boundary map; Foreman correction
  `docs/reviews/2026-08-20-grammar-census-foreman-correction-5b-ii-ruling-reasoning.md`;
  carried-forward candidate dimensions from
  `docs/reviews/2026-08-19-grammar-census-track-0-boundary-map-external-critique.md`
  ("Standing value beyond this repair")
- Charter: `docs/reviews/2026-08-20-grammar-census-track-3-synthesis-and-comparison-charter.md`
  (Track 3b section)

This brief **scopes** a later comparative review. It does not conduct one.
It makes no grammar change, product contract, ADR, governance
interpretation, or external-standards claim. It selects nothing. The
phase stays open; the next milestone is owner-held.

Every statement about **this engine** cites a reconciled construct
(`U-###`), a catalog entry (`T#`), a named trace, a committed path with
version, or an execution shown under `#Source checks this stream ran`.
Every characterisation of an external system is **external and
unverified**: this stream did not read those systems' artifacts, and
this milestone's evidence ceiling does not cover them. Where the
characterisation is a recollection rather than a checkable claim, the
text says so.

Do not cite the sibling Track 3a map. The census is the source.

## What this brief is

The plan's `#External comparison brief`
(`docs/phases/grammar-census/milestones/engine-language-map.md`) requires
five statements:

1. which semantic dimensions are now worth comparing;
2. which external systems appear relevant to each dimension;
3. what questions a comparison could answer;
4. what evidence would change an engine decision;
5. which comparisons would be superficial or inapplicable.

Exit criterion 7 is that a follow-on comparative review can be scoped
from those questions rather than from a generic survey of other
languages. A paragraph that summarises what Catala or OpenFisca *is*
has failed that criterion; a paragraph that says "compare us to Catala
on X, because the census found Y, and answer Z would be relevant to
the owner call already named in T#" has met it.

The candidate corpora the plan names — Catala, OpenFisca, DMN/FEEL,
Datalog/RIF, LegalRuleML, provenance standards, other tax-computation
systems — are **candidates to attach to a dimension**, not a checklist
to tour. None is presumed a model to adopt.

## Method

1. Start from the tension catalog's expressiveness entries (T8, T9)
   and from the census facts the traces selected as semantic contrasts
   (two expression grammars; false-`when` is inapplicable; source-set
   closure; blocking-code collapse; producer conflict). Those pressure
   the dimension list harder than the Track 0 consultation's six
   suggestions.
2. For each of the six carried-forward candidates, say keep or drop,
   with the census purchase that decides it. A drop is a finding about
   this engine, not a gap in the brief.
3. For each kept dimension: name the engine facts, name the external
   systems that appear relevant, write the questions, name the owner
   call a positive or negative answer would be relevant to, and name
   the superficial comparison on that same dimension.
4. Do not originate an engine finding from an external recollection.
   If the census did not pressure a dimension, drop it.
5. Re-check load-bearing engine facts against source in this worktree
   (shown under `#Source checks this stream ran`).

## Carried-forward candidates: keep or drop

These six arrived as an external-model consultation, recorded in
`docs/reviews/2026-08-19-grammar-census-track-0-boundary-map-external-critique.md`
as "a substantive first draft of comparison dimensions for Track 3's
brief" and as "an external model consultation, never as authority."
This stream treats each as a candidate to assess.

| Candidate as carried | Decision | Census purchase, or the absence of one |
| --- | --- | --- |
| Peer languages versus one grammar with satellites (DMN/FEEL vs boxed expressions vs tables) | **Keep** as dimension 1 | The census has two expression grammars that share op *strings* and are not the same constructs (reconciliation naming table; U-008 vs U-114; U-015 vs U-121; U-010/U-011 vs U-122/U-123). Trace 6 exists because traces 1–5 do not exhibit the second grammar. Track 0 reversed 5b-i from adjacent to proper after finding `$defs/term` / `$defs/predicate` on `source-family.v2`, not on any attachment-rule schema. |
| Embedded versus standalone (where meaning is allowed to live) | **Keep** as dimension 2 | T1 (ADR-0066 decision 2 is not what admission does to term trees), T5 (`bracket_fold` loads canon `spec` and does not read it), T6 (required clause `blocked` is authored, not consumed), T7 (`OPERATION_VOCABULARY` is a 14-name leftover), T8 (exclusive-graph axioms live as Python tax ids). The census pressured *locus*, not a textbook language-design category. |
| Object language versus observational theory (traces as productions) | **Keep, narrowed** as dimension 5 | T3: evaluator-native codes (`LOOKUP_MISS`, `FAMILY_VALIDATION_BLOCKED`) and later record codes (`SLI_*`) do not survive onto the walk the explanation path can legally carry. That is a produced-record fidelity question the census actually found. The broader question "are these artifacts the law, or a description of it?" is not a catalog entry and is dropped as framed. |
| Defeasibility — whether rules can be overridden by other rules, as a paradigm rather than a blocking enum | **Drop as framed.** A narrower residue is kept as dimension 6 | The census did not find a missing yield-to operator, a priority lattice, or an exception-to-default form. What it found is T4: `selected_producer` *permits* two publishers at admission; the runner never reads the field; runtime is first-eligible-wins (U-044, U-072, U-073). Current committed conflict is guard-partitioned (`count == 0` vs `count != 0`). Blocking is a disposition (Trace 2, Trace 3, U-006), not an override. Comparing "does Catala have defeasible rules" would be the generic survey the plan forbids. |
| Period and horizon semantics, as OpenFisca handles them | **Drop** | Surface 8 records family-horizon succession (U-157) and the act/fact/entity/horizon substrate (U-154) as **grammar-adjacent store**. All 49 `source-closure-mapping` files write `admission.condition` `current-literal-true` (U-144). The clause language has no period operator in the 23-op dispatcher (U-027). No catalog entry treats that absence as a gap. An OpenFisca-period tour would not be answering a question the census asked. |
| Constitutive versus prescriptive rules, as LegalRuleML distinguishes them | **Drop** | The census did not pressure a deontic/constitutive split. Rule-artifacts compute and publish (U-033, U-034); `when` false is inapplicable, not forbidden (Trace 2, U-032, U-043); `block` is an expression op that raises `EvalBlocked` (U-006). T8's exclusive-graph axioms are the nearest constitutive *form*, and they already drive dimension 3. A LegalRuleML constitutive/prescriptive survey would not be answering a census question. |

The two drops that are findings about this engine, restated: **this
engine's clause language does not encode period as an expression-level
feature**, and **this engine does not have a defeasibility paradigm**.
Those are census observations (U-027, U-144, U-157; T4, Trace 2), not
comparative conclusions. They are why those two carried-forward
dimensions do not earn a comparison.

## Census-pressured dimensions (the list that should drive a later unit)

Seven dimensions. Order is consequence for a later comparative review,
not a ranking of tax importance, and not a recommendation.

| # | Dimension | Driven by | External systems that appear relevant |
| --- | --- | --- | --- |
| 1 | Two expression grammars that share names and do not share meaning | Trace 6; reconciliation naming table; Track 0 5b-i reversal | DMN/FEEL and its peer notations; Catala (whether it is one language); Datalog (whether it is one) |
| 2 | Where a construct's meaning is allowed to live | T1, T5, T6, T7, T8 | Catala; OpenFisca; DMN (FEEL spec vs host) |
| 3 | Exclusive-graph / non-confusion axioms as content or as host-language literals | T8, U-085; contrast U-110 | Datalog-style integrity constraints; DMN hit-policy UNIQUE; RIF (uncertain) |
| 4 | Whether `ref` / `collect` names are typed against a fact schema | T9, Track 0 gap 5, U-153 | DMN item definitions / FEEL names; OpenFisca registered variables; Datalog predicate schemas |
| 5 | What the produced explanation record is allowed to say | T3, D5, D14, Trace 6's remap ending | provenance standards (W3C PROV); Catala explanation traces; DMN decision traces |
| 6 | Conflict: admission permit versus runtime winner; applicability versus override | T4, U-044, U-072, U-073; Trace 2 | DMN hit policies; Catala default/exception (uncertain as a mapping); OpenFisca formula replacement (uncertain) |
| 7 | Empty versus nonempty source-set closure | Trace 1 S4 surprise; Trace 3; D8; U-004, U-005, U-026 | OpenFisca empty collections; DMN collect; Catala aggregates (all unverified) |

Each dimension is written out below. The `#Superficial or inapplicable`
section then names the comparisons that would bound a later unit even
if that unit never opens these seven.

## Dimension 1 — Two expression grammars that share names and do not share meaning

**Why the census pressures this.** The reconciliation's naming table is
explicit: rule-artifact `add` and source-family term `add` "share an op
**string** and are **not** the same construct." Same split for
`subtract`, `compare` (`cmp`/`gte`/`lte` vs `comparison`/`ge`/`le`),
and `all`/`any` (predicate `all` has no `not` sibling; rule-artifact
`not` is U-016). Track 0 classified 5b-i grammar proper after finding
the vocabulary on `source-family.v2.schema.json` `$defs/term` and
`$defs/predicate`, not on any attachment-rule schema — the Q1 error
recorded in the 2026-08-19 critique. Trace 6 exists because traces 1–5
do not exhibit this second grammar: `member_constraints` are evaluated
by `packages/derivation/declarative_validation.py`, not by
`evaluator.evaluate`, and raise `GrammarError` /
`MemberConstraintTooDeep` rather than `EvalBlocked`.

**Engine facts (census).**

- Surface 1 dispatcher is a 23-op if-chain in `evaluator.py`
  (U-027). This stream re-listed it: `ref, collect, count, block,
  parameter, add, subtract, multiply, divide, max, compare, all, any,
  not, choose, round, range_lookup, bracket_fold, require_closed,
  categorical_compare, category_literal,
  collect_categorical_all_equal, conditional_dependency_set`.
- Surface 5b term ops are `{field, literal, add, subtract, floor_zero}`;
  predicate ops are `{field_present, field_absent, field_equals,
  field_not_equals, compare, all, any}`
  (`declarative_validation.py:6-10`; U-112–U-123). Term `add` is binary
  `left`/`right` and unused in 48 source-family files (U-114). Rule-artifact
  `add` is n-ary `args` and flattens lists (U-008, Trace 1).
- Shared op *strings* this stream computed from those two closed sets:
  `add, all, any, compare, subtract`. Term-only: `field, floor_zero,
  literal`. Predicate-only: `field_absent, field_equals,
  field_not_equals, field_present`. Rule-artifact `not` (U-016) has no
  5b counterpart; ADR-0066 decision 2 says the predicate language has
  no `not` (catalog: intentional, not a tension).
- Hosts: term/predicate exist only on `source-family.v2` (U-107: 48
  files, 40 host v1 / 8 host v2). Primary content that uses the nested
  grammar is two wash-sale families (Trace 6).
- The two grammars are not "one language plus helpers." They do not
  share an evaluator, an error type, an arity convention, or a
  comparison-field name.

**External systems that appear relevant.** External and unverified.

- **DMN/FEEL.** Publicly described as one expression language (FEEL)
  sitting next to peer notations (decision tables, boxed expressions,
  function definitions) rather than as a second closed op-set with
  colliding names. A comparison would ask whether DMN's split is
  *notation* (same semantics, several writings) or *language* (this
  engine's split). I have not verified DMN's semantics against a
  specification and I am not confident that "boxed expressions" are
  a second grammar in this engine's sense.
- **Catala.** Publicly described as a single legislative DSL. I do not
  know, and I am not asserting, whether Catala embeds a second
  expression language for membership constraints. The useful question
  is whether it is *one* grammar. A comparison that opened Catala only
  to count operators would have missed the dimension.
- **Datalog / RIF.** Datalog is commonly one rule language over a
  relational store. I am unsure how RIF dialects (Core / BLD / PRD)
  sit relative to one another — whether they are peer languages or
  profile restrictions of one language — and a later unit must not
  take this sentence as an answer.

**Questions a comparison could answer.**

1. Is a second closed expression grammar, hosted on a different
   citizen and evaluated by a different module, a common pattern in
   this class of systems, or is this engine's split unusual?
2. When two grammars share op strings (`add`, `compare`, `all`), do
   other systems keep one evaluator and one arity, or do they accept
   the collision the way this census recorded it?
3. Does any peer system put a closed constraint language *inside a
   source-family-like declaration* whose name does not advertise that
   it contains a grammar (Track 0 gap 4, the surviving discoverability
   point)? That is a discoverability comparison, not a syntax one.

**Evidence that would change an engine decision.** This brief does not
pick. A later owner-held grammar unit already faces no "merge the two
grammars" call in the catalog — T8 and T9 are the expressiveness
entries; the two-grammar fact is a census *structure* finding, not a
catalogued defect. Evidence that *would* become relevant:

- If a comparison showed that peer systems with two evaluators and
  colliding names incur the T1 class of failure (one bound, two
  tree-walks) as a standing hazard, that would be relevant to
  surviving question 5 / T1 (whether admission should walk
  `left`/`right`/`value`, or the evaluator should only count `args`)
  — not as a reason to merge the grammars, but as a reason the
  well-formedness rule has to be one algorithm.
- If a comparison showed a workable pattern for one expression
  language used both as clause `value`/`when` and as
  `violated_when`, that would be relevant to a *future* grammar
  proposal. No such proposal is in scope. The catalog does not ask
  for one.

**Superficial on this dimension.** Counting operators across languages
("they have `add` too"). Comparing JSON syntax to FEEL syntax.
Treating `source-family.v2` `$defs/term` as "just more rule-artifact
ops" — the reconciliation forbids that collapse. Asking whether
Catala is "more expressive" without first matching the two-host,
two-evaluator, colliding-name fact.

## Dimension 2 — Where a construct's meaning is allowed to live

**Why the census pressures this.** The carried-forward "embedded versus
standalone" question is kept only in this narrowed form. The census
did not ask whether the language should be a standalone compiler. It
repeatedly found that a construct's *meaning* is split across a
published schema, an ADR sentence, a runtime walk, an unread field,
and a Python literal, and that those can disagree.

**Engine facts (census).**

- **T1 / U-124 / D4.** ADR-0066 decision 2 says resolver admission
  rejects predicate depth greater than six; JSON Schema is not claimed
  to encode recursive depth. Admission `_predicate_depth`
  (`package_validation.py:182-188`) walks `args` only. The evaluator
  (`declarative_validation.py:20,61-88`) increments on
  `left`/`right`/`value`. Same integer, two algorithms. Catalog C1 and
  the Foreman correction's synthetic: `compare(add^n(field,1), 0)` has
  admission depth 1 for every n; evaluator `MemberConstraintTooDeep`
  at n≥5. Content max observed depth 2. Meaning of "depth 6" lives in
  ADR prose, two Python literals, and *not* in the published schema.
- **T5 / U-019 / U-056.** ADR-0006 decisions 3–4 say versioned canon
  is the runtime authority for `bracket_fold`. The evaluator binds
  `canon = env.canon["bracket_fold"]["spec"]` and never reads it
  (`evaluator.py:345-360`). Presence of the key is required
  (`KeyError` if missing). 95 committed occurrences. Meaning of the
  fold lives in hardcoded arithmetic, not in the spec fields the
  schema requires.
- **T6 / U-035.** Schema-required clause field `blocked: {code,
  missing}` is authored on every rule-artifact version. Runner does
  not read it. Authors write `DEPENDENCY_ABSENT` (81 files) and
  `OPEN_DEPENDENCY` (33 files); the latter is not an evaluator
  constant and remaps on the v2 ledger (D6). Meaning of the authored
  string is commentary unless a later unit says otherwise.
- **T7 / U-027 / U-063.** `loader.OPERATION_VOCABULARY` is 14 names,
  never called; the dispatcher is 23 ops. A reader of `loader.py`
  who treats the frozenset as the language misses nine implemented
  ops. Meaning of "the closed vocabulary" lives in the schema
  `oneOf` (ADR-0006 decision 2) and in the dispatcher, not in that
  constant.
- **T8 / U-085.** Exclusive-graph / non-confusion axioms live as
  Python frozensets of tax citizen ids (`package_validation.py:197-206,
  :1635-1662`). The package language has no content form for them.
  Meaning of "these two graphs are exclusive" lives in the host
  language.

The engine is an embedded JSON-citizen language interpreted by Python
modules. That sentence is a census description (Track 0 surfaces 1–5b
as declared citizens; Layer 3 as evaluators). It is not yet a
comparison.

**External systems that appear relevant.** External and unverified.

- **Catala.** Publicly described as a compiled legislative language
  whose semantics are in the language, not in a host interpreter's
  unread fields. I have not verified that Catala's published
  semantics actually bind the way that description implies, and I am
  unsure how much meaning still lives in its compiler. The comparison
  worth doing is: when Catala states a well-formedness bound, is that
  bound one algorithm?
- **OpenFisca.** Publicly described as Python formulas on named
  variables — meaning lives in the host language by design. I have
  not verified the current OpenFisca formula protocol. The comparison
  worth doing is not "Python versus JSON"; it is whether OpenFisca
  *intends* host-language meaning for the T8 class of axiom, and
  whether it has the T5 class of unread spec.
- **DMN / FEEL.** Publicly described as a specification-defined
  expression language with a conformance clause. I am not confident
  about which FEEL constructs are required versus optional in which
  DMN version, and I will not claim DMN "enforces its spec." The
  comparison worth doing is whether a published FEEL clause can be
  unread by an engine the way `bracket_fold` `spec` is unread here.

**Questions a comparison could answer.**

1. In systems that publish a spec citizen *and* an evaluator, is it
   normal for the evaluator to require the citizen's presence and
   ignore its fields (T5), or is that an unusual split?
2. Do peer systems let an ADR-or-spec sentence name a well-formedness
   bound that admission and evaluation implement with different
   tree-walks (T1)?
3. Where do exclusive-graph / non-confusion axioms live — in the
   rule language, in a package/manifest language, or in the host
   (T8, which is also dimension 3)?
4. Is a required unread field (T6) a documented commentary channel
   in any peer system, or do those systems refuse a field the
   evaluator does not consume?

**Evidence that would change an engine decision.** Relevant to owner
calls already named, not to a new one:

- T1 plausible next action: change `_predicate_depth` to walk the
  evaluator's keys, or amend ADR-0066 decision 2 to describe what
  admission does. Evidence that peer systems treat "the bound the
  spec names" as *the evaluator's walk* would be relevant to the
  first option; evidence that they treat admission as a shallower
  syntactic check would be relevant to the second.
- T5: wire `_bracket_fold` to the spec fields, or shrink the
  published spec to presence-as-a-load-key. Evidence that a
  published spec unread by the evaluator is treated as a contract
  break in peer systems would be relevant to wiring; evidence that
  presence-only load keys are an accepted pattern would be relevant
  to shrinking.
- T6: drop the field from a new generation, fail-closed on
  authored-versus-emitted mismatch, or document as commentary.
  Evidence that peer systems have an authored-block-code channel
  the engine does not interpret would be relevant to the commentary
  option.
- T8 is dimension 3.

**Superficial on this dimension.** "JSON-embedded versus a standalone
compiler" as a language-design textbook category. "OpenFisca is
Python so they are similar." Comparing T7's leftover frozenset to
another project's dead constants. Any comparison that treats T1 as
"they also have bugs."

## Dimension 3 — Exclusive-graph / non-confusion axioms as content or as host-language literals

**Why the census pressures this.** T8 is an expressiveness entry, not a
schema/runtime disagreement about a shared form. The form does not
exist as a versioned citizen. T9's plausible next action already
points Track 3 at a name-domain comparison; T8 is the other
expressiveness entry and is the stronger "what the package language
cannot say" fact.

**Engine facts (census).**

- U-085: `package_validation.py:197-206` `_LINE_1A_8A_NON_CONFUSION_IDS`
  names `tax.us.2025.rule.schedule-d-line1a-gain` and
  `tax.us.2025.rule.schedule-d-line8a-gain`. `:1635-1662` rejects mixed
  historical/successor graphs with issue codes `MIXED_BOX2A_GRAPH`,
  `MIXED_BOX12_GRAPH`, `MIXED_BOX7_GRAPH`, `MIXED_LINE2A_GRAPH`, each
  testing specific fact-type and rule ids. This stream re-read those
  two sites; the comments name ADR-0061 decision 5, ADR-0059 decision 7,
  and ADR-0050 decision 3 as the invariants being preserved.
- U-084: 83 distinct `MemberIssue.code` strings, unversioned,
  Python-only. No single schema enum enumerates them.
- Track 0 put generic package rules on surface 4 and domain axioms on
  6i; U-085 sits on both. Track 2 surviving question 3 / T8: an owner
  call on whether those belong in a versioned citizen would settle
  the locus. The *invariants* are contractual; the *locus* (Python
  literals vs a package-language form) is the tension.
- Contrast that is easy to miss: U-110 `identity_exclusivity` *is* a
  versioned content form on `source-family.v2` (`incompatible_family` +
  `components`; 1 object in each of the two wash-sale family files).
  The language can declare that two families' member identities are
  exclusive. It cannot declare that two *package graphs* of named
  tax citizens are exclusive. Those are different axioms. Collapsing
  them would manufacture an expressiveness the census did not find.

**External systems that appear relevant.** External and unverified.

- **Datalog-style integrity constraints.** Publicly described as
  allowing uniqueness / exclusion constraints over relations as
  part of the rule corpus rather than as compiler kill-tests. I have
  not verified any Datalog system's constraint language against an
  artifact, and I am unsure whether "these two graphs of rules may
  not coexist in one program" is even a Datalog-shaped sentence.
- **DMN hit policy UNIQUE.** Publicly described as rejecting
  overlapping rule matches in a table. I am not confident that UNIQUE
  is an exclusive-*graph* axiom rather than an exclusive-*match*
  axiom, and a comparison that treated them as the same thing would
  have missed T8.
- **RIF.** I am not confident how RIF dialects express exclusion and
  I will not characterise them. If a later unit opens RIF, it should
  start from T8's question, not from a RIF tutorial.

**Questions a comparison could answer.**

1. Do peer systems have a *content* form for "these two named graphs
   of citizens are exclusive," or do they also encode that class of
   axiom in the host language / compiler?
2. Is U-110-style identity exclusivity (two families, shared
   identity components) the form those systems use for T8-style
   graph exclusivity, or a different form? A comparison that found
   they are the same form would be relevant to whether T8 is a
   missing generalisation of U-110. A comparison that found they
   are different would be relevant to keeping Python kill-tests
   as the accepted locus for ADR-named graph invariants.
3. When a new tax year or a successor citizen id appears, do peer
   systems change a versioned artifact or a host-language literal?

**Evidence that would change an engine decision.** T8's plausible
next action is already the owner call: keep them as commented
ADR-backed Python (and classify them grammar-adjacent, surface 6i),
or add a versioned package-language form so a new year does not
require a validator edit. This brief does not pick.

- Evidence that a peer system's content form for exclusive graphs
  is used in production, versioned, and does not collapse into
  identity-exclusivity, would be relevant to adding a package-language
  form.
- Evidence that peer tax-computation systems keep this class of
  axiom as compiler/host literals, with the same "too tax-shaped to
  lift" rationale T8 records as remaining uncertainty, would be
  relevant to keeping the Python locus.
- Evidence that U-110 already *is* the form those systems use, and
  that T8's graphs could be rewritten as family identity
  exclusivity, would be relevant to a *content* rewrite rather than
  a new construct. No such rewrite is in scope.

**Superficial on this dimension.** Asking whether OpenFisca "has
package validation." Counting LegalRuleML constitutive tags.
Treating `_LINE_1A_8A_NON_CONFUSION_IDS` as evidence that
artifact-package schema is incomplete against its own declared
vocabulary — T8 forbids that reading: it has no such vocabulary.

## Dimension 4 — Whether `ref` / `collect` names are typed against a fact schema

**Why the census pressures this.** T9 is the other expressiveness
entry. Its plausible next action already names this comparison:
"external systems that type rule names against a fact schema." Track
0 gap 5 recorded the schema silence; Track 2 surviving question 8
left a closed taxonomy of 216 `ref.name` store kinds as a different
census unit.

**Engine facts (census).**

- Track 0 gap 5: nothing in
  `packages/schemas/derivation/rule-artifact.vN.schema.json`
  constrains which fact-type ids a `ref` may legally name.
- Binding, Track 2 resolved question 9 / T9: `ref` →
  `env.symbols[name]` (marshalled current findings / publications);
  `collect` → `env.sources.get(name, [])`. `ref` of a missing symbol
  blocks `DEPENDENCY_ABSENT` naming that symbol (this stream
  re-read `evaluator.py:108-116`). Neither schema-constrains `name`
  to a fact-type id.
- U-153: fact-type v1–v3; `_SUPPORTED` names `fact-type.v2` only.
  `ref.name` is not schema-constrained to a fact-type id.
- Surface 8 is grammar-adjacent (store): a rule's `ref`/`collect`
  reads against it and never declares its shape (Track 0 eighth
  surface). T9 treats the collapse of fact vs finding vs parameter
  vs publication symbol to an unconstrained string as consistent
  with that adjacent label, and does not upgrade the question into
  a defect.
- Observed: 1333 `ref` occurrences / 115 files (U-003); 44 `collect`
  occurrences, all with `source_set` (U-004). The failure mode for a
  nonsense name is evaluation-time `DEPENDENCY_ABSENT`, not schema
  rejection.

**External systems that appear relevant.** External and unverified.

- **DMN item definitions / FEEL names.** Publicly described as
  requiring names to be declared (item definitions, inputs) before
  an expression may use them. I have not verified whether that
  check is schema-level, compiler-level, or runtime, and I am
  unsure whether DMN distinguishes store-kind the way surface 8
  does.
- **OpenFisca registered variables.** Publicly described as a
  registry of named variables that formulas reference. I have not
  verified whether a formula that names an unregistered variable
  fails at load or at compute, and I will not claim it types names
  against a fact schema.
- **Datalog predicate schemas.** Publicly described as declaring
  predicate arity and (in some systems) types. I am unsure whether
  any Datalog in this candidate set types a name as fact-versus-
  derived the way surviving question 8 would need.

**Questions a comparison could answer.**

1. Do peer systems schema-constrain expression names to a declared
   fact/variable/item set, or do they also fail at evaluation with
   a missing-name block?
2. If they constrain names, do they do it in the *expression*
   schema (which would pull surface 8 into grammar-proper) or in a
   *package/manifest* index (which would leave surface 8 adjacent)?
   That is the question T9's remaining uncertainty actually is.
3. Does a typed name domain catch the T9 class of error (a `ref`
   to a string that will never be a symbol) at author time without
   collapsing fact vs finding vs parameter into one grammar?

**Evidence that would change an engine decision.** T9's plausible
next action is: only if a later grammar unit wants schema-level
name-domain closure (a fact-type / publication-symbol enum, or a
package-level name index); otherwise leave the collapse. This brief
does not pick.

- Evidence that peer systems type names in the expression schema
  *and* still keep a store/module cut would be relevant to a
  schema-level enum that does not reclassify surface 8.
- Evidence that the only workable typed-name pattern pulls the
  store into the expression grammar would be relevant to leaving
  the collapse, which is T9's "that may be the point of keeping
  surface 8 adjacent."
- Evidence that a package-level name index (not an expression
  schema enum) is how peer systems close the domain would be
  relevant to a package-language form rather than a
  rule-artifact schema change.

**Superficial on this dimension.** Comparing identifier syntax
(`tax.us.2025…` versus `qualified.names`). Asking whether Catala
"has variables." Counting unused `ref` names. A per-name taxonomy
of the 216 distinct `ref` names — that is surviving question 8,
a different census unit, not a comparison.
