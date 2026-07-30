# Capital-Gain Distributions / Line 7a — Track 2 Independent Review Charter

Audience: Reviewer.

Status: **chartered for owner launch.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-track2` with implementation commit
  `96a94d1c4c3a5490867a15fcd288b8a0fe10dab4`. The review-charter commit is
  context and must be its direct successor.
- **Exact object or commit range:** implementation range
  `c4f1a4934381df67ee0386911eea2abc9583f5cd..96a94d1c4c3a5490867a15fcd288b8a0fe10dab4`.
  The preceding `c4f1a49` commit binds the Builder charter and pointer to the
  Track-1 merge; it is context, not part of the implementation object.
- **Role:** one author-independent Reviewer, High tier / high effort. Do not
  consult the Builder's thread or self-assessment. The implementation was
  recovered from the Builder's remote after its thread was interrupted; judge
  only committed evidence.
- **Scope and evidence-rung ceiling:** measure Track 2's declared rules,
  admission and package interlocks, successor package, coordinator behavior,
  lifecycle/currency behavior, explanations, and production-shaped synthetic
  goldens through `live_coordinate_run`. No presentation/browser or real-data
  work; do not design or implement a repair or reopen ADR-0050.
- **Stop conditions:** stop and report if the implementation object is not the
  exact range above or if the review-charter commit is not its direct
  successor; if a published historical schema, manifest entry, content
  version, package, or accepted ADR changed; if the implementation introduces
  a new evaluator operation or generic substrate not authorized by the
  charter; if Schedule D, Form 8949, Form 1099-B, excluded-box computation,
  presentation, or Track-3 work appears; if review requires governance
  interpretation; if any real/private material is encountered; or if a
  failure cannot be attributed to this range without a base comparison.
- **Full reads before acting:** this charter;
  `docs/roles/reviewer.md`;
  `docs/reviews/charter-2026-07-29-capital-gain-distributions-line7a-track2.md`;
  `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md`;
  `docs/adr/0050-capital-gain-distributions-and-line-7a.md`;
  `docs/adr/0031-real-data-residency-boundary.md`;
  `docs/adr/0035-dividend-composition-and-lines-3a-3b.md`;
  `docs/adr/0036-schedule-attachment-ontology.md`;
  `docs/adr/0038-qdcg-worksheet-and-declared-absence.md`;
  every file in the exact implementation range;
  `docs/reviews/2026-07-29-capital-gain-distributions-line7a-track1-repair-recheck.md`;
  `AGENTS.md#Schema Publication Protocol`;
  `AGENTS.md#Fixture Rules`; and `AGENTS.md#Data Safety Rules`.

Before reviewing, echo the resolved implementation commit and ancestry, exact
range, review ceiling, independence constraint, authoritative golden entrypoint,
immutable-history constraint, and every stop condition.

## Required measurements

1. **Exact object, history, and boundary.** Enumerate the range and map every
   changed file to a Track-2 deliverable. Confirm that the new package, bundle,
   rules, schema, loader/runner/validation changes, synthetic adoption/release
   fixtures, and tests are necessary to this track. Treat edits to existing
   adoption/release fixtures, generic kernel/registry code, or established
   contradiction tests as review surfaces rather than assuming they are
   harmless. Fail for prototype copying, presentation/browser/real-data work,
   Schedule D/Form 8949/Form 1099-B artifacts, excluded-box computation, or a
   new evaluator operation/generic substrate.
2. **Publication immutability and successor graph.** Verify no historical
   published schema, checksum, content version, or package changed. The
   derivation manifest may only append the unused
   `artifact-package.v5.schema.json` row whose checksum matches exact bytes.
   Confirm the v7 package and v2 Form-1099-DIV bundle form a strict exclusive
   successor graph rooted in Track-1 citizens, without mixing historical and
   successor box-2a content. Determine whether each changed current
   adoption/release fixture is synthetic pointer evidence rather than a
   mutation of published history.
3. **Checked conclusion and line 7b.** Exercise individual and combined C1–C4
   absence, all-`"yes"`, and each component-`"no"` case. Confirm missing
   components block with the exact absent set, the truth table derives the
   accepted conclusion, and line 7b publishes only from conclusion `"no"` with
   exactly the accepted citation. Independently mutate the conclusion inputs
   and citation identity/cardinality rather than accepting committed tests at
   face value.
