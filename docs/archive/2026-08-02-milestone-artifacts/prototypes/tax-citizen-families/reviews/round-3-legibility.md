# Round 3 legibility review

## Scope and method

This is a fresh-reader review of only `roles/reviewer-legibility.md`, this
round file, and the files listed under its Legibility Scope, read from
`exhibits/tax-citizen-families/it3`. I did not read the charter, examination,
git history, prior reviews, or peer reviews.

The checks below are static reproductions from the scoped content. I did not
run the saturation machinery, inspect a run record, or treat a file's claim
that a harness check passed as an observed execution result. Confidence uses
the required vocabulary: certain, probable, or guessing.

## Overall finding

Iteration 3 is substantially more legible than a bare rule-symbol interface.
The reader can follow W-2 slip identity, source-set closure intent, symbol
bindings, guarded branches, the five rendered-absence dispositions, and the
included line-16 boundary. The scenarios give useful named pressure points.

The review remains **still disputed** for contract ratification. Several
important joins are prose or harness-shaped rather than citizens in the
scoped artifacts: scenario booleans are not closure findings, line-1-other
source membership has no fact type, package membership does not include the
bundle or presentation artifacts, and citation attachments cover only a
subset of the declared citizens. The `closed_sets` contract is candid about
being load-bearing, but its actual projection and the absence walks cannot be
reproduced from these artifacts alone.

## Artifact-by-artifact reading

