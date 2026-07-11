# Round 2 Expressiveness Review

Reviewer: codex-expressiveness-r2-2026-07-11
Role: expressiveness and implementation results
Round: 2
Prototype branch: prototypes/tax-citizen-families/it2
Prototype commit reviewed: 989d9fe

I ran reproduction checks from an extracted copy of 989d9fe before opening
docs/prototypes/tax-citizen-families/examination-it2.md. I did not read
same-round peer outputs or same-round commit-message bodies before this review.

## Checks

### Coverage

Result: partial fail. The artifact set covers the core 2025 path and improves
the it1 gaps around F3 and F6, but it does not represent every chartered
fixture or evidence requirement.

F2, F3, F4, and the main positive portions of F6 are represented. The line 2b
mapping distinguishes box 1 and box 3 from excluded box 8. The
interest_only_closed_w2 scenario supplies an empty closed W-2 set and a line 1a
zero. The wages_only_closed_interest scenario supplies an empty closed 1099-INT
set and a line 2b zero. All seven requested Form 1040 fields are concrete
form-field.v1 citizens.

F1 is incomplete. The fixture corpus has only one W-2 source in every
scenario, so it does not exercise the required two-source identity pressure
(same employee/employer/year, or a corrected/reissued source). The harness
peerage check computes the same hash twice and mutates a hand-built finding's
evidence_ids; it does not run a two-source fixture or evidence replacement
through the scenario runner.

F5 is incomplete. It has present-zero, empty-closed, and present-invalid
states, plus a present-but-unclosed state. It has no empty source set with no
closure assertion, which is a separate required matrix state.

F7 is only declared and partially exercised. The form-field content declares
all five rendered-absence dispositions, and the runner can produce an
inapplicable line-12 itemized disposition. The committed scenarios all set
itemize_election to false, so no scenario exercises the guard state, and the
harness explanation walk covers only the line 2b closure-backed zero, not all
F5/F7 states.

F8 has citation catalog coverage but not citation placement coverage. The
seven form fields reference line citations. The W-2, 1099-INT, standard
deduction, and rate-schedule citations are present and resolved, but are
orphaned: rules, parameters, and fact types have no citation binding. This
does not satisfy the charter requirement that each named fact/rule cite its
official source.

F9 is incomplete. The 2026 artifacts demonstrate distinct validation and a
mixed-year package rejection, but there is no later-year execution fixture,
no old-year/later-year positive pair, and no structural source-box evolution
probe. The committed scenario set is 2025 only.

F10 has useful edge evidence, but not a complete correction record. The
harness changes the source finding_id and re-runs the calculation; it does not
materialize a same-fact correction/supersession act. The downstream
displacement calculation is still a useful test of derived-edge reachability.

F11's stale projection probe is represented, but the required coverage rebuild
is not. The harness coverage_report ignores its result argument and returns
closed or open directly from fixture booleans. Re-serializing that same
dictionary twice is byte-identical, but it is not deletion and rebuild from an
act log, read model, and derivation records.

F12 has positive content and six hand-written negative mutations in the
harness, including undeclared shape and wrong schema version. The evidence is
runtime-checkable, although the negatives are code-local mutations rather than
committed example files.

Exhibit:

~~~sh
python3 - <<'PY'
import json
from pathlib import Path
p = Path('/tmp/tcf-it2-review/docs/prototypes/tax-citizen-families/it2/fixtures/scenarios.json')
s = json.loads(p.read_text())
print('fixtures=' + ','.join(s))
print('max_w2_sources=' + str(max(len(v.get('wage_sources', [])) for v in s.values())))
print('f5_empty_open=' + str(any(not v.get('interest_box1') and not v.get('interest_box3') and not v.get('interest_closed') for v in s.values())))
print('f7_guard_fixture=' + str(any(v.get('itemize_election') is True for v in s.values())))
print('f9_scenario_years=' + str(sorted({2025})))
PY
~~~

Output:

~~~text
fixtures=w2_and_interest,wages_only_closed_interest,interest_only_closed_w2,present_zero_interest,box_distinction,unclosed_interest,invalid_source_value
max_w2_sources=1
f5_empty_open=False
f7_guard_fixture=False
f9_scenario_years=[2025]
~~~

### Reproduction

Result: pass for the claims the harness actually tests; coverage claims are
falsified as described above. The extracted artifact harness passed all 77
checks with both runners and deterministic repeat runs. The independent
citation-text mutation also left output unchanged. A direct guard probe
produced line12.itemized: inapplicable, guard_result=False, but this is a
reviewer probe, not a committed fixture.

Exhibit:

