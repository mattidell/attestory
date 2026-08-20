<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Grammar Census",
  "topic": "grammar-census",
  "active_plan": "docs/phases/grammar-census/milestones/engine-language-map.md",
  "milestone_state": "closed",
  "status": "Grammar Census opened 2026-08-19 as an owner-selected, independent milestone. Engine Language Map is CLOSED 2026-08-20, all eight exit criteria met (docs/phases/grammar-census/exit-criteria-assessment.md). Deliverable chain: Track 0 boundary/corpus (4f66bc83, five repair rounds); Tracks 1a/1b/1c declared/implemented/observed construct sets (983b6102/495adeac/bb5ea26b, 108/90/84 constructs, independence held); Track 2 reconciliation (f276cc5b, 166 constructs), representative traces (3dba1a80, 6 traces), tension catalog (5ba385c1, 9 entries); Track 3 plain-language map (4dbc23e3) and bounded comparison brief (3bd1c5bd, 7 census-pressured dimensions). Most consequential finding: Track 2's adversarial spot-check falsified the Foreman's own round-3 ruling reasoning on surface 5b-ii — ADR-0066 decision 2's admission-depth contract is not enforced as written — corrected on the record at docs/reviews/2026-08-20-grammar-census-foreman-correction-5b-ii-ruling-reasoning.md with no census label moved. Owner-facing final report: docs/phases/grammar-census/final-report.md. Retrospective: docs/milestone-retrospectives/2026-08-20-grammar-census-engine-language-map.md. No production code, schema, or ADR changed anywhere in this milestone. The Grammar Census phase remains open; the next milestone within it is unselected and owner-held. No PR opened or pushed — owner direction required before either.",
  "current_role": "none — milestone closed, awaiting owner selection of next Grammar Census milestone or other direction",
  "current_prompt": "docs/phases/grammar-census/final-report.md"
}
-->

# Phase State

This is the **single re-entry document** pointing to the current state of the
project **on this branch**. This branch (`milestone/grammar-census-engine-language-map`,
primary worktree `engine-worktree-2`) carries the Grammar Census phase only.
It was created from `origin/main` at `20cf03ab` and diverges deliberately from
the Claim Boundary Exploration phase-state content that lives on
`milestone/declaration-request-claim-boundary-inquiry` (primary worktree
`engine-worktree-1`). The two lines are independent and run concurrently;
neither is authoritative over the other until one merges to `origin/main` and
the other rebases.

Curated history and architectural decisions live in retrospectives and
`docs/adr/`; historical execution records live under `docs/archive/`.

## High Level Briefing

**Grammar Census was opened on 2026-08-19** by explicit owner selection,
independent of and concurrent with Claim Boundary Exploration. The engine's
declarative rule and semantics language accumulated incrementally as tax
milestones required new capability. Before extending it again or comparing it
with other systems, the project wants a trustworthy, reconciled account of
what language it actually has: its layers, its constructs, where each
construct's meaning is declared, validated, executed, and tested, which
constructs are actually used and how, and where schema, runtime, content, and
observed behavior agree or diverge.

This is an exploratory, documentation-and-evidence phase — not a grammar
redesign, implementation milestone, standards-conformance exercise, or ADR
request.

## Operational State

- **Phase:** Grammar Census — **ACTIVE 2026-08-19**.
- **Opening milestone:** Engine Language Map — **TRACK 3 IN FLIGHT
  2026-08-20.** Plan approved by the owner and repaired before dispatch.
- **Track 0 — COMPLETE, accepted at `4f66bc83`.** Term boundary and bounded
  corpus. Charter (with five repair rounds appended):
  `docs/reviews/2026-08-19-grammar-census-track-0-boundary-corpus-builder-charter.md`.
  Deliverable:
  `docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md`.
  Supporting review record:
  `docs/reviews/2026-08-19-grammar-census-track-0-boundary-map-external-critique.md`.
  Its boundary map and bounded corpus are **binding on Tracks 1a-1c**.
- **Tracks 1a, 1b, 1c — COMPLETE**, accepted at `983b6102` (declared, 108
  constructs), `495adeac` (implemented, 90), and `bb5ea26b` (observed, 84).
  Independence held: each stream saw sibling deliverables appear and none
  opened one. Every record carries `status: pending-reconciliation`.
  Charter:
  `docs/reviews/2026-08-20-grammar-census-track-1-parallel-readings-charter.md`.
  Deliverables, one per stream, non-overlapping:
  `track-1a-declared-constructs.md`, `track-1b-implemented-constructs.md`,
  `track-1c-observed-usage.md`, all under
  `docs/phases/grammar-census/inquiries/`. The three streams are isolated
  from one another's drafts until the third commits; the Foreman does not
  relay one stream's findings to another during Track 1. **Independence has
  now ended** — Track 2 reads all three.