| Scoped artifact | What I believe it declares; identity and lifecycle | What it would cause a renderer or rule to do | Confidence |
|---|---|---|---|
| `schemas/form-field.v1.schema.json` | A first-class citizen for one form line. Identity is `id` plus `version` and the embedded authority/form/year/jurisdiction and line. The description says published versions are immutable and a later form change is a new instance/version. The schema `$id` says `it2`, which conflicts with the file's `it3` location. | A renderer chooses the literal and explanation for computed zero, closure-backed zero, blocked-unclosed, blocked-invalid, or guard-absent. The field bridges a form line to a derivation symbol and citation. It is not a saturation input. | Certain for the declared schema; probable for its use by a renderer. |
| `schemas/source-citation.v1.schema.json` | A citizen naming an official source document, optional year applicability, and optional locator. Identity is `id`; no separate content version is required. `resolved` is a lifecycle/status flag, not a version. | A citation consumer can reject `resolved: true` without a year or locator. The citation is inert and cannot affect derivation output. | Certain. |
| `schemas/citation-attachment.v1.schema.json` | An attachment citizen binds a subject kind/id and role to a citation and declares an expected year/locator fingerprint. Identity is attachment `id`; no version field is present. | A validator can resolve both IDs and reject a mismatched year, locator kind, or locator substring. The attachment itself is inert to the runner. Cross-file existence and fingerprint checking are described, but not encoded as JSON Schema constraints. | Certain for the declared contract; probable for enforcement. |
| `schemas/symbol-binding.v1.schema.json` | A tax-year binding set identifies the correspondence from fact type to runner symbol or collect name, with a projection kind. Identity is set `id` plus tax year; no version field is present. | A reader can use it to map a fact or closure projection to a rule input/collect name. The schema does not define the semantics of `ref`, `collect`, or the projection values. | Certain for the bridge; probable for operation semantics. |
| `schemas/scenario.v1.schema.json` | A synthetic scenario has an id, description, provenance, inputs, and optional golden dispositions. Provenance identifies package/version, bundle, year, jurisdiction, and three content files. It has no scenario version. Inputs are workspace-shaped, including source records and closure booleans. | A runner or fixture loader would use `inputs`; a checker would compare `expect`, `expect_blocked`, `expect_inapplicable`, `expect_unpublished`, or `expect_no_publications`. The schema does not make an input into a typed finding with fact type, basis, evidence, or correction lineage. | Certain for the shape; still disputed for the workspace-to-finding join. |
| `content/bundle.tax-2025.json` | A 2025 bundle declares fact types. W-2 identity is employer + tax year + individual `w2-instance`, explicitly not evidence. Interest identity is payer + year + box. Filing status, rounding, itemization, and the two condition objects are elective/determinable as described; the three source closures are determinable and attested. Fact types say supersession policy is free. The bundle has no explicit `version` property. | It supplies the fact-type meaning used by bindings and rules. Its descriptions make same-control-number W-2 correction semantics and box-1/box-3/box-8 distinctions readable. It does not supply a correction artifact, evidence schema, or line-1-other source fact type. | Certain for the declared meanings; probable for correction behavior beyond the prose. |
| `content/form-fields.2025.json` | Eight concrete Form 1040 fields, each with `v1`, form/year/jurisdiction, a bound symbol, and a citation id. | The renderer follows the disposition-specific `render` and `explain` instructions. The records explicitly distinguish computed zero, closure-backed zero, open/invalid blockage, and false-guard non-existence. | Certain. |
| `content/citations.2025.json` | Fourteen 2025 IRS source-citation records, all marked resolved, with form-line, form-box, section, table, or publication-page locators. IDs identify them; no citation version is present. The notes carry build-time verification claims that cannot be independently reproduced from this scope. | They provide named source targets for attachment and field citation references; they do not enter rule evaluation. | Certain for the records; probable for the external verification claims. |
| `content/citation-attachments.2025.json` | Eight attachment records. They cover W-2 meaning, two 1099-INT boxes, all three parameters, the taxable-income rule, and only the line-1a form field. | A matching attachment can demonstrate that the cited locator has the expected year/kind/text. The set does not attach citations to every form field, rule, fact type, closure, choice, or condition that the bundle/rules claim. | Certain; the incompleteness is certain. |
| `content/symbol-bindings.2025.json` | Eleven 2025 mappings: choices, W-2 and interest collects, three closure projections, and two boolean condition projections. Identity is set id + year; no version field is present. | It resolves the former `us.filing-status`/`filing_status` style ambiguity and names the three source sets. Closure rows explicitly say they also project into `closed_sets`. | Certain for the named mappings; still disputed for the authoritative finding that supplies each projection. |
| `content/rules.2025.json` | Ten versioned rules scoped to 2025/US federal/individual income tax. Each has role, requirements, guard, expression, published symbol, blocked code, and notes. | A runner can aggregate wages, map taxable interest, gate line 1z on omitted siblings, choose standard/itemized, compute taxable income, and choose tax-table/rate-schedule by guard. The rules require machinery meanings for `collect`, `ref`, `round`, `range_lookup`, `bracket_fold`, stages, and blocked propagation that are not declared here. | Certain for rule intent; probable for execution details. |
| `content/parameters/standard-deduction.2025.json` | A versioned, scoped 2025 parameter keyed by filing status. | The standard branch looks up a filing-status amount. | Certain. |
| `content/parameters/tax-rate-schedule.2025.json` | A versioned, scoped 2025 parameter with single and MFJ marginal brackets. | The rate-schedule rule folds the applicable brackets for taxable income at or above $100,000. Other filing statuses are not present in this artifact. | Certain for the supplied parameter; probable that missing keys block. |
| `content/parameters/tax-table.2025.json` | A versioned, scoped, fixture-minimal 2025 range table with only three single-filer bands. | The tax-table rule can produce the included fixture values and, per the rule note, should block on an authored-band miss. The `on_miss` behavior is in prose, not in the parameter record. | Certain for the three bands; probable for the miss behavior. |
| `content/package.tax-2025.json` | A versioned 2025 package lists the ten rules and three parameters and states mutual-exclusion semantics for lines 12 and 16. It does not list the bundle, form fields, citations, attachments, or symbol bindings as members. | A package consumer can load the listed rules/parameters and resolve the two conflict policies. The scenario's extra provenance files are therefore a parallel content join, not package membership visible in this artifact. | Certain. |
| `content/closure-projection.md` | An adopted machinery projection contract: `closed_sets` is a pure projection of current complete closure findings, with a three-row fact-type-to-source-set map. It explicitly says the dependency is load-bearing and that removing the projection blocks. | It supplies the second view needed for an empty `collect` to publish a closure-backed zero, while claiming the closure finding remains the authority. It still relies on an undeclared current-finding/run implementation and names machinery outside this scope. | Certain for the written contract; still disputed as standalone evidence. |
| `fixtures/scenarios.json` | Named synthetic scenarios cover normal aggregation, closure-backed zeros, present zero, box distinction, two same-employer W-2s, itemization, open/invalid interest, line-1z closure, standard-deduction conditions, both line-16 methods, and all-open state. Each has 2025 package/bundle/file provenance. The fixture booleans and source arrays are not themselves declared findings. | A runner/checker would use the inputs and compare the expected publications/dispositions. The descriptions are unusually helpful, but several provenance links still depend on knowing how the harness materializes them. | Certain for declared examples; still disputed for end-to-end traversal. |

