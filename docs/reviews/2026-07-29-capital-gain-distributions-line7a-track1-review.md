# Capital-Gain Distributions / Line 7a — Track 1 Independent Review

**Verdict: NOT READY**

## Object and posture

- Reviewed branch: `track/capital-gain-distributions-line7a-track1`.
- Orientation resolved `HEAD` to
  `7045aea36ccea5109a04277bc9a4238eb70d9461`; `git rev-parse HEAD`
  independently matched it.
- Exact implementation object:
  `b80b5c8b87d4125c55c788e20af2171206bdb5ea..b8a44e37462c464e5f9989dff24477d17f51930f`.
  The reviewed implementation commit is the latter; the checked review-charter
  commit is its direct successor.
- Evidence ceiling: Track 1 versioned schema/content citizens, publication
  evidence, focused contract tests, immutable history, and charter boundary.
  No Track 2 runtime behavior was evaluated.
- Independence: this was a fresh author-independent artifact review. The
  Builder's thread and self-assessment were not consulted.
- Freshness: after `git fetch origin --prune`,
  `git rev-list --left-right --count origin/main...HEAD` returned `0 3` and
  `gh pr list --state merged --head track/capital-gain-distributions-line7a-track1 --limit 3`
  returned no merged PR. The review object remains unmerged and is not behind
  `origin/main`.

## Measurements

1. **Range and boundary — pass.** The range contains only Track-1 content,
   three new versioned schemas, additive manifest entries, synthetic
   examples/negatives, and the focused test. It contains no evaluator,
   coordinator, admission, package-successor, line-9, line-16, QDCG,
   presentation, browser, coverage, README, retrospective, or prototype code.
2. **Exception-1 authority and checked conclusion — pass.** The committed
   bundle declares C1–C4 with the accepted identities, `{yes,no}` domains,
   no defaults, and `free` supersession. The declarative binding pins exactly
   C1–C4 and fixes the complete accepted truth table. Independent in-memory
   mutations of an `all_present_any_no` conclusion and of one component
   rejection both failed through `checked-conclusion-binding.v1`; direct
   component value mutations (`"maybe"` and `true`) rejected against each
   committed component value schema.
3. **Box-2a topology and successor universe — pass.** The new member follows
   the existing 1a/1b payer/statement/tax-year identity pattern; its independent
   2a family, horizon closure, and mapping authorize only the 2a subtotal and
   state closed-empty authority. The successor universe maps exactly 1a, 1b,
   and 2a once, and v2 recorded boxes omit 2a. Historical content/schema hashes
   and historical manifest entries are unchanged.
4. **Publication and loader evidence — pass.** The two derivation-manifest and
   one kernel-manifest additions are new filenames only. Their recorded SHA-256
   values match the corresponding exact schema bytes. All three new schema
   versions have fully resolved `demo.*` positive instances. The focused test
   routes family, closure-mapping, and form-field claims through the established
   production loader where that loader exists.
5. **Form fields, citations, and negatives — finding F1.** The committed
   line-7b form field has the required single citation pin and its printed
   locator text names the required 2025 Form 1040 Instructions paragraph.
   The multiple-citation negative rejects. The required *wrong-identity*
   mutation does not reject, however; see F1.
6. **Data safety — pass.** Range inspection found only repository-relative,
   obviously synthetic `demo.*` fixture identities and no personal or private
   material. The required envelope scan passed.

## Findings

### F1. Wrong line-7b citation identity is accepted instead of rejected

The review charter's Form-fields-and-citations measurement requires both the
wrong-identity and multiple-citation mutations to reject. The named
wrong-identity fixture supplies `demo.citation.form1040.line-7a` at
[`packages/sample_data/capital_gain_distributions_line7a_t1/negatives/form-field.v3.line-7b-wrong-citation-id.json:15`](../../packages/sample_data/capital_gain_distributions_line7a_t1/negatives/form-field.v3.line-7b-wrong-citation-id.json#L15),
but the focused test deliberately validates it rather than asserting rejection
at [`tests/test_capital_gain_distributions_line7a_t1_citizens.py:381`](../../tests/test_capital_gain_distributions_line7a_t1_citizens.py#L381).

Reproduction, run independently against the published registry:

```text
python3 - <<'PY'
import json
from pathlib import Path
from packages.derivation.loader import DERIVATION_SCHEMA_DIR
from packages.kernel.schema_registry import KERNEL_SCHEMA_DIR, SchemaRegistry
from packages.tax.loader import TAX_SCHEMA_DIR

registry = SchemaRegistry([KERNEL_SCHEMA_DIR, DERIVATION_SCHEMA_DIR, TAX_SCHEMA_DIR])
candidate = json.loads(Path(
    "packages/sample_data/capital_gain_distributions_line7a_t1/negatives/"
    "form-field.v3.line-7b-wrong-citation-id.json"
).read_text())
print(registry.validate_declared(candidate))
PY
```

Observed result:

```text
form-field.v3
```

Thus the negative does not fail at its intended load-bearing condition, and
the focused test cannot establish the charter-required rejection of an incorrect
line-7b citation identity. This finding is limited to Track 1's citation
contract evidence; it recommends no scope expansion or repair design.

## Commands run once and results

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t1_citizens
# Ran 21 tests in 2.183s — OK

python3 -m unittest tests.test_schema_registry
# Ran 10 tests in 0.070s — OK

git diff --check b80b5c8b87d4125c55c788e20af2171206bdb5ea..b8a44e37462c464e5f9989dff24477d17f51930f
# clean

python3 tools/governance_lint.py
# governance lint: conformant

python3 tools/envelope_scan.py --range main..HEAD
# clean (exit 0)
```

The independent negative/mutation probe also confirmed rejection for the
incomplete and incorrect checked-conclusion bindings, both malformed universe
fixtures, invalid family and closure-mapping fixtures, and the multiple-citation
fixture. The boolean-domain fixture validates as generic `fact-type.v2`, as its
focused test expressly documents; the committed C1–C4 value schemas themselves
reject non-`{yes,no}` values.
