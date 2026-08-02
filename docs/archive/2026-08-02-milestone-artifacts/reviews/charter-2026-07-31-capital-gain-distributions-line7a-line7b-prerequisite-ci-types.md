# Capital-Gain Distributions / Line 7a — Prerequisite CI Type Repair

Audience: Builder.

Status: **chartered for one invariant-container inference error.**

## Context Capsule

- **Source ref and resolved launch commit:** current prerequisite branch at this
  committed charter/pointer. Resolve and verify `HEAD` before acting.
- **Exact object:** mypy reports one `arg-type` error at
  `tests/test_capital_gain_distributions_line7a_line7b_prerequisite.py:232`.
  The heterogeneous case table is inferred as a union of invariant dictionary
  types rather than its intended `dict[str, str | None]` component shape.
- **Role:** the prerequisite Builder continues its CI repair lineage.
- **Scope and evidence-rung ceiling:** add only an explicit static annotation
  for the existing case table in the named test file. Runtime data, cases,
  assertions, control flow, production code, and configuration are frozen.
- **Stop conditions:** stop if another file or runtime change is needed; if a
  case/value/assertion is changed; if the error requires a suppression; or if
  governance/private material is implicated.
- **Full reads before acting:** this charter; `docs/roles/builder.md`; the named
  test module; and `AGENTS.md#Data Safety Rules`.

Before editing, echo the error, one-annotation/no-runtime ceiling, and stop
conditions.

## Verification and handoff

Run once:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_line7b_prerequisite
python3 -m mypy
git diff --check <charter-commit>..HEAD
python3 tools/envelope_scan.py --range main..HEAD
```

Commit one type-repair commit, leave the tree clean, and report the SHA,
annotation, and results. Do not review, edit pointers/charters, push, merge,
restart Track 3, or begin Track 4.
