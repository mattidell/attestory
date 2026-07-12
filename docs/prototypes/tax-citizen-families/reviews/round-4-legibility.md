# Round 4 Legibility Review

## Fresh-reader method

I read only the legibility role, this round file, and the listed it4 exhibits
from `exhibits/tax-citizen-families/it4`. I inspected the exhibits with repeated
`git show exhibits/tax-citizen-families/it4:<path>` commands. I did not run the
runner or tests: doing so would require reading material outside this scope.

Confidence means confidence in what the artifact declares, not confidence that
an unseen implementation honors it.

## Artifact and example readout

| Exhibit | What I can recover as a fresh reader | Lifecycle, effect, and confidence |
|---|---|---|
| `schemas/citation-attachment.v1.schema.json` | A citation attachment is a citizen binding one citation to a subject (`fact-type`, `rule`, `parameter`, or `form-field`) with a semantic role and an expected year/locator fingerprint. | `schema` is `citation-attachment.v1`; the schema makes it inert data, while a resolver must enforce the relationship. The `$id` says `it3`, which conflicts with the it4 location. Declared shape: certain; enforcement: probable. |
| `schemas/symbol-binding.v1.schema.json` | A tax-year-scoped citizen maps a fact type to the symbol a rule reads, and declares whether that mapping is a choice, attested input, source collect, closure projection, or condition projection. | `symbol-binding.v1`, identified by `id` and `tax_year`; it makes fact-type → runner-symbol correspondence content. The `$id` also says `it3`. Shape/effect: certain. |
| `schemas/scenario.v1.schema.json` | A synthetic scenario names its package, bundle, year, jurisdiction, form/citation/binding files, workspace inputs, and expected outcomes. Inputs distinguish choices, source findings, and closure booleans. | `scenario.v1`; `id` identifies the case and `expect*` fields are goldens. The schema requires only the three closure flags, so provenance resolution and actual persistence are not established by the shape alone. Certain for declaration; probable for intended runner use. |
| `content/bundle.tax-2025.json` | The bundle declares the 2025/2026 fact types: W-2 wage identity includes employer, year, and W-2 slip; interest identity includes payer, year, and box; filing/election choices; scalar closure, ordinary-deduction-eligibility, and tax-method attestations. | `bundle.v1`, id `us.tax.individual-income.2025`; facts have `supersession.policy: free`. Rules can collect distinct slips and boxes. The aggregate eligibility/method booleans carry their condition meaning in prose, not as separately identified condition citizens. Certain for declared identity and value domains. |
| `content/rules.2025.json` | Versioned 2025 US-federal rules map W-2 wages to line 1a, line-1 siblings to line 1z, taxable interest boxes 1/3 to line 2b, then compute lines 9, 11, 12, 15, and 16. Guards distinguish open sets, itemizing, ordinary eligibility, tax-table/rate-schedule bands, and alternate methods. Five projection rules turn closure/eligibility/method inputs into symbols downstream rules read. | Each rule has `id`, `version`, scope, role, `requires`, guard, value, publication, and block disposition. A rule only has package lifecycle if the package adopts it. It is readable as a dependency graph; actual adoption/execution is not independently present here. Certain for declared rule behavior; probable for runtime effect. |
| `content/package.tax-2025.json` | A v1 package adopts the ten form/computation rules, five projection rules, and three parameters, with role/id/version membership and a 2025 effective date. It declares mutual exclusion for line 12 and line 16 branches. | `artifact-package.v1`, id/version/scope identify the package. The role on each member is part of identity and can reject a role mismatch. Certain as an adoption declaration; probable as an adoption gate because no record is in scope. |
| `content/symbol-bindings.2025.json` | Filing status and rounding are direct choices; itemization is a direct choice; wages and interest are source collects; closure, eligibility, and method are raw attested inputs whose adopted projection rules publish the symbols consumed by form rules. | `symbol-binding.v1`, year 2025. The path is followable from fact type to symbol to rule, but the scenario field names (`filing_status`, `std_ordinary_eligible`, etc.) are fixture-facing names rather than fact IDs. Certain for declared correspondence. |
| `content/citation-resolver.v1.json` | The resolver is a v1, US-federal semantic contract: subject must exist with the declared kind; citation must resolve; year, jurisdiction, locator kind, allowed role locator kinds, and locator substring must agree. | Identified by resolver id/version/jurisdiction. It is a validation service/configuration, not a rule input or derived value. Certain for declared checks; adoption/invocation is only asserted in its description. |
| `content/citation-attachments.2025.json` | Eight attachments bind W-2/1099 boxes, deduction and tax-method parameters, taxable-income rule, and line 1a form field to citations with expected fingerprints. | Each is `citation-attachment.v1` and identified by attachment id; no version field is present on the individual attachment. Attachments are inert and require resolver validation. Certain for the relationships written. |
| `content/closure-projection.md` | `closed_sets` is declared as a pure function of current closure findings: complete wage/interest/line-1-other findings map to the three collect source-set names. The same finding supplies the rule pin and the empty-collect gate. | Marked “adopted” but explicitly not independent. The note says the runner currently needs an unpinnable `frozenset`; withholding it blocks an empty set. Contract meaning: certain; production lifecycle: failed/escalated. |
| `spikes/integration-substrate.md` | The intended authoritative path is bundle adoption → entity introduction → evidence → validated assertions → current-finding projection → `run_and_record` → appended publications → composed workspace currency, with coverage/explanations derived afterward. | This is a design/evidence note, not a persisted record. It clearly separates the `closed_sets` machinery gap from content projections. Certain as a declaration; only probable as proof of execution. |