~~~sh
git archive 989d9fe docs/prototypes/tax-citizen-families/it2 | tar -x -C /tmp/tcf-it2-review
PYTHONPATH=. python3 /tmp/tcf-it2-review/docs/prototypes/tax-citizen-families/it2/tools/harness.py
~~~

Output:

~~~text
============================================================
ALL CHECKS PASSED
~~~

Exhibit:

~~~sh
PYTHONPATH=. python3 - <<'PY'
import importlib.util
import json
from pathlib import Path
p = Path('/tmp/tcf-it2-review/docs/prototypes/tax-citizen-families/it2/tools/harness.py')
spec = importlib.util.spec_from_file_location('h', p)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
c = h.load_content()
f = json.loads((p.parent.parent / 'fixtures/scenarios.json').read_text())['w2_and_interest']
f['id'] = 'cite_parity'
def canon():
    return h.canonical_pubs(h.run(h.build_context(f, c), h.DerivationSchemas()))
a = canon()
c['citations'][0]['locator']['ref'] = 'mutated locator'
b = canon()
print('citation_text_mutation_changes_output=' + str(a != b))
print('result=' + ('PASS' if a == b else 'FAIL'))
PY
~~~

Output:

~~~text
citation_text_mutation_changes_output=False
result=PASS
~~~

### Schema Authority

Result: pass for the declared schema checks, with an expressiveness caveat.
The harness validates the new JSON Schemas, validates fact types, rules,
parameters, and package through the published runtime registry, and rejects
the negative mutations. The positive form-field and citation instances
validate; the negative extra-property, wrong-version, invalid-domain,
malformed-rule, bad-citation, and roleless-pin cases fail.

The caveat is scope: the citation negative checks the resolver's recomputed
flag rather than a consumer binding, and the rule/parameter/fact-type
citations that the charter asks for do not exist as schema-linked content.
Strictness itself is demonstrated; complete citation authority is not.

Exhibit:

~~~sh
PYTHONPATH=. python3 /tmp/tcf-it2-review/docs/prototypes/tax-citizen-families/it2/tools/harness.py | sed -n '1,13p;59,65p;99,105p'
~~~

Output:

~~~text
[PASS] it2 schemas are valid JSON Schema
[PASS] all 7 tax fact types conform to UNCHANGED kernel fact-type.v1
[PASS] tax fact-type bundle conforms to kernel bundle.v1
[PASS] all 8 rule artifacts conform to rule-artifact.v1
[PASS] all parameters conform to parameter-declaration.v1
[PASS] artifact package is closed + unique-output-valid
[PASS] all 7 form-field citizens conform to form-field.v1
[PASS] all 12 citations conform + resolved-flag honest
[PASS] every form field binds a real symbol and a real citation
[PASS] F12 negative rejected: W-2 wage value '-50.00' (below declared domain)
[PASS] F12 negative rejected: rule with add/args=[] (empty operand list)
[PASS] F12 negative rejected: form field with an undeclared property (no tolerant reader)
[PASS] F12 negative rejected: form field naming an undeclared schema version (form-field.v2)
[PASS] F12 negative rejected: citation resolved=true with no locator (F8 mutation)
[PASS] F12 negative rejected: derived finding with a bare id pin (no role)
[PASS] F9 2026 citation us.cite.std-deduction-2026 conforms
[PASS] F9 2026 citation us.cite.f1040-2026.line1a conforms
[PASS] F9 well-formed 2026 package validates
[PASS] F9 mixed-year package (2025 member in 2026 package) is REJECTED
~~~

### Hard Distinctions

Result: mixed.

- Fact type vs fact vs finding: partial. bundle.tax-2025.json declares
  identity keys and value domains, and runner findings have distinct finding
  ids. The F1 identity calculation is hand-built in the harness and the
  fixtures do not carry concrete fact ids or two W-2 instances, so the
  end-to-end identity/evidence distinction is not demonstrated.
- Form field vs output symbol: pass. The seven form-field citizens carry form
  identity and binds_symbol; the runner continues to publish only the
  abstract output symbol.
- Computed zero vs closure-backed zero: pass where exercised. A present zero
  pins a source finding, while an empty closed set pins the closure choice
  finding. The W-2 and 1099-INT empty-closed scenarios provide both families.
- Blocked unclosed vs blocked invalid: pass where exercised. The runner
  produces DEPENDENCY_ABSENT for the open source set and DEPENDENCY_INVALID for
  not-a-number, with no publication.
- Guard/non-existence: declared and runner-supported, but not scenario-backed
  or explanation-walk-backed. The custom probe found the itemized branch
  disposition inapplicable with guard_result=False.

Exhibit:

~~~sh
nl -ba /tmp/tcf-it2-review/docs/prototypes/tax-citizen-families/it2/tools/harness.py | sed -n '417,451p;458,488p'
~~~

