# Capital-Gain Distributions / Line 7a — Track 2 CI Repair Recheck

Charter:
`docs/reviews/charter-2026-07-30-capital-gain-distributions-line7a-track2-ci-repair-review.md`

Role: fresh, author-independent Reviewer. Focused CI-consistency recheck, not a
second review of the credited Track-2 runtime contract.

## Echo

- **Resolved launch commit:** `27db79909ce89601d9844a10604d38831f354545`;
  verified equal to `git rev-parse HEAD` before measurement.
- **Reviewed object:** `55b5e6a5bd2237b15f2b39d575e8392dc229f384..
  68f0628c02b460e98db3211bdc05b499a299716e`, one immediate-child
  implementation commit titled `Close Track 2 CI consistency failures`.
- **Exact file set:** `packages/derivation/loader.py`,
  `tools/generate_frrs_t3_fixtures.py`, and
  `tools/presentation_harness/examples/pages/citation-walk-fixtures/
  production-shaped.v1.json`.
- **C1:** keep the published `checked-conclusion-binding` role in the one
  master `ROLE_VOCABULARY`, without editing schema history or weakening the
  subset test.
- **C2:** make the deterministic FRRS generator own explicit v1 and v2
  release routes; v6 selects v1 and v7 selects v2, while the v1 registry,
  v1 release, and v6 adoption remain byte-identical to the pre-Track-2
  baseline.
- **C3:** reproduce the presentation golden through `live_coordinate_run`;
  permit only section 3's line-16 derived-ID replacement and one declared
  line-16 citation pin.
- **C4:** independently close the four CI-failing modules and preserve the
  adjacent coordinator, runner, and schema-registry regressions without
  changing tests.
- **Credited evidence:** the prior F1/F2 `READY` recheck remains credited
  except where this three-file delta could disturb it.
- **Evidence ceiling:** synthetic repository integration only.
- **Stop conditions:** wrong object or file set; schema/checksum, runtime,
  test, registry/release/adoption, resolver, runner, projection, or
  presentation drift outside the explicit allowance; non-reproducible
  generator or golden; private material; or required governance
  interpretation. None fired.

The review charter names
`packages/schemas/artifact-package/artifact-package.v5.schema.json`, which
does not exist. The unique committed schema is
`packages/schemas/derivation/artifact-package.v5.schema.json`; that file was
the inspected published artifact. This stale read-path is a non-blocking
charter residual because the review object and the schema identity are
unambiguous. The Reviewer did not edit the charter.

## Measurements

### 1. Object custody

`git show --format=fuller --stat --name-status 68f0628` establishes that the
implementation is the immediate child of clarified charter `55b5e6a` and
changes exactly the three named files: 50 insertions and 22 deletions. A
targeted `git diff 55b5e6a..68f0628` over tests, schemas, registries,
adoptions, releases, runner, presentation projection, and phase state is
empty.

No test, schema, checksum manifest, package registry, adoption, release,
runner, projection, pointer, or review record changed in the implementation
commit.

### 2. C1 — one role vocabulary

The complete loader delta is one line:
`"checked-conclusion-binding"` added to `ROLE_VOCABULARY`.

The already-published
`packages/schemas/derivation/artifact-package.v5.schema.json` contains that
exact member-role token. The schema has no implementation-range diff.
`tests/derivation/test_language_schemas.py` also has no implementation-range
diff; its existing
`test_all_role_enums_subset_of_master_vocabulary` assertion remains intact
and passed.

**C1: satisfied.**

### 3. C2 — two explicit publication routes

Read the full generator and independently called `render_fixture_files()` in
memory. Its 14 keys exactly equal the 14 committed FRRS files and every
rendered byte equals the corresponding committed byte:

```text
rendered_count 14
committed_count 14
key_sets_equal True
byte_maps_equal True
missing []
extra []
mismatched []
```

The generator selects registry bytes by release version before looking up a
package checksum. Independent checksum tracing established:

```text
v6 route v1: registry hash, release hash, and package checksum all match
v7 route v2: registry hash, release hash, and package checksum all match
```

