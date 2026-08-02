# ADR 0038 — QDCG Worksheet and Declared Absence

- Status: **accepted** (owner ratification 2026-07-19, Tier 3)
- Tier: 3
- Date: 2026-07-19

## Context

Line 16 is currently a declared rule over ordinary tax brackets — correct
for a return with no qualified dividends, wrong the moment they publish.
This ADR makes line 16 honest for the qualified-dividends case: the
Qualified Dividends and Capital Gain Tax (QDCG) Worksheet as declared rule
content, with its two capital-gain inputs bound to contributed
declared-absence facts rather than assumed, and a contradiction check that
keeps a declared "no capital-gain distributions" answer honest against
facts on record.

Owner directions bound and are not relitigated: the worksheet is built
(block-on-3a retired by principle); declared zero is factual completeness
— zero is never assumed, only declared; a declaration contradicted by
facts on record is a hard error (the source-closure precedent extended to
this new declared-absence pattern).

Prototype evidence spans five documents across two owner-directed repair
cycles: `docs/archive/2026-08-02-milestone-artifacts/prototypes/qdcg-worksheet/` — Round 1 (incumbent it1, rival
it2, governance and adversary review, `round-1-triage.md`), Repair 1
(`repair1/design.md`, `examination-repair1.md`), Confirmation R1
(`reviews/confirmation-r1.md`, **not confirmed** — one decision-blocking
gap), Repair 2 (`repair2/design.md`, `examination-repair2.md`),
Confirmation R2 (`reviews/confirmation-r2.md`, **confirmed**). The full
disposition is `evaluation-analysis.md`.

