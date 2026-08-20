# Track 3a — Engine language map

- Phase: Grammar Census
- Milestone: Engine Language Map (`grammar-census`)
- Track: 3a — plain-language engine language map
- Role: Builder
- Status: in progress
- Source ref verified: `HEAD` `af766540adbc5a1963e0a8f6a6100fc39909bdb8`
  on `milestone/grammar-census-engine-language-map`
- Assigned path: this file only
- Primary inputs (Track 2, Foreman-accepted):
  reconciliation `docs/phases/grammar-census/inquiries/track-2-reconciliation.md`
  at `f276cc5b` (166 constructs);
  traces `docs/phases/grammar-census/inquiries/track-2-representative-traces.md`
  at `3dba1a80` (6 traces);
  tension catalog `docs/phases/grammar-census/inquiries/track-2-tension-catalog.md`
  at `5ba385c1` (9 entries).
- Boundary: `docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md`
- Correction: `docs/reviews/2026-08-20-grammar-census-foreman-correction-5b-ii-ruling-reasoning.md`

This is the **map**, not the census. One hundred and sixty-six reconciled
rows live one directory over. This file answers a different question: what
*kind of language* the engine actually has — where its boundary falls, what
its layers are and how they relate, what a clause can say, and what the
language cannot say. Claims here cite a reconciled construct (`U-###`), a
catalog entry (`T#`), a named trace, a committed path with version, or an
execution this stream ran and shows under `#Source checks this stream ran`.

This file does not select a next milestone, assess the exit criteria, or
propose a grammar change, ADR, product contract, or external-standards
claim. The phase stays open.

## Who this is for

A reader who can follow JSON and Python, has not read this milestone, does
not know this repository, and will not open the census to check the map.
If a sentence here only makes sense after looking up a `U-###`, the
sentence has failed. The identifiers are grounding, not homework.

## What kind of language this is

This engine has a **closed, JSON-hosted, versioned clause language** for
computing tax findings. An author does not write a procedure. An author
writes schema-typed citizens — most of them **rule artifacts** — each of
which is one guarded publication: a dependency list (`requires`), an
applicability guard (`when`), a value tree (`value`), and exactly one
output symbol (`publishes`). That shape is ADR-0006 decision 1
(`docs/adr/0006-rule-artifact-language.md:15`; U-001, U-031–U-034). The
runtime walks those clauses to a fixpoint (U-050,
`packages/derivation/runner.py:1343-1358`) and records a disposition for
each: `published`, `blocked`, or `inapplicable` (U-042).

It is **not one expression grammar**. It is a **small family of closed
languages** that share JSON hosting, published-schema versioning (ADR-0003;
U-163), and package admission, but not operators, field names, or
evaluators.

Two of those languages are expression trees, and they are not the same
tree:

1. **The clause language.** `when` and `value` on `rule-artifact.v1` through
   `rule-artifact.v6`. Twenty-three operations, dispatched by an if-chain
   in `packages/derivation/evaluator.py` (U-027). A failure is
   `EvalBlocked` carrying a code such as `DEPENDENCY_ABSENT` or
   `SOURCE_SET_UNCLOSED`. This is the language of subtotals, worksheets,
   categorical equality, source-set closure, and explicit `block`. This
   stream listed the twenty-three names from `inspect.getsource(evaluate)`:
   `ref`, `collect`, `count`, `block`, `parameter`, `add`, `subtract`,
   `multiply`, `divide`, `max`, `compare`, `all`, `any`, `not`, `choose`,
   `round`, `range_lookup`, `bracket_fold`, `require_closed`,
   `categorical_compare`, `category_literal`,
   `collect_categorical_all_equal`, `conditional_dependency_set`.

2. **The term/predicate language.** `violated_when` trees on
   `source-family.v2` (`$defs/term`, `$defs/predicate`; U-112–U-123). Five
   term operations (`field`, `literal`, `add`, `subtract`, `floor_zero`)
   and seven predicate operations (`field_present`, `field_absent`,
   `field_equals`, `field_not_equals`, `compare`, `all`, `any`), evaluated
   by `packages/derivation/declarative_validation.py`. A failure is
   `GrammarError` or `MemberConstraintTooDeep`. This is the language of
   per-member constraints on a family — wash-sale flags, adjustment
   exceeding loss. Term and predicate exist only on `source-family.v2`
   (U-107: 48 source-family files, 8 of them v2).

