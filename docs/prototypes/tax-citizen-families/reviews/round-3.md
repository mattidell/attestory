# Round 3 - Targeted Repair Review

Status: open. Iteration 3 is preserved as exhibit tag
`exhibits/tax-citizen-families/it3` at commit `be72d63`.

## Scope

Review it3 against `charter-it3.md`, especially its repair gates R1-R13. Use
the round-2 reviews and it2 exhibit only where needed to determine whether a
named gap was actually closed rather than restated.

The it3 prototype artifacts live under
`docs/prototypes/tax-citizen-families/it3/` at tag
`exhibits/tax-citizen-families/it3`. The examination is on `main` at
`docs/prototypes/tax-citizen-families/examination-it3.md`.

## Open Seats

- Governance reviewer: `roles/reviewer-governance.md`
- Expressiveness reviewer: `roles/reviewer-expressiveness.md`
- Adversary reviewer: `roles/reviewer-adversary.md`
- Legibility reviewer: `roles/reviewer-legibility.md` (context-starved; owner launch only)

## Required Output

- `reviews/round-3-governance.md`
- `reviews/round-3-expressiveness.md`
- `reviews/round-3-adversary.md`
- `reviews/round-3-legibility.md`

Same-round peer outputs and commit-message bodies are off-limits before
submission. Unstarved reviewers may read prior-round reviews and prior exhibits.
Expressiveness must run its reproduction checks before opening
`examination-it3.md`.

## Repair Questions

Report each applicable R1-R13 gate as closed, failed, or still disputed, with a
specific exhibit and reproduced check. In particular:

- Does W-2 source-instance identity remain peer to evidence while correction
  semantics remain coherent?
- Is closure honestly modeled and is the load-bearing `closed_sets` machinery
  dependency acceptable evidence for a contract decision?
- Is coverage actually reconstructed from authoritative records rather than a
  second state store?
- Do citation attachment and package/year validation cover every claimed
  citizen role, or only the supplied fixtures?
- Are line 1z, standard-deduction eligibility, and line 16 method boundaries
  honest enough for the included slice?
- Do all-open saturation and the five absence walks terminate in declared
  content and authoritative records?
- Can a reader traverse scenario -> package -> facts -> rules -> citations ->
  form fields without importing harness knowledge?
- Are the examination's R3 and R9 limitations ordinary implementation breadth,
  or unresolved contract boundaries that prevent ratification?

Reviewers should distinguish a passing prototype check from sufficient evidence
for a contract-foundational Tier 2 decision. Dissent must remain explicit.

## Legibility Scope

The legibility reviewer reads only `roles/reviewer-legibility.md`, this round
file, and the following files from tag
`exhibits/tax-citizen-families/it3`:

- `docs/prototypes/tax-citizen-families/it3/schemas/form-field.v1.schema.json`
- `docs/prototypes/tax-citizen-families/it3/schemas/source-citation.v1.schema.json`
- `docs/prototypes/tax-citizen-families/it3/schemas/citation-attachment.v1.schema.json`
- `docs/prototypes/tax-citizen-families/it3/schemas/symbol-binding.v1.schema.json`
- `docs/prototypes/tax-citizen-families/it3/schemas/scenario.v1.schema.json`
- `docs/prototypes/tax-citizen-families/it3/content/bundle.tax-2025.json`
- `docs/prototypes/tax-citizen-families/it3/content/form-fields.2025.json`
- `docs/prototypes/tax-citizen-families/it3/content/citations.2025.json`
- `docs/prototypes/tax-citizen-families/it3/content/citation-attachments.2025.json`
- `docs/prototypes/tax-citizen-families/it3/content/symbol-bindings.2025.json`
- `docs/prototypes/tax-citizen-families/it3/content/rules.2025.json`
- `docs/prototypes/tax-citizen-families/it3/content/parameters/standard-deduction.2025.json`
- `docs/prototypes/tax-citizen-families/it3/content/parameters/tax-rate-schedule.2025.json`
- `docs/prototypes/tax-citizen-families/it3/content/parameters/tax-table.2025.json`
- `docs/prototypes/tax-citizen-families/it3/content/package.tax-2025.json`
- `docs/prototypes/tax-citizen-families/it3/content/closure-projection.md`
- `docs/prototypes/tax-citizen-families/it3/fixtures/scenarios.json`
