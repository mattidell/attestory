# Review: `blocked-names-question` (Core v89 / Rule Artifact v17)

- **Branch:** `milestone/blocked-names-question-2025`
- **Reviewed commit:** the Track 1 head (removed at closeout)
- **Comparison base:** `github/main` (`080d27585dc0ef90910f32e70d6ff76e8618bb6b`)
- **Charter:** `docs/reviews/blocked-names-question/charter-review.md` (`4657bbd9c3e7956ee464ef3776efc47938e402b1`)
- **Verdict:** **not ready** — blocked by `BNQ-R1` and `BNQ-R2`

---

## Charter Questions (1–7)

### 1. The contract (`rule-artifact.v17` and `expressions.py`)

- **Schema diff (`packages/schemas/derivation/rule-artifact.v16.schema.json` vs `packages/schemas/derivation/rule-artifact.v17.schema.json`):**
  - Top-level `$id` and `properties.schema.const` advance from `rule-artifact.v16` to `rule-artifact.v17` (`packages/schemas/derivation/rule-artifact.v17.schema.json:3,13`).
  - On the `block` expression branch (`packages/schemas/derivation/rule-artifact.v17.schema.json:770-791`), `v17` adds only the optional `missing` property (`type: "array"`, `minItems: 1`, `uniqueItems: true`, `items: {"type": "string", "minLength": 1}`), with `additionalProperties: false` and `required: ["op", "code"]`. No other schema property or definition changes.
  - Direct schema validation checks confirm:
    - `rule-artifact.v17` accepts `{"op": "block", "code": "DEPENDENCY_ABSENT"}` and `{"op": "block", "code": "DEPENDENCY_ABSENT", "missing": ["a", "b"]}`.
    - `rule-artifact.v17` rejects `missing: []`, duplicate entries `missing: ["a", "a"]`, empty strings `missing: [""]`, and unknown keys on `block`.
    - `rule-artifact.v16` rejects `missing` on `block` (`additionalProperties: false`).
- **Loader and validator (`packages/derivation/loader.py:72,217` and `packages/derivation/package_validation.py:32`):**
  - Accept `"rule-artifact.v17"` alongside `"rule-artifact.v1"` through `"rule-artifact.v16"`.
- **Evaluator (`packages/derivation/expressions.py:389-396`):**
  - When `op == "block"`, `_eval_node` reads `missing = node.get("missing")` and raises `EvalBlocked(str(node["code"]), [str(item) for item in missing] if isinstance(missing, list) else [])`.
  - Direct evaluation checks confirm:
    - A `v17` rule with `missing: ["tax.us.2025.q1", "tax.us.2025.q2"]` raises `EvalBlocked(category="DEPENDENCY_ABSENT", missing=["tax.us.2025.q1", "tax.us.2025.q2"])`.
    - A `v17` rule without `missing` and a `v16` rule both raise `EvalBlocked(category="DEPENDENCY_ABSENT", missing=[])` identically to prior behavior.

### 2. Routing only

- **Can a declared name in `block.missing` change a read, a pin, scheduling, a closure, an answer, or a number?**
  - **No** for reads, pins, scheduling, closures, answers, and numbers:
    - `packages/derivation/expressions.py:389-396` only inspects `node.get("missing")` inside the `if op == "block":` branch at the moment `EvalBlocked` is raised; it never calls `access.record(...)` or reads `env.symbols` for the names in `missing`.
    - `packages/derivation/runner.py:2526-2548` (`_record_blocked`) builds `pins` strictly from `self.ledger_pins_for(rule, access)` (`AccessLog`), never from `missing`.
    - Rule scheduling and readiness (`packages/derivation/runner.py:2938-2967`) read only `rule["requires"]` and `conditional_dependency_set`, never `block.missing`.
    - Source closures (`packages/derivation/source_authority.py`), answers, and published numbers cannot be altered because `EvalBlocked` aborts the rule before any value is published to `self.symbols`.
  - **One internal disposition-code coupling (`BNQ-R6`, `note`):** `packages/derivation/runner.py:2532` passes `(code, missing)` to `self._apply_covered_flag_block(code, missing)` (`packages/derivation/source_authority.py:268-293`). If a rule ever declared a covered sale family ID from `self.refused_covered_families` inside `block.missing`, `_apply_covered_flag_block` would rewrite `code` to `"DEPENDENCY_INVALID"` and replace that family ID with `"BASIS_NOT_REPORTED_ON_COVERED"`. None of the 11 `v17` rules in core `v89` name a covered sale family in `block.missing`.

### 3. Every dead end closed (Track 0 cases on core v89)

Running the production coordinator (`live_coordinate_run`) on published core `v89` across all 10 Track 0 matrix cases (`unanswered` and `truthful_answer`) and the 3 long-term authority cases reveals two blocking defects (`BNQ-R1`, `BNQ-R2`) and one question-targeting defect (`BNQ-R3`):

| Case | Unanswered: every blocked field names a question? | Question(s) shown on `unanswered` | Truthful answer reaches 2025-instruction hand value? | Defect |
| --- | --- | --- | --- | --- |
| `sd_yes_nothing` | Yes | `Q1`, `Q2`, `NO_8949` (+ v88 age/blind) | Yes (`schedule-d.line-3: 0`, `line-16: 0`, `form1040.line-7a: 0`) | — |
| `sd_8949_no_unadmitted` | Yes | `IC80` (+ v88 age/blind) | Yes (`schedule-d.line-3: -6000`, `form1040.line-7a: -3000`, `line-11a: 47000`) | — |
| `sd_sale_beside_8949_yes` | Yes, but asks wrong/already-answered questions | `NO_8949`, `IC80` (already `"yes"`), and `IC81` (Code B question when no Code B sale exists) | Partial on wave 1 (`schedule-d.line-3: -6000`, but `form1040.line-7a: blocked` on `PATH_B`); reaches `form1040.line-7a: -3000` only after a second answer `PATH_B = "no"` | `BNQ-R2`, `BNQ-R3` |
| `sd_amounts_disagree` | Yes | `f8949.no1099b-st-txn.proceeds`, `.basis`, `.wash-sale-code`, `.adjustment-amount` | Yes (`schedule-d.line-3: -6000`, `form1040.line-7a: -3000`, `line-11a: 47000`) | — |
| `sd_path_b_unanswered` | Yes | `PATH_B` (+ v88 age/blind) | Yes (`schedule-d.line-3: -6000`, `form1040.line-7a: -3000`, `line-11a: 47000`) | — |
| `codeb_yes_nothing` | Yes | `Q3`, `IC81` (+ v88 age/blind) | Yes (`schedule-d.line-1b: 0`, `line-16: 0`, `form1040.line-7a: 0`) | — |
| `codeb_sale_beside_8949_yes` | Yes, but also asks `IC80` (box C/F question when no box C/F sale exists) | `NO_8949`, `IC80`, `IC81` (already `"yes"`) | Partial on wave 1 (`schedule-d.line-1b: 6000`, but `form1040.line-7a: blocked` on `PATH_B`); reaches `form1040.line-7a: 6000` only after a second answer `PATH_B = "no"` | `BNQ-R2`, `BNQ-R3` |
| `codeb_amounts_disagree` | Yes | `f1099b.code-b-st-txn.proceeds`, `.basis`, `.form8949-code`, `.adjustment-amount` | Yes (`schedule-d.line-1b: 6000`, `form1040.line-7a: 6000`, `line-11a: 56000`) | — |
| `exception1_personal_loss_8949` | Asks 4 questions already answered `"no"` | `Q1`, `Q2`, `NO_8949`, `PATH_B` (all 4 already answered `"no"` in `unanswered`) | **No** — remains `blocked` on `truthful_answer` with the exact same 4 already-answered questions and no hand value | `BNQ-R2` |
| `wash_adjustment_open` | Yes | `f1099b.covered-w-st-adjustment.source-closure` | Yes (`schedule-d.line-1b: -5000`, `form1040.line-7a: -3000`, `line-11a: 47000`) | — |

