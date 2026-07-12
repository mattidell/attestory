# Round 4 - Bounded Integration Review

Status: closed; owner disposition pending. Iteration 4 is preserved as exhibit
tag `exhibits/tax-citizen-families/it4` at commit `9debc4d`.

## Scope

Review it4 against `charter-it4.md` v2. The question is whether I1-I9 now
provide sufficient end-to-end evidence for the tax citizen-family contract,
and whether the explicitly escalated `closed_sets` machinery limitation blocks
the contract-foundational Tier 2 decision or can be isolated as a required
production machinery patch.

The it4 prototype artifacts live under
`docs/prototypes/tax-citizen-families/it4/` at tag
`exhibits/tax-citizen-families/it4`. The examination is on `main` at
`docs/prototypes/tax-citizen-families/examination-it4.md`.

## Open Seats

- Governance reviewer: `roles/reviewer-governance.md`
- Expressiveness reviewer: `roles/reviewer-expressiveness.md`
- Adversary reviewer: `roles/reviewer-adversary.md`
- Legibility reviewer: `roles/reviewer-legibility.md` (context-starved; owner launch only)

## Required Output

- `reviews/round-4-governance.md`
- `reviews/round-4-expressiveness.md`
- `reviews/round-4-adversary.md`
- `reviews/round-4-legibility.md`

Same-round peer outputs and commit-message bodies are off-limits before
submission. Unstarved reviewers may read prior-round material. Expressiveness
must run its reproduction and independent probes before opening
`examination-it4.md`.

## Integration Questions

Report every I1-I9 gate as closed, failed, or still disputed, with commands and
specific exhibits. In particular:

- Does the normal path truly begin with acts and current projected findings,
  pass through adoption-gated `run_and_record`, append publications, and read
  ADR-0010 composed currency?
- Are closure, eligibility, and method symbols produced only by adopted and
  pinned rules, with direct fixture truth rejected?
- Does the W-2 correction exercise same-fact supersession, downstream
  displacement, and re-derivation without collapsing a second slip?
- Do package/provenance checks resolve every claimed citizen role and reject
  mixed-year substitutions rather than checking strings selectively?
- Are coverage and all five explanations derived from actual persisted records
  and pins, without hard-coded maps or indexes becoming authority?
- Is citation role/subject/year enforcement declared, adopted where necessary,
  and resistant to schema-valid semantic mismatches?
- Do committed relationship examples and bypass probes cover the relationships
  named by charter v2, not merely the supplied happy path?
- Does the scalar rewrite of closure/eligibility/method fact values preserve the
  intended meaning, or discard required condition structure?
- Is the `closed_sets` escalation a separable machinery implementation
  condition, or proof that the proposed contract still depends on an
  unmodeled/unadopted authoritative input?

Reviewers must distinguish prototype evidence, a production ratification
condition, and an unresolved contract decision. Dissent remains explicit.

## Legibility Scope

The legibility reviewer reads only `roles/reviewer-legibility.md`, this round
file, and the following files from tag
`exhibits/tax-citizen-families/it4`:

- `docs/prototypes/tax-citizen-families/it4/schemas/citation-attachment.v1.schema.json`
- `docs/prototypes/tax-citizen-families/it4/schemas/symbol-binding.v1.schema.json`
- `docs/prototypes/tax-citizen-families/it4/schemas/scenario.v1.schema.json`
- `docs/prototypes/tax-citizen-families/it4/content/bundle.tax-2025.json`
- `docs/prototypes/tax-citizen-families/it4/content/rules.2025.json`
- `docs/prototypes/tax-citizen-families/it4/content/package.tax-2025.json`
- `docs/prototypes/tax-citizen-families/it4/content/symbol-bindings.2025.json`
- `docs/prototypes/tax-citizen-families/it4/content/citation-resolver.v1.json`
- `docs/prototypes/tax-citizen-families/it4/content/citation-attachments.2025.json`
- `docs/prototypes/tax-citizen-families/it4/content/closure-projection.md`
- `docs/prototypes/tax-citizen-families/it4/fixtures/scenarios.json`
- `docs/prototypes/tax-citizen-families/it4/spikes/integration-substrate.md`
- `docs/prototypes/tax-citizen-families/it4/instances/positive/rule.projection.json`
- `docs/prototypes/tax-citizen-families/it4/instances/negative/rule.projection-no-require.json`
- `docs/prototypes/tax-citizen-families/it4/instances/positive/finding.w2-correction.json`
- `docs/prototypes/tax-citizen-families/it4/instances/negative/finding.w2-correction-different-fact.json`
- `docs/prototypes/tax-citizen-families/it4/instances/positive/package-member.projection.json`
- `docs/prototypes/tax-citizen-families/it4/instances/negative/package-member.role-mismatch.json`
- `docs/prototypes/tax-citizen-families/it4/instances/positive/coverage.expected.json`
- `docs/prototypes/tax-citizen-families/it4/instances/negative/coverage.stale.json`
- `docs/prototypes/tax-citizen-families/it4/instances/positive/explanation.closure-zero.expected.json`
- `docs/prototypes/tax-citizen-families/it4/instances/negative/explanation.fabricated.json`
- `docs/prototypes/tax-citizen-families/it4/instances/negative/scenario.dangling-package.json`
- `docs/prototypes/tax-citizen-families/it4/instances/negative/citation-attachment.wrong-year-reverse.json`
- `docs/prototypes/tax-citizen-families/it4/instances/negative/citation-attachment.wrong-role.json`
- `docs/prototypes/tax-citizen-families/it4/instances/negative/citation-attachment.wrong-subject.json`
