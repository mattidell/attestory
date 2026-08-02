# Presentation — Citation Walk Track 1 Repair Recheck Charter

Audience: Reviewer.

Status: **prepared.**

## Context Capsule

- **Source ref:** `track/presentation-citation-walk-track1` at
  `8109048c8da31435463ec7528e44f1398634eb0e` (PR #77, same branch/PR as
  Track 1 — the repair is an intermediate commit, not a new unit).
- **Exact object:** the repair diff on top of the reviewed Track 1 commit
  `6ce90e75cc20eaaaf93a8166bb1c9fc5bb8a7528` — limited to
  `tools/presentation_harness/examples/pages/citation-walk.v1.html`,
  `tools/presentation_harness/examples/pages/citation-walk-fixtures/`, and
  `tools/presentation_harness/examples/manifests/citation-walk.v1.json`. No
  other file changed by the repair.
- **Role:** one Reviewer, High tier / medium effort (same lineage as the
  original Track 1 review gate), per
  `docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/presentation-citation-walk.md#Economical execution`.
- **Scope:** a **focused recheck**, not a repeat of the full eight-measurement
  sweep. Confirm exactly:
  1. **F1 closed** — every numeric disposition render
     (`published_value`/`computed_zero`/`closure_backed_zero`) carries a
     citation bound to `field.citation`, including both previously-uncited
     zero lines; missing `field.citation` fails loud rather than rendering
     uncited.
  2. **F2 closed** — diagnostic eligibility requires the resolved value to be
     an actual finite number, not merely a numeric-kind disposition; the new
     `diag-t2-invalid-input` fixture case is suppressed correctly.
  3. **No regression** in the invariants the repair directly touches:
     citation identity-under-reuse, keyboard tab order
     (`citation-keyboard-focus-reachable`), and no new `innerHTML` or
     dependency.
  4. Measurements 2–8 from the original review record remain true (spot-check
     against the current diff; do not re-derive them from scratch).
- **Evidence-rung ceiling:** same as the original review gate — content/
  contract correctness against ADR-0046 only; credit the browser evaluation
  runner's own F1–F6 floor; no redesign, no new check family, no re-review of
  runner trustworthiness, no reopening of ADR-0046's three resolved
  rule-points.
- **Stop conditions:** stop and route back to the foreman if a residual
  survives this recheck (per the milestone's fixed cap, a survivor goes to
  the owner for disposition, not a further repair cycle); if closing a gap
  would require touching `form-field.v3` or `act-derived-publication.v1`; or
  if any check would need real workspace, credential, remote, or personal
  data.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`;
  the repair charter
  (`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-26-presentation-citation-walk-track1-repair.md`);
  the original review record in full
  (`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-26-presentation-citation-walk-track1-review.md`);
  `docs/adr/0046-presentation-surface-contract.md`; the repair commit diff
  itself (`git show 8109048`).

Before reviewing, echo the resolved source commit, object, F1/F2 scope, and
stop conditions. Treat the repair commit message as input, not proof —
independently rerun the manifest.

## Required measurements

1. `node tools/presentation_harness/run.mjs --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json` exits `0`, independently rerun; confirm the count is 26/26 (23 original + `line-2a-field-citation`, `line-3a-field-citation`, `t2-diagnostic-suppressed-on-invalid-input`).
2. F1: both zero-kind lines (`computed_zero`, `closure_backed_zero`) render a
   citation bound to `field.citation` in the actual DOM output, not only in
   the manifest criterion.
3. F2: the invalid-numeric-input diagnostic case is suppressed; a
   valid-numeric-input diagnostic case (already covered) still renders.
4. Citation identity-under-reuse and keyboard tab order are unchanged from
   the original review's confirmed state.
5. `git diff --check` clean; CI `verify` green on the repair commit.

## Verdict

`READY` requires all measurements confirmed with F1 and F2 closed and no new
ADR-0046 violation introduced. Otherwise return `NOT READY` with the smallest
exact residual — per the milestone's fixed cap, route the residual to the
owner for disposition rather than a further repair cycle.
