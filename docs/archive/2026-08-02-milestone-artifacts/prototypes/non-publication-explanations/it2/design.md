# Design (Iteration 2, Clean-Room Rival): The Run Disposition Ledger and its Projection Walk

Status: **paper only (Rung 2 static evidence).** No runtime, no execution, no
git writes. This document and `examination-it2.md` are the only outputs.

## 0. Scope and boundary honored

- **Scope:** how non-publication dispositions (`blocked`, `guard_inapplicable`,
  `invalid` per ADR-0012) are represented and *walked* in the derivation
  cascade, so that (NPE-P1) the workspace act log is never polluted with mock
  values or empty findings, and (NPE-P2) the returned lineage structurally
  distinguishes missing dependencies from unsatisfied applicability guards.
- **Paper boundary:** API contract, JSON Schema for the walk payload, and paper
  walkthroughs of the three required cases. No runner code, no python run.
- **Stop conditions:** static files only; no edits outside the two outputs.
- **Clean-room exclusions honored:** did not read `it1/`, `examination-it1.md`,
  `reviews/`, `round-1-triage.md`, `evaluation-analysis.md`, `SEAT.md`,
  `process-log.md`, ADR-0019/0020, other topics' iteration/review material, or
  any uncommitted working-tree change under `packages/` (evaluator.py and
  runner.py are modified in the tree and were **not** read). Grounding came only
  from `plan.md`, `charter-it2.md`, governance, the permitted ADRs (0002, 0004,
  0006–0012, 0016, 0017), and committed schema/contract files.

## 1. Thesis: recorded evidence is *necessary*, not merely convenient

The charter asks me to start from the runner-recorded-evidence family (the
runner emits a record of non-execution which the walker traverses) and build the
strongest version, or argue it unworkable. I find the family not only workable
but **the shape the ratified record contract already points at**, and I can give
a first-principles reason it is the *right* one:

