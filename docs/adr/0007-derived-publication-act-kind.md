# ADR 0007 — Derived-Publication Act Kind

- Status: proposed
- Tier: 2
- Date: 2026-07-10

## Context

Derived findings must enter the record through an act whose vocabulary preserves the determinism boundary — not `assertion`, which records human claims. Both prototype iterations independently kept derived publication distinct from assertion (`evaluation-analysis.md` C4), and the reserved T1 guardrail (charter Q9) held in both: this decision is vocabulary and record shape only.

## Decision

1. A new act kind, **`derived-publication-act`**, records each derived finding's entry into the record. It is never an `assertion`.
2. The act is **attributed to the adopting actor through the adopted instrument** (adoption pin), not to the evaluator (C4; `examination-it2.md` Q9).
3. The act **pins its full lineage with roles**: input findings, choice findings, parameter declarations, the firing rule, mappings/bridges, the adoption act, governance versions, and (optionally) engine identity. Pin roles are required — bare id bags are rejected (C3, both examinations Q8).
4. **Deterministic content-addressed ids**: act, finding, and record ids are hashes of canonical payloads; double-run and shuffled-order byte-equality is the verification contract (both examinations Q10).
5. **Reserved-entry guardrail**: this ADR does not resolve T1 derived-finding authority doctrine; the act shape must remain compatible with any future T1 resolution (round-0/1/2 governance check 6, pass in all rounds).

## Consequences

- The finding schema's `pins` shim (rejected pending derivation machinery) gains its intended consumer.
- Explanation surfaces can answer *why a dependency was consulted* from pin roles alone (`examination-it2.md` Q8).
- Ratification condition inherited from the analysis (§5.4): deterministic-id portability must be re-proven against a second implementation before production adoption.

## Links

- Evidence: `docs/prototypes/rule-language/evaluation-analysis.md` (C3, C4, §5)
- Companions: ADR-0006 (rule language), ADR-0008 (record placement)
