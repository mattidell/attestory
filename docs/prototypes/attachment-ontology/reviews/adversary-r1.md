# Adversary Review R1 — Attachment Ontology (D1)

Seat: Adversary (High tier, independent context). Advisory only; owner decides
disposition, foreman triages. I authored none of what I review. Designs read:
`it1/design.md` + `examination-it1.md` (incumbent), `it2/design.md` +
`examination-it2.md` (sealed rival). Committed machinery verified against
`packages/derivation/runner.py`, `packages/derivation/evaluator.py`, and the
`packages/schemas/derivation/` + `packages/schemas/tax/` schemas at HEAD
(`d3e5a52`). All values below synthetic. No git writes; no repo modification
outside this file.

Verdict headline: **it1 has a decision-blocking completeness hole that it2
does not** (A1/A5), and **it1's tie-out divergence guard rests on a misapplied
committed-machinery citation** (A2/A6). it2 is the sounder design at Rung 1,
with two non-blocking gaps of its own.

---

## A1 — Blocking placement, both directions

**Direction 1 (a required-incomplete block swallows a publishable sibling
line 2b/3b/3a): both designs survive, verified.** The runner fires each rule
independently; `attempt` (`runner.py:302–418`) blocks only the artifact under
evaluation and never un-publishes a symbol already in `self.symbols`
(`:400`). A block can reach a line only through an `unmet_reference` edge, and
that edge exists only if the line rule lists the attachment symbol in
`requires`/refs. The committed line rules (2b/3b/3a) predate the attachment
symbol and cannot reference it; the NPE walk (`npe-walk.v1`) therefore has no
edge from a line node to the attachment node. Shared-closure coupling does not
break this: if 2b and the attachment both read the same family and that closure
blocks, both block *on their own honest dependency*, not on each other. Holds
for it1 and it2.

**Direction 2 (a required-incomplete attachment publishes whole): it1 FAILS;
it2 survives.** — DECISION-BLOCKING, it1 only.

it1's completeness token (`it1/design.md:188–197`) is a single `choose`:

```
choose
  when: foreign-account == "yes"
  then: ref(foreign-account-country)   # only country checked
  else: ref(foreign-trust)             # only trust checked
```

`choose` evaluates only the taken branch (verified `evaluator.py:169–171`).
So when `foreign-account = "yes"` and the country is present, the `then`
branch returns and **`foreign-trust` is never dereferenced** — its absence is
never detected. A taxpayer who has a foreign account can have the attachment
publish as `required_complete` **while the Schedule B foreign-trust question
(line 8) is unanswered**. That is precisely the forbidden failure mode: a
factually incomplete attachment publishes whole. The two Part III questions are
independent mandatory answers; it1 collapses them into mutually-exclusive
branches of one `choose`, so one always masks the other. This is a structural
logic hole, independent of value representation.

it2 uses `all(ref(foreign_financial_accounts), ref(foreign_trusts),
<country gate>)` (`it2/design.md:100–105`). `all` iterates its args
(`evaluator.py:160–161`) and each `ref` raises `EvalBlocked(DEPENDENCY_ABSENT)`
on absence (`evaluator.py:108–111`), so **both** base answers must be present or
the attachment blocks. it2 does not have the masking hole. (Fragility note under
A-notes below: `all` short-circuits on the first *falsy* value, so it2's
presence-guarantee relies on "no"/"yes" being non-empty truthy strings; a
boolean-`false` representation would let a later answer's absence slip
unblocked. Robust form evaluates every presence ref unconditionally, not inside
`all`.)

---

## A2 — Row/line tie-out: break divergence unnoticed

**it1: DECISION-BLOCKING — the divergence guard cites a mechanism that does not
apply to the case it guards.** it1 (`design.md:164–170`, `exam:46–48`) states:
"the runner pins the exact closure finding id a subtotal stood on
(`runner.py:279`); the itemization must stand on that same pinned closure
finding; if a statement is superseded … the subtotal's closure-finding id
changes → `SOURCE_SET_OPEN`." Two verified errors:

1. `runner.py:279` (`admission.closure_finding_id`) is reached only for
   `access.closure_reads` families, and `closure_reads` is populated **only on
   the empty-family path** of `collect` (`evaluator.py:122–130`). When line 3b
   has actual members — cases 2 and 4, two 1099-DIV statements — `collect`
   returns amounts at `evaluator.py:131` and **never registers a closure read**;
   the subtotal pins the member finding ids as inputs (`runner.py:261–266`), not
   a closure finding. So "the subtotal's closure-finding id" does not exist in
   the populated tie-out case, and superseding a *member* statement changes a
   *member* finding id, not any closure finding.
2. By it1's own account (`design.md:152–154`) "rows are not a rule value" — the
   itemization is a declarative projection outside the evaluator. It therefore
   produces no `AccessLog`, reaches `pins_for` never, and cannot "stand on" any
   runner pin at all. The cited runtime guard structurally cannot bind the
   itemization.

The real protection it1 *could* have claimed (subtotal and projection both
enumerate the same member findings, so a member supersession displaces both) is
never stated; instead the only enforcement is deferred to an unbuilt Track-2
package validation ("true by construction"). Against the attack's bar —
"a hard error, not a hope" — it1 offers a hope plus a misapplied citation, on a
proposition Gate-5 marks decision-blocking. Hence decision-blocking.

**it2: NON-BLOCKING gap.** it2 makes rows a real op `collect_members` returning
`{finding_id, identity, value}` pinned as ordinary inputs (`design.md:140–147`),
so rows are genuinely in the derivation graph and supersession displaces along
input edges (Article 7) — a materially stronger provenance story. But its
tie-out enforcement — `compare(subtotal, ref(tie_out_symbol), eq)` "else
`DEPENDENCY_INVALID`" (`design.md:156–158`) — is **not committed behavior**:
`compare` returns a boolean (`evaluator.py:155–158`); `DEPENDENCY_INVALID`
(`BLOCK_INVALID`) is raised only for type errors (`evaluator.py:79,83,204,300`),
never for a false equality. No op converts a false tie-out into a block, and
it2's Track-1 inventory (`design.md:280–288`) adds only `collect_members`, not
an asserting op. So it2's "never silent divergence" is not yet expressible; the
hard error is asserted, not exhibited. Non-blocking because it is a namable
paper canon addition, and rows remain pinned regardless.

Net A2: **it2 is the stronger design; neither exhibits a committed hard-error
tie-out.** it1's is decision-blocking (misapplied load-bearing citation on a
decision-blocking proposition); it2's is a non-blocking specification gap.

---

## A3 — Generalization: find the hidden Schedule-B assumption

**Both pass the thin Schedule-D stub; both embed a 1099-shaped row model —
shared HARDENING note, slightly worse for it1.** At the *citizen* level neither
stub touches Schedule-B-only schema keys: threshold-as-parameter and
Part-III-as-array/empty let both instantiate `form.form_id:"Schedule D"`
unmodified (`it1:235–243`, `it2:261–276`). The generalization defended by the
plan's case 6 (citizen shape) holds for both.

But the **row model** carries a Schedule-B assumption the stub does not exercise.
it1 hardcodes `row_projection: { payer_key, amount_key }` (`design.md:52`) — a
two-field payer+single-amount shape lifted straight from 1099-INT/DIV. A
Schedule D transaction row is not payer+amount; it is
`{description, acquired, sold, proceeds, basis, gain}`. it1's schema cannot
express it without adding fields — i.e. the row surface *is* Schedule-B-shaped.
it2 abstracts to `member_fact_type` + `payer_key` + a single `value`
(`design.md:44–49,145–147`), marginally more generic but still single-valued;
it too cannot carry proceeds-and-basis without extension. The plan's case 6 only
demands a stub with zero SB-specific *schema* surface, which both meet, so this
is non-blocking — but it undercuts the "ontology, not Schedule-B-shaped" claim
both examinations make. it1 is more exposed (named `amount_key`); it2 is one
abstraction better. Recommend the eventual ADR state row cardinality
(single-amount vs multi-column) as an explicit open question, not a settled one.

---

## A4 — Threshold boundary (exactly $1,500)

