# Charter — Track 3, stage B1 Builder: the coverage contract's declarative artifacts

One builder unit. Implements the **declarative half** of the accepted contract
[`track3-coverage-contract.md`](track3-coverage-contract.md): the ADR, the schema successors,
package validation and admission. **No runtime behaviour** — the evaluator operation, the per-subject
slot and sentinel, and the behavioural tests are stage B2.

## Context Capsule

- **Source ref:** `milestone/student-loan-circumstance-association` at `df1abb02` or later; verify
  with `git rev-parse HEAD` and `git branch --show-current`.
- **Milestone:** `student-loan-circumstance-association`; primary branch `main`.
- **Role:** Track 3 stage B1 Builder.
- **Assigned paths:** `docs/adr/0075-*.md` (new; take the next free number, and add it to
  `docs/adr/INDEX.md`); `packages/schemas/derivation/rule-artifact.v10.schema.json` and
  `artifact-package.v31.schema.json` (new files only) and that directory's `published.json`
  (append only, via `packages.kernel.schema_registry.write_manifest`); `packages/derivation/package_validation.py`;
  `packages/derivation/marshal.py` (`_rule_required_symbols` schema set only);
  `packages/derivation/live.py` (`_resolved_run_material` only); `packages/derivation/runner.py`
  (the `use_v2` schema sets only); new tests `tests/derivation/test_link_coverage_contract.py`.
- **Deep reads, complete:** the contract, all of it; `AGENTS.md` "Schema Publication Protocol";
  `docs/adr/INDEX.md` and one recent Tier 2 ADR for form; `rule-artifact.v9` and
  `artifact-package.v30` schemas; `package_validation.validate_package` and its supported-schema set.
- **Stop conditions:** stop and report if any published schema file or existing `published.json` entry
  would change; if meeting the contract needs a change the contract rules out (ordinary
  `collect`/`count`, closure, marshal semantics beyond the schema set, rendered ids); or if the
  contract is ambiguous on a point this unit must decide — report it, do not decide it.

## What to build

1. **ADR (Tier 2), accepted-pending-review status per the repo's convention.** Its decision is the
   contract's section 9 paragraph; it cites the P3 tests and the contract as evidence; it records the
   record-code choice (no `derivation-record.v10`, `DEPENDENCY_INVALID` with link ids, P4 decides) and
   the open scheduling limit.
2. **`rule-artifact.v10`** — v9 plus the `link_coverage` expression alternative exactly as the contract's
   section 2 fragment. **`artifact-package.v31`** — v30 admitting `rule-artifact.v10`. New files only;
   append checksums with `write_manifest`; confirm the manifest diff only adds.
3. **Package validation** — `rule-artifact.v10` supported; the section 2 checks (distinct names, `links`
   a package fact type, `reductions` a predecessor's `publishes`, parameter a member, node only in
   `value`, not in `when`, names not in the coverage rule's `requires`); and
   `LINK_COVERAGE_NAME_REUSED` for every forbidden use in section 2, **including attachment-rule
   symbols**.
4. **Admission** — `marshal._rule_required_symbols` and the runner's `use_v2` sets include v10;
   `live._resolved_run_material` includes v10 and appends each node's two names to `collect_names`.

## Acceptance — the contract's validation obligations

In `tests/derivation/test_link_coverage_contract.py`: obligation 14 (the worked example validates
against v10 and is accepted on v31; rejected on v30; rejections for the node in `when`, the names in
`requires`, an unpublished `reductions`; no id gate) and obligation 17 (every
`LINK_COVERAGE_NAME_REUSED` rejection, including attachment symbols; a compliant package leaves a sibling
fact type's scalar binding unchanged, one finding and several agreeing), and that
`_resolved_run_material` registers both names for a v10 package and nothing for a package without the
node. Ordinary behaviour unchanged: the full suite stays green.

## Verification

`python3 -m pytest -n auto -q`, `python3 -m pytest tests/test_schema_registry.py -q`,
`python3 -m mypy`, `python3 tools/governance_lint.py`, `git diff --check`, and the manifest diff.

## Hand-off

Do not commit; the foreman reviews and commits. Report to `temp/a4-pass2/track3b1-report.md`: each
artifact, each test and what it asserts, the manifest diff, verification tails verbatim, and any stop
condition met or contract ambiguity found.
