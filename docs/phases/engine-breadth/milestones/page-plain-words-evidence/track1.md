# Track 1: Plain Saved-Page Wording and Auditor Reachability

Branch: `milestone/page-plain-words-2025` (rebased onto `e3a4397f`, published core `v101`, registry `v99`, release `v99`).
Charter: `docs/reviews/page-plain-words/charter-track1.md`.
Plan: `docs/phases/engine-breadth/milestones/page-plain-words.md` (Decisions 1–7).

## 1. What changed

### Saved product page (`packages/presentation/pages/citation-walk.v1.html`)
- **Shell (Decision 2):** `<title>` and `<h1 id="page-heading">` read `Form 1040 — Return Summary`. Subtitle reads: *"Every figure below comes from your saved records, with its source cited. This page shows saved results; it does not calculate anything."*
- **Status badges (Decisions 4, 6, 7):**
  - Line badges: `Calculated`, `Calculated zero`, `Confirmed none`, `Determined`, `Not calculated` (Decision 6), `Not applicable`.
  - Attachment badges: `Complete`, `Incomplete`, `Not required`.
  - Every badge keeps its CSS class and adds `data-disposition="<raw>"` and `title="Recorded status: <raw>"`.
- **Blocked banners & remedies (Decisions 4, 6):**
  - Line blocked heading: `This line could not be calculated.` Plain code summaries replace raw `Missing dependency code(s): ...` when no `Why:` reasons are present; raw `activeCodes` move into `data-active-codes` and a collapsed `<details class="technical-details"><summary>Technical details</summary>...</details>`. Remedy reads `What to do: add or confirm the missing information so this line can be calculated.` ADR-0087's bold `memberLabel` prefix on roster-member reasons is preserved.
  - Attachment blocked heading: `Cannot include yet — required information is incomplete.`, plain explain/code summaries, raw codes in `data-active-codes` + collapsed `Technical details`, and `What to do: add or correct the missing information to complete this attachment.`
- **Question groups panel:** heading `Questions holding up lines below`; statuses `An answer is recorded here.`, `Needs reconfirmation.`, `Needs an answer.`.
- **Citations (Decision 3):** fallback button labels read `Line reference` (field citations) or `Supporting record` (source-fact citations); `data-pin-id`, `data-pin-version`, and `title="<pinId>@<pinVersion>"` remain on the button, and the expandable `.citation-detail` `<dl>` labels them `Record ID` and `Record version` with backlinks `also used in <context>`.
- **Support trace (`renderShared`, Decision 4):** summary reads `How this line was determined`. Node captions, edge buttons, disposition captions, predecessor buttons (`Show earlier calculated value`), dependency buttons (`Show what this waits on: ...`), and reuse buttons (`Jump to earlier ...`) use plain role labels and `MODEL.sections` field labels (`binds_symbol`). Exact `role`, `symbol`, `id`, `version`, `produced_by.id`, and disposition `artifact_id` / `disposition` move into collapsed `<details class="audit-ids"><summary>Technical IDs</summary>...</details>` plus `data-*` and `title` attributes.
- **Line 21 explanation (`renderLine21Account`, `renderLine21Explanation`):** plain older-answer currency wording, plain limit names (`Maximum deduction`, `Income phaseout start`, `Income phaseout range`), and snapshot run footer; `Combined class`, raw `parameter.id@version`, and `Run ID` / `workspace revision` move into collapsed `Technical details`.
- **Mortgage interest & mortgage borrowing explanations (Decision 1):** plain headings/labels (`What the calculation determined`, `Default settings used`, `— default setting`, `Schedule A line 8a amount unavailable; the combined result could not be calculated.`, `Answers available for this linked form`, `used in line 8a` / `recorded, not used in line 8a`, `used in this result` / `not shown as used`, `Technical calculation record (for audit)`, plain relationship dispositions with `data-disposition` and `title`); parameter pins, finding IDs, and reason-chain pins move into collapsed `Technical details`.
- **Diagnostics & error alerts (Decisions 1, 7):** suppressed diagnostic reads `Not shown — depends on a line that could not be calculated or does not apply.`. `REASON_TEXT` remains a closed table of static strings (ADR-0046), updated to plain wording plus an explicit entry for `malformed-blocked-reason` (P0 risk 5), and `.section-error` elements carry `data-reason-code`.
- **Preserved anchors:** `const MODEL = Object.freeze(__MODEL_JSON__);`, `function validateMortgageBorrowingExplanation(`, `\ndocument.addEventListener`, and zero provenance markers are unchanged.

### Harness example page (`tools/presentation_harness/examples/pages/citation-walk.v1.html`)
- Updated `renderMortgageBorrowingExplanation` byte-for-byte with the product page (Decisions 1, 5); nothing else in that file or its five manifests changed.

