# Evaluation Analysis — Conditional Multi-Dependency Non-Publication

Date: 2026-07-18

The owner accepted the incumbent candidate for this analysis and ADR drafting.
The ADR remains proposed until a separate owner ratification.

## Evidence and convergence

The topic asks whether a declared condition can jointly require several factual
dependencies, name every absent member in one non-publication walk when active,
and leave those members undemanded and unpinned when inactive.

| Exhibit | Branch / commit | Evidence |
|---|---|---|
| Incumbent | proto/d2-qdcg-worksheet, 01104d8 | it1/design.md and examination-it1.md: evaluator-node shape on all six cases. |
| Clean-room rival | proto/d2-qdcg-worksheet, 15c01a6 | it2/design.md and examination-it2.md: top-level conditional-requires shape on the same cases. |
| Governance R1 | proto/d2-qdcg-worksheet, eff8c57 | Both shapes are schema-declared candidates; five IT1 findings are non-blocking precision items. |
| Adversary R1 | proto/d2-qdcg-worksheet, eff8c57 | IT2 permits a conditionally demanded member to escape pinning and supersession; IT1 survives all attacks. |
| Gate-5 triage | proto/d2-qdcg-worksheet, eff8c57 | IT2 rejected; IT1 is the converged candidate. |

No production code or schema is evidence. The production conditions below are
obligations, not claims about HEAD.

| Proposition | Outcome | Evidence |
|---|---|---|
| CMDN-P1 — active joint demand and all-missing walk | Settled at Rung 1 | IT1 cases 1–5; Governance measurements 1, 3, 5; Adversary attacks 1–4. |
| CMDN-P2 — declared semantics, not runner policy | Settled at Rung 1 | IT1 map and case 6; Governance measurements 1, 5, 6; Adversary attack 6. |
| CMDN-P3 — no inactive demand, normal pins/currency | Settled at Rung 1 | IT1 cases 1 and 5; Governance measurements 2 and 4; Adversary attack 5. |

The six cases and Gate-6 floor are met. Paper plus committed-code review
distinguished the alternatives, so the plan's Rung-2 escalation condition is
not met.

## Accepted candidate

The accepted candidate is the IT1 evaluator expression named
conditional_dependency_set:

1. It carries a declared condition expression and a non-empty ordered array of
   declared ref member expressions.
2. The evaluator reads the condition first. If false, the node succeeds
   without evaluating, naming, or pinning a member.
3. If true, it evaluates every member once and accumulates only
   dependency-absence results. Any absence returns the existing
   dependency-absent disposition with the complete ordered missing list.
4. If all members are present, the node succeeds. Condition and member access
   enter the ordinary access log, so a published finding pins every consumed
   input through existing derivation edges.
5. Supersession of an evaluated condition or member displaces a published
   result through existing edges. Contribution resolving an absence is observed
   by a fresh run, never a third currency edge.

The candidate is sharpened by review: it reuses the existing
dependency-absence category and missing-list surface, rather than inventing an
opaque exception or a tax-specific code path.

## Rejected rival

IT2's top-level conditional-requires gate is rejected. It can inspect a member
for admission while relying on a separate value reference to pin it. If that
value reference is omitted, the member controls eligibility without being
pinned, so its supersession leaves a stale result current. This is Adversary
R1's decision-blocking attack, not a wording defect.

## Precision and production obligations

Governance findings GR1-F1 through GR1-F5 carry forward: per-rule rather than
run-wide halt; an explicit inactive-to-active condition-pin lifecycle; a
positive no-reach-around argument; and accurate description of the existing
multi-entry missing-list surface.

Production adoption requires:

1. A new rule-artifact schema version admitting conditional_dependency_set,
   with a declared condition and non-empty ordered ref members only.
2. Evaluator accumulation of every active dependency absence, ordinary
   propagation of non-absence failures, and access-log coverage for every
   evaluated condition/member.
3. Record and NPE tests proving all and only missing members appear in the
   existing dependency-absence walk; add a schema surface only if implementation
   proves one necessary.
4. Coordinator-from-facts goldens for all six paper cases, including
   condition/member supersession.
5. Portability and mutation tests that reject unpinned active members and
   tax-specific missing-list paths.

## Outcome

Proposed ADR-0037 records the contract and its plain-language companion
explains the effect. Ratification, production work, and D2 adoption remain
separate.
