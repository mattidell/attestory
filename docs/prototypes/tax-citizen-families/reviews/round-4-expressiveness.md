# Round 4 Expressiveness Review

Reviewer: codex-expressiveness-r4-2026-07-11  
Role: expressiveness and implementation results  
Round: 4  
Exhibit: `exhibits/tax-citizen-families/it4` (`9debc4d`)

## Ordering And Isolation

I read the charter, round file, role, and tagged it4 artifacts without opening
`examination-it4.md`. I then extracted the tag, ran the tagged harness and
regression, ran the adapter directly, and ran independent I1-I9 and scalar
probes. Only after those results were recorded did I open the examination. I did
not read same-round peer reviews or commit-message bodies.

Pre-examination commands:

```sh
PYTHONPATH=. python3 /tmp/tax-citizen-families-it4-review.5jrr76/docs/prototypes/tax-citizen-families/it4/tools/harness.py
PYTHONPATH=. python3 /tmp/tax-citizen-families-it4-review.5jrr76/docs/prototypes/tax-citizen-families/it4/tools/regression.py
PYTHONPATH=. python3 /tmp/tax-citizen-families-it4-review.5jrr76/docs/prototypes/tax-citizen-families/it4/tools/integration.py
```

Results: the I1-I9 harness exited 0, all 14 regression scenarios passed, and
the direct adapter run persisted 16 materialization acts, projected 11 current
kernel findings, appended 13 publications, and returned 13 current derived
findings with line 16 = 3011. A separate inline Python probe exercised I1-I9
without calling the harness checks; all ten initial assertions passed. Those
passes establish that the supplied positive route works. They do not establish
the charter's authority and bypass claims.

## Disposition

The iteration proves a useful persisted integration path, but it does not close
I1-I9 as a contract-foundational Tier 2 basis. I1 and I3 close. I2 remains
failed/escalated. I4-I7 and I9 fail. I8 is still disputed because the files are
present but several declared negative relationships have only harness-local
authority.

| Gate | Result | Basis |
|---|---|---|
| I1 | closed | Acts project real findings into `RunContext`; `run_and_record`, publication append, and composed currency are exercised. |
| I2 | failed / escalated | Symbol rules are adopted and pinned, but `closed_sets` is produced by an unadopted hard-coded adapter map and has no pin. |
| I3 | closed | Same-fact W-2 correction displaces the original and its derived chain, preserves the second slip, and re-derives 47000. |
| I4 | failed | Only rule/parameter members use package validation; other citizen and provenance checks are selective harness predicates. Bogus provenance files and bundle id run successfully. |
| I5 | failed | Coverage consumes a persisted record, but family meaning comes from the hard-coded Python `FAMILY` map, not declared content. |
| I6 | failed | Numeric explanation walks work; no-source and false-guard cases merely inspect record entries, which the charter expressly says cannot close the gate. |
| I7 | failed | The resolver is versioned content, but it is neither adopted nor called by normal package validation; `resolve_attachment` is a harness function. |
| I8 | still disputed | Relationship files exist, but several negatives pass published schemas and are rejected only by hard-coded comparisons in `i8_relationships`. |
| I9 | failed | Non-package provenance strings, hard-coded coverage authority, and explanation-index relabeling bypass the claimed resistance. |

## Findings

### 1. Coverage remains hard-coded authority (I5, I8, I9)

`harness.py` defines:

```python
FAMILY = {
    "wage-sources": ("us.rule.f1040.line1a.wages", "us.f1040.2025.wage-sources.closed"),
    "interest-sources": ("us.rule.f1040.line2b.interest", "us.f1040.2025.interest-sources.closed"),
}
```

`coverage_from_record` reads the real completion record, but this dictionary
supplies the relationship between a family, mapping rule, and closure symbol.
No adopted or declared artifact identifies covered families. The stale-map
probe does not submit contradictory state to a real consumer; it creates an
unused local dictionary and calls the same hard-coded helper again. This is the
exact authority substitution I5 and I9 prohibit.

Prototype proof: the completion record contains the expected line-2b block.  
Production condition: a consumer can reconstruct coverage from persisted
records.  
Unresolved contract: which declared citizen identifies family membership and
non-closure dependencies. Until that exists, I5 is not a machinery-only patch.

### 2. Three claimed explanation walks are not walks (I6)

Present numeric zero and closure-backed zero traverse real derived-finding pins.
The no-source case calls `rec_block`; the false-guard case calls
`rec_inapplicable`; invalid input is caught at projection and has no requested
output disposition to walk. This is inspection of blocked/inapplicable record
entries, explicitly excluded by the charter's non-substitution rule. The
examination repeats the record-terminal claim rather than disclosing that no
explanation traversal exists for those states.

Prototype proof: published numeric outputs explain through actual pins.  
Production condition: explanation needs an entry point for output dispositions
that did not publish.  
Unresolved contract: the authoritative identity and traversal shape for a
non-publication explanation.

### 3. Package and provenance closure are selective (I4, I7, I9)

`package.tax-2025.json` contains rules and parameters only. The bundle, fact
types, symbol bindings, form fields, citations, attachments, and citation
resolver are not package members. `validate_package` therefore cannot check
their claimed package/content scope. The adapter is passed a preloaded `content`
dictionary and uses only the scenario package id/version and tax year; scenario
`bundle_id`, `form_fields_file`, `citations_file`, and
`symbol_bindings_file` do not resolve content.

