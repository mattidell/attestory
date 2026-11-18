# Fresh Review: Every Line Speaks Plainly (Core v96)

- **Reviewer**: Independent Reviewer (fresh context)
- **Charter**: `docs/reviews/plain-line-texts/charter-review.md`
- **Plan**: `docs/phases/engine-breadth/milestones/plain-line-texts.md` (Decisions 1–10)
- **Reviewed range**: `github/main..baa93e55776cb55c1b327b86e12e53d7de3f9647` (`0bde6638a9d9b744f12422073fcb4b071ea26a7e..baa93e55776cb55c1b327b86e12e53d7de3f9647` on `milestone/plain-line-texts-2025`, 0 behind `origin/main`, 24 ahead, no merged PRs)
- **Verdict**: **READY**

---

## Findings

No blocking or should-fix defects were found within the chartered scope. Two non-blocking observations (`note`) are recorded for closeout/follow-up visibility:

### `PLT-R1` (`note` — evidence precision): `tests/test_plain_line_texts_v96.py` checks inactive disposition leaves in `_drawn` and omits active `explain` texts from `spoken`

- **Claim / invariant**: `docs/reviews/plain-line-texts/charter-track1.md` Item 5 specifies that `tests/test_plain_line_texts_v96.py` should assert that *"the drawn manifest texts appear, no census term remains in any drawn content text, and values match v95."*
- **Artifact and reproduction**:
  - In `tests/test_plain_line_texts_v96.py:116-117`, `_drawn(model)` flattens `_leaves(model["sections"])`, which includes all five declared disposition keys inside `s["field"]["dispositions"]` for every section regardless of which disposition `s["resolved"]["disposition"]` selected for display (`packages/presentation/pages/citation-walk.v1.html:986-1086`).
  - In `tests/test_plain_line_texts_v96.py:146-150`, `spoken` collects only `s["resolved"].get("reasons", [])` (`r["sentence"]`) and `s["field"].get("label")`, omitting the active `s["field"]["dispositions"][instruction_key]["explain"]`, `model["attachments"][*]["title"]`, and `model["mortgageBorrowingExplanation"]["calculationChain"]["resolvedContent"][*]["notes"]`.
- **Consequence**: Evidence precision only (non-blocking). Reverted manifest sentences still fail both `tests/test_plain_line_texts_v96_package.py` and `tests/test_plain_line_texts_v96.py` (verified by Mutations 1a and 1b below), and active DOM rendering of all 57 manifest replacements is verified across the 699 saved pages in `track0-drawn-check.json` and the 51 live review pairs.
- **Smallest property-level repair (optional)**: In `tests/test_plain_line_texts_v96.py`, project each section's active rendered explanation (`"published_value"` when `disposition == "published_categorical"`, else `s["resolved"]["disposition"]`, when `disposition != "blocked"` or `not s["resolved"].get("reasons")`) together with `attachments[*]["title"]` and `mortgageBorrowingExplanation` `resolvedContent[*]["notes"]`.

### `PLT-R2` (`note` — parked-ledger / follow-up scope): Four drawn `explain` properties without `census.py` `TERMS` keywords remain on pre-v96 wording

