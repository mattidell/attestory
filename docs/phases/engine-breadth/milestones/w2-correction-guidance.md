<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "w2-correction-guidance",
  "status": "Closed. The v6/v70 reader distinguishes saved corrections, calculation status and authorization, preserves recovery after unusable responses, and passes attached v70 closure questions through without inventing diagnoses.",
  "retrospective": "docs/milestone-retrospectives/2026-11-02-w2-correction-guidance.md",
  "scope": [
    "plain-language guidance when a W-2 correction cannot produce a usable result on the supported v6 and v70 entry profiles",
    "distinguish rejected input, a saved correction awaiting calculation, missing answers and authorization currentness using actual recorded outcomes",
    "preserve first-entry, correction history and successful calculation behavior"
  ],
  "non_goals": [
    "no new tax coverage, content package, schema or kernel change",
    "no general explanation framework or v70 usability scorecard",
    "no automatic assertion of missing facts or grant of authorization"
  ],
  "deep_reads": {
    "planning": ["docs/process/planning-and-development.md", "docs/phases/engine-breadth/milestones/w2-correction-guidance.md"],
    "implementation": ["docs/process/planning-and-development.md", "docs/phases/engine-breadth/milestones/w2-correction-guidance.md"],
    "review": ["docs/roles/qualitative-review.md", "docs/phases/engine-breadth/milestones/w2-correction-guidance.md"],
    "new_milestone": ["docs/milestone-retrospectives/2026-11-02-w2-correction-guidance.md", "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"]
  }
}
-->

# When a W-2 Correction Cannot Recalculate (2025)

Milestone key: w2-correction-guidance.
Branch: milestone/w2-correction-guidance-2025.
Base: merged PR #249, core v70. This milestone publishes no core package.

## Purpose and current state

A person correcting wages needs to distinguish whether the new amount was
saved, whether the selected figures calculated, and whether current
authorization is recorded. The bounded v6/v70 entry surface now reports these
as separate outcomes using the existing recorder, coordinator report, and
saved presentation. This is surface guidance, not new tax coverage.

The implementation and the repair for unusable successful responses are
complete within scope. Independent semantic review is complete. The milestone
is closed on its branch; curated-range confirmation and exact-candidate CI
remain publication gates. Support is bounded to v6/v70, not the newer core v71.

## Current contract

- The ActLog is authoritative for the saved W-2 amount. The existing saved
  report and presentation supply calculation disposition, line values, and
  authorization currentness. The entry page adds no second outcome record.
- A rejected value remains a pre-save validation error with its field-specific
  instruction. An accepted correction is shown as saved even if another line
  is blocked. Lines with `computed: false` and `value: null` display as
  unavailable, never as zero.
- A calculated figure remains calculated when authorization is absent; the
  page states currentness separately. A prior calculation shown after a
  post-save calculation failure is identified as prior, while the latest
  calculation and authorization are unknown.
- HTTP success does not establish a usable confirmed snapshot. The page
  parses and shape-checks bounded JSON before installing it, for both submit
  and state-read responses. Malformed or unusable responses preserve the last
  confirmed snapshot, show uncertainty, disable resubmission, and offer the
  existing state read. A usable read recovers the saved state without another
  POST.
- Recovery is a state read within the existing running session. It does not
  promise recovery after process restart, rerun calculation, or provide an
  automatic recalculation retry. General missing-answer copy remains the
  deliberate fallback when the saved outcome carries no safe question. In the
  v70 case where a blocked line reaches only one unconfirmed source family, the
  existing v69+ presentation includes that family's declared closure question
  verbatim, and the compiled v2 page displays it. This bounded pass-through
  does not mean every dependency block names its question or license diagnosis
  from an unattached mapping.
- The bounded default is the v2 surface successor; `legacy-v1` remains
  explicitly selectable and its published bytes are unchanged. No kernel,
  schema, core, tax-content, runner-attachment, or authorization workflow
  change is included.

## Review dispositions

- Unusable HTTP success previously erased recovery controls. The repaired
  page admits only parsed, usable snapshots on submission and recovery reads.
  Independent compiled-page tests confirmed recovery without duplicate saves.
- The no-question claim was too broad. Live v70 evidence and the compiled
  page show an existing closure question verbatim for a single unconfirmed
  family root. All current accounts now preserve that bounded capability and
  the general fallback for other cases.
- The duplicated W-2 missing/answered projection now uses one helper;
  normal and post-save-failure behavior remains unchanged.
- Final independent review found no material product-code defect. Its
  remaining documentation finding was the stale no-question claim in README,
  roadmap and coverage frontier; those accounts are corrected.
- The final local full suite had 4,121 passes, 11 skips and three browser
  failures. Each failed test passed independent focused reproduction. This
  does not establish their original cause or make that full run green.
  Exact-head CI must pass before merge; no test was removed or weakened.

## Deferred questions

- Identify an exact missing question only when the saved outcome supplies an
  authoritative connection; do not infer it from a derived symbol.
- Decide separately whether process-restart recovery or recalculation retry
  is needed and how it would be authorized.
- Consider broader internal-error guidance only from evidence, not as a
  refusal-code catalogue.

Retrospective: `docs/milestone-retrospectives/2026-11-02-w2-correction-guidance.md`.