4. **Box-2a family, closure, and admission interlock.** Verify collect/subtotal
   behavior over the successor family: single and multiple statements sum once,
   closed-empty publishes closure-backed zero, and open/undeclared/stale closure
   blocks. Confirm the signal is fed only by current non-null successor members
   and that declaration-first, signal-first, and same-batch contradictions
   reject before mutation. Historical null/residual content must not raise the
   successor signal.
5. **Line 7a route and state propagation.** Verify conclusion `"no"` selects
   the box-2a subtotal, missing authority becomes
   `blocked(DEPENDENCY_ABSENT)` with the exact missing set, and conclusion
   `"yes"` becomes `guard_inapplicable`. Confirm no state is converted to zero
   and no Schedule D/Form 8949 artifact is fabricated. Line 9 must consume the
   selected line-7a publication exactly once, never raw box 2a or qualified
   dividends again, and blocked/inapplicable line 7a must block line 9 and the
   downstream taxable-income chain through declared dependencies.
6. **Package validation and forbidden reads.** Independently mutate the package
   graph to cover mixed historical/successor box-2a membership, non-`{yes,no}`
   component domains, historical recorded-box-2a collection, and raw box-2a
   reads by line 9 or QDCG. Each must reject through the production-relevant
   package/loader boundary for its intended reason. Confirm strict
   exclusive-graph and checksum behavior still reject unrelated-package or
   byte-mismatch cases.
7. **Line 16 and QDCG partition.** Recover ADR-0050 Decision 7's typed-state
   partition from the committed rules and runtime path before numeric
   comparison. Preserve blocked and guard-inapplicable states. For numeric
   line 7a `L` and qualified dividends `Q`, verify QDCG selection exactly when
   `Q>0` or `L>0`, ordinary tax only when both are closure-backed zero, and
   QDCG line 3 binds only selected line 7a. Exercise all four branch-specific
   direct-pin sets, including the declaration/conclusion-free both-zero
   ordinary branch.
8. **Pins, explanations, lifecycle, and currency.** Compare direct pins and
   citations against ADR-0050 Decision 8 without duplicating transitive
   lineage. Missing-component walks must name the exact absent set. Exercise
   same-member correction without horizon advance, membership removal with
   horizon advance, stale closure, component and conclusion correction, and
   forward/reverse correction orders. Every affected publication from line 7a
   through line 16 must displace; no historical publication may revive.
9. **Golden and test honesty.** Inventory every chartered non-presentation
   kill-test class and identify its committed test. Confirm authoritative
   integration enters through `live_coordinate_run` from a synthetic act log,
   never a hand-built `RunContext` or private reconstruction. Read assertions
   for false positives, hard-coded allowlists, broad exception acceptance, and
   mutations that fail for an unrelated earlier reason. Report every chartered
   class that lacks authoritative evidence.
10. **Regression and data safety.** Verify touched generic registry/findings,
    loader, runner, package validation, adoption/release, and contradiction
    surfaces do not weaken established behavior. Inspect the exact range for
    real/private material and run the required envelope scan. All identities
    and values must be obviously synthetic; no absolute local path or generated
    private artifact may appear.

## Verification

Run once, independently:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t2_coordinator
python3 -m unittest tests.tax.test_capital_gain_distributions_line7a_t2_package
python3 -m unittest tests.tax.test_dsbs_t3_contradiction_interlock
python3 -m unittest tests.test_dsbs_t2_coordinator
python3 -m unittest tests.test_dsbs_t3_line16_coordinator
python3 -m unittest tests.test_dsbs_t3_qdcg_declarations
python3 -m unittest tests.derivation.test_package_validation
python3 -m unittest tests.test_schema_registry
git diff --check c4f1a4934381df67ee0386911eea2abc9583f5cd..96a94d1c4c3a5490867a15fcd288b8a0fe10dab4
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

Do not run the full suite merely to duplicate CI. Use a base comparison only to
attribute a specific failure.

## Review record and verdict

Write
`docs/reviews/2026-07-29-capital-gain-distributions-line7a-track2-review.md`
and commit it on the same branch. Report one explicit verdict:

- `READY` — every required measurement passes with cited evidence; or
- `NOT READY` — numbered findings F1… identify the violated
  charter/ADR/publication/safety clause, precise file/line evidence, and a
  reproducible measurement.

Record all commands and results. Findings recommend no scope expansion and no
repair design. Do not edit implementation, manifests, charters, phase state, or
the milestone plan; do not push, open/merge a PR, or begin Track 3. Stop after
the review-record commit and return custody to the foreman.