> **NPE-P2's distinction is a run fact, not a static rule fact.** Whether a line
> is empty because a dependency is *missing* or because a guard is *false* is a
> property of *this input state and this run*, not of the rule text. The rule
> artifact's `when` expression is the same bytes whether the guard evaluated
> true or false; only the run knows which. Any design that reconstructs lineage
> purely from unexecuted rule ASTs must **re-evaluate** the guard against the
> input state to recover `guard_result` — which is exactly the re-evaluation the
> explanation surface must never do (`explanation.py` docstring: "a traversal of
> committed data — never a re-evaluation, and never a guess"). Recording the
> guard outcome and the missing symbols *at evaluation time* is therefore the
> only shape that lets the walk stay a pure projection.

So the standing effect I build on is already ratified. ADR-0008 puts a
structured, narrative-free **closing derivation record** in a stream *separate
from the act log* (`derivation_records.jsonl`), and its decision 4 already
requires the record vocabulary to "distinguish evaluated-and-inapplicable rules
from rules never reached." The committed `derivation-record.v1` schema already
carries `published[]`, `blocked[]`, and a `dispositions[]` ledger whose
description states the intent verbatim: an inapplicable disposition "carries the
guard_result and the pins the guard read, so 'why is this line empty?' is
answered by walking the record, never by re-evaluating."

My contribution is to make that ledger **load-bearing for a walk**: (a) require
it to be *total* over eligible artifacts, (b) fold the block refinement onto the
ledger row, (c) define the walk-payload schema and projection algorithm with
node/edge kinds that carry NPE-P2 structurally, and (d) give an explicit
cycle/termination strategy. Where these press on the committed record schema I
surface the tension as an authority question (§8) rather than resolve it.

## 2. What the runner records: the Disposition Ledger

The runner's closing record (`phase ∈ {completed, interrupted, failed}`) carries
a **disposition ledger**: exactly one row per *eligible* artifact in the adopted
package, in evaluation order. A row is the atomic run-fact for one artifact:

| field | meaning |
|---|---|
| `artifact_id`, `artifact_version` | which rule/selector artifact this row accounts for |
| `publishes` | the output symbol the artifact would publish |
| `disposition` | `published` \| `inapplicable` \| `blocked` |
| `guard_result` | boolean the `when` guard evaluated to (required when `inapplicable`) |
| `guard_read` | the pins the guard consulted (role-bearing pins) |
| `block` | `{code, missing[]}` present only when `blocked` |
| `finding_ref` | `{finding_id, act_id}` present only when `published` |

This is the committed `derivation-record.v1` ledger with two refinements the
strongest version needs (both flagged in §8):

1. **Totality.** Every eligible artifact gets a row, including artifacts that
   were *never reached* because an upstream dependency blocked. A never-reached
   artifact is recorded `blocked` with `block.code = UNREACHED` and
   `block.missing = [<the immediate upstream symbol that did not publish>]`. This
   is what discharges ADR-0008 decision 4: the reader sees, per artifact,
   evaluated-inapplicable vs never-reached, without re-evaluation.
2. **Block refinement on the row.** The committed schema splits block detail into
   a separate top-level `blocked[]` array (`{artifact_id, code, missing}`) and
   also allows `dispositions[disposition="blocked"]`. The strongest version folds
   `{code, missing}` onto the ledger row as `block`, so one row is
   self-contained and the walk needs no cross-array join. (Reconciling the two
   committed surfaces is a schema decision — §8.2.)

The **block code** is the ADR-0012 machine refinement of `blocked` — the vocabulary
that carries the `invalid` disposition and the unclosed-source disposition:

| `block.code` | ADR-0012 meaning |
|---|---|
| `ABSENT` | required dependency finding is not present |
| `INVALID` | a required input finding is present but failed a validation constraint |
| `OPEN_SOURCE` | a required source family is not closed (no current true closure finding) |
| `UNREACHED` | never reached; an upstream dependency did not publish |

`block.missing[]` names the immediate symbols (or source-family ids) that were
absent/invalid/open. These are the edges the walk follows.

### 2.1 Why this is not act-log pollution (NPE-P1)

The ledger lives in `derivation_records.jsonl` — the **record stream**, a
distinct citizen kind, not the act log (ADR-0002, ADR-0008 decision 1). The act
log (`acts.jsonl`) admits only kernel acts and real `derived-publication` acts
each carrying a complete `derived-finding.v1` (ADR-0010 decision 1). A blocked
or inapplicable artifact produces **no finding and no act** — it produces a
*ledger row in the run account*. There is no mock value, no empty finding, no
stub citizen anywhere in the authoritative store. The walker itself is
read-only: it *writes nothing*. NPE-P1 holds by construction, and it holds
*because* the evidence is recorded as a run account rather than as a finding.

## 3. What the walker consumes and produces

The walk is a **pure projection** — a fold over committed data with no
evaluation:

Inputs (all committed/adopted, none computed at walk time):
1. the **target** form-field citizen (`form-field.v2`) → its `binds_symbol`;
2. the closing **disposition ledger** for the run being explained;
3. the adopted **artifact set** (rule + selector artifacts) → a static
   `symbol → publishing artifact` index and each artifact's guard structure;
4. for `published` rows, the workspace **derived findings**, walked by the
   existing pin-lineage walker (`explanation.py`) unchanged.

Output: one `npe-walk.v1` tree (§4). The published sub-lineage is exactly the
ADR-0007/0009 pin tree the current `explanation.py` already emits; the new work
is the non-publication frontier.

### 3.1 Node and edge kinds carry NPE-P2

The returned lineage distinguishes missing-dependency from unsatisfied-guard
**both at the node and at the edge**, so a consumer cannot conflate them:

- a `blocked` node has **`unmet[]` edges** — one child per missing symbol — the
  *missing-dependency* frame;
- an `inapplicable` node has a **`guard{result:false, read:[…]}`** and **no
  `unmet` edges** — nothing is missing; the branch simply does not apply — the
  *unsatisfied-guard* frame. Its guard inputs, if surfaced, are labelled
  `guard_input`, never `unmet_dependency`.

That edge-label difference (`unmet_dependency` vs `guard_input`) is the
structural NPE-P2 guarantee: the two reasons for an empty cell are different node
kinds reached by different edge kinds.

## 4. Walk payload schema (`npe-walk.v1`, prototype — does not merge)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "prototype/npe-walk.v1",
  "title": "Non-publication explanation walk",
  "description": "A read-only projection over one run's disposition ledger and the adopted artifact set (ADR-0008 record + ADR-0006 artifacts). It is never re-evaluation: every node is a fold of committed run facts. published nodes hand off to the ADR-0007/0009 pin lineage; blocked nodes carry unmet[] edges (missing-dependency frame); inapplicable nodes carry a false guard and no unmet edges (unsatisfied-guard frame).",
  "type": "object",
  "required": ["schema", "run_id", "workspace_revision", "target", "root", "shared"],
  "additionalProperties": false,
  "properties": {
    "schema": { "const": "npe-walk.v1" },
    "run_id": { "type": "string", "minLength": 1 },
    "workspace_revision": { "type": "integer", "minimum": 0 },
    "target": {
      "type": "object",
      "required": ["form_field_id", "form_field_version", "symbol"],
      "additionalProperties": false,
      "properties": {
        "form_field_id": { "type": "string", "minLength": 1 },
        "form_field_version": { "type": "string", "pattern": "^v[0-9]+$" },
        "symbol": { "type": "string", "minLength": 1 }
      }
    },
    "root": { "$ref": "#/$defs/node" },
    "shared": {
      "description": "Memo table: node_id -> node, for every subtree referenced more than once (diamonds). Keeps the payload a DAG-with-pointers, O(artifacts) not O(paths).",
      "type": "object",
      "additionalProperties": { "$ref": "#/$defs/node" }
    }
  },
  "$defs": {
    "pin": {
      "type": "object",
      "required": ["role", "id", "version"],
      "additionalProperties": false,
      "properties": {
        "role": { "enum": ["parameter","computation","applicability","field-mapping","cross-form-bridge","input","choice","adoption","governance","engine","package","operation-semantics"] },
        "id": { "type": "string", "minLength": 1 },
        "version": { "type": "string", "pattern": "^v[0-9]+$" }
      }
    },
    "edge": {
      "description": "How a parent reached a child. edge_kind is the NPE-P2 signal.",
      "type": "object",
      "required": ["edge_kind", "via_symbol", "child"],
      "additionalProperties": false,
      "properties": {
        "edge_kind": { "enum": ["target", "unmet_dependency", "guard_input", "published_input"] },
        "via_symbol": { "type": "string", "minLength": 1 },
        "child": { "oneOf": [ { "$ref": "#/$defs/node" }, { "$ref": "#/$defs/ref" } ] }
      }
    },
    "ref": {
      "description": "A pointer, not an expansion. cycle = a rule-reference cycle was cut; shared = a diamond sub-walk already expanded under `shared`.",
      "type": "object",
      "required": ["node_kind", "ref_kind", "points_to"],
      "additionalProperties": false,
      "properties": {
        "node_kind": { "const": "ref" },
        "ref_kind": { "enum": ["cycle", "shared"] },
        "points_to": { "type": "string", "minLength": 1 }
      }
    },
    "node": {
      "type": "object",
      "required": ["node_id", "node_kind", "symbol"],
      "properties": {
        "node_id": { "type": "string", "minLength": 1 },
        "node_kind": { "enum": ["published", "blocked", "inapplicable"] },
        "symbol": { "type": "string", "minLength": 1 },
        "artifact_id": { "type": "string" },
        "artifact_version": { "type": "string", "pattern": "^v[0-9]+$" }
      },
      "allOf": [
        {
          "if": { "properties": { "node_kind": { "const": "published" } } },
          "then": {
            "required": ["finding_id", "value", "zero_class", "lineage"],
            "properties": {
              "finding_id": { "type": "string", "minLength": 1 },
              "value": {},
              "zero_class": { "enum": ["published_value", "computed_zero", "closure_backed_zero"] },
              "lineage": { "description": "ADR-0007/0009 pin explanation subtree, from explanation.py, unchanged.", "type": "object" }
            }
          }
        },
        {
          "if": { "properties": { "node_kind": { "const": "blocked" } } },
          "then": {
            "required": ["block_code", "unmet"],
            "properties": {
              "block_code": { "enum": ["ABSENT", "INVALID", "OPEN_SOURCE", "UNREACHED"] },
              "invalid_input": {
                "description": "present iff block_code=INVALID: the present-but-invalid finding and the constraint it failed.",
                "type": "object",
                "required": ["finding_id", "constraint"],
                "additionalProperties": false,
                "properties": {
                  "finding_id": { "type": "string", "minLength": 1 },
                  "constraint": { "type": "string", "minLength": 1 }
                }
              },
              "open_family": {
                "description": "present iff block_code=OPEN_SOURCE: the source-family declaration that is not closed.",
                "type": "object",
                "required": ["source_family_id", "version"],
                "additionalProperties": false,
                "properties": {
                  "source_family_id": { "type": "string", "minLength": 1 },
                  "version": { "type": "string", "pattern": "^v[0-9]+$" }
                }
              },
              "unmet": { "type": "array", "items": { "$ref": "#/$defs/edge" } }
            }
          }
        },
        {
          "if": { "properties": { "node_kind": { "const": "inapplicable" } } },
          "then": {
            "required": ["guard"],
            "not": { "required": ["unmet"] },
            "properties": {
              "guard": {
                "type": "object",
                "required": ["result", "read"],
                "additionalProperties": false,
                "properties": {
                  "result": { "const": false },
                  "read": { "type": "array", "items": { "$ref": "#/$defs/pin" } },
                  "selected_alternative": {
                    "description": "optional: the symbol that WAS selected instead (e.g. standard deduction chosen over itemization), for legibility.",
                    "type": "string", "minLength": 1
                  }
                }
              }
            }
          }
        }
      ]
    }
  }
}
```

Two structural invariants worth stating: an `inapplicable` node **may not** carry
`unmet` (`"not": {"required": ["unmet"]}`), and a `blocked` node's children are
reached only through `edge_kind = unmet_dependency`. NPE-P2 is thus enforced by
the schema, not merely by convention.

## 5. Walk algorithm

```
walk(symbol, edge_kind, ledger, artifacts, findings, visited, shared):
  artifact = artifacts.publisher_of(symbol)        # static symbol->artifact index
  node_id  = artifact.id + "@" + symbol
  if node_id in visited.active:                     # on the current path -> cycle
      return ref(cycle, points_to=node_id)
  if node_id in shared:                             # already fully expanded -> reuse
      return ref(shared, points_to=node_id)
  row = ledger.row_for(artifact.id)                 # the run fact; no evaluation

  visited.active.add(node_id)
  case row.disposition of
    published:
      finding = findings[row.finding_ref.finding_id]
      node = published_node(node_id, symbol, finding,
                            zero_class = classify_zero(finding),   # §6
                            lineage    = explanation.explain(finding.id, ...))  # ADR-0007/0009
    inapplicable:
      node = inapplicable_node(node_id, symbol,
                               guard = { result:false, read: row.guard_read,
                                         selected_alternative: sibling_published_symbol(artifact) })
      # NOTE: no unmet edges. Guard inputs are evidence, not missing deps.
    blocked:
      children = []
      for m in row.block.missing:                   # each missing symbol -> recurse
          child = walk(m, unmet_dependency, ledger, artifacts, findings, visited, shared)
          children.append(edge(unmet_dependency, via_symbol=m, child=child))
      node = blocked_node(node_id, symbol,
                          block_code = row.block.code,
                          invalid_input = row.block.invalid_input?,   # if INVALID
                          open_family   = row.block.open_family?,     # if OPEN_SOURCE
                          unmet = children)
  visited.active.remove(node_id)
  if node_id was reached more than once:  shared[node_id] = node; return ref(shared, node_id)
  return node

