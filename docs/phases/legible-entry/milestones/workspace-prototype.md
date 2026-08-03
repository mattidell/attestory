<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "workspace-prototype",
  "retrospective": "docs/milestone-retrospectives/2026-08-02-workspace-prototype.md",
  "status": "Open on main-ui 2026-08-01. The owner directs the work and decides what to try and when it is done.",
  "scope": [
    "prototype a workspace view: the home, map, and inbox for the record",
    "let a person understand the workspace's scope and current state at a glance",
    "surface what needs attention and why, without flattening the presentation model that already explains each line",
    "reuse the entry loop's existing explanation walk as the drill-down from the workspace into one fact",
    "return from the drill-down to the workspace without losing context",
    "adapt the work as the running prototype reveals the next useful question"
  ],
  "non_goals": [
    "no dashboard-building ahead of a real orientation need -- keep the surface to orientation and navigation, not summary statistics or new visualizations",
    "no second explanation engine -- the workspace view links into the existing walk rather than deriving tax meaning again",
    "no fixed track sequence or predetermined definition of done",
    "no maturity claim or broad criteria exercise",
    "no real personal data unless the owner separately chooses a real-data exercise"
  ],
  "deep_reads": {
    "implementation": [
      "docs/phases/legible-entry/milestones/workspace-prototype.md",
      "packages/derivation/entry_loop.py",
      "packages/derivation/presentation_projection.py",
      "packages/sample_data/entry_loop_t1/surface/content/app/src/EntryPage.svelte",
      "AGENTS.md#Owner-directed mode",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/phases/legible-entry/milestones/workspace-prototype.md",
      "AGENTS.md#Owner-directed mode",
      "AGENTS.md#Data Safety Rules"
    ],
    "merge_or_records": [
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ]
  }
}
-->
# Workspace Prototype

Status: **closed on `main-ui`, 2026-08-02.**

## A note on the name

