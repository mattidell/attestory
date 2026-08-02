# Retrospective — The Entry Loop (synthetic)

Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-loop-synthetic.md`
Phase: Legible Entry. Third milestone of the phase; the first that builds
product.
Closed: 2026-07-29.

## What it produced

A guided W-2 entry loop on a synthetic workspace: a person can see what is
missing, type a fact, watch it land, correct it, and see the return computed
— through `act-contribution.v1` on the existing admission path, never
writing a fact directly. Usability criteria were written and owner-accepted
before any surface existed
(`docs/phases/legible-entry/entry-usability-criteria.md`), and two
independent rounds of two-evaluator scoring ran against the built loop
without amendment.

The second round returned FAIL, on the accessibility row: the amount
input's focus indicator measured 1.02:1 against a required 3:1, the same
element and the same underlying gap that survived a first repair aimed at
the wrong layer. **The W-2 cell stays at L1.** A later track repaired the
defect, but nothing re-scored the surface afterward, so the failure stands
as the reported outcome — the milestone's discipline is to report a failed
evaluation rather than treat a repair as a retroactive pass.

The durable deliverable is not the surface. It is `entry-field.v1`
(`packages/schemas/entry/entry-field.v1.schema.json`): what an entry field
must declare about itself — source document and box, return destination,
purpose, an accepted-format variant, and a correction affordance —
extracted from the one W-2 Box 1 field this milestone built. The surface
may well be thrown away; the contract is meant to survive it.

## What actually happened

### The criteria document held under pressure

It was written before the surface existed, specifically so the evaluation
would not be shaped by the thing it scored. It was then scored twice,
unchanged, and found something real both times: a genuine `90,000`-comma
guidance/behaviour gap in the first round (resolved for the evaluator who
found it, on reasoning neither evaluator argued), and the focus-indicator
defect in the second, on the same element, twice. Charters across two
repair rounds were explicitly forbidden from amending it, and none did. That
restraint, held under real pressure from a document that kept finding
problems, is the strongest evidence this milestone produced about method
rather than product.

### Three rejections in Track 3, all correct, all the same shape

Track 3 modelled the entry-field contract and was sent back twice before it
was honest. Every rejection had the same shape: the build added machinery
that asserted something that was not true.

1. A format discriminator that did not discriminate: `entry-field.v1`
   validated that a declaration was well-formed and named a *supported*
   format variant, but related nothing about `format.kind` to the field's
   own `source`/`destination` — so a declaration for an employer name, a
   checkbox, a date, or a filing-status choice validated unchanged as long
   as it still carried the ten-key currency-amount object. Closed by
   stating the true, narrower boundary, not by inventing a semantic
   discriminator with no evidence behind it.
2. Regression tests that never reached the code they claimed to guard: a
   test fixture's closing-marker text didn't match the loader's parser, so
   every case failed at the parse step before schema validation ever ran —
   and would have kept "passing" with schema validation deleted outright.
   Closed by fixing the fixture and then proving each case now bites: a
   temporary stub that always validates was patched in and the tests were
   confirmed to fail against it, before being confirmed to pass again with
   real validation restored.
3. An equality check that could not be false: the loader substituted its
   own format spec into the only slot its parser accepts, then compared the
   result to that same spec — necessarily true on every declaration it
   could parse. Closed by deleting the check and the claim, after
   confirming no non-tautological residue existed to keep.

All three closed by **subtracting** — deleting a false claim or an inert
mechanism — not by adding a new layer to compensate. Name the pattern
because it will recur: the natural response to "this claim is false" is to
add something that makes it true, and the right response, at least twice
running here, was to say the narrower true thing instead.

### Two vacuous-test failures, one caught by a reviewer and one by the foreman

Both are the identical shape: **a test that fails earlier than the thing it
is probing tells you nothing.** The Track 3 F2 regression fixtures failed at
a marker-parsing step before the schema validator they claimed to exercise
ever ran — caught by the reviewer. The Track 4 focus-indicator test,
mutation-tested by reverting the fix, failed at the surface's own checksum
gate (`SURFACE_ENTRY_CHECKSUM_MISMATCH`) before it ever measured a pixel —
caught by the foreman's own inspection, one build later.

The operational consequence, stated so it does not have to be rediscovered
a third time: **a content-tree mutation on this surface must be followed by
`python3 -m tools.generate_entry_loop_t1_fixtures` before the result means
anything.** Without it, the checksum gate answers first, and every
mutation test — valid or not — fails (or trivially "passes," if the probe
happens to interpret the refusal as absence of coverage) for a reason that
has nothing to do with what is being tested.

### The foreman's own two defects

`milestone_state` was set to `track-2e` during the second evaluation round.
`tools/foreman_context.py` accepts only `track-<digits>` and refused to
render for both Track 2e evaluators, who correctly declined to infer scope
from the failure and continued under their charters rather than treating
the refusal as license to guess. No evidence in either evaluator's file
appears to have been affected, but the tool a role depends on was broken by
the foreman, not by the tool.

Separately, the Track 4 charter's root-cause diagnosis was wrong. It
attributed the missing focus indicator to a model that was per-background-
context rather than per-control. The actual cause, found by the builder and
confirmed on inspection, was a Svelte scoped-style specificity tie: a
component-scoped `input { outline: 0; ... }` rule compiles to the same CSS
specificity as the global `:focus-visible` selector, and a tie is broken by
source order — the input's own resting rule sat later in the file and won.
The charter's *prescription* (state the rule once, per control, so a future
control inherits it) was still right, and the fix followed it. The
*reasoning* that produced the prescription was mistaken, and the inspection
corrected it rather than letting a wrong diagnosis stand next to a right
fix.

**Both are instances of the same recurring pattern this project has now
named three times: phase-state (or its close analogue, a charter's own
diagnosis) drifting from what the code actually does.** It is not a
one-person lapse; it is a structural risk of writing prose about a system
state that the prose does not mechanically check against.

## What worked

**The evaluation procedure's dispute rule did its job.** Two evaluators
split on criterion 2.3 in round one — one scored the format hint sufficient,
one typed a plausible-looking `90,000` and got refused. The procedure
escalated the disputed judgement to the owner rather than averaging it away,
and the owner's resolution (the hint states enough for 2.3 to pass; the
`90,000` refusal is a separate, mechanical guidance/behaviour defect,
fixed) drew a distinction neither evaluator had argued for. That is the
procedure working as designed: disagreement as signal, not noise.

**Repairs closed by removing, not by adding**, three times running in Track
3 — see above. Every attempt to compensate for a false claim by building
more validation around it would have made the record more elaborate and no
more honest.

**Real measurement over inference, both times accessibility was at issue.**
The Track 4 fix was verified by driving a real keyboard Tab through a real
compiled, served page and computing WCAG contrast from live rendered
colours — not by reading CSS and reasoning about what should happen. The
same discipline caught the Svelte specificity tie in the first place: the
evaluators measured computed `outline-style`/`outline-width`, not the
source, which is what found `outline-style: none, outline-width: 0px`
instead of a plausible-looking rule that silently did not apply.

## What to carry forward

Recorded in the milestone plan under each track's outcome, not scheduled
here as new work:

- **The evaluation harness cannot measure keyboard operability.** Four
  evaluators across two rounds could not verify Tab/Shift+Tab traversal or
  Enter/Space activation through the harness. The foreman resolved it at
  source level (every control is a native `<button>`, so this holds by
  construction), but an evaluator was not permitted to do that, and a
  mechanical criterion has now gone partly unverified twice. This is the
  most important instrument gap to close before the next evaluation.
- **The accessibility row bundles five requirements into one Pass/Fail** —
  text contrast, non-text contrast, landmarks, keyboard reachability, focus
  visibility — so one narrow miss sinks a row otherwise comfortably met. A
  future criteria revision should split it.
- **Criterion 2.3's "without guessing" bar conflates two things**:
  knowledge sufficiency (judgement) and guidance/behaviour congruence
  (mechanical). The first round's dispute was this conflation surfacing as
  a disagreement. Noted, not amended — the criteria document is fixed for
  this milestone's evaluations.
- **The substitution seam's guarantee is untested and about to expire.**
  `entry_loop.py` reads a JS `export const` by string-marker indexing plus
  one regex substitution, refusing when the match count isn't exactly one.
  That refusal is the entire reason the served field format cannot diverge
  from the runtime's own — a structural guarantee of this seam, not a
  tested property of it, and one that disappears the moment the seam
  recommendation's canonical-JSON migration happens, at which point a real
  equality constraint becomes necessary rather than moot. Whoever performs
  that migration should add one.
- **`entry-field.v1` is evidenced by exactly one field.** Whether `source`,
  `destination`, `purpose`, and `correction` survive as a shared core once a
  second fact family exists is unknown. The schema checks well-formedness
  and that `format` names a supported variant; it does not and cannot check
  that the variant is *correct* for the named source — a declaration for an
  employer that claims a currency format is a false declaration, not a
  malformed one, and nothing here catches that lie.
- **Two smaller carried findings**, both already recorded and neither
  blocking: the kernel's `apply_contribution` refusing contribution-id
  reuse masks whether `entry_loop.py`'s own staleness check does any work,
  since no test isolates it; `launchChrome()` leaves an orphaned process
  and a `mkdtemp` profile directory if the calling process is killed on
  timeout.

## Process notes

**One PR opened the milestone, this one closes it.** Four tracks and two
repair rounds landed as branch commits with their own review gates (Track 4
had none, by owner decision, with a foreman inspection standing in); no
track took its own PR, matching the project's two-PR-per-milestone shape.

**Two ADRs, ADR-0049 and ADR-0051, arrive at this close still `proposed`,**
carrying five tracks of dependent work. Both held under everything this
milestone threw at them — a real interactive page rebuilt through the
surface-artifact container across every content change, and the full
contribution-only/validated-admission/redacted-failure/data-boundary
contract exercised by two evaluation rounds and repeated adversarial
testing. Neither needed amendment; both are the owner's to ratify at this
close.

**Nine build-adjacent units**, roughly: Track 0 plus its repair, Track 1
plus its repair, Track 2 (two evaluator pairs, 2 and 2e), Track 3 plus two
repair rounds, Track 4. Three of those nine exist only because a prior
round's claim did not hold under review — the same ratio of correction to
forward progress this phase's other milestones have shown, and worth
naming rather than treating as unusual.
