# Independent review — exact family-version closure authority

Audience: Foreman.

- Reviewer: fresh Grok 4.7. No production edits, subagents, or Git writes.
- Source ref checked at launch: HEAD `627ada0a66ea85d12db2708a54f09c5f0aa9e9cb` on `milestone/multiple-statement-circumstances-consolidation`. Working tree porcelain was empty.
- Candidate `34ca5860562a2d7cbbce9012a3a84b0e6c439ee6` is an ancestor of that HEAD. The range `1893749a..34ca5860` is one commit and five files. Those five files are unchanged between the candidate and HEAD.
- Object: that range only. Sale Track 0 and the milestone are outside this verdict.

## Box

Adopted closure mappings and recorded horizon chains enter `marshal_closure_authority`. A closure may authorize a family only when it is the single current literal-true finding on the horizon of the mapping's exact family id and version. Run admission and `coverage_report` consume that pair. Another version's horizon must not supply the selected version, and two scopes of the selected version must still refuse. Historical v1 wash-sale acts stay in the log. This unit does not accept sale production, a migration act, or a general rollback framework.

## Verdict

**REPAIR REQUIRED.**

Exact-version selection and the fresh synthetic v2 attestations are in place for the static cases that were read and for the fixture scan below. They are not sufficient. An executed later member-transition on the unselected version leaves the selected version's earlier closure admitted and a derived zero pinned to that closure current, while the new member is also current.

## Finding 1 — selected closure and its zero stay current after the other version's transition

- Claim violated: a current member of a family's predicate displaces that family's closure and any closure-backed zero (`ADR-0017` decisions 3 and 5; `ADR-0023` consequence; `ADR-0014` decision 5). The shared-authority charter also requires membership succession to displace the old closure. Exact version selection does not keep that displacement when both versions already have closure.
- This is a real counterexample of the guard's new coexistence path. It is not a request for a migration or rollback framework. No predecessor type is retired, and no migration artifact is involved. One ordinary `member-transition` on the other version of the same predicate is enough.
- What this commit newly allows: the pre-change horizon fold, reconstructed from the candidate diff and executed on the same state, raises `SourceAuthorityError` (`family ... has horizon chains in multiple scopes`). After the guard, marshal admits the stale selected closure. Derivation currency itself was not in the diff; an already recorded zero stays current because only the named chain's horizon is an individuation root (`packages/kernel/horizons.py` `apply_transition`; `packages/kernel/findings.py` `apply_member_transition`; `packages/derivation/projection.py` `compute_derivation_currency`). The new defect is successful admission of that closure.
- Consequence: lifecycle. Coverage stays closed and a later run can still treat the old closure as authority. The fresh numeric subtotal of a full coordinator run was not executed, so this finding does not claim that the next run still prints `0.0`. Present-source collection is a separate number. The measured failure is admission, coverage, and currentness of the earlier pinned zero.
- Smallest repair property: if a later transition introduces a current member of the selected family's predicate on another version's chain, that selected closure is not admitted and a derived zero pinned to it is not current. Keep the selected-version control: a transition that names the selected chain still opens that chain. Do not add a migration act. If the mechanism belongs in kernel admission rather than `marshal_closure_authority`, that choice stays with the Foreman.

Executed probe (not a committed test), family `tax.us.2025.f1099b.covered-w-st-proceeds`. v1 and v2 predicates are the same fact type, `tax.us.2025.f1099b.covered-w-st-txn.proceeds`. Both versions have horizon genesis and a literal-true closure. A `derived-publication` value `0.0` pins role `input` to `demo.closure.proceeds.v2` (the dependency role `packages/derivation/runner.py` writes on a closure pin). Then a member-transition names only v1 and asserts proceeds `1000.0`.

| Case | Result |
| --- | --- |
| Both closed, v2 mapping | v2 horizon `demo.wst-p.v2.h0` admitted, coverage `closed`, both closure findings current, v2 zero current. Old fold raises the multiple-scope error. |
| Later transition on unselected v1 | v2 still admitted on `demo.wst-p.v2.h0`, coverage `closed`, `demo.closure.proceeds.v2` current, v2 zero current and not displaced, member `f.proceeds.v1` current, v1 closure not current. Old fold still raises. |
| Later transition on v2 while the adopted mapping is v1 | v1 horizon `demo.wst-p.v1.h0` admitted, v1 closure current, v1 zero current. The v2 zero is displaced. |
| Control: transition names selected v2 | horizon `demo.wst-p.v2.h1`, not admitted, coverage `open`, v2 closure not current, v2 zero displaced, member current. |

The committed succession test only transitions the selected v2 chain (`tests/source_completeness/test_exact_family_version.py`, member-transition on `version: "v2"`). It does not observe the unselected chain.

## Verified, for a bounded repair to preserve

- All eight wash-sale declaration pairs: `closure_claim`, `member_predicate`, and `authorizes_subtotal` match. Parent v2 adds `member_constraints` and `identity_exclusivity`. Scalar v2 adds `projects_from`. Helper closure fact types match the v2 mappings. `package.core-calculations.v48.json` adopts these eight families and mappings at v2.
- `append_wash_sale_v2_empty_authority` on `_make_base_acts(include_v2_empty_authority=False)`: 185 acts before, 201 after, prefix identical, eight v1 horizons left on `demo.ug.*` ids, no member fact of those eight predicates, appended closures are `True`, no act-id or horizon-id collision. Historical `_ug_acts` v1 genesis is not rewritten. The helper is test-only.
- Same-version duplicate mappings: `marshal_closure_authority` does not raise; `resolve_closure_admissions` raises `duplicate mapping authority`. A v2 mapping paired with the v1 declaration raises the version pin error in `validate_mapping_against_family`. The committed test raises only for v1-versus-v2 mappings inside marshal.
- A v1-only chain is omitted from `current_horizons` for a v2 mapping by the new loop in `packages/derivation/marshal.py` (about lines 294–322). Two scopes of one selected version still raise when `len(matching) > 1`. Those two committed tests were read, not re-run.

## Incomplete

- Saved `out.json` of `test_real_coordinator_v1_only_vs_fresh_v2_empty_authority` was not executed and its bytes were not read. Source trace only: an unadmitted family makes `_evaluate_family_validation` block with that family id missing; proceeds v2 `projects_from` the constrained parent, so `compile_validation_graph` adds the parent `.member-validation` symbol to `requires`; the ordinary rule path records `DEPENDENCY_ABSENT` for a missing `requires` entry before the authored `SOURCE_SET_UNCLOSED` body. The test's `0.0` assertion reads in-memory publications. The saved input pin version `v1` matches the hardcoded closure-pin version in `runner.py`, while the mapping and declaration pins are v2. This does not by itself make a sale or migration claim. The builder's pass counts were not re-run and are not evidence.
- Neighbor callers of `_make_base_acts` (`tests/test_f1099k_computation_rules.py`, `tests/test_f1099k_personal_item_sale_demonstration.py`, `tests/test_f1099k_statement_review.py`, and the other track-1 paths) were not executed. Full CI remains the broad gate.
- No full suite, lifecycle file, historical v20 file, mypy, or envelope scan was run in this review.

## Next check

Re-measure the unselected-v1 proceeds case after a bounded repair: v2 must not be admitted, and the derived zero pinned to `demo.closure.proceeds.v2` must be displaced, while the selected-v2 control still opens `demo.wst-p.v2.h1`. Do not open with a full suite.