An independent mutation replaced all four with bogus values. The ordinary path
still published line 16 = 3011. This falsifies I4's complete provenance join and
I9's unresolved-provenance resistance. Similarly, citation semantics are
enforced by `harness.py::resolve_attachment`, not the normal package validation
path named by I7.

Prototype proof: rule/parameter package scope and selected semantic relations
can be validated.  
Production condition: every authoritative citizen role must be adopted and
resolved by the normal loader/validator.  
Unresolved contract: the package membership and pinning model for bundles,
bindings, form fields, citations, attachments, and resolver contracts.

### 4. Scalar rewriting loses condition structure and mishandles false closure

The it3 eligibility object named five conditions and the method object named
three triggers. It4 replaces each whole object with one aggregate boolean. The
individual conditions survive only in `description` prose, so no finding can
identify which condition made eligibility or method false. This is semantic
loss, not merely a serialization change.

The supporting artifacts disagree. `spikes/integration-substrate.md` says
eligibility becomes five scalar fact types and method becomes three; the actual
bundle has one aggregate boolean fact type for each. `closure-projection.md`
still defines closure using `f.value.complete == true`, although the actual
value is boolean.

The closure boolean also creates a concrete failure. I independently asserted
a schema-valid false interest-closure finding. `project_run_context` inserted
the source set into `closed_sets` based only on fact type, the line-2b rule was
inapplicable because the projected symbol was false, and `coverage_from_record`
reported the family `closed` because it saw no missing-closure block:

```text
closed_sets_contains_interest=True
line2b_disposition=inapplicable
coverage_consumer_result=closed
```

Prototype proof: true and false aggregate scalars persist and projection rules
pin them.  
Production condition: the rule language needs a declared way to project
structured conditions, or the contract needs separately identified condition
facts.  
Unresolved contract: whether eligibility/method/closure are aggregate
attestations or derivations over component facts, and what false closure means.

### 5. `closed_sets` is not yet a separable implementation detail (I2)

The examination correctly discloses that `closed_sets` is unpinnable. The gap
is larger than adding a native runner read. `integration.py` also owns the
undeclared `CLOSURE_SET_2025` mapping from fact type to source-set name, and its
projection ignores the closure value. That mapping is tax meaning outside an
adopted artifact. A production patch cannot be specified until the preceding
closure representation and family-membership contracts are settled.

Accordingly, this is not yet a separable production condition. It is evidence
of an unresolved contract that blocks the Tier 2 decision.

### 6. Explanation-index bypass succeeds (I9)

The I9 probe supplies fake metadata under the real closure finding id and then
checks only that the real id remains in the tree and an unrelated fabricated id
does not. `explain` uses the supplied index to label leaves. Reproducing the
probe and rendering the tree produced:

```text
[input] FAKE-INJECTED = 999
```

Pins preserve structural identity, but the displayed symbol and value are
replaceable by the hard-coded index. The examination's claim that the index
"relabels nothing structural" does not answer the user-visible explanation
bypass the gate is meant to resist.

## Hard Distinctions

Fact type, fact, asserted finding, and derived finding remain distinct on the
W-2 path. W-2 slip identity remains separate from evidence identity. Form-field
citizens remain distinct from output symbols. Present numeric zero and
closure-backed zero are distinguishable by pins, and non-existence remains
different from a published zero.

The weak boundary is non-publication: false guard, missing dependency, invalid
source, and no source/no closure have distinct runner outcomes, but there is no
single record-grounded explanation contract that begins at the requested form
or output disposition for all four.

## Schema Authority And Relationship Examples

The supplied positive files validate. Several negative files do not fail under
their published schema: the unpinnable projection rule is schema-valid; the
mislabelled correction is a schema-valid finding; dangling package provenance
is schema-valid; stale coverage and fabricated explanation files have no
published schema. Harness comparisons detect the intended opposition, but they
do not establish schema or normal-path authority. I8 therefore demonstrates
examples, not yet an enforceable relationship contract.

## Honesty Audit

The examination honestly reports the `closed_sets` gap, runner `KeyError`
fragility, and projection-time value validation. It overstates the rest:

- "Every gate ... ordinary path" is false for coverage, non-publication
  explanations, citation resolution, and several relationship checks.
- "scenario -> package -> ... fully resolves" omits provenance fields that the
  adapter never resolves.
- "hard-coded coverage map ... ignored" conceals that the consumer's own family
  mapping is hard-coded.
- "hard-coded explanation input index" is reported rejected even though it can
  replace rendered leaf meaning.
- The scalar change inventory does not disclose the loss of component-condition
  identity or the contradiction with `integration-substrate.md`.

## Conclusion

The persisted `ActLog -> projection -> run_and_record -> append_publications ->
workspace_currency` path is genuine, and I1/I3 are strong prototype evidence.
It4 does not supply sufficient end-to-end evidence for the citizen-family Tier
2 decision. Coverage identity, non-publication explanation identity, complete
package/provenance membership, citation resolver adoption, scalar condition
meaning, and closure-set projection remain contract work. I dissent from the
examination's eight-gates-closed disposition.

The next production step should not merely patch `closed_sets`. First ratify
the missing contracts for component conditions, source-family membership,
non-publication explanations, and package membership across all citizen roles;
then the runner/loader changes become testable production conditions rather
than new authority hidden in code.
