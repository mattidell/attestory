<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-covered-ltcg-8a",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md",
  "milestone_state": "production-work-landed-track2-3-review-chartered",
  "status": "**ENGINE BREADTH / COVERED LONG-TERM GAINS, SCHEDULE D LINE 8a — ALL PRODUCTION WORK IN TRACKS 2/3 LANDED (`36c7e94..88cb5e1`).** Track 2, the ADR-0055 completeness value-check, Track 3 presentation, and the ADR-0056 attachment-visibility fix are all committed. Foreman-run focused suites, full local gates, governance lint, and envelope/whitespace scans are clean at every step; foreman spot-checked the ADR-0056 golden regenerations as additive-only. Tracks 2 and 3 have not yet had the milestone's own required author-independent review (owed per 'Production track gates'; only Track 1 has one on record) — a combined Track 2/3 review is chartered, doubling as a first Completion-gate pass over the full post-Track-1 range.",
  "current_role": "Track 2/3 Independent Reviewer (owner-launched)",
  "current_prompt": "docs/reviews/charter-2026-08-02-schedule-d-covered-ltcg-8a-track2-3-review.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Curated history and architectural decisions live in retrospectives
and `docs/adr/`; historical execution records live under `docs/archive/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

The engine computes the bounded direct-reporting path for Form 1099-DIV box 2a
through Form 1040 line 7a, the bounded 2025 Schedule K-1 (Form 1065) box-5
taxable-interest path through line 2b and Schedule B Part I, and the bounded
2025 payer-reported current-inclusion market-discount class in Form 1099-INT
box 10 or Form 1099-OID box 5. The selected next slice is covered,
long-term, gain-only Form 1099-B transactions reported directly on Schedule D
line 8a without Form 8949. Its accepted contract and source-layer citizens are
now present on the milestone branch; downstream Schedule D computation is not
yet claimed.

## Operational State: Engine Breadth

* **Active milestone:** Covered Long-Term Gains, Schedule D Line 8a —
  **all Track 2/3 production work landed; independent review chartered
  before closeout.**
* **Product change (target):** covered, long-term, gain-only Form 1099-B
  transactions become a closed source family that reaches Schedule D line 8a,
  Part II line 15, Part III line 16, Form 1040 line 7a, and the correct QDCG
  line-16 computation with an attachment disposition and explanation walk.
* **Plan:** `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md`
  — committed on the draft milestone branch.
* **Scope:** covered, long-term, gain-only, no-adjustment 2025 Form 1099-B
  transactions reported directly on Schedule D line 8a without Form 8949.
  Short-term transactions, losses, carryovers, Form 8949, noncovered
  securities, digital assets, and other Schedule D sources remain outside it.
* **Reconstruction source:** the complete discarded state is preserved at
  `snapshot/2026-08-02-schedule-d-covered-ltcg-pre-curation` (`4af36ca`).
  Its old PR, charter, and repair chronology is evidence, not current process.
* **Completed on this branch:** the bounded evidence archive and accepted
  ADR-0052/0053/0054 contract; Track 1's transaction identity, family, closure,
  and completeness-boundary citizens with focused tests (independently
  reviewed); Track 2's Schedule D content, selected-preferential-base, and
  line 7a/9/16 production route (`37b4426`); ADR-0055 (attachment
  completeness value-check) and its implementation (`8b26db4`); Track 3's
  presentation projection of Schedule D fields and the attachment through
  the citation walk (`ef921d4`); ADR-0056 (attachment disposition
  visibility) and its implementation (`88cb5e1`) — Tracks 2/3 not yet
  independently reviewed.
* **Next:** owner-launch the Track 2/3 Independent Reviewer from the
  current prompt. `READY` closes the last gap before the closeout stage
  (coverage frontier, roadmap, phase state, deferral ledger, retrospective,
  milestone PR); `NOT READY` returns findings to the foreman for a
  findings-only repair charter.
* **Branch line:** `milestone/schedule-d-covered-ltcg-8a-v2`, one draft-to-final
  milestone PR based on the current `main`.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
