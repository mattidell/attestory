# Review: parallel recorded-return replay (`parallel-replay`)

Reviewer: fresh reader, author-independent.
Charter: `docs/reviews/parallel-replay/charter-review.md`.
Object: `milestone/parallel-replay-2025` at `80aab2624fcc11888967adfc456311dec6ebc16d`, diffed against `github/main` (`080d2758`, 0 behind, 6 ahead; branch is not spent).
The Orientation Block SHA (`80aab2624fcc11888967adfc456311dec6ebc16d`) matches `git rev-parse HEAD`.
Sources read: `docs/phases/engine-breadth/milestones/parallel-replay.md`, `docs/reviews/parallel-replay/charter-track1.md`, `tools/recorded_replay.py`, `tests/test_recorded_replay.py`, `docs/phases/engine-breadth/milestones/parallel-replay-evidence/compare_neighbour.py`, `docs/phases/engine-breadth/milestones/parallel-replay-evidence/equivalence.json`, `docs/phases/engine-breadth/milestones/question-wording-evidence/track0.py`, `docs/phases/engine-breadth/milestones/question-wording-evidence/rerun.py`, `docs/phases/engine-breadth/milestones/question-wording-evidence/track0-neighbour.json`, `docs/phases/engine-breadth/milestones/question-wording-evidence/rerun-output.json`, `tests/evidence_loader.py`, `tests/conftest.py`, and the referenced test/evidence harnesses (`v82`–`v85`). Governance was not read.

## The box

`tools/recorded_replay.py` gathers the 775 de-duplicated recorded act lists from five committed fixture/evidence sources (`v83`, `v84`, `v85`, `v82`, `v81`), runs a caller-supplied `per_list` function across a `concurrent.futures.ProcessPoolExecutor` with an atomic resumable part file, and provides a `neighbour` subcommand plus `run_neighbour()` to classify pin diffs between two cores. Package, content, schema, engine, kernel, and closed milestones' committed evidence files stay outside and unchanged.

## Findings, ordered by consequence

### F1 (`blocking`). `test_recorded_lists_returns_775_keys_equal_to_committed` hides a ~70 s `recorded_lists()` call in a module fixture to evade the 3.0 s fast-lane budget

- **Where.** `tests/test_recorded_replay.py:37-53`, `tools/recorded_replay.py:142-221`, `docs/phases/engine-breadth/milestones/parallel-replay.md:75-77` (checked against `tests/conftest.py:38-51, 150-171`).
- **Violated claim.** Charter Question 4 ("Do the new tests stay under the fast-lane budget?"), Track 1 charter (`docs/reviews/parallel-replay/charter-track1.md:36`, "`tests/test_recorded_replay.py`, fast lane (under 3.0 s each)"), and `AGENTS.md` ("Test lanes": fast lane `pytest -m "not live"` is ~15 s; `tests/conftest.py` enforces `FAST_LANE_BUDGET_SECONDS = 3.0` and routes `subprocess`-spawning tests to `live`).
- **Reproduction.** Run:
  ```sh
  python3 -c 'import time; from tools import recorded_replay; t0 = time.perf_counter(); lists = recorded_replay.recorded_lists(); print(len(lists), round(time.perf_counter() - t0, 2))'
  ```
  Output: `775 69.88` (69.88 s wall time). `recorded_lists()` calls `test.export_returns(...)` twice (`tools/recorded_replay.py:164, 207`), each spawning a child interpreter (`subprocess.run` on `export_v81_returns.py`) that builds 213 returns, and executes case builders across four Track 0 harnesses (`v83`, `v84`, `v85`, `v82`). Because `tests/test_recorded_replay.py` does not contain the literal string `"subprocess"` in its own source, `tests/conftest.py:56-65` leaves it unmarked (in the fast lane). Because `tests/conftest.py:153` checks only `if report.when != "call": return`, moving `recorded_replay.recorded_lists()` into `@pytest.fixture(scope="module") def all_recorded_lists()` (`tests/test_recorded_replay.py:37-40`, docstring `"Fixture to load recorded lists before test timing."`) shifts the 69.88 s runtime into the untimed `setup` phase so the plan (`parallel-replay.md:77`) reports `< 0.005 s call` while every `pytest -m "not live"` run pays ~70 s.
