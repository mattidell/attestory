# First Real Return Slice — Track 1 (Boundary and Contribution Schemas) — Pre-Merge Review

Reviewer: owner-launched pre-merge reviewer (author-independent — did not write the development). Date: 2026-07-17. Branch under review: `track/frrs-t1-boundary-contribution-schemas` @ `109defb`, against `main` base `a213cf3`. Advisory — the owner decides disposition. This review does not redesign ratified contracts or authorize runtime behavior.

Track 1 development commits reviewed: `9f3a020` (add boundary and contribution schemas), `109defb` (repair boundary and contribution schema contracts). The branch also carries the D3 decision merge (`c973c72`, PR #7) in its history because that unit is not yet on `main`; it is out of this review's scope and is reviewed only for the scope-fence question below.

## Verdict

**Merge-ready for its declared scope (D1/D2 schema citizens). No blocking finding.** The D1 and D2 ratified contracts are faithfully rendered as versioned schema citizens with positive examples, named negatives, schema-validation tests, registry rows, and a deterministic fixture generator; the whole suite, mypy, governance lint, and the data-safety scan are green; schema-registry byte integrity holds. One item needs an **owner scope reconciliation before or at merge** (F1): the review charter lists "D3 release-registry and package-adoption schemas," which are absent — correctly so against the ratified milestone plan, which scopes Track 1 to D1/D2 and places the resolver in Track 3. Nothing else rises above non-blocking.

## Evidence (re-run by the reviewer on this branch)

- `.venv/bin/python3 -m unittest` → **358 tests OK**. Track-1 test `tests/test_frrs_t1_boundary_contribution_schemas` → **6 OK**.
- `.venv/bin/mypy packages tools tests` → **Success: no issues found in 78 source files**.
- `tools/governance_lint.py` → **conformant**.
- Data-safety: the Track-1 test's own private-marker scan passes; an independent `git diff` scan of `packages/sample_data` + `packages/schemas` finds no personal path or value (the only `real` hit is the word "real values" in a schema *description*). All identifiers are `demo.*` synthetic.
- Schema-registry integrity: `published.json` sha256 rows match the on-disk schema bytes (spot-checked `finding.v2`, `act-member-transition.v2`, `classification.v1`, `run-request.v1` — all match).
- Fixture provenance: `test_fixture_corpus_is_regenerated_from_its_public_pins` regenerates the corpus from the generator and asserts byte-equality, and checks every manifest `sha256` against actual bytes.

## What is sound (keep — do not redo)

- **D2 schema fidelity — faithful (ADR-0032).** `finding.v2` **requires** `evidence_ids` (Article 1 documentary channel retained), carries `contribution_id` as **optional** and **outside `pins`** (provenance-only, creates no derivation edge — ADR-0032 Decision 2). `run-request.v1` is **closed** (`additionalProperties:false`, only `schema`; no value-bearing member — ADR-0032 Decision 3); its negative adds a value and rejects. `act-assertion.v2` and `act-member-transition.v2` are the successor carrier acts that admit `finding.v2` — the exact `act-*.v2` gap the D2 committee (Governance M1) named. `act-member-transition.v2` also encodes ADR-0017 D3 (one same-family/scope successor) and D4 (a same-member value correction uses the assertion act, not this one). `contribution.v1`/`act-contribution.v1`/`contribution-record.v1` are present and well-formed; the record is an Article-14 process account with a correct `started` vs terminal-phase conditional.
- **D1 schema fidelity — faithful (ADR-0031).** `classification.v1` is a **total, fail-closed** binary: the `oneOf` forces `MAY_CROSS`→one of the three declared `kind`s and `NEVER_CROSSES`→a `reason` with `kind` explicitly forbidden (Decisions 2/7). `reserved-illustration-domain.v1` is the fixed non-resolvable enumeration (Decision 5). `fixture-provenance-manifest.v1` matches Decision 6 (generator id/version/digest, grammar/profile digests, seed, constraints, input_kinds, per-artifact `path`+`sha256`, `attestation_no_live_data: const true`), and its `path` pattern forbids absolute paths and `..` traversal — a defensive touch aligned with the residency boundary.
- **Provenance/byte-regeneration mechanism — exercised, not merely declared.** The generator (`tools/generate_frrs_t1_fixtures.py`) renders the corpus deterministically and the test pins byte-equality plus manifest-sha256 correspondence, so ADR-0031 Decision 6's synthetic-derivation-by-reconstruction is demonstrated in-repo.
- **Test coverage.** 10 positive examples (one per new schema, count-asserted), 10 named negatives (≥ schema count, each asserted to reject), a dedicated fail-closed classification case, byte-regeneration, and a private-marker scan. Negatives target real constraints (v1 finding in a v2 carrier; NEVER_CROSSES-with-kind; missing evidence; bad basis; missing attestation; illustration extra-prop; value in a closed run-request; bad scope; invalid `started` record; bad act schema).

## Findings

### F1 — D3 release-registry / package-adoption schemas absent; charter vs ratified-plan scope mismatch
**Classification: scope observation (non-blocking against the ratified plan; needs owner reconciliation).** The review charter's checklist includes "D3 release-registry and package-adoption schemas," and it references `docs/phases/real-return/milestones/first-real-return-slice-tracks.md`. That file does not exist; the Track spec lives in `first-real-return-slice.md`, whose **Track 1** is *"Schema/contract citizens from the ratified D1/D2 ADRs"* and whose **Track 3** owns *"Production resolver and live workspace bootstrap."* ADR-0033's `release-registry.v1` and `act-package-adoption.v1` are therefore Track-3 citizens; their absence here is **consistent with the ratified plan**, not a gap. Because ADR-0033 ratified after the plan's Track text was written, surface this to the owner: if Track 1 is intended to also carry the D3 resolver schemas, that is a plan amendment and those two schemas + examples/negatives/registry rows are then a Track-1 gap; otherwise they land in Track 3. As the branch stands against the current plan, no defect. (Also: correct the charter's doc reference to `first-real-return-slice.md`.)

