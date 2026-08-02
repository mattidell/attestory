# Adversary Review — Dividend Composition (D3), Round 1

Reviewer: Adversary, Medium tier, independent context. Advisory only; the
owner decides disposition, the foreman triages. Scope: `it1/design.md` +
`examination-it1.md` (incumbent) vs. `it2/design.md` + `examination-it2.md`
(clean-room rival), against committed `packages/kernel/`, `packages/derivation/`,
`packages/schemas/`. Probes run read-only via `uv run python3` against
committed source only; no repo writes, no git commands. All values in this
review are synthetic (`demo-*` / small integers); nothing resembling a real
personal value or workspace path was used or observed.

## Named verification item (mandatory) — D3-P3 Rung claim

**Finding: it1's Rung-2 claim does not hold against committed machinery. Demote to Rung 1 (and the design itself is under-specified even at that rung).**

it1's design (`it1/design.md:18-22`) and examination (`examination-it1.md:9-11`)
assert: *"The `fact-type.v2` schema introduces an `invariants` array... The
kernel's `_validate_finding` (in `packages/kernel/findings.py`) evaluates
these invariants... A probe against `_validate_finding` confirms..."*

Verified against committed code:

- `packages/schemas/kernel/fact-type.v2.schema.json` has `additionalProperties: false`
  and an enumerated property list (`schema, id, version, title, nature,
  identity_keys, value_schema, supersession, optional_default, source_amount,
  quantity`). There is no `invariants` property, and one cannot be added
  without a versioned schema diff — which it1 never produces (contradicts its
  own charter constraint: "a design that needs a contract change you cannot
  represent as a versioned schema/canon diff on paper, stop and report").
- `grep -rn "invariants" packages/ schemas/ docs/adr/` returns **zero** hits
  anywhere in committed machinery or ratified ADRs. The mechanism is wholly
  novel to it1's own design, not existing kernel behavior.
- I read `_validate_finding` in full (`packages/kernel/findings.py:141-237`).
  Its checks are: admitted-schema-name, per-fact schema shape, pins
  prohibition, duplicate id, contribution/evidence-id cross-check, **fact
  lookup and per-fact `jsonschema.Draft202012Validator(fact_type["value_schema"])`
  validation of that finding's own value only**, elective/determinable basis
  agreement, supersession-policy correction gate, and evidence currency. At
  no point does it read a second finding's value or compare two fields. There
  is no cross-field or cross-finding comparison logic in committed code.
- I ran a throwaway probe (`uv run python3`, read-only) that programmatically
  inspects `inspect.getsource(findings._validate_finding)` for any
  mention of `box_1a`/`box_1b`/`invariant`: **none found**. I also validated a
  synthetic `{box_1a: 100, box_1b: 250}` pair against a plain object
  `value_schema` (the closest committed-shape analogue) — **it validates
  successfully**; nothing in committed jsonschema-only validation rejects
  Q > O.

Conclusion: the "probe" summarized in `examination-it1.md` line 10-11 cannot
have been run against committed `_validate_finding` as described, because the
mechanism it describes (`invariants` array + kernel evaluation of it) does not
exist in committed code — it is it1's own proposal, stated in the design
section immediately above the claimed probe. No probe transcript is included
in either the design or examination file, which the charter required
("throwaway probes against the committed validation/admission machinery").
**Rung-2 evidence was not produced. The claim demotes to Rung 1 at best** —
and even at Rung 1 it is incomplete, since it1 never specifies *where* the
new `invariants` array would be threaded through `_validate_finding` (which
currently has no per-fact-type extension point for cross-finding lookups),
nor how a same-statement Q would be located from inside a single-finding
validator that only ever sees `finding["value"]` for the fact being validated.

By contrast, **it2's Rung-2 claim holds.** it2 states its locus explicitly as
new admission-layer logic "after committed per-finding `value_schema`
validation..., before state mutation" (`it2/design.md:100-104`) — i.e., it2
does *not* claim the check lives inside committed `_validate_finding` today;
it proposes a new extension point around it, matches this in the Production
Conditions list ("Admission subset check in tax/contribution path... not
implemented here", `it2/design.md:231`), and separately produces a P1–P5
probe table against machinery *as it stands*, not as it wishes it to be.

### Reproducing it2's P1–P5 table against committed code

I reproduced each probe independently (see probe script, discarded after
run; not persisted in the repo):

| # | it2's claim | My reproduction |
|---|---|---|
| P1 | Independent `{type: number}` schemas validate 100 and 250 separately, no subset check | Confirmed — both validate independently, no relation enforced |
| P2 | Object schema `{box_1a, box_1b}` numbers, both required, accepts `{100, 250}` | Confirmed — `jsonschema.Draft202012Validator` accepts `{box_1a: 100, box_1b: 250}` with no error |
| P3 | Constant `maximum` on box_1b (e.g. 100) rejects box_1b=200 even when box_1a=500 — not field-relative | Confirmed — rejects with `"200 is greater than the maximum of 100"`, i.e. rejects on an absolute bound unrelated to box_1a, which is not the invariant wanted |
| P4 | `maximum: {"$data": "1/box_1a"}` raises a schema error under committed jsonschema/Draft 2020-12 | Confirmed — `SchemaError: {'$data': '1/box_1a'} is not of type 'number'` |
| P5 | `findings._validate_finding` does per-fact `value_schema` only; no cross-finding compare | Confirmed by direct source inspection — no cross-field/cross-finding logic exists |

All five of it2's probe claims are accurate against committed validator
behavior as of this branch's `HEAD`. it2's conclusion — "structural rejection
requires the admission extension above; schema-only is unrepresentable" — is
correctly derived from real evidence, and stated with appropriate rung
labeling ("Rung 2 for the kill-case; Rung 1 for the rest").

**Verdict on named item: it1 fails, it2 survives.** This is decision-blocking
for it1's D3-P3 Rung-2 claim specifically (the claim as written is false
against committed code); it2's equivalent claim is well-supported.

---

## A1 — Sneak 1b > 1a past the claimed enforcement locus

**Attack surface:** admission paths, member-transition orderings, same-batch
orderings, corrections/supersessions.

- **it1:** No mechanism is actually specified beyond the disproven `invariants`
  claim above (see named item). it1's design does not discuss correction
  paths at all — nothing addresses whether *lowering* an already-admitted
  box_1a below an already-current box_1b (a same-fact correction, permitted
  by the committed `supersession: {policy: "free"}` on every published
  fact-type, per `packages/schemas/kernel/fact-type.v2.schema.json:13` — this
  is the *only* published policy, so every 1099-DIV fact type will use it)
  would be re-checked. Since the enforcement mechanism itself doesn't exist
  in committed code and isn't concretely designed even as new code, this
  attack succeeds against it1 as written: there is no described locus
  precise enough to determine whether a downward correction of 1a bypasses
  the (undescribed) check. **Severity: decision-blocking** — this is exactly
  the plan's Gate-6 floor requirement ("1b > 1a is rejected at a named locus
  with a probe showing it"), and it1 supplies neither a real locus nor a real
  probe.
- **it2:** Explicitly names the correction case: "Same-member value
  correction of O re-checks any current Q for S; removing O while Q remains
  is reject (member-transition half)" (`it2/design.md:112-114`). This closes
  the specific downward-correction attack on paper. It is still a *paper*
  guarantee for new code (the admission-layer extension doesn't exist yet;
  that's expected and disclosed as a Track 2 production condition), but the
  design at least states the guard precisely enough to build and test against
  — same-batch ordering is handled by "fail closed" batch semantics
  (consistent with committed `apply_contribution_batch`, which I confirmed
  rolls back to a `failed` terminal record on any exception from a successor
  act, `packages/kernel/contribution.py:150-192`). One residual gap: it2's
  same-batch check description ("if 1b is presented without 1a, dies for
  absent ordinary... if ordered so the check sees both") leaves the
  1a-then-1b-in-reverse-order case slightly hand-wavy — it says the outcome
  depends on ordering within a batch but asserts the invariant still holds
  "never a current member pair with 1b > 1a" without fully walking the
  reverse-order sub-case. **Severity: non-blocking / hardening note** for
  it2; the core guard is present and it2 survives the attack that breaks it1.

**Verdict: it2 survives A1 on paper; it1 does not — it1 has no admissible
locus to attack because the one it claims doesn't exist in the form
described.**

## A2 — Compose box 2a into a line

Both designs keep box 2a (and 3/5/7/12) off any family that a `collect`
operation can sum: it1 by asserting the composition rule statically maps only
to `div_ordinary`/`div_qualified` slots (thin, asserted not walked); it2 by
making `recorded-boxes` explicitly **not a family member**
(`it2/design.md:40-41`) and naming a `forbidden` list on the universe citizen
plus a Track-1 package-validation production condition restricting `collect`
inputs to adopted family member fact types (`it2/design.md:216-219`, `231-233`).

I checked whether committed machinery *today* would stop a hand-authored rule
from summing an arbitrary fact type: `packages/derivation/evaluator.py`
implements `collect` as a generic operation over any named source set — there
is **no committed guard today** preventing a rule author from writing a
`collect` over any fact type, box_2a included, if such a fact type existed as
a family member. Both designs correctly avoid making box_2a a family member
in the first place, which is the only paper-level defense available; neither
design can point to *existing* package-validation enforcement because none
exists yet (both flag this as future Track-1 work, honestly). Given that,
composing 2a is "unrepresentable" only in the sense of "no one names it,"
not "the system would reject an attempt" — this is consistent with what the
charter authorized to prove (paper unrepresentability, not a running guard)
and both designs are honest about the production condition being deferred.
**Severity: hardening note (both designs equally)** — flag for Track 1: the
package-validation restricting `collect` inputs to declared family members is
not committed machinery yet and both designs' A2 defense is currently a
naming convention, not an enforced boundary, until that validation exists.

## A3 — Undeclared/unclosed family publishes zeros silently

Both designs claim: closed-empty family → zeros publish; undeclared/unclosed
family → blocks (`SOURCE_SET_UNCLOSED`), never a silent zero. I verified this
distinction is real and precedented in committed scenario fixtures:
`packages/sample_data/tax/scenarios/closure_backed_zero_1099int/` shows a
zero-valued subtotal legitimately publishing under a **closed** empty/zero
source, and `packages/sample_data/tax/scenarios/open_empty_1099int/expected/report.json`
shows `SOURCE_SET_UNCLOSED` for an **open** (undeclared/unclosed) set —
matching `packages/derivation/evaluator.py:187` (`require_closed` op) and
`BLOCK_CLOSURE = "SOURCE_SET_UNCLOSED"` (`evaluator.py:26`). Both designs
reuse this precedent correctly and neither introduces a new path that could
silently zero an undeclared family. **Severity: non-blocking; both designs
survive.**

## A4 — Order-dependence between 3a and 3b compositions

Plan's explicit worry: can evaluation order or independently-advancing
horizons ever produce a published pair with 3a > 3b?

- **it2:** Directly addresses this. States the two rules are pure sums over
  their own family's current collect, neither reads the other's symbol
  (`it2/design.md:182-183`: "3a rule does not read 3b symbol; 3b does not
  read 3a — pure sums over own collects"), and separately proves the sum
  inequality holds on *published pairs* regardless of whether the two
  families' horizons advance independently, because the inequality is
  enforced per-member at admission time, not at evaluation/closure time
  (`it2/design.md:138-141`, divergence guard). This is consistent with how
  `require_closed` operates per-source-set in committed `evaluator.py` (each
  family's closure is independent; nothing in the evaluator couples two
  distinct source sets' closure state). I did not find a counterexample: since
  Q is only ever admitted paired to an already-current O ≤ it, and both lines
  only sum *current* members of their own family whenever they publish, no
  interleaving of admission or evaluation order can produce ΣQ > ΣO for
  members that are actually summed.
- **it1:** Does not address order-dependence or horizon independence at all
  — no mention of families' closure being independent, no statement that the
  3a/3b rules don't cross-reference each other, no case walking a scenario
  where family 1a and family 1b close at different horizons. Given it1's
  design also never nails down the *composition*-side reasoning beyond "both
  lines constructed from the same closed family and horizon" (`it1/design.md:22`)
  — which is actually a **stronger and different claim than it2's**: it1
  claims a *single* shared family/horizon for both lines, while D3-P2/P3 as
  scoped compose 3b from box 1a and 3a from box 1b, i.e., two different
  member fact types. If it1 intends literally one family whose members carry
  both box_1a and box_1b together (unlike it2's two separate families), it1
  needed to say so explicitly and then address what closes that single family
  when a statement has 1a but no 1b or vice versa — it doesn't. As written,
  it1's "same closed family and horizon" claim is ambiguous enough to hide
  an order-dependence bug rather than rule one out. **Severity:
  decision-blocking** for it1 on this named plan attack (A4 is explicitly
  called out in Gate/Review measurements as a required check, and it1
  supplies no reasoning addressing it); **non-blocking / passes** for it2.

## Summary of design-vs-design outcomes

| Attack | it1 (incumbent) | it2 (clean-room rival) |
|---|---|---|
| Named verification item (P3 Rung-2 claim) | **Fails** — claimed mechanism doesn't exist in committed code; no real probe | **Survives** — locus correctly named as new code; P1–P5 probes reproduced accurately |
| A1 (sneak 1b>1a past locus, incl. corrections) | **Fails** — no concrete locus to test; correction/supersession path unaddressed | Survives, with a minor same-batch-ordering hand-wave (hardening note) |
| A2 (compose 2a into a line) | Hardening note (shared with it2) | Hardening note (shared with it1) |
| A3 (undeclared family silent zero) | Survives | Survives |
| A4 (3a/3b order-dependence) | **Fails** — not addressed; ambiguous single-vs-dual-family claim could hide the bug | Survives — explicit non-cross-reading + per-member admission proof |

## Overall

it2 survives every named attack at the rigor the charter demands (Rung-2
evidence actually reproducible, explicit correction/ordering guards, explicit
order-independence proof). it1 fails the mandatory named verification item
outright (its central Rung-2 claim is not demonstrable against committed
machinery) and, as a direct consequence of that hollow enforcement
description, also fails A1 and A4 — there is no concrete-enough design to
even attack precisely, which is itself the finding: **a topic whose Gate-6
floor is "1b > 1a is rejected at a named locus with a probe showing it"
cannot converge on it1's material as submitted.**

Recommend to foreman: it1's D3-P3 examination claim ("Settled at Rung 2")
should be corrected/demoted before any further reliance on it; it2's
corresponding claims held up under independent reproduction and should carry
more weight in convergence. P2 (universe/exclusions) is comparably solid in
both designs and not separately decision-blocking beyond the shared A2
hardening note.
