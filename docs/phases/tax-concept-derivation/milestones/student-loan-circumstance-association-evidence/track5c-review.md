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
