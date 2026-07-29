# Charter — Packaging the Surface, Track 1: the surface artifact

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/phases/legible-entry/milestones/packaging-the-surface.md`
- Branch: `milestone/packaging-the-surface`
- Deliverable: a second artifact container for UI code, one trivial Svelte
  page shipped through it, and the tests that show it working and refusing.

## What you are building, in one sentence

A second sealed container, separate from the artifact package, that carries
program files across the Developer/Supply → Live-Run Data boundary under the
owner's adoption, verified by digest and never read for meaning — plus one
boring page that proves it works.

## Why it is a second container and not a change to the existing one

The artifact package (`packages/schemas/derivation/artifact-package.v4.schema.json`)
holds members shaped `{role, schema, id, version}`: identities pointing at
typed declarative citizens from a closed enum. No paths, no files. Its whole
value is that the entire member graph hard-validates before anything runs.
Source code and a vendored dependency tree cannot be members of that, and
adding an opaque-member kind would turn "everything in this package validates"
into "everything except the parts that don't," permanently.

The owner decided against that. **Do not modify `artifact-package.v4`, add a
member role, add an admitted schema, or loosen any validation on it.** If you
find yourself needing to, stop and report — that is a finding, not a licence.

## What the container must do

Read `packages/derivation/production_resolver.py` and ADR-0033 before
designing anything. The release and registry verification there is the part
you reuse.

- It hangs off the **same verified release and registry chain** the artifact
  package already uses. Do not write a second verification path. If the
  existing one turns out not to be reusable, stop and report it rather than
  duplicating it — a parallel verification path is not an acceptable outcome
  of this track.
- It is opened by a **distinct owner adoption**. Whether that is a new act
  schema or a scoped reuse of `act-package-adoption.v1` is yours to determine
  against the code; say which you chose and why.
- Every entry carries a **digest**, checked before use.
- Its contents are **opaque**: program files, verified by fingerprint, never
  validated for meaning. Say that in the schema's own description so nobody
  later mistakes it for a package that validates.

## What you ship through it

One deliberately boring page. A heading and a static line of text. No input,
no workspace data, no styling worth arguing about. It is a Svelte component
only so that the build path is genuinely exercised — a hand-written HTML file
would prove nothing.

Inside the artifact: the source, the lockfile, and the resolved dependency
tree. Nothing is fetched at build time.

## The build

At the workspace, not in the repository. One fixed command. **Network off and
install-time lifecycle scripts disabled** — this is the whole reason the
dependencies travel inside the artifact, so make it observably true rather
than assumed. Say how you made it true.

Node is not shipped and is assumed present on the machine. Note what version
you relied on; the ADR will have to declare it as a workspace precondition.

## Then open it

The built page renders in the live-viewing vehicle
(`packages/derivation/live_viewing.py`, ADR-0047) against a **synthetic**
workspace. The page reads nothing and writes nothing, which keeps it inside
what that vehicle was already evaluated for. Do not extend the vehicle's
preflight or attestation — that belongs to the milestone that builds the loop.

## The refusal case is part of the deliverable

Corrupt a shipped byte and show resolution refuses. Not a follow-up, not a
TODO. A test in this track.

## Measure the cost

Record the vendored tree's size: entry count and total bytes. Track 2 has to
justify that number to the owner, so it needs to be real and stated, not
estimated.

## Boundaries

- Synthetic only. No real workspace, no residency locator, anywhere.
- No form fields, no typed input, no contribution events.
- No missing-facts view, no entry loop, no product screens.
- No maturity claim. Nothing moves on any matrix.
- No ADR. Track 2 writes it; your job is to make it have something true to
  say.

## Stop conditions

- The release/registry verification cannot be reused for a second container.
- Doing this cleanly requires changing `artifact-package.v4`.
- The vendored dependency tree is large enough that you think the owner would
  not accept it. Report the number rather than deciding for them.
- The offline build cannot be made observably offline.

## Verification

The CI `verify` sequence, or a stated subset with each omission justified.
Include the data-safety scan. State the commit you built from.

## Report back

What the container is and how it verifies; which adoption route you chose and
why; how you made the build offline; the vendored tree's real size; the
refusal test; the Node version you relied on; and the weakest part of what you
built.
