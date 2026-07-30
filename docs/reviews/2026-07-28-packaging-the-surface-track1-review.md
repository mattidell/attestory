# Review — Packaging the Surface, Track 1: the surface artifact

- Reviewer role: `docs/roles/reviewer.md`
- Charter: `docs/reviews/charter-2026-07-28-packaging-the-surface-track1.md`
- Object: `bb751ba..0fd05e7` on `milestone/packaging-the-surface`
- Commit reviewed: `0fd05e723bb66e2d888926a9e4f19df2de4f2ec2` (verified against
  `git rev-parse HEAD`)
- Note on orientation: `python3 tools/build_orientation_block.py --ref main
  --role reviewer` reports a topic mismatch, because `main` is still pinned
  to the prior (Real Return) phase-state and this track has not merged.
  That is expected mid-cycle state, not an anomaly (per project convention
  that build-done/review-pending is normal). I oriented from the charter,
  the branch's `docs/phase-state.md`, and `docs/roles/reviewer.md` directly,
  as the charter and task instructed.

## Verdict: READY

## What I checked

Full diff outside `node_modules` (16 files, 5,809 insertions / 3 deletions):
`packages/derivation/production_resolver.py` (+15/-3),
`packages/derivation/surface_resolver.py` (new, 196 lines),
`packages/schemas/derivation/surface-artifact.v1.schema.json` (new),
`packages/schemas/derivation/published.json` (+1 checksum line),
the `packages/sample_data/surface_t1/` fixture tree (adoption, manifest,
release, registry, content — content excludes vendored bytes but I did spot
checks there too), `tools/generate_surface_t1_fixtures.py`, and both test
files. I ran the code, not just read it: pytest, mypy, governance_lint,
envelope_scan, and several ad hoc probes described below.

### 1. Reuse vs. fork of the verification chain — genuine reuse

`surface_resolver.py` imports `PublicationSurface`, `Refusal`,
`_json_candidates`, `_sha256_bytes`, `_verify_release_and_registry`, and
`select_current_adoption` from `production_resolver.py` and calls them
directly; it does not reimplement release/registry byte verification or
adoption selection. I read ADR-0033's Decisions 1–3 and confirmed the split
is exactly the one the ADR describes: Decisions 1 (release-rooted adoption)
and 2 (verify-release-before-registry) are reused verbatim; only Decision 3
(closed member-graph resolution with hard `ok==True`) is replaced, and it has
to be — a manifest of opaque file entries has no closed graph to validate.
The module docstring states this honestly and specifically, naming which
decisions are reused and which diverge.

The only real cost is that three of the six imported names
(`_json_candidates`, `_sha256_bytes`, `_verify_release_and_registry`) are
underscore-prefixed — a private-by-convention cross-module import, not a
published internal API. That is a maintenance fragility (an unannounced
signature change in `production_resolver.py` breaks `surface_resolver.py`
without a contract saying so), not a second verification path. I do not
think it rises to a stop condition; it is worth naming as a residual for
whoever eventually hardens this into a stable internal boundary, but it is
the honest, disclosed cost of reuse the charter asked for, not evasion of it.

### 2. `artifact-package.v4` — untouched in substance, not just in bytes

```
git diff bb751ba..HEAD -- packages/derivation/package_validation.py \
  packages/derivation/loader.py packages/kernel/schema_registry.py \
  packages/schemas/derivation/artifact-package.v4.schema.json
```
produces no output. Every function the artifact package's own hard-validation
depends on — `package_instance_checksum`, `verify_published_package`,
`load_published_package_checksums`, the closed member-graph walk in
`production_resolver.py` (`resolve_production_package`, `_resolve_member_corpus`,
lines ~297+) — is byte-identical to `bb751ba`. The only change to
`production_resolver.py` is the 15-line `expected_kind` addition described
below, which is additive and defaults to the old behavior. Nothing about the
existing package's "whole member graph hard-validates" guarantee is weakened.

### 3. The adoption-kind separation — correctly isolated, not just by convention

`_well_formed_adoption` now takes `expected_kind` (default
`"package-adoption"`) and filters on `act.get("kind") != expected_kind` before
anything else. `select_current_adoption` builds its `candidates` dict only
from acts that pass this filter, so a surface-adoption act is excluded from
the candidate pool before supersession or revision logic ever runs — it is
not merely "checked and rejected later," it never enters the pool a
package-adoption's supersession chain draws from, and vice versa. I confirmed
the single existing caller (`resolve_production_package`, line ~315) does not
pass `expected_kind`, so every pre-existing caller keeps exactly the old
behavior (verified by the unchanged rest of the test suite passing green).

