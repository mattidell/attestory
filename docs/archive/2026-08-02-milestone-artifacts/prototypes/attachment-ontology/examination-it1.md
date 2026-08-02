# Examination: Attachment Ontology (D1, Incumbent It1)

Rung 1 only. Each proposition is stated separately as **settled-at-rung** or
**unresolved**, citing the design's cases. No probe was executed: the one
climb-eligible question (does ratified machinery express the threshold
conditional and the completeness gate *as committed*?) was settled by *reading*
committed contract text — `packages/derivation/runner.py:302–351` and
`evaluator.py:108–192` — which is static Rung-1 evidence, not a probe.

## D1-P1 — The attachment citizen — **settled at Rung 1**

The three states map 1:1 onto three ratified disposition kinds
(`published` / `guard_inapplicable` / `blocked`), each an `npe-walk.v1` node
kind — so the ontology adds a citizen (`attachment.v1`) but **no new
disposition machinery**. Settled by:

- **Requirement conditional (cases 1a/1b):** expressible in committed
  `rule-artifact.v2` ops (`any`/`compare gt`/`parameter`/`ref`); the $1,500
  threshold is a *parameter*, "over" ⇒ `gt`, so exactly $1,500 is not over
  (case-1 boundary). R1 publishes a walkable `required` finding.
- **Not-required is a disposition, not silence (case 1b):** R2's guard-false
  path yields a recorded, walkable `guard_inapplicable` node (`runner.py:342`),
  and R1's published `required=false` carries the threshold trace.
- **Blocking placement (case 3):** committed evaluation order — `requires`
  checked before guard (`:315`), guard short-circuits value (`:342`), an absent
  `ref` blocks naming the fact (`evaluator.py:110`) — makes incomplete a true
  `blocked` while not-required never demands answers. Non-propagation to sibling
  lines is **by construction**: no line rule refs the attachment symbol, so no
  NPE edge exists for the block to travel; already-published line symbols persist
  (`:400`). The "publish a categorical state" rival is rejected — a published
  `"incomplete"` violates honest blocking.

No representation gap; nothing requires a contract change I could not express as
the on-paper `attachment.v1` diff plus two `rule-artifact.v2` rules.

## D1-P2 — Part I/II repeating-row itemization + tie-out — **settled at Rung 1**

- **Row model (case 2):** `collect` drops payer identity (`evaluator.py:118`),
  so rows are *not* a rule value; the `itemization_part` declares a projection
  over the closed family's **member statement facts** (ADR-0015 payer identity).
  This is the first repeating-row content and the one genuinely new sub-shape —
  settled on paper as a declaration, not new evaluator ops.
- **Tie-out (case 4):** `sum(rows) == published(ties_to_symbol)` holds by
  construction (same closed family, same horizon *H*); enforced by package
  validation, the `taxable-interest-composition.v1` slot-bijection analogue.
- **Divergence guard (case 4):** both stand on the *same pinned closure finding*
  (`runner.py:279`); a supersession/horizon advance re-blocks both on
  `SOURCE_SET_OPEN` (ADR-0017) — silent divergence is structurally excluded.

Owed to Track 2 as a named production condition (design, "Production
conditions"): tie-out validation. Recorded, never allowlisted — not a Rung-1
gap.

## D1-P3 — Part III contributed assertions — **settled at Rung 1**

Two boolean assertion fact types (+ one 7b country) on the ratified
`filing-status` pattern, contributed via ADR-0032 (`origin: assertion`).
`choose` evaluates only the taken branch (`evaluator.py:169`), so the yes-branch
demands the 7b country while the no-branch never references it (case 5); an
absent base answer or absent required country blocks incomplete (case-3 posture)
naming the fact. 7a **names** the FinCEN-114 obligation as disposition content;
the citizen never produces the filing (milestone non-goal, honored). Pattern-
following; one case per branch as chartered. Settled.

## Generalization (case 6, mandatory) — **holds**

The Schedule D stub instantiates `attachment.v1` with **zero Schedule-B-specific
schema surface**: threshold-as-parameter and Part-III-as-array mean the second
schedule changes *data* (a different requirement rule, a different family,
`assertion_parts: []`) and **no schema field**. The shape is an ontology, not
Schedule-B-shaped. Gate-6 minimum converged subset is met.

## Convergence

All three propositions settle at Rung 1; the mandatory cases (1, 3, 6) and the
supporting cases (2, 4, 5) resolve against committed contracts. Paper settles
the citizen shape — per the plan's stop rule, **stop at paper**. Three
production conditions (tie-out, disposition-wiring, generalization-guard
validation) are handed to milestone Tracks 1–2 for candidate ADR-0036; none is
an unresolved design question. No unresolved proposition; no authorized climb
consumed.
