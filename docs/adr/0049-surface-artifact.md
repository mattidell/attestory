# ADR 0049 — Surface Artifact: Packaging UI Program Bytes for the Live Workspace

- Status: **proposed**. Records what Track 1 of Packaging the Surface built
  and Track 1's review (`ee50b8f`, READY) accepted. Ratification is the
  owner's.
- Tier: 3
- Date: 2026-07-28

## Context — the source repository has no authority to touch the live workspace

ADR-0048 settled that a browser form is an acceptable place to type a tax
fact. It did not say how the browser gets there. UI code is written in this
repository; the live workspace is where real financial data lives, and the
only sanctioned way anything crosses into it is the artifact package the
owner has adopted, verified against a published digest chain
(ADR-0033). Today that package carries declarative rule content: a member is
`{role, schema, id, version}`, an identity pointing at a typed citizen whose
whole member graph hard-validates before anything runs. UI source and a
vendored dependency tree cannot be members of that in any form — there is no
path, no file, and no way to "validate" a `.svelte` file or a third-party
npm package for meaning that isn't a validator that always passes.

The owner settled the shape of the answer before this track existed
(`docs/phases/legible-entry/milestones/packaging-the-surface.md`): a second,
separate artifact, its own adoption act, carrying program files verified only
by fingerprint. Track 1 built it and shipped one page through it. This ADR
records the rule, and settles the three questions the milestone plan left
open.

## Decision — a second container, reusing what already exists

`packages/derivation/surface_resolver.py` defines `resolve_surface_artifact`,
which mirrors `production_resolver.resolve_production_package` through
adoption and release/registry verification and diverges only at member
resolution.

**Reused, unchanged:** ADR-0033 Decisions 1 and 2 — a release-rooted,
current-user adoption, and release bytes verified before registry entries
authenticate supply. `surface_resolver.py` imports and calls
`select_current_adoption` and `_verify_release_and_registry` directly rather
than reimplementing them.

**Diverges at Decision 3.** Where the artifact package resolves a closed,
strictly-typed member graph, a surface artifact is one manifest citizen —
verified as a published instance the same way an `artifact-package.v4`
instance is (`package_instance_checksum` / `verify_published_package` against
the registry) — whose `entries` list is a flat array of `{path, sha256,
bytes}`. Each entry is read from `content_dir` and checked by SHA-256 before
use, confined to the content root by `Path.relative_to` (a symlink resolving
outside the root is refused; one resolving back inside is followed, matching
real `node_modules/.bin` layout). Nothing in an entry is parsed, typed, or
opened for meaning. `surface-artifact.v1.schema.json` shapes only the
manifest itself.

**The adoption is a distinct act kind, `surface-adoption`,** not a new
schema. `_well_formed_adoption` now takes an `expected_kind` parameter
(default `package-adoption`, so every existing caller is unaffected) and
filters the candidate pool on it before supersession logic runs — a
surface-adoption act can never tie or supersede a package-adoption act, or
vice versa, because it never enters the other's candidate pool. The
adoption's payload reuses `act-package-adoption.v1` unchanged: that schema is
already an exact `{id, version, checksum}` pin on a package and a release,
generic enough for either kind of adopted thing. A second payload schema
would have recorded nothing a `kind` string doesn't already say.

## Decision — why the artifact package was left alone

The alternative was cheaper: add an opaque-member role to
`artifact-package.v4` and let UI files ride inside the existing package.
Rejected, and stated plainly rather than left implicit — that change turns
"everything in this package validates" into "everything validates except the
parts that don't," permanently, to save building one resolver once. The
package's whole reason to exist is that its member graph hard-validates
before anything runs; a member that is a raw file with no schema is not a
smaller version of that guarantee, it is the guarantee's negation, footnoted
into every future reader's understanding of what "member" means.