### Scenario fixtures

All entries in `fixtures/scenarios.json` are `scenario.v1` records with the
same package/bundle/year/jurisdiction provenance. Their fixture role is
legible, but the file carries expected outcomes rather than the persisted
derivation record that would prove them.

| Scenario | Recovered concept and effect | Confidence |
|---|---|---|
| `w2_and_interest` | Normal path: one W-2, box 1 plus box 3 interest, all sets closed; computes through line 16 via the tax table. | Probable |
| `wages_only_closed_interest` | Empty but closed interest set produces a closure-backed line-2b zero. | Probable |
| `interest_only_closed_w2` | Empty but closed W-2 set produces a closure-backed line-1a zero; later zeros are computed. | Probable |
| `present_zero_interest` | A present `$0.00` source produces a computed zero distinct from an empty-set closure zero. | Probable |
| `box_distinction` | Box 1 and box 3 contribute to line 2b; box 8 is present but outside that source membership. | Certain from rule/fixture declarations |
| `two_w2_same_employer` | Two control-number-distinct W-2 slip entities yield two wage facts and aggregate to line 1a. | Certain for identity declaration; probable for execution |
| `itemize_true` | Itemized line-12 branch applies and standard branch is inapplicable. | Probable |
| `unclosed_interest` | A present interest source without closure blocks line 2b and downstream lines. | Probable |
| `no_source_no_closure` | An empty interest set without closure also blocks; it is distinct from present-but-open. | Probable |
| `invalid_source_value` | A closed set containing an invalid value blocks as present-but-invalid. | Probable |
| `line1z_unclosed` | Line 1a may publish, but line 1z and downstream total income block until other line-1 sources are closed. | Probable |
| `std_special_condition` | False ordinary-eligibility makes both line-12 branches inapplicable; line 12 is unpublished and downstream rules block. | Probable |
| `std_eligibility_unknown` | Missing eligibility blocks the standard rule rather than supplying a default deduction. | Probable |
| `high_income_rate_schedule` | At/above the declared `$100,000` boundary, rate schedule applies and tax table is inapplicable. | Probable |
| `alternate_method_blocked` | False ordinary-method makes both ordinary line-16 rules inapplicable and leaves line 16 unpublished. | Probable |
| `all_open` | With all choices and closures absent, every rule blocks and nothing publishes. | Probable |

### Positive and negative examples

| Exhibit | Fresh-reader interpretation | Confidence |
|---|---|---|
| `instances/positive/rule.projection.json` | A projection rule requires the closure input it references and publishes the closed symbol, so its output can pin that input. | Certain as artifact shape; probable as validator result |
| `instances/negative/rule.projection-no-require.json` | The same reference without a `requires` entry is intentionally unpinnable and should be rejected. | Certain for intended contrast |
| `instances/positive/finding.w2-correction.json` | A corrected value targets the same wage fact keyed by employer, year, and W-2 slip `acme-ctrl-001`. | Certain for same-fact identity; supersession/rederivation not shown |
| `instances/negative/finding.w2-correction-different-fact.json` | Control number `002` identifies a different wage fact, so it must not masquerade as correction of `001`. | Certain for identity distinction |
| `instances/positive/package-member.projection.json` | The projection rule is adopted as a `computation` member with id and version. | Certain |
| `instances/negative/package-member.role-mismatch.json` | The same rule id presented as a `parameter` is a role mismatch. | Certain for intended rejection |
| `instances/positive/coverage.expected.json` | Coverage should be reconstructed from the persisted `unclosed_interest` record as wage closed / interest open. | Certain for declared expectation; record derivation not visible |
| `instances/negative/coverage.stale.json` | A stored projection saying interest is closed must be rejected when the record says line 2b blocked on missing closure. | Certain for intended contrast; actual rejection not visible |
| `instances/positive/explanation.closure-zero.expected.json` | The line-2b closure-backed-zero explanation terminates at the interest-closure finding. | Certain for declared expected terminal; pin walk not visible |
| `instances/negative/explanation.fabricated.json` | A terminal id absent from the record must not be accepted as an explanation. | Certain for intended contrast |
| `instances/negative/scenario.dangling-package.json` | A schema-valid scenario whose package id does not resolve must be rejected before it can run. | Certain for intended rejection |
| `instances/negative/citation-attachment.wrong-year-reverse.json` | A 2026 parameter/citation combination with expected year 2025 is a semantic year mismatch despite schema validity. | Certain for intended rejection |
| `instances/negative/citation-attachment.wrong-role.json` | A W-2 fact-type with a form-line locator violates the wage-box role locator set. | Certain for intended rejection |
| `instances/negative/citation-attachment.wrong-subject.json` | A standard-deduction parameter attached to a rate-schedule citation violates subject/citation meaning even though the shape is valid. | Certain for intended rejection |

