# Presentation — Citation Walk Track 1 Repair Charter (F1, F2)

Audience: Builder.

Status: **prepared — not an approved route.** This milestone's fixed cap is
one Track 1 build and one review gate; a remaining `NOT READY` residual
returns to the owner for disposition rather than an automatic second cycle.
This charter is therefore the foreman's *recommended* disposition, drafted so
the option is costed and ready. It becomes live only if the owner chooses
repair and then supplies the literal `I authorize dispatch`.

## Context Capsule

- **Source ref:** `track/presentation-citation-walk-track1` at
  `6ce90e75cc20eaaaf93a8166bb1c9fc5bb8a7528` (the reviewed Track 1 commit).
- **Exact object:** a repair on top of that commit, limited to
  `tools/presentation_harness/examples/pages/citation-walk.v1.html` and its
  fixtures/manifest under
  `tools/presentation_harness/examples/pages/citation-walk-fixtures/` and
  `tools/presentation_harness/examples/manifests/citation-walk.v1.json`. No
  other file.
- **Role:** one Repair Builder, Medium tier / medium effort.
- **Scope:** close exactly the two blocking findings from the review record
  at `docs/reviews/2026-07-26-presentation-citation-walk-track1-review.md`:

  1. **F1 — numeric zero lines render without a source citation.** The
     `computed_zero` and `closure_backed_zero` fixtures have a
     `field.citation` but an empty `citationSites` array; the renderer only
     calls `renderCitation` while iterating `citationSites`, so it never
     reads `field.citation` directly and the value reaches the DOM uncited.
     Bind a citation to every numeric field render, including both zero
     kinds, and add executable manifest coverage proving it.
  2. **F2 — diagnostic eligibility ignores an invalid numeric input.**
     `healthyDisposition()` (or equivalent) accepts a diagnostic input
     because its disposition is numeric, without checking that the resolved
     value is actually a finite number. Require a finite resolved numeric
     value for diagnostic eligibility, and add the invalid-input diagnostic
     case (paired with T2's non-numeric `published_value`) to the manifest.

- **Evidence-rung ceiling:** presentation-layer repair only. No schema
  change, no new dependency, no framework, no build step, no reopening of
  ADR-0046's resolved rule-points, no change beyond F1/F2 and their direct
  regressions.
- **Stop conditions:** stop and route back to the foreman if closing either
  finding seems to require touching `form-field.v3` or
  `act-derived-publication.v1`; if a new dependency or framework seems
  necessary; or if a fix would touch a passing measurement (2–8 in the
  review record) in a way that changes its outcome.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  the review record in full
  (`docs/reviews/2026-07-26-presentation-citation-walk-track1-review.md`);
  `docs/adr/0046-presentation-surface-contract.md`; the Track 1 charter
  (`docs/reviews/charter-2026-07-25-presentation-citation-walk-track1.md`);
  the current renderer and fixtures at the source ref above.

Before editing, echo the resolved source commit, object, F1/F2 scope, and
stop conditions. Reproduce both findings against the current renderer before
repairing.

## Verification before handoff

```text
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json
git diff --check
```

Exit `0` is required, including new criteria proving F1 and F2 are closed.
All previously passing measurements (2–8 in the review record) must remain
true — this is a repair, not a redesign.

## Handoff

On completion, route back to the same reviewer lineage for a focused
recheck limited to F1 and F2 plus directly touched invariants — not a
repeat of the full eight-measurement sweep, per the milestone's fixed cap.
