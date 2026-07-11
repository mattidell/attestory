# Review Round 2 — Governance Fidelity (Comparative: it2 vs it1)

Reviewer: Claude resume session, 2026-07-10.

Seat: governance fidelity.

Artifacts reviewed:
- `docs/governance/` v0.1 (constitution, ontology; engineering-constraints/principles/commentary consulted for cross-reference)
- `docs/prototypes/rule-language/charter-it1.md` v2
- `docs/prototypes/rule-language/reviews/round-2.md`
- `docs/prototypes/rule-language/examination-it2.md`
- branch `prototypes/rule-language/it2` at the round-stated tip `623957c`: `rival-rule-language/artifacts/{rules,parameters,package}.json`, `rival-rule-language/schemas/prototype.schema.json`, `rival-rule-language/schemas/negative-kind-id-mismatch.json`, `rival-rule-language/evaluator.py`, `rival-rule-language/tests/test_prototype.py`, `rival-rule-language/evolution-probe.md`, `rival-rule-language/README.md`
- for direct tightness comparison: tag `exhibits/rule-language/it1`, `prototype-rule-language-it1/machinery/evaluator.py` and `schemas/artifact-package.v1.prototype-it1.schema.json`
- `reviews/round-1-governance.md` (prior-round peer review; permitted — independence rule forbids only same-round peer reading)

I did not read any other round-2 reviewer's output before writing this review.

## Check 1 — Article 11 Legibility

Check: for each artifact kind, is the complete rule meaning recoverable from the artifact without reading evaluator code? Name any meaning that lives only in the evaluator.

Result: partial pass with governance findings — **tighter than it1 on expression vocabulary, equal to it1 on several sealed operation semantics.**

Exhibits:
- `rival-rule-language/schemas/prototype.schema.json` (`$defs/expr`, `op` enum)
- `rival-rule-language/evaluator.py` (`evaluate_expr`, saturation loop)
- `rival-rule-language/artifacts/rules.json`