## Reproduced legibility checks

These are content-level walks, not executed runner checks.

- `two_w2_same_employer` gives two records with the same employer and year but
  `acme-ctrl-001` versus `acme-ctrl-002`, and expects one aggregate line 1a of
  42000. Together with the bundle's identity keys, this makes W-2 slip identity
  peer to evidence rather than evidence identity. The same bundle description
  says a corrected W-2 with the same control number is the same instance. No
  correction record is supplied, so the correction claim is readable but not
  demonstrated.

- `wages_only_closed_interest` and `interest_only_closed_w2` make the intended
  closure-backed zero distinction readable. `present_zero_interest` separately
  makes a present source with value `0.00` a computed zero. The form-field
  records say what a renderer should show in both cases.

- `unclosed_interest`, `no_source_no_closure`, and `invalid_source_value` name
  three different absence/invalidity states. The rule and form-field records
  provide distinct blocked codes/render explanations. The expected arrays do
  not provide a run record or a pin trace, so the walk stops before execution
  evidence.

- `line1z_unclosed` follows line 1a -> line 1z -> line 9 and shows that line 1a
  may remain published while line 1z and downstream total income are blocked.
  The rule's collect source set is named, but no line-1-other fact type or
  source mapping declares what can inhabit that set.

- `std_special_condition` and `std_eligibility_unknown` make the standard
  deduction boundary honest for the included slice: false eligibility makes
  the base rule inapplicable, while unknown eligibility blocks. The additional
  deduction/dependent paths are explicitly absent rather than silently filled.

- `high_income_rate_schedule` and `alternate_method_blocked` make the line-16
  boundary readable: at/above 100,000 the rate schedule is selected; when an
  alternate worksheet is required both ordinary rules are inapplicable. The
  sparse tax table means this is still a fixture slice, not a complete table.

- `itemize_true`, `std_special_condition`, and the package conflict semantics
  make false-guard non-existence followable for the supplied line-12 and
  line-16 branches. This is the strongest guard legibility in the exhibit.

- `all_open` declares `expect_no_publications: true` and sets all choices and
  closures open. The rule requirements make the intended result plausible,
  but there is no expected blocked list, termination trace, or authoritative
  run record in the allowed files. I cannot reproduce saturation termination
  from content alone.

## R1-R13 gate report

The round file names R1-R13 but does not define every gate label. The labels
below therefore use the concrete repair topics named by the scoped artifacts
and round questions; I do not import definitions from an excluded document.