walk_target(form_field, run):
  ledger = record_stream.closing(run).dispositions      # the run account
  return { schema:"npe-walk.v1", run_id:run, workspace_revision:...,
           target:{form_field.id, form_field.version, form_field.binds_symbol},
           root: walk(form_field.binds_symbol, "target", ledger, adopted_artifacts,
                      workspace_findings, visited={active:{}}, shared={}),
           shared }
```

Every branch reads a committed row or a committed pin. Nothing recomputes a
guard or a value. The only index built at walk time is the static
`symbol → artifact` map from the adopted package's `publishes` fields, which is
run-independent.

## 6. Zero classification (the ADR-0012 published refinements)

The record disposition enum is `{published, inapplicable, blocked}` — it does not
carry `computed_zero`/`closure_backed_zero`. Those are refinements of a
*published* value and are read from the published finding's **lineage**, not from
the ledger: a published numeric zero whose pins include a current
source-family closure finding is `closure_backed_zero`; a published numeric zero
grounded only in present input/source findings is `computed_zero`; any nonzero is
`published_value`. `classify_zero()` inspects the finding's pins (already walked
for `lineage`), so the distinction is preserved in explanation exactly as
ADR-0012 decision 6 requires, with no new authority. (That this division of
labor between ledger and lineage is intended is an authority question — §8.3.)

## 7. Required cases

### Case 1 — blocked line 2b cascades to 9, 11, 12, 15, 16

Wage citizen present; the 1099-INT box-1 source family is **unclosed** (no
current true closure finding — ADR-0011 decision 5, ADR-0016 decision 5). Line
2b's artifact cannot publish `taxable_interest`: `block.code = OPEN_SOURCE`,
`open_family` names the family declaration. Lines 9/11/12/15/16 each require a
downstream symbol; each is recorded `blocked` — line 9 with `ABSENT`/`UNREACHED`
on `taxable_interest` (its direct dependency), the rest chained on the symbol
above them. The walk of the line-2b field:

```json
{
  "schema": "npe-walk.v1",
  "run_id": "run-7f3a",
  "workspace_revision": 42,
  "target": { "form_field_id": "form1040.line-2b.form-field", "form_field_version": "v1", "symbol": "taxable_interest" },
  "root": {
    "node_id": "rule.form1040-line2b@taxable_interest",
    "node_kind": "blocked",
    "symbol": "taxable_interest",
    "artifact_id": "rule.form1040-line2b",
    "artifact_version": "v1",
    "block_code": "OPEN_SOURCE",
    "open_family": { "source_family_id": "source-family.1099int-box1.2025", "version": "v1" },
    "unmet": [
      {
        "edge_kind": "unmet_dependency",
        "via_symbol": "interest_1099int_box1_subtotal",
        "child": {
          "node_id": "rule.1099int-box1-subtotal@interest_1099int_box1_subtotal",
          "node_kind": "blocked",
          "symbol": "interest_1099int_box1_subtotal",
          "artifact_id": "rule.1099int-box1-subtotal",
          "artifact_version": "v1",
          "block_code": "OPEN_SOURCE",
          "open_family": { "source_family_id": "source-family.1099int-box1.2025", "version": "v1" },
          "unmet": []
        }
      }
    ]
  },
  "shared": {}
}
```

The downstream lines project the *same* line-2b subtree once and point at it. The
line-11 field walk (elided for brevity) reaches `taxable_interest` through
`unmet_dependency` edges and, on the second encounter, emits
`{"node_kind":"ref","ref_kind":"shared","points_to":"rule.form1040-line2b@taxable_interest"}`;
the expanded subtree sits once in `shared`. So the whole cascade is O(lines), and
every leaf terminates at `OPEN_SOURCE` with the same family id — the reader sees
one root cause, not five unrelated empties.

### Case 2 — inapplicable itemization override (MFJ, standard deduction larger)

Married-filing-jointly; the itemization override symbol is inapplicable because
the standard deduction is larger and the itemization bypass is not asserted. The
deduction selector's itemization case guard is false. The override field's walk:

```json
{
  "schema": "npe-walk.v1",
  "run_id": "run-7f3a",
  "workspace_revision": 42,
  "target": { "form_field_id": "form1040.line-12.itemized-override.form-field", "form_field_version": "v1", "symbol": "itemized_deduction_applied" },
  "root": {
    "node_id": "selector.deduction-method@itemized_deduction_applied",
    "node_kind": "inapplicable",
    "symbol": "itemized_deduction_applied",
    "artifact_id": "selector.deduction-method",
    "artifact_version": "v1",
    "guard": {
      "result": false,
      "read": [
        { "role": "input",  "id": "finding.filing-status.mfj",        "version": "v1" },
        { "role": "input",  "id": "finding.itemized-deductions-total", "version": "v1" },
        { "role": "input",  "id": "finding.standard-deduction-amount", "version": "v1" },
        { "role": "choice", "id": "finding.itemization-bypass-absent", "version": "v1" }
      ],
      "selected_alternative": "standard_deduction_applied"
    }
  },
  "shared": {}
}
```

There is **no `unmet` array**. Nothing is missing: filing status, both deduction
amounts, and the (absent) bypass election were all read; the guard simply
evaluated false. `selected_alternative` names the branch that *did* apply, so the
consumer can say "the standard deduction was larger, so itemization does not
apply here" — categorically different from "we could not compute this."

### Case 3 — invalid finding blocks a down-cascade derivation

A fact fails a validation constraint (e.g. a negative value on a field the fact
type constrains non-negative). The finding is *present but invalid*, so the
artifact that consumes it blocks with `INVALID` (not `ABSENT`), and it publishes
nothing; its consumers block `ABSENT`/`UNREACHED` on the un-published symbol.
The walk of a downstream field (schematic):

```
line-11 (adjusted_gross_income)  blocked ABSENT
  └─[unmet_dependency via total_income]→ line-9 (total_income)  blocked ABSENT
       └─[unmet_dependency via wages_total]→ rule.wages-total (wages_total)  blocked INVALID
            invalid_input: { finding_id: "finding.w2-slip-A.wages", constraint: "wages >= 0" }
            unmet: []   (the input is present, so nothing is "missing" below it)
