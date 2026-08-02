# Examination — rule language iteration 2 (rival)

Builder: rival-builder seat, clean-room iteration 2. Branch: `prototypes/rule-language/it2`. Governance: v0.1 set. Charter: `charter-it1.md` v2, shared rival exam.

## Candidate

The candidate is a closed adopted dataflow package. A rule artifact is one guarded clause that publishes one named fact. Computations, applicability declarations, field mappings, and cross-form bridges share the same evaluator; their roles remain explicit for fresh readers and lineage pins. Expressions form a small generic tree language. Policy values are separate parameter citizens. Package and artifact scope is content (`tax_year`, `jurisdiction`, `family`, and optional effective date), and the package enumerates every exact member version.

Artifacts and evidence live under `rival-rule-language/`. The evaluator is throwaway Python with no tax/form identifiers. All fixture data is constructed synthetic data.

## Fixture results

- F1/F13: collection plus `round(stage=after_aggregate)` maps two W-2 wages to line 1a. The divergence fixture publishes 3 from 1.49 + 1.49; the deliberately wrong per-input procedure yields 2.
- F2/F3a/F11: gross and taxable interest clauses declare the Schedule B threshold path, line 1/3/4 mappings, exclusion block, and explicit Schedule B-to-1040 bridge. Below the threshold a separate direct mapping fires.
- F3b: foreign-account applicability and its surfaced Part III questions depend only on the asserted foreign-account fact, not interest amount.
- F4: W-2 box 2 and 1099-INT box 4 publish distinct line 25 components and a declared total.
- F5/F14: filing status and rounding convention are required facts. Their absence produces schema-shaped block entries and no operative default.
- F6: a generic maximum over subtraction declares the zero floor.
- F7: below $100,000 uses declared row ranges; at or above it uses an artifact-declared bracket fold. No worksheet coefficients or thresholds live in evaluator code.
- F8: mutually exclusive guarded clauses publish line 34 or line 37; the unselected output fact does not exist.
- F9: the convention is an asserted elective finding (`rounding.convention`). Every amount-producing entry rule that needs it names it in `requires`; the round expression names its stage. `none` and `whole_after_aggregate` are generic arithmetic modes implemented by the expression contract.
- F10: `rival-rule-language/evolution-probe.md` names persistent/new IDs, versions, scope changes, and when migration is or is not implicated.
- F12: line 9, Schedule 1 line 26, the Schedule 1-to-1040 line 10 bridge, and line 11 form an artifact-declared chain.

## Answers

**Q1 — one grammar and deletion.** Yes for all charter fixtures: every behavior is a guarded expression publication, with no fixture-specific evaluator branch. The adopted package is closed, so physically deleting a member from an unchanged adopted package fails validation rather than silently changing results. The deletion-attribution test creates a new package version omitting the Schedule B bridge: Schedule B line 4 still publishes while 1040 line 2b and only its downstream consequences disappear.

**Q2 — parameters and effective scope.** Parameter declarations are versioned citizens pinned by rules and derived findings. Artifacts and the closed package carry scope as content; adoption repeats and pins that scope. The runner receives no year, jurisdiction, family, directory convention, or form traversal configuration.

**Q3 — applicability and blocking.** `when` declares applicability; `requires` declares standing dependencies; `blocked` supplies a stable code and declared missing symbols. A false guard is inapplicable, not blocked. A true or unresolved guard with open dependencies appears in the completion record as structured data.

**Q4 — expression form and legibility.** A fixed flat operation record does not survive F7. This design uses a bounded expression tree plus two generic data operations, range lookup and bracket fold. The cost is punctuation and nested structure. Single-publication clauses, named symbols, explicit roles, and shallow intermediate facts partially recover legibility; a purpose-built rendering would still be needed for nontechnical adoption review.

**Q5 — stable and stage-correct.** The evaluator operates in snapshot rounds, sorts candidate publications, and reaches saturation. Double runs and three independently shuffled artifact orders are byte-identical. F13 separately proves the declared post-aggregate stage, so equality cannot conceal a consistently misplaced round.

**Q6 — elective dependence.** Elective values are findings, not configuration. F5 requires `filing_status`; amount entry rules require `rounding.convention`. Open choices block with no default.

**Q7 — fresh-reader recovery.** Computation bodies name inputs, guard, expression, result, and block. `role=field-mapping` names source-to-output mappings; `role=cross-form-bridge` makes form crossings discoverable; applicability artifacts publish explicit applicability facts and question-set facts; package and parameter citizens declare identity, exact versions, and effective scope; output identity is the `publishes` symbol. No corresponding names occur in evaluator code.

**Q8 — pins.** Roles earn their place. Pins distinguish input and choice findings, parameter declarations, computation rules, field mappings, bridges, adoption, governance, and diagnostic engine identity (the prototype does not currently emit the optional engine pin). This lets an explanation renderer say why a dependency was consulted instead of presenting an undifferentiated ID bag.

**Q9 — act and record timing.** Each derived finding has a deterministic `derived-publication-act` attributed to the adopting actor through the adopted instrument. This is vocabulary and record shape only; it does not resolve reserved T1 authority theory. A run first creates an immutable `derivation-record` with phase `started`, then publication acts may accumulate, then a separate immutable `completed`, `interrupted`, or `failed` record accounts for outputs, blocks, and stop reason. A crash after publication therefore still has the start record and the publication acts; recovery adds an interrupted/completion record rather than mutating the start record.

**Q10 — deterministic IDs.** Run, derived-finding, publication-act, and record IDs are truncated SHA-256 over canonical JSON payloads. Fixture double-run and shuffled-order equality demonstrates portability at this boundary.

**Q11 — citizens.** `schemas/prototype.schema.json` drafts strict shapes for rule artifacts, parameter declarations, artifact packages, adoption acts, derived findings, derived-publication acts, and derivation records. Every drafted instance names its schema version. `schemas/negative-kind-id-mismatch.json` is rejected because an `artifact-package` carries a `rule:` identity instead of `package:`.

## Negative results and limits

1. The row-range declaration is deliberately a fixture slice, not the complete IRS table below $100,000. Unrepresented rows block. The grammar passed F7; the policy corpus is not deployable. The clean-room materials supplied thresholds and the bracket/table distinction but not the full table, so the sampled row values were not independently source-audited in this seat.
2. Raw JSON is recoverable but not pleasant. F7 is markedly harder to review than F1, and adoption needs a renderer that shows named intermediate steps and tables without hiding the underlying citizen.
3. The JSON Schema expression definition enumerates the whole operation vocabulary and forbids unknown object fields, but it does not yet express every operation-specific required-field combination. The evaluator rejects missing operands rather than repairing them; a production schema must move those constraints fully into schema so Canon, not Python failure behavior, is the authority.
4. The tax-table fixture cannot show portability against a second independent evaluator; this iteration supplies one minimal runner plus order/double-run checks. E11.2 remains unproven until another implementation consumes the corpus.
5. The start/completion record pair closes the orphan-publication window conceptually, but the throwaway evaluator returns records in memory rather than fault-injecting real atomic workspace writes. E6.1/E14.1 need storage-level evidence later.
6. Expression operation semantics are generic but still a contract surface. `round`, `range_lookup`, and `bracket_fold` require their own versioned semantic specification before production; an enum alone is insufficient canon.

## Verification

`python3 -m unittest discover -s rival-rule-language/tests -v` passes eight tests: fixture expectations and blocks, package closure/scope, negative identity validation, double-run equality, shuffled-order equality, F13 divergence, bridge deletion attribution, and evaluator tax-identifier absence.
