# Round 2 - Comparative Rival Review

Status: open. Iteration 2 is built on branch
`prototypes/tax-citizen-families/it2` at commit `989d9fe`.

## Scope

Review it2 against `charter-it1.md` v3 and compare it to it1 only where the
comparison is needed to answer the contract decision. The it1 exhibit is tag
`exhibits/tax-citizen-families/it1` at `88f0139`; the it2 branch is
`prototypes/tax-citizen-families/it2` at `989d9fe`.

The it2 prototype artifacts live under
`docs/prototypes/tax-citizen-families/it2/` on the it2 branch. The examination
is on `main` at `docs/prototypes/tax-citizen-families/examination-it2.md`.

## Open Seats

- Governance reviewer: `roles/reviewer-governance.md`
- Expressiveness reviewer: `roles/reviewer-expressiveness.md`
- Adversary reviewer: `roles/reviewer-adversary.md`
- Legibility reviewer: `roles/reviewer-legibility.md` (context-starved; owner launch only)

## Required Output

- `reviews/round-2-governance.md`
- `reviews/round-2-expressiveness.md`
- `reviews/round-2-adversary.md`
- `reviews/round-2-legibility.md`

Same-round peer outputs and commit-message bodies are off-limits before
submission. Unstarved reviewers may read round-1 reviews and it1 artifacts as
prior-round material. Expressiveness must run its reproduction checks before
opening `examination-it2.md`.

## Comparative Questions

Reviewers should preserve measurement discipline and avoid scalar winner
language. Useful comparison axes:

- Does it2 close or sharpen the it1 findings on incomplete F3/F6 coverage,
  1040 line 1z, standard-deduction/line-16 guard defaults, engagement identity,
  invalid source values, citation resolution, mixed-year consistency, stale
  coverage, and scenario-as-proof?
- Does it2 introduce new defects, especially by relying on machinery behavior,
  choosing fewer new citizen families, or encoding closure as elective facts?
- Which conclusions now have convergent evidence across both designs?
- Which conclusions remain disputed or require a third iteration?

## Legibility Scope

The legibility reviewer reads only `roles/reviewer-legibility.md`, this round
file, and the following branch files:

- `docs/prototypes/tax-citizen-families/it2/schemas/form-field.v1.schema.json`
- `docs/prototypes/tax-citizen-families/it2/schemas/source-citation.v1.schema.json`
- `docs/prototypes/tax-citizen-families/it2/content/bundle.tax-2025.json`
- `docs/prototypes/tax-citizen-families/it2/content/form-fields.2025.json`
- `docs/prototypes/tax-citizen-families/it2/content/citations.2025.json`
- `docs/prototypes/tax-citizen-families/it2/content/rules.2025.json`
- `docs/prototypes/tax-citizen-families/it2/content/parameters/standard-deduction.2025.json`
- `docs/prototypes/tax-citizen-families/it2/content/parameters/tax-rate-schedule.2025.json`
- `docs/prototypes/tax-citizen-families/it2/content/package.tax-2025.json`
- `docs/prototypes/tax-citizen-families/it2/fixtures/scenarios.json`

