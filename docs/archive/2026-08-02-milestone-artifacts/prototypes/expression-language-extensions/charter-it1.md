# Charter: Iteration 1 — Expression Language Extensions (Incumbent)

Date: 2026-07-13. Plan approved by owner (2026-07-13 directive).

- **Builder:** incumbent, High tier, owner-launched external context.
- **Working location:** `docs/archive/2026-08-02-milestone-artifacts/prototypes/expression-language-extensions/it1/`; foreman holds git custody.
- **Evidence:** Rung 2 — paper schema/canon diffs, expression traces against the committed evaluator, and throwaway probes in a scratch directory outside the repository. No repository modifications beyond the two outputs.
- **Questions:** ELX-P1 (declared optional defaults) and ELX-P2 (categorical comparison).

## Assignment

Design the two language extensions against the committed contracts at `HEAD`:

1. **ELX-P1.** A *declared* default mechanism for optional scalar inputs. Hard constraints: the default is versioned, declared content (schema/rule/parameter surface — not runner-resident policy, Article 11); an asserted input is never overwritten; when an input is asserted after a run, dependent derived findings displace and re-derive through the existing two edge kinds only (Article 7 — no third edge); pins must record whether a value came from the default or an assertion. Your design must explicitly defeat the three refuted workarounds from the conditional-selectors round 2R (multi-publisher staging, closure-aggregation misuse, evaluation-order tricks) by being none of them.
2. **ELX-P2.** Categorical comparison in guard expressions without decimal coercion: contract shape (new operation? typed compare via operation-semantics citizens? enum declaration on the input schema?), mismatch behavior as a contained explained failure, and migration for ADR-0024's interim numeric status codes.

Read: the topic `plan.md`, this charter, `docs/governance/`, ADRs 0002, 0004, 0006–0012, 0016, 0017, 0023, 0024, and committed `packages/derivation/` and `packages/kernel/` source and schemas. The conditional-selectors evidence (`docs/archive/2026-08-02-milestone-artifacts/prototypes/conditional-selectors/evaluation-analysis.md`, round-1R/2R reviews, `it2/design.md`) is *in scope* for the incumbent — you are designing to close its recorded gap.

## Required cases

The plan's five Gate 2 cases, each with two positive instances, two negatives, one lifecycle trace, and claim → contract change → evaluator/runner behavior → derived finding and pin map. Case 2's initial-run-then-assertion displacement trace is mandatory and must name every pin and edge.

## Outputs

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/expression-language-extensions/it1/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/expression-language-extensions/examination-it1.md` (≤120 lines) stating ELX-P1 and ELX-P2 separately as settled-at-static-level or unresolved, citing every case.

Before writing, echo scope, paper boundary, and stop conditions. Report unresolved authority questions explicitly.

## Stop conditions

Stop at the two static files. No evaluator/runner/schema edits, no git write commands. If the design requires a contract change you cannot represent as a versioned schema/canon diff on paper, stop and report rather than improvising.