They share five *spellings* (`add`, `subtract`, `compare`, `all`, `any`)
and **no constructs**. Clause `add` is n-ary `args`, flattens lists so
that an arity-1 `add` of a `collect` is a sum of members, and raises
`EvalBlocked` (U-008; Trace 1). Term `add` is binary `left`/`right` and
raises `GrammarError` (U-114). Clause `compare` takes field `cmp` and
tokens `gte`/`lte` (U-015). Predicate `compare` takes field `comparison`
and tokens `ge`/`le` (U-121). The nested language has no `not`; the
clause language does (U-016). ADR-0066 decision 2 says the *predicate*
language has no `not` on purpose; that sentence does not touch the clause
op. Treating the two `add`s as one operator manufactures a language the
engine does not have (Track 2 naming table,
`track-2-reconciliation.md` after the unification list).

A leftover 14-name frozenset, `loader.OPERATION_VOCABULARY`
(`packages/derivation/loader.py:86-103`; U-063, T7), looks like the clause
vocabulary and is not. It is defined, cited to ADR-0006 decision 2 in a
comment, and referenced from no other `*.py` file. The dispatcher is the
implemented language. Nine of the twenty-three ops — including
`multiply`, `divide`, `require_closed`, and `categorical_compare` — are
absent from the frozenset and present in committed primary content.

Around those two trees sit **constraint citizens that are not expression
languages**: the package (who may run, which schemas are admitted, what
is closed, who owns an output); attachment-rules and form-fields (when a
schedule is required, and how a finding becomes a line); and the produced
ledger and walk (the schema-typed record a run is contractually required
to leave behind). The kernel store of facts, acts, entities, and horizons
is the **domain those trees read**. It is schema-typed and ADR-contracted.
It is not the language.

That is the kind of thing it is: a **declarative, closed, multi-citizen
clause family** with two nested expression grammars evaluated by different
modules, a package composition layer, attachment and form-field gates, and
a produced disposition record — sitting next to a store it does not
reshape.

## Where the boundary falls

The plan asked the census not to treat every JSON artifact in the
repository as one undifferentiated grammar
(`docs/phases/grammar-census/milestones/engine-language-map.md`, `#Term
boundary`). Track 0 drew the cut. The labels below are Track 0's, as
Track 2 left them (D17: this census does not reclassify Track 0
surfaces).

**Grammar proper** means: this is part of what a rule — or a citizen
that composes or extends rules (a package, an attachment-rule, a
source-family) — may accept as well-formed or express as compositional
structure, *or* it is the schema-typed record a rule's execution is
contractually required to produce. **Grammar-adjacent** means: no such
enforced citizen exists, or the citizen is the data substrate (the
store) that such content reads or writes without being reshaped by it.
That is Track 0's amended primary criterion
(`track-0-boundary-and-corpus.md`, `#The primary criterion`).

| Surface | What it is, in this repository | Label |
| --- | --- | --- |
| 1 | Rule-artifact `when`/`value` trees; the 23-op clause language | proper |
| 2 | `requires`, `when`, `publishes`, blocking codes, inapplicable-vs-blocked | proper |
| 3 | Versioned `operation-semantics.v1` / `.v2` canon citizens | proper |
| 4 | `artifact-package.v1..v25`: membership, admission, closure, ownership | proper (module side) |
| 5a | Attachment-rule and form-field citizens | proper |
| 5b-i | Source-family term/predicate vocabulary | proper |
| 5b-ii | Predicate depth bound of six | proper (Foreman ruling) |
| 6i | Domain axioms as Python registry pairs (`findings.py`) | adjacent |
| 6ii | Displacement-closure over already-published findings | adjacent (store side) |
| 6iii | Rounding-mode tokens on `operation-semantics.v1` | proper |
| 7 | `derivation-record.v1..v7` and `npe-walk.v1..v3` | proper (produced) |
| 8 | Kernel act/fact/entity/horizon store, including `act-package-adoption.v1` | adjacent (store side) |

Track 0 added surface 8; the plan's `#Term boundary` still names seven.
The eighth is required to answer what `ref` and `collect` read against
(U-153, U-154). The plan-vs-Track-0 count is inherited, not re-opened
(Track 2 item 3 under `#Track 0, Track 1, or plan problems`).

### Why not wider

