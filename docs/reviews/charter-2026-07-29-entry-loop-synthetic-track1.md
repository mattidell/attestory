# Charter — The Entry Loop (synthetic), Track 1: build the loop for W-2

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Deliverable: the guided entry loop for W-2, end to end, on a synthetic workspace.
- The bar you are building against: `docs/phases/legible-entry/entry-usability-criteria.md`

## What this is

The first product build of the phase. A person opens the surface, sees what the
return is missing, types a W-2 fact, watches it land, corrects it if they got it
wrong, and reaches a computed return. Five steps, one fact family, synthetic
data throughout.

Two milestones cleared the way and neither built any of it: ADR-0048 decided the
surface emits contributions rather than writing facts, and ADR-0049 built the
route that gets UI code onto the machine.

Track 0 wrote the criteria you are aiming at, before you existed and
deliberately not shaped by what you build. Read them first. They are the bar
Track 2 will score you against, and they are more specific than usual — named
Form 1040 lines, contrast ratios, keyboard reachability, what a field must say
before someone types in it.

## Phase A — confirm the four dependencies. Do this first, and stop if they fail.

The criteria document names four things Track 1 must establish before the
evaluation can run. **They are unconfirmed. Nobody has opened the code to check
them.** The last milestone in this phase shipped a plan built on an unchecked
premise about a schema, and it survived a plan PR and an owner decision before
anyone opened the file. Do not repeat it.

1. A synthetic workspace can be seeded with every required non-W-2 fact, so W-2
   is the only missing family and a computed return is reachable by entering
   only W-2.
2. The entry surface can be served at a URL, and can send contributions through
   the existing admission path.
3. The surface can make the fixed W-2 evaluation sets and the zero-missing,
   fully-computed state observable.
4. The fixture makes every expected-impact line change when the W-2 Box 1 value
   is entered or corrected — 1a, 9, 11, 15, 16 — and leaves every
   untouched-comparison line unchanged — 2b, 3a, 3b, 12.

Dependency 1 is the one the milestone plan singles out: if a synthetic workspace
cannot be seeded that way, the fifth loop step needs a different design and the
plan is wrong about it. Dependency 4 is the one the Track 0 reviewer expects to
break: a correctly seeded workspace can still yield a fixture where one
expected-impact line does not move.

**If any of the four does not hold, stop and report before building.** That is a
finding about the milestone, not a failure of this track, and it is worth more
than a surface built on a premise that does not hold. Report what you found
against which code.

## Phase B — build the loop

Only after Phase A holds.

- **Know what is missing.** The outstanding W-2 facts, presented as the guide
  through entry. Not a diagnostic report beside a form — criterion 1.2 requires
  every missing item to carry an action that takes the person straight to its
  input.
- **Enter a fact.** Fields that name their source document and box, and say why
  the fact is being asked for.
- **See it land.** The person can tell the contribution was accepted, which of
  the expected-impact lines changed, and that the comparison lines did not.
- **Correct an entered fact.** Find an answered fact, change it, understand the
  result. Every fact type ships `free` today, so no correction can be refused —
  do not build refusal UI for a refusal that cannot fire.
- **Know the return is complete.** A definite end state: zero missing facts, a
  computed return, no further prompted required entry, and correction still
  reachable.

Entry emits `act-contribution.v1` through the existing admission path. **Nothing
in the surface writes a fact.** The surface ships and builds by the route
ADR-0049 established. Reuse what exists — if something turns out not to be
reusable, stop and report rather than writing a parallel path.

## Open questions this track answers by doing

**What serves the page.** ADR-0049 left it open. Whether the server is part of
the shipped surface or part of the runtime already present is yours to find out
against the code; say which you chose and why.

**Whether the viewing preflight covers an entry session.** ADR-0048 flagged that
an entry session creates content and the preflight was written for sessions that
only read. Everything here is synthetic, so nothing typed is real — but this is
the surface that will later carry real typing. Note what you relied on. **Do not
quietly extend the preflight**; if it needs extending, that is a finding and it
belongs to a later milestone.

## Boundaries

- **Synthetic only.** No real workspace, no real data, no residency locator in
  any surface — not in logs, request paths, subprocess arguments, diagnostics,
  or test names.
- **W-2 only.** No 1099-INT, 1099-DIV, or taxpayer-assertion entry.
- No filing. No new tax rule, no change to any derivation package, no change to
  `artifact-package.v4`, no new correction-authority mechanism.
- **No per-field explanation schema.** Build the fields; the shape they needed
  gets written down at close by Track 3. Do not design the representation up
  front — that ordering is deliberate.
- No maturity claim. Track 2 scores the criteria; you do not score yourself.
- No separate missing-facts screen.

## Stop conditions

- Any of the four dependencies does not hold.
- The admission path cannot accept a contribution originated this way.
- Serving the surface requires extending the preflight or the confined vehicle.
- Reaching a computed return needs a fact family outside W-2 that cannot be
  seeded.

## Verification

The CI `verify` sequence, or a stated subset with each omission justified,
including the data-safety scan, and the commit you worked from — recorded in the
commit message. The last two repairs on this branch set the standard and the
reviewer confirmed it; match them.

Orient with `python3 tools/build_orientation_block.py --ref HEAD`. There is no
`.venv`; use system `python3`. The ratified line is `origin/main-ui` and is
derived for you; the merged PR #109 is this milestone's opening plan PR and does
not mean the workspace is spent.

## Report back

Phase A first: each of the four dependencies, what you checked it against, and
whether it holds. Then what you built, what serves the page and why, what you
relied on from the preflight, which criteria you believe you meet and which you
are unsure about, and the weakest part of what you built.
