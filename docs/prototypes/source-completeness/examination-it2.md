# Examination: Source Completeness Iteration 2

Date: 2026-07-12

Rung: 1 — static documents only

## Evidence inventory

- Design: `it2/design.md`
- Governance authority: Constitution Articles 1, 4, 7, 9–15; Ontology fact
  type, finding, adoption, rule artifact, run, currency, and two-edge entries;
  Engineering Constraints E1.1, E4.1, E7.1–2, E11.1–3, E12.1, E14.1, E15.1.
- Accepted boundary: ADR-0011 decisions 4–6 and its explicit “Not Decided”
  list.
- Primary tax material: IRS Instructions for Forms 1099-INT and 1099-OID
  (January 2024), account-number instruction; IRS Publication 1099 (2026),
  corrected-return account-number instruction. Consulted 2026-07-12.
- Fixture provenance: manufactured solely for this iteration; years, names,
  identifiers, labels, and amounts are visibly synthetic.

## Pre-declared check results

1. **Concrete Gate 2 fixtures — pass.** Interest and W-2 positives name
   artifacts, families, closure findings, and outcomes. False, displaced,
   absent, caller-injected, payer-collision, and document-key negatives resolve
   to explicit outcomes. No placeholder remains.
2. **Genuine rivalry — pass.** Mapping is an immutable parameter embedded in
   and adopted with each collecting rule, with no independently lifecycled
   mapping citizen. Identity is keyed by a logical statement-instance citizen,
   not an account composite.
3. **Affirmative-only against two-layer `collect` — pass on paper.** Layer 1
   reads members; only a projection that resolves the current closure finding
   and compares its value to literal `true` may satisfy Layer 2 for emptiness.
   Finding presence alone never admits membership.
4. **No evidence/document identity — pass.** The chosen identity has no source
   citizen or file id. The statement instance is explicitly a peer logical
   reporting event; PDFs and scans remain evidence.
5. **Zero explanation reaches closure — pass.** The positive pin walk reaches
   the exact true closure finding and its assertion act, plus the rule,
   embedded parameter, adoption, and run.
6. **Negatives fail as declared — pass on paper.** False fails value equality;
   displaced fails currency (and its current false successor fails equality);
   absent fails current-finding resolution; caller injection lacks declared
   authority; payer-only collides; document-key violates Article 1/E1.1.

## Proposition dispositions

### SC-P1 — supported at rung 1, execution caveat disclosed

The adopted-parameter shape expresses affirmative-only authority, pins the
closure finding into an empty-source zero, generalizes unchanged to W-2, and
has a complete correction/displacement/rerun lifecycle. It is distinguishable
from a dedicated mapping citizen: reuse requires repeated parameter content,
and any mapping change versions and re-adopts the whole collecting rule.

Paper does not measure whether the production evaluator's real projection is
free of a value-insensitive adapter. The design therefore supports the contract
shape but cannot close the plan's sole execution question.

### SC-P2 — supported at rung 1

The statement-instance key distinguishes one payer's two furnished statements,
preserves correction as a new finding of the same fact, and cleanly separates
logical statement identity from evidence. Payer-only demonstrably collides.
Account-composite is a genuinely different semantic choice, not a parameter
variation: it selects an account rather than an information-return statement as
the source instance.

Production condition: define how assertion individuates a stable logical
statement instance when payer metadata is sparse, without deriving that
identity from evidence. This is schema/content work, not permission to use a
file key.

### SC-P3 — supported at rung 1

The definition is stated once and exercised by both closure mappings and by the
repeatable statement instances. It stores neither member enumeration nor
coverage state, avoiding a second authoritative representation.

## Negative-result summary

| Case | Failed predicate | Required result |
|---|---|---|
| current false closure | value is literal `true` | Layer 2 blocks |
| displaced historical true | finding is current | Layer 2 blocks |
| no closure finding | current finding exists | Layer 2 blocks |
| caller-supplied closed family | authority is adopted artifact projection | reject/ignore injection; block |
| payer-only interest key | distinct statements have distinct facts | reject key |
| evidence-file interest key | identity excludes evidence | reject key |

## Rung recommendation

Stop SC-P2 and SC-P3 at rung 1: paper distinguishes the rivals and identifies a
bounded production condition. For SC-P1 only, recommend—not authorize—the
plan's next rung because the one declared open question is executable: rung 2
validator/resolver mutations should test true, false, absent, and displaced
closure against the adopted parameter projection. Rung 3 should be considered
only if rung 2 cannot expose a presence-only adapter. No rung 4 work is
recommended or authorized.