### Readers and pinned-string tests (Decision 7)
- `tools/presentation_harness/sale-page-observation.mjs` now also extracts `disposition_raw` from `.badge[data-disposition]`.
- `tools/sale_page_observation.py` compares `data-disposition` and the plain badge label tables (`_LINE_BADGE_LABELS`, `_ATTACHMENT_BADGE_LABELS`) and `_BLOCKED_LINE_VALUE_TEXT`.
- Updated pinned-string assertions in `tests/helpers/sale_page_observation.py`, `tests/test_sale_page_observation.py`, `tests/test_presentation_live_session.py`, `tests/test_explanation_saved_browser.py`, `tests/test_line12d_boxes_v90.py`, `tests/test_page_alerts_v92.py`, `tests/test_sli_line21_page_reasons.py`, and `tests/test_sli_line21_explanation_page.py`.

## 2. Track 1 census result (core v101, registry v99, release v99)

`track1_census.py` + `check_page_dom.mjs` executed the real page script (before at `9358e904` vs after) on all 691 rendered recorded lists (of 775; 84 unchanged pre-page errors: 82 `FindingModelError`, 1 `HorizonModelError`, 1 `SourceAuthorityError`) plus three synthetic pages covering mortgage interest (with declared default), mortgage borrowing (v4 with comparisons, conflicts, reason chain, links, groups, orphans), and Schedule 1 line 21 (C1). The check inspects first-read visible text outside collapsed `<details class="technical-details">` / `<details class="audit-ids">` and attributes, including expanded support-trace captions/buttons and non-audit detail panels. Results are saved in `track1-census.json`.

| Corpus | Before (lists / leaks) | After (lists / leaks) | After `.section-error` |
| --- | ---: | ---: | ---: |
| 691 rendered recorded lists (core v101) | 691 / 4,004,368 | **0 / 0** | **0** |
| `synthetic/mortgage-interest-qualified-default` | 1 / 2,498 | **0 / 0** | 1 (unchanged pre-existing v44 line alert) |
| `synthetic/mortgage-borrowing-v4` | 1 / 8 | **0 / 0** | **0** |
| `synthetic/line21-c1` | 1 / 2,325 | **0 / 0** | 1 (unchanged pre-existing v40 line alert) |

Content-supplied text (outside Track 1 scope) is tracked separately by `check_page_dom.mjs`: 2 of the 691 recorded lists (`v83/returns/v80/probe_a_bw_on_w_broker/recorded` and `v83/returns/v80/probe_a_high_on_w_broker/recorded`) carry content-supplied wash-sale `reason.sentence` strings that cite `tax.us.2025.block.f8949.*` (96 occurrences total).

## 3. Full-surface replay (no model change)

`python3 tools/recorded_replay.py full v101 v101` across all 775 recorded lists:
- `lists`: 775
- `identical`: 775
- `failing`: 0
- `unexpected_differences`: 0
- `optional_blocks_reached`: `{"line21Explanation": 2}`

## 4. Tests and checks run

- `node tools/presentation_harness/check_mortgage_renderer.mjs`: passed.
- `pytest -m "not live"`: **1952 passed, 8 skipped** in 15.84 s.
- `python3 -m mypy` on all touched Python files (9 repo files + `track1_census.py`): **0 issues**.
- Targeted live/browser tests:
  - `tests/test_presentation_live_session.py`, `tests/test_f1098_circumstances_explanation.py`, `tests/test_sale_page_observation_diagnostics.py`, `tests/test_sale_page_observation_temp_paths.py`, `tests/test_explanation_saved_browser.py`, `tests/test_sli_line21_page_reasons.py`, `tests/test_sli_line21_explanation_page.py`, `tests/test_eic_child_answers_walk.py`, `tests/test_eic_child_answers_v101.py`: all passed.
  - `tests/test_line12d_boxes_v90.py`, `tests/test_page_alerts_v92.py`, `tests/test_line6b_reason_v93.py`, `tests/test_presentation_question_groups_v3.py`, `tests/test_closure_questions.py`, `tests/test_sli_track5_worksheet_integration.py`, `tests/test_sli_track2_explanation.py`: **111 passed**.
  - Opt-in `SALE_PAGE_OBSERVATION_BROWSER=1 pytest tests/test_sale_page_observation.py`: all 10 cases rendered in Chrome and passed all badge/value checks; `sale-answer-needs-reconfirmation` hit a pre-existing v3 `questionGroups` mismatch in `tools/sale_page_observation.py:_compare_model_and_dom` (the DOM renders `See the question and affected lines above` for a grouped reason while `_expected_reason_text` expects the raw sentence). Noted for the foreman.
