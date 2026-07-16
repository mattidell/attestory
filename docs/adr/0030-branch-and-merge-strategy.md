# ADR 0030 — Branch and Merge Strategy

- Status: **proposed** (owner directed Option B 2026-07-15; awaits explicit ratification)
- Tier: 2 (process)
- Date: 2026-07-15

## Context

Work was integrated at **milestone granularity**: an entire milestone (all Track-0 decisions + all development) lived on one branch and merged to `main` as a single no-ff commit (e.g. Core Tax Conditions, `2fbc3a7`, ~104 commits). That unit proved far too coarse:

- The merge was all-or-nothing and un-reviewed — a decision-blocking gap (ADR-0027 d9 exclusive projection) and a stubbed condition (Track 4 checksum) shipped invisibly inside one green branch.
- Rollback was coarse (revert the whole milestone or nothing).
- `main` said "completed milestones only," so in-flight work hid on a side branch — causing repeated discoverability failures (a clerk that couldn't see the active seat; foreman re-entry from `main` reading stale state).

The failure was not no-ff vs fast-forward (milestone merges already used no-ff). It was the **unit**. The fix: make the merge unit equal the review unit equal the governance unit the process already produces — the ADR for decisions, the track for development.

## Decision

1. **`main` is a continuous ratified record (Option B), not a completed-milestones-only line.** Ratified ADRs and reviewed development tracks merge to `main` as they land; `main` may carry in-flight milestone state. It is honest running state, not a shippable release line. This makes `main` track reality, so re-entry and clerk/foreman discoverability work from `main` again.

2. **Decision unit = the ADR.** Each decision topic gets its own short-lived branch (milestone-planning charters the questions/scope). Build/review/repeat under the existing prototype discipline; author the ADR; **no-ff merge to `main` on ratification**, bundling the topic's evidence (plan, charters, exhibits, reviews, evaluation-analysis) under one labeled merge.

3. **Development unit = the track.** Each implementation track gets its own branch and a **review gate**, then a **no-ff merge to `main`**. No monolithic milestone-development branch. A track that stubs or defers an owned condition fails *its* gate instead of surfacing post-merge.

4. **Merge unit = review unit; every merge is no-ff.** No unit reaches `main` without its review (ADR: committee + ratification; track: pre-merge review). No-ff preserves branch topology and gives each unit a labeled, revertable boundary.

5. **Re-entry pointer discipline (carried from the handoff).** Because `main` is now the running record, `phase-state.md`'s "Next" must be advanced with each merge; a unit is not done until the re-entry pointer reflects it.

## Consequences

- **Granular rollback:** revert a single ADR or track merge, not a milestone.
- **Continuous review:** state can't hide inside a large blob; the boundary that merges is the boundary that was reviewed.
- **Discoverability dissolves:** `main` reflects current progress, so the "main says complete / real work on a branch" trap does not recur.
- `main`'s history becomes a legible sequence of ratified decisions and reviewed tracks rather than occasional milestone blobs.
- Trade accepted: `main` is never a clean "completed-only" line; a reader treats it as a running ledger (the phase-state briefing remains the plain-language summary).

## Transition

Applies to the **next phase**. The current Core Tax Conditions milestone finishes remediation (R2→R5) on its existing (already-rebased) branch and merges **once** — no re-cutting of settled history. This ADR is itself a candidate first user of the per-decision-merge model.

## Alternatives Considered

- **Option A — `main` = completed milestones only** (per-unit merges land on a milestone integration branch that merges to `main` only at milestone completion). Rejected: keeps `main` releasable but preserves the discoverability trap (in-flight work invisible from `main`) that caused repeated failures this cycle.
- **Status quo — milestone as the merge unit.** Rejected: the coarse-unit failures above.

## Links

- Related process: ADR-0005, ADR-0013 (and its 2026-07-15 proposed amendment — foreman-authored fixes default to confirmation).
- Evidence of the failure this addresses: `docs/reviews/2026-07-15-core-tax-conditions-premerge-review.md` (PMR-1–7).