A wider cut — "everything with a published schema is grammar" — would
pull in the store. Surface 8 is as rigorously schema-typed as surfaces
4 and 7: `act.v1`, fact-type, entity, horizon, `act-package-adoption.v1`.
The naive test calls it proper. Track 0 refused that test on purpose.
A `ref` reads a fact; it does not declare what a fact *is*. A package
does not compose the act log. If the store were grammar, "what the
language can express" would include how a fact enters currency, and
the declared-versus-used reconciliation would have no place to put
input domains. Surface 6i (subset invariants, companion pairs) and
6ii (displacement-closure) sit on the same side: ADR-fixed, kernel-
enforced, no separately versioned module-side citizen. Round 4
explicitly declined "named in an accepted ADR" as sufficient
(`track-0-boundary-and-corpus.md`, `#The primary criterion`,
"Widening that is not adopted").

### Why not narrower

A narrower cut — "only the rule-artifact `$defs/expr` tree is grammar"
— would drop the package, the nested term/predicate language,
attachments, and the produced record. Each of those is a separately
versioned citizen whose shape is enforced by JSON Schema, by package
admission, or both, and each changes what a run may accept or leave
behind:

- A package is itself declared content. ADR-0006 decisions 6–7 make
  membership, closure, and unique output ownership contract, not
  plumbing (U-065, U-073). Without it, a clause has no well-formed
  ensemble.
- Term/predicate is a second closed expression grammar on
  `source-family.v2`, not a Python-only dialect inside attachment-rule.
  Track 0 reversed an earlier adjacent label after opening the schema
  whose filename gave no hint (S1; U-107–U-123). Dropping it would
  describe an engine that does not have wash-sale member constraints
  as language.
- Attachment-rule and form-field citizens decide whether a schedule is
  required and which finding lands on a line (U-088, U-101). They have
  their own ops (`collect_members`, U-093) that are not clause ops.
- Surface 7 is the record a run must produce (clause (b) of the
  criterion). ADR-0020 makes a non-publication a walkable ledger
  entry, not a log line. Dropping it would describe computation
  without a contractual consequence.

### The honest hole in the cut

The 5b-ii row — the predicate depth bound of six — is grammar proper
because a Foreman ruling said so, and because Track 0 then **amended
the criterion to fit the ruling**. That is not how the other eleven
rows were classified, and a reader is owed that in this file, not
only in the reconciliation.

What happened, in order:

1. Round 2 of Track 0 derived a criterion whose opening conjunct was
   "declared in a schema-typed, separately versioned citizen." The
   depth bound has no JSON Schema keyword. ADR-0066 decision 2 says
   so on purpose: "Resolver admission rejects predicate depth greater
   than six; JSON Schema is not claimed to enforce recursive depth by
   itself" (`docs/adr/0066-declarative-structured-validation-and-consumer-closure.md:54-56`).
   Round 2 left 5b-ii `uncertain`.
2. Round 3: the Foreman ruled it `proper`. The stated reason was that
   package admission is an enforcement site — the same kind of gate
   that makes surface 4 proper — and that "a package carrying an
   over-deep predicate is refused before it can execute."
3. Round 4: the opening conjunct did not cover the ruling. Track 0
   widened "schema-typed citizen" to "contractually enforced citizen"
   (JSON Schema **or** package admission **or both**), recorded the
   widening as an amendment fitted after the fact, and showed that no
   other label moved.
4. Track 2 then executed the two depth functions against the same
   tree (`compare(add^n(field, 1), 0)`). Admission walks only `args`;
   `add`/`compare` carry `left`/`right`. Admission reports depth 1 at
   any nesting. The evaluator refuses at n≥5. **The ruling's stated
   reason is false for term trees.** The correction record
   (`docs/reviews/2026-08-20-grammar-census-foreman-correction-5b-ii-ruling-reasoning.md`)
   strikes the sentence and leaves the label in place: 5b-ii stays
   `proper` because the amended criterion does not require that *this
   particular* constraint be the one admission enforces, and 5b-i's
   vocabulary is schema-enforced regardless. Net census: no label
   moves. The supporting sentence is struck.

This stream re-ran the same tree (shown under `#Source checks this
stream ran`). Admission depth stays 1 for n = 0, 1, 3, 4, 5, 8, 20.
The evaluator raises `MemberConstraintTooDeep` at n≥5. Track 2 D4 /
U-124 / T1 / Trace 6 hold.

