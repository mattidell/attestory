# Confirmation Review R1 — Attachment Ontology (D1) synthesis

Seat: Confirmation (High tier, independent context, single seat). Advisory —
owner decides. I authored none of what I review. Read in charter order:
`plan.md`, `evaluation-analysis.md`, `reviews/governance-r1.md`,
`reviews/adversary-r1.md`, `it1/design.md`, `it2/design.md`, then
`synthesis.md` under confirmation. Committed machinery verified against
`packages/derivation/evaluator.py`, `runner.py`, and the
`packages/schemas/derivation/` + `packages/schemas/tax/` schemas at HEAD
(`bd274d1`). Read-only probes only; no git writes; no repo change outside
this file. All values synthetic.

**Verdict: NOT-CONFIRMED.** Case 4 fails: the synthesis claims committed
error-vocabulary behavior the source does not support, and its "correction"
of the tie-out code misstates the round-1 finding and lands on a code the
record/walk schema forbids. Cases 1, 2, 5 hold only with a named condition
the synthesis leaves open. Cases 3 and 6 hold clean.

---

## The six cases against the synthesized shape

### Case 1 — Over-blocking (both answers "no"/"no" present → publishes whole)
Scenario: required attachment, `foreign-account="no"`, `foreign-trust="no"`,
country not applicable. Synthesized completeness is `all(ref(fa), ref(ft),
<gate>)`. `all` is `all(bool(evaluate(a)) for a in args)`
(`evaluator.py:160-161`). With string answers, `bool("no")=True`, so both
refs resolve truthy, none absent → publishes `required_complete`. Does **not**
over-trigger. **Holds — but conditionally.** it2's declared Part III fact
types are **boolean** (`it2/design.md:188-189`), and `bool(False)=False`, so
under boolean encoding `all(ref(fa)=False, …)` short-circuits at the first
"no" and mis-branches away from `required_complete` — the opposite failure.
The synthesis says "a 'no' is an answer" and "no answer masks another" but
never pins the answer encoding, and `all(...)` delivers presence-semantics
only when every answer is a non-empty truthy value (it1's enum `["yes","no"]`,
not it2's boolean). **HOLDS-WITH-CONDITION:** completeness must be a presence
test independent of answer truthiness. This is exactly the adversary's A1
fragility note ("robust form evaluates every presence ref unconditionally,
not inside `all`"), which the synthesis did not adopt.

### Case 2 — Each answer absent individually → blocks naming that fact
`fa` absent: `all` evaluates `ref(fa)` first → `EvalBlocked(DEPENDENCY_ABSENT,
[fa])` (`evaluator.py:108-111`) → recorded `blocked`, `missing:[fa]`
(`runner.py:340,357,406`). Holds. `ft` absent with `fa` present-and-truthy:
`all` passes `ref(fa)`, reaches `ref(ft)` → blocks naming `ft`. Holds — **but
only because `fa` is truthy**. Under boolean `fa=False`, `all` short-circuits
before `ref(ft)`, so an absent `ft` is never dereferenced and never blocks —
the round-1 masking hole reappears through the short-circuit. **HOLDS-WITH-
CONDITION** (same condition as case 1).

### Case 3 — Not-required as an atomic disposition (G1, ADR-0012)
The synthesis adopts it1's mapping: not-required → `guard_inapplicable`,
required-complete → `published`, required-incomplete → `blocked` — three
distinct kinds on the ratified triad, no embedded state field. Verified:
record disposition enum `{published, blocked, inapplicable}`
(`derivation-record.v2:10`); walk `node_kind {published, blocked,
guard_inapplicable, no_disposition_recorded}` (`npe-walk.v1:7`); R2 guard
false → `inapplicable`/`guard_inapplicable` node (`runner.py:342-349`). Three
atomic dispositions, no consumer must parse a `value.state` blob — G1
resolved, ADR-0012 atomicity held. **HOLDS.** (Minor imprecision: the
synthesis attributes the `guard_inapplicable` node to "the requirement rule";
it is the disposition rule R2 whose guard goes false. Not blocking.)

### Case 4 — Tie-out divergence both directions → hard error, committed-consistent
Scenario: `sum(Part II rows) ≠ published(3b)`, via stale row and via stale
line. The synthesis asserts this is "a hard projection error using the
committed error vocabulary (`SOURCE_SET_UNCLOSED` family / projection-error
path)." **Source does not support this.**
- There is **no committed path** that converts `sum(rows) ≠ line` into a
  block. `compare` returns a boolean (`evaluator.py:155-158`) and never
  raises; `all`/`any`/`choose` consume the boolean but never block on a false
  value. `DEPENDENCY_INVALID`/`BLOCK_INVALID` is raised **only for type
  errors** (`evaluator.py:79,83,204,300`). No "projection-error path" exists
  in the evaluator or runner.
- `SOURCE_SET_UNCLOSED` (`BLOCK_CLOSURE`, `evaluator.py:26`) is specifically
  the **empty-source-set closure** code — raised by `require_closed` and the
  empty-`collect` path (`evaluator.py:191-193`, `:122-130`). It is about
  whether a family is *closed*, not about a row-sum/line invariant. For the
  populated tie-out case (2+ members) `collect` returns at `:131` and
  **registers no closure read** (adversary A2, verified), so a stale *member*
  supersession changes a member finding id, not any closure finding — even
  the horizon-skew subclass does not route through `SOURCE_SET_UNCLOSED` here.
The honest position — held by *both* builders — is that tie-out is an
**unbuilt Track-1/2 package-validation invariant** ("true by construction" /
package validation), not a committed evaluator code. The synthesis restates
an unbuilt invariant as committed vocabulary. **FAILS.** The charter's "check
the semantics, not the string" does not rescue this: the *semantics* claimed
(a committed projection-error family covers tie-out) is itself the unsupported
claim.

### Case 5 — Supersession both ways (late answer; superseded answer under a current attachment)
The synthesis adopts it2's posture: the attachment pins every Part III answer
and row-source fact; a superseded pinned fact makes it non-current (ADR-0010);
a late answer supersedes the *blocked* disposition via re-run. This requires
every answer to actually be **referenced and pinned**. Under string encoding
`all(...)` evaluates every arg (all truthy) → every answer enters
`access.refs` → pinned → displacement reaches the attachment. Holds. But under
boolean encoding the `all` short-circuit (cases 1–2) leaves a later answer
un-referenced and therefore **un-pinned**, so its supersession has no input
edge to displace the attachment — exactly adversary A5. **HOLDS-WITH-
CONDITION** (same encoding/unconditional-pin condition).

### Case 6 — Generalization: Schedule D stub, zero Schedule-B surface
The synthesized citizen leaves row *shape* to per-schedule content (hardening
note), removing the 1099-shaped `payer_key`+`amount_key` surface from the
ontology — which directly answers adversary A3. Governance and adversary both
verified the schema is schedule-agnostic (threshold-as-parameter,
Part-III-as-array). The Schedule D stub instantiates with zero SB-specific
schema keys. **HOLDS** (strengthened by the hardening note).

---

## Beyond the six — error-vocabulary claim (charter-directed)

The charter directs me to verify two committed-behavior claims. **Both are
mis-stated.**

1. **"projection-error path is the right family for tie-out":** No such path
   exists (case 4). Unsupported by source.
2. **"`SOURCE_SET_UNCLOSED` is the committed code where the designs cited
   `SOURCE_SET_OPEN`":** Both strings are committed, in different layers.
   The runner emits `SOURCE_SET_UNCLOSED` in reports (`evaluator.py:26`,
   recorded verbatim `runner.py:406-417`; see committed
   `sample_data/.../open_empty_1099int/expected/report.json:5`). But the
   **disposition-record/walk/form-field code enums permit only
   `SOURCE_SET_OPEN`**, not `SOURCE_SET_UNCLOSED` (`derivation-record.v2:10`,
   `npe-walk.v1:7`, `form-field.v2:5`, and committed content
   `form1040.line-2b.form-field.json:32`). So:
   - `evaluation-analysis.md` calling `SOURCE_SET_OPEN` a **"nonexistent
     code"** (and `synthesis.md` "corrected to `SOURCE_SET_UNCLOSED`")
     **misstates the round-1 finding.** Adversary A6 said the opposite: both
     exist, in two layers, and "implementation must reconcile the emitted
     category with the recorded code … Hardening note, pre-existing." The
     synthesis flattens a real two-layer reconciliation into a false
     "nonexistent → corrected," silently dropping the adversary's actual point.
   - The chosen "committed code" `SOURCE_SET_UNCLOSED` is the one the
     **disposition record/walk enum forbids** — a blocked attachment recorded
     with it would violate `derivation-record.v2`. The designs' original
     `SOURCE_SET_OPEN` is the valid *recorded* code at the layer an
     attachment's block actually lives. The synthesis's correction runs
     backwards for that layer.

This unreconciled emit-vs-record discrepancy is pre-existing to D1; the
synthesis should surface it as a production condition owed to Track 1, not
paper over it as a settled "committed code."

## Data safety
No real personal value or workspace path in the synthesis or in this review.
"$1,500"/"over $1,500" are public statutory constants. (Governance's G3
`tax.us.2025.*`-vs-`demo-*` process flag persists in the synthesis's carried
examples; not a data-safety breach, noted.)