- **Consequence.** Fast-lane gate and developer inner-loop regression: a single unmarked module multiplies the ~15 s fast lane by ~5x while bypassing `FAST_LANE_BUDGET_SECONDS`.
- **Fix.**
  1. In `tools/recorded_replay.py:163-165, 206-210`, call `test.export_returns(...)` once and reuse the `exported` dict for both `v83` (`test.return_acts(track, exported)` does not mutate `exported`) and `v81`, eliminating one ~25 s subprocess call.
  2. Do not hide a slow call inside a fixture to bypass `report.when == "call"`: mark the full 775-list integration check `@pytest.mark.live` (where `subprocess`-spawning tests belong under `tests/conftest.py:38-46`), and test `recorded_lists()`'s gathering order and SHA-256 de-duplication in the fast lane with stubbed/lightweight inputs that finish under 3.0 s including setup.

### F2 (`blocking`). `replay()` does not bind the part file to the replayed cores or filter to requested keys, so a stale part file from different cores silently corrupts results

- **Where.** `tools/recorded_replay.py:344-348, 370-395`.
- **Violated claim.** Charter Question 2 ("Can the result depend on worker count, finish order, a crash and resume, or a stale part file from a different pair of cores?").
- **Reproduction.** Run:
  ```sh
  python3 -c '
  import json, tempfile
  from pathlib import Path
  from tools import recorded_replay
  with tempfile.TemporaryDirectory() as tmp:
      p = Path(tmp) / "part.json"
      p.write_text(json.dumps({"k1": {"from_cores": "v85_v86"}, "extra_stale": {"from_cores": "v85_v86"}}))
      res = recorded_replay.replay([("k1", [])], ("v86", "v87"), recorded_replay.fake_per_list, workers=1, part=p)
      print(res)
  '
  ```
  Output: `{'extra_stale': {'from_cores': 'v85_v86'}, 'k1': {'from_cores': 'v85_v86'}}`.
  `_write_part()` (`lines 344-348`) writes a flat `{key: result}` JSON mapping with no core or function metadata. `replay()` (`lines 372-380`) loads any existing dict from `part`, skips every `key in found` without checking whether `cores` (or the underlying scratch core files) match, and returns `dict(sorted(found.items()))` (`line 395`), including keys in `part` that were not in `lists`.
- **Consequence.** If a builder reuses a `--part` path after switching core pairs or rebuilding a scratch core during prototype/Track 0 iteration, `replay()` silently returns stale rows from the earlier cores (or a mixture of old and new cores) and leaks any extra keys from the part file into the result.
- **Fix.** Record a core-pair fingerprint in the part file (version, registry, release version, `loader_from`, `presence_pairs`, and SHA-256 digests of `package_path` and `release_path` when resolved to cores), refuse or reset the part file when the fingerprint disagrees with `cores`, and return `{k: found[k] for k, _ in sorted(lists, key=lambda item: item[0])}` so only keys from `lists` are returned.

### F3 (`blocking`). `neighbour_classify_per_list` and `run_neighbour` hard-code `"v86"` for identical-error tracking, dropping `same_error_on_both_cores` on any other baseline core