- **Track 2 — COMPLETE.** All three plan-named deliverables exist.
  Reconciliation accepted at `f276cc5b`. Charter:
  `docs/reviews/2026-08-20-grammar-census-track-2-reconciliation-charter.md`.
  Deliverable: `docs/phases/grammar-census/inquiries/track-2-reconciliation.md`.
  It is the **only** track permitted to make declared-versus-implemented-
  versus-used set-difference claims, and it assigned every construct's final
  `status`: 166 constructs — 157 active, 7 unused, 1 legacy-only, 1
  apparently unreachable. Seven of eight spot-checked three-way agreements
  held; **S2 failed**, and that failure is the milestone's most consequential
  finding so far.
- **Foreman correction, filed 2026-08-20:**
  `docs/reviews/2026-08-20-grammar-census-foreman-correction-5b-ii-ruling-reasoning.md`.
  Track 2's S2 failure falsified the reasoning of the Foreman's own round-3
  ruling on surface 5b-ii. `_predicate_depth`
  (`package_validation.py:182-188`) recurses through `args` only, so
  admission scores depth 1 for an arbitrarily deep tree nesting through
  `left`/`right`/`value` and admits it; only the evaluator refuses it.
  ADR-0066 decision 2's "Resolver admission rejects predicate depth greater
  than six" is therefore **not enforced as written**. The 5b-ii `proper`
  label survives under the round-4 amended criterion — **no census label
  moved** — but the struck sentence, the Track 0 axes row, and Track 0
  representational gap 8 were corrected on the record. Recorded as a
  finding; **no production code changes in this milestone**.
- **Track 2b — COMPLETE.** A continuation unit inside Track 2, not a new
  track; it existed because the reconciliation charter covered only one of the
  plan's three Track 2 deliverables, a gap the Track 2 Builder flagged and
  recorded rather than resolving by expanding its own scope. Charter:
  `docs/reviews/2026-08-20-grammar-census-track-2b-traces-and-tensions-charter.md`.
  - `track-2-representative-traces.md`, accepted at `3dba1a80` — six traces
    chosen for semantic contrast, each tagged **Executed** or **Inferred**
    step by step, each closing with the nearby inferences its evidence does
    *not* support. Three end in something other than a published finding.
  - `track-2-tension-catalog.md`, accepted at `5ba385c1` — nine entries
    ranked by consequence and separated into contract-versus-enforcement
    tensions (the project believes something untrue about itself) and
    implementation-versus-implementation tensions (two code paths disagree).
    Eighteen candidates were considered and dropped, with reasons, per the
    plan's instruction not to pad the catalog.
- **Track 3 — chartered.** Plain-language engine language map and bounded
  external-comparison brief. Charter:
  `docs/reviews/2026-08-20-grammar-census-track-3-synthesis-and-comparison-charter.md`.
  Deliverables: `track-3-engine-language-map.md` and
  `track-3-comparison-brief.md` under
  `docs/phases/grammar-census/inquiries/`. **The exit-criteria assessment,
  the owner-facing final report, and the milestone retrospective are Foreman
  work and are explicitly withheld from Track 3** — the retrospective must
  assess the Foreman's own conduct, including a Foreman ruling this milestone
  falsified, and that is not a Builder's to grade. Track 3 selects nothing.
- **Milestone key:** `grammar-census`.
- **Active plan:**
  `docs/phases/grammar-census/milestones/engine-language-map.md`.
- **Phase overview:** `docs/phases/grammar-census/grammar-census-overview.md`.
- **Phase roadmap:** `docs/phases/grammar-census/grammar-census-roadmap.md`.
- **Decision posture:** documentation-only and non-authoritative. No ADR,
  governance revision, production UI, schema, rule-language, engine, or
  tax-content change belongs to this milestone.
- **Phase lifecycle:** the phase stays **open** after this milestone closes.
  The next milestone within it is unselected and owner-held.
- **PR posture:** do not open or push a PR until the owner explicitly directs
  it.

Dispatch authorization is ephemeral live-thread context and is never recorded
here (`AGENTS.md`, "Dispatch authorization").

## Opening milestone — Engine Language Map

See `docs/phases/grammar-census/milestones/engine-language-map.md` for the
full plan: term boundary, evidence layers, census unit, representative
traces, tension catalog, bounded external-comparison brief, tracks, and exit
criteria.