```

The leaf is `INVALID` with `invalid_input` naming the offending finding and the
constraint it failed — the ADR-0012 refinement of `blocked` into *invalid* vs
*absent*. A reader distinguishes "your W-2 wage value is invalid" from "a value
is missing" by the `block_code`, while both remain the `blocked` disposition (so
NPE-P2's top-level blocked/inapplicable split is undisturbed and the invalid
refinement lives beneath it, exactly as ADR-0012 decision 4 prescribes).

## 8. Cycle and termination strategy

- **Rule-reference cycles.** Package closure (ADR-0006 decisions 6–7, unique
  output ownership + closed manifest) should forbid a `publishes/requires` cycle
  at authoring, but the walker must be robust to a malformed adopted package. A
  `visited.active` set holds node_ids on the current path; re-entering one emits
  a `ref{cycle}` pointer and does not recurse. The tree is therefore finite even
  if the package graph is not a DAG.
- **Repeated sub-walks (diamonds).** Case 1 is the canonical diamond: lines 11
  and 15 both funnel through blocked line 2b. The second full encounter is
  memoized in `shared` and every further encounter is a `ref{shared}` pointer.
  Each artifact is fully expanded **at most once**; all other encounters are
  constant-size refs.
- **Termination proof.** The adopted package is a finite, closed set of
  artifacts (ADR-0006 decision 6). Each `walk` call either expands a not-yet-seen
  node_id (bounded by |artifacts|) or returns a constant-size ref. Edges followed
  are the union of `block.missing` fan-outs, bounded by total declared
  dependencies. Hence the walk is O(|artifacts| + |edges|) and always halts.
- **Retention sufficiency (Rung-2 question).** The walk never re-evaluates
  because every fact it needs is a committed row or pin: `published` → finding
  pins (on the finding); `blocked` → `block.{code,missing,invalid_input,open_family}`
  (on the ledger row); `inapplicable` → `guard_result` + `guard_read` (on the
  ledger row). The one non-ledger input is the static `symbol → artifact` index
  from adopted `publishes` fields. So the ledger + adopted artifacts retain
  exactly enough structure to walk an unexecuted rule's dependencies — provided
  the ledger is total (§8, authority question 1).

## 9. Unresolved authority questions (surfaced, not resolved by fiat)

1. **Ledger totality.** The committed `derivation-record.v1` does not *require*
   `dispositions[]` to cover every eligible artifact. My walk's completeness
   (evaluated-inapplicable vs never-reached, ADR-0008 decision 4) and its
   no-re-evaluation guarantee depend on totality, including `UNREACHED` rows for
   down-cascade artifacts. **Is the runner contractually obliged to emit a row
   per eligible artifact?** If the ledger may be sparse, the walker must
   synthesize never-reached nodes by following adopted-artifact `requires`
   edges — still traversal, not evaluation, but a weaker completeness claim. This
   is a runner-contract / record-schema decision, not the walker's to make.
2. **Two committed blocked surfaces.** The committed schema carries both a
   top-level `blocked[]` (`{artifact_id, code, missing}`) and
   `dispositions[disposition="blocked"]` (`{guard_result, pins}`) with no declared
   join beyond `artifact_id`. My strongest version folds `{code, missing}` onto
   the ledger row. **Which surface is authoritative, and is the fold acceptable?**
   A schema decision.
3. **Zero refinement division of labor.** The record disposition enum lacks
   `computed_zero`/`closure_backed_zero`; §6 computes them from the published
   finding's lineage. **Is it settled that the ledger records only
   published/inapplicable/blocked and the zero refinement is a lineage
   projection?** This is a live cross-ADR seam (ADR-0012 decision 6 vs the record
   enum).
4. **`guard_result` requiredness.** The committed schema makes `pins` required on
   a disposition but `guard_result` optional. For an `inapplicable` row,
   `guard_result = false` is the load-bearing evidence NPE-P2 needs. **Should
   `guard_result` be required whenever `disposition = inapplicable`?**
5. **Disposition vocabulary term.** The record says `inapplicable`; ADR-0012 says
   `guard_inapplicable`. The mapping is 1:1 and I treat them as synonyms, but the
   canonical term across record and form-field families should be pinned.

None of these blocks the walk *design*; each is a contract point the walker
consumes and cannot ratify alone.

## 10. Strongest and weakest points

- **Strongest:** the design rests on an already-ratified standing effect
  (ADR-0008's separate, structured, narrative-free record with a
  guard-result-bearing disposition), and it gives a first-principles reason the
  family is *necessary* (NPE-P2's distinction is a run fact, so recording it at
  evaluation time is the only way to keep the walk a pure projection). NPE-P1 is
  airtight: nothing non-published ever becomes a finding or an act. NPE-P2 is
  schema-enforced: `inapplicable` nodes cannot carry `unmet`.
- **Weakest:** the walk's completeness leans on ledger **totality**, which the
  committed record schema does not yet compel (§9.1). Without it, down-cascade
  never-reached lines depend on the walker re-deriving the dependency graph from
  adopted `requires` edges — sound but a weaker guarantee — and the committed
  schema's split blocked surfaces (§9.2) must be reconciled before implementation.
```
