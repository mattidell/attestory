# Track 5c — review record

- **Independent review, round 1:** sonnet sub-agent, fresh context, read-only, 2026-09-24. **Verdict: pass
  with notes.** The reviewer reverted `live.py` and `subject_dispatch.py` to HEAD and re-ran the new and
  extended tests: 10 of 23 failed exactly as the build report states, confirming each defect was reproduced
  before its fix. It confirmed the new live-path tests go through `validate_package` →
  `_resolved_run_material` → marshalling → `run` / `run_reference` with no hand-populated `RunContext.sources`
  or `fact_types`; that a subject or joined type that is also a collect name stays emitted with keys and still
  marked used, while unrelated scalar binding is unchanged; that the foreman's update of the stale 5a
  assertion to `(LINKS, BOX1)` is correct; and that `tests/test_sli_g2_binding_probe.py` is byte-unedited and
  passes. Full suite 2275 passed, 20 skipped; mypy clean; lint conformant.
- **Defect 4 (open at this commit), same class as Defect 2:** `optional_default` is resolved by fact-type id
  alone — last declaration wins in `package_validation.py` (binding validation) and in `runner.py`'s ordinary
  path, first wins in `subject_dispatch._optional_default`. Reproduced: a binding pinning v1 (no default) beside
  a v2 with a default validates, and at runtime publishes v2's default. Track 5c's keeping every declared
  version makes this reachable for standalone declared types. `runner.py`'s categorical domains collapse by id
  the same way (to be examined). **Round 2** repairs these; the first round-2 builder run stopped on a model
  session limit before making any change.
- **Out of scope, confirmed:** a declared-subject rule with no subject rows records no disposition; no existing
  disposition shape represents it without a record change. Owner decision.

## Round 2

- **Independent review:** sonnet sub-agent, fresh context, read-only, 2026-09-25. **Verdict: pass with
  notes.** Defect 4 fixed at all three sites (`package_validation.py` binding validation, `runner.py`'s
  ordinary path, `subject_dispatch._optional_default`), each on the exact pinned `(id, version)`. The reviewer
  reverted the three modules to round 1 and re-ran: 4 of the 6 new live-path tests failed as claimed, 2 passed
  only because declaration order happened to favour the pinned version. Full suite 2281 passed, 20 skipped;
  mypy clean; lint conformant; legacy probes unedited.
- The `ft.get("version", "v1")` fallback is unreachable in content (every bundle fact type carries a version;
  only negative fixtures lack one) and validation and runtime use the same default.
- **Still open — the exact-version class is not closed on the path.** Both reproduced:
  1. `runner.py` / `evaluator.py`: categorical domains and `symbol_fact_types` are keyed by bare id, and
     `_eval_categorical_operand` drops a `category_literal`'s pinned version. With two versions whose enums
     differ, a valid value blocks or publishes depending on declaration order. Fixing it changes the
     evaluator — outside this track's authority.
  2. `package_validation.py` (conditional-dependency yes/no check and `check_field_ref_bindings`): the binding's
     pinned version is discarded and fact types collapse to one per id, first declared wins. A field-ref to a
     field only the pinned version has is wrongly rejected in one order and wrongly accepted in the other.
  Content declares three fact-type ids at several versions (`tax.us.2025.f1099div.recorded-boxes` v1–v4,
  `tax.us.2025.w2.box1-wages` v1–v2, `tax.us.2025.w2.source-closure` v1–v3), so this is latent for real
  packages that resolve two versions together. Owner decision.
