<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "entry-loop-synthetic",
  "status": "Planned 2026-07-28, milestone 3 of Legible Entry. The first milestone in this phase that builds product. Scope settled by the owner: W-2 only, all five loop steps, synthetic workspace, no real data and no L3 claim. Usability criteria are written before the surface is built (Track 0) so the L2 claim has a scorer that was not shaped by the thing it scores. The per-field explanation schema is left to emerge from the build and is written down at close, not designed up front. Four tracks, each one build-and-review cycle. Milestone opens on one PR and closes on another; tracks keep their review gate and land on the milestone branch. Prerequisite to confirm before Track 1 writes code: that a synthetic workspace can be seeded so W-2 facts are the only thing missing, and that the surface can be served and can emit act-contribution.v1 through the existing admission path. Check it against the code, do not assume it. Amended 2026-07-29: the owner withdrew ADR-0048's entry-vehicle condition and ADR-0051 replaced it. Browser and workstation behaviour are the owner's trusted environment, not the entry surface's contract; the surface owes contribution-only entry, validated admission that fails closed, redacted failure, data-boundary behaviour, and no false claim of isolation. Open question 3 (does the viewing preflight cover an entry session) is closed, and Track 1's blocking review finding is disposed by recheck rather than by building a vehicle.",
  "retrospective": "docs/milestone-retrospectives/2026-07-29-entry-loop-synthetic.md",
  "scope": [
    "write the usability evaluation criteria for entry, and how a cell is scored against them, before any surface exists",
    "build the guided entry loop for W-2 on a synthetic workspace: know what is missing, enter a fact, see it land, correct an entered fact, know the return is complete",
    "drive entry through act-contribution.v1 on the existing admission path, per ADR-0048",
    "ship the surface through the surface artifact and build it at the workspace, per ADR-0049",
    "run the usability evaluation against the built loop and record the result",
    "record the per-field explanation shape that the build actually needed",
    "move the W-2 column of the entry-loop matrix to L2 only if the evaluation passes"
  ],
  "non_goals": [
    "no real data, no real workspace, no owner attestation, no L3 claim",
    "no 1099-INT, 1099-DIV, or taxpayer-assertion entry",
    "no filing",
    "no new tax rule and no change to any derivation package",
    "no change to artifact-package.v4",
    "no new correction-authority mechanism -- every fact type stays free",
    "no separate missing-facts screen",
    "no entry vehicle, no browser launch flag, no spellcheck control, no entry-session preflight or affirmation -- per ADR-0051"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/legible-entry/milestones/entry-loop-synthetic.md",
      "docs/phases/legible-entry/legible-entry-roadmap.md",
      "docs/adr/0048-entry-boundary.md",
      "docs/adr/0051-entry-surface-contract.md",
      "docs/adr/0049-surface-artifact.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "AGENTS.md#Data Safety Rules",
      "AGENTS.md#Fixture Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/legible-entry/milestones/entry-loop-synthetic.md",
      "docs/adr/0048-entry-boundary.md",
      "docs/adr/0051-entry-surface-contract.md",
      "docs/adr/0049-surface-artifact.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "merge_or_records": [
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ]
  }
}
-->
# Milestone: The Entry Loop (synthetic)

