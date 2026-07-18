# First Real Return Slice — Track 1 — D3 Schema-Additions Pre-Merge Re-Review

Reviewer: owner-launched, author-independent pre-merge reviewer (did not implement
the D3 additions). Date: 2026-07-17. Charter:
`charter-2026-07-17-frrs-t1-d3-schemas-rereview.md`. Branch:
`track/frrs-t1-boundary-contribution-schemas`, delta reviewed **`109defb` →
`5e55b0e`** (the only implementation commit in the delta; `10aeb66`/`97929aa` are
records). The D1/D2 citizens carry their existing merge-ready verdict from
`2026-07-17-frrs-t1-premerge-review.md` and were not reopened except where the D3
delta touches shared files (generator, manifest, Track-1 test, `published.json`).
Advisory — the owner decides disposition.

## Verdict

**Merge-ready. No blocking finding and no scope defect.** The two D3 (ADR-0033
Decision 1) schema citizens are faithful to the ratified contract; registry-row
and manifest byte-integrity hold; the negatives reject for exactly their named
constraint (verified by single-field repair, not only by `assertRaises`); the
delta is synthetic-only; the scope fence is respected; the full verification
battery is green. Prior finding **F1 is discharged**: the 2026-07-17 Track 1
amendment (PR #9, merged to `main` at `157cd80`) pulls the D3 schema citizens into
Track 1, which is exactly and only what this delta adds. Findings below are
production conditions for the behavior tracks plus non-blocking notes.

## Evidence (re-run by this reviewer at `97929aa`)

- `.venv/bin/python3 -m unittest` → **358 tests OK** (Track-1 test green with the
  updated counts: 12 positives asserted equal to `NEW_SCHEMAS`, ≥12 negatives).
- `.venv/bin/mypy packages tools tests` → **no issues in 78 source files**.
- `tools/governance_lint.py` → **conformant**.
- **Registry integrity:** `derivation/published.json` row for
  `release-registry.v1.schema.json` and `kernel/published.json` row for
  `act-package-adoption.v1.schema.json` both equal the sha256 of the on-disk
  schema bytes (recomputed independently).
- **Fixture provenance:** all 23 manifest artifact sha256s match actual bytes
  (23 = 12 examples + 12 negatives − the manifest itself); the updated
  `generator.digest` equals the sha256 of `tools/generate_frrs_t1_fixtures.py`;
  `test_fixture_corpus_is_regenerated_from_its_public_pins` asserts byte-equality
  of corpus vs generator output and passes.
- **Right-reason rejection (mutation-checked):**
  `release-registry.v1.missing-registry-sha` rejects on
  `'package_registry_sha256' is a required property` and becomes **valid** when
  only that field is added; `act-package-adoption.v1.missing-release` rejects on
  `'release' is a required property` and becomes valid when only the release pin
  is added. The adoption negative validates under the explicit `ACT_SCHEMA`
  mapping, so it cannot pass vacuously as an undeclared schema.
- **Constraint binding (spot-probed live):** uppercase/short checksums reject
  (`^[a-f0-9]{64}$` binds); empty `scope` rejects (`minProperties: 1`); negative
  `revision` rejects; an extra property (including an in-payload `actor`) rejects
  on both schemas; a split `citizen_registry_sha256` map validates when non-empty
  with 64-hex values and rejects when empty or malformed.
- **Data safety:** a marker scan of the full `109defb..HEAD` diff
  (`/Users/`, `/private/`, `local-data/`, `uploads/`, personal names/values)
  finds nothing; all identifiers are `demo.*`; every 64-hex checksum is a
  patterned synthetic literal; the Track-1 private-marker test passes.

## Fidelity to ADR-0033 Decision 1

- **`release-registry.v1` — faithful.** Versioned publication-root citizen under
  `packages/schemas/derivation/` (sibling to `artifact-package.*`):
  `schema` const, `id`, `version`, **required** `package_registry_sha256`
  (`^[a-f0-9]{64}$`) — the SHA-256 of the exact package registry document it
  attests — and an **optional** `citizen_registry_sha256` non-empty map of
  per-registry digests for the split-registries case. `additionalProperties:
  false`. No invented fields: `schema`/`id`/`version` are the standard citizen
  identity trio every published citizen carries; the two digest surfaces are
  precisely the two Decision 1 names.
- **`act-package-adoption.v1` — faithful.** Article-4 act payload under
  `packages/schemas/kernel/` (sibling to `act-contribution.v1`): required exact
  package `{id, version, checksum}` **and** release `{id, version, checksum}`
  pins (closed sub-objects, 64-hex checksums), required non-empty structured
  `scope`, required non-negative integer `revision`, optional `supersedes`
  reference, optional open-object `audit`. `additionalProperties: false`.

## The actor question (charter item 2) — envelope placement is faithful

The payload carries no actor; the **`act.v1` envelope** requires `actor` on every
act, and no existing act payload (`act-contribution.v1`, `act-assertion.v2`,
`act-member-transition.v2`) duplicates it. Mirroring that committed convention is
correct. The envelope's `actor` is a free string with no actor-kind vocabulary
anywhere in the schema corpus, so there is no existing convention under which the
schema could constrain "user" — and ADR-0033 itself implies well-formed non-user
acts can exist (*"a non-user act … never **selects authority**"* is a
resolver-time refusal, not a well-formedness rule). A schema-level user-only
constraint would therefore overreach the ratified contract. The implementer took
the charter's designated fallback and **noted it in the schema description**:
sole-current-user-in-scope selection is Track-3 admission. Probed: an in-payload
`actor` property is rejected by `additionalProperties: false`, so the payload
cannot grow a second, conflicting actor channel.

## Scope fence — clean

The implementation delta touches only: the two schema files, two registry rows,
two examples, two negatives, the generator, the manifest, and the Track-1 test.
No `packages/kernel`/`packages/derivation` runtime module (loader, resolver,
validation, runner) is modified; no ADR is edited; no Track-2 contribution
machinery appears. The `published.json` rows make the citizens *validatable*
schema citizens — the charter's explicitly required deliverable — and confer no
resolver behavior: no runtime module consults either schema. This is publication,
not the "wiring into a production registry or loader" the fence forbids.

## Findings

### F1 — Adoption authority semantics are schema-unenforceable; owed to Track 3
**Classification: production condition (Track 3).** Decision 1's selection rules —
sole current user in scope, *same-scope* supersession, unique-maximum-revision
selection, refusal on zero candidates or a tied maximum, non-user/stale acts never
selecting authority — are cross-instance semantics a single-document JSON Schema
cannot express. The schema correctly pins the per-document shape (`supersedes` is
a bare reference; `revision` a non-negative integer) and defers the rest. Track 3
must implement and kill-test these at admission/resolution, per ADR-0033's own
Consequences list. Recorded so the deferral is not lost at merge.

### F2 — `audit` is the one open interior surface
**Classification: non-blocking.** `audit: {"type": "object"}` is unconstrained and
optional, inside otherwise fully closed schemas. This is defensible — ADR-0033
names it **non-authoritative** audit metadata, and closing it would invent a
vocabulary Decision 1 does not state — but it is the only place arbitrary content
can ride an adoption act. Condition to carry: nothing in Tracks 2–4 may ever read
`audit` to make a decision; if audit content ever becomes load-bearing, that is a
new schema version, not a reinterpretation.

### F3 — Split-registry branch and checksum-pattern constraints not pinned in the corpus
**Classification: non-blocking.** The committed example omits
`citizen_registry_sha256` and no committed negative targets a malformed checksum
or an empty split map, so those constraints are enforced by the schema but not
regression-pinned by a fixture. This reviewer verified them live (they bind); the
charter required only one named negative each, which is satisfied. Optional
hardening for a later track: a split-registry positive example and a bad-checksum
negative.

### F4 — Carried forward unchanged from the prior review
**Classification: production condition (unchanged).** Prior F2 (boundary schema
directory wired into a registry only in-test) and F3 (marshal-only `RunContext`)
are unaffected by this delta and remain owed to Tracks 2/3. Prior F4 (`mypy .`
vs `archive/tests`) remains pre-existing hygiene. Note for the record: the local
`main` ref lags the remote; this review verified the Track-1 amendment text on
`origin/main` (`157cd80`).

## Recommendation

Merge PR #8. The amended Track 1 scope is fully delivered: D1 + D2 + D3 schema
citizens, each with examples, named negatives, registry rows, deterministic
regeneration, and green verification. Carry F1 (and the prior review's F2/F3)
into the Track-3 charter as named production conditions; F2/F3 here are
non-blocking observations requiring no change to this branch.
