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
