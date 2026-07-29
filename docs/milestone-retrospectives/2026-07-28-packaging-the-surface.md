# Retrospective — Packaging the Surface

Milestone: `docs/phases/legible-entry/milestones/packaging-the-surface.md`
Closed 2026-07-28. Track 1 `0fd05e7` (review `ee50b8f`), Track 2 `8d8ef76`
(review `17338d9`). ADR-0049 proposed.

## What the milestone did

UI code now has a way to reach the machine holding real financial data. It
travels in its own sealed container, separate from the one carrying tax rules,
under a distinct owner adoption, verified by fingerprint and never read for
meaning. One deliberately boring Svelte page went through it end to end: built
at the workspace with no network, opened in the confined browser against a
synthetic workspace, with five refusal paths tested. The rule package was not
touched.

## The thing worth learning

**The plan shipped with a false premise, and the only reason it was caught was
that chartering forced someone to open the schema.**

The plan said the UI would ship as members of the artifact package the owner
already adopts. The foreman called that route "close to forced" and reasoned
about the interesting question downstream of it — build steps, dependency
delivery — for two rounds with the owner, who made a real decision on that
basis.

It was not possible at all. A package member is `{role, schema, id, version}`,
an identity pointing at a typed declarative citizen from a closed enum. No
path, no file. Thirty seconds with the schema would have shown it. The foreman
had read ADR-0033 and the roadmap's framing of the question and reasoned from
the prose description of the package rather than from the package.

What makes this worth writing down is not the error but where it sat. It was
upstream of everything: the plan, the owner's framework choice, the dependency
decision. All of that was sound reasoning on a premise nobody had checked. And
it survived a plan PR and an owner approval, because neither of those is a
place where anyone reads a schema.

The correction was cheap because it was caught before a builder ran. Had the
charter been written from the plan without opening the code first, a builder
would have discovered it — probably by extending `artifact-package.v4`,
because that is the path of least resistance when the plan says the UI is a
package member and the schema won't take one. That would have been the
expensive version: the guarantee weakened by a builder doing as instructed.

**What to do differently:** when a plan asserts that a route is obvious or
forced, that is precisely the claim to verify against the code before writing
it down, not after. The word "forced" should read as an alarm, not a
conclusion.

## The smaller pattern, twice

Two agents deferred a check that took one command.

The Track 2 builder concluded the build was probably deterministic from
reading the compiler's documentation, named that as the weakest point in its
own reasoning, and filed the actual check as future work. The foreman ran it:
copy the app twice, build, diff. Byte-identical. Under a minute.

Both the builder and, on the first pass, the foreman treated "run it and see"
as heavier than it was. The builder deserves credit for naming the gap rather
than hiding it — that self-report is what prompted the check. But the honest
version is that the reasoning about whether to verify cost more than
verifying.

**What to do differently:** when the weakest point in an argument is something
observable, observe it. Estimate the cost of the check before deciding to
defer it.

## What went right

The two-container decision held up under review and is the right shape. The
owner's framing — one box with a footnote, or two boxes each meaning exactly
one thing — was what made it decidable, and translating the packaging question
out of its own vocabulary is what surfaced the real trade.

Track 1 came in far cheaper than forecast. The foreman warned the owner about
a vendored tree in the tens to hundreds of megabytes; it landed at 5.07 MB and
20 packages, because the builder skipped a bundler and compiled with the
framework's own compiler against browser import maps. The forecast was
pessimistic by two orders of magnitude, which is worth noting as its own
estimation failure even though it fell in the harmless direction.

Both reviews reran the evidence rather than reading the reports, and both
caught things worth catching.

## What is still open

- The build's output is not fingerprinted by anything, and cannot be — it did
  not exist until the workspace made it. Determinism is checked on one machine
  under one Node version and unverified across machines or versions. ADR-0049
  states this at its real width rather than closing it.
- Offline enforcement is proved only under macOS `sandbox-exec` and CI carries
  none of it, because those tests need Node and Chrome present. The evidence
  exists but is not continuously checked.
- `surface_resolver.py` reuses three underscore-private names from
  `production_resolver.py`. Real reuse, fragile coupling.
- The sample page uses no TypeScript, so that toolchain cost is untested and
  will appear in a later milestone.
- `tools/build_orientation_block.py` defaults to `--ref main`, which in this
  repository is a stale branch. The Track 2 reviewer hit it and reported it
  rather than routing around it.

## Instrument

No maturity cell moved. This milestone built no part of the entry loop, and
the instrument measures the loop.
