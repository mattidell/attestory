# Round 4 Governance Review - Iteration 4

Reviewer: codex-governance-r4-2026-07-11  
Scope: `exhibits/tax-citizen-families/it4` at `9debc4d`  
Role: governance fidelity only

This review separates four questions for every gate: what the tagged prototype
reproduces, whether that evidence is sufficient for the citizen-family
contract, what remains a production ratification condition, and what remains
an unresolved decision. A green harness check is not treated as contract
sufficiency where the check uses a harness-local authority excluded by charter
v2.

## Measurements

### I1 - Authoritative scenario materialization

**Disposition: still disputed (mechanical path closed; scalar contract not
closed).**

**Reproduced evidence.** The tagged harness passes I1. `materialize` appends
bundle-adoption, entity-introduced, evidence-submitted, and assertion acts;
kernel projection supplies current findings; `project_run_context` reads those
findings; `run_and_record` runs with the adoption gate active; publications are
appended; and ADR-0010 composed currency is used in I3. Closure, standard-
deduction eligibility, and method arrive at the runner as attested findings and
then as outputs of package-member `us.rule.proj.*` rules, not as direct fixture
inputs to the tax rules. Exhibit: `it4/tools/integration.py`, `it4/tools/harness.py`
I1, and `it4/EVIDENCE.txt` I1.

**Contract sufficiency.** The authoritative transport is sufficient. The
meaning transported is not yet sufficient. It4 rewrites the it3 eligibility
object (five named conditions) and method object (three named triggers) to one
attested boolean each. The new projection rules are identity functions over
those booleans. The named conditions survive only in `value_schema.description`;
they are no longer findings, structured values, or rule inputs. The regression
therefore proves equality of downstream goldens after replacing the original
question with its precomputed answer; it does not prove preservation of the
condition contract. Under Articles 9-11 and ADR-0006, the tax determination
`ordinary eligible = not any(five conditions)` and the alternate-method trigger
mapping must be structurally declared and executable, not compressed into an
attestation because the operation vocabulary lacks field access.

**Production ratification condition.** A production path must validate values
before appending an assertion act, rather than allowing a schema-invalid value
to poison projection as the I5/I6 probe observes. Every run record must also pin
all five governance artifacts; it4 pins Constitution, Ontology, Principles, and
Engineering Constraints but omits Commentary, contrary to Article 14 and the
Constitution governance note.

**Unresolved decision.** Decide whether eligibility and method are (a)
structured determinable facts whose declared projection computes the aggregate,
(b) separate condition facts consumed by a declared rule, or (c) genuinely
aggregate facts whose assertion presentation and schema make the full legal
predicate the question being answered. It4 silently chooses (c) to accommodate
current machinery. That contract choice is not ratified by an integration
workaround.

### I2 - Adopted and pinned projections

**Disposition: failed and escalated.**

**Reproduced evidence.** The five symbol projections are package members, and
their derived findings pin the projection rule and attested input finding.
Withholding `us.rule.proj.interest-closed` blocks line 2b. The independent I2(c)
run also reproduces the declared failure: with the closure finding and symbol
projection present but `closure_project=False`, line 2b blocks with
`SOURCE_SET_UNCLOSED`. Exhibit: `it4/content/rules.2025.json`,
`it4/content/package.tax-2025.json`, and harness I2.

**Contract sufficiency.** I2 is sufficient for identity projections of the
five scalar inputs, subject to I1's unresolved scalar semantics. It fails for
`closed_sets`. `RunContext.closed_sets` is an unpinned `frozenset`; the mapping
from closure fact type to source-set id lives in the adapter constant
`CLOSURE_SET_2025`, not in adopted content. This is tax-bearing mapping code
under Article 11 and an unpinned dependency under Article 12/E12.1.

**Production ratification condition.** The runner must consume a versioned,
schema-declared closure-to-source-family mapping from the adopted content scope,
derive empty-set eligibility from current closure findings, and preserve the
mapping and finding in lineage. Withholding or substituting that artifact must
block or change the ordinary path.

**Unresolved decision.** The machinery mechanism is separable from the closure
fact's citizen shape: it4 strengthens the evidence that a determinable,
attested closure finding can be a `fact-type.v1`. The load-bearing relationship
between that fact and a named source family is not separable from the broader
citizen-family contract, because it determines when absence becomes a valid
zero. The current exhibit has not declared that relationship as a citizen or
adopted artifact. The full contract-foundational Tier 2 decision therefore
cannot treat `closed_sets` as a patch with all contract meaning already settled.

### I3 - W-2 correction lifecycle

**Disposition: closed.**

**Reproduced evidence.** Two W-2-slip entities from one employer/year
individuate distinct wage facts. A later finding for the first fact displaces
the original kernel finding; ADR-0010 currency displaces the dependent line 1a;
the second slip remains current; re-derivation publishes `47000`; evidence ids
remain separate. Exhibit: harness I3 and
`instances/{positive,negative}/finding.w2-correction*.json`.

