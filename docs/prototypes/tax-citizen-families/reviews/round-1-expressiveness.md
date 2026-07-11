# Round 1 Expressiveness Review

Reviewer: codex-expressiveness-r1-2026-07-11
Role: expressiveness and implementation results
Round: 1
Prototype branch: `prototypes/tax-citizen-families/it1`
Prototype commit reviewed: `88f0139`

Ordering note: I ran reproduction checks from the `88f0139` artifact snapshot
before opening `docs/prototypes/tax-citizen-families/examination-it1.md`.

## Checks

### Coverage

Result: partial fail.

F1, F2, F4, F5, F7, F8, F9, F10, F11, and F12 are represented well enough for
this reviewer seat. F3 is not represented as chartered, and F6 is only partly
represented.

F3 requires an empty closed W-2 set with a closure-backed zero wage value. The
scenario has two W-2 source instances and a W-2 closure finding, but no no-W-2
fixture and no zero line 1a derived finding.

Exhibit:

```sh
jq -r '[.source_instances[] | select(.source_family == "w2")] as $w2 | [.closure_findings[] | select(.symbol == "tax.2025.source-set.w2.closed")] as $closures | "w2_source_count=\($w2|length)", "w2_closure_count=\($closures|length)", "w2_zero_derived=" + (([.derived_findings[]? | select(.symbol == "tax.2025.form1040.line1a" and .value == "0")] | length) | tostring)' /tmp/tcf-it1-review/docs/prototypes/tax-citizen-families/it1/scenarios/synthetic-slice.json
```

Output:

```text
w2_source_count=2
w2_closure_count=1
w2_zero_derived=0
```

F6 requires the Form 1040 core fields to be represented with enough declared
meaning for rules, rendering, source citations, and explanation. The scenario
has derived symbols for the core lines, but the only concrete `form-field.v1`
instance is line 2b. Line 9 is absent from the source catalog output below, and
the other core lines do not have concrete form-field citizens in the artifact
set.

Exhibit:

```sh
find /tmp/tcf-it1-review/docs/prototypes/tax-citizen-families/it1 -path '*form-field*.json' -type f | sed 's#/tmp/tcf-it1-review/docs/prototypes/tax-citizen-families/it1/##' | sort
```

Output:

```text
examples/negative/form-field.bare-line11.json
examples/positive/form-field.form1040.line2b.json
schemas/form-field.v1.schema.json
```

Exhibit:

```sh
jq -r '.derived_findings[] | select(.symbol|test("form1040.line(1a|2b|9|11|12|15|16)")) | [.id, .symbol, ((.pins // [])|join(","))] | @tsv' /tmp/tcf-it1-review/docs/prototypes/tax-citizen-families/it1/scenarios/synthetic-slice.json
```

Output:

```text
derived.form1040.line1a.2025	tax.2025.form1040.line1a	finding.w2-main.box1.2025,finding.w2-bonus.box1.2025,finding.close-w2.demo-001.2025,tax.2025.rule.w2-box1-to-form1040-line1a.v1,irs.2025.form1040.line1a
derived.form1040.line2b.2025	tax.2025.form1040.line2b	finding.1099int-bank.box1.2025,finding.close-1099int.demo-001.2025,tax.2025.rule.1099int-box1-to-form1040-line2b.v1,irs.2025.form1099int.box1,irs.2025.form1040.line2b
derived.form1040.line9.2025	tax.2025.form1040.line9	derived.form1040.line1a.2025,derived.form1040.line2b.2025
derived.form1040.line11b.2025	tax.2025.form1040.line11b	derived.form1040.line9.2025,irs.2025.form1040.line11b
derived.form1040.line12e.2025	tax.2025.form1040.line12e	irs.2025.instructions1040.standard-deduction
derived.form1040.line15.2025	tax.2025.form1040.line15	derived.form1040.line11b.2025,derived.form1040.line12e.2025
derived.form1040.line16.2025	tax.2025.form1040.line16	derived.form1040.line15.2025,finding.filing-status.single.2025,irs.2025.instructions1040.tax-table-row-26550-single
```

Exhibit:

```sh
jq -r '.sources[] | select(.id|test("form1040.line(1a|2b|9|11|12|15|16)")) | [.id, .locator] | @tsv' /tmp/tcf-it1-review/docs/prototypes/tax-citizen-families/it1/source-catalog.json
```

Output:

```text
irs.2025.form1040.line1a	page 1, Income, line 1a
irs.2025.form1040.line2b	page 1, Income, lines 2a and 2b
irs.2025.form1040.line11b	page 2, Tax and Credits, line 11b
irs.2025.form1040.line12e	page 2, Tax and Credits, line 12e
irs.2025.form1040.line15	page 2, Tax and Credits, line 15
irs.2025.form1040.line16	page 2, Tax and Credits, line 16
```