Round 1 converged D2-P1 (declared-absence assertion pattern) and D2-P3
(bidirectional admission-locus contradiction interlock) but not D2-P2's
supersession/disposition posture; the owner authorized a bounded
repair/confirmation pass rather than a further rival round. Repair 1
settled the successor posture, the qualified-zero reduction, and the
honest present-`"yes"` disposition, but Confirmation R1 found the
qualified-positive/both-declarations-absent case could name only the
first missing declaration — the committed evaluator raised on the first
absent reference and the guard's `all([ref, ref])` short-circuited there.
The owner routed the underlying generic capability to a separate topic
rather than deferring or absorbing it into D2; that topic ratified as
**ADR-0037** (`conditional_dependency_set`), production-hardened through
its own independent review chain (Track 0a, PR #30). Repair 2 substituted
the ratified node for the plain guard; Confirmation R2 independently
re-verified every claim against committed HEAD source and found it
resolves the gap without disturbing anything Repair 1 settled.

## Decision

1. **Declared-absence facts.** Two taxpayer-assertion fact types on the
   existing ADR-0032/ADR-0036 pattern — categorical `{yes, no}` domain,
   never boolean, no default, presence-before-value: whether the taxpayer
   has capital-gain distributions to declare, and whether Schedule D is
   required. They are not unconditional `requires` on line 16; they are
   expression dependencies of the qualified-positive path only. A
   qualified-zero return never reads, names, or pins either declaration.

2. **Single successor, `conditional_dependency_set`-gated declaration
   walk.** One versioned `rule-artifact.v3` successor owns line 16
   (no dual producers, no `conflict_semantics` as a dynamic selector, no
   first-publisher policy claim). Its guard places a
   `conditional_dependency_set` node (condition: qualified dividends > 0;
   members: the two declaration refs) first and unconditionally, so the
   node's own false-condition contract — not incidental operand order —
   grounds the qualified-zero reduction to the unchanged ordinary-bracket
   result. When qualified dividends are positive, the node's
   accumulate-then-raise member evaluation produces one non-publication
   walk naming every currently-absent declaration — both, if both are
   absent; exactly one, if only one is — never fewer than the true absent
   set, never an implied zero. When both declarations are present, guard
   evaluation proceeds to an ordinary categorical read: both `"no"`
   publishes the worksheet result; either `"yes"` yields the committed
   `inapplicable`/`guard_inapplicable` disposition, structurally distinct
   from the absence path (no exception, no custom blocked code).

3. **Reduction and ladder.** Qualified dividends of zero reach the
   existing ordinary-bracket computation unchanged and read neither
   declaration — the reduction property, cited to
   `conditional_dependency_set`'s own contract. The worksheet's ladder
   (preferential-base binding, ordinary-portion subtraction, rate-slice
   comparison, final minimum) is expressed in the closed committed
   expression vocabulary (`choose`/`compare`/`subtract`/`max`/
   `bracket_fold`/`round`) over versioned parameter declarations — no new
   evaluator operation.

4. **Pins and currency.** Every evaluated declaration and the qualified-
   dividends condition enter the ordinary access log; a published
   worksheet result pins the condition and both active declarations
   through the existing derivation edges (ADR-0037 decision 3). A later
   supersession of either declaration displaces line 16 to non-current
   through the existing two-edge model; contribution resolving a blocked
   absence is observed by a new run, not a third edge kind.

5. **Bidirectional contradiction interlock.** A current
   capital-gain-distributions declaration of `"no"` and the
   `CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal (ADR-0035, a contributed
   1099-DIV box 2a) may never both be current. Enforcement is
   admission-locus, pre-mutation rejection — declaration-first,
   signal-first, and same-batch attempts all fail closed (ADR-0032
   terminal-batch semantics) — reusing the ADR-0035-style admission-check
   mechanism rather than a new admitted citizen unless implementation
   demonstrates one is necessary. The worksheet has no route to box 2a,
   its signal, or any recorded-non-composable content; the only path from
   a real capital-gain distribution to line 16 is this hard error.

## Production conditions (owed to milestone Track 3; never allowlisted)

1. Declared-absence fact-type citizens and their package admission;
   package validation must reject a non-`{yes, no}` domain.
2. The line-16 `rule-artifact.v3` successor rule; package pin moves the
   adopted line-16 producer from v1/v2 to this v3 successor (the
   `conditional_dependency_set` node is admissible only under
   `rule-artifact.v3` — confirmed by direct schema inspection in both
   Repair 2 and Confirmation R2).
3. QDCG ladder parameters and intermediate expressions; coordinator-
   from-facts goldens for: qualified-positive both present (`"no"`/`"no"`)
   publishing below the ordinary result; qualified-zero reduction;
   qualified-positive with both declarations absent (walk names both);
   qualified-positive with exactly one absent (walk names that one only);
   each present-`"yes"` outcome; declaration supersession displacing a
   published result.
4. The bidirectional admission-locus contradiction interlock, kill-tested
   in both temporal orders and the same-batch case.
5. The no-reach-around boundary demonstrated structurally: the worksheet's
   declared bindings do not and cannot include box 2a, its signal, or
   recorded-non-composable content.

## Consequences

- Line 16 is honest under qualified dividends: it never assumes a
  capital-gain declaration, never silently computes ordinary tax over an
  undeclared qualified-positive return, and cannot publish over a
  declaration/signal contradiction.
- The `conditional_dependency_set` substrate proves its second real
  consumer beyond its own production hardening — a generic rule-language
  capability, not a D2-specific mechanism, exactly as ADR-0037 intended.
- The bidirectional admission-locus contradiction pattern (declared "no"
  vs. a contributed contradicting signal, both temporal orders and
  same-batch) is now precedent for any future declared-absence fact meant
  to stay honest against later-contributed facts on record.

## Alternatives Considered

- **Dual line-16 producers with dynamic `conflict_semantics` selection
  (Round 1 it2 posture).** Rejected: the committed package contract
  selects one static producer; the runner has no guard-exclusivity
  validation. No ADR may claim this as HEAD behavior.
- **Universal, unconditional declaration demand (Round 1 it1 posture).**
  Rejected: conflicts with the owner-ratified factual-completeness
  boundary — a qualified-zero return must retain the ordinary result
  without unrelated capital-gain declarations.
- **A custom `DECLARATION_OUT_OF_SCOPE` blocked code for present-`"yes"`
  (Round 1 it1 claim).** Rejected as a claim about HEAD: the closed
  record/walk vocabularies have no such code. The committed
  `inapplicable`/`guard_inapplicable` disposition is honest and walkable;
  a dedicated code remains an optional, unauthorized future production
  condition, not adopted here.
- **A plain `all([ref, ref])` presence guard (Repair 1 posture).**
  Rejected after Confirmation R1: `ref` raises on the first absent
  symbol and `all`'s generator short-circuits, so the walk could never
  name more than one missing declaration — the exact defect
  `conditional_dependency_set` exists to fix.
- **A new `admission-constraint.v1` citizen for the contradiction
  interlock (Round 1 proposal).** Not adopted: the lighter existing
  ADR-0035-style admission-locus mechanism is preferred unless
  implementation demonstrates it insufficient.

## Links

- Prototype evidence: `docs/archive/2026-08-02-milestone-artifacts/prototypes/qdcg-worksheet/` (`plan.md`,
  `round-1-triage.md`, `repair1/`, `repair2/`, `examination-repair1.md`,
  `examination-repair2.md`, `reviews/`, `evaluation-analysis.md`)
- Builds on: ADR-0006/0024/0025 (expressions, conditionals), ADR-0010
  (currency), ADR-0012 (form-field atomicity), ADR-0014–0017 (identity,
  closure), ADR-0031/0032 (data boundary, contribution), ADR-0035
  (dividend composition, the `CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal
  this ADR's contradiction check consumes), ADR-0036 (the taxpayer-
  assertion declared-absence pattern this ADR instantiates a second time),
  **ADR-0037** (`conditional_dependency_set`, the substrate this ADR's
  missing-declaration walk depends on)
- Consumed by: milestone Track 3 (line-16 production implementation)
