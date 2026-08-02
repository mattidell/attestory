<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-covered-ltcg-8a",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md",
  "milestone_state": "track-2",
  "status": "**ENGINE BREADTH / COVERED LONG-TERM GAINS, SCHEDULE D LINE 8a — TRACK 2 CHARTERED.** ADR-0052, Track 1, and ADR-0053 are all on `main-engine` (the ratified line as of PR #145). Track 2 (Schedule D content, the `attachment-rule.v3` categorical requirement, the single-rule selected-preferential-base producer, line 7a/9/16 successors, package successor, and synthetic goldens) is chartered on `track/schedule-d-covered-ltcg-8a-track2`, High tier / high effort. NEXT ACTION: owner-launch the Track 2 Builder; on return, the foreman takes custody and charters an author-independent Track 2 review.",
  "current_role": "Builder (Track 2 — Schedule D content and line 7a/9/16 production path)",
  "current_prompt": "docs/reviews/charter-2026-08-02-schedule-d-covered-ltcg-8a-track2.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

The engine computes the bounded direct-reporting path for Form 1099-DIV box 2a
through Form 1040 line 7a, the bounded 2025 Schedule K-1 (Form 1065) box-5
taxable-interest path through line 2b and Schedule B Part I, and the bounded
2025 payer-reported current-inclusion market-discount class in Form 1099-INT
box 10 or Form 1099-OID box 5. The next breadth slice, Covered Long-Term
Gains through Schedule D line 8a, has its transaction identity and
completeness-boundary citizens on `main-engine` (Track 1) and a ratified
addendum (ADR-0053) closing two production gaps; Track 2 (Schedule D
content and downstream computation) is now chartered.

## Operational State: Engine Breadth

* **Active milestone:** Covered Long-Term Gains, Schedule D Line 8a — **Track 2 in flight.**
* **Product change (target):** covered, long-term, gain-only Form 1099-B
  transactions become a closed source family that reaches Schedule D line 8a,
  Part II line 15, Part III line 16, Form 1040 line 7a, and the correct
  QDCG-computed line-16 tax, with a real Schedule D attachment disposition,
  explanation walk, and presentation section.
* **Plan:** `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md`
  — merged on `main` in PR #136. Prototype plan:
  `docs/prototypes/schedule-d-covered-ltcg-8a/plan.md` — owner-approved,
  merged in the same PR.
* **Scope:** covered, long-term, gain-only, no-adjustment 1099-B transactions
  reported directly on Schedule D line 8a without Form 8949; short-term
  transactions, losses, carryovers, Form 8949, noncovered securities, digital
  assets, and other Schedule D sources remain outside it.
* **Accepted contract (ADR-0052, `main-engine`):**
  - independent, anchor-keyed transaction identity one level below the
    existing statement-identity pattern — implemented in Track 1;
  - a nine-part completeness boundary read directly (two closures plus
    seven categorical absence declarations), with box-2a required to be
    closed (not closed-empty) as an explicit adopted successor —
    implemented in Track 1;
  - Schedule D line 8a/13/15/16 as content on the existing attachment
    ontology (ADR-0036) — no new mechanism, not yet implemented (Track 2);
  - a shared `selected-preferential-base` symbol with an exact,
    independently confirmed per-producer pin contract, resolving the one
    recorded committee dissent (CA-04) — not yet implemented (Track 2).
* **Accepted addendum (ADR-0053):** a foreman-run paper spike (no
  committee, Gate-1 scores 4 and 5) discharging ADR-0052's two named
  production conditions:
  - CA-05: publish `attachment-rule.v3`, an additive successor adding a
    categorical `family_nonempty` requirement trigger alongside the
    existing threshold shape;
  - CA-06: no new producer-selection substrate is needed — model the
    selected preferential base as one rule citizen with an internal
    `choose` branch, the same pattern already accepted for line 7a and
    line 16, preserving the single-producer-per-symbol invariant.
* **Next:** owner-launch the Track 2 Builder against
  `docs/reviews/charter-2026-08-02-schedule-d-covered-ltcg-8a-track2.md`
  on branch `track/schedule-d-covered-ltcg-8a-track2`. On return, the
  foreman charters an author-independent Track 2 review.
* **Branch line:** ADR-0052, Track 1, ADR-0053, and the `main-engine`
  rename are all on `main-engine` (PRs #137, #141, #143, #145) — the
  ratified line going forward.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