Track 1's diff confirms the package was not touched in substance, not merely
in bytes: `package_validation.py`, `loader.py`,
`packages/kernel/schema_registry.py`, and
`artifact-package.v4.schema.json` are byte-identical to the commit before
this track began (Track 1's review verified this by diff). The only change
to `production_resolver.py` is the additive `expected_kind` parameter.

**The cost accepted:** a second thing the owner adopts, a second manifest
schema, and a second resolver — reusing two of the three decisions ADR-0033
already made, but still a second container someone has to know exists.
Someone will propose merging the two later, on the reasoning that the
adoption-kind filter already keeps them from colliding, so why not one
package with two kinds of member. What they have to argue against is the
paragraph above: adding an opaque member to a package that promises a hard
member graph does not save the second resolver, it deletes the promise the
first resolver exists to keep.

## Decision — the build's output rests on provenance, not on content identity, and that is the weakest joint here

Every input the surface artifact carries — the source, the lockfile, all 941
vendored files — is digest-verified before the build runs. The output is
not: `dist/index.html` and the JavaScript served alongside it did not exist
until `node build.mjs` ran on the owner's machine, so no published digest
covers it. The manifest records the exact command
(`"build_command": "node build.mjs"`), and the build script itself is one of
the verified entries — nothing here is convention, everything that decides
what runs is inside the verified set except the interpreter that runs it.
That is the whole trust chain: **verified inputs, plus a command whose own
text is itself verified, executed once by whatever Node is on the machine.**

**What this actually establishes.** It rules out substitution: nobody can
swap the source, the compiler, or the vendored tree without the digest chain
catching it, and nobody can run a different command, because the command
that runs is read from the same verified manifest, not typed by hand at the
workspace. That is a real, load-bearing guarantee — it is the same shape of
guarantee ADR-0033 already makes for every other artifact, extended to cover
"what produced this," not just "what is present."

**What it does not establish, and cannot, as built.** It does not establish
that the bytes served today are the bytes anyone looked at. Track 1's review
ran the build once, on one machine, and read the result; the owner's own run,
the one that actually serves the page, is trusted by analogy to that run, not
verified against it. "Verified inputs plus one fixed command" is a claim
about *provenance* — this came from that, unmodified — not a claim about
*reproducibility* — that same-inputs-in always yields same-bytes-out. The two
are not the same claim: a non-deterministic build could satisfy the entire
chain above on every single run while producing a different
`dist/index.html` each time, and nothing in this design would notice, because
nothing digests the output.

**What sufficiency would require, stated precisely.** For "verified inputs
plus one fixed command" to also mean "the served bytes are the reviewed
bytes," the build has to be a pure function of {source, vendored tree, Node's
own version} — no wall-clock timestamp embedded in output, no random
identifier, no branch on locale, hostname, or CPU architecture, and no
dependence on anything outside the vendored tree (an `NODE_PATH`, an
`.npmrc`, a global npm config) that could vary between the review's machine
and the owner's.

**Part of that was checked, not assumed.** The content tree was copied to two
separate directories, `node build.mjs` was run in each with a gap between the
runs, and the two `dist/` trees were compared. Both runs exited 0 and the
output is **byte-identical** (`diff -r`, no differences), on Node v25.8.0.
This was performed twice independently — by the foreman and again for this
ADR — with the same result.

That observation is narrower than "the build is deterministic," and the
distinction is the point of recording it rather than the headline:

- **What it rules out.** The common causes of build nondeterminism that would
  surface immediately — an embedded build timestamp, a randomized ordering, a
  per-run identifier. Any of those would have differed between two runs
  separated in time on the same machine, and none did.
- **What it does not touch.** Same machine, same Node version, same
  filesystem, minutes apart. Determinism across machines, across Node
  versions, across operating systems, or over time is untested. Anything that
  varies with platform or toolchain version could not have shown up in this
  comparison, by construction.

**The conclusion is unchanged; what changed is what holds it up.** "Verified
inputs plus one fixed command" is still not sufficient to claim the served
bytes are bytes anyone reviewed — nothing published a digest for the output,
and no amount of same-machine determinism supplies one. What this ADR no
longer does is rest that reasoning on a *reading* of `build.mjs` and
`svelte/compiler` and the word "plausible," which is exactly the kind of
unchecked plausibility this project's own reviewer craft-notes warn against
accepting in place of a checked fact. It now says: determinism holds on one
machine under one toolchain, checked, and is unverified beyond that.

The chain is sufficient for the narrower claim this milestone actually needed
— a page can cross the boundary at all, built from exactly what the owner
adopted rather than from something else — and is materially stronger than
"trust the build" with no verified inputs at all. It is not the same strength
of claim this project makes about every other artifact, where the published
digest and the served bytes are literally the same bytes.

**Future work, sharpened to what is actually left.** The single-machine,
single-toolchain case is checked. The cross-machine and cross-Node-version
cases are not: run the fixed build command against the same verified inputs
on two machines, or under two Node versions, and assert the `dist/` trees are
byte-identical. Re-run on any toolchain upgrade — a new vendored `svelte`
version or a new Node major — since a check on one compiler cannot bind a
compiler nobody has run yet.

## Decision — Node is a new kind of precondition, and it is the same gap as the one above seen from the other side

The build needs Node, and Node ships in neither container. That makes Node a
condition of the live workspace itself, not something the crossing carries —
a category this project has not declared before ADR-0047's Class D
("workstation precondition") named the closest existing shape: a property of
the owner's machine that the mechanism cannot see and does not verify.