- **Where.** `tools/recorded_replay.py:260-262, 297-309, 416-418`.
- **Violated claim.** Milestone scope (`docs/phases/engine-breadth/milestones/parallel-replay.md:10`, "one reusable tool replays the recorded act lists earlier milestones replay, on any set of cores").
- **Reproduction.** Run:
  ```sh
  python3 -c '
  from tools import recorded_replay
  pin_err = {"error": "FindingModelError", "message": "bad"}
  row = recorded_replay.classify(pin_err, pin_err, name_a="v87", name_b="v88")
  print("classify row:", row)
  '
  ```
  Output: `classify row: {'class': 'identical'}`.
  When both cores produce the same error pin (83 of the 775 lists on `v86`/`v87`), `left_pin == right_pin` is `True`, so `classify()` (`line 261-262`) returns `{"class": "identical"}` without setting `f"{name_a}_error"`. Then `neighbour_classify_per_list()` (`lines 307-308`) runs:
  ```python
  if "v86_error" not in row:
      row["v86_error"] = pin_a.get("error") if isinstance(pin_a, dict) and core_a.version == "v86" else None
  ```
  When `core_a.version != "v86"` (e.g., `v87` vs `v88`), `row["v86_error"]` is set to `None` and `row[f"{core_a.version}_error"]` is never populated. In `run_neighbour()` (`line 416`), `err = row.get("v86_error") or row.get(f"{core_a.version}_error")` is `None`, so `same_error_on_both_cores` is `{}` (all 83 identical errors vanish), while non-identical rows on non-`v86` cores still get a spurious `"v86_error": null` field. Conversely, if `core_a` errors and `core_b` succeeds (`row["class"] == "numbers_changed"`), `classify()` sets `row[f"{core_a.version}_error"]` (`line 278`) and `run_neighbour()` (`lines 416-418`) erroneously counts it under `same_error_on_both_cores` because it does not check `row["class"] == "identical"`.
- **Consequence.** On the next milestone (`v87` vs `v88`), `recorded_replay.py neighbour v87 <core-v88>` will report `"same_error_on_both_cores": {}` and inject `"v86_error": null` into `changes`.
- **Fix.** Record the baseline error on identical rows under `f"{core_a.version}_error"` (and `"v86_error"` only when `core_a.version == "v86"`, or a core-neutral key), and in `run_neighbour()` (`line 416`) count `same_error_on_both_cores` only when `row["class"] == "identical"`.

### F4 (`blocking`). `"How a milestone uses it"` and `recorded_replay.py` do not support producing both the P0 rerun and Track 0 neighbour diff from one replay or writing a custom `per_list` function

- **Where.** `docs/phases/engine-breadth/milestones/parallel-replay.md:82-89`, `tools/recorded_replay.py:83, 291-337, 398-443`.
- **Violated claim.** Milestone scope (`docs/phases/engine-breadth/milestones/parallel-replay.md:12`, "a milestone's rerun and its Track 0 neighbour diff can share one replay") and Charter Question 5 ("Is 'How a milestone uses it' enough for a builder to run a P0 rerun and a Track 0 neighbour diff from one replay with a new per-list function? Name what is missing.").
- **Reproduction / what is missing.**
  1. **No path from one replay to `rerun-output.json`:** `"How a milestone uses it"` (`parallel-replay.md:84-88`) gives only:
     `python3 tools/recorded_replay.py neighbour <baseline-core> <new-core> --workers N --part <scratch>/part.json --out <scratch>/track0-neighbour.json`
     and claims this produces both the P0 rerun table and the Track 0 neighbour diff. In fact, `run_neighbour()` writes only `track0-neighbour.json`. A P0 rerun (`question-wording-evidence/rerun.py:140-158, 218-251`) is over the 298 `v83/*` lists (with `"v83/"` stripped) and requires `v86_matches_fixture` (comparing the baseline pin against `tests/fixtures/f1099b_backup_withholding_v83/expected.json`) and `restored_present_no`. Because `neighbour_classify_per_list` (`tools/recorded_replay.py:297-309`) discards `pin_a` and `pin_b` inside the worker without checking `expected.json` or storing the pins/fixture-match boolean in `part.json`, `rerun-output.json` cannot be derived from `part.json` or `track0-neighbour.json` without re-running the 298 lists.
  2. **Missing public helpers and contract for a custom `per_list` function:**
     - `_pin_run(test, core, acts, run_id)` (`line 291`) and `_get_test()` (`line 83`) are private, so a builder writing a custom `per_list` function has no public helper in `tools/recorded_replay.py` to execute `(core, acts)` and obtain its pin.
     - `"How a milestone uses it"` does not show how to call `recorded_replay.replay(lists, cores, per_list, workers=..., part=...)` from Python.
     - It does not state that `per_list` must be a module-level importable function (a lambda or closure fails with `PicklingError` when submitted to `ProcessPoolExecutor`) or document the positional signatures `_invoke_per_list` (`lines 312-337`) dispatches: `(key, acts)`, `(key, acts, cores)`, or `(key, acts, *cores)`.
     - It does not document the `core.json` schema required by `resolve_core()` (`lines 115-125`: `version`, `registry`, `release_version`, and optional `content`, `releases`, `loader_from`, `presence_pairs`) when replaying an unpublished scratch core (where the `"vN"` string shorthand `registry = release_version = f"v{N-2}"` under `packages/content/tax/2025` does not apply).
