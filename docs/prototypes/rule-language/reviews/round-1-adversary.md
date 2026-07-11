# Review Round 1 — Adversary

Reviewer: Codex resume session, 2026-07-10.

Artifact under review: iteration 1 primary design on branch `prototypes/rule-language/it1` at `362f8a3`, directory `prototype-rule-language-it1/`, plus `docs/prototypes/rule-language/examination-it1.md` and charter v2.

Context read: `docs/prototypes/rule-language/SEAT.md`, `process-log.md`, `harvest-notes.md`, `reviews/round-1.md`, `charter-it1.md`, `examination-it1.md`, the governance set, official IRS 2025 Schedule B and instructions, and the it1 schemas, artifacts, fixtures, and evaluator.

Process disclosure: before taking this seat, I read `process-log.md`, which includes summaries of same-round governance and expressiveness reviews. I did not read `round-1-governance.md` or `round-1-expressiveness.md` themselves. This contaminates the adversary seat with high-level peer outcomes; the attacks below are therefore grounded in direct exhibits and should be conformance-checked with that disclosure in mind.

Verification command run in a temporary worktree at `/private/tmp/rule-language-it1-review`:

```sh
python3 prototype-rule-language-it1/machinery/evaluator.py
```

Result: passed. The evaluator reported schema validation ok, negative example rejected, double-run equality true, shuffled-output equality true, and F13 stage divergence detected (`3` post-total versus `2` per-input).

## Attack 1 — Missing fixture: Schedule B adjustments remain too narrow

Attack: Try to express Schedule B Part I cases beyond raw 1099-INT box 1 and the v2-added box 3 exclusion. The 2025 Schedule B instructions require Schedule B for seller-financed mortgage interest, accrued interest, OID reported below Form 1099-OID, amortizable bond premium adjustments, nominee interest, and nominee dividends. Exhibits: IRS Schedule B instructions, General Instructions and Part I lines for nominees/accrued interest/OID/amortizable bond premium; `charter-it1.md` F2, F11, F12; it1 package rules for Schedule B.

Outcome: finding against evidence sufficiency, not against the current charter as approved. Charter v2 closed the round-0 holes it named, but it1 can still pass while representing only a narrow Schedule B line 1/2/3/4 path. The language has not been forced to model payer-row annotations, subtractive statement rows such as "Nominee Distribution," "Accrued Interest," "OID Adjustment," or "ABP Adjustment," nor the seller-financed mortgage identity/reporting requirement. These are not broad tax coverage; they are Schedule B Part I behaviors inside the already selected form.

Disposition pressure: the rival design or an amended charter should include at least one Schedule B row-adjustment fixture where the displayed row total differs from the taxable total because an artifact-declared adjustment row is subtracted.

## Attack 2 — Misleading artifact: expression vocabulary validates as arbitrary JSON

Attack: Construct a rule artifact that validates against `rule-artifact.v1.prototype-it1.schema.json` but whose expression is an undeclared executor operation. I copied the W-2 line 1a rule, changed the id to `rule.2025.validates.but.nonsense.v1`, and set:

```json
{ "op": "executor_secret_tax_rule", "meaning": "not declared by schema" }
```

Exhibit: `prototype-rule-language-it1/schemas/rule-artifact.v1.prototype-it1.schema.json` defines `expression` as any object/string/number/boolean/null/array. Validation experiment result: `schema_errors 0`.

Outcome: successful attack. The current schema can reject one hand-coded label/id mismatch, but it cannot say what expression language a rule artifact is allowed to contain. That leaves the central rule vocabulary outside the schema contract and lets sealed behavior enter as a validating artifact, to be rejected only by evaluator code. This directly weakens Article 9 and Article 11 evidence: the schema is not yet the authority on rule meaning.

Disposition pressure: it1 should not be ratifiable as-is. A successor design needs a schema-declared expression grammar or a separate expression-language citizen whose version is pinned by every rule artifact.

## Attack 3 — Smuggled default: elective choices block, but absent source collections become zero

Attack: Leave elective facts open and see whether evaluation makes a choice operative. Exhibits: `fixture.no_rounding_convention`, the evaluator output, and the W-2/1099 rules in `federal-1040-core-2025.package.json`.

Outcome: partial failed attack. The direct elective-default attack did not succeed: missing rounding convention blocks money rules with `missing_rounding_convention`, and filing status is required for standard deduction and line 16.

Secondary outcome: a nearby non-elective default remains exposed. Inputs with `required: false` and `cardinality: many` bind to an empty list when no matching facts exist, and sum to zero. That means absence of 1099-INT box 1, W-2 box 2, 1099-INT box 4, or 1099-INT box 2 can become an operative zero without an asserted "no such source exists" fact or a declared closed source set. This is not an unasserted elective choice, but it is an unasserted negative factual claim. The design needs to distinguish "no rows because the source set is closed and empty" from "unknown because no such facts are present."

Disposition pressure: require source-set closure or fact-universe closure to be artifact-declared before optional-many inputs can publish zero.

## Attack 4 — Ordering trap: duplicate output identities make rule order authoritative

Attack: Add a second validating rule that publishes the same output fact id as the W-2 line 1a rule but computes a different value. Run with the duplicate before versus after the original.

Exhibit: in-memory experiment against `happy-path-table.fixture.json` using `machinery/evaluator.py`:

```text
rogue_first 999
rogue_last 100000
```

