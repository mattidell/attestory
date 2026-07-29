<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "packaging-the-surface",
  "milestone_state": "closed",
  "retrospective": "docs/milestone-retrospectives/2026-07-28-packaging-the-surface.md",
  "status": "CLOSED 2026-07-28. Both tracks READY; ADR-0049 PROPOSED, not ratified. Track 1 0fd05e7 / review ee50b8f, Track 2 8d8ef76 / review 17338d9. A second sealed container (surface-artifact.v1) now carries UI program bytes into Live-Run Data under a distinct surface-adoption, verified by digest and never validated for meaning; artifact-package.v4 is untouched. One Svelte page built offline at the workspace and opened in the live-viewing vehicle on a synthetic workspace; five refusal paths tested. Vendored tree 941 entries / 5,065,001 bytes. Build determinism CHECKED byte-identical on one machine under Node v25.8.0, UNVERIFIED across machines or versions. NO MATURITY CELL MOVED. Retrospective subject: the plan shipped a FALSE PREMISE — the foreman called the package-member route 'close to forced' without opening the schema, and it survived a plan PR and an owner decision built on top of it. Owner decision after the close (370f8a6): THE REPOSITORY DOES NOT STORE THE VENDORED TREE — node_modules is gitignored, ships in the artifact, and is rebuilt with `npm ci` in packages/sample_data/surface_t1/content/app plus tools/generate_surface_t1_fixtures.py; six surface tests skip without it, so the digest and refusal evidence is reproducible on demand rather than continuously checked. Carried open: build output never digest-verified, offline enforcement macOS-only with no CI coverage, three underscore-private imports from production_resolver, no TypeScript in the sample page. Next: milestone 3, The Entry Loop synthetic, unplanned. Current state lives in docs/phase-state.md; this plan is a closed record.",
  "scope": [
    "define a second artifact container for UI code, with its own adoption act, hanging off the existing verified release and registry chain",
    "ship a trivial Svelte page, its lockfile, and its vendored dependency tree inside that artifact, each entry digested",
    "build it at the workspace with the network off and install scripts disabled, by one fixed command",
    "open the result in the live-viewing vehicle against a synthetic workspace",
    "show resolution refuses when the shipped bytes do not match their digest",
    "measure what the vendored tree costs in entries and bytes",
    "record the rule, why the artifact package was left alone, the build-output trust argument, and the Node precondition as a short ADR"
  ],
  "non_goals": [
    "NO CHANGE TO artifact-package.v4 — no new member role, no new admitted schema, no opaque-member kind, no loosened validation",
    "no second, independently written verification path — reuse the release and registry chain or stop and report",
    "no form fields, no typed input, no contribution events",
    "no real data, no real workspace, no owner attestation, no maturity claim",
    "no extension of the viewing preflight or attestation to entry sessions",
    "no missing-facts view, no entry loop, no product screens",
    "no new tax rule"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/legible-entry/milestones/packaging-the-surface.md",
      "docs/phases/legible-entry/legible-entry-roadmap.md",
      "docs/adr/0033-production-package-resolver.md",
      "packages/schemas/derivation/artifact-package.v4.schema.json",
      "docs/adr/0044-live-run-system-boundary-and-trust-domains.md",
      "docs/adr/0047-live-viewing-environment.md",
      "docs/adr/0048-entry-boundary.md",
      "packages/derivation/live_viewing.py",
      "AGENTS.md#Data Safety Rules",
      "AGENTS.md#Fixture Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/legible-entry/milestones/packaging-the-surface.md",
      "docs/adr/0033-production-package-resolver.md",
      "packages/schemas/derivation/artifact-package.v4.schema.json",
      "docs/adr/0044-live-run-system-boundary-and-trust-domains.md",
      "docs/adr/0047-live-viewing-environment.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "merge_or_records": [
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ]
  }
}
-->
# Milestone: Packaging the Surface

Status: **closed 2026-07-28.** Both tracks built and reviewed READY. ADR-0049
proposed. Retrospective:
`docs/milestone-retrospectives/2026-07-28-packaging-the-surface.md`.

## What this is for

The last milestone decided a browser form is an acceptable place to type a tax
fact, and that such a form must emit contribution events rather than write
anything itself. It did not say how the form gets onto the owner's machine in
the first place.

That turns out to be a real question. UI code is written in the source
repository, and the source repository has no authority to touch the live
workspace. The only sanctioned way anything crosses into the live workspace is
the package the owner has adopted, whose bytes are verified against a
published digest chain. Today that package carries derivation rules —
declarative documents. A user interface is a different kind of thing: it is
code and assets, and most ways of producing it involve a build step that makes
the shipped bytes different from the bytes anyone read.

The owner has settled the shape of the answer, below. What this milestone does
is prove it by shipping something through it. The thing we ship is deliberately
boring: one page that renders and does nothing interesting. We are testing the
pipe, not the product.

## What the owner decided, 2026-07-28

Two choices were settled before this plan was approved, and the rest of the
milestone follows from them.

**The UI is written with a component framework — Svelte and TypeScript — and
built at the workspace, not in the repository.** The alternative was to forbid
a build entirely and hand-write plain browser code so that shipped bytes and
readable bytes were the same thing. That was rejected as too costly for a
form-heavy application, in favour of shipping readable source and building it
where it runs.

**The libraries ship with the UI, not fetched at build time.** The resolved
dependency tree travels alongside the source, digest-verified, so the workspace
build runs with the network off. The alternative — a package-manager install
against the public registry at build time — was rejected because it would let a
second, unadopted supply chain into the domain holding real financial data, and
would run install-time scripts there.

