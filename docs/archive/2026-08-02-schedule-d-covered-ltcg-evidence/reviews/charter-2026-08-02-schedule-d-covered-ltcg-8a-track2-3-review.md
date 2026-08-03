# Covered Long-Term Gains, Schedule D Line 8a — Track 2/3 Independent Review Charter

Audience: Reviewer.

Status: **chartered for owner launch.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `milestone/schedule-d-covered-ltcg-8a-continuation` at `88cb5e1bfb188cf3cea1b426a907a6146cf66709`.
- **Exact object or commit range:** `36c7e94..88cb5e1` — the full sequence
  since Track 1's accepted state: Track 2 (`37b4426`), the ADR-0055
  attachment completeness-violation paper spike/draft (`49ca48e`) and its
  implementation (`8b26db4`), Track 3 (`ef921d4`), and the ADR-0056
  attachment disposition-visibility paper spike/draft (`97953e3`) and its
  implementation (`88cb5e1`). Track 1 (`dbc1c62` and its own review) is
  accepted history and out of scope here except as a base comparison.
- **Role:** one author-independent Reviewer, High tier / high effort. Do
  not consult the Builder's threads, the foreman's verification notes in
  this session, or any self-assessment in the commit messages — verify
  every claim against committed source directly.
- **Scope and evidence-rung ceiling:** measure Track 2's Schedule D content
  and production route, ADR-0055 and ADR-0056's implementations against
  their ratified ADR text, and Track 3's presentation projection — this is
  the milestone's own Production track gate for Tracks 2 and 3 (owed,
  never taken independently until now) and doubles as the Completion gate's
  first pass against this range. No presentation/browser real session, no
  repair design, no new charter.
- **Stop conditions:** stop and report if the exact range or branch tip
  differs from above; if any accepted ADR (0036, 0046, 0050, 0052, 0053,
  0054, 0055, 0056), published schema, historical content/package, or
  Track-1 citizen changed; if a review finding would require interpreting
  governance text; if a real value, identity, document, disposition,
  reason, workspace location, or generated private artifact is
  encountered; or if a failure cannot be attributed to this range without
  a base comparison against `dbc1c62`.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`;
  `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md`
  (Contracts, Fixtures, Verification, Tracks, Review gates, Exit criteria);
  `docs/adr/0036`, `0046`, `0050`, `0052`, `0053`, `0054`, `0055`, `0056`
  in full; every charter in the range
  (`charter-2026-08-02-schedule-d-covered-ltcg-8a-track2.md`,
  `charter-2026-08-02-schedule-d-attachment-completeness-decision.md`,
  `charter-2026-08-02-attachment-completeness-violation-implementation.md`,
  `charter-2026-08-02-schedule-d-covered-ltcg-8a-track3.md`,
  `charter-2026-08-02-attachment-disposition-visibility-decision.md`,
  `charter-2026-08-02-attachment-disposition-visibility-implementation.md`);
  every file in the exact commit range; `packages/derivation/runner.py`,
  `presentation_projection.py`, `package_validation.py`, `marshal.py`,
  `live.py`, `records.py`, `explanation.py`; `AGENTS.md#Schema Publication
  Protocol`, `AGENTS.md#Fixture Rules`, and `AGENTS.md#Data Safety Rules`.

Before reviewing, echo the resolved branch tip, exact range, review
ceiling, independence constraint, and every stop condition.

## Required measurements

1. **Exact object and boundary.** Enumerate the full `36c7e94..88cb5e1`
   range and map every changed file to one of: Track 2, the ADR-0055
   decision unit, the ADR-0055 implementation, Track 3, the ADR-0056
   decision unit, the ADR-0056 implementation. Confirm no file outside
   those six units' own charters was touched, and no accepted ADR,
   published schema/content/package, or Track-1 citizen changed.
2. **Track 2 — Schedule D content and production route.** Verify the
   twin scalar companions (ADR-0054), `attachment-rule.v3` (ADR-0053
   Decision 1), Schedule D line 8a/13/15/16 content, the single-rule
   `selected-preferential-base` citizen with its exact ADR-0052 Decision 4
   pin table per branch (confirm the direct-producer branch does not
   acquire a spurious proceeds-family pin — the exact fidelity concern the
   builder flagged mid-charter), and the line 7a/9/16 successors. Confirm
   package v11/v6 preserve v10/v5 resolution and reject mixed-current,
   raw-reach-around, duplicate-producer, and stale-authority graphs.
3. **ADR-0055 — completeness value-check.** Verify `attachment-rule.v4`'s
   `check: "value"`/`equals` shape matches ADR-0055 Decision 1 exactly;
   verify `attempt_attachment`'s value-check branch reads only the
   already-fetched presence finding (no new lookup), checks presence
   independently of value first, and names every missing and every
   violated answer in one walk (Decision 3). Confirm `COMPLETENESS_VALUE_VIOLATION`
   is distinct from `DEPENDENCY_ABSENT` in the record/walk vocabulary and
   that `attachment.schedule-d.v2` is the only content adopting `v4` —
   `v1`/`v2`/`v3` and `attachment.schedule-d` v1 remain immutable.
   Independently reproduce the N1 (violated-declaration convergence), N2
   (absent-declaration, unaffected), and T0→T2 lifecycle goldens.
