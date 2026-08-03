# Attachment Disposition Visibility — Implementation Charter

Audience: Builder

Status: **chartered for owner launch**

## Context capsule

- **Source ref:** orient from `HEAD` on
  `milestone/schedule-d-covered-ltcg-8a-continuation`, which contains Track 3
  (`ef921d4`) and the ratified `docs/adr/0056-attachment-disposition-visibility.md`
  (accepted 2026-08-02, Tier 2, Decision 3 amended before ratification).
- **Role:** Builder, High capability. Production integration, not a
  prototype or paper unit — the design questions are settled by the
  ratified ADR and its paper spike
  (`docs/archive/2026-08-02-schedule-d-covered-ltcg-evidence/prototypes/schedule-d-covered-ltcg-8a/attachment-disposition-visibility-paper-spike.md`).
- **Scope and evidence-rung ceiling:** implement ADR-0056 Decisions 1-5
  through the internal `presentation-model.v1` shape, `_resolve_attachment`,
  `validate_presentation_model`, the renderer, and production-shaped
  synthetic coordinator/harness goldens. Ceiling is synthetic
  `live_coordinate_run` and `presentation_harness` integration; no real
  workspace or real viewing session.
- **Stop conditions:** stop if `citationGroups`' existing shape or meaning
  changes for any currently-published entry; if any existing v1/v6/v8
  presentation golden or harness manifest changes in a way not explained
  by the new `attachments` key's addition; if an accepted ADR (including
  ADR-0036, ADR-0046, ADR-0055) needs mutation; if the attachment's
  blocked/not-required explanation text or known-code allowlist ends up
  needing to live in tax content rather than the renderer (ADR-0056
  Decision 3 forecloses this — if paper turns out wrong once you inspect
  the actual attachment vocabulary, stop and report rather than add a new
  content field); or if a ledger code outside the closed three-code
  allowlist (`DEPENDENCY_ABSENT`, `ITEMIZATION_TIE_OUT_VIOLATION`,
  `COMPLETENESS_VALUE_VIOLATION`) is ever observed in a goldens run —
  that is a stop condition, not a case to silently handle.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/adr/0036-schedule-attachment-ontology.md`;
  `docs/adr/0046-presentation-surface-contract.md`;
  `docs/adr/0055-attachment-completeness-violation-semantics.md`;
  `docs/adr/0056-attachment-disposition-visibility.md` in full (Decisions
  1-5 as amended, Production Conditions); the paper spike named above;
  `packages/derivation/presentation_projection.py` in full, especially
  `_resolve_attachment`, `_resolve_field_row`, `build_presentation_model`,
  and `validate_presentation_model`; `packages/presentation/pages/citation-walk.v1.html`
  and its `tools/presentation_harness` frozen copy, especially `renderLine`'s
  `blocked`/`guard_inapplicable` branches (the pattern to adapt, not call
  directly — confirm this before writing code); `packages/derivation/runner.py`'s
  `attempt_attachment`, `_attachment_block`, and the `BLOCK_ABSENT` /
  `ITEMIZATION_TIE_OUT_VIOLATION` / `COMPLETENESS_VALUE_VIOLATION` constants
  (`packages/derivation/evaluator.py`, `packages/derivation/runner.py`);
  `tests/test_presentation_l2_integration.py`;
  `tools/generate_capital_gain_distributions_line7a_t3_presentation_goldens.py`
  and the Track 3 goldens generator for this milestone (nearest precedent);
  `tools/presentation_harness/examples/manifests/schedule-d-covered-ltcg-8a.v1.json`;
  `AGENTS.md#Schema Publication Protocol`, `AGENTS.md#Fixture Rules`, and
  `AGENTS.md#Data Safety Rules`.

Before editing, echo the resolved `HEAD`, scope, evidence ceiling, and
every stop condition.

## Goal

Make every attachment disposition — published, blocked, and not-required —
visible and honest on the presentation surface, closing the gap Track 3
flagged: a blocked or not-required Schedule D (or Schedule B) attachment
currently renders no signal at all.

## Deliverables (ADR-0056 Production Conditions)

1. **`attachments` model key and `_resolve_attachment` widening.** Add
   `attachments: [...]` to the internal presentation-model shape: one entry
   per attachment citizen regardless of disposition,
   `{"id", "title", "resolved": {"disposition", "activeCodes", "act": null}}`.
   `_resolve_attachment`'s `inapplicable` and `blocked` branches produce a
   value instead of `None`; the `published` branch is unchanged and
   additionally contributes an `attachments` entry alongside its existing
   `citationGroups` contribution. `citationGroups` remains byte-identical
   in shape and meaning.
2. **`validate_presentation_model` extension.** Validate the new
   `attachments` key with the same rigor `sections` already receives:
   duplicate-id rejection, known-disposition enforcement, no
   unsafe-string leakage.
3. **Renderer addition.** One new render function in
   `citation-walk.v1.html` (and the frozen `tools/presentation_harness`
   copy) adapted from `renderLine`'s blocked/`guard_inapplicable`
   branches — not calling `renderLine` directly, since attachments have no
   `field.dispositions`. Source explanation/remedy text and the closed
   three-code known allowlist from renderer-owned declared constants, per
   ADR-0056 Decision 3 as amended. Filter `resolved.activeCodes` through
   the allowlist before display; raise `SectionError` on an unrecognized
   code. Same `role="alert"` banner pattern, same `createElement`/
   `textContent` construction discipline, same `renderSafely` blast
   containment, same accessibility bar (contrast, ARIA roles, keyboard
   reachability, `:focus-visible`) as the existing field-blocked
   rendering.
4. **Coordinator-from-facts goldens.** Prove: a not-required attachment now
   shows a visible "not required" signal; a required-and-incomplete
   attachment shows a visible blocked banner naming the exact code, for
   both the `DEPENDENCY_ABSENT` case (missing declaration) and the
   `COMPLETENESS_VALUE_VIOLATION` case (violated declaration); the
   published case is unaffected in both `attachments` and `citationGroups`;
   every existing v1/v6/v8 harness manifest remains green unmodified.
5. **Browser-manifest regression.** Extend or add to the Schedule D
   presentation harness manifest to exercise the new blocked/not-required
   rendering in the real DOM, alongside the existing published-case
   coverage.

## Boundary

No real browser/workspace session, no edit to any accepted ADR or
published history, no new tax-content schema or field, no Track 4/closeout
work. Do not add attachment explanation text to
`attachment.schedule-d.v2.json` or any other content citizen — Decision 3
is explicit that this text and the code allowlist are renderer-owned.

## Verification before handoff

```text
python3 -m unittest tests.test_schedule_d_covered_ltcg_8a_t2_coordinator
python3 -m unittest tests.test_presentation_l2_integration
python3 -m unittest tests.test_presentation_live_session
python3 -m unittest tests.test_presentation_live_viewing_vehicle
python3 -m unittest tests.test_attachment_rule_v4_completeness_value
node --test tools/presentation_harness/tests/*.test.mjs
node tools/presentation_harness/run.mjs --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json
node tools/presentation_harness/run.mjs --manifest tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json
node tools/presentation_harness/run.mjs --manifest tools/presentation_harness/examples/manifests/schedule-d-covered-ltcg-8a.v1.json
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
git diff --check main..HEAD
```

Run the full local gate at most once if useful; CI is the gate of record.

## Handoff

Commit the complete working state as one atomic implementation commit.
Leave the tree clean and report the SHA, changed surfaces, focused results,
golden entrypoint evidence, manifest inspection, and any charter-stop
finding. Do not review your own work, begin closeout, or open a PR.
