# Charter — Track 3, stage B2 Builder: the coverage operation's runtime

One builder unit. Implements the **runtime half** of the accepted contract
[`track3-coverage-contract.md`](track3-coverage-contract.md), on top of stage B1's schemas,
validation and admission (committed). ADR 0075 is `proposed`, not yet accepted.

## Context Capsule

- **Source ref:** `milestone/student-loan-circumstance-association` at `cbf2ce55` or later; verify
  with `git rev-parse HEAD` and `git branch --show-current`.
- **Milestone:** `student-loan-circumstance-association`; primary branch `main`.
- **Role:** Track 3 stage B2 Builder.
- **Assigned paths:** `packages/derivation/evaluator.py` (a new defaulted `Environment` slot and the
  `link_coverage` arm only — no change to any existing arm); `packages/derivation/subject_dispatch.py`
  (install the slot for both declared names on every subject, the `keys_unavailable` sentinel);
  `packages/derivation/authorization_closure.py` (admit `rule-artifact.v10` and the same
  coverage-node edges package validation adds); `tests/test_sli_circumstance_association_a4_pass2.py`
  (flip `ObservedUnresolvedLinkDefect` and add the behavioural classes — do not edit other existing
  tests); `tests/derivation/test_link_coverage_runtime.py` (new).
- **Deep reads, complete:** the contract, all of it; ADR 0075; `temp/a4-pass2/track3b1-review.md`;
  `evaluator.py` (`Environment`, `evaluate`, `bound_sources` for the defaulted-field pattern);
  `subject_dispatch.py`; `authorization_closure.py` and how `package_validation` added the v10 edges.
- **Stop conditions:** stop and report if meeting an obligation needs: a change to any existing
  evaluator arm, to `collect`/`count`, to closure, to `marshal_run_context`, or to a published schema;
  comparing a rendered `fact_id` or symbol; or a decision the contract leaves open.

## What to build

Exactly the contract's sections 3–6: the slot, the `link_coverage` arm, the fail-closed checks in their
table order, the three outcomes with the pins and `missing` the contract specifies, and
`link-coverage-scope-unbound` / `link-coverage-keys-unavailable`. Plus `authorization_closure` walking
v10 so a v10 rule's dependencies are inside the authorization closure.

## Acceptance — the contract's behavioural obligations, and the owner's list

1. **Flip** `ObservedUnresolvedLinkDefect`: one of two links unresolved → North **blocks**
   `DEPENDENCY_INVALID`, `missing` exactly that link's `finding_id`; only link unresolved → blocks the
   same way, **not** `SOURCE_SET_UNCLOSED` and not the default. Rename the class to state the required
   behaviour; keep the unrelated-statement byte-identity assertions.
2. **No link** → box 1 on the declared default, pinning the parameter and the box finding, no link, no
   reduction, no closure.
3. **All links resolved** → box 1 minus the sum, pinning **every** covered link and reduction.
4. **An inapplicable reduction** → uncovered → blocks naming the link.
5. **Correction** of a link → matched through its successor; the pin walk reaches the successor.
6. **Withdrawal** of a link → the default; state what was observed if a reduction survives.
7. **Isolation** of another statement: byte-identical.
8. **The blocked disposition names the uncovered link**; a successful amount pins every covered link.
9. **An undeclared empty collection still blocks** `SOURCE_SET_UNCLOSED`; ordinary `collect`/`count`
   unchanged; `attempt()` of a coverage rule outside per-subject dispatch fail-closes
   `link-coverage-scope-unbound`.
10. **Missing keys** on either declared name block `link-coverage-keys-unavailable`, never the default.
11. **Authorization:** a v10 package's coverage rule, reduction rule, link fact type and parameter are
    inside the authorization closure.

Use B1's validated rule shapes (v10 with `source_set`-valid content) where the obligations run rules,
so these probes are no longer synthetic-unvalidated: state in the report which runs use rules that pass
`validate_package` and which still hand-assemble the run.

## Verification

`python3 -m pytest -n auto -q`, `python3 -m mypy`, `python3 tools/governance_lint.py`, `git diff --check`.

## Hand-off

Do not commit; the foreman reviews and commits. Report to `temp/a4-pass2/track3b2-report.md`: each
obligation, its test, what it asserts; verification tails verbatim; stop conditions met; the evidence
boundary (what still hand-assembles the run; nothing here establishes the durable reader — P4).