### 4. Form 1040 Line 16 on the 4 recorded `v82/*` returns

On the 4 recorded returns in `docs/phases/engine-breadth/milestones/blocked-names-question-evidence/rerun-repair-output.json` where `form1040.line-16` changes from `guard_inapplicable` (v87) to `blocked` (v89) — `v82/m_2a_only_exc1_only2a_no/honest`, `v82/m_empty_exc1_nolosses_no/honest`, `v82/m_empty_exc1_only2a_no/honest`, and `v82/t4_s1_removed/honest`:
1. **Is the block true?** The return is genuinely blocked from computing `form1040.line-16` (and 27 other lines) because `schedule-d-required.conclusion == "yes"` (due to `exception1.only-box2a-capital-gains = "no"` or `exception1.no-capital-losses = "no"`), while `rule.selected-preferential-base.v10.json:920-1105` evaluates its `when` guard to `False` (`inapplicable`) whenever `schedule-d-required.conclusion == "yes"` and all 10 sale family counts and `schedule-d.line-1b..10` are `0` (even on `v82/m_2a_only_exc1_only2a_no/honest`, where `schedule-d.line-13 = 1000` and `schedule-d.line-16 = 1000` from Form 1099-DIV box 2a).
2. **Does `form1040.line-16` name a question on these 4 returns, and does that question lead to the right number?** **No (`BNQ-R1`, `blocking`).**
   - On all 4 returns, `form1040.line-16` is unattempted because `capital-gains.selected-preferential-base` is `inapplicable`. In `finalize_unattempted` (`packages/derivation/runner.py:3034-3077`), `evaluate(rule["when"], ...)` raises `EvalBlocked("DEPENDENCY_ABSENT", [Q1, Q2, NO_8949, PATH_B])`, which prevents `form1040-line16` from being marked `inapplicable`, **but `runner.py:3055-3075` discards `guard_blocked.missing`** and records `missing: ["income.taxable-income", "capital-gains.selected-preferential-base", "qdcg-worksheet.line-24", "qdcg-worksheet.line-25"]`.
   - Because `capital-gains.selected-preferential-base` has disposition `inapplicable` (neither `blocked` nor a question target), `packages/derivation/presentation_projection.py:578-629` (`_all_roots_resolved`) treats it as an unexplainable leaf root and suppresses all `reasons` and `questions` on `form1040.line-16` (`reasons: []`, `questions: []`).
   - After answering the unrelated v85/v88 questions (`no-sale-box4-present = "no"`, `taxpayer-over-65 = False`, `taxpayer-blind = False`), all 4 returns have **28 blocked lines and `questions: []` (zero questions on the page)**.
   - Even if `rule.form1040-line16.v8.json`'s declared `missing` (`[Q1, Q2, NO_8949, PATH_B]`) were surfaced, all 4 facts are already answered on those 4 returns (`Q1 = "no"`, `Q2 = "no"`, `NO_8949 = "yes"`, `PATH_B = "yes"`), and changing `NO_8949` to `"no"` still leaves `selected-preferential-base` `inapplicable` once `PATH_B` is answered; only changing the Exception 1 answers (`exception1.only-box2a-capital-gains = "yes"`, `exception1.no-capital-losses = "yes"`) makes `selected-preferential-base` publish and `form1040.line-16` compute `3875`.

### 5. Immutability

- **Schema manifests (`packages/schemas/derivation/published.json`, `packages/schemas/releases/published.json`):**
  - `packages/schemas/derivation/published.json` is strictly add-only: all 24 existing entries are unchanged, and `rule-artifact.v17.schema.json` (`94a3f11f59781b3556d3c761b18aa75e78c8f519a5dc7d25b1309aa500b5a4d5`) is appended.
  - `packages/schemas/releases/published.json` is unchanged.
- **Package registry (`packages/content/tax/2025/published-packages.v87.json` vs `v86`):**
  - Strictly add-only over `published-packages.v86.json`: all 86 prior package entries and checksums are byte-identical, and `tax.us.2025.package.core-calculations@v89` (`7d598359958ef15f63cf1ad53408587eb2555da100b8ac6e38f9f8e1a36b04d6`) is appended.
- **Byte-identity with `prototype.py`:**
  - Running `prototype.build_into(tmp)` and comparing against `packages/content/tax/2025/` and `packages/sample_data/student_loan_worksheet_integration/publication_surface/releases/` confirms that all 11 new `v17` rule files, `package.core-calculations.v89.json`, `published-packages.v87.json`, and `demo.release.sli-worksheet-integration.2025.v87.json` are **byte-for-byte identical** to `prototype.py`'s output, and every `artifact_hashes` entry matches `citizen_checksum`.
- **Loader and kernel boundaries:**
  - `packages/tax/loader.py` changes only to add `("tax.us.2025.package.core-calculations", "v89")` to `domain_package_companion_declarations()` and `named_covered_flag_refusal_maps()`.
  - `git diff github/main..HEAD -- packages/kernel` is **empty**.

