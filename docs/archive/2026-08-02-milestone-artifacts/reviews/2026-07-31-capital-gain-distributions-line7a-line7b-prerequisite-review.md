# Capital-Gain Distributions / Line 7a — Line 7b Prerequisite Review

Charter:
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-31-capital-gain-distributions-line7a-line7b-prerequisite-review.md`

Role: existing author-independent Luna Reviewer, with no exposure to the
Builder's implementation process.

## Echo

- **Resolved launch commit:** `ec438d48e77c3f48508b88da7c6cf7ef74b4bfe6`;
  verified equal to `git rev-parse HEAD` before measurement.
- **Reviewed object:** `16c6f63e946686f3f590de504c5ce05882519235..
  87e004f244254fba85ac9819fe9086ba957326f7`, one immediate-child
  implementation commit titled `Add line 7b prerequisite successors`.
- **Exact file set:** line-7b field v2, core package v8, registry v3,
  synthetic release v3, synthetic adoption v8, the deterministic FRRS
  generator, and the focused prerequisite test module — exactly seven files.
- **Credited evidence:** Track 2 merged through PR #120 with green `verify`.
  Its reviewed line-7b rule and line-7a/9/16 runtime behavior remain credited
  except where this seven-file delta could disturb them.
- **Generic-join invariant:** the unchanged projector indexes run dispositions
  by their declared symbol, falling back to the resolved rule's `publishes`
  for rows without a symbol, then joins a resolved form field's
  `binds_symbol` to exactly one row. Line 7b must join only because field v2's
  `binds_symbol` equals the unchanged rule's `publishes`; no tax-specific
  projector branch is permitted.
- **Evidence ceiling:** resolved graph plus authoritative synthetic
  `live_coordinate_run`; Track-3 projection and rendering are excluded.
- **Immutable-history boundary:** existing field v1, package v7, v1/v6 and
  v2/v7 registry/release/adoption routes, published schemas, and recorded
  checksums must remain byte-identical to the repair-charter parent.
- **Stop conditions:** object drift; historical-byte mutation; field-v2 tax
  meaning, citation, or disposition drift beyond the generic-symbol repair;
  both field versions or unrelated content in v8; broken checksum edges;
  nondeterministic generation; disturbed line-7b rule or line-7a/9/16
  behavior; a `RunContext` shortcut; weakened tests; or governance/private
  material. None fired.

## Measurements

### 1. Object custody and immutable history

`git show --format=fuller --stat --name-status 87e004f` establishes that the
implementation is the immediate child of repair charter `16c6f63` and changes
exactly the seven named files: six additions and one generator modification.
No administrative file rode inside the implementation object.

The following comparison returned exit 0 with no diff:

```text
git diff --exit-code 16c6f63..87e004f -- \
  packages/content/tax/2025/form1040.line-7b.form-field.json \
  packages/content/tax/2025/package.core-calculations.v7.json \
  packages/content/tax/2025/published-packages.json \
  packages/content/tax/2025/published-packages.v2.json \
  packages/sample_data/frrs_t3/adoptions/adopt-core-v6-current.json \
  packages/sample_data/frrs_t3/adoptions/adopt-core-v7-current.json \
  packages/sample_data/frrs_t3/publication_surface/releases/demo.release.2025.v1.json \
  packages/sample_data/frrs_t3/publication_surface/releases/demo.release.2025.v2.json \
  packages/schemas \
  packages/derivation/production_resolver.py \
  packages/derivation/presentation_projection.py \
  packages/content/tax/2025/rule.form1040-line7b.json