- **Consequence.** A builder following `"How a milestone uses it"` still has to either run the 298 `v83` lists a second time for P0 or read the implementation of `tools/recorded_replay.py` and private helpers to write a custom replay script.
- **Fix.**
  1. Have the per-list replay record (or optionally compute) the `v83` baseline fixture-match and `restored_present_no` flags (or provide a `rerun` subcommand / `summarize_rerun(part_or_results)` helper Alongside `run_neighbour`) so one `--part` file genuinely feeds both `rerun-output.json` and `track0-neighbour.json`.
  2. Export a public `pin_run(core, acts, run_id)` helper in `tools/recorded_replay.py`.
  3. Expand `"How a milestone uses it"` in `docs/phases/engine-breadth/milestones/parallel-replay.md` to show: (a) how one `part.json` produces both `rerun-output.json` and `track0-neighbour.json`, (b) how to write a top-level picklable `per_list(key, acts, cores)` using `pin_run` and pass it to `replay()`, and (c) the `core.json` fields for a scratch core vs a published `"vN"` core string.

### S1 (`should-fix`). `compare_neighbour.py` compares only summary classifications and per-set error totals, not per-list error keys or baseline pins

- **Where.** `docs/phases/engine-breadth/milestones/parallel-replay-evidence/compare_neighbour.py:36-102`.
- **Violated claim.** Charter Question 3 ("Does compare_neighbour.py compare every row that matters, so a wrong replay could not pass?").
- **Reproduction.** In `track0-neighbour.json`, 774 of 775 keys have `"class": "identical"`, and only the 1 non-identical key (`v82/m_empty_exc1_unanswered/honest`) appears in `changes`. Passing `compare()` a crafted `replay_data` that swaps `"v81/case/a_8949_yes"` (a valid return) and `"v81/case/a_corrected_basis_missing"` (a `FindingModelError` return) keeps `classes`, `counts`, `changes`, and `same_error_on_both_cores` identical, so `compare()` returns `"equivalent": true` with `mismatches: []`. Similarly, if a buggy replay evaluated `core_a` against itself on the 774 identical rows, `left_pin == right_pin` would hold and `compare_neighbour.py` would pass. `compare()` also omits checking top-level `runs`, `distinct_lists`, `sets`, and `len(changes)` before indexing `changes` by `row["id"]` (`lines 67-68`).
- **Consequence.** Evidence completeness: `compare_neighbour.py` verifies the summary fields present in `track0-neighbour.json` (except `runs`/`distinct_lists`/`sets`), but cannot detect swapped error keys within a fixture set or identical wrong pins on non-changed rows unless checked against the raw `part.json` (`v86_error` per key) and the `v83` expected fixture pins.
- **Fix.** Check `runs`, `distinct_lists`, `sets`, and ordered `changes` list equality in `compare_neighbour.py`, and add an optional `--part` check that verifies per-key error counts and `v83` fixture pin equality.

### S2 (`should-fix`). `ProcessPoolExecutor` omits `mp_context="spawn"`, and `recorded_lists()` leaves a single active `evidence_loader` owner in the parent and returns a mutable cache list

