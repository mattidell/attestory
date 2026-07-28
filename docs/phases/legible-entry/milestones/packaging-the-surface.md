<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "packaging-the-surface",
  "milestone_state": "planned",
  "status": "PLANNED. Get UI code across the Developer/Supply to Live-Run Data boundary. Track 1 ships one trivial page as verified package members, no build step, opened in the live-viewing vehicle on a synthetic workspace, with a refusal test. Track 2 records the rule as a short ADR. Build first, ADR after — the route is close to forced by ADR-0044 and the real unknown is whether no-build is workable. No form fields, no contributions, no real data, no maturity claim.",
  "scope": [
    "ship one trivial page as members of the adopted package, byte-identical to source, no build step",
    "open it in the live-viewing vehicle against a synthetic workspace",
    "show resolution refuses when the shipped bytes do not match their digest",
    "record where UI lives, whether a build step is permitted, and what serves the page, as a short ADR"
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

So this milestone answers how UI reaches the workspace, and then proves the
answer by shipping something through it. The thing we ship is deliberately
boring: one page that renders and does nothing interesting. We are testing the
pipe, not the product.

## The questions

**1. Where does the UI live?** Inside the adopted package, as members
alongside the rules, inheriting the existing verification and adoption act? Or
as a separate artifact with its own adoption? Shipping it inside the package
means one adoption act and one verified chain, but it also means the package
is no longer only declarative content.

**2. Is a build step allowed?** If shipped bytes are compiled from source
bytes, the digest chain verifies an output nobody read. The plain alternative
is to forbid a build: the surface ships as files that are byte-identical to
what is in the repository. That constrains what the UI can be built with. We
should find out whether that constraint is survivable before accepting it.

**3. What serves the page, and from where?** The live-viewing vehicle already
launches a confined browser against a loopback address. Does the entry surface
reuse it, and is the server code part of the shipped package or part of the
runtime already resident on the machine?

## How we will answer them

The last milestone was a decision with no build, and that was right — the
question there was whether to build at all. This one is not shaped like that.
Question 1 is close to forced: the adopted package is the only sanctioned
crossing, and standing up a second adoption chain for a UI is plainly more
expensive than adding members to the one that exists. Questions 2 and 3 are
answered better by attempting the thing than by reasoning about it. So this
milestone builds first and records the rule afterwards.

### Track 1 — ship one page across the boundary

Implement the crossing and prove it with one deliberately boring page:

- the page is a heading and a static line of text — no input, no workspace
  data;
- it ships as package members, byte-identical to what is in the repository,
  with no build step;
- it resolves through the same verification chain any other package member
  resolves through;
- it opens in the live-viewing vehicle against a synthetic workspace;
- and the chain refuses when the bytes do not match their digest. That
  negative case is part of the deliverable, not a follow-up.

If the no-build constraint turns out to be unworkable, stop and say so rather
than adding a build step. That result changes the ADR and is worth more than a
page that renders.

### Track 2 — write down the rule

A short ADR recording what Track 1 established: where UI code lives, whether a
build step is permitted, and what serves the page. It documents a constraint
we have already tested, so it should be brief.

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

- A page ships as verified package members and renders in the vehicle on a
  synthetic workspace, with no build step between source and shipped bytes.
- The ADR is accepted, and it answers all three questions or says plainly
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