| Gate | Status | Exhibit and static reproduction | Legibility conclusion |
|---|---|---|---|
| R1 — W-2 source-instance identity | **closed** | `two_w2_same_employer`; compare its two `w2_instance` values with the bundle identity keys and line-1a aggregate. | Peer-to-evidence identity is explicit. Same-control-number correction semantics are stated but lack a correction example. |
| R2 — closure nature and closure-backed zeros | **still disputed** | Bundle closure fact types say determinable + attested; `wages_only_closed_interest`, `interest_only_closed_w2`, and `present_zero_interest` distinguish the intended outcomes. | The concept is clear, but scenario `*_closed` booleans do not identify the authoritative current closure findings that the projection requires. |
| R3 — `closed_sets` dependency | **still disputed** | `symbol-bindings.2025.json` names the closure projections; `closure-projection.md` gives the three mappings and says the machinery is load-bearing. | The dependency is honestly surfaced, which is good evidence of legibility, but no allowed artifact executes or records the projection. |
| R4 — stale projection cannot manufacture truth | **still disputed** | The fourth property in `closure-projection.md` states the stale-projection result. | No scoped scenario contains a stale projection with no backing finding, so this is a declared check, not a reproduced check. |
| R5 — resolved citation invariant | **closed** | `source-citation.v1.schema.json` makes a resolved citation require non-null year and locator; all 14 supplied citations have both and are resolved. | The local schema/data relationship is legible. External source resolution is only asserted in notes. |
| R6 — citation attachment coverage and fingerprinting | **failed** | All eight records in `citation-attachments.2025.json` have readable subjects and expected fingerprints, but only line 1a is attached among the eight form fields; most rules/fact types/closures/choices have no attachment. | The mechanism is understandable but coverage is only for supplied fixtures/selected roles, not every claimed citizen role. |
| R7 — line 1z completeness honesty | **still disputed** | `line1z_unclosed`; the line-1z rule requires `line1-other.closed`, and the form field says to render a blocked dash. | The blocking behavior is clear, but the line-1-other source family has no bundle fact type or symbol binding beyond its closure. |
| R8 — standard-deduction eligibility | **closed** | `std_special_condition`, `std_eligibility_unknown`, the bundle condition object, and the standard rule/form field. | For the included base-table slice, false and unknown eligibility do not silently receive a base amount. Out-of-scope paths are explicitly stated. |
| R9 — line-16 method boundary | **closed** | `high_income_rate_schedule`, `alternate_method_blocked`, both guarded rules, and package conflict semantics. | The $100,000 ordinary-method split and alternate-method non-publication are legible for the included slice. Sparse table breadth is disclosed. |
| R10 — all-open saturation | **still disputed** | `all_open` supplies all-null choices, open closures, no sources, and `expect_no_publications`. | No default is visible, but termination and the complete blocked set cannot be reproduced from the scoped content. |
| R11 — guarded branch non-existence | **closed** | `itemize_true`, `std_special_condition`, `alternate_method_blocked`, package conflict semantics, and each form field's `guard_absent` instruction. | The supplied false-guard branches have declared inapplicable dispositions rather than renderer blanks. |
| R12 — scenario-to-form traversal | **still disputed** | `w2_and_interest` provenance points to package, bundle, fields, citations, and bindings; symbol bindings connect fact names to rule inputs. | A reader can traverse the happy path, but the package does not include those supporting artifacts and scenario inputs are not typed findings. Harness knowledge is still required at the workspace boundary. |
| R13 — package/year validation and absence-walk breadth | **still disputed** | Scenario provenance, package scope, parameter scope, citation years, and attachment expectations all say 2025; the named absence scenarios cover the intended matrix. | Positive consistency is visible, but no mismatched-year/package fixture or run-record evidence proves rejection and termination for all five absence walks. |

## Dissent and disposition

I would accept this exhibit as strong legibility evidence for the included
slice and as a useful declaration of the intended contract. I would not treat
it, by itself, as sufficient evidence for a contract-foundational Tier 2
decision. In particular, the missing correction artifact, missing line-1-other
fact family, partial attachment coverage, and unexecuted `closed_sets`/absence
walk evidence leave the authoritative-record path incomplete for a fresh
reader.
