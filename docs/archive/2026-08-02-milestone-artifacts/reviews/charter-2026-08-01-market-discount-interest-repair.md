# Payer-Reported Current-Inclusion Market-Discount Interest — Findings-Only Repair Charter

Audience: Builder.

Status: **chartered for owner launch.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `milestone/market-discount-interest` at
  `9334cca21e50bcf7f603b56d60d757aab72cc1ad`; verify the resolved SHA against
  Git before acting.
- **Object:** repair the two findings recorded in
  `docs/archive/2026-08-02-milestone-artifacts/reviews/review-2026-08-01-market-discount-interest.md` and the red
  `verify` run for PR #134. This is the one permitted findings-only repair
  cycle.
- **Role and tier:** one Builder, Medium/medium. Do not spawn sub-agents.
- **Scope and evidence ceiling:** update the stale current-version expectation
  for the selected line-2b field citizen; retain the historical v3 assertion
  where it describes the schema; remove the copied malformed presentation
  artifact and stop its generator from recreating it; preserve the in-memory
  MD-N12 mutation and one canonical positive golden. Focused local tests only.
- **Stop conditions:** stop if product content, runtime behavior, published
  schema history, package selection, a second malformed golden, or a new
  presentation behavior appears necessary; if another independent failure
  appears; if the worktree is dirty at launch; or if real/private data is
  encountered. Return the scope to the Foreman rather than widening it.

## Deliverables

1. In `tests/test_dsbs_t1_schema_citizens.py`, rename the affected method to
   describe the current line-2b field citizen and change only its current
   version expectation from `v3` to `v4`. Preserve the `form-field.v3` schema
   assertion, disposition-code assertions, and historical compatibility tests.
2. In `tools/generate_market_discount_interest_goldens.py`, generate only the
   canonical positive golden. Remove the copied malformed-model output and
   related dead code.
3. Remove
   `packages/sample_data/market_discount_interest/presentation/malformed-market-discount-line2b.presentation-model.v1.json`.
   Keep `mixed-market-discount.presentation-model.v1.json` unchanged unless
   deterministic regeneration proves it differs for a legitimate reason.
4. Do not edit phase state, the milestone plan, the review, or the retrospective;
   the Foreman owns those records.

## Focused verification

Run each command once:

```text
python3 -m unittest tests.test_dsbs_t1_schema_citizens
python3 -m unittest tests.test_market_discount_interest_integration
git diff --check 9334cca21e50bcf7f603b56d60d757aab72cc1ad..HEAD
```

Do not run the full suite. The replacement PR `verify` run is the gate of
record. Return the repair commit identity, focused results, and self-reported
turn and tool-call counts to the Foreman.
