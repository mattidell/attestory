# ADR 0042 — Foreman Context Capsule and Progressive Disclosure

- Status: **accepted** (owner ratification 2026-07-23)
- Tier: 2 (process)
- Date: 2026-07-23
- Plain-language analysis: [0042-foreman-context-capsule.md](analyses/0042-foreman-context-capsule.md)

## Context

Foreman re-entry currently begins by reading a wide, prose-heavy set of
canonical documents. The same state is repeated across phase state, handoff,
role seed, milestone plan, prototype plan, seat record, and process manuals:
dispatch approval, data-boundary stop conditions, active-topic status, and the
next step. The repetition makes the first read costly and creates a drift risk
despite ADR-0030's requirement that `main` honestly describe current state.

The alternative cannot be a maintained summary that becomes a second source of
truth, nor a generic/LLM summary whose omissions are untestable. ADR-0039
already establishes the acceptable pattern for reducing context cost: a compact
routing surface that is advisory, while accepted ADR text remains binding.

The owner approved a process-contract change after reviewing the paper evidence
in `docs/proposals/foreman-context-loading-paper-analysis.md`. Its Gate 1
scores (5/5/3) and positive/negative instances show a paper-sufficient Tier 2
decision. It does not alter governance, product behavior, data residency, or
the approval gate in ADR-0034.

## Decision

1. **A context capsule is an advisory routing artifact, never authority.** A
   standard-library renderer produces a compact record for a resumed foreman.
   It may state only structured facts owned by canonical documents and direct
   the foreman to deeper reads. If it conflicts with `AGENTS.md`, an accepted
   ADR, governance, a role seed, a milestone plan, or a charter, that source
   controls. A routing omission never exempts an applicable contract.

2. **Every capsule is bound to one explicit committed Git ref.** The renderer
   requires `--ref`; it resolves that ref to a commit and reads tracked blobs
   from that commit only. Its output includes the selected ref, commit id,
   source path/blob id pairs, and separately reported worktree reconciliation
   state. It never reads working-tree document content, silently falls back to
   another ref, follows a remote, or accesses a workspace, credential, or
   personal output.

3. **Volatile re-entry documents carry compact JSON front matter with named
   ownership.** Phase state owns the active phase/plan pointer; handoff owns
   current status and next permitted action; the active plan owns scope,
   non-goals, and action-specific deep-read routing; the prototype seat owns
   the assigned role, rung, and stop conditions. Shared topic identifiers are
   repeated only so the renderer can reject disagreement. The metadata is
   canonical document content, not a fifth maintained summary.

4. **The renderer fails closed before emitting a capsule.** An unresolvable
   ref, missing source, malformed metadata, unsupported metadata version, or
   disagreement among phase state, handoff, plan, and seat is a refusal that
   names the relative source paths. A dirty worktree is reported, not treated
   as an error or read as authority.

5. **Initial routing and action-specific reading are distinct.** A foreman
   first loads the capsule, the ADR index, its role core, and the active plan
   slice it needs to interpret the capsule. Before dispatch, ADR drafting,
   schema/fixture work, merge/records work, or another declared action, it
   reads the complete controlling sources named by the capsule's deep-read map.
   The capsule cannot authorize an action or replace citation verification.

6. **The five-retrospective rule stays at new-milestone planning.** Before
   planning a new milestone, the foreman reads up to the five most recent
   retrospective files, newest first, as the existing protocol requires. A
   routine foreman resume of an already-planned or executing milestone need not
   preload them wholesale; it loads them when it is planning a successor or a
   mapped action requires their evidence.

7. **The handoff is continuity, not a second archive.** It keeps the current
   state, next permitted action, and durable pointers. Historical narratives
   remain in retrospectives, reviews, phase records, and Git. Shortening the
   handoff under this rule does not delete or supersede that history.

## Consequences

- Foreman re-entry becomes proportional to the current action rather than the
  accumulated prose corpus, while each compact claim stays traceable to a
  selected source blob.
- A stale branch or contradictory re-entry record becomes visible before a
  foreman acts; the tool cannot manufacture a coherent story from mixed refs.
- Existing documents gain small machine-readable fields and validation tests.
  They remain readable Markdown and retain their authority order.
- The planning protocol must distinguish execution resume from new-milestone
  planning. The latter retains the full retrospective read and all other
  action-specific mandatory reads.
- The renderer adds a process-tool maintenance surface; any new metadata field
  or deep-read trigger needs an owning document and fixture coverage.

## Alternatives considered

- **Load every canonical document at every resume.** Rejected: safe but
  needlessly repeats status and history; it does not reliably expose ref drift.
- **Hand-maintained foreman summary.** Rejected: an independent prose summary
  becomes another stale state surface.
- **Lossy AI summary or binary compression.** Rejected: neither creates an
  inspectable, testable authority path; binary compression saves storage, not
  expanded model context.
- **Make the capsule normative.** Rejected: this would turn a routing error
  into a contract hole, the precise posture ADR-0039 rejected for the ADR
  index.

## Links

- Paper evidence: `docs/proposals/foreman-context-loading-paper-analysis.md`
- Milestone plan: `docs/phases/real-return/milestones/foreman-context-loading.md`
- Extends: ADR-0039 (advisory routing)
- Preserves: ADR-0005, ADR-0013, ADR-0030, ADR-0034
- Implementation: `tools/foreman_context.py` (Track 1)

## Amendment (2026-07-23, accepted) — Charter and clerk task capsules

The original decision optimized only the foreman’s repository re-entry. The
owner directed an extension before review: all operational dispatch roles need
their smallest safe context, while the Trusted Advisor remains deliberately out
of scope because its owner-launched strategic counsel is not an execution
dispatch.

8. **Builder and reviewer capsules live in their charter, not in the Python
   renderer.** Every newly prepared builder or review charter carries a compact
   `Context Capsule` section naming the source ref (and the resolved commit at
   dispatch), exact object/range, role, scope, evidence-rung ceiling where
   relevant, stop conditions, and the full documents to read before acting.
   The capsule is a routing section of the charter; the charter and cited
   authority remain controlling. The foreman prepares it before requesting the
   owner's dispatch approval, and the dispatch record captures the resolved
   commit so a self-referential charter need not predict its own final commit.

9. **Clerk work begins from a foreman-prepared Clerk Task Capsule.** It names
   the selected ref/commit, one mechanical task, allowed input paths, required
   output shape/paths, verification, and stop rule. A clerk must not infer the
   active dispatch from phase state or handoff narrative, choose among candidate
   charters, compose scope, or inspect a workspace. The task capsule is not a
   general renderer and does not authorize the clerk's dispatch; ADR-0034 still
   requires contemporaneous, explicit owner approval.

10. **Trusted Advisor remains unchanged.** Its owner-launched, question-led
    strategic read set is intentionally not routed through operational capsules
    in this decision. A future advisor optimization is a separate topic.

This amendment preserves decisions 1–7: the Python renderer remains foreman
only, advisory routing remains non-normative, and the five-retrospective read
still applies before a new milestone plan.
