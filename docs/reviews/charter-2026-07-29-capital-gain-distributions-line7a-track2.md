# Capital-Gain Distributions / Line 7a — Track 2 Production Builder Charter

Audience: Builder.

Status: **prepared for launch only after Track-1 PR #111 reaches `main` with
CI `verify` green.**

## Context Capsule

- **Source ref and resolved launch commit:** `main`, resolved at launch to the
  no-fast-forward merge commit for Track-1 PR #111. The Builder must fetch and
  verify that `6b5321b6639b403476c4b4a1331efcc60261e3bb` is an ancestor of
  `origin/main`; otherwise stop without creating the implementation branch.
- **Exact object or commit range:** create
  `track/capital-gain-distributions-line7a-track2` from that resolved
  `origin/main` commit. Do not continue building on the spent Track-1 branch.
- **Role:** one Builder, High tier / high effort. This is a contract-dense
  production integration track, not a prototype or review.
- **Scope and evidence-rung ceiling:** implement ADR-0050's declared rules,
  admission/package interlocks, package successor, coordinator integration,
  lifecycle behavior, explanations, and authoritative synthetic goldens for
  line 7a → line 9 → taxable income → line 16. Production-shaped synthetic
  integration is the ceiling. No presentation/browser or real-data work.
- **Stop conditions:** stop and report if PR #111 is not merged with green
  `verify`; if an accepted historical schema/content/package/ADR would need
  mutation; if a new evaluator operation, generic substrate, or governance
  interpretation appears necessary; if the accepted branch/state/pin topology
  cannot be represented by existing declared machinery; if Schedule D,
  Form 8949, Form 1099-B, excluded-box computation, UI redesign, or Track-3
  presentation becomes necessary; or if any real/private material would be
  needed.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md`;
  `docs/adr/0050-capital-gain-distributions-and-line-7a.md`;
  ADR-0010, ADR-0011, ADR-0012, ADR-0020, ADR-0023, ADR-0024, ADR-0025,
  ADR-0027, ADR-0029, ADR-0032, ADR-0035, ADR-0037, ADR-0038, and ADR-0046
  only where the implementation turns on their exact accepted text;
  all Track-1 production citizens;
  `packages/content/tax/2025/rule.form1040-line9.v2.json`;
  `packages/content/tax/2025/rule.form1040-line16.v2.json`;
  `packages/content/tax/2025/qdcg.bundle.json`;
  `packages/derivation/live.py`;
  `packages/derivation/runner.py`;
  `packages/derivation/marshal.py`;
  `packages/derivation/package_validation.py`;
  `packages/tax/loader.py`;
  `tests/test_dsbs_t2_coordinator.py`;
  `tests/test_dsbs_t3_line16_coordinator.py`;
  `tests/test_dsbs_t3_qdcg_declarations.py`;
  `tests/tax/test_dsbs_t3_contradiction_interlock.py`;
  `AGENTS.md#Schema Publication Protocol`;
  `AGENTS.md#Fixture Rules`; and `AGENTS.md#Data Safety Rules`.

Before editing, echo the resolved `main` SHA and PR-#111 ancestry proof, the
Track-2 scope and ceiling, authoritative golden entrypoint, immutable-history
constraint, and every stop condition.

## Goal

Make the accepted direct-reporting class execute entirely through declared,
versioned production artifacts: authoritative box-2a source and Exception-1
facts publish line 7a/7b, line 9 includes line 7a once, and line 16 selects the
accepted QDCG or ordinary branch with exact dispositions and pins.

## Deliverables

1. **Checked conclusion and line 7b.** Load/admit the Track-1 C1–C4 and
   checked-conclusion citizens. Derive the conclusion from exactly C1–C4:
   missing components block with the exact missing set; all four `"yes"`
   produce conclusion `"no"`; any current `"no"` produces conclusion `"yes"`.
   Publish line 7b's affirmative Schedule-D-not-required disposition only from
   conclusion `"no"` and pin its exact citation once.
2. **Box-2a family and line 7a.** Add the declared box-2a collect/subtotal and
   line-7a production artifacts over the successor family/closure mapping.
   A closed-empty family publishes closure-backed zero; open, undeclared, or
   stale closure blocks; multiple statements sum once; same-member correction
   without horizon advance and membership removal with horizon advance obey
   ADR-0023/ADR-0010 displacement.
