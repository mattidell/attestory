# Review: Round 1R (Adversary) — Conditional Selectors, Iteration 1

Independent re-performance of the round-1 adversary review. Grounded against
`docs/governance/`, ratified ADRs 0002–0012 and 0016–0017, and the committed
(HEAD, `41a9948`) `packages/derivation/evaluator.py`, `packages/derivation/runner.py`,
`packages/derivation/package_validation.py`, and the derivation schemas
(`rule-artifact.v1`, `parameter-declaration.v1`, `operation-semantics.v1`).
Paper attacks only; no execution.

Findings are ordered roughly most- to least-severe. Each states: input state →
expected result → where the shape fails or survives, traced against the real
evaluator/runner contracts, not just schema validity.

---

## CS-A1R — Missing operation-semantics canon citizens crashes both shapes' Case 5 (decision-blocking, both shapes)

**Input state:** Any run that reaches `rule.tax-calculation.2025` (Shape A) or
`selector.tax-calculation.2025` (Shape B) — e.g. Case 5, single filer, taxable
income $15,000.

**Expected result (per both designs' walkthroughs):** tax due = $1,568.

**What actually happens:** `_round()` and `_bracket_fold()` in
`packages/derivation/evaluator.py` both unconditionally index
`env.canon["round"]["spec"]` / `env.canon["bracket_fold"]["spec"]` (lines
210, 237). `RunContext.canon` is a caller-supplied `dict[operation ->
operation-semantics citizen]`; nothing populates it automatically. Neither
design's "Instance Payloads" section authors an `operation-semantics.v1`
citizen for `round` or `bracket_fold` (both are `required` per
`operation-semantics.v1.schema.json`: `modes`/`stages`/`tie_break`/`unit` for
round; `method`/`boundary`/`open_top`/`on_miss`/`row_shape` for bracket_fold).
Without them, `env.canon["round"]` raises a bare `KeyError` — an **uncaught
crash**, not the evaluator's own documented contract of "a typed, contained
signal" (`evaluator.py` module docstring, line 10–12; `EvalBlocked` is never
raised here, Python's `KeyError` propagates instead).

**Where it fails:** Both shapes' Case 5 walkthrough is unexecutable as
literally specified — the "step-by-step cascade" for tax calculation is a
narrated hypothetical, not a traced run, since a required citizen was never
authored. This is symmetric across shapes (both cite the same missing
canon), so it doesn't discriminate between A and B, but it must gate
production readiness for either.

---

## CS-A2R — Bracket table row shape (`limit`) is illegal under the real `bracket_fold` contract (decision-blocking, both shapes)

**Input state:** Case 5 as above, using `demo.parameter.tax-brackets.2025`
whose rows are `{"limit": "11600", "rate": "0.10"}` (both shapes cite the
identical table).

**Expected result:** $1,568 (both designs' hand computation:
$11,600 × 0.10 + $3,400 × 0.12$).

**What actually happens:** `_lookup_rows` / `_bracket_fold` in
`evaluator.py` (lines 236–251) read `row["lower"]` (mandatory) and
`row.get("upper")`. There is no code path that reads a `"limit"` key. On the
design's row shape, `Decimal(row["lower"])` raises `KeyError: 'lower'`
before any arithmetic occurs. This isn't a style nit: the
`operation-semantics.v1.schema.json` canon (`row_shape` for `bracket_fold`,
lines 96–100) restricts the field to the enum `["lower", "upper", "rate"]` —
`"limit"` is not a legal token in the very citizen CS-A1R says must exist.
Both designs would need to (a) author the canon citizen at all, and (b)
reshape every bracket row to `lower`/`upper` pairs before `bracket_fold` can
run.

**Where it fails / survives:** Fails as drafted for both shapes — same
citizen, same defect. Notably, the *math* the authors hand-computed
(cumulative marginal fold) is consistent with what `_bracket_fold` would
produce **if** the rows were reshaped correctly — so the arithmetic
reasoning survives, but the artifact as published does not execute.

---

## CS-A3R — Shape B's selector enumerates 2 of 5 filing statuses; no fallback defined (decision-blocking, Shape B)

**Input state:** `filing_status = "head_of_household"`, `taxpayer_over_65 =
false`, `taxpayer_blind = false` (a case within the same axis the topic
plan's own parameter table supports — `parameter.standard-deduction-base.2025`
lists `head_of_household: "22500"`, and both designs cite this exact table).

**Expected result:** standard deduction = $22,500.

**What actually happens:** `selector.standard-deduction.2025`'s `cases`
array (design.md lines 545–571) contains exactly two entries: `filing_status
== "single"` and `filing_status == "married_filing_jointly"`. For
`head_of_household` (or `married_filing_separately`, or
`qualifying_surviving_spouse`), **no case's `when` evaluates true.** The
`selector-artifact.v1.schema.json` draft (design.md lines 474–528) defines
`cases` as a plain array with no exhaustiveness constraint, no declared
"otherwise" case type, and no field describing runner behavior when zero
cases match. No runner code for `selector-artifact.v1` is committed anywhere
in `packages/derivation/`, so this is not merely under-specified in the
design — it is **unimplementable-as-specified**: does the runner block, is
`taxable_income` undefined, does it silently publish nothing?

**Where it fails / survives:** Shape B fails for 3 of the 5 filing statuses
the topic's own reference parameter table declares. Shape A **survives** the
identical input: `rule.base-standard-deduction`'s `value` is `{"op":
"parameter", "parameter_id": ..., "key": {"op": "ref", "name":
"filing_status"}}` — a generic keyed lookup against the same table, which
resolves any of the 5 keys without per-status enumeration (evaluator.py
lines 126–137, `parameter` op). This is the sharpest asymmetry found: Shape
A's "boring" table lookup is exhaustive by construction; Shape B's
case-list, as the authors actually wrote it, is not.

---

## CS-A4R — Shape A's default-injector rules silently overwrite an already-asserted spousal fact (decision-blocking, Shape A)

**Input state:** `filing_status = "single"`, and — via a data-correction
workflow, prior-year carryover, or intake defect — `spouse_over_65 = true`
is *also* present as an input finding in the same run (nothing in the
intake schema or the rule contract prevents a `spouse_over_65` input finding
from coexisting with a non-married `filing_status`).

**Expected result:** the asserted fact (`true`) should either be honored, or
the conflict should be surfaced (blocked/flagged), not silently discarded.

**What actually happens:** `rule.spouse-over-65-default`'s `requires` is
only `["filing_status"]`; `is_eligible()` (runner.py line 203) checks
presence, nothing else. Its `when` guard depends only on marital status —
never on whether `spouse_over_65` already has a value. Once the guard is
true, `attempt()` executes `self.symbols[symbol] = value` (runner.py line
249) **unconditionally** — there is no check for a pre-existing value on
that symbol, whether it arrived as an input finding or otherwise. The
default-injector fires, publishes `spouse_over_65 = false`, and overwrites
the true asserted fact with a "published" disposition — not a conflict or
blocked disposition. `package_validation.py`'s "Unique output ownership"
check (decision 7, lines 146–154) only compares **rule-to-rule** producers
declared inside a package; it has no visibility into runtime input
findings, so this class of collision is invisible to every validation layer
shown in the design or the committed source.

**Where it fails:** This is exactly the "silent fallback" pattern the round
was chartered to hunt, and it is specific to Shape A's default-injection
pattern (Shape B's `optional` field, whatever its unproven implementation
turns out to be, at least declares intent at the schema level — see CS-A5R).

---

## CS-A5R — Shape B's "native optional resolution" is unverified and likely reduces to the same default-injection mechanism, just hidden (production condition, Shape B)

**Input state:** N/A — this is a claim-vs-implementation check, not a data
attack.

**What the design claims:** the comparative table (design.md line 680)
calls Shape B "**Robust.** Native support for `optional` inputs resolves
missing dependencies gracefully at evaluation time," contrasted with Shape
A's "Fragile" default-injector rules — and the recommendation's reason #1
(examination-it1.md lines 21–22) leans on this distinction.

**What the committed evaluator actually does:** `evaluate()`'s `ref` op
(evaluator.py lines 105–109) unconditionally raises `EvalBlocked(BLOCK_ABSENT,
[name])` for any symbol absent from `env.symbols` — there is no "optional"
concept anywhere in the committed evaluator, and no selector-runner exists
in `packages/derivation/` to demonstrate one. For Shape B's claimed behavior
("references... resolve to null or false rather than blocking") to be true,
the not-yet-written selector runner must pre-populate `env.symbols` with
defaults for every declared `optional` name **before** calling `evaluate()`
— which is the identical default-injection Shape A performs via rules,
merely relocated into unimplemented, unverified runner code with no test
surface shown anywhere in the design. The "Robust" vs "Fragile" framing in
the comparison table is not supported by anything traceable to committed
code; it is a claim about code that does not exist.

---

## CS-A6R — Shape B's file-count/density win evaporates once exhaustiveness is restored (production condition, Shape B)

**Input state:** scaling attack — extend `selector.standard-deduction.2025`
to cover all 5 filing statuses (required by CS-A3R) with full age/blind/
spouse cross-products.

**What happens:** each additional `case` must inline its own full
nested-`choose` share arithmetic (the MFJ case already duplicates 4
`choose` clauses verbatim rather than referencing a shared computation —
design.md lines 558–570). There is no sub-expression reuse mechanism across
`cases` in the `selector-artifact.v1` draft. Shape A, by contrast,
factors the identical logic into `rule.additional-share-rate` /
`rule.taxpayer-shares` / `rule.spouse-shares`, each computed once and
referenced by symbol. Restoring the 3 missing filing statuses to Shape B
would produce copy-pasted case bodies concentrated in one growing file — the
opposite of the "Low. 2 files" claim in the comparative table (design.md
line 679), which was measured against an incomplete (2-of-5-status)
instance. This is the "graph density explosion" attack vector the topic
plan (Gate 2, Gate 5) specifically calls out, and it currently favors Shape
A once the comparison is made on equal (exhaustive) footing.

---

## CS-A7R — Itemized-deduction override interaction is unaddressed but the platform has a real backstop (non-blocking, both shapes)

**Input state:** a taxpayer whose itemized deductions exceed the standard
deduction; a future rule/selector would need to publish an alternate
`demo.form1040.standard_deduction`-equivalent value.

**What happens:** neither design shows this composition (consistent with
plan.md Gate 5 scoping it out as "separate or deferred," though
examination-it1.md never states the deferral explicitly). If a future
override rule publishes to the same symbol without a declared
`conflict_semantics` entry, `package_validation.py`'s "Unique output
ownership" check (decision 7) *would* catch it as `OUTPUT_OWNERSHIP_CONFLICT`
— so this is not a silent-collision risk at the package level the way
CS-A4R is at the runtime level. Flagging as an explicit open item for
whichever shape is chosen, not a defect in either.

---

## CS-A8R — Zero and negative taxable income survive correctly under the real bracket-fold loop (non-blocking, both shapes)

**Input state:** `taxable_income = 0` or a negative value (e.g., a defensive
input despite upstream floors).

**What happens:** `_bracket_fold`'s loop (evaluator.py lines 243–251) skips
every row where `value <= lower` (true for all rows when `value` is 0 or
negative, given a first band with `lower = 0`), and returns `Decimal(0)`
with no exception. Both shapes inherit this correctly — once CS-A1R/CS-A2R
are fixed, this edge case poses no additional risk.

---

## CS-A9R — Bracket-threshold edge ($11,600 exactly) resolves correctly, but the boundary convention is never stated in either design (non-blocking, both shapes)

**Input state:** `taxable_income = 11600` exactly, single filer.

**What happens:** `_bracket_fold`'s `value <= lower: continue` rule causes
the boundary income to land entirely inside the lower bracket band (none
spills into the next row) — consistent with a "lower-exclusive" read at the
row's own lower edge, matching the marginal-fold convention. Neither design
states which `boundary` / `open_top` / `on_miss` values it assumes for its
(unauthored, see CS-A1R) `bracket_fold` canon citizen; this should be made
an explicit, cited value rather than left to the reader's inference once the
citizen is actually authored.

---

## Verdicts

### Shape A (Rule-driven Cascade): **Conditionally accept**

Conditions:
1. Author the missing `operation-semantics.v1` citizens for `round` and
   `bracket_fold` (CS-A1R) — without them nothing in Case 5 executes.
2. Correct the bracket-table row shape to `lower`/`upper`/`rate` per the
   canon's `row_shape` enum (CS-A2R).
3. Resolve the default-injector overwrite hazard (CS-A4R): either add an
   explicit "unless already present" guard primitive (not currently
   expressible in the closed `rule-artifact.v1` expr vocabulary — `ref`
   raises `EvalBlocked` rather than returning a presence boolean, so this
   likely requires a new op or moving spousal defaulting out of the rule
   layer into intake-time normalization instead).
4. State the assumed `bracket_fold` boundary convention explicitly (CS-A9R).

With those addressed, Shape A's remaining traced behavior (share-counting
cross-products, filing-status-generic table lookup, zero/negative income,
threshold edges) is verifiably correct against the committed evaluator.

### Shape B (First-class Selector Citizen): **Reject as currently specified**

Rationale: beyond the two cross-cutting blockers shared with Shape A
(CS-A1R, CS-A2R), Shape B has three defects of its own that are not merely
missing polish but undermine its stated case for existing at all: it is
non-exhaustive over the plan's own reference filing-status axis with no
defined fallback (CS-A3R); its headline advantage over Shape A — "native"
optional-dependency resolution — is an unverified claim about unwritten
runner code that, on inspection of the real `evaluate()` contract, likely
reduces to the same mechanism Shape A uses today (CS-A5R); and its
file-count/density advantage does not survive being measured on an
exhaustive instance (CS-A6R). Since Shape B also requires new kernel/runner
surface with zero committed implementation to trace against (unlike Shape A,
whose every claimed step was mechanically verifiable against
`packages/derivation/evaluator.py` and `runner.py` as they exist today), the
round finds no traceable evidence supporting its recommendation. A future
iteration would need to name a fallback-case semantics, either prove the
optional-resolution mechanism against a concrete runner change, or abandon
the claim, and re-run the exhaustive-case scalability comparison before this
shape can be reconsidered.

Advisory only — disposition is the owner's.