**It does not belong in Class D as written, and forcing it in would misdescribe
both.** ADR-0047's four classes are a total classification of *viewing-session
channels* — where typed or displayed data could leak once it is already
inside the residency. Node's absence or version is not a leakage channel: it
is a functional precondition for producing the page at all, evaluated once at
build time, not once per session. The two ideas rhyme — both are things true
of the machine that no artifact digest can see — but Class D's whole
apparatus (refusal-vs-warning disposition, detectability, the attestation's
enumerated conditions) is built for a different question than "is the
interpreter present." I am naming this as its own kind of precondition — a
**build-toolchain precondition** — rather than stretching Class D to cover
it, because stretching it would blur a class this project has taken care to
define exactly around session-time leakage.

**If Node is simply missing:** the fixed command exits non-zero. Nothing
partial or corrupted gets served, because the exit code is checked before
anything downstream trusts `dist/` — Track 1's own test asserts this
(`self.assertEqual(result.returncode, 0, result.stderr)`), and any real
consumer of a surface manifest's `build_command` needs to do the same. This
failure mode is benign: fail-closed by absence.

**If a different Node version is present:** this is not benign, and it is not
a separate question from the one above — it is precisely the case the
two-run check did *not* cover. Nothing pins a Node version anywhere in the
surface artifact or its schema, and nothing digests the output, so a
workspace on a different Node major version could produce a different
`dist/index.html` from the identical verified inputs and nothing in this
design would detect it. The two-run comparison above holds Node fixed at
v25.8.0 by construction, so it says nothing here. The Node-version question
and the residual build-output question are the same gap, not two: both close
together if the remaining future work (a byte-identity check across machines
and Node versions) is ever built, because a cross-machine check is exactly a
check across whatever Node versions those machines run.

**Where this belongs.** Recorded here as a named workspace precondition, not
filed under ADR-0047. A future milestone that formalizes preconditions this
project's mechanism cannot see should treat "build-toolchain presence and
version" as its own category, distinct from Class D's session-leakage
concerns, and this ADR's Node-version residual as its first concrete
instance.

## The offline build, scoped honestly

`build.mjs`'s own comment states the claim precisely: there is nothing in the
script that could reach the network or run an install hook even if it tried
— it imports `svelte/compiler` via Node's own module resolution against the
vendored `node_modules/`, and never shells out to a package manager. That
claim about the script's own code path is true by inspection.

The *enforcement* of "no network" is a separate, narrower claim, scoped
honestly to one platform. Track 1's test proves it under `sandbox-exec`
(macOS-only, deprecated upstream) by making a real network call under the
same deny-network profile and confirming it fails — not by asserting on the
profile's text. On any other platform the build still runs offline in fact
(the vendored tree ships as literal files; the script never invokes a package
manager), but that enforcement is unverified there, and CI carries none of
this: CI has no Node, so the build-and-open tests are skipped, not failed,
and only the resolver's pure-Python guarantees run there.

These tests are not unrunnable — on a machine with Node, `sandbox-exec`, and
a local Chrome present they run and pass, and did so for Track 1's review and
again for this ADR. The gap is precisely and only that CI does not carry
them: the evidence for the offline claim is real and reproducible, but it is
not *continuously* checked, so a regression in it would be caught by whoever
next runs the suite locally rather than by the gate of record.

## Known weak points, carried forward rather than smoothed over

- **Cross-module coupling.** `surface_resolver.py` imports three
  underscore-prefixed names from `production_resolver.py`
  (`_json_candidates`, `_sha256_bytes`, `_verify_release_and_registry`) — a
  private-by-convention import, not a published internal contract. This is
  genuine reuse, not a second verification path, but it is fragile: an
  unannounced signature change in `production_resolver.py` breaks
  `surface_resolver.py` silently, with no contract naming the dependency. If
  it drifts, the failure mode is an import error or a silent behavior change
  at the call site, not a security gap — but it will cost whoever changes
  `production_resolver.py` next a search they would not otherwise have to
  do. Worth promoting to a stable, named internal boundary the next time
  either module is touched.
- **TypeScript is untested.** The sample page is plain Svelte with no
  TypeScript, so the toolchain cost of TypeScript compilation — a real
  dependency of the milestone's own settled UI language choice — has not
  been exercised. It will appear as new cost the first time a real page uses
  it, not as a surprise this ADR failed to name.
- **Untested minority refusal paths.** `SURFACE_AMBIGUOUS`,
  `SURFACE_SCHEMA_INVALID`, `SURFACE_CONTENT_ROOT_UNREADABLE`,
  `SURFACE_INTEGRITY`, and `REGISTRY_INVALID` are reachable but untested in
  this track — the same pattern `production_resolver.py` already has for
  `PACKAGE_AMBIGUOUS`, not a new gap. None sit on the security-relevant
  surface (digest, path confinement, adoption-kind isolation) this track
  actually exercised.

## Measured cost

