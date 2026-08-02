<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-covered-ltcg-8a",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md",
  "milestone_state": "track-1",
  "status": "**ENGINE BREADTH / COVERED LONG-TERM GAINS, SCHEDULE D LINE 8a — TRACK 1 MERGED. ADR-0053 PROPOSED, AWAITING OWNER RATIFICATION.** Track 1 merged in PR #141; ADR-0052's transaction identity and completeness-boundary citizens are on `main`. Before Track 2, a foreman-run paper spike discharged ADR-0052's two named production conditions (CA-05: categorical attachment-requirement schema successor; CA-06: no new producer-selection substrate needed, one rule with an internal `choose` branch suffices) as proposed ADR-0053. NEXT ACTION: owner reviews and ratifies ADR-0053 (or directs a different resolution); the foreman then charters Track 2 against both settled contracts.",
  "current_role": "Foreman (ADR-0053 proposed; owner ratification decision pending)",
  "current_prompt": "docs/adr/0053-covered-ltcg-schedule-d-attachment-and-producer-substrate.md"
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
completeness-boundary citizens on `main` (Track 1); a small addendum
(ADR-0053) closing two named production gaps awaits ratification before
Schedule D content and downstream computation (Track 2) can be chartered.

## Operational State: Engine Breadth

* **Active milestone:** Covered Long-Term Gains, Schedule D Line 8a — **Track 1 merged; ADR-0053 awaiting ratification.**
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
* **Accepted contract (ADR-0052, `main`):**
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
* **Proposed addendum (ADR-0053, not yet ratified):** a foreman-run paper
  spike (no committee, Gate-1 scores 4 and 5) discharging ADR-0052's two
  named production conditions:
  - CA-05: publish `attachment-rule.v3`, an additive successor adding a
    categorical `family_nonempty` requirement trigger alongside the
    existing threshold shape;
  - CA-06: no new producer-selection substrate is needed — model the
    selected preferential base as one rule citizen with an internal
    `choose` branch, the same pattern already accepted for line 7a and
    line 16, preserving the single-producer-per-symbol invariant.
* **Next:** owner reviews and ratifies
  `docs/adr/0053-covered-ltcg-schedule-d-attachment-and-producer-substrate.md`
  (merge is the ratification record) or directs a different resolution.
  Only then does the foreman charter production Track 2 (Schedule D
  content and the line 7a/9/16 production path) against both settled
  contracts.
* **Branch line:** ADR-0052 and Track 1 are on `main` (PRs #137, #141).
  ADR-0053's paper spike and proposed text are on
  `decisions/schedule-d-covered-ltcg-8a-ca05-ca06`, cut from `main`.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