- **Where.** `tools/recorded_replay.py:155-221, 384` (and `tests/evidence_loader.py:131-138`).
- **Violated claim.** Charter Question 4 ("Do worker processes share any module state with the parent or each other that a live evidence harness writes (see tests/evidence_loader.py)?").
- **Reproduction.** In `recorded_lists()`, line 161 calls `test.track0()`, which invokes `evidence_loader.load(...)`, replaces `sys.modules` with `evidence_loader._Modules`, and calls `evidence_loader.activate("rr_v83_test")` without ever calling `evidence_loader.release("rr_v83_test")`. Because `evidence_loader.load` checks `chosen = owner if owner is not None else _owner.get()` (`tests/evidence_loader.py:131`), the subsequent loads of `v84` (`line 182`), `v85` (`line 191`), and `v82` (`line 201`) in `recorded_lists()` all bind to the same owner `"rr_v83_test"`. On macOS, `multiprocessing.get_start_method()` defaults to `"spawn"`, so worker processes start fresh and do not inherit parent module state; on Linux (`ubuntu-latest` CI runs Python 3.13, where the default start method is `"fork"`), `ProcessPoolExecutor(max_workers=max_workers)` (`line 384`) forks workers from the parent after `recorded_lists()` has mutated `sys.modules` and populated `evidence_loader` state. In addition, `recorded_lists()` returns `_RECORDED_LISTS_CACHE` directly (`lines 155, 221`), so in-place caller mutation mutates the process cache.
- **Consequence.** Cross-platform worker isolation risk on Linux (`fork`) and in-process cache mutation if a caller modifies returned `(key, acts)` lists.
- **Fix.** Pass `mp_context=multiprocessing.get_context("spawn")` to `ProcessPoolExecutor` in `tools/recorded_replay.py:384`, release `evidence_loader` owners after each harness load in `recorded_lists()`, and return a shallow copy (or tuple) from `recorded_lists()`.

### N1 (`note`). `_write_part()` does not run `_check_no_local_paths()`

- **Where.** `tools/recorded_replay.py:344-348, 351-354, 440`.
- **What was measured.** `run_neighbour()` checks `_check_no_local_paths(text, str(out_path))` before writing `--out` (`line 440`), and `neighbour_classify_per_list` scrubs paths via `test.pin()`. However, `_write_part()` (`lines 344-348`) writes `part_path` without calling `_check_no_local_paths()`, so a custom `per_list` function that accidentally returned an unredacted path would write it to `part.json`.
- **Fix.** Call `_check_no_local_paths(text, str(part_path))` inside `_write_part()` before writing `tmp`.

## Answers to the six charter questions

1. **Same lists (`recorded_lists()` vs `neighbour_tasks()`).**
   Verified by direct execution in a fresh process: `recorded_replay.recorded_lists()` and `question-wording-evidence/track0.py`'s `neighbour_tasks()` both return 775 `(key, acts)` tuples, with identical keys in the exact same order and byte-identical `acts` (`recorded_lists() == neighbour_tasks()` is `True`). Both read the exact same inputs (`tests/fixtures/f1099b_backup_withholding_v83/expected.json`, `docs/phases/engine-breadth/milestones/f1099b-box4-only-evidence/track0-neighbour.json`, `tests/test_f1099b_backup_withholding_v83.py`, `docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py`, `tests/test_f1099b_box7_loss_v84.py`, `tests/test_f1099b_box4_only_v85.py`, `tests/test_sale_family_audit_v82.py`, and their underlying Track 0 harnesses and `export_v81_returns.py`) and de-duplicate by `sha256(json.dumps(acts, sort_keys=True))`. Neither reads any file or input the other did not.
2. **Independence from scheduling and part-file integrity.**
   For fixed cores and a clean or matching part file, output is independent of worker count, completion order, and crash/resume because `replay()` returns `dict(sorted(found.items()))` (`tools/recorded_replay.py:395`) and `run_neighbour()` sorts all output maps and change rows (`lines 420, 431-434`). `_write_part()` (`lines 344-348`) writes `<part.name>.tmp` and replaces `part_path` via `Path.replace()`, so an interrupted write cannot corrupt the previous part file. However, `replay()` is **not** independent of a stale part file from a different pair of cores or a different list set (**F2**).
