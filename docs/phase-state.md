<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Grammar Census",
  "topic": "grammar-census",
  "active_plan": "docs/phases/grammar-census/milestones/engine-language-map.md",
  "milestone_state": "track-1",
  "status": "Grammar Census opened 2026-08-19 as an owner-selected, independent milestone — not a continuation of Claim Boundary Exploration. Purpose: produce a reconciled, plain-language census of the declarative language the engine actually has (layers, constructs, sources of authority, runtime interpreters, actual committed use, and where schema/runtime/content/observed behavior agree or diverge). Documentation-and-evidence only; no grammar change, ADR, or standards claim. Plan owner-approved 2026-08-19 and repaired before dispatch. Track 0 is complete and accepted at 4f66bc83 after five verified repair rounds; its bounded corpus is binding on Track 1. Tracks 1a, 1b, and 1c are chartered and running in parallel under the plan's Parallel Work Manifest, isolated from one another's drafts until all three commit. The phase stays open after this milestone closes.",
  "current_role": "Track 1a/1b/1c Builder — three independent parallel readings",
  "current_prompt": "docs/reviews/2026-08-20-grammar-census-track-1-parallel-readings-charter.md"
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
- **Opening milestone:** Engine Language Map — **TRACK 1 IN FLIGHT
  2026-08-20.** Plan approved by the owner and repaired before dispatch.
- **Track 0 — COMPLETE, accepted at `4f66bc83`.** Term boundary and bounded
  corpus. Charter (with five repair rounds appended):
  `docs/reviews/2026-08-19-grammar-census-track-0-boundary-corpus-builder-charter.md`.
  Deliverable:
  `docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md`.
  Supporting review record:
  `docs/reviews/2026-08-19-grammar-census-track-0-boundary-map-external-critique.md`.
  Its boundary map and bounded corpus are **binding on Tracks 1a-1c**.
- **Tracks 1a, 1b, 1c — chartered, running in parallel.** Charter:
  `docs/reviews/2026-08-20-grammar-census-track-1-parallel-readings-charter.md`.
  Deliverables, one per stream, non-overlapping:
  `track-1a-declared-constructs.md`, `track-1b-implemented-constructs.md`,
  `track-1c-observed-usage.md`, all under
  `docs/phases/grammar-census/inquiries/`. The three streams are isolated
  from one another's drafts until the third commits; the Foreman does not
  relay one stream's findings to another during Track 1.
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
