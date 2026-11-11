# Review: live harness isolation

Reviewed `github/main..541070bc` on `milestone/live-harness-isolation-2025`.
Object: the per-owner loader, the twenty moved test modules, the guard, and
`tests/conftest.py`. One worker (`-o addopts='' -p no:xdist`) for every run
below. No push, no spawn.

The box takes an evidence file and the test module that loads it. It may
publish a private module object for that owner and a restored `packages`
attribute when the owner is parked, released, or finished. `packages.*` and
`tests.*` stay shared. Published packages, schemas, fixture bytes, case
assertions, and the fast-lane budget stay as they were. A result on one
worker must not depend on which other test module ran before it.

## Findings

### 1. `exec` of an evidence file skips the guard and the restore

- Severity: should-fix.
- File: `docs/phases/engine-breadth/milestones/live-harness-isolation-evidence/inventory.py:594`; `tests/test_evidence_loader.py:193`; `tests/evidence_loader.py:433`.
- Claim: Decision 4. A test module that loads an evidence file by path outside the loader fails the guard, and a `packages` write from that load is restored when the owner finishes.

`_note_call` records `spec_from_file_location`, `import_module`, `run_path`, and a `sys.path` insert. It has no branch for `exec`. The guard only fails a direct load the inventory emitted (`test_evidence_loader.py:193`). `_record` stores a `packages` write only when some frame's filename is an evidence path (`evidence_loader.py:433`). `exec` of source text runs under the filename `<string>`.

Reproduction, scratch repository, same predicate the guard uses. A test module whose body is only:

```python
from pathlib import Path
path = Path("docs/phases/demo-evidence/probe.py")
exec(path.read_text(encoding="utf-8"))
```

leaves the miss list empty. The same predicate reports a miss for each of these bodies:

- `importlib.util.spec_from_file_location("probe", "docs/phases/demo-evidence/probe.py")` followed by `exec_module`
- `runpy.run_path("docs/phases/demo-evidence/probe.py")`
- `sys.path.insert` of the evidence directory, then `import probe`

Runtime, after `load` has armed `packages` modules (the session state once any harness has loaded). `exec` of `loader._lhi_exec = "x"` on `packages.tax.loader` leaves the attribute set after `release`. The same source compiled with the evidence file's path as its filename is restored by `release`. No test module contains `exec(`.

Consequence: a later test can load a harness by `exec` and leak a `packages` attribute across modules on the worker, and the guard stays green. Evidence and compatibility risk for the isolation claim. The loads that exist today are unaffected: the real-tree miss list and unrestored-unrestorable list are both empty.

Fix: in `_note_call`, treat `exec` of a read of an evidence `.py` path as a non-loader load, so `test_in_process_evidence_loads_use_the_loader` fails. Keep snapshotting tied to evidence frames so a test's own `packages` patch still sticks.

### 2. Ten spec-construction asserts were removed

- Severity: note.
- File: the `evidence_loader.load(...)` call that replaced each `spec_from_file_location` block. The removed line in each file was `assert spec is not None and spec.loader is not None`.
- Files: `tests/test_code_b_sales_v81.py`, `tests/test_code_b_sales_v81_package.py`, `tests/test_credit_line_explanations.py`, `tests/test_f1099b_backup_withholding_v83.py`, `tests/test_f1099b_backup_withholding_v83_package.py`, `tests/test_f1099b_box4_only_v85_package.py`, `tests/test_f1099b_box7_loss_v84_package.py`, `tests/test_no1099b_sales_v80.py`, `tests/test_sale_family_audit_v82.py`, `tests/test_sale_family_audit_v82_package.py`.

Those ten lines are the only `assert`, `parametrize`, marker, `skip`, or `xfail` lines that differ from `github/main` in the twenty modules. A missing spec now raises `ImportError` from `tests/evidence_loader.py:147`. Case assertions are unchanged.

`raise RuntimeError(...)` on a missing spec was also removed, where that was the old load failure, from `tests/test_all_questions_at_once.py`, `tests/test_child_tax_credit_track1.py`, `tests/test_closure_question_coverage.py`, `tests/test_earned_income_credit_track1.py`, `tests/test_other_dependents_credit_track1.py`, `tests/test_statement_withholding_pairing.py`, and `tests/test_tax_on_taxable_income_track1.py`.

