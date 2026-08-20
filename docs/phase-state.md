<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Grammar Census",
  "topic": "grammar-census",
  "active_plan": "docs/phases/grammar-census/milestones/engine-language-map.md",
  "milestone_state": "track-0",
  "status": "Grammar Census opened 2026-08-19 as an owner-selected, independent milestone — not a continuation of Claim Boundary Exploration. Purpose: produce a reconciled, plain-language census of the declarative language the engine actually has (layers, constructs, sources of authority, runtime interpreters, actual committed use, and where schema/runtime/content/observed behavior agree or diverge). Documentation-and-evidence only; no grammar change, ADR, or standards claim. Plan owner-approved 2026-08-19 and repaired before dispatch. Track 0 (term boundary and bounded corpus) is chartered and in flight. The phase stays open after this milestone closes.",
  "current_role": "Track 0 Builder — term boundary and bounded corpus",
  "current_prompt": "docs/reviews/2026-08-19-grammar-census-track-0-boundary-corpus-builder-charter.md"
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
- **Opening milestone:** Engine Language Map — **TRACK 0 IN FLIGHT
  2026-08-19.** Plan approved by the owner and repaired before dispatch.
- **Track 0 — chartered.** Term boundary and bounded corpus. Charter:
  `docs/reviews/2026-08-19-grammar-census-track-0-boundary-corpus-builder-charter.md`.
  Sole deliverable:
  `docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md`.
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