Relevant output:

~~~text
417 def coverage_report(fixture: dict[str, Any], result: RunResult) -> dict[str, str]:
421     report["wage-sources"] = "closed" if fixture.get("wage_closed") else "open"
422     report["interest-sources"] = "closed" if fixture.get("interest_closed") else "open"
443     # Coverage recomputed twice is byte-identical (delete-and-rebuild, E5.1/E7.1)
458 def explanation_walks(content: dict[str, Any]) -> None:
460     fixture = load_json(FIXTURES / "scenarios.json")["wages_only_closed_interest"]
474     print("\n--- explanation walk: line 2b closure-backed zero ---")
478     check("F5/F7 closure-backed zero on line 2b PINS the interest closure finding",
~~~

### Gap Reporting

Result: fail for the required implementation check, pass for the stale-string
rejection. The stale projection probe is useful: an injected closed_sets entry
without a closure finding does not publish line 2b. However, coverage_report
derives its answer only from fixture booleans and ignores the RunResult, act
log, read model, and derivation records. Its two rebuilds are the same
in-memory calculation serialized twice. It reports an open interest set, but
does not prove that current-state coverage is recomputable from records or
that a stale stored coverage projection is ignored as such.

Exhibit:

~~~sh
nl -ba /tmp/tcf-it2-review/docs/prototypes/tax-citizen-families/it2/tools/harness.py | sed -n '417,451p'
~~~

Output:

~~~text
417 def coverage_report(fixture: dict[str, Any], result: RunResult) -> dict[str, str]:
418     """Coverage derived fresh from current closure findings + the run's blocks --
421     report["wage-sources"] = "closed" if fixture.get("wage_closed") else "open"
422     report["interest-sources"] = "closed" if fixture.get("interest_closed") else "open"
447     cov1 = json.dumps(coverage_report(honest, res), sort_keys=True)
448     cov2 = json.dumps(coverage_report(honest, res), sort_keys=True)
~~~

### Honesty Audit

Result: fail. The examination honestly discloses the closure blocking-code
tradeoff, the line 16 rate-schedule simplification, the narrow AGI case,
unexercised governed supersession, and lack of storage-level fault injection.
It does not disclose the material negative results found here. In particular,
it states that F1 has the required evidence mutation, that F5 has four states
and explanation paths, that F7 has a fixture-backed false guard, that F8
citations are referenced by rules/parameters, that F9 has the required
old-year/later-year positives, and that F11 coverage is rebuilt from current
findings. Those statements exceed the artifacts and harness.

The examination's all checks passed statement is accurate for the harness's
implemented checks, but its fixture evidence map and Q3/Q5/Q9 answers turn
those checks into broader claims that the prototype does not reproduce.

## Observations

The strongest it2 evidence is the declared closure finding pin: unlike the
native closed_sets convenience, the empty-set zero has a choice pin, and the
stale projection does not create a zero by itself. The box-to-line mapping and
the distinct invalid/unclosed block behavior are also concrete and portable
across both runners.

Compared with it1, it2 materially closes the prior F3 gap and provides all
seven concrete form-field citizens, addressing the prior F6 weakness. The
comparison also matters in the opposite direction: it1 had two W-2 source
findings and an explicit coverage mutation record, while it2 has only one W-2
source per fixture and a boolean-only coverage helper. Both iterations provide
useful line-2b distinctions; neither prototype establishes complete citation
binding for every named fact/rule/parameter.

The new form-field family is expressively promising, but its rendered-absence
meaning is not yet demonstrated as a complete artifact-and-record recovery
contract. The next iteration should add the missing matrix state, two-source
peerage/correction scenarios, per-state explanation walks, citation links for
all named content, a real coverage rebuild/stale projection test, and executed
cross-year positives.

## Dissent

I dissent from the examination's claims that:

- F1 is fully covered by the hand-built hash/evidence mutation;
- F5 has all four required states and explanation-walk evidence;
- F7 has fixture-backed false-guard and rendered-absence evidence;
- F8 places citations on every named fact/rule/parameter;
- F9 has the complete old-year/later-year and structural evolution probe; and
- F11 rebuilds coverage from current records rather than fixture booleans.

The reproduction result is strong, but these omissions prevent the examination
from being accepted as a complete expressiveness result for the charter.

## Verification

git diff --check -- docs/prototypes/tax-citizen-families/reviews/round-2-expressiveness.md
was run after writing this file and produced no output. Because the review is
new and untracked, git diff --check --no-index /dev/null
docs/prototypes/tax-citizen-families/reviews/round-2-expressiveness.md was also
run; it produced no whitespace warnings and returned the expected nonzero
comparison status.