Two disagreements remain visible, as exit criterion 4 requires:

- **A reader who rejects the enforcement-versus-declaration
  distinction** — who requires the depth bound itself to appear in
  the published `source-family.v2` schema — still draws 5b-ii as
  **adjacent**. Track 0 says so in the 5b-ii entry. The ruling and
  the later amendment do not erase that reading.
- **A reader who requires the admission gate to do what the ruling
  said it does** has a further problem: that gate does not refuse
  over-deep *term* trees. The bound is enforced once, at evaluation,
  not twice. Whether admission should walk `left`/`right`/`value` the
  way the evaluator does, or the evaluator should only count `args`,
  is Track 2 surviving question 5 / T1. This file does not choose.

The rest of the boundary does not rest on that hole. Surfaces 1–5a,
5b-i, 6, 7, and 8 were classified against source before the ruling,
and Track 2 did not move them.

## How the layers relate

A run does not evaluate "the language." It walks a stack. Each layer
has a job the others do not do. Collapsing them is how a reader ends
up believing `loader.OPERATION_VOCABULARY` is the op set, or that an
authored `blocked.code` is the ledger code, or that `selected_producer`
picks a winner.

**The store (surface 8, adjacent).** Facts, entities, horizons, and
adoption acts. A clause never declares a fact-type's shape. `ref`
reads `env.symbols[name]` and blocks `DEPENDENCY_ABSENT` if the name
is missing (U-003, `evaluator.py:108-116`). `collect` reads
`env.sources.get(name, [])` (U-004). JSON Schema does not constrain
those names to fact-type ids (Track 0 gap 5; T9; U-153). The store
is the domain. The language points at it with strings.

**The package (surface 4, proper).** An `artifact-package` citizen
lists members, admitted schemas, entrypoints, input bindings, and
optional `conflict_semantics` (U-065–U-072). Production will not
execute a package until `validate_package` returns `ok`
(`production_resolver.py:363-371`; U-075). That gate is how a
well-formed ensemble is defined: unique output ownership unless a
conflict is declared (U-073), reachability from entrypoints (U-079),
and eighty-three unversioned `MemberIssue.code` strings in Python
(U-084). Current core-calculations is instance v33 sitting on schema
`artifact-package.v25` — two independent version axes (U-164). There
is no committed adoption that pins `tax.us.2025.package.core-calculations`
as current (Track 0; U-080). The census used a bounded corpus instead
of "the package presently in force."

**The clause (surfaces 1–2, proper).** Each member that is a
rule-artifact is one guarded publication. Evaluation order in
`runner.py` attempt is: missing `requires` → `DEPENDENCY_ABSENT`
before the guard; `evaluate(when)` catching `EvalBlocked` → blocked
with the evaluator code; truthy guard → evaluate `value`; falsy
guard → `inapplicable` with `guard_result: False` (U-043; Trace 2).
A later eligible publisher of a symbol already in `self.symbols` is
also `inapplicable`, but with **no** `guard_result` (U-044; T4).
Those two inapplicables are different runner steps. The authored
`blocked` field is required on every rule-artifact version and is
not read (U-035; T6). The runner emits its own codes.

**The nested term/predicate language (surface 5b, proper).** A
`source-family.v2` declaration may carry `member_constraints` whose
`violated_when` trees are the second grammar (U-109). They are
evaluated by `declarative_validation.py`, not by `evaluator.evaluate`
(Trace 6). A violation does not publish the family symbol; the
synthesized producer records `FAMILY_VALIDATION_BLOCKED` internally
and, on the v2 ledger, remaps that code to `DEPENDENCY_INVALID`
(U-047, U-045; T3). Identity-exclusivity components are not term
nodes (U-110). Membership itself is `member_predicate: {fact_type}`
— a different construct from the nested predicates (U-108).

**Operation-semantics (surface 3, proper).** Three ops — `round`,
`range_lookup`, `bracket_fold` — are supposed to take their meaning
from a separately versioned canon citizen (ADR-0006 decision 4;
U-053). `operation-semantics.v1` and `.v2` have **disjoint**
operation enums: v1 is `round, range_lookup, bracket_fold`; v2 is
`categorical_compare, require_closed`. Highest-numbered is not a
superset. The evaluator loads `env.canon["bracket_fold"]["spec"]`
and does not read it (U-019, U-056; T5); it does read the spec for
`round` and `range_lookup`. Multiply, divide, count, block, and the
categorical ops are not in `CANON_OPERATIONS` and do not pin
operation-semantics (U-064).