The vendored dependency tree: **941 entries, 5,065,001 bytes (~5.07 MB)**,
one direct dependency (`svelte@5.56.8`). Confirmed independently by Track 1's
review, not taken from a commit message. This is the number future decisions
about what else ships through this container need to weigh against: one
trivial page and its transitive build-time dependencies already cost five
megabytes of opaque, unreadable bytes whose verification is pinning, not
review.

**The repository does not store that tree** (owner decision 2026-07-28). It
ships in the artifact and it is checked into nothing. It is reconstructed from
the lockfile with `npm ci` before the fixtures are regenerated or the surface
tests are run, and the tests skip with an explicit message when it is absent.

That is a deliberate trade and it costs something. Before, the digest and
refusal tests ran in any clone, because the bytes were present. Now nothing
surface-related runs until someone restores the tree, and CI restores nothing.
The evidence for this container's central claim — that it refuses on a digest
mismatch — is therefore reproducible on demand rather than continuously
checked. That is the same shape as the offline-enforcement gap above, and it
is now the second place where this milestone's evidence exists but is not
standing guard.

The narrower fix, not taken here: the digest, confinement, and adoption-kind
tests do not care what the bytes are. They could run against a three-file
synthetic tree built inside the test, leaving only the real build-and-open
tests dependent on the vendored dependencies. That would restore continuous
coverage of the security-relevant surface without storing five megabytes.
Worth doing; not done in this milestone.

## Consequences

- UI code has a sanctioned route into the live workspace, separate from and
  no threat to the artifact package's hard-validation guarantee.
- Any future page shipped through this container inherits, unchanged, the
  provenance guarantee and its stated limit: the served bytes come from
  exactly what was adopted, run through exactly the declared command, on
  whatever Node is present — not a guarantee that those bytes are the ones
  anyone reviewed.
- No maturity cell moves. This ADR records a container and its trust
  argument; it implements no enforcement substrate, and it closes the
  same-machine half of the determinism question by observation while leaving
  the cross-machine half and offline enforcement on non-macOS platforms open.
- Future work, named rather than silently owed: a byte-identity check for the
  build output *across machines and Node versions* (the same-machine case is
  checked), and a decision about where a "build-toolchain precondition"
  category is formally recorded once more than one milestone needs it.

## Alternatives considered

- **Add an opaque-member role to `artifact-package.v4`.** Rejected; see
  "why the artifact package was left alone" above.
- **A second, independently written verification path for the surface
  artifact.** Rejected by the milestone plan itself before Track 1 started;
  Track 1's review confirmed the actual result is genuine reuse of ADR-0033
  Decisions 1 and 2, not a fork.
- **Treat "verified inputs plus fixed command" as sufficient without
  qualification.** Rejected here; see the build-output decision above. The
  weaker, precise claim is the honest one.
- **File Node under ADR-0047 Class D.** Considered and rejected; Class D is
  a total classification of viewing-session leakage channels, and Node's
  presence is a build-time functional precondition, not a channel a session
  could leak through. Forcing it in would blur a class this project defined
  exactly around a different question.

## Links

- Milestone: `docs/phases/legible-entry/milestones/packaging-the-surface.md`
- Track 1 charter and review:
  `docs/reviews/charter-2026-07-28-packaging-the-surface-track1.md`,
  `docs/reviews/2026-07-28-packaging-the-surface-track1-review.md`
- Track 2 charter: `docs/reviews/charter-2026-07-28-packaging-the-surface-track2.md`
- Resolver: `packages/derivation/surface_resolver.py`
- Schema: `packages/schemas/derivation/surface-artifact.v1.schema.json`
- Production package resolver (reused decisions): `docs/adr/0033-production-package-resolver.md`
- Live-run trust domains: `docs/adr/0044-live-run-system-boundary-and-trust-domains.md`
- Live viewing environment (Class D framing considered and rejected here):
  `docs/adr/0047-live-viewing-environment.md`
- Entry boundary: `docs/adr/0048-entry-boundary.md`
- Fixture and build script: `packages/sample_data/surface_t1/`
- Offline build and open-through-vehicle proof:
  `tests/test_surface_t1_build_and_open.py`

## Evidence limits

No real workspace and no real owner adoption was consulted. The
same-machine determinism observation is a direct experiment — the content
tree copied twice, `node build.mjs` run in each copy with a gap, `diff -r`
over the two `dist/` trees, byte-identical, run independently twice — and is
used as load-bearing evidence for exactly the claim it supports and no wider.
It was performed on one machine, on macOS, under Node v25.8.0, against the
synthetic `surface_t1` fixture tree; no other machine, operating system, or
Node version was involved, so nothing here speaks to cross-environment
reproducibility. The offline-enforcement evidence is likewise
one-machine, macOS-only, and outside CI.
