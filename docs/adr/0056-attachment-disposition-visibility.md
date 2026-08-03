# ADR 0056 — Attachment Disposition Visibility

- Status: **accepted** (owner ratification 2026-08-02, Tier 2; Decision 3
  amended before ratification per owner direction to make the renderer-owned
  declared-constants source and the closed known-code allowlist explicit)
- Tier: 2 — narrow, additive presentation-shape widening with future blast
  radius (every attachment-bearing schedule inherits the fix or the gap),
  not a product-thesis or rival-topology decision.
- Date: 2026-08-02

## Context

Track 3 of the Covered Long-Term Gains, Schedule D Line 8a milestone
(`ef921d4`) landed a charter-stop finding: `_resolve_attachment` in
`packages/derivation/presentation_projection.py` produces a visible model
entry only for the `published` (required-and-complete) attachment
disposition. For `inapplicable` (not-required) and `blocked`
(required-and-incomplete) it returns `None`, and
`build_presentation_model`'s own filtering (`if group is not None`) then
drops the attachment from `citationGroups` entirely. `citation-walk.v1.html`
(both the product page and the frozen presentation-harness copy) only ever
iterates `MODEL.citationGroups`, so a not-required or required-and-incomplete
attachment is rendered as if it did not exist — not a redacted placeholder,
not an error banner, no signal at all.

