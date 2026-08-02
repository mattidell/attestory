# ADR 0030 — Branch and Merge Strategy

- Status: **retired** (ADR-0045, 2026-07-25) — history only, not authority. Previously: **accepted** (owner ratification 2026-07-15; Option B). Applies to the next phase; the Core Tax Conditions milestone merges once per this ADR's Transition clause.
- Tier: 2 (process)
- Date: 2026-07-15

> **Retired 2026-07-25 by [ADR-0045](0045-agent-instruction-consolidation.md).**
> Process is the owner's operational domain and is no longer recorded as ADRs.
> This record is retained permanently as history and rationale — cite it for
> *why* a practice exists, never as binding authority. Its still-operative
> content lives in `PROJECT_PLANNING.md`, "Branch, PR, and Merge Protocol".

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
- Evidence of the failure this addresses: `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-15-core-tax-conditions-premerge-review.md` (PMR-1–7).

## Amendment (2026-07-16, **accepted**) — Commit references, pull requests, and agent push

Status: **accepted** (owner ratification 2026-07-16, dual approval alongside
the First Real Return Slice milestone plan). Motivated by the owner's move
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
8. **A push is publication, regardless of current repo visibility.** The
   remote (`github.com/mattidell/attestory`) hosts a copy of the record on a
   third party; visibility is a mutable setting, so the privacy posture must
   not depend on it — anything ever pushed is treated as potentially
   world-readable (and, while public, may be cached or indexed even if later
   deleted). The synthetic-only fixture-safety suite is therefore a
   **pre-push gate**, not just a pre-commit courtesy, and the Real Return
   phase's D1 residency contract extends to the remote: live data is never in
   the repository *or* on any remote, and the D1 kill-test list must include
   the push surface. *Interim posture (owner decision, 2026-07-16): the repo
   was found public and is set **private**. This amendment is now ratified
   (2026-07-16); the remote stays private until the merge gates
   (merge-commit-only, `main` branch protection) are configured. Making it
   public again is a standalone owner decision.*

## Amendment (2026-07-19, **accepted**) — What actually gets a PR

Status: **accepted** (owner ratification 2026-07-19). Motivated by a
foreman error: mid-milestone, foreman-authored commits (a full D2 prototype
repair/confirmation arc and an ADR ratification) were pushed directly to
`main` instead of through a unit PR, on the mistaken belief — drawn from
`git log` showing single-parent commits reachable from `main` — that some
historical ADR ratifications had skipped PRs. They had not: every one went
through a PR (decision 2, item 5); the single-parent commits observed were
antecedent commits *inside* a merged branch, not evidence the branch skipped
review. This amendment makes explicit, with concrete examples, a practice
that decisions 2–4 already implied but never enumerated.

### D. Merge unit, restated with this milestone's actual units

The governing idea remains decision 4: **merge unit = review unit.** A PR is
cut when something is complete and independently reviewable; everything that
builds toward it rides as plain commits on the unit's branch and reaches
`main` only inside that PR.

9. **Units that have gotten a PR this milestone, and will continue to:**
   the milestone plan (approval + activation — PR #23); each prototype
   plan's approval (PR #24, #26, #28); each ratified ADR **together with
   its entire evidence chain** — charters, both sealed builder designs,
   governance/adversary reviews, evaluation-analysis, any repair and
   confirmation rounds — as one unit (PR #25 for ADR-0035, #27 for
   ADR-0036, and their ADR-0037/0038 equivalents); each development track
   (PR #31 Track 1, #32 Track 2); and, in the First Real Return Slice,
   records/attestation units (PR #20, #21).
10. **Units that stay a branch commit and ride inside the unit's PR, never
    landing on `main` alone:** every intermediate event inside a unit —
    charters cut, builder outputs landed under custody, individual
    governance/adversary/confirmation reviews, a foreman synthesis, a
    NOT-CONFIRMED round, a **proposed** (inert) ADR draft, and routine
    status flips. A proposed ADR is explicitly not its own PR — only
    ratification (the status flip to accepted, decision 2) closes the unit
    and triggers the merge.
11. **The one confirmed exception: `phase-state.md`/`foreman-handoff.md`
    pointer advances and other inconsequential phase-state edits do not
    need a PR.** Direct commits to `main` are fine here — requiring a PR for
    every re-entry-pointer bump is heavier than the discoverability problem
    decision 5 was solving for.
12. **Recommended narrowing (not yet adopted, owner-callable per topic):**
    the prototype-topic PR is currently the fattest unit — one PR can carry
    charter → both builder designs → reviews → repair/confirmation rounds
    → the ratified ADR. Where a topic runs a repair/confirmation cycle, a
    clean split that preserves merge-unit-equals-review-unit is to land the
    **round** (charters, builds, reviews, evaluation-analysis) as one PR
    when the round completes, then land **ratification** as a small second
    PR that only flips the ADR to accepted and advances phase state. What
    this amendment does **not** authorize is narrowing below reviewability:
    a PR of builder designs without their reviews, or a ratified ADR
    without its evidence chain, cannot be judged standalone — that
    property (a unit is self-contained evidence, not a fragment) is what
    makes owner-merge meaningful in the first place. Track PRs (#31, #32)
    are already at the correct grain and are not affected by this note.
13. **Known gap, not resolved by this amendment:** item 7 states `main`
    merges are owner-held, "enforced structurally by branch protection on
    `main` (require a PR; no direct pushes)." As of this amendment, that
    branch protection is **not configured** — direct pushes to `main`
    currently succeed, which is exactly how the triggering error was
    possible. Configuring it (or confirming it deliberately stays
    unconfigured) is a standalone owner action this amendment flags but
    does not itself resolve.
