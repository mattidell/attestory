# Review — Re-score the Entry Loop, Track 1: keyboard operability

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-30-entry-loop-rescore-track1-review.md`
- Build charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-30-entry-loop-rescore-track1.md`
- Branch: `track/entry-loop-rescore-track1`, base `main-ui` @ `8d903f6`
- Under review: `b261aae` — 2 files, 597 insertions

## Orientation and review object

`python3 tools/build_orientation_block.py --ref HEAD` resolved reviewer at
`09082d14030fc836d8d3b28503b77ba0a022b101`, matching `git rev-parse HEAD`.
`main-ui` carries one commit past the build's stated base (`09082d1`, the
charter-filing commit that made this review possible) plus the build commit
`b261aae` itself; the reviewed diff is `8d903f6..b261aae`, exactly the two
files the charter names.

## Verdict: NOT READY

The probe's activation-by-effect and vacuous-pass properties hold up under
independent, adversarial testing, and both demonstration tests genuinely bite
for the stated reason. But the reverse-traversal check does not verify what
the milestone plan and the charter both explicitly ask for: that Shift+Tab
"returns through the same set **in reverse order**." The implementation
checks only set membership (`forwardOnly`/`backwardOnly`), and I constructed
a concrete case, against the real unmodified surface, where the recorded
backward order is not the reverse of the forward order and `matches` is still
`true`. That is a real, uncaught gap relative to the track's own stated
requirement, not a matter of interpretation.

## Findings

### Blocking

**F1. The reverse-traversal check verifies set membership, not order, contrary to the milestone's explicit requirement.**

`docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-loop-rescore.md` Track 1 states:
"Shift+Tab from the last focusable control returns through the same set in
reverse order, with no control reachable forward but not backward." The
charter repeats this almost verbatim as the second thing to verify. The
implementation in `entry_loop_keyboard_operability_client.mjs`
(`reverseTraversalCheck`) computes only:

```js
matches: forwardOnly.length === 0 && backwardOnly.length === 0,
```

I ran the unmodified probe against the real compiled surface and captured the
raw `forward`/`backward` arrays directly (not through the test's own
assertions, which never inspect order):

```
incomplete forward:  [wordmark, "Enter this fact", w2-box1 input, "Add W-2 Box 1"]
incomplete backward: [w2-box1 input, "Enter this fact", wordmark, "Add W-2 Box 1"]
```

`backward` reversed is `["Add W-2 Box 1", wordmark, "Enter this fact",
w2-box1 input]`, which is not `forward`. In this instance the discrepancy is
explained by a harmless artifact — `collectOrder`'s backward pass is seeded
by focusing `forward[forward.length - 1]` and then pressing Shift+Tab, so the
walk wraps around the whole tab cycle and re-records the starting control
(`"Add W-2 Box 1"`) a second time at the tail of `backward`, once the true
reverse walk (`[input, "Enter this fact", wordmark]`) is exhausted. Excluding
that wraparound entry, the order genuinely is correct here.

That the current surface happens to pass an order check is exactly the
problem: the code does not perform one. `matches` is computed from set
differences alone, so a defect that visits the *same set* of controls in a
scrambled order — for example, a custom keyboard handler that reassigns
focus out of native tab sequence while still landing on every control
eventually — would report `matches: true`, `forwardOnly: []`,
`backwardOnly: []`, with no finding at all. The charter asked me to determine
whether this gap is real and, if so, whether set membership alone satisfies
the criterion. My conclusion: it does not. Order matters to the underlying
accessibility requirement (a keyboard user expects Shift+Tab to retrace Tab's
exact path, not merely visit the same elements in some order), and this
project's own Track 1 description commits to checking it. Repair: compare
`backward` (minus the wraparound duplicate of the seeding element) against
`forward` reversed, positionally, not just as sets.

I verified independently, with a fresh workspace and server for each run,
that this is not a rerun artifact: the raw JSON dump above came directly from
`node tests/helpers/entry_loop_keyboard_operability_client.mjs <url>` against
the unmodified build, with no defect injected.

### Not blocking, worth recording

**N1. The demonstration tests are genuine — verified independently.**

I reran both `break-reverse-traversal` and `swallow-activation` against fresh
server instances (not reusing the pytest run) and confirmed each fails for
the stated reason, not by crashing the harness:

