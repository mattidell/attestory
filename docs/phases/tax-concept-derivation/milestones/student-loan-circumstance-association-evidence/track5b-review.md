# Track 5b — review record

- **Foreman review, round 1 (executed):** two fail-open defects in the Part 2 presence check.
  (1) An unreadable reference identity (declared fact type absent from the run) left the required-name list
  empty, and every row then joined every subject. (2) A subject lacking one of its own required identity
  names took the no-link result, against ADR 0076 Part 2 ("when its own keys are present"). Both fixed by the
  builder: (1) every subject blocks `DEPENDENCY_INVALID` naming the reference fact-type id; (2) that subject
  blocks through the existing keys-unavailable path. Three tests added, including the
  `subject_contains_joined` variant. Re-executed by the foreman: both fail closed; the runners agree.
- **Independent review:** sonnet sub-agent, fresh context, read-only, 2026-09-24. **Verdict: pass, no
  defects.** Confirmed Part 1 placement (after pairing/nominee checks; `attempt` and `finalize_unreached`
  dispatch per subject and never evaluate once; `reference_runner` unchanged and shares the code), the
  don't-wait branch executed, and Part 2's required names from declarations. Adversarial runs beyond the
  shipped tests, both runners agreeing: mutually circular declared rules resolve through
  `finalize_unreached` without hanging; a subject type with no rows; a joined row with no keys at all is
  malformed and blocks every subject; a reduction keyed only on a shared tax year beside presence-joined
  links fails closed rather than cross-joining. `tests/test_sli_g2_binding_probe.py` is byte-unedited and
  passes 23/23, including both `..._dropped_today` tests.
- **Notes, not defects:** the type-level "unjoinable" check becomes unreachable for a presence-declared
  rule's joined type (every such row is already malformed); `_attempt_subject_scoped`'s summary return value
  is discarded by every caller.
- **Verification (reviewer's run):** full suite 2263 passed, 20 skipped; mypy clean (280 files); governance
  lint conformant; `git diff --check` clean.

- **Later finding (owner's independent review at `6ca54a8d`):** both reviews above checked the dispatcher with
  test-supplied sources and fact types. The live path was not exercised, and three defects were reproduced
  there (declarations not reaching marshalling; runtime ignoring the pinned fact-type version; a run-wide
  scalar bypassing a declared relationship). "Pass" above means the dispatcher, not the capability. Repaired
  in Track 5c.
