# Paper Spike — CA-05 and CA-06 Production Substrates

Audience: Owner, Foreman.

Date: 2026-08-02. Foreman-run, Rung 1 paper only. No Builder charter, no
committee review — a bounded substrate question, not a rival-topology
design question (Gate 1 scores below the prototype-eligible band for both).

## Why this exists

ADR-0052 Decisions 3 and 4 named two production conditions explicitly not
resolved by that ADR: CA-05 (Schedule D's required/not-required disposition
is categorical, but `attachment-rule.v2`'s `requirement` block is
threshold-only) and CA-06 (whether two mutually exclusive rule citizens may
both declare `publishes` for the shared `selected-preferential-base` symbol,
or a dedicated selection mechanism is needed). Per `PROJECT_PLANNING.md`
Gate 2, a missing substrate discovered mid-prototype routes to its own
decision rather than being silently absorbed into the next track's
implementation charter. This spike is that decision, sized to its actual
cost: both questions are narrow schema/representation choices, not
competing product topologies, so a paper spike is the correct rung —
no incumbent/rival round, no committee.

## CA-05 — categorical attachment requirement

**Gate 1 score:** blast radius 1 (future schedules may reuse the shape, but
the shape itself is a narrow generalization); migration cost 1 (additive
`oneOf`, no existing citizen changes); residual uncertainty 1 (the shape is
determined by the existing `completeness.required_answers` presence-check
idiom already in `attachment-rule.v2`); inability to test cheaply 1. Total
4 — paper spike, not full prototype.

**Current shape.** `packages/schemas/tax/attachment-rule.v2.schema.json`'s
`requirement` object requires `subtotals`, `threshold_parameter`,
`comparison: strictly_greater_than`, and `citation` — every field
mandatory, numeric-threshold only.

**Resolution.** Publish `attachment-rule.v3` as an additive successor
(unused version, `attachment-rule.v2` untouched) whose `requirement` block
becomes a `oneOf` between the existing threshold shape and a new
categorical shape:

```
requirement.categorical = {
  kind: "family_nonempty",
  source_family: <pin to the eligible-transaction source family>,
  citation: <pin>
}
```

Semantics: the attachment is required whenever the named source family is
current and closed with at least one member; not required when the family
is current and closed-empty; the trigger itself is `blocked` (not
`not-required`) when the family is unclosed, mirroring the existing
threshold branch's honest-block behavior on an unclosed subtotal. This
follows the milestone's bounded scope directly — for this class, Schedule
D's requirement is driven by the eligible long-term family's own presence,
not by a numeric comparison, and not by any other named absent-source
condition (those are completeness authorities, Decision 2, not independent
triggers).

**Production condition, still owed:** the exact JSON Schema text, its
schema-registry publication, and Schedule D's `attachment.schedule-d.v1`
citizen instantiating it are Track 2 implementation work, not this spike.
This spike settles only the shape and trigger semantics.

## CA-06 — exactly-one-producer for the selected preferential base

**Gate 1 score:** blast radius 2 (a generic multi-producer-symbol pattern
could recur); migration cost 1 (no existing citizen changes — see
resolution); residual uncertainty 1 (resolved below by direct evaluator
inspection, not by design judgment); inability to test cheaply 1. Total 5 —
paper spike, not full prototype.

**The question as ADR-0052 left it.** Whether two mutually exclusive rule
citizens may both declare `publishes: "...selected-preferential-base"`, or
whether a dedicated selected-binding citizen is required. ADR-0052 Decision
4 already noted that current package validation enforces exactly one
*reachable adopted* producer per symbol (ADR-0027 Decision 5), and that
ADR-0038 Decision 2 forecloses a *dynamic* `conflict_semantics` selector as
a line-16 pattern. Read together, those two facts mean: a package **may
not** contain two separate rule citizens that each declare `publishes` for
the same symbol, full stop — that is exactly the shape ADR-0038 forecloses,
and exactly what would trip ADR-0027's exclusivity check.

**Resolution: no new substrate is needed.** The existing accepted pattern
already used by `rule.form1040-line7a.json` and the current
`rule.form1040-line16` successor is a **single** rule citizen with multiple
pinned upstream inputs and internal branching via the evaluator's `choose`
operator (`packages/derivation/evaluator.py`, `op == "choose"`), which
lazily evaluates only the taken branch — so an untaken branch's absent
inputs are never read and never surface as a missing dependency. The
selected preferential base is modeled the same way: **one** rule, `publishes:
"tax.us.2025.schedule-d-covered-ltcg-8a.selected-preferential-base"`
(exact identifier is Track 2's naming), pinning both the direct-route
inputs (box-2a subtotal, C1-C4, checked conclusion) and the Schedule-D
inputs (Schedule D line 16, the attachment disposition, the nine
completeness authorities). Its top-level expression is a `choose` keyed on
whether the eligible long-term transaction family is current and
closed-nonempty (checked via `require_closed` plus a non-empty `collect`,
the same idiom every existing family-gated rule already uses):

- when the eligible family is closed-nonempty: evaluate the Schedule-D
  branch (requires Decision 2's full boundary; publishes Schedule D line
  16's value; the untaken direct branch's inputs are never read, so a
  missing/absent C1 is never named);
- otherwise: evaluate the direct branch (requires the checked conclusion
  and box-2a subtotal; publishes the box-2a value or its blocked/guard
  disposition; the untaken Schedule-D branch's inputs are never read).

This is not a new evaluator operation, a new schema, or a new generic
substrate — it is the existing single-producer, internal-`choose` pattern
already accepted and in production for line 7a and line 16. `P`'s
"producer signature" (ADR-0052 Decision 4's exact pin table) is exactly
which branch of this one rule's `choose` was taken, recoverable from which
inputs the rule's own access log pinned — matching the Rung-1 pin contract
ADR-0052 already ratified, now with its mechanical representation settled.

**Production condition, still owed:** the exact rule content and its
`choose` expression tree are Track 2 implementation work. This spike
settles only that no new generic substrate, schema, or evaluator feature is
required — the existing single-rule/internal-`choose` idiom suffices.

## Disposition

Both questions resolve at the paper rung; neither needs a rival round or
committee. CA-05 gets one new additive schema successor
(`attachment-rule.v3`); CA-06 gets no new schema or substrate at all — a
representation clarification that Track 2 was always free to use. Recorded
as ADR-0053, an additive addendum to ADR-0052, not an edit to it or to
ADR-0027/ADR-0036/ADR-0038/ADR-0050.
