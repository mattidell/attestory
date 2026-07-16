# ADR 0024 — Conditional Structures in the Rule Language

- Status: **accepted** (owner ratification 2026-07-13, principal foreman custody)
- Tier: 2
- Date: 2026-07-13

## Context

Standard-deduction selection and tax-computation-method selection require multidimensional conditional branching (five filing statuses, age/blindness/spousal adjustments, bracket tables, an asserted itemization override). ADR-0019 proposed a first-class selector citizen for this and was rejected on independent round-1R evidence (see its rejection note). The remediated conditional-selectors prototype — clean-room rival iteration 2, reviewed in two independent rounds — settled the question in the opposite direction: the existing rule language suffices for the whole conditional subset, and the one genuine gap it cannot cover is not about selection at all but about optional-input absence.

Evidence: `docs/prototypes/conditional-selectors/evaluation-analysis.md` (rewritten 2026-07-13) and the round-1R/2R reviews and triages it cites. Owner accepted iteration 2 with errata on 2026-07-13.

## Decision

1. **Conditional selections are rule-driven derived findings in the existing rule language.** Guarded rule artifacts, `choose`/`all` control expressions, and parameter lookups model standard-deduction selection and tax-method selection. No selector citizen, no new runner pathway, no new edge kind.

2. **All policy values live in versioned parameter citizens.** Deduction bases, additional-deduction amounts, and bracket tables are structured parameter citizens (`p.standard-deduction`, `p.additional-deduction`, `p.brackets`) that rules reference; rules carry only logic, references, and control mechanics (CS-P2).

3. **Canon operation citizens are mandatory content.** Every operation an expression uses (`round`, `bracket_fold`, …) must ship its `operation-semantics.v1` citizen in the package; bracket tables use the canon row shape (`lower`/`upper`/`rate`) with lower-inclusive/upper-exclusive bands and clamping at zero via explicit `max(0, …)` rules.

4. **Guard-order errata (CS-A10R/A11R).** Expressions that combine an eligibility guard with a possibly-absent input must place the guard first (`all(spouse_allowed, EQ(R("spouse_age65"),1), …)`) so the evaluator's left-to-right short-circuit skips absent references for statuses where the branch is inapplicable.

5. **Explicit-assertion requirement (interim).** Taxpayer demographic flags (`taxpayer_age65`, `taxpayer_blind`) and — when the status makes spouse adjustments applicable — spouse flags must be explicitly asserted, even as zero. No runner-resident defaulting exists or is permitted (Articles 7/11). This is an interim contract: the declared absence/default mechanism is delegated to the `expression-language-extensions` decision topic.

6. **Interim categorical representation.** Filing status is carried as numeric-string codes ("1"–"5") because the committed evaluator's `compare` coerces operands to decimals. This is executable but a recognized legibility concession (CS-G8R); it upgrades to a first-class categorical comparison when `expression-language-extensions` ratifies one.

7. **The itemization override blocks honestly.** An asserted itemization election makes the standard-deduction rule guard-inapplicable; downstream taxable-income and tax rules block on the missing dependency rather than inventing a zero, until an itemized-deduction package is adopted.

## Consequences

- Track 3 rebuilds on existing contracts: rules, parameters, canon citizens — no engine change is a prerequisite for the conditional subset itself.
- Decisions 5 and 6 make this ADR's contract deliberately partial: absence/defaults and categorical comparison are owned by `expression-language-extensions`, and content written under this ADR upgrades when that topic ratifies.
- Graph density is bounded by composable guarded rules and parameter tables rather than a consolidated selector artifact; exhaustiveness across the five statuses is carried by parameter-table keys, not case lists.

## Alternatives Considered

- **First-class selector citizen (ADR-0019).** Rejected: embedded policy values, an optional contract matching no committed schema, an unlicensed native runner pathway, non-exhaustive cases; see ADR-0019's rejection note and round-1R.
- **Default-injecting rules for optional inputs.** Rejected: silently overwrite asserted inputs (CS-A4R; reproduced by iteration 2's probe).
- **Post-hoc coercion workarounds for categorical comparison beyond the interim codes.** Rejected: schema acceptance is not runtime conformance (round-1R CS-G1R); the durable fix is a language-level decision.

## Links

- Evidence: `docs/prototypes/conditional-selectors/evaluation-analysis.md`; rounds 1R/2R reviews and triages; `it2/design.md`, `examination-it2.md`.
- Supersedes in direction: ADR-0019 (rejected, retained).
- Delegates to: `docs/prototypes/expression-language-extensions/plan.md` (absence/defaults, categorical comparison).
- Contracts: ADR-0006 (rule language), ADR-0007–0010, ADR-0012.