4. **Track 3 — presentation projection.** Verify the new Schedule D field
   citizens bind to the correct symbols; verify line 7a/9/16's existing
   field citizens were confirmed unchanged rather than assumed so (check
   the actual bound symbol identity); verify the `ATTACHMENT_SCHEMAS`
   widening to admit `attachment-rule.v4` is the only projector code
   change and that `_resolve_attachment`'s itemization-reading logic is
   genuinely unchanged across v2/v3/v4. Confirm core-calculations v13/
   published-packages v8 preserve v12 and earlier. Reproduce the 5 new
   `live_coordinate_run` goldens and the new harness manifest
   (`schedule-d-covered-ltcg-8a.v1.json`) independently.
5. **ADR-0056 — attachment disposition visibility.** Verify the new
   `attachments` presentation-model key matches ADR-0056 Decisions 1-2
   exactly (disposition-tagged, `{id, title, resolved}`, mirroring
   `_resolve_field_row`'s shape); verify `citationGroups` is genuinely
   byte-unchanged in shape and meaning by diffing every regenerated golden
   in the range and confirming each diff is *only* the new `attachments`
   key addition (spot-check at least three across different milestones:
   Schedule D, capital-gain-distributions-line7a, k1-interest-breadth, or
   market-discount-interest). Verify the renderer addition does not call
   `renderLine` directly on an attachment (confirm `field.dispositions`
   is genuinely absent from the attachment shape, so this was a real
   constraint, not a false claim), and that the blocked/not-required
   explanation text and the closed three-code allowlist
   (`DEPENDENCY_ABSENT`, `ITEMIZATION_TIE_OUT_VIOLATION`,
   `COMPLETENESS_VALUE_VIOLATION`) live only in
   `citation-walk.v1.html`/the frozen harness copy — never in
   `attachment.schedule-d.v2.json` or any other tax-content citizen, per
   ADR-0056 Decision 3 as amended. Independently inject a fourth,
   out-of-allowlist code into a blocked attachment's `activeCodes` and
   confirm the renderer raises `SectionError` rather than displaying it.
6. **Accessibility and blast containment.** Exercise the new attachment
   render path for contrast, ARIA roles (`role="alert"`), keyboard
   reachability, and `:focus-visible`, matching the existing field-blocked
   rendering. Confirm `renderSafely` blast containment: a malformed
   attachment entry blocks only its own attachment section, not sibling
   numeric lines or unrelated attachments.
7. **Regression proof.** Confirm every pre-existing presentation golden
   and harness manifest (`citation-walk.v1.json` 26/26,
   `citation-walk-production-shaped.v1.json` 19/19, and the
   capital-gain-distributions/k1-interest-breadth/market-discount
   manifests) remains fully green, unmodified in meaning. Re-run the full
   focused module set named in each of the six charters' Verification
   sections and confirm identical pass counts to what each builder
   reported.
8. **Data safety and immutable history.** Verify no real value, identity,
   document, disposition, reason, workspace location, or generated
   private artifact appears anywhere in the range. Run the required
   envelope scan and `git diff --check` over the full range independently.

## Verification

Run once, independently:

```text
python3 -m unittest tests.test_schedule_d_covered_ltcg_8a_t1_citizens
python3 -m unittest tests.test_schedule_d_covered_ltcg_8a_t2_coordinator
python3 -m unittest tests.test_schedule_d_presentation_t3
python3 -m unittest tests.test_attachment_rule_v4_completeness_value
python3 -m unittest tests.test_schema_registry
python3 -m unittest tests.derivation.test_package_validation
python3 -m unittest tests.test_presentation_l2_integration
python3 -m unittest tests.test_presentation_live_session
python3 -m unittest tests.test_presentation_live_viewing_vehicle
node --test tools/presentation_harness/tests/*.test.mjs
node tools/presentation_harness/run.mjs --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json
node tools/presentation_harness/run.mjs --manifest tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json
node tools/presentation_harness/run.mjs --manifest tools/presentation_harness/examples/manifests/schedule-d-covered-ltcg-8a.v1.json
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range dbc1c62..HEAD
git diff --check dbc1c62..HEAD
```

Use a base comparison against `dbc1c62` (Track 1's accepted tip) only to
attribute a specific failure. Do not run the full suite merely to
duplicate CI.

## Review record and verdict

Write `docs/reviews/2026-08-02-schedule-d-covered-ltcg-8a-track2-3-review.md`
and commit it on the same branch. Report one explicit verdict:

- `READY` — every required measurement passes with cited evidence; or
- `NOT READY` — numbered findings F1… identify the violated
  charter/ADR/publication/safety clause, precise file/line evidence, and a
  reproducible measurement.

Findings recommend no scope expansion and no repair design. Do not edit
implementation, charters, phase state, or the milestone plan; do not push,
open or merge a PR, begin closeout, or review your own record. Stop after
the review-record commit and return custody to the foreman.
