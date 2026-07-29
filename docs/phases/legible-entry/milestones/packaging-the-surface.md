<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "packaging-the-surface",
  "milestone_state": "planned",
  "status": "PLANNED. Get UI code across the Developer/Supply to Live-Run Data boundary. OWNER SETTLED 2026-07-28: UI is Svelte + TypeScript, built at the workspace not in the repo, and its pinned dependency tree is VENDORED INTO THE ADOPTED PACKAGE rather than fetched at build time — so the workspace build runs with the network off and no install scripts. Track 1 ships one trivial Svelte page plus lockfile plus vendored deps as verified package members, builds offline at the workspace, opens it in the live-viewing vehicle on a synthetic workspace, and shows a digest-mismatch refusal. Track 2 records the rule as a short ADR. Still open: what the build's unverified output rests on, the Node toolchain as an undeclared workspace precondition, and what serves the page. No form fields, no contributions, no real data, no maturity claim.",
  "scope": [
    "ship a trivial Svelte page, its lockfile, and its vendored dependency tree as members of the adopted package",
    "build it at the workspace with the network off and install scripts disabled, by one fixed command",
    "open the result in the live-viewing vehicle against a synthetic workspace",
    "show resolution refuses when the shipped bytes do not match their digest",
    "measure what the vendored tree costs in members and bytes",
    "record the rule, the build-output trust argument, and the Node precondition as a short ADR"
  ],
  "non_goals": [
    "no form fields, no typed input, no contribution events",
    "no real data, no real workspace, no owner attestation, no maturity claim",
    "no extension of the viewing preflight or attestation to entry sessions",
    "no missing-facts view, no entry loop, no product screens",
    "no new tax rule or schema"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/legible-entry/milestones/packaging-the-surface.md",
      "docs/phases/legible-entry/legible-entry-roadmap.md",
      "docs/adr/0033-production-package-resolver.md",
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

Status: **proposed.** Awaiting owner approval.

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

**The libraries ship inside the adopted package, not fetched at build time.**
The resolved dependency tree is vendored as package members, so it carries the
same digest verification as everything else and the workspace build runs with
the network off. The alternative — a package-manager install against the
public registry at build time — was rejected because it would let a second,
unadopted supply chain into the domain holding real financial data, and would
run install-time scripts there.

The cost accepted along with that: the package gets much larger, and the
vendored bytes are third-party and not readable in any useful sense. Their
verification is pinning and digests, not review.

## What is still open

**1. Is the build's output trustworthy when nothing verifies it?** Every input
to the build is digest-verified; the output is not, because it did not exist
until the workspace made it. The trust rests on verified inputs plus a fixed
build command. Whether that is enough, and whether the build needs to be
reproducible for it to be enough, is a real question.

**2. What toolchain is assumed present?** The build needs Node, and Node is
not shipped in the package. That makes it a precondition of the live workspace
rather than something the crossing carries, which is a different kind of
dependency than anything the project has declared so far.

**3. What serves the page?** The live-viewing vehicle already launches a
confined browser against a loopback address. Does the entry surface reuse it,
and is the server part of the package or part of the runtime already on the
machine?

## How we will answer them

The last milestone was a decision with no build, and that was right — the
question there was whether to build at all. This one is not shaped like that.
The route is settled; what remains is answered better by attempting it than by
reasoning about it. So this milestone builds first and records the rule
afterwards.

### Track 1 — ship one page across the boundary

Implement the crossing and prove it with one deliberately boring page:

- the page is a heading and a static line of text — no input, no workspace
  data. It is a Svelte component only so that the build is exercised;
- source, lockfile, and the vendored dependency tree all ship as members of
  the adopted package;
- they resolve through the same verification chain any other package member
  resolves through, and resolution refuses when bytes do not match their
  digest. That negative case is part of the deliverable, not a follow-up;
- the workspace builds it with the network off and install-time scripts
  disabled, by one fixed command;
- and the result opens in the live-viewing vehicle against a synthetic
  workspace.

Along the way, record what the vendored tree actually costs — member count and
total size — because that number is what the ADR has to justify.

### Track 2 — write down the rule

A short ADR recording what Track 1 established: UI ships as source plus
vendored dependencies inside the adopted package, builds at the workspace
offline, and is served by whatever Track 1 found workable. It should also say
what the build's unverified output rests on, and name the Node toolchain as a
workspace precondition. It documents something already tested, so it should be
brief.

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

- A page ships as verified package members — source, lockfile, vendored
  dependencies — builds at the workspace with the network off, and renders in
  the vehicle on a synthetic workspace.
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