## I1–I9 gate readout

I number below follows the nine integration questions in the round-4 file, in
their listed order. “Closed” here means legible from the scoped exhibits; it
does not substitute for an unseen execution trace.

| Gate | Disposition | Evidence and legibility finding |
|---|---|---|
| I1 normal authoritative path | Still disputed | `spikes/integration-substrate.md`, `schemas/scenario.v1.schema.json`, `content/package.tax-2025.json`, and the normal fixture describe adoption, acts, current projections, `run_and_record`, appended publications, and composed currency. No persisted record or command output is in scope, so the sequence is recoverable as a claim, not proven end-to-end. |
| I2 adopted/pinned closure, eligibility, and method symbols | Closed for the three projection rules; failed/escalated for `closed_sets` | The five `us.rule.proj.*` rules in `content/rules.2025.json`, their package membership, symbol bindings, and `rule.projection.json` make the pin path legible. `content/closure-projection.md` and `spikes/integration-substrate.md` explicitly say the `closed_sets` input remains unpinnable and empty collects block when it is withheld. |
| I3 W-2 correction | Still disputed | The bundle's W-2 identity keys and the two finding examples make same-slip versus second-slip identity clear. They do not show an original finding, displaced current finding, append sequence, or re-derived downstream result, so same-fact supersession is not end-to-end recoverable from scope. |
| I4 package/provenance and mixed-year rejection | Still disputed | Package member roles/versions, scenario provenance, the dangling-package negative, and the wrong-year citation negative state the checks. The scoped exhibits do not include the referenced form/citation files or a persisted resolution result, so “every claimed citizen resolves” cannot be independently followed. |
| I5 record-derived coverage and explanations | Still disputed | The positive/negative coverage and explanation examples explicitly require actual records and pins, and the substrate describes deriving them after publication. The records and pin walks themselves are absent, so a fresh reader can understand the anti-hard-coding contract but cannot verify its authority. |
| I6 citation role/subject/year enforcement | Still disputed | `citation-resolver.v1.json`, the eight attachments, and three schema-valid negative examples give a clear semantic rule set. The resolver says it is invoked, but adoption/invocation and the cited source citizens are outside the scoped exhibits. |
| I7 relationship examples and bypass probes | Closed as an example set; execution remains probable | The fixture matrix covers two W-2 identities, box membership, empty/present/invalid/open sets, branch guards, thresholds, and all-open saturation. The projection, package-role, stale-coverage, fabricated-explanation, dangling-package, and three citation negatives provide readable bypass contrasts. |
| I8 scalar rewrite | Still disputed | Scalar booleans preserve an aggregate “closed / ordinarily eligible / ordinary method” value and are easy for rules to read. But the eligibility and method condition structures are only prose; the bundle does not expose the five/three constituent condition citizens described by `spikes/integration-substrate.md`. Preservation of aggregate meaning is legible; preservation of required condition structure is not proven. |
| I9 `closed_sets` escalation | Failed/escalated, but separable | `content/closure-projection.md` gives a deterministic, finding-derived contract and says stale projections cannot manufacture truth. It also states that the ratified runner consumes an unpinnable `frozenset`, so the current implementation depends on machinery outside the adopted rule/pin graph. The exhibit isolates this as a production machinery patch rather than a second content authority; until that patch is ratified and verified, the ordinary empty-source path is not contract-complete. |

## Overall legibility verdict

The content vocabulary is substantially recoverable: a fresh reader can follow
fact identity, rule publication, package roles, source-set closure, branch
guards, and citation relationship intent. The negative examples make several
semantic mismatches visible even when JSON Schema would accept them.

The contract-foundational decision is not fully legible as closed evidence yet.
The largest gaps are the absent persisted execution records, the unshown
resolver/source-citizen inputs, the unshown W-2 displacement/rederivation, and
the explicit unpinnable `closed_sets` machinery input. The latter is plausibly a
separable production patch, but the scoped exhibits do not demonstrate that
patch or make the current ordinary path independent of it. The stale `it3`
values in the three schema `$id`s are a smaller but concrete version-legibility
defect.