### 6. CI cost and isolation

- **Redundant runs (`BNQ-R4`, `should-fix`):** Across the 328 live runs (`30` in `tests/test_blocked_names_question_v89.py` + `298` in `tests/test_blocked_names_question_v89_recorded.py`), 6 runs in `test_blocked_names_question_v89.py` are either state-identical duplicates of sibling runs or assert nothing beyond `outcome == "success"`, and `test_blocked_names_question_v89_recorded.py` builds 477 non-`v83/` act lists it immediately discards and runs 264 `v83/` lists that do not touch any v89 rule change. See `BNQ-R4` for exact run IDs.
- **`evidence_loader` bypasses (`BNQ-R5`, `should-fix`):** `common.py`, `rerun.py`, and the transitive `question-wording-evidence` / `age-blindness-asked-evidence` loaders bypass `tests/evidence_loader.py` via raw `importlib.util.spec_from_file_location`, leaking 4 test modules into the main pytest process's `sys.modules`, and both v89 test modules call `evidence_loader.load` inside `ProcessPoolExecutor` child processes where `evidence_loader` is not activated. See `BNQ-R5`.

### 7. Data safety

- `python3 tools/envelope_scan.py --range github/main..HEAD` exits `0` with no findings.
- This review contains no absolute or temporary-directory paths.

---

## Findings

### `BNQ-R1` — `form1040.line-16` blocks with `reasons: []` and `questions: []` on the 4 recorded `v82/*` returns, and `rule.form1040-line16.v8.json`'s `when` block `missing` is discarded by `finalize_unattempted`

- **Severity:** `blocking`
- **Locations:**
  - `packages/content/tax/2025/rule.form1040-line16.v8.json:534-544`
  - `packages/derivation/runner.py:3034-3077`
  - `packages/content/tax/2025/rule.selected-preferential-base.v10.json:920-1105`
- **Reproduction:**
  Run `v82/m_2a_only_exc1_only2a_no/honest`, `v82/m_empty_exc1_nolosses_no/honest`, `v82/m_empty_exc1_only2a_no/honest`, and `v82/t4_s1_removed/honest` from `tests/test_sale_family_audit_v82.py` through `track0.run` on published core `v89`, both as recorded and after answering the v85/v88 questions (`tax.us.2025.f1099b.no-sale-box4-present = "no"`, `tax.us.2025.taxpayer-over-65 = False`, `tax.us.2025.taxpayer-blind = False`):
  ```python
  import tests.test_sale_family_audit_v82 as sfa
  from tests import evidence_loader

  evidence_loader.activate("repro")
  ev = "docs/phases/engine-breadth/milestones/blocked-names-question-evidence"
  evidence_loader.load(f"{ev}/common.py", "common")
  evidence_loader.load(f"{ev}/probe.py", "probe")
  evidence_loader.load(f"{ev}/prototype.py", "prototype")
  track0 = evidence_loader.load(f"{ev}/track0.py", "track0")

  t = sfa.track0()
  acts = sfa.track0_acts(t, "m_2a_only_exc1_only2a_no", "honest", sfa.v82(t))
  core = track0.h.Core("v89", "v87", "v87")
  res = track0.run(core, acts, "demo.repro.v82.m2a", scratch=False)
  print([b for b in res["blocked"] if "form1040.line-16" in b["fields"]])
  # -> [{'fields': ['form1040.line-16'], 'artifact': 'form1040-line16',
  #      'code': 'DEPENDENCY_ABSENT',
  #      'missing': ['income.taxable-income', 'capital-gains.selected-preferential-base',
  #                  'qdcg-worksheet.line-24', 'qdcg-worksheet.line-25'],
  #      'reasons': [], 'questions': []}]
  ```
  1. On all 4 returns, `no-form8949-sources = "yes"`, `noncovered-sold.source-closure = "no"`, `no1099b-sold.source-closure = "no"`, `code-b-sold.source-closure = "no"`, all 10 sale family counts are `0`, and `schedule-d-required.conclusion = "yes"` (because `exception1.only-box2a-capital-gains = "no"` or `exception1.no-capital-losses = "no"`).
  2. Because `no-form8949-sources = "yes"`, `schedule-d.line-3 = 0` and `schedule-d.line-10 = 0` publish, and `schedule-d.line-16` publishes (`1000` on `m_2a_only_exc1_only2a_no` from Form 1099-DIV box 2a; `0` on the other 3).
  3. However, `rule.selected-preferential-base.v10.json:920-1105` evaluates its `when` guard to `False` (`inapplicable`) when `schedule-d-required.conclusion == "yes"` and all 10 sale family counts and `schedule-d.line-1b..10` are `0`.
  4. Because `capital-gains.selected-preferential-base` is `inapplicable` (not published and not blocked), `form1040-line7a`, `qdcg-worksheet.line-4`, `qdcg-worksheet.line-5`, and `form1040-line16` are never attempted in the main loop and enter `finalize_unattempted` (`packages/derivation/runner.py:3034`).
  5. In `finalize_unattempted`, `evaluate(rule["when"], ...)` on `rule.form1040-line16.v8.json` raises `EvalBlocked("DEPENDENCY_ABSENT", [Q1, Q2, NO_8949, PATH_B])` (`runner.py:3037-3040`). That stops `form1040-line16` from being marked `inapplicable` (as it was on v87), **but `runner.py:3055-3075` discards `guard_blocked.missing`** and records `missing = [req for req in rule["requires"] if req not in self.symbols]` (`['income.taxable-income', 'capital-gains.selected-preferential-base', 'qdcg-worksheet.line-24', 'qdcg-worksheet.line-25']`).
  6. Because `capital-gains.selected-preferential-base` is `inapplicable` (neither `blocked` nor a question target), `packages/derivation/presentation_projection.py:578-629` (`_all_roots_resolved`) sees an unexplainable leaf root and suppresses all `reasons` and `questions` on `form1040.line-16` (`reasons: []`, `questions: []`). After answering the v85/v88 questions (`no-sale-box4-present = "no"`, `taxpayer-over-65 = False`, `taxpayer-blind = False`), all 4 returns have **28 blocked lines and `questions: []` (0 questions on the page)**.
  7. Furthermore, on those 4 returns, the 4 facts declared in `rule.form1040-line16.v8.json` (`Q1`, `Q2`, `NO_8949`, `PATH_B`) are already answered (`"no"`, `"no"`, `"yes"`, `"yes"`), and only changing the Exception 1 answers (`exception1.only-box2a-capital-gains = "yes"`, `exception1.no-capital-losses = "yes"`) makes `selected-preferential-base` publish and `form1040.line-16` reach `3875`.