**Both PASS.** it1: `cmp:"gt"`, threshold in a parameter, "over ⇒ gt, exactly
$1,500 is not over," citation `demo.citation.schedule-b.threshold`, boundary
exercised as testable case content (`design.md:76–92,216`). it2: `gt`,
`{ "over": 1500 }`, "exactly $1,500 → not_required; 1500.01 → required," citation
pin (`design.md:84–91,230`). `_compare`/`gt` is strict (`evaluator.py:155–158`),
so both are correct and the boundary is testable content, not prose. "over
$1,500" is the real statutory phrasing (a public constant, not a personal
value). No finding.

---

## A5 — Supersession posture

**it2 sound and explicit; it1's masking bug (A1) recurs here — advantage it2,
non-blocking except as it compounds the A1 finding.** it2 makes Part III fact
types freely supersedable and pins every consumed answer, so a post-publish
answer correction displaces the attachment along input edges
(`design.md:171,185`, Article 7). Verified plausible: refs are recorded in
`access.refs` and pinned as inputs, so displacement reaches the attachment.

it1 relies on generic supersession without stating it, and — critically — its
`choose` token does not reference `foreign-trust` when `foreign-account="yes"`,
so that answer is **never pinned**. A later supersession of the foreign-trust
answer therefore has no input edge to the attachment finding: **the attachment
stays "current" over a foreign-trust fact that is no longer current.** This is
the A1 hole viewed through supersession; it strengthens, not duplicates, the
decision-blocking A1 finding against it1.

---

## A6 — Verify Rung-1 committed-machinery citations

**it1 evaluation-order citations: verified correct.** `requires` checked before
guard (`runner.py:314–318`), guard short-circuits value (`:342–351` returns
before `:354`), absent `ref` blocks naming the fact (`evaluator.py:108–111`),
`choose`/single-branch (`:169–171`), `collect` drops identity (`:118–131`),
three walkable node kinds `published`/`blocked`/`guard_inapplicable`
(`npe-walk.v1.schema.json:7`). The state-model spine (three states ↔ three
ratified disposition/walk kinds, no new disposition machinery) is accurately
grounded — this part of it1 is solid.

**it1's one wrong load-bearing citation is the P2 divergence guard**
(`runner.py:279`, closure-finding pinning) — see A2. Per the plan's A6 rule ("if
a load-bearing citation is wrong, that is a decision-blocking finding") and
Gate-5 (the tie-out relation is decision-blocking), this is decision-blocking.

**it2 citations: verified correct.** Value-time `EvalBlocked` recorded as
`blocked` (`runner.py:354–358`), `choose` single branch, `compare`/`gt`/`any`
committed. `collect_members` is honestly flagged as a *new* paper canon op
(`operation-semantics.v2`), not passed off as committed — within the rung.
it2's only citation-adjacent overreach is the `DEPENDENCY_INVALID`-on-tie-out
claim (A2), which mis-describes what `compare` does; non-blocking as noted.

**Shared minor (both):** both cite `SOURCE_SET_OPEN` as the open-family
incompleteness code. The evaluator raises `SOURCE_SET_UNCLOSED`
(`evaluator.py:26`); the record/walk vocabularies use `SOURCE_SET_OPEN`
(`derivation-record.v2`, `npe-walk.v1`, `form-field.v2`). Implementation must
reconcile the emitted category with the recorded code; the designs quietly
assume a translation that is not visible in `evaluator.py`. Hardening note,
pre-existing to this topic.

---

## Attacks not landed (both designs sound)

- A1 direction 1 (block swallowing a sibling line) — structurally excluded by
  the independent-rule / no-back-edge argument, verified in the runner.
- "not-required is silence" — both publish a walkable disposition (it1
  `guard_inapplicable`; it2 a published `not_required` finding). Both defensible;
  it2's is arguably more explicit (a positive finding vs a guard-false node).
- FinCEN 114 named-not-produced — both name the obligation as disposition
  content only; neither introduces a form/rule/package member for it.

---

## Data safety

All reviewed values are synthetic (`demo-*`, `tax.us.2025.*`). "$1,500" and
"over $1,500" are the public statutory Schedule B threshold/phrasing, not a
personal value. No real personal value or quarantined workspace path appears in
either design or in this review.
