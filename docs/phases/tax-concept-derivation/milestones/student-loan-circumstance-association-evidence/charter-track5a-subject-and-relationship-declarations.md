# Charter — Track 5a Builder: subject and relationship declarations (ADR 0076 Parts 1–2, declarative half)

One builder unit. Implements the **declarative half** of ADR 0076 Parts 1 and 2, accepted by the owner on
2026-09-24: the first rule and package successors, their admission, and the static relationship checks.
**No runtime behaviour** — scheduling (Part 1's `is_eligible` / `attempt` / `finalize_unreached`) and the
runtime presence check (Part 2) are Track 5b. Part 3 is open and is not touched.

## Context Capsule

- **Source ref:** `milestone/student-loan-circumstance-association` at the commit that adds this charter, or
  later; verify with `git rev-parse HEAD` and `git branch --show-current`. Run `git status --short` before
  editing and again before handing off: the foreman edits `docs/` and
  `tests/test_sli_bare_statement_chain_probe.py` in the same worktree at the same time. Do not touch those.
- **Milestone:** `student-loan-circumstance-association`; primary branch `main`.
- **Role:** Track 5a Builder.
- **Assigned paths:**
  - new `packages/schemas/derivation/rule-artifact.v11.schema.json` and
    `packages/schemas/derivation/artifact-package.v32.schema.json`; that directory's `published.json`
    (append only, via `packages.kernel.schema_registry.write_manifest`);
  - `packages/derivation/package_validation.py`;
  - the closed schema-name sets that list `rule-artifact.v10` in `packages/derivation/live.py`
    (`_resolved_run_material`), `packages/derivation/marshal.py` (`_rule_required_symbols`) and
    `packages/derivation/authorization_closure.py` — **admission only**, v11 treated exactly as v10;
  - new test file `tests/derivation/test_subject_relationship_declarations.py`.
  - **Not assigned:** `packages/derivation/runner.py`, `reference_runner.py`, `subject_dispatch.py`,
    `evaluator.py`. Those are 5b. Do not add v11 to the runner's schema sets.
- **Deep reads, complete:** `docs/adr/0076-per-subject-scheduling-and-binding-relationships.md` (Parts 1 and
  2, and the publication plan); `AGENTS.md` "Schema Publication Protocol";
  `packages/schemas/derivation/rule-artifact.v10.schema.json` and `artifact-package.v31.schema.json`;
  `package_validation.validate_package` and `_link_coverage_issues`; the `fact-type.v2` schema's
  `identity_keys`.
- **Schema intent:** the foreman has recorded `propose` events for `rule-artifact.v11` and
  `artifact-package.v32` on `milestone-schema-ledger`. Do not touch the ledger.
- **Stop conditions:** stop and report if any published schema file or existing `published.json` entry
  would change; if a check needs runtime information (row values, dispatch); if the ADR is ambiguous on a
  point this unit must decide — report it, do not decide it; or if an existing test fails for any reason.

## What to build

1. **`rule-artifact.v11`** — a byte-for-byte copy of v10's grammar (new `$id`, `schema` discriminator
   `rule-artifact.v11`), plus:
   - `subject` — **required**, a fact-type pin `{id, version}` in the same shape v10 uses for fact-type pins;
   - `joined` — optional, a fact-type pin; `direction` — optional, enum `joined_contains_subject` |
     `subject_contains_joined`. Present together or absent together (schema-enforced if expressible;
     otherwise in package validation).
   Nothing else. No `wording`, `lineNote` or `link_count`: those are the second successor.
2. **`artifact-package.v32`** — v31 plus `rule-artifact.v11` in the member schema enum. No package-level
   subject map.
3. **Package validation** (on `artifact-package.v32`; `rule-artifact.v11` supported wherever v10 is):
   - `subject` and `joined` each resolve to a `fact-type.v2` member of the package (id and version).
   - `joined_contains_subject`: the joined type's `identity_keys` names ⊇ the subject type's names.
     `subject_contains_joined`: the subject type's names ⊇ the joined type's names. **Nothing weaker** —
     one shared name is not a pass.
   - A v11 rule whose `value` contains `link_coverage` must declare `joined` equal to the node's `links`
     type and `direction: joined_contains_subject`; otherwise reject.
   - Each rejection is an issue with a new, specific code (name them in the report). No ids are gated.
   - v10 and earlier rules, and v31 and earlier packages, validate exactly as today.
4. **Admission** — the closed sets in `live.py`, `marshal.py` and `authorization_closure.py` treat v11
   as v10 (including `link_coverage` edges and names). Nothing else in those files.

## Acceptance — tests that exercise the new declarations

In `tests/derivation/test_subject_relationship_declarations.py`, every behaviour test uses **v11 rules on a
v32 package** (the ADR's condition: new behaviour tests exercise the new declarations; do not edit
`tests/test_sli_g2_binding_probe.py` or other probe files — they record undeclared behaviour):

- Schema: v11 without `subject` is rejected; `joined` without `direction` (and the reverse) is rejected; an
  unknown direction is rejected; v11 is rejected as a member of a v31 package and accepted on v32.
- ADR Part 2's key-name table, as declared fact types:
  - tax-year + borrowing link vs statement identity (lender, statement, tax-year): both directions reject;
  - statement id only: both reject; lender + tax-year + borrowing: both reject;
  - full statement identity + borrowing: only `joined_contains_subject` accepts;
  - full enrolment (period, institution, programme) vs financing (borrowing, period, institution,
    programme): only `subject_contains_joined` accepts;
  - period-only enrolment: `subject_contains_joined` **accepts**, and the test says this is ADR residual 1,
    not a fix.
- A v11 `link_coverage` rule with `direction: subject_contains_joined`, or with `joined` not its `links`
  type, or with no `joined`, is rejected; with the right pair it is accepted.
- An unresolvable `subject` or `joined` pin is rejected.
- A v10 package that validated before still validates (use an existing v10 fixture), and admission sets
  give v11 the same `link_coverage` edges as v10 (`_resolved_run_material` names; authorization closure).

## Verification

`python3 -m pytest -n auto -q`, `python3 -m pytest tests/test_schema_registry.py -q`, `python3 -m mypy`,
`python3 tools/governance_lint.py`, `git diff --check`, and `git diff packages/schemas/derivation/published.json`
(only two added entries).

## Hand-off

Do not commit; the foreman reviews, has the unit independently reviewed, and commits. Write the report to
`docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/track5a-build-report.md`:
each change with file and function, each test and what it asserts, the new issue codes, the verification
tails verbatim, the manifest diff, and any stop condition met.