- **Fix:**
  1. Address the root guard gap in `selected-preferential-base` (and matching downstream guards in `form1040-line16`) when `schedule-d-required.conclusion == "yes"` on a return whose closed sale families are empty (or where `schedule-d.line-13` / `schedule-d.line-16` carries a box 2a distribution, as in `v82/m_2a_only_exc1_only2a_no/honest`, or where Exception 1 was answered `"no"` with no sales): either `selected-preferential-base` must compute from the published Schedule D lines when Schedule D is complete, or its guard must block naming the contradicted Exception 1 / sale-closure questions so `selected-preferential-base` is `blocked` (with explainable question roots) rather than `inapplicable`.
  2. If a rule's `when` guard raises `EvalBlocked` with explicit `guard_blocked.missing` during `finalize_unattempted` (`packages/derivation/runner.py:3057-3065`), do not silently drop `guard_blocked.missing` when `missing` contains an `inapplicable` required symbol that has no blocked producer.

---

### `BNQ-R2` — Three Track 0 cases (`exception1_personal_loss_8949`, `sd_sale_beside_8949_yes`, `codeb_sale_beside_8949_yes`) do not reach their 2025-instruction hand values on `truthful_answer`, and `test_blocked_names_question_v89.py:119` suppresses all `hand_failures`

- **Severity:** `blocking`
- **Locations:**
  - `docs/phases/engine-breadth/milestones/blocked-names-question-evidence/probe.py:73-74, 86, 94`
  - `docs/phases/engine-breadth/milestones/blocked-names-question-evidence/track0.py:112-135, 150-167`
  - `tests/test_blocked_names_question_v89.py:117-120`
- **Reproduction:**
  Inspect `docs/phases/engine-breadth/milestones/blocked-names-question-evidence/track0-matrix.json` or run `track0.resolved(case_id, core_path)` on published core `v89`:
  1. **`exception1_personal_loss_8949` (`probe.py:73-74`, `track0.py:165-166`):**
     - `probe.personal_loss_8949()` calls `empty(form8949="no", path_b="no", exc1_only_2a="no", exc1_no_losses="no")`, which already asserts `NONCOV_SOLD = "no"`, `NO1099B_SOLD = "no"`, `NO_8949 = "no"`, and `PATH_B = "no"`.
     - `track0.resolved("exception1_personal_loss_8949", ...)` (`track0.py:165-166`) calls `answer(acts, PATH_B, "no", ...)`, re-asserting the exact same `PATH_B = "no"` value already in `acts`.
     - Consequently, in both `unanswered` and `truthful_answer`, the return remains `blocked` across all 28 lines (`schedule-d.line-3`, `schedule-d.line-10`, `form1040.line-7a`, `form1040.line-16`, etc.), surfaces the exact same 4 questions that the filer **already answered `"no"`** (`NONCOV_SOLD`, `NO1099B_SOLD`, `NO_8949`, `PATH_B`), never names the Exception 1 questions (`exception1.only-box2a-capital-gains`, `exception1.no-capital-losses`), and never reaches a 2025-instruction hand value (`track0.HAND` omits `exception1_personal_loss_8949`).
  2. **`sd_sale_beside_8949_yes` and `codeb_sale_beside_8949_yes` (`probe.py:86, 94`, `track0.py:153-155`):**
     - Both cases start with `form8949="yes", path_b=None`.
     - `track0.resolved` only answers `NO_8949 = "no"`, leaving `PATH_B` unanswered (`None`).
     - On `truthful_answer`, `schedule-d.line-3` (`-6000`) / `schedule-d.line-1b` (`6000`) compute, but `form1040.line-7a`, `form1040.line-11a`, `form1040.line-15`, `form1040.line-16`, and `form1040.line-24` remain `blocked` asking `PATH_B` ("Is it true that every Form 8949 adjustment code is W..."). Answering `PATH_B = "no"` as well resolves `form1040.line-7a` (`-3000` and `6000`) and `form1040.line-11a` (`47000` and `56000`).
  3. **`tests/test_blocked_names_question_v89.py:118-120` never checks `hand_failures`:**
     ```python
     hand = cast(dict[str, Any], claim.get("hand") or {})
     bad = track.hand_failures(result, hand)
     if bad and not result.get("questions"):
         failures.append(f"{claim['category']} {claim['id']}: {bad}")
     ```
     Because none of the Track 0 cases answer the v88 `taxpayer-over-65` and `taxpayer-blind` questions, `result.get("questions")` has length `>= 2` on **every single `truthful_answer` run in `test_blocked_names_question_v89.py`**. As a result, `not result.get("questions")` is **always `False`**, and `hand_failures` is completely dead code in `test_blocked_names_question_v89.py`!
- **Fix:**
  1. In `tests/test_blocked_names_question_v89.py:119`, assert `if bad:` unconditionally whenever `claim.get("hand")` is non-empty (do not gate `hand` checks on `not result.get("questions")`).
  2. In `track0.py` / `probe.py`, ensure `exception1_personal_loss_8949` starts with an unanswered question (or surfaces the contradicted Exception 1 / sale-closure question) and that its `truthful_answer` state (either by recording the personal loss sale or correcting the contradicted answer) reaches the 2025-instruction hand values in `track0.HAND`.
  3. In `sd_sale_beside_8949_yes` and `codeb_sale_beside_8949_yes`, include the truthful `PATH_B = "no"` answer in `truthful_answer` (or include `form1040.line-7a` and `form1040.line-11a` in `track0.HAND` after answering the surfaced questions) so the full return path through Form 1040 line 7a / 11a is verified.

---

### `BNQ-R3` — `rule.schedule-d-line3.v3.json` and `rule.schedule-d-line10.v3.json` ask the Code-B question (`form8949-code-b-in-class`) when there are no Code-B sales, and ask the box C/F question (`form8949-in-class`) when there are only Code-B sales

- **Severity:** `should-fix`
- **Locations:**
  - `packages/content/tax/2025/rule.schedule-d-line3.v3.json:195-202`
  - `packages/content/tax/2025/rule.schedule-d-line10.v3.json:195-202`
