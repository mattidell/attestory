# Retrospective — The Entry Boundary

Milestone: `docs/phases/legible-entry/milestones/entry-boundary.md`
Phase: Legible Entry. First milestone of the phase.
Closed: 2026-07-28.

## What it produced

ADR-0048, proposed. A browser form is an acceptable place for a person to type
real tax facts, on stated conditions. An entry surface emits contribution
events rather than writing facts directly.

Behind it: a throwaway probe under `tools/entry_probe/` and a findings note
recording what a browser actually retained when typed into, in three runs —
headless, headed, and a widened search past the confinement boundary.

No product code changed. No maturity cell moved. That was the plan.

## What actually happened

The milestone was chartered on the theory that we did not know what browsers
retain, and should look before building a form. That was right, but it
understated the problem. The harder thing turned out to be knowing when we had
looked properly.

Three times, a negative result was believed before it had earned belief.

**First:** the builder charter named `tools/presentation_harness/lib/chrome.mjs`,
which hardcodes `--headless=new`. Headless Chrome stubs some of the features the
probe was built to detect. The probe found nothing because it was pointed at a
browser that could not have shown anything. That was a foreman error, caught by
the Track 1 review.

**Second:** the corrected headed run also found nothing, and ADR-0048's first
draft turned that into "confinement is already total." But every run had searched
only *inside* the directory the confinement manages — the one place the question
was not. The Track 2 review caught it, and the widened run then found that the
vehicle does write outside the confined tree: a single-instance lock directory in
the temp directory, surviving a crash, never touched by disposal. No typed
content in it. But "confinement is total" was simply false, and had shipped in
the section titled "answer."

**Third:** the repair scoped the Confinement paragraph and left the Disposal
paragraph directly beneath it still claiming to cover "channels this project has
never enumerated." Caught by the recheck.

## The pattern worth keeping

All three are the same shape: **a search whose scope quietly presupposed its
answer**, and a document that stated the conclusion more strongly than the search
supported.

The reviewer's own observation at close is the useful generalization: this defect
appeared three times in one ADR, in three different sections, and each instance
surfaced only by reading the whole document against itself. It is structural to
how a long document gets revised — a section gets corrected, and the sentence two
paragraphs down that depended on the old claim does not. It is not a lapse by any
one author.

That matters for this phase specifically. Legible Entry exists to make documents
honest to a reader who has no context. The failure mode we hit repeatedly is the
one where the qualification *feels* present to the author because they remember
writing it, three sections away. A reader who stops at the section called
"answer" gets the unqualified version.

## What worked

**The review gate caught every one of the three.** None surfaced from a builder's
self-report, and none would have been visible in a diff. Each needed someone
reading the whole artifact against its own evidence.

**Positive controls.** The first builder found that its `grep -rlaI` flag
combination silently suppressed matches inside binary stores, caught it by
planting a token and confirming the grep missed it, and re-verified after fixing.
Without that, every channel would have reported "not fired" for a reason that had
nothing to do with browsers. Two later runs re-ran the control rather than
inheriting the result.

**Attribution by process, not timing.** The widened search ran on a machine with
an unrelated real Chrome running throughout. Using `lsof` against the exact
launched pid, and birthtime rather than mtime, is what makes the result mean
anything.

**Refusing to make the claim true by construction.** Adding `--disable-breakpad`
would have converted the open question into a closed one in a single line. The
charter forbade it and the builder recommended it as owed work instead. The
milestone's job was to find out what is true, not to arrange for a convenient
answer.

## What to carry forward

Recorded in ADR-0048 under "Left undecided," not scheduled:

- **Nothing has searched for the residency locator outside confinement.** Every
  run looked for typed tokens. The locator is protected in its own right. This is
  a gap in what has been checked, not evidence of a leak — and it is the most
  direct descendant of this milestone's recurring error.
- The single-instance lock directory is a second orphan surface, outside the
  residency, that nothing sweeps.
- Whether crash-reporting or GPU-shader-cache paths write outside confinement —
  narrowed by the widened run, not closed.
- The spellcheck network path must be affirmatively closed by a flag, not
  observed to be off. Mechanism not designed.
- Whether crash-orphaned session directories need a sweep, given ADR-0047 treats
  backup and indexing as silently fatal.

## Process notes

**PR granularity changed with this milestone.** One PR to open, one to close;
tracks kept their review gate but not their own PR. It worked well here. The
tracks were tightly coupled — each existed because the previous one's result was
wrong — and splitting them across PRs would have put three superseded findings on
`main-ui` as if they were conclusions.

**The foreman left `phase-state.md` pointing at a discharged charter three
times** in this milestone, twice caught by a reviewer rather than by the foreman.
Recurring, named previously, still recurring.

**Six agent dispatches**: three builders, three reviewer rounds (one full, one
folded, one recheck plus confirmation). Two of the six existed only because of the
first charter's wrong vehicle. The recheck's final finding was repaired by the
foreman directly rather than by a seventh dispatch, which was the right call at
that size.
