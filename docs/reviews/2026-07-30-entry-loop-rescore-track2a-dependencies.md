# Track 2a — Run-dependency re-confirmation

Charter: `docs/reviews/charter-2026-07-30-entry-loop-rescore-track2a.md`.
Branch: `track/entry-loop-rescore-track2a`, from `main-ui` at `10af67ac37`
(Track 1 merged). This is a factual re-confirmation, not a build and not a
score. No surface behaviour was changed to produce it.

The Scoring Procedure in
`docs/phases/legible-entry/entry-usability-criteria.md#scoring-procedure`
names four dependencies and states plainly that naming them does not confirm
them. Each is re-checked below against the current surface — the one carrying
Milestone 3's Track 4 focus-indicator repair and this milestone's Track 1
keyboard-operability probe.

## Dependency 1 — synthetic workspace: W-2 is the only missing family

**Claim:** a synthetic workspace can be seeded with every required non-W-2
fact, so W-2 is the only missing family.

**Test named for it:**
`tests/test_entry_loop_t1.py::PhaseADependencies::test_dependency_1_w2_is_the_only_prompt_and_entry_reaches_complete`.

**What the test actually asserts (read, not assumed from the name):** it
takes the runtime's initial snapshot and asserts `missing` is a list with
*exactly one* entry — `w2-box1` — and nothing else; that `complete` is
`False` before entry; and that after entering the W-2 Box 1 fact, `missing`
becomes `[]`, `answered` has exactly one member, `computed` and `complete`
are both `True`. This is a direct check of the claim: if any other fact
family were still missing, the seeded workspace's `missing` list would carry
more than the one W-2 entry, and the test would fail on the first assertion.

**Evidence run:**
```
python3 -m pytest tests/test_entry_loop_t1.py -k "PhaseADependencies" -v
```
Result: 4 passed (all four dependency tests; this one included).

**Status: CONFIRMED.**

## Dependency 2 — the surface can be served and can admit contributions

**Claim:** the entry surface can be served at a URL and can send
contributions through the admission path.

**Test named for it:**
`tests/test_entry_loop_t1.py::PhaseADependencies::test_dependency_2_loopback_post_uses_admitted_contribution_acts`.

**What the test actually asserts:** it starts a real `EntryLoopServer`,
performs a real HTTP `GET` on the served root (asserts `200`), a real `GET`
on `/api/state`, and a real `POST` to `/api/contributions` carrying a W-2 Box
1 value; it asserts the response reports `complete: True`; then it reads the
act log directly and asserts the last three acts are exactly
`["contribution", "member-transition", "assertion"]`, that the first is a
`contribution.v1` payload, and that the `member-transition` act's finding
references that same contribution's id. This does not merely check "no
exception" — it inspects the admitted act *kinds* and the linkage between
them, which is the actual admission path, not just an HTTP 200.

**Evidence run:** same command as above; this test is one of the 4 that
passed.

**Status: CONFIRMED.**

## Dependency 3 — fixed W-2 evaluation sets and zero-missing/fully-computed state are observable

**Claim:** the surface makes the fixed W-2 evaluation sets and the
zero-missing, fully-computed state observable.

**Test named for it:**
`tests/test_entry_loop_t1.py::PhaseADependencies::test_dependency_3_fixed_sets_and_completion_are_observable`.

**What the test actually asserts:** it takes the initial snapshot and
asserts the set of line ids present in `state.lines` equals exactly
`EXPECTED_IMPACT_LINES + COMPARISON_LINES` (`packages/derivation/entry_loop.py`
defines these as `("1a", "9", "11", "15", "16")` and `("2b", "3a", "3b",
"12")`, which are byte-identical to the fixed sets named in
`entry-usability-criteria.md`: Form 1040 lines 1a, 9, 11, 15, 16 for expected
impact and 2b, 3a, 3b, 12 for the untouched comparison set). After entry, it
asserts `missing == []`, `complete is True`, and every line in `state.lines`
has `computed is True`. This checks both halves of the claim: the fixed sets
are the exact vocabulary surfaced, and the zero-missing/fully-computed state
is directly readable off the snapshot.

**Evidence run:** same command; this test passed.

**Status: CONFIRMED.**

## Dependency 4 — entry and correction move exactly the fixed set

**Claim:** the evaluation fixture makes every expected-impact member change
when the fixture's W-2 Box 1 value is entered or corrected, and leaves every
untouched comparison member unchanged.

**Test named for it:**
`tests/test_entry_loop_t1.py::PhaseADependencies::test_dependency_4_entry_and_correction_move_exactly_the_fixed_set`.