3. **Direct-route disposition.** Line 7a publishes the selected subtotal only
   when the checked conclusion is `"no"`. Missing authority is
   `blocked(DEPENDENCY_ABSENT)` with the exact missing set. Conclusion `"yes"`
   is `guard_inapplicable`. Neither state becomes zero or fabricates a Schedule
   D/Form 8949 artifact.
4. **Signal and admission interlock.** Re-home
   `CAPITAL_GAIN_DISTRIBUTION_RECORDED` to current non-null successor box-2a
   members. Preserve pre-mutation rejection against a current
   `capital-gain-distributions="no"` declaration in declaration-first,
   signal-first, and same-batch orders. Null/residual historical content may
   not masquerade as the successor signal.
5. **Package validation and successor package.** Publish a new package/content
   successor without changing history. Reject mixed historical/successor
   box-2a graphs, non-`{yes,no}` component domains, and any rule that collects
   historical recorded box 2a or raw box-2a members into line 9 or QDCG.
   Downstream consumers use selected publications only. Preserve strict
   exclusive-graph and checksum behavior.
6. **Line-9 successor and displacement chain.** Publish a new line-9 rule
   version that adds the selected line-7a publication exactly once to its
   existing inputs. Do not add qualified dividends again or read raw box 2a.
   Lines 11/12/15 and taxable income recompute through their existing declared
   dependencies. A blocked or guard-inapplicable line 7a makes line 9
   `blocked(DEPENDENCY_ABSENT)` on selected line 7a and blocks taxable income
   through line 9.
7. **Line-16/QDCG successor.** Implement ADR-0050 Decision 7's typed state
   partition before numeric comparison. Preserve blocked and
   guard-inapplicable states. For numeric line 7a `L` and qualified dividends
   `Q`, select QDCG when `Q>0` or `L>0`; select ordinary tax only when both are
   closure-backed zero. QDCG line 3 binds only selected line 7a. Implement the
   four branch-specific declaration/conclusion direct-pin sets exactly,
   including R2-Q3's declaration/conclusion-free ordinary branch.
8. **Pins, explanations, and correction currency.** Enforce ADR-0050 Decision
   8's direct-pin graph and exact citations without duplicating transitive
   lineage. Missing-component walks name the exact absent set. Forward and
   reverse component/member/closure/conclusion corrections displace the full
   line 7a → 9 → taxable-income → 16 chain and never revive displaced history.
9. **Authoritative synthetic goldens.** Add production-shaped synthetic
   coordinator-from-facts goldens through `live_coordinate_run` from an act
   log—never a hand-built `RunContext`—for every non-presentation kill-test
   class in ADR-0050 Decision 8: individual and all-component absence; each
   component `"no"`; single/multi-payer and closed-empty; open/stale closure;
   all contradiction orders; mixed graph and forbidden raw reads; blocked and
   guard-inapplicable line-9 propagation; QDCG Q/L partition and exact pin
   branches; exact line-7b citation; and forward/reverse correction chains.

## Boundary

No presentation projection or product-page/browser work (Track 3); no real
session; no Schedule D/Form 8949/1099-B or excluded-box family; no filing or
transmission; no UI redesign; no historical migration. Do not edit accepted
ADRs, published historical schemas, manifests entries, content versions, or
packages. Add new unused versions and manifest rows only where a new schema is
actually necessary; a new evaluator operation or generic substrate is a stop,
not an implicit extension.

## Verification before handoff

Create focused Track-2 modules for coordinator, lifecycle, package validation,
and admission behavior, and run each while iterating. Also run once:

```text
python3 -m unittest tests.test_dsbs_t2_coordinator
python3 -m unittest tests.test_dsbs_t3_line16_coordinator
python3 -m unittest tests.test_dsbs_t3_qdcg_declarations
python3 -m unittest tests.tax.test_dsbs_t3_contradiction_interlock
python3 -m unittest tests.derivation.test_package_validation
python3 -m unittest tests.test_schema_registry
git diff --check main..HEAD
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

Run only touched focused modules while iterating; do not repeatedly run the full
suite. CI `verify` is the gate of record. Inspect every intentional golden and
manifest diff before handoff.

## Handoff

Commit the complete Track-2 implementation as one implementation commit after
the charter/base commit. Leave the worktree clean and report the SHA, exact
files, focused results, golden entrypoint evidence, manifest inspection, and
any charter-stop finding. Do not review the work, push, open a PR, begin Track
3, or modify the charter/pointers. The foreman will charter an independent
Track-2 review.