This is a pre-existing gap in ADR-0036's generalized attachment shape, not
introduced by Schedule D: `attachment-rule.v2` (Schedule B) has always used
the same `_resolve_attachment` function, but every committed Schedule B
golden happens to exercise only the `published` path, so the gap was never
surfaced until Schedule D's own Track 2/3 goldens exercised
`blocked`/`inapplicable` for the first time on this milestone. It violates
ADR-0046 Requirement 2 ("honest blocking... a blocked line shows what fact
is missing and the remedy, never a value") for the one citizen whose entire
purpose, per ADR-0036 Decision 1, is to "publish a walkable inapplicability
disposition... never silence." The gap is at its most consequential for
ADR-0055's `COMPLETENESS_VALUE_VIOLATION`: the derivation-record ledger
already carries the exact violated declaration and its value, and none of
it can currently reach the page.

Paper evidence:
`docs/archive/2026-08-02-schedule-d-covered-ltcg-evidence/prototypes/schedule-d-covered-ltcg-8a/attachment-disposition-visibility-paper-spike.md`
— a producer→authority→consumer→failure map, two positive instances (the
unaffected published-attachment baseline, for both Schedule D and Schedule
B), two negative instances (not-required renders nothing; required-and-
incomplete, including the ADR-0055 violation case, renders nothing), and an
evaluation of two candidate shapes. Per
`docs/archive/2026-08-02-schedule-d-covered-ltcg-evidence/reviews/charter-2026-08-02-attachment-disposition-visibility-decision.md`
(Gate 1 score 5, paper-spike-plus-ADR-draft rung, matching the ADR-0055
precedent on this same milestone — lower residual uncertainty than
ADR-0055 was, since the shape to mirror already exists and is proven in
production), this ADR is grounded in that paper spike alone.

## Decision

1. **A new top-level model key, disposition-tagged, parallel to
   `sections`.** `presentation-model.v1` (or its next additive successor)
   gains `attachments: [...]`, one entry per attachment citizen regardless
   of disposition: `{"id": <attachment id>, "title": <attachment title>,
   "resolved": {"disposition": "published" | "blocked" |
   "guard_inapplicable", "activeCodes": [...], "act": null}}` — the same
   field names `_resolve_field_row` already produces for a blocked/
   guard-inapplicable field, so the renderer reuses that shape rather than
   inventing a second one. `citationGroups` is unchanged in meaning and
   shape: it continues to hold *only* published attachments' itemization
   detail, exactly as today. A published attachment therefore appears in
   both `attachments` (status entry) and `citationGroups` (itemization
   detail); a blocked or not-required attachment appears only in
   `attachments`, since there is no itemization to show.

2. **`_resolve_attachment` produces a value for all three dispositions,
   not two.** The function's `inapplicable` and `blocked` branches, which
   today `return None`, instead return a status entry: `inapplicable`
   (not-required) produces `{"disposition": "guard_inapplicable",
   "activeCodes": [], "act": None}`; `blocked` (required-and-incomplete)
   produces `{"disposition": "blocked", "activeCodes": [row["code"]] if
   "code" in row else [], "act": None}`, reading the exact code the
   disposition ledger already carries (`DEPENDENCY_ABSENT`,
   `ITEMIZATION_TIE_OUT_VIOLATION`, or `COMPLETENESS_VALUE_VIOLATION`) —
   never a new lookup, the same field `_resolve_field_row` already reads
   for a blocked field. The `published` branch is unchanged; it continues
   to build the existing `{id, title, parts}` shape for `citationGroups`
   and additionally contributes a `{"disposition": "published", ...}`
   entry to the new `attachments` list.

3. **`citation-walk.v1.html` gains one new render function, adapted from
   `renderLine`'s blocked/`guard_inapplicable` branches, not a new
   mechanism.** Parallel to the existing `sections` and `citationGroups`
   loops: `for (const attachment of MODEL.attachments || [])`, each
   wrapped in the existing `renderSafely` blast-containment call (ADR-0046
   Requirement 4). `renderLine` itself is not reused unmodified — it reads
   `section.field.dispositions[instructionKey].explain`/`.codes`, and an
   attachment has no `field` object and no tax-content-declared
   `dispositions` vocabulary (confirmed: `attachment.schedule-d.v2.json`
   declares no per-state explain text or code allowlist anywhere in its
   shape). The new attachment-render function instead sources its
   `role="alert"` banner text, its `guard_inapplicable` "not required"
   text, and its known-code allowlist from **renderer-owned declared
   constants in `citation-walk.v1.html` itself** (and the frozen
   `tools/presentation_harness` copy) — not a new tax-content field, not a
   new schema property, not anything read from the derivation record beyond
   `resolved.activeCodes` and `resolved.disposition`. This mirrors
   `renderLine`'s existing discipline (declared text, never derived
   prose) while keeping the declaration site in the renderer, since the
   attachment ontology (ADR-0036) has no per-schedule blocked-text content
   surface and this ADR does not add one.

   The renderer-owned known-code allowlist is the complete, closed set of
   codes `attempt_attachment` can ever emit for a blocked attachment,
   enumerated here rather than left implicit: `DEPENDENCY_ABSENT` (a
   required answer, subtotal, itemization symbol, or threshold parameter
   is absent — `BLOCK_ABSENT` in `packages/derivation/evaluator.py`),
   `ITEMIZATION_TIE_OUT_VIOLATION` (ADR-0036 Decision 3's row-sum/line
   mismatch), and `COMPLETENESS_VALUE_VIOLATION` (ADR-0055 Decision 2's
   value-checked-answer mismatch). A `guard_inapplicable` (not-required)
   entry carries no code — `attempt_attachment`'s `inapplicable` branch
   fires on `guard_result: false` alone, never a code. The renderer must
   filter `resolved.activeCodes` through this exact three-code allowlist
   before display — the same discipline `renderLine` already applies
   against a field's declared `dispositions.blocked.codes`, adapted to a
   renderer-constant set here because the attachment ontology has no
   per-citizen declared allowlist to filter against instead. A ledger code
   outside this set is a rendering error (`SectionError`), never displayed
   verbatim and never silently dropped. No new DOM pattern, no new
   accessibility surface, no `innerHTML` interpolation — the identical
   `createElement`/`textContent` construction discipline ADR-0046
   Foreclosure 5 already requires, and the same `section-error` fallback
   on any thrown `SectionError`.

4. **`citationGroups` and every existing consumer/golden are unaffected by
   construction.** No existing entry's shape or meaning changes; nothing
   is removed or renamed. A renderer or test that has not yet adopted the
   new `attachments` key continues to render exactly what it renders
   today — the published case correctly, the blocked/not-required case
   invisibly, same as before this ADR. This is a strict addition, not a
   breaking change, satisfying Track 3's own regression obligation (no
   rejected-value or citation regression on the v1/v6/v8 goldens) by
   construction rather than by re-verification of unrelated goldens.

5. **Content-only instantiation; no new schema/evaluator/admission
   mechanism.** This ADR touches the internal `presentation-model.v1`
   shape (an implementation detail with its own strict validator, never a
   published citizen schema per `presentation_projection.py`'s own
   docstring), `_resolve_attachment`, and one HTML/JS file. It adds no new
   derivation-record code, no new evaluator operation, no new admission
   check. The `derivation-record.v4`/`npe-walk.v3` vocabulary ADR-0055
   already widened is sufficient; this ADR only completes the path from
   that ledger to the page.

## Production conditions (owed to the implementation unit; never allowlisted)