The cost accepted along with that: whatever carries the UI gets much larger, and
the vendored bytes are third-party and not readable in any useful sense. Their
verification is pinning and digests, not review.

## Correction: the UI cannot be a package member

This plan was approved saying the UI would ship as members of the adopted
artifact package. That was wrong, and the error was the foreman's.

A member of that package is `{role, schema, id, version}` — an identity
pointing at a typed declarative citizen, from a closed enum of roles and
schemas (`packages/schemas/derivation/artifact-package.v4.schema.json`). There
is no path and no file. The package's guarantee is that its whole member graph
hard-validates before anything runs. Source files and a vendored dependency
tree cannot be members of that in any form.

So the container was a real choice, not a formality. The owner settled it on
2026-07-28:

**The UI ships in a second, separate artifact with its own adoption act.** It
reuses the release and registry verification the artifact package already
depends on, but it is its own container with its own rule about its contents:
program files, verified by digest, never read for meaning. The artifact
package's promise — everything in here validates — stays true without a
footnote.

The alternative was to add an opaque-member kind to the existing package.
Cheaper to build, but it turns "everything in this package validates" into
"everything validates except the parts that don't," permanently, to save
effort once. Rejected.

The cost accepted: a second thing the owner adopts, plus the schema and
resolver path to open it.

## What is still open

**1. Is the build's output trustworthy when nothing verifies it?** Every input
to the build is digest-verified; the output is not, because it did not exist
until the workspace made it. The trust rests on verified inputs plus a fixed
build command. Whether that is enough, and whether the build needs to be
reproducible for it to be enough, is a real question.

**2. What toolchain is assumed present?** The build needs Node, and Node is
not shipped in either container. That makes it a precondition of the live
workspace rather than something the crossing carries, which is a different kind
of dependency than anything the project has declared so far.

**3. What serves the page?** The live-viewing vehicle already launches a
confined browser against a loopback address. Does the entry surface reuse it,
and is the server part of the shipped surface or part of the runtime already on
the machine?

**4. How much of the existing adoption machinery does the second container
reuse?** The release and registry verification is shared. Whether the adoption
act itself is a new schema or a scoped reuse of the existing one is for Track 1
to find out against the code.

## How we will answer them

Build first, record the rule afterwards. The container is chosen; what remains
is answered better by attempting it than by reasoning about it.

### Track 1 — build the second container and ship one page through it

Define the surface artifact and prove it with one deliberately boring page:

- the page is a heading and a static line of text — no input, no workspace
  data. It is a Svelte component only so that the build is exercised;
- source, lockfile, and the vendored dependency tree ship inside the surface
  artifact, each entry carrying a digest;
- the artifact hangs off the same verified release and registry chain the
  artifact package uses, and is opened by a distinct owner adoption;
- resolution refuses when bytes do not match their digest. That negative case
  is part of the deliverable, not a follow-up;
- the workspace builds it with the network off and install-time scripts
  disabled, by one fixed command;
- and the result opens in the live-viewing vehicle against a synthetic
  workspace.

Reuse the existing release and registry verification rather than writing a
parallel one. If that turns out not to be reusable, stop and report it — a
second, independently written verification path is not an acceptable outcome
of this track.

Along the way, record what the vendored tree actually costs in entries and
bytes, because that number is what the ADR has to justify.

### Track 2 — write down the rule

A short ADR recording what Track 1 established: the surface ships in its own
adopted artifact, separate from the artifact package, carrying source plus
vendored dependencies; it builds at the workspace offline; it is served by
whatever Track 1 found workable. It should also say why the artifact package
was left alone, what the build's unverified output rests on, and name the Node
toolchain as a workspace precondition. It documents something already tested,
so it should be brief.

## Not in this milestone

No form fields, no typed input, no contribution events. No real data, no real
workspace, no attestation, no maturity claim — this milestone moves no cell of
the phase's instrument, because it builds no part of the entry loop.

ADR-0048 noted that an entry session, which creates content, is not the
session type the viewing preflight was written for. That extension belongs to
the milestone that builds the loop. This milestone opens a page that reads
nothing and writes nothing, which stays inside what the vehicle was already
evaluated for.

## How we will know it is done

- A page ships in the surface artifact — source, lockfile, vendored
  dependencies — builds at the workspace with the network off, and renders in
  the vehicle on a synthetic workspace.
- The artifact package is unchanged. No new member role, no new schema, no
  loosened validation.
- The ADR is accepted, and it answers the three open questions or says plainly
  which one it is deferring and why.
- Corrupting the shipped bytes makes resolution refuse, shown by a test.
- The data-safety scan passes, and no real workspace was involved.

## Language

The phase has a stated goal of plainer writing, and it applies to this
document as much as to the product. The habit we are correcting is writing
every planning document as though defending it to a hostile auditor — hedged,
heavily qualified, assuming the reader already knows the whole history. That
voice is right for an ADR making a safety claim. It is wrong for a plan, and
it is the same context assumption the phase exists to fix in the product.

Plans and charters in this milestone are written for a reader who knows the
product and not the record.

## Shape of the work

Two tracks, sequential, each one build-and-review cycle. Track 1 is the work;
Track 2 writes down what it found. Milestone plan opens on a PR and the close
opens another; individual tracks keep their review gate but land on the
milestone branch without their own PRs.
