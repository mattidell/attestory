# ADR 0005 — Consequential ADRs Require Prototype Evidence

- Status: **retired** (ADR-0045, 2026-07-25) — history only, not authority. Previously: accepted (ratified 2026-07-10)
- Tier: 3
- Date: 2026-07-10

> **Retired 2026-07-25 by [ADR-0045](0045-agent-instruction-consolidation.md).**
> Process is the owner's operational domain and is no longer recorded as ADRs.
> This record is retained permanently as history and rationale — cite it for
> *why* a practice exists, never as binding authority. Its still-operative
> content lives in `PROJECT_PLANNING.md`, "Prototype-Driven Decisions".

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
8. Prototype branches (`prototypes/<topic>/it<N>`) are maintained evidence exhibits — never merged, never deleted. Only documents merge to `main`. Every analysis conclusion cites a followable exhibit; a broken evidence chain sends the ADR back.

## Consequences

- Consequential ratification requests arrive with evidence attached; the owner's decision surface becomes auditing evidence quality rather than evaluating intentions.
- Decision latency for consequential contracts increases by design; the cost is paid in prototype iterations rather than in rework of ratified mistakes.
- The repository accumulates maintained prototype branches and `docs/prototypes/` document sets as a permanent evidence record.
- The process is itself under evaluation: the first run (Rule Language Design) treats the process as a retrospective subject, and this ADR may be amended by a superseding ADR as lessons accumulate.

## Amendment (2026-07-10) — Exhibit tags

Point 8's "never merged, never deleted" branch rule created standing branch sprawl (one permanent ref per iteration), against the owner's worktree/branch-hygiene posture. Amended mechanics, owner-directed: a prototype branch exists only while its iteration is active; on conclusion the foreman tags the tip as `exhibits/<topic>/it<N>` and deletes the branch ref. Evidence preservation is unchanged — commits are permanent and cited by tag; exhibit tags are never deleted or moved. The decision content (prototype code never merges; only documents merge; evidence chains cite exhibits) is unchanged.

## Erratum (2026-07-10)

Minutes after ratification, the branch namespace was corrected from `prototype/<topic>/it<N>` to `prototypes/<topic>/it<N>`: the ref `refs/heads/prototype` already exists (the project's original real-data prototype branch, which is never touched), and git cannot nest a namespace under an existing branch name. Editorial correction only; no decision content changed.

## Links

- Process definition: `PROJECT_PLANNING.md`, Prototype-Driven Decisions; operational rules in `AGENTS.md`, Decision Records
- Precipitating rejection: `docs/adr/0004-derivation-machinery-contracts.md`
- First application: `docs/phases/foundation/milestones/rule-language-design.md`
- Amended/extended by: `docs/adr/0013-prototype-economic-gates.md` (economic gates, the prototype plan, role capability budget, and foreman scope-and-economy stewardship)