3. **Equivalence evidence (`compare_neighbour.py`, `equivalence.json`, and 10-list spot check).**
   - **Spot check:** 10 lists across all five sets (`v81/case/a_8949_yes`, `v81/case/a_adjustment_row_missing`, `v82/m_empty_exc1_only2a_no/honest`, `v82/m_empty_exc1_unanswered/honest`, `v83/returns/case/a_8949_yes/recorded`, `v83/track0/s0/b4_yes_covered`, `v84/authority/alc_closed_empty`, `v84/authority/alc_count_two`, `v85/authority/alc_double_count`, `v85/authority/alc_present_no`) were replayed from scratch on `v86` and `v87` with `--workers 2` (76.04 s for the 10-list batch). Every row matched `question-wording-evidence/track0-neighbour.json` with 0 mismatches, including the 40-item `sentence_fields` list on `v82/m_empty_exc1_unanswered/honest`.
   - **`compare_neighbour.py` coverage:** It compares `classes`, `changes` (by `id`), `counts`, and `same_error_on_both_cores`, which is sufficient to verify equality against `track0-neighbour.json`'s stored summary fields, but could pass a wrong replay that produced identical wrong pins on both cores on the 774 `"identical"` lists or swapped erroring keys within the same set (**S1**).
4. **Isolation (`tests/evidence_loader.py` and fast-lane budget).**
   - **Worker state:** On macOS (`spawn` start method), each worker starts a fresh process, loads `rr_v83_test` on demand, and scopes `packages.tax.loader` companion/refusal overrides inside `with track.h.loader_entries(core):` (`tools/recorded_replay.py:293`; `audit_harness.py:87-112`), so workers share no harness-written module state with the parent or each other. On Linux (`fork` default in Python 3.13), `ProcessPoolExecutor` without `mp_context="spawn"` inherits the parent's `evidence_loader` state after `recorded_lists()` (**S2**).
   - **Fast-lane budget:** `test_recorded_lists_returns_775_keys_equal_to_committed` does **not** stay under the 3.0 s fast-lane budget; its `all_recorded_lists` fixture takes 69.88 s and bypasses `tests/conftest.py:153` solely because `pytest_runtest_makereport` only checks `report.when == "call"` (**F1**).
5. **Use by a milestone ("How a milestone uses it").**
   Not sufficient as written (**F3**, **F4**): running `recorded_replay.py neighbour ...` produces only `track0-neighbour.json` (not `rerun-output.json` with `v86_matches_fixture` and `restored_present_no`), drops `same_error_on_both_cores` whenever `core_a.version != "v86"`, leaves `_pin_run` private, and omits the Python `replay()` API, `per_list` picklability/signature requirements, and the scratch `core.json` format.
6. **Data safety and mechanical gates.**
   - `python3 tools/envelope_scan.py --range github/main..HEAD` exited 0 (clean).
   - `python3 -m mypy` exited 0 (`Success: no issues found in 486 source files`).
   - `python3 tools/governance_lint.py` exited 0 (`governance lint: conformant`).
   - No absolute or temp-directory paths appear in the committed files or in this review.

## Verdict

Blocking list: **F1, F2, F3, F4**.

The equivalence result on `v86` vs `v87` (`docs/phases/engine-breadth/milestones/parallel-replay-evidence/equivalence.json`) and the 775-list gathering equivalence in `recorded_lists()` are verified and can be preserved across the repair.

## Re-review (`dd90f0dc..f8907298`)

Object: repair commits `dd90f0dc..f8907298` at `HEAD` (`f8907298c0a2ec770349ec23b46a4fa306b116d5`), checked against Decisions 1–7 in `docs/phases/engine-breadth/milestones/parallel-replay.md:171-195` and `docs/reviews/parallel-replay/charter-repair.md`.

### Verification of Decisions 1–7