- **Claim / invariant**: `docs/phases/engine-breadth/milestones/plain-line-texts.md` Decisions 1–3, 7, 9, and 10 scoped core v96 to the 57 properties in 50 citizens flagged by `census.py`'s `TERMS` list (`track0-wording.json`).
- **Artifact and reproduction**: Because `census.py:28-32` flagged `"publishes"` (and 24 other terms) rather than `"computed zero"`, `"conclusion"`, or `"absence"`, four active drawn `explain` properties in `p0b-content-trace.json` had `terms: []` and remained outside the 50-citizen manifest:
  1. `packages/content/tax/2025/form1040.line-6a.form-field.v2.json:24` (`dispositions.computed_zero.explain`, drawn on 693 of 699 pages): `"computed zero for Form 1040 line 6a"`.
  2. `packages/content/tax/2025/form1040.line-6b.form-field.v3.json:24` (`dispositions.computed_zero.explain`, drawn on 319 of 699 pages): `"computed zero for Form 1040 line 6b"`.
  3. `packages/content/tax/2025/form1040.line-7b.form-field.v4.json:32` (`dispositions.published_value.explain`, drawn on 62 of 699 pages via `published_categorical`): `"No sale is recorded and the checked Schedule-D-required conclusion is no; Exception 1 applies and the Schedule D not required box on line 7b is affirmative."`
  4. `packages/content/tax/2025/form1040.tax-after-credits.form-field.v3.json:32` (`dispositions.published_value.explain`, drawn on 2 of 699 pages): `"Tax after nonrefundable credits floors at zero: line 16 regular tax minus line 20 credits under line 17/19 absence. Line 16 meaning is preserved."` (which retains v1's `"line 17/19 absence"` wording).
- **Consequence**: Non-blocking for core v96, as Track 1 was explicitly chartered (Decisions 9–10 and Question 2) to publish only the 50 citizens and 57 properties in `track0-wording.json`.
- **Smallest property-level repair**: Note these four properties in the roadmap's parked list at closeout or succeed them in a follow-up wording pass.

---

## Charter Questions

### 1. Truth to the filer (57 published sentences checked)

All **57 published sentences** in `docs/phases/engine-breadth/milestones/plain-line-texts-evidence/track0-wording.json` were audited against their adopted producer rules and read in drawn saved pages built and run live through `live_coordinate_run` and `live_session._render_page` on published `core v96 / registry v94 / release v94` (and compared against `core v95 / registry v93 / release v93`) across **9 reviewer-constructed synthetic states** (`demo.rev.*`) plus **42 recorded lists**:

- **Reviewer-constructed synthetic states (`demo.rev.*`, all 9 classified `expected_sentences` with `renderAlert = None`)**:
  1. `demo.rev.mfs-lived-with-corrected`: Married filing separately with `mfs-lived-apart-all-year` superseded from `"yes"` to `"no"` — verifies `form1040.line-6d` `guard_inapplicable` on the MFS lived-with branch (`#37`) and `form1040.line-6d-not-checked` `published_categorical`.
  2. `demo.rev.mfj-spouse-int-div`: Married filing jointly with a second spouse W-2 slip ($32,000 wages, $2,800 box 2), Form 1099-INT box 8 ($150), Form 1099-DIV box 12 ($100), and Form 1099-DIV box 1a ($600.30 rounded to $600) — verifies joint/spouse records, `form1040.line-2a` dual-source `published_value` (`#25`), `form1040.line-3b` `published_value` (`#33`), Schedule 8812 lines 14/17 (`#8`, `#9`), and Form 1040 lines 19/28/32/37 (`#16`, `#23`, `#28`, `#29`).
  3. `demo.rev.closed-empty-w2-odc-no-corrected`: Single return with closed-empty `w2` and `w2-box2` families (no Forms W-2 recorded), $100 taxable interest on `form1040.line-2b` (`Schedule B` `guard_inapplicable` / not required), `ctc.no-other-dependent = "no"` with zero qualifying dependents, a superseded estimated-tax payment answer ($300 -> $0), and a retracted-then-reasserted `line38-scope.no-estimated-tax-penalty` finding — verifies `form1040.line-25a` `computed_zero` by absence (`#17`), `form1040.line-2b` `published_value` without Schedule B (`#27`), `sch8812.line-6` `computed_zero` on the `"no"` branch (`#11`), `form1040.line-26` after answer correction (`#21`), and `form1040.line-38` after retraction/reassertion (`#30`).
  4. `demo.rev.rounding-zeros-w2g`: Sub-50-cent positive amounts ($0.40 / $0.20) rounding to $0 across W-2 box 2, estimated tax, 1099-INT box 1/4/8, 1099-DIV box 1a/1b/2a/12, 1099-R box 1, and W-2G box 4, plus W-2G box 1 ($200) alone on Schedule 1 line 10 and Form 1040 line 8 — verifies the rounding-to-zero branch of `#17`, `#18`, `#19`, `#20`, `#21`, `#24`, `#26`, `#31`, `#32`, `#34`, `#38`, `#44`, and single-source W-2G on `#41` and `#47`.
  5. `demo.rev.int8-only-unemp-w2g`: Form 1099-INT box 8 only ($300.40 -> $300) on `form1040.line-2a` (`#25`), plus Form 1099-G box 1 unemployment ($500.40 -> $500 on `schedule1.line-7`, `#50`) and Form W-2G ($300) on `schedule1.line-10` (`#47`) and `form1040.line-8` (`#41`).
  6. `demo.rev.removed-member-low-w2`: Form 1099-INT box 1 member ($500) added then removed via `member-transition` (`form1040.line-2b` `computed_zero`, `#26`), W-2 box 1 wages $0.40 rounding to $0 (`eic-worksheet-a.line-2` `computed_zero` via line 1 < $1, `#4`, and `eic-worksheet-a.line-5` `guard_inapplicable`, `#6`), and Form 1099-G box 1 $0.40 rounding to $0.
  7. `demo.rev.sale`: Schedule D short-term loss sale ($2,000 proceeds, $8,000 basis) — verifies `#39` (`form1040.line-7a` `published_value`), `#40` (`form1040.line-7b` `guard_inapplicable` via recorded sale), and `#46` (`schedule-d.line-16` `published_value`).
  8. `demo.rev.student-loan-detail`: Form 1098-E student loan interest ($700) — verifies `#13` (`form1040.line-10` `published_value`) and `#49` (`schedule1.line-21` `published_value`).
  9. `demo.rev.mortgage-detail`: Form 1098 mortgage interest itemizer ($18,000) — verifies all 5 mortgage calculation-detail `notes` (`#53`–`#57`).
- Together with the 42 recorded lists (which include `v82/m_2a_box_f_loss/honest` and `v82/m_2a_only_exc1_only2a_no/honest` for `#45` `schedule-d.line-13` `published_value` and the Exception-1 `"no"` branch of `#40`, and `v81/case/a_ic3_no` for `#35` `form1040.line-6b` `blocked`, `#42` `form1040.tax-after-credits` `blocked`, `#51` `schedule3.line-1` `blocked`, and `#52` `schedule3.line-8` `blocked`), every one of the 57 sentences was observed as active rendered text on the saved page. None claims a record, form, or calculation the return lacks, and none drops the basis (absence, closure/completeness, rounding, table lookup, or eligibility check) carried by its v95 predecessor.

### 2. Only words changed

- **50 content successors**: Independently verified against `packages/content/tax/2025/` and `track0-wording.json` (which is byte-identical to `p0c-wording.json` on `HEAD`). Each of the 50 new citizen files increments its predecessor version by `+1` and differs from its predecessor JSON only in `version` and the exact property path(s) listed in `track0-wording.json` (57 properties across 50 citizens). All 50 predecessor files are byte-unchanged.
- **Package, registry, and release**:
  - `package.core-calculations.v96.json` has the same 815-member count as `v95`, replaces only those exact 50 `(id, old_version)` member pins with `(id, new_version)` and the 16 of them in `entrypoints`, and matches `package_instance_checksum`.
  - `published-packages.v94.json` preserves every `v93` citizen and package entry unchanged and adds only the 50 new citizen checksums and `("tax.us.2025.package.core-calculations", "v96")`.
  - `demo.release.sli-worksheet-integration.2025.v94.json` differs from `v93` only in `"version": "v94"` and `"package_registry_sha256"`.
  - `packages/tax/loader.py` adds only the `("tax.us.2025.package.core-calculations", "v96")` entries in `named_covered_flag_refusal_maps()` and `domain_package_companion_declarations()`, carrying `v95`'s values unchanged (and the `>= 86` / `>= 92` / `>= 93` version comparisons automatically include `v96`).
- **Validator change (Decision 5)**: `packages/derivation/package_validation.py` adds only the `"v96"` entry in `_successor_graphs`, identical to `"v68"` except `"tax.us.2025.form1040.line-2b": ("form-field.v3", "v7")`.
- **Three re-pinned tests**:
  - `tests/test_capital_gain_distributions_line7a_t1_citizens.py`: updates `self.assertEqual(line_7b["version"], "v4")` (was `"v3"`) where `load_form_fields` loads the newest `form1040.line-7b` form-field citizen (`v2` remains pinned directly on the next lines).
  - `tests/test_dsbs_t1_schema_citizens.py`: updates `self.assertEqual(line_2b["version"], "v7")` (was `"v6"`) where `load_form_fields` loads the newest `form1040.line-2b` form-field citizen (`v4` remains pinned directly below).
  - `tests/test_noncovered_sales_v78_switch.py`: adds `"v96"` to the exact tuple of core versions (`"v79"`..`"v96"`) in `test_only_cores_v79_through_v96_name_the_covered_flag_refusal`.
  - None of the three loosens any check.

### 3. Replay claim

- **Recomputed classification from Track 1 evidence**: Re-ran `p0c_compare.classify` and `track1_replay.mutation_controls` across all **784** pairs (`775` recorded + `9` synthetic) from the preserved v95 baseline and Track 1's replay part file (wall time `81.40s`). The recomputed results match `track1-replay.json` and `track1-mutations.json` exactly:
  - Recorded (`775` lists): `691` `expected_sentences`, `84` `same_error`, `0` `unexpected`.
  - Synthetic (`9` lists): `8` `expected_sentences`, `1` `same_refusal`, `0` `unexpected`.
  - Totals: `223,157` disposition rows and `60,114` page fields compared; all `16` mutation controls rejected.
- **Independent live sample replay (`42` recorded lists + `9` reviewer synthetic lists on published `v95` and `v96`)**:
  - Selected a stratified sample of **42 recorded lists** spanning all five recorded cohorts (`v81`, `v82`, `v83`, `v84`, `v85`), including all 21 recorded example lists named in `track0-wording.json`, 15 additional `expected_sentences` lists across `v81`–`v85`, and 6 `same_error` lists across `v81`–`v83`.
  - Executed both published `v95` (`registry v93`, `release v93`) and published `v96` (`registry v94`, `release v94`) live through `live_coordinate_run` and `_render_page` for all 42 recorded lists (plus the 9 reviewer synthetic cases = 51 pairs / 102 live runs, wall time `161.80s`).
  - Result: **36 `expected_sentences` and 6 `same_error` (0 `unexpected`)** on the 42 recorded lists — 100% agreement with `track1-replay.json` — and **9 `expected_sentences` (0 `unexpected`)** on the 9 reviewer synthetic lists, with `renderAlert = None` and exact saved-HTML `MODEL` parity on every successful page.

### 4. Tests and mutations

Unmutated test runs:
- `pytest tests/test_plain_line_texts_v96_package.py tests/test_plain_line_texts_v96_validator.py tests/test_noncovered_sales_v78_switch.py tests/test_capital_gain_distributions_line7a_t1_citizens.py tests/test_dsbs_t1_schema_citizens.py tests/test_schema_registry.py` -> **80 passed** (`20.54s`).
- `pytest tests/test_plain_line_texts_v96.py` -> **6 passed** (`42.17s`).

Controlled mutations (all files restored byte-for-byte afterward):
1. **Sentence reverted (`form1040.line-2b.form-field.v7.json` `dispositions.computed_zero.explain` reverted to v6 text)**:
   - `pytest tests/test_plain_line_texts_v96_package.py` -> **FAILED** (`3 failed, 4 passed`: `test_successor_bytes_match_the_accepted_digests`, `test_successors_carry_exactly_the_manifest_texts`, `test_registry_v94_is_add_only`).
   - With `published-packages.v94.json` and `release v94` checksums updated so `live_coordinate_run` reaches the page assertions: `pytest tests/test_plain_line_texts_v96.py -k "wage-only"` -> **FAILED** (`1 failed`: `AssertionError: ('tax.us.2025.form1040.line-2b', 'dispositions.computed_zero.explain')` at line 143).
2. **Value changed (`new_model["sections"][0]["resolved"]["value"] = 999999`)**:
   - `pytest tests/test_plain_line_texts_v96.py -k "wage-only"` -> **FAILED** (`1 failed`: `AssertionError` at line 152 comparing `_states(new_model) == _states(old_model)`).
3. **`v96` validator entry removed from `packages/derivation/package_validation.py`**:
   - `pytest tests/test_plain_line_texts_v96_validator.py` -> **FAILED** (`2 failed, 2 passed`: `test_published_v96_with_line_2b_field_v7_is_accepted` failed with `AssertionError: assert ['NOMINEE_RETURN_SUCCESSOR_GRAPH_MIXED'] == []`, and `test_v96_with_line_2b_field_v6_is_rejected` failed with `assert [] == ['NOMINEE_RETURN_SUCCESSOR_GRAPH_MIXED']`).

### 5. Scope and debt

- **Parked items**: Decisions 1–2 and the milestone non-goals appropriately keep page-owned support-trace labels, status badges, fixed blocked banners, citation button `id@version` labels, repeated shared questions / stale Schedule D line 9 reason (`blocked-sale-pages`), and line 12d's two-section boxes parked. The four unflagged drawn `explain` texts without `census.py` `TERMS` keywords are noted in `PLT-R2` above.
- **Single-source rule (ADR-0045)**: No rule or definition is written twice across the milestone's code, content, or documentation changes.
- **Data safety and paths**:
  - `python3 tools/envelope_scan.py --range github/main..HEAD` and `python3 tools/envelope_scan.py --range main..HEAD` both exited `0` with no findings.
  - Direct regex scan across all 122 changed files on `github/main..HEAD` found `0` absolute workstation/temp paths (`/(Users|private|tmp|var|opt)/...`) and `0` non-demo identifiers.
  - `python3 -m mypy` across all 8 touched Python modules passed with `0` issues.
