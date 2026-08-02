# Design: Attachment Ontology (D1, Incumbent It1)

Rung 1. All identifiers, payers, values, and answers synthetic (`demo-*`);
the owner's real shapes inform cases only by stated re-expression (ADR-0031).
Designed against committed contracts at HEAD: `rule-artifact.v2`,
`form-field.v2`, `source-family.v1`, `taxable-interest-composition.v1`,
`fact-type.v2`, `npe-walk.v1`, `citation.v1`, and the committed evaluator
(`packages/derivation/runner.py`, `evaluator.py`). Consumes ADR-0035 as-is.

## Core claim: three states map 1:1 onto three *ratified* disposition kinds

The attachment needs no new disposition machinery. The runner already emits
three per-rule dispositions, and `npe-walk.v1` already carries them as
walkable node kinds (`packages/schemas/derivation/npe-walk.v1.schema.json`:
`published` / `blocked` / `guard_inapplicable` / `no_disposition_recorded`):

| Attachment state | Ratified disposition kind | Runner path |
|---|---|---|
| **not-required** | `guard_inapplicable` (walkable node, *not* silence) | `runner.py:342` guard false |
| **required-and-complete** | `published` (a finding, pins every consumed fact) | `runner.py:385` |
| **required-and-incomplete** | `blocked` (code + `unmet_references`) | `runner.py:406` `_record_blocked` |

This is the design's spine: an attachment is a **derived symbol** whose
disposition is one of these three, produced by two ratified `rule-artifact.v2`
rules over existing subtotals and contributed Part III facts. "Schema-as-canon"
is honored — the attachment gets its own citizen (`attachment.v1`) — but the
*derivation* reuses committed ops. See D1-P1 for why the rival "publish a
categorical state, block on incomplete" mapping is rejected.

## D1-P1 — The attachment citizen

### The `attachment.v1` citizen (versioned schema diff, on paper)

A presentation-and-binding citizen, sibling to `form-field.v2` (which maps a
*line* disposition to render/explain); this maps an *attachment* disposition.
Deliberately schedule-agnostic (case 6):

```
attachment.v1 {
  schema: "attachment.v1", id, version,
  form: { authority, form_id, tax_year, jurisdiction },   // "Schedule B"
  requirement: {                     // the hard-trace conditional, declared
    rule:   { id, version },         // applicability rule R1 (below)
    publishes_symbol: string,        // e.g. demo.schedule-b.required (boolean)
    citation: { id, version }        // Schedule B instructions, $1,500 text
  },
  disposition_rule: { id, version }, // rule R2, publishes the attachment symbol
  disposition_symbol: string,        // e.g. demo.schedule-b.attachment
  itemization_parts: [ {             // Part I / Part II — D1-P2
    part_label, source_family:{id,version}, ties_to_symbol,
    row_projection: { payer_key, amount_key }
  } ],
  assertion_parts: [ {               // Part III — D1-P3 (EMPTY for Sched. D)
    part_label,
    assertions: [ { fact_type:{id,version},
                    yes_followups: [ { requires_fact:{id,version},
                                       obligation_note } ] } ]
  } ],
  dispositions: {                    // instruction per ratified kind
    not_required:        { render, explain },   // <- guard_inapplicable
    required_complete:   { render, explain },   // <- published
    required_incomplete: { render, explain, codes[] }  // <- blocked
  }
}
```

No `$1,500`, no `foreign_account`, no `scheduleB` appears as schema surface —
the threshold is a parameter pin (below), Part III is a generic array. That is
what makes case 6 pass without modification.

### The requirement conditional — rule R1 (applicability), declared, walkable

Schedule B is required when taxable interest **or** ordinary dividends is
**over** $1,500 (IRS Schedule B instructions; "over" = strictly greater, so
**exactly $1,500 is not over** → `cmp: gt`, never `gte`). Expressed entirely in
committed `rule-artifact.v2` ops (schema `$defs.expr`: `any`, `compare`,
`parameter`, `ref`):

```
R1  rule-artifact.v2  role: "applicability"
  requires: [ demo.interest.taxable-total,          // line 2b (committed)
              demo.dividends.ordinary-total ]        // line 3b (ADR-0035, Track 1)
  when: true
  value: { op:"any", args:[
    { op:"compare", cmp:"gt",
      left:{op:"ref", name:"demo.interest.taxable-total"},
      right:{op:"parameter", parameter_id:"demo.parameter.schedule-b-threshold.2025"} },
    { op:"compare", cmp:"gt",
      left:{op:"ref", name:"demo.dividends.ordinary-total"},
      right:{op:"parameter", parameter_id:"demo.parameter.schedule-b-threshold.2025"} } ] }
  publishes: demo.schedule-b.required          // boolean finding
  citations: [ { id:"demo.citation.schedule-b.threshold", version:"v1" } ]
  blocked: { code:"DEPENDENCY_ABSENT",
             missing:[ ...subtotals... ] }
```

