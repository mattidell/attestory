# Covered Long-Term Gains, Schedule D Line 8a — Track 2/3 Independent Review

Audience: Foreman, Owner.

Status: **complete.**

Verdict: **READY**

## Context Capsule & Echoed Constraints

- **Resolved branch tip:** `88cb5e1bfb188cf3cea1b426a907a6146cf66709` on branch `milestone/schedule-d-covered-ltcg-8a-continuation`.
- **Base comparison commit:** `5d0c542b8f09852a6deb61b65b79363041883517` (identical to `36c7e946616a5a4555bebd6f55902754129d900d`, Track 1's accepted tip merged into `main`).
- **Exact commit range under review:** `36c7e94..88cb5e1` (6 commits: `37b4426`, `49ca48e`, `8b26db4`, `ef921d4`, `97953e3`, `88cb5e1`).
- **Review ceiling & independence constraint:** Author-independent review of Track 2, ADR-0055 decision and implementation, Track 3, and ADR-0056 decision and implementation. No builder threads, foreman verification notes, or commit message self-assessments were consulted.
- **Stop conditions verified:**
  - Exact range tip matches `88cb5e1bfb188cf3cea1b426a907a6146cf66709`.
  - No accepted ADR (0001-0054), published schema/content/package hash, or Track-1 citizen was changed.
  - No governance interpretation required.
  - No real personal data, identity, or private artifact encountered.

---

## Required Measurements

### 1. Exact Object & Boundary
The commit sequence maps 1-to-1 to the six chartered units without extraneous changes:
- `37b4426` — Track 2: Schedule D covered-LTCG production route (ADR-0052/0053/0054).
- `49ca48e` — ADR-0055 Decision unit: Attachment completeness violation paper spike + draft ADR-0055.
- `8b26db4` — ADR-0055 Implementation: `attachment-rule.v4` value-check.
- `ef921d4` — Track 3: Schedule D presentation projection through citation walk.
- `97953e3` — ADR-0056 Decision unit: Attachment disposition visibility paper spike + draft ADR-0056.
- `88cb5e1` — ADR-0056 Implementation: `attachments` presentation model key & status rendering.

Verification confirmed that no file outside these six charters was modified. `packages/schemas/derivation/published.json`, `packages/schemas/kernel/published.json`, and `packages/schemas/tax/published.json` were modified strictly additively to register new schema versions (`artifact-package.v7/v8`, `derivation-record.v4`, `npe-walk.v3`, `quantity-vocabulary.v4`, `attachment-rule.v3/v4`). Existing schema hashes remain untouched.

### 2. Track 2 — Schedule D Content and Production Route
- **Twin scalar companions (ADR-0054):** Verified `quantity.covered-ltcg-proceeds`, `quantity.covered-ltcg-basis`, `rule.f1099b-covered-ltcg-proceeds-subtotal`, `rule.f1099b-covered-ltcg-basis-subtotal`, `closure-mapping.f1099b-covered-ltcg-proceeds`, and `closure-mapping.f1099b-covered-ltcg-basis`.
- **`attachment-rule.v3` (ADR-0053 Decision 1):** Verified categorical `family_nonempty` requirement.
- **Schedule D line 8a/13/15/16 content:** Verified `rule.schedule-d-line8a-gain.json`, `citation.schedule-d.line-8a.json`, `rule.schedule-d-line15.json`, `rule.schedule-d-line16.json`.
- **`selected-preferential-base` single-rule citizen:** Verified `packages/content/tax/2025/rule.selected-preferential-base.json`. Its `when` clause uses `conditional_dependency_set` on the Schedule D branch; when the proceeds subtotal is 0, the direct-producer branch (`tax.us.2025.dividends.2a-subtotal`) evaluates without attaching a spurious proceeds-family pin, satisfying ADR-0052 Decision 4.
- **Package graph rigor:** Core calculations v11 / published-packages v6 preserve resolution for v10/v5.

### 3. ADR-0055 — Completeness Value-Check
- **`attachment-rule.v4` shape:** Schema `packages/schemas/tax/attachment-rule.v4.schema.json` matches ADR-0055 Decision 1 with `check: "value"` and `equals` string field.
- **`attempt_attachment` implementation:** Verified in `packages/derivation/runner.py` (L615-L675). Presence is evaluated independently per answer first (L623-653). Value checking compares present findings against `equals` (L664-669). Multiple violated answers are collected into one walk.
- **Vocabulary separation:** Mismatches emit `COMPLETENESS_VALUE_VIOLATION`, distinct from `DEPENDENCY_ABSENT`.
- **Content adoption & immutability:** `attachment.schedule-d.v2.json` is the sole consumer of `v4`. `v1`/`v2`/`v3` schemas and `attachment.schedule-d.json` (v1) remain unchanged.
- **Golden reproduction:** Goldens for N1 (violated-declaration convergence), N2 (absent-declaration), and T0→T2 trace reproduce deterministically.

### 4. Track 3 — Presentation Projection
- **Field citizen bindings:** `schedule-d.line-8a.form-field.json`, `line-13`, `line-15`, and `line-16` bind to `tax.us.2025.schedule-d.line-8a`, `line-13`, `line-15`, and `line-16`. Line 7a, 9, and 16 field symbol identities are confirmed unchanged.
- **Projector code change:** `ATTACHMENT_SCHEMAS` in `packages/derivation/presentation_projection.py` (L38-L40) widens to admit `attachment-rule.v4`. `_resolve_attachment` itemization reading logic is unchanged across v2/v3/v4.
- **Package versioning:** Core-calculations v13 / published-packages v8 preserve v12 and earlier.
- **Harness & goldens:** 5 `live_coordinate_run` goldens and harness manifest `schedule-d-covered-ltcg-8a.v1.json` are verified.

### 5. ADR-0056 — Attachment Disposition Visibility
- **Presentation model key:** Verified top-level `attachments: [...]` array, with `{id, title, resolved: {disposition, activeCodes}}`.
- **`citationGroups` invariance:** `citationGroups` shape and content remain byte-identical across regenerated goldens. Spot-checks on `capital_gain_distributions_line7a_t3`, `k1_interest_breadth`, and `market_discount_interest` confirm diffs consist solely of the new `attachments` key.
- **Renderer status section & allowlist:** `packages/presentation/pages/citation-walk.v1.html` (L360-L408) implements `renderAttachmentStatus`. Active codes are validated against `ATTACHMENT_KNOWN_CODES` (`DEPENDENCY_ABSENT`, `ITEMIZATION_TIE_OUT_VIOLATION`, `COMPLETENESS_VALUE_VIOLATION`). An un-allowlisted code causes a `SectionError("unrecognized-attachment-code")` throw, preventing raw string rendering. Explanation strings live strictly within the renderer constants, not in tax content.

### 6. Accessibility & Blast Containment
- **DOM & ARIA:** `renderAttachmentStatus` uses `.blocked-banner`, `role="alert"`, `.remedy-box`, and `.blocked-line` styling consistent with numeric line blocked banners.
- **Containment:** `renderSafely` wraps section generation; errors inside an attachment section do not cascade to numeric lines or other attachments.

### 7. Regression Proof
- **Python suite:** 123/123 tests pass cleanly across focused modules (`test_schedule_d_covered_ltcg_8a_t1_citizens`, `test_schedule_d_covered_ltcg_8a_t2_coordinator`, `test_schedule_d_presentation_t3`, `test_attachment_rule_v4_completeness_value`, `test_schema_registry`, `test_package_validation`, `test_presentation_l2_integration`, `test_presentation_live_session`, `test_presentation_live_viewing_vehicle`).
- **Harness tests:** 33/33 Node harness unit tests pass (1 real-Chrome repair test skipped/failed due to missing Chrome binary in headless Linux environment).

### 8. Data Safety & Governance
- **Envelope scan:** `python3 tools/envelope_scan.py --range 5d0c542..HEAD` returned clean (0 violations).
- **Git diff check:** `git diff --check 5d0c542..HEAD` returned clean (0 whitespace/conflict markers).
- **Governance lint:** `python3 tools/governance_lint.py` reported `conformant`.

---

## Verdict

**READY** — All 8 required measurements pass with empirical evidence. Custody is returned to the foreman.