**What the test actually asserts:** it enters the fixture's Box 1 figure,
then corrects it, and for *both* the entered and corrected snapshots asserts
(a) the set of expected-impact lines whose `change` field equals `"changed"`
is exactly the full expected-impact set, (b) the set of untouched-comparison
lines whose `change` field equals `"unchanged"` is exactly the full
comparison set, (c) each expected-impact line's numeric `value` differs
between the entered and corrected snapshots, and (d) each comparison line's
`value` is identical between them. This is the strongest of the four tests
against its name: it checks both the labelled `change` status and the actual
`value` movement (or non-movement), for both the first entry and the
correction, so a surface that mislabelled a line's status without actually
moving its value — or vice versa — would fail it.

**Evidence run:** same command; this test passed.

**Status: CONFIRMED.**

## Summary

| # | Dependency | Test | Status |
| - | - | - | - |
| 1 | W-2 is the only missing family | `test_dependency_1_*` | CONFIRMED |
| 2 | Surface served + admits contributions | `test_dependency_2_*` | CONFIRMED |
| 3 | Fixed sets + complete state observable | `test_dependency_3_*` | CONFIRMED |
| 4 | Entry/correction move exactly the fixed set | `test_dependency_4_*` | CONFIRMED |

Each test's assertions were read in full (not inferred from its name) and
each one exercises the code path it claims to guard through a real runtime,
a real HTTP round-trip, or a real snapshot/line-state comparison — none of
them assert only "no exception was raised." Re-run alongside the rest of
`tests/test_entry_loop_t1.py` (40 tests, 774 subtests, all passed — see the
quartet section of the Track 2a build report) to confirm nothing else in the
current surface state (Milestone 3 Track 4's focus-indicator repair, this
milestone's Track 1 keyboard-operability probe) disturbed them.

**All four dependencies hold against the current surface. The evaluation is
runnable.**

## Evaluation launch materials

For briefing Evaluators E and F identically. Command:

```
python3 -m packages.derivation.runners.entry_loop_evaluation
```

The launcher seeds a fresh temporary synthetic workspace, builds the entry
surface, starts a loopback server, and blocks (`Ctrl-C` to stop; re-run for a
clean restart). It prints exactly this shape (values below are one real run's
output; the fingerprint and the URL's random port/token change on every
run — that is expected and does not indicate a different surface):

```
Synthetic W-2 entry evaluation
URL: http://127.0.0.1:60483/entry/ZAGx_nry8rBLuiw_fizaesX3Qa2TfPfRA-7f0I3XcJg/index.html
Evidence pack: docs/phases/legible-entry/entry-loop-synthetic-evidence-pack.md
W-2 Box 1 figure to enter: 90000
W-2 Box 1 corrected figure: 91000
Starting-state fingerprint: sha256:ac7735a5d9ab4e057e193966aec89df7534e478ee329e47e9f7b8b19018b79e8
Stop: press Ctrl-C in this terminal.
Clean restart: stop this command, then run the same command again.
```

- **Synthetic W-2 Box 1 first-entry figure:** printed as `W-2 Box 1 figure to
  enter` — sourced from
  `packages/sample_data/entry_loop_t1/evaluation-w2.json`'s
  `entries.initial.box1` (`90000` at this commit).
- **Corrected figure:** printed as `W-2 Box 1 corrected figure` — the same
  fixture's `entries.correction.box1` (`91000` at this commit).
- **Starting-state fingerprint:** printed as `Starting-state fingerprint` — a
  sha256 over the canonicalized initial entry-snapshot payload (contribution
  template stripped), the evaluation fixture, and every file byte in the
  freshly built `dist/` tree. Each evaluator's own run will print a different
  fingerprint (fresh temp workspace, fresh build, fresh port/token each
  launch); the fingerprint's purpose is for each evaluator to record *their
  own* run's value in their transcript, not to match a fixed constant across
  runs.
- Each evaluator gets their own process/run of the same command; two
  evaluators must not share one running instance, since a submitted
  contribution from one would advance the `complete` state the other sees.

**Evidence pack vs. launcher — drift check:** read
`docs/phases/legible-entry/entry-loop-synthetic-evidence-pack.md` against the
launcher's actual source
(`packages/derivation/runners/entry_loop_evaluation.py`) and the fixture it
reads (`packages/sample_data/entry_loop_t1/evaluation-w2.json`):

- The pack tells evaluators to use "the W-2 Box 1 figure printed by the
  launcher" and "the corrected W-2 Box 1 figure printed by the launcher" and
  "the starting-state fingerprint printed by the launcher" — it does not
  hardcode any of the three values itself, so there is no value for these to
  drift from; confirmed by running the launcher above and reading its prints
  against the pack's instructions.
- The pack's "Document: Synthetic Form W-2 from Demo Workshop" matches the
  fixture's own `"document"` field exactly.
- The pack's relative link to the "committed synthetic source record"
  (`../../../packages/sample_data/entry_loop_t1/evaluation-w2.json`, from
  `docs/phases/legible-entry/`) resolves to the real fixture file.
- The pack's criterion score-sheet table lists exactly 20 rows: the 15
  numbered criteria (1.1–5.3) plus the 5 carried-over ADR-0046 rows, matching
  `entry-usability-criteria.md` row-for-row with no addition or omission.
- The fixture's `expected_impact_lines` (`1a`, `9`, `11`, `15`, `16`) and
  `untouched_comparison_lines` (`2b`, `3a`, `3b`, `12`) are byte-identical to
  the criteria document's fixed W-2 evaluation sets and to
  `packages/derivation/entry_loop.py`'s `EXPECTED_IMPACT_LINES` /
  `COMPARISON_LINES` constants that the runtime actually evaluates against.

**No drift found. The evidence pack matches what the launcher actually
emits.**

## What an evaluator will see (factual, not evaluative)

This section states what exists on the surface at launch and what states it
can be in. It does not score, judge, or characterize any of it.

**Controls present, in page order:**

1. A wordmark link (`attestory`, `href="./index.html"`, `aria-label="Attestory
   entry home"`) in the page header.
2. Conditionally, in the "missing" section (present only while `w2-box1` is
   unanswered): a button labelled "Enter this fact" that moves keyboard focus
   to the amount input.
3. A form labelled `aria-label="W-2 Box 1 entry"` containing:
   - a text input, `id="w2-box1"`, `inputmode="decimal"`, `required`,
     `aria-describedby` pointing at the purpose text and the format-hint
     text beside it;
   - a submit button, labelled "Add W-2 Box 1" before any entry exists or
     "Update W-2 Box 1" once an entry exists (or "Checking…" while a request
     is in flight, during which it is `disabled`).
4. Conditionally, once a fact has been answered: a text button labelled
   "Correct this fact" that moves keyboard focus back to the amount input.
5. Conditionally, only when `complete` is true: a "Review W-2 Box 1" button
   in a review section, which also moves focus to the amount input.

**Landmarks:** one `<main>` element (class toggles `complete` when the state
is complete); the entry form itself is a named form landmark via
`aria-label="W-2 Box 1 entry"`.

**States the surface can be in:**

- **Loading:** before the first `GET /api/state` resolves, an
  `aria-live="polite"` region reads "Loading the synthetic return…" or, on a
  load failure, "The entry session is unavailable."
- **Incomplete / one fact missing:** the status card reads "1 missing fact ·
  W-2 Box 1"; the missing-facts section lists that one item with its label,
  document, and box, each paired with an "Enter this fact" control; the
  entry form is present and unanswered (no "Answered fact" block, no
  "Correct this fact" control); the impact panel's expected-impact lines show
  `"Waiting for W-2"` where a computed value would go, and the untouched
  comparison lines show their standing values; there is no review section.
- **Entry accepted (first submission):** the status card gains an "Accepted.
  The entry landed through a contribution." line; the missing-facts section
  disappears; an "Answered fact" block appears with the entered value and a
  "Correct this fact" control; every expected-impact line shows `change:
  "changed"` and a computed value, every comparison line shows `change:
  "unchanged"`; the status card reads "0 missing facts · fully computed"; a
  review section appears with a "Review W-2 Box 1" button.
- **Correction accepted:** same shape as "entry accepted," with the status
  card's accepted line reading "The correction landed through a
  contribution" and the expected-impact values reflecting the corrected
  figure.
- **Rejected submission (malformed input):** a `role="alert"` error block
  appears reading "Check this entry." plus a message; the rejected value
  itself is never echoed into that text; the state (revision, `complete`,
  `missing`) does not advance.

**Visual/CSS facts observable without judgement:** every focusable element
(`button`, `input`, `a`, `[tabindex="-1"]`) carries one `:focus-visible` rule
(`outline: 2px solid #fffdf8` plus a 5px `box-shadow` ring, both
`!important`); minimum touch target height on buttons is declared at `44px`.

This is a description of what exists, not a claim that any criterion is
satisfied by it — that determination belongs to Evaluators E and F under the
Scoring Procedure, which this track does not run.