Fix: keep the loader's `ImportError`. No case assertion has to come back.

### 3. Reactivating a parked owner discards a later non-owner write

- Severity: note.
- File: `tests/evidence_loader.py:83` (`release`) and `tests/evidence_loader.py:457` (`_show`); wired by `tests/conftest.py:202`.

Reproduction. Owner A loads a harness that sets `packages.tax.loader._lhi_park`. `release` clears it. A direct assignment then sets the same attribute to another value. `activate` of A puts A's harness value back. The following `release` removes the attribute, so the intervening value is gone.

No test module assigns the fourteen snapshotted targets below. The coupling shows up only for a later writer of one of those names. `pytest_runtest_setup` (`tests/conftest.py:205`) re-binds the same module the module fixture binds. Pytest 9.1.1 runs that hook and the test in one context. Each xdist worker is its own process.

Fix: on `release`, if the live value is neither the baseline nor this owner's stored value, leave it and treat it as the new baseline.

## Checks

### 1. No weakened case assertion

`git diff github/main..541070bc` for the twenty modules named in `live-harness-isolation-evidence/p0.md`. Each evidence `spec_from_file_location` or bare `import_module` became `evidence_loader.load` of the same path. Representative hunk (`tests/test_all_questions_at_once.py`):

```diff
 def _load_probe() -> Any:
-    spec = importlib.util.spec_from_file_location("all_questions_probe", _PROBE_PATH)
-    if spec is None or spec.loader is None:
-        raise RuntimeError("question-round probe failed to load")
-    module = importlib.util.module_from_spec(spec)
-    spec.loader.exec_module(module)
-    return module
+    return evidence_loader.load(_PROBE_PATH, "all_questions_probe")
```

The other modules match that shape, with these differences:

- `tests/test_noncovered_sales_v79.py` still inserts the evidence directory on `sys.path`. The four `import_module` calls (`p0b`, `probe`, `prototype`, `track0`) are now `evidence_loader.load` of those four files.
- `tests/test_f1099b_box4_only_v85.py` and `tests/test_f1099b_box7_loss_v84.py`: `load_track0` uses the loader. The repo-root `sys.path.insert` that lived inside `_module` is now in `load_track0`. `_module` still loads `tests/test_f1099b_backup_withholding_v83.py` by `spec_from_file_location`. That path is a test, and the guard's evidence miss list does not include it.
- `tests/test_f1099b_backup_withholding_v83.py` and `tests/test_sale_family_audit_v82.py` moved the same repo-root insert out of the cache-miss branch. The condition is unchanged.
- `tests/test_f1099b_backup_withholding_v83.py:118` and `tests/test_sale_family_audit_v82.py:298` still run `export_v81_returns.py` in a subprocess. The inventory marks both `isolated=True`, so the guard leaves them. They are the two direct evidence loads whose mechanism is `subprocess`.

No module dropped a harness. `packages/`, schema files, and fixture files are absent from the diff. `FAST_LANE_BUDGET_SECONDS` is still `3.0` (`tests/conftest.py:51`); the diff does not touch it.

### 2. Isolation is real

One process. Two owners load one scratch `probe.py` that imports `sibling` and calls `importlib.import_module("sibling")`.

- The two `probe` objects differ. One owner reloads the same object.
- Assigning `VALUE` on A's `probe` and A's `sibling` leaves B's values as the text the file set.
- `packages.tax.loader` and `tests.evidence_loader` are the same objects for both owners.
- The interpreter module dict does not hold either owner's `probe` or `sibling`.

The same run loads the real `f8949-code-b-evidence/codeb_prototype.py` twice. The module objects differ. `companion_v81` on A replaces `domain_package_companion_declarations` and sets `_codeb_patched`. Activating B restores the original callable and clears the flag. B's `companion_v81` installs a different callable. Activating A puts A's callable and flag back.

`tests/test_evidence_loader.py` and `tests/test_code_b_sales_v81_package.py`, one worker: 34 passed in 21.83s. That includes `test_two_owners_get_different_objects`, `test_nested_bare_import_resolves_to_the_owners_copy`, and `test_datetime_strptime_imports_while_an_owner_is_active`.

