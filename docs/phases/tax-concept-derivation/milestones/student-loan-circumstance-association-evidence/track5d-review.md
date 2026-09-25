# Track 5d — review record

- **Builder:** grok (headless CLI), three rounds; the foreman narrowed one round-3 validation check.
- **Foreman review before independent review:** found the attachment threshold still reading its parameter
  by id (value/pin mismatch; then a false block with two versions resolved) and the exact-version parameter
  index stored under a sentinel key inside the id-keyed map. Round 2 fixed both (`parameter_index` field
  carried from resolution through marshalling to run and environment).
- **Independent review (grok, fresh session, read-only), 2026-09-25: pass with notes.** Reproduced the old
  behaviour from HEAD copies and confirmed, through the live path in both declaration orders and on both
  runners, that each consumer uses and pins the version it names and blocks when that exact version is
  absent: `optional_default` (runner and per-subject dispatch), `link_coverage`'s empty parameter, the
  `parameter` op, `range_lookup` / `bracket_fold` tables, the attachment threshold, `ref` validation,
  `categorical_compare`, `collect_categorical_all_equal`, the conditional-dependency yes/no check and
  `check_field_ref_bindings`. Stage-2 characterisations accurate, including the three core-package rules that
  read `tax.us.2025.schedule-d-required.conclusion` through the symbol-name fallback.
- **Notes acted on (round 3):** `BINDING_DEFAULT_ABSENT` now requires the exact pinned parameter version; an
  attachment's top-level `threshold_parameter` rejects when a sibling version is resolved and the pinned one
  is not. **Confirming review (grok, fresh session): confirm** — no sibling can stand in at validation or
  runtime, in both orders.
- **Notes reported to the owner, not changed (outside these consumers; none can use a wrong version's
  value):** `packages/tax/pairing_consequences.py` builds its environment without `parameter_index`, so with
  two versions resolved it blocks; `packages/derivation/runners/derive.py` (fixture adapter, not `live_run`)
  still keys parameters by id; a versionless parameter citizen would satisfy any exact lookup, but
  `parameter-declaration.v1` requires `version`; a top-level threshold parameter absent altogether passes
  validation and blocks at runtime; keyed publications carry no categorical type (stage 2, C1).
- **Verification:** full suite 2305 passed, 20 skipped; mypy clean (282 files); governance lint conformant;
  `git diff --check` clean; legacy probes unedited.