- **Reproduction:**
  In `sd_sale_beside_8949_yes.unanswered` (`docs/phases/engine-breadth/milestones/blocked-names-question-evidence/track0-matrix.json:273-320`), the filer has recorded a no-1099-B (box C) sale (`no1099b-sold.source-closure = "yes"`, `form8949-in-class = "yes"`) and has **no** Code-B sales (`code-b-sold.source-closure = "no"`), alongside an earlier `no-form8949-sources = "yes"`.
  Because `value.then.else` in `rule.schedule-d-line3.v3.json:195-202` and `rule.schedule-d-line10.v3.json:195-202` uses a single unconditional `block`:
  ```json
  "else": {
    "code": "DEPENDENCY_ABSENT",
    "missing": [
      "tax.us.2025.schedule-d-boundary.no-form8949-sources",
      "tax.us.2025.schedule-d-boundary.form8949-in-class",
      "tax.us.2025.schedule-d-boundary.form8949-code-b-in-class"
    ],
    "op": "block"
  }
  ```
  the blocked `schedule-d.line-3` and `schedule-d.line-10` fields surface all three questions on the page, including:
  - `"Is every Form 1099-B sale with Form 8949 code B a basic sale..."` (`form8949-code-b-in-class`), even though `code-b-sold.source-closure == "no"` (contradicting `rule.schedule-d-line3.v3.json:16`: `"read only when the code B answer is yes"`), and
  - `"Is every sale you are reporting on Form 8949 without a Form 1099-B (box C or box F) a basic sale..."` (`form8949-in-class`), even though the filer already answered `"yes"`.
  Conversely, in `codeb_sale_beside_8949_yes.unanswered` (where `no1099b-sold.source-closure == "no"` and `code-b-sold.source-closure == "yes"`), it asks the box C/F `form8949-in-class` question alongside `form8949-code-b-in-class`.
- **Fix:**
  Split `value.then.else` in `rule.schedule-d-line3` and `rule.schedule-d-line10` into conditional `choose` branches keyed on `no-form8949-sources == "yes"` (naming `no-form8949-sources`), `no1099b-sold.source-closure == "yes"` with `form8949-in-class != "yes"` (naming `form8949-in-class`), and `code-b-sold.source-closure == "yes"` with `form8949-code-b-in-class != "yes"` (naming `form8949-code-b-in-class`), so only the question relevant to the filer's present sale family and unanswered/contradicted state is named.

---

### `BNQ-R4` — Redundant live runs and wasted fixture-building work across `test_blocked_names_question_v89.py` and `test_blocked_names_question_v89_recorded.py`

- **Severity:** `should-fix`
- **Locations:**
  - `tests/test_blocked_names_question_v89.py:45-85, 133-155`
  - `tests/test_blocked_names_question_v89_recorded.py:58-96`
- **Reproduction:**
  1. **`tests/test_blocked_names_question_v89.py` (30 runs):**
     - Three pairs of runs have **identical effective workspace state** (differing only in act IDs, correction tags, or a duplicate assertion of the same value) and test nothing their sibling does not:
       - `exception1_personal_loss_8949.unanswered` (`probe.py:73-74`) and `exception1_personal_loss_8949.truthful_answer` (`track0.py:165-166`).
       - `sd_amounts_disagree.truthful_answer` (`track0.py:156`) and `amount_corrected.corrected` (`test_blocked_names_question_v89.py:62-63`).
       - `sd_sale_beside_8949_yes.truthful_answer` (`track0.py:154`) and `sd_path_b_unanswered.unanswered` (`probe.py:90`).
     - A fourth pair has **identical tag-normalized workspace state**:
       - `sd_8949_no_unadmitted.truthful_answer` (`track0.py:152`) and `sale_after_form8949_yes.truthful_no` (`test_blocked_names_question_v89.py:46-53`).
     - Two additional `_late_rows` runs — `sale_after_form8949_yes.form8949_yes` (`test_blocked_names_question_v89.py:55`) and `wash_adjustment_after_close.closed` (`test_blocked_names_question_v89.py:80`) — set neither `open: True` nor `hand` and are not in category `"surface"`, so `_run_case_shard` (`lines 105-120`) performs zero assertions on their outputs beyond `outcome == "success"`.
  2. **`tests/test_blocked_names_question_v89_recorded.py` (298 runs, ~11 minutes):**
     - Lines 80-83 call `qw.neighbour_tasks()` (`docs/phases/engine-breadth/milestones/question-wording-evidence/track0.py:801-849`), which builds all 775 act lists across `v83`, `v84`, `v85`, `v82`, and `v81` (including exporting 213 `v81` returns to a temporary directory on disk) and then filters to `item[0].startswith("v83/")`, discarding 477 built lists before any worker starts.
     - Of the 298 `v83/` lists, 264 have zero interaction with the 11 rules modified in v89 (only the 34 blocked-return lists in `docs/phases/engine-breadth/milestones/blocked-names-question-evidence/rerun-repair-output.json` touch any v89 rule change), and 13 groups within `v83/` (accounting for 23 duplicate runs) share identical effective fact/closure states:
       - `['track0/s0/b4_no_sales', 'returns/case/wage_q3_no/recorded']`
       - `['returns/case/a_high/recorded', 'returns/case/late_member_reanswered_yes/recorded']`
       - `['returns/case/a_q3_no_with_member/recorded', 'returns/case/late_member_after_no/recorded']`
       - `['returns/case/b_code_b_v80_route/recorded', 'returns/v80/probe_b_code_b_on_b/recorded']`
       - `['returns/case/x_q3_no_late_both_terms_reanswered/recorded', 'returns/case/x_q3_yes_late_member/recorded', 'returns/case/x_q3_yes_late_member_reanswered/recorded']`
       - `['returns/case/x_shared_transaction_complete/recorded', 'returns/case/x_shared_transaction_missing_g/recorded']`
       - `['returns/v80/carried_duplicate_horizon/recorded', 'returns/v80/carried_wage_unclosed/recorded']`
       - `['returns/v80/v80_c_and_f_same_sale/recorded', 'returns/v80/v80_c_basis_missing/recorded', 'returns/v80/v80_c_code_w_on_gain/recorded', 'returns/v80/v80_c_loss/recorded', 'returns/v80/v80_c_proceeds_missing/recorded', 'returns/v80/v80_c_wash/recorded', 'returns/v80/v80_f_gain/recorded', 'returns/v80/v80_f_holding_mismatch/recorded', 'returns/v80/v80_q2_late_yes_reanswered/recorded', 'returns/v80/v80_q2_late_yes_stale/recorded', 'returns/v80/v80_w_c_amounts_disagree/recorded']`
       - `['returns/v80/v80_c_loss_path_b_unanswered/recorded', 'returns/v80/v80_f_gain_path_b_unanswered/recorded']`
       - `['returns/v80/v80_f_gain_new_ic_no/recorded', 'returns/v80/v80_m_c_new_ic_no/recorded']`
       - `['returns/v80/v80_f_gain_q2_no_with_member/recorded', 'returns/v80/v80_m_c_q2_no_with_member/recorded']`
       - `['returns/v80/v80_m_c_8949_yes_pathb_no/recorded', 'returns/v80/v80_t1_stage3/recorded']`
       - `['returns/v80/v80_t2_stage0/recorded', 'returns/v80/v80_t2_stage1/recorded']`
