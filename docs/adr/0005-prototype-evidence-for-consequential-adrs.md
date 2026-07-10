# ADR 0005 — Consequential ADRs Require Prototype Evidence

- Status: proposed (pending owner ratification)
- Tier: 3
- Date: 2026-07-10

## Context

ADR-0004 was rejected because it asked for ratification of a contract whose central design element — the rule-artifact language — was a placeholder. The failure was procedural, not personal: nothing in the planning protocol prevented a machinery plan from carrying its most consequential decision as a line-item, and nothing required evidence before ratification. The owner directed a process change: agents should be authorized and empowered to prototype *before* proposing consequential ADRs, and most such ADRs should be supported by a prototype evaluation analysis.

## Decision

The Prototype-Driven Decisions process defined in `PROJECT_PLANNING.md` governs consequential decisions:

1. Tier 3 ADRs, and contract-foundational Tier 2 ADRs, must cite a prototype evaluation analysis as evidence. An ADR whose central design element is a placeholder is not proposable. Exceptions must be argued in the ADR itself.
2. Agents are pre-authorized to prototype before proposing such ADRs; prototyping is the expected first move, not a request.
3. The process loop is: charter (with committee-reviewed fixture selection) → build → examine → committee review → disposition → iterate or conclude → evaluation analysis → ADR.
4. Reviews are measurements against pre-declared checks; impression-only reviews are invalid. The owner audits reviews by sampling.
5. Roles are separated: builder ≠ reviewers ≠ foreman; no one reviews artifacts produced under their own charter.
6. Evidence must include at least one rival design on the same fixtures before the committee may conclude, or an explicit argument why comparison was unnecessary.
7. Termination is disciplined: declared questions per iteration, stop-and-decide on no-new-questions, three-iteration default cap, owner kill at any disposition.
8. Prototype branches (`prototype/<topic>/it<N>`) are maintained evidence exhibits — never merged, never deleted. Only documents merge to `main`. Every analysis conclusion cites a followable exhibit; a broken evidence chain sends the ADR back.

## Consequences

- Consequential ratification requests arrive with evidence attached; the owner's decision surface becomes auditing evidence quality rather than evaluating intentions.
- Decision latency for consequential contracts increases by design; the cost is paid in prototype iterations rather than in rework of ratified mistakes.
- The repository accumulates maintained prototype branches and `docs/prototypes/` document sets as a permanent evidence record.
- The process is itself under evaluation: the first run (Rule Language Design) treats the process as a retrospective subject, and this ADR may be amended by a superseding ADR as lessons accumulate.

## Links

- Process definition: `PROJECT_PLANNING.md`, Prototype-Driven Decisions; operational rules in `AGENTS.md`, Decision Records
- Precipitating rejection: `docs/adr/0004-derivation-machinery-contracts.md`
- First application: `docs/phases/foundation/milestones/rule-language-design.md`