**Attachment-rule and form-field (surface 5a, proper).** Fifteen
attachment-rule files and fifty form-field files in the corpus
(U-088, U-101). An attachment decides not-required /
required-and-complete / required-and-incomplete (U-090). Completeness
is `presence` or `value` (U-095, U-096). `collect_members` is not a
rule-artifact op (U-093). Form-fields bind a symbol onto a line with
five disposition keys (U-102). There is no `attachment-rule.v7`. The
file named `attachment-rule.v5.schema.json` claims `$id`
`tax/attachment-rule.v3` and a `schema` const of `attachment-rule.v3`
(U-089; T2). Naming v5 on an instance is a catch-22; the v5 bytes
never validate an instance. No committed content hosts v5.

**The produced record (surface 7, proper).** `use_v2` selects
`derivation-record.v7` despite the flag's name (U-052; V6). The
walker hardcodes `"schema": "npe-walk.v3"` (`explanation.py:332`;
U-133). Record v7 enumerates twelve block codes, including `SLI_*`.
Walk v3 enumerates seven, stopping before `SLI_*`, and including
neither `LOOKUP_MISS` nor `FAMILY_VALIDATION_BLOCKED` (U-132,
U-135; T3; D14). The pairing is real and undeclared as a pair.
Runtime publication pins are not the rule-artifact `pins` field:
content writes `input` and `parameter`; `pins_for` adds
operation-semantics, adoption, governance, collected inputs (U-039,
U-139, U-143).

**Kernel axioms and currency (6i, 6ii, adjacent).** Subset
invariants and companion pairs live as registry attributes a
tax-layer loader populates; `findings.py` enforces them generically
without naming a domain (U-125–U-127). Displacement-closure walks
`derivation` and `individuation` edges on already-published findings
(U-128). Neither is an expression vocabulary a rule composes.

**How a finding actually happens.** A production resolver admits a
package. Marshal fills `env.symbols` and `env.sources` from current
findings (U-082). The runner saturates: for each rule, attempt the
guard and value as above. `choose` evaluates only the taken branch
(U-017). `conditional_dependency_set` does not read members when its
condition is false (U-025; Trace 5). Empty unclosed `collect` blocks;
nonempty unclosed `collect` succeeds; `count` always requires
closure, even when rows exist (U-004, U-005; Traces 1 and 3). A
published finding carries pins the runner constructed, not only the
pins the author wrote. A blocked finding carries a ledger code that
may already have been remapped. A walk of that ledger uses a smaller
code enum than the ledger does.

Two version axes run through the stack and are easy to conflate.
Every content citizen parsed has both `schema` (which contract
validates it) and `version` (the instance generation), except
fact-type.v1/v3 (U-164). Classify by the instance `schema` field,
never by filename (Track 0 gap 6; T2).

## What the language can express

The six representative traces were chosen for semantic contrast, not
tax coverage (`track-2-representative-traces.md`). They are the
load-bearing demonstrations. What follows is what a reader should
believe after them, not a retelling.

**A clause can sum a family of facts, and empty is not silently
zero.** Trace 1 evaluates the production tree on
`packages/content/tax/2025/rule.f1099b-covered-lt-basis-subtotal.json`
(`schema`: `rule-artifact.v2`): `add` of `collect`. This stream
re-ran the same ops. Nonempty unclosed `collect` returns the list
and `add` sums it (`Decimal('150')` from `"100"` and `"50"`). Empty
unclosed `collect` blocks `SOURCE_SET_UNCLOSED`. Empty closed
`collect` returns `[]` and `add` yields `Decimal('0')`. Arity-1
`add` of a collect is a sum because `_flatten` unwraps the list
(U-008); it is not identity. Closure is required to treat empty as
zero, not to read a nonempty source. ADR-0006 decision 8 and
ADR-0011: an absent source is never an asserted zero.