### Reproduction

Result: pass, with the coverage caveats above.

The validator passes from an extracted copy of commit `88f0139`.

Exhibit:

```sh
rm -rf /tmp/tcf-it1-review && mkdir -p /tmp/tcf-it1-review && git archive 88f0139 docs/prototypes/tax-citizen-families/it1 | tar -x -C /tmp/tcf-it1-review && python3 /tmp/tcf-it1-review/docs/prototypes/tax-citizen-families/it1/validators/validate_it1.py /tmp/tcf-it1-review/docs/prototypes/tax-citizen-families/it1
```

Output:

```text
OK: positives validate, negatives fail for declared reasons, scenario checks pass
```

### Schema Authority

Result: pass with one caveat.

All positive examples validate, all negative examples fail, and the undeclared
schema version is rejected. The caveat is that
`negative/form-field.bare-line11.json` is not an isolated negative for the bare
line 11 locator. It also fails because it omits required rendered-absence
members. That does not make the rejection wrong, but it weakens the evidence
that the declared reason is independently enforced.

Exhibit:

```sh
python3 - <<'PY'
import importlib.util
from pathlib import Path
root = Path('/tmp/tcf-it1-review/docs/prototypes/tax-citizen-families/it1')
spec = importlib.util.spec_from_file_location('validate_it1', root/'validators/validate_it1.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
schemas = mod.load_schemas()
for kind, directory in [('positive', root/'examples/positive'), ('negative', root/'examples/negative')]:
    for path in sorted(directory.glob('*.json')):
        inst = mod.load_json(path)
        errors = mod.validate_instance(inst, schemas) + mod.semantic_errors(path, inst)
        print(f'{kind}/{path.name}: ' + ('PASS' if not errors else 'FAIL: ' + ' | '.join(errors)))
PY
```

Output:

```text
positive/citation.form1040.line1a.json: PASS
positive/coverage-report.open-interest.json: PASS
positive/form-field.form1040.line2b.json: PASS
positive/rule-content-binding.interest-line2b.json: PASS
positive/source-field.1099int.box1.json: PASS
positive/tax-fact-type.w2-box1.json: PASS
negative/citation.missing-locator.json: FAIL: 'locator' is a required property
negative/coverage-report.authoritative-state.json: FAIL: False was expected | False was expected
negative/form-field.bare-line11.json: FAIL: 'closure_backed_zero' is a required property | 'blocked_unclosed_source' is a required property | 'blocked_invalid_source' is a required property | 'guard_inapplicable' is a required property | TY2025 Form 1040 AGI locator is line 11b, not bare line 11
negative/rule-content-binding.citation-operative.json: FAIL: False was expected
negative/source-field.box2-misbridged-to-line2b.json: FAIL: 1099-INT box 2 early-withdrawal penalty cannot feed Form 1040 line 2b
negative/tax-fact-type.document-child-identity.json: FAIL: False was expected
negative/undeclared-schema-version.json: FAIL: undeclared schema 'form-field.v2'
```

### Hard Distinctions

Result: pass for the exercised 1099-INT line-family and W-2 peerage path;
partial for broader coverage because F3 and F6 are incomplete.

Fact type, fact, and finding are separable in the W-2 evidence: the positive
tax fact type is a declared content artifact, while scenario findings carry
separate finding ids and fact ids. W-2 identity keys avoid source-document
identity. The 1099-INT source finding has a fact id and evidence id, but it does
not carry the same explicit identity-key detail as the W-2 findings.

Exhibit:

```sh
jq -r '.source_findings[] | [.id, .fact_id, .symbol, ((.identity_keys|keys_unsorted? // [])|join(",")), ((.evidence_ids // [])|join(","))] | @tsv' /tmp/tcf-it1-review/docs/prototypes/tax-citizen-families/it1/scenarios/synthetic-slice.json
```

Output:

```text
finding.w2-main.box1.2025	fact.w2-box1.demo-001.demo-north.demo-main.2025	tax.2025.w2.box1	taxpayer,employer,employment_engagement,tax_year,source_field	evidence.w2.demo-main.original
finding.w2-bonus.box1.2025	fact.w2-box1.demo-001.demo-north.demo-bonus.2025	tax.2025.w2.box1	taxpayer,employer,employment_engagement,tax_year,source_field	evidence.w2.demo-bonus.original
finding.1099int-bank.box1.2025	fact.1099int-box1.demo-001.demo-bank.2025	tax.2025.1099-int.box1		evidence.1099int.demo-bank.original
```