The `$1,500` lives in the **parameter**, not the schema — so Schedule D's stub
reuses R1's shape with its own threshold parameter (case 6). If either subtotal
is unclosed/absent, R1 blocks honestly (`runner.py:315`) — the determination
itself blocks, never guesses.

### Blocking placement — required-and-incomplete blocks *the attachment*

Rule R2 publishes the attachment symbol. Its guard is the requirement; its
value dereferences the Part III answers. The committed runner's evaluation
order (`runner.py:302–351`) is what makes the completeness gate exact:

1. `requires` absent → blocked **before** guard (`:315`). So R2's `requires`
   lists **only** `demo.schedule-b.required`, never the Part III answers.
2. guard evaluated (`:338`); guard false → `guard_inapplicable`, **value never
   evaluated** (`:342`). Not-required therefore never demands Part III answers.
3. guard true → value evaluated (`:355`); a `ref` to an absent answer raises
   `EvalBlocked(DEPENDENCY_ABSENT, [name])` (`evaluator.py:110`) → `_record_blocked`
   naming the missing fact → **blocked (incomplete)**, walkable.

```
R2  rule-artifact.v2  role: "field-mapping"
  requires: [ demo.schedule-b.required ]
  when: { op:"ref", name:"demo.schedule-b.required" }     // guard = required
  value: <completeness token; see D1-P3 — dereferences every Part III answer,
           conditionally the 7b country>
  publishes: demo.schedule-b.attachment
  blocked: { code:"DEPENDENCY_ABSENT", missing:[ demo.schedule-b.required ] }
```

**Why the block cannot propagate to sibling lines — by construction, not
convention.** Derivation edges are *only* input/choice pins
(`rule-artifact.v2` description; `runner.py:pins_for`), and edges flow one way:
subtotals → R1 → R2. **No line rule (`line-2b`, the 3a/3b rules) lists the
attachment symbol in its `requires` or refs it.** The runner saturates each
rule independently and never un-publishes a symbol already in `self.symbols`
(`runner.py:400`); a blocked R2 only records *its own* `missing`
(`_record_blocked`). So in the NPE walk, no line node can carry the attachment
symbol as an `unmet_reference` — there is no edge for it to travel. Sibling
lines 2b/3b/3a publish in the same saturation regardless of R2's block.

### Rejected rival mapping

"R2 always **publishes** a categorical state (`not_required` / `complete` /
`incomplete`)." Rejected: a published `"incomplete"` value **violates honest
blocking** — a required-but-incomplete attachment must *block*, not publish a
value that reads as an answer. The primary mapping keeps incomplete as a true
`blocked` disposition. It also needs zero new machinery.

## D1-P2 — Part I/II repeating-row itemization and the tie-out

`collect` returns only amounts, dropping payer identity (`evaluator.py:118`),
so **rows are not a rule value** — this is the genuinely new shape the plan
flagged. An `itemization_part` *declares* a projection over the **member
statement facts** of a closed family (ADR-0015 statements carry payer identity):
each current member contributes one row `{payer_key, amount_key}`. Part II
reads `demo.f1099div.1a` and ties to line 3b; Part I reads `demo.f1099int.b1`
and ties to line 2b.

**Tie-out is a declared relation, true by construction.** The subtotal (e.g.
3b) is `collect` over exactly the family's current members at horizon *H*; the
itemization rows are those same members at the same *H*. Therefore
`sum(row.amount) == published(ties_to_symbol)` — same closed set, same
arithmetic. Validated in package validation (Track 2 production condition), the
`taxable-interest-composition.v1` slot-bijection analogue.

**Divergence guard — the stale-closure analogue.** The runner pins the *exact
closure finding id* a subtotal stood on (`runner.py:279`). The itemization must
stand on that **same** pinned closure finding. If a statement is superseded
between reads or the horizon advances, the subtotal's closure-finding id
changes; an itemization pinned to the stale finding fails freshness (ADR-0017
recorded-family-horizons) → `SOURCE_SET_OPEN`, **never a silent row/line
divergence**. Producer: 1099-DIV statements. Authority: the family's closure
finding at *H*. Consumer: line 3b subtotal + Part II rows. Failure: horizon
skew → both re-block together, they cannot diverge silently.

## D1-P3 — Part III contributed taxpayer assertions

Two fact types on the ratified assertion pattern (the `filing-status` /
`taxpayer-over-65` shape: `fact-type.v2`, contributed via ADR-0032, `origin:
assertion`):

