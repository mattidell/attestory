# ADR 0046 — Presentation Surface Contract

- Status: **accepted** (owner direction 2026-07-25)
- Tier: 3
- Date: 2026-07-25
- Plain-language analysis:
  [0046-presentation-surface-contract.md](analyses/0046-presentation-surface-contract.md)

## Context — the citation walk exists as evidence, not as a contract

The Presentation aspect is the matrix's named frontier: "the first aspect a
real user (the owner) now touches every run, across every domain the matrix
covers" (`docs/phases/real-return/maturity-matrix.md`, Frontier reading).
Today it sits at L3 with a standing shim — "form-field disposition content,
not a human surface" — because no milestone has yet built the actual rendered
page a filer reads.

The Presentation Exploratory Milestone (2026-07-24, no ADR, no matrix cell
raised by design — `docs/milestone-retrospectives/2026-07-24-presentation-exploratory-milestone.md`)
studied exactly this surface under a synthetic fixture: a read-only
line → subtotal → per-source disposition → citation pin → source fact walk.
Five two-builder/two-reviewer cycles, ten builder runs, and standardized
tamper/fault tests (T1 inject-on-blocked-line, T2 non-numeric published value,
T3 unknown line status) converged on an invariant set independently of any
up-front design brief — accreted from a criterion-generating loop (surface via
adversarial execution → specify in next brief → verify), documented in
`docs/prototypes/human-presentation-citation-walk/analysis/02-adr-convergence.md`.
That analysis names the requirements, the foreclosures each tamper case
proved necessary, and three rule-points it deliberately left open for a real
product decision.

This ADR ratifies that converged shape as the project's Presentation Surface
Contract and resolves the three open rule-points, so a later milestone can
build the real citation walk against actual derivation output without
re-deriving invariants a synthetic-fixture exercise already settled five times
over.

**Evidence basis.** This decision ratifies directly from the exploratory
milestone's existing five-cycle record — two rival builders converging on the
same invariants under independent adversarial review, with reference
implementations satisfying all accumulated criteria
(`docs/prototypes/human-presentation-citation-walk/reference/prototypes/cycle5-{a,b}`).
No new rival-prototype round precedes this ratification; the owner accepted
that evidence bar explicitly (2026-07-25). A later milestone's real-data
implementation tracks are the proving ground for correctness against real
inputs, not a repeat of this convergence exercise.

## Decision — the contract

Any human-facing rendering of a computed return (the citation walk and any
later presentation surface built on the same pattern) must satisfy:

### Requirements

1. **Zero-authority projection.** A single frozen source object is the sole
   numeric input; each citation site has exactly one render path. The surface
   adds no authority — it may render only what its source already published.
2. **Honest blocking.** A blocked line shows what fact is missing and the
   remedy, never a value. Absence-of-key, not `null`/`0`/a guarded default,
   signals "no value."
3. **Fail-loud.** Any guard failure produces a visible on-page signal.
   Console-only failure does not satisfy this requirement.
4. **Sub-section blast containment.** A broken part must not hide or
   invalidate correct siblings, and must not show a value whose evidence is
   itself broken.
5. **Structural citation identity under reuse.** A citation's identity is
   enforced structurally (freeze-prevention or signature-detection), not by
   convention or naming discipline alone.
6. **Accessibility baseline.** Contrast thresholds, ARIA landmarks, keyboard
   reachability, and `:focus-visible` are load-bearing requirements of the
   surface, not a later pass.

### Foreclosures

1. No fabricated value — nothing rendered without a source citation.
2. No value **derived** from invalid or blocked input reaching the DOM,
   including diagnostic or tie-out arithmetic. **Resolved rule-point:**
   derived/diagnostic values fall fully under zero-authority (Requirement 1).
   A derived value is a rendered claim like any other; if any input feeding it
   is invalid or blocked, the derived value must not render. This closes the
   side-channel the exploratory milestone's cycle 4 found around honest
   blocking — a diagnostic tie-out number is exactly as capable of
   misrepresenting a blocked return as a primary line would be.
3. No console-only failure signal.
4. No cross-line or cross-section blast from one broken part.
5. No `innerHTML` dynamic interpolation — construct nodes
   (`createElement`/`textContent`), never string-build markup.
6. No echo of a rejected value into visible error text. **Resolved
   rule-point:** the policy is blanket redaction, not a split policy by field
   sensitivity. Error text is itself a leak channel (cycles 3–4); a per-field
   sensitivity classification is an ongoing maintenance burden that fails
   silently the first time a field is misclassified, where blanket redaction
   fails safe by construction.

### Resolved rule-point — blocked-state salience

The visible blocked-state signal is **section-level**: inline, in place,
within the line's normal position in the walk. No page-level banner
enumerating blocked lines is required. This follows directly from Requirement
4 (sub-section blast containment) and keeps the walk's own
line → subtotal → citation structure as the single source of truth for where
a block lives, rather than introducing a second surface that must be kept
consistent with the inline signal.

## Consequences

- A later implementation milestone may build the real citation walk against
  actual derivation output by citing this contract directly, rather than
  re-running a discovery cycle already completed on the synthetic fixture.
- The contract binds any future human-facing presentation surface built on
  this pattern, not only the citation walk specifically.
- This ADR makes no maturity-matrix claim by itself. Raising the Presentation
  matrix cell requires a real-data implementation milestone that builds and
  verifies a surface against this contract — the matrix's L3 evidential
  standard (Ontology §8) applies to that later milestone, not to this
  decision.
- The companion process finding from the same exploratory milestone
  (execution-based, adversarially-driven agent review; per-agent browser
  isolation; standardized break-test sets) is a reusable practice, not a
  product contract, and is not ratified by this ADR. A later milestone may
  reuse it as demonstrated technique without a separate decision record.

### Alternatives considered

- **Defer ratification and re-run rival prototypes against real derivation
  output first.** Considered and declined by the owner (2026-07-25): the
  exploratory milestone's five-cycle, two-rival-builder record already
  demonstrates convergence under adversarial review; a repeat round would
  re-spend the same discovery cost the exploratory milestone was chartered to
  absorb cheaply, on a synthetic surface, precisely so a later real-data
  milestone would not have to.
- **Split redact/echo policy by field sensitivity.** Rejected: more
  informative error messages are not worth an ongoing sensitivity
  classification that fails open (an unmisclassified-as-safe field leaks) the
  first time it is wrong.
- **Exempt derived/diagnostic values from zero-authority.** Rejected:
  identified in cycle 4 as a side-channel that lets a blocked return still
  publish a computed-looking number through a "just a diagnostic" path.
- **Banner-level blocked-state salience.** Rejected for now: a second,
  page-level enumeration surface must be kept consistent with the inline
  section-level signal, and the contract's own blast-containment requirement
  already gives each block a well-defined home. Not foreclosed for a later
  ADR if a real filer-facing evaluation finds section-level signals
  insufficiently visible on a long return.

## Links and evidence limits

- Evidence: `docs/prototypes/human-presentation-citation-walk/analysis/` (all
  seven vectors), especially `01-feature-citation-walk.md` (heuristics with
  emergence cycle) and `02-adr-convergence.md` (this ADR's direct source).
- Reference implementations satisfying the accumulated criteria:
  `docs/prototypes/human-presentation-citation-walk/reference/prototypes/cycle5-{a,b}`.
- Retrospective: `docs/milestone-retrospectives/2026-07-24-presentation-exploratory-milestone.md`.
- This ADR does not itself instantiate a runner, schema, or fixture against
  real derivation output; it ratifies the contract those artifacts must
  satisfy. No payload-instantiation gate applies to this record.