- The exact `attachments` entry shape and `_resolve_attachment` changes
  (Decisions 1–2), plus `validate_presentation_model`'s extension to
  validate the new key with the same rigor `sections` already receives
  (duplicate-id rejection, known-disposition enforcement, no
  unsafe-string leakage).
- The `citation-walk.v1.html` (and frozen `tools/presentation_harness`
  copy) rendering addition (Decision 3), with accessibility parity to the
  existing field-blocked rendering (contrast, ARIA roles, keyboard
  reachability, `:focus-visible`) — ADR-0046 Requirement 6 is not a later
  pass.
- The renderer-owned declared constants (Decision 3): blocked/
  `guard_inapplicable` explanation and remedy text for an attachment, and
  the closed three-code known allowlist (`DEPENDENCY_ABSENT`,
  `ITEMIZATION_TIE_OUT_VIOLATION`, `COMPLETENESS_VALUE_VIOLATION`) that
  `resolved.activeCodes` is filtered through before display. These live in
  `citation-walk.v1.html`/the frozen harness copy, never in
  `attachment.schedule-d.v2.json` or any other tax-content citizen. A
  ledger code outside the allowlist must raise `SectionError`, never
  render verbatim.
- Coordinator-from-facts presentation goldens proving: a not-required
  attachment now shows a visible "not required" signal; a required-and-
  incomplete attachment (both the `DEPENDENCY_ABSENT` and
  `COMPLETENESS_VALUE_VIOLATION` cases) now shows a visible blocked banner
  naming the exact code; the published case is unaffected in both
  `attachments` and `citationGroups`; every existing v1/v6/v8 harness
  manifest remains green unmodified.

## Consequences

- Every attachment-bearing schedule — Schedule B today, Schedule D now, any
  future schedule instantiating ADR-0036 — gets an honest, visible
  three-state disposition for free once it adopts the widened model,
  closing the ADR-0046 Requirement 2 gap this milestone surfaced.
- `citationGroups` and every existing consumer, golden, and harness
  manifest remain byte-for-byte unaffected; nothing already committed is
  at risk from this ADR.
- The pattern generalizes: a future presentation surface built on this
  model inherits a proven, disposition-tagged shape for any citizen kind
  that is not a simple scalar field (an attachment today; a future
  multi-state citizen kind would follow the same template).

## Alternatives Considered

- **Extend the existing `citationGroups` entry with a disposition field
  (Option A in the paper spike).** Rejected: changes the meaning of every
  existing entry (membership no longer implies "published"), forcing every
  read site — including ones this milestone never touched — to gain a
  branch it did not previously need. More disruptive to existing goldens
  than Option B for no compensating benefit.
- **Leave the gap unresolved, relying on the numeric lines' own correct
  redaction.** Rejected: no wrong number ever reaches the page, but the
  attachment citizen's entire purpose is to be the honest completeness
  account (ADR-0036 Decision 1); silently omitting it — worse than
  redacting it — defeats that purpose for every attachment-bearing
  schedule, present and future.
- **A page-level banner enumerating blocked/not-required attachments,
  separate from the per-line walk.** Not proposed: ADR-0046's own resolved
  rule-point already forecloses page-level banners for blocked-state
  salience in favor of section-level, in-place signals (the resolved
  rule-point in ADR-0046 itself); this ADR's `attachments` entries render
  in the walk's own attachment section, consistent with that precedent,
  not as a new banner surface.

## Links

- Paper spike: `docs/archive/2026-08-02-schedule-d-covered-ltcg-evidence/prototypes/schedule-d-covered-ltcg-8a/attachment-disposition-visibility-paper-spike.md`
- Charter: `docs/archive/2026-08-02-schedule-d-covered-ltcg-evidence/reviews/charter-2026-08-02-attachment-disposition-visibility-decision.md`
- Implementation charter: `docs/archive/2026-08-02-schedule-d-covered-ltcg-evidence/reviews/charter-2026-08-02-attachment-disposition-visibility-implementation.md`
- Builds on: ADR-0036 (attachment ontology, the three-state disposition this
  ADR makes fully visible), ADR-0046 (presentation surface contract,
  Requirement 2 honest blocking / Requirement 4 blast containment /
  Requirement 6 accessibility, all reused unchanged), ADR-0055 (the
  `COMPLETENESS_VALUE_VIOLATION` code this ADR's `blocked` rendering path
  makes visible for the first time)
- Consumed by: a subsequent implementation unit, once ratified — not this
  charter, which is paper-and-draft only