```

Thus field v1, package v7, both historical publication routes, every published
schema/checksum manifest, the existing rule, resolver, and generic projector
are byte-identical to the repair-charter parent.

### 2. Field successor

Parsed comparison of field v2 against v1 established:

```text
field_equal_after_version_symbol_normalization True
field_identity True
citation_equal True
dispositions_equal True
field_v2_binds_rule_publishes True
```

The only semantic changes are `version: "v2"` and `binds_symbol` changed to
`tax.us.2025.form1040.line7b-schedule-d-not-required`, exactly the unchanged
line-7b rule's `publishes`. The fixed `"checked"` rendering instruction,
atomic blocked and guard-inapplicable meanings, exact
`tax.us.2025.citation.form1040.line-7b@v1` identity, form identity, label, and
description all remain unchanged.

**Field successor: satisfied.**

### 3. Package exclusivity and registry additivity

After normalizing v8's package version/checksum and removing the one new
field-v2 member, its parsed document equals package v7 exactly. V8 contains:

```text
line-7b field members:
[tax.us.2025.form1040.line-7b@v2]
```

It contains no line-7b field v1 member. V7 still contains no line-7b field
member. No unrelated package member, entrypoint, binding, obligation, or
admission changed.

After removing exactly the field-v2 citizen entry and package-v8 entry,
registry v3 equals registry v2 exactly.

**Package exclusivity: satisfied.**

### 4. Publication checksum verification and fail-closed mutations

Independent recomputation using the production checksum functions and exact
file bytes established:

```text
field-v2 citizen checksum == registry-v3 citizen checksum          True
package-v8 instance checksum == package self-checksum              True
package-v8 instance checksum == registry-v3 package checksum       True
package-v8 instance checksum == adoption-v8 package checksum       True
sha256(registry-v3 bytes) == release-v3 registry attestation       True
sha256(release-v3 bytes) == adoption-v8 release checksum           True
```

The recomputed digests were:

```text
field v2:    aab09865eb9c7fe18ab6ab50e5b99ce8cd48a0d2ad557c43bfce81def31319a8
package v8:  d92d2d266a0e30f3974dbb16368926f5571636bf11f85544bfb501018ab0442d
registry v3: 6ca74479ea35a7a91f0478703e8dc28db9a243aa833456268f3ccbf16e9e643e
release v3:  2f6a3de770e71238b7c0a94582a6ff3ab7952583aecac6d57ec7190adbb1448e
```

The Reviewer copied the publication surface into isolated temporary
directories, mutated each new edge independently, and invoked the unchanged
production resolver. Results:

```text
baseline                            ResolvedGraph
member body checksum mutation       Refusal: MEMBER_ABSENT_OR_MISMATCH
package body checksum mutation      Refusal: PACKAGE_ABSENT_OR_MISMATCH
registry byte mutation              Refusal: REGISTRY_CHECKSUM_MISMATCH
release body checksum mutation      Refusal: RELEASE_ABSENT_OR_MISMATCH
adoption release checksum mutation  Refusal: RELEASE_ABSENT_OR_MISMATCH
adoption package checksum mutation  Refusal: PACKAGE_ABSENT_OR_MISMATCH
```

Every edge fails closed through existing verification; no new resolver path or
exception is involved.

**Publication verification: satisfied.**

### 5. Deterministic generator ownership

The Reviewer invoked both renderer functions in memory and compared their maps
against committed bytes:

```text
line-7b prerequisite content map: 3 rendered / 3 committed / equal
FRRS fixture map:                 16 rendered / 16 committed / equal
missing []
extra []
```

The three new content files and the v3 release/v8 adoption route regenerate
exactly. The implementation-range byte comparison in Measurement 1 proves all
prior v1/v2 routes retain their prior bytes.

**Generator ownership: satisfied.**

### 6. Production-shaped resolved behavior

Direct grep found `live_coordinate_run` imported and called by the focused
module and no `RunContext` reference. The helper patches only the existing
presentation call seam so this prerequisite stops at the chartered
resolved-member/disposition boundary; the coordinator, resolver, marshalling,
runner, and act-log entry remain production-shaped.

Independent runs produced:

```text
v8 eligible             line 7b published
v8 missing C4 authority line 7b blocked(DEPENDENCY_ABSENT)
v8 conclusion "yes"     line 7b inapplicable with guard_result false
```

Every v8 run resolved exactly one line-7b field:
`tax.us.2025.form1040.line-7b@v2`, whose `binds_symbol` equals the unchanged
rule's publication symbol. Blocked and guard-inapplicable rows contain no
value.

The v7 live control still publishes the existing rule result while resolving
zero line-7b form-field members. That proves the successor does not retrofit or
mutate the historical package.

**Production-shaped behavior: satisfied.**

### 7. Regression and safety

The Reviewer ran each charter command once:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_line7b_prerequisite
Ran 5 tests in 2.735s
OK

python3 -m unittest tests.test_capital_gain_distributions_line7a_t2_coordinator
Ran 9 tests in 5.162s
OK

python3 -m unittest tests.test_frrs_t3_resolver_bootstrap
Ran 31 tests in 6.734s
OK

python3 -m unittest tests.test_frrs_t4_w2_live_integration
Ran 17 tests in 5.291s
OK

python3 -m unittest tests.derivation.test_package_validation
Ran 13 tests in 2.468s
OK

python3 -m unittest tests.test_schema_registry
Ran 10 tests in 0.076s
OK

git diff --check 16c6f63..87e004f
(clean)

python3 tools/governance_lint.py
governance lint: conformant

python3 tools/envelope_scan.py --range main..HEAD
(clean)
```

All 85 tests passed. No existing test changed in the implementation object.
The new release, adoption, test run IDs, entities, and paths are synthetic,
use established `demo.*` identities, and remain repository-relative. Direct
inspection found no personal identifier, credential, absolute machine path,
or private artifact.

## Residuals

- CI `verify` remains the gate of record after this local review.
- This prerequisite ends at the resolved member/disposition boundary. Track 3
  remains paused and still owns categorical projection, strict presentation
  validation, product rendering, goldens, and browser criteria after this
  prerequisite is merged with green CI.

## Verdict

**READY**

The exact seven-file prerequisite delta supplies an immutable field-v2 /
package-v8 / registry-v3 / release-v3 / adoption-v8 successor chain, exposes
the existing line-7b atomic states through the generic symbol join, preserves
all historical bytes and credited Track-2 behavior, regenerates
deterministically, and fails closed at every checksum edge.