**A false guard is inapplicable, not blocked.** Trace 2 evaluates
`when` on the committed sample_data tax-table rule. A compare that
returns false becomes ledger `inapplicable` with `guard_result:
False`, walked as `node_kind: guard_inapplicable` (U-043, U-134).
A missing `ref` *inside* `when` is `DEPENDENCY_ABSENT` — a block,
not inapplicable. A missing `requires` is also a block, and it
happens before the guard is evaluated. Primary 2025 content has no
`"when": false` and no numeric `compare` as top-level `when` (Track
1c C05); production false-guards go through `categorical_compare` or
`require_closed`. The sample_data rule is the asserting fixture.

**Absence of closure is a first-class block, and three ops do not
share a rule.** Trace 3. `require_closed` in `when` raises
`SOURCE_SET_UNCLOSED` on an unclosed set, so the runner records a
block, not Trace 2's inapplicable (U-024). `count` always requires
the set in `closed_sets`, even when rows exist (U-005). `collect`
does not (U-004). This stream re-ran: nonempty unclosed `count` →
`SOURCE_SET_UNCLOSED`; nonempty unclosed `collect` → the list.
`SOURCE_SET_UNCLOSED` is in both the v7 record enum and the v3 walk
enum, so it survives the remap that swallows other codes (U-045,
U-135). Closed-empty on the SLI worksheet publishes `"0"` rather
than blocking.

**A clause can test categorical equality against a declared domain.**
Trace 4. `categorical_compare` plus `category_literal` are the most
frequent expression ops after `ref` (368 and 373 occurrences;
U-022, U-023). Every observed compare uses `cmp: eq`; `ne` is
declared and implemented, not observed. Unequal domains raise
`CATEGORICAL_DOMAIN_MISMATCH`. An out-of-domain value raises
`DEPENDENCY_INVALID`. This is not numeric `compare` (field `cmp`,
tokens `gte`/`lte`). Top-level `category_literal` does not
domain-check; the operand helper does. Path A of the capital-loss-
carryover rule publishes literal `0` when a boundary fact is
`"yes"`, and `choose` does not evaluate the `else` (U-017).

**A worksheet can be declared content rather than a Python
procedure.** Trace 5 reads
`packages/content/tax/2025/rule.sli-worksheet.json`
(`schema`: `rule-artifact.v6`) as one citizen that composes
`require_closed`, `count`, `conditional_dependency_set`,
`categorical_compare`, `collect_categorical_all_equal`, `choose`,
`block` with tax-shaped codes (`SLI_MFS_INELIGIBLE`, …),
`multiply`, `divide` (`rounding: half_up`, `min_decimal_places: 3`),
`max`, `subtract`, and `round`. A live test publishes Schedule 1
line 21 `"1334"` from box-1 `2000` and MAGI `90000`. MFS filing
status takes the `block` op — a block during `value`, not Trace 2
inapplicable, because `when` already passed. Empty
`collect_categorical_all_equal` is `DEPENDENCY_ABSENT`, not a
closure block (U-026; D8). False CDS does not read members (U-025).
`multiply` appears in one primary file; `divide` in two. They are
absent from `OPERATION_VOCABULARY` and present in the dispatcher.

**A family can constrain its members in a second grammar.** Trace 6
reads `packages/content/tax/2025/family.f1099b-covered-w-st.v2.json`
(`schema`: `source-family.v2`). Four `member_constraints` use
predicate `all` / `field_equals` / `field_absent` / `compare` /
term `field` / `subtract` / `floor_zero`. They are evaluated by
`declarative_validation.py`. `field_not_equals` on an absent field
is False and does not fire (U-120); a member that omits the
wash-sale flag entirely does not violate
`BOX_1G_AMOUNT_WITHOUT_FLAG`, while a member that writes `"no"`
does. An invalid member blocks the family as
`FAMILY_VALIDATION_BLOCKED` internally. Term `add` and predicate
`any` are declared and implemented and unused in the 48
source-family files (U-114, U-123) — reserved closed-grammar slots,
not defects.

**What those six add up to.** The engine can: compute over collected
facts with explicit closure; distinguish inapplicable from blocked;
branch without evaluating the untaken arm; emit an author-chosen
block code from the `block` op (as distinct from the unread clause
`blocked` field); domain-check categorical values; and constrain
family members in a nested closed language. One hundred and
fifty-seven of the 166 reconciled constructs are `active` as their
primary status. The language is small, closed, and in production
use on 2025 content. It is also not the language a leftover
14-name frozenset, an authored `blocked.code`, or a `bracket_fold`
spec document would lead a reader to picture.