- `break-reverse-traversal`: `incomplete` phase reports `matches: false` with
  `forwardOnly` naming both the wordmark link and the "Add W-2 Box 1" button
  (the wordmark assertion the test itself checks, plus one more the test
  doesn't inspect but which is consistent with trapping the "Enter this
  fact" button's Shift+Tab handler); the `complete` phase, which doesn't
  reach that trapped control before the trap's effect matters, still passes
  clean. Mouse-event count stayed zero throughout.
- `swallow-activation`: with a fresh runtime (my first attempt reused a
  server across two probe invocations and produced a misleading result where
  the "incomplete" phase showed post-completion controls — a flaw in my own
  test script, not the code under review), "Enter this fact" correctly shows
  `activatedWith: null` while every other control activates normally and
  `mouseEventsDispatched` stays zero.

**N2. Backward-traversal seeding is not a masking risk.** The probe seeds the
backward walk with `el.focus()` on `forward[forward.length - 1]` — but that
element was itself only added to `forward` after being reached by genuine
Tab traversal in the same run, so the programmatic focus call never
introduces an untested starting point.

**N3. Focus-only activation effects are the surface's genuine intended
behavior, not a loophole.** For "Enter this fact," "Correct this fact," and
"Review W-2 Box 1," the *only* fingerprint component that changes on
activation is `focusedKey` — moving focus to the target field is exactly
what Criteria 1.2 and 4.1 require these controls to do, so counting it as
the observed effect is correct here. The general risk the charter named (a
control could register as activated purely because focus shifted for
unrelated reasons) remains a theoretical limit of any effect-based
measurement, but N1's `swallow-activation` result shows the check does
correctly report `activatedWith: null` when a control's key press produces
no effect at all, which is the concrete failure mode the charter was
worried about.

**N4. `settle()` did not observably reintroduce the bleed it was added to
fix**, across every run I captured: "Add W-2 Box 1" and "Update W-2 Box 1"
both show the full settled post-submit fingerprint (status heading, accepted
flag, answered count) rather than a stale in-flight read.

## Measurements

### 1. Reverse traversal — FAIL (F1)

Set-membership check passes on the real surface and correctly fails when
backward reachability is broken (demonstrated, N1), but does not check order
as the milestone requires. See F1.

### 2. Activation by observed effect — PASS

Every actionable control (button, submit input, link routed separately)
activates with its standard key and is confirmed by a real fingerprint
change; the swallow-activation demonstration shows the check correctly fails
closed when a control silently eats its key. See N1, N3.

### 3. No mouse — PASS

`mouseEventsDispatched` was `0` in every run I captured, including both
demonstration-defect runs, via the `client.send` monkeypatch that counts
every `Input.dispatchMouseEvent` call — a real instrumented count, not a
value that is zero by construction.

### 4. Vacuous-pass guard — PASS

`test_reverse_traversal_matches_and_activation_bites_by_effect` asserts both
phases ran, at least 5 activation findings with `w2-box1` among them, and a
non-empty navigation list — the same shape `FocusIndicators` (Track 4) uses.
None of these are satisfiable by an empty findings list.

### 5. Scope discipline — PASS

`git diff --name-only 8d903f6 b261aae` shows exactly the two files the
charter names: the new probe client and its test file. No change to
`docs/phases/legible-entry/entry-usability-criteria.md`, no surface behavior
change — I diffed the criteria file across the range and it is empty.

### 6. Data safety and verification — PASS

- `python3 tools/envelope_scan.py --range main-ui..HEAD`: exit 0, no output.
- `python3 -m pytest -n auto`: 747 passed, 3322 subtests passed (116.65s).
- `python3 -m mypy`: no issues in 136 source files.
- `python3 tools/governance_lint.py`: conformant.
- `git diff --check main-ui..HEAD`: clean.

Per the build charter's noted governance gap, `verify` does not run as CI on
this branch; the above are my own local reruns, not a CI report, consistent
with the review charter's instruction to treat the build's self-report as
input and confirm independently.

## Remaining uncertainty

I did not attempt to construct an actual order-scrambling defect injection
(a keyboard handler that reassigns focus out of native tab sequence while
preserving the same reachable set) to prove F1 bites when repaired — that is
the repair builder's demonstration to produce, per the same "prove it bites"
discipline this track otherwise followed well. My finding rests on reading
the `matches` computation directly and on a concrete counterexample captured
from the unmodified surface's own raw output, not on a constructed failure.

No product code, fixture, criterion, or matrix entry was changed in this
review.