- **Fix:**
  1. In `tests/test_blocked_names_question_v89.py`, deduplicate by effective workspace state (or share the `track0` cases with `_late_rows`) and add explicit assertions (`hand` or `questions == []`) on the baseline `.form8949_yes` / `.closed` rows if retained.
  2. In `tests/test_blocked_names_question_v89_recorded.py`, call `qw_rerun.tasks(...)` directly instead of `qw.neighbour_tasks()` (avoiding building and discarding the 477 `v81`/`v82`/`v84`/`v85` lists), and scope the live regression slice to the 34 affected `v83/` lists plus a small representative sample of unaffected computing returns.

---

### `BNQ-R5` — `evidence_loader` bypasses in `common.py`, `rerun.py`, and transitive evidence loaders, plus unactivated child-process loads

- **Severity:** `should-fix`
- **Locations:**
  - `docs/phases/engine-breadth/milestones/blocked-names-question-evidence/common.py:46-58`
  - `docs/phases/engine-breadth/milestones/blocked-names-question-evidence/rerun.py:37-49`
  - `tests/test_blocked_names_question_v89.py:34-38, 89, 162`
  - `tests/test_blocked_names_question_v89_recorded.py:59-61, 79, 95`
- **Reproduction:**
  1. `docs/phases/engine-breadth/milestones/blocked-names-question-evidence/common.py:46-58` (`module("bnq_harness", HARNESS)`) and `rerun.py:37-49` (`module("bnq_qw_track0", QW_TRACK0)`) load evidence modules via raw `importlib.util.spec_from_file_location` and write directly to `sys.modules` instead of using `tests/evidence_loader.py`.
  2. `tests/test_blocked_names_question_v89_recorded.py:61, 79` calls `qw_rerun.load_test()` (`docs/phases/engine-breadth/milestones/question-wording-evidence/rerun.py:46-62`) and `qw.neighbour_tasks()` (`docs/phases/engine-breadth/milestones/question-wording-evidence/track0.py:75-92, 815-831`), which use raw `spec_from_file_location` to load `tests/test_f1099b_backup_withholding_v83.py`, `tests/test_f1099b_box7_loss_v84.py`, `tests/test_f1099b_box4_only_v85.py`, and `tests/test_sale_family_audit_v82.py` into `sys.modules` under synthetic names (`qw_p0_rerun_v83_test`, `qw_t0_box7_test`, `qw_t0_box4_test`, `qw_t0_sfa_test`). Because their `__file__` paths are under `tests/` rather than `*-evidence/`, `tests/evidence_loader.py:72-86` (`_is_evidence_module`) returns `False` and `evidence_loader.finish()` leaves all 4 modules permanently in the pytest parent process's `sys.modules`.
  3. Both `tests/test_blocked_names_question_v89.py:89` and `tests/test_blocked_names_question_v89_recorded.py:59-60` call `evidence_loader.load(...)` inside `ProcessPoolExecutor` `spawn` workers where pytest's `conftest.py` item hooks never run (`_active_owner` is `None`).
- **Fix:**
  Route helper module loading in `common.py` and `rerun.py` through `tests/evidence_loader.py`, wrap worker-process execution in `evidence_loader.activate(...)` / `evidence_loader.finish(...)`, and avoid loading `tests/test_*.py` modules into `sys.modules` under ad-hoc names outside `evidence_loader`'s cleanup scope.

---

### `BNQ-R6` — `_apply_covered_flag_block` inspects `EvalBlocked.missing` on every rule block

- **Severity:** `note`
- **Locations:**
  - `packages/derivation/runner.py:2532`
  - `packages/derivation/source_authority.py:268-293`
- **Reproduction:**
  When `_eval_node` raises `EvalBlocked(code, missing)` for `op == "block"`, `packages/derivation/runner.py:2532` (`_record_blocked`) passes `(code, missing)` through `self._apply_covered_flag_block(code, missing)`. If a rule's `block.missing` ever included a family name present in `self.refused_covered_families`, `_apply_covered_flag_block` would rewrite `code` to `"DEPENDENCY_INVALID"` and replace that name with `"BASIS_NOT_REPORTED_ON_COVERED"`. No rule in core `v89` names a covered sale family in `block.missing`.
- **Fix:**
  No change required for core `v89`; if `block.missing` is intended strictly for question-routing target names, consider restricting `_apply_covered_flag_block` to closure/collect-originated blocks or documenting the invariant.

---

## Verdict

**`not ready`** — blocked by:
- **`BNQ-R1`** (`packages/content/tax/2025/rule.form1040-line16.v8.json:534-544`, `packages/derivation/runner.py:3034-3077`, `packages/content/tax/2025/rule.selected-preferential-base.v10.json:920-1105`)
- **`BNQ-R2`** (`docs/phases/engine-breadth/milestones/blocked-names-question-evidence/probe.py:73-74, 86, 94`, `docs/phases/engine-breadth/milestones/blocked-names-question-evidence/track0.py:150-167`, `tests/test_blocked_names_question_v89.py:117-120`)

---

## Re-review (the repair commits, removed at closeout)

- **Reviewed range:** the repair commits (removed at closeout)
- **Controlling decisions:** Decisions 7–12 in `docs/phases/engine-breadth/milestones/blocked-names-question.md`
- **Re-review verdict:** **`ready`**

### Verification of Decisions 7–12 (`BNQ-R1` through `BNQ-R6`)

