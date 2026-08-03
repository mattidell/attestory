# Covered Long-Term Gains, Schedule D Line 8a — Track 3 Builder Charter

Audience: Builder

Status: **chartered for owner launch**

## Context Capsule

- **Source ref and resolved launch commit:** orient from `HEAD` on
  `milestone/schedule-d-covered-ltcg-8a-continuation`, which contains Track 2
  (`37b4426`) and the ADR-0055 completeness-value-check implementation
  (`8b26db4`). Both are foreman-verified clean (full local suite 850 passed,
  governance lint conformant, envelope/whitespace scans clean).
- **Role:** Builder, High capability. Presentation and integrated-regression
  integration, not a new contract or computation round — but attachment/
  itemization projection through the presentation surface is genuinely
  unattempted ground (see Stop conditions).
- **Scope and evidence-rung ceiling:** project the Schedule D line
  8a(d)/(e)/(h), line 13, line 15, line 16, line 7a, and line 9 fields, and
  the Schedule D attachment's own disposition/explanation walk, through the
  existing presentation model and citation-walk product page; add
  authoritative synthetic presentation goldens and browser-manifest
  regressions against the current core-calculations v12 / published-packages
  v7 chain; prove no rejected-value or citation regression on the existing
  v1/v6/v8 goldens. Synthetic coordinator and synthetic browser evidence are
  the ceiling — no real workspace or real viewing session.
- **Stop conditions:** stop and report, do not improvise, if: an accepted
  ADR (including ADR-0036, ADR-0046, ADR-0052/0053/0054/0055), published
  schema, historical content/package, or an existing golden unrelated to
  this slice would need mutation; if projecting the Schedule D attachment's
  itemization rows (line 8a's `collect_members` row set, the
  `ITEMIZATION_TIE_OUT_VIOLATION` invariant) or its three-state disposition
  cannot be expressed as an ordinary `form-field` `binds_symbol` projection
  and instead requires a new generic presentation capability or product
  contract — **no attachment or itemization citizen has ever been projected
  through the presentation surface before** (grep confirms zero
  `attachment`/`itemization`/`collect_members`/`row_set` references in
  `packages/derivation/presentation_projection.py` or ADR-0046); if the
  new `COMPLETENESS_VALUE_VIOLATION` walk cannot render through the
  existing non-publication-walk presentation path without a new rendering
  rule; or if line 7a/9/16's existing form-field citizens do not bind
  unchanged to the new Track-2/ADR-0055 producers (confirm the symbol
  identity is unchanged before assuming so).
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md`
  (Contracts, Fixtures item 10, Verification, Track 3 section);
  `docs/adr/0036-schedule-attachment-ontology.md`;
  `docs/adr/0046-presentation-surface-contract.md`;
  `docs/adr/0052`, `0053`, `0054`, `0055` in full;
  `packages/derivation/presentation_projection.py`;
  `packages/derivation/live.py`;
  `packages/presentation/pages/citation-walk.v1.html`;
  `tools/presentation_harness/examples/pages/citation-walk.v1.html`;
  `tools/generate_presentation_l2_golden.py`;
  `tools/generate_capital_gain_distributions_line7a_t3_presentation_goldens.py`
  (nearest precedent — the nearest prior Track-3 unit on this same phase);
  `tools/presentation_harness/examples/manifests/capital-gain-distributions-line7a.v1.json`
  and `citation-walk-production-shaped.v1.json`;
  `packages/schemas/tax/form-field.v3.schema.json`;
  `packages/content/tax/2025/form1040.line-7a.form-field.json`,
  `form1040.line-9.form-field.json`, `form1040.line-16.form-field.json`
  (confirm whether these bind unchanged or need successor versions);
  `packages/content/tax/2025/attachment.schedule-d.v2.json`;
  `tests/test_presentation_l2_integration.py`;
  `tests/test_presentation_live_session.py`;
  `tests/test_presentation_live_viewing_vehicle.py`;
  `tests/test_schedule_d_covered_ltcg_8a_t2_coordinator.py`;
  `AGENTS.md#Fixture Rules`; and `AGENTS.md#Data Safety Rules`.

Before editing, echo the resolved `HEAD`, scope, evidence ceiling,
zero-attachment-precedent risk, immutable-history constraint, and every
stop condition.

## Goal

Make the covered-LTCG Schedule D result and its attachment honestly
viewable through the existing product page and presentation model, with no
rejected-value leakage and no regression to any prior slice's presentation
goldens.

## Deliverables

1. **Field citizens.** Confirm or version form-field citizens binding to
   the Schedule D line 8a(d)/(e)/(h), line 13, line 15, and line 16
   symbols, and confirm the existing line 7a/9/16 field citizens bind
   unchanged to the Track-2/ADR-0055 producers (no edit if unchanged; a new
   version only if the bound symbol identity actually changed).
2. **Attachment projection.** Project the Schedule D attachment's
   `not-required`/`required-and-complete`/`required-and-incomplete`
   disposition, including the new `COMPLETENESS_VALUE_VIOLATION` walk
   entries, honestly through the presentation surface — reusing the
   existing non-publication-walk rendering path if it fits; escalating per
   Stop conditions if it does not.
3. **Authoritative synthetic presentation goldens.** A deterministic,
   production-shaped act log adopting the current v12/v7 chain through
   `live_coordinate_run`, covering at minimum: eligible published Schedule
   D (line 8a/13/15/16, line 7a, line 9); the attachment
   `required-and-incomplete` case from a violated boundary declaration
   (the ADR-0055 N1 case); the missing-declaration case (N2); box-2a
   present alongside an eligible transaction (no double count); and the
   not-required case (eligible family closed-empty). Commit new
   slice-specific goldens; do not rewrite the established v1/v6/v8
   goldens.
4. **Browser-manifest regression.** New `presentation_harness` manifest
   case(s) for this slice, run against the product and frozen harness
   pages, with existing baseline manifests remaining unchanged and green.
5. **Regression proof.** Re-run the existing presentation/live-session/
   viewing-vehicle/coordinator focused modules and confirm no rejected
   value, citation, or accessibility regression.

## Boundary

No real browser/workspace session, real data, tax computation redesign,
Track 4/closeout records, or reopening any accepted ADR. Do not copy
line7a-Track-3 code verbatim; adapt the pattern to Schedule D's actual
shape, especially wherever attachment/itemization projection diverges from
a flat scalar field.

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
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
git diff --check main..HEAD
```

Run the full local gate at most once if useful; CI is the gate of record.

## Handoff

Commit the complete working state as one atomic Track-3 implementation
commit. Leave the tree clean and report the SHA, changed surfaces, focused
results, golden entrypoint evidence, manifest inspection, and any
charter-stop finding — especially whether the attachment/itemization
projection required new generic capability. Do not review your own work,
begin the closeout stage, or open a PR.
