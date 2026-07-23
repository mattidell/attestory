# Milestone: Foreman Context Loading

Status: **planning draft — owner-directed 2026-07-23.** This is an
interstitial process-maintenance milestone. It does not replace the selected
Live-Run Trust-Domain Definition topic or authorize its first charter.

## Objective

Make a resumed foreman's initial context both smaller and more reliable. A
deterministic, provenance-bearing context capsule will route the foreman from
one resolved Git revision to the current seat, active plan, hard stops, and
the exact documents that become load-bearing for a proposed action. The capsule
is navigation, never a new source of authority.

## Current state

The authoritative process is distributed across `AGENTS.md`, the planning
protocol, role seed, phase state, handoff, active milestone plan, prototype
seat, prototype plan, ADR index, governance, and retrospectives. This is
deliberately thorough, but a wholesale re-entry load repeats the same
dispatch/data-boundary/status constraints and consumes material context before
the foreman knows which source applies. `docs/foreman-handoff.md` also carries
historical detail that its own preamble says belongs in retrospectives, reviews,
and Git.

The owner selected Live-Run Trust-Domain Definition, but its first charter and
every dispatch remain unapproved. This milestone therefore improves the shared
foreman mechanism before any live-run prototype seat is consumed.

## Scope

1. Record a paper Gate-0/Gate-1/Gate-2 analysis for the process change and
   ratify a Tier 2 ADR if the owner-approved paper evidence suffices.
2. Add a standard-library-only `tools/foreman_context.py` renderer. It reads
   committed Markdown from one explicit Git ref, parses compact JSON front
   matter from the volatile re-entry documents, validates cross-document
   agreement, and emits deterministic JSON or compact Markdown.
3. Add the minimal structured front matter to phase state, foreman handoff,
   the active milestone plan, and its prototype seat record. Each field has a
   named owning document; the tool must expose every source path and blob id.
4. Replace repeated operational prose in the role seed, handoff, phase state,
   and active plan with pointers to the owning authority where that does not
   remove a reader-facing product statement or a required stop condition.
5. Amend the planning protocol so a validated capsule and action-specific
   deep reads satisfy initial re-entry routing, while full authority remains
   mandatory at the point an action relies on it. The five-retrospective rule
   becomes a new-milestone-planning read, not a routine execution-resume load.
6. Test normal, stale-ref, malformed-front-matter, and cross-document-conflict
   cases entirely with synthetic repository fixtures.

## Non-goals

- No change to governance v0.1, tax contracts, schemas, package resolution,
  data residency, credentials, Git transport, or live-run tooling.
- No generic summarizer, LLM-produced authority cache, binary compression, or
  lossy rewrite of canonical text.
- No claim that an advisory capsule overrides an accepted ADR, `AGENTS.md`,
  a milestone plan, or a required review.
- No live-run charter, builder/reviewer dispatch, or maturity-matrix change.
- No deletion of durable planning history; the handoff may be shortened only
  because its durable history remains reachable through its existing pointers.

## Decision and contract surface

This is a Tier 2 process contract: future foremen consume its routing protocol,
but it does not change product or governance meaning. The candidate ADR is
**ADR-0042 — Foreman Context Capsule and Progressive Disclosure**. Its paper
analysis must score the decision and show two normal re-entry cases, two
meaningful failures, a lifecycle, and a source-to-authority-to-consumer-to-
failure map. The expected eligibility result is a paper-sufficient Tier 2
decision; if the analysis finds a genuine unresolved rival design, stop and
open a separately owner-approved prototype topic rather than treating this plan
as standing prototype authority.

The ADR must preserve ADR-0039's advisory-routing posture and ADR-0034's
dispatch gate. It must make `AGENTS.md` and accepted ADR text controlling,
name the selected Git ref and source blobs, and require the renderer to fail
closed on malformed or contradictory volatile state.

## Fixtures and verification

Synthetic fixture repositories will cover:

- a coherent committed re-entry state that renders stable JSON and Markdown;
- a dirty working tree whose capsule still identifies the committed source ref
  and reports, rather than reads, worktree drift;
- a phase/plan/seat topic mismatch and malformed front matter, each rejected
  before a capsule is emitted; and
- an unavailable ref or missing source document, rejected with no fallback to
  a different revision.

Track verification includes focused unit tests for the renderer, full
`.venv/bin/python3 -m unittest`, `.venv/bin/python3 -m mypy`,
`.venv/bin/python3 tools/governance_lint.py`, and
`.venv/bin/python3 tools/envelope_scan.py --range main..HEAD`. Documentation
checks prove the capsule's deep-read map names the full ADR/process sources
that become controlling for dispatch, ADR drafting, a new milestone plan,
schema/fixture work, and merge/records work.

## Data safety

All fixture repositories and context records use synthetic topic names and
relative repository paths only. The renderer never reads a workspace, local
credential, remote configuration, personal output, or absolute local path.
It invokes Git only for the selected repository ref, relative tracked paths,
blob ids, branch name, and porcelain status.

## Exit criteria

1. ADR-0042 is accepted with its required plain-language analysis and the ADR
   index updated in the same ratification unit.
2. A foreman can render a compact capsule from an explicit ref, see its source
   blob identities and worktree reconciliation state, and navigate to the
   action-specific deep reads without treating the output as authority.
3. A contradictory, malformed, missing, or stale selected source is refused
   honestly; the tool never silently reads a different ref or working-tree
   content.
4. The active re-entry documents expose compact, validated metadata and no
   longer duplicate their shared hard stops as independent rules.
5. The handoff describes current state and pointers rather than a second
   historical archive, while durable historical references remain intact.
6. The planning protocol distinguishes initial routing, action-specific deep
   reads, and the full retrospective read required before planning a new
   milestone.
7. Full verification passes with synthetic-only committed data.

## Tracks

### Track 0 — Paper decision and ratification

**Goal:** turn the owner-approved context-loading direction into a ratified,
bounded Tier 2 process contract.

**Boundary:** no renderer, metadata, or protocol rewrite before the paper
analysis and ADR establish the advisory/fail-closed boundary.

**Inputs:** ADR-0005, ADR-0013, ADR-0034, ADR-0039, the re-entry documents,
and the five retrospectives already read for this planning step.

**Outputs:** paper analysis, ADR-0042, plain-language companion analysis, ADR
index row, and any narrowly necessary status note.

**Verification:** paper cases and source map are traceable; ADR links to its
analysis; index/status lint passes; governance lint passes.

**Migration risk:** process wording only. Existing canonical documents remain
authoritative until the ratification unit lands.

### Track 1 — Deterministic capsule and tests

**Goal:** render and validate the advisory context capsule against committed,
single-ref source material.

**Boundary:** no network, credential, workspace, live-run, schema, or generic
summarization capability.

**Inputs:** accepted ADR-0042 and explicitly owned JSON front-matter fields.

**Outputs:** renderer, synthetic tests, and focused documentation.

**Verification:** focused fixtures prove determinism, provenance, dirty-state
reporting, and all named refusal paths; full verification floor passes.

**Migration risk:** an older ref with no metadata is an honest refusal, not a
fallback. No existing artifact shape changes.

### Track 2 — Re-entry documents and completion records

**Goal:** install the metadata, remove redundant current-state prose, and
record the protocol's operational boundary.

**Boundary:** do not alter the live-run prototype's scope, dispatch authority,
or maturity claim.

**Inputs:** accepted ADR-0042 and Track 1's validated renderer.

**Outputs:** compact metadata in the four volatile sources, planning/role
updates, a shortened handoff, phase/roadmap pointers, and retrospective.

**Verification:** renderer succeeds against `HEAD`; deep-read map is reviewed
against the cited controlling texts; full verification floor passes.

**Migration risk:** documentation pointers may change, but the capsule rejects
inconsistent combinations rather than presenting stale state.