I wrote an ad hoc probe (not committed) confirming a manifest whose `entries`
were mutated to inject a path-traversal string is caught before path
resolution even runs, because the injected content invalidates the manifest's
own recorded `package_checksum` and it no longer matches the adoption pin —
a second, independent layer behind the schema's path regex. The committed
test (`DistinctAdoptionKind.test_surface_adoption_kind_never_selected_as_a_package_adoption`)
checks the direction the charter called out explicitly (surface adoption
never selected as a package adoption); the reverse direction isn't separately
tested, but it's the same filter function and the same code path, so I
consider it adequately covered by symmetry, not a gap worth blocking on.

### 4. Path confinement — held up against direct attempts to break it

The schema's `path` pattern (`^(?!/)(?!\.\.)(?!.*\.\.)[^\x00]+$`) rejects
absolute paths, any `..` substring, and null bytes at the schema layer, before
the resolver ever touches the filesystem. At the resolver layer, every entry
resolves against `content_dir.resolve(strict=True)` and is confined via
`Path.relative_to`; a symlink whose final target resolves outside the root is
refused (`SURFACE_ENTRY_NOT_CONFINED`), while one whose target resolves back
inside is followed and its target bytes digested (matches real npm layout —
I confirmed `node_modules/.bin/acorn` is a real symlink in the committed tree,
correctly listed in the manifest with the *target's* 60 bytes, and the
digest matches). I could not find a path past this with plain traversal
strings, absolute paths, or a `.` entry (harmless — resolves to the root
itself, then fails on `read_bytes()` since it's a directory). I did not find
a working bypass.

### 5. The offline claim — honestly scoped, not overclaimed

The claim in code and docs is careful, not sweeping: `build.mjs`'s own
comment says there is "nothing here that could reach the network or run an
install hook even if it tried" — a claim about the build script's own code
path, which is true (it never shells out to `npm`; it imports
`svelte/compiler` via Node's own module resolution against the vendored
`node_modules/`). The *enforcement* claim is separately and honestly scoped
to macOS: the test file's docstring says plainly that `sandbox-exec` is
macOS-only and deprecated upstream, that on other platforms "the build still
runs (offline in fact...) but the *enforcement* is unverified there," and
calls that "an honest limitation, not an assumption." I ran both offline
tests locally (Node v25.8.0, Chrome present): the build succeeds under the
sandbox profile, and — importantly — `test_a_real_network_attempt_is_actually_blocked_under_the_same_profile`
proves the profile is not a no-op by making a real `fetch()` under it and
checking it fails, rather than just asserting on the sandbox profile string.
That is exactly the kind of "don't accept a green run on a synthetic probe"
rigor the reviewer craft-notes call for, and it is already in the diff.

### 6. Refusal paths — five claimed, five checked, all genuine

`DigestMismatchRefusal` in `tests/test_surface_t1_resolver.py` covers:
corrupted shipped byte (`SURFACE_ENTRY_CHECKSUM_MISMATCH`), missing shipped
entry (`SURFACE_ENTRY_ABSENT`), a symlink escaping the content root
(`SURFACE_ENTRY_NOT_CONFINED`), a tampered manifest body — an injected extra
entry that breaks the manifest's own checksum
(`SURFACE_ABSENT_OR_MISMATCH`), and replaced registry bytes under an honest
release (`REGISTRY_CHECKSUM_MISMATCH`, inherited unchanged from
`production_resolver.py`). I traced each test's corruption to the exact
`return Refusal(...)` line it claims and confirmed no earlier check would
have caught it for a different reason first — e.g., the tampered-manifest
test really is caught at the checksum-match stage (an unrecognized digest,
so `matching` stays empty), not by a later schema-validation step that would
have masked the real failure mode.

Four additional refusal reasons in `surface_resolver.py`
(`SURFACE_AMBIGUOUS`, `SURFACE_SCHEMA_INVALID`,
`SURFACE_CONTENT_ROOT_UNREADABLE`, `SURFACE_INTEGRITY`, plus `REGISTRY_INVALID`)
are reachable but untested in this track. This mirrors an existing gap in
`production_resolver.py` itself (e.g. `PACKAGE_AMBIGUOUS` is also untested
there), so it's a pre-existing convention rather than a new regression, and
none of the untested paths are on the security-relevant surface the charter
called out (digest, path confinement, registry/release integrity, adoption
kind). Not a blocker, worth a note for whoever next touches this module.

### 7. Fixture and data-safety rules — followed

Synthetic IDs throughout (`demo.surface.entry-page`, `demo.user.filer-1`,
`demo.surface-release.2025`). `ProvenanceRegeneration.test_content_tree_is_synthetic_and_locator_free`
greps the whole fixture tree plus the resolver and generator source for
`/Users/`, `/private/`, `local-data/`, `uploads/`, `generated/user/` and
finds none; I additionally spot-checked the vendored `node_modules` tree by
eye (real, MIT-licensed npm output for `svelte@5.56.8`, nothing hand-edited
or extraneous). `test_fixtures_regenerate_from_the_committed_content_tree`
proves the manifest/registry/release/adoption fixtures are exactly
reproducible from the committed content tree via
`tools/generate_surface_t1_fixtures.py` — a real anti-drift guard, not a
one-time hand assertion.

## The vendored tree's cost, independently confirmed

`content_stats()` (imported and run directly, not taken from the commit
message): **941 entries, 5,065,001 bytes (~5.07 MB)**. This matches the
commit message exactly. `find -type f` under-counts at 935 because it
doesn't follow the `.bin/` symlinks by default; `du -sh` reports 7.4 MB
because of filesystem block overhead. The number the owner needs for Track 2
is the byte-sum one, and it's real and accurately reported.

## Verification run

- `pytest` (full suite): `687 passed, 2481 subtests passed in 26.20s`.
- `pytest tests/test_surface_t1_resolver.py tests/test_surface_t1_build_and_open.py -v`:
  **14 passed**, none skipped — Node (v25.8.0), `sandbox-exec`, and a local
  Chrome were all present, so every test in the build/open file genuinely
  ran, including the real network-block probe and the real vehicle launch
  against a synthetic workspace.
- `python -m mypy`: `Success: no issues found in 131 source files`.
- `python tools/governance_lint.py`: `governance lint: conformant`
  (confirms the new schema's checksum in `published.json` matches its file
  bytes — I independently recomputed the SHA-256 and it matches
  `d5a022e08db53025e58261e4f975f3278980276f392da3a897eb268b47eb0cfd`).
- `python tools/envelope_scan.py --range bb751ba..HEAD`: clean, exit 0.

I did not omit anything from the stated CI `verify` sequence.

## What I could not check

- Whether `Path.resolve()`'s symlink-following semantics differ in some way
  I haven't thought of on a non-macOS/non-POSIX filesystem; I only tested on
  this machine (macOS/APFS).
- CI's actual behavior, since CI has no Node — I can only confirm what the
  test file's docstring already discloses (the resolver's pure-Python tests
  run in CI; the build/open tests are skipped there, not failed). I did not
  have a non-macOS machine to independently confirm the "still runs offline,
  just unverified" claim for the enforcement gap; I evaluated it as an
  honest, clearly-labeled limitation rather than as a proven fact for other
  platforms.