1. **Decision 7 (`BNQ-R1` — `packages/derivation/evaluator.py:521, 529, 539`, `packages/derivation/runner.py:3054-3060`, `tests/test_blocked_names_question_v89.py:190-224`):**
   - `EvalBlocked` now sets `from_declaring_block = True` only when raised by `op == "block"` (`evaluator.py:521, 539`) and preserves that flag across `_any_recording_later_refs` (`evaluator.py:529`).
   - In `finalize_unattempted` (`runner.py:3054-3060`), when `guard_blocked is not None and guard_blocked.from_declaring_block and guard_blocked.missing`, the runner records the guard's declared `missing` list via `self._record_blocked(rule, guard_access, guard_blocked.category, list(guard_blocked.missing))`. When a `when` guard blocks without declared names (a `v16` or earlier `block`, or a `ref`/`collect` inside `when`), `finalize_unattempted` retains the `requires`-derived `missing` list.
   - Direct coordinator runs on all 4 recorded `v82/*` returns (`v82/m_2a_only_exc1_only2a_no/honest`, `v82/m_empty_exc1_nolosses_no/honest`, `v82/m_empty_exc1_only2a_no/honest`, `v82/t4_s1_removed/honest`) confirm that `form1040.line-16` (along with `form1040.line-20`, `schedule3.line-1`, `schedule3.line-8`, and `form.sch8812.worksheet-a.line-5`) and the page (`result["questions"]`) now name the 4 declared questions (`Q1`, `Q2`, `NO_8949`, `PATH_B`).
   - **Status:** Fixed per Decision 7 (see `BNQ-R7` below on the stated residual for lines 24, 33, and 37).

2. **Decision 8 (`BNQ-R2` — `docs/phases/engine-breadth/milestones/blocked-names-question-evidence/track0.py:47-59, 152, 161`, `tests/test_blocked_names_question_v89.py:145, 168-170, 226-252`):**
   - `tests/test_blocked_names_question_v89.py:145` now checks `if bad:` unconditionally on every claim with hand values, so remaining page questions never excuse a hand-value miss.
   - All Track 1 test cases state the v88 implied age and blindness facts (`age.answered(row["acts"], age.implied(row["acts"]))`).
   - In `track0.py`, `sd_sale_beside_8949_yes` and `codeb_sale_beside_8949_yes` answer `PATH_B = "no"` alongside `NO_8949 = "no"`, and `exception1_personal_loss_8949` records the omitted no-1099-B sale (`add_sale(acts, "no1099b", "st", "resolved-personal-loss")`). Direct coordinator runs confirm all three reach their exact 2025-instruction hand values with `questions = []` (`exception1_personal_loss_8949`: `schedule-d.line-3 = -6000`, `line-7 = -6000`, `line-21 = 3000`, `form1040.line-7a = -3000`, `line-11a = 47000`, `line-16 = 3515`, `line-24 = 3515`; `sd_sale_beside_8949_yes`: `schedule-d.line-3 = -6000`, `form1040.line-7a = -3000`, `line-11a = 47000`; `codeb_sale_beside_8949_yes`: `schedule-d.line-1b = 6000`, `form1040.line-7a = 6000`, `line-11a = 56000`).
   - **Status:** Fixed per Decision 8.

3. **Decision 9 (`BNQ-R3` — `docs/phases/engine-breadth/milestones/blocked-names-question-evidence/prototype.py:147-161`, `packages/content/tax/2025/rule.schedule-d-line3.v3.json:195-363`, `packages/content/tax/2025/rule.schedule-d-line10.v3.json:195-363`):**
   - `applicable_boundary_block()` replaces the single 3-name block in `value.then.else` with conditional `choose` branches naming `no-form8949-sources` when `no-form8949-sources == "yes"`, `form8949-in-class` when `no1099b-sold.source-closure == "yes"` and `form8949-in-class != "yes"`, and `form8949-code-b-in-class` when `code-b-sold.source-closure == "yes"` and `form8949-code-b-in-class != "yes"`.
   - Direct coordinator runs confirm `sd_sale_beside_8949_yes.unanswered` now asks only `no-form8949-sources` (no Code-B question and no already-answered `form8949-in-class`), and `codeb_sale_beside_8949_yes.unanswered` asks only `no-form8949-sources` and `form8949-code-b-in-class` (no box C/F `form8949-in-class` question).
   - All 11 `v17` rules match `prototype.py`'s build and `published-packages.v87.json` / `demo.release.sli-worksheet-integration.2025.v87.json` checksums.
   - **Status:** Fixed per Decision 9.

4. **Decision 10 (`BNQ-R4` — `tests/test_blocked_names_question_v89.py:62-99`, `tests/test_blocked_names_question_v89_recorded.py:89-105`):**
   - `_late_rows` drops the 4 duplicate/assertion-free rows (`sale_after_form8949_yes.form8949_yes`, `sale_after_form8949_yes.truthful_no`, `amount_corrected.corrected`, `wash_adjustment_after_close.closed`), reducing `test_track0_authority_matrix_late_and_surface_on_v89` from 30 to 26 distinct digests, while the two pairs that previously collided (`exception1_personal_loss_8949` and `sd_sale_beside_8949_yes.truthful_answer`) are now distinct states after the `BNQ-R2` repair. (`test_named_cases_reach_instruction_hand_values` re-runs 3 `.truthful_answer` cases in process; non-blocking.)
   - `test_blocked_names_question_v89_recorded.py:89-105` calls `qw_rerun.tasks(...)` directly instead of `qw.neighbour_tasks()`, avoiding building and exporting the 477 non-`v83/` act lists.
   - **Status:** Fixed per Decision 10.

5. **Decision 11 (`BNQ-R5` — `docs/phases/engine-breadth/milestones/blocked-names-question-evidence/common.py:45-50`, `rerun.py:36-41`, `tests/test_blocked_names_question_v89.py:105-110`, `tests/test_blocked_names_question_v89_recorded.py:59-68, 90`):**
   - `common.py` and `rerun.py` load evidence modules through `tests.evidence_loader.load`.
   - Worker shards in both test modules wrap execution in `evidence_loader.activate(owner)` / `evidence_loader.finish(owner)`, and `test_blocked_names_question_v89_recorded.py` imports `tests.test_f1099b_backup_withholding_v83` as a normal package module instead of calling `qw_rerun.load_test()`, eliminating the 4 synthetic `qw_*_test` modules from `sys.modules`.
   - **Status:** Fixed per Decision 11.

6. **Decision 12 (`BNQ-R6`):**
   - Remains a `note` as decided.

---

### Evaluation of the Stated Residual on the 4 `v82/*` Returns

