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