The v1 registry contains core versions v1–v6 only. The v2 registry contains
v1–v7. There is no fallback from v7 to v1.

The byte-identity command

```text
git diff --exit-code e478f20..68f0628 -- \
  packages/content/tax/2025/published-packages.json \
  packages/sample_data/frrs_t3/adoptions/adopt-core-v6-current.json \
  packages/sample_data/frrs_t3/publication_surface/releases/demo.release.2025.v1.json
```

returned exit 0 with no diff. Thus the canonical v1 registry, v1 release, and
v6 adoption are byte-identical to the pre-Track-2 baseline.

**C2: satisfied.**

### 4. C3 — golden provenance and exact semantic delta

Direct grep of `tools/generate_presentation_l2_golden.py` found its import and
call of `live_coordinate_run` and no `RunContext` reference. Calling
`regenerate()` without writing the fixture, then serializing exactly as
`main()` does, produced 39,223 bytes equal to the committed golden byte for
byte.

A recursive parsed comparison of the clarified-charter golden at `55b5e6a`
against the implementation golden established:

- top-level `schema`, `runId`, `citationGroups`, and `pinLabels` are unchanged;
- section count and ordering are unchanged;
- every section except index 3, `line-16`, is exactly equal;
- the line-16 finding ID changes from
  `finding:derived:e8e901e2ce825b360931a766` to
  `finding:derived:212a14483e9c91b7aa6346f6`;
- the new pin multiset is the old pin multiset plus exactly
  `{"id": "tax.us.2025.citation.form1040.line-16",
  "role": "citation", "version": "v1"}`; no pin was removed; and
- replacing the old ID and pin list with those two allowed results makes the
  entire line-16 section exactly equal.

Values, dispositions, all other citations and citation groups, redaction,
package selection, and every other section are unchanged.

**C3: satisfied.**

### 5. C4 — exact regression closure

The Reviewer ran each required module directly once:

```text
python3 -m unittest tests.derivation.test_language_schemas
Ran 29 tests in 7.381s — OK

python3 -m unittest tests.test_frrs_t3_resolver_bootstrap
Ran 31 tests in 6.717s — OK

python3 -m unittest tests.test_frrs_t4_w2_live_integration
Ran 17 tests in 4.989s — OK

python3 -m unittest tests.test_presentation_l2_integration
Ran 29 tests in 3.028s — OK

python3 -m unittest tests.test_capital_gain_distributions_line7a_t2_coordinator
Ran 9 tests in 4.810s — OK

python3 -m unittest tests.test_dsbs_t2_coordinator
Ran 7 tests in 2.686s — OK

python3 -m unittest tests.derivation.test_runner
Ran 12 tests in 3.040s — OK

python3 -m unittest tests.test_schema_registry
Ran 10 tests in 0.071s — OK
```

All 144 tests passed. The first four modules close the exact CI failures; the
four adjacent modules preserve the Track-2, legacy coordinator, generic
runner, and published-schema integrity evidence. No test file changed in the
implementation commit.

**C4: satisfied.**

### 6. Safety and diff hygiene

```text
git diff --check 55b5e6a..68f0628
(clean)

python3 tools/governance_lint.py
governance lint: conformant

python3 tools/envelope_scan.py --range main..HEAD
(clean)
```

Direct inspection found no absolute machine path, credential, personal
identity, or private artifact in the implementation file set. Generator
identities and the golden run identity use established `demo.*` synthetic
labels; paths are repository-relative. The review used no real or private
material.

## Residuals

- CI `verify` remains the gate of record after this focused local recheck.
- The charter's stale artifact-package schema path should be corrected by the
  process owner in a later pointer/charter-maintenance unit if desired; it did
  not obscure the exact published schema or the implementation object.

## Verdict

**READY**

The three-file CI-repair delta satisfies C1–C4. It restores full-suite
consistency without changing the credited Track-2 runtime contract, tests,
published schemas/checksums, legacy v1/v6 bytes, production resolution
semantics, or presentation semantics beyond the explicitly allowed line-16
identity and citation update.
