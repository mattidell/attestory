# Schedule K-1 Box-5 Interest Breadth — Closing CI Repair Charter

Audience: Builder.

Status: **chartered for owner launch.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `milestone/k1-interest-breadth` at
  `99b0978f3d7b7e6f211c0add634c40fc93128eea`.
- **Object:** repair the one failure from closing PR #133's `verify` run
  30681893808. The failing test is
  `tests.test_dsbs_t1_schema_citizens.ReconciledVocabularies.test_form_field_v3_carries_the_emitted_code_and_line_2b_v2_rides_it`.
- **Role:** one Builder, normal tier / medium effort. Do not spawn sub-agents.
- **Scope and evidence ceiling:** one deterministic test-maintenance repair in
  `tests/test_dsbs_t1_schema_citizens.py`, verified with focused local unit
  tests. Product content, runtime behavior, packages, schemas, fixtures, and
  closeout records are outside scope.
- **Stop conditions:** stop if the failing assertion is still correct against
  package v9 or loader semantics; if a product/content/runtime edit appears
  necessary; if another test fails for a different reason; if any published
  artifact would need to change; if the worktree is dirty at launch; or if real
  or private data is encountered.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `tests/test_dsbs_t1_schema_citizens.py` around `ReconciledVocabularies`;
  `packages/tax/loader.py#load_form_fields`;
  `packages/content/tax/2025/form1040.line-2b.form-field.v2.json`;
  `packages/content/tax/2025/form1040.line-2b.form-field.v3.json`;
  package v9's line-2b form-field member; and K1-N12 in
  `tests/test_k1_interest_breadth_contracts.py`.

Before editing, echo the resolved branch tip, one-file scope, evidence ceiling,
and stop conditions.

## Failure attribution

Closing CI completed 781 tests and failed one assertion:

```text
AssertionError: 'v3' != 'v2'
tests/test_dsbs_t1_schema_citizens.py:227
```

`load_form_fields()` intentionally selects the highest published citizen
version for an ID. The milestone additively published line-2b field content v3
and package v9 selects it. Historical v2 remains published and is explicitly
rejected as a mixed successor graph by K1-N12. The old test's expected current
version and method name were not advanced with that successor.

## Deliverable

1. In `tests/test_dsbs_t1_schema_citizens.py`, rename the affected method so it
   accurately describes the current line-2b field and change its expected
   citizen version from `v2` to `v3`.
2. Preserve the assertions that the citizen uses `form-field.v3`, admits
   `SOURCE_SET_UNCLOSED`, rejects retired `SOURCE_SET_OPEN`, and therefore still
   proves the reconciled vocabulary contract.
3. Do not weaken or remove K1-N12's independent proof that historical line-2b
   field v2 cannot enter package v9.
4. Commit only the one-file repair and return custody to the Foreman with the
   commit identity plus self-reported turn and tool-call counts.

## Focused verification

Run each command once:

```text
python3 -m unittest tests.test_dsbs_t1_schema_citizens
python3 -m unittest tests.test_k1_interest_breadth_contracts
git diff --check 99b0978f3d7b7e6f211c0add634c40fc93128eea..HEAD
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range 7066f26e02467a58ca6cb329666782b32bd7dd12..HEAD
```

Do not run the full suite; PR #133's replacement `verify` run is the gate of
record.
