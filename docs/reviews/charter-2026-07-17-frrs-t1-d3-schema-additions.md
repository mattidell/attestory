# Charter: Track 1 follow-up — D3 resolver schema citizens

Date: 2026-07-17. Foreman-authored implementation charter. Governed by the
milestone plan's **2026-07-17 Track 1 amendment** (PR #9) and dispositions
finding **F1** of `2026-07-17-frrs-t1-premerge-review.md`. Lands on
`track/frrs-t1-boundary-contribution-schemas` (updates open **PR #8**).

- **Type:** implementation follow-up (not a prototype topic — single implementer,
  no rival; the existing Track 1 pre-merge review gate re-runs after).
- **Scope:** add the two **D3 (ADR-0033 Decision 1)** schema citizens as
  schema/contract citizens, in the exact pattern the D1/D2 citizens already use in
  this branch. **Schemas + examples + named negatives + registry rows +
  validation tests only. No resolver runtime behavior** (that is Track 3).

## Assignment

Add, faithful to **ADR-0033 Decision 1**:

1. **`release-registry.v1`** — a versioned publication-root citizen. Place under
   `packages/schemas/derivation/` (sibling to `artifact-package.*`). Its immutable
   identity **includes the SHA-256 of the exact package registry document it
   attests**, and — where citizen registries are split — the SHA-256 of each
   separately attested registry document. Model the attested-registry digest(s) as
   required, `^[a-f0-9]{64}$`-patterned fields; `additionalProperties: false`;
   `schema` const. Do not invent fields beyond what Decision 1 states.

2. **`act-package-adoption.v1`** — a declared **Article-4 user act**. Place under
   `packages/schemas/kernel/` (sibling to `act-contribution.v1`). It pins an exact
   package `{id, version, checksum}` **and** an exact release
   `{id, version, checksum}`, with: the **user actor**, structured **scope**,
   **revision**, an **optional** same-scope **supersession** reference, and
   **non-authoritative audit metadata**. Checksums `^[a-f0-9]{64}$`; scope a
   non-empty object; revision a non-negative integer; supersession optional;
   `additionalProperties: false`. Encode "user actor" per the committed actor
   convention (mirror how existing acts express actor identity — do not permit an
   automation/non-user actor at the schema level if the existing convention
   supports constraining it; otherwise leave actor kind to Track-3 admission and
   note it).

## Required deliverables (mirror the D1/D2 citizens)

- Two schema files at the placements above.
- A **registry row** for each in the correct `published.json`, sha256 = the exact
  bytes of the schema file (deterministic; the existing rows are the reference).
- One **positive example** each under `packages/sample_data/frrs_t1/examples/`,
  fully synthetic (`demo.*` identifiers; any path-shaped token drawn from the
  reserved illustration domain; 64-hex checksums are synthetic literals).
- At least one **named negative** each under `.../negatives/` targeting a real
  constraint — e.g. `act-package-adoption.v1` missing the release pin; a
  non-`^[a-f0-9]{64}$` checksum; `release-registry.v1` missing the attested
  registry digest.
- Extend `tools/generate_frrs_t1_fixtures.py` to render the new fixtures
  deterministically, and update the **fixture-provenance-manifest** so the
  byte-regeneration test (`test_fixture_corpus_is_regenerated_from_its_public_pins`)
  stays green (corpus == generator output; manifest lists every artifact + sha256).
- Update the Track-1 test `NEW_SCHEMAS` set (10 → 12) so the positive-count and
  negative-count assertions hold; add any schema-specific assertion in the pattern
  of `test_never_crosses_requires_a_reason...`.

## Scope fence (do not cross)

- No changes to `packages/derivation` / `packages/kernel` **runtime** modules
  (loader, resolver, validation, runner). No wiring of these schemas into
  production resolution or a runtime registry — Track 3 owns resolver behavior;
  Track 2 owns contribution machinery. If the boundary/derivation registry needs
  wiring for the test, do it **in the test only** (as the existing Track-1 test
  already does for `boundary/`).
- Do not modify or re-review the ratified ADR-0033 contract; implement to it.

## Verification (all must pass, re-run and reported)

- `.venv/bin/python3 -m unittest` (full suite) green; the Track-1 test green with
  updated counts.
- `.venv/bin/mypy packages tools tests` clean.
- `tools/governance_lint.py` conformant.
- Data-safety: no personal path or value; every value/identifier synthetic; the
  Track-1 private-marker scan green.

## Stop conditions

Stop when the two citizens, their examples/negatives/registry rows/tests, and the
generator/manifest updates are in and all verification is green. No runtime
behavior, no resolver, no ADR edits. The Track 1 pre-merge review re-runs over the
amended branch before merge.
