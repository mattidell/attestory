# Covered Long-Term Gains, Schedule D Line 8a — Track 2 Builder Charter

Audience: Builder

Status: **chartered for owner launch**

## Context Capsule

- **Source ref and resolved launch commit:**
  `milestone/schedule-d-covered-ltcg-8a-v2`, with recovered Track 1 at
  `63e7dc0`. Orient from `HEAD`, which also contains this charter and the
  Track-2 phase pointer.
- **Exact object or commit range:** Track 2 on the milestone branch. The
  complete pre-curation state is preserved at
  `snapshot/2026-08-02-schedule-d-covered-ltcg-pre-curation`
  (`4af36ca1d4945cceeae0f7203fdca12151350f47`). Its unfinished Track-2 diff is
  permitted implementation source material, not accepted work.
- **Role:** Builder, High capability. This is a production integration track,
  not a prototype or review.
- **Scope and evidence-rung ceiling:** implement ADR-0052 Decisions 3–7,
  ADR-0053, and ADR-0054 through declared schemas, content, package wiring,
  focused tests, and production-shaped synthetic coordinator goldens. The
  ceiling is synthetic `live_coordinate_run` integration; there is no
  presentation/browser or real-data work.
- **Stop conditions:** stop if any accepted ADR, Track-1 citizen, existing
  published schema, content version, package, or manifest entry would need
  mutation; if a new generic evaluator/marshal operation beyond the accepted
  machinery is required; if the exact producer-signature pin contract cannot
  be represented without leaking an untaken branch's dependencies; if the
  work requires short-term transactions, losses, carryovers, Form 8949,
  noncovered securities, digital assets, other Schedule D sources, Track-3
  presentation, or private material; or if the recovered diff conflicts with
  the accepted contracts.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md`
  (Contracts, Fixtures, Verification, and Tracks); ADR-0052 Decisions 3–7;
  ADR-0053; ADR-0054; the plan's implementation deep reads emitted by
  `python3 tools/build_orientation_block.py --ref HEAD`; all Track-1 citizens;
  `packages/schemas/tax/attachment-rule.v2.schema.json`;
  `packages/content/tax/2025/rule.attachment.schedule-b.v3.json`;
  the current line 7a, 7b, 9, and 16 rules and QDCG bundle; core package v10
  and published-packages v5; `packages/derivation/evaluator.py`, `runner.py`,
  `marshal.py`, `package_validation.py`, and `live.py`; the Track-1 focused
  test; and `AGENTS.md`'s Schema Publication Protocol, Fixture Rules, and Data
  Safety Rules.

Before editing, echo the resolved `HEAD`, scope, evidence ceiling, immutable-
history constraint, and stop conditions.

## Goal

Make the accepted covered-long-term-gain class execute through declared,
versioned production artifacts: closed eligible transactions drive Schedule D
line 8a/13/15/16, the selected preferential base chooses the correct route,
and line 7a/9/16 publish without double counting, reach-around, or stale pins.

## Efficient recovery sequence

The interrupted pre-curation work already established useful implementation
facts. After orientation, inspect only the in-scope product/test diff between
`63e7dc0` and `4af36ca`; do not load its charters, reviews, process log, phase
state, or plan. Reuse a file only after checking it against the accepted ADRs
and the current branch. In particular:

1. Recover and verify the additive `quantity-vocabulary.v4` twin scalar
   companions, their families/closure mappings, and `attachment-rule.v3`.
2. Recover and verify Schedule D attachment/rule content and the runner's
   categorical `family_nonempty` interpretation.
3. Complete or rework the selected-preferential-base rule before building its
   consumers. The direct-producer disposition must not acquire a spurious pin
   to the proceeds family merely because the branch discriminator was tested;
   untaken-branch inputs must never be read or pinned.
4. Add the line 7a, line 9, and line 16 successors, then the coherent package
   successor and authoritative goldens.

This order is an economy aid, not permission to checkpoint an invalid package
graph as the completed track.

## Deliverables

1. **Twin scalar companions.** Publish the additive proceeds and basis scalar
   fact types, families, and closure mappings required by ADR-0054, using a new
   `quantity-vocabulary.v4` schema and add-only manifest update. Track 1's
   object-valued member remains byte-for-byte unchanged. Prove sibling identity,
   admission, correction, and independent closure behavior.
2. **Categorical attachment schema.** Publish `attachment-rule.v3` as the
   additive threshold-or-`family_nonempty` successor required by ADR-0053.
   Include a hand-written positive instance and focused negatives for each new
   constraint. Its interpreter returns required for closed-nonempty,
   not-required for closed-empty, and blocked for unclosed.
3. **Schedule D content.** Publish the attachment and rules for line 8a columns
   (d), (e), and (h), line 13, line 15, and line 16. Proceeds and basis collect
   from their scalar families; gain is `(d)-(e)`. Line 13 consumes the closed
   box-2a subtotal exactly once. Completeness uses the eligible-family closure,
   the box-2a closure, and all seven declarations, with exact missing/violated
   reasons and the ADR-0036 tie-out invariant.
4. **Selected preferential base.** Publish exactly one rule for the shared
   symbol. Its Schedule-D producer signature reads the complete Schedule D
   route; its direct producer signature reads the checked conclusion and
   closed box-2a subtotal. Each disposition carries only ADR-0052 Decision 4's
   pins for the producer actually selected. Package validation continues to
   reject duplicate publishers.
5. **Successor routing.** Publish the additive line-7a, line-9, and line-16
   successors required by ADR-0052. Line 7a consumes the selected base once;
   line 9 consumes line 7a once; line 16 substitutes the selected preferential
   base while preserving the existing QDCG/ordinary partition and branch-
   specific direct-route authorities. Do not version line 7b unless evidence
   disproves the accepted conclusion that it remains unchanged.
6. **Coherent package graph.** Publish core-calculations v11 and
   published-packages v6 (plus only the synthetic release/adoption artifacts
   actually needed). Preserve v10/v5 resolution. Reject mixed-current,
   raw-reach-around, duplicate-producer, invalid-boundary-domain, and stale-
   authority graphs.
7. **Authoritative synthetic evidence.** Add focused schema/content/package
   tests and `live_coordinate_run` goldens from an act log for the plan's
   non-presentation fixture classes: single and multiple transactions/brokers;
   each boundary authority missing or violated; box-2a nonzero and closed-empty;
   family lifecycle and forward/reverse corrections; both producer signatures;
   QDCG/ordinary selection; and rejection cases. Inspect every golden and
   manifest diff.

## Boundary

No presentation or browser work, UI redesign, real session, filing,
transmission, historical migration, or broader Schedule D class. Do not edit
accepted ADRs, Track-1 citizens, or published history. Add unused versions and
manifest rows only. Do not copy prototype pseudocode into production; implement
against the accepted contracts and current engine patterns.

## Verification before handoff

Run touched focused modules while iterating, then once before handoff:

```text
python3 -m unittest tests.test_schedule_d_covered_ltcg_8a_t1_citizens
python3 -m unittest tests.test_schema_registry
python3 -m unittest tests.derivation.test_package_validation
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
git diff --check main..HEAD
```

Run the full local gate at most once if useful; CI is the gate of record.

## Handoff

Commit the complete working state as one atomic Track-2 implementation commit.
Temporary checkpoints and fixes are allowed during development, then folded
into that commit before independent review. Leave the tree clean and report
the SHA, changed surfaces, focused results, golden entrypoint evidence,
manifest inspection, selected-preferential-base identifier and exact pins,
what was adopted versus reworked from the snapshot, and any charter-stop
finding. Do not review your own work, begin Track 3, or open another PR.
