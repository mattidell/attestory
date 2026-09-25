# Charter — Track 5c Builder: carry declarations from package to execution

One builder unit. Repairs three defects an independent review reproduced at `6ca54a8d` in Track 5's
declaration-to-execution path. Track 5a/5b's dispatcher tests pass because they hand-populate
`RunContext.sources` and `fact_types`; the live path does not supply them the same way. **Test how the engine
obtains its inputs, not only what it does after a test supplied them.** A declaration has not established a
capability until its meaning survives package resolution, live material, marshalling and dispatch.

No ADR or published-schema change is expected. ADR 0076 Parts 1–2 stand as accepted; Part 3 is open.

## Context Capsule

- **Source ref:** `milestone/student-loan-circumstance-association` at the commit that adds this charter, or
  later; verify with `git rev-parse HEAD`. Run `git status --short` before editing and before handing off; the
  foreman edits `docs/` concurrently.
- **Role:** Track 5c Builder.
- **Assigned paths:** `packages/derivation/live.py` (`_resolved_run_material` only);
  `packages/derivation/subject_dispatch.py`; `packages/derivation/marshal.py` only if a test proves it is
  needed; new `tests/derivation/test_subject_declaration_live_path.py`; additions to
  `tests/derivation/test_relationship_presence.py`; your report (Hand-off).
- **Deep reads, complete:** ADR 0076 Parts 1–2; `track5a-build-report.md`, `track5b-build-report.md`,
  `track5b-review.md`; `live._resolved_run_material` and its caller `live_coordinate_run`;
  `marshal.marshal_run_context` (the emission-only names and the used-id rule, Track 4 option B);
  `package_validation._subject_relationship_issues` and how it builds `fact_types_by_key`;
  `subject_dispatch.evaluate_subject_scoped_rule`, `_presence_declaration`, `_identity_names`,
  `_presence_matched`, and the required-name binding loop (including the run-wide
  `req in run.symbol_pin and req in run.symbols` branch).
- **Stop conditions:** stop and report if a repair needs a published schema, an ADR change, an evaluator arm,
  `_scope`'s body, pairing, or `derivation-record`; if the two runners need different code; if any existing
  test fails, including the legacy probes (`tests/test_sli_g2_binding_probe.py` and its `..._dropped_today`
  tests must pass unedited); or if a repair would change scalar binding for rules that do not declare a subject.

**First, reproduce.** Write each defect's test so it fails on the current code, confirm it fails, then fix.
Say in the report that each failed before the fix.

## Defect 1 — declared subjects and relationships do not reach live execution

`_resolved_run_material` loads fact types only from `bundle.v1`/`bundle.v2` members, though package validation
accepts standalone `fact-type.v2` members; and it arranges source emission only for `link_coverage` link
types, not for a v11 rule's `subject` or `joined` type. Reproduced: a validated subject-only rule with a
current finding reached both schedulers with zero sources and produced neither a publication nor a disposition.

Required:
- The material's fact types include standalone `fact-type.v2` members as well as bundle-contained ones, keeping
  every declared version of an id (de-duplicate only identical `(id, version)` entries).
- Every v11 rule's `subject` type and `joined` type is added to the **emission-only** names — emitted as keyed
  sources — and **not** to the collect names. Emission is not scalar binding: an emission-only finding is not
  marked used and does not change what the input-binding loop or legacy fallback binds (Track 4's rule).
- No artificial source family and no added `ref` is needed to make a declared subject visible.
- If adding standalone fact types changes anything for existing packages (for example categorical domains),
  report exactly what, with the tests that show it.

Test (`test_subject_declaration_live_path.py`) through **normal package resolution and marshalling** — a v32
package accepted by `validate_package`, its resolved members passed through `_resolved_run_material`, then
`marshal_live_run_context` (or `marshal_run_context` with exactly that material) over a kernel state that
carries a fact lattice (see `tests/derivation/test_subject_dispatch.py`'s `_State`), then `run` and
`run_reference`. **Do not hand-populate `RunContext.sources` or `fact_types`.** Cases:
- a subject-only v11 rule, standalone fact types (no bundle), one current finding per statement → one keyed
  publication per statement, both runners;
- a v11 rule declaring `joined`/`direction` over standalone fact types → the joined rows are emitted with keys
  and the presence check runs (one joining case, one malformed-row block);
- the emission-only distinction: an ordinary rule elsewhere in the package that binds a scalar keeps the same
  binding with and without the v11 rule present.

## Defect 2 — runtime does not honour the pinned fact-type version

`_identity_names` takes the first declaration whose id matches. Package validation resolves the exact
`(id, version)` pin. Reproduced: pinning a stronger v2 identity while a weaker v1 of the same id was declared
first let a malformed link publish 42 for both subjects; reversing the declaration order blocked both.

Required: runtime resolves the **exact pinned** `(id, version)` declaration for the reference type, and fails
closed (every subject blocks `DEPENDENCY_INVALID`, naming the pinned type) if it is unavailable. Static
validation and runtime examine the same identity definition. Test both declaration orders; both must block the
malformed link.

## Defect 3 — a run-wide scalar bypasses a declared relationship

With a declared financing-to-enrolment relationship, no enrolment source rows, and an enrolment value in
run-wide inputs, dispatch published using that unscoped value.

Required: for a rule that declares `joined`, the joined type's value is available inside dispatch **only** from
a row that joined this subject. It is never bound from the run-wide scalar, and it is not readable from the
run-wide environment during that subject's evaluation. With no joined row: an explicitly declared
`optional_default` for that symbol still takes its existing, visibly pinned `declared_default` path; otherwise
the subject blocks `DEPENDENCY_ABSENT`. Tests: the bypass (no rows, run-wide scalar present → no publication
from that value; `DEPENDENCY_ABSENT`); the ordinary valid joined case (publishes, pinning the joined row); and
the declared-default case, showing it stays distinct.

## Out of scope — report only

A declared-subject rule with **zero** subject rows records no disposition at all. Do not change this; say in
the report whether any existing record or disposition shape could represent it without a schema change.

## Verification

`python3 -m pytest -n auto -q`, `python3 -m mypy`, `python3 tools/governance_lint.py`, `git diff --check`.

## Hand-off

Do not commit. Report to
`docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/track5c-build-report.md`:
each reproduction and that it failed first, each change with file and function, each test and what it
asserts, the out-of-scope finding, and verification tails verbatim.