**Contract sufficiency.** This closes the round-3 Article 1/7/12 objection for
the tested correction lifecycle and supports W-2-slip identity as a thing,
never a document child.

**Production ratification condition.** Preserve the same-fact and
derivation-edge tests as contract fixtures against the production workspace
path.

**Unresolved decision.** None for this bounded identity and correction claim.

### I4 - Closed package and provenance joins

**Disposition: still disputed.**

**Reproduced evidence.** `validate_package` closes over its rule/parameter
corpus, rejects tested rule and parameter scope substitutions, and accepts the
2026 package. The harness also checks fact-type year filtering on the run path
and checks form-field, citation, binding, and scenario year relationships.
Exhibit: harness I4.

**Contract sufficiency.** The package contains only rules and parameters. The
bundle/fact types, symbol bindings, form fields, citations, attachments, and
resolver are not package members. Their joins and most mixed-year rejections
are separate harness predicates over hand-built maps or year strings, not one
normal package validation path. This does not establish ADR-0006's closed-
manifest boundary or charter I4's scope checks across every claimed citizen
role.

**Production ratification condition.** Define the adopted content boundary for
all these families, make exact versions and roles load-bearing, and run both-
direction mixed-year substitutions through that validator. The later-year
positive must use the same complete boundary.

**Unresolved decision.** Decide whether these citizens are package members or
members of another versioned adopted manifest referenced by the package. A
collection of resolvable ids is not yet that contract.

### I5 - Record-derived coverage

**Disposition: failed.**

**Reproduced evidence.** The consumer reads an actual persisted completed
`derivation-record.v1`, and a contradictory stored coverage dictionary is not
read. Exhibit: harness I5.

**Contract sufficiency.** `coverage_from_record` depends on the harness constant
`FAMILY`, a hard-coded map from family names to rule ids and closure symbols.
Charter I5 requires declared content identifying covered families, and the
non-substitution rule excludes a hard-coded map. The I9 stale-map probe only
shows that one dictionary is ignored in favor of another consumer whose
meaning remains in code. It does not close Article 11 or Article 14.

**Production ratification condition.** Declare the family/rule/closure
relationship in versioned content and derive coverage fresh from persisted
records plus that content. Exercise missing non-closure dependencies and
multiple relevant records.

**Unresolved decision.** The citizen or artifact shape that declares coverage
families and their rule relationships remains open.

### I6 - Record-grounded explanations

**Disposition: failed.**

**Reproduced evidence.** Present-zero and closure-backed-zero use the production
`explain` walk over real derived pins. Removing closure blocks publication. The
other three states are found in a persisted record or kernel validation result.
Exhibit: harness I6.

**Contract sufficiency.** The no-source, invalid-source, and false-guard cases
are record/schema lookups, not explanation walks beginning at the requested
form/output disposition. This repeats the round-3 limitation that charter v2
explicitly required I6 to close. The invalid-source case has no derivation
record and does not begin from a form disposition. The positive walk's terminal
index is reconstructed from current findings rather than demonstrated as a
complete historical explanation surface. Article 15/E15.1 is not established
for all five states.

**Production ratification condition.** Provide one normal explanation API that
walks every required state from form/output disposition to acts, findings,
adopted artifacts, and persisted records, and prove removal of each real
terminal makes that walk incomplete.

**Unresolved decision.** The declared representation of pre-run invalidity and
its connection to a requested output disposition remains open.

### I7 - Citation semantic attachment

**Disposition: failed.**

**Reproduced evidence.** The harness-local resolver rejects wrong line, both
year directions, wrong role, and wrong subject; one negative is schema-valid
before semantic rejection. Exhibit: `it4/content/citation-resolver.v1.json`,
attachment negatives, and harness I7.

**Contract sufficiency.** The resolver document names schema
`citation-resolver.v1`, but the exhibit contains no corresponding schema. It has
identity, version, and dependents, so Articles 9 and 10 require declaration
before use. It is not a package member, and I4's package validation does not
invoke it; `resolve_attachment` is implemented in the harness. Consequently the
normal package validation path does not enforce the claimed contract, and the
role table is not adopted or pinned.

**Production ratification condition.** Publish the resolver schema before its
instance, include the exact resolver version in adopted scope, wire one normal
validator to it, and retain the committed semantic negatives.

**Unresolved decision.** Decide the resolver's citizen family, package role,
and pin/adoption relationship.

### I8 - Relationship examples

**Disposition: still disputed.**

**Reproduced evidence.** Hand-written positive and negative files exist for
projection pinnability, correction identity, package role, provenance,
coverage, explanation termination, and citation semantics. Harness I8/I8b
executes checks over them.

**Contract sufficiency.** The files satisfy the existence requirement, but
several are judged by the same insufficient harness authorities identified in
I4-I7. The materially changed scalar eligibility/method relationship has no
example preserving the former named conditions or proving the aggregate from
them; the method family has no corresponding committed relationship pair. A
boolean type check cannot substitute for the removed tax-condition structure.