Form field and output symbol are distinct in the line 2b example.

Exhibit:

```sh
jq -r '.id + "\t" + .logical_symbol + "\t" + .printed_locator' /tmp/tcf-it1-review/docs/prototypes/tax-citizen-families/it1/examples/positive/form-field.form1040.line2b.json
```

Output:

```text
irs.form1040.2025.line2b	tax.2025.form1040.line2b	line 2b
```

Computed zero, closure-backed zero, blocked states, and guard/non-existence are
distinct for the 1099-INT line-family.

Exhibit:

```sh
jq -r '.rendered_absence_states[] | [.state, (.publish_finding|tostring), (.artifact_guard // "none"), .explanation_terminal] | @tsv' /tmp/tcf-it1-review/docs/prototypes/tax-citizen-families/it1/scenarios/synthetic-slice.json
```

Output:

```text
computed_zero	true	none	finding.1099int-zero.box1.2025
closure_backed_zero	true	none	finding.close-1099int.demo-001.2025
blocked_unclosed_source	false	none	block.rule.1099int-box1-to-line2b.SOURCE_SET_UNCLOSED
blocked_invalid_source	false	none	validation-result.1099int-box1.negative-money
guard_inapplicable	false	tax.2025.rule.line16-qualified-dividend-tax.v1	derivation-record.disposition.line16-qualified-dividend-tax.inapplicable
```

### Gap Reporting

Result: pass.

The coverage report is explicitly non-authoritative, reports an open 1099-INT
source set without storing form state, and the stale closed projection is
rejected when it lacks a current closure finding.

Exhibit:

```sh
jq -r '.authoritative_state as $auth | .source_sets[] | [.source_set, .closure_state, (.closure_finding_id // "null"), (.gap_code // "null"), ($auth|tostring)] | @tsv' /tmp/tcf-it1-review/docs/prototypes/tax-citizen-families/it1/examples/positive/coverage-report.open-interest.json
```

Output:

```text
w2	closed	finding.close-w2.demo-001.2025	null	false
1099-int	open	null	SOURCE_SET_UNCLOSED	false
```

Exhibit:

```sh
jq -r '.mutations.coverage_rebuild | [.deleted_projection, .byte_equal, .stale_injected_projection.closure_state, (.stale_injected_projection.closure_finding_id // "null"), .stale_result, .reason] | @tsv' /tmp/tcf-it1-review/docs/prototypes/tax-citizen-families/it1/scenarios/synthetic-slice.json
```

Output:

```text
true	true	closed	null	reject	closed projection has no current closure finding
```

### Honesty Audit

Result: partial fail.

The examination discloses several negative results and its validator claim
reproduces. It overclaims coverage for F3 and F6:

- F3 is described as covered by a closure pattern, but the artifacts do not show
  the required empty closed W-2 source set with a closure-backed zero wage value.
- F6 is described as represented by scenario lines, but most core fields do not
  have concrete form-field citizens and line 9 is missing from the source
  catalog output.
- The examination says negatives fail for declared reasons, but the bare line
  11 negative fails for extra schema-shape reasons in addition to the declared
  semantic reason.

## Observations

The candidate shape is promising: companion `tax-fact-type.v1`, first-class
`form-field.v1`, explicit `source-field.v1`, non-operative citations, and
non-authoritative coverage reports are all expressive enough for the parts that
are actually exercised.

The strongest expressiveness evidence is the 1099-INT line 2b slice. It shows
source-box meaning, line meaning, closure-backed zero, computed zero, blocked
unclosed source, invalid source, citation parity, and stale coverage rejection.

The weaker evidence is breadth. The prototype often demonstrates one line or
one family and then generalizes in prose. That is acceptable for a sketch only
where the charter asks for a pattern; it is not enough where the charter names
specific fixtures such as empty W-2 closure and core Form 1040 field coverage.

## Dissent

I dissent from the examination's claim that F3 is covered.

I dissent from the examination's claim that F6 is fully covered.

I do not dissent from the examination's core Q1/Q2 conclusion that kernel
`fact-type.v1` can remain the question contract while tax-specific companion
families carry citations, form fields, source fields, and closure semantics.

## Verification

`git diff --check -- docs/prototypes/tax-citizen-families/reviews/round-1-expressiveness.md`
produced no output. Because the file is untracked, I also ran
`git diff --check --no-index /dev/null docs/prototypes/tax-citizen-families/reviews/round-1-expressiveness.md`;
it produced no whitespace warnings. Its exit code is nonzero because the file
differs from `/dev/null`.