## Independent read of the builder's named weaknesses

The builder named three weaknesses (macOS-only offline enforcement / no CI
coverage; no TypeScript in the sample page; the build's output never being
digest-verified). I agree with all three as genuine, correctly self-scored,
residuals — none of them are charter violations, and the charter explicitly
placed the build-output digest question, TypeScript, and the live-loop
integration out of this track's scope ("Do not extend the vehicle's
preflight," "No ADR," ship "one trivial page," Node/TS toolchain decisions
already settled at the milestone level). Looking past that list, the
findings I'd add are the two named above: the underscore-prefixed
cross-module imports as a coupling/maintenance residual (not a second
verification path — a real distinction, and this stays on the reuse side of
it), and the untested minority refusal paths (a pre-existing pattern, not a
new gap). Neither is a stop condition under the charter's own terms
("cannot be reused," "requires changing artifact-package.v4," "vendored tree
too large," "cannot be made observably offline") — none of those four
conditions occurred.

## Recommendation

READY. The container is a genuine second, separate authority path that
reuses the release/registry/adoption verification ADR-0033 already
established rather than forking it; `artifact-package.v4` and its validation
machinery are provably untouched; the new adoption-kind parameter is
additive and correctly isolates surface and package adoption candidate
pools; path confinement resists direct attempts to break it; the offline
claim is scoped and enforced honestly, with a real (not simulated) proof
that the sandbox profile blocks network; all five claimed refusal paths
fail for the reason they claim to, verified by tracing each to its exact
`Refusal(...)` line; and the vendored tree's cost is real, reproducible, and
accurately reported. Full CI `verify` sequence passes green, including the
Node/Chrome-dependent tests that CI itself cannot run.
