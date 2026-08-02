# Presentation — Citation Walk Track 1 Review Gate Charter

Audience: Reviewer.

Status: **prepared.**

## Context Capsule

- **Source ref:** `track/presentation-citation-walk-track1` at
  `6ce90e75cc20eaaaf93a8166bb1c9fc5bb8a7528` (PR #77, CI `verify` green,
  mergeable, not yet merged).
- **Exact object:** the six files PR #77 adds —
  `tools/presentation_harness/examples/pages/citation-walk.v1.html`,
  `tools/presentation_harness/examples/manifests/citation-walk.v1.json`, and
  four fixture files under
  `tools/presentation_harness/examples/pages/citation-walk-fixtures/`
  (`baseline.v1.json`, `t1-inject-on-blocked-line.v1.json`,
  `t2-non-numeric-published-value.v1.json`,
  `t3-unknown-line-status.v1.json`). No other file changed.
- **Role:** one Reviewer, High tier / medium effort
  (`docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/presentation-citation-walk.md#Economical execution`).
- **Scope:** verify the renderer against every ADR-0046 requirement and
  foreclosure, including its three resolved rule-points (derived/diagnostic
  values are zero-authority; rejected values are blanket-redacted, never
  echoed; blocked-state salience is section-level). Independently reproduce
  the manifest's 23 criteria and the T1/T2/T3 fault-injection cases against
  the real renderer, not the Builder's claimed pass. Confirm the five
  `form-field.v3` disposition kinds
  (`published_value`/`computed_zero`/`closure_backed_zero`/`blocked`/`guard_inapplicable`)
  and the healthy-vs-blocked-input diagnostic pair are each covered by an
  executable case, not a doc claim.
- **Evidence-rung ceiling:** content/contract correctness against ADR-0046
  only. Credit the browser evaluation runner's own F1–F6 floor (isolation,
  injection integrity, cleanup, confinement, validation, redacted failures) —
  do not re-derive it. No redesign of the renderer, no new check family, no
  presentation-economy comparison, no re-review of the runner's own
  trustworthiness.
- **Stop conditions:** stop and route back to the foreman if a violation
  cannot be fixed without touching `form-field.v3` or
  `act-derived-publication.v1`; if closing a gap would need a new
  dependency, framework, or build step; if the review would need to
  reopen one of ADR-0046's three resolved rule-points; or if any check would
  need real workspace, credential, remote, or personal data.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`;
  `docs/adr/0046-presentation-surface-contract.md`; the milestone plan's
  `## Review gate` section, plus its Scope items 3 and 6, Verification, and
  Exit criteria
  (`docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/presentation-citation-walk.md`); the
  Track 1 charter
  (`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-25-presentation-citation-walk-track1.md`);
  and the PR #77 diff itself.

Before reviewing, echo the resolved source commit, object, scope, evidence
ceiling, and stop conditions. Treat the Builder's PR description as input, not
proof — independently rerun the manifest and reproduce each fault case.

## Required measurements

1. `node tools/presentation_harness/run.mjs --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json` exits `0`, independently rerun.
2. Each of the five `dispositions` kinds renders correctly and each blocked/degraded case shows the missing-fact/remedy text, not a value.
3. A derived/diagnostic value whose input is blocked does not render (zero-authority foreclosure).
4. No rejected or tampered value appears anywhere in visible text (T1–T3 fixtures).
5. A citation reused across two sites keeps distinct, non-colliding identity.
6. Blocked-state salience is section-level only — no page-level banner introduced.
7. No `innerHTML`, no new dependency, no framework, no build step.
8. `git diff --check main..HEAD` clean; CI `verify` green on the reviewed commit.

## Verdict

`READY` requires all eight measurements independently confirmed with no
ADR-0046 violation found. Otherwise return `NOT READY` with the smallest
exact residual, per the milestone's fixed one-review cap — a remaining
blocker routes back to the foreman rather than an automatic second review
cycle.
