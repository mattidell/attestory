# ADR 0030 — Branch and Merge Strategy

- Status: **accepted** (owner ratification 2026-07-15; Option B). Applies to the next phase; the Core Tax Conditions milestone merges once per this ADR's Transition clause.
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

## Amendment (2026-07-16, **proposed**) — Commit references, pull requests, and agent push

Status: proposed (awaiting owner ratification). Motivated by the owner's move
to GitHub pull requests with possibly batched merges (rebase-before-merge
rewrites pre-merge SHAs) and by the ~50 SHA references orphaned by the Core
Tax Conditions rebase (retrospective follow-up).

### A. Two-phase commit referencing

The unit's *name* is its identity; commits are its transient representation
until `main` freezes them.

1. **Before a unit reaches `main`, governance records cite the unit by name,
   never by SHA.** Durable names that predate the commits: the ADR number, the
   charter/review filename, the branch name, and the PR number. In-flight
   documents (charters, reviews, process logs, the handoff) write "R2 landed
   on `<branch>` (PR #N)", not "R2 landed (`<sha>`)".
2. **A SHA may be cited only once it is reachable from `main`** (which this
   ADR makes append-only in practice — those SHAs are durable). Post-merge
   records (roadmap status lines, retrospectives, ADR closing notes) backfill
   the unit's no-ff **merge-commit** SHA as the anchor for the whole unit.
3. **Annotated tags are reserved for landmarks** (ratified ADRs, milestone
   closes), applied on `main` post-merge. Not every track — tag sprawl is its
   own legibility cost.
4. Already-orphaned historical SHAs stay as history (per the retrospective);
   this rule prevents new ones.

### B. Pull-request integration

5. **Each merge unit gets a pull request**; the PR number joins the unit's
   durable name. The repository merge method is **merge commit only** —
   squash-merge and rebase-merge are disabled in repo settings, since either
   would silently destroy the no-ff topology decisions 2–4 depend on. As a
   hedge against platform dependency, the merge commit message retains the
   "Merge pull request #N" line so a bare clone resolves PR references.
6. **Unit branches are ephemeral and may be rebased freely before merge;
   `main` never is.** Batching *merges* is permitted; batching *reviews* is
   not — the review happens at PR-open cadence (merge unit = review unit is
   unchanged; only the merge may lag its review).

### C. Agent push and the publication boundary

7. **Agents may push unit branches and open PRs** — clerical, auditable,
   reversible acts. **Merging to `main` is owner-held**, enforced structurally
   by branch protection on `main` (require a PR; no direct pushes), so the
   premature-merge failure mode this ADR responds to becomes impossible rather
   than merely forbidden. Agents force-push only their own unit branch, and
   only before its review has begun.
8. **A push is publication.** The remote (`github.com/mattidell/attestory`)
   is public; anything pushed is world-readable and may be cached or indexed
   even if later deleted. The synthetic-only fixture-safety suite is therefore
   a **pre-push gate**, not just a pre-commit courtesy, and the Real Return
   phase's D1 residency contract extends to the remote: live data is never in
   the repository *or* on any remote, and the D1 kill-test list must include
   the push surface.