1. **F1 (Decision 1) — closed.** `test_recorded_lists_returns_775_keys_equal_to_committed` (`tests/test_recorded_replay.py:37-49`) is now marked `@pytest.mark.live` with the measured runtime reason and no longer hides `recorded_lists()` inside an untimed module fixture. `recorded_lists()` (`tools/recorded_replay.py:164-166, 207-209`) also invokes `test.export_returns(...)` once and reuses `exported` for both `v83` and `v81`. All 6 unmarked fast-lane tests in `tests/test_recorded_replay.py` run on synthetic list sets in 0.54 s total.
2. **F2 (Decision 2) — closed.** `core_fingerprint()` (`tools/recorded_replay.py:376-399`) records `version`, `registry`, `release_version`, `loader_from`, `presence_pairs`, `package_sha256`, and `release_sha256`. `_write_part()` (`lines 402-406`) writes `{"_metadata": {"cores": ...}, "results": ...}`, `replay()` (`lines 440-457`) raises `ValueError` when a part file's core fingerprint disagrees with the requested cores (or lacks core metadata when cores are specified), and `replay()` (`lines 477-478`) filters its return value to `requested_keys`. Verified by `test_stale_part_file_for_different_cores_is_refused` and `test_resume_skips_keys_in_part_file` (`tests/test_recorded_replay.py:74-126`).
3. **F3 (Decision 3) — closed.** `classify()` (`tools/recorded_replay.py:270-280`) records `res["error"] = err` and `res[f"{name_a}_error"] = err` whenever `left_pin == right_pin` and `err is not None` for any baseline version `name_a` (setting `v86_error` only when `name_a == "v86"`), and `run_neighbour()` (`lines 499-502`) increments `same_error_on_both_cores` only when `row.get("class") == "identical"`. Verified by `test_baseline_other_than_v86_records_identical_errors` (`tests/test_recorded_replay.py:162-170`).
4. **F4 (Decision 4) — closed.** `neighbour_classify_per_list()` (`tools/recorded_replay.py:331-341`) stores `row["pins"] = {core_a.version: pin_a, core_b.version: pin_b}` in the part file (stripped from `changes` in `run_neighbour()` at `line 505`), `summarize_rerun()` (`lines 544-622`) and the `rerun` CLI subcommand (`lines 636-640, 656-675`) derive the P0 rerun table (`rerun-output.json`, including `f"{baseline_version}_matches_fixture"` and `restored_present_no`) from those stored pins without re-running any return, `pin_run()` (`lines 319-325`) and `classify()` (`line 263`) are exposed publicly, and `"How a milestone uses it"` (`docs/phases/engine-breadth/milestones/parallel-replay.md:114-169`) documents both CLI commands, `resolve_core()` core specifications, and a worked top-level `custom_per_list` function. Verified by `test_summarize_rerun_from_replay_pins` (`tests/test_recorded_replay.py:173-186`).
5. **S1 (Decision 5) — closed.** `compare()` (`docs/phases/engine-breadth/milestones/parallel-replay-evidence/compare_neighbour.py:52-112`) checks top-level `sets`, `distinct_lists`, `runs`, `counts`, and `same_error_on_both_cores`, per-key `classes`, exact ordered `changes` list equality, and per-change-row equality. `equivalence.json` was regenerated from a fresh 4-worker replay (`wall_time_s: 2559.48`, `mismatches: []`, `equivalent: true`).
6. **S2 (Decision 6) — closed.** `replay()` (`tools/recorded_replay.py:465-466`) passes `mp_context=multiprocessing.get_context("spawn")` to `ProcessPoolExecutor`, `recorded_lists()` (`lines 212-219`) releases any active `evidence_loader` owner, and `recorded_lists()` (`lines 156, 230`) returns a shallow copy `list(...)`.
7. **N1 (Decision 7) — closed.** `_write_part()` (`tools/recorded_replay.py:408`) calls `_check_no_local_paths(text, str(part_path))` before writing `<part.name>.tmp`.

### Mechanical gates and regressions

- No regressions or new findings were introduced by `dd90f0dc..f8907298`.
- `python3 -m mypy` exited 0 (`Success: no issues found in 486 source files`).
- `python3 tools/governance_lint.py` exited 0 (`governance lint: conformant`).
- `python3 tools/envelope_scan.py --range github/main..HEAD` exited 0.

### Re-review verdict

ready