Status: **open.** Plan merged 2026-07-28 (PR #109, `506f785`). Track 0 closed;
Track 1 built and reviewed `NOT READY`. Its blocking finding rested on
ADR-0048's entry-vehicle condition, which the owner withdrew on 2026-07-29
(ADR-0051). Track 1 is in a scoped repair covering the two coverage findings,
plus a recheck that disposes the blocking one.

## What this is for

The owner still gets tax data into this system by editing JSON by hand, and
still finds out what is missing by reading a machine's account of it. Two
milestones have cleared the way: one decided a browser form is an acceptable
place to type a tax fact and that it must hand its work to the existing
contribution boundary rather than write anything itself, and one built the
route that gets UI code onto the machine at all.

Neither built any part of the thing a person uses. This one does.

The loop is the product here, not the form. A person opens the surface, sees
what the return is missing, types one of those facts, watches it land, fixes it
if they got it wrong, and keeps going until the return computes. The
missing-facts account is the guide through that loop, not a separate page to
reconcile against by hand — a form beside a diagnostic report is exactly the
legibility failure this phase exists to remove.

Everything here runs on synthetic data. No real return is touched and no
maturity row reaches L3 in this milestone.

## What the owner decided, 2026-07-28

**W-2 only, all five steps of the loop.** One fact family taken all the way
through rather than four families taken partway. W-2 is the simplest family and
the one with the most precedent in the system. Fifteen of the twenty matrix
cells are deliberately left for later milestones. The reasoning: a loop that
works end to end for one thing tells us whether the loop is right; a loop that
covers four families but stops before correction and completion tells us
nothing about whether a person can finish.

**The usability criteria are written before the surface is built.** A cell in
this phase reaches L2 when a usability evaluation passes, and that evaluation
does not exist yet. Writing it after the build means writing it in the shape of
whatever got built. It goes first, and the build aims at a bar someone else set.

**The per-field explanation schema is left to emerge.** The phase thesis wants
a representation of the explanation, context, and navigation each point of
entry carries. We will find that shape by building W-2 fields and seeing what
they need, and write it down at close. The last milestone's plan asserted a
shape nobody had tried and was wrong about it; the correction is to make the
claim after the attempt, not before.

## What is still open

**1. Can a synthetic workspace be arranged so W-2 is the only thing missing?**
The fifth step of the loop is "know the return is complete," and a return needs
more than a W-2. The intended answer is to seed the synthetic workspace with
every other fact already present, so the only gap the loop has to close is the
one being built. Confirm that against the code before writing any of the
surface. If it does not hold, the fifth step needs a different design and this
plan is wrong about it.

**2. What serves the page, and how does a contribution get from the browser to
the admission path?** ADR-0048 settled that the surface emits
`act-contribution.v1` rather than writing facts, and ADR-0049 settled how the
code arrives. The mechanism in between — what process is listening, what it
accepts, what it refuses — is not settled and is Track 1's to find out against
the existing code.

**3. ~~Does the viewing preflight cover an entry session?~~ Closed by
ADR-0051, 2026-07-29.** This asked what browser confinement an entry session
owes, because ADR-0048 made it a condition of entry being acceptable at all.
The owner withdrew that condition: browser and workstation behaviour are the
owner's trusted environment, not the entry surface's contract. The entry
surface owes contribution-only entry, validated admission that fails closed,
redacted failure, data-boundary behaviour, and no false claim of isolation.
Nothing here owes a preflight, a launch flag, or a spellcheck control.

**4. What does correction look like when nothing can refuse it?** Every fact
type shipped today declares `free`, so a correction on synthetic W-2 data is
always allowed. The interesting refusals of ADR-0041 cannot occur here. The
correction step is therefore about whether a person can find and change an
answered fact and understand what happened — not about refusal design. Do not
build refusal UI for a refusal that cannot fire.

## How we will answer them

### Track 0 — usability criteria for entry

Write the criteria a guided entry loop has to meet, and the procedure that
scores a cell against them. Concrete enough that two agents evaluating the same
surface would agree on most of it, and specific to entry rather than generic
usability advice — what a person must be able to tell about a field before
typing in it, what they must be able to tell after, and what "I know the return
is complete" has to look like to count.

It should also say who evaluates and how disagreement resolves. The phase's
stated method is a mix of agent viewpoints, with the owner reviewing the
criteria, the evidence, and the result. Where evaluators disagree, that
disagreement is signal, and the procedure should say what happens to it rather
than averaging it away.

The existing presentation contract (ADR-0046) is the nearest thing to prior
art: zero-authority foreclosure, blanket redaction, section-level salience.
Read it, but do not assume entry inherits it — it was written for a surface
that only displays.

This track writes no product code and scores nothing yet.

### Track 1 — build the loop for W-2

The guided loop, end to end, on a synthetic workspace:

- **know what is missing** — the surface shows the outstanding W-2 facts, as
  the guide through entry rather than a report beside it;
- **enter a fact** — fields that explain what they are asking for and why;
- **see it land** — the person can tell the fact was accepted, and what it
  changed;
- **correct an entered fact** — find an answered fact, change it, understand
  the result;
- **know the return is complete** — the loop ends somewhere definite, with a
  computed return.

Entry emits `act-contribution.v1` through the existing admission path. The
surface ships and builds by the route the last milestone established. Reuse
what exists; if something turns out not to be reusable, stop and report rather
than writing a parallel path.

Track 0's criteria are visible to this track. Building toward a known bar is
the point of writing it first.

### Track 2 — evaluate

Run Track 0's procedure against Track 1's surface and record the result,
including where evaluators disagreed. If the evaluation fails, that is a real
outcome and the milestone reports it rather than adjusting the criteria to fit.
A repair cycle is fine; rewriting the bar is not.

### Track 3 — write it down and close

Record the per-field explanation shape the build actually needed — what each
point of entry carries for explanation, context, and navigation — as a short
ADR. Then move the W-2 column of the entry-loop matrix to L2 if and only if
Track 2 passed, file the retrospective, and close.

## Not in this milestone

No real data, no real workspace, no attestation. No 1099-INT, 1099-DIV, or
taxpayer-assertion entry. No filing. No new tax rule, no change to any
derivation package, no change to `artifact-package.v4`. No new
correction-authority mechanism — every fact type stays `free`. No separate
missing-facts screen, by design.

## How we will know it is done

- A person can go from an incomplete synthetic return to a computed one by
  typing W-2 facts into the surface, without opening a text editor.
- Entry goes through `act-contribution.v1` on the existing admission path.
  Nothing in the surface writes a fact.
- An entered fact can be corrected through the surface.
- Track 0's criteria existed before Track 1's code, and Track 2 scored against
  them unchanged.
- The W-2 column moves to L2 only if that evaluation passed. If it did not, the
  column does not move and the milestone says why.
- The per-field explanation shape is written down as something observed, not
  proposed.
- The data-safety scan passes and no real workspace was involved.

## Shape of the work

Four tracks, sequential, each one build-and-review cycle. Track 0 sets the bar,
Track 1 builds, Track 2 scores, Track 3 records and closes. The milestone opens
on this PR and closes on another; tracks keep their review gate and land on the
milestone branch without their own PRs.

Plans and charters here are written for a reader who knows the product and not
the record.

## Track 3 — the entry-field contract, outcome

Charter: `docs/reviews/charter-2026-07-29-entry-loop-synthetic-track3.md`. Per
that charter, this track models the field contract rather than the
presentation surface, and does not draft an ADR (that call is the owner's).

**The model.** `packages/schemas/entry/entry-field.v1.schema.json` declares
what an entry field must state about itself: `source` (document, box, and the
box's own printed label), `destination` (return form and line), `purpose`
(the completion reason), `format` (a discriminated union keyed by `kind`, with
exactly one member today — `currency-amount`, Track 2d's accepted-format shape,
unchanged in behaviour — because a money field is the only shape this
milestone built or evaluated; see the Track 3 repair below), and `correction`
(a `kind` enum closed to one observed member, `same-field-reuse`, naming how an
answered fact is located and changed, because that is the only shape this
milestone built or observed). W-2 Box 1 is declared against it in
`w2-box1-field.js`, which composes the existing `w2-box1-format.js` rather
than duplicating it. `EntryPage.svelte` now renders its source label,
field name, and purpose sentence from that declaration
(`formatSourceLabel()`, `W2_BOX1_FIELD.source.label`,
`formatDestinationPurpose()`) instead of carrying the same words a second
time as template literals, and `entry_loop.py` loads, validates, and exposes
the same declaration at `GET /api/state` under `field_contract`.

**How much of 2.1, 2.2, 2.3 is now checkable against a declaration.**

- **2.1 (source document and box) — checkable against data.** `source.document`,
  `source.box`, and `source.label` are structured fields an evaluator (or a
  test) can read from `field_contract["w2-box1"]` without touching rendered
  text, and the schema requires all three non-empty.
- **2.2 (destination and purpose) — checkable against data, with one residue.**
  `destination.form`/`destination.line` and `purpose` are likewise structured
  and required non-empty. What is *not* mechanised is judging whether the
  purpose text actually reads as an explanation rather than filler — the
  schema can enforce presence and non-triviality (it is not literally the
  string `"required"`), but not prose quality. That residue is small compared
  to before, when an evaluator had to read the whole rendered sentence to
  decide both facts (is a destination named at all, does the purpose go
  beyond "required") that are now separately checkable as data.
- **2.3 (format stateable without guessing) — irreducibly judgement.** The
  `format` sub-object is fully mechanically checkable for *consistency* (does
  the validator accept what the hint claims — this is exactly the
  guidance/behaviour congruence gap the Track 2 owner resolution named).
  Whether the stated examples are *sufficient for a person* to state the
  format without guessing is a judgement call on the examples' content, not
  their presence — the Track 2 evaluator split on exactly this question with
  identical data in front of both evaluators. No schema field closes that; a
  human reader is irreducibly required here.

**Seam recommendation.** The load-bearing seam is `entry_loop.py` parsing a
JavaScript module by locating an `export const NAME = ` marker and JSON-decoding
the slice after it — used for `W2_BOX1_FORMAT` since Track 2d, and now for
`W2_BOX1_FIELD` too, with an added wrinkle: `W2_BOX1_FIELD`'s `format` property
is the imported `W2_BOX1_FORMAT` binding, not inline JSON, so the loader must
regex-substitute the already-parsed format spec back in before decoding the
rest. That is a second, more specific way for this seam to break (the
substitution's own pattern going stale) layered on the first (the marker
string, the JSON-decodability requirement, the exact closing-brace shape all
being convention rather than contract). Recommendation: the field contract's
canonical form should be a JSON document (an `entry-field.v1` instance,
already valid JSON as this schema requires), owned by neither side, checked
into the fixture directly (as `w2-box1-field.json`, sibling to today's `.js`).
The JS side imports it with a plain JSON module import (`import W2_BOX1_FIELD
from "./w2-box1-field.json" with { type: "json" }`, or bundled equivalently at
build time); the Python side reads it with `json.loads` and no marker, no
regex, no JS parser of any kind. This removes the parsing seam for the field
contract entirely rather than generalising it, at the cost of the `format`
sub-object needing the same treatment (a `w2-box1-format.json` alongside
today's `.js`, with the `.js` re-exporting it or being retired). Not built
here, per the charter.

**Presentation evidence, recorded (not modelled).** From
`docs/reviews/2026-07-29-entry-loop-synthetic-track2-aggregation.md` and
`...track2e-aggregation.md`:

- The accessibility row failed twice on the same element (`#w2-box1`'s focus
  indicator) for the same structural reason: Track 2c's repair modelled focus
  contrast *per background context*, not *per focusable control*, so a
  control with a strong resting boundary and no focus treatment read as
  handled without ever entering the model. A future presentation model needs
  a per-control rule, not only a per-context one.
- The evaluation harness cannot exercise Tab/Shift+Tab traversal or
  Enter/Space activation. Two evaluators across two rounds hit this
  independently; the controls are native `<button>` elements so the
  requirement is almost certainly met by construction, but that is an
  inference, not a measurement, and it is a capability gap in the instrument.
- The accessibility criterion bundles five requirements (text contrast,
  non-text contrast, landmarks, keyboard reachability, focus visibility) into
  one Pass/Fail, so one narrow miss sinks a row otherwise comfortably met.
- The criteria conflate knowledge sufficiency (judgement: does a person have
  enough information) with guidance/behaviour congruence (mechanical: does
  the system honour what its own guidance licensed) under one "without
  guessing" bar. The first evaluation round's disputed 2.3 was this
  conflation surfacing as a disagreement; the owner's resolution separated
  the two rather than picking a side.

**The two carried findings.**

1. `test_duplicate_submission_fails_closed` and
   `test_out_of_order_submission_fails_closed` pass because the kernel's
   `apply_contribution` refuses contribution-id reuse, not because
   `entry_loop.py`'s own staleness check (`contribution_act["committed_against"]
   != contents.revision`, `entry_loop.py`) does any work — nothing in the
   current suite submits a request whose `committed_against` is stale while
   its contribution id is fresh, which is the one case that isolates that
   check. It is left as-is: a coverage gap in the test suite, not an observed
   defect in behaviour, and closing it is a small, separate test-only change
   (one more adversarial-boundary test with a fresh id and a stale revision)
   with no product risk, left for whoever next touches `entry_loop.py`'s test
   suite.
2. `launchChrome()`'s orphaned-process/`mkdtemp`-directory leak on a killed
   caller is left unfixed. It is a harness reliability issue local to
   `tools/presentation_harness/`, not a defect in anything this milestone
   built or evaluated, and fixing it here would mean touching a shared tool
   outside this track's chartered unit for no benefit to the field-contract
   model. Recorded for whoever next hardens that harness.

**Least confident this generalises beyond W-2.** The `correction` shape.
W-2 Box 1's correction is trivially `same-field-reuse` because there is
exactly one field and no navigation is needed to reach it again. A fact
family with several fields, or one where the missing-facts list and the
already-answered list interleave, may need a `kind` this milestone never
built — something closer to "locate in a list, then reopen." The schema keeps
`correction.kind` closed to the one member this milestone actually observed
rather than opening it on speculation; add a member (an addition to the enum,
not a breaking change to existing declarations) the next time a field
actually needs one.

Whether this model should become a ratified ADR is, per the charter, the
owner's call and not made here.

### Track 3 repair — an honest contract, schema enforced at load time

Charter:
`docs/reviews/charter-2026-07-29-entry-loop-synthetic-track3-repair.md`,
against `docs/reviews/2026-07-29-entry-loop-synthetic-track3-review.md`
(`NOT READY`). Two blocking findings, closed:

**F1 — the schema now claims only what it covers.** `entry-field.v1`'s
`format` is a discriminated union (`$defs.format`, keyed by `kind`) with
exactly one member, `currency_amount_format`. The title and description now
say plainly that this is a money-field contract with one format variant,
extracted from W-2 Box 1, and that a checkbox, an identifier, a date, or a
choice field each need a variant this milestone has no evidence for and does
not invent. `w2-box1-format.js`'s `W2_BOX1_FORMAT` gained the literal
`"kind": "currency-amount"` tag — a non-behavioural addition; the hint,
error, and validator functions read the same named keys as before and Track
2d's format work is otherwise untouched. `correction.kind` was already a
closed JSON Schema enum (`{"enum": ["same-field-reuse"]}`); what was wrong
was the prose calling it open. The prose above and the schema's own
description now both say the same true thing: closed to the one member this
milestone observed, extended by evidence rather than spoken of as already
open. The shared core (`source`, `destination`, `purpose`, `correction`) is
unchanged, per the charter's instruction not to restructure it on
speculation from one field. **This did not make the schema refuse a
declaration for a checkbox, an identifier, a date, or a choice field — see
the Track 3 repair 2 correction below.**

**F2 — the loader now enforces the schema it publishes.** `_load_w2_box1_field`
previously hand-rolled its own presence/type checks for `source`,
`destination`, `purpose`, and `correction`, and never checked `id`,
`version`, or `additionalProperties` at all. It now parses the declaration
and calls `jsonschema.Draft202012Validator(...).is_valid(...)` against
`entry-field.v1` directly, deleting the hand-rolled checks entirely.

*Confirmed unchanged:* the served `field_contract` still validates against
the amended `entry-field.v1`, and every failure path still raises only a
generic `entry-field-unavailable` or `entry-format-unavailable` with no
rejected declaration or value in the message, exactly as before. **The
claimed regression coverage for this finding, and the separate
format-equality claim below it, were both wrong — see the Track 3 repair 2
correction.**

**F3 — rendered derivation, proven, not just inspected.** Attempted and
landed. `tests.test_entry_loop_t1.RenderedFieldDerivation` copies the real
surface content, mutates `w2-box1-field.js`'s `source.box`, `source.label`,
`destination.line`, and `purpose` to distinct synthetic strings, builds it
with the same offline `node build.mjs` the surface actually ships with,
serves the compiled output through the real running entry-loop server, and
drives it with a Chrome-based probe
(`tests/helpers/entry_loop_field_derivation_client.mjs`) that asserts the
mutated text reached the DOM and the original text did not. This is gated
the same way `CompiledClientIntegration` already is (needs Node, a local
Chrome/Chromium, and the vendored dependency tree) and is not a new,
separately-skipping path — it runs whenever that existing test does, and did
on the machine of record.

**F4 — the seam was not widened further.** `_load_w2_box1_field` still uses
the same `export const` marker plus one regex substitution it did before this
repair; nothing was added to parse `format`'s new `"kind"` key specially (it
travels through the same substitution as every other format key, since
`format_spec` is loaded and injected as one dict). The seam recommendation in
this document stands unchanged and unbuilt, per the charter.

No owner decision was required to close F1 or F2 — both were narrowing moves
the charter authorized directly (state the true scope; enforce the schema
that is already published), not widenings that would need one. Nothing here
draws a maturity conclusion, amends the criteria document, or fixes the
accessibility defect; the W-2 cell verdict stays FAIL, unchanged from Track
2.

### Track 3 repair 2 — delete two false claims, add nothing

Charter:
`docs/reviews/charter-2026-07-29-entry-loop-synthetic-track3-repair-2.md`,
against `docs/reviews/2026-07-29-entry-loop-synthetic-track3-repair-review.md`
(`NOT READY`). Both findings close by deleting something. Confirmed still
holding from that review and left untouched: the `oneOf` discriminator, the
load-time schema validation and the deletion of the hand-rolled checks, the
F3 derivation test, and the Track 2d format regressions.

**F1, corrected — the schema's actual boundary.** The discriminator is real
(an unknown `kind` is rejected, adding a second variant is additive), but the
prior repair's record overstated what it does. `entry-field.v1` validates
that a declaration is **well-formed** and that its `format` names a
**supported variant**. It does **not** verify that the declared format is
the *correct* one for the field's own `source`/`destination` — nothing in
the schema relates `format.kind` to either. A declaration for the W-2 Box 13
checkbox, an employer name/EIN, a date, or a filing-status choice validates
unchanged as long as it still carries the ten-key `currency-amount` object;
that is a **false declaration, not a malformed one**, and no schema of this
shape can catch a lie about its own subject. Nothing in this milestone
catches that lie either — it would take a person reading the rendered field
against the document it claims to describe, which is evaluation, not a
mechanical check. This is now stated directly in the schema's own
`description` and in `$defs.format`'s, rather than left for a reader to
infer, and `tests.test_entry_loop_t1.FieldContract.test_schema_does_not_relate_format_to_source_or_destination`
reproduces the reviewer's four non-money declarations and confirms all four
still validate. No semantic discriminator was added; there is no evidence
for the value-type taxonomy one would need, and inventing it now would be
the same premature generalisation the owner has already declined twice in
this milestone.

**F2, corrected — two vacuous tests, and a tautology deleted.**

*The fixtures never reached validation.* `_write_field_declaration` wrote
`..., "format": W2_BOX1_FORMAT};\n`, but the loader's closing-marker search
requires `"\n};\n"` — a newline before the brace. A compact single-line JSON
body followed directly by `};\n` never matches, so every case using that
helper raised `entry-field-unavailable` at the marker step, before schema
validation ever ran, and would still have passed with schema validation
deleted outright. The helper also wrote no schema file at the temporary
root, a second, independent way to pass for the wrong reason. Both are
fixed: the helper now closes the object literal on its own line (matching
the real file's shape) and copies the real `entry-field.v1.schema.json` into
the temporary root before the loader ever runs.

*Proof each repaired case now bites:* with `_entry_field_validator` patched
to return an always-valid stub (not committed; a manual check performed for
this report), all three subcases of
`test_loader_now_rejects_what_the_schema_rejects` (missing `id` with a bad
`version`, an unrecognized top-level key, an unrecognized `correction.kind`)
failed as expected — proving the test now depends on schema validation
actually running, not on an earlier, unrelated parse failure. With schema
validation restored, all three pass again.

*The equality check was a tautology, and is deleted.* `_load_w2_box1_field`
substitutes the caller-supplied `format_spec` into the declaration's only
accepted `"format": W2_BOX1_FORMAT` expression, then the deleted check
compared the resulting value to that same `format_spec`. Equality was
necessarily true on every declaration this function could successfully
parse — a literally different format failed earlier, at the regex-count
guard, for a parsing reason, never for the documented runtime reason. No
non-tautological residue survived inspection: there is no path by which
`contract["format"]` can come from anywhere other than the substitution
itself, so there was nothing left to keep or test. The check, its test
(`test_loader_still_refuses_a_schema_valid_but_different_format`), and the
milestone record's claim about it are all deleted, per the charter's
instruction not to contrive a code path that makes the check false.

**Condition attached to the seam recommendation.** The marker-and-regex seam
*structurally guarantees* the property the deleted check was trying to
verify — the field's declared format and the runtime's own format cannot
disagree, because the loader writes the runtime's own format into the only
place the parser will accept one. That guarantee is a property of this seam
specifically, and it disappears the moment the seam recommendation's
canonical-JSON migration happens: once the field's `format` is parsed from
its own independent JSON rather than substituted in from the side, a real
equality (or inequality) becomes possible again, and a genuine check belongs
there. Whoever performs that migration should add one; its absence today is
not evidence that none is needed later.

**Tempted to add, and did not:** a semantic discriminator relating
`format.kind` to `source`/`destination` (no evidence for the shape it would
need); a contrived non-tautological variant of the deleted equality check
(would have been a code path built to make a check pass, not a real
guarantee); and a note in the schema enumerating exactly which fields are
"safe" to declare (that list does not exist independently of the evaluation
this milestone already runs).

No owner decision was required for either finding: both closed by removing a
false claim the charter had already identified precisely, not by choosing
among design options. Nothing here draws a maturity conclusion, amends the
criteria document, fixes the accessibility defect, or widens the seam; the
W-2 cell verdict stays FAIL, unchanged from Track 2.

## Track 4 — focus indicators, stated per control

Charter: `docs/reviews/charter-2026-07-29-entry-loop-synthetic-track4-focus.md`,
against `docs/reviews/2026-07-29-entry-loop-synthetic-track2e-aggregation.md`
(cell FAIL, the accessibility row failing twice on `#w2-box1`'s missing
focus indicator). **No review gate**; the full record is the commit message.
This section is a short pointer to it, not a duplicate.

**The rule, stated once and made to hold.** The existing global
`:global(button:focus-visible), :global(input:focus-visible),
:global(a:focus-visible), :global([tabindex="-1"]:focus-visible)` rule
already named every focusable control by element type, not by ID — the model
was already per-control in that sense. What made it fail on `#w2-box1` was a
Svelte scoped-style specificity tie: the input's own resting
`outline: 0; box-shadow: 0 0 0 2px #fffdf8;` rule compiles to the same
specificity as the `:global(...)` focus rule, and the later rule in the
stylesheet wins a tie — which was the input's own resting rule, not the
focus rule. Fixed with `!important` on the focus rule's `outline` and
`box-shadow`, which wins regardless of a control's own resting declarations
or where they sit in the file, so a control added later inherits the
guarantee without anyone needing to notice the ordering risk.

**Six focusable controls found**, confirmed by real Tab traversal through
the compiled page in both the incomplete and complete states (the sweep
finds nothing further; wrapping back to the wordmark closes the loop): the
wordmark link, `Enter this fact`, `#w2-box1`, the submit button (`Add`/
`Update W-2 Box 1`, same element), `Correct this fact`, and
`Review W-2 Box 1`. The `tabindex="-1"` status-card live region is not among
them — it is not part of the Tab order (browsers exclude `tabindex="-1"`
from sequential navigation) and is reached only programmatically after a
submission, so it is a live region, not a control.

**Measured, before and after, for `#w2-box1`:** before, resting and focus
were the same style — `box-shadow: 0 0 0 2px #fffdf8`, computing to
**1.02:1** against the white field, per the evaluators. After, focus adds
`box-shadow: 0 0 0 5px #17251f !important`, computing to **15.90:1** against
the entry-panel card background, live-measured via a real keyboard Tab in a
built, served page. Every other control's dark ring measured 13.85–15.64:1
against its own adjacent background (main, the missing section, the
answered strip); all were already distinct from their (ring-less) resting
states, unchanged by this fix. `Review W-2 Box 1`'s two-tone ring is
untouched and unchased, exactly as the charter directed: its light
component still measures ~7.59:1 against the dark-green review section
(passing), its dark outer component still ~2.06:1 (the aesthetic edge the
foreman already resolved as a legitimate treatment, not a missing
indicator).

**One durable, non-snapshot test.** `tests.test_entry_loop_t1.FocusIndicators`
enumerates every focusable control from the real, compiled, Tab-driven page
and asserts one general invariant per control — focus style differs from
resting style, and some component of the focus indicator measures at least
3:1 against its live adjacent background — computed from actual rendered
colours every run, never against a stored value. Verified to fail
specifically on `#w2-box1` when the `!important` fix is reverted (confirmed
by hand before committing), and verified to keep passing after a palette
change that swaps the ring colour for a different, still-dark one (also
confirmed by hand, not committed). No per-control or per-colour assertion
was added.

**Surface metadata regenerated:** 943 entries, **5,085,046 bytes** (up from
5,083,946 before this track — the CSS comment plus three `!important`
declarations account for the difference). Manifest, registry, release, and
adoption pins all recomputed and agree. New starting-state fingerprint for
any future re-score: `sha256:ac7735a5d9ab4e057e193966aec89df7534e478ee329e47e9f7b8b19018b79e8`
(superseding `sha256:212e525d…`).

No maturity movement: the W-2 cell verdict stays FAIL and the cell stays at
L1 — this track repaired the one outstanding defect but did not re-score,
and the charter directed that repairing the defect after the fact does not
move the cell. No criteria-document change, no second fact family, no ADR.