```
fact-type.v2  demo.schedule-b.foreign-account   value_schema: enum ["yes","no"]
fact-type.v2  demo.schedule-b.foreign-trust      value_schema: enum ["yes","no"]
fact-type.v2  demo.schedule-b.foreign-account-country  value_schema: string  // 7b
```

R2's completeness token dereferences both base answers (absence → block, case
3) and, only on the yes-branch, the 7b country — using `choose`, which
evaluates only the taken branch (`evaluator.py:169`):

```
value: { op:"choose",
  when: { op:"categorical_compare", cmp:"eq",
          left:{op:"ref", name:"demo.schedule-b.foreign-account"},
          right:{op:"category_literal",
                 fact_type:{id:"demo.schedule-b.foreign-account", version:"v1"},
                 value:"yes"} },
  then: { op:"ref", name:"demo.schedule-b.foreign-account-country" },  // absent→block
  else: { op:"ref", name:"demo.schedule-b.foreign-trust" } }           // still refs trust
```

Foreign-account = yes → **7a names the FinCEN-114 obligation** in
`assertion_parts[].yes_followups[].obligation_note` (a string in the
disposition; the citizen never produces the filing — milestone non-goal), and
**7b country is required** (missing country = factual incompleteness, case-3
posture). Foreign-trust = yes is analogous (obligation named, no country).
Producer: the taxpayer (ADR-0032 contribution). Authority: the assertion fact.
Consumer: R2. Failure: any answer absent, or a required 7b country absent →
attachment blocks incomplete, naming the missing fact; lines still publish.

## Cases (Gate-2)

1. **Hard trace, both outcomes (mandatory).** (a) `demo-payer` ordinary
   dividends 1,600 / interest 900: R1.value `any(gt(900,1500)=F, gt(1600,1500)=T)`
   = **true** → required; the walk shows both `compare` inputs, the parameter
   1,500, the per-trigger outcome (dividends trigger, interest does not), and
   R1's citation. (b) 1,400 / 900: `any(F,F)` = false → R1 publishes
   `required=false`; R2 guard false → `guard_inapplicable` = **not-required, a
   recorded walkable disposition, never silence**. Boundary: dividends exactly
   1,500 → `gt(1500,1500)=F` → not over (cite "over $1,500").
2. **Required and complete.** required=true; Part II two rows from two
   `demo.f1099div.1a` statements sum to 3b; Part I from `demo.f1099int.b1` ties
   to 2b; foreign-account=no, foreign-trust=no present → R2 value evaluates,
   **publishes whole**; the finding's pins enumerate every consumed statement
   and answer (`runner.py:pins_for`).
3. **Required and factually incomplete (mandatory kill-case).** required=true;
   foreign-account answer absent → R2 `ref` → `EvalBlocked` → **blocked**,
   `unmet_references:[demo.schedule-b.foreign-account]`. Lines 2b/3b/3a already
   published and stay published (no edge from them to the attachment) —
   propagation is structurally impossible, per D1-P1.
4. **Row/line tie-out + divergence guard.** `sum(Part II rows) ==
   published(3b)` by same-closed-family construction; a statement superseded
   between reads advances the horizon → stale closure finding → both re-block
   on `SOURCE_SET_OPEN` together (D1-P2).
5. **Part III yes-branch.** foreign-account=yes, country present → 7a FinCEN-114
   obligation *named*, 7b country consumed, publishes. Same, country absent →
   incomplete block (case-3 posture). Foreign-trust=yes analogous.
6. **Generalization (mandatory).** **Schedule D stub**, zero Schedule-B
   surface: `attachment.v1` with `form.form_id:"Schedule D"`; `requirement.rule`
   = a different applicability rule reading ADR-0035's
   `CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal (its own threshold parameter);
   one `itemization_part` over a capital-gain family; `assertion_parts: []`
   (Part III empty). Same three dispositions, same two-rule mechanism, **no
   schema field changed**. The threshold-as-parameter and Part-III-as-array
   choices are exactly what let the second schedule instantiate unmodified — the
   shape is an ontology, not Schedule-B-shaped.

## Production conditions owed to milestone Tracks 1–2 (candidate ADR-0036)

- **Tie-out validation:** package validation asserts each `itemization_part`'s
  `source_family` is the family whose subtotal is `ties_to_symbol`, and that one
  closure read backs both (D1-P2). Never allowlisted.
- **Disposition-wiring validation:** the `disposition_rule` (R2) `requires`
  exactly the requirement symbol and refs Part III answers only in `value`, so
  not-required cannot demand answers (D1-P1).
- **Generalization guard:** validation rejects any `attachment.v1` whose schema
  use encodes a schedule-specific constant or field (keeps case 6 true forever).
- Schema citizens, the two rules, the three Part III fact types, R1's citation,
  and the coordinator-from-facts goldens named in the milestone Verification
  section (both existence outcomes; complete form; honest incomplete block).
```

