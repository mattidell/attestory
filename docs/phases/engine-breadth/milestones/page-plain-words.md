<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "page-plain-words",
  "status": "Closed 2026-11-23. Page and tests only; no package version change.",
  "retrospective": "docs/milestone-retrospectives/2026-11-23-page-plain-words.md",
  "scope": [
    "the words the saved page writes itself (status badges, blocked banners, support-trace captions and their buttons) read as plain language to a filer, not as engine enums, symbols or ids",
    "the ids stay reachable for an auditor where they are the evidence, but are not the caption a filer reads first",
    "every recorded return keeps its numbers, dispositions, reasons and questions"
  ],
  "non_goals": [
    "no package, rule, schema, projection or kernel change; the page file and its tests only",
    "no change to content-supplied text (field titles, reasons, questions), which plain-line-texts covered",
    "no layout or visual redesign beyond the words"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/page-plain-words.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/page-plain-words.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/page-plain-words.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/page-plain-words.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# The Saved Page Writes Its Own Words Plainly (2025)

Milestone key: page-plain-words.
Branch: milestone/page-plain-words-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-23.
Starting point: main at `3f11bde2` (core v100, registry v98, release v98); rebased onto `e3a4397f` (core v101, registry v99, release v99) after #297.
Expected target: no package version change; the page
(`packages/presentation/pages/citation-walk.v1.html`) and its tests.

## What we are trying to accomplish

plain-line-texts made the text that content supplies plain, and parked
the words the page writes itself until blocked-sale-pages, which owned
the same page, merged (plain-line-texts Decision 1). It has now merged
(#299). The page still shows a filer engine words:

- status badges print the disposition enum (`published value`,
  `computed zero`, `closure backed zero`, `guard inapplicable`, `blocked`);
- blocked lines say "No value published — cannot compute." and
  "Missing dependency code(s):";
- support-trace captions print the symbol, finding and rule ids and the
  recorded disposition, and the buttons read "Show <role> <id>",
  "Show recorded predecessor" and "Show dependency <ref>".

A filer who opens the saved page should be able to read what each line is,
whether it has a value, and why not, without knowing the engine. An auditor
must still be able to follow every pin to its id.

## Stages

1. **P0.** Inventory every string the page writes itself and the filer can
   see, with file:line, the condition that shows it, and how many of the
   775 recorded lists show it. Name every test, golden, harness example
   and Chrome observation that pins each string. Draft plain wording for
   each, with what it replaces, and say where an id must stay visible for
   an auditor (for example behind the caption, in a details line). Check
   the harness example page (`tools/presentation_harness/examples/pages/`)
   for the same strings and say whether it must follow. Stop and report;
   do not edit the page.
2. **Decisions** by the foreman on wording and on where ids stay.
3. **Track 1.** Change the page and the tests that pin the old strings.
   Full-surface replay shows no model change (the page is not in the
   model); a page-level check over the recorded lists shows no engine
   enum, symbol or id in the caption text a filer reads first.
4. **Fresh review**, repair, closeout.

## P0 result

Completed 2026-11-23. Evidence in
`docs/phases/engine-breadth/milestones/page-plain-words-evidence/` (`p0.md`; the census script and raw
output were not kept).

- **775-list census (core v100, registry v98, release v98):** 691 recorded
  lists rendered to saved `presentation-model.v3` pages with zero
  `.section-error` alerts; 84 failed with unchanged pre-page errors (82
  `FindingModelError`, 1 `HorizonModelError`, 1 `SourceAuthorityError`).
  Full replay took 172.187 s on 9 workers; 7 representative saved pages
  covering all observed kinds were cross-checked in headless Chromium
  with zero render alerts.
- **Inventory:** 140 filer-visible page-owned string kinds across
  `packages/presentation/pages/citation-walk.v1.html` (1,369 lines).
  70 kinds appeared on at least one recorded list (including 18
  `line21Explanation` kinds on 2 lists); 70 did not appear on any
  recorded list (`REASON_TEXT` alerts, mortgage explanations,
  diagnostics, empty-code fallbacks). 69 kinds need plain wording or
  moving raw IDs/codes behind auditor details (44 observed on recorded
  lists); 71 already read plainly.
- **Top observed leaks (691/691 rendered pages):** all 6 line badges and
  2–3 attachment badges print raw disposition enums; blocked banners
  print `"No value published — cannot compute."`,
  `"Missing dependency code(s): DEPENDENCY_ABSENT"` (and
  `SOURCE_SET_UNCLOSED` on 28 lists), and `"Remedy: contribute the
  missing dependency..."` (148 lists); question groups use `"blocked"`
  and `"this scope"`; citation buttons fall back to raw
  `pinId@pinVersion` on 691/691 lists (`pinLabels` is empty on live
  models); all 9 live support-trace templates print raw symbols, rule
  IDs, finding IDs, pin roles, and disposition enums. On the 2
  `line21Explanation` lists, `"Combined class: none."`, `"Currency:
  current."`, raw parameter IDs (`tax.us.2025.parameter.sli-*`), and
  raw run ID / workspace revision appear.
- **Pins & risks:** 16 test files/helpers, `tools/sale_page_observation.py`
  (parses `.badge` against `disposition.replace("_", " ")` and
  `.line-value` against `"No value published — cannot compute."`),
  `tools/presentation_harness/check_mortgage_renderer.mjs`, and 5
  standalone harness manifests pin existing strings.
  `tests/test_f1098_circumstances_explanation.py:199-214` enforces exact
  byte parity of `validateMortgageBorrowingExplanation` and
  `renderMortgageBorrowingExplanation` between the product page and
  `tools/presentation_harness/examples/pages/citation-walk.v1.html`.
- **Decisions awaiting foreman (`p0.md` Section 7):** (1) Track 1 scope
  (live surfaces + alerts vs also mortgage borrowing), (2) page
  title/heading (`Form 1040 — Citation Walk`), (3) citation button
  fallback labels, (4) auditor ID presentation (`<details>` vs secondary
  line), (5) whether `tools/presentation_harness/examples/pages/citation-walk.v1.html`
  and its 5 manifests follow or stay frozen, and (6) sign-off on drafted
  wording.

## Decisions

1. Track 1 covers every surface in p0.md section 2 that needs words,
   including the mortgage interest and mortgage borrowing explanations
   (P0 Option B), the error texts and the suppressed-diagnostic text. The
   harness copy of `validateMortgageBorrowingExplanation` and
   `renderMortgageBorrowingExplanation` changes byte for byte with the
   product page, as `test_f1098_circumstances_explanation.py` requires.
2. The page is titled `Form 1040 — Return Summary`. The subtitle reads:
   "Every figure below comes from your saved records, with its source
   cited. This page shows saved results; it does not calculate anything."
3. Citation buttons read `Line reference` or `Supporting record`. The pin
   id and version stay in the expandable detail, labelled `Record ID` and
   `Record version`, and in `data-pin-id`, `data-pin-version` and `title`.
4. Ids, enums and codes an auditor follows move into a collapsed
   `<details>` ("Technical details" on banners and panels, "Technical IDs"
   in the support trace) plus `data-*` and `title` attributes, never into
   the text a filer reads first (p0.md section 3).
5. The harness example page otherwise stays a frozen evaluation baseline;
   its five manifests do not change.
6. Wording is p0.md section 2 as drafted, with one change: the blocked
   line badge reads `Not calculated`, not `Cannot calculate`, because a
   blocked line may wait on an answer or a correction, and "not
   calculated" is true of every blocked cause (p0.md risk 6).
7. Anything that reads page text as data reads the raw value instead:
   `tools/sale_page_observation.py` compares `data-disposition` and the
   plain label table, not the badge text. Tests that pin old strings
   follow the new words. `malformed-blocked-reason` gets its own error
   text (p0.md risk 5).
8. Repair before merge (review PPW-R1 to R5). Badges claim only what the
   disposition proves, since a published amount may be carried from
   another line: `published_value` reads `Amount`, `computed_zero` reads
   `Zero`, `closure_backed_zero` keeps `Confirmed none`,
   `published_categorical` keeps `Determined`, `guard_inapplicable` keeps
   `Not applicable`, and `blocked` reads `No result`, with the banner
   "This line has no result." The support trace says `has a result`, not
   `calculated`. The attachment badge for `blocked` reads `Not ready`.
   Under a blocked line or attachment, the explanation sentence, heading
   and remedy are chosen from the code: every code a current field or
   attachment can carry has its own true sentence and remedy (an invalid
   record or a total that does not match is not "missing"), including
   `CATEGORICAL_DOMAIN_MISMATCH` and `ITEMIZATION_TIE_OUT_VIOLATION`. An
   unmapped code, and an unknown mortgage-link disposition, fail closed
   into the static error banner. A render-boundary test fails when a
   first-read text node or an `aria-label` holds a raw id or a badge holds
   the disposition enum. The sale page observer treats an empty
   `data-disposition` on a rendered row as a difference. The first-read
   census judges `aria-label` too.
- **Repair result:** recorded in `page-plain-words-evidence/track1.md` section 5. After that repair, the core v101 census was 691 rendered lists, 0 first-read leaks, and 0 section errors. Synthetic mortgage-interest, mortgage-borrowing, and line 21 pages stayed at 0 page-owned leaks. Full-surface replay v101 against v101 stayed 775 identical, 0 failing, 0 unexpected differences.
9. Repair before merge (re-review PPW-R6 to R8). The Schedule 1 part II
   block says another Part II adjustment is recorded and this calculation
   does not include it, and points to those answers. Because the runner
   stores every code outside `RECORD_CODES` as `DEPENDENCY_INVALID`
   (a refused combination such as line 12e's gambling losses, an absent
   table row, a blocked source family), that code's sentence says only that a
   rule could not use the saved information as it stands and points to
   the related answers; it never says the information is invalid or
   missing. Keeping the specific code on the row is a derivation change,
   parked. The render-boundary test runs Node, so it is an honest live
   test (conftest's rule) and runs in the full suite that gates merge, not
   the fast lane.

## Track 1 result

Completed 2026-11-23 on published core v101 (registry v99, release v99).
Evidence in `docs/phases/engine-breadth/milestones/page-plain-words-evidence/`
(`track1.md` and `check_page_dom.mjs`, which the render-boundary test loads;
the census script and raw output were not kept).

- **Page & harness copy:** updated `packages/presentation/pages/citation-walk.v1.html`
  to the plain wording of P0 section 2 as amended by Decisions 1–7, with
  auditor IDs/codes/enums moved behind collapsed `Technical details` /
  `Technical IDs` `<details>` elements and `data-*` / `title` attributes.
  Synced `renderMortgageBorrowingExplanation` byte-for-byte into
  `tools/presentation_harness/examples/pages/citation-walk.v1.html`
  (nothing else in the harness file or its five manifests changed).
  Preserved `const MODEL = Object.freeze(__MODEL_JSON__);`, all anchors,
  ADR-0046 static `REASON_TEXT` (adding `malformed-blocked-reason`), and
  ADR-0087's bold `memberLabel` prefix.
- **Readers & pinned tests:** updated `tools/presentation_harness/sale-page-observation.mjs`,
  `tools/sale_page_observation.py` (reads `data-disposition` and plain
  badge label tables), and all pinned-string tests in P0 section 4.
- **Track 1 census (core v101):** across 691 rendered recorded lists (of
  775; 84 unchanged pre-page errors), page-owned first-read leaks dropped
  from **691 lists / 4,004,368 leaks** to **0 lists / 0 leaks**, with **0**
  `.section-error` alerts. Synthetic mortgage interest, mortgage
  borrowing (v4), and Schedule 1 line 21 pages dropped from 2,498 / 8 /
  2,325 page-owned leaks to **0 / 0 / 0**. (Two recorded lists carry
  content-supplied wash-sale `reason.sentence` text naming
  `tax.us.2025.block.f8949.*`, outside Track 1 scope.)
- **No model change:** `tools/recorded_replay.py full v101 v101` reported
  **775 / 775 identical**, 0 failing, 0 unexpected differences.
- **Tests:** `check_mortgage_renderer.mjs` passed; fast lane
  `pytest -m "not live"` passed (1952 passed, 8 skipped); `mypy` clean on
  all touched Python files; all targeted live/browser suites (including
  `test_eic_child_answers_walk.py` and `test_eic_child_answers_v101.py`)
  passed. Opt-in `SALE_PAGE_OBSERVATION_BROWSER=1` passed all badge/value
  checks on all 10 cases and surfaced a pre-existing v3 `questionGroups`
  reason-comparison mismatch on `sale-answer-needs-reconfirmation` in
  `tools/sale_page_observation.py`.

## Closeout

Closed 2026-11-23. The saved page now writes its own words plainly. Status
badges say only what the disposition proves (a published amount may be
carried from another line, so it reads `Amount`, not `Calculated`). A
blocked line or attachment chooses its sentence, heading and remedy from
its code, for the 15 codes a current field, attachment or rule can carry,
and an unknown code fails closed. Ids, enums, codes and pins an auditor
follows are in collapsed technical details and attributes. On all 691
rendered recorded lists on core v101, no engine id or enum is in the text a
filer reads first (before: every list). The full-surface replay is
identical on all 775 lists, so the model did not move. Two items are
parked in the roadmap: the runner's collapse of non-record codes into
`DEPENDENCY_INVALID`, and the opt-in sale observer's reconfirmation case.
