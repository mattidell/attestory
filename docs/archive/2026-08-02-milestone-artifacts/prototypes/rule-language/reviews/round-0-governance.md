# Review Round 0 — Governance Fidelity

Reviewer: Codex resume session, 2026-07-10.

Artifact under review: `docs/archive/2026-08-02-milestone-artifacts/prototypes/rule-language/charter-it1.md`.
Context read: `docs/archive/2026-08-02-milestone-artifacts/prototypes/rule-language/harvest-notes.md`, `docs/archive/2026-08-02-milestone-artifacts/prototypes/rule-language/reviews/round-0.md`, `docs/governance/`.

## 1. Article 11 Legibility

Check: for each planned artifact kind, does the charter force complete rule meaning to be recoverable from artifacts without evaluator code?

Result: partial pass with one charter gap. The charter directly tests legibility for arithmetic aggregation, cross-form bridges, applicability, parameter tables, floors, line 16 table/worksheet logic, output-branch selection, and whole-dollar rounding. Exhibits: F1-F9 and Q1 in `charter-it1.md`; F2 explicitly requires the bridge to be artifact-declared; F7 explicitly forbids "the executor implements the worksheet"; Q7 defines a fresh-reader recovery measurement for F3, F5, and F7.

Gap: Q7 samples only F3, F5, and F7. Article 11 applies to all tax meaning, including bridges, mappings, method conventions, and output existence rules. A design could pass the named fresh-reader check while leaving F2, F8, or F9 meaning recoverable only from evaluator behavior. The charter should either broaden Q7 or add a separate legibility measurement for every artifact kind represented by F1-F9.

## 2. Article 11 Purity

Check: does the charter force artifacts to declare all inputs and avoid implicit clock, environment, ordering, or ambient constants?

Result: partial pass with one charter gap. Q5 requires shuffled-artifact order stability; Q10 requires deterministic derived-finding and record IDs in fixture mode; F5 requires filing status to block while open; F9 requires the rounding convention to live somewhere explicit and be applied consistently. These are real purity checks because they catch ordering dependence, unasserted choices, and unstable identifiers.

Gap: the charter says the rules are "2025 federal" and F10 probes 2026, but it does not explicitly require tax year, jurisdiction, effective scope, and adoption scope to be declared as artifact/package inputs rather than inferred from directory layout, runner arguments, or branch context. Exhibit: `harvest-notes.md` lesson 4 says adoption scope needs dimensions; `charter-it1.md` does not turn that lesson into a fixture or question. Add a charter requirement that every artifact or artifact package declares its effective scope and that the evaluator cannot provide tax meaning through ambient run configuration.

## 3. Ontology §5 Conformance

Check: does the charter cover inputs, conditions, operation, results, applicability, thresholds, mappings, dependencies, and whether a value may be derived?

Result: partial pass with one gap shared with check 5. Inputs and operations are forced by F1, F4, F6, and F7. Conditions and applicability are forced by F3 and Q3. Thresholds and parameters are forced by F3, F5, and F7. Mappings and bridges are forced by F2 and F4. Dependency declaration is tested through Q5, Q8, and Q10. Whether a value may be derived is tested by F3, F5, F8, and Q3.

Gap: Ontology §5 also says rule artifacts are citizens, versioned, immutable once published, and typed against the schemas they consume and produce. The charter discusses a candidate encoding and versioned parameters, but it does not require the iteration to draft artifact schemas or show how artifact instances name those schema versions. Without that, a prototype could answer the computation questions while leaving citizen/canon obligations to later prose.

## 4. E11.3 No Orchestrated Traversal

Check: does the charter prevent form order, traversal, or cross-form bridging from living outside artifacts?

Result: pass for charter purposes. F2 requires the 1099-INT to Schedule B to Form 1040 bridge to be artifact-declared. F3 makes Schedule B a conditional path rather than just a conditional value. F7 forces the line 16 worksheet logic into artifacts. Q1 requires zero engine special cases and says deleting an artifact must remove exactly its behavior. Q5 requires stable output with artifacts shuffled. Together these are the right failure detectors for E11.3 at the charter stage.

## 5. Articles 9 and 10 Canon/Declaration

Check: are artifacts required to be schema-versioned citizens with declared shape, and is any meaning carried only by convention?

Result: fail as currently chartered. The milestone objective is a "rule-artifact encoding," and F5 requires a "versioned parameter declaration," but the charter does not require the prototype to define schemas for rule artifacts, parameter declarations, publication acts, derivation records, or any artifact package/adoption envelope implied by the design. It also does not require drafted artifacts to carry schema-version identifiers. Exhibits: `charter-it1.md` "What iteration 1 builds", F5, Q2, Q9, and expected evidence.

Required amendment: before opening the builder seat, add an expected evidence item that the iteration drafts schema-level shapes for every citizen, act, and record kind it proposes, and that all drafted artifact instances name their schema versions. The prototype can remain throwaway, but the meanings cannot remain convention-shaped if the evaluation is to support Tier 2/Tier 3 ADRs.

## 6. Reserved-Entry Safety

Check: does the charter improvise T1 derived-finding authority or T2 stance doctrine?

Result: pass with a guardrail. F9 uses a whole-dollar rounding convention, which maps to the Ontology's defined convention-record family rather than the reserved stance/position entry. Q9 asks whether a `derived-publication` act kind and final run record hold up, which is a necessary publication/record-placement question for Articles 13-15. It does not, by itself, settle the reserved T1 authority construction.

Guardrail: Q9's expected output should explicitly state that publication-act vocabulary and record timing are being evaluated without resolving the T1 authority theory beyond the existing instrument framing. If the prototype begins defining why the user is legally or doctrinally the author of derived findings, it has crossed into reserved T1 work.

## Observations

The charter is strong where the previous lineages failed: it forces real 1040 line 16 logic into artifacts, tests cross-form bridging, and treats rounding as an explicit user convention rather than a hidden executor behavior.

The main governance risk is that computation expressiveness could crowd out Canon and Declaration. For this milestone, the prototype's schemas do not need production polish, but they do need to exist as evidence. Otherwise the ADR would be deciding from examples whose meaning still depends on prose and evaluator convention.

## Dissent

No dissent against the direction. I recommend amending the charter before opening the iteration-1 builder seat to cover the schema/citizen and explicit-scope gaps above.
