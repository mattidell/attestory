# Charter — Track 5d Builder: the version a rule names is the version whose definition and value are used

One builder unit, in two stages. Owner direction, 2026-09-25: the definition and value actually used must
match the version the rule or binding names; declaration order must change neither the answer nor its
provenance. Evaluator changes are authorized for this track. Track 5c's repairs stay.

**The principle to apply at every step: trace the whole chain of authority.** Finding the right declaration is
not enough if its value is then read from a different version, or its pin records a version whose value was
not the one used. Before handing off, review your own implemented chain against that principle, consumer by
consumer, and write that self-review into the report.

## Context Capsule

- **Source ref:** `milestone/student-loan-circumstance-association` at the commit adding this charter, or later.
  Run `git status --short` before editing and before handing off; the foreman edits `docs/` concurrently.
- **Role:** Track 5d Builder.
- **Assigned paths:** `packages/derivation/live.py` (`_resolved_run_material`), `packages/derivation/runner.py`,
  `packages/derivation/subject_dispatch.py`, `packages/derivation/evaluator.py` (categorical and parameter
  resolution only), `packages/derivation/marshal.py` (only if a test proves it is needed),
  `packages/derivation/package_validation.py` (the checks named below); new
  `tests/derivation/test_exact_version_authority.py`; your report (Hand-off).
- **Deep reads, complete:** `track5c-build-report.md` and `track5c-review.md` (evidence directory);
  `evaluator.Environment`, the `ref`, `parameter`, `category_literal`, `categorical_compare`,
  `collect_categorical_all_equal`, `link_coverage` empty-parameter paths, `_eval_categorical_operand`,
  `_validate_categorical_value`; `runner._Run.__init__` (type maps, inputs, optional_default) and
  `dependency_pins_for_access`; `subject_dispatch._optional_default`, `_fact_type_of` and the local
  `fact_types` map; `package_validation`'s conditional-dependency yes/no check and `check_field_ref_bindings`.
- **Stop conditions:** a published schema or ADR change; an existing test failing (legacy probes unedited);
  the two runners needing different code; a genuine contract choice not settled below — stop on that item
  and report it; a new defect outside these consumers — show its consequence (executed) and stop on it rather
  than expanding the track.

## Facts the foreman established (2026-09-25, executed)

- **Repository coexistence ≠ package resolution.** Three fact-type ids exist at several versions in the
  repository (`tax.us.2025.f1099div.recorded-boxes` v1–v4, `tax.us.2025.w2.box1-wages` v1–v2,
  `tax.us.2025.w2.source-closure` v1–v3). **No** content package (40) resolves two versions of one fact type
  or one parameter together, and every one of the 2 891 `category_literal` pins in resolved content rules names
  a version its package resolves. These defects are latent for content, real for any package that resolves two
  versions. Your tests must build packages that genuinely resolve both versions together.

## Stage 1 — build (no contract choice involved)

Every test through the live path (`validate_package` → `_resolved_run_material` → marshalling → `run` and
`run_reference`), **both declaration orders**, asserting **the value and the authority recorded in its pins**.
Reproduce each defect as a failing test first.

1. **Default parameters, the whole chain.** A fact type's `optional_default` pins parameter v1; the package
   also resolves parameter v2 of the same id with a different value. Today `_resolved_run_material` keys
   parameters by id (last wins) and both runners then read that value while pinning v1, so either runner can
   publish v2's value under a v1 pin. Required: parameters are held by exact `(id, version)`; every consumer
   that names a version reads that version's value and pins that version — `optional_default` in the runner
   and in per-subject dispatch, and `link_coverage`'s empty parameter (which today checks the version against
   whichever declaration won, so it may block although the pinned version exists). An unavailable exact version
   blocks; it never borrows a sibling. Cover ordinary and declared-subject rules.
2. **Categorical domains and symbol types.** Domains are held by exact `(id, version)`. A binding's input symbol
   carries its pinned `(id, version)`; an `optional_default` symbol carries the binding's pinned version. A
   `category_literal` operand carries its own pinned version. `ref` validation, `categorical_compare`,
   `collect_categorical_all_equal` and `_validate_categorical_value` read the exact domain. Two different
   versions of one id are **different domains**: comparing them is a domain mismatch, not an equality — no
   invented equivalence. An unavailable exact version blocks.
3. **Validation reads what runtime reads.** The conditional-dependency yes/no check and
   `check_field_ref_bindings` use each binding's pinned `(id, version)`, never a map collapsed to one entry per
   id. Reproduce the reviewer's case (v1 scalar, v2 object with `amount`, binding pins v2) in both orders.
4. **Zero-subject rules — tests only, no new disposition.** (a) A declared-subject rule whose subject type has
   genuinely no current finding: no publication, no disposition, and no downstream consumer treats the silence
   as favourable or complete (show a consumer that requires it blocking `DEPENDENCY_ABSENT`). (b) The same
   package with current subject findings: each reaches execution through the live path.

## Stage 2 — contract choices: reproduce and report, do not implement

The foreman identified these as genuine choices for the owner. For each, write a failing or characterising test
of today's behaviour, describe the options with their consequences, and stop:

- **C1. Derived categorical results.** A derived finding carries no fact type; a downstream `ref` to it falls
  back to the symbol name as a fact-type id (`symbol_fact_types.get(name, name)`), and keyed same-run
  publications carry no type (`subject_dispatch._fact_type_of`). Options include typing a derived value from
  the `category_literal` actually evaluated (per evaluation, in-run only) or requiring a declared output type (a
  schema successor). In stage 1, keep today's behaviour for a derived symbol when exactly one version of that
  id is resolved, and block when several are (today that silently takes the last); say which content, if any,
  relies on the symbol-name fallback.
- **C2. Unversioned `parameter` references.** The rule grammar's `parameter` op names no version. When a
  package resolves two versions of that id, either validation rejects the package as ambiguous or something
  selects a version. In stage 1, block at runtime rather than select; report whether any content resolves two
  versions (the foreman found none) and the options.

## Verification

`python3 -m pytest -n auto -q`, `python3 -m mypy`, `python3 tools/governance_lint.py`, `git diff --check`.

## Hand-off

Do not commit. Report to
`docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/track5d-build-report.md`
(no absolute workstation paths — the commit gate refuses them): each reproduction and that it failed first;
each change, file and function; each test, what it asserts about value **and** pins; the chain-of-authority
self-review, consumer by consumer; stage 2's characterisations and options; any stop condition; verification
tails verbatim.