The child-binding fix (`_is_submodule_binding`) leaves `packages.tax.loader` on its parent across `release`. The sentinel that the harness wrote on that module is hidden while parked and removed by `finish`. Evidence module objects stay per owner. The interpreter-dict mirror does the same: shared modules stay visible to `datetime.strptime`, evidence copies stay out of that dict.

### 3. Restore is exact

The real-tree guard reports zero unrestored writes the loader refuses. The fourteen reached targets, all attribute stores:

| File | Line | Target |
| --- | --- | --- |
| `f8949-boxes-cf-evidence/cf_prototype.py` | 801 | `loader.domain_package_companion_declarations` |
| `f8949-boxes-cf-evidence/cf_prototype.py` | 802 | `loader.named_covered_flag_refusal_maps` |
| `f8949-boxes-cf-evidence/cf_prototype.py` | 803 | `loader._cf_patched` |
| `f8949-code-b-evidence/codeb_prototype.py` | 1007 | `loader.domain_package_companion_declarations` |
| `f8949-code-b-evidence/codeb_prototype.py` | 1008 | `loader.named_covered_flag_refusal_maps` |
| `f8949-code-b-evidence/codeb_prototype.py` | 1009 | `loader._codeb_patched` |
| `noncovered-sales-evidence/p0b.py` | 101 | `proto.loader.domain_package_companion_declarations` |
| `noncovered-sales-evidence/p0b.py` | 373 | `marshal_mod.marshal_closure_authority` |
| `noncovered-sales-evidence/p0b.py` | 374 | `runner_mod.resolve_closure_admissions` |
| `noncovered-sales-evidence/p0b.py` | 375 | `runner_mod._Run._record_blocked` |
| `noncovered-sales-evidence/p0b.py` | 376 | `presentation_mod._closure_question_reasons` |
| `noncovered-sales-evidence/p0b.py` | 377 | `live_mod.live_coordinate_run` |
| `noncovered-sales-evidence/prototype.py` | 703 | `loader.domain_package_companion_declarations` |
| `noncovered-sales-evidence/track0.py` | 113 | `proto.loader.domain_package_companion_declarations` |

Paths are under `docs/phases/engine-breadth/milestones/`. The code-b triple was executed across two owners; `release` restored the original callable, the original map, and cleared `_codeb_patched`. The class-attribute shape is `test_class_attribute_is_restored_when_the_owner_finishes`, which passed in the 34.

A scratch harness that sets a sentinel and then raises leaves the attribute in place until teardown. `activate` of the next owner clears it. `release` clears it. `finish` clears it. On the real conftest fixtures, a test that loaded such a harness and raised, then a test in the next module: 1 failed, 1 passed. The second module saw the attribute gone. That is `tests/conftest.py:202` running after the failure.

In-memory mutation of a clean report, appending `loader.cache[]` and `loader.add()`, makes the guard predicate return both. A scratch harness that executes `loader.cache['k'] = 1`, reached through `evidence_loader.load`, produces the bare target `loader.cache[]`.

### 4. Guard

Covered by finding 1. `spec_from_file_location`, `runpy.run_path`, and `sys.path.insert` plus `import probe` each fail the predicate on a scratch copy. `exec` does not. The committed tree's own guard test passed inside the 34: zero evidence direct-loads outside the loader except the two isolated subprocess exports, and zero unrestorable writes.

### 5. Hidden coupling

The two fixes do not put one owner's harness object into the other owner's map or into the interpreter dict. Measurements are in check 2. `tests/conftest.py` is process-local. Finding 3 is the remaining order coupling, and no current test writes those attributes from the test module.

### 6. Cost

`tests/test_code_b_sales_v81_package.py` alone, one worker: 23 passed in 0.28s. Slowest setup 0.21s. That is the fast module Decision 2 kept in-process. The loader's unit tests are in the 34 and are unmarked except `test_in_process_evidence_loads_use_the_loader`, which is `pytest.mark.live` because the scan exceeds the 3.0s budget. That test scans source. It does not repeat a `live_coordinate_run`. The fast-lane budget is unchanged.

### 7. Data safety

`python3 tools/envelope_scan.py --range github/main..HEAD` exited 0.

## Verdict

ready

Blocking list: none. Finding 1 is the repair to take before relying on the guard as a complete pin.
