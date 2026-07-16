# Prototype Evaluation Analysis — Conditional Selectors

Foreman (principal), 2026-07-13. Status: **complete** (rewritten from remediated evidence; supersedes the withdrawn 2026-07-13 analysis that recommended the selector citizen — see process log for the remediation history).

## Decision under evidence

How conditional standard-deduction selection and tax-computation-method selection are modeled and resolved within the derivation cascade (CS-P1), and how their tables are represented (CS-P2).

## Evidence

| Evidence | Contribution |
|---|---|
| `it1/design.md` + `examination-it1.md` (incumbent, both shapes) | Shape A vs Shape B designs |
| Round 1R (`reviews/round-1r-*.md`, `round-1r-triage.md`) | Independent re-review: Shape A conditionally accepted, Shape B rejected as specified; executability defects in both as drafted |
| `it2/design.md` + `examination-it2.md` (clean-room rival) | Strongest Shape A form, verified by read-only evaluator execution |
| Round 2R (`reviews/round-2r-*.md`, `round-2r-triage.md`) | Both seats conditionally accept it2; optional-input impossibility claim confirmed after counterexample attempts |

The plan's rival requirement is genuinely satisfied: it2 was built clean-room (all incumbent and prior-round material denied), and each review round ran in independent contexts.

## Supported conclusions

### C1 — CS-P1 settled for the guarded-derivation subset (owner accepted 2026-07-13)
Conditional selections are modeled as rule-driven derived findings in the existing rule language — guarded rules, parameter lookups, `choose`/`all` control, canon operation citizens — with no new citizen type and no new runner pathway. All five filing statuses, age/blindness/spousal scoping, bracket folding with lower-inclusive/upper-exclusive bands, zero/negative income, and the asserted itemization override (which honestly blocks downstream rather than inventing a deduction) execute against the committed evaluator.

**Errata accepted with the design (CS-A10R/A11R):** the spouse-adjustment `all(...)` expressions must place `spouse_allowed` before the spouse-flag references so the evaluator's left-to-right short-circuit skips absent spouse inputs for Single/HoH/QSS and ineligible-MFS filers; and the design's requirement that demographic flags be explicitly asserted must be documented. Recorded here and in ADR-0024 rather than rebuilt.

### C2 — CS-P2 settled
Every amount and rate lives in a versioned parameter citizen (`p.standard-deduction`, `p.additional-deduction`, `p.brackets`); rules carry only logic, references, and control mechanics. Confirmed sound by round-2R governance (Articles 9/11).

### C3 — The optional-input absence gap is a genuine contract gap, split out
Under committed contracts there is no honest optional default: referencing an absent scalar input blocks, and a default-injecting rule silently overwrites an asserted input. The rival proved it by probe; the round-2R adversary confirmed it after refuting three counterexample constructions (staged multi-publisher rules, closure-aggregation, evaluation-order tricks). Routed to the `expression-language-extensions` topic together with categorical/string comparison (the numeric status-code workaround is executable but illegible — CS-G8R).

## Rejected alternatives

- **Shape B (first-class selector citizen), ADR-0019:** rejected — policy values embedded in logic, an optional contract matching no committed schema, an unlicensed native runner pathway, non-exhaustive cases (round 1R). ADR-0019 retained with rejected status.
- **Default-injecting rules:** rejected — silent overwrite of asserted inputs (CS-A4R, reproduced by it2's probe).

## Production conditions

- Apply the C1 errata in implementation content and tests.
- Categorical status representation upgrades from numeric codes when `expression-language-extensions` ratifies (ADR-0024 carries this as a condition).
- Package validation over the complete parameter/canon/rule corpus, adoption, and two-runner parity — implementation evidence for the rebuilt Track 3.
- Itemized-deduction package design (authority question 2) stays with roadmap content planning.