### F2 — Boundary schema directory not wired into a runtime registry
**Classification: production condition (for the behavior tracks).** The Track-1 test constructs a `SchemaRegistry` that explicitly adds `packages/schemas/boundary`; the production kernel/derivation registries do not yet load `boundary/`. This is appropriate for a schema-only track (wiring the boundary citizens into runtime classification/enforcement is behavior owned by Tracks 2/3 and by ADR-0031's installed-gate production conditions), but it must be discharged there so the boundary schemas are enforced in a real run, not only validated in-test.

### F3 — `run-request.v1` is schema-only; the marshal-only RunContext remains a production condition
**Classification: production condition (correctly deferred).** The closed `run-request.v1` schema is the request-side half of ADR-0032 Decision 3. The MUST condition that ADR-0032 names — a marshal-only `RunContext` constructor + entrypoint-unreachability kill-test making runs-consume-facts structural at the *runtime input* — is runtime behavior and is correctly **absent** from this schema track. Recorded here so it is not lost: it is owed to Track 2/3, not to Track 1.

### F4 — `mypy .` at repo root collides with `archive/tests`
**Classification: non-blocking (pre-existing hygiene, not introduced by Track 1).** Invoking `mypy .` fails with a duplicate-module error because `archive/tests/` shadows `tests/`. Running mypy on the project targets (`packages tools tests`) is clean. Not a Track-1 defect; noted so a future reviewer does not misread it as one. Optionally exclude `archive/` in `mypy.ini`.

## Scope fence

Clean. The only `.py` changes are the new test and the new fixture generator; no `packages/kernel` or `packages/derivation` runtime module is modified. No contribution machinery (Track 2), no resolver or live-workspace bootstrap (Track 3), no closure mapping or live-run harness (Track 4) behavior is present. The track delivers schemas, examples/negatives, registry rows, tests, and a fixture tool — exactly its declared surface.

## Recommendation

Merge once F1 is reconciled with the owner (confirm Track 1 = D1/D2 schemas, or amend the plan to pull the D3 resolver schemas forward). F2/F3 are production conditions to carry into Tracks 2/3; F4 is optional hygiene. No implementation change is required for the D1/D2 scope this branch delivers.