This project already uses "workspace" for the machine hosting a confined
session (`AGENTS.md`'s residency and preflight language). This milestone uses
the same word for a different thing: the product surface a person lands on
to orient themselves in the record. The two senses do not overlap in any
document this milestone touches, but a reader moving between `AGENTS.md` and
this plan should not assume they are the same concept.

## Goal

The Improvised Prototype answered "what produced this value?" one line at a
time. This milestone asks a broader question: what is this workspace, what
does it contain, where do I stand, and what should I do next? It is the home,
map, and inbox for the record -- the place a person starts and returns to,
not a replacement for the explanation walk already built.

A working prototype should let someone:

1. understand the workspace's scope and current state -- what fact families
   exist, what's been entered, what the record currently computes to;
2. see what needs attention and why -- not just that something is missing,
   but the same kind of grounded reason the explanation walk already gives
   for a computed line;
3. enter one granular fact or explanation walk from there -- the workspace
   is a launching point into the existing entry and explanation surface, not
   a second place that re-implements it;
4. return to the workspace without losing context -- the trip out and back
   preserves where the person was and what they'd already opened.

## The strongest argument against this

Premature dashboard-building: inventing summary widgets and status tiles
ahead of any real orientation need, which would be scope invented rather
than scope discovered. The guard is to keep the surface narrow --
orientation and navigation only -- and to treat the existing explanation
work as the drill-down rather than building a second one. If a card on the
workspace can't point back to something the presentation model already
computed, it doesn't belong yet.

## How we will work

This is owner-directed work, in the same mode as the Improvised Prototype.
No fixed tracks, no charter requirement, no precommitted exit test or
scoring sheet. Builders and reviewers are optional tools, used when they
answer a question actually in front of us. Because this is new ground with
no established goals, the intent is a set of experiments: try a shape, run
it, see what it teaches, keep or discard it. There is no wrong answer at
this stage -- a discarded experiment that narrows the next one is a good
outcome.

## First card

Build a workspace landing view against the existing synthetic W-2 workspace:
list what the entry loop already knows about (fact families, entered vs.
missing, current computed state) using data the presentation model already
supplies, and let selecting an item open the existing entry/explanation
surface. Add a way back to the workspace that preserves what was open.

The work stays synthetic by default and does not add tax logic or a second
account of what a line means.

## Findings so far

**Card 1a (reverted): a client-side view swap inside `EntryPage.svelte`,
defaulting the root to a workspace landing screen.** Broke the ratified
keyboard-operability harness -- 12 test failures. The harness's own
navigation-and-control-discovery design (`tests/helpers/entry_loop_keyboard_operability_client.mjs`)
hard-depends on `dist/index.html` booting straight into the entry form
(`#w2-box1` present on load) and on the wordmark being exactly the one `<a>`
control it already knows how to check. **`index.html`'s default boot state is
load-bearing for the W-2 column's L2 claim, not just a UI convenience.**

**Card 1b (kept): `workspace.html` as a genuinely separate, additive page.**
Fetches the same `/api/state` the entry surface already uses, no backend
change. `index.html` and `EntryPage.svelte` are byte-for-byte untouched; full
suite green (47 passed). This is the shape to keep building on.

**Card 1c (kept, harness fixed): a second "back to workspace" link added to
`EntryPage.svelte`, alongside the existing wordmark.** First attempt broke
the harness's `navigationChecks()` phase (`browser-evaluation-failed`): that
phase fires every discovered href control's Enter key at the end of a run,
but wasn't written to survive a control's activation causing a *real*
document reload. The wordmark had never previously exposed this -- not
because it "doesn't navigate" (it does; every successful link activation
here is a fresh document load, same URL or not), but because with only one
queued link, nothing needed the page again afterward. A second link exposed
that the harness would try to keep using the first page's now-gone JS
globals on whatever page it left. Fixed in
`tests/helpers/entry_loop_keyboard_operability_client.mjs`: after any real
navigation, the harness now returns to the original page and reinstalls its
probe helpers before checking the next queued control, so coverage doesn't
quietly drop a control instead of erroring. A second, narrower fix was
needed in the `scramble-order` defect-injection fixture (demonstration-only,
not the real check): its hand-built redirect cycle had one anchor wired in
by name; the new anchor needed wiring into the same cycle to keep
demonstrating what it's meant to demonstrate. Full suite green (47 passed)
with both fixes and the link. The harness change is a real generalization,
not a scope carve-out -- any future link on this page is now covered the
same way.

**Card 1d: preserving the explanation trail across the round trip.** The
back-to-workspace link is a real page reload, so `expandedLines` -- the
in-memory record of which lines' explanation panels are open -- reset to
closed every time, even though the round trip is otherwise fast. Fixed by
persisting `expandedLines` to `sessionStorage` on every open/close and
restoring it on mount, in `EntryPage.svelte`. sessionStorage survives a
same-tab navigation and clears itself when the tab closes, which matches
the shape of the problem exactly: remember what was open for this visit to
the record, not forever. Verified directly against a running server (not
just the test suite): opened line 1a's panel, read `sessionStorage` before
navigating (`["1a"]`), followed the real link to `workspace.html` and back,
and found the panel open again with no extra step. Full suite still green
(47 passed). "Return to the workspace without losing context" is now
answered for the entry page's own state; the workspace page itself carries
no per-visit state yet to lose.

**Card 2: deep-linking from the record map.** Each row in `workspace.html`'s
record map now links straight to that line's explanation on the entry page,
instead of just to the entry page generally. The obvious approach -- a URL
query string like `index.html?w2-box1` -- doesn't work here: the entry
surface's own request handler (`_target()` in `entry_loop.py`) rejects any
request carrying a query string outright, a data-safety boundary that
predates this milestone and isn't this milestone's to relax. A URL
**fragment** (`index.html#line=9`) sidesteps the question entirely rather
than needing an exception to it -- a fragment never leaves the browser, so
the server never sees it and the boundary is untouched. `EntryPage.svelte`
reads the fragment on mount, after state loads, and reuses the existing
`jumpToLine` (the same function dependency chips already call) to expand
and scroll to that line, then clears the fragment via
`history.replaceState` so a reload or bookmark doesn't re-trigger it.
Verified directly against a running server: followed the workspace's line-9
link, landed on the entry page with that line's explanation open and
focused, hash cleared after. Full suite still green (47 passed).

**Card 3: fixing a boundary violation the guard-rail check found.** A
holistic look at whether `workspace.html` had drifted toward a dashboard
(inventing new computed meaning, inviting the reader to stay) found it
hadn't -- but found something adjacent and worth fixing anyway: two of the
three Scope-card fields (`Fact families`, and the denominator of `Facts
entered`) were hardcoded literals (`1`), not values read from `state`. They
looked like live data next to the one field that was, and there was no
`state` field they could have pointed back to even if they'd tried -- the
backend doesn't expose a fact-family count today, only ever having exactly
one. That's not dashboard drift; it's the same failure in the other
direction, presenting an assumption as though it were sourced. It would
have surfaced as a visibly wrong page the moment a second fact family
existed -- exactly the next experiment on the list -- so it's a
prerequisite fix, not a separate cleanup. Now reads both fields from
`state.field_contract` (one entry per fact the workspace can accept, so its
key count and each entry's `source.document` are already live). Verified
against a running server: "Fact families" now reads "1 · Form W-2" and
"Facts entered" reads "0 of 1", both computed, not written. Full suite
still green (47 passed).

**Card 4: the second fact family, done for real.** The scope-card fix
above was a prerequisite for actually testing whether the workspace's
design holds up with more than one fact -- this card is that test, done
against a genuinely second enterable fact rather than a simulated one. Two
sub-decisions the owner made explicitly shaped how this went:

- *Reopen the real fixture, not an isolated sibling.* The safer-looking
  option was a parallel fixture that couldn't touch the ratified
  keyboard-operability suite at all. The owner chose to reopen
  `entry_loop_t1` itself instead -- accepting that the suite's "exactly one
  missing fact" assumption would break across roughly 15 tests, on the
  view that the L2 rating describes what was true of the old shape, not a
  lock on it, and that avoiding the change to protect a number would be
  backwards. It did break that many, all fixed in one structural pass (not
  test-by-test): a `enter_both()`/keyed-`enter()` helper generalization,
  then updated assertions reflecting genuinely new behavior -- most
  notably that Tax (line 16) now honestly depends on qualified dividends
  (3a) as well as wages, a dependency that was always arithmetically true
  but invisible while dividends was pre-closed.
- *Expose the minimum multi-fact model first, then build one vertical
  experiment through it, before touching any UI.* `entry_loop.py`
  generalized from every W-2-specific constant and method into a small
  `_FactFamily` dataclass with exactly two instances (W-2 Box 1, 1099-DIV
  Box 1b -- mirrored, not abstracted to unbounded N): `field_contract`,
  `missing`, `answered`, and a new `contributions` dict (one submission
  template per family, replacing the single `contribution`) all now
  iterate the family list. `entryTargets` generalizes the old single-entry
  `tracesToEntry` boolean to a list -- and it's genuinely correct, not
  just renamed: Tax's explanation now reports `["w2-box1",
  "div1b-qualified"]`, reachable from both entry points at once, verified
  directly against the real derivation engine. One honest limitation
  surfaced here: the dependency graph only carries edges for lines that
  have actually computed, so a *blocked* composite line's `entryTargets`
  is unreliable (empty) even though an entry line itself can always
  self-report while blocked. The workspace's "why" copy was redesigned
  around this rather than working past it -- it states which Form 1040
  line a missing fact feeds (`field_contract[key].destination.line`,
  always sourced, never guessed) instead of trying to count blocked lines
  it can't honestly attribute.

**Both surfaces are now field-keyed, not duplicated.** `EntryPage.svelte`
was rewritten around a `FIELDS` registry (one entry per fact, still
importing each field's own declaration module rather than reading labels
from the API -- that's what keeps `RenderedFieldDerivation`'s
mutation-to-DOM guarantee true) and a single `{#each FIELDS}` block
renders one full entry panel per fact, instead of two hand-written copies.
`amounts`/`inputRefs` became per-key objects; `focusField(key)` replaced
the single hardcoded `goToWages`. `WorkspacePage.svelte` needed almost no
structural change -- `factFamilyDocuments`, the attention list, and the
record map were already iterating `state`'s own collections, so they
scaled from one fact to two for free; only the "why" line's per-fact
sourcing (above) needed real work.

**A field-keyed UI surfaced a real accessibility bug the harness caught
directly, not a UI polish item.** With two missing facts, both "Enter this
fact" buttons carried identical text -- genuinely ambiguous to Tab and
screen-reader navigation, not just to the harness's text-based control
keying. Same collision on "Correct this fact" once both facts were
answered. Fixed by making both labels state the specific fact ("Enter Form
W-2 Box 1" / "Enter Form 1099-DIV Box 1b", "Correct W-2 Box 1" / "Correct
1099-DIV Box 1b") -- the harness's reverse-traversal check is what
surfaced this, exactly the shape of defect Track 4 built it to catch.

**Exercised deliberately, not just tested.** Both entry orders were driven
live against a real server and the intermediate state inspected at each
step, not just the final complete state: entering W-2 first left Tax
correctly still "Waiting" while Total income correctly computed (proving
16 needs both facts, 9 needs only wages); entering 1099-DIV first showed
"1 missing fact" and line 3a's value landing correctly before W-2 was ever
touched. Both converge on the same complete state regardless of order.

**Browser tests unified through one shared journey driver, not three
patched scripts.** `tests/helpers/entry_loop_journey.mjs` is new: it knows
the loop's known fields once (mirroring `_FactFamily` on the JS side) and
exposes `populateAllFields` (data population without submitting, for the
keyboard-operability probe's own measured Enter/Space activation to
submit for real) and `completeJourney` (populate-and-submit, for the two
scripts that don't care about measuring keyboard activation specifically).
All three existing browser-driving scripts
(`entry_loop_browser_client.mjs`, `entry_loop_focus_indicator_client.mjs`,
`entry_loop_keyboard_operability_client.mjs`) now import it instead of
each re-typing its own single-field submission sequence. The
`scramble-order` and `swallow-activation`/`break-reverse-traversal` defect
fixtures (demonstration-only, not the real check) were rewired from
brittle exact-text matching to stable selectors, threading a full
Hamiltonian cycle through all eight of the new controls the second field
adds.

Full suite green (47 passed, 810 subtests), stable across two consecutive
runs. mypy clean on every touched Python file.

## Completion

The owner-directed prototype reached a natural stopping point after the
workspace had been exercised with two genuinely enterable fact families.
The delivered shape is a separate landing page that reads the existing
state model, links into the existing entry and explanation surfaces, and
keeps the entry UI field-keyed rather than duplicating one panel per fact.
The synthetic fixture's full suite remained green: 47 tests and 810
subtests, with mypy clean on the touched Python files. No maturity claim,
real-data exercise, or new tax logic was part of the close.