Outcome: successful attack. The evaluator's own shuffled-order check passes for the shipped corpus, but the schema and package do not forbid duplicate output fact ids or declare conflict resolution. `run_fixture` skips a rule once all its output fact ids are known, so the first publisher wins. That makes array order tax-significant as soon as a corpus contains duplicate outputs.

Disposition pressure: the artifact package schema must enforce unique output ownership, or the language must declare multi-publisher conflict semantics as rule content. Without that, E11.3's no-orchestrated-traversal guarantee depends on corpus hygiene outside the artifact contract.

## Attack 5 — Evolution trap: persisting 2025 rule ids across 2026 scope is ambiguous

Attack: Apply the F10 paper evolution story to a 2026 package. The it1 package says pure parameter updates create successor parameter citizens and a successor package scope for 2026 while `rule.2025.standard_deduction.line12e.v1` and `rule.2025.regular_tax.line16.v1` can persist if statutory structure is unchanged.

Outcome: successful attack. The proposed persisting artifact ids embed `2025`, and the actual rule artifacts also carry `scope.tax_year: 2025` and cite 2025 parameters directly. A 2026 package that adopts these unchanged rules either contains 2025-scoped artifacts in a 2026 package or mutates/versions the same logical rule into a different scope while keeping a 2025 id. The schema does not cross-check package scope against member artifact scopes, and rule inputs cite parameter ids literally, so parameter succession is not a clean package-level substitution.

Disposition pressure: the design needs an explicit identity rule for tax-year-scoped artifacts: either rules are year-generic and bind parameters through package slots, or each tax year has successor rule artifact ids. The current F10 answer is not stable enough for an ADR.

## Attack 6 — Package integrity trap: package membership is advisory

Attack: Treat the package envelope as the adoption target and ask whether it guarantees its declared members are present, scoped consistently, and used. Exhibit: `artifact-package.v1.prototype-it1.schema.json` requires only arrays of strings for `artifact_ids` and `parameter_ids`; `federal-1040-core-2025.package.json` separately embeds `rules` and `parameters`; the evaluator iterates `corpus["rules"]` rather than resolving package membership.

Outcome: successful attack. A package can validate while listing missing, extra, duplicated, or wrong-scope artifact ids. Because adoption is supposed to be over a specific versioned body of artifacts, package membership is contract-critical, not metadata. In it1, the package is a label around a JSON file rather than the schema-enforced closure of what was adopted.

Disposition pressure: package validation must prove exact membership: every listed id exists once, every embedded rule/parameter is listed once, member scopes are compatible with package scope, and evaluator execution is over the package-declared set.

## Attack 7 — Record/act schemas are too loose to carry the governance guarantees

Attack: Validate whether the drafted act and record citizens constrain the fields that Article 12, Article 14, and Article 15 need. Exhibits: `derived-publication-act.v1.prototype-it1.schema.json` and `derivation-record.v1.prototype-it1.schema.json`.

Outcome: successful attack. The publication act schema requires pins, but not `run_start_record_id`; the derivation record schema accepts arbitrary `governance_versions`, `artifact_versions`, `parameter_versions`, `published`, and `blocked` arrays. It also allows `record_phase: "started"` while still requiring `published` and `blocked`, and it has no start/completion linkage field. The examination's start/completion conclusion is therefore present in prose and evaluator output but not captured as a strong citizen contract.

Disposition pressure: the companion ADR on publication acts and run-record placement needs a stronger schema sketch before ratification: start and completion records should be distinct or discriminated shapes, publication acts should require the start-record pin if that is the selected timing model, and blocked/published entries need declared structure.

## Failed attacks

I attempted to break the no-rounding-convention case by omitting the rounding mode. The design held for elective rounding: rules needing `round_money` blocked with `missing_rounding_convention`, and downstream rules blocked rather than publishing rounded or unrounded money.

I attempted to find a shipped-corpus ordering failure under the evaluator's `shuffle_rules` path. The shipped corpus held: all fixture `shuffle_equal` results were true. The ordering failure requires an adversarial but schema-valid duplicate-output artifact, so it is a contract-hole finding rather than a failure of the current corpus.

I attempted to treat the line 16 ordinary tax table/worksheet split as sealed evaluator meaning. That attack mostly failed: the artifact declares the threshold branch, row lookup, row binding, multiplication, and subtraction. The remaining weakness is not the worksheet formula but the unconstrained expression schema that permits a future artifact to smuggle an undeclared operation.

## Observations

The it1 design is valuable evidence that expression trees can cover the charter fixtures, and the evaluator checks are meaningful for the concrete corpus. The adversary failures are mostly contract-boundary failures: the schema admits too much, package closure is not enforced, and the paper evolution story has not settled artifact identity.

The strongest issue for the next iteration is not "make it more legible" in the fresh-reader sense. It is making the declared contract tight enough that a second runner or a hostile corpus cannot import meaning through evaluator rejection paths, array order, or package conventions.

## Dissent

I dissent from treating it1 as ratifiable as-is. I do not dissent from proceeding to the rival design; the evidence is strong enough to inform a rival. Before an ADR can be proposed, the process needs either an iteration that closes the schema/package/identity holes or an evaluation analysis that explicitly rejects those it1 features and cites rival evidence for the replacement.

## Source material

- IRS 2025 Schedule B instructions: https://www.irs.gov/instructions/i1040sb
- IRS 2025 Schedule B form: https://www.irs.gov/pub/irs-pdf/f1040sb.pdf
- IRS 2025 Instructions for Form 1040: https://www.irs.gov/pub/irs-pdf/i1040gi.pdf