Measurements:
- **Tighter:** the schema enumerates the closed operation vocabulary (`ref, collect, parameter, add, subtract, max, compare, all, any, not, choose, range_lookup, bracket_fold, round`) with `additionalProperties: false` on the expression object. it1's round-1-governance Check 1/5 found `expression` "permitted as object/string/number/boolean/null/array without enumerating operation forms" — that specific defect is closed here. Every operation actually used in `rules.json` (`add, bracket_fold, collect, compare, max, parameter, range_lookup, ref, round, subtract`) is a declared enum member.
- **Equal to it1 (same defect class, not resolved):** `round`'s two mode strings (`none`, `whole_after_aggregate`) and their tie-break rule are not declared anywhere — `mode == "whole_after_aggregate": value.quantize(Decimal("1"), rounding=ROUND_HALF_UP)` is a Python conditional. The schema's `mode` field is typed as any `expr`, not an enum of valid mode strings. This is the same finding round-1-governance made against it1's `ROUND_HALF_UP` constant (Check 1, Check 2).
- **Equal to it1 (same defect class):** `range_lookup` (half-open interval `lower <= value < upper`) and `bracket_fold` (marginal-rate accumulation over bracket rows) are enum members, but their computational semantics live only in `evaluate_expr`. The examination discloses this itself (negative result 6: "`round`, `range_lookup`, and `bracket_fold` require their own versioned semantic specification before production; an enum alone is insufficient canon") — credit for honest disclosure, but the underlying gap is the direct successor to it1's F7 worksheet-in-evaluator risk the charter was written to catch.
- **Equal to it1 (same defect, not disclosed in the examination):** the distinction between "guard evaluated `False`" (silently inapplicable, never published, never reported blocked) and "guard has an open dependency" (blocked with a schema'd code) is evaluator control flow, not artifact content. In the main saturation loop, `if condition is False: fired.add(...); continue` permanently retires the rule with no record; in the blocked-computation pass, the same `if condition is False: continue` skips it from the blocked list too. Examination Q3 states in prose "A false guard is inapplicable, not blocked" — that is a claim about the design, not a citation to where the artifact declares it. This is the same finding round-1-governance made against it1 ("The false-applicability rule is evaluator meaning... the artifact declares an applicability expression and output, but not the record semantics for a false condition").
- **New finding, not present in round-1-governance (nothing to compare against) and not disclosed by the it2 examination:** `collect` returns `[]` for zero matching facts, and `add` sums an empty list to `Decimal("0")` via `sum(values, Decimal("0"))`. Rule `rule:f1.wages-to-1040-line1a` requires only `["rounding.convention"]` — not any `w2.box1` fact — so a workspace with zero W-2s and an asserted rounding convention publishes `form1040.line1a = 0` with no finding recording "zero W-2s" as an input. The zero is smuggled through evaluator aggregation behavior, not asserted. This is the same shape as round-1-adversary's attack 3 secondary finding against it1 ("optional-many-to-zero smuggles unasserted negative claims"), now observed independently in it2 without having read that document's specific line (I read the round-1-adversary review only after forming this observation from the artifact and evaluator directly — noted for the independence record since round-1 peer review is fair game this round, but this finding was self-derived).

Finding: Article 11's "obtuse is permitted; hidden is not" is not fully satisfied by it2, on a narrower surface than it1 left open. The vocabulary is closed and enumerated (real tightening), but rounding tie-break, table/bracket-fold arithmetic semantics, false-vs-blocked distinction, and empty-collection defaulting all still resolve only by reading `evaluator.py`.

## Check 2 — Article 11 Purity

Check: do artifacts declare all inputs? Name any implicit input: clock, environment, ordering assumption, ambient constant.

Result: partial pass — **tighter than it1 on one axis (package identity no longer hardcoded), equal on another (governance version constant).**

Exhibits:
- `rival-rule-language/evaluator.py` (`GOVERNANCE` tuple, `run_id` construction, `round` handling)

Measurements:
- No dependency on clock, network, environment, or filesystem beyond the fixed prototype corpus. `random.Random(seed)` is verification machinery (shuffle-order tests), not rule meaning — same posture as it1.
- **Tighter than it1:** `run_id = stable_id("run", {"revision":case["workspace_revision"], "package":package["package_id"], "version":package["version"]})` derives run identity from the *loaded* package citizen. Round-1-governance's Check 2 found it1 hardcoded `pkg.2025.us-federal.1040-core.v1` directly in evaluator code for the equivalent construction. That specific ambient constant is gone in it2.
- **Equal to it1 (not improved):** `GOVERNANCE = ("constitution", "ontology", "engineering-constraints", "principles", "commentary")` and the literal `"version":"0.1"` in `governance_pins` construction are ambient Python constants, not values read from any governance-version citizen or run input — the same defect round-1-governance found in it1 ("Governance versions are hardcoded in the evaluator's derivation record construction").
- **Equal to it1 (not improved):** the rounding mode string values and `ROUND_HALF_UP` tie-break are ambient code constants (see Check 1).

Finding: it2 closes one purity gap (package identity) that it1 left open, but carries forward two others (governance-version pinning, rounding semantics) unchanged.

## Check 3 — Ontology §5 Conformance

Check: inputs, conditions, operation, results, applicability, thresholds, mappings, dependencies declared? Name each missing or smuggled item.

Result: partial pass, materially the same shape as it1.

Exhibits:
- `rival-rule-language/artifacts/rules.json`, `parameters.json`
- `rival-rule-language/schemas/prototype.schema.json` (`$defs/parameters.values: {}`)

Measurements:
- Declared: inputs (`requires`, `when`, `collect`/`ref` targets), conditions (`when`), operations (enumerated `op` vocabulary — an improvement over it1, see Check 1), results (`publishes`), applicability (`role: applicability` + `when` + a dedicated `publishes` fact such as `schedule_b.part_i.applicable`), thresholds (parameter references via `op: parameter`), mappings (`role: field-mapping`), cross-form bridges (`role: cross-form-bridge`), dependencies (`requires` plus `pins_for` derivation).
- **Missing/smuggled, equal to it1:** `parameters.values` is schema-typed as `{}` (unconstrained) — table row shape, bracket row shape, and the standard-deduction key set are private conventions between `parameters.json` and `evaluator.py`, exactly the defect round-1-governance found against it1's parameter schema.
- **Missing/smuggled, equal to it1:** optional-many-to-zero (Check 1) is an Ontology §5 "inputs...declared" gap as much as a legibility one — a rule fires without every input that determined its value (the fact of "no W-2s") being a declared dependency.
- Fact-type/form-field references remain string ids rather than drafted citizens in both designs — charter-scoped exclusion (F1–F14 charter, not Q11's citizen-drafting scope beyond what Q11 lists), disclosed by neither examination as resolved, consistent between iterations.

Finding: Check 3 is a wash between the two designs — the enumerated operation vocabulary is a real improvement that partially strengthens Ontology §5's "operation declared" clause, but parameter-value shape and optional-input semantics remain conventional in both.

## Check 4 — E11.3 No Orchestrated Traversal

Check: does form order, traversal, or cross-form bridging live anywhere but artifacts?

Result: pass — **tighter than it1.**

Exhibits:
- `rival-rule-language/evaluator.py` (full read; generic saturation loop, no scheduler)
- `rival-rule-language/artifacts/rules.json` (`role: cross-form-bridge` on `rule:f2.schedule-b-to-1040-line2b`, `rule:f12.schedule1-to-1040-line10`)
- `rival-rule-language/tests/test_prototype.py::test_evaluator_contains_no_tax_form_identifiers` and `test_f13_stage_divergence`

Measurements:
- Cross-form bridges are declared artifacts with `role: cross-form-bridge`, same pattern as it1.
- The evaluator contains zero form-specific identifiers anywhere — confirmed by direct read and corroborated by the design's own test (`test_evaluator_contains_no_tax_form_identifiers` asserts `form1040`, `schedule_b`, `schedule1`, `w2.box`, `int1099` are absent from the evaluator source).
- **Tighter than it1:** round-1-governance recorded a caveat against it1 — its F13 wrong-stage diagnostic hardcoded a specific rule id (`rule.2025.w2.box1.to.f1040.line1a.v1`) as a target inside evaluator code for the mutation test. it2's equivalent test (`test_f13_stage_divergence`) computes the deliberately-wrong per-input rounding independently in the *test file* from fixture data (`sum(Decimal(f["value"]).quantize(...) for f in case["facts"] if f["symbol"]=="w2.box1")`) rather than the evaluator targeting a hardcoded artifact id. The verification machinery itself is form-identifier-free in the production evaluator; it1's was not.

Finding: it2 succeeds on E11.3 and closes the one prototype-only caveat round-1-governance raised against it1's diagnostic machinery.

## Check 5 — Article 9/10 Canon and Declaration

Check: are artifacts schema-versioned citizens with declared shape? Is any meaning carried by convention?

Result: partial pass — **mixed: tighter than it1 on declared shape and package-closure enforcement; looser than it1 on whether the schema is actually the runtime authority.**

Exhibits:
- `rival-rule-language/schemas/prototype.schema.json`, `rival-rule-language/schemas/negative-kind-id-mismatch.json`
- `rival-rule-language/evaluator.py` (`validate_citizen`, `validate_contract`)
- `exhibits/rule-language/it1:prototype-rule-language-it1/machinery/evaluator.py` (`validate_package`, imports `from jsonschema import Draft202012Validator`)
- `exhibits/rule-language/it1:prototype-rule-language-it1/schemas/artifact-package.v1.prototype-it1.schema.json`

Measurements:
- **Tighter than it1 (declared shape):** every citizen kind in `prototype.schema.json` — rule, parameter, package, adoption, publication, finding, record — carries `additionalProperties: false`, a `const` schema_version, and a `pattern`-constrained id field (e.g., `artifact_id: "^rule:[a-z0-9._-]+$"`). it1's round-1-governance Check 5 found several of it1's schemas loose (unconstrained `expression`, no item schemas on record arrays); it2's schema file is a stricter document by direct comparison.
- **Tighter than it1 (package closure, enforced not advisory):** `validate_contract` computes `available = {(identity(c), c["version"]) for c in rules+parameters}` and `declared = {(m["citizen_id"], m["version"]) for m in package["members"]}` and raises `Invalid` on any mismatch — an exact-set closure check that fails the run. I confirmed it1's package schema (`artifact-package.v1.prototype-it1.schema.json`) declares `artifact_ids`/`parameter_ids` as plain string arrays with **no version per member** and no runtime cross-check against the loaded corpus (`grep -n "artifact_ids\|parameter_ids"` in it1's evaluator shows these lists used only for pin bookkeeping, never compared against what was actually loaded). This directly confirms round-1-adversary's attack 6 characterization of it1's package membership as "advisory." it2 closes that gap.
- **Tighter than it1 (scope-escape check):** `validate_contract` additionally rejects any member citizen whose `tax_year`/`jurisdiction`/`family` scope diverges from the package's declared scope. No equivalent check exists in it1's evaluator.
- **Looser than it1 — the central finding of this check, undisclosed by the it2 examination:** it2's `evaluator.py` never loads or validates against `prototype.schema.json` at all. `validate_citizen` is a hand-written Python function with its own hardcoded `expected` dict (schema name string, id-key name, regex pattern) that happens to overlap with the schema file's constraints today but is a second, independent encoding of them — not a consumer of the schema. By contrast, it1's evaluator imports `jsonschema.Draft202012Validator`, loads the actual schema files from `schemas/`, and calls `iter_errors()` against every corpus instance in `validate_package()`, failing the run (`return 1`) on any error. Article 9 states "the schema is the sole authority on what a thing is... none carries a private notion of meaning" and Article 10 forecloses "provisional shapes." On this specific test — is the declared schema file the thing actually enforcing shape at runtime, or is it documentation next to a hand-rolled duplicate — it1 passes and it2 fails. This is a real regression on a governance-load-bearing property, and it sharpens the design's own negative result 3 ("a production schema must move those constraints fully into schema so Canon, not Python failure behavior, is the authority") — the examination frames this as a scope gap in the schema's expressiveness, not as the schema being entirely disconnected from enforcement, which understates the finding.

Finding: it2's schema *documents* are stricter, but it1's schema *mechanism* is the one actually wired to reject nonconforming instances. A design that adopted it2's schema content and it1's validator wiring would beat both.

## Check 6 — Reserved-Entry Safety

Check: does the design improvise T1 (derived-finding authority) or T2 (stance) doctrine?

Result: pass — equal to it1.

Exhibits:
- `rival-rule-language/artifacts/rules.json`, `evaluator.py` (`derived-publication-act` construction)
- `docs/prototypes/rule-language/examination-it2.md`, Q9

Measurements:
- `derived-publication-act` stays within the existing instrument framing: pins inputs/choices/parameters/rule/adoption, attributes `actor_id` from the adoption act. No stance or filed-position artifact appears.
- Examination Q9 explicitly scopes itself to "vocabulary and record shape only; it does not resolve reserved T1 authority theory" — same guardrail language it1's examination used.
- The `started` → `completed`/`interrupted`/`failed` record-phase split is a proposal about run timing, not about T1/T2 doctrine, and does not smuggle authority theory into the phase enum.

Finding: no reserved-entry doctrine improvised by either design; parity holds.

## Observations

The two designs make different bets on where tightness lives, and round 2's contract-tightness axis surfaces a genuine, previously uncaptured tradeoff: it1 has a looser schema but a real validator behind it; it2 has a stricter schema with no validator behind it, plus a hand-enforced package-closure check it1 never attempted. Neither design is uniformly tighter — an evaluation analysis that scores "governance fidelity" as a single scalar would erase this. The Check 5 finding (schema disconnected from runtime enforcement) is, in my judgment, the most consequential single fact this round produced: it means the examination's own honesty-audit answer (negative result 3) is technically true but frames the gap one step too narrowly, and a reader trusting the examination's self-assessment would not learn that the schema file is presently inert.

The rounding-semantics and false-vs-blocked findings (Check 1) are now confirmed present, unchanged, across two independent clean-room designs. That convergence is evidence the charter itself under-specified these two points (F9's convention concept covers rounding *stage*, not tie-break *mechanism*; no fixture forces a false-guard-vs-blocked distinction to be declared) — an evaluation-analysis or charter-authoring finding, not a builder failure in either iteration.

## Dissent

No dissent from proceeding with the process. I dissent from any framing that treats it2 as the strictly-superior successor on governance grounds alone: it2 is ahead on vocabulary closure, package-closure enforcement, and scope-escape checking; it1 is ahead on schema-to-runtime binding. An it3 or an evaluation-analysis synthesis should explicitly combine it2's package/scope enforcement and enumerated vocabulary with it1's genuine `jsonschema`-backed validation — treating either artifact corpus alone as ratifiable would carry forward a defect the other iteration already solved.