**Production ratification condition.** Bind every example to the production
schema/validator/runner authority and add examples for the ratified resolution
of scalar condition semantics and `closed_sets` mapping.

**Unresolved decision.** I8 cannot close until the I1, I2, I5, I6, and I7
relationship contracts are settled.

### I9 - Bypass resistance

**Disposition: failed.**

**Reproduced evidence.** Withholding an asserted closure finding or an adopted
symbol-projection rule blocks downstream publication; unknown package adoption
is rejected; the harness resolver rejects a schema-valid bad citation; a stale
coverage dictionary and fabricated explanation label do not alter the tested
outputs. Exhibit: harness I9.

**Contract sufficiency.** The strongest adoption and pin bypasses are real.
The citation, coverage, and explanation probes rely on the harness-local
authorities already found insufficient. The probe does not reject the actual
`closed_sets` bypass: `extra_closed_sets` can add arbitrary source-set ids to
`RunContext` without a finding, adopted artifact, or pin. Thus the exact
load-bearing authority bypass remains available at the adapter/runner boundary.

**Production ratification condition.** Remove caller-supplied authoritative
`closed_sets`, route citation/coverage/explanation through declared production
contracts, and repeat each bypass against those entry points.

**Unresolved decision.** The normal authority boundary for source-set closure
remains the I2 decision.

## Cross-Gate Conclusions

### Scalar fact rewrite

The closure scalar is the least problematic rewrite: the it3 object admitted
only `{complete: true}`, so replacing it with `true` can preserve the bounded
claim if false continues to mean no current closure finding rather than an
asserted authoritative closure. The eligibility and method rewrites are
different. They replace multi-condition determinations and declared
projections with aggregate attestations, making the tax mapping non-executable
and removing the ability to explain which condition changed the result. That
is a contract decision forced by a machinery limitation, not evidence that the
original contract works. It remains unresolved under Articles 9-11 and 15.

### `closed_sets` separability

The failing `closed_sets` test is valuable negative evidence. It isolates a
real runner limitation and supports preserving closure as a determinable,
attested fact. A future implementation patch is separable only after the
closure-fact-to-source-family mapping is declared as adopted content and its
lineage obligation is fixed. Today that mapping is `CLOSURE_SET_2025` in code
and the runner accepts an arbitrary unpinned frozenset. Therefore the closure
citizen shape may proceed as evidence, but the complete citizen-family contract
is not ratification-ready with `closed_sets` characterized as implementation
only.

### ADR-0005 disposition

Iteration 4 materially improves the evidence chain for authoritative
materialization, adopted symbol projections, correction currency, and persisted
records. It does not yet supply sufficient evidence for the full contract-
foundational Tier 2 decision. The unresolved scalar semantics and closure
mapping are contract questions; I4-I7 also retain normal-path authority gaps.
An evaluation analysis may cite the closed portions and the explicit negative
evidence, but should not propose the whole corpus as the production contract.

## Observations

1. The tagged commands reproduce: the I1-I9 harness exits `0` with 92 passing
   checks, and the 14-scenario regression exits `0`.
2. The correction lifecycle is the clearest new governance evidence in it4 and
   closes a material round-3 gap without entering reserved T1/T2 doctrine.
3. The exhibit remains synthetic and contains no personal source material or
   absolute local paths observed during review.
4. No it4 artifact resolves T1 derived-authority, T2 stance/position,
   redaction, or multi-party authority.
5. The examination accurately escalates `closed_sets`, but its final banner
   `ALL I1-I9 CHECKS PASSED` conflicts with I2's own failed/escalated charter
   disposition and should not be read as a governance closeout.

## Dissent

I dissent from treating I1-I9 as sufficient end-to-end evidence for the full
tax citizen-family contract. I agree with the reproduced execution results and
with the examination's `closed_sets` escalation. I disagree that the scalar
eligibility/method rewrite preserves the prior contract, that coverage is
declared rather than hard-coded, that all five explanation states are walks,
that the resolver is a declared adopted contract on the normal validation path,
or that the package closes over every claimed citizen role.

## Verification

- Read the ratified governance set, governance reviewer role, charter it4 v2,
  round-4 scope, examination it4, ADR-0001/0003/0005-0010, and prior-round
  governance material.
- Inspected it4 artifacts from tag `exhibits/tax-citizen-families/it4` at
  `9debc4d`; compared the it3 object-valued facts only to measure the scalar
  rewrite.
- Did not read same-round peer reviews or commit-message bodies before
  submission.
- Reproduced `PYTHONPATH=. python3 .../it4/tools/harness.py`: exit `0`, 92
  passing checks including the explicit I2(c) escalation.
- Reproduced `PYTHONPATH=. python3 .../it4/tools/regression.py`: exit `0`, 14
  scenarios.
- Independently confirmed the missing resolver schema, four-of-five governance
  pins, package roles limited to rule/parameter roles, hard-coded
  `CLOSURE_SET_2025`, hard-coded coverage `FAMILY`, and caller-supplied
  `extra_closed_sets` path.