#### `BNQ-R7` — On the 4 recorded `v82/*` returns (`m_2a_only_exc1_only2a_no`, `m_empty_exc1_nolosses_no`, `m_empty_exc1_only2a_no`, `t4_s1_removed`), `form1040.line-16` and the page name 4 questions, while `form1040.line-24`, `line-33`, and `line-37` (and `line-7a`..`line-15`) remain blocked with `questions: []` because `capital-gains.selected-preferential-base` is `inapplicable`

- **Severity:** `note`
- **Locations:**
  - `packages/content/tax/2025/rule.selected-preferential-base.v10.json:920-1105`
  - `packages/derivation/presentation_projection.py:578-609`
  - `tests/test_blocked_names_question_v89.py:190-224`
- **Coordinator reproduction and analysis:**
  Running the production coordinator (`track0.run` / `live_coordinate_run`) on core `v89` for all 4 `v82/*` returns (`v82/m_2a_only_exc1_only2a_no/honest`, `v82/m_empty_exc1_nolosses_no/honest`, `v82/m_empty_exc1_only2a_no/honest`, `v82/t4_s1_removed/honest`) with `f1099b.no-sale-box4-present = "no"`, `taxpayer-over-65 = False`, and `taxpayer-blind = False` shows:
  1. **Why those 4 returns are in that state:**
     In all 4 returns, every Form 1099-B and Form 8949 sale family is closed empty (`noncovered-sold.source-closure = "no"`, `no1099b-sold.source-closure = "no"`, `code-b-sold.source-closure = "no"`, `no-form8949-sources = "yes"`, covered/code-W families closed empty), while an Exception 1 answer is `"no"` (`exception1.only-box2a-capital-gains = "no"` on `m_2a_only_exc1_only2a_no`, `m_empty_exc1_only2a_no`, and `t4_s1_removed`; `exception1.no-capital-losses = "no"` on `m_empty_exc1_nolosses_no`). As `docs/phases/engine-breadth/milestones/sale-family-audit-evidence/track0.py:505, 507, 536, 780` documents, a negative Exception 1 answer beside zero recorded sales is either an untruthful Exception 1 answer (`"answered no (false: Exception 1 holds)"`), a leftover answer after removing a mistake sale (`t4_s1_removed`), or a truthful Exception 1 answer by a filer who has a capital gain/loss sale not yet entered (the `exception1_personal_loss_8949` scenario).
  2. **Why `form1040.line-16` names questions while `form1040.line-24`, `line-33`, and `line-37` have `questions: []`:**
     - `form1040.line-16` (`rule.form1040-line16.v8.json`) raises a declaring `when`-guard block in `finalize_unattempted` with `missing = ["f1099b.noncovered-sold.source-closure", "f8949.no1099b-sold.source-closure", "schedule-d-boundary.no-form8949-sources", "schedule-d-boundary.no-other-form8949-adjustments"]`. Those 4 questions appear on `form1040.line-16`, `form1040.line-20`, `schedule3.line-1`, `schedule3.line-8`, `form.sch8812.worksheet-a.line-5`, and at the page level (`result["questions"]`).
     - In contrast, `form1040.line-7a` requires `capital-gains.selected-preferential-base`, whose producer (`rule.selected-preferential-base.v10.json:920-1105`) evaluates its `when` guard to `False` (`inapplicable`) when `schedule-d-required.conclusion == "yes"` and all 10 sale family counts are `0`. Because `form1040.line-7a` feeds `income.total-income` (`line-9`) -> `income.agi` (`line-11a/11b`) -> `ctc.form1040-line19` (`line-19`) -> `form1040.tax-after-credits` -> `form1040.line-24` -> `form1040.line-33` / `line-37`, every field along that chain has `capital-gains.selected-preferential-base` (disposition `inapplicable`, not a question target) among its leaf roots, so `presentation_projection.py:578-609` (`_all_roots_resolved`) suppresses field-level `reasons` and `questions` (`questions: []`) on those 22 rows.
  3. **Is this a dead end for a truthful filer (does answering the page's questions unblock them)?**
     - **For a truthful filer whose Exception 1 `"no"` reflects an unentered sale** (the only case in which a truthful filer with no currently recorded sales answers `"no"` to `only-box2a-capital-gains` or `no-capital-losses`): answering the page's surfaced sale question (`f8949.no1099b-sold.source-closure = "yes"`, `no-form8949-sources = "no"`, `no-other-form8949-adjustments = "no"`, `form8949-in-class = "yes"`) and recording that sale makes `no1099b-st-count > 0`, which makes `capital-gains.selected-preferential-base` applicable and **unblocks every line on all 4 returns**, computing `form1040.line-7a = -3000`, `form1040.line-16 = 3515`, `form1040.line-24 = 3515`, `form1040.line-33 = 4500`, and `form1040.line-37 = 0` with `questions = []`.
     - **For a filer with no sale to enter** (who answered Exception 1 `"no"` falsely, or removed a mistake sale in `t4_s1_removed` without updating Exception 1): re-answering only `NO_8949` and `PATH_B` in any of the 4 `(yes/no, yes/no)` combinations while leaving `Q1 = "no"`, `Q2 = "no"` and `exception1.* = "no"` leaves `form1040.line-7a`, `line-16`, `line-24`, `line-33`, and `line-37` blocked; unblocking a zero-sale return requires changing the contradicted `exception1.*` answer to `"yes"` (which computes `form1040.line-16 = 3875`, `line-24 = 3875`).
  4. **Why this is `note` (not `blocking` or `should-fix`):**
     - On all 4 returns, the page (`result["questions"]`) and `form1040.line-16` are no longer silent, and a truthful filer whose Exception 1 `"no"` reflects an unentered sale unblocks lines 24, 33, and 37 by answering the page's sale question and entering the sale.
     - Turning `capital-gains.selected-preferential-base` from `inapplicable` into a named block when `schedule-d-required.conclusion == "yes"` beside empty closed sale families (and surfacing the contradicted Exception 1 questions on `line-7a`..`line-15` and `line-24`/`line-33`/`line-37`) requires a successor to `rule.selected-preferential-base.v10.json`, which is outside the 11-rule scope of `blocked-names-question`. (Also note that `tests/test_blocked_names_question_v89.py:218-221` checks only that `line-24`, `line-33`, and `line-37` are present in `blocked`, not that they carry field-level `questions`, despite the test function's name.)
- **Fix:**
  No change required for this milestone; consider a follow-up on `rule.selected-preferential-base` so that an empty-sales + `schedule-d-required.conclusion == "yes"` state blocks naming the Exception 1 / sale-closure questions rather than evaluating `selected-preferential-base` to `inapplicable`.
